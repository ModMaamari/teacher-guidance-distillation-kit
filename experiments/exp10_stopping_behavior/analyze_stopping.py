#!/usr/bin/env python3
"""Why each arm stopped, and whether stopping voluntarily predicts being right.

Reads the episode files eval.py writes. No models, no API, no GPU.
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import pathlib
import sys


def arm_of(p: pathlib.Path) -> str:
    return p.parts[-3] if len(p.parts) >= 3 else "?"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs/eval")
    ap.add_argument("--judge", default="runs/judge/verdicts.jsonl")
    a = ap.parse_args()

    files = sorted(glob.glob(str(pathlib.Path(a.runs) / "*" / "*" / "episodes.jsonl")))
    if not files:
        print(f"!! no episodes under {a.runs}", file=sys.stderr)
        return 1

    verdict: dict[tuple[str, str], int] = {}
    jp = pathlib.Path(a.judge)
    if jp.exists():
        for line in jp.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            v = (r.get("verdict") or {}).get("correct")
            if v is not None:
                verdict[(str(pathlib.Path(r["source"]).resolve()), r["qid"])] = int(v)   # match the lookup below

    reasons: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    steps: dict[str, list[int]] = collections.defaultdict(list)
    by_reason_correct: dict[str, dict[str, list[int]]] = collections.defaultdict(
        lambda: collections.defaultdict(list))

    for f in files:
        p = pathlib.Path(f)
        arm = arm_of(p)
        for line in p.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            r = str(e.get("stop_reason") or "?")
            reasons[arm][r] += 1
            fm = e.get("final_metrics") or {}
            # eval.py records the step count as used_steps; "steps" is the list of step records
            n_steps = e.get("used_steps")
            if n_steps is None:
                n_steps = len(e["steps"]) if isinstance(e.get("steps"), list) else fm.get("steps", 0)
            steps[arm].append(int(n_steps or 0))
            key = (str(p.resolve()), e["qid"])
            c = verdict.get(key)
            if c is None:
                c = int(bool(fm.get("cover_match")))
            by_reason_correct[arm][r].append(c)

    src = "judge" if verdict else "cover-match (no verdicts found)"
    n_cover = sum(1 for f in files for line in open(f, encoding="utf-8") if line.strip()
                  and (str(pathlib.Path(f).resolve()), json.loads(line)["qid"]) not in verdict)
    if verdict and n_cover:
        src += f" ({n_cover} episodes without a verdict fall back to cover-match)"
    print(f"accuracy source: {src}\n")
    for arm in sorted(reasons):
        tot = sum(reasons[arm].values())
        mean_steps = sum(steps[arm]) / max(len(steps[arm]), 1)
        print(f"== {arm}   n={tot}   mean steps {mean_steps:.2f}")
        for r, c in reasons[arm].most_common():
            xs = by_reason_correct[arm][r]
            acc = 100.0 * sum(xs) / len(xs) if xs else float("nan")
            print(f"   {r:<22} {c:>5} ({100.0 * c / tot:5.1f}%)   accuracy {acc:5.1f}%")
        # voluntary = the agent (or, guided, its teacher) ended the episode before the budget did
        vol = [r for r in reasons[arm] if "budget" not in r.lower() and "error" not in r.lower() and r != "?"]
        nvol = sum(reasons[arm][r] for r in vol)
        if vol:
            print(f"   voluntary finish: {100.0 * nvol / tot:.1f}%  (reasons: {', '.join(sorted(vol))})")
        print()

    print("If voluntary-stop accuracy is far above budget-exhausted accuracy, the stopping")
    print("gap is worth points, and exp10 step 2 estimates how many before you spend a GPU.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
