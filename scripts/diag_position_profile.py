"""Where along the completion does the trained student's distribution go flat?

``scripts/diag_distributions.py`` measures a single position: the first token the model must
generate. It found a near-uniform distribution there (entropy ~11 nats, top-1 ~0.001)
while the argmax stayed correct, which explains why greedy works and sampling collapses.

That leaves the decisive question open. On this project's student the average training loss was ~0.5, and one
catastrophic position diluted by several hundred easy ones is arithmetically consistent
with that. So the flatness may be confined to the transition into generation rather than
spread across the whole completion. The two cases call for completely different fixes:

* front-loaded  -> force greedy for the first k tokens, sample the rest. A decoding change.
* everywhere    -> the objective has to change. A training problem.

This script settles it. For each held-out example it runs ONE teacher-forced pass over
prompt + reference completion and records, at every completion position, the entropy, the
top-1 probability, and the probability the model assigns to the reference token. It then
reports those as a profile over position index, so the shape is readable directly.

Usage::

    python scripts/diag_position_profile.py \
        --models base=ibm-granite/granite-4.1-3b trained=<merged dir> \
        --data data/splits/uniform/dev.jsonl \
        --n 64 --out runs/diag_positions
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # project root -> import tgd/agentsim

import argparse  # noqa: E402
import json  # noqa: E402
from typing import Any, Dict, List  # noqa: E402

from tgd.io import read_jsonl
from tgd.logit_scale import describe as describe_scaling  # noqa: E402
from tgd.models import load_lm  # noqa: E402  # noqa: E402  (gz-aware: the shipped data is gzipped)

# Position buckets. Fine near the start, where the pathology is suspected, coarse later.
BUCKETS = [(0, 1), (1, 2), (2, 4), (4, 8), (8, 16), (16, 32), (32, 64),
           (64, 128), (128, 256), (256, float("inf"))]


def _key(a: int, b: float) -> str:
    """Bucket label. The last bucket is open-ended, so no position can fall outside it."""
    return f"{a}+" if b == float("inf") else f"{a}-{b}"


def load_rows(path: str, n: int) -> List[Dict[str, Any]]:
    rows = []
    for r in read_jsonl(path):
        rows.append(r)
        if len(rows) >= n:
            break
    return rows


def summarise(values: List[float]) -> Dict[str, float]:
    if not values:
        return {}
    s = sorted(values)
    return {"n": len(s), "mean": round(sum(s) / len(s), 4),
            "median": round(s[len(s) // 2], 4),
            "p10": round(s[int(0.10 * (len(s) - 1))], 4),
            "p90": round(s[int(0.90 * (len(s) - 1))], 4)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", nargs="+", required=True, help="name=path_or_hf_id")
    ap.add_argument("--data", default="data/splits/uniform/dev.jsonl")
    ap.add_argument("--n", type=int, default=64)
    ap.add_argument("--max-length", type=int, default=8192)
    ap.add_argument("--out", default="runs/diag_positions")
    ap.add_argument("--device", default="cuda:0")
    args = ap.parse_args()

    import torch
    from transformers import AutoTokenizer

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = load_rows(args.data, args.n)
    print(f"{len(rows)} examples from {args.data}")

    summary: Dict[str, Any] = {}
    per_pos_path = out / "per_position.jsonl"
    fh_out = per_pos_path.open("w", encoding="utf-8")

    for spec in args.models:
        name, path = spec.split("=", 1)
        print(f"\nloading {name} from {path}", flush=True)
        tok = AutoTokenizer.from_pretrained(path)
        model, _ = load_lm(path, dtype=torch.bfloat16, device_map=args.device)
        print(f"  {describe_scaling(model.config)}")
        model.eval()

        buckets: Dict[str, Dict[str, List[float]]] = {
            _key(a, b): {"entropy": [], "top1": [], "ref_prob": []} for a, b in BUCKETS}
        skipped = 0

        for i, r in enumerate(rows):
            # Tokenise prompt alone and prompt+completion, so the completion positions are
            # exactly the difference. This mirrors how completion-only loss is masked.
            p_text = tok.apply_chat_template(r["prompt"], tokenize=False,
                                             add_generation_prompt=True)
            full_text = p_text + r["completion"][0]["content"]
            p_ids = tok(p_text, return_tensors="pt", add_special_tokens=False)["input_ids"]
            f_ids = tok(full_text, return_tensors="pt", add_special_tokens=False)["input_ids"]
            start = p_ids.shape[1]
            if f_ids.shape[1] <= start or f_ids.shape[1] > args.max_length:
                skipped += 1
                continue
            f_ids = f_ids.to(model.device)

            with torch.no_grad():
                logits = model(input_ids=f_ids).logits[0].float()
            # logits[t] predicts token t+1, so completion token at index j = start + k is
            # predicted by logits[start + k - 1].
            for k in range(f_ids.shape[1] - start):
                pos = start + k
                lg = logits[pos - 1]
                probs = torch.softmax(lg, dim=-1)
                ent = float(-(probs * torch.log(probs.clamp_min(1e-12))).sum())
                top1 = float(probs.max())
                ref = float(probs[int(f_ids[0, pos])])
                for a, b in BUCKETS:
                    if a <= k < b:
                        key = _key(a, b)
                        buckets[key]["entropy"].append(ent)
                        buckets[key]["top1"].append(top1)
                        buckets[key]["ref_prob"].append(ref)
                        break
                if k < 8:      # keep the fine detail for the first few positions
                    fh_out.write(json.dumps({"model": name, "example": i, "k": k,
                                             "entropy": round(ent, 4),
                                             "top1": round(top1, 6),
                                             "ref_prob": round(ref, 6)}) + "\n")
            if (i + 1) % 16 == 0:
                print(f"  {i + 1}/{len(rows)}")

        summary[name] = {key: {m: summarise(v[m]) for m in ("entropy", "top1", "ref_prob")}
                         for key, v in buckets.items() if v["entropy"]}
        summary[name]["_skipped"] = skipped

        print(f"\n== {name}: entropy / top-1 / P(reference token) by completion position")
        print(f"{'positions':>12}{'n':>8}{'entropy':>10}{'top1':>9}{'ref_prob':>10}")
        for key in [_key(a, b) for a, b in BUCKETS]:
            b = summary[name].get(key)
            if not b:
                continue
            print(f"{key:>12}{b['entropy']['n']:>8}{b['entropy']['mean']:>10.3f}"
                  f"{b['top1']['mean']:>9.3f}{b['ref_prob']['mean']:>10.3f}")

        del model
        torch.cuda.empty_cache()

    fh_out.close()
    (out / "position_profile.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(f"\nwrote {out / 'position_profile.json'} and {per_pos_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
