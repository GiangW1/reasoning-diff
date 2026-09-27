"""Fair text, attention/rollout, and four-tier verbalizer baselines."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

import numpy as np


@dataclass
class Visibility:
    prefix: str
    kind: str  # prospective | retrospective
    includes_reflection: bool = False


def _token_bucket(token: str, dim: int) -> int:
    digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") % dim


def _bow(text: str, dim: int = 32) -> np.ndarray:
    vec = np.zeros(dim)
    for token in text.lower().split():
        vec[_token_bucket(token, dim)] += 1.0
    norm = np.linalg.norm(vec)
    return vec / norm if norm else vec


def _pair_features(prefix: str, premise: str, dim: int = 32) -> np.ndarray:
    return np.concatenate([[1.0], _bow(f"{prefix} {premise}", dim=dim)])


def _logistic_weights(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    weights = np.zeros(x.shape[1])
    for _ in range(30):
        z = x @ weights
        pred = 1.0 / (1.0 + np.exp(-np.clip(z, -20, 20)))
        scale = np.clip(pred * (1.0 - pred), 1e-5, None)
        target = z + (y - pred) / scale
        weights, *_ = np.linalg.lstsq(x * np.sqrt(scale)[:, None], target * np.sqrt(scale), rcond=None)
    return weights


def fit_text_predictor(
    prefixes: list[str],
    labels: np.ndarray,
    split: str = "probe_train",
    premises: list[str] | None = None,
) -> dict:
    from .splits import require_split

    require_split(split, ("probe_train",), "text predictor")
    premises = premises if premises is not None else [""] * len(prefixes)
    x = np.stack([_pair_features(prefix, premise) for prefix, premise in zip(prefixes, premises, strict=True)])
    y = np.asarray(labels, dtype=float)
    known = np.isfinite(y) & ((y == 0) | (y == 1))
    if not known.any():
        raise ValueError("text predictor needs known labels")
    weights = _logistic_weights(x[known], y[known])
    return {"weights": weights, "split": split, "trained": True, "hash": "blake2b"}


def text_predictor(prefix: str, premise: str, weights: dict | None = None) -> float:
    if weights is None or not weights.get("trained"):
        raise ValueError("text predictor requires the same labeled split as the probe")
    feat = _pair_features(prefix, premise)
    w = np.asarray(weights["weights"], dtype=float)
    feat = feat[: len(w)]
    if len(feat) < len(w):
        feat = np.pad(feat, (0, len(w) - len(feat)))
    z = float(feat @ w)
    return float(1.0 / (1.0 + np.exp(-np.clip(z, -20, 20))))


def attention_mean(weights: np.ndarray, premise_idx: list[int]) -> float:
    if weights.size == 0 or not premise_idx:
        return 0.0
    return float(weights[..., premise_idx].mean())


def attention_rollout(layers: list[np.ndarray]) -> np.ndarray:
    eye = np.eye(layers[0].shape[-1])
    acc = eye
    for attn in layers:
        acc = (0.5 * attn + 0.5 * eye) @ acc
    return acc


def select_attention_heads(dev_scores: dict[int, float]) -> int:
    if not dev_scores:
        raise ValueError("attention head selection requires a dev curve")
    return max(dev_scores, key=dev_scores.get)


def fit_attention_threshold(scores: np.ndarray, labels: np.ndarray, split: str = "dev") -> dict:
    from .splits import require_split

    require_split(split, ("dev",), "attention threshold")
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels, dtype=float)
    known = np.isfinite(labels) & ((labels == 0) | (labels == 1))
    if not known.any():
        raise ValueError("attention threshold needs known dev labels")
    best = {"threshold": 0.0, "f1": None}
    for thr in np.unique(np.concatenate([[0.0], scores[known]])):
        pred = scores >= thr
        tp = float(((pred == 1) & (labels == 1) & known).sum())
        fp = float(((pred == 1) & (labels == 0) & known).sum())
        fn = float(((pred == 0) & (labels == 1) & known).sum())
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        if best["f1"] is None or f1 >= best["f1"]:
            best = {"threshold": float(thr), "f1": float(f1), "split": split}
    return best


def verbalizer(
    tier: str,
    prefix: str,
    gold: str | None,
    trained: bool,
    weights: dict | None = None,
    generate_fn=None,
    icl_examples: list[tuple[str, str]] | None = None,
) -> dict:
    if tier not in {"zeroshot", "fiveshot", "reflection", "supervised"}:
        raise ValueError(tier)
    visibility = "retrospective" if tier == "reflection" else "prospective"
    if tier == "supervised" and not trained:
        raise ValueError("supervised verbalizer requires the same labeled split as the probe")
    if tier == "supervised" and weights:
        return {"tier": tier, "score": text_predictor(prefix, gold or "", weights), "visibility": visibility, "status": "trained"}
    if generate_fn is None:
        return {"tier": tier, "score": None, "visibility": visibility, "status": "generate_unavailable"}
    shots = ""
    if tier == "fiveshot":
        for src, ans in (icl_examples or [])[:5]:
            shots += f"{src}\n{ans}\n"
    instruction = "reflect on the prefix then answer.\n" if tier == "reflection" else ""
    text = generate_fn(instruction + shots + prefix)
    from .events import extract_answer

    pred = extract_answer(str(text), "numeric")
    if pred is None:
        pred = extract_answer(str(text), "text")
    gold_n = extract_answer(str(gold), "numeric") if gold else None
    if gold_n is None:
        gold_n = str(gold).strip() if gold else None
    score = 1.0 if gold_n is not None and pred is not None and str(pred) == str(gold_n) else 0.0
    return {"tier": tier, "score": score, "visibility": visibility, "status": "generated", "text": str(text), "extracted": pred}
