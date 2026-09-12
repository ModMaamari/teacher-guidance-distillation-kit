#!/usr/bin/env python3
"""Did the student's steps actually parse into actions?

The harness records a step whose output it could not parse as an action with no tool. That
is easy to miss: the episode still finishes, still gets an answer, and only the invalid
step count shows it. On granite-4.2-3b every middle step failed this way -- the model spent
its token budget on reasoning prose and was truncated before the JSON -- against 0.0% over
8,687 steps for granite-4.1-3b, whose template does not reason.

    python scripts/check_student_actions.py --runs runs/collect_studenttest
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
import pathlib
import sys


def iter_episodes(root: pathlib.Path):
    for f in root.rglob("teacher_guidance_episodes.jsonl"):
        with f.open(encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    yield json.loads(line)
    for f in list(root.rglob("episodes.jsonl.gz")) + list(root.rglob("episodes.jsonl")):
        op = gzip.open if f.suffix == ".gz" else open
        with op(f, "rt", encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    yield json.loads(line)


def tool_of(step: dict) -> str:
    sa = step.get("student_action") or {}
    act = sa.get("action") if isinstance(sa.get("action"), dict) else sa
    return (act or {}).get("tool") or ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs/collect_studenttest")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-invalid-pct", type=float, default=1.0,
                    help="fail above this percentage of unparsed steps")
    a = ap.parse_args()

    root = pathlib.Path(a.runs)
    if not root.exists():
        print(f"!! {root} not found", file=sys.stderr)
        return 1

    per_pos = collections.Counter()
    tot_pos = collections.Counter()
    tools = collections.Counter()
    stops = collections.Counter()
    n = bad = tot = 0
    truncated = 0
    for ep in iter_episodes(root):
        n += 1
        stops[str(ep.get("stop_reason"))] += 1
        for i, s in enumerate(ep.get("steps") or []):
            t = tool_of(s)
            tot += 1
            tot_pos[i] += 1
            tools[t or "(unparsed)"] += 1
            if not t:
                bad += 1
                per_pos[i] += 1
                raw = str(s.get("student_raw") or "")
                if raw and not raw.rstrip().endswith(("}", "]")):
                    truncated += 1
        if a.limit and n >= a.limit:
            break

    if not tot:
        print(f"!! no steps found under {root}", file=sys.stderr)
        return 1

    pct = 100.0 * bad / tot
    print(f"episodes {n}   steps {tot}   unparsed {bad} ({pct:.1f}%)")
    print("\n  by step position:")
    for i in sorted(tot_pos):
        b = per_pos.get(i, 0)
        print(f"    step {i}: {b}/{tot_pos[i]} unparsed ({100.0 * b / tot_pos[i]:5.1f}%)")
    print("\n  tools chosen:")
    for t, c in tools.most_common():
        print(f"    {t:<14}{c:>6}")
    print("\n  stop reasons:")
    for t, c in stops.most_common():
        print(f"    {t:<24}{c:>6}")
    if bad:
        print(f"\n  {truncated}/{bad} unparsed steps ended mid-token -- that is truncation,")
        print("  not a malformed reply. Switch the student's thinking off")
        print('  (VLLM_CHAT_TEMPLATE_KWARGS={"enable_thinking": false}) or raise max_tokens.')
    verdict = "OK" if pct <= a.max_invalid_pct else "TOO MANY UNPARSED STEPS"
    print(f"\n{verdict} (threshold {a.max_invalid_pct}%)")
    return 0 if pct <= a.max_invalid_pct else 1


if __name__ == "__main__":
    raise SystemExit(main())
