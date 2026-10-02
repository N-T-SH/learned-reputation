# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN, run in progress.** Frozen loop is proven. A longer Qwen run is on Nitesh's machine: episode 0 of 10 finished, not yet pushed. Train pilot and gate note still open. Do not open T3. Pace note: `notes/for-plan-bot.md`.

## Locks (do not reopen)

1. Visibility: local. Last working-set contributions, plus messages to me from the previous round.
2. Groups: both must nominate each other. One-sided nominate is not a pair.
3. Units: y=1, scripted threshold 0.5, r=1.6, isolation 0.8.
4. This Qwen file stays N=4. Next frozen run, before any training, is N=8. Frozen and trained must use the same N.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.

## Exit criteria

- [x] FakeLM smoke
- [x] OpenRouter smoke: Ling, 4 seats x 5 rounds, all replies ok
- [x] Prompt checklist committed. Sample `ok True ok`.
- [x] Partner-choice vs fixed-group logged. Working sets did not differ (null contrast).
- [x] Reasoning toggle skipped as a study aim. Comparison model must still accept reasoning off.
- [ ] Longer frozen run logged (Qwen, 10x20, in progress)
- [ ] Training pilot, or a clear failure report
- [ ] `notes/t2-gate.md` from real logs
- [ ] Tracker marked FINISHED

## Instructions

Do not edit `notes/2month-plan.md`. Sync from this file and `notes/for-plan-bot.md`.

Lab loop from 2 Oct: implementation bot writes the code, explains it, and asks a check question. Do not leave functions empty.

## Log

| Block | Result |
|-------|--------|
| T2-a | FakeLM smoke green. |
| Router | `openrouter/free` returned `User Safety: safe`. Gemma free was upstream 429. |
| T2-b | Checklist committed. Sample `ok True ok`. |
| T2-c | Ling choice and fixed. Both kept all four seats. Seat 3 nominated nobody in fixed round 4 and stayed in. |
| T2-d | Skipped. Not a study aim. |
| Comparison model | `openai/gpt-oss-20b` rejected reasoning off: mandatory on that endpoint. Switched to `qwen/qwen3-8b` with `reasoning.enabled: false`. |
| Longer run | In progress locally. 4 seats, 20 rounds, 10 episodes, partner choice, reasoning off. Episode 0 done as of 2 Oct ~06:20 EDT. Not on GitHub yet. Drops and 429s are retried; a saved seat reply is not called again. |
| T2-e | Not started. No local GPU. OpenRouter cannot fine-tune. |

## Next

Let the Qwen file finish, then push the JSONL. Do not change N on this file. Next frozen run is N=8, same model, reasoning off, before any training. Then `notes/t2-gate.md`. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-02 ~06:25 EDT — Qwen longer run in progress, episode 0 done, not pushed. N=8 is the next frozen setting, before training. T2 not finished.
