def episode_ids(n: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    ids = set()
    while len(ids) < n:
        ids.add("".join(rng.choice(ALPHABET) for _ in range(6)))
    ids = list(ids)
    rng.shuffle(ids)
    return ids


def episode_ids_stable(n: int, seed: int) -> list[str]:
    """Same draw as episode_ids, but sort before the shuffle so set order cannot move the roles."""
    rng = random.Random(seed)
    ids = set()
    while len(ids) < n:
        ids.add("".join(rng.choice(ALPHABET) for _ in range(6)))
    ids = sorted(ids)
    rng.shuffle(ids)
    return ids
