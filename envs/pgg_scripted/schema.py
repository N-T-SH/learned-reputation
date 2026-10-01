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
    if not isinstance(raw, dict):
        return (empty_action(), False)
    if 'message' not in raw or not isinstance(raw['message'], str):
        return (empty_action(), False)
    if 'nominate' not in raw or not isinstance(raw['nominate'], list)\
        or not all(isinstance(x, int) for x in raw['nominate']):
        return (empty_action(), False)
    if 'contribute' not in raw\
        or not isinstance(raw['contribute'], (int, float))\
        or not (0 <= raw['contribute'] <= 1)\
        or isinstance(raw['contribute'], bool):
        return (empty_action(), False)
    raw['message'] = raw['message'][:MSG_CAP]
    raw['nominate'] = [x for x in raw['nominate'] if x in range(n_seats)] 
    raw['nominate'] = list(dict.fromkeys(raw['nominate']))
    raw['contribute'] = raw['contribute']
    return (raw, True)
