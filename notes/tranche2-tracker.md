# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Qwen 3.8 27B frozen file is on `main` and is the better before picture. Exclusion happened. It still did not track a low contribution. Gate note and train decision still open. Do not open T3.

## Locks (do not reopen)

1. Visibility: local. Last working-set contributions, plus messages to me from the previous round.
2. Groups: both must nominate each other. One-sided nominate is not a pair.
3. Units: y=1, scripted threshold 0.5, r=1.6, isolation 0.8.
4. If the pilot is on Qwen 3.8 27B, the frozen file is `runs/pgg/frozen_qwen_qwen3.8-27b_choice_s8_t0.4_seed0_n5.jsonl`. The 8B file is a separate baseline, not the before picture for that pilot.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.

## Exit criteria

- [x] FakeLM smoke
- [x] OpenRouter smoke: Ling, 4 seats x 5 rounds, all replies ok
- [x] Prompt checklist committed. Sample `ok True ok`.
- [x] Partner-choice vs fixed-group logged. Ling working sets did not differ.
- [x] Reasoning toggle skipped as a study aim. Comparison model must still accept reasoning off.
- [x] Longer frozen run logged. `runs/pgg/frozen_qwen_qwen3-8b_choice_seed0_n10.jsonl`
- [x] N=8, temperature 0.4, 5 episodes, Qwen3 8B.
- [x] N=8, temperature 0.4, 5 episodes, Qwen 3.8 27B. Smoke replies were short JSON.
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
| T2-c | Ling choice and fixed. Both kept all four seats. |
| T2-d | Skipped. Not a study aim. |
| Comparison model | GPT-OSS rejected reasoning off. Qwen3 8B and Qwen 3.8 27B both returned short JSON with reasoning off. |
| N=4, temperature 0 | 800 replies, all ok. Seat 3 out after round 1 in every episode. Episodes were copies. |
| N=8, Qwen3 8B, temperature 0.4 | 800 replies, all ok. Working size mostly 4. 376 seat-rounds left out. Contributions 0.5 to 0.8. Three episodes ended on the same four seats. |
| N=8, Qwen 3.8 27B, temperature 0.4 | 100 rows, 800 replies, all ok. Working size spread from 1 to 8, most often 3. 388 seat-rounds left out. Seat 7 out most often. Contributions 0.5 to 1.0, mean 0.754. None below 0.5. In-group mean contribution 0.775, out 0.731. Pay in 1.465, out 0.8. 27 distinct working sets. Episodes did not copy each other. No timer fields: this process started before that commit. Not a training result. |
| T2-e | Not started. Fireworks serverless can do a GRPO-style LoRA on a listed model, not on the 8B id. |

## Next

Write `notes/t2-gate.md` from the 27B file. Then the train-or-not call. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-03 ~04:20 EDT — 27B frozen file finished. Better before picture, still no low-contribution exclusion. T2 not finished.
**Signed:** ReputationLearning — 2026-10-02 ~15:58 IST — one-line pointer: 2month-plan speed-run synced; no exit-criteria edits.
**Signed:** ReputationLearning — 2026-10-02 ~16:01 IST — pointer only: go/no-go + optional <$25 pilot after N=4 finish + N=8 frozen.
