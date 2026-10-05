# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Three frozen measurement episodes logged. Trained measurement not started. The last adapter was not saved. Do not open T3.

## Log

| Block | Result |
|-------|--------|
| Frozen measure | `runs/train/measure_frozen.jsonl`. Seeds 11, 12, 13. Probes fixed inside each episode. Seed 11 named zero 68/120 and 0.3 42/120. Seed 12 named zero 28/120 and 0.3 14/120. Seed 13 named zero 44/120 and 0.3 42/120. Late rounds named the zero 24/30, 6/30, and 4/30. Repair failures 1, 0, 1. No optimizer step. |

## Next

The frozen side varies by episode. A trained comparison needs a saved adapter and three episodes with no further steps. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-05 ~10:33 EDT — three frozen episodes, rates not stable.
