"""Tiny linear PGG + working set. Week 1 scripted toy. No LLM."""

from __future__ import annotations

import random

Y = 1.0
R = 1.6
N = 4
ISOLATION = 0.8  # below typical contributor in the n=4 all-C example (1.6)


class ScriptedPGG:
    def __init__(self, n=N, r=R, y=Y, isolation=ISOLATION, seed=0):
        self.n = n
        self.r = r
        self.y = y
        self.isolation = isolation
        self.rng = random.Random(seed)
        self.ids = list(range(n))
        self.working = set(self.ids)  # start all in
        self.last_c = {i: None for i in self.ids}
        self.t = 0

    def visible_c(self, i: int) -> dict[int, float | None]:
        """Local: last working-set partners, including self if i was in."""
        return {j: self.last_c[j] for j in self.working}

    def payoffs(self, contrib: dict[int, float], working: set[int]) -> dict[int, float]:
        inn = [j for j in working]
        if not inn:
            return {i: self.isolation for i in self.ids}
        g = self.r * sum(contrib[j] for j in inn)
        share = g / len(inn)
        out = {}
        for i in self.ids:
            if i in working:
                out[i] = (self.y - contrib[i]) + share
            else:
                out[i] = self.isolation
        return out
