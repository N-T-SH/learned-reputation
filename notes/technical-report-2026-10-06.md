# Technical report — 6 Oct 2026

**Repo:** `N-T-SH/learned-reputation`
**Design:** `notes/design-2026-10-03.md`
**Plan:** `notes/2month-plan.md` (T3 closed until T2 is marked finished)
**Spend:** $10 on Fireworks, stated by Nitesh. OpenRouter before that was $0.23. No other total is in the tracker.

## Question

The design asks whether a trained policy uses the public ledger when it nominates, and whether that differs from the same model frozen. A result, in that note, is a scripted free rider named less often after training than before, and higher contributions among the seats that remain. It is not a claim that 0 is ranked below 0.3. It is not a claim of emergent reputation.

## What matched the design

Eight seats. Contribution in [0, 1]. Pot is the working-set sum times 1.6, split equally. A lone seat gets 0.8. A pair exists only if both name each other. The prompt carries the last five rounds of every seat's contribution and nominations. Labels are shuffled per seat. No reputation score and no game-theory words in the task block. The training reward is return from the decision round to the end of the episode. Thinking was off. Qwen 3.8 27B. Temperature 0.4.

The comparison that can be read is Fireworks against Fireworks. The OpenRouter file is a different endpoint and a plain prompt. It is not the before picture for these adapters.

## What was run

| File | What it is |
|---|---|
| `runs/train/measure_frozen.jsonl` | Seeds 11–13. Fresh adapter. No steps. Probes at 0 and 0.3. |
| `runs/train/measure_trained.jsonl` | Seeds 14–16. After one 20-round GRPO episode. No further steps. New ids. |
| `runs/train/control_high_frozen.jsonl` | Seeds 21–23. Third scripted seat contributes 1. |
| `runs/train/control_high_trained.jsonl` | Seeds 24–26. Same saved snapshot. No further steps. |

Earlier files are not this comparison. The 15-round resume changed probe seats at round 5. The plain-prompt pilot failed repair on 13 of 30 continuing actions. The chat-wrapped five-round pilot used a system line the frozen file did not have.

## Findings

Frozen seats named the zero 68, 28, and 44 times out of 120, and the 0.3 seat 42, 14, and 42. Those probes were in the working set 14, 5, and 10 rounds out of 20.

Trained seats named the zero 0, 0, and 2 times out of 120, and the 0.3 seat 0, 0, and 2. The probes were in the working set once or twice, and never in the last five rounds. Mean contribution was 0.94, 0.92, and 0.81, against a frozen spread from about 0.5 to 1.0. That gap is outside the frozen range. It is one training episode.

The trained file is a core group, not a ranking. Both probes were left out together. In seed 15, two model seats were named 96 and 101 times and three others were named 0, 1, and 2 times. A low contribution was not required for exclusion.

The control asks whether a visible 1 is treated like an outsider. On the frozen side the high seat was named 82, 75, and 80 times out of 100, and was in the working set 18, 17, and 19 rounds out of 20. The zero was named 12, 10, and 10. The 0.3 seat was named 5, 8, and 10. The base model already prefers the high seat.

On the trained snapshot the high seat was named 86, 77, and 85 times out of 100, and was in the working set 18, 17, and 18 rounds. The zero was named 2, 8, and 3. The 0.3 seat was named 0, 10, and 3. Seed 25 sits inside the frozen range for the low probes. The high seat does not. Exclusion can track a visible 1 against a visible 0. It does not rank 0 below 0.3.

## What the design asked for that these files do not have

Messages from the previous round were in the design and were passed as an empty inbox. The ledger has nominations and contributions. It does not test whether a message changes a nomination.

The return used in training held the other seats' actions fixed. It is not a fresh rollout of the model for each of the four replies. A reply that would have changed later nominations by other model seats is not scored for that.

The episode continued with the first of the four samples, not a draw from the group. The update used all four. The path the episode walked is the first reply.

Sampled log probabilities were often missing, so the importance ratio was built from zeros. The step ran. It is not a clean importance-sampling update.

The design's before picture was the OpenRouter ledger file. The trainable sampler does not follow that plain block. The comparison prompt is the ledger block as the user message, with thinking off in the chat template. Same words in the task. Different wrapper.

Sixteen seats were correctly left out. One training seed is not the three the plan lists for T3. The adapter path loaded for the control. An earlier second client 404ed. A new session is not yet a reliable way to reload.

## Gate

T3 in the plan is three training seeds, reasoning off, a message classifier with a hand check, and the trained-versus-frozen nomination analysis. It is closed until T2 is marked finished. The trainer is not the blocker.

A go is reasonable if T3 is aimed at the question these files can support: does a trained policy name a visible high contributor and withhold a visible zero, more than the frozen policy, across three seeds. A go is not reasonable if T3 is aimed at ranking 0 below 0.3, or at emergent reputation. Those are not in the files.

The no-go path in the plan, frozen-only, is the wrong spend. The frozen policy already names the high seat. The trained difference is real on one seed and needs replication, not a return to frozen-only.

## Budget

The $10 bought the smokes, two 20-round training episodes, and the measurement and control files above. A training episode is the costly part: six model seats, twenty rounds, four replies. A measurement episode is one reply.

A T3 that replicates the present design is three training seeds, three measurement episodes each, and a matched frozen set, plus the high-seat control on each seed. That is about three times the training already paid for, and about as much measurement again. At the rate implied by the $10, that is on the order of $40 to $80 on Fireworks. A hard cap of $100 covers a failed seed and a rerun. It does not cover a 16-seat arm, a second game, or training past one episode per seed.

Human time in the plan is 40–60 hours for the go path: the classifier, the hand check, and the write-up. That is not in the $100.

## Recommendation

Write the go/no-go as a narrow go. Three seeds. Same prompt, same probes, same high-seat control. Measurement with no further steps. Do not add seats. Do not claim a 0 versus 0.3 ranking unless a seed separates them. Mark T2 finished only after that sentence is in `notes/t2-gate.md`. Then open T3.
