"""Aggregate the forgetting-eval runs into statistics, tables and box plots.

Handles both layouts written by slurm/eval_forgetting.sbatch:

    runs/forgetting/<arm>/<benchmark>/            a single greedy run
    runs/forgetting/<run>/<arm>/<benchmark>/      replicates (run1..runN, sampled)

With replicates it reports, per benchmark and pooled:

* per-run accuracy for each arm, then mean, variance, standard deviation and the 95 %
  confidence interval of the mean (Student t, n-1 degrees of freedom);
* the paired difference across runs, tested with a paired t-test and the exact Wilcoxon
  signed-rank test (both on the R paired run accuracies);
* an item-level exact McNemar test on the pooled predictions of all runs, which uses all
  R x N decisions rather than R summary numbers;
* box plots (inline SVG, no dependencies) of the per-run accuracy distributions.

With a single run it reports the point estimates and an item-level paired bootstrap CI.

Usage::

    python scripts/forgetting_report.py --runs runs/forgetting --out runs/forgetting/report
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # project root -> import tgd/agentsim

import argparse
import json
import math
import random
import statistics as st
from typing import Dict, List

BENCH_ORDER = ["mmlu", "gsm8k", "hellaswag"]
NAMES = {"mmlu": "MMLU", "gsm8k": "GSM8K", "hellaswag": "HellaSwag", "pooled": "Pooled"}


# ----------------------------------------------------------------- loading
def discover(root: Path):
    """-> {run: {arm: {benchmark: predictions_path}}}; a flat layout becomes run 'greedy'."""
    found: Dict[str, Dict[str, Dict[str, Path]]] = {}
    for p in sorted(root.glob("**/predictions.jsonl")):
        rel = p.relative_to(root).parts
        if len(rel) == 4:                      # <run>/<arm>/<benchmark>/predictions.jsonl
            run, arm, bench = rel[0], rel[1], rel[2]
        elif len(rel) == 3:                    # <arm>/<benchmark>/predictions.jsonl
            run, arm, bench = "greedy", rel[0], rel[1]
        else:
            continue
        found.setdefault(run, {}).setdefault(arm, {})[bench] = p
    return found


def load_preds(path: Path) -> Dict[str, dict]:
    return {r["id"]: r for r in (json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip())}


# ----------------------------------------------------------------- statistics
def mean_ci(xs: List[float]):
    """Mean, variance, sd and the 95 % t-interval of the mean."""
    n = len(xs)
    m = st.mean(xs)
    if n < 2:
        return {"mean": m, "variance": 0.0, "sd": 0.0, "sem": 0.0, "ci95": [m, m], "n": n}
    var = st.variance(xs)
    sd = math.sqrt(var)
    sem = sd / math.sqrt(n)
    # two-sided 95 % t critical values, df = n-1
    tcrit = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365,
             8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179}.get(n - 1, 1.96)
    return {"mean": m, "variance": var, "sd": sd, "sem": sem,
            "ci95": [m - tcrit * sem, m + tcrit * sem], "n": n}


def paired_tests(a: List[float], b: List[float]):
    """Paired t-test and exact Wilcoxon signed-rank on R paired run accuracies."""
    out: Dict[str, object] = {}
    d = [y - x for x, y in zip(a, b)]
    n = len(d)
    out["mean_diff"] = st.mean(d) if d else 0.0
    if n >= 2 and any(x != 0 for x in d):
        sd = st.stdev(d)
        t = st.mean(d) / (sd / math.sqrt(n)) if sd > 0 else float("inf")
        out["t"] = t
        out["t_df"] = n - 1
        out["t_p"] = _t_sf(abs(t), n - 1) * 2
        out["wilcoxon_p"] = _wilcoxon_exact(d)
    return out


def _t_sf(t: float, df: int) -> float:
    """Upper-tail probability of Student's t (continued-fraction incomplete beta)."""
    if t == float("inf"):
        return 0.0
    x = df / (df + t * t)
    return 0.5 * _betainc(df / 2.0, 0.5, x)


def _betainc(a: float, b: float, x: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(math.log(x) * a + math.log(1 - x) * b - lbeta) / a
    f, c, d = 1.0, 1.0, 0.0
    for i in range(0, 300):
        m = i // 2
        if i == 0:
            num = 1.0
        elif i % 2 == 0:
            num = (m * (b - m) * x) / ((a + 2 * m - 1) * (a + 2 * m))
        else:
            num = -((a + m) * (a + b + m) * x) / ((a + 2 * m) * (a + 2 * m + 1))
        d = 1.0 + num * d
        d = 1e-30 if abs(d) < 1e-30 else d
        d = 1.0 / d
        c = 1.0 + num / c
        c = 1e-30 if abs(c) < 1e-30 else c
        f *= c * d
        if abs(1.0 - c * d) < 1e-10:
            break
    return front * (f - 1.0)


def _wilcoxon_exact(d: List[float]) -> float:
    """Exact two-sided signed-rank p over all 2^n sign assignments (n is small here)."""
    nz = [x for x in d if x != 0]
    n = len(nz)
    if n == 0:
        return 1.0
    order = sorted(range(n), key=lambda i: abs(nz[i]))
    ranks = [0.0] * n
    for r, i in enumerate(order, start=1):
        ranks[i] = float(r)
    w_obs = sum(ranks[i] for i in range(n) if nz[i] > 0)
    count = 0
    total = 1 << n
    for mask in range(total):
        w = sum(ranks[i] for i in range(n) if mask >> i & 1)
        if abs(w - n * (n + 1) / 4.0) >= abs(w_obs - n * (n + 1) / 4.0) - 1e-12:
            count += 1
    return min(1.0, count / total)


def mcnemar_exact(a: List[int], b: List[int]):
    b01 = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    b10 = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    m = b01 + b10
    if m == 0:
        return {"b_wins": 0, "a_wins": 0, "p": 1.0}
    k = min(b01, b10)
    return {"b_wins": b01, "a_wins": b10,
            "p": min(1.0, 2 * sum(math.comb(m, i) for i in range(k + 1)) / 2 ** m)}


def paired_bootstrap(a: List[int], b: List[int], iters=10000, seed=13):
    rnd = random.Random(seed)
    n = len(a)
    if n == 0:
        return None
    d = [b[i] - a[i] for i in range(n)]
    boots = sorted(sum(d[rnd.randrange(n)] for _ in range(n)) / n for _ in range(iters))
    return {"diff": sum(d) / n, "ci95": [boots[int(0.025 * iters)], boots[int(0.975 * iters) - 1]]}


# ----------------------------------------------------------------- box plot (inline SVG)
def boxplot_svg(groups: Dict[str, Dict[str, List[float]]], title: str) -> str:
    """groups: {benchmark: {arm: [per-run accuracy]}} -> one SVG with a box per arm."""
    arms = sorted({a for g in groups.values() for a in g})
    colors = {arms[0]: "#8a94a6", arms[-1]: "#1f5f8b"}
    W, H, L, R, T, B = 760, 300, 52, 16, 34, 54
    vals = [v for g in groups.values() for a in g.values() for v in a]
    if not vals:
        return ""
    lo, hi = min(vals), max(vals)
    pad = max((hi - lo) * 0.25, 0.01)
    lo, hi = max(0.0, lo - pad), min(1.0, hi + pad)
    def y(v):
        return T + (H - T - B) * (1 - (v - lo) / max(hi - lo, 1e-9))
    gw = (W - L - R) / len(groups)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{title}" class="chart">']
    for i in range(5):
        v = lo + (hi - lo) * i / 4
        out.append(f'<line x1="{L}" y1="{y(v):.1f}" x2="{W-R}" y2="{y(v):.1f}" class="grid"/>')
        out.append(f'<text x="{L-8}" y="{y(v)+4:.1f}" class="ax" text-anchor="end">{v*100:.0f}%</text>')
    for gi, (bench, arms_vals) in enumerate(groups.items()):
        x0 = L + gi * gw
        n_arms = len(arms_vals)
        bw = gw / (n_arms + 1.4)
        for ai, arm in enumerate(sorted(arms_vals)):
            xs = sorted(arms_vals[arm])
            if not xs:
                continue
            q1, med, q3 = _quartiles(xs)
            x = x0 + bw * (0.7 + ai)
            c = colors.get(arm, "#a8672a")
            out.append(f'<line x1="{x+bw*0.4:.1f}" y1="{y(xs[0]):.1f}" x2="{x+bw*0.4:.1f}" y2="{y(xs[-1]):.1f}" class="whisk"/>')
            out.append(f'<rect x="{x:.1f}" y="{y(q3):.1f}" width="{bw*0.8:.1f}" height="{max(y(q1)-y(q3),1):.1f}" fill="{c}" fill-opacity="0.30" stroke="{c}"/>')
            out.append(f'<line x1="{x:.1f}" y1="{y(med):.1f}" x2="{x+bw*0.8:.1f}" y2="{y(med):.1f}" stroke="{c}" stroke-width="2.5"/>')
            for v in xs:
                out.append(f'<circle cx="{x+bw*0.4:.1f}" cy="{y(v):.1f}" r="2.4" fill="{c}"/>')
            out.append(f'<text x="{x+bw*0.4:.1f}" y="{H-B+16}" class="ax" text-anchor="middle">{arm}</text>')
        out.append(f'<text x="{x0+gw/2:.1f}" y="{H-B+34}" class="ax lab" text-anchor="middle">{NAMES.get(bench, bench)}</text>')
    out.append("</svg>")
    return "\n".join(out)


def _quartiles(xs: List[float]):
    n = len(xs)
    def q(p):
        if n == 1:
            return xs[0]
        k = (n - 1) * p
        f = math.floor(k)
        c = min(f + 1, n - 1)
        return xs[f] + (xs[c] - xs[f]) * (k - f)
    return q(0.25), q(0.5), q(0.75)


# ----------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", default="runs/forgetting")
    ap.add_argument("--out", default="runs/forgetting/report")
    ap.add_argument("--base-arm", default="base")
    ap.add_argument("--metric", choices=["strict_correct", "lenient_correct"], default="strict_correct")
    args = ap.parse_args()
    root, out = Path(args.runs), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    found = discover(root)
    if not found:
        print(f"no predictions under {root}")
        return 1
    runs = sorted(found)
    arms = sorted({a for r in found.values() for a in r})
    other = [a for a in arms if a != args.base_arm]
    if not other:
        print(f"only one arm found ({arms}); nothing to compare")
        return 1
    trained = other[0]
    benches = [b for b in BENCH_ORDER if any(b in found[r].get(a, {}) for r in runs for a in arms)]

    # per (run, arm, benchmark) accuracy on the items both arms answered in that run
    acc: Dict[str, Dict[str, Dict[str, float]]] = {}
    fmt: Dict[str, Dict[str, Dict[str, float]]] = {}
    items: Dict[str, Dict[str, Dict[str, Dict[str, int]]]] = {}
    for r in runs:
        for b in benches:
            pa = found[r].get(args.base_arm, {}).get(b)
            pb = found[r].get(trained, {}).get(b)
            if not pa or not pb:
                continue
            A, B = load_preds(pa), load_preds(pb)
            common = sorted(set(A) & set(B))
            for arm, P in ((args.base_arm, A), (trained, B)):
                acc.setdefault(r, {}).setdefault(arm, {})[b] = sum(P[i][args.metric] for i in common) / len(common)
                fmt.setdefault(r, {}).setdefault(arm, {})[b] = sum(P[i]["strict_format_ok"] for i in common) / len(common)
                items.setdefault(r, {}).setdefault(arm, {})[b] = {i: P[i][args.metric] for i in common}
            acc[r].setdefault("_n", {})[b] = len(common)

    scopes = benches + (["pooled"] if len(benches) > 1 else [])
    result: Dict[str, object] = {"runs": runs, "arms": [args.base_arm, trained], "metric": args.metric,
                                 "benchmarks": benches, "per_run": {}, "summary": {}, "tests": {}}
    for r in runs:
        result["per_run"][r] = {a: dict(acc.get(r, {}).get(a, {})) for a in (args.base_arm, trained)}
        if len(benches) > 1:
            for a in (args.base_arm, trained):
                tot = sum(acc[r]["_n"][b] for b in benches)
                result["per_run"][r][a]["pooled"] = sum(acc[r][a][b] * acc[r]["_n"][b] for b in benches) / tot

    for scope in scopes:
        row = {}
        series = {}
        for a in (args.base_arm, trained):
            xs = [result["per_run"][r][a][scope] for r in runs if scope in result["per_run"][r][a]]
            series[a] = xs
            row[a] = {**mean_ci(xs), "per_run": xs,
                      "format_ok_mean": st.mean([fmt[r][a][b] for r in runs for b in ([scope] if scope != "pooled" else benches) if b in fmt.get(r, {}).get(a, {})]) if fmt else None}
        row["tests"] = paired_tests(series[args.base_arm], series[trained])
        # item-level McNemar over every decision of every run
        xa = [items[r][args.base_arm][b][i] for r in runs for b in (benches if scope == "pooled" else [scope])
              for i in sorted(items[r][args.base_arm][b])]
        xb = [items[r][trained][b][i] for r in runs for b in (benches if scope == "pooled" else [scope])
              for i in sorted(items[r][trained][b])]
        row["tests"]["mcnemar_items"] = {**mcnemar_exact(xa, xb), "n_decisions": len(xa)}
        if len(runs) == 1:
            row["tests"]["bootstrap_items"] = paired_bootstrap(xa, xb)
        result["summary"][scope] = row

    (out / "stats.json").write_text(json.dumps(result, indent=2, default=float), encoding="utf-8")
    svg = boxplot_svg({b: {a: result["summary"][b][a]["per_run"] for a in (args.base_arm, trained)} for b in benches},
                      "per-run accuracy by benchmark")
    (out / "boxplot.svg").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" '
        + svg[len("<svg"):].replace("class=\"chart\"", 'style="background:#fff"', 1)
          .replace('class="grid"', 'stroke="#d5d9e2"').replace('class="ax"', 'font-size="11" fill="#727a8a" font-family="monospace"')
          .replace('class="ax lab"', 'font-size="12" fill="#464e5e" font-family="sans-serif"')
          .replace('class="whisk"', 'stroke="#727a8a"'),
        encoding="utf-8")

    # markdown
    md = [f"# Forgetting check — {len(runs)} run(s), metric: {args.metric.replace('_correct','')}", "",
          f"Arms: `{args.base_arm}` vs `{trained}`. Same items, one server, adapter is the only difference.", "",
          "| Scope | Arm | Mean | SD | Variance | 95% CI of the mean | Per-run |",
          "|---|---|---|---|---|---|---|"]
    for scope in scopes:
        for a in (args.base_arm, trained):
            s = result["summary"][scope][a]
            md.append(f"| {NAMES.get(scope, scope) if a == args.base_arm else ''} | {a} | {s['mean']*100:.2f}% | "
                      f"{s['sd']*100:.2f} | {s['variance']*1e4:.3f}e-4 | "
                      f"[{s['ci95'][0]*100:.2f}, {s['ci95'][1]*100:.2f}] | "
                      f"{', '.join(f'{v*100:.2f}' for v in s['per_run'])} |")
    md += ["", "## Significance", "",
           "| Scope | Δ mean (pts) | paired t | df | t p | Wilcoxon p | item-level McNemar p | decisions |",
           "|---|---|---|---|---|---|---|---|"]
    for scope in scopes:
        t = result["summary"][scope]["tests"]
        mc = t["mcnemar_items"]
        md.append(f"| {NAMES.get(scope, scope)} | {t.get('mean_diff', 0)*100:+.2f} | "
                  f"{t.get('t', float('nan')):.3f} | {t.get('t_df', '—')} | "
                  f"{_fmt_p(t.get('t_p'))} | {_fmt_p(t.get('wilcoxon_p'))} | {_fmt_p(mc['p'])} | {mc['n_decisions']:,} |")
    (out / "REPORT.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"\nwrote {out/'stats.json'}, {out/'REPORT.md'}, {out/'boxplot.svg'}")
    return 0


def _fmt_p(p):
    if p is None:
        return "—"
    return "<1e-6" if p < 1e-6 else f"{p:.4g}"


if __name__ == "__main__":
    raise SystemExit(main())
