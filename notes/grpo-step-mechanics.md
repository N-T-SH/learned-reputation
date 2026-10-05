# How one training step works

This note is the mechanics of the short GRPO pilot. It is not a result. The frozen probe file is still the before picture. The pilot has not been interpreted yet.

## The game the step sits on

Eight seats play a public-goods round. Each seat sends a message, names other seats, and contributes between 0 and 1. A pair exists only if both seats name each other. Seats in a pair of at least two share a pot: contributions in the group are multiplied by 1.6 and split evenly. A seat outside the group, or a group of one, gets 0.8 and its own contribution is not a pot. Two seats are scripted. One always contributes 0. One always contributes 0.3. Both name the two highest contributors from the last round. The other six seats are the model.

A round is simultaneous. The prompt shows the last five finished rounds for every seat: contribution and nominations. It does not show what the other seats are doing in this round. Seat labels are a fresh 6-character id each episode, so a habit cannot attach to "seat 7."

## What Fireworks does, and what we do

Fireworks does not run the game. It holds a frozen copy of Qwen 3.8 27B and a small adapter, a LoRA of rank 8. We save that adapter, sample replies from that snapshot, score them, and send the scores back. Fireworks computes the token probabilities and the gradient, then takes one optimizer step on the adapter only. The base weights do not move.

A decision is not one reply. It is a group of four replies to the same prompt, drawn at temperature 0.4, with thinking off in the chat template. Four replies to the same state are what make the baseline. There is no separate value network.

## The reward is the rest of the episode

Each reply is repaired into a message, a nomination list, and a contribution. Broken text becomes an empty nomination and a contribution of 0, and is marked not ok. The reward is not that contribution number. It is the seat's payoffs from this round through the end of the episode, if this reply is the action and the other seats hold the actions they took for the continuing episode.

That timing is the point. Withholding wins the current round and loses the later ones, because the other seats can stop naming a low contributor once the ledger shows it. A same-round payoff would pay the withhold. The return pays the consequence.

The group average is then subtracted from each return. A reply that paid better than the other three gets a positive advantage. A worse one gets a negative one. If all four returns match, every advantage is zero. That group is logged and skipped. An update with no difference would not move the adapter, and the smoke runs showed the frozen model often has no difference: it refuses a visible zero every time.

## The step itself

For a group that differs, each reply becomes a training datum. The datum is the prompt tokens plus the reply tokens. The advantage is applied to the reply tokens, not the prompt. Fireworks runs an importance-sampling loss: it compares the probability of those reply tokens under the current adapter with the probability under the snapshot that produced them, and weights that by the advantage. Then one Adam step. The next round samples from the updated adapter.

Prompt tokens are not trained. A reply that failed repair can still be a datum. Its return will usually be worse, because contribution 0 and no nominations leave the seat on the isolation payoff. That is a usable signal. A group of four identical refusals is not.

## What this pilot is not

Five rounds, one episode, four replies per model decision. That is 120 replies. It checks that a later payoff can move the adapter on this game. It does not show that reputation was learned. A learned change would be a later file, on the same ledger and the same two probes, in which the model names the zero less often than the 0.3 seat, and names that 0.3 seat less often than a seat that contributed. The frozen file is the comparison. In that file the model already names both probes about 3 percent of the time and names another model seat about half the time. It does not separate 0 from 0.3.

Groups with no spread are expected. They are not a failed run. They mean the policy was already sure. The pilot only teaches where the four replies disagreed.
