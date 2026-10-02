# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** T2-a FakeLM smoke is green. OpenRouter client is wired (`eb61d22`) and not yet run. Default model is `openrouter/free` until we pin an id. No GRPO this tranche.

## Locks (do not reopen)

1. Visibility: local. Last working-set contributions, plus messages to me from the previous round.
2. Groups: both must nominate each other. One-sided nominate is not a pair.
3. Units: y=1, scripted threshold 0.5, r=1.6, isolation 0.8.
4. N=4 until a real-provider smoke is green.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.

## Exit criteria

- [x] FakeLM smoke
- [ ] OpenRouter smoke JSONL
- [ ] Prompt checklist committed
- [ ] Partner-choice on vs fixed-group
- [ ] Reasoning on/off, or a signed blocker
- [ ] Training pilot, or a clear failure report
- [ ] `notes/t2-gate.md` from real logs
- [ ] Tracker marked FINISHED

## Instructions

Do not edit `notes/2month-plan.md`.

T2-b: prompt states what a seat can do. It does not teach the game. Checklist fails on forbidden words.

T2-c: one run uses nominations. One run ignores them and uses a fixed working set.

T2-d: reasoning on/off if the provider can toggle it. Otherwise sign a blocker. Do not block the pilot on it.

T2-e: shared policy, reasoning off, about 200 episodes or fewer if the count is written down. Do not claim emergence.

Lab loop from 2 Oct: implementation bot writes the code, explains it, and asks a check question. Do not leave functions empty.

## Log

| Block | Result |
|-------|--------|
| T2-a | Green. FakeLM, 5 rounds, all ok. Not a model result. |
| T2-b | Chat printed `ok True` on 2 Oct. Confirm the function is committed. |
| OpenRouter | Client on main. Key stays in `.env`. Model not pinned. |
| T2-c..e | not started |

## Next

Add $10 at https://openrouter.ai/settings/credits. Key in `.env`. Then `SPEAKER=openrouter python -m envs.pgg_scripted.run_frozen`. Pin `OPENROUTER_MODEL` after one smoke answers.

---
**Signed:** ReputationLearning — 2026-10-01 opened T2.
**Signed:** Implementation bot — 2026-10-02 ~12:40 IST — OpenRouter speaker wired. FakeLM remains the default. Model unpinned. Restored block notes after a short overwrite.
