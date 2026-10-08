# For the plan bot

> **Stale (2 Oct 2026), historical.** Round closed 8 Oct; T3 NO-GO. Kept at this path because `skills/lab-coordination/SKILL.md` names it as the implementation-bot → plan-bot channel. Index: `notes/README.md`.

**From:** implementation bot
**Date:** 2026-10-02
**Do not treat this as an edit of `notes/2month-plan.md`.** ReputationLearning syncs the plan.

## What changed in the lab loop
Nitesh, 2 Oct: implementation bot writes the code, explains it, and asks a check question. Do not leave functions empty. Nitesh reviews, pushes back, and can edit.

## Pace Nitesh stated
About 24 hours a week for this estimate. Today's session was about 5 hours. Coach still owns the calendar. This note does not invent a hold.

## T2 state after 2 Oct
Done: repair door, FakeLM smoke, Ling smoke (4 seats, 5 rounds, all replies ok), prompt checklist committed and sample `ok True`, choice vs fixed logged. Working sets did not differ because Ling nominated broadly. Reasoning toggle skipped by Nitesh: not a study aim.

Still open in T2: a train pilot or a written "no train path" failure, then `notes/t2-gate.md` from real logs, then mark T2 finished. Do not open T3 until that mark.

## Before a training run
Nothing scientific is blocking. Schema, repair, env, prompt, and logs exist. What is missing is a trainer. OpenRouter free cannot fine-tune. There is no local GPU. A pilot that only calls a frozen model is an inference run, not training.

## Cost of an inference pilot, not training
200 episodes, 4 seats, 20 rounds is 16,000 calls. At the dry size, about 1.1M prompt tokens and under 1M short replies. On a cheap paid id that is about a dollar before the platform fee. Ling free is $0 but about 1,000 calls a day after the $10 credit purchase, so 16 days. The $10 purchase is the quota unlock, not the inference bill.

A real LoRA or GRPO pilot is not priced here. It needs a rented GPU or a fine-tune API. That is the T2-end go/no-go, not a number to invent.

## Remaining study, if the bot writes the code
Estimate at 24h/week, review-not-type. Wall clock stretches if Coach holds are shorter.

| Piece | Hours | Weeks at 24h |
|-------|------|----------------|
| Close T2: gate note, train-path decision, no emergence claim | 4–6 | this week |
| T3 if frozen-only substitute: more seeds, message check, nomination analysis | 20–30 | 1–2 |
| T3 if full GRPO, 3 seeds, after a GPU path exists | 40–60 | 2–3 |
| T4 reintegration only if the main result is positive, plus write-up | 20–30 | 1–2 |

Frozen-only finish is about 4–6 weeks. Full training finish is about 6–8 weeks, and only after the GPU call. Do not spend T3 debugging a trainer.

## T3, from the current plan
If the T2-end call is go: GRPO, 3 seeds, reasoning off; a message classifier with a hand check; analysis of whether history or messages predict nomination, and whether training changes that versus frozen.

If the call is no: frozen-only or a smaller toy. Same question, no trained policy. Reintegration stays T4 and only if the main result is positive.

## Ask
Sync `notes/2month-plan.md` from this note. Leave T3 closed until T2 is marked finished. Hours stay with Coach.

---
**Signed:** ReputationLearning — 2026-10-08 ~15:55 IST — Stale banner added; body unchanged.
