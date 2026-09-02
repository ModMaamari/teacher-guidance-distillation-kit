"""Prepare three standard held-out benchmarks for the catastrophic-forgetting check.

The question this eval answers: after LoRA-SFT on teacher-guidance agent trajectories,
does the student still have its general abilities? The three benchmarks are chosen to
cover capabilities the fine-tuning data never touches, so any drop is forgetting rather
than distribution shift toward the training task:

    MMLU        broad factual knowledge, 4-way multiple choice   (test split)
    GSM8K       multi-step arithmetic reasoning, free-form        (test split)
    HellaSwag   commonsense sentence completion, 4-way choice     (validation split;
                the test split ships without public labels)

Each row is normalised to a single schema so one evaluator handles all three::

    {"id", "benchmark", "kind": "mcq"|"numeric", "question", "choices": [...],
     "gold": "A"|"42", "meta": {...}}

Sampling is deterministic (seeded, stratified by subject where applicable) so both arms
see identical items and a re-run reproduces the set exactly.

Usage::

    python scripts/prepare_benchmarks.py --out data/benchmarks
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # project root -> import tgd/agentsim

import argparse
import hashlib
import json
import random
import re
from collections import defaultdict
from pathlib import Path

from tgd.io import write_jsonl  # noqa: E402

LETTERS = ["A", "B", "C", "D"]


def _norm_space(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def load_mmlu(n: int, seed: int):
    """MMLU test split, stratified over its 57 subjects."""
    from datasets import load_dataset
    ds = load_dataset("cais/mmlu", "all", split="test")
    by_subject = defaultdict(list)
    for i, r in enumerate(ds):
        by_subject[r["subject"]].append(i)
    rnd = random.Random(seed)
    subjects = sorted(by_subject)
    per = max(1, n // len(subjects))
    picked = []
    for s in subjects:
        idx = sorted(by_subject[s])
        rnd.shuffle(idx)
        picked += idx[:per]
    rnd.shuffle(picked)
    picked = sorted(picked[:n])
    rows = []
    for i in picked:
        r = ds[i]
        if len(r["choices"]) != 4 or not (0 <= r["answer"] < 4):
            continue
        rows.append({"id": f"mmlu-{i}", "benchmark": "mmlu", "kind": "mcq",
                     "question": _norm_space(r["question"]),
                     "choices": [_norm_space(c) for c in r["choices"]],
                     "gold": LETTERS[r["answer"]], "meta": {"subject": r["subject"]}})
    return rows


def load_gsm8k(n: int, seed: int):
    """GSM8K test split; the gold answer is the number after the '####' marker."""
    from datasets import load_dataset
    ds = load_dataset("openai/gsm8k", "main", split="test")
    idx = list(range(len(ds)))
    if n and n < len(idx):
        rnd = random.Random(seed)
        rnd.shuffle(idx)
        idx = sorted(idx[:n])
    rows = []
    for i in idx:
        r = ds[i]
        gold = r["answer"].split("####")[-1].strip().replace(",", "")
        rows.append({"id": f"gsm8k-{i}", "benchmark": "gsm8k", "kind": "numeric",
                     "question": _norm_space(r["question"]), "choices": [],
                     "gold": gold, "meta": {}})
    return rows


def load_hellaswag(n: int, seed: int):
    """HellaSwag validation split (test labels are not public)."""
    from datasets import load_dataset
    ds = load_dataset("Rowan/hellaswag", split="validation")
    idx = list(range(len(ds)))
    rnd = random.Random(seed)
    rnd.shuffle(idx)
    idx = sorted(idx[:n]) if n else idx
    rows = []
    for i in idx:
        r = ds[i]
        try:
            label = int(r["label"])
        except (TypeError, ValueError):
            continue
        if len(r["endings"]) != 4 or not (0 <= label < 4):
            continue
        ctx = _norm_space((r.get("ctx_a", "") + " " + r.get("ctx_b", "")).strip() or r.get("ctx", ""))
        rows.append({"id": f"hellaswag-{i}", "benchmark": "hellaswag", "kind": "mcq",
                     "question": ctx, "choices": [_norm_space(e) for e in r["endings"]],
                     "gold": LETTERS[label], "meta": {"activity": r.get("activity_label", "")}})
    return rows


LOADERS = {"mmlu": load_mmlu, "gsm8k": load_gsm8k, "hellaswag": load_hellaswag}
LICENSES = {"mmlu": ("cais/mmlu", "test", "MIT", "https://github.com/hendrycks/test"),
            "gsm8k": ("openai/gsm8k", "test", "MIT", "https://github.com/openai/grade-school-math"),
            "hellaswag": ("Rowan/hellaswag", "validation", "MIT", "https://rowanzellers.com/hellaswag/")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="data/benchmarks")
    ap.add_argument("--mmlu", type=int, default=1710, help="~30 per subject over 57 subjects")
    ap.add_argument("--gsm8k", type=int, default=0, help="0 = the full test split (1,319)")
    ap.add_argument("--hellaswag", type=int, default=1500)
    ap.add_argument("--seed", type=int, default=13)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {"seed": args.seed, "benchmarks": {}}
    for name, size in (("mmlu", args.mmlu), ("gsm8k", args.gsm8k), ("hellaswag", args.hellaswag)):
        rows = LOADERS[name](size, args.seed)
        path = out / f"{name}.jsonl.gz"
        write_jsonl(path, rows)
        src, split, lic, home = LICENSES[name]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest["benchmarks"][name] = {"n": len(rows), "source": src, "split": split,
                                        "license": lic, "homepage": home,
                                        "requested": size or "all", "sha256": digest,
                                        "kind": rows[0]["kind"] if rows else None}
        print(f"{name:<10} {len(rows):>5} items from {src} [{split}] -> {path}")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote {out/'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
