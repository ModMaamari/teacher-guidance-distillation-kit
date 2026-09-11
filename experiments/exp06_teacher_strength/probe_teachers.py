#!/usr/bin/env python3
"""Confirm each candidate teacher answers, before committing to a collection run.

Reports whether a model puts its chain-of-thought in ``reasoning_content``: those need a
large ``--teacher-max-tokens`` or the critique budget is spent thinking and ``content``
comes back empty, which looks like a broken model but is not.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

PROMPT = "Critique in one sentence: 'Search the director, then his birth year.'"


def probe(base: str, key: str, model: str, timeout: int) -> str:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": 400, "temperature": 0.1,
    }).encode()
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read()).get("error", {}).get("message", "")
        except Exception:
            msg = ""
        return f"FAIL http {e.code}: {str(msg)[:60]}"
    except Exception as e:
        return f"FAIL {type(e).__name__}: {str(e)[:60]}"
    if "error" in d:
        return f"FAIL {str(d['error'].get('message', d['error']))[:64]}"
    try:
        m = d["choices"][0]["message"]
    except Exception:
        return "FAIL malformed response"
    content = (m.get("content") or "").strip()
    reasoning = "yes" if m.get("reasoning_content") else "no "
    if not content:
        return f"EMPTY content (reasoning={reasoning}) -- raise --teacher-max-tokens"
    return f"ok  reasoning={reasoning}  {len(content):>4}ch"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=os.environ.get("OAI_TEACHER_BASE_URL")
                    or os.environ.get("OAI_BASE_URL", ""))
    ap.add_argument("--api-key", default=os.environ.get("OAI_TEACHER_API_KEY")
                    or os.environ.get("OAI_API_KEY", ""))
    ap.add_argument("--timeout", type=int, default=90)
    ap.add_argument("models", nargs="+")
    a = ap.parse_args()

    if not a.base_url:
        print("!! no base url: set OAI_TEACHER_BASE_URL in .env or pass --base-url",
              file=sys.stderr)
        return 2
    print(f"endpoint: {a.base_url}")
    bad = 0
    for m in a.models:
        r = probe(a.base_url, a.api_key, m, a.timeout)
        print(f"  {m:<52} {r}")
        if r.startswith(("FAIL", "EMPTY")):
            bad += 1
    print(f"\n{len(a.models)} probed, {bad} unusable")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
