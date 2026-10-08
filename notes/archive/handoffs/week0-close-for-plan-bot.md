> **Archived 8 Oct 2026** — see `notes/README.md`. Body below unchanged except link fixes.

# Plan-bot update — Week 0 closed (Tue 29 Sep 2026)
**For:** ResilientBots / plan Grok updating `resilient-lab-2month-30h-plan.md`
**From:** Nitesh + web Grok
**Rule:** After each design week, write a note like this. Do not reopen parked tracks.

## Week status
**Week 0: CLOSED enough to start Week 1.** Speakable gates 1–4 done in chat. vLLM local serve = **blocker** (no GPU), not a halt.

## Locked decisions
- Track: LLM-group design. Ueshima tabular = intuition only.
- Scripted controls: include j next round iff last visible c_j ≥ 0.5; null = random per round; visibility local.
- Withhold RepuNet scalar/update/gossip/score-coupled connect.

## Next
Week 1: scripted PGG + JSONL + recover the two rules. No LLM seats until the regression gate is green.
