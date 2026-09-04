"""Independent check of the temperature collapse, using transformers rather than vLLM.

Two questions:

1. Is the collapse a property of the weights, or of the inference server? This samples
   with plain HF ``generate`` -- a different sampling implementation entirely. If the
   trained model breaks here too, the server is exonerated.
2. Does truncation fix it? If the cause is a flat distribution with a junk tail, then
   restricting sampling to the head (top_k, or a tighter top_p) should restore the
   model, which both confirms the mechanism and gives a practical setting.

Usage::

    python scripts/sweep_decoding.py --models base=<hf id> trained=<merged dir> --n 100
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
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


from diag_distributions import mmlu_prompts  # noqa: E402

LETTERS = ["A", "B", "C", "D"]
CONFIGS = [
    {"label": "greedy",                 "do_sample": False},
    {"label": "T=0.3",                  "do_sample": True, "temperature": 0.3, "top_p": 0.95},
    {"label": "T=0.7",                  "do_sample": True, "temperature": 0.7, "top_p": 0.95},
    {"label": "T=1.0",                  "do_sample": True, "temperature": 1.0, "top_p": 0.95},
    {"label": "T=0.7 top_p=0.8",        "do_sample": True, "temperature": 0.7, "top_p": 0.80},
    {"label": "T=0.7 top_k=5",          "do_sample": True, "temperature": 0.7, "top_k": 5},
    {"label": "T=1.0 top_k=5",          "do_sample": True, "temperature": 1.0, "top_k": 5},
    # min-p (Nguyen et al., ICLR 2025) truncates relative to the top token's probability,
    # which is exactly the failure mode here: an absolute nucleus keeps a huge flat tail.
    {"label": "T=0.7 min_p=0.1",        "do_sample": True, "temperature": 0.7, "min_p": 0.1, "top_p": 1.0, "top_k": 0},
    {"label": "T=1.0 min_p=0.1",        "do_sample": True, "temperature": 1.0, "min_p": 0.1, "top_p": 1.0, "top_k": 0},
    {"label": "T=1.0 min_p=0.05",       "do_sample": True, "temperature": 1.0, "min_p": 0.05, "top_p": 1.0, "top_k": 0},
    # sharpening: the trained model's logits are ~3x too flat, so a sub-1 temperature
    # restores a base-like distribution while still sampling
    {"label": "T=0.2 (sharpened)",      "do_sample": True, "temperature": 0.2, "top_p": 0.95},
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", nargs="+", required=True, help="name=path_or_hf_id")
    ap.add_argument("--mmlu", default="data/benchmarks/mmlu.jsonl.gz")
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--out", default="runs/diag")
    ap.add_argument("--device", default="cuda:0")
    args = ap.parse_args()

    import torch
    from transformers import AutoTokenizer

    prompts = mmlu_prompts(args.mmlu, args.n)
    gold = {}
    with open(args.mmlu, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                r = json.loads(line)
                gold[r["id"]] = r["gold"]

    results: Dict[str, Dict[str, Any]] = {}
    for spec in args.models:
        name, path = spec.split("=", 1)
        print(f"\nloading {name}")
        tok = AutoTokenizer.from_pretrained(path)
        model, _ = load_lm(path, dtype=torch.bfloat16, device_map=args.device)
        print(f"  {describe_scaling(model.config)}")
        model.eval()
        for cfg in CONFIGS:
            torch.manual_seed(args.seed)
            kw = {k: v for k, v in cfg.items() if k != "label"}
            n_fmt = n_ok = 0
            samples = []
            for row in prompts:
                text = tok.apply_chat_template(row["messages"], tokenize=False, add_generation_prompt=True)
                ids = tok(text, return_tensors="pt").to(model.device)
                with torch.no_grad():
                    out = model.generate(**ids, max_new_tokens=8, pad_token_id=tok.eos_token_id, **kw)
                gen = tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()
                first = gen[:1]
                in_fmt = first in LETTERS
                n_fmt += int(in_fmt)
                n_ok += int(in_fmt and first == gold[row["id"]])
                if len(samples) < 3:
                    samples.append(gen[:60])
            results.setdefault(name, {})[cfg["label"]] = {
                "n": len(prompts), "format_ok": round(n_fmt / len(prompts), 4),
                "accuracy": round(n_ok / len(prompts), 4), "samples": samples}
            print(f"  {cfg['label']:<20} format-ok {n_fmt/len(prompts):.2f}  acc {n_ok/len(prompts):.3f}  "
                  f"e.g. {samples[0]!r}")
        del model
        torch.cuda.empty_cache()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "hf_sampling_check.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nwrote {out/'hf_sampling_check.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
