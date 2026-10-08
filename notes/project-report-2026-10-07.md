# Project report — 7 Oct 2026

**Repo:** `N-T-SH/learned-reputation`
**Design:** `notes/design-2026-10-03.md`
**Plan:** `notes/2month-plan.md`
**Status:** T2 finished as a pipeline tranche. PI no-go for now. T3 is not open.
**Spend:** about $10 on Fireworks. Cap $40. About $30 left. OpenRouter before that was $0.23.

## Decision

The PI no-go is the right call on these files. The trainer runs. The comparison that would justify three seeds does not. Closing T2 does not reverse that. A later go needs a paired frozen file on the same ids, a parse rate low enough to read, and a payoff-versus-placebo gap that survives both. None of those three are in hand.

## Question

The design asks whether a trained policy uses the public ledger when it nominates, and whether that differs from the same model frozen. A result would be a scripted free rider named less often after training, and higher contributions among the seats that remain. It is not a 0-versus-0.3 ranking. It is not emergent reputation.

Three outcomes were named in review, and all three stay in the analysis plan:

- Sharper exclusion: the trained policy names a visible high contributor and leaves out a visible zero more than frozen does.
- Closure: the trained policy names fewer seats and leaves model seats out with the probes. This is a result, not a failed run.
- Unchanged prior: training does not move the frozen preference.

## What was built

Eight seats. One unit each. Contribution in [0, 1]. A working set of at least two splits 1.6 times the sum. A lone seat gets 0.8. A pair exists only if both name each other. The prompt is the last five rounds of every seat's contribution and nominations, labels shuffled per seat. No reputation score. No game-theory words. Thinking off. Qwen 3.8 27B on Fireworks. Temperature 0.4.

The training path that can be interpreted is the later one. Four complete episodes share a starting id list. The score is each seat's return over the episode. Other seats are not held fixed. Log probabilities are requested and the step aborts if they are missing. A placebo shuffles those returns before the advantage. Measurement finishes in the same process, because a fresh process cannot reload a snapshot.

The earlier path should not be cited as training. It filled missing log probabilities with zeros, held other seats fixed, and measured frozen and trained on different seeds.

## Evidence

Frozen seats, seeds 11–13, probes at 0 and 0.3, no step: the zero was named 68, 28, and 44 times out of 120. The spread across three episodes is already large.

Frozen control, seeds 21–23, a third seat at 1: the high seat was named 82, 75, and 80 times out of 100. The zero was named 12, 10, and 10. The base model already prefers a visible 1. That is the before picture. It does not need a training claim attached to it.

The old trained snapshot, seeds 14–16, named the zero 0, 0, and 2 times out of 120 and also dropped model seats. The high-seat control on that snapshot named the high seat 86, 77, and 85 times out of 100, in line with frozen. That update is not interpretable. It is not the arm to replicate.

The interpretable pair is one payoff group and one placebo group, seed 40, twenty rounds, measurement in the same process.

| Arm | High named | Zero named | 0.3 named | Names per reply | Repair failures | Mean contribution |
|---|---|---|---|---|---|---|
| Payoff | 73/100 | 1/100 | 1/100 | 1.76 | 18 | 0.55 |
| Placebo | 43/100 | 3/100 | 11/100 | 1.05 | 41 | 0.31 |

The payoff file names the high seat more than the placebo file. It also fails repair less often. A failed reply is repaired to an empty nomination and a contribution of 0, so the gap can be a parse gap. Two model seats in the payoff file were named 42 and 46 times. Three were named 3, 3, and 7. A core is still there. There is no frozen episode on these ids. The earlier frozen control, on other ids, already named the high seat about 80 times out of 100. The payoff rate of 73 may be the prior.

A fresh process returned 404 on the saved snapshot. Measurement has to finish before the process exits. A run that dies after the step loses the measurement.

Messages were an empty inbox. That question is deferred, not dropped. Eight seats stay. Sixteen seats stay out.

## Why this is a no-go

The plan-bot review asked not to buy three seeds of an update that cannot be read. That still holds for the old path. The new path fixed the log probabilities and the held-fixed return, and it added a placebo. It did not fix the parse rate, the missing same-id frozen file, or the reload. One pair with 41 placebo repair failures is not a seed to scale.

A future go would need all three of these, in this order:

1. A frozen episode on the same ids as the trained file, no step. If it already names the high seat about 70 times out of 100, the payoff step did not move the prior.
2. Repair failures under about 5 out of 100 on frozen and on both trained arms. Otherwise selectivity is a parse count.
3. A payoff-versus-placebo gap on those same ids that remains after the parse rate is low. Stop if the high-versus-zero contrast sits inside the frozen range.

Closure stays a named outcome. Fewer names per reply, with model seats left out beside the probes, is reported as closure. It is not counted as sharper exclusion.

## Leftover cap

About $30 remains. Do not buy another 20-round training group until the two cheap checks are read. A training group is about 400 samples plus 100 measurement samples. Two of those already fit in the $10. A third, with the same parse rate, would spend the chance to answer the missing question.

Spend in this order.

1. Frozen episode on seed 40, the ids in `runs/train/long_payoff.jsonl`. No step. One hundred model replies. Print named zero, named high, names per reply, and repair failures. This is the missing before picture for the only interpretable pair. If the high seat is already near 73, training did not do the thing the payoff file appeared to do.
2. One frozen episode at temperature 0.2, new ids, same probes. Count repair failures. If they fall from the 18–41 range to near zero, a later train is readable. If they do not, the prompt or the parser is the next fix, and that fix does not need Fireworks.
3. Stop and write the numbers into this note. Only if the frozen seed-40 file is clearly below the payoff file, and the low-temperature parse rate is low, spend the rest on one placebo group at that temperature, measurement in the same process. If either check fails, do not spend the rest.

A graded frozen episode, probes at 0, 0.3, 0.7, and 1, is the optional third file if the first two are cheap. It documents the prior. It does not train. It does not reopen T3.

What the leftover cap cannot buy: a reload that works in a new process, a 16-seat arm, a message arm, or three seeds.

## Next steps that do not need the cap

Write the no-go sentence into `notes/t2-gate.md` and leave T3 closed. Keep the three outcomes in the analysis plan. Tabulate repair failures in the payoff and placebo files: empty output, non-JSON, unknown ids. That table is the confound a reviewer will ask for. Do not cite the zero-filled update as a trained effect.

A later proposal, if the cheap checks are kind, is one seed at a parse rate that can be read, with a same-id frozen file and a placebo, under the remaining cap. It is not T3. T3 remains three seeds, a message check, and a main analysis, and it waits on a go.
