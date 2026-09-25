#!/usr/bin/env python
"""What each trained student actually cost to build, as it was run.

pipeline_cost.py prices a standardised build (every route collects until 3,818 episodes pass the
filter, then pays the same 684-PFLOP training run). That makes routes comparable per usable
episode, but the accuracies in the paper come from students built differently. This script prices
those students: the collection each one was trained from, measured call by call with the same
method as pipeline_cost.py, plus the trainer's own compute counter for its training run.

  collection   episodes collected and PFLOPs over all of them (2 x active params x tokens); some
               were collected on held-out questions, whose episodes are priced but never trained on
  kept         episodes of training questions that passed the filter (the split's train set)
  training     examples and PFLOPs of the training run (identical across seeds of one split)

    python experiments/exp23_pipeline_cost/actual_build.py --json-out actual_build.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(KIT / "experiments" / "exp20_correctness_filter"))

import pipeline_cost as pc   # noqa: E402
import train_cost as tc      # noqa: E402

# route -> (label, collection dir, actor, critic, split dir, training runs, experiment)
ROUTES = {
    "selfdist":  ("student's own rollouts, unguided", "data/episodes_selfdist", "student", None,
                  "data/splits_selfdist", ["selfdist_full", "selfdist_full_s17", "selfdist_full_s23",
                                           "selfdist_full_s29", "selfdist_full_s31", "selfdist_full_s37"], "E25"),
    "self":      ("self-guided (ours)", "data/episodes_self", "student", "student",
                  "data/splits_self", ["selftaught", "selftaught_s17", "selftaught_s23",
                                       "selftaught_s29", "selftaught_s31", "selftaught_s37"], "E25"),
    "deepseek":  ("teacher-guided (DeepSeek)", "data/episodes", "student", "deepseek",
                  "data/splits", ["seed13", "seed17", "seed23"], "E19"),
    "glm":       ("teacher-guided (GLM)", "data/episodes_glm", "student", "glm",
                  "data/splits_glm", ["glmtaught"], "E06"),
    "teachdist_or": ("teacher's own rollouts, all questions", "data/episodes_teachdist_or", "deepseek", None,
                     "data/splits_teachdist_or", ["teachdist_full_s13", "teachdist_full_s17",
                                                  "teachdist_full_s23"], "E24"),
    "teachdist": ("teacher's own rollouts, 2,000 questions", "data/episodes_teachdist", "deepseek", None,
                  "data/splits_teachdist", ["sup_teachdist", "sup_teachdist_s17", "sup_teachdist_s23"], "E21"),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    out: dict = {}
    print("BUILD AS RUN  (collection measured call by call; training from the trainer's own counter)\n")
    print(f"  {'route':<40}{'collected':>10}{'held out':>9}{'kept':>7}{'examples':>10}{'collect PF':>12}"
          f"{'train PF':>10}{'total PF':>10}  seeds")
    for key, (label, coll, actor, critic, split, runs, exp) in ROUTES.items():
        t = pc.tokens_of(KIT / coll / "episodes.jsonl.gz")
        flops = 2 * pc.MODELS[actor][2] * (t["actor_in"] + t["actor_out"])
        if critic:
            flops += 2 * pc.MODELS[critic][2] * (t["critic_in"] + t["critic_out"])
        collect_pf = flops * t["episodes"] / 1e15
        st = json.loads((KIT / split / "stats.json").read_text(encoding="utf-8"))["splits"]["uniform"]
        pools = json.loads((KIT / split / "pools.json").read_text(encoding="utf-8"))
        heldout = sum(1 for v in pools.values() if v == "heldout_test")
        trains = [tc.one(r) for r in runs]
        pfs = sorted({r.get("pflops") for r in trains})
        if len(pfs) != 1 or pfs[0] is None:
            raise SystemExit(f"{key}: training runs disagree or are missing: {pfs}")
        train_pf = pfs[0]
        row = {"label": label, "experiment": exp, "episodes_collected": t["episodes"],
               "heldout_questions_collected": heldout,
               "pflops_per_episode": flops / 1e15, "collect_pflops": collect_pf,
               "kept_episodes": st["train_questions"], "train_examples": st["train_examples"],
               "train_pflops": train_pf, "total_pflops": collect_pf + train_pf, "runs": runs}
        out[key] = row
        print(f"  {label:<40}{t['episodes']:>10,}{heldout:>9,}{st['train_questions']:>7,}{st['train_examples']:>10,}"
              f"{collect_pf:>12,.0f}{train_pf:>10,.0f}{collect_pf + train_pf:>10,.0f}  {len(runs)} ({exp})")
    print("\n  Every run of one route trains on the same split, so seeds share one training cost. 'held out'")
    print("  counts collected episodes on held-out questions, which are priced but never trained on.")
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
