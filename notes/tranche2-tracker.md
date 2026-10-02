# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Frozen Ling loop, checklist, and choice/fixed contrast are done. Reasoning toggle skipped. Train pilot and gate note still open. Pace note for the plan bot: `notes/for-plan-bot.md`. No GRPO this tranche.

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
- [x] Prompt checklist committed. Sample printed `ok True ok` in chat. Function is on main.
- [x] Partner-choice vs fixed-group logged. Working sets did not differ (null contrast).
- [x] Reasoning on/off skipped. Not a study aim. Signed 2 Oct.
- [ ] Training pilot, or a clear failure report
- [ ] `notes/t2-gate.md` from real logs
- [ ] Tracker marked FINISHED

## Instructions

Do not edit `notes/2month-plan.md`. Plan-bot handoff is `notes/for-plan-bot.md`.

T2-e: shared policy, reasoning off, about 200 episodes or fewer if the count is written down. Do not claim emergence. No local GPU. OpenRouter free cannot fine-tune. A written failure is acceptable.

Lab loop from 2 Oct: implementation bot writes the code, explains it, and asks a check question. Do not leave functions empty.

## Log

| Block | Result |
|-------|--------|
| T2-a | FakeLM smoke green. |
| OpenRouter | `openrouter/free` returned safety stubs. Pinned Ling. Gemma free was upstream 429. |
| T2-b | `analysis/prompt_check.py` committed. Sample `ok True ok`. |
| T2-c choice | Working stayed [0,1,2,3]. Everyone contributed 0.5. Pay 1.3. |
| T2-c fixed | Working stayed [0,1,2,3] even when seat 3 nominated nobody in round 4. Contributions moved from 0.5 to 0.6. |
| T2-d | Skipped. Nitesh: not the main aim. |
| T2-e | not started. Nothing scientific blocks it. Missing a trainer. |

## Next

Train pilot, or a written failure if there is no train path. Then `notes/t2-gate.md`. Do not open T3. Plan bot should sync from `notes/for-plan-bot.md`.

---
**Signed:** Implementation bot — 2026-10-02 ~15:00 IST — checklist confirmed. Pace proposal left for the plan bot. T2 still open on the train pilot and the gate note.
