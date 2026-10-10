"""2-layer ReLU MLP, hidden=256, for step-end boundary detection."""
from __future__ import annotations

import numpy as np


class BoundaryMLP:
    def __init__(self, dim: int, hidden: int = 256):
        if hidden != 256:
            raise ValueError("paper specifies Hidden=256")
        rng = np.random.default_rng(1)
        self.W1 = rng.normal(scale=0.05, size=(dim, hidden))
        self.b1 = np.zeros(hidden)
        self.W2 = rng.normal(scale=0.05, size=(hidden, 1))
        self.b2 = np.zeros(1)

    def logits(self, x: np.ndarray) -> np.ndarray:
        h = np.maximum(0.0, x @ self.W1 + self.b1)
        return (h @ self.W2 + self.b2).reshape(-1)

    def predict(self, x: np.ndarray) -> np.ndarray:
        z = self.logits(x)
        return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

    def fit(self, x: np.ndarray, y: np.ndarray, steps: int = 200, lr: float = 0.05) -> dict:
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        known = np.isfinite(y) & ((y == 0) | (y == 1))
        if not known.any():
            return {"loss": None, "status": "no_known_labels"}
        for _ in range(steps):
            pred = self.predict(x)
            err = np.where(known, pred - y, 0.0)
            hidden = np.maximum(0.0, x @ self.W1 + self.b1)
            dlogits = err[:, None] / max(int(known.sum()), 1)
            self.W2 -= lr * (hidden.T @ dlogits)
            self.b2 -= lr * dlogits.sum(axis=0)
            dhidden = (dlogits @ self.W2.T) * (hidden > 0)
            self.W1 -= lr * (x.T @ dhidden)
            self.b1 -= lr * dhidden.sum(axis=0)
        pred = self.predict(x)
        p = np.clip(pred[known], 1e-6, 1 - 1e-6)
        loss = float(np.mean(-(y[known] * np.log(p) + (1 - y[known]) * np.log(1 - p))))
        return {"loss": loss, "status": "ok", "hidden": 256}
