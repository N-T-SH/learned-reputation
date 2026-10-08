"""Action schema for a seat. This module is the only door into the env.

allowed may be a seat count, or the ids for this episode.
A 6-character label is a valid id. A missing message, a null nominate, or a
numeric string can be recovered. A reply with no object still fails closed.
"""

from __future__ import annotations

MSG_CAP = 200


def empty_action() -> dict:
    return {"message": "", "nominate": [], "contribute": 0.0}


def allowed_ids(allowed) -> set:
    if isinstance(allowed, int):
        return set(range(allowed))
    return set(allowed)


def repair(raw, allowed) -> tuple[dict, bool]:
    """Return (action, ok). On failure: empty message, no nominations, contribution 0."""
    ids = allowed_ids(allowed)
    if not isinstance(raw, dict):
        return (empty_action(), False)
    message = raw.get("message", "")
    if message is None:
        message = ""
    if not isinstance(message, str):
        message = str(message)
    noms = raw.get("nominate")
    if noms is None or noms is False:
        noms = []
    elif isinstance(noms, str):
        noms = [part for part in noms.replace(",", " ").split() if part]
    elif not isinstance(noms, list) or not all(
        isinstance(x, (int, str)) and not isinstance(x, bool) for x in noms
    ):
        return (empty_action(), False)
    contrib = raw.get("contribute")
    if isinstance(contrib, str):
        try:
            contrib = float(contrib)
        except ValueError:
            return (empty_action(), False)
    if (
        not isinstance(contrib, (int, float))
        or isinstance(contrib, bool)
        or not (0 <= contrib <= 1)
    ):
        return (empty_action(), False)
    kept = []
    for x in noms:
        if x in ids and x not in kept:
            kept.append(x)
    return (
        {"message": message[:MSG_CAP], "nominate": kept, "contribute": float(contrib)},
        True,
    )
