"""Summarize a frozen JSONL. No API calls."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def main() -> None:
    path = Path(sys.argv[1])
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not rows:
        print("empty", path)
        return
    ok = Counter(v for row in rows for v in row["ok"].values())
    sizes = Counter(len(row["working"]) for row in rows)
    left_out = Counter()
    contrib = []
    for row in rows:
        working = set(row["working"])
        for seat, action in row["action"].items():
            contrib.append(action["contribute"])
            if int(seat) not in working:
                left_out[int(seat)] += 1
    episodes = sorted({row["episode"] for row in rows})
    print("file", path.name)
    print("rows", len(rows), "episodes", len(episodes), "speaker", rows[0].get("speaker"))
    print("temperature", rows[0].get("temperature"), "seats", rows[0].get("seats"), "groups", rows[0].get("groups"))
    print("ok", dict(ok))
    print("working sizes", dict(sorted(sizes.items())))
    print("seat-rounds left out", dict(sorted(left_out.items())))
    print("contribute min/mean/max", min(contrib), round(sum(contrib) / len(contrib), 3), max(contrib))
    for ep in episodes:
        ep_rows = [row for row in rows if row["episode"] == ep]
        print(
            "episode",
            ep,
            "first",
            ep_rows[0]["working"],
            "last",
            ep_rows[-1]["working"],
        )


if __name__ == "__main__":
    main()
