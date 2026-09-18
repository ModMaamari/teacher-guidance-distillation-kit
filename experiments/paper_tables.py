#!/usr/bin/env python3
"""Write the paper's LaTeX tables from the published results, never from runs/.

    python experiments/paper_tables.py            # every table whose results exist
    python experiments/paper_tables.py E00 E13    # only these

Each table lands next to its numbers as ``table.tex`` (booktabs; ``\\label`` = the registry's
``paper`` key) and a line per table is printed. An experiment whose results are not published
yet is skipped. Accuracy is the primary judge's (judge-correct, %); differences are paired, with
the bootstrap 95 % CI and the exact McNemar p-value from scripts/collect_results.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

KIT = Path(__file__).resolve().parents[1]
DS = [("hotpotqa", "HotpotQA"), ("2wikimultihopqa", "2Wiki"), ("musique", "MuSiQue"), ("strategyqa", "StrategyQA")]

# experiment -> results table, arm order with row labels, and the baseline for the Δ column
ARMS = {
    "E00": ("E00_reference/gemma", [("base", "Base student"), ("guided", "Guided student (live teacher)"),
                                    ("trained", "Trained student"), ("teacher", "Teacher alone")], "base"),
    "E01": ("E01_supervision_ablation/kit", [("base", "Base student"), ("selfdist", "Student's own rollouts"),
                                             ("teachdist", "Teacher's own rollouts"),
                                             ("guided", "Teacher-guided rollouts")], "base"),
    "E02": ("E02_seed_variance/kit", [("base", "Base student"), ("seed13", "Trained, seed 13"),
                                      ("seed17", "Trained, seed 17"), ("seed23", "Trained, seed 23")], "base"),
    "E04": ("E04_data_scaling/kit", [("base", "Base student"), ("ep500", "500 episodes"), ("ep1000", "1,000 episodes"),
                                     ("ep2000", "2,000 episodes"), ("ep4000", "4,000 episodes"),
                                     ("full", "7,252 episodes (all)")], "base"),
    "E05": ("E05_student_family/kit", [("granite_base", "Granite-4.1-3B, base"),
                                       ("granite_trained", "Granite-4.1-3B, trained"),
                                       ("minicpm_base", "MiniCPM5-2B, base"),
                                       ("minicpm_trained", "MiniCPM5-2B, trained")], None),
    "E06": ("E06_teacher_strength/kit", [("base", "Base student"), ("deepseek_taught", "Taught by DeepSeek-V4-Flash"),
                                         ("glm_taught", "Taught by GLM-5.3-flash"),
                                         ("self_taught", "Taught by itself")], "base"),
    "E11": ("E11_training_knobs/kit", [("base", "Base student"), ("r8", "LoRA rank 8"), ("r16", "LoRA rank 16"),
                                       ("r32", "LoRA rank 32 (default)"), ("r64", "LoRA rank 64")], "base"),
}


def pct(x) -> str:
    return "--" if x is None else f"{100 * x:.1f}"


def pval(p) -> str:
    if p is None:
        return "--"
    return "$<$0.001" if p < 0.001 else f"{p:.3f}"


def per_set(res: dict, arm: str) -> dict:
    out = {}
    for key, r in res["rows"].items():          # "<arm>/<test-set>" -> metrics
        a, _, test = key.partition("/")
        if a == arm and r.get("judge_correct") is not None:
            out[test.split("_", 1)[-1]] = r["judge_correct"]
    return out


def paired(res: dict, a: str, b: str, scope: str = "pooled"):
    for name, scopes in res["paired"].items():   # "a -> b" -> {scope: stats}
        if name == f"{a} -> {b}" and scope in scopes:
            return scopes[scope], 1
        if name == f"{b} -> {a}" and scope in scopes:
            return scopes[scope], -1
    return None, 1


def arms_table(eid: str, label: str, caption: str) -> str | None:
    sub, arms, baseline = ARMS[eid]
    f = KIT / "results" / sub / "results.json"
    if not f.exists():
        return None
    res = json.loads(f.read_text(encoding="utf-8"))
    head = " & ".join(n for _, n in DS)
    cols = "l" + "r" * (len(DS) + 1) + ("rl" if baseline else "")
    lines = [r"\begin{table}[t]", r"\centering", r"\small", rf"\caption{{{caption}}}", rf"\label{{{label}}}",
             rf"\begin{{tabular}}{{{cols}}}", r"\toprule",
             f"Arm & {head} & All" + (r" & $\Delta$ vs base [95\% CI] & $p$" if baseline else "") + r" \\", r"\midrule"]
    for arm, name in arms:
        if arm not in res["pooled"]:
            continue
        s = per_set(res, arm)
        row = f"{name} & " + " & ".join(pct(s.get(d)) for d, _ in DS) + f" & {pct(res['pooled'][arm].get('judge_correct'))}"
        if baseline:
            if arm == baseline:
                row += " & -- & --"
            else:
                c, sign = paired(res, baseline, arm)
                if c:
                    lo, hi = sorted(sign * x for x in c["ci95"])
                    row += f" & {sign * 100 * c['diff']:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] & {pval(c['p'])}"
                else:
                    row += " & -- & --"
        lines.append(row + r" \\")
    n = res["pooled"][arms[0][0]]["n"] if arms[0][0] in res["pooled"] else ""
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    out = f.parent / "table.tex"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return f"{out.relative_to(KIT)} (n={n})"


def lodo_table(label: str) -> str | None:
    f = KIT / "results" / "E13_lodo_transfer" / "gemma" / "results.json"
    if not f.exists():
        return None
    res = json.loads(f.read_text(encoding="utf-8"))
    acc = {tuple(k.split("/", 1)): r for k, r in res["rows"].items()}
    lines = [r"\begin{table}[t]", r"\centering", r"\small",
             r"\caption{Leave-one-dataset-out transfer: each fold student is trained on three datasets and "
             r"evaluated on every question of the fourth. Judge-correct (\%), paired difference with bootstrap 95\% CI.}",
             rf"\label{{{label}}}", r"\begin{tabular}{lrrrrl}", r"\toprule",
             r"Unseen dataset & $n$ & Base & Fold student & $\Delta$ & 95\% CI \\", r"\midrule"]
    for d, name in DS:
        b, fo = acc.get(("base", f"full_{d}")), acc.get((f"fold_{d}", f"full_{d}"))
        c, sign = paired(res, "base", f"fold_{d}", f"full_{d}")
        if not (b and fo and c):
            continue
        lo, hi = sorted(sign * x for x in c["ci95"])
        lines.append(f"{name} & {fo['n']:,} & {pct(b['judge_correct'])} & {pct(fo['judge_correct'])} & "
                     f"{sign * 100 * c['diff']:+.1f} & [{100 * lo:+.1f}, {100 * hi:+.1f}]" + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    out = f.parent / "table.tex"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(out.relative_to(KIT))


CAPTIONS = {
    "E00": "Four arms on the 747 held-out questions. Judge-correct (\\%) per dataset and overall; "
           "$\\Delta$ is the paired difference to the base student with bootstrap 95\\% CI and exact McNemar $p$.",
    "E01": "What causes the gain: students trained on the same number of usable episodes from three sources.",
    "E02": "Seed variance: the trained student with three training seeds.",
    "E04": "Data scaling: students trained on nested subsets of the teacher-guided episodes.",
    "E05": "A second student family. Each student is compared with its own base model.",
    "E06": "Teacher strength: the same student trained on episodes collected with different teachers.",
    "E11": "LoRA rank.",
}


def main() -> int:
    want = set(sys.argv[1:])
    reg = {e["id"]: e for e in yaml.safe_load((KIT / "experiments" / "registry.yaml").read_text(encoding="utf-8"))["experiments"]}
    for eid in [*ARMS, "E13"]:
        if want and eid not in want:
            continue
        label = reg.get(eid, {}).get("paper", f"tab:{eid}")
        done = lodo_table(label) if eid == "E13" else arms_table(eid, label, CAPTIONS[eid])
        print(f"{eid}: {done or 'no published results yet'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
