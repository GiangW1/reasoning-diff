#!/usr/bin/env python
"""Generate and validate official iGSM snapshots for the T1 experiment."""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path
from types import ModuleType

import numpy as np


REVISION = "a1ed1d04600add811beb08b58d9912ed30999642"
SOURCE_ROOT = Path("/mnt/mydata/igsm-source/facebookresearch-iGSM-a1ed1d0")


class _SkipTask(Exception):
    pass


class _DummyIds:
    def __getitem__(self, index):
        return self

    def tolist(self):
        return [1]


class _DummyTokenizer:
    def encode(self, *args, **kwargs):
        return _DummyIds()

    def decode(self, *args, **kwargs):
        return ""


def _install_offline_stubs() -> None:
    """The generator only needs tokenizer calls; avoid an unrelated GPT-2 download."""
    torch = ModuleType("torch")
    torch.__path__ = []
    torch.Tensor = object
    sys.modules["torch"] = torch
    for name in ("torch.nn", "torch.nn.functional", "torch.distributed"):
        module = ModuleType(name)
        module.__path__ = []
        sys.modules[name] = module
    transformers = ModuleType("transformers")
    transformers.GPT2Tokenizer = type(
        "GPT2Tokenizer",
        (),
        {"from_pretrained": classmethod(lambda cls, *args, **kwargs: _DummyTokenizer())},
    )
    sys.modules["transformers"] = transformers


def _param_id(param: tuple[int, int, int, int]) -> str:
    return "p_%d_%d_%d_%d" % param


def _expression(expression, root, sketches=None) -> tuple[str, list[tuple[int, int, int, int]]]:
    refs: list[tuple[int, int, int, int]] = []

    def visit(item, is_root: bool = False) -> str:
        param = getattr(item, "param", None)
        if param is not None and not (is_root and param == root):
            if param != root:
                referenced = sketches.get(param) if sketches is not None else None
                # iGSM can leave an unused cross-layer variable as an implicit zero.
                if referenced is not None and not getattr(referenced, "param_list", []) and not hasattr(referenced, "value"):
                    return "0"
                refs.append(param)
                return _param_id(param)
        children = getattr(item, "param_list", [])
        if not children:
            return str(item.value.a) if hasattr(item, "value") else "0"
        pieces = [visit(child) for child in children]
        if len(pieces) == 1:
            return pieces[0]
        operator = "-" if item.op == "diff" else "*" if item.op == "mul" else "+"
        return "(" + (f" {operator} ").join(pieces) + ")"

    return visit(expression, True), refs


def _snapshot(generator, native_id: str, seed: int, op: int) -> dict:
    problem = generator.problem
    target = problem.ques_idx
    closure: list[tuple[int, int, int, int]] = []

    def visit(param) -> None:
        if param in closure:
            return
        expression, refs = _expression(problem.sketch[param], param, problem.sketch)
        for ref in refs:
            visit(ref)
        closure.append(param)

    visit(target)
    question = ". ".join(problem.problem[:-1]) + ". " + problem.problem[-1]
    premise_nodes = []
    compute_nodes = []
    # Bind spans by the generator's statement order. Searching by text alone is
    # ambiguous when two parameters happen to receive the same sentence.
    param_spans = {}
    used_params = set()
    cursor = 0
    for statement in problem.problem[:-1]:
        start, end = cursor, cursor + len(statement)
        candidates = [
            param for param, text in problem.prob_dict.items()
            if text == statement and param not in used_params
        ]
        if not candidates:
            raise ValueError(f"problem statement has no parameter: {statement}")
        param_spans[candidates[0]] = (start, end)
        used_params.add(candidates[0])
        cursor = end + 2
    for param in closure:
        expression, refs = _expression(problem.sketch[param], param, problem.sketch)
        if refs:
            compute_nodes.append(
                {
                    "kind": "compute",
                    "param": _param_id(param),
                    "parents": [_param_id(ref) for ref in refs],
                    "aliases": [_param_id(param), problem.get_ntn(param)],
                    "expression": expression,
                    "value": int(problem.lookup[param].a),
                }
            )
            continue
        statement = problem.prob_dict.get(param)
        if not statement:
            raise ValueError(f"constant parameter {param} has no problem statement")
        if param not in param_spans:
            raise ValueError(f"problem statement not found for {param}: {statement}")
        start, end = param_spans[param]
        premise_nodes.append(
            {
                "kind": "premise",
                "param": _param_id(param),
                "literal": int(problem.lookup[param].a),
                "span": [start, end],
            }
        )

    # Scientific prepare edits a numeric premise. Some official graph closures
    # contain only implicit zero relations with no editable number; resample
    # those rare cases while preserving the requested operation balance.
    if not any(
        re.search(rf"(?<![\d.]){re.escape(str(node['literal']))}(?![\d.])", question[node["span"][0]:node["span"][1]])
        for node in premise_nodes
    ):
        raise _SkipTask("official closure has no editable numeric premise")

    nodes = [{"kind": "shared_rng", "id": [-1, 0, 0, 0]}] + premise_nodes + compute_nodes
    edges = []
    for node in compute_nodes:
        edges.extend([ [parent, node["param"]] for parent in node["parents"] ])
    return {
        "native_id": native_id,
        "family_id": native_id,
        "variant_id": "base",
        "revision": REVISION,
        "seed": seed,
        "mod": 23,
        "op": op,
        "n_op": int(problem.n_op),
        "answer": str(problem.ans),
        "target": _param_id(target),
        "question": question,
        "lookup": {
            _param_id(param): int(value.a)
            for param, value in problem.lookup.items()
            if isinstance(param, tuple)
        },
        "G": {"nodes": ["structure_only"], "edges": []},
        "template": {"nodes": nodes, "edges": edges},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--n", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260926)
    parser.add_argument("--ops", type=int, nargs="+", default=[5, 10, 15, 21])
    args = parser.parse_args()

    _install_offline_stubs()
    sys.path.insert(0, str(SOURCE_ROOT))
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from data_gen.pretrain.id_gen import IdGen
    from reasoning_diff.tasks.t1_official import load_igsm_snapshot

    args.out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"revision": REVISION, "seed": args.seed, "n": args.n, "ops": args.ops, "files": []}
    index = 0
    attempt = 0
    while index < args.n:
        seed = args.seed + attempt
        random.seed(seed)
        np.random.seed(seed)
        op = args.ops[index % len(args.ops)]
        generator = IdGen(max_op=21, max_edge=28, op=op, perm_level=5, detail_level=0)
        generator.gen_prob(list(range(23)), p_format="pq")
        native_id = f"igsm-official-{index:04d}-op{op}"
        try:
            payload = _snapshot(generator, native_id, seed, op)
        except _SkipTask:
            attempt += 1
            continue
        path = args.out_dir / f"{native_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        load_igsm_snapshot(path)
        manifest["files"].append(path.name)
        if (index + 1) % 25 == 0 or index == 0:
            print(f"validated {index + 1}/{args.n}", flush=True)
        index += 1
        attempt += 1
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
