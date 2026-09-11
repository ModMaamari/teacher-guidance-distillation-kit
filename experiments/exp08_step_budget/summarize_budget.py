#!/usr/bin/env python3
"""Accuracy and cost against step budget, from arms named ``<arm>_b<budget>``."""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

ARM_RE = re.compile(r"^(?P<arm>.+)_b(?P<budget>\d+)$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="runs/results/results.json")
    ap.add_argument("--metric", default="judge_correct")
    a = ap.parse_args()

    p = pathlib.Path(a.results)
    if not p.exists():
        print(f"!! {p} not found -- run collect_results.py first", file=sys.stderr)
        return 1
    pooled = json.loads(p.read_text(encoding="utf-8")).get("pooled", {})

    table: dict[str, dict[int, dict]] = collections.defaultdict(dict)
    for name, row in pooled.items():
        m = ARM_RE.match(str(name))
        if m and row.get(a.metric) is not None:
            table[m.group("arm")][int(m.group("budget"))] = row
    if not table:
        print("no arms named <arm>_b<budget>; arms present:", ", ".join(sorted(pooled)))
        return 1

    budgets = sorted({b for v in table.values() for b in v})
    print(f"metric: {a.metric}   (steps used / tokens per episode in brackets)\n")
    print("  " + "arm".ljust(16) + "".join(f"b={b}".rjust(22) for b in budgets))
    for arm in sorted(table):
        cells = []
        for b in budgets:
            r = table[arm].get(b)
            if not r:
                cells.append("-".rjust(22)); continue
            v = float(r[a.metric]); v = v * 100 if v <= 1 else v
            cells.append(f"{v:5.1f}% [{r.get('mean_steps', 0):.2f}/{r.get('total_tokens_per_ep', 0):,.0f}]".rjust(22))
        print("  " + arm.ljust(16) + "".join(cells))

    print("\nreading: a student that gains with budget is stopping too early, not retrieving badly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
