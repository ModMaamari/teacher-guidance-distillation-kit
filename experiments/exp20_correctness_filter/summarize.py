#!/usr/bin/env python
"""E20 summary: correct-only vs mixed training episodes, across seeds.

Reads the E20 view (one folder per arm, symlinked to runs/eval/<run>, plus verdicts.jsonl) and
the results.json that collect_results.py wrote for it. Arms are named <family><seed>
(correct13, mixall17, ...) or by a plain name (base, wrongonly). Prints, per family, the
judge-correct accuracy of every seed with mean and SD, steps, tokens per question, voluntary
finishes and median answer length; then each contrast seed by seed (paired bootstrap CI and exact
McNemar from results.json) and seed-averaged: every question's accuracy is averaged over the seeds
of each family, and the per-question difference gets a bootstrap 95 % CI and a sign-flip
permutation p over the questions. Holm is applied over the primary contrasts. Other studies
name their own contrasts (E19: ``--primary tg:self --secondary -``).

    python experiments/exp20_correctness_filter/summarize.py --view runs/views/E20 \\
        --results runs/results/E20/results.json --json-out runs/results/E20/summary.json
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import statistics as st
from pathlib import Path

import numpy as np

FAMILY_RE = re.compile(r"^([a-z_]+?)(\d+)?$")
PRIMARY = [("correct", "mixall"), ("correct", "mixmatch")]
SECONDARY = [("mixmatch", "mixall"), ("wrongonly", "correct"), ("base", "wrongonly")]


def per_question(view: Path) -> dict[str, dict[tuple[str, str], int]]:
    """arm -> {(test set, qid): judge verdict} for every judged episode of the view."""
    verdicts: dict[str, dict[str, int]] = collections.defaultdict(dict)
    with open(view / "verdicts.jsonl", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                r = json.loads(line)
                verdicts[str(Path(r["source"]).resolve())][r["qid"]] = int(bool(r["verdict"]["correct"]))
    out: dict[str, dict[tuple[str, str], int]] = {}
    for arm_dir in sorted(p for p in view.iterdir() if p.is_dir()):
        got = {}
        for ep_file in sorted(arm_dir.glob("*/episodes.jsonl")):
            v = verdicts.get(str(ep_file.resolve()), {})
            for q in v:
                got[(ep_file.parent.name, q)] = v[q]
        out[arm_dir.name] = got
    return out


def answer_words(view: Path, arm: str) -> float:
    words = []
    for ep_file in (view / arm).glob("*/episodes.jsonl"):
        with open(ep_file, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    words.append(len(str(json.loads(line).get("final_answer") or "").split()))
    return float(np.median(words)) if words else float("nan")


def seed_averaged(pq, a_arms, b_arms, n_boot=10000, seed=0):
    """Mean over questions of (mean over b's seeds - mean over a's seeds), in points."""
    keys = sorted(set.intersection(*(set(pq[x]) for x in a_arms + b_arms)))
    a = np.array([[pq[x][k] for x in a_arms] for k in keys], dtype=float).mean(axis=1)
    b = np.array([[pq[x][k] for x in b_arms] for k in keys], dtype=float).mean(axis=1)
    d = b - a
    rng = np.random.default_rng(seed)
    boots = d[rng.integers(0, len(d), size=(n_boot, len(d)))].mean(axis=1)
    flips = (rng.integers(0, 2, size=(n_boot, len(d))) * 2 - 1) * d
    p = (np.sum(np.abs(flips.mean(axis=1)) >= abs(d.mean()) - 1e-12) + 1) / (n_boot + 1)
    return {"diff": round(100 * d.mean(), 2), "ci95": [round(100 * float(np.percentile(boots, 2.5)), 2),
            round(100 * float(np.percentile(boots, 97.5)), 2)], "p": round(float(p), 4), "n": len(keys),
            "a": a_arms, "b": b_arms}


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, running = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = running
    return adj


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--view", default="runs/views/E20")
    ap.add_argument("--results", default="runs/results/E20/results.json")
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--primary", nargs="+", default=[f"{x}:{y}" for x, y in PRIMARY],
                    help="family contrasts a:b (b - a), Holm-corrected together")
    ap.add_argument("--secondary", nargs="+", default=[f"{x}:{y}" for x, y in SECONDARY],
                    help="further contrasts a:b, uncorrected; '-' for none")
    a = ap.parse_args()
    primary = [tuple(c.split(":")) for c in a.primary if c != "-"]
    secondary = [tuple(c.split(":")) for c in a.secondary if c != "-"]
    view = Path(a.view)
    res = json.loads(Path(a.results).read_text(encoding="utf-8"))
    pooled, paired = res["pooled"], res["paired"]
    pq = per_question(view)

    families: dict[str, dict[str, str]] = collections.defaultdict(dict)   # family -> seed -> arm
    for arm in pooled:
        m = FAMILY_RE.match(arm)
        if m:
            families[m.group(1)][m.group(2) or "13"] = arm

    out = {"families": {}, "per_seed": {}, "seed_averaged": {}}
    print("metric: judge-correct accuracy (%) on the held-out questions; steps and tokens per question\n")
    print(f"  {'family':<10}{'seeds':>22}{'mean':>8}{'sd':>6}{'steps':>7}{'tokens':>8}{'vol.fin':>8}{'words':>7}")
    for fam, seeds in families.items():
        arms = [seeds[s] for s in sorted(seeds, key=int)]
        acc = [100 * pooled[x]["judge_correct"] for x in arms]
        row = {
            "arms": arms, "acc": [round(v, 2) for v in acc], "mean": round(st.mean(acc), 2),
            "sd": round(st.stdev(acc), 2) if len(acc) > 1 else None,
            "steps": round(st.mean(pooled[x]["mean_steps"] for x in arms), 2),
            "tokens": round(st.mean(pooled[x]["total_tokens_per_ep"] for x in arms)),
            "voluntary_finish": round(100 * st.mean(pooled[x]["voluntary_finish"] for x in arms), 1),
            "median_words": st.mean(answer_words(view, x) for x in arms),
        }
        for x in arms:   # the per-question table must agree with collect_results
            mine = 100 * np.mean(list(pq[x].values())) if pq[x] else float("nan")
            if abs(mine - 100 * pooled[x]["judge_correct"]) > 0.15:
                print(f"!! {x}: per-question accuracy {mine:.2f} != results.json {100 * pooled[x]['judge_correct']:.2f}")
        out["families"][fam] = row
        sd = f"{row['sd']:.1f}" if row["sd"] is not None else "-"
        print(f"  {fam:<10}{' / '.join(f'{v:.1f}' for v in acc):>22}{row['mean']:>8.1f}{sd:>6}"
              f"{row['steps']:>7.2f}{row['tokens']:>8,}{row['voluntary_finish']:>8.1f}{row['median_words']:>7.1f}")

    print("\nper seed (b - a, pooled paired bootstrap 95 % CI, exact McNemar):")
    for fa, fb in primary + secondary:
        if fa not in families or fb not in families:
            continue
        for s in sorted(set(families[fa]) & set(families[fb]), key=int) or []:
            x, y = families[fa][s], families[fb][s]
            pr = paired.get(f"{x} -> {y}") or paired.get(f"{y} -> {x}")
            if not pr:
                continue
            sign = 1 if f"{x} -> {y}" in paired else -1
            p = pr["pooled"]
            lo, hi = sorted(sign * 100 * c for c in p["ci95"])
            out["per_seed"][f"{x} -> {y}"] = {"diff": round(sign * 100 * p["diff"], 2), "ci95": [lo, hi], "p": p["p"]}
            print(f"  {x:>12} -> {y:<12}{sign * 100 * p['diff']:+7.1f}  [{lo:+.1f}, {hi:+.1f}]  p {p['p']:.4f}")

    print("\nseed-averaged (each question averaged over the seeds of each family):")
    contrasts = [(fa, fb) for fa, fb in primary + secondary if fa in families and fb in families]
    for fa, fb in contrasts:
        r = seed_averaged(pq, [families[fa][s] for s in sorted(families[fa], key=int)],
                          [families[fb][s] for s in sorted(families[fb], key=int)])
        out["seed_averaged"][f"{fa} -> {fb}"] = r
    prim = [f"{fa} -> {fb}" for fa, fb in primary if f"{fa} -> {fb}" in out["seed_averaged"]]
    for k, h in zip(prim, holm([out["seed_averaged"][k]["p"] for k in prim])):
        out["seed_averaged"][k]["holm"] = round(h, 4)
    for k, r in out["seed_averaged"].items():
        extra = f"  Holm {r['holm']:.4f}" if "holm" in r else ""
        print(f"  {k:<24}{r['diff']:+7.1f}  [{r['ci95'][0]:+.1f}, {r['ci95'][1]:+.1f}]  "
              f"p {r['p']:.4f}{extra}  (n {r['n']}, seeds {len(r['a'])} vs {len(r['b'])})")

    if a.json_out:
        Path(a.json_out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
