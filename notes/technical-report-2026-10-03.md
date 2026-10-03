# Technical report: frozen baselines through 3 Oct 2026
**Repo:** `N-T-SH/learned-reputation`
**Author:** implementation bot, from logs on `main`
**Training:** not started

## What was built

A scripted public-goods environment with bilateral partner choice, a repair door, and a frozen speaker. Model text never becomes an action except through repair. Logs are JSONL. A dropped connection is retried. A seat reply is saved before the next seat is called, so a rerun does not pay for it again. Speaker, model, group rule, seat count, and temperature are command-line flags. A new setting writes a new file.

OpenRouter is the inference path. The key stays in `.env`. FakeLM is the no-key path. The prompt check rejects a forbidden word and a seat the prompt is not allowed to see.

## Pipeline checks

The scripted positive file named high contributors and the null file did not. That gate passed before any model seat. Ling, on choice and on fixed groups, kept all four seats, so the choice rule had nothing to do. `openrouter/free` returned a safety stub. Gemma's free id was rate-limited. GPT-OSS rejected reasoning off. Qwen3 8B and Qwen 3.8 27B both returned short JSON with reasoning off.

The Qwen3 8B bill for the four-seat file was $0.03 for 877 requests and 172,000 tokens.

## Findings

Qwen3 8B, four seats, temperature 0, ten episodes. Eight hundred replies, all accepted. Seat 3 was out after round 1 in every episode. The ten episodes were copies. Isolation paid 0.8. The three inside paid about 1.42. Contributions settled at 0.7.

Qwen3 8B, eight seats, temperature 0.4, five episodes. Eight hundred replies, all accepted. Working size was 4 in 69 of 100 rounds. Three hundred seventy-six seat-rounds were out. Contributions were 0.5 to 0.8. Nobody was below 0.5. Three episodes ended on the same four seats.

Qwen 3.8 27B, eight seats, temperature 0.4, five episodes. File: `runs/pgg/frozen_qwen_qwen3.8-27b_choice_s8_t0.4_seed0_n5.jsonl`. Eight hundred replies, all accepted. Working size ran from 1 to 8, most often 3. Twenty-seven distinct working sets. Episodes did not copy each other. Three hundred eighty-eight seat-rounds were out. Seat 7 was out most often. Contributions were 0.5 to 1.0, mean 0.75. In-group mean 0.78, out-group mean 0.73. Pay in about 1.47, pay out 0.8. No timer fields: that process started before the timer commit.

Exclusion is real, and it is costly. It does not track a low contribution, because these frozen models do not produce a low contribution. That is the before picture. It is not a reputation result.

## Training path

There is no local GPU. OpenRouter cannot fine-tune. Fireworks serverless training can run a GRPO-style LoRA on its listed models and bill prefill, sample, and train tokens. Qwen 3.8 27B is on that rate card. Qwen3 8B is not a serverless training id. A twenty-step pilot with short JSON replies is on the order of a few dollars. A hundred steps can stay under $25 if replies stay short. Dedicated GPU training is not required for that pilot. A pilot on the 27B must be compared with the 27B frozen file, not the 8B file. Thinking must be off, and that flag has to be checked on the Fireworks sampler before a paid step.

## Next

Write `notes/t2-gate.md` from the 27B file. Then one call: a small Fireworks pilot on Qwen 3.8 27B, thinking off, reward equal to the environment payoff, or a written decision not to train. Do not open T3 before T2 is marked finished. A second game is a later check, not the next run.
