# T1 tracker — scripted PGG pipeline
**Path:** `notes/tranche1-tracker.md`  
**Repo:** `N-T-SH/learned-reputation`  
**Pacing:** tranches, not calendar weeks.

## Status
**T1-a, T1-b, T1-c GREEN.** T1-d in progress (Thu 1 Oct).  
Schema smoke green. Dry tokens and bad-action JSONL still open.  
**N=6 skipped.** No LLM seats.

## Today’s Lab wedge (Thu 1 Oct)

- **Window:** 10:00–15:30 IST. Hard stop 15:30.
- **Main work:** T1-d schema + dry tokens.
- **Out:** LLM seats, N=16, GRPO, reopening locks.

## Locks

1. Visibility: **local**
2. Groups: **bilateral form / unilateral break**
3. Units: **y=1**, threshold **0.5**, r=1.6, isolation 0.8
4. N=4 gate. N=6 skipped.
5. Schema repair: drop duplicate and out-of-range ids; whole action fails on non-dict, bad types, or c outside [0, 1]. Failure is empty message, empty noms, c=0, ok=False.
6. Messages in the prompt are from the **previous** round.

## Log

| Block | Result |
|-------|--------|
| T1-a/b/c | Green (see rates below). |
| T1-d repair | Smoke: good `ok=True` nominate `[0, 1]` (dropped dup and id 9). Bad string → empty action, `ok=False`. |
| T1-d log + tokens | Not run yet. |

### T1-c rates (seed 0, N=4)

| file | n high / low c | P(nom \| c≥0.5) | P(nom \| c<0.5) |
|------|----------------|-----------------|-----------------|
| positive | 252 / 96 | **1.0** | **0.0** |
| null | 228 / 120 | 0.526 | 0.408 |

## Exit criteria

- [x] T1-a/b/c
- [x] `repair` smoke
- [ ] Bad action row in `runs/pgg/schema_bad.jsonl`
- [ ] Dry tokens/episode number
- [ ] N=6 — skipped

---
**Signed:** Implementation bot — 2026-10-01 ~10:40 IST — repair smoke green; illegal id dropped not whole-fail; commit local schema.py before pull.
