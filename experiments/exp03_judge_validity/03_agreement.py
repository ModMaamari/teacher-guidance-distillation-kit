#!/usr/bin/env python3
"""Judge validity: human agreement, judge-swap agreement, arm-ranking stability, and the
answer-length confound.

Nothing here calls a model. It reads verdict files that judge.py already wrote plus an
optional human-labelled CSV from 01_sample_for_human.py.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import math
import pathlib
import sys


def arm_of(source: str) -> str:
    parts = pathlib.Path(source).parts
    return parts[-3] if len(parts) >= 3 else "?"


def load(path: pathlib.Path) -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], dict] = {}
    for line in path.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        v = (r.get("verdict") or {}).get("correct")
        if v is None:
            continue
        out[(r["source"], r["qid"])] = {"v": int(v), "arm": arm_of(r["source"]),
                                        "answer": r.get("final_answer", "")}
    return out


def kappa(a: list[int], b: list[int]) -> tuple[float, float]:
    """Cohen's kappa and raw agreement for two binary label lists."""
    n = len(a)
    if n == 0:
        return float("nan"), float("nan")
    obs = sum(1 for x, y in zip(a, b) if x == y) / n
    pa, pb = sum(a) / n, sum(b) / n
    exp = pa * pb + (1 - pa) * (1 - pb)
    k = (obs - exp) / (1 - exp) if exp < 1 else float("nan")
    return k, obs


def rank_arms(v: dict[tuple[str, str], dict]) -> list[tuple[str, float, int]]:
    agg: dict[str, list[int]] = collections.defaultdict(list)
    for rec in v.values():
        agg[rec["arm"]].append(rec["v"])
    rows = [(arm, 100.0 * sum(xs) / len(xs), len(xs)) for arm, xs in agg.items()]
    return sorted(rows, key=lambda r: -r[1])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--primary", default="runs/judge/verdicts.jsonl")
    ap.add_argument("--swap", nargs="*", default=[])
    ap.add_argument("--human", default="")
    a = ap.parse_args()

    p = pathlib.Path(a.primary)
    if not p.exists():
        print(f"!! {p} not found", file=sys.stderr)
        return 1
    prim = load(p)
    print(f"primary judge: {len(prim)} verdicts, {len({r['arm'] for r in prim.values()})} arms\n")

    print("== arm ranking, primary judge")
    base_rank = rank_arms(prim)
    for arm, pct, n in base_rank:
        print(f"   {arm:<16} {pct:6.2f}%  (n={n})")

    for s in a.swap:
        sp = pathlib.Path(s)
        if not sp.exists():
            print(f"\n!! {sp} not found -- skipping")
            continue
        other = load(sp)
        shared = sorted(set(prim) & set(other))
        if not shared:
            print(f"\n!! {sp.parent.name}: no overlapping verdicts")
            continue
        k, obs = kappa([prim[x]["v"] for x in shared], [other[x]["v"] for x in shared])
        print(f"\n== swap: {sp.parent.name}   n={len(shared)}")
        print(f"   agreement {obs:.1%}   kappa {k:.3f}")
        r2 = rank_arms(other)
        order_same = [x[0] for x in base_rank] == [x[0] for x in r2]
        for arm, pct, n in r2:
            print(f"   {arm:<16} {pct:6.2f}%  (n={n})")
        print(f"   ranking {'UNCHANGED' if order_same else 'CHANGED -- report this'}")

    if a.human:
        hp = pathlib.Path(a.human)
        keyp = hp.with_suffix(".key.json")
        if not hp.exists() or not keyp.exists():
            print(f"\n!! need both {hp} and {keyp}", file=sys.stderr)
        else:
            key = {int(r["sample_id"]): r for r in json.loads(keyp.read_text(encoding="utf-8"))}
            hu, ju = [], []
            with hp.open(encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    raw = (row.get("human_correct") or "").strip()
                    if raw not in ("0", "1"):
                        continue
                    k_ = key.get(int(row["sample_id"]))
                    if not k_:
                        continue
                    hu.append(int(raw))
                    ju.append(int(k_["judge"]))
            if not hu:
                print(f"\n== human agreement: no labelled rows yet in {hp}")
            else:
                k, obs = kappa(hu, ju)
                se = 1.96 / math.sqrt(len(hu))
                print(f"\n== human vs primary judge   n={len(hu)}")
                print(f"   agreement {obs:.1%}   kappa {k:.3f}   (+/-{se:.2f} rough 95% band)")
                print("   " + ("defensible (>0.6)" if k > 0.6 else "WEAK -- the judge needs work"))

    print("\n== answer-length confound (primary judge)")
    by = collections.defaultdict(list)
    for rec in prim.values():
        by[rec["v"]].append(len((rec["answer"] or "").split()))
    for v in sorted(by):
        xs = by[v]
        print(f"   judged {'correct' if v else 'wrong  '}: mean {sum(xs)/len(xs):6.1f} words  (n={len(xs)})")
    if len(by) == 2:
        m1 = sum(by[1]) / len(by[1]); m0 = sum(by[0]) / len(by[0])
        print(f"   correct answers are {m1 - m0:+.1f} words longer on average")
        print("   large gaps mean the judge may be rewarding verbosity; report it either way")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
