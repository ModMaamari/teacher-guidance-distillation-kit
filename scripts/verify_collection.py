#!/usr/bin/env python3
"""Check that every question marked done actually produced an episode, and optionally
delete the markers that lie.

A worker writes ``_SUCCESS`` into a question's directory, and the collector skips any
question whose marker exists. If the worker dies between the marker and the episode file
-- an OOM kill will do it -- the question is skipped forever and the dataset quietly ends
up short. It happened here: 3,060 of 4,106 marked questions held no episode record, and
every progress counter still read them as finished.

    python scripts/verify_collection.py --runs runs/collect_glm
    python scripts/verify_collection.py --runs runs/collect_glm --prune   # then resume
"""
from __future__ import annotations

import argparse
import collections
import pathlib
import sys

RECORD = "teacher_guidance_episodes.jsonl"
DATASETS = ("hotpotqa", "2wikimultihopqa", "musique", "strategyqa")


def scan(root: pathlib.Path):
    complete, orphan = [], []
    for marker in root.rglob("_SUCCESS"):
        d = marker.parent
        (complete if (d / RECORD).exists() else orphan).append(d)
    return complete, orphan


def dataset_of(d: pathlib.Path) -> str:
    s = str(d)
    return next((x for x in DATASETS if f"/{x}/" in s), "?")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs/collect_glm")
    ap.add_argument("--prune", action="store_true",
                    help="delete markers with no episode record so they are re-collected")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    a = ap.parse_args()

    root = pathlib.Path(a.runs)
    if not root.exists():
        print(f"!! {root} not found", file=sys.stderr)
        return 1

    complete, orphan = scan(root)
    per = collections.Counter(dataset_of(d) for d in complete)
    bad = collections.Counter(dataset_of(d) for d in orphan)

    print(f"marked done {len(complete) + len(orphan)}   "
          f"real {len(complete)}   orphaned markers {len(orphan)}\n")
    print(f"  {'dataset':<20}{'real':>8}{'orphaned':>10}")
    for ds in DATASETS:
        print(f"  {ds:<20}{per.get(ds, 0):>8}{bad.get(ds, 0):>10}")

    if not orphan:
        print("\nevery marked question has an episode record.")
        return 0

    print(f"\n{len(orphan)} questions are marked done but hold no episode.")
    print("The collector will skip them on resume, so the dataset ends up short.")
    if not a.prune:
        print("Re-run with --prune to delete those markers, then resume the collection.")
        return 1

    if not a.yes:
        reply = input(f"delete {len(orphan)} _SUCCESS markers? [y/N] ").strip().lower()
        if reply != "y":
            print("nothing deleted")
            return 1
    removed = 0
    for d in orphan:
        try:
            (d / "_SUCCESS").unlink()
            removed += 1
        except OSError as exc:
            print(f"  could not remove {d}: {exc}", file=sys.stderr)
    print(f"removed {removed} markers -- resume the collection to fill them in")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
