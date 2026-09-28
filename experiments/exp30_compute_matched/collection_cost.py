#!/usr/bin/env python
"""Collection compute of self-guidance against three unguided attempts, measured call by call.

E30's premise is that three unguided rollouts per question cost about what one self-guided episode
costs. This checks it on the collected episodes rather than assuming it: tokens per episode come
from every recorded call (E23's walker), and compute is 2 x active parameters x tokens with the
student (Granite-4.1-3B, 3.4B) in every role.

    python experiments/exp30_compute_matched/collection_cost.py --json-out cost.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT / "experiments" / "exp23_pipeline_cost"))
from pipeline_cost import tokens_of  # noqa: E402

PARAMS = 3.4e9
SETS = [
    ("self-guided (ours)", "data/episodes_self"),
    ("unguided attempt 1 (T 0.2)", "data/episodes_selfdist"),
    ("unguided attempt 2 (T 0.7)", "data/episodes_selfdist_a2"),
    ("unguided attempt 3 (T 0.7)", "data/episodes_selfdist_a3"),
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    rows = []
    for label, d in SETS:
        t = tokens_of(KIT / d / "episodes.jsonl.gz")
        tokens = t["actor_in"] + t["actor_out"] + t["critic_in"] + t["critic_out"]
        pf = 2 * PARAMS * tokens / 1e15
        rows.append({"set": label, "dir": d, **t, "tokens_per_ep": round(tokens, 1),
                     "pflops_per_ep": round(pf, 4), "pflops_total": round(pf * t["episodes"], 1)})
    print("COLLECTION COMPUTE (PFLOPs ~ 2 x 3.4B x tokens, every recorded call)\n")
    print(f"  {'set':<30}{'episodes':>9}{'tokens/ep':>11}{'PF/ep':>9}{'total PF':>10}")
    for r in rows:
        print(f"  {r['set']:<30}{r['episodes']:>9,}{r['tokens_per_ep']:>11,.0f}{r['pflops_per_ep']:>9.4f}{r['pflops_total']:>10,.0f}")
    three = sum(r["pflops_total"] for r in rows[1:])
    self_pf = rows[0]["pflops_total"]
    print(f"\n  three unguided attempts: {three:,.0f} PF = {100 * three / self_pf:.1f} % of self-guided collection ({self_pf:,.0f} PF)")
    if a.json_out:
        Path(a.json_out).write_text(json.dumps({"rows": rows, "three_attempts_pf": three,
                                                "self_guided_pf": self_pf}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
