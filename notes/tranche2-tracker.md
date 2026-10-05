# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Three frozen and three trained measurement episodes logged. One training episode. Do not open T3.

## Log

| Block | Result |
|-------|--------|
| Frozen measure | Seeds 11, 12, 13. Zero named 68/120, 28/120, 44/120. 0.3 named 42/120, 14/120, 42/120. Late zero named 24/30, 6/30, 4/30. |
| Trained measure | `runs/train/measure_trained.jsonl`. Seeds 14, 15, 16. No steps during measurement. Zero named 0/120, 0/120, 2/120. 0.3 named 0/120, 0/120, 2/120. Late rounds named neither probe in all three. Model named model 352/600, 193/600, 299/600. Mean contribution 0.94, 0.92, 0.81. |

## Next

The gap is outside the frozen range. It is one training episode. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-05 ~11:43 EDT — trained measurement almost never named either probe.
