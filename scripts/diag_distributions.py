"""Why does the trained student break when sampled? Measure the distribution it samples from.

Temperature below 1.0 *sharpens* a distribution, so "the fine-tune collapsed the entropy"
cannot explain a model that is fine at T=0 and broken at T=0.7-1.0. The opposite would:
if the trained model's next-token distribution on out-of-distribution prompts is FLAT --
right token on top, but a large share of the mass spread over junk -- then greedy is
correct while sampling near T=1 draws junk, and lowering T recovers the argmax.

This script tests that directly. For each model and each prompt set it takes the
next-token distribution at the position where the answer must start and records:

    entropy                nats; higher = flatter
    top1_prob              probability of the most likely token
    top1_is_valid          whether that token is a legal answer token
    valid_mass             total probability on legal answer tokens (A/B/C/D, or the
                           digits/step tokens an agent answer may open with)
    tail_mass_beyond_top10 probability outside the ten most likely tokens
    perplexity             exp(entropy): the effective number of tokens competing

Two prompt sets are compared: MMLU items (out of distribution for the trained student)
and teacher-guidance agent prompts (its training distribution). The prediction is that
the trained model looks confident in distribution and flat out of distribution, while the
base model looks the same on both.

Usage::

    python scripts/diag_distributions.py \
        --models base=<hf id> trained=<merged dir> --out runs/diag
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # project root -> import tgd/agentsim
sys.path.insert(0, str(Path(__file__).resolve().parent))       # sibling scripts

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List


from tgd.io import read_jsonl  # noqa: E402  (gz-aware: the shipped data is gzipped)

MCQ_SYSTEM = "You are a helpful assistant answering multiple-choice questions."
MCQ_TEMPLATE = """{question}

A. {a}
B. {b}
C. {c}
D. {d}

Answer with the single letter (A, B, C or D) of the correct option. Reply with the letter only."""


def mmlu_prompts(path: str, n: int) -> List[Dict[str, Any]]:
    rows = []
    for r in read_jsonl(path):
        if True:
            if True:
                c = r["choices"]
                rows.append({"id": r["id"], "kind": "mmlu",
                             "messages": [{"role": "system", "content": MCQ_SYSTEM},
                                          {"role": "user", "content": MCQ_TEMPLATE.format(
                                              question=r["question"], a=c[0], b=c[1], c=c[2], d=c[3])}],
                             "valid": ["A", "B", "C", "D"]})
        if len(rows) >= n:
            break
    return rows


def agent_prompts(episodes: str, n: int) -> List[Dict[str, Any]]:
    """Real student prompts from teacher-guidance episodes: the trained model's own
    training distribution. The answer must open with a JSON object."""
    rows = []
    for ep in read_jsonl(episodes):
        for st in (ep.get("steps") or [])[:1]:
            p = st.get("student_prompt")
            if p:
                rows.append({"id": f'{ep["qid"]}-s{st.get("t", 0)}', "kind": "agent",
                             "messages": [{"role": "user", "content": p}],
                             "valid": ["{", '{"', "{\n", " {"]})
        if len(rows) >= n:
            break
    return rows[:n]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", nargs="+", required=True, help="name=path_or_hf_id")
    ap.add_argument("--mmlu", default="data/benchmarks/mmlu.jsonl.gz")
    ap.add_argument("--episodes", default="data/episodes/episodes.jsonl.gz")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--out", default="runs/diag")
    ap.add_argument("--device", default="cuda:0")
    args = ap.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    prompt_sets = {"mmlu_ood": mmlu_prompts(args.mmlu, args.n),
                   "agent_in_dist": agent_prompts(args.episodes, args.n)}
    for k, v in prompt_sets.items():
        print(f"{k}: {len(v)} prompts")

    summary: Dict[str, Any] = {}
    rows_out: List[Dict[str, Any]] = []
    for spec in args.models:
        name, path = spec.split("=", 1)
        print(f"\nloading {name} from {path}")
        tok = AutoTokenizer.from_pretrained(path)
        model = AutoModelForCausalLM.from_pretrained(path, dtype=torch.bfloat16, device_map=args.device)
        model.eval()
        for set_name, prompts in prompt_sets.items():
            stats = []
            for row in prompts:
                text = tok.apply_chat_template(row["messages"], tokenize=False, add_generation_prompt=True)
                ids = tok(text, return_tensors="pt").to(model.device)
                with torch.no_grad():
                    logits = model(**ids).logits[0, -1].float()
                probs = torch.softmax(logits, dim=-1)
                top = torch.topk(probs, 10)
                top1_tok = tok.decode(top.indices[0]).strip()
                valid_ids = set()
                for v in row["valid"]:
                    for cand in (v, " " + v):
                        enc = tok.encode(cand, add_special_tokens=False)
                        if enc:
                            valid_ids.add(enc[0])
                valid_mass = float(probs[list(valid_ids)].sum()) if valid_ids else 0.0
                ent = float(-(probs * torch.log(probs.clamp_min(1e-12))).sum())
                stats.append({
                    "id": row["id"], "model": name, "set": set_name,
                    "entropy": ent, "perplexity": math.exp(min(ent, 20)),
                    "top1_prob": float(top.values[0]), "top1_token": top1_tok,
                    "top1_is_valid": int(top1_tok[:1] in [v[:1] for v in row["valid"]] or top1_tok in row["valid"]),
                    "valid_mass": valid_mass,
                    "tail_mass_beyond_top10": float(1.0 - top.values.sum()),
                })
            rows_out += stats
            import statistics as st
            summary.setdefault(name, {})[set_name] = {
                "n": len(stats),
                "entropy_mean": round(st.mean(s["entropy"] for s in stats), 4),
                "entropy_median": round(st.median(s["entropy"] for s in stats), 4),
                "perplexity_mean": round(st.mean(s["perplexity"] for s in stats), 2),
                "top1_prob_mean": round(st.mean(s["top1_prob"] for s in stats), 4),
                "top1_is_valid_rate": round(st.mean(s["top1_is_valid"] for s in stats), 4),
                "valid_mass_mean": round(st.mean(s["valid_mass"] for s in stats), 4),
                "valid_mass_median": round(st.median(s["valid_mass"] for s in stats), 4),
                "tail_beyond_top10_mean": round(st.mean(s["tail_mass_beyond_top10"] for s in stats), 4),
            }
            s = summary[name][set_name]
            print(f"  {set_name:<14} entropy {s['entropy_mean']:.3f} | top1 {s['top1_prob_mean']:.3f} "
                  f"| valid-token mass {s['valid_mass_mean']:.3f} | tail>top10 {s['tail_beyond_top10_mean']:.3f}")
        del model
        torch.cuda.empty_cache()

    (out / "distribution_stats.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    with (out / "per_prompt.jsonl").open("w", encoding="utf-8") as fh:
        for r in rows_out:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nwrote {out/'distribution_stats.json'} and {out/'per_prompt.jsonl'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
