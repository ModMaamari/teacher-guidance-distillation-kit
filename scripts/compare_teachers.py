#!/usr/bin/env python
"""Does the teacher have to be a stronger model? Compare teacher-guided collections that
differ in the teacher -- typically a larger model against the student guiding itself.

Self-teaching means one model plays both roles. As the teacher it sees the gold answer and
supporting facts and reviews the student's plan and every step; the leakage sanitiser
(agentsim/teacher_guidance/leakage.py) removes any statement of the answer before the
guidance reaches the student, which is the same model. A self-taught collection therefore
isolates what privileged information and a reviewer role are worth with model capability
held fixed; a stronger teacher adds capability on top.

Each arm is one consolidated collection (scripts/consolidate_episodes.py) and, optionally,
its judge verdicts (scripts/judge.py). Arms are compared on the questions all of them share:

* outcome: judge-correct, cover (answer_correct), EM, F1, doc recall, grounding and steps,
  with every arm tested against the baseline by a paired bootstrap 95% CI and an exact
  McNemar test, pooled and per dataset;
* training value: the SFT examples the kit would build from the arm (correct episodes
  only, after the leakage gate), which is what a collection is for;
* teacher behaviour: how often the teacher's guidance stated the gold answer and had to be
  redacted, whether any statement survived redaction (must be 0), how often its output was
  unusable and generic feedback was substituted, how often it changed the student's plan,
  and how well its own verdict on the final answer agrees with the judge;
* cost: teacher and student tokens and API spend per episode.

The difference between arms is attributable to the teacher only when every arm has the same
student and collection config; the report warns when either differs.

Usage::

    python scripts/compare_teachers.py \\
        --arm self=data/episodes_self/episodes.jsonl.gz,runs/judge_self/verdicts.jsonl \\
        --arm deepseek=data/episodes/episodes.jsonl.gz,runs/judge_shipped/verdicts.jsonl \\
        --baseline self --out runs/compare_teachers
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # project root -> import tgd/agentsim

import tgd  # noqa: F401
from agentsim.teacher_guidance.leakage import _contains, asserts_gold_answer
from tgd.episode_lib import build_episode_examples
from tgd.episodes import is_error
from tgd.io import read_jsonl
from tgd.logging_utils import write_json
from tgd.metrics import episode_tokens
from tgd.stats import mcnemar_exact, paired_bootstrap

# Provider prefixes from docs/PROVIDERS.md; the model behind "oai-x/org/model" is "org/model".
_PROVIDER_PREFIX = re.compile(r"^(?:oai(?:-[\w-]+)?|custom|vllm|openrouter|ollama|mock|hf|edenchat|together)/",
                              re.IGNORECASE)


def bare_model(model_id: Optional[str]) -> str:
    return _PROVIDER_PREFIX.sub("", str(model_id or "")).strip().lower()


def parse_arm(spec: str) -> Dict[str, Any]:
    name, sep, rest = spec.partition("=")
    episodes, _, verdicts = rest.partition(",")
    if not (sep and name and episodes):
        raise argparse.ArgumentTypeError(f"--arm expects NAME=EPISODES[,VERDICTS], got {spec!r}")
    path = Path(episodes)
    if path.is_dir():
        found = [p for p in (path / "episodes.jsonl.gz", path / "episodes.jsonl") if p.exists()]
        if not found:
            raise argparse.ArgumentTypeError(f"{path} has no episodes.jsonl[.gz]")
        path = found[0]
    return {"name": name, "episodes": path, "verdicts": Path(verdicts) if verdicts else None}


def load_verdicts(path: Optional[Path], episodes: Path) -> Dict[str, int]:
    """qid -> 0/1. When the file judged several sources, keep this arm's rows only."""
    if path is None:
        return {}
    rows = list(read_jsonl(path))
    mine = [r for r in rows if Path(str(r.get("source", ""))).resolve() == episodes.resolve()]
    return {r["qid"]: int(bool(r["verdict"]["correct"])) for r in (mine or rows)}


def episode_row(ep: Dict[str, Any], verdict: Optional[int]) -> Dict[str, Any]:
    fm = ep.get("final_metrics") or {}
    gold = ep.get("gold_answer") or ""
    question = ep.get("query") or ""
    steps = ep.get("steps") or []
    pr = ep.get("plan_review") if isinstance(ep.get("plan_review"), dict) else {}

    # Guidance events: the plan review plus every reviewed step.
    checks = [s.get("leakage_check") or {} for s in steps if not s.get("teacher_skipped")]
    visible = [s.get("student_visible_guidance") for s in steps]
    if pr.get("enabled"):
        checks.append(pr.get("leakage_check") or {})
        visible.append(pr.get("student_visible_plan_feedback"))
    # What the student actually saw must never state the answer. The sanitiser guarantees
    # this; re-checking it here is what lets a report claim it.
    answer_in_question = _contains(question, gold)
    residual = 0 if answer_in_question else sum(
        1 for v in visible if v and asserts_gold_answer(json.dumps(v, ensure_ascii=False), gold))

    cover = bool(fm.get("answer_correct", fm.get("cover_match")))
    tokens = episode_tokens(ep)
    teacher_verdict = fm.get("teacher_answer_correct")
    return {
        "qid": ep["qid"], "dataset": ep.get("dataset"), "error": is_error(ep),
        "judge": verdict, "cover": cover, "em": bool(fm.get("exact_match")), "f1": fm.get("f1"),
        "doc_recall": fm.get("supporting_doc_recall"), "grounded": bool(fm.get("answer_grounded")),
        "steps": ep.get("used_steps"), "teacher_accept": ep.get("stop_reason") == "teacher_accept",
        "guidance_events": len(checks),
        "leak_redactions": sum(1 for c in checks if c.get("gold_answer_leaked")),
        "residual_leaks": residual,
        "fallback_feedback": sum(1 for c in checks if c.get("feedback_fallback_used")),
        "plan_changed": (pr.get("metrics") or {}).get("plan_changed") if pr.get("enabled") else None,
        "teacher_verdict": None if teacher_verdict is None else int(bool(teacher_verdict)),
        # build_splits.py trains on correct episodes only
        "sft_examples": len(build_episode_examples(ep)) if cover else 0,
        "teacher_tokens": tokens["teacher_in"] + tokens["teacher_out"],
        "student_tokens": tokens["student_in"] + tokens["student_out"] + tokens["plan_in"] + tokens["plan_out"],
        "api_cost_usd": tokens["api_cost_usd"],
    }


def _rate(num: float, den: float) -> Optional[float]:
    return round(num / den, 4) if den else None


def _mean(rows: List[Dict[str, Any]], key: str) -> Optional[float]:
    vals = [float(r[key]) for r in rows if r.get(key) is not None]
    return round(sum(vals) / len(vals), 4) if vals else None


def summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    judged = [r for r in rows if r["judge"] is not None]
    # "Correct" for teacher-behaviour rates: the judge when present, else cover.
    truth = lambda r: r["judge"] if r["judge"] is not None else int(r["cover"])  # noqa: E731
    accepts = [r for r in rows if r["teacher_accept"]]
    graded = [r for r in rows if r["teacher_verdict"] is not None]
    wrong = [r for r in graded if not truth(r)]
    right = [r for r in graded if truth(r)]
    events = sum(r["guidance_events"] for r in rows)
    return {
        "n": len(rows), "errors": sum(r["error"] for r in rows), "judged": len(judged),
        "judge_correct": _mean(judged, "judge"), "cover": _mean(rows, "cover"), "em": _mean(rows, "em"),
        "f1": _mean(rows, "f1"), "doc_recall": _mean(rows, "doc_recall"), "grounded": _mean(rows, "grounded"),
        "steps": _mean(rows, "steps"), "teacher_accept_rate": _mean(rows, "teacher_accept"),
        "teacher_accept_precision": _rate(sum(truth(r) for r in accepts), len(accepts)),
        "leak_redaction_rate": _rate(sum(r["leak_redactions"] for r in rows), events),
        "episodes_with_redaction": _rate(sum(1 for r in rows if r["leak_redactions"]), len(rows)),
        "residual_leaks": sum(r["residual_leaks"] for r in rows),
        "fallback_feedback_rate": _rate(sum(r["fallback_feedback"] for r in rows), events),
        "plan_changed_rate": _mean([r for r in rows if r["plan_changed"] is not None], "plan_changed"),
        "teacher_verdict_agreement": _rate(sum(r["teacher_verdict"] == truth(r) for r in graded), len(graded)),
        "teacher_false_approval": _rate(sum(r["teacher_verdict"] for r in wrong), len(wrong)),
        "teacher_false_rejection": _rate(sum(1 - r["teacher_verdict"] for r in right), len(right)),
        "sft_examples": sum(r["sft_examples"] for r in rows),
        "sft_examples_per_episode": _mean(rows, "sft_examples"),
        "teacher_tokens_per_episode": _mean(rows, "teacher_tokens"),
        "student_tokens_per_episode": _mean(rows, "student_tokens"),
        "api_cost_usd_per_episode": _mean(rows, "api_cost_usd"),
    }


def paired(base: Dict[str, Dict[str, Any]], arm: Dict[str, Dict[str, Any]], qids: List[str], key: str,
           iters: int) -> Optional[Dict[str, Any]]:
    qs = [q for q in qids if base[q][key] is not None and arm[q][key] is not None]
    if not qs:
        return None
    a = [int(bool(base[q][key])) for q in qs]
    b = [int(bool(arm[q][key])) for q in qs]
    res = {**paired_bootstrap(a, b, iters), **mcnemar_exact(a, b)}
    return {"n": res["n"], "diff": res["diff"], "ci95": res["ci95"], "arm_wins": res["b_wins"],
            "baseline_wins": res["a_wins"], "p": res["p"]}


def _pct(x: Optional[float]) -> str:
    return "—" if x is None else f"{100 * x:.1f} %"


def _num(x: Optional[float], fmt: str = "{:.2f}") -> str:
    return "—" if x is None else fmt.format(x)


def render_markdown(result: Dict[str, Any]) -> str:
    arms, base = result["arms"], result["baseline"]
    names = [a["name"] for a in arms]
    md = ["# Teacher comparison", "",
          f"{result['shared_questions']:,} questions shared by every arm. Baseline: **{base}**; "
          "differences are arm − baseline in percentage points.", "",
          "| arm | student | teacher | self-teaching | config | episodes | judged |", "|---|---|---|---|---|---|---|"]
    for a in arms:
        md.append(f"| {a['name']} | {', '.join(a['students'])} | {', '.join(a['teachers'])} | "
                  f"{'yes' if a['self_teaching'] else 'no'} | {', '.join(a['config_hashes'])} | "
                  f"{a['episodes']:,} | {a['judged']:,} |")
    if result["warnings"]:
        md += ["", "**Warnings**", ""] + [f"* {w}" for w in result["warnings"]]

    s = result["summary"]
    md += ["", "## Outcome", "",
           "| arm | n | judge | cover | EM | F1 | doc recall | grounded | steps | SFT examples | SFT / episode | teacher tok / ep | student tok / ep | API $ / ep |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for n in names:
        r = s[n]["ALL"]
        md.append(f"| {n} | {r['n']:,} | {_pct(r['judge_correct'])} | {_pct(r['cover'])} | {_pct(r['em'])} | "
                  f"{_num(r['f1'], '{:.3f}')} | {_num(r['doc_recall'], '{:.3f}')} | {_pct(r['grounded'])} | "
                  f"{_num(r['steps'])} | {r['sft_examples']:,} | {_num(r['sft_examples_per_episode'])} | "
                  f"{_num(r['teacher_tokens_per_episode'], '{:,.0f}')} | {_num(r['student_tokens_per_episode'], '{:,.0f}')} | "
                  f"{_num(r['api_cost_usd_per_episode'], '{:.5f}')} |")

    datasets = [d for d in result["datasets"]]
    key = "judge_correct" if all(s[n]["ALL"]["judged"] for n in names) else "cover"
    md += ["", f"### {'Judge-correct' if key == 'judge_correct' else 'Cover'} by dataset", "",
           "| dataset | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for d in datasets:
        md.append(f"| {d} | " + " | ".join(_pct(s[n][d][key]) for n in names) + " |")

    md += ["", "## Paired differences against the baseline", "",
           "| arm | scope | metric | n | Δ pts | 95 % CI | arm wins / baseline wins | McNemar p |",
           "|---|---|---|---|---|---|---|---|"]
    for p in result["paired"]:
        md.append(f"| {p['arm']} | {p['scope']} | {p['metric']} | {p['n']:,} | {100 * p['diff']:+.1f} | "
                  f"[{100 * p['ci95'][0]:+.1f}, {100 * p['ci95'][1]:+.1f}] | {p['arm_wins']} / {p['baseline_wins']} | "
                  f"{'<1e-6' if p['p'] < 1e-6 else f'{p['p']:.3g}'} |")

    md += ["", "## Teacher behaviour", "",
           "| arm | guidance redacted for stating the answer | episodes with a redaction | answer statements that reached the student | generic fallback feedback | plan changed | teacher-accept rate | teacher-accept precision | teacher verdict agrees with judge | teacher approves wrong answers | teacher rejects right answers |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for n in names:
        r = s[n]["ALL"]
        md.append(f"| {n} | {_pct(r['leak_redaction_rate'])} | {_pct(r['episodes_with_redaction'])} | {r['residual_leaks']} | "
                  f"{_pct(r['fallback_feedback_rate'])} | {_pct(r['plan_changed_rate'])} | {_pct(r['teacher_accept_rate'])} | "
                  f"{_pct(r['teacher_accept_precision'])} | {_pct(r['teacher_verdict_agreement'])} | "
                  f"{_pct(r['teacher_false_approval'])} | {_pct(r['teacher_false_rejection'])} |")
    md += ["", "Rates over guidance events count the plan review and every reviewed step. Teacher-behaviour "
           "rates use the judge verdict as the truth when the arm was judged, cover otherwise. "
           "\"Answer statements that reached the student\" re-checks the student-visible guidance and must be 0."]
    return "\n".join(md) + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arm", type=parse_arm, action="append", required=True,
                    help="NAME=EPISODES[,VERDICTS]; EPISODES is a consolidated episodes.jsonl[.gz] or its directory")
    ap.add_argument("--baseline", default=None, help="arm the others are tested against (default: the first)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--iters", type=int, default=10000, help="bootstrap resamples")
    args = ap.parse_args(argv)

    names = [a["name"] for a in args.arm]
    if len(names) < 2 or len(set(names)) != len(names):
        ap.error("give at least two arms with distinct names")
    baseline = args.baseline or names[0]
    if baseline not in names:
        ap.error(f"--baseline {baseline!r} is not one of the arms {names}")

    warnings: List[str] = []
    rows: Dict[str, Dict[str, Dict[str, Any]]] = {}
    arm_info: List[Dict[str, Any]] = []
    for a in args.arm:
        verdicts = load_verdicts(a["verdicts"], a["episodes"])
        by_qid: Dict[str, Dict[str, Any]] = {}
        students, teachers, hashes = collections.Counter(), collections.Counter(), collections.Counter()
        duplicates = 0
        for ep in read_jsonl(a["episodes"]):
            duplicates += ep["qid"] in by_qid
            by_qid[ep["qid"]] = episode_row(ep, verdicts.get(ep["qid"]))
            students[bare_model(ep.get("student_model"))] += 1
            for t in ep.get("teacher_models_used") or [ep.get("teacher_model")]:
                teachers[bare_model(t)] += 1
            hashes[ep.get("config_hash") or "?"] += 1
        if not by_qid:
            ap.error(f"arm {a['name']}: no episodes in {a['episodes']}")
        if duplicates:
            warnings.append(f"{a['name']}: {duplicates} duplicate question(s); the last episode of each was kept")
        if a["verdicts"] is not None and not verdicts:
            warnings.append(f"{a['name']}: {a['verdicts']} holds no verdicts")
        rows[a["name"]] = by_qid
        arm_info.append({"name": a["name"], "episodes_path": str(a["episodes"]),
                         "verdicts_path": str(a["verdicts"]) if a["verdicts"] else None,
                         "episodes": len(by_qid), "students": sorted(students), "teachers": sorted(teachers),
                         "config_hashes": sorted(hashes),
                         "self_teaching": set(teachers) <= set(students) and len(students) == 1})

    shared = sorted(set.intersection(*(set(r) for r in rows.values())))
    if not shared:
        ap.error("the arms share no questions")
    for a in arm_info:
        a["judged"] = sum(rows[a["name"]][q]["judge"] is not None for q in shared)
        if a["episodes"] > len(shared):
            warnings.append(f"{a['name']}: {a['episodes'] - len(shared):,} question(s) not in every arm are left out")
        if not a["judged"]:
            warnings.append(f"{a['name']}: no judge verdicts; judge comparisons involving it are skipped")
    if len({tuple(a["students"]) for a in arm_info}) > 1:
        warnings.append("the arms have different students, so differences mix the teacher's effect with the student's")
    if len({tuple(a["config_hashes"]) for a in arm_info}) > 1:
        warnings.append("the arms were collected with different configs (config_hash), so settings other than the teacher differ too")

    datasets = sorted({rows[baseline][q]["dataset"] for q in shared})
    summary: Dict[str, Dict[str, Any]] = {}
    for n in names:
        sel = [rows[n][q] for q in shared]
        summary[n] = {"ALL": summarize(sel), **{d: summarize([r for r in sel if r["dataset"] == d]) for d in datasets}}
        if summary[n]["ALL"]["residual_leaks"]:
            warnings.append(f"{n}: {summary[n]['ALL']['residual_leaks']} student-visible guidance message(s) state the gold answer")

    paired_rows: List[Dict[str, Any]] = []
    for n in names:
        if n == baseline:
            continue
        for scope in ["ALL"] + datasets:
            qids = [q for q in shared if scope == "ALL" or rows[baseline][q]["dataset"] == scope]
            for metric in ("judge", "cover"):
                res = paired(rows[baseline], rows[n], qids, metric, args.iters)
                if res:
                    paired_rows.append({"arm": n, "scope": scope, "metric": metric, **res})

    result = {"baseline": baseline, "shared_questions": len(shared), "datasets": datasets, "arms": arm_info,
              "warnings": warnings, "summary": summary, "paired": paired_rows}
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "comparison.json", result)
    (out / "REPORT.md").write_text(render_markdown(result), encoding="utf-8")
    with (out / "per_question.jsonl").open("w", encoding="utf-8") as fh:
        for q in shared:
            fh.write(json.dumps({"qid": q, "dataset": rows[baseline][q]["dataset"],
                                 **{n: {"judge": rows[n][q]["judge"], "cover": rows[n][q]["cover"]} for n in names}},
                                ensure_ascii=False) + "\n")
    print(f"{len(shared):,} shared questions, {len(names)} arms, baseline {baseline} -> {out}/REPORT.md")
    for w in warnings:
        print(f"  warning: {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
