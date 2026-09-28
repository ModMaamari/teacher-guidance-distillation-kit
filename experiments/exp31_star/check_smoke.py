#!/usr/bin/env python
"""E31 smoke check on a handful of real answer-hinted episodes: the hint reached every step
prompt, the training examples built from them carry no hint and no ungrounded answer, and the
rest of the episode record is intact. Exit 0 only if all of that holds and at least one example
survives.

    python experiments/exp31_star/check_smoke.py runs/e31_smoke/episodes/episodes.jsonl.gz
"""
from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))

from agentsim.teacher_guidance.prompts import ANSWER_HINT_PREFIX  # noqa: E402
from agentsim.teacher_guidance.sft_internalize import has_answer_hint  # noqa: E402
from tgd.episode_lib import build_episode_examples  # noqa: E402


def main(path: str) -> int:
    eps = [json.loads(l) for l in gzip.open(path, "rt", encoding="utf-8") if l.strip()]
    problems, examples, steps, hinted_steps, correct = [], 0, 0, 0, 0
    for ep in eps:
        correct += bool((ep.get("final_metrics") or {}).get("answer_correct"))
        for st in ep.get("steps") or []:
            steps += 1
            hinted_steps += has_answer_hint(st.get("student_prompt") or "")
        pr = (ep.get("plan_review") or {}).get("initial_student_plan_prompt") or ""
        if ANSWER_HINT_PREFIX in pr:
            problems.append(f"{ep['qid']}: the plan prompt carries the hint")
        for ex in build_episode_examples(ep, "smoke"):
            examples += 1
            text = ex["prompt"][1]["content"]
            if ANSWER_HINT_PREFIX in text:
                problems.append(f"{ep['qid']}: hint left in a training input")
    print(f"episodes {len(eps)} (correct {correct}), steps {steps}, hinted steps {hinted_steps}, "
          f"training examples {examples}")
    if hinted_steps != steps:
        problems.append(f"only {hinted_steps} of {steps} step prompts carry the hint")
    if not examples:
        problems.append("no training example survived")
    for p in problems:
        print("!!", p)
    if eps:
        st = eps[0]["steps"][0]
        print("\nfirst hinted prompt, hint paragraph:")
        print([b for b in st["student_prompt"].split("\n\n") if b.startswith(ANSWER_HINT_PREFIX)][0][:300])
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
