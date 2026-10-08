# notes/ — index

**Status (8 Oct 2026): round closed.** T2 finished, and T3 is a **no-go** (Nitesh + PI). On the seed-40 comparison, one valid GRPO update on Qwen 3.8 27B did not move the frozen prior. The thesis is **untested, not refuted**. About $10 of the $40 Fireworks cap was spent, and the rest is not reused. A later round would be a new proposal, not T3 reopened. Start with the final report: [`project-report-2026-10-07.md`](project-report-2026-10-07.md) (content dated 8 Oct).

## Files

| Path | Purpose | Status |
|---|---|---|
| [`README.md`](README.md) | This index | current |
| [`project-report-2026-10-07.md`](project-report-2026-10-07.md) | Final project report for a new reader: question, build, deciding comparison, claims, later-round sketch | current (final) |
| [`2month-plan.md`](2month-plan.md) | Plan of record. Has the "Round status — CLOSED 8 Oct 2026" section, the tranche map, and the funding artifacts | current (closed round) |
| [`design-2026-10-03.md`](design-2026-10-03.md) | Game and prompt design after the 3 Oct review: public five-round ledger, lone seat 0.8, shuffled ids, return-to-go, 8 seats | current (design of record) |
| [`t2-gate.md`](t2-gate.md) | Frozen N=8 before-picture gate (5 Oct), plus the 8 Oct T3 no-go decision | current |
| [`grpo-step-mechanics.md`](grpo-step-mechanics.md) | How one Fireworks LoRA GRPO step works on this game (reusable reference) | current (reference) |
| [`tranche2-tracker.md`](tranche2-tracker.md) | T2 tracker. FINISHED 6 Oct as a pipeline tranche, closed 8 Oct | closed. Kept here because `skills/lab-coordination/SKILL.md` and the root `README.md` name it |
| [`for-implementation-bot.md`](for-implementation-bot.md) | Plan bot → implementation bot rules doc. Its standing rules still apply; the "Active work" section is historical | current (rules). Kept here, `SKILL.md` names it |
| [`for-plan-bot.md`](for-plan-bot.md) | Implementation bot → plan bot note, 2 Oct | stale. Kept here, `SKILL.md` names it |
| [`archive/reports/technical-report-2026-10-03.md`](archive/reports/technical-report-2026-10-03.md) | Frozen baselines through 3 Oct; OpenRouter costs; Fireworks path found | archived |
| [`archive/reports/measure-2026-10-05.md`](archive/reports/measure-2026-10-05.md) | 5 Oct frozen vs trained measurement from the broken (zero-filled log-prob) update. Not a result | archived |
| [`archive/reports/technical-report-2026-10-06.md`](archive/reports/technical-report-2026-10-06.md) | 6 Oct report and revision: trained gap is not a result; $40 cap; next-step budget | archived |
| [`archive/reports/seed40-frozen-addendum.md`](archive/reports/seed40-frozen-addendum.md) | 7 Oct seed-40 frozen / payoff / placebo table (the deciding comparison; also in the report) | archived |
| [`archive/trackers/tranche1-tracker.md`](archive/trackers/tranche1-tracker.md) | T1 scripted PGG pipeline tracker. FINISHED 1 Oct | archived |
| [`archive/superseded/locked-controls.md`](archive/superseded/locked-controls.md) | 1 Oct locks (local visibility, N=4), superseded by the 3 Oct design | archived |
| [`archive/handoffs/week0-close-for-plan-bot.md`](archive/handoffs/week0-close-for-plan-bot.md) | Week 0 close note (29 Sep, resilient-lab era) | archived |

`notes/tranche3-tracker.md` does not exist on purpose, because T3 is a no-go.

## Rules

- `2month-plan.md` is written only by ReputationLearning. The implementation bot reads it.
- The implementation bot owns its trackers and reports (`tranche*-tracker.md`, technical reports, gate notes from real logs). ReputationLearning appends signed lines only.
- Pull before editing (`git pull --ff-only`).
- Sign at the bottom of every note you create or materially edit (bot name, IST time, one line), then push to `main`.
- Archive, don't delete: move superseded notes with `git mv` into `archive/` and update this index.

---
**Signed:** ReputationLearning — 2026-10-08 ~15:57 IST — Created the notes index after the round close and the archive tidy.
