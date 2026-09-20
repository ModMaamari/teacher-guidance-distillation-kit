#!/usr/bin/env python
"""How often does the correctness filter disagree with the judge?

The filter that builds every training split keeps an episode when its final answer covers the
gold answer (a string match, ``tgd.metrics.cover_match``), never asking an LLM. E15 judged the
same collected episodes with the paper's judge, so the two can be crossed: the episodes the
filter throws away include answers that are right but phrased differently, and the ones it keeps
include answers the judge rejects. Reads E15's per-question file (self-guided collection).

    python experiments/exp20_correctness_filter/filter_vs_judge.py
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--per-question", default="results/E15_teacher_datasets/per_question.jsonl")
    ap.add_argument("--collection", default="self", help="key in the per-question file")
    a = ap.parse_args()
    c = collections.Counter()
    for line in (KIT / a.per_question).read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = (json.loads(line).get(a.collection) or {})
            if "judge" in r and "cover" in r:
                c[(bool(r["cover"]), bool(r["judge"]))] += 1
    n = sum(c.values())
    kept, dropped = c[(True, True)] + c[(True, False)], c[(False, True)] + c[(False, False)]
    print(f"collection: {a.collection}   episodes: {n:,}\n")
    print(f"  {'':<22}{'judged correct':>16}{'judged wrong':>16}")
    print(f"  {'filter keeps':<22}{c[(True, True)]:>16,}{c[(True, False)]:>16,}")
    print(f"  {'filter drops':<22}{c[(False, True)]:>16,}{c[(False, False)]:>16,}\n")
    print(f"  kept {kept:,} ({100 * kept / n:.1f}% of episodes); of them {100 * c[(True, False)] / kept:.1f}% "
          f"are judged wrong")
    print(f"  dropped {dropped:,}; of them {100 * c[(False, True)] / dropped:.1f}% are judged correct "
          f"(right answer, different wording)")
    print(f"\n  filter accept rate {100 * kept / n:.1f}%, judge accept rate "
          f"{100 * (c[(True, True)] + c[(False, True)]) / n:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
