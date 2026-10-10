"""Walk official or derived snapshot directories without inventing graphs."""
from __future__ import annotations

from pathlib import Path

from .t1_official import load_igsm_snapshot
from .t2_gsm_plus import load_gsm_plus
from .t2_gsm_symbolic import load_gsm_symbolic
from .t3_hotpot import load_hotpot
from .t3_humaneval import load_humaneval
from .t3_musique import load_musique_records
from .t4_boundary import load_t4


LOADERS = {
    "igsm": load_igsm_snapshot,
    "t1_official": load_igsm_snapshot,
    "gsm_symbolic": load_gsm_symbolic,
    "t2_gsm_symbolic": load_gsm_symbolic,
    "symbolic": load_gsm_symbolic,
    "gsm_plus": load_gsm_plus,
    "t2_gsm_plus": load_gsm_plus,
    "hotpot": load_hotpot,
    "t3_hotpot": load_hotpot,
    "humaneval": load_humaneval,
    "t3_humaneval": load_humaneval,
}


def iter_snapshot_files(root: str | Path) -> list[Path]:
    root = Path(root)
    if root.is_file():
        return [root]
    return sorted(p for p in root.glob("**/*") if p.suffix == ".json")


def load_snapshot(kind: str, path: str | Path):
    path = Path(path)
    if kind in {"musique", "t3_musique"}:
        return load_musique_records(path)
    if kind in {"t4", "t4_boundary"}:
        return load_t4(path)
    if kind not in LOADERS:
        raise ValueError(f"unknown snapshot kind {kind}")
    return LOADERS[kind](path)
