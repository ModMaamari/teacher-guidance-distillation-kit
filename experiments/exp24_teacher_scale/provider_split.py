#!/usr/bin/env python
"""Are the teacher's rollouts the same whichever gateway served them?

E24's collection was interrupted when the primary gateway's DeepSeek deployment began returning
HTTP 500, and finished through a second gateway serving the same model id. A provider swap is not
free: the appendix already records a teacher run whose accuracy moved when the provider and the
token cap changed. This splits the collected episodes by the model id recorded in their calls and
compares what matters for the experiment -- how often an episode ends correct (that is the filter
that decides what trains the student), how many steps it takes and how many tokens it writes.

    python experiments/exp24_teacher_scale/provider_split.py --episodes data/episodes_teachdist/episodes.jsonl.gz
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]


def provider_of(ep: dict) -> str:
    for s in ep.get("steps") or []:
        for c in s.get("student_calls") or []:
            m = str(c.get("model") or "")
            if m:
                return m.split("/")[0] if "/" in m else m
    return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--episodes", default="data/episodes_teachdist/episodes.jsonl.gz")
    a = ap.parse_args()
    f = KIT / a.episodes
    agg: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    opener = gzip.open if f.suffix == ".gz" else open
    with opener(f, "rt", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            ep = json.loads(line)
            p = agg[provider_of(ep)]
            p["episodes"] += 1
            p["correct"] += bool((ep.get("final_metrics") or {}).get("answer_correct"))
            p["steps"] += len(ep.get("steps") or [])
            for s in ep.get("steps") or []:
                for c in s.get("student_calls") or []:
                    u = c.get("usage") or {}
                    p["in"] += int(u.get("prompt_tokens") or 0)
                    p["out"] += int(u.get("completion_tokens") or 0)

    print(f"{'provider':<16}{'episodes':>10}{'kept by filter':>16}{'steps/ep':>10}{'tokens in':>11}{'tokens out':>12}")
    for name, c in sorted(agg.items(), key=lambda kv: -kv[1]["episodes"]):
        n = c["episodes"]
        print(f"{name:<16}{n:>10,}{100 * c['correct'] / n:>15.1f}%{c['steps'] / n:>10.2f}"
              f"{c['in'] / n:>11,.0f}{c['out'] / n:>12,.0f}")
    if len(agg) > 1:
        rates = {k: v["correct"] / v["episodes"] for k, v in agg.items()}
        lo, hi = min(rates.values()), max(rates.values())
        print(f"\n  keep-rate spread between providers: {100 * (hi - lo):.1f} points. The training split mixes "
              f"them,\n  so a large gap belongs in the write-up as a caveat for this arm.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
