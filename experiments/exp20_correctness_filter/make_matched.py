#!/usr/bin/env python
"""E20: an unfiltered training split as large as the filtered one.

Takes whole episodes (every example of one question) from the unfiltered split in one seeded
order until the number of training examples reaches that of the correct-only split. The mix of
correct and incorrect episodes, and of datasets, is whatever the unfiltered pool has; only the
amount of training data is matched (to within one episode). Dev is the unfiltered split's dev
set, which training only monitors.

    python experiments/exp20_correctness_filter/make_matched.py \\
        --source data/splits_self_all/uniform --target data/splits_self/uniform \\
        --out data/splits_self_mixmatch/uniform
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tgd.io import read_jsonl, write_jsonl  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, help="unfiltered split (build_splits.py --keep all)")
    ap.add_argument("--target", required=True, help="split whose train_examples count to match")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", default="e20")
    a = ap.parse_args()
    src, out = Path(a.source), Path(a.out)
    want = json.loads((Path(a.target) / "manifest.json").read_text(encoding="utf-8"))["train_examples"]

    rows = list(read_jsonl(src / "train.jsonl"))
    key = lambda r: (r["metadata"]["dataset"], r["metadata"]["qid"])  # noqa: E731
    size = collections.Counter(key(r) for r in rows)
    order = sorted(size)
    random.Random(f"tgd-e20-matched:{a.seed}").shuffle(order)
    chosen, n = set(), 0
    for k in order:
        if n >= want:
            break
        chosen.add(k)
        n += size[k]
    train = [r for r in rows if key(r) in chosen]   # keeps the source's shuffled order

    correct_ep = {key(r) for r in train if r["metadata"].get("episode_correct")}
    manifest = {
        "split": "uniform (size-matched, unfiltered)", "source": str(src), "matched_to": a.target,
        "target_examples": want, "train_examples": len(train), "train_questions": len(chosen),
        "correct_episode_fraction": round(len(correct_ep) / max(len(chosen), 1), 4),
        "correct_example_fraction": round(sum(bool(r["metadata"].get("episode_correct")) for r in train)
                                          / max(len(train), 1), 4),
        "per_dataset_examples": dict(collections.Counter(r["metadata"]["dataset"] for r in train)),
        "dev_file": str(src / "dev.jsonl"),
    }
    write_jsonl(out / "train.jsonl", train)
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
