"""Reconcile the measured next-token distribution with what sampling actually does.

The distribution measured at the answer position said the trained model is nearly flat
(top-1 probability ~0.006). Taken literally, sampling at T=1 with nucleus 0.95 should
almost never produce a valid answer letter -- yet it produces one about half the time.
One of those two measurements is wrong, or the arithmetic linking them is.

This script measures both in the same process, on the same prompts, and prints them side
by side:

    predicted   P(first token is a valid letter) computed from the model's own
                distribution after the exact temperature and nucleus filtering that
                generation applies
    observed    the rate over real sampled generations

If they agree, the distribution measurement is sound and the mechanism is settled. If
they disagree, the discrepancy is in how the distribution is being read, and the
mechanism claim has to wait.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # project root -> import tgd/agentsim
sys.path.insert(0, str(Path(__file__).resolve().parent))       # sibling scripts

import argparse

from tgd.logit_scale import describe as describe_scaling  # noqa: E402
from tgd.models import load_lm  # noqa: E402
import json
import sys
from pathlib import Path


from diag_distributions import mmlu_prompts  # noqa: E402

LETTERS = ["A", "B", "C", "D"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--mmlu", default="data/benchmarks/mmlu.jsonl.gz")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--samples", type=int, default=20, help="generations per prompt")
    ap.add_argument("--temps", nargs="+", type=float, default=[0.3, 0.7, 1.0])
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--top-k", type=int, default=0,
                    help="0 = nucleus only. transformers' generate defaults to 50, which is why a "
                         "prediction that ignores it under-estimates the observed rate")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--out", default="runs/diag/consistency.json")
    args = ap.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(args.model)
    model, _ = load_lm(args.model, dtype=torch.bfloat16, device_map=args.device)
    print(f"  {describe_scaling(model.config)}")
    model.eval()
    prompts = mmlu_prompts(args.mmlu, args.n)
    letter_ids = []
    for L in LETTERS:
        for cand in (L, " " + L):
            enc = tok.encode(cand, add_special_tokens=False)
            if enc:
                letter_ids.append(enc[0])
    letter_ids = sorted(set(letter_ids))

    out = {"model": args.model, "n_prompts": len(prompts), "samples_per_prompt": args.samples,
           "top_p": args.top_p, "top_k": args.top_k, "by_temperature": {}}
    for T in args.temps:
        pred_sum = 0.0
        obs_hits = obs_total = 0
        for row in prompts:
            text = tok.apply_chat_template(row["messages"], tokenize=False, add_generation_prompt=True)
            ids = tok(text, return_tensors="pt").to(model.device)
            with torch.no_grad():
                logits = model(**ids).logits[0, -1].float()
            # exactly what generation does: scale by temperature, then nucleus-filter
            scaled = logits / T
            if args.top_k:                       # top-k is applied before nucleus, as in generate
                kth = torch.topk(scaled, args.top_k).values[-1]
                scaled = scaled.masked_fill(scaled < kth, float("-inf"))
            probs = torch.softmax(scaled, dim=-1)
            srt, idx = torch.sort(probs, descending=True)
            cum = torch.cumsum(srt, dim=-1)
            keep = cum <= args.top_p
            keep[0] = True                      # the top token is always kept
            kept_idx = idx[keep]
            kept_p = srt[keep]
            kept_p = kept_p / kept_p.sum()
            mask = torch.tensor([int(i) in set(letter_ids) for i in kept_idx.tolist()], device=kept_p.device)
            pred_sum += float(kept_p[mask].sum()) if mask.any() else 0.0

            with torch.no_grad():
                gen = model.generate(**ids, do_sample=True, temperature=T, top_p=args.top_p,
                                     top_k=args.top_k if args.top_k else 0,
                                     max_new_tokens=1, num_return_sequences=args.samples,
                                     pad_token_id=tok.eos_token_id)
            for g in gen:
                txt = tok.decode(g[ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()
                obs_total += 1
                obs_hits += int(txt[:1] in LETTERS)
        pred = pred_sum / len(prompts)
        obs = obs_hits / max(obs_total, 1)
        out["by_temperature"][str(T)] = {"predicted_letter_rate": round(pred, 4),
                                         "observed_letter_rate": round(obs, 4),
                                         "n_generations": obs_total}
        print(f"  T={T}: predicted {pred:.3f} | observed {obs:.3f} | "
              f"{'AGREE' if abs(pred - obs) < 0.08 else 'DISAGREE'}")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
