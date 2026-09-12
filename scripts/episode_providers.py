#!/usr/bin/env python3
"""Which upstream provider served each episode's teacher calls.

OpenRouter returns the serving provider in every response and the harness stores the raw
response, so provenance is recoverable even though nothing records it as its own field.
That matters when a collection spans more than one provider -- pinning can fail mid-run
when a provider rate-limits you out -- because the split is then documented in the data
rather than being an untracked confound.

    python scripts/episode_providers.py --runs runs/collect_glm
    python scripts/episode_providers.py --runs runs/collect_glm --by-dataset
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
import pathlib
import sys


def teacher_calls(obj):
    if isinstance(obj, dict):
        if "model" in obj and isinstance(obj.get("usage"), dict):
            yield obj
        for v in obj.values():
            yield from teacher_calls(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from teacher_calls(v)


def providers_of(ep: dict) -> set[str]:
    out = set()
    for c in teacher_calls(ep):
        if "vllm" in str(c.get("model", "")) or "student" in str(c.get("model", "")):
            continue
        raw = c.get("raw_response")
        if isinstance(raw, dict) and raw.get("provider"):
            out.add(str(raw["provider"]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs/collect_glm")
    ap.add_argument("--by-dataset", action="store_true")
    a = ap.parse_args()

    root = pathlib.Path(a.runs)
    files = list(root.rglob("teacher_guidance_episodes.jsonl"))
    files += [p for p in (root.rglob("episodes.jsonl.gz"), root.rglob("episodes.jsonl"))
              for p in p]
    if not files:
        print(f"!! no episode files under {root}", file=sys.stderr)
        return 1

    counts: collections.Counter = collections.Counter()
    per_ds: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    mixed = unknown = total = 0
    for f in files:
        op = gzip.open if f.suffix == ".gz" else open
        with op(f, "rt", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                ep = json.loads(line)
                total += 1
                provs = providers_of(ep)
                ds = ep.get("dataset", "?")
                if not provs:
                    unknown += 1
                    counts["(not recorded)"] += 1
                    per_ds[ds]["(not recorded)"] += 1
                    continue
                if len(provs) > 1:
                    mixed += 1
                for p in provs:
                    counts[p] += 1
                    per_ds[ds][p] += 1

    print(f"episodes {total}\n")
    for p, c in counts.most_common():
        print(f"  {p:<24}{c:>7}  ({100.0 * c / max(total, 1):5.1f}%)")
    if mixed:
        print(f"\n  {mixed} episodes used more than one provider within a single episode")
    if unknown:
        print(f"  {unknown} episodes carry no provider (older runs, or a non-OpenRouter teacher)")

    if a.by_dataset:
        print("\n  by dataset:")
        for ds in sorted(per_ds):
            row = ", ".join(f"{p}={c}" for p, c in per_ds[ds].most_common())
            print(f"    {ds:<20} {row}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
