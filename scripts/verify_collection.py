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
import json
import pathlib
import sys

RECORD = "teacher_guidance_episodes.jsonl"
CHECKPOINT = "checkpoint_*.json"
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


def repair_checkpoints(root: pathlib.Path, apply: bool) -> tuple[int, int]:
    """Drop samples a checkpoint claims are done but that produced no episode.

    The worker records a sample in ``completed_samples`` once it has finished *attempting*
    it, and sets ``status: completed`` when it reaches the end of its list -- whether or
    not episodes came out. A shard can therefore claim 125/125 while holding 93 episodes,
    and because the status is terminal, a resume skips the shard entirely. The missing
    questions become unreachable, and the collector's own advice to "re-run to retry the
    missing ones" quietly does nothing.

    Returns (checkpoints touched, samples freed).
    """
    touched = freed = 0
    for cp in root.rglob(CHECKPOINT):
        shard = cp.parent
        try:
            data = json.loads(cp.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            # unreadable or malformed checkpoint; skip it. Deliberately narrow: a bare
            # `except Exception` here swallowed a NameError from a missing import and
            # turned this entire function into a silent no-op.
            continue
        done = data.get("completed_samples")
        if not isinstance(done, list):
            continue
        # a sample is real if ANY run under this shard produced its episode
        real = {d.parent.name for d in shard.rglob(RECORD)}
        missing = [s for s in done if s not in real]
        if not missing:
            continue
        touched += 1
        freed += len(missing)
        if apply:
            data["completed_samples"] = [s for s in done if s in real]
            data["status"] = "in_progress"
            data.pop("completed_at", None)
            tmp = cp.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
            tmp.replace(cp)
    return touched, freed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs/collect_glm")
    ap.add_argument("--prune", action="store_true",
                    help="delete markers with no episode record so they are re-collected")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    ap.add_argument("--repair-checkpoints", action="store_true",
                    help="also drop samples a checkpoint claims but that produced no "
                         "episode, so the worker retries them")
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

    t, fr = repair_checkpoints(root, apply=a.repair_checkpoints)
    if t:
        verb = "freed" if a.repair_checkpoints else "would free"
        print(f"\ncheckpoints claiming samples that produced no episode: {t} shards, "
              f"{fr} samples {verb}")
        if not a.repair_checkpoints:
            print("  those shards are marked status=completed, so a resume SKIPS them and")
            print("  the questions are unreachable. Re-run with --repair-checkpoints.")

    if not orphan and not t:
        print("\nevery marked question has an episode record, and no checkpoint overclaims.")
        return 0
    if not orphan:
        return 0 if a.repair_checkpoints else 1

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
