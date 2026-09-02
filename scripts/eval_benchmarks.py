"""Catastrophic-forgetting evaluation: base student vs teacher-guidance-trained student.

Both arms are served by ONE vLLM server (base weights + the LoRA adapter as a named
module), so the only difference between them is the adapter. Prompts are ordinary chat
prompts in each benchmark's conventional format -- deliberately NOT the agent format the
adapter was trained on, because the question is whether general ability survived.

Scoring is generative with strict parsing, plus a lenient fallback, and both are
reported:

    strict   the reply is exactly the expected shape (a bare letter for MCQ,
             "#### <number>" or a final number for GSM8K)
    lenient  the answer is recoverable from a messier reply (first standalone letter,
             last number in the text)
    format_fail   nothing usable could be parsed even leniently

The gap between strict and lenient, and the format-failure rate, are the sharpest
forgetting signals: a model that has over-fitted to emitting agent JSON keeps the
knowledge but loses the ability to answer in the requested form.

Resumable: predictions are appended to <out>/predictions.jsonl as they land and skipped
on a re-run. Progress in <out>/status.json.

Usage::

    python training_methods/forgetting/eval_benchmarks.py \
        --benchmarks training_methods/forgetting/data/mmlu.jsonl \
        --served-model student --out training_methods/forgetting/runs/base/mmlu
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # project root -> import tgd/agentsim

from tgd.io import read_jsonl  # noqa: E402
from tgd.logging_utils import setup_logger, write_json  # noqa: E402

LETTERS = ["A", "B", "C", "D"]

MCQ_SYSTEM = "You are a helpful assistant answering multiple-choice questions."
MCQ_TEMPLATE = """{question}

A. {a}
B. {b}
C. {c}
D. {d}

Answer with the single letter (A, B, C or D) of the correct option. Reply with the letter only."""

GSM_SYSTEM = "You are a helpful assistant that solves grade-school math word problems."
GSM_TEMPLATE = """{question}

Solve the problem step by step, then give the final numeric answer on its own last line in the form:
#### <number>"""


def build_messages(row: Dict[str, Any]) -> List[Dict[str, str]]:
    if row["kind"] == "mcq":
        c = row["choices"]
        return [{"role": "system", "content": MCQ_SYSTEM},
                {"role": "user", "content": MCQ_TEMPLATE.format(question=row["question"],
                                                                a=c[0], b=c[1], c=c[2], d=c[3])}]
    return [{"role": "system", "content": GSM_SYSTEM},
            {"role": "user", "content": GSM_TEMPLATE.format(question=row["question"])}]


_NUM = re.compile(r"-?\d[\d,]*\.?\d*")


def parse_mcq(text: str):
    """(strict, lenient) letter predictions."""
    t = (text or "").strip()
    strict = t if t in LETTERS else (t[0] if len(t) >= 1 and t[0] in LETTERS and (len(t) == 1 or not t[1].isalnum()) else None)
    lenient = strict
    if lenient is None:
        m = re.search(r"\b([ABCD])\b", t)                      # a standalone letter
        if not m:
            m = re.search(r"(?:answer|option)\D{0,12}([ABCD])", t, re.I)
        if not m:                                              # JSON-ish or quoted letter
            m = re.search(r'["\':\s]([ABCD])["\',\s]', t)
        lenient = m.group(1) if m else None
    return strict, lenient


def _clean_num(s: str) -> str:
    s = s.replace(",", "").rstrip(".")
    if s.endswith(".0"):
        s = s[:-2]
    try:                       # normalise 18.00 -> 18, keep non-numerics as-is
        f = float(s)
        return str(int(f)) if f == int(f) else str(f)
    except ValueError:
        return s


def parse_numeric(text: str):
    t = (text or "").strip()
    strict = None
    m = re.search(r"####\s*(-?[\d,]+\.?\d*)", t)
    if m:
        strict = _clean_num(m.group(1))
    lenient = strict
    if lenient is None:
        nums = _NUM.findall(t)
        lenient = _clean_num(nums[-1]) if nums else None
    return strict, lenient


def score(row: Dict[str, Any], text: str) -> Dict[str, Any]:
    parse = parse_mcq if row["kind"] == "mcq" else parse_numeric
    strict, lenient = parse(text)
    gold = row["gold"] if row["kind"] == "mcq" else _clean_num(row["gold"])
    return {"strict_pred": strict, "lenient_pred": lenient,
            "strict_correct": int(strict is not None and strict == gold),
            "lenient_correct": int(lenient is not None and lenient == gold),
            "format_fail": int(lenient is None),
            "strict_format_ok": int(strict is not None)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--benchmarks", nargs="+", required=True, help="prepared benchmark jsonl file(s)")
    ap.add_argument("--out", required=True, help="fixed output dir (resumable)")
    ap.add_argument("--server-url", default="http://127.0.0.1:8300")
    ap.add_argument("--served-model", default="student", help="'student' = base weights; a LoRA module name = trained")
    ap.add_argument("--arm", default=None, help="label recorded in metrics (default: --served-model)")
    ap.add_argument("--max-tokens", type=int, default=None, help="default: 8 for MCQ, 512 for numeric")
    ap.add_argument("--temperature", type=float, default=0.0,
                    help="0 = greedy and deterministic; >0 with distinct --seed values gives "
                         "independent replicates whose spread measures decoding noise")
    ap.add_argument("--seed", type=int, default=None,
                    help="per-request sampling seed (only meaningful with --temperature > 0)")
    ap.add_argument("--run", default=None, help="label for this replicate, recorded in metrics.json")
    ap.add_argument("--concurrency", type=int, default=32)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--timeout", type=float, default=180.0)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    log = setup_logger("forgetting", out / "eval.log")
    rows: List[Dict[str, Any]] = []
    for f in args.benchmarks:
        rows += list(read_jsonl(f))
    if args.limit:
        rows = rows[:args.limit]

    pred_path = out / "predictions.jsonl"
    done = set()
    if pred_path.exists():
        for line in pred_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["id"])
    todo = [r for r in rows if r["id"] not in done]
    log.info(f"{len(rows)} items | {len(done)} already done | {len(todo)} to run "
             f"| arm={args.arm or args.served_model} served={args.served_model} "
             f"run={args.run} T={args.temperature} seed={args.seed}")
    if not todo:
        log.info("nothing to do")

    client = httpx.Client(timeout=args.timeout)
    t0 = time.time()
    n_done = [len(done)]
    fh = pred_path.open("a", encoding="utf-8")

    def one(row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        max_tok = args.max_tokens or (8 if row["kind"] == "mcq" else 512)
        body = {"model": args.served_model, "messages": build_messages(row),
                "max_tokens": max_tok, "temperature": args.temperature}
        if args.temperature and args.temperature > 0:
            body["top_p"] = 0.95
            if args.seed is not None:
                body["seed"] = args.seed
        for attempt in range(3):
            try:
                r = client.post(f"{args.server_url}/v1/chat/completions", json=body)
                r.raise_for_status()
                data = r.json()
                text = (data["choices"][0]["message"]["content"] or "")
                usage = data.get("usage") or {}
                return {"id": row["id"], "benchmark": row["benchmark"], "kind": row["kind"],
                        "gold": row["gold"], "response": text[:4000],
                        "prompt_tokens": usage.get("prompt_tokens", 0),
                        "completion_tokens": usage.get("completion_tokens", 0),
                        "meta": row.get("meta", {}), **score(row, text)}
            except Exception as exc:  # noqa: BLE001 -- retried, then left for the next pass
                if attempt == 2:
                    log.warning(f"{row['id']} failed: {type(exc).__name__}: {str(exc)[:120]}")
                time.sleep(1.5 * (attempt + 1))
        return None

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        for rec in pool.map(one, todo):
            if rec is None:
                continue
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            n_done[0] += 1
            if n_done[0] % 100 == 0 or n_done[0] == len(rows):
                rate = (n_done[0] - len(done)) / max(time.time() - t0, 1e-9)
                write_json(out / "status.json", {"done": n_done[0], "total": len(rows),
                                                 "rate_per_s": round(rate, 2),
                                                 "eta_min": round((len(rows) - n_done[0]) / max(rate, 1e-9) / 60, 1)})
                log.info(f"[{n_done[0]}/{len(rows)}] {rate:.1f} it/s")
    fh.close()

    preds = [json.loads(l) for l in pred_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    by_bench: Dict[str, List[Dict[str, Any]]] = {}
    for p in preds:
        by_bench.setdefault(p["benchmark"], []).append(p)
    metrics: Dict[str, Any] = {"arm": args.arm or args.served_model, "served_model": args.served_model,
                               "temperature": args.temperature, "seed": args.seed,
                               "run": args.run, "n_total": len(preds),
                               "wall_time_s": round(time.time() - t0, 1), "benchmarks": {}}
    for b, ps in sorted(by_bench.items()):
        n = len(ps)
        metrics["benchmarks"][b] = {
            "n": n,
            "strict_accuracy": round(sum(p["strict_correct"] for p in ps) / n, 4),
            "lenient_accuracy": round(sum(p["lenient_correct"] for p in ps) / n, 4),
            "strict_format_ok": round(sum(p["strict_format_ok"] for p in ps) / n, 4),
            "format_fail_rate": round(sum(p["format_fail"] for p in ps) / n, 4),
            "mean_completion_tokens": round(sum(p["completion_tokens"] for p in ps) / n, 1),
        }
    write_json(out / "metrics.json", metrics)
    missing = len(rows) - len(preds)
    if missing == 0:
        (out / ".done").write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    else:
        log.warning(f"{missing} items still missing; re-run to retry")
    print(json.dumps(metrics, indent=2))
    return 0 if missing == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
