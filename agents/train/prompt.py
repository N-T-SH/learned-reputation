"""The prompt both the Fireworks frozen file and the pilot must use.

The OpenRouter file was a chat call. This is that same ledger block as the
user message, with thinking off. A raw completion of the block does not parse.

v2 is the 20 Oct harness only. It does not change prompt_for.
"""

from __future__ import annotations

RULES = (
    "Rules. Each round every seat has one unit and chooses how much of it to put in, from 0 to 1.\n"
    "Under partners, list the seats you want to work with. A pair forms only when both seats list each other.\n"
    "Every seat in at least one pair joins the working group for that round.\n"
    "The working group's inputs are added, multiplied by 1.6, and shared equally among its members.\n"
    "A member also keeps whatever it did not put in. A seat in no pair gets 0.8 for the round."
)


def rendered_prompt(tokenizer, seat: str, env, order: list[str], inbox: list[str], extra: str = "") -> str:
    from envs.pgg_scripted.run_frozen import prompt_for

    body = prompt_for(seat, env, order, inbox)
    body += (
        "\nReply with only the JSON object. nominate is a list of seat ids. "
        "contribute is a number. Keep the message under ten words."
    )
    if extra:
        body += "\n" + extra
    return _template(tokenizer, body)


def v2_body(seat: str, env, order: list[str], extra: str = "") -> str:
    lines = [
        f"You are seat {seat}.",
        RULES,
        "Reply with a JSON object with keys message, partners, contribute.",
        "Recent rounds, newest last. c is contribution. partners is who that seat listed.",
    ]
    if not env.history:
        lines.append("  (no prior round)")
    for round_i, item in enumerate(env.history, start=1):
        lines.append(f"  round {round_i}")
        for sid in order:
            lines.append(f"    seat {sid}: c={item['c'][sid]} partners={item['nom'][sid]}")
    lines.append("Messages from the previous round:")
    lines.append("  (none)")
    if extra:
        lines.append(extra)
    lines.append(
        "Reply with only the JSON object. partners is a list of seat ids. "
        "contribute is a number. Keep the message under ten words."
    )
    return "\n".join(lines)


def rendered_prompt_v2(tokenizer, seat: str, env, order: list[str], extra: str = "") -> str:
    return _template(tokenizer, v2_body(seat, env, order, extra))


def _template(tokenizer, body: str) -> str:
    messages = [{"role": "user", "content": body}]
    try:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
    except TypeError:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
