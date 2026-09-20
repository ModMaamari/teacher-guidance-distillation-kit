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

EMPTY = {"", "unknown", "none", "n/a", "no answer"}


def episode_files(spec: str):
    p = KIT / spec
    if p.is_dir():
        return sorted(p.glob("*/episodes.jsonl"))
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
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    rows = {}
    print(f"  {'configuration':<40}{'n':>6}{'judged':>8}{'correct':>9}{'answered':>10}{'steps':>7}{'tokens':>9}")
    for spec in a.arm:
        label, _, rest = spec.partition("=")
        eps, _, verd = rest.partition(":")
        v = {}
        vp = KIT / verd
        if vp.exists():
            for r in read(vp):
                v[str(r["qid"])] = int(bool((r.get("verdict") or {}).get("correct")))
        c = collections.Counter()
        for f in episode_files(eps):
            for ep in read(f):
                qid = str(ep.get("qid"))
                if pool_of(qid, 0.10, DEFAULT_SALT) != "heldout_test":
                    continue
                c["n"] += 1
                ans = str(ep.get("final_answer") or "").strip().lower()
                c["answered"] += ans not in EMPTY
                c["steps"] += len(ep.get("steps") or [])
                for s in ep.get("steps") or []:
                    for call in (s.get("student_calls") or []) + (s.get("teacher_calls") or []):
                        u = call.get("usage") or {}
                        c["tok"] += int(u.get("prompt_tokens") or 0) + int(u.get("completion_tokens") or 0)
                if qid in v:
                    c["judged"] += 1
                    c["correct"] += v[qid]
        n = max(c["n"], 1)
        acc = 100 * c["correct"] / c["judged"] if c["judged"] else float("nan")
        rows[label] = {"n": c["n"], "judged": c["judged"], "judge_correct": round(acc, 2),
                       "answered_pct": round(100 * c["answered"] / n, 1),
                       "steps": round(c["steps"] / n, 2), "tokens": round(c["tok"] / n)}
        tok = f"{c['tok'] / n:,.0f}" if c["tok"] else "--"
        print(f"  {label:<40}{c['n']:>6}{c['judged']:>8}{acc:>8.1f}%{100 * c['answered'] / n:>9.1f}%"
              f"{c['steps'] / n:>7.2f}{tok:>9}")
    print("\n  'answered' is the share of episodes that ended with a non-empty final answer: an agent that")
    print("  never commits is scored wrong, so this column says whether two rows are comparable at all.")
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
