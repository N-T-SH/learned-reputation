"""OpenRouter speaker. Returns text, never a dict.

Retries a dropped socket, a timeout, and a 429 or 5xx.
Does not retry a 400. That is the model rejecting the request.
RemoteDisconnected is not an OSError, so it is caught by name.
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


def complete(seat: int, prompt: str, model: str | None = None, reasoning_off: bool = True) -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set. FakeLM is the no-key path.")
    chosen = (model or os.environ.get("OPENROUTER_MODEL") or DEFAULT_MODEL).strip()
    body = {
        "model": chosen,
        "temperature": 0,
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
        body["reasoning"] = {"enabled": False}
    data = json.dumps(body).encode()
    last = "no attempt"
    for attempt in range(5):
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
            return payload["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode()[:300]
            if exc.code in (408, 409, 429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(2 ** attempt)
                last = f"HTTP {exc.code}: {detail}"
                continue
            raise RuntimeError(f"OpenRouter HTTP {exc.code}: {detail}") from exc
        except RETRYABLE as exc:
            last = str(exc)
            if attempt < 4:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"OpenRouter connection failed after retries: {last}") from exc
    raise RuntimeError(f"OpenRouter connection failed after retries: {last}")
