# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** High-contributor control done on both sides. Trained policy names the seat that contributes 1. It does not rank 0 below 0.3. Do not open T3 until the go/no-go is written.

## Log

| Block | Result |
|-------|--------|
| Frozen measure | Seeds 11–13. Zero named 68/120, 28/120, 44/120. |
| Trained measure | Seeds 14–16. Zero named 0/120, 0/120, 2/120. Core group on that file. |
| High control, frozen | Seeds 21–23. High seat named 82/100, 75/100, 80/100. Zero 12, 10, 10. 0.3 named 5, 8, 10. |
| High control, trained | `runs/train/control_high_trained.jsonl`. Seeds 24–26. Saved snapshot, no further steps. High seat named 86/100, 77/100, 85/100. Zero named 2, 8, 3. 0.3 named 0, 10, 3. High seat in the working set 18, 17, 18 of 20. |

## Next

The control says exclusion can track a visible 1 against a visible 0. It does not say 0 is ranked below 0.3. Go/no-go is Nitesh + PI. Do not open T3 from this file alone.

---
**Signed:** Implementation bot — 2026-10-06 ~04:52 EDT — trained control names the high seat.
