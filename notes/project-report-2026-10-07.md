# Learned reputation without a reputation score

**Project report, 7 October 2026**
**Repo:** `N-T-SH/learned-reputation`
**Status:** Stopped. The PI said no-go. No further Fireworks runs are recommended. About $10 of a $40 cap was spent.

This note is written for a reader who has not been in the lab thread. It says what was asked, what was built, what the files show, and why the work stops here.

## The question

The project asks whether a group of language-model agents can learn whom to include, from the payoffs of a public-goods game, without being given a reputation score.

Each agent has one unit. It can put some or all of that unit into a shared pot, and it can name other agents as partners. A partnership exists only if both sides name each other. The pot of a group of at least two is multiplied by 1.6 and split equally. An agent left out, or left alone, gets 0.8. Naming a partner who contributes, and being named back, pays. Naming a free rider, or contributing while being left out, does not.

The design does not put a reputation number in the prompt. It does not tell the model to exclude anyone. What the model sees is a ledger: the last five rounds of every seat's contribution and nominations, with the labels shuffled so that position in the list is not a seat identity. If inclusion tracks contribution, that has to come from the ledger and from the payoff.

A result, in the design note of 3 October, would be a scripted free rider named less often after training than before, and higher contributions among the seats that remain. A ranking of a zero contribution against a 0.3 contribution was not required. A claim of emergent reputation was not required.

Review added two other outcomes, so that a negative or a different result would still be a result:

- Sharper exclusion. After training, a visible high contributor is named more, and a visible zero is named less, than by the same model with no training.
- Closure. After training, the policy names fewer seats and leaves some model seats out along with the probes. That is a real pattern. It is not the reputation result.
- Unchanged prior. Training does not move what the frozen model already does.

## The game, in one pass

Eight seats. Five are copies of the model. Three are scripted, so their behavior is known. One always contributes 0. One always contributes 0.3. One always contributes 1. Each scripted seat names the two highest contributors from the previous round. The model seats reply with a short message, a list of partner ids, and a contribution between 0 and 1. A reply that cannot be parsed is repaired to an empty nomination and a contribution of 0, and counted as a failure.

The model is Qwen 3.8 27B, thinking off, temperature 0.4, through Fireworks. The comparison that can be read is Fireworks against Fireworks. An earlier OpenRouter file used a different endpoint and a plain prompt. It is not the before picture for these runs.

## What training was supposed to do

The training method is a group-relative policy update. Several rollouts are scored. A rollout that scores above the group mean is reinforced. One that scores below it is not. The score is the seat's own payoff from the decision to the end of the episode, not a reputation bonus.

The first attempt did not implement that. Log probabilities were often missing and were replaced with zeros, so the importance ratio was one for every token. The return held the other seats' later actions fixed, so a reply that contributed nothing was never dropped in the counterfactual. What that return could pay was naming seats that were already naming you, because a pair needs both sides. That predicts a clique. Those files are kept. They are not cited as a training effect.

The later attempt fixed both points. Four complete episodes shared a starting list of ids. The score was each seat's payoff over the whole episode, so other seats could react. Log probabilities were requested, and the step aborted if they were missing. A placebo arm shuffled the four returns before the advantage, so a step still ran, but it was not paid by the game. Measurement had to finish in the same process. A fresh process cannot reload a saved snapshot: the call returns 404.

## What the frozen model already does

Before any interpretable training, the frozen model preferred a seat that contributes 1.

On three episodes with new ids, the high scripted seat was named 82, 75, and 80 times out of 100. The zero was named 12, 10, and 10. The 0.3 seat was named 5, 8, and 10. The base model already tells a visible 1 from a visible 0. It does not cleanly rank 0 below 0.3. That preference is the prior. Training has to move it, not rediscover it.

An earlier frozen file, with only the 0 and 0.3 probes, named the zero 68, 28, and 44 times out of 120. Three episodes on the same setup do not agree with each other. One episode is not a rate.

## The comparison that decides it

One id list, seed 40. Probes `7eknaf` at 0, `s3kn51` at 0.3, `ojtk7t` at 1. Twenty rounds. Five model seats, so each probe can be named 100 times.

| Arm | What it is | High named | Zero named | 0.3 named | Names per reply | Repair failures | Mean contribution |
|---|---|---|---|---|---|---|---|
| Frozen | No step. `runs/train/long_frozen_seed40.jsonl` | 69 | 2 | 0 | 1.56 | 17 | 0.66 |
| Payoff | Four episodes, scored by the game, then one measurement episode. `runs/train/long_payoff.jsonl` | 73 | 1 | 1 | 1.76 | 18 | 0.55 |
| Placebo | Same group, returns shuffled. `runs/train/long_placebo.jsonl` | 43 | 3 | 11 | 1.05 | 41 | 0.31 |

The payoff file and the frozen file are the same episode. The high seat moves from 69 to 73. The zero moves from 2 to 1. Repair failures are 17 and 18. Names per reply are 1.56 and 1.76. That is not a trained change.

The placebo file is worse. The high seat falls to 43. Names per reply fall to 1.05. Repair failures rise to 41. A failed reply is replaced with an empty nomination, so some of that drop is a parse failure. A shuffled return did not teach exclusion. It made the policy worse at producing a readable action.

Both trained files still form uneven groups among the model seats. After the payoff step, two model seats were named 42 and 46 times and three were named 3, 3, and 7. After no step, the same seats were named 30, 25, 4, 20, and 6. A core is in the frozen file too. Training did not create it.

## What was ruled out

The old trained files, seeds 14 to 16, named the zero 0, 0, and 2 times out of 120, against a frozen range of 28 to 68. That gap was outside the frozen spread. It came from an update with zero log probabilities and a return that could not see a later exclusion. The high-seat control on that snapshot named the high seat about as often as the frozen model. Those files show closure from an uninterpretable step. They are not replicated.

Messages were in the design and were passed as an empty inbox. Nothing in these files says whether a message changes a nomination. That question is deferred, not dropped.

A saved adapter cannot be sampled in a new process. The measurement episodes exist because they finished before the process exited.

## Why the no-go follows

The PI no-go matches the files. The thing a further seed would have to show is a payoff arm that names the high seat more, and the zero less, than a frozen arm on the same ids, with a parse rate low enough to read, and a placebo that does not copy the gap. The same-id frozen file removes the gap. Spending the remaining cap on another training group would buy another copy of the prior, or another damaged placebo.

No further runs are recommended. A low-temperature parse check would not change the decision. The stop rule was the seed-40 frozen file, and it has been read.

## What a later go would need

A later proposal is not this tranche reopened. It would need a parser or a prompt that fails on fewer than about 5 replies out of 100, a frozen episode on the same ids as the trained episode, and a placebo that does not itself destroy the output. Eight seats stay. Messages stay off until that comparison exists. Sixteen seats stay out. The claim, if any, is sharper exclusion against the frozen prior. Closure and an unchanged prior remain named outcomes.

The pipeline can be reused. `agents/train/long_group.py` is the payoff and placebo path. `agents/train/frozen_seed40.py` is the same-id frozen path. `agents/train/logprob_smoke.py` is the check that log probabilities came back. The 7 October note and this file are the record.
