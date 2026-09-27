"""Split conformal on full traces/sequences. N is exchangeable units, not seeds."""
from __future__ import annotations

import math

import numpy as np


def sequence_score(
    edge_scores: list[float],
    labels_known: bool,
    empty_truth: bool,
    nonconformity: str = "prob",
    truth_indices: list[int] | None = None,
) -> float | None:
    if not labels_known:
        return None
    if empty_truth:
        return 0.0
    if truth_indices is not None:
        edge_scores = [edge_scores[j] for j in truth_indices if 0 <= j < len(edge_scores)]
    if not edge_scores:
        return None
    if nonconformity == "one_minus_p":
        return float(max(1.0 - float(s) for s in edge_scores))
    return float(max(edge_scores))


def conformal_threshold(scores: list[float], alpha: float) -> dict:
    if not scores or alpha is None or not (0.0 <= alpha < 1.0):
        return {"q": None, "status": "invalid", "infinity": False}
    arr = np.sort(np.asarray(scores, dtype=float))
    n = len(arr)
    k = math.ceil((n + 1) * (1.0 - alpha))
    if k < 1:
        return {"q": None, "status": "invalid", "infinity": False, "k": k, "n": n}
    if k > n:
        return {"q": math.inf, "status": "infinity", "infinity": True, "k": k, "n": n}
    return {"q": float(arr[k - 1]), "status": "finite", "infinity": False, "k": k, "n": n}


def predict_set(p_hat: np.ndarray, q: float) -> np.ndarray:
    if math.isinf(q):
        return np.ones_like(p_hat, dtype=bool)
    return (1.0 - np.asarray(p_hat, dtype=float)) <= (float(q) + 1e-12)
