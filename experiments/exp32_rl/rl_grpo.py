#!/usr/bin/env python
"""Outcome-reward RL for the search agent (E32): GRPO on the harness's own episodes.

Each round samples a batch of trainable questions, runs ``--group`` unguided episodes per
question with the current policy through the same agent harness every other collection uses
(``scripts/collect_episodes.py --no-teacher``, the policy served by vLLM as a LoRA adapter),
rewards an episode 1 when its final answer passes the cover match -- the correctness test every
SFT route in this kit filters on -- and takes one policy-gradient step:

    loss = - sum_i sum_t A_i * log pi(y_it) / sum_i |y_i|,   A_i = (r_i - mean_g) / (std_g + eps)

over every student call of every episode (plan and step calls, including repairs), on exactly
the prompt the policy saw (one user message, the model's chat template) and the text it sampled.
One update per batch keeps it on-policy, so no importance ratio or clipping is needed; no KL
term (as in DAPO / Dr. GRPO). Groups whose episodes all score the same carry no signal and are
not trained on.

Compute is counted as everywhere in the kit: collection 2 x 3.4B x tokens of every recorded call,
training 6 x 3.4B x trained tokens (the trainer's convention). When the running total passes a
``--milestones`` value, the adapter is published to ``runs/train/<name>_c<k>/adapter`` (with
``.done``) so the standard eval/judge tasks pick it up.

Resumable at round granularity: ``state.json`` + ``optimizer.pt`` + the last adapter are written
atomically after every round; a restart reloads them, re-registers the adapter with vLLM and
continues (a half-collected round resumes inside the harness).

Needs a vLLM server on $VLLM_ENDPOINT started with LoRA enabled and
VLLM_ALLOW_RUNTIME_LORA_UPDATING=True (the pool task does this).

    python experiments/exp32_rl/rl_grpo.py --name rl_s13 --seed 13 --milestones 1474 2948
    python experiments/exp32_rl/rl_grpo.py --name rl_smoke --smoke      # 2 tiny rounds
"""
from __future__ import annotations

import argparse
import gzip
import json
import math
import os
import random
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))

from tgd import DATASETS  # noqa: E402
from tgd.io import corpus_file, question_file, read_jsonl  # noqa: E402
from tgd.splits import pool_of  # noqa: E402

PARAMS = 3.4e9                      # Granite-4.1-3B, the convention of every cost table
SEP = "__g"                         # group copies of a question: <qid>__g<k>


def log(msg: str) -> None:
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} | {msg}", flush=True)


# ------------------------------------------------------------------------------ questions
def trainable_questions(root: str, per_dataset: int):
    """(dataset, row) for every trainable question among the first ``per_dataset`` of each
    dataset -- the questions every SFT route in the kit was collected on."""
    out = []
    for ds in DATASETS:
        for r in read_jsonl(question_file(root, ds), per_dataset):
            if pool_of(str(r.get("qid") or r["id"])) == "trainable":
                out.append((ds, r))
    return out


def batch_for_round(pool, rnd: int, size: int, seed: int):
    """Round ``rnd`` (1-based) takes the next ``size`` questions of a seeded permutation,
    reshuffled each pass, so every question is used before any repeats."""
    per_pass = len(pool) // size
    p, k = divmod(rnd - 1, per_pass)
    order = list(range(len(pool)))
    random.Random(seed * 1000 + p).shuffle(order)
    return [pool[i] for i in order[k * size:(k + 1) * size]]


def write_round_questions(batch, group: int, qdir: Path, root: str):
    """One question file per dataset with ``group`` renamed copies of each question. The copy's
    id goes into ``id`` (the harness's task id) and ``gold.qid`` (what the exporter records as the
    episode's qid), so the copies do not collide; ``retrieval_scope.qid`` keeps the original,
    because the retriever scopes search by it."""
    by_ds = {}
    for ds, r in batch:
        by_ds.setdefault(ds, []).append(r)
    for ds, rows in by_ds.items():
        d = qdir / ds
        d.mkdir(parents=True, exist_ok=True)
        with gzip.open(d / f"{ds}_questions.jsonl.gz", "wt", encoding="utf-8") as fh:
            for r in rows:
                qid = str(r.get("qid") or r["id"])
                for g in range(group):
                    new = f"{qid}{SEP}{g}"
                    row = {**r, "id": new, "gold": {**(r.get("gold") or {}), "qid": new}}
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        link = d / f"{ds}_corpus.jsonl.gz"
        if not link.exists():
            os.symlink(corpus_file(root, ds).resolve(), link)
    return sorted(by_ds)


# ------------------------------------------------------------------------------ vLLM
def vllm(path: str, payload: dict | None = None):
    url = os.environ["VLLM_ENDPOINT"].rstrip("/") + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"},
                                 method="POST" if payload is not None else "GET")
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.read().decode()


def served_models():
    return {m["id"] for m in json.loads(vllm("/v1/models"))["data"]}


def register_adapter(name: str, path: Path, keep: set):
    for old in served_models() - keep - {"student", name}:
        try:
            vllm("/v1/unload_lora_adapter", {"lora_name": old})
        except Exception as e:                                   # noqa: BLE001
            log(f"   could not unload {old}: {e}")
    if name not in served_models():
        vllm("/v1/load_lora_adapter", {"lora_name": name, "lora_path": str(path.resolve())})
    assert name in served_models(), f"vLLM did not register {name}"


# ------------------------------------------------------------------------------ rollouts
def collect(rnd_dir: Path, policy: str, datasets, a) -> Path:
    out = rnd_dir / "collect"
    eps = rnd_dir / "episodes"
    if (eps / "episodes.jsonl.gz").exists():
        return eps / "episodes.jsonl.gz"
    cmd = [sys.executable, "scripts/collect_episodes.py", "--datasets", *datasets,
           "--questions", str(rnd_dir / "questions"), "--num-samples", "100000",
           "--no-teacher", "--student", f"vllm/{policy}",
           "--student-temperature", str(a.temperature), "--student-max-tokens", str(a.max_tokens),
           "--shards", str(a.shards), "--out", str(out), "--tag", f"{a.name}_{rnd_dir.name}"]
    rc = subprocess.call(cmd, cwd=str(KIT))
    if rc not in (0, 3):                  # 3 = some episodes missing; checked below
        raise RuntimeError(f"collection failed rc={rc}")
    rc = subprocess.call([sys.executable, "scripts/consolidate_episodes.py", "--runs", str(out),
                          "--out", str(eps), "--gzip"], cwd=str(KIT))
    if rc != 0 or not (eps / "episodes.jsonl.gz").exists():
        raise RuntimeError(f"consolidation failed rc={rc}")
    return eps / "episodes.jsonl.gz"


def student_calls(ep):
    """Every call the student made in an episode, in order: its plan, then each step's calls
    (repairs and the forced-finish call included). Each is (prompt, response, usage)."""
    pr = ep.get("plan_review") or {}
    calls = list(pr.get("initial_plan_calls") or []) + list(pr.get("revised_plan_calls") or [])
    for st in ep.get("steps") or []:
        calls += list(st.get("student_calls") or [])
    return [(c.get("prompt") or "", c.get("response_text") or "", c.get("usage") or {})
            for c in calls if c.get("prompt")]


def call_tokens(ep) -> int:
    """Every model call's tokens, walked the way E23 prices a collection (student only here)."""
    n = 0

    def walk(o):
        nonlocal n
        if isinstance(o, dict):
            u = o.get("usage")
            if isinstance(u, dict) and ("prompt_tokens" in u or "completion_tokens" in u):
                n += int(u.get("prompt_tokens") or 0) + int(u.get("completion_tokens") or 0)
            for k, v in o.items():
                if k != "usage":
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(ep)
    return n


def advantages(episodes, group: int):
    groups = {}
    for ep in episodes:
        base = str(ep["qid"]).rsplit(SEP, 1)[0]
        r = 1.0 if (ep.get("final_metrics") or {}).get("answer_correct") else 0.0
        groups.setdefault(base, []).append((ep, r))
    out, informative = [], 0
    for base, members in groups.items():
        rs = [r for _, r in members]
        mu = sum(rs) / len(rs)
        sd = math.sqrt(sum((r - mu) ** 2 for r in rs) / len(rs))
        if sd < 1e-6:
            continue
        informative += 1
        out += [(ep, (r - mu) / (sd + 1e-4)) for ep, r in members]
    return out, len(groups), informative


# ------------------------------------------------------------------------------ training
def build_sequences(tok, weighted, max_tokens):
    """Token ids for every student call of every weighted episode: prompt ids, completion ids
    (the sampled text, plus the end token when the call was not cut off), and the advantage."""
    eos = tok.eos_token_id
    seqs = []
    for ep, adv in weighted:
        for prompt, response, usage in student_calls(ep):
            # render to text, then tokenize -- what vLLM does with a chat request
            text = tok.apply_chat_template([{"role": "user", "content": prompt}],
                                           add_generation_prompt=True, tokenize=False)
            p = tok(text, add_special_tokens=False)["input_ids"]
            c = tok(response, add_special_tokens=False)["input_ids"]
            if int(usage.get("completion_tokens") or 0) < max_tokens and eos is not None:
                c = c + [eos]
            if c:
                seqs.append((list(p), c, adv))
    return seqs


def pg_step(model, opt, seqs, a, torch, check=False):
    """One policy-gradient step over ``seqs``; token-level normalisation across the batch.

    One sequence per forward pass, and logits only at the positions that predict a sampled
    completion token (``logits_to_keep``, which runs the model's own head and logit scaling on
    those positions). Full-sequence logits for a 100k vocabulary do not fit next to vLLM on a
    45 GB card. ``check`` compares this path with a full forward on the first sequence."""
    model.train()
    total_c = sum(len(c) for _, c, _ in seqs)
    opt.zero_grad(set_to_none=True)
    loss_sum, trained_tokens = 0.0, 0
    for k, (p, c, adv) in enumerate(seqs):
        x = p + c
        ids = torch.tensor([x], device="cuda")
        keep = torch.arange(len(p) - 1, len(x) - 1, device="cuda")    # positions predicting c
        logits = model(input_ids=ids, logits_to_keep=keep).logits[0]    # [len(c), vocab]
        tgt = ids[0, len(p):]
        tok_logp = torch.log_softmax(logits.float(), dim=-1).gather(-1, tgt.unsqueeze(-1)).squeeze(-1)
        if check and k == 0:
            with torch.no_grad():
                full = model(input_ids=ids).logits[0, len(p) - 1:len(x) - 1].float()
                ref = torch.log_softmax(full, dim=-1).gather(-1, tgt.unsqueeze(-1)).squeeze(-1)
            diff = float((ref - tok_logp.detach()).abs().max())
            log(f"   loss-path check: max |log p| difference, selected vs full logits = {diff:.2e}")
            assert diff < 5e-2, f"logits_to_keep path disagrees with the full forward ({diff})"
        loss = -(tok_logp * adv).sum() / total_c
        loss.backward()
        loss_sum += float(loss)
        trained_tokens += len(x)
        del logits, tok_logp, loss
    gn = float(torch.nn.utils.clip_grad_norm_([q for q in model.parameters() if q.requires_grad],
                                              a.max_grad_norm))
    opt.step()
    opt.zero_grad(set_to_none=True)
    return loss_sum, gn, trained_tokens


# ------------------------------------------------------------------------------ main
def save_json(path: Path, obj) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="run name; outputs under runs/rl/<name>")
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--model", default=os.environ.get("STUDENT_MODEL", "ibm-granite/granite-4.1-3b"))
    ap.add_argument("--questions", default="data/questions")
    ap.add_argument("--per-dataset", type=int, default=2000)
    ap.add_argument("--batch", type=int, default=32, help="questions per round")
    ap.add_argument("--group", type=int, default=8, help="episodes per question (GRPO group)")
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=3000, help="student max tokens per call")
    ap.add_argument("--shards", type=int, default=8, help="collection workers per dataset")
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--max-grad-norm", type=float, default=1.0)
    ap.add_argument("--lora-r", type=int, default=32)
    ap.add_argument("--lora-alpha", type=int, default=64)
    ap.add_argument("--milestones", type=float, nargs="+", default=[1474.0, 2948.0],
                    help="cumulative PFLOPs at which to publish the adapter; the last one ends the run")
    ap.add_argument("--max-rounds", type=int, default=10_000)
    ap.add_argument("--smoke", action="store_true", help="2 rounds of 4 questions x 4 episodes")
    a = ap.parse_args()
    if a.smoke:
        a.batch, a.group, a.shards, a.max_rounds = 4, 4, 2, 2
        a.milestones = [1e9]

    import torch
    from peft import LoraConfig, PeftModel, get_peft_model
    from transformers import AutoTokenizer
    from tgd.models import load_lm

    random.seed(a.seed)
    torch.manual_seed(a.seed)
    run = KIT / "runs" / "rl" / a.name
    run.mkdir(parents=True, exist_ok=True)
    state_f = run / "state.json"
    state = json.loads(state_f.read_text(encoding="utf-8")) if state_f.exists() else {
        "round": 0, "pflops": 0.0, "collect_pflops": 0.0, "train_pflops": 0.0, "adapter": None,
        "published": [], "args": vars(a)}
    if state.get("done"):
        log(f"{a.name} already finished at {state['pflops']:.0f} PFLOPs")
        return 0

    tok = AutoTokenizer.from_pretrained(a.model)
    model, _ = load_lm(a.model, dtype=torch.bfloat16)
    model.cuda()
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    if state["adapter"]:
        model = PeftModel.from_pretrained(model, str(KIT / state["adapter"]), is_trainable=True)
    else:
        model = get_peft_model(model, LoraConfig(r=a.lora_r, lora_alpha=a.lora_alpha, lora_dropout=0.0,
                                                 target_modules="all-linear", task_type="CAUSAL_LM"))
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr,
                            betas=(0.9, 0.99), weight_decay=0.0)
    if state.get("optimizer") and state["adapter"]:
        opt.load_state_dict(torch.load(KIT / state["optimizer"], map_location="cuda"))
    log(f"{a.name}: round {state['round']} done, {state['pflops']:.0f} PFLOPs so far; "
        f"trainable params {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")

    if a.smoke:   # the completion must end the way vLLM stops sampling: on the end token
        full = tok.apply_chat_template([{"role": "user", "content": "q"}, {"role": "assistant", "content": "ANSWER"}],
                                       tokenize=False)
        log(f"eos {tok.eos_token!r}; chat template renders the assistant turn as ...{full[-40:]!r}")
        assert tok.eos_token and tok.eos_token in full.split("ANSWER", 1)[1], "assistant turn does not end with eos"
    pool = trainable_questions(a.questions, a.per_dataset)
    log(f"{len(pool)} trainable questions; {a.batch} x {a.group} episodes per round")
    policy = "student"
    if state["adapter"]:
        policy = f"{a.name}_r{state['round']}"
        register_adapter(policy, KIT / state["adapter"], keep=set())

    state_round0 = state["round"]
    while state["round"] < a.max_rounds:
        rnd = state["round"] + 1
        t0 = time.time()
        rnd_dir = run / "rounds" / f"r{rnd:04d}"
        batch = batch_for_round(pool, rnd, a.batch, a.seed)
        datasets = write_round_questions(batch, a.group, rnd_dir / "questions", a.questions)
        eps_file = collect(rnd_dir, policy, datasets, a)
        episodes = [json.loads(l) for l in gzip.open(eps_file, "rt", encoding="utf-8") if l.strip()]
        expected = len(batch) * a.group
        if len(episodes) < 0.9 * expected:
            raise RuntimeError(f"round {rnd}: only {len(episodes)} of {expected} episodes")
        t_collect = time.time() - t0
        c_tokens = sum(call_tokens(ep) for ep in episodes)
        reward = sum(bool((ep.get("final_metrics") or {}).get("answer_correct")) for ep in episodes) / len(episodes)
        weighted, n_groups, informative = advantages(episodes, a.group)
        if a.smoke and not weighted:          # exercise the gradient path even if no group varies
            weighted = [(ep, (1.0 if (ep.get("final_metrics") or {}).get("answer_correct") else 0.0) - 0.5)
                        for ep in episodes]
        seqs = build_sequences(tok, weighted, a.max_tokens)
        loss, gn, t_tokens = (0.0, 0.0, 0)
        if seqs:
            loss, gn, t_tokens = pg_step(model, opt, seqs, a, torch, check=a.smoke or rnd == state_round0 + 1)
        if a.smoke:
            assert seqs and math.isfinite(loss) and math.isfinite(gn) and gn > 0, (len(seqs), loss, gn)
        # adapter and optimizer are written under round-specific names and only then referenced
        # from state.json, so a crash at any point leaves a consistent (adapter, optimizer) pair
        adapter_dir = run / "adapters" / f"r{rnd:04d}"
        model.save_pretrained(str(adapter_dir))
        opt_file = run / "adapters" / f"optimizer_r{rnd:04d}.pt"
        torch.save(opt.state_dict(), opt_file)
        cp = 2 * PARAMS * c_tokens / 1e15
        tp = 6 * PARAMS * t_tokens / 1e15
        prev, prev_opt = state["adapter"], state.get("optimizer")
        state.update(round=rnd, adapter=str(adapter_dir.relative_to(KIT)),
                     optimizer=str(opt_file.relative_to(KIT)),
                     pflops=state["pflops"] + cp + tp, collect_pflops=state["collect_pflops"] + cp,
                     train_pflops=state["train_pflops"] + tp)
        row = {"round": rnd, "episodes": len(episodes), "reward": round(reward, 4),
               "groups": n_groups, "informative_groups": informative, "sequences": len(seqs),
               "loss": round(loss, 5), "grad_norm": round(gn, 4), "collect_tokens": c_tokens,
               "train_tokens": t_tokens, "collect_pflops": round(cp, 2), "train_pflops": round(tp, 2),
               "cum_pflops": round(state["pflops"], 1), "collect_s": round(t_collect),
               "total_s": round(time.time() - t0)}
        with open(run / "rl_log.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
        # publish every milestone this round crossed
        for k, m in enumerate(a.milestones, start=1):
            if state["pflops"] >= m and k not in state["published"]:
                dest = KIT / "runs" / "train" / f"{a.name.replace('_s', f'_c{k}_s', 1)}" / "adapter"
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(adapter_dir, dest)
                save_json(dest.parent / "rl_milestone.json", {**row, "milestone_pflops": m,
                                                              "adapter_from": str(adapter_dir.relative_to(KIT))})
                (dest / ".done").touch()
                state["published"].append(k)
                log(f"   milestone {k}: {state['pflops']:.0f} >= {m:.0f} PFLOPs -> {dest.relative_to(KIT)}")
        save_json(state_f, state)
        if prev and "adapters" in prev:        # keep the latest adapter and optimizer only
            shutil.rmtree(KIT / prev, ignore_errors=True)
        if prev_opt:
            (KIT / prev_opt).unlink(missing_ok=True)
        # the consolidated episodes stay; the harness's per-question traces are not needed again
        shutil.rmtree(rnd_dir / "collect", ignore_errors=True)
        log(f"round {rnd}: reward {reward:.3f}, informative groups {informative}/{n_groups}, "
            f"{len(seqs)} sequences, loss {loss:+.4f}, grad norm {gn:.3f}, "
            f"{cp + tp:.1f} PF (cum {state['pflops']:.0f}), {row['total_s']} s")
        if len(state["published"]) == len(a.milestones):
            state["done"] = True
            save_json(state_f, state)
            log(f"{a.name} finished: {state['pflops']:.0f} PFLOPs in {rnd} rounds")
            return 0
        policy = f"{a.name}_r{rnd}"
        register_adapter(policy, adapter_dir, keep=set())
    log(f"{a.name}: stopped at --max-rounds {a.max_rounds}")
    return 0 if a.smoke else 3


if __name__ == "__main__":
    sys.exit(main())
