"""Write one repaired-bad action row. Does not rerun the T1-c controls."""

import json
from pathlib import Path

from envs.pgg_scripted.schema import repair

raw = "not an action"
action, ok = repair(raw, n_seats=4)
row = {
    "t": 0,
    "seat": 0,
    "raw_type": type(raw).__name__,
    "ok": ok,
    "action": action,
}
path = Path("runs/pgg/schema_bad.jsonl")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(row) + "\n")
print("wrote", path)
print(row)
