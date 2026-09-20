#!/usr/bin/env python
"""Do the new benchmarks overlap what our students trained on?

The students are trained on trajectories over HotpotQA, 2WikiMultihopQA, MuSiQue and StrategyQA. A
new benchmark is only an independent test if its questions are not those questions again. This
reuses the contamination test of E07: a rare 8-gram shared between a new question and any training
example is a flag.

    python experiments/exp27_new_benchmarks/leak_check.py
"""
from __future__ import annotations

import collections
import gzip
import json
import re
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
SPLITS = ["data/splits_self/uniform/train.jsonl", "data/splits_selfdist/uniform/train.jsonl"]
NEW = ["multihoprag", "framesqa"]
N = 8


def grams(text: str, n: int = N):
    w = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {" ".join(w[i:i + n]) for i in range(max(len(w) - n + 1, 0))}


def main() -> int:
    train = collections.Counter()
    for rel in SPLITS:
        f = KIT / rel
        if not f.exists():
            continue
        for line in f.open(encoding="utf-8"):
            if line.strip():
                q = (json.loads(line).get("metadata") or {}).get("query", "")
                train.update(grams(q))
    rare = {g for g, k in train.items() if k <= 3}
    print(f"training questions contribute {len(train):,} distinct {N}-grams ({len(rare):,} rare)\n")
    for ds in NEW:
        f = KIT / "data" / "questions" / ds / f"{ds}_questions.jsonl.gz"
        if not f.exists():
            print(f"{ds}: not built yet")
            continue
        n = flagged = 0
        examples = []
        with gzip.open(f, "rt", encoding="utf-8") as fh:
            for line in fh:
                r = json.loads(line)
                n += 1
                hit = grams(r["query"]) & rare
                if hit:
                    flagged += 1
                    if len(examples) < 3:
                        examples.append((r["query"][:70], sorted(hit)[0]))
        print(f"{ds}: {flagged}/{n} questions share a rare {N}-gram with a training question "
              f"({100 * flagged / max(n, 1):.1f}%)")
        for q, g in examples:
            print(f"    e.g. {q!r} shares {g!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
