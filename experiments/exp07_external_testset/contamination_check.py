#!/usr/bin/env python3
"""N-gram overlap between held-out test questions and the training examples.

scripts/check_leakage.py guarantees no question id is in both splits. This is the softer
check a reviewer actually means by "contamination": the same fact asked in other words.
Reports, per test set, how many test questions share a rare n-gram with any training text.
"""
from __future__ import annotations

import argparse
import glob
import gzip
import json
import pathlib
import re
import sys
from collections import Counter

WORD = re.compile(r"[a-z0-9]+")


def toks(s: str) -> list[str]:
    return WORD.findall((s or "").lower())


def grams(words: list[str], n: int) -> set[str]:
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def read_any(p: pathlib.Path):
    op = gzip.open if p.suffix == ".gz" else open
    with op(p, "rt", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="data/splits/uniform")
    ap.add_argument("--test", default="data/splits/test/heldout_*_questions.jsonl")
    ap.add_argument("--n", type=int, default=8, help="n-gram length")
    ap.add_argument("--max-df", type=int, default=3,
                    help="ignore n-grams appearing in more than this many training rows")
    ap.add_argument("--flagged-out", default="",
                    help="write the flagged test questions (id, test set, overlap) as JSON, for exclude_flagged.py")
    a = ap.parse_args()

    train = pathlib.Path(a.split) / "train.jsonl"
    if not train.exists():
        print(f"!! {train} not found -- run 'make data'", file=sys.stderr)
        return 1

    df: Counter[str] = Counter()
    rows = 0
    for rec in read_any(train):
        parts = [m.get("content", "") for m in rec.get("prompt", []) if isinstance(m, dict)]
        c = rec.get("completion")
        if isinstance(c, list):
            parts += [m.get("content", "") for m in c if isinstance(m, dict)]
        elif isinstance(c, dict):
            parts.append(c.get("content", ""))
        g = grams(toks(" ".join(parts)), a.n)
        rows += 1
        for x in g:
            df[x] += 1
    rare = {g for g, c in df.items() if c <= a.max_df}
    print(f"training rows {rows}   distinct {a.n}-grams {len(df)}   rare (df<={a.max_df}) {len(rare)}\n")

    files = sorted(glob.glob(a.test))
    if not files:
        print(f"!! nothing matched {a.test}", file=sys.stderr)
        return 1
    worst: list[tuple[float, str, str]] = []
    flagged: list[dict] = []
    for f in files:
        p = pathlib.Path(f)
        hits = tot = 0
        for q in read_any(p):
            text = q.get("question") or q.get("query") or ""
            g = grams(toks(text), a.n)
            tot += 1
            if g & rare:
                hits += 1
                worst.append((len(g & rare) / max(len(g), 1), p.stem, text[:70]))
                flagged.append({"id": q.get("id") or q.get("qid"), "test_set": p.stem.replace("_questions", ""),
                                "overlap": round(len(g & rare) / max(len(g), 1), 4)})
        pct = 100.0 * hits / max(tot, 1)
        flag = "  <-- look at these" if pct > 5 else ""
        print(f"  {p.stem:<34} {hits:>4}/{tot:<5} ({pct:5.2f}%){flag}")

    if a.flagged_out:
        pathlib.Path(a.flagged_out).write_text(json.dumps(flagged, indent=1), encoding="utf-8")
    worst.sort(reverse=True)
    if worst:
        print("\nhighest-overlap test questions:")
        for frac, ds, text in worst[:8]:
            print(f"  {frac:5.1%}  {ds:<28} {text}")
    print("\nA small non-zero number is normal and worth reporting. A large one on a single")
    print("dataset usually means shared source documents, not a broken split.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
