#!/usr/bin/env python
"""Build training-set-size ablation splits: "what if only N episodes had been collected?"

The kit's uniform split turns every *correct* trainable episode into SFT examples. This
script answers the data-scaling question at the level the collection actually happens --
episodes, not examples -- by sampling N episodes from the trainable pool and keeping only
the examples that came from them.

Sampling is:
  * stratified by dataset, proportional to the trainable pool (so the dataset mix is the
    same at every size, and size is the only variable);
  * nested -- the 1k sample is a subset of the 2k sample is a subset of the 5k sample,
    from one seeded shuffle per dataset. A larger run therefore never loses an episode the
    smaller run had, which is what makes the curve a scaling curve rather than three
    unrelated draws;
  * over ALL trainable episodes, correct or not. Only the correct ones yield training
    examples, exactly as in a real collection run, so "5,000 episodes collected" costs
    5,000 teacher-guided rollouts and buys whatever fraction of them succeeded.

Dev is left alone: every size trains against the same dev.jsonl, so dev loss is comparable.

Usage::

    python scripts/make_size_splits.py --sizes 1000 2000 5000
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tgd  # noqa: F401
from tgd.io import load_jsonl, read_jsonl, write_jsonl
from tgd.splits import DEFAULT_DEV_SALT, DEFAULT_SALT, is_dev, pool_of


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--index", default="data/episodes/index.jsonl")
    ap.add_argument("--split", default="data/splits/uniform", help="full split to subset")
    ap.add_argument("--out-root", default="data/splits", help="writes <out-root>/uniform_ep<N>/")
    ap.add_argument("--sizes", type=int, nargs="+", default=[1000, 2000, 5000])
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--heldout-fraction", type=float, default=0.10)
    ap.add_argument("--dev-fraction", type=float, default=0.03)
    ap.add_argument("--salt", default=DEFAULT_SALT)
    ap.add_argument("--dev-salt", default=DEFAULT_DEV_SALT)
    args = ap.parse_args()

    # 1. the pool a collection run would draw from: trainable, non-dev episodes
    by_ds = collections.defaultdict(list)
    for rec in read_jsonl(Path(args.index)):
        qid = rec["qid"]
        if pool_of(qid, args.heldout_fraction, args.salt) != "trainable":
            continue
        if is_dev(qid, args.dev_fraction, args.dev_salt):
            continue
        by_ds[rec["dataset"]].append(qid)
    pool_total = sum(len(v) for v in by_ds.values())
    print(f"trainable non-dev episode pool: {pool_total} "
          f"({ {d: len(v) for d, v in sorted(by_ds.items())} })")

    # 2. one seeded shuffle per dataset -> nested prefixes at every size
    order = {}
    for ds, qids in sorted(by_ds.items()):
        qids = sorted(qids)                       # deterministic before shuffling
        random.Random(f"{args.seed}:{ds}").shuffle(qids)
        order[ds] = qids

    train_rows = load_jsonl(Path(args.split) / "train.jsonl")
    dev_file = Path(args.split) / "dev.jsonl"
    rows_by_qid = collections.defaultdict(list)
    for r in train_rows:
        rows_by_qid[r["metadata"]["qid"]].append(r)
    print(f"full split: {len(train_rows)} examples from {len(rows_by_qid)} episodes")

    summary = []
    for n in sorted(args.sizes):
        if n > pool_total:
            print(f"!! {n} > pool ({pool_total}); skipping")
            continue
        keep, counts = set(), {}
        for ds, qids in order.items():
            k = round(n * len(qids) / pool_total)
            counts[ds] = k
            keep.update(qids[:k])
        # rounding can miss the target by a couple of episodes; top up from the largest pool
        rows = [r for r in train_rows if r["metadata"]["qid"] in keep]
        d_out = Path(args.out_root) / f"uniform_ep{n}"
        write_jsonl(d_out / "train.jsonl", rows)
        per_ds = collections.Counter(r["metadata"]["dataset"] for r in rows)
        used = len({r["metadata"]["qid"] for r in rows})
        manifest = {
            "target": n, "episodes_sampled": len(keep), "episodes_per_dataset": counts,
            "episodes_with_examples": used,
            "yield": round(used / max(len(keep), 1), 4),
            "train_examples": len(rows), "examples_per_dataset": dict(per_ds),
            "dev_file": str(dev_file), "seed": args.seed, "nested": True,
            "source_split": str(args.split),
        }
        (d_out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"  uniform_ep{n:<6} {len(keep):>5} episodes -> {used:>5} usable "
              f"({manifest['yield']:.1%}) -> {len(rows):>6} examples   {d_out}")
        summary.append(manifest)

    # nesting proof: every smaller size must be a subset of the next one up
    def qids_of(n):
        return {r["metadata"]["qid"] for r in
                load_jsonl(Path(args.out_root) / f"uniform_ep{n}" / "train.jsonl")}
    sizes = [m["target"] for m in summary]
    for a, b in zip(sizes, sizes[1:]):
        assert qids_of(a) <= qids_of(b), f"ep{a} is not a subset of ep{b}"
    if len(sizes) > 1:
        print("nesting check OK: " + " subset of ".join(f"ep{n}" for n in sizes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
