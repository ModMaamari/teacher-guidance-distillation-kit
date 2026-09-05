#!/usr/bin/env python
"""Accuracy vs. number of training episodes, from a collect_results.py results.json.

Reads the pooled per-arm numbers, maps each arm name to the episode count it was
trained on (``base`` -> 0, ``ep<N>`` -> N), and draws one line per accuracy metric with a
Wilson 95% interval band on the primary one. Writes PNG + SVG + a tidy CSV.

Usage::

    python scripts/plot_size_curve.py --results runs/results/results.json --out runs/results
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path

# Metrics in reporting order, and the categorical slots of the validated default palette.
# Colour is assigned to the series that are actually present, in slot order: a run without
# judge verdicts starts at slot 1 rather than leaving blue unused and opening on orange.
SERIES = [
    ("judge_correct", "LLM judge"),
    ("cover_match",   "Cover"),
    ("f1",            "Token F1"),
    ("em",            "Exact match"),
]
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
INK_1, INK_2, INK_3 = "#0b0b0b", "#52514e", "#8a8880"
SURFACE, GRID = "#fcfcfb", "#e6e5e1"


def wilson(k: int, n: int, z: float = 1.96):
    """95% Wilson interval — the right one at n=100 near the tails, where the normal
    approximation puts a bound outside [0, 1]."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def episodes_of(arm: str):
    if arm in ("base", "base_student", "ep0"):
        return 0
    m = re.search(r"ep(\d+)", arm)
    return int(m.group(1)) if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", default="runs/results/results.json")
    ap.add_argument("--out", default="runs/results")
    ap.add_argument("--title", default="Trained-student accuracy vs. teacher-guided episodes")
    ap.add_argument("--subtitle", default="")
    args = ap.parse_args()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    res = json.loads(Path(args.results).read_text(encoding="utf-8"))
    pooled = res["pooled"]
    pts = sorted(((episodes_of(a), a, r) for a, r in pooled.items() if episodes_of(a) is not None),
                 key=lambda t: t[0])
    if not pts:
        print("no arms named base/ep<N> in", args.results)
        return 2
    xs = [p[0] for p in pts]

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    with (out / "size_curve.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["episodes", "arm", "n"] + [k for k, _ in SERIES])
        for x, arm, r in pts:
            w.writerow([x, arm, r["n"]] + [r.get(k) for k, _ in SERIES])

    live = [(k, lab, PALETTE[i]) for i, (k, lab) in enumerate(
        [(k, lab) for k, lab in SERIES
         if any(p[2].get(k) is not None for p in pts)])]

    fig, ax = plt.subplots(figsize=(8.4, 5.2), dpi=200)
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)

    # 95% Wilson band on the primary metric only — one band reads, four overlap into mud
    pk = live[0][0]
    n = pts[0][2]["n"]
    lo = [wilson(round(p[2][pk] * p[2]["n"]), p[2]["n"])[0] for p in pts]
    hi = [wilson(round(p[2][pk] * p[2]["n"]), p[2]["n"])[1] for p in pts]
    ax.fill_between(xs, lo, hi, color=live[0][2], alpha=0.13, linewidth=0, zorder=1)

    for k, label, colour in live:
        ys = [p[2].get(k) for p in pts]
        ax.plot(xs, ys, color=colour, linewidth=2, zorder=3, solid_capstyle="round")
        ax.plot(xs, ys, "o", color=colour, markersize=8, markeredgecolor=SURFACE,
                markeredgewidth=2, zorder=4)
        # direct label at the right end: identity is never carried by colour alone
        ax.annotate(f"{label}  {ys[-1]:.0%}", (xs[-1], ys[-1]), textcoords="offset points",
                    xytext=(12, 0), va="center", ha="left", fontsize=9.5, color=INK_2)

    ax.set_xlim(-max(xs) * 0.06, max(xs) * 1.42)
    top = max(max(p[2].get(k) or 0 for p in pts) for k, _, _ in live)
    ax.set_ylim(0, min(1.0, max(0.35, top * 1.25)))
    ax.set_xticks(xs)
    ax.set_xticklabels([f"{x:,}" if x else "0\n(base)" for x in xs], fontsize=9.5, color=INK_2)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.tick_params(axis="y", labelsize=9.5, colors=INK_2, length=0)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="y", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)

    ax.set_xlabel("teacher-guided episodes used for SFT", fontsize=10, color=INK_2, labelpad=14)
    ax.set_title(args.title, fontsize=13.5, color=INK_1, loc="left", pad=22 if args.subtitle else 12)
    if args.subtitle:
        ax.text(0, 1.035, args.subtitle, transform=ax.transAxes, fontsize=9.5, color=INK_3)
    ax.legend([plt.Line2D([], [], color=c, linewidth=2) for _, _, c in live],
              [lab for _, lab, _ in live], frameon=False, fontsize=9.5, labelcolor=INK_2,
              loc="upper left", bbox_to_anchor=(0, -0.235), ncol=len(live), handlelength=1.6,
              columnspacing=1.8)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(out / f"size_curve.{ext}", facecolor=SURFACE, bbox_inches="tight")
    print(f"wrote {out/'size_curve.png'}, {out/'size_curve.svg'}, {out/'size_curve.csv'}")
    for x, arm, r in pts:
        print(f"  {x:>5} ep  {arm:<12} n={r['n']:<4} " +
              "  ".join(f"{k}={r.get(k)}" for k, _, _ in live))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
