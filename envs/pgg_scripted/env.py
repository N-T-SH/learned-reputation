"""Linear PGG + working set. No LLM.

Ids are whatever the episode uses. A count still means 0..n-1.
A lone seat gets isolation. The ledger keeps five rounds.
"""

from __future__ import annotations

import random

Y = 1.0
R = 1.6
N = 4
ISOLATION = 0.8
LEDGER = 5


class ScriptedPGG:
    def __init__(self, n=N, ids=None, r=R, y=Y, isolation=ISOLATION, seed=0, ledger=LEDGER):
        self.r = r
        self.y = y
        self.isolation = isolation
        self.ledger_n = ledger
        self.rng = random.Random(seed)
        self.ids = list(ids) if ids is not None else list(range(n))
        self.n = len(self.ids)
        self.working = set(self.ids)
        self.last_c = {i: None for i in self.ids}
        self.history: list[dict] = []
        self.t = 0

    def visible_c(self, i) -> dict:
        return {j: self.last_c[j] for j in self.working}

    def record(self, contrib: dict, noms: dict) -> None:
        self.history.append(
            {
                "c": {i: contrib[i] for i in self.ids},
                "nom": {i: [j for j in noms.get(i, []) if j in self.ids] for i in self.ids},
            }
        )
        self.history = self.history[-self.ledger_n :]

    def payoffs(self, contrib: dict, working: set) -> dict:
        inn = [j for j in working if j in self.ids]
        if len(inn) < 2:
            return {i: self.isolation for i in self.ids}
        share = self.r * sum(contrib[j] for j in inn) / len(inn)
        return {
            i: ((self.y - contrib[i]) + share) if i in working else self.isolation
            for i in self.ids
        }

    def form_groups(self, noms: dict) -> set:
        nxt = set()
        for i in self.ids:
            for j in noms.get(i, ()):
                if i != j and i in noms.get(j, ()):
                    nxt.add(i)
                    nxt.add(j)
        return nxt
