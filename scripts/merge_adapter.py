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
import json
import shutil
from pathlib import Path

from tgd.logit_scale import describe, merge_lost_scaling  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", default=None,
                    help="the base the adapter was trained on. Defaults to the one the "
                         "adapter itself records, which is almost always what you want")
    ap.add_argument("--force-base", action="store_true",
                    help="merge onto --base even though the adapter records a different one")
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    if (out / "config.json").exists():
        print(f"merged model already present: {out}")
        return 0

    # A LoRA adapter records the base it was trained on. Merging onto a different one
    # produces garbage or a crash, and with several students in flight it is an easy
    # mistake -- so take the base from the adapter unless told otherwise, and refuse a
    # silent mismatch.
    recorded = None
    acfg = Path(args.adapter) / "adapter_config.json"
    if acfg.exists():
        recorded = json.loads(acfg.read_text()).get("base_model_name_or_path")
    if args.base is None:
        if not recorded:
            print("ERROR: this adapter does not record a base model; pass --base explicitly.")
            return 2
        args.base = recorded
        print(f"base from the adapter: {args.base}")
    elif recorded and recorded != args.base and not args.force_base:
        print(f"ERROR: the adapter was trained on {recorded!r} but --base is {args.base!r}. "
              f"Merging onto the wrong base produces a broken model. Drop --base to use the "
              f"recorded one, or pass --force-base if you are certain they are the same "
              f"weights under a different path.")
        return 2

    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"loading base {args.base}")
    model = AutoModelForCausalLM.from_pretrained(args.base, dtype=torch.bfloat16)
    base_config = model.config
    print(f"  {describe(base_config)}")
    print(f"applying adapter {args.adapter}")
    model = PeftModel.from_pretrained(model, args.adapter)
    model = model.merge_and_unload()
    out.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(out), safe_serialization=True)
    tok = AutoTokenizer.from_pretrained(args.adapter if (Path(args.adapter) / "tokenizer_config.json").exists() else args.base)
    tok.save_pretrained(str(out))

    # Merging writes a fresh config.json. If a logit-rescaling field did not survive it,
    # every later inference on this model runs at the wrong scale -- greedy would look
    # perfect and sampling would produce junk. Check before anyone depends on it.
    from transformers import AutoConfig
    lost = merge_lost_scaling(base_config, AutoConfig.from_pretrained(str(out)))
    if lost:
        print(f"ERROR: {lost}")
        print("       Refusing to leave a silently-wrong model on disk; removing it.")
        shutil.rmtree(out, ignore_errors=True)
        return 2

    print(f"merged model saved to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
