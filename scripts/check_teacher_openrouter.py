#!/usr/bin/env python3
"""Verify the OpenRouter teacher before spending a collection run on it.

Checks, in order: the key has headroom, the model answers when pinned to one provider with
fallbacks off, what the reasoning setting actually did (reasoning bills at the output rate),
and the reply looks like a usable critique. Prints the measured cost per call so the
projected spend for a full collection is grounded in a real request.

    python scripts/check_teacher_openrouter.py
    python scripts/check_teacher_openrouter.py --model z-ai/glm-5.3-flash --provider DeepInfra
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from tgd.openrouter import provider_payload, reasoning_payload  # noqa: E402

CRITIQUE = (
    "You are a teacher reviewing one step of a student's retrieval agent.\n"
    "Question: What nationality was the director of Alien?\n"
    "Student's plan: search for 'Alien', then read the first result.\n"
    "In two sentences, say what is wrong with the plan and what to do instead."
)


def load_env(p: pathlib.Path) -> None:
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def post(url: str, key: str, body: dict | None, timeout: int, attempts: int = 4):
    """POST with backoff on the transient failures.

    A single 429 used to abort this check, and the collection job runs it as a gate -- so
    one rate-limited probe threw away a GPU allocation the job had queued hours for. Rate
    limits and 5xx are retried; everything else fails fast, because a 400 or 401 will not
    fix itself.
    """
    data = json.dumps(body).encode() if body is not None else None
    delay = 3.0
    for i in range(attempts):
        req = urllib.request.Request(url, data=data, headers={
            "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (408, 429, 500, 502, 503, 504) and i < attempts - 1:
                wait = float(e.headers.get("Retry-After") or delay)
                print(f"  transient HTTP {e.code}; retrying in {wait:.0f}s "
                      f"({i + 1}/{attempts - 1})")
                time.sleep(wait)
                delay *= 2
                continue
            raise
        except (TimeoutError, OSError) as e:
            if i < attempts - 1:
                print(f"  transient {type(e).__name__}; retrying in {delay:.0f}s")
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("unreachable")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="z-ai/glm-5.3-flash")
    ap.add_argument("--provider", default=os.environ.get("OPENROUTER_PROVIDER_ONLY", "DeepInfra"))
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--reasoning", default=os.environ.get("OPENROUTER_REASONING", ""),
                    help="off|minimal|low|medium|high|exclude; must match the run's setting")
    ap.add_argument("--episodes", type=int, default=7999,
                    help="episode count to project cost for")
    a = ap.parse_args()

    load_env(pathlib.Path(__file__).resolve().parents[1] / ".env")
    base = (os.environ.get("CUSTOM_LLM_ENDPOINT") or "https://openrouter.ai/api").rstrip("/")
    key = os.environ.get("CUSTOM_LLM_API_KEY", "")
    if not key:
        print("!! CUSTOM_LLM_API_KEY not set (see .env)", file=sys.stderr)
        return 2

    print(f"endpoint {base}   model {a.model}   provider {a.provider or '(any)'}")

    # 1. key headroom
    try:
        d = post(base + "/v1/key", key, None, 60)["data"]
        lim, used = d.get("limit"), d.get("usage", 0)
        rem = d.get("limit_remaining")
        print(f"  key: used ${used:.2f}" + (f" of ${lim:.2f} limit, ${rem:.2f} left" if lim else ", no key limit"))
        if lim is not None and (rem or 0) <= 0:
            print("  !! this key is capped out -- raise its limit or make a new key at")
            print("     https://openrouter.ai/workspaces/default/keys")
            return 1
    except Exception as e:
        print(f"  key check failed: {type(e).__name__}: {str(e)[:60]}")

    # 2. a real critique, pinned, with whatever reasoning mode the run will use.
    # This must mirror the client exactly: asking to disable reasoning on a model that
    # mandates it answers 400, and this check gates the collection job.
    body = {"model": a.model,
            "messages": [{"role": "user", "content": CRITIQUE}],
            "max_tokens": 600, "temperature": 0.1, "usage": {"include": True}}
    if a.provider:
        body["provider"] = provider_payload(a.provider)
    reason = reasoning_payload(a.reasoning)
    if reason:
        body["reasoning"] = reason
    mode = (a.reasoning or "").strip().lower()
    print(f"  reasoning mode: {mode or '(model default)'}")

    t0 = time.time()
    try:
        d = post(base + "/v1/chat/completions", key, body, a.timeout)
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read()).get("error", {}).get("message", "")
        except Exception:
            msg = ""
        print(f"  !! HTTP {e.code}: {str(msg)[:90]}")
        return 1
    except Exception as e:
        print(f"  !! {type(e).__name__}: {str(e)[:70]}")
        return 1
    dt = time.time() - t0

    if "error" in d:
        print(f"  !! {str(d['error'])[:110]}")
        return 1
    m = d["choices"][0]["message"]
    u = d.get("usage") or {}
    content = (m.get("content") or "").strip()
    thinking = m.get("reasoning") or m.get("reasoning_content")

    print(f"  served by : {d.get('provider', '?')}")
    print(f"  latency   : {dt:.2f}s   in {u.get('prompt_tokens', 0)} / out {u.get('completion_tokens', 0)} tokens")
    print(f"  reasoning : {'on (billed as output)' if thinking else 'none returned'}")
    print(f"  cost/call : ${u.get('cost', 0):.6f}" if u.get("cost") is not None else "  cost/call : not reported")
    print(f"  critique  : {content[:96]!r}")

    # A mandatory-reasoning model is fine; an empty critique is not.
    ok = bool(content)
    if a.provider and str(d.get("provider", "")).lower() != a.provider.lower():
        print(f"  !! served by {d.get('provider')}, not {a.provider}")
        ok = False
    if not content:
        print("  !! empty content")
    if u.get("cost"):
        # The probe prompt is short; a real critique prompt is ~1,600 input tokens, so this
        # projection understates the run. Measured on real prompts from the shipped
        # episodes, glm-5.3-flash at low effort costs ~$0.00017/call, about $7.4 for 8k
        # episodes. Treat the number below as a lower bound.
        print(f"\n  lower bound from this short probe: "
              f"${u['cost'] * 5.36 * a.episodes:.2f} for {a.episodes:,} episodes")
        print("  (real critique prompts are ~10x longer; budget ~$7-8 for the full set)")
    print("\n" + ("READY" if ok else "NOT READY"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
