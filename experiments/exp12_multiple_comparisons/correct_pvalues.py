#!/usr/bin/env python3
"""Holm-Bonferroni and Benjamini-Hochberg correction over the paired tests in results.json.

Six pairwise tests from four arms already put the family-wise error rate near 26 % at
alpha 0.05. Every extra experiment adds more. This says which conclusions survive.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys


def holm(ps: list[float]) -> list[float]:
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i])
    adj = [0.0] * m
    prev = 0.0
    for rank, i in enumerate(order):
        val = min(1.0, (m - rank) * ps[i])
        prev = max(prev, val)
        adj[i] = prev
    return adj


def bh(ps: list[float]) -> list[float]:
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i])
    adj = [0.0] * m
    prev = 1.0
    for rank in range(m - 1, -1, -1):
        i = order[rank]
        val = min(1.0, ps[i] * m / (rank + 1))
        prev = min(prev, val)
        adj[i] = prev
    return adj


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="runs/results/results.json")
    ap.add_argument("--scope", default="pooled")
    ap.add_argument("--alpha", type=float, default=0.05)
    a = ap.parse_args()

    p = pathlib.Path(a.results)
    if not p.exists():
        print(f"!! {p} not found -- run collect_results.py first", file=sys.stderr)
        return 1
    paired = json.loads(p.read_text(encoding="utf-8")).get("paired", {})

    names, ps, diffs = [], [], []
    for pair, scopes in paired.items():
        row = scopes.get(a.scope) or (scopes.get(next(iter(scopes))) if scopes else None)
        if not row or row.get("p") is None:
            continue
        names.append(pair)
        ps.append(float(row["p"]))
        diffs.append(row.get("diff"))
    if not ps:
        print(f"no paired tests with scope {a.scope!r} in {p}")
        return 1

    h, b = holm(ps), bh(ps)
    print(f"{len(ps)} comparisons, alpha {a.alpha}   "
          f"(uncorrected family-wise error ~{1 - (1 - a.alpha) ** len(ps):.0%})\n")
    print(f"  {'comparison':<44}{'diff':>8}{'raw p':>11}{'Holm':>11}{'BH':>11}  verdict")
    for i in sorted(range(len(ps)), key=lambda i: ps[i]):
        d = f"{diffs[i]:+.1f}" if isinstance(diffs[i], (int, float)) else "-"
        if h[i] < a.alpha:
            v = "survives Holm"
        elif b[i] < a.alpha:
            v = "survives BH only"
        else:
            v = "NOT significant"
        raw = f"{ps[i]:.2e}" if ps[i] < 1e-4 else f"{ps[i]:.4f}"
        print(f"  {names[i]:<44}{d:>8}{raw:>11}{h[i]:>11.4f}{b[i]:>11.4f}  {v}")
    print("\nReport which correction you used. 'Survives Holm' is the strong claim.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
