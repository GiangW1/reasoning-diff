"""P1–P3, Week-8 decisions, appendix geometry/cone/retrieval. No invented gates."""
from __future__ import annotations

from typing import Iterable

import numpy as np

FORBIDDEN_CLAIMS = (
    "already decided",
    "spurious dependencies are only a consequence",
    "joint-edit soundness",
)


def _auc(scores: np.ndarray, labels: np.ndarray) -> float | None:
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels, dtype=float)
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    if len(pos) == 0 or len(neg) == 0:
        return None
    greater = np.mean(pos[:, None] > neg[None, :])
    equal = np.mean(pos[:, None] == neg[None, :])
    return float(greater + 0.5 * equal)


def _fit_scores(x: np.ndarray, y: np.ndarray, train: np.ndarray) -> np.ndarray:
    design = np.c_[np.ones(len(y)), np.asarray(x, dtype=float)]
    xt = design[train]
    yt = np.asarray(y[train], dtype=float)
    w = np.zeros(design.shape[1])
    for _ in range(30):
        z = xt @ w
        p = 1.0 / (1.0 + np.exp(-np.clip(z, -20, 20)))
        weight = np.clip(p * (1.0 - p), 1e-5, None)
        target = z + (yt - p) / weight
        w, *_ = np.linalg.lstsq(xt * np.sqrt(weight)[:, None], target * np.sqrt(weight), rcond=None)
    return 1.0 / (1.0 + np.exp(-np.clip(design @ w, -20, 20)))


def p1_incremental(
    length: np.ndarray,
    op: np.ndarray,
    rho: np.ndarray,
    y: np.ndarray,
    held_out: np.ndarray | None = None,
    precomputed: bool = False,
    groups: list[str] | None = None,
    rng: np.random.Generator | None = None,
) -> dict:
    if len(np.unique(y)) < 2:
        return {"auc_base": None, "auc_full": None, "delta_auc": None, "status": "single_class", "held_out": False}
    if held_out is None and not precomputed:
        return {"auc_base": None, "auc_full": None, "delta_auc": None, "status": "requires_held_out", "held_out": False}
    if held_out is None:
        base_scores = np.asarray(length, dtype=float)
        full_scores = np.asarray(rho, dtype=float)
        eval_y = y
        held = False
    else:
        held_out = np.asarray(held_out, dtype=bool)
        if held_out.all() or not held_out.any():
            return {"auc_base": None, "auc_full": None, "delta_auc": None, "status": "held_out_empty", "held_out": True}
        train = ~held_out
        if groups is not None:
            if len(groups) != len(held_out):
                raise ValueError("p1 groups must cover every row")
            if any(item is None or str(item) == "" for item in groups):
                raise ValueError("p1 requires a problem identity for every row")
            train_groups = {g for g, flag in zip(groups, held_out, strict=True) if not flag}
            held_groups = {g for g, flag in zip(groups, held_out, strict=True) if flag}
            overlap = train_groups & held_groups
            if overlap:
                raise ValueError(f"p1 held-out groups overlap train: {sorted(overlap)[:5]}")
        base_scores = _fit_scores(np.c_[length, op], y, train)[held_out]
        full_scores = _fit_scores(np.c_[length, op, rho], y, train)[held_out]
        eval_y = y[held_out]
        held = True
    if len(np.unique(eval_y)) < 2:
        return {"auc_base": None, "auc_full": None, "delta_auc": None, "status": "single_class", "held_out": held}
    base = _auc(base_scores, eval_y)
    full = _auc(full_scores, eval_y)
    delta = None if base is None or full is None else full - base
    partial = _partial_corr(np.asarray(rho, dtype=float), np.asarray(y, dtype=float), np.c_[length, op])
    boot = None
    if groups is not None and delta is not None:
        boot = _bootstrap_p1(
            np.asarray(length, dtype=float),
            np.asarray(op, dtype=float),
            np.asarray(rho, dtype=float),
            np.asarray(y, dtype=float),
            None if held_out is None else np.asarray(held_out, dtype=bool),
            precomputed,
            list(groups),
            rng or np.random.default_rng(0),
        )
    elif rng is not None and delta is not None:
        boot = bootstrap_cluster(list(np.asarray(rho, dtype=float)), [str(i) for i in range(len(rho))], rng)
    return {
        "auc_base": base,
        "auc_full": full,
        "delta_auc": delta,
        "status": "estimate",
        "held_out": held,
        "estimator": "precomputed_scores" if held_out is None else "held_out_logistic",
        "partial_corr_rho_y_given_len_op": partial,
        "bootstrap": boot,
    }


def _partial_corr(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> float | None:
    if len(x) < 3:
        return None
    z = np.c_[np.ones(len(x)), np.asarray(z, dtype=float)]
    bx, *_ = np.linalg.lstsq(z, x, rcond=None)
    by, *_ = np.linalg.lstsq(z, y, rcond=None)
    rx = x - z @ bx
    ry = y - z @ by
    if np.std(rx) < 1e-12 or np.std(ry) < 1e-12:
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


def p2_paired(
    base_rho: float | None,
    noop_rho: float | None,
    base_acc: float | None,
    noop_acc: float | None,
    shared_denom: int | None,
    shared_premises: list[str] | None = None,
    injected_premises: list[str] | None = None,
    contamination_positions: list[int] | None = None,
) -> dict:
    if shared_premises is None and shared_denom is not None:
        return {
            "delta_rho": None,
            "delta_acc": None,
            "shared_denominator": shared_denom,
            "shared_premises": [],
            "injected_premises": list(injected_premises or []),
            "contamination_positions": list(contamination_positions or []),
            "status": "denominator_unverified",
            "note": "shared_denom without shared_premises is not a support set",
        }
    if shared_premises is not None:
        computed = len(shared_premises)
        if shared_denom is not None and shared_denom != computed:
            return {
                "delta_rho": None,
                "delta_acc": None,
                "shared_denominator": None,
                "shared_premises": list(shared_premises),
                "injected_premises": list(injected_premises or []),
                "contamination_positions": list(contamination_positions or []),
                "status": "denominator_inconsistent",
                "note": "shared_denom must equal |shared_premises|",
            }
        shared_denom = computed
    if None in (base_rho, noop_rho, base_acc, noop_acc, shared_denom):
        return {
            "delta_rho": None,
            "delta_acc": None,
            "shared_denominator": shared_denom,
            "shared_premises": list(shared_premises or []),
            "injected_premises": list(injected_premises or []),
            "contamination_positions": list(contamination_positions or []),
            "status": "missing_pair",
            "note": "new premises change rho_S denominator; report shared and injected separately",
        }
    return {
        "delta_rho": noop_rho - base_rho,
        "delta_acc": noop_acc - base_acc,
        "shared_denominator": shared_denom,
        "shared_premises": list(shared_premises or []),
        "injected_premises": list(injected_premises or []),
        "contamination_positions": list(contamination_positions or []),
        "status": "ok",
        "note": "new premises change rho_S denominator; report shared and injected separately",
    }


def p2_from_rows(rows: list[dict]) -> dict:
    if not rows:
        return {"status": "missing_pair", "n": 0, "delta_rho": None, "delta_acc": None, "per_item": []}
    items = [
        p2_paired(
            row.get("base_rho"),
            row.get("noop_rho"),
            row.get("base_acc"),
            row.get("noop_acc"),
            row.get("shared_denom"),
            shared_premises=row.get("shared_premises"),
            injected_premises=row.get("injected_premises"),
            contamination_positions=row.get("contamination_positions"),
        )
        for row in rows
    ]
    ok = [item for item in items if item.get("status") == "ok"]
    return {
        "n": len(rows),
        "delta_rho": float(np.mean([item["delta_rho"] for item in ok])) if ok else None,
        "delta_acc": float(np.mean([item["delta_acc"] for item in ok])) if ok else None,
        "per_item": items,
        "status": "ok" if ok else (items[0].get("status") if items else "missing_pair"),
    }


def p3_recovery(
    main_acc: float | None,
    crand_acc: float | None,
    clayer_acc: float | None,
    invalid_rate: float | None,
    nontarget: float | None = None,
    baseline_acc: float | None = None,
) -> dict:
    def _sub(left, right):
        if left is None or right is None:
            return None
        return left - right

    return {
        "vs_crand": _sub(main_acc, crand_acc),
        "vs_clayer": _sub(main_acc, clayer_acc),
        "vs_baseline": None if baseline_acc is None else _sub(main_acc, baseline_acc),
        "invalid_rate": invalid_rate,
        "nontarget": nontarget,
        "causal_reverse_claim": False,
        "restriction": "REST-02: undetected P3 does not imply spurious dependence is only a consequence",
    }


def p3_from_rows(rows: list[dict]) -> dict:
    if not rows:
        return {"status": "missing", "n": 0, "vs_crand": None, "vs_clayer": None, "per_item": []}
    items = [
        p3_recovery(
            row.get("main_acc"),
            row.get("crand_acc"),
            row.get("clayer_acc"),
            row.get("invalid_rate"),
            nontarget=row.get("nontarget"),
            baseline_acc=row.get("baseline_acc"),
        )
        for row in rows
    ]
    crand = [item["vs_crand"] for item in items if item["vs_crand"] is not None]
    clayer = [item["vs_clayer"] for item in items if item["vs_clayer"] is not None]
    return {
        "n": len(rows),
        "vs_crand": float(np.mean(crand)) if crand else None,
        "p3_vs_crand": float(np.mean(crand)) if crand else None,
        "vs_clayer": float(np.mean(clayer)) if clayer else None,
        "n_vs_crand": len(crand),
        "n_vs_clayer": len(clayer),
        "invalid_rate": None
        if any(item.get("invalid_rate") is None for item in items)
        else float(np.mean([item["invalid_rate"] for item in items])),
        "per_item": items,
        "status": "ok" if crand or clayer else "missing",
        "causal_reverse_claim": False,
    }


def _p1_delta_only(length, op, rho, y, held_out, precomputed) -> float | None:
    out = p1_incremental(length, op, rho, y, held_out=held_out, precomputed=precomputed, groups=None, rng=None)
    return out.get("delta_auc")


def _bootstrap_p1(length, op, rho, y, held_out, precomputed, groups, rng, n: int = 200) -> dict:
    unique = list(dict.fromkeys(groups))
    if not unique:
        return {"mean": None, "interval": None, "status": "no_groups"}
    grouped = {g: [i for i, gg in enumerate(groups) if gg == g] for g in unique}
    deltas = []
    for _ in range(n):
        draw = rng.choice(unique, size=len(unique), replace=True)
        idx = np.array([i for g in draw for i in grouped[g]], dtype=int)
        ho = None if held_out is None else held_out[idx]
        d = _p1_delta_only(length[idx], op[idx], rho[idx], y[idx], ho, precomputed)
        if d is not None:
            deltas.append(float(d))
    if not deltas:
        return {"mean": None, "interval": None, "status": "degenerate"}
    lo, hi = np.quantile(deltas, [0.025, 0.975])
    return {"mean": float(np.mean(deltas)), "interval": [float(lo), float(hi)], "n": len(deltas), "status": "resampled_delta_auc"}


def week8_decision(measurements: dict, gate_thresholds: dict | None = None) -> dict:
    gates = {}
    metric_key = {"gate0": "rho_S_excess", "gate1": "delta_auc", "gate2": "vs_crand"}
    for name in ("gate0", "gate1", "gate2"):
        thr = None if not gate_thresholds else gate_thresholds.get(name)
        metric = measurements.get(name) if measurements.get(name) is not None else measurements.get(metric_key[name])
        if thr is None:
            decision = "unregistered"
            side = None
        elif metric is None:
            decision = "threshold_present_measurement_missing"
            side = None
        else:
            side = "above" if float(metric) >= float(thr) else "below"
            decision = "compared"
        gates[name] = {
            "threshold": thr,
            "metric": metric,
            "side": side,
            "decision": decision,
        }
    text = str(measurements)
    leaked = [claim for claim in FORBIDDEN_CLAIMS if claim in text.lower()]
    excess = measurements.get("rho_S_excess")
    branch = measurements.get("status", "not_evaluated")
    if measurements.get("measurement_unresolved") or measurements.get("null_reason"):
        branch = "measurement_unresolved"
    elif excess is None and branch in {None, "not_evaluated"}:
        branch = "not_evaluated"
    elif excess == 0 or measurements.get("rho_S_significant") is False or measurements.get("c3_negative"):
        branch = "c3_negative_descriptive"
    elif measurements.get("p1_failed"):
        branch = "p1_appendix"
    elif measurements.get("evaluated"):
        branch = "evaluated"
    return {
        "gates": gates,
        "status": branch,
        "scientific_conclusion": None,
        "forbidden_claims_blocked": leaked,
        "restriction": ["REST-01", "REST-02", "REST-03"],
        "skip_p2_p3": branch in {"c3_negative_descriptive", "measurement_unresolved", "not_evaluated"},
    }


def cone_fit(x: np.ndarray, y: np.ndarray) -> dict:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.size < 2:
        return {"form": "1-exp{-lambda(1-x)^gamma}", "r2": None, "wording": "descriptive_only"}
    best = None
    for lam in np.logspace(-2, 2, 25):
        for gam in np.linspace(0.2, 4.0, 20):
            pred = 1.0 - np.exp(-lam * np.clip(1.0 - x, 0.0, None) ** gam)
            ss_res = float(np.sum((y - pred) ** 2))
            ss_tot = float(np.sum((y - np.mean(y)) ** 2))
            r2 = None if ss_tot <= 1e-12 else 1.0 - ss_res / ss_tot
            if best is None or ss_res < best[0]:
                best = (ss_res, r2, float(lam), float(gam))
    return {
        "form": "1-exp{-lambda(1-x)^gamma}",
        "r2": None if best is None else best[1],
        "lambda": None if best is None else best[2],
        "gamma": None if best is None else best[3],
        "wording": "descriptive_only",
    }


def procrustes(a: np.ndarray, b: np.ndarray) -> dict:
    if a.shape != b.shape:
        return {"status": "not_applicable_shape_mismatch"}
    ua, _, va = np.linalg.svd(a.T @ b)
    r = ua @ va
    return {"status": "adapted_geometry", "R": r}


def retrieval_scatter(
    pairs: Iterable[tuple[float, bool]] | None = None,
    embeddings_a: np.ndarray | None = None,
    embeddings_b: np.ndarray | None = None,
    answer_changed: Iterable[bool] | None = None,
    texts_a: Iterable[str] | None = None,
    texts_b: Iterable[str] | None = None,
) -> dict:
    embedding_kind = "provided"
    if texts_a is not None and texts_b is not None and embeddings_a is None:
        from .baselines import _bow

        embeddings_a = np.stack([_bow(t) for t in texts_a])
        embeddings_b = np.stack([_bow(t) for t in texts_b])
        embedding_kind = "bow_descriptive_not_paper_embed"
    if embeddings_a is not None and embeddings_b is not None:
        a = np.asarray(embeddings_a, dtype=float)
        b = np.asarray(embeddings_b, dtype=float)
        na = a / np.clip(np.linalg.norm(a, axis=-1, keepdims=True), 1e-8, None)
        nb = b / np.clip(np.linalg.norm(b, axis=-1, keepdims=True), 1e-8, None)
        xs = (na * nb).sum(axis=-1).tolist()
        ys = [int(v) for v in (answer_changed or [False] * len(xs))]
    else:
        items = list(pairs or [])
        xs = [p[0] for p in items]
        ys = [int(p[1]) for p in items]
    return {
        "n": len(xs),
        "mean_sim": float(np.mean(xs)) if xs else None,
        "answer_change_rate": float(np.mean(ys)) if ys else None,
        "embedding_kind": embedding_kind if embeddings_a is not None or texts_a is not None else "pairs",
        "status": "ok" if embedding_kind == "provided" or (texts_a is None and embeddings_a is None) else "embeddings_missing_bow_fallback",
    }


def bootstrap_cluster(values: list[float], groups: list[str], rng: np.random.Generator, n: int = 200) -> dict:
    unique = list(dict.fromkeys(groups))
    if not unique:
        return {"mean": None, "interval": None}
    means = []
    grouped = {g: [v for v, gg in zip(values, groups) if gg == g] for g in unique}
    for _ in range(n):
        draw = rng.choice(unique, size=len(unique), replace=True)
        sample = [x for g in draw for x in grouped[g]]
        means.append(float(np.mean(sample)))
    lo, hi = np.quantile(means, [0.025, 0.975])
    return {"mean": float(np.mean(values)), "interval": [float(lo), float(hi)]}
