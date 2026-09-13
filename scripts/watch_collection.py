#!/usr/bin/env python3
"""Live view of a teacher-guidance collection run: progress, rate, ETA and spend.

collect_episodes.py writes one folder per question with a _SUCCESS marker, so progress is
counted from the filesystem and stays correct across resumes and restarts. Teacher cost is
summed from the per-call usage each episode records, so the number shown is what was
actually billed, not an estimate.

    python scripts/watch_collection.py --out runs/collect_glm            # one snapshot
    python scripts/watch_collection.py --out runs/collect_glm --follow   # refresh
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys
import time

TARGETS = {"hotpotqa": 2000, "2wikimultihopqa": 2000, "musique": 2000, "strategyqa": 1999}


def episode_files(out: pathlib.Path):
    """Finished questions: a _SUCCESS marker AND the episode record beside it.

    The marker alone is not enough. A worker killed between writing the marker and writing
    the episode leaves a question the collector will skip forever, and counting markers
    reports it as done -- an OOM kill here left 3,060 such questions while every counter
    read 100%. scripts/verify_collection.py --prune clears them.
    """
    # One per question. A shard relaunched into a fresh run directory repeats questions it
    # already had, and counting every marker reported 3,110 episodes for a 2,000-question
    # dataset. Layout: <out>/<dataset>/<shard>/<run>/<dataset_name>/<sample>/_SUCCESS.
    seen = {}
    for m in out.rglob("_SUCCESS"):
        if not (m.parent / "teacher_guidance_episodes.jsonl").exists():
            continue
        seen.setdefault((str(m.parent.parent.parent.parent), m.parent.name), m)
    return list(seen.values())


def scan(out: pathlib.Path) -> dict:
    """Count finished questions per dataset, and sum teacher usage where recorded."""
    done = collections.Counter()
    tin = tout = cost = 0.0
    calls = 0
    records = 0
    newest = 0.0
    for marker in episode_files(out):
        ds = next((k for k in TARGETS if f"/{k}/" in str(marker)), "?")
        done[ds] += 1
        newest = max(newest, marker.stat().st_mtime)

    # usage lives in the episode records the workers append, not next to the markers
    for f in out.rglob("teacher_guidance_episodes.jsonl"):
        try:
            for line in f.open(encoding="utf-8"):
                line = line.strip()
                if not line:
                    continue
                records += 1
                for c in walk_calls(json.loads(line)):
                    u = c.get("usage") or {}
                    m = str(c.get("model", "")).lower()
                    if "granite" in m or "student" in m:
                        continue
                    tin += u.get("prompt_tokens", 0) or 0
                    tout += u.get("completion_tokens", 0) or 0
                    cost += (u.get("cost") or 0) or 0
                    calls += 1
        except Exception:
            continue
    return {"done": done, "in": tin, "out": tout, "cost": cost,
            "calls": calls, "records": records, "newest": newest}


def walk_calls(o):
    if isinstance(o, dict):
        if "model" in o and isinstance(o.get("usage"), dict):
            yield o
        for v in o.values():
            yield from walk_calls(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk_calls(v)


def render(out: pathlib.Path, s: dict, started: float, first: int) -> None:
    total_done = sum(s["done"].values())
    total_target = sum(TARGETS.values())
    el = max(time.time() - started, 1e-9)
    rate = (total_done - first) / el * 3600.0
    print(f"\n{out}   {time.strftime('%H:%M:%S')}")
    print(f"  {'dataset':<20}{'done':>7}{'target':>8}{'':>4}")
    for ds in sorted(TARGETS):
        d, t = s["done"].get(ds, 0), TARGETS[ds]
        bar = "#" * int(20 * d / t) if t else ""
        print(f"  {ds:<20}{d:>7}{t:>8}  {bar:<20} {100.0 * d / t:5.1f}%")
    print(f"  {'ALL':<20}{total_done:>7}{total_target:>8}  "
          f"{'':<20} {100.0 * total_done / total_target:5.1f}%")
    if rate > 1:
        left = (total_target - total_done) / rate
        print(f"\n  rate {rate:,.0f} episodes/h   eta {left:5.1f} h")
    if s["calls"]:
        # Per episode record, not per distinct question: spend includes duplicates, so
        # dividing it by distinct questions overstates what one more episode costs.
        n = max(s.get("records", 0), 1)
        print(f"  teacher: {s['calls'] / n:.1f} calls/ep  "
              f"{s['in'] / n:,.0f} in  {s['out'] / n:,.0f} out per episode")
        if s["cost"]:
            per = s["cost"] / n
            left_cost = per * max(total_target - total_done, 0)
            print(f"  spend  : ${s['cost']:.4f} so far   ~${left_cost:.2f} to finish "
                  f"(${per:.5f}/episode)")
    if s["newest"]:
        age = time.time() - s["newest"]
        flag = "  <-- nothing finished recently, check the log" if age > 900 else ""
        print(f"  last episode {age / 60:.1f} min ago{flag}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="runs/collect_glm")
    ap.add_argument("--follow", action="store_true")
    ap.add_argument("--interval", type=int, default=60)
    a = ap.parse_args()

    out = pathlib.Path(a.out)
    if not out.exists():
        print(f"!! {out} does not exist yet", file=sys.stderr)
        return 1
    started = time.time()
    first = sum(scan(out)["done"].values())
    while True:
        render(out, scan(out), started, first)
        if not a.follow:
            return 0
        time.sleep(a.interval)


if __name__ == "__main__":
    raise SystemExit(main())
