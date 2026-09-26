#!/usr/bin/env python
"""Build the compute-matched unguided training sets from k sampled attempts per question.

Self-Guidance spends about three times the per-episode compute of a plain unguided rollout
(0.099 vs 0.032 PFLOPs, E23). The fair question is therefore not "self-guided vs one unguided
attempt" but "self-guided vs the same compute spent on more unguided attempts", which is what
rejection-sampling self-training (ReST-EM style) would do. Three ways to spend it:

  all     every attempt that passes the correctness filter (most data, duplicate questions)
  first   the first correct attempt per question (question coverage, no duplicates)
  match   a random subset of `first` with as many correct episodes as the self-guided split

Writes merged episode files that scripts/build_splits.py then turns into splits, and reports
pass@k: the share of trainable questions solved at least once, for k = 1, 2, 3 and for the
self-guided collection.

    python experiments/exp30_compute_matched/pick_attempts.py --out-root data --target 3818
"""
from __future__ import annotations

import argparse
import gzip
import json
import random
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))
from tgd.splits import DEFAULT_SALT, pool_of  # noqa: E402


def read(path: Path):
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def correct(ep) -> bool:
    return bool((ep.get("final_metrics") or {}).get("answer_correct"))


def write(path: Path, episodes) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        for ep in episodes:
            fh.write(json.dumps(ep, ensure_ascii=False) + "\n")
            n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--attempts", nargs="+",
                    default=["data/episodes_selfdist/episodes.jsonl.gz",
                             "data/episodes_selfdist_a2/episodes.jsonl.gz",
                             "data/episodes_selfdist_a3/episodes.jsonl.gz"])
    ap.add_argument("--self-guided", default="data/episodes_self/episodes.jsonl.gz")
    ap.add_argument("--out-root", default="data")
    ap.add_argument("--target", type=int, default=3818, help="correct episodes the matched variant keeps")
    ap.add_argument("--seed", type=int, default=30)
    a = ap.parse_args()

    attempts = []
    for rel in a.attempts:
        p = KIT / rel
        if not p.exists():
            print(f"!! missing attempt file {rel}")
            return 1
        attempts.append(list(read(p)))
        print(f"{rel}: {len(attempts[-1]):,} episodes, {sum(map(correct, attempts[-1])):,} correct")

    trainable = lambda ep: pool_of(str(ep.get("qid")), 0.10, DEFAULT_SALT) == "trainable"  # noqa: E731
    solved: list[set] = []
    for k, eps in enumerate(attempts, 1):
        solved.append({str(e["qid"]) for e in eps if correct(e) and trainable(e)})
    allq = {str(e["qid"]) for e in attempts[0] if trainable(e)}
    cum = set()
    print(f"\npass@k over {len(allq):,} trainable questions:")
    for k in range(len(attempts)):
        cum |= solved[k]
        print(f"  k={k + 1}: {len(cum):,} solved at least once ({100 * len(cum) / len(allq):.1f} %)")
    sg = {str(e["qid"]) for e in read(KIT / a.self_guided) if correct(e) and trainable(e)}
    print(f"  self-guided (k=1): {len(sg):,} ({100 * len(sg) / len(allq):.1f} %)")
    print(f"  solved by self-guidance but not by {len(attempts)} unguided attempts: {len(sg - cum):,}")
    print(f"  solved by unguided attempts but not by self-guidance: {len(cum - sg):,}")

    out = Path(a.out_root)
    every = [ep for eps in attempts for ep in eps]
    n = write(out / "episodes_k3_all" / "episodes.jsonl.gz", every)
    print(f"\nall:   {n:,} episodes written ({sum(map(correct, every)):,} correct)")

    first, seen = [], set()
    for eps in attempts:                       # attempt order is the sampling order
        for ep in eps:
            q = str(ep.get("qid"))
            if correct(ep) and q not in seen:
                seen.add(q)
                first.append(ep)
    n = write(out / "episodes_k3_first" / "episodes.jsonl.gz", first)
    print(f"first: {n:,} episodes written (one correct attempt per solved question)")

    train_first = [ep for ep in first if trainable(ep)]
    rng = random.Random(a.seed)
    rng.shuffle(train_first)
    keep = {id(ep) for ep in train_first[: a.target]}
    matched = [ep for ep in first if not trainable(ep) or id(ep) in keep]
    n = write(out / "episodes_k3_match" / "episodes.jsonl.gz", matched)
    print(f"match: {n:,} episodes written ({min(a.target, len(train_first)):,} trainable correct, "
          f"target {a.target:,})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
