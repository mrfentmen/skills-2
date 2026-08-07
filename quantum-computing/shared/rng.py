"""
rng.py, shared seeded-randomness helper for themed skills.

Provides a small deterministic PRNG plus value noise, so generative skills
don't each reimplement `random` seeding and noise by hand. Copy next to your
code or reference from outputs.

Usage:
    from rng import RNG
    r = RNG(42)          # seeded -> reproducible output
    r.uniform(), r.gauss(), r.choice([...]), r.value_noise(x, y)
"""
from __future__ import annotations

import math
from typing import Any, List, Sequence

NOISE_SALT = 123456789  # fixed lattice-hash salt keeps noise deterministic


class RNG:
    """Deterministic LCG-based PRNG with common distributions."""

    def __init__(self, seed: int = 0x5EED):
        self.state = seed & 0xFFFFFFFF or 1

    def next_u32(self) -> int:
        # Numerical Recipes LCG
        self.state = (self.state * 1664525 + 1013904223) & 0xFFFFFFFF
        return self.state

    def uniform(self, lo: float = 0.0, hi: float = 1.0) -> float:
        return lo + (self.next_u32() / 0xFFFFFFFF) * (hi - lo)

    def gauss(self, mean: float = 0.0, sigma: float = 1.0) -> float:
        # Box-Muller
        u1 = max(self.uniform(), 1e-9)
        u2 = self.uniform()
        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        return mean + z * sigma

    def choice(self, items: Sequence[Any]) -> Any:
        return items[self.next_u32() % len(items)]

    def shuffle(self, items: List[Any]) -> List[Any]:
        out = list(items)
        for i in range(len(out) - 1, 0, -1):
            j = self.next_u32() % (i + 1)
            out[i], out[j] = out[j], out[i]
        return out

    def value_noise(self, x: float, y: float, scale: float = 1.0) -> float:
        """Smooth bilinear value noise in [0, 1] from lattice hashes."""
        xi, yi = int(x * scale), int(y * scale)
        fx, fy = x * scale - xi, y * scale - yi

        def _hash(ix: int, iy: int) -> float:
            n = ix * 374761393 + iy * 668265263 + NOISE_SALT
            n = (n ^ (n >> 13)) * 1274126177
            return ((n ^ (n >> 16)) & 0xFFFFFFFF) / 0xFFFFFFFF

        sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
        a = _hash(xi, yi)
        b = _hash(xi + 1, yi)
        c = _hash(xi, yi + 1)
        d = _hash(xi + 1, yi + 1)
        return (a + (b - a) * sx) * (1 - sy) + (c + (d - c) * sx) * sy
