# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01
**Closed:** 2026-10-06

## Status
**FINISHED as a pipeline tranche.** T3 is not open. The go/no-go sentence is still Nitesh + PI.

## What closed

The trainer runs on Fireworks. Log probabilities come back in-session. A group can be four complete episodes. A placebo step can be measured against a payoff step on the same ids. Spend is about $10 of a $40 cap.

## What did not close

A fresh process cannot reload a snapshot (404). The 20-round payoff file named the high seat 73/100 and the zero 1/100. The placebo file named the high seat 43/100 and the zero 3/100, with 41 repair failures against 18. That gap is not a result. One pair. No 0-versus-0.3 ranking. Messages were not tested.

## Do not

Do not open T3 from this mark. Do not replicate the earlier update that filled missing log probabilities with zeros.

---
**Signed:** Implementation bot — 2026-10-06 ~08:52 EDT — T2 closed as pipeline. T3 not open.
**Signed:** ReputationLearning — 2026-10-06 ~19:55 IST — Read the FINISHED mark. `notes/2month-plan.md` synced. `notes/tranche3-tracker.md` not created: waits on the Nitesh + PI go/no-go, per the mark above.
**Signed:** ReputationLearning — 2026-10-08 ~15:50 IST — Round closed 8 Oct; T3 NO-GO (Nitesh + PI); see `notes/project-report-2026-10-07.md` and `notes/2month-plan.md`.
