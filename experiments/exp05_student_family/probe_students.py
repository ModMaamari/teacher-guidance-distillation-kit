#!/usr/bin/env python3
"""Cheap pre-flight for candidate students: tokenizer and chat template only, no weights.

Catches, before a GPU is booked:
  * no chat template                -> unusable as an agent
  * a template that opens a reasoning block -> answer-token metrics are meaningless unless
    it is closed first (tgd.chat_template does that; you still want to know)
  * an architecture transformers cannot resolve -> vLLM and the trainer will fail too
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

MESSAGES = [{"role": "system", "content": "You are a retrieval agent."},
            {"role": "user", "content": "Who directed Alien?"}]


def probe(model_id: str) -> tuple[str, str]:
    try:
        from transformers import AutoConfig, AutoTokenizer
    except Exception as exc:                                    # pragma: no cover
        return "ERROR", f"transformers unavailable: {exc}"

    arch = "?"
    try:
        cfg = AutoConfig.from_pretrained(model_id, trust_remote_code=False)
        arch = (getattr(cfg, "architectures", None) or ["?"])[0]
    except Exception as exc:
        text = str(exc)
        msg = text.splitlines()[0][:70]
        if "trust_remote_code" in text:
            return "REMOTE-CODE", f"needs trust_remote_code ({msg})"
        if any(k in text for k in ("couldn't connect", "offline mode", "Connection error",
                                   "OfflineModeIsEnabled", "Max retries")):
            return "OFFLINE", "not in the local cache and the network is off; re-probe online"
        return "NO-CONFIG", msg

    try:
        tok = AutoTokenizer.from_pretrained(model_id, trust_remote_code=False)
    except Exception as exc:
        return "NO-TOKENIZER", f"{arch}: {str(exc).splitlines()[0][:60]}"

    if not getattr(tok, "chat_template", None):
        return "NO-TEMPLATE", f"{arch}: no chat template -- cannot be used as an agent"

    try:
        from tgd import chat_template as ct
        text = tok.apply_chat_template(MESSAGES, tokenize=False, add_generation_prompt=True)
        if ct.opens_reasoning(text):
            by_kwarg = any(ct.render_prompt(tok, MESSAGES, **kw) and
                           not ct.opens_reasoning(ct.render_prompt(tok, MESSAGES, **kw))
                           for kw in ct.CANDIDATE_KWARGS)
            if by_kwarg:
                return "REASONING-OK", f"{arch}: opens a reasoning block; a template keyword closes it"
            forced = ct.force_close(text)
            if forced is not None and not ct.opens_reasoning(forced):
                return "REASONING-FORCED", (f"{arch}: opens a reasoning block unconditionally; "
                                            "closed by appending the marker")
            return "REASONING-OPEN", f"{arch}: opens a reasoning block, NOT closable -- answer metrics invalid"
        return "OK", f"{arch}: plain template, {len(text)} chars"
    except Exception as exc:
        return "TEMPLATE-ERROR", f"{arch}: {str(exc).splitlines()[0][:60]}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="")
    ap.add_argument("--file", default=str(pathlib.Path(__file__).with_name("students.txt")))
    a = ap.parse_args()

    ids = [m.strip() for m in a.models.split(",") if m.strip()]
    if not ids:
        p = pathlib.Path(a.file)
        if not p.exists():
            print(f"!! no --models and no {p}", file=sys.stderr)
            return 2
        ids = [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines()
               if ln.strip() and not ln.startswith("#")]

    bad = 0
    for m in ids:
        status, detail = probe(m)
        print(f"  {status:<14} {m:<34} {detail}")
        if status in ("NO-TEMPLATE", "REASONING-OPEN", "NO-CONFIG", "NO-TOKENIZER"):
            bad += 1
    print(f"\n{len(ids)} probed, {bad} need attention before training")
    print("OFFLINE just means the model is not cached here; re-probe with network access.")
    print("REMOTE-CODE is not fatal: re-probe with trust_remote_code once you trust the repo.")
    print("REASONING-FORCED is handled: tgd.chat_template closes the block so the diagnostics")
    print("measure the answer token, but expect that model to emit empty reasoning.")
    print("Run scripts/diag_distributions.py on a GPU before trusting any accuracy number.")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
