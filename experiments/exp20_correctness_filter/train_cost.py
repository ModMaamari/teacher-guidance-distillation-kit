#!/usr/bin/env python
"""What each training arm cost: examples, tokens, compute, time and memory.

Accuracy is only half of the correctness-filter question; the other half is that keeping the
failed episodes doubles the training set. For every arm this reports:

  examples   training examples (prompt/completion pairs) in its split
  tokens     training tokens the trainer counted, derived from its own FLOP counter
  PFLOPs     the trainer's floating-point-operation counter (transformers counts 6 x parameters
             x tokens, so it is an upper bound for LoRA, which needs no weight gradients for the
             frozen base, and is directly comparable between arms)
  GPU-h      wall-clock on the worker's GPU, summed over resumed chunks. Several runs shared one
             GPU with another training, so this is an upper bound on exclusive GPU time.
  peak GiB   peak memory the training process itself allocated (torch), unaffected by sharing

    python experiments/exp20_correctness_filter/train_cost.py \\
        --arm correct13=selftaught --arm mixall13=mixall_s13 ... --json-out cost.json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
PARAMS = 3.4e9          # Granite-4.1-3B, as in the paper's cost table
PEAK_RE = re.compile(r"peak ([\d.]+) GiB")


def one(run: str) -> dict:
    d = KIT / "runs" / "train" / run
    out: dict = {"run": run}
    fm = d / "final_metrics.json"
    if fm.exists():
        m = json.loads(fm.read_text(encoding="utf-8"))
        out["flops"] = m.get("total_flos")
        out["epochs"] = m.get("epoch")
        out["train_loss"] = m.get("train_loss")
        out["eval_loss"] = m.get("eval_loss")
    cfg = d / "train_config.json"
    if cfg.exists():
        c = json.loads(cfg.read_text(encoding="utf-8"))
        c = c.get("args", c)
        out["split"] = c.get("train_file")
        out["batch"] = (c.get("batch_size") or 0) * (c.get("grad_accum") or 0)
        f = KIT / str(out["split"] or "no-such-file")
        if f.is_file():
            out["examples"] = sum(1 for line in f.open(encoding="utf-8") if line.strip())
    log = d / "train.log"
    if log.exists():
        peaks = [float(x) for x in PEAK_RE.findall(log.read_text(encoding="utf-8", errors="replace"))]
        out["peak_gib"] = max(peaks) if peaks else None
        out["resumes"] = log.read_text(encoding="utf-8", errors="replace").count("training ... resuming")
    hours, gpus = 0.0, []
    peaks_tsv = KIT / "runs" / "pool" / "queue" / "peaks.tsv"
    if peaks_tsv.exists():
        for line in peaks_tsv.read_text(encoding="utf-8").splitlines():
            p = line.split("\t")
            if len(p) >= 4 and p[0] == f"train_{run}":
                hours += float(p[2])
                gpus.append(p[3])
    st = d / "status.json"
    if not hours and st.exists():     # still running, or killed before the worker recorded it
        hours = json.loads(st.read_text(encoding="utf-8")).get("elapsed_s", 0) / 3600
    out["gpu_hours"] = round(hours, 2) or None
    out["gpu"] = sorted(set(gpus)) or None
    if out.get("flops"):
        out["tokens"] = round(out["flops"] / (6 * PARAMS))
        out["pflops"] = round(out["flops"] / 1e15, 1)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arm", nargs="+", required=True, help="<arm>=<training run under runs/train>")
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    rows = {arm: one(run) for arm, run in (s.split("=", 1) for s in a.arm)}
    print(f"  {'arm':<12}{'examples':>10}{'tokens':>12}{'PFLOPs':>9}{'GPU-h':>8}{'peak GiB':>10}  gpu")
    for arm, r in rows.items():
        def f(k, w, fmt=","):
            v = r.get(k)
            return f"{v:>{w}{fmt}}" if isinstance(v, (int, float)) else f"{'--':>{w}}"
        print(f"  {arm:<12}{f('examples', 10)}{f('tokens', 12)}{f('pflops', 9, '.1f')}"
              f"{f('gpu_hours', 8, '.2f')}{f('peak_gib', 10, '.1f')}  {', '.join(r.get('gpu') or ['--'])}"
              + (f"  (resumed {r['resumes']}x)" if r.get("resumes") else ""))
    print("\nPFLOPs: the trainer's own counter (6 x parameters x tokens; an upper bound for LoRA).")
    print("GPU-h: wall-clock on the worker's GPU, summed over chunks; some runs shared a GPU.")
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
