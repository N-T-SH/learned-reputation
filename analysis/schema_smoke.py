"""One good action and one bad action. Does not touch the T1-c JSONL."""

from envs.pgg_scripted.schema import repair

good = {"message": "hi", "nominate": [0, 1, 1, 9], "contribute": 1}
bad = "not an action"

for label, raw in (("good", good), ("bad", bad)):
    action, ok = repair(raw, n_seats=4)
    print(label, "ok=", ok, "action=", action)
