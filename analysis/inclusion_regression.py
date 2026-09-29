"""T1-c: P(i nominates j | last visible c_j). Not 'j in working'."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def rates(path: str) -> dict:
    rows = [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]
    if not rows:
        raise SystemExit(f"empty {path}")
    if "noms" not in rows[0]:
        raise SystemExit(f"{path} has no noms field — pull and re-run run_controls")

    tallies = Counter()
    parsed = []
    for rec in rows:
        parsed.append(
            {
                "working": set(rec["working"]),
                "contrib": {int(k): float(v) for k, v in rec["contrib"].items()},
                "noms": {int(k): set(v) for k, v in rec["noms"].items()},
            }
        )

    for t in range(1, len(parsed)):
        prev, cur = parsed[t - 1], parsed[t]
        for i in cur["working"]:
            for j in cur["working"]:
                if i == j:
                    continue
                c = prev["contrib"].get(j)
                if c is None:
                    continue
                high = c >= 0.5
                nominated = j in cur["noms"].get(i, set())
                tallies[(high, nominated)] += 1

    def p(high: bool):
        yes = tallies[(high, True)]
        no = tallies[(high, False)]
        n = yes + no
        return None if n == 0 else yes / n

    return {
        "n_high": tallies[(True, True)] + tallies[(True, False)],
        "n_low": tallies[(False, True)] + tallies[(False, False)],
        "p_nom_given_c_ge_0.5": p(True),
        "p_nom_given_c_lt_0.5": p(False),
    }


if __name__ == "__main__":
    for pth in ("runs/pgg/positive_seed0.jsonl", "runs/pgg/null_seed0.jsonl"):
        print(pth)
        for k, v in rates(pth).items():
            print(f"  {k}={v}")
