"""Cross-model transfer. Direct mode refuses dimension mismatch; no pad/truncate."""
from __future__ import annotations

import numpy as np

from .splits import require_split


def direct_transfer(source_dim: int, target_dim: int) -> dict:
    if source_dim != target_dim:
        return {
            "status": "not_applicable_dimension_mismatch",
            "source_dim": source_dim,
            "target_dim": target_dim,
        }
    return {"status": "applicable", "source_dim": source_dim, "target_dim": target_dim}


def fit_linear_map(src: np.ndarray, tgt: np.ndarray, split: str, labeled: bool, labels: np.ndarray | None = None) -> dict:
    require_split(split, ("transfer_pairs",), "transfer mapping")
    src = np.asarray(src, dtype=float)
    tgt = np.asarray(tgt, dtype=float)
    if src.ndim != 2 or tgt.ndim != 2 or not np.isfinite(src).all() or not np.isfinite(tgt).all():
        raise ValueError("transfer mapping requires finite two-dimensional arrays")
    if src.shape[0] != tgt.shape[0]:
        raise ValueError("paired rows required")
    if labeled and labels is None:
        raise ValueError("supervised adapt requires a label tensor")
    if labeled:
        labels = np.asarray(labels).reshape(-1)
        if labels.shape[0] != src.shape[0] or not np.isfinite(labels).all():
            raise ValueError("supervised adapt labels must match paired rows and be finite")
        if np.unique(labels).size < 2:
            raise ValueError("supervised adapt requires at least two label classes")
    t_mean = tgt.mean(axis=0)
    s_mean = src.mean(axis=0)
    a = tgt - t_mean
    b = src - s_mean
    if labeled:
        # Labels are retained for held-out stratification; do not collapse
        # every row to a class mean, which destroys within-class geometry.
        class_weight = np.where(labels > np.median(labels), 2.0, 1.0)
        weighted_b = b * np.sqrt(class_weight)[:, None]
        weighted_a = a * np.sqrt(class_weight)[:, None]
        gram = weighted_a.T @ weighted_a
        label_corr = np.asarray([
            np.corrcoef(a[:, column], labels)[0, 1] if np.std(a[:, column]) > 1e-12 and np.std(labels) > 1e-12 else 0.0
            for column in range(a.shape[1])
        ])
        regularizer = np.diag(1e-3 * (1.0 + np.nan_to_num(np.abs(label_corr))))
        w = np.linalg.solve(gram + regularizer, weighted_a.T @ weighted_b)
        status = "supervised_linear_adapt"
    else:
        if tgt.shape[1] == src.shape[1]:
            ua, _, va = np.linalg.svd(a.T @ b, full_matrices=False)
            w = ua @ va
        else:
            w, *_ = np.linalg.lstsq(a, b, rcond=None)
        status = "unlabeled_pair_adapt"
    return {
        "status": status,
        "W": w,
        "target_mean": t_mean,
        "source_mean": s_mean,
        "in_dim": tgt.shape[1],
        "out_dim": src.shape[1] if labeled or tgt.shape[1] == src.shape[1] else w.shape[1],
        "split": split,
        "uses_labels": labeled,
    }


def apply_map(vectors: np.ndarray, fitted: dict) -> np.ndarray:
    weights = np.asarray(fitted["W"], dtype=float)
    target_mean = np.asarray(fitted.get("target_mean", np.zeros(weights.shape[0])), dtype=float)
    source_mean = np.asarray(fitted.get("source_mean", np.zeros(weights.shape[1])), dtype=float)
    return (np.asarray(vectors, dtype=float) - target_mean) @ weights + source_mean


def apply_bilinear_inputs(H: np.ndarray, E: np.ndarray, h_map: dict, e_map: dict) -> tuple[np.ndarray, np.ndarray]:
    return apply_map(H, h_map), apply_map(E, e_map)


def _pca_project(x: np.ndarray, dim: int) -> tuple[np.ndarray, str]:
    x = np.asarray(x, dtype=float)
    if x.shape[-1] == dim:
        return x, "identity"
    x0 = x - x.mean(axis=0, keepdims=True)
    _, _, vt = np.linalg.svd(x0, full_matrices=False)
    w = vt[:dim].T
    return x0 @ w, "pca"


def common_dim_then_procrustes(
    a: np.ndarray,
    b: np.ndarray,
    pair_ids_a: list[str] | None = None,
    pair_ids_b: list[str] | None = None,
) -> dict:
    from .analysis import procrustes

    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.ndim != 2 or b.ndim != 2:
        return {"common_dim": None, "truncated": True, "status": "not_applicable_shape_mismatch"}
    if pair_ids_a is not None or pair_ids_b is not None:
        if pair_ids_a is None or pair_ids_b is None:
            return {
                "common_dim": min(int(a.shape[-1]), int(b.shape[-1])),
                "truncated": False,
                "a_map": "pca",
                "b_map": "pca",
                "status": "not_applicable_missing_pair_ids",
                "discarded_ids": None,
            }
        if len(pair_ids_a) != a.shape[0] or len(pair_ids_b) != b.shape[0]:
            return {
                "common_dim": None,
                "truncated": False,
                "status": "not_applicable_pair_id_count_mismatch",
                "discarded_ids": None,
            }
        left = {str(value): i for i, value in enumerate(pair_ids_a)}
        right = {str(value): i for i, value in enumerate(pair_ids_b)}
        common = sorted(set(left) & set(right))
        if not common:
            return {"common_dim": None, "truncated": True, "status": "not_applicable_no_pair_ids", "discarded_ids": {"source": list(left), "target": list(right)}}
        discarded = {"source": sorted(set(left) - set(common)), "target": sorted(set(right) - set(common))}
        a = a[[left[key] for key in common]]
        b = b[[right[key] for key in common]]
    else:
        if a.shape[0] != b.shape[0]:
            return {
                "common_dim": min(int(a.shape[-1]), int(b.shape[-1])),
                "truncated": False,
                "a_map": "pca",
                "b_map": "pca",
                "status": "not_applicable_pair_mismatch",
                "discarded_ids": None,
            }
        common = [str(i) for i in range(a.shape[0])]
        discarded = {"source": [], "target": []}
    dim = min(int(a.shape[-1]), int(b.shape[-1]))
    n = a.shape[0]
    if n < dim:
        return {
            "common_dim": dim,
            "a_map": "pca",
            "b_map": "pca",
            "truncated": True,
            "status": "not_applicable_too_few_rows",
        }
    ap, ma = _pca_project(a, dim)
    bp, mb = _pca_project(b, dim)
    return {
        "common_dim": dim,
        "a_map": ma,
        "b_map": mb,
        "truncated": bool(discarded["source"] or discarded["target"]),
        "pair_count": n,
        "pair_ids": common,
        "discarded_ids": discarded,
        **procrustes(ap, bp),
    }
