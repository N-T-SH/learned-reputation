"""OpenRouter speaker. Returns text, never a dict.

reasoning_off sends both OpenRouter's switch and Qwen's enable_thinking false.
max_tokens caps a reasoning leak. A 400 is not retried.
A successful call does not print. Waits still print.
"""

from __future__ import annotations

import http.client
import json
import os
import time
import urllib.error
import urllib.request

BASE = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openrouter/free"
RETRYABLE = (
    urllib.error.URLError,
    TimeoutError,
    ConnectionError,
    OSError,
    http.client.RemoteDisconnected,
    http.client.IncompleteRead,
    http.client.BadStatusLine,
)


def complete(
    seat: int,
    prompt: str,
    model: str | None = None,
    reasoning_off: bool = True,
    temperature: float = 0.0,
) -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set. FakeLM is the no-key path.")
    chosen = (model or os.environ.get("OPENROUTER_MODEL") or DEFAULT_MODEL).strip()
    body = {
        "model": chosen,
        "temperature": temperature,
        "max_tokens": 200,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Reply with one JSON object only. Keys: message (string), "
                    "nominate (list of integers), contribute (number from 0 to 1). "
                    "No markdown."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }
    if reasoning_off:
        body["reasoning"] = {"enabled": False, "effort": "none"}
        body["chat_template_kwargs"] = {"enable_thinking": False}
    data = json.dumps(body).encode()
    last = "no attempt"
    for attempt in range(8):
        req = urllib.request.Request(
            BASE,
            data=data,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                payload = json.loads(resp.read().decode())
            message = payload["choices"][0]["message"]
            return message.get("content") or ""
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode()[:300]
            if exc.code == 400:
                raise RuntimeError(f"OpenRouter HTTP 400: {detail}") from exc
            if exc.code in (408, 409, 429, 500, 502, 503, 504) and attempt < 7:
                wait = 30 * (attempt + 1) if exc.code == 429 else 2 ** attempt
                print(f"HTTP {exc.code}, waiting {wait}s", flush=True)
                time.sleep(wait)
                last = f"HTTP {exc.code}: {detail}"
                continue
            raise RuntimeError(f"OpenRouter HTTP {exc.code}: {detail}") from exc
        except RETRYABLE as exc:
            last = str(exc)
            if attempt < 7:
                wait = 2 ** attempt
                print(f"connection dropped, waiting {wait}s", flush=True)
                time.sleep(wait)
                continue
            raise RuntimeError(f"OpenRouter connection failed after retries: {last}") from exc
    raise RuntimeError(f"OpenRouter connection failed after retries: {last}")
