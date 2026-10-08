# Learned reputation without a reputation score

**Project report, 8 October 2026**
**Repo:** `N-T-SH/learned-reputation`
**Status:** This round stops. The PI said no-go. About $10 of a $40 Fireworks cap was spent. No further runs in this round.
**Signed:** Implementation bot, 8 October 2026. Local parse check `parse_ok 5`. Round closed.

This note is for a reader who was not in the lab thread. It says what was asked, what was built, what the files show, and what can be claimed. The deciding comparison has been run.

## How to read the null

Training made no measurable difference in this round. That sentence is about one update, not about reinforcement learning in general.

The trained arm received one update from one group of four games. Expecting one step to visibly change a 27B model was optimistic. The honest claim is that one valid update did not move the prior. The thesis is untested, not refuted. A later proposal is not undercut by this report if it is read that way.

## The question

The project asks whether a group of language-model agents can learn whom to include, from the payoffs of a public-goods game, without being given a reputation score.

Each agent has one unit. It can put some or all of that unit into a shared pot, and it can name other agents as partners. A partnership exists only if both sides name each other. The pot of a group of at least two is multiplied by 1.6 and split equally. An agent left out, or left alone, gets 0.8. Naming a partner who contributes, and being named back, pays. Naming a free rider, or contributing while being left out, does not.

The design does not put a reputation number in the prompt. It does not tell the model to exclude anyone. What the model sees is a ledger: the last five rounds of every seat's contribution and nominations, with the labels shuffled so that position in the list is not a seat identity. If inclusion tracks contribution, that has to come from the ledger and from the payoff.

A result, in the design note of 3 October, would be a scripted free rider named less often after training than before, and higher contributions among the seats that remain. A ranking of a zero contribution against a 0.3 contribution was not required. A claim of emergent reputation was not required.

Three outcomes stay in the analysis plan:

- Sharper exclusion. After training, a visible high contributor is named more, and a visible zero is named less, than by the same model with no training. A drop in names per reply is not this result. The count that matters is nominations of the zero divided by nominations of model seats that contributed about 1.
- Closure. The policy names fewer seats and leaves some model seats out along with the probes. This is a result, not a failed run. In this round it was already present before training.
- Unchanged prior. Training does not move what the frozen model already does. This is the outcome this round supports.

## The game, in one pass

Eight seats. Five are copies of the model. Three are scripted, so their behavior is known. One always contributes 0. One always contributes 0.3. One always contributes 1. Each scripted seat names the two highest contributors from the previous round. The model seats reply with a short message, a list of partner ids, and a contribution between 0 and 1. A reply that cannot be parsed is repaired to an empty nomination and a contribution of 0, and counted as a failure.

The model is Qwen 3.8 27B, thinking off, temperature 0.4, through Fireworks. The comparison that can be read is Fireworks against Fireworks. An earlier OpenRouter file used a different endpoint and a plain prompt. It is not the before picture for these runs. It does matter for the parse rate, below.

## What training was supposed to do

The training method is a group-relative policy update. Several rollouts are scored. A rollout that scores above the group mean is reinforced. One that scores below it is not. The score is the seat's own payoff from the decision to the end of the episode, not a reputation bonus.

The first attempt did not implement that. Log probabilities were often missing and were replaced with zeros, so the importance ratio was one for every token. The return held the other seats' later actions fixed, so a reply that contributed nothing was never dropped in the counterfactual. What that return could pay was naming seats that were already naming you, because a pair needs both sides. That predicts a clique. Those files are kept. They are not cited as a training effect. They are a caution: a flawed update produced a dramatic, convincing-looking freeze-out of free riders. Combined with the frozen baselines, that contrast is worth a short note. It should not be lost as a failed pilot. Do not replicate that update.

The later attempt fixed both points. Four complete episodes shared a starting list of ids. The score was each seat's payoff over the whole episode, so other seats could react. Log probabilities were requested, and the step aborted if they were missing. A placebo arm shuffled the four returns before the advantage, so a step still ran, but it was not paid by the game. Measurement had to finish in the same process. A fresh process cannot reload a saved snapshot: the call returns 404.

## What the frozen model already does

Before any interpretable training, the frozen model preferred a seat that contributes 1.

On three episodes with new ids, the high scripted seat was named 82, 75, and 80 times out of 100. The zero was named 12, 10, and 10. The 0.3 seat was named 5, 8, and 10. The base model already tells a visible 1 from a visible 0. It does not cleanly rank 0 below 0.3. That is simple first-order judgment from pretraining, the pattern Horibe and coauthors reported for models that have not been trained on the game. It is the prior. Training has to move it, not rediscover it.

An earlier frozen file, with only the 0 and 0.3 probes, named the zero 68, 28, and 44 times out of 120. Three episodes on the same setup do not agree with each other. One episode is not a rate.

The in-group is also in the untrained model. On the seed-40 frozen episode, the five model seats were named 30, 25, 4, 20, and 6 times. Training did not create that unevenness.

## The comparison that decides this round

One id list, seed 40. Probes `7eknaf` at 0, `s3kn51` at 0.3, `ojtk7t` at 1. Twenty rounds. Five model seats, so each probe can be named 100 times. The untrained file is `runs/train/long_frozen_seed40.jsonl`.

| Arm | What it is | High named | Zero named | 0.3 named | Names per reply | Repair failures | Mean contribution |
|---|---|---|---|---|---|---|---|
| Untrained | No step | 69 | 2 | 0 | 1.56 | 17 | 0.66 |
| Trained, real rewards | Four episodes, then one measurement episode. `runs/train/long_payoff.jsonl` | 73 | 1 | 1 | 1.76 | 18 | 0.55 |
| Placebo | Same group, returns shuffled. `runs/train/long_placebo.jsonl` | 43 | 3 | 11 | 1.05 | 41 | 0.31 |

The trained file and the untrained file are the same episode. The high seat moves from 69 to 73. The zero moves from 2 to 1. Unreadable replies are 17 and 18. Names per reply are 1.56 and 1.76. One valid update did not move the prior.

The apparent gain over the placebo came from the placebo getting worse. Scrambled rewards produced 41 unreadable replies out of 100, against 17 with no step. A failed reply is replaced with an empty nomination, so the drop in names is partly a parse failure. The placebo did not show that the game taught exclusion.

After the payoff step, two model seats were named 42 and 46 times and three were named 3, 3, and 7. The untrained file already favored some model seats over others. The clique pattern was not created by the update.

## The broken first run

The old trained files, seeds 14 to 16, named the zero 0, 0, and 2 times out of 120, against a frozen range of 28 to 68. That gap looked like emergent exclusion. It came from an update with zero log probabilities and a return that could reward reciprocal pairing and could not show a seat being dropped later. The high-seat control on that snapshot named the high seat about as often as the frozen model. Those files are the caution above. They are not replicated, and they are not the arm in the deciding table.

## Unreadable replies

About 17 of 100 untrained replies failed on Fireworks. The earlier OpenRouter ledger file had essentially none. That points to the prompt wrapper or the chat template, not to the game.

A local recovery is in `agents/train/parse_reply.py`. It closes a cut-off object when the written keys are intact, accepts a string or null nomination, and reads a contribution written as text. A reply with no object still fails closed. The check `python -m agents.train.parse_reply` printed `parse_ok 5` on 8 October. The reply cap is now 160 tokens, and the prompt asks for only the JSON object. The live rate is unmeasured. A later round still needs fewer than about 5 unreadable replies out of 100 before any paid step.

Messages were in the design and were passed as an empty inbox. Nothing in these files says whether a message changes a nomination. That question is deferred, not dropped.

A saved adapter cannot be sampled in a new process. The measurement episodes exist because they finished before the process exited. A later run has to measure before it exits, until a reload works.

## What can be claimed

- A working, cheap environment and pipeline, reusable for a later attempt. The payoff and placebo path is `agents/train/long_group.py`. The same-id untrained path is `agents/train/frozen_seed40.py`. The log-probability check is `agents/train/logprob_smoke.py`. The reply recovery is `agents/train/parse_reply.py`.
- Frozen Qwen 3.8 27B shows first-order discrimination, a 1 over a 0, and some in-group formation, without any training.
- One valid update did not change that.
- A broken update can manufacture the appearance of emergent exclusion.

## Why this round stops

The PI no-go matches the deciding file. The remaining cap stays unspent. Another training group in this setup would buy another copy of the prior, or another damaged placebo. A low-temperature parse run is not recommended as a Fireworks spend. The leftover $30 is not the budget for a later round.

## What a later round would need

A later proposal is not this tranche reopened. It starts only if all of these hold.

The live unreadable rate is under about 5 out of 100, on the recovered parser, before any step. An untrained episode is run on the same ids as the trained episode. A placebo is run on those ids, and it does not wreck the output. The selectivity count is printed beside names per reply. Eight seats stay. Messages stay off. Sixteen seats stay out. Learning rate stays at `1e-5`. Log probabilities are required. A missing log probability aborts the step. Measurement finishes in the saving process.

The length this round never had is a learning curve, not one update. A later run is eight updates. Each update is four complete episodes of twenty rounds, five model seats, same ids within the group. That is about 400 training samples per update, the size of the payoff group already run. Measure, with no further step, after updates 1, 4, and 8, on those same ids, one episode of twenty rounds each time. Stop after update 1 if the high-versus-zero contrast sits inside the untrained range. The untrained episode is the first file, before update 1. A placebo group is one update only, after the parse rate is low, not eight.

Eight updates are a new budget. At the rate of this round, one update was a few dollars inside the $10. Eight updates, plus the three measurement episodes and one placebo, are on the order of $40 to $80, separate from the unspent remainder. Graded probes at 0, 0.3, 0.7, and 1 can replace the three scripted seats in that run. They are not a reason to start.

The claim, if any, is sharper exclusion against the frozen prior, read off the curve. Closure and an unchanged prior remain named outcomes. The thesis stays open.

## Sign-off

This round is closed. No further Fireworks run. The report, the seed-40 files, and the local parse check are the handoff.
