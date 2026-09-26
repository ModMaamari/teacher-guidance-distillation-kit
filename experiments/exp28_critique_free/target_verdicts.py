#!/usr/bin/env python
"""Verdicts on answers inside the self-guided training targets.

A target's critique is written with the gold answer in view, but the student must produce it from
an answer-free input. This counts, over the answer ("finish") targets of the self-guided split:

  negative    targets whose critique calls an answer incorrect or wrong (the words "incorrect",
              "wrong", "not correct" or "inaccurate"); every such target's own answer is checked
              with cover match against the gold answer
  repeated    of those, targets whose previous step finished with the same answer (equal after
              lowercasing and removing punctuation, or cover match in both directions): the critique
              rejects an answer and the target then gives it again
  yes/no      on StrategyQA, targets after a finish step: does the answer's polarity (a leading
              "yes" or "no") change after a negative critique, which would mean the verdict gave
              the answer away?

    python experiments/exp28_critique_free/target_verdicts.py --json-out target_verdicts.json
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))
from agentsim.teacher_guidance.metrics import cover_match  # noqa: E402

NEG = re.compile(r"\b(incorrect|wrong|not correct|inaccurate)\b", re.I)


def norm(s) -> str:
    return re.sub(r"[^a-z0-9 ]", "", str(s).lower()).strip()


def polarity(s):
    m = re.match(r"\s*(yes|no)\b", str(s).lower())
    return m.group(1) if m else None


def answer(action: dict) -> str:
    return str(((action.get("action") or {}).get("params") or {}).get("answer", ""))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="data/splits_self/uniform/train.jsonl")
    ap.add_argument("--episodes", default="data/episodes_self/episodes.jsonl.gz")
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    eps = {}
    with gzip.open(KIT / a.episodes, "rt", encoding="utf-8") as fh:
        for line in fh:
            e = json.loads(line)
            eps[(e["dataset"], e["qid"])] = e
    c = collections.Counter()
    for line in open(KIT / a.split, encoding="utf-8"):
        r = json.loads(line)
        m = r["metadata"]
        if m["kind"] != "action" or m["tool"] != "finish":
            continue
        o = json.loads(r["completion"][0]["content"])
        fb = (o.get("teacher_guidance") or {}).get("feedback", "")
        e = eps[(m["dataset"], m["qid"])]
        ans = answer(o)
        c["finish_targets"] += 1
        neg = bool(NEG.search(fb))
        prev = next((s.get("student_action") or {} for s in e["steps"] if s["t"] == m["step"] - 1), {})
        prev_finish = (prev.get("action") or {}).get("tool") == "finish"
        if neg:
            c["negative"] += 1
            c["negative_answer_passes_cover"] += cover_match(ans, str(e["gold_answer"]))
            if prev_finish:
                pa = answer(prev)
                if norm(pa) == norm(ans) or (cover_match(ans, pa) and cover_match(pa, ans)):
                    c["negative_repeats_previous_answer"] += 1
        if m["dataset"] == "strategyqa":
            c["strategyqa_finish_targets"] += 1
            c["strategyqa_negative"] += neg
            if prev_finish:
                p, q = polarity(answer(prev)), polarity(ans)
                if p and q:
                    key = "negative" if neg else "other"
                    c[f"strategyqa_after_finish_{key}"] += 1
                    c[f"strategyqa_after_finish_{key}_flips"] += p != q
    out = dict(c)
    for k, v in sorted(out.items()):
        print(f"  {k:<42}{v:>6,}")
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
