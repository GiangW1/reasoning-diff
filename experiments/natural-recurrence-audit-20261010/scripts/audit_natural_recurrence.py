"""Read-only source audit of saved generations; no model inference or network calls.

Flags retrieve passages only. They are NOT semantic annotations or prevalence
estimates. Character offsets refer to the exact saved serialized trace text.
"""
import argparse
import hashlib
import json
import re
import tarfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ART = ROOT / "artifacts"
PR9 = ART / "rd-pr9-single-pass-validation-20261010-light"


def jsonl(path):
    return [json.loads(line) for line in path.open() if line.strip()]


def load():
    result = []
    for code, name, inp in [("P", "pr9-pilot-20261009", "pr9-pilot-20261009"),
                            ("V", "pr9-validation-natural-20261010", "pr9-validation-20261010")]:
        folder = PR9 / "runs" / name
        cps = {r["id"]: r for r in jsonl(folder / "checkpoint_summary.jsonl")}
        tasks = {r["task_id"]: r for r in jsonl(PR9 / "inputs" / inp / "tasks.jsonl")}
        path = folder / "parser_recall_audit.jsonl"
        for i, r in enumerate(jsonl(path), 1):
            c = cps[r["trace_id"]]
            task = dict(tasks[c["base_group_id"]])
            task["question"] = r["text"].split("<|im_start|>user\n", 1)[-1].split("\n\nWork through", 1)[0]
            task["task_id"] = c["task_id"]
            result.append(dict(code=f"{code}{i:02}", source=str(path.relative_to(ROOT)),
                               source_line=i, task=task, meta=c, text=r["text"],
                               events=r["parsed_events"]))
    archive = ART / "rd-pr8-natural-pilot-20261007-light/raw-and-reparsed-pilot.tar.gz"
    with tarfile.open(archive) as tf:
        n = 0
        for gpu in (2, 3):
            base = f"pr8-natural-pilot-20261007-d02a40c/pilot-gpu{gpu}"
            tasks = {r["task_id"]: r for r in map(json.loads, tf.extractfile(base + "/tasks.jsonl"))}
            for i, r in enumerate(map(json.loads, tf.extractfile(base + "/traces.jsonl")), 1):
                n += 1
                result.append(dict(code=f"E{n:02}", source=str(archive.relative_to(ROOT)),
                                   archive_member=base + "/traces.jsonl", source_line=i,
                                   task=tasks[r["task_id"]], meta={k: r.get(k) for k in
                                   ("id", "task_id", "base_group_id", "seed", "status", "correct", "answer")},
                                   text=r["text"], events=r["events"]))
    return result


def paragraphs(r):
    return [(m.start(), m.end(), m.group()) for m in re.finditer(r"[^\n]+(?:\n(?!\n)[^\n]+)*", r["text"])]


def flags(r):
    events = [e for e in r["events"] if e.get("event_region") == "thinking"
              and e.get("status") == "ok" and e.get("event_phase") not in ("raw", "raw_arithmetic")]
    bynode = defaultdict(list)
    for e in events:
        if isinstance(e.get("correct"), bool):
            bynode[e["node_id"]].append(e)
    alternating = []
    for node, es in bynode.items():
        es.sort(key=lambda x: x["start"])
        compressed = []
        for e in es:
            if not compressed or compressed[-1]["correct"] != e["correct"]:
                compressed.append(e)
        if any(not e["correct"] for e in compressed):
            alternating.append(dict(node=node, sequence="".join("T" if e["correct"] else "F" for e in compressed),
                                    spans=[{k: e.get(k) for k in ("start", "end", "text", "value", "correct")} for e in compressed]))
    return alternating


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["inventory", "show", "flags", "search", "export"])
    ap.add_argument("codes", nargs="*", default=[])
    ap.add_argument("--pattern", default=r"misread|mistake|contradict|conflict|souvenir|instead|initially|wrong")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--end", type=int, default=10**9)
    args = ap.parse_args()
    rows = load()
    if args.codes:
        rows = [r for r in rows if r["code"] in args.codes]
    for r in rows:
        meta = r["meta"]
        if args.mode == "inventory":
            print(json.dumps(dict(code=r["code"], task=meta["task_id"], seed=meta["seed"],
                                  correct=meta["correct"], status=meta["status"], answer=meta["answer"],
                                  chars=len(r["text"]), flags=[(f["node"], f["sequence"]) for f in flags(r)])))
        elif args.mode == "flags":
            print(r["code"], meta["task_id"], json.dumps(flags(r), ensure_ascii=False))
        elif args.mode in ("show", "search"):
            print("\nTRACE", r["code"], meta["task_id"], "seed", meta["seed"], "gold", r["task"]["answer_spec"])
            for i, (start, end, para) in enumerate(paragraphs(r), 1):
                if end < args.start or start > args.end:
                    continue
                if args.mode == "show" or re.search(args.pattern, para, re.I):
                    print(f"[P{i:03} chars {start}:{end}] {para}")
        elif args.mode == "export":
            dest = Path(__file__).parent / "natural_recurrence_audit"
            dest.mkdir(exist_ok=True)
            item = {k: v for k, v in r.items() if k != "events"}
            item["text_sha256"] = hashlib.sha256(r["text"].encode()).hexdigest()
            item["flags_not_labels"] = flags(r)
            (dest / (r["code"] + ".json")).write_text(json.dumps(item, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
