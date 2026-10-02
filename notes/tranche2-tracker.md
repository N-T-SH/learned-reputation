# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`

## Status
**OPEN.** T2-a FakeLM smoke is green. OpenRouter client is wired (`eb61d22`) and not yet run. Default model is `openrouter/free` until we pin an id. No GRPO this tranche.

## Locks
Local visibility. Bilateral groups. y=1. Repair is the only door. No reputation wording in prompts. N=4 until a real smoke is green.

## Log

| Block | Result |
|-------|--------|
| T2-a | Green. FakeLM, 5 rounds, all ok. Not a model result. |
| T2-b | Checklist printed `ok True` in chat on 2 Oct. Confirm `prompt_is_ok` is committed. |
| OpenRouter | Client on main. Key in env, not in git. Model not pinned. |
| T2-c..e | not started |

## Next
Nitesh adds $10 at https://openrouter.ai/settings/credits, puts the key in `.env`, runs `SPEAKER=openrouter python -m envs.pgg_scripted.run_frozen`. Then pin `OPENROUTER_MODEL`. Do not open T3.

Lab loop from 2 Oct: implementation bot writes the code, explains it, and asks a check question. Do not leave functions empty.

---
**Signed:** ReputationLearning — 2026-10-01 opened T2; 15:20 IST ack close.
**Signed:** Implementation bot — 2026-10-02 ~12:40 IST — OpenRouter speaker wired; FakeLM remains default; model unpinned.
