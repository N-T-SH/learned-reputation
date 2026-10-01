"""Action schema for a seat. T1-d crux is repair().

A later LLM emits text. This module is the only door into the env.
Broken text must not become a nomination or a contribution.
"""

from __future__ import annotations

MSG_CAP = 200


def empty_action() -> dict:
    return {"message": "", "nominate": [], "contribute": 0.0}


def repair(raw, n_seats: int) -> tuple[dict, bool]:
    """Return (action, ok).

    ok True only if raw was a usable action.
    On failure: empty message, empty nominate, contribute 0.0, ok False.

    Usable means:
    - raw is a dict with keys message, nominate, contribute (extra keys ignored)
    - message is a str; truncate to MSG_CAP
    - nominate is a list of ints in range(n_seats), duplicates dropped, order kept
    - contribute is int or float in [0, 1]
    """
    raise NotImplementedError("T1-d crux: fill repair")
