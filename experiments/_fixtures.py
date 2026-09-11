#!/usr/bin/env python3
"""Build the synthetic inputs run_smoke_tests.sh feeds to the analysis helpers.

Deterministic, tiny, and shaped like the real thing: two split roots with different yields,
verdicts from two judges over three arms, episodes with a stop-reason split, and the six
pairwise comparisons the paper actually reports.
"""
from __future__ import annotations

import json
import pathlib
import random
import sys

def dump(path: pathlib.Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj), encoding="utf-8")


def dump_lines(path: pathlib.Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")


def main() -> int:
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(17)

    # two split roots with deliberately different yields, so matching has work to do
    for name, (pool, usable) in (("a", (7252, 3959)), ("b", (7252, 1200))):
        dump(out / f"split_{name}" / "stats.json",
             {"per_dataset": {"ds": {"trainable": pool, "train_episodes": usable}}})

    dump(out / "results_seeds.json", {"pooled": {
        "seed13": {"judge_correct": 0.655},
        "seed17": {"judge_correct": 0.641},
        "seed23": {"judge_correct": 0.663},
        "base": {"judge_correct": 0.298},
    }})

    budget = {}
    for arm, base in (("base", 0.22), ("trained", 0.55), ("teacher", 0.70)):
        for b, bump in ((1, -0.10), (3, 0.0), (5, 0.04), (8, 0.05)):
            budget[f"{arm}_b{b}"] = {"judge_correct": round(base + bump, 3),
                                     "mean_steps": b * 0.95,
                                     "total_tokens_per_ep": 1500 * b}
    dump(out / "results_budget.json", {"pooled": budget})

    # the six comparisons docs/RESULTS.md actually reports
    dump(out / "results_paired.json", {"paired": {
        "base student -> trained student": {"pooled": {"p": 1e-7, "diff": 35.6}},
        "base student -> guided student": {"pooled": {"p": 1e-7, "diff": 30.7}},
        "trained student -> guided student": {"pooled": {"p": 0.0052, "diff": -5.0}},
        "trained student -> teacher alone": {"pooled": {"p": 0.00018, "diff": 6.8}},
        "guided student -> teacher alone": {"pooled": {"p": 1e-7, "diff": 11.8}},
        "base student -> teacher alone": {"pooled": {"p": 1e-7, "diff": 42.4}},
    }})

    # verdicts from two judges, and episodes whose stop reasons match the reported rates
    prim, swap = [], []
    for arm, p, pvol in (("base", 0.30, 0.02), ("trained", 0.65, 0.11), ("teacher", 0.72, 1.0)):
        d = out / "eval" / arm / "heldout_hotpotqa"
        src = str(d / "episodes.jsonl")
        eps = []
        for i in range(80):
            c = 1 if rng.random() < p else 0
            ans = " ".join(["w"] * (rng.randint(12, 25) if c else rng.randint(4, 12)))
            row = {"source": src, "qid": f"{arm}-{i}", "query": "q?",
                   "gold_answer": "g", "final_answer": ans, "verdict": {"correct": c}}
            prim.append(row)
            swap.append({**row, "verdict": {"correct": c if rng.random() < 0.88 else 1 - c}})
            vol = rng.random() < pvol
            eps.append({"qid": f"{arm}-{i}", "query": "q?", "gold_answer": "g",
                        "final_answer": ans, "steps": 2 if vol else 3,
                        "stop_reason": "answered" if vol else "budget_exhausted",
                        "final_metrics": {"cover_match": c}})
        dump_lines(d / "episodes.jsonl", eps)
    dump_lines(out / "verdicts.jsonl", prim)
    dump_lines(out / "verdicts_swap.jsonl", swap)

    # external-dataset input, including one malformed row the converter must skip
    ext = [{"question": f"Who directed film {i}?", "answer": f"Director {i}",
            "documents": [
                {"title": f"Film {i}", "text": f"Film {i} was directed by Director {i}."},
                {"title": f"Other {i}", "text": f"Unrelated text about topic {i}."}]}
           for i in range(12)]
    ext.append({"question": "no documents", "answer": "x"})
    dump_lines(out / "ext.jsonl", ext)

    print(f"fixtures in {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
