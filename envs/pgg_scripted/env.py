"""Linear PGG + working set. No LLM.

A lone seat gets isolation. Contributing alone is not a profitable pot.
The ledger keeps the last five rounds of every seat's contribution and nominations.
"""

from __future__ import annotations

import random

Y = 1.0
R = 1.6
N = 4
ISOLATION = 0.8
LEDGER = 5


class ScriptedPGG:
    def __init__(self, n=N, r=R, y=Y, isolation=ISOLATION, seed=0, ledger=LEDGER):
        self.n = n
        self.r = r
        self.y = y
        self.isolation = isolation
        self.ledger_n = ledger
        self.rng = random.Random(seed)
        self.ids = list(range(n))
        self.working = set(self.ids)
        self.last_c = {i: None for i in self.ids}
        self.history: list[dict] = []
        self.t = 0

    def visible_c(self, i: int) -> dict[int, float | None]:
        return {j: self.last_c[j] for j in self.working}

    def record(self, contrib: dict[int, float], noms: dict[int, set[int]]) -> None:
        self.history.append(
            {
                "c": {i: contrib[i] for i in self.ids},
                "nom": {i: sorted(noms.get(i, set())) for i in self.ids},
            }
        )
        self.history = self.history[-self.ledger_n :]

    def payoffs(self, contrib: dict[int, float], working: set[int]) -> dict[int, float]:
        inn = [j for j in working]
        if len(inn) < 2:
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

    def form_groups(self, noms: dict[int, set[int]]) -> set[int]:
        """Bilateral form. A lone self-nomination does not open a pot."""
        nxt = set()
        for i in self.ids:
            for j in noms.get(i, set()):
                if i == j:
                    continue
                if i in noms.get(j, set()):
                    nxt.add(i)
                    nxt.add(j)
        return nxt
