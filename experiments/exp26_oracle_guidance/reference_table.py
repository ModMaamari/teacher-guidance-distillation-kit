#!/usr/bin/env python
"""Every way of answering the held-out questions without training, side by side.

The paper's reference points mix agents (student, teacher) with critics (none, the teacher, the
model itself). This puts them in one table on the same 747 questions, with the detail that makes
them comparable or not: whether the agent ever produced an answer, how many steps it took and how
many tokens it processed. Arms whose critic sees the gold answer are upper bounds, not deployable
systems, and are marked as such by the caller.

    python experiments/exp26_oracle_guidance/reference_table.py \\
        --arm "base student alone=runs/eval/base:runs/judge/base/verdicts.jsonl" ...
"""
from __future__ import annotations

import argparse
import collections
import glob
import gzip
import json
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))
from tgd.splits import DEFAULT_SALT, pool_of  # noqa: E402
from tgd.stats import mcnemar_exact, paired_bootstrap  # noqa: E402

EMPTY = {"", "unknown", "none", "n/a", "no answer"}


def episode_files(spec: str, tests: str = "heldout_*"):
    """Episode files of one arm. An evaluation directory accumulates every test set the arm was
    ever run on, so only the ones asked for are read; a consolidated collection is one file."""
    p = KIT / spec
    if p.is_dir():
        return sorted(f for t in tests.split() for f in p.glob(f"{t}/episodes.jsonl"))
    return [q for q in (Path(x) for x in glob.glob(str(KIT / spec))) if q.exists()]


def read(f: Path):
    op = gzip.open if f.suffix == ".gz" else open
    with op(f, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arm", nargs="+", required=True, help="<label>=<episodes path or glob>:<verdicts.jsonl>")
    ap.add_argument("--tests", default="heldout_hotpotqa heldout_2wikimultihopqa heldout_musique heldout_strategyqa",
                    help="test directories to read from an evaluation arm")
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--pair", nargs="*", default=[],
                    help="<label a>|<label b>: paired difference b - a over the questions both arms judged")
    ap.add_argument("--pairs-out", default=None)
    a = ap.parse_args()
    rows = {}
    per_q = {}   # label -> {(dataset, qid): 0/1}, for the paired comparisons
    print(f"  {'configuration':<40}{'n':>6}{'judged':>8}{'correct':>9}{'answered':>10}{'steps':>7}{'tokens':>9}")
    for spec in a.arm:
        label, _, rest = spec.partition("=")
        eps, _, verd = rest.partition(":")
        # Key verdicts by (episode file, qid): a verdicts file often holds several arms, and keying
        # by qid alone silently reads another arm's verdict for the same question.
        v = {}
        vp = KIT / verd
        if vp.exists():
            for r in read(vp):
                src = Path(r["source"])
                src = src if src.is_absolute() else (KIT / src)
                v[(str(src.resolve()), str(r["qid"]))] = int(bool((r.get("verdict") or {}).get("correct")))
        c = collections.Counter()
        by_ds = collections.defaultdict(collections.Counter)
        per_q[label] = {}
        for f in episode_files(eps, a.tests):
            key = str(Path(f).resolve())
            for ep in read(f):
                qid = str(ep.get("qid"))
                if pool_of(qid, 0.10, DEFAULT_SALT) != "heldout_test":
                    continue
                # a consolidated collection records the dataset; an evaluation arm's directory names it
                ds = ep.get("dataset") or Path(f).parent.name.removeprefix("heldout_")
                c["n"] += 1
                ans = str(ep.get("final_answer") or "").strip().lower()
                c["answered"] += ans not in EMPTY
                c["steps"] += len(ep.get("steps") or [])
                for s in ep.get("steps") or []:
                    for call in (s.get("student_calls") or []) + (s.get("teacher_calls") or []):
                        u = call.get("usage") or {}
                        c["tok"] += int(u.get("prompt_tokens") or 0) + int(u.get("completion_tokens") or 0)
                # Every call, plan review included, split by who made it (a locally served model is the
                # student): what an inference-cost estimate needs. "tokens" above stays step calls only.
                pr = ep.get("plan_review") or {}
                calls = list(pr.get("initial_plan_calls") or [])
                for r in pr.get("rounds") or []:
                    calls += list(r.get("review_calls") or [])
                for s in ep.get("steps") or []:
                    calls += list(s.get("student_calls") or []) + list(s.get("teacher_calls") or [])
                for call in calls:
                    u = call.get("usage") or {}
                    n_tok = int(u.get("prompt_tokens") or 0) + int(u.get("completion_tokens") or 0)
                    local = str(call.get("model") or "").startswith(("vllm/", "hf-local"))
                    c["tok_student_all" if local else "tok_other_all"] += n_tok
                if (key, qid) in v:
                    c["judged"] += 1
                    c["correct"] += v[(key, qid)]
                    by_ds[ds]["judged"] += 1
                    by_ds[ds]["correct"] += v[(key, qid)]
                    per_q[label][(ds, qid)] = v[(key, qid)]
        n = max(c["n"], 1)
        acc = 100 * c["correct"] / c["judged"] if c["judged"] else float("nan")
        rows[label] = {"n": c["n"], "judged": c["judged"], "judge_correct": round(acc, 2),
                       "answered_pct": round(100 * c["answered"] / n, 1),
                       "steps": round(c["steps"] / n, 2), "tokens": round(c["tok"] / n),
                       "tokens_all_calls": {"student": round(c["tok_student_all"] / n),
                                            "large_model": round(c["tok_other_all"] / n)},
                       "by_dataset": {d: round(100 * x["correct"] / x["judged"], 2)
                                      for d, x in sorted(by_ds.items()) if x["judged"]}}
        tok = f"{c['tok'] / n:,.0f}" if c["tok"] else "--"
        print(f"  {label:<40}{c['n']:>6}{c['judged']:>8}{acc:>8.1f}%{100 * c['answered'] / n:>9.1f}%"
              f"{c['steps'] / n:>7.2f}{tok:>9}")
    print("\n  'answered' is the share of episodes that ended with a non-empty final answer: an agent that")
    print("  never commits is scored wrong, so this column says whether two rows are comparable at all.")
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(rows, indent=2), encoding="utf-8")
    pairs = []
    if a.pair:
        print("\n  paired over the questions both arms judged (b - a, points; bootstrap 95% CI; exact McNemar):")
    for spec in a.pair:
        la, _, lb = spec.partition("|")
        common = sorted(set(per_q.get(la, {})) & set(per_q.get(lb, {})))
        if not common:
            print(f"  {la} -> {lb}: no common questions"); continue
        xa = [per_q[la][k] for k in common]
        xb = [per_q[lb][k] for k in common]
        bs, mc = paired_bootstrap(xa, xb), mcnemar_exact(xa, xb)
        pairs.append({"a": la, "b": lb, "n": len(common), "diff": round(100 * bs["diff"], 1),
                      "ci95": [round(100 * x, 1) for x in bs["ci95"]], "p": mc["p"],
                      "b_wins": mc["b_wins"], "a_wins": mc["a_wins"]})
        r = pairs[-1]
        print(f"  {la} -> {lb}: {r['diff']:+.1f} [{r['ci95'][0]:+.1f}, {r['ci95'][1]:+.1f}]  "
              f"p {r['p']:.4g}  (n {r['n']}, {r['b_wins']} / {r['a_wins']})")
    if a.pairs_out:
        Path(a.pairs_out).write_text(json.dumps(pairs, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
