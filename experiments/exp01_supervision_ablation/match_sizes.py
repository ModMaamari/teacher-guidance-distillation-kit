#!/usr/bin/env python3
"""Work out, per arm, how many episodes to *collect* so every arm ends up with the same
number of *usable* training episodes.

``make_size_splits.py --sizes N`` samples N episodes from the trainable pool whether or not
they are correct; only correct ones yield training examples. The yield differs sharply by
supervision source -- a guided student is correct far more often than a solo one -- so equal
N gives unequal supervision. Matching has to be on the usable count:

    collected_arm = ceil(target * pool_arm / usable_arm)      capped at pool_arm

Reads ``<root>/stats.json`` as written by ``build_splits.py --out <root>``.
Prints one ``<arm> <collected>`` line on stdout; a table on stderr.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys


def totals(root: pathlib.Path) -> tuple[int, int]:
    """(trainable pool, usable train episodes) from a build_splits output root."""
    per = json.loads((root / "stats.json").read_text(encoding="utf-8"))["per_dataset"].values()
    return (sum(d.get("trainable", 0) for d in per),
            sum(d.get("train_episodes", 0) for d in per))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", action="append", required=True, metavar="ARM=DIR",
                    help="build_splits output root for one arm; repeat per arm")
    ap.add_argument("--target", type=int, default=0,
                    help="usable episodes to match on (default: the smallest arm)")
    a = ap.parse_args()

    roots: dict[str, pathlib.Path] = {}
    for spec in a.root:
        if "=" not in spec:
            print(f"!! --root wants ARM=DIR, got {spec!r}", file=sys.stderr)
            return 2
        arm, d = spec.split("=", 1)
        roots[arm] = pathlib.Path(d)

    stats = {}
    for arm, d in roots.items():
        if not (d / "stats.json").exists():
            print(f"!! no stats.json under {d} -- build that arm's split first", file=sys.stderr)
            return 1
        stats[arm] = totals(d)

    target = a.target or min(u for _, u in stats.values())
    print(f"{'arm':<12} {'pool':>7} {'usable':>7} {'yield':>7} {'collect':>8}", file=sys.stderr)
    for arm, (pool, usable) in stats.items():
        if usable <= 0:
            print(f"!! {arm}: no usable training episodes", file=sys.stderr)
            return 1
        collect = min(pool, math.ceil(target * pool / usable))
        print(f"{arm:<12} {pool:>7} {usable:>7} {usable / pool:>6.1%} {collect:>8}",
              file=sys.stderr)
        print(f"{arm} {collect}")
    print(f"\nmatching on {target} usable training episodes", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
