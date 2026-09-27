"""Prospective swap, INLP ablation, rescue, and matched C-rand/C-layer controls."""
from __future__ import annotations

import numpy as np

from .schema import finite_or_none


def project_delta(base: np.ndarray, donor: np.ndarray, basis: np.ndarray) -> np.ndarray:
    # Π_Z (h_d - h_b); basis columns are orthonormal
    delta = donor - base
    return basis @ (basis.T @ delta)


def apply_swap(base: np.ndarray, donor: np.ndarray, basis: np.ndarray) -> np.ndarray:
    return base + project_delta(base, donor, basis)


def orthonormal_basis(dim: int, rank: int, rng: np.random.Generator) -> np.ndarray:
    q, _ = np.linalg.qr(rng.normal(size=(dim, rank)))
    return q[:, :rank]


def scale_to_norm(delta: np.ndarray, target_norm: float):
    n = float(np.linalg.norm(delta))
    if n == 0.0:
        return delta, "zero_norm"
    return delta * (target_norm / n), "ok"


def c_rand_delta(
    base: np.ndarray,
    donor: np.ndarray,
    rank: int,
    rng: np.random.Generator,
    target_norm: float | None = None,
) -> dict:
    if target_norm is None:
        raise ValueError("C-rand requires the actual main-intervention norm")
    basis = orthonormal_basis(base.shape[-1], rank, rng)
    delta = project_delta(base, donor, basis)
    scaled, status = scale_to_norm(delta, float(target_norm))
    return {"delta": scaled, "basis": basis, "status": status, "actual_norm": float(np.linalg.norm(scaled))}


def c_layer_delta(base: np.ndarray, donor: np.ndarray, layer_basis: np.ndarray, target_norm: float) -> dict:
    delta = project_delta(base, donor, layer_basis)
    scaled, status = scale_to_norm(delta, float(target_norm))
    return {"delta": scaled, "basis": layer_basis, "status": status, "actual_norm": float(np.linalg.norm(scaled))}


def inlp_remove(H: np.ndarray, labels: np.ndarray, steps: int = 8) -> np.ndarray:
    """Iterative nullspace projection on the already-projected representation."""
    dim = H.shape[1]
    p = np.eye(dim)
    work = np.array(H, dtype=float, copy=True)
    y = labels * 2 - 1
    for _ in range(steps):
        w, *_ = np.linalg.lstsq(work, y, rcond=None)
        n = np.linalg.norm(w)
        if n < 1e-8:
            break
        u = w / n
        step = np.eye(dim) - np.outer(u, u)
        work = work @ step
        p = p @ step
    return p


def rescue(ablated: np.ndarray, component: np.ndarray) -> np.ndarray:
    return ablated + component


def rescue_controls(ablated: np.ndarray, matched: np.ndarray, error_source: np.ndarray, rng: np.random.Generator) -> dict:
    target = float(np.linalg.norm(matched))
    noise = rng.normal(size=matched.shape)
    n = float(np.linalg.norm(noise))
    random = noise * (target / n) if n else noise
    return {
        "matched": rescue(ablated, matched),
        "error_source": rescue(ablated, error_source),
        "random": rescue(ablated, random),
        "matched_norm": target,
        "random_norm": float(np.linalg.norm(random)),
    }


def ie_z(g_intervened: np.ndarray, g_base: np.ndarray) -> float:
    return float(np.mean(np.asarray(g_intervened, dtype=float)) - np.mean(np.asarray(g_base, dtype=float)))


def select_weak_layer(dev_scores: dict[int, float]) -> int:
    if not dev_scores:
        raise ValueError("C-layer requires a dev-split layer curve")
    return min(dev_scores, key=dev_scores.get)


def intervention_report(main: dict, crand: dict, clayer: dict) -> dict:
    def rel(key):
        if key not in main or key not in crand or key not in clayer:
            return None
        if main[key] is None or crand[key] is None or clayer[key] is None:
            return None
        return {
            "vs_crand": finite_or_none(main[key] - crand[key]),
            "vs_clayer": finite_or_none(main[key] - clayer[key]),
        }

    return {
        "target": rel("target"),
        "nontarget": rel("nontarget"),
        "task_correct": rel("task_correct"),
        "invalid": rel("invalid"),
        "acknowledged_effect": "relative_to_controls_only",
    }
