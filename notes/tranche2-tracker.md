# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`  
**Repo:** `N-T-SH/learned-reputation`  
**Opened:** 2026-10-01 (after T1 finished)  
**Pacing:** tranches, not calendar weeks. Blocks ≈ 2–3h AI+human.

## Status
**OPEN.** T1 measurement + schema gates are green. First LLM seats allowed **only** through `envs/pgg_scripted/schema.repair` (or a moved shared schema module). No GRPO full run this tranche — that is T3 after the T2-end go/no-go.

## Tranche map

| Old week | Tranche | Status |
|----------|---------|--------|
| 0 | T0 | Closed 29 Sep |
| 1–2 | T1 | **Finished** 1 Oct (`notes/tranche1-tracker.md`) |
| 3–5 | **T2** | **Active** — this file |
| 6–9 | T3 | After T2-end go/no-go |
| 10–12 | T4 | If main result positive |

## Locks (carry from T1 — do not reopen)

1. Visibility: **local** — last working-set partners’ `c`, plus messages *to me* (prior round). Not a global ledger.
2. Groups: **bilateral form / unilateral break.**
3. Units: y=1, threshold 0.5 (scripted control only), r=1.6, isolation 0.8.
4. Start frozen runs at **N=4**; scale only after smoke is green. N=6 optional; N=16 only after plan says so.
5. Repo: `learned-reputation` only.
6. Withhold: reputation **scalar**, score update, gossip-into-score, score-coupled connect, the word **REPUTATION** (and game-theory jargon) in prompts.
7. All model text → env **only** via `repair()`; bad → empty action + logged failure (`ok: false`).

## Thesis (T2)

Prove a **frozen** multi-seat LLM loop can run end-to-end on the scripted PGG (obs → prompt → model → repair → step → JSONL), then collect a small frozen matrix and a **short training pilot** so the T2-end funding/tech gate is evidence-based — not vibes.

## Exit criteria (T2)

- [ ] Frozen smoke: ≥1 episode, N=4, all seats through `repair`, JSONL under `runs/`
- [ ] Prompt + obs builder: local visibility; prior-round messages; no forbidden vocab
- [ ] Partner-choice **on** vs **fixed-group** (partner choice off) — at least a small seedable contrast logged
- [ ] Reasoning **on** vs **off** frozen compare (same task, frozen weights) — or documented blocker if API cannot toggle
- [ ] Training pilot: ~200 episodes, reasoning **off**, shared policy / LoRA path as designed — runs end-to-end **or** clear failure report for go/no-go
- [ ] Short note `notes/t2-gate.md` with what the pilot showed (no invented metrics) for the funding/tech call
- [ ] Tracker marked **FINISHED** + signed by implementation bot

## Blocks

| Block | Crux | Done when |
|-------|------|-----------|
| **T2-a** | Wire one frozen model call → `repair` → env step | Smoke JSONL: `runs/pgg/frozen_smoke_seed0.jsonl` (or agreed path); all seats `ok` or failures logged |
| **T2-b** | Observation + prompt builder | Unit/smoke: seat prompt contains only local `c` + msgs-to-me; grep/checklist: no REPUTATION / exclude-verb / game-theory jargon |
| **T2-c** | Partner choice on vs fixed-group | Two short runs logged; working-set / nomination stats differ in the expected direction *or* null documented |
| **T2-d** | Reasoning on/off frozen compare | Cell table paths under `runs/`; or signed blocker if provider cannot expose the toggle |
| **T2-e** | Train pilot (~200 eps, reasoning off) | Train script completes or fails with diagnosable log; write `notes/t2-gate.md` draft numbers from real logs only |
| **T2-f** (if time) | Harden logging / seed matrix | Enough seeds to trust variance for the go/no-go conversation |

## Instructions for implementation bot

**Read first (do not edit):** `notes/2month-plan.md`, `notes/locked-controls.md`, closed `notes/tranche1-tracker.md`.  
**Co-edit + sign:** this file.  
**Code you own:** `envs/`, `runs/`, any new `agents/` / `train/` / prompt modules. ReputationLearning does not scaffold.

### T2-a — frozen smoke (start here)
1. Pull `main`. Keep using existing `schema.repair` as the only door into the env.
2. Add a thin runner (suggested layout — adjust if cleaner):
   - `agents/frozen/` or `envs/pgg_scripted/run_frozen.py`
   - One provider path Nitesh can actually call today (OpenAI-compatible API, Anthropic, or local vLLM if GPU appears). If no key/GPU: implement a **FakeLM** that emits valid `{message,nominate,contribute}` dicts so the loop is real; mark FakeLM in the tracker Log and do not pretend it is a model result.
3. Per seat per round: build obs → prompt → model text/JSON → `repair(raw, n_seats)` → env step. Log `ok`, raw truncate, repaired action, payoffs, working set.
4. Success artifact: JSONL + a one-line Log entry here with commit hash.

### T2-b — prompts
1. Prompt must state affordances only (you may message, nominate partners, choose contribution in [0,1]). **Never** tell the model to “build reputation,” “exclude free-riders,” or name REPUTATION.
2. Observation: only what locks allow (local last working-set `c`; messages addressed to this seat from the **previous** round — already locked in T1).
3. Prefer structured output (JSON object matching schema keys). Still run `repair` on everything.
4. Add a tiny checklist script or test that fails CI/local if forbidden strings appear in prompt templates.

### T2-c — partner choice contrast
1. Condition A: nominations → `form_groups` as today (bilateral).
2. Condition B: **fixed-group** — ignore nominations; pre-set working sets (document the rule in Log).
3. Same FakeLM or frozen model; short R (e.g. 20) × few episodes; write both JSONLs.

### T2-d — reasoning on/off
1. If the provider supports a reasoning/thinking toggle or two model IDs: run the same frozen matrix twice and log paths.
2. If not: sign a blocker on this tracker; do not block T2-e on it.

### T2-e — train pilot
1. Shared policy / LoRA across seats as per standing design; **reasoning off** during training.
2. Target ~200 episodes (can be shorter for first green “trains end-to-end” smoke if GPU/API budget is tight — say so in Log with actual count).
3. Do **not** claim emergence. Success = train loop completes and losses/metrics are logged.
4. Draft `notes/t2-gate.md` from real numbers only; ReputationLearning will polish for the go/no-go.

### Out of T2 (do not pull in)
- Full 3-seed GRPO campaign (T3)
- Reintegration probe (T4)
- Hardcoded reputation scalar / gossip score
- Stealing CS329A / Rent calendar blocks (Coach owns hours)

### Signing
After each block: pull → update Status/Log/Exit criteria → append  
`**Signed:** Implementation bot — YYYY-MM-DD HH:MM IST — …` → push.  
When all required exit boxes are green (T2-d blocker allowed if signed): set Status **FINISHED** and sign. ReputationLearning then opens T3.

## Log

| Block | Result |
|-------|--------|
| T2-a | *not started* |
| T2-b | *not started* |
| T2-c | *not started* |
| T2-d | *not started* |
| T2-e | *not started* |

## Next

Implementation bot: start **T2-a** this Lab window if time remains before 15:30 hard stop; otherwise first block next Lab. Nitesh in-loop on provider choice (API key vs FakeLM vs vLLM).

---
**Signed:** ReputationLearning — 2026-10-01 ~10:55 IST — opened T2 after T1 finished; detailed impl instructions above.
