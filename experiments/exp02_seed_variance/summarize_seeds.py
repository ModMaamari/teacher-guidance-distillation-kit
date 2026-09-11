#!/usr/bin/env python3
"""Mean and spread across training seeds, from the table collect_results.py writes.

The bootstrap CI in results.json describes *question* sampling. This describes *training*
randomness, which a single-seed paper does not report at all. Give both.

Reads ``pooled`` (a dict keyed by arm name) and keeps arms called ``seed<N>``.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import statistics as st

SEED_RE = re.compile(r"^seed(\d+)$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="runs/results/results.json")
    ap.add_argument("--metric", default="judge_correct")
    ap.add_argument("--arm-pattern", default=r"^seed(\d+)$",
                    help="regex with one group naming the varying part")
    a = ap.parse_args()

    p = pathlib.Path(a.results)
    if not p.exists():
        print(f"!! {p} not found -- run scripts/collect_results.py first")
        return 1
    pooled = json.loads(p.read_text(encoding="utf-8")).get("pooled", {})
    if not isinstance(pooled, dict):
        print("!! unexpected results.json: 'pooled' is not an object")
        return 1

    rx = re.compile(a.arm_pattern)
    vals: dict[str, float] = {}
    for arm, row in pooled.items():
        m = rx.match(str(arm))
        if not m or row.get(a.metric) is None:
            continue
        v = float(row[a.metric])
        vals[m.group(1)] = v * 100.0 if v <= 1.0 else v

    if not vals:
        print(f"no arms matching {a.arm_pattern!r} with metric {a.metric!r}")
        print("arms present:", ", ".join(sorted(pooled)) or "(none)")
        return 1

    xs = list(vals.values())
    print(f"metric: {a.metric}   arms: {len(xs)}")
    for k in sorted(vals, key=lambda s: (len(s), s)):
        print(f"  {k:<8} {vals[k]:6.2f}")
    mean = st.mean(xs)
    sd = st.stdev(xs) if len(xs) > 1 else 0.0
    print(f"\n  mean {mean:.2f}   sd {sd:.2f}   range {min(xs):.2f}-{max(xs):.2f}")
    if len(xs) > 1:
        print(f"  report as: {mean:.1f} +/- {sd:.1f} (n={len(xs)})")
    else:
        print("  one seed only -- this is the gap exp02 exists to close")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
