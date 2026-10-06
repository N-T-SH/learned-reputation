# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** High-contributor frozen control logged. Trained control not started. Do not open T3.

## Log

| Block | Result |
|-------|--------|
| Frozen measure | Seeds 11–13. Zero named 68/120, 28/120, 44/120. 0.3 named 42/120, 14/120, 42/120. |
| Trained measure | Seeds 14–16. Zero named 0/120, 0/120, 2/120. 0.3 named the same. Core group, not a ranking. |
| High control, frozen | `runs/train/control_high_frozen.jsonl`. Seeds 21–23. Five model seats. High seat named 82/100, 75/100, 80/100. Zero named 12, 10, 10. 0.3 named 5, 8, 10. High seat in the working set 18, 17, 19 of 20 rounds. One repair failure each. No steps. |

## Next

Run `python -m agents.train.control_high trained`. If the snapshot 404s, stop. Do not retrain. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-06 ~04:31 EDT — frozen control names the seat that contributes 1.
