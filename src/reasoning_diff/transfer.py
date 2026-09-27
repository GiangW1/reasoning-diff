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
        y = np.asarray(labels).reshape(-1)
        paired = np.stack([src[y == yi].mean(axis=0) if np.any(y == yi) else s_mean for yi in y])
        w, *_ = np.linalg.lstsq(a, paired - s_mean, rcond=None)
        status = "supervised_adapt"
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


def common_dim_then_procrustes(a: np.ndarray, b: np.ndarray) -> dict:
    from .analysis import procrustes

    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.ndim != 2 or b.ndim != 2:
        return {"common_dim": None, "truncated": True, "status": "not_applicable_shape_mismatch"}
    dim = min(int(a.shape[-1]), int(b.shape[-1]))
    n = min(int(a.shape[0]), int(b.shape[0]))
    if n < dim:
        return {
            "common_dim": dim,
            "a_map": "pca",
            "b_map": "pca",
            "truncated": True,
            "status": "not_applicable_too_few_rows",
        }
    ap, ma = _pca_project(a[:n], dim)
    bp, mb = _pca_project(b[:n], dim)
    return {"common_dim": dim, "a_map": ma, "b_map": mb, "truncated": False, **procrustes(ap, bp)}
