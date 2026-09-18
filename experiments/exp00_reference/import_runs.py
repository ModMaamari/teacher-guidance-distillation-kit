#!/usr/bin/env python3
"""Import the research workspace's E00 and E13 evaluation episodes into the kit's run layout,
so they can be re-judged with the current judge and tabulated by scripts/collect_results.py.

    python experiments/exp00_reference/import_runs.py --research-root <teacher-guidence checkout>

Writes (all under runs/, never committed)::

    runs/e00/eval/{base,guided,trained,teacher}/heldout_<ds>/episodes.jsonl
    runs/e13/eval/{base,all4,fold_<ds>,teacher}/{heldout_<ds>,full_<ds>}/episodes.jsonl

The research workspace calls the held-out questions ``heldin`` (held out of training, held in
the dataset) and shards the full unseen sets (``__s0..s2``); shards are concatenated here. A
question evaluated twice (a resumed run) keeps its last episode. The teacher arm was collected
as teacher-guidance records with no teacher in the loop; only the fields the judge and the
results table read are kept, so no provider or host name is copied.

Idempotent: a finished test set carries a ``.done`` marker and is skipped unless --force.
Prints per test set the episode count and its overlap with the kit's test question file.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
DATASETS = ("hotpotqa", "2wikimultihopqa", "musique", "strategyqa")
KEEP = ("qid", "query", "gold_answer", "final_answer", "budget", "used_steps", "stop_reason",
        "final_metrics", "elapsed_s", "steps", "plan", "error")


def read(paths):
    """qid -> last episode across files, in the given order."""
    out = {}
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    e = json.loads(line)
                    out[e["qid"]] = {k: e[k] for k in KEEP if k in e}
    return out


def eval_dirs(root: Path, name: str):
    """research eval dirs <timestamp>_<name>/, oldest first, that hold episodes."""
    return sorted(p / "episodes.jsonl" for p in root.glob(f"*_{name}") if (p / "episodes.jsonl").exists())


def teacher_files(research: Path, prefix: str):
    base = research / "data" / "simulation_output" / "teacher_arm"
    return sorted(base.glob(f"{prefix}_s*/**/teacher_guidance_episodes.jsonl"))


def test_qids(name: str):
    p = KIT / "data" / "splits" / "test" / f"{name}_questions.jsonl"
    if not p.exists():
        return None
    return {json.loads(line)["id"] for line in open(p, encoding="utf-8") if line.strip()}


def write(dest: Path, eps: dict, force: bool):
    if (dest / ".done").exists() and not force:
        return "skip"
    dest.mkdir(parents=True, exist_ok=True)
    tmp = dest / "episodes.jsonl.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        for e in eps.values():
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    os.replace(tmp, dest / "episodes.jsonl")
    (dest / ".done").write_text(f"{len(eps)} episodes imported\n", encoding="utf-8")
    return "wrote"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--research-root", default=os.environ.get("RESEARCH_ROOT"), required=not os.environ.get("RESEARCH_ROOT"))
    ap.add_argument("--out", default="runs")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    research = Path(a.research_root)
    lodo = research / "training_methods" / "m1_lodo" / "runs"
    out = KIT / a.out

    plan = []  # (experiment, arm, test set, source files)
    for ds in DATASETS:
        base = eval_dirs(lodo / "lodo" / "eval", f"base__heldin_{ds}")
        guided = eval_dirs(lodo / "uniform" / "eval", f"guided__heldin_{ds}")
        all4 = eval_dirs(lodo / "uniform" / "eval", f"all4__heldin_{ds}")
        tarm = teacher_files(research, f"tarm_heldin_{ds}")
        plan += [("e00", "base", f"heldout_{ds}", base), ("e00", "guided", f"heldout_{ds}", guided),
                 ("e00", "trained", f"heldout_{ds}", all4), ("e00", "teacher", f"heldout_{ds}", tarm),
                 ("e13", "base", f"heldout_{ds}", base), ("e13", "all4", f"heldout_{ds}", all4),
                 ("e13", "teacher", f"heldout_{ds}", tarm),
                 ("e13", "base", f"full_{ds}",
                  [f for s in range(3) for f in eval_dirs(lodo / "lodo" / "eval", f"base__unseen_{ds}__s{s}")]),
                 ("e13", f"fold_{ds}", f"full_{ds}",
                  [f for s in range(3) for f in eval_dirs(lodo / "lodo" / "eval", f"fold_{ds}__unseen_{ds}__s{s}")]),
                 ("e13", "teacher", f"full_{ds}", teacher_files(research, f"tarm_unseen_{ds}"))]
        for other in DATASETS:
            if other != ds:
                plan.append(("e13", f"fold_{ds}", f"heldout_{other}",
                             eval_dirs(lodo / "lodo" / "eval", f"fold_{ds}__heldin_{other}")))

    missing = 0
    print(f"{'set':<42} {'files':>5} {'episodes':>8} {'in test file':>12}  action")
    for exp, arm, test, files in plan:
        label = f"{exp}/{arm}/{test}"
        if not files:
            print(f"{label:<42} {0:>5} {'-':>8} {'-':>12}  MISSING")
            missing += 1
            continue
        eps = read(files)
        want = test_qids(test)
        overlap = "-" if want is None else f"{len(set(eps) & want)}/{len(want)}"
        act = write(out / exp / "eval" / arm / test, eps, a.force)
        print(f"{label:<42} {len(files):>5} {len(eps):>8} {overlap:>12}  {act}")
    if missing:
        print(f"!! {missing} set(s) had no source files", file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
