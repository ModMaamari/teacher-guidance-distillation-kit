#!/usr/bin/env python3
"""Does the result survive dropping the test questions the contamination check flagged?

Judge accuracy per arm on all questions and without the flagged ones, and the paired change
between two arms both ways. Reads the evaluation episodes, a verdicts file from judge.py and
the list written by ``contamination_check.py --flagged-out``.

    python exclude_flagged.py --runs runs/e00/eval --verdicts runs/judge/e00/verdicts.jsonl \
        --flagged runs/results/E07/flagged.json --pair base trained
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", required=True, help="<runs>/<arm>/<test-set>/episodes.jsonl")
    ap.add_argument("--verdicts", required=True)
    ap.add_argument("--flagged", required=True)
    ap.add_argument("--pair", nargs=2, default=["base", "trained"], metavar=("A", "B"))
    a = ap.parse_args()

    flagged = {f["id"] for f in json.loads(pathlib.Path(a.flagged).read_text(encoding="utf-8"))}
    verdict = {}
    for line in open(a.verdicts, encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            if (r.get("verdict") or {}).get("correct") is not None:
                verdict[(str(pathlib.Path(r["source"]).resolve()), r["qid"])] = int(r["verdict"]["correct"])
    per_arm: dict[str, dict[str, int]] = collections.defaultdict(dict)
    for f in sorted(pathlib.Path(a.runs).glob("*/*/episodes.jsonl")):
        arm = f.parent.parent.name
        for line in open(f, encoding="utf-8"):
            if line.strip():
                e = json.loads(line)
                v = verdict.get((str(f.resolve()), e["qid"]))
                if v is not None:
                    per_arm[arm][e["qid"]] = v

    print(f"flagged questions: {len(flagged)}\n")
    print(f"{'arm':<12} {'all':>14} {'without flagged':>18} {'flagged only':>14}")
    for arm, v in sorted(per_arm.items()):
        keep = [x for q, x in v.items() if q not in flagged]
        only = [x for q, x in v.items() if q in flagged]
        pct = lambda xs: f"{100 * sum(xs) / len(xs):5.1f}% (n={len(xs)})" if xs else "—"  # noqa: E731
        print(f"{arm:<12} {pct(list(v.values())):>14} {pct(keep):>18} {pct(only):>14}")
    A, B = (per_arm.get(x, {}) for x in a.pair)
    both = sorted(set(A) & set(B))
    for label, qs in (("all", both), ("without flagged", [q for q in both if q not in flagged])):
        if qs:
            d = 100 * (sum(B[q] for q in qs) - sum(A[q] for q in qs)) / len(qs)
            print(f"\n{a.pair[0]} -> {a.pair[1]}, {label}: {d:+.1f} points on {len(qs)} paired questions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
