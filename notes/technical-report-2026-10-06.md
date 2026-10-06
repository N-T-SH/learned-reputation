# Technical report — 6 Oct 2026

**Repo:** `N-T-SH/learned-reputation`
**Design:** `notes/design-2026-10-03.md`
**Plan:** `notes/2month-plan.md` (T3 closed until T2 is marked finished)
**Spend:** $10 on Fireworks, stated by Nitesh. OpenRouter before that was $0.23.
**Revision:** 6 Oct, after review. The trained gap is not a result. Do not replicate this update.

## Question

The design asks whether a trained policy uses the public ledger when it nominates, and whether that differs from the same model frozen. A result is a scripted free rider named less often after training than before, and higher contributions among the seats that remain. It is not a 0-versus-0.3 ranking. It is not emergent reputation.

Closure is a named outcome, beside sharper exclusion and no change. A policy that names fewer seats, and leaves model seats out with the probes, counts as closure. It does not count as a failed run.

## What matched the design

Eight seats. Contribution in [0, 1]. Pot is the working-set sum times 1.6, split equally. A lone seat gets 0.8. A pair exists only if both name each other. The prompt carries the last five rounds of every seat's contribution and nominations. Labels are shuffled per seat. No reputation score and no game-theory words in the task block. Thinking was off. Qwen 3.8 27B. Temperature 0.4. The comparison is Fireworks against Fireworks.

## What was run

| File | What it is |
|---|---|
| `runs/train/measure_frozen.jsonl` | Seeds 11–13. Fresh adapter. No steps. Probes at 0 and 0.3. |
| `runs/train/measure_trained.jsonl` | Seeds 14–16. After one 20-round episode. No further steps. Different seeds from the frozen file. |
| `runs/train/control_high_frozen.jsonl` | Seeds 21–23. Third scripted seat contributes 1. |
| `runs/train/control_high_trained.jsonl` | Seeds 24–26. Same saved snapshot. No further steps. |

## Findings

Frozen seats named the zero 68, 28, and 44 times out of 120. Trained seats named it 0, 0, and 2. The trained file also left model seats out. In seed 15, three model seats were named 0, 1, and 2 times. Both probes were left out together.

The frozen control named the high seat 82, 75, and 80 times out of 100, and the zero 12, 10, and 10. The trained snapshot named the high seat 86, 77, and 85, and the zero 2, 8, and 3. The base model already prefers a visible 1. The trained high-seat rate did not move past that.

These files show closure. They do not show sharper judgment of contributions.

## Why the trained gap is not a result

Sampled log probabilities were missing and replaced with zeros. The importance ratio was then one for every token. A step ran. It cannot be read as the reward being optimized.

The return held the other seats' later actions fixed. A reply that contributed nothing was not dropped in that counterfactual, because nobody else was allowed to react. What the return could pay was naming seats that were already naming you. That pays in the same round, because a pair needs both sides. It predicts a core.

Frozen and trained measurement used different seeds. The zero-naming gap sits outside the frozen spread of 28 to 68. That is not enough to call it real, because the update was not interpretable.

Messages were an empty inbox. That question is deferred, not dropped.

## Gate

T3 stays closed. Frozen-only is the wrong spend: the base model already names the high seat. Replicating the present update across three seeds is also the wrong spend.

The claim, if T3 opens later, is that a trained policy names a visible high contributor and leaves out a visible zero more than frozen does, across three seeds. No 0-versus-0.3 ranking unless a seed separates them. No messages. A selectivity count sits beside it: nominations of the zero divided by nominations of model seats that contributed about 1. Fewer names overall is not a result. Stop after seed 1 if that contrast is inside the frozen range.

## Next block, before any seed

1. A smoke that requests log probabilities and refuses to train if they are missing. `agents/train/logprob_smoke.py`.
2. A group of four complete episodes from the same ids. The score is each seat's return over the episode. The other seats are not held fixed.
3. One placebo episode, shuffled or constant rewards. If a core still forms, the effect is drift.
4. Paired measurement seeds, and a reload that does not 404.

Graded probes at 0, 0.3, 0.7, and 1 wait until the step is interpretable. Eight seats stay. Messages stay off. Learning rate stays at 2.5e-5 until the ratio is real, then a smaller rate is the next knob.

## Budget

The $10 bought the smokes, two training episodes, and the files above. The log-probability smoke and the placebo are a few dollars. The $100 hard cap still covers three seeds after those pass. It does not cover 16 seats or a second game.
