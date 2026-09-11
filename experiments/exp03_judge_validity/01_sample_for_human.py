#!/usr/bin/env python3
"""Draw a blind, stratified sample of judged answers for a human to label.

The annotator must not be able to tell which arm produced an answer or what the judge
said, or the agreement number is worthless. This writes only question / gold / answer,
shuffled, with an empty ``human_correct`` column to fill in.

Stratifies by (arm, judge verdict) so agreement is measured on both the easy and the
contested regions rather than only where the judge was confident.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import pathlib
import random
import sys


def arm_of(source: str) -> str:
    """runs/eval/<arm>/<test-set>/episodes.jsonl -> <arm>"""
    parts = pathlib.Path(source).parts
    return parts[-3] if len(parts) >= 3 else "?"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verdicts", default="runs/judge/verdicts.jsonl")
    ap.add_argument("--out", default="runs/judge/human_sample.csv")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()

    src = pathlib.Path(a.verdicts)
    if not src.exists():
        print(f"!! {src} not found -- run scripts/judge.py first", file=sys.stderr)
        return 1

    cells: dict[tuple[str, int], list[dict]] = collections.defaultdict(list)
    total = 0
    for line in src.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        v = (r.get("verdict") or {}).get("correct")
        if v is None:
            continue
        total += 1
        cells[(arm_of(r["source"]), int(v))].append(r)

    if not cells:
        print("!! no usable verdicts", file=sys.stderr)
        return 1

    rng = random.Random(a.seed)
    per = max(1, a.n // len(cells))
    picked: list[dict] = []
    for key in sorted(cells):
        rows = cells[key]
        rng.shuffle(rows)
        picked += rows[:per]
    rng.shuffle(picked)

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["sample_id", "question", "gold_answer", "model_answer", "human_correct"])
        for i, r in enumerate(picked):
            w.writerow([i, r.get("query", ""), r.get("gold_answer", ""),
                        r.get("final_answer", ""), ""])

    key = out.with_suffix(".key.json")
    key.write_text(json.dumps(
        [{"sample_id": i, "source": r["source"], "qid": r["qid"],
          "arm": arm_of(r["source"]), "judge": int(r["verdict"]["correct"])}
         for i, r in enumerate(picked)], indent=2), encoding="utf-8")

    print(f"{total} verdicts, {len(cells)} (arm, verdict) cells, {per} per cell")
    print(f"wrote {out}  ({len(picked)} rows to label)")
    print(f"wrote {key}  <- the un-blinding key; do NOT show it to the annotator")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
