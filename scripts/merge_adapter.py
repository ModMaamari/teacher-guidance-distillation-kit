"""Merge a LoRA adapter into the base weights and save a standalone model.

Why: vLLM's runtime LoRA path corrupts a fraction of sequences when sampling (T>0) under
concurrent batching -- verified on this stack by probing one server: the base arm is
clean at every concurrency, while the adapter arm degrades from 0/32 bad at concurrency
8 to near-total garbage at 64. Greedy decoding is unaffected. Merging removes the LoRA
code path, so both arms run through byte-identical inference and the comparison cannot be
contaminated by a serving bug.

Usage::

    python scripts/merge_adapter.py --base <hf id> \
        --adapter runs/train/uniform/adapter --out runs/train/uniform/merged
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # project root -> import tgd/agentsim
sys.path.insert(0, str(Path(__file__).resolve().parent))       # sibling scripts

import argparse
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", default="ibm-granite/granite-4.1-3b",
                    help="the base the adapter was trained on; must match exactly")
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    if (out / "config.json").exists():
        print(f"merged model already present: {out}")
        return 0

    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"loading base {args.base}")
    model = AutoModelForCausalLM.from_pretrained(args.base, dtype=torch.bfloat16)
    print(f"applying adapter {args.adapter}")
    model = PeftModel.from_pretrained(model, args.adapter)
    model = model.merge_and_unload()
    out.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(out), safe_serialization=True)
    tok = AutoTokenizer.from_pretrained(args.adapter if (Path(args.adapter) / "tokenizer_config.json").exists() else args.base)
    tok.save_pretrained(str(out))
    print(f"merged model saved to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
