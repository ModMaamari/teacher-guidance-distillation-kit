#!/usr/bin/env python3
"""Does answer form (verbosity) move the ranking? Accuracy of every arm under several judges,
and paired differences between chosen arm pairs under each judge.

    python report.py --runs runs/eval --arms base seed13 selftaught ... \
        --judge primary=runs/judge --judge strict=runs/judge_e18/strict --judge kimi=... \
        --pair seed13:selftaught --pair sup_selfdist:sup_selftaught

A judge given as a directory contributes every ``*/verdicts.jsonl`` under it (the pool writes
the primary judge's verdicts per arm) or its own ``verdicts.jsonl``.
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tgd.stats import mcnemar_exact, paired_bootstrap  # noqa: E402


def verdicts(d: Path, runs: str) -> dict:
    files = [d / "verdicts.jsonl"] if (d / "verdicts.jsonl").exists() else sorted(d.glob("*/verdicts.jsonl"))
    out = {}
    for f in files:
        for line in open(f, encoding="utf-8"):
            if line.strip():
                r = json.loads(line)
                c = (r.get("verdict") or {}).get("correct")
                if c is not None and r["source"].startswith(runs.rstrip("/") + "/"):
                    p = Path(r["source"])
                    out[(p.parent.parent.name, p.parent.name, r["qid"])] = int(c)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", default="runs/eval")
    ap.add_argument("--arms", nargs="+", required=True)
    ap.add_argument("--judge", action="append", required=True, metavar="NAME=DIR")
    ap.add_argument("--pair", action="append", default=[], metavar="A:B")
    a = ap.parse_args()
    runs = Path(a.runs)
    keys, words = {}, {}
    for arm in a.arms:
        ks, ws = [], []
        for f in sorted(runs.glob(f"{arm}/heldout_*/episodes.jsonl")):
            for line in open(f, encoding="utf-8"):
                if line.strip():
                    e = json.loads(line)
                    ks.append((arm, f.parent.name, e["qid"]))
                    ws.append(len(str(e.get("final_answer") or "").split()))
        keys[arm], words[arm] = ks, ws
    judges = {n: verdicts(Path(d), a.runs) for n, _, d in (j.partition("=") for j in a.judge)}

    print("## Accuracy by judge (judge-correct, %; n judged in brackets)\n")
    print("| Arm | median answer words | " + " | ".join(judges) + " |")
    print("|---|---|" + "---|" * len(judges))
    for arm in a.arms:
        cells = []
        for v in judges.values():
            xs = [v[k] for k in keys[arm] if k in v]
            cells.append(f"{100 * sum(xs) / len(xs):.1f} ({len(xs)})" if xs else "—")
        print(f"| {arm} | {st.median(words[arm]) if words[arm] else '—'} | " + " | ".join(cells) + " |")

    if a.pair:
        print("\n## Paired differences, b − a (points, 95 % CI, McNemar p)\n")
        print("| a → b | " + " | ".join(judges) + " |")
        print("|---|" + "---|" * len(judges))
        for spec in a.pair:
            x, y = spec.split(":")
            cells = []
            for v in judges.values():
                qa = {k[1:]: v[k] for k in keys[x] if k in v}
                qb = {k[1:]: v[k] for k in keys[y] if k in v}
                common = sorted(set(qa) & set(qb))
                if not common:
                    cells.append("—")
                    continue
                va, vb = [qa[q] for q in common], [qb[q] for q in common]
                b = paired_bootstrap(va, vb)
                p = mcnemar_exact(va, vb)
                p = p.get("p") if isinstance(p, dict) else p
                cells.append(f"{100 * b['diff']:+.1f} [{100 * b['ci95'][0]:+.1f}, {100 * b['ci95'][1]:+.1f}] p={p:.2g}")
            print(f"| {x} → {y} | " + " | ".join(cells) + " |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
