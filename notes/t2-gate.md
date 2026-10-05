# T2 gate — 5 Oct 2026
**File:** `runs/pgg/frozen_qwen_qwen3.8-27b_choice_s8_t0.4_ledger_id6_probe_seed0_n5.jsonl`
**Training:** not started

## What the file shows

Five episodes, twenty rounds, eight seats. Two scripted probes, contribution 0 and 0.3. Six model seats. Ledger of five rounds. Six-character ids. Qwen 3.8 27B, temperature 0.4, reasoning off.

After round 0, a model seat named the zero probe 15/570 times and the 0.3 probe 21/570 times. It named another model seat 1492/2850 times. The zero seat was in the working set 6/100 rounds. The 0.3 seat was in 13/100. A model seat was in 404/600.

Model contributions were 0 to 1, mean 0.63. Only 3 of 600 were below 0.5. Two replies failed repair.

The twelve-hour clock includes a sleep in episode 3. Active time was about 37 minutes.

## Call

The frozen model refuses a clearly low contribution. It does not rank 0 against 0.3. That is enough of a before picture to train against, on this same setup.

Do not train on the older no-ledger file. Do not score a decision with that round's payoff alone. The reward is the seat's return from that round to the end of the episode.

Next is a Fireworks smoke on Qwen 3.8 27B: thinking off, one short GRPO step, reward equal to return-to-go. Not a full pilot until that smoke prices and parses.
