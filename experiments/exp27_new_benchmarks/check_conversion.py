#!/usr/bin/env python
"""Did the conversion produce episodes the agent can actually solve?

A converted benchmark can look fine as JSON and still be unusable: the gold documents may not be
retrievable, the answers may not be strings the judge can grade, or the agent may never reach a
finish action. This checks a handful of episodes before thirteen arms are evaluated on it.

    python experiments/exp27_new_benchmarks/check_conversion.py --dataset multihoprag \\
        --episodes runs/eval/smoke_multihoprag/newtest_multihoprag/episodes.jsonl
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--episodes", required=True)
    a = ap.parse_args()
    qf = KIT / "data" / "questions" / a.dataset / f"{a.dataset}_questions.jsonl.gz"
    cf = KIT / "data" / "questions" / a.dataset / f"{a.dataset}_corpus.jsonl.gz"
    nq = sum(1 for _ in gzip.open(qf, "rt", encoding="utf-8"))
    docs = collections.Counter()
    chars = 0
    with gzip.open(cf, "rt", encoding="utf-8") as fh:
        for line in fh:
            d = json.loads(line)
            docs[d["qid"]] += 1
            chars += len(d["text"])
    n_docs = sum(docs.values())
    print(f"dataset {a.dataset}: {nq} questions, {n_docs} documents "
          f"({n_docs / max(nq, 1):.1f} per question, {chars / max(n_docs, 1):,.0f} chars each)")

    c = collections.Counter()
    for line in open(a.episodes, encoding="utf-8"):
        if not line.strip():
            continue
        ep = json.loads(line)
        c["n"] += 1
        fm = ep.get("final_metrics") or {}
        c["answered"] += bool(str(ep.get("final_answer") or "").strip())
        c["cover"] += bool(fm.get("answer_correct"))
        c["gold_retrieved"] += bool(fm.get("doc_recall"))
        c["steps"] += len(ep.get("steps") or [])
        c[f"stop:{ep.get('stop_reason')}"] += 1
        for s in ep.get("steps") or []:
            tool = ((s.get("student_action") or {}).get("action") or {}).get("tool")
            c[f"tool:{tool}"] += 1
    n = max(c["n"], 1)
    print(f"smoke episodes: {c['n']}  answered {100 * c['answered'] / n:.0f}%  "
          f"gold doc retrieved {100 * c['gold_retrieved'] / n:.0f}%  "
          f"cover-correct {100 * c['cover'] / n:.0f}%  steps {c['steps'] / n:.2f}")
    print("  tools:", {k.split(":")[1]: v for k, v in c.items() if k.startswith("tool:")})
    print("  stop: ", {k.split(":")[1]: v for k, v in c.items() if k.startswith("stop:")})
    problems = []
    if c["answered"] < n:
        problems.append("some episodes produced no answer")
    if c["gold_retrieved"] == 0:
        problems.append("no episode retrieved a gold document: retrieval or the candidate sets are wrong")
    if c["steps"] / n < 1.5:
        problems.append("fewer than 1.5 steps per episode: the agent is not using the tools")
    print(("\nPROBLEMS: " + "; ".join(problems)) if problems else "\nlooks usable")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
