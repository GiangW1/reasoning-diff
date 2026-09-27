"""Independent, replayable RNG streams. A single seed field is not enough."""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib

import numpy as np


def _seed_bytes(name: str, seed: int) -> int:
    digest = hashlib.sha256(f"{name}:{seed}".encode()).digest()
    return int.from_bytes(digest[:8], "big") % (2**31 - 1)


@dataclass
class Stream:
    name: str
    seed: int
    numpy_state: dict | None = None
    _rng: np.random.Generator = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = np.random.default_rng(_seed_bytes(self.name, self.seed))
        if self.numpy_state is not None:
            self._rng.bit_generator.state = self.numpy_state

    def integers(self, *args, **kwargs):
        return self._rng.integers(*args, **kwargs)

    def random(self, *args, **kwargs):
        return self._rng.random(*args, **kwargs)

    def snapshot(self) -> dict:
        return {"name": self.name, "seed": self.seed, "numpy_state": self._rng.bit_generator.state}

    @classmethod
    def restore(cls, payload: dict) -> Stream:
        return cls(payload["name"], payload["seed"], payload["numpy_state"])


class StreamBank:
    NAMES = ("sample", "direction", "perturb", "bootstrap", "split")

    def __init__(self, seed: int) -> None:
        self.streams = {name: Stream(name, seed) for name in self.NAMES}

    def get(self, name: str) -> Stream:
        if name not in self.streams:
            raise KeyError(f"unknown stream {name}; sample/direction/perturb/bootstrap are isolated")
        return self.streams[name]

    def snapshot(self) -> dict:
        return {name: stream.snapshot() for name, stream in self.streams.items()}
