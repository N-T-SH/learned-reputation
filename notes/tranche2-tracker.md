# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Frozen Ling loop and the choice/fixed contrast are logged. Reasoning toggle skipped by Nitesh on 2 Oct: not a study aim. Train pilot and gate note still open. No GRPO this tranche.

## Locks (do not reopen)

1. Visibility: local. Last working-set contributions, plus messages to me from the previous round.
2. Groups: both must nominate each other. One-sided nominate is not a pair.
3. Units: y=1, scripted threshold 0.5, r=1.6, isolation 0.8.
4. N=4 until a real-provider smoke is green.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.

## Exit criteria

- [x] FakeLM smoke
- [x] OpenRouter smoke: Ling, 4 seats x 5 rounds, all replies ok
- [ ] Prompt checklist committed
- [x] Partner-choice vs fixed-group logged. Working sets did not differ (null contrast).
- [x] Reasoning on/off skipped. Not a study aim. Signed 2 Oct.
- [ ] Training pilot, or a clear failure report
- [ ] `notes/t2-gate.md` from real logs
- [ ] Tracker marked FINISHED

## Instructions

Do not edit `notes/2month-plan.md`.

T2-e: shared policy, reasoning off, about 200 episodes or fewer if the count is written down. Do not claim emergence. No local GPU, so a hosted path or a written failure are both acceptable.

Lab loop from 2 Oct: implementation bot writes the code, explains it, and asks a check question. Do not leave functions empty.

## Log

| Block | Result |
|-------|--------|
| T2-a | FakeLM smoke green. |
| OpenRouter | `openrouter/free` returned safety stubs. Pinned Ling. Gemma free was upstream 429. |
| T2-c choice | Working stayed [0,1,2,3]. Everyone contributed 0.5. Pay 1.3. |
| T2-c fixed | Working stayed [0,1,2,3] even when seat 3 nominated nobody in round 4. Contributions moved from 0.5 to 0.6. |
| T2-d | Skipped. Nitesh: not the main aim. |
| T2-e | not started |

## Next

Train pilot, or a written failure if there is no train path. Then `notes/t2-gate.md` from these logs. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-02 ~14:55 IST — reasoning toggle skipped by Nitesh. T2 still open on the train pilot and the gate note.
