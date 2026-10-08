"""The prompt both the Fireworks frozen file and the pilot must use.

The OpenRouter file was a chat call. This is that same ledger block as the
user message, with thinking off. A raw completion of the block does not parse.
"""

from __future__ import annotations


def rendered_prompt(tokenizer, seat: str, env, order: list[str], inbox: list[str]) -> str:
    from envs.pgg_scripted.run_frozen import prompt_for

    body = prompt_for(seat, env, order, inbox)
    body += (
        "\nReply with only the JSON object. nominate is a list of seat ids. "
        "contribute is a number. Keep the message under ten words."
    )
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
