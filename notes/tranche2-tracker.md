# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** N=8 temperature-0.4 frozen run is on `main`. Exclusion happened. It did not track contribution, because nobody contributed below 0.5. Gate note and train decision still open. Do not open T3.

## Locks (do not reopen)

1. Visibility: local. Last working-set contributions, plus messages to me from the previous round.
2. Groups: both must nominate each other. One-sided nominate is not a pair.
3. Units: y=1, scripted threshold 0.5, r=1.6, isolation 0.8.
4. Frozen comparison setting is N=8, temperature 0.4, `qwen/qwen3-8b`, reasoning off. A later trained run must match that, or be a different model with its own frozen file.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.

## Exit criteria

- [x] FakeLM smoke
- [x] OpenRouter smoke: Ling, 4 seats x 5 rounds, all replies ok
- [x] Prompt checklist committed. Sample `ok True ok`.
- [x] Partner-choice vs fixed-group logged. Ling working sets did not differ.
- [x] Reasoning toggle skipped as a study aim. Comparison model must still accept reasoning off.
- [x] Longer frozen run logged. `runs/pgg/frozen_qwen_qwen3-8b_choice_seed0_n10.jsonl`
- [x] N=8, temperature 0.4, 5 episodes. `runs/pgg/frozen_qwen_qwen3-8b_choice_s8_t0.4_seed0_n5.jsonl`
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
| Comparison model | GPT-OSS rejected reasoning off. Qwen accepted `reasoning.enabled: false`. |
| N=4, temperature 0 | 800 replies, all ok. Seat 3 out after round 1 in every episode. Episodes were copies. |
| N=8, temperature 0.4 | 100 rows, 800 replies, all ok. Working size mostly 4 (69 rows), not 8 (5 rows). 376 seat-rounds left out. Seats 2, 4, and 7 were out most often. Contributions were 0.5 to 0.8, mean 0.685. No seat contributed below 0.5, so exclusion could not be scored against a low contribution. Episodes 0, 1, and 3 ended on the same four seats. Episodes 2 and 4 did not. Not a training result. |
| T2-e | Not started. No local GPU. OpenRouter cannot fine-tune. Fireworks serverless can do a GRPO-style LoRA, but not on this Qwen3 8B id. |

## Next

Write `notes/t2-gate.md` from these two Qwen files. Then the train-or-not call. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-03 ~03:10 EDT — N=8 temperature 0.4 finished. Exclusion happened, not tied to low contribution. T2 not finished.
**Signed:** ReputationLearning — 2026-10-02 ~15:58 IST — one-line pointer: 2month-plan speed-run synced; no exit-criteria edits.
**Signed:** ReputationLearning — 2026-10-02 ~16:01 IST — pointer only: go/no-go + optional <$25 pilot after N=4 finish + N=8 frozen.
