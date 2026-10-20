# For the planning bot, 20 Oct 2026

**Repo:** `N-T-SH/learned-reputation`
**Pre-registration:** `878692c` in `notes/prereg-2026-10-20.md`. Committed before any paid call.
**Status:** Step 1 probes are in. Step 2 game runs have not started. No training.

## Spend

`runs/oct20/spend.jsonl` has call counts only, not dollars.

- Fake dry run: 48 calls, $0.
- Fireworks Qwen 3.8 27B: 240 calls.
- OpenRouter `anthropic/claude-haiku-5.5`: 240 calls. List price $0.10 / $0.50 per 1M tokens.

Cap is $8. Nitesh has the dollar total. Do not open the game runs until that number is known.

## What can be scored

`runs/oct20/probes/summary.csv` is wrong. It scored every variant against the first variant's ids. The rates below are recomputed from each row's own `targets`. Use the jsonl, not that csv.

### Qwen 3.8 27B, Fireworks, thinking off, temperature 0.4

File: `runs/oct20/probes/qwen3.8-27b.jsonl`. 240 calls. Repair: 192 ok, 33 non-JSON, 15 empty.

| Cell | Contrast | Rate |
|---|---|---|
| A1 | same last move, opposite record | Y (all 1s) 0.7, X (four 0s then 1) 0.3 |
| A2 | good record then a 0, vs all 0s | both 0.1 |
| A3 | record and last move conflict | X (good record, bad last) 0.1, Y (bad record, good last) 0.3 |
| A4 | 12-round reformer vs steady | reformer 0.3, steady 0.7 |
| D-neutral | A3 wording | X 0.3, Y 0.2 |
| D-kitchen | kitchen wording | 9 of 10 failed to parse |
| D-game | explicit game words | both 0.0, 5 of 10 failed |

T4, as written, failed on this model. P(named | good record, bad last move) is 0.1. P(named | bad record, good last move) is 0.3. The last move beat the longer record on the conflict cell.

A1 and A4 do show a preference for a clean all-1s record over a record that contains zeros, when the last move is also good. That is not the T4 contrast.

Forgiveness surface, P(named target):

| bad rounds \ good rounds | 1 | 3 | 6 |
|---|---|---|---|
| 2 | 0.5 | 0.5 | 0.5 |
| 6 | 0.4 | 0.5 | 0.7 |
| 12 | 0.2 | 0.4 | 0.5 |

A long bad record with one good round is the lowest cell. There is no clean dose curve. n=10 per cell.

Leading Eight, P(named D):

- Justification, good-record D: refused a bad partner 0.1, included a good partner 0.4. Not "about as often."
- Apology, bad-record D: included a good partner 0.2, did not 0.0. Direction matches. The gap is one or two namings in ten.

### Haiku 5.5, OpenRouter

File: `runs/oct20/probes/anthropic_claude-haiku-5.5.jsonl`. 240 calls. Repair: 9 ok, 5 unknown id, 9 non-JSON, 217 empty.

This is not a behavioral result. 217 replies had empty `content`. The 23 non-empty ones are mostly a cut-off `partners` object or a sentence. T4 cannot be scored on this model. A rerun would need the reader to capture a reasoning field and to send thinking off. Do not treat the zeros as a null on the claim.

## Pre-registered predictions, probes only

- T4: failed on Qwen. Unscorable on Haiku. Not held in both models.
- Leading Eight justification: failed on Qwen.
- Leading Eight apology: direction held on Qwen, n too small to call.
- P1, P3, P4, T1, T2, T3: not tested. Those need the game runs.

## What is not done

Step 2 has not started. No memory-window episode, no fixed-group control, no reformer latency. The harness is `agents/probes/oct20_game.py`. The parse gate is window seed 0: stop the game runs if more than 15 of the first 50 replies fail.

## Recommendation

Do not spend the rest of the $8 on a Haiku rerun unless the interview needs a second model. The Qwen probe file already answers the probe question: on the conflict cell, recency beat the longer record.

If dollars remain, the highest-value next file is one window-5 choice episode, seed 0, as the parse gate. If it passes, the other seven episodes are the pre-registered game comparison. If it fails, stop and report the repair types.

No interpretation beyond held, failed, or unscorable. Nitesh writes that.
