# Oct 20 v2 tracker: instrument fix, then four episodes

**Repo:** `N-T-SH/learned-reputation`
**Pre-registration:** unchanged, `878692c` in `notes/prereg-2026-10-20.md`. Do not edit it.
**Status:** FINISHED. Report `notes/report-2026-10-20-v2.md`.
**Deadline:** report pushed by 00:30 IST on 21 Oct.
**Cap:** about $1 for this tracker. Stop if the running total for the 20 Oct round passes $8.

## Why there is a v2

The 20 Oct game files are scored correctly, and the audit found no role bug. They still cannot be read as partner choice, for two reasons.

1. The seat prompt never states the rules. `prompt_for` in `envs/pgg_scripted/run_frozen.py` says only "nominate partner ids, and set contribution". It does not say that a pair needs both names, that the pot is multiplied by 1.6, or that a seat in no pair gets 0.8. The design note has those rules. The model never saw them.
2. Without the rules, "nominate" is ambiguous. In `full_s0` and `full_s1` every model seat named the zero seat, with messages such as "Solidarity against the free rider" and "Cooperate fully. Nominate ex4i9b." The seats used the word to flag a seat, not to pick a partner. Contributions near 1.0 and five or six names per reply fit the same reading: with no stated cost, naming everyone and giving everything looks harmless.

There is also a pairing fault. `episode_ids` builds a `set` and then shuffles it. Set order depends on the process hash seed, so the same seed gave a different id order, and different role seats, in each arm. The 8 Oct seed-40 files are not affected, because they share a stored id list.

This is a logged instrument fix, not a rerun to change a result. Commit this tracker and the code change before any paid call.

## Steps

### V2-a: prompt, schema and ids (no paid calls)

Done. See Log.

### V2-b: four episodes (about $0.50)

Done. Parse gate passed. Four files in `runs/oct20/game/`.

### V2-c: report

Done. `notes/report-2026-10-20-v2.md`. Planning note updated.

## Log

### V2-b

Parse gate passed: `window_s0_v2` had 0 repair failures. A leftover line after the write raised `NameError`; the file was already written. That line was removed before the other three episodes.

Sanity line, rounds 1–8, not a gate. Window seed 0: steady 9, zero 15. Window seed 1: steady 1, zero 7. No change made because of it.

### V2-c

P1 failed. P3 failed. P4 failed. T1 failed. T2 reported. T3 not tested.

---
**Signed:** ReputationLearning, 2026-10-20 ~22:05 IST. Opened v2.
**Signed:** implementation bot, 2026-10-20. V2-a done.
**Signed:** Nitesh, 2026-10-20. Rules text accepted as written.
**Signed:** implementation bot, 2026-10-20. V2-b and V2-c done. Tracker finished.
