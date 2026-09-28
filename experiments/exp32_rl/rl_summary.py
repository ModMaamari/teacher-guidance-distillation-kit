#!/usr/bin/env python
"""Training curves of the E32 RL runs: per seed, rounds, compute, and the training reward
(fraction of sampled episodes whose answer passes the cover match) early, at each milestone and
at the end. Accuracy on the held-out questions comes from the eval tables, not from here.

    python experiments/exp32_rl/rl_summary.py --runs runs/rl/rl_s13 runs/rl/rl_s17 --json-out rl.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    out = []
    print("E32 RL training curves (reward = share of sampled episodes answered correctly, cover match)\n")
    print(f"  {'run':<10}{'rounds':>7}{'PFLOPs':>9}{'collect':>9}{'train':>8}"
          f"{'reward r1-5':>12}{'last 5':>8}{'informative':>13}")
    for r in a.runs:
        run = Path(r)
        rows = [json.loads(l) for l in (run / "rl_log.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        st = json.loads((run / "state.json").read_text(encoding="utf-8"))
        if not rows:
            print(f"  {run.name:<10} no rounds")
            continue
        milestones = st.get("args", {}).get("milestones", [])
        at = {}
        for m in milestones:
            hit = next((x for x in rows if x["cum_pflops"] >= m), None)
            if hit:
                window = [x["reward"] for x in rows if hit["round"] - 4 <= x["round"] <= hit["round"]]
                at[str(m)] = {"round": hit["round"], "reward_last5": round(mean(window), 4)}
        inf = mean([x["informative_groups"] / max(x["groups"], 1) for x in rows])
        rec = {"run": run.name, "rounds": len(rows), "pflops": st["pflops"],
               "collect_pflops": st["collect_pflops"], "train_pflops": st["train_pflops"],
               "reward_first5": round(mean([x["reward"] for x in rows[:5]]), 4),
               "reward_last5": round(mean([x["reward"] for x in rows[-5:]]), 4),
               "informative_share": round(inf, 3), "milestones": at, "done": bool(st.get("done"))}
        out.append(rec)
        print(f"  {run.name:<10}{rec['rounds']:>7}{rec['pflops']:>9,.0f}{rec['collect_pflops']:>9,.0f}"
              f"{rec['train_pflops']:>8,.0f}{rec['reward_first5']:>12.3f}{rec['reward_last5']:>8.3f}"
              f"{rec['informative_share']:>13.2f}")
        for m, v in at.items():
            print(f"  {'':<10}milestone {float(m):,.0f} PFLOPs at round {v['round']}: reward (last 5 rounds) {v['reward_last5']:.3f}")
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(out, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
