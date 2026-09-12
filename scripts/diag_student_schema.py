#!/usr/bin/env python3
"""Isolate why a served student returns empty completions.

Sends one realistic student prompt four ways -- with and without the action JSON schema,
with and without the chat template's thinking block -- against a running vLLM server. The
cell that comes back empty names the cause.

    python scripts/diag_student_schema.py --server-url http://127.0.0.1:8311
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

PROMPT = (
    "You are a retrieval agent. Question: Who directed Alien?\n"
    "Available tools: search(query,k), finish(answer,citations).\n"
    "Reply with a JSON object: {\"thought\": str, \"action\": {\"tool\": str, \"params\": obj}}"
)

SCHEMA = {
    "type": "object",
    "properties": {
        "thought": {"type": "string"},
        "action": {
            "type": "object",
            "properties": {"tool": {"type": "string"},
                           "params": {"type": "object"}},
            "required": ["tool", "params"],
        },
    },
    "required": ["thought", "action"],
}


def call(url: str, body: dict, timeout: int):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read()[:120].decode(errors='replace')}"
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:80]}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--server-url", default="http://127.0.0.1:8311")
    ap.add_argument("--served-model", default="student")
    ap.add_argument("--max-tokens", type=int, default=1200)
    ap.add_argument("--timeout", type=int, default=240)
    a = ap.parse_args()

    url = a.server_url.rstrip("/") + "/v1/chat/completions"
    print(f"{'schema':<8}{'thinking':<10}{'status':<10}{'len':>6}{'finish':>12}  head")
    worst = 0
    for schema in (False, True):
        for thinking in (True, False):
            body = {"model": a.served_model,
                    "messages": [{"role": "user", "content": PROMPT}],
                    "max_tokens": a.max_tokens, "temperature": 0.2}
            if schema:
                body["response_format"] = {"type": "json_schema",
                                           "json_schema": {"name": "response", "schema": SCHEMA}}
            if not thinking:
                body["chat_template_kwargs"] = {"enable_thinking": False}
            d, err = call(url, body, a.timeout)
            if err:
                print(f"{str(schema):<8}{str(thinking):<10}{'ERROR':<10}{'':>6}{'':>12}  {err}")
                worst = 2
                continue
            m = d["choices"][0]["message"]
            fin = d["choices"][0].get("finish_reason")
            c = (m.get("content") or "")
            status = "ok" if c.strip() else "EMPTY"
            if status == "EMPTY":
                worst = max(worst, 1)
            print(f"{str(schema):<8}{str(thinking):<10}{status:<10}{len(c):>6}{str(fin):>12}  {c[:46]!r}")

    print("\nreading:")
    print("  empty only when schema=True  -> structured output is the problem")
    print("  empty only when thinking=False -> the template needs its reasoning block")
    print("  empty in both schema rows    -> the grammar and this template cannot coexist")
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
