#!/usr/bin/env python
"""LoRA SFT of a student on guidance-as-internal-thought examples (TRL SFTTrainer).

Data: prompt/completion conversational JSONL as written by ``scripts/build_splits.py``
(``{"prompt": [messages], "completion": [message], "metadata": {...}}``). TRL applies
the model's own chat template and computes the loss on completion tokens only, so the
model learns to GENERATE the ``teacher_guidance`` block + thought + action and is never
trained on the (long) prompt tokens.

**Keeping the student samplable.** A model can be excellent at greedy decoding and unusable
when sampled, and no greedy evaluation will show it. Before training starts this script checks
that the loss it is about to optimise matches the model's own forward pass; if they disagree it
stops rather than producing a student that decodes correctly and samples junk. See
``docs/STABILITY.md``.

``--health-every`` samples a few held-out prompts at temperature 0.7 during training and logs
how many parse. That is the signal whose absence let the failure above reach evaluation
unnoticed.

Resumable: ``--out`` is a fixed directory. If ``<out>/adapter/.done`` exists the run is
skipped; if ``<out>/checkpoints/checkpoint-*`` exists training resumes from the latest
checkpoint (optimizer state included). Monitorable: ``<out>/train.log`` (UTC timestamps)
and ``<out>/status.json`` (step, epoch, loss, ETA -- rewritten at every logging step).

Artifacts: ``<out>/adapter/`` (PEFT adapter + tokenizer), ``train_config.json``,
``trainer_state.json`` (full log history), ``final_metrics.json``.

Examples::

    # group B student (train on all four datasets)
    python scripts/train_sft.py --train-file data/splits/uniform/train.jsonl \
        --dev-file data/splits/uniform/dev.jsonl --out runs/train/uniform

    # group A fold (never sees musique)
    python scripts/train_sft.py --train-file data/splits/lodo/fold_musique/train.jsonl \
        --dev-file data/splits/lodo/fold_musique/dev.jsonl --out runs/train/fold_musique

    # any other HF causal LM student
    python scripts/train_sft.py --model Qwen/Qwen2.5-3B-Instruct ...

    # 2-minute pipeline validation
    python scripts/train_sft.py --smoke --out runs/train/smoke ...
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import random
import time
from pathlib import Path

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # project root -> import tgd/agentsim

import tgd  # noqa: F401
from tgd.io import load_jsonl
from tgd import chat_template  # noqa: E402
from tgd.models import load_lm, vocab_size  # noqa: E402
from tgd.logit_scale import (autoscale_batch, chunked_loss_conflict,  # noqa: E402
                             describe as describe_scaling, loss_path_matches_forward)
from tgd.logging_utils import setup_logger, write_json


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="ibm-granite/granite-4.1-3b", help="HF id or local path of the student")
    ap.add_argument("--train-file", required=True)
    ap.add_argument("--dev-file", default=None)
    ap.add_argument("--out", required=True, help="run directory (fixed; resumable)")
    ap.add_argument("--epochs", type=float, default=2.0)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--batch-size", type=int, default=4, help="per-device micro-batch")
    ap.add_argument("--grad-accum", type=int, default=4, help="effective batch = batch-size x grad-accum x GPUs")
    ap.add_argument("--max-length", type=int, default=8192)
    ap.add_argument("--lora-r", type=int, default=32)
    ap.add_argument("--lora-alpha", type=int, default=64)
    ap.add_argument("--lora-dropout", type=float, default=0.05)
    ap.add_argument("--warmup-ratio", type=float, default=0.03)
    ap.add_argument("--eval-steps", type=int, default=200)
    ap.add_argument("--save-steps", type=int, default=200)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--no-autoscale-batch", action="store_true",
                    help="keep --batch-size as given even when the non-chunked loss would "
                         "materialise a very large logit tensor")
    ap.add_argument("--loss-type", choices=["auto", "nll", "chunked_nll"], default="auto",
                    help="auto: use nll when the model rescales logits, else TRL's "
                         "memory-chunked default")
    ap.add_argument("--health-every", type=int, default=0,
                    help="every N steps, sample --health-prompts held-out prompts at "
                         "--health-temperature and log how many parse as JSON (0 = off)")
    ap.add_argument("--health-prompts", type=int, default=8)
    ap.add_argument("--health-temperature", type=float, default=0.7)
    ap.add_argument("--limit", type=int, default=None, help="cap training examples")
    ap.add_argument("--load-4bit", action="store_true",
                    help="load the base weights in NF4 (QLoRA). The 3B student needs "
                         "~7.3 GB in bf16, which does not fit an 8 GB card; NF4 brings "
                         "that to ~2.3 GB. LoRA parameters and compute stay bf16.")
    ap.add_argument("--smoke", action="store_true", help="64 examples, 8 optimizer steps, no eval")
    ap.add_argument("--force", action="store_true", help="ignore an existing .done marker")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    done = out / "adapter" / ".done"
    if done.exists() and not args.force:
        print(f"already trained: {out / 'adapter'} (delete {done} or pass --force to retrain)")
        return 0
    log = setup_logger("train_sft", out / "train.log")
    log.info(f"args: {vars(args)}")

    for f in [args.train_file] + ([args.dev_file] if args.dev_file else []):
        if not Path(f).exists():
            log.error(f"{f} not found. The SFT train/dev files are not shipped; they are "
                      f"built from the episodes in data/episodes: run 'make data' "
                      f"(or scripts/build_splits.py) first.")
            return 2

    import torch
    from datasets import Dataset
    from peft import LoraConfig
    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainerCallback
    from trl import SFTConfig, SFTTrainer

    t0 = time.time()

    def take(path, limit, tag):
        """Load a split, sampling when capped. A cap must never be a file prefix: the
        splits used to be written dataset-by-dataset, so `--limit 1000` was one dataset
        and `--smoke` trained on HotpotQA alone. build_splits.py now shuffles, and
        sampling here keeps the guarantee for any file, however it was produced."""
        rows = [{"prompt": r["prompt"], "completion": r["completion"]} for r in load_jsonl(path)]
        if limit and limit < len(rows):
            log.info(f"{tag}: sampling {limit} of {len(rows)} examples (seed {args.seed})")
            rows = random.Random(f"{args.seed}:{tag}").sample(rows, limit)
        return rows

    limit = 64 if args.smoke else args.limit
    train_rows = take(args.train_file, limit, "train")
    dev_rows = take(args.dev_file, 32 if args.smoke else None, "dev") if args.dev_file else []
    log.info(f"loaded {len(train_rows)} train / {len(dev_rows)} dev examples")

    tokenizer = AutoTokenizer.from_pretrained(args.model)

    # Training renders prompt+completion and supervises the completion; inference renders
    # the prompt alone and asks the model to continue. Those must share a prefix, and for
    # reasoning models they silently do not. tgd/chat_template.py checks the real thing --
    # does the trained rendering start with the generation prompt? -- on a real example.
    probe = train_rows[0]
    ct_kwargs = chat_template.alignment_kwargs(tokenizer, probe["prompt"], probe["completion"])
    log.info(chat_template.describe(tokenizer, ct_kwargs, probe["prompt"], probe["completion"]))
    if not chat_template.aligned(tokenizer, probe["prompt"], probe["completion"], **ct_kwargs):
        log.error(
            "this model renders a different prompt for training than for inference, and no "
            "known chat-template keyword reconciles them. The student would be trained to "
            "continue one prefix and asked at evaluation to continue another: the loss looks "
            "healthy and the model writes into the gap. "
            f"{chat_template.divergence(tokenizer, probe['prompt'], probe['completion'])}. "
            "Add the keyword this template uses to tgd/chat_template.CANDIDATE_KWARGS.")
        return 2
    if ct_kwargs:
        for row in train_rows:
            row["chat_template_kwargs"] = dict(ct_kwargs)
        for row in dev_rows:
            row["chat_template_kwargs"] = dict(ct_kwargs)

    # bf16 needs a GPU. Falling back to fp32 on CPU keeps `--smoke` usable as a
    # pipeline check on a laptop; real training always runs on a GPU.
    on_gpu = torch.cuda.is_available()
    # Not every student is a plain causal LM: some ship as vision-language / conditional
    # generation architectures that are not in the causal-LM auto mapping at all.
    from tgd import sdpa_compat
    sdpa_compat.apply(log)

    quant_kwargs = {}
    if args.load_4bit:
        if not on_gpu:
            log.error("--load-4bit needs a GPU")
            return 2
        from transformers import BitsAndBytesConfig
        quant_kwargs = {"quantization_config": BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16), "device_map": {"": 0}}
    model, auto_cls = load_lm(args.model, dtype=torch.bfloat16 if on_gpu else torch.float32,
                              **quant_kwargs)
    if args.load_4bit:
        # Deliberately NOT peft.prepare_model_for_kbit_training: it upcasts every
        # non-quantized parameter to fp32, which for this student means the 100k-row
        # embedding and output projection go from 0.96 GB to 1.92 GB. On an 8 GB card
        # that gigabyte is the difference between training and paging to host memory,
        # and it buys nothing here -- the LoRA parameters are fp32 either way and the
        # loss-path check below verifies the objective against the model's own forward.
        # All that is actually needed is a gradient path into the frozen embedding.
        model.enable_input_require_grads()
        log.info("base weights loaded in NF4 (QLoRA); embeddings and compute stay bf16")
    if auto_cls != "AutoModelForCausalLM":
        log.info(f"loaded via {auto_cls} (this architecture is not a plain causal LM); "
                 f"SFT trains its text stack")
    log.info(f"model loaded in {time.time() - t0:.1f}s | cuda={torch.cuda.is_available()} "
             f"gpus={torch.cuda.device_count()}")

    def gpu_mem(tag):
        """Allocated vs reserved, logged at every phase. On an 8 GB card the difference
        between these two and the card's capacity is the difference between training and
        silently paging to host memory, which looks like a 5x slower GPU and nothing else."""
        if not on_gpu:
            return
        log.info(f"gpu[{tag}]: allocated {torch.cuda.memory_allocated()/2**30:.2f} GiB | "
                 f"reserved {torch.cuda.memory_reserved()/2**30:.2f} GiB | "
                 f"peak {torch.cuda.max_memory_allocated()/2**30:.2f} GiB")
        torch.cuda.reset_peak_memory_stats()

    gpu_mem("model loaded")
    log.info(describe_scaling(model.config))
    # Pick the loss path before building the config: a scaling mismatch silently produces a
    # model that decodes greedily but cannot be sampled.
    conflict = chunked_loss_conflict(model.config)
    if conflict and args.loss_type == "auto":
        log.warning(conflict + " Using loss_type='nll' instead.")
    use_nll = args.loss_type == "nll" or (conflict and args.loss_type == "auto")
    if conflict and args.loss_type == "chunked_nll":
        log.error(conflict + " Refusing to run: pass --loss-type nll, or --loss-type "
                  "chunked_nll is only safe for models without logit rescaling.")
        return 2

    # The chunked path exists to avoid materialising [batch, seq, vocab] logits. Without it
    # that tensor is real, and at the default micro-batch it is large enough to OOM partway
    # through an epoch -- when the first batch of full-length sequences arrives, not at step 0.
    # Trade micro-batch for accumulation so the effective batch, and the run, are unchanged.
    if use_nll and not args.no_autoscale_batch:
        new_bs, new_ga, gb = autoscale_batch(args.batch_size, args.grad_accum,
                                             args.max_length,
                                             vocab_size(model.config, tokenizer))
        if new_bs != args.batch_size:
            factor = args.batch_size
            args.batch_size, args.grad_accum = new_bs, new_ga
            log.warning(
                f"loss_type=nll materialises a {gb:.1f} GB logit tensor at micro-batch "
                f"{factor} (seq {args.max_length} x vocab "
                f"{vocab_size(model.config, tokenizer)}). Using "
                f"--batch-size 1 --grad-accum {args.grad_accum} instead: same effective "
                f"batch ({args.batch_size * args.grad_accum}), ~25% more wall time. "
                f"Pass --no-autoscale-batch to keep your own values.")

    peft_config = LoraConfig(r=args.lora_r, lora_alpha=args.lora_alpha, lora_dropout=args.lora_dropout,
                             target_modules="all-linear", task_type="CAUSAL_LM")
    do_eval = bool(dev_rows) and not args.smoke

    class Health(TrainerCallback):
        """Periodically sample held-out prompts and log how many parse -- the check whose
        absence let a model that cannot be sampled pass every other test."""

        def __init__(self, trainer, prompts):
            self.trainer, self.prompts = trainer, prompts

        def on_step_end(self, a, state, control, **kw):
            if not (args.health_every and state.global_step
                    and state.global_step % args.health_every == 0 and state.is_world_process_zero):
                return
            m = self.trainer.model
            m.eval()
            ok = 0
            with torch.no_grad():
                for row in self.prompts:
                    text = tokenizer.apply_chat_template(row["prompt"], tokenize=False,
                                                         add_generation_prompt=True,
                                                         **ct_kwargs)
                    ids = tokenizer(text, return_tensors="pt", truncation=True,
                                    max_length=args.max_length).to(m.device)
                    gen = m.generate(**ids, do_sample=True, temperature=args.health_temperature,
                                     top_p=0.95, max_new_tokens=200, pad_token_id=tokenizer.eos_token_id)
                    txt = tokenizer.decode(gen[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)
                    try:
                        json.loads(txt[txt.index("{"):txt.rindex("}") + 1]); ok += 1
                    except Exception:
                        pass
            m.train()
            rec = {"step": state.global_step, "temperature": args.health_temperature,
                   "parseable": ok, "of": len(self.prompts), "rate": round(ok / max(len(self.prompts), 1), 3)}
            with (out / "health_checks.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec) + "\n")
            log.info(f"HEALTH step {state.global_step}: {ok}/{len(self.prompts)} parseable "
                     f"at T={args.health_temperature}")

    cfg = SFTConfig(
        output_dir=str(out / "checkpoints"),
        num_train_epochs=args.epochs,
        max_steps=8 if args.smoke else -1,
        per_device_train_batch_size=args.batch_size,
        # Dev loss is measured with the same micro-batch as training. TRL's default of 8
        # would make the evaluation pass, not the training step, the peak-memory event.
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_ratio=args.warmup_ratio,
        max_length=args.max_length,
        bf16=on_gpu,
        use_cpu=not on_gpu,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        logging_steps=1 if args.smoke else 10,
        eval_strategy="steps" if do_eval else "no",
        eval_steps=args.eval_steps,
        save_strategy="no" if args.smoke else "steps",
        save_steps=args.save_steps,
        save_total_limit=2,
        seed=args.seed,
        report_to=[],
        completion_only_loss=True,
        # "nll" routes through the model's own forward pass, so any logit rescaling the
        # architecture applies is honoured. "chunked_nll" is TRL's memory-saving default.
        **({"loss_type": "nll"} if use_nll else {}),
    )

    class Status(TrainerCallback):
        """status.json for monitoring: step, epoch, last loss, ETA."""
        def on_log(self, a, state, control, logs=None, **kw):
            if not state.is_world_process_zero:
                return
            elapsed = time.time() - t0
            rate = state.global_step / max(elapsed, 1e-9)
            eta = (state.max_steps - state.global_step) / max(rate, 1e-9)
            write_json(out / "status.json", {
                "step": state.global_step, "max_steps": state.max_steps,
                "epoch": round(state.epoch or 0, 3), "elapsed_s": round(elapsed),
                "eta_s": round(eta), "last_log": {k: v for k, v in (logs or {}).items()},
            })

    trainer = SFTTrainer(
        model=model, args=cfg,
        train_dataset=Dataset.from_list(train_rows),
        eval_dataset=Dataset.from_list(dev_rows) if do_eval else None,
        processing_class=tokenizer, peft_config=peft_config, callbacks=[Status()],
    )
    # A prompt longer than --max-length truncates the completion away entirely. TRL then
    # trains on nothing: the loss is exactly 0.0, no warning is printed, and the run looks
    # healthy until evaluation. Check on a sample of real batches before spending the GPU.
    kept = total = 0
    probe = trainer.get_train_dataloader()
    first_batch = None
    for i, batch in enumerate(probe):
        if i >= 4:
            break
        if first_batch is None:
            first_batch = batch
        lab = batch["labels"]
        kept += int((lab != -100).any(dim=-1).sum())
        total += int(lab.shape[0])
    frac = kept / max(total, 1)
    if frac == 0:
        log.error(f"every example loses its completion to truncation at --max-length "
                  f"{args.max_length}. Nothing would be trained. Raise --max-length.")
        return 2
    if frac < 0.9:
        log.warning(f"only {frac:.0%} of sampled examples keep completion tokens at "
                    f"--max-length {args.max_length}; the rest contribute no loss.")
    log.info(f"supervision check: {frac:.0%} of sampled examples carry completion tokens")
    gpu_mem("after dataloader probe")

    # The authoritative check, and the only one that works for an architecture nobody
    # anticipated: does the loss the trainer is about to optimise match the distribution
    # this model produces at inference? A loss path that reconstructs logits differently --
    # a rescaling field read under the wrong name, a custom kernel -- shows up here as a
    # numeric disagreement, whatever the cause. Greedy evaluation cannot see it later.
    if first_batch is not None:
        try:
            device = next(model.parameters()).device
            probe_batch = {k: v.to(device) for k, v in first_batch.items()
                           if k in ("input_ids", "attention_mask", "labels")}
            ref, actual, ok = loss_path_matches_forward(trainer.model_wrapped or model, probe_batch)
            if ok:
                log.info(f"loss-path check: training loss {actual:.4f} matches the model's own "
                         f"forward pass {ref:.4f} -- training and inference agree")
            else:
                log.error(
                    f"loss-path check FAILED: the trainer would optimise a loss of {actual:.4f} "
                    f"while this model's forward pass gives {ref:.4f} on the same batch. The "
                    f"training objective does not match the distribution inference produces, so "
                    f"the result would decode correctly at greedy and produce junk when sampled. "
                    f"Pass --loss-type nll (which routes through the model's own forward), and "
                    f"see docs/STABILITY.md.")
                return 2
        except Exception as e:      # a probe must never be the reason a real run cannot start
            log.warning(f"loss-path check could not run ({type(e).__name__}: {e}); "
                        f"verify sampling manually with scripts/diag_distributions.py")

    gpu_mem("after loss-path check")
    # The check above runs one un-chunked forward, whose [batch, seq, vocab] logits are the
    # single largest tensor this script ever allocates. Hand that memory back before the
    # first real step rather than carrying it as reserve for the whole run.
    if on_gpu:
        torch.cuda.empty_cache()
        gpu_mem("after empty_cache")
    if args.health_every:
        trainer.add_callback(Health(trainer, (dev_rows or train_rows)[:args.health_prompts]))
    if trainer.is_world_process_zero():
        write_json(out / "train_config.json", {"args": vars(args), "trl_config": cfg.to_dict()})

    ckpts = sorted(glob.glob(str(out / "checkpoints" / "checkpoint-*")),
                   key=lambda p: int(p.rsplit("-", 1)[1]))
    resume = ckpts[-1] if ckpts and not args.smoke else None
    log.info(f"training ... {'resuming from ' + resume if resume else 'from scratch'}")
    result = trainer.train(resume_from_checkpoint=resume)
    gpu_mem("end of training")
    log.info(f"train done in {time.time() - t0:.1f}s: {result.metrics}")

    adapter_dir = out / "adapter"
    trainer.save_model(str(adapter_dir))
    final = dict(result.metrics)
    if do_eval:
        final.update(trainer.evaluate())
        log.info(f"final eval: {final}")
    if trainer.is_world_process_zero():
        tokenizer.save_pretrained(str(adapter_dir))
        write_json(out / "final_metrics.json", final)
        with open(out / "trainer_state.json", "w", encoding="utf-8") as f:
            json.dump(trainer.state.log_history, f, indent=2)
        done.write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), encoding="utf-8")
        log.info(f"adapter saved: {adapter_dir}")
        print(json.dumps({"out": str(out), "adapter": str(adapter_dir),
                          **{k: v for k, v in final.items() if isinstance(v, (int, float))}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
