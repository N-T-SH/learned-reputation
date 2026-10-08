"""The prompt both the Fireworks frozen file and the pilot must use.

The OpenRouter file was a chat call. This is that same ledger block as the
user message, with thinking off. A raw completion of the block does not parse.
"""

from __future__ import annotations


def rendered_prompt(tokenizer, seat: str, env, order: list[str], inbox: list[str]) -> str:
    from envs.pgg_scripted.run_frozen import prompt_for

    messages = [{"role": "user", "content": prompt_for(seat, env, order, inbox)}]
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
