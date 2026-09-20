#!/usr/bin/env python
"""End-to-end cost of each route, from collecting trajectories to answering a question.

Every number is hardware-independent so it transfers to other setups: token counts are what the
serving engines reported (inputs and outputs separately), and compute is estimated as

    FLOPs ~ 2 x active parameters x tokens processed          (inference/collection)
    FLOPs ~ 6 x parameters x tokens                           (training, the trainer's own counter)

attention and caching ignored. Reported per route:

  collection   episodes run, input and output tokens per episode (actor and critic separately),
               PFLOPs per episode and for the whole collection
  filter       which episodes become training data, and what the filter itself costs (a string
               match costs nothing; an LLM judge costs tokens)
  training     examples, tokens, PFLOPs
  inference    tokens and PFLOPs per question, and the parameters that must be served
  accuracy     judge-correct accuracy of the resulting agent

    python experiments/exp23_pipeline_cost/pipeline_cost.py --json-out cost.json
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))

# total and active parameters of every model in the pipelines (active = per token, for MoE)
MODELS = {
    "student":  ("Granite-4.1-3B", 3.4e9, 3.4e9),
    "deepseek": ("DeepSeek-V4-Flash", 284e9, 13e9),
    "glm":      ("GLM-5.3-flash", 320e9, 18e9),
    "judge":    ("Gemma-4-31B-it", 31e9, 31e9),
}
# collection -> (actor, critic or None); the critic is the model that writes guidance
COLLECTIONS = {
    "self":      ("data/episodes_self", "student", "student", "self-guided (ours)"),
    "deepseek":  ("data/episodes", "student", "deepseek", "teacher-guided (DeepSeek)"),
    "glm":       ("data/episodes_glm", "student", "glm", "teacher-guided (GLM)"),
    "selfdist":  ("data/episodes_selfdist", "student", None, "student's own rollouts, unguided"),
    "teachdist": ("data/episodes_teachdist", "deepseek", None, "teacher's own rollouts, unguided"),
}


CRITIC_CALLS = ("teacher_calls", "review_calls")   # every other call is the actor's own


def tokens_of(path: Path, limit: int | None = None) -> dict:
    """Input/output tokens per episode, split into actor and critic, from the recorded usage.

    Every call anywhere in the episode is counted, found by walking the record: the agent's steps,
    its initial plan and its plan revisions (actor), and the step reviews and plan reviews
    (critic). Missing a call group would understate a route's cost, so nothing is hard-coded to a
    fixed set of fields.
    """
    c = collections.Counter()
    opener = gzip.open if path.suffix == ".gz" else open

    def walk(o, role):
        if isinstance(o, dict):
            u = o.get("usage")
            if isinstance(u, dict) and ("prompt_tokens" in u or "completion_tokens" in u):
                c[f"{role}_in"] += int(u.get("prompt_tokens") or 0)
                c[f"{role}_out"] += int(u.get("completion_tokens") or 0)
                c[f"{role}_calls"] += 1
            for k, v in o.items():
                if k != "usage":
                    walk(v, "critic" if k in CRITIC_CALLS else role)
        elif isinstance(o, list):
            for x in o:
                walk(x, role)

    with opener(path, "rt", encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            if limit and i >= limit:
                break
            if not line.strip():
                continue
            c["episodes"] += 1
            walk(json.loads(line), "actor")
    n = max(c["episodes"], 1)
    return {"episodes": c["episodes"],
            **{k: round(c[k] / n, 1) for k in ("actor_in", "actor_out", "critic_in", "critic_out")},
            "actor_calls": round(c["actor_calls"] / n, 2), "critic_calls": round(c["critic_calls"] / n, 2)}


def load(rel: str):
    f = KIT / rel
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=None, help="episodes per collection (a quick check)")
    ap.add_argument("--target", type=int, default=3818, help="usable episodes every route must end up with")
    ap.add_argument("--train-pflops", type=float, default=684.0, help="training compute for that many episodes")
    ap.add_argument("--judge-filter", action="store_true", help="price an LLM-judge filter instead of the string one")
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    out: dict = {"models": {k: {"name": v[0], "total_params": v[1], "active_params": v[2]}
                            for k, v in MODELS.items()}, "collections": {}}

    print("COLLECTION  (tokens per episode as the engines reported them; PFLOPs ~ 2 x active params x tokens)\n")
    print(f"  {'route':<34}{'episodes':>9}{'actor in':>10}{'actor out':>10}{'critic in':>10}"
          f"{'critic out':>11}{'PFLOPs/ep':>11}{'total PF':>10}")
    for key, (path, actor, critic, label) in COLLECTIONS.items():
        f = KIT / path / "episodes.jsonl.gz"
        if not f.exists():
            print(f"  {label:<34}{'(not collected)':>9}")
            continue
        t = tokens_of(f, a.limit)
        act = MODELS[actor][2]
        flops = 2 * act * (t["actor_in"] + t["actor_out"])
        if critic:
            flops += 2 * MODELS[critic][2] * (t["critic_in"] + t["critic_out"])
        row = {**t, "actor": actor, "critic": critic, "label": label,
               "pflops_per_episode": flops / 1e15, "pflops_total": flops * t["episodes"] / 1e15}
        out["collections"][key] = row
        print(f"  {label:<34}{t['episodes']:>9,}{t['actor_in']:>10,.0f}{t['actor_out']:>10,.0f}"
              f"{t['critic_in']:>10,.0f}{t['critic_out']:>11,.0f}{row['pflops_per_episode']:>11.3f}"
              f"{row['pflops_total']:>10,.0f}")

    # ---- what each filter keeps, and what the filter itself costs
    print("\nFILTER  (of the trainable pool; the string filter costs nothing, the judge costs tokens)\n")
    e15 = load("results/E15_teacher_datasets/comparison.json")
    fv = (KIT / "results/E20_correctness_filter/kit/filter_vs_judge.txt")
    if e15:
        s = e15["summary"]["self"]["ALL"]
        judge_tok = out.get("judge_tokens_per_episode", 250)   # prompt + verdict, measured below if available
        jf = 2 * MODELS["judge"][2] * judge_tok / 1e15
        print(f"  cover match (the kit's filter): keeps {100 * s['cover']:.1f}% of self-guided episodes, 0 FLOPs")
        print(f"  LLM judge ({MODELS['judge'][0]}): keeps {100 * s['judge_correct']:.1f}%, "
              f"about {judge_tok} tokens and {jf:.4f} PFLOPs per episode judged")
        out["filter"] = {"cover_keep_rate": s["cover"], "judge_keep_rate": s["judge_correct"],
                         "judge_pflops_per_episode": jf, "judge_tokens_per_episode": judge_tok}
    if fv.exists():
        print("  disagreement: " + [l for l in fv.read_text(encoding="utf-8").splitlines() if "dropped" in l][0].strip())

    # ---- what it costs to build one trained student, at equal training data
    print(f"\nBUILD A STUDENT  (every route collects until it has {a.target:,} usable episodes)\n")
    keep = {k: v for k, v in (out.get("keep_rate") or {}).items()}
    stats = {k: load(f"{p}/stats.json") for k, (p, *_rest) in COLLECTIONS.items()}
    for key, row in out["collections"].items():
        st = stats.get(key) or {}
        per_ds = [v for v in st.values() if isinstance(v, dict) and "episodes" in v and "correct" in v]
        tot = sum(v["episodes"] for v in per_ds) or None
        cor = sum(v["correct"] for v in per_ds) or None
        keep[key] = (cor / tot) if tot and cor else None
    print(f"  {'route':<34}{'keep':>7}{'episodes':>10}{'collect PF':>12}{'filter PF':>11}"
          f"{'train PF':>10}{'total PF':>11}")
    for key, row in out["collections"].items():
        k = keep.get(key)
        if not k:
            continue
        eps = a.target / k
        collect_pf = eps * row["pflops_per_episode"]
        filt = 0.0 if not a.judge_filter else eps * (out.get("filter", {}).get("judge_pflops_per_episode") or 0)
        train_pf = a.train_pflops
        row.update({"keep_rate": k, "episodes_needed": round(eps), "collect_pflops": collect_pf,
                    "filter_pflops": filt, "train_pflops": train_pf, "total_pflops": collect_pf + filt + train_pf})
        print(f"  {row['label']:<34}{100 * k:>6.0f}%{eps:>10,.0f}{collect_pf:>12,.0f}{filt:>11,.0f}"
              f"{train_pf:>10,.0f}{collect_pf + filt + train_pf:>11,.0f}")
    print("\n  'keep' is the share of collected episodes the correctness filter keeps, so a route with a low")
    print("  keep rate must collect more episodes for the same training set. Training compute is the")
    print(f"  measured {a.train_pflops:,.0f} PFLOPs of a {a.target:,}-episode LoRA run (E20), identical across routes.")

    if a.json_out:
        Path(a.json_out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
