"""Week 1 crux lives here."""

from __future__ import annotations

import random


def include_next(
    i: int,
    visible_c: dict[int, float | None],
    mode: str,
    rng: random.Random,
    threshold: float = 0.5,
) -> set[int]:
    """Return the set of seats i nominates for NEXT round's working set.

    mode == "positive": include j iff last visible c_j >= threshold.
      If c_j is None (no history), include (benefit of the doubt on first round).
    mode == "null": each other seat included independently with p=0.5; always
      include self (you can always volunteer).
    Never invent a reputation number.
    """
    raise NotImplementedError("Week 1 crux: fill include_next")
