"""Low-rank bilinear task/behavior heads. Unknown labels are masked."""
from __future__ import annotations

import numpy as np


class BilinearProbe:
    def __init__(self, dim_h: int, dim_e: int, rank: int = 64, fn_weight: float = 10.0):
        if rank < 1:
            raise ValueError("rank must be positive")
        rng = np.random.default_rng(0)
        self.U = rng.normal(scale=0.05, size=(dim_h, rank))
        self.V = rng.normal(scale=0.05, size=(dim_e, rank))
        self.b = 0.0
        self.fn_weight = fn_weight
        self.dim_h = dim_h
        self.dim_e = dim_e
        self.rank = rank
        self.head_type = "unspecified"

    def score(self, h: np.ndarray, e: np.ndarray) -> np.ndarray:
        logits = (h @ self.U) * (e @ self.V)
        if logits.ndim == 1:
            logit = float(logits.sum() + self.b)
            return _sigmoid(np.array([logit]))[0]
        return _sigmoid(logits.sum(axis=-1) + self.b)

    def predict_matrix(self, H: np.ndarray, E: np.ndarray) -> np.ndarray:
        return _sigmoid((H @ self.U) @ (E @ self.V).T + self.b)

    def fit(
        self,
        H: np.ndarray,
        E: np.ndarray,
        Y: np.ndarray,
        mask: np.ndarray | None = None,
        steps: int = 200,
        lr: float = 0.1,
        split: str = "probe_train",
    ) -> dict:
        from ..splits import require_split

        require_split(split, ("probe_train",), "probe fit")
        known = np.ones_like(Y, dtype=bool) if mask is None else np.asarray(mask, dtype=bool)
        known &= np.isfinite(Y) & ((Y == 0) | (Y == 1))
        if H.ndim == 2:
            known &= np.isfinite(H).all(axis=1)[:, None]
        if E.ndim == 2:
            known &= np.isfinite(E).all(axis=1)[None, :]
        if not known.any():
            return {"loss": None, "status": "no_known_labels", "split": split, "rank": self.rank}
        H_fit = np.nan_to_num(H, nan=0.0)
        E_fit = np.nan_to_num(E, nan=0.0)
        for _ in range(steps):
            hu = H_fit @ self.U
            ev = E_fit @ self.V
            pred = _sigmoid(hu @ ev.T + self.b)
            weights = np.where(Y > 0.5, self.fn_weight, 1.0)
            err = np.where(known, weights * (pred - Y), 0.0)
            scale = 1.0 / max(int(known.sum()), 1)
            dlogits = err * scale
            self.U -= lr * (H_fit.T @ (dlogits @ ev))
            self.V -= lr * (E_fit.T @ (dlogits.T @ hu))
            self.b -= lr * float(dlogits.sum())
        pred = self.predict_matrix(H_fit, E_fit)
        return {
            "loss": weighted_bce(pred, Y, known.astype(float), self.fn_weight),
            "split": split,
            "rank": self.rank,
            "U": self.U.tolist(),
            "V": self.V.tolist(),
            "b": self.b,
            "fn_weight": self.fn_weight,
            "dim_h": self.dim_h,
            "dim_e": self.dim_e,
        }

    @classmethod
    def from_row(cls, row: dict) -> "BilinearProbe":
        probe = cls(int(row["dim_h"]), int(row["dim_e"]), rank=int(row["rank"]), fn_weight=float(row.get("fn_weight", 10)))
        probe.U = np.asarray(row["U"], dtype=float)
        probe.V = np.asarray(row["V"], dtype=float)
        probe.b = float(row["b"])
        probe.head_type = row.get("head", "unspecified")
        return probe


def _sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, -30, 30)
    return 1.0 / (1.0 + np.exp(-x))


def weighted_bce(pred: np.ndarray, target: np.ndarray, mask: np.ndarray, fn_weight: float = 10.0) -> float:
    pred = np.clip(pred, 1e-6, 1 - 1e-6)
    known = mask.astype(bool) & np.isfinite(target) & ((target == 0) | (target == 1))
    if not known.any():
        return float("nan")
    y = target[known]
    p = pred[known]
    weights = np.where(y > 0.5, fn_weight, 1.0)
    return float(np.mean(weights * (-y * np.log(p) - (1 - y) * np.log(1 - p))))
