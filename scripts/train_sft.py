#!/usr/bin/env python
"""LoRA SFT of a student on guidance-as-internal-thought examples (TRL SFTTrainer).

Data: prompt/completion conversational JSONL as written by ``scripts/build_splits.py``
(``{"prompt": [messages], "completion": [message], "metadata": {...}}``). TRL applies
the model's own chat template and computes the loss on completion tokens only, so the
model learns to GENERATE the ``teacher_guidance`` block + thought + action and is never
trained on the (long) prompt tokens.

**Keeping the student samplable.** Plain SFT can leave a model that is excellent at greedy
decoding and unusable when sampled: it keeps ranking the right token first while spreading its
probability mass across the vocabulary, so greedy (which needs only the ranking) is fine and
sampling (which needs calibrated probabilities) draws junk. Measured on this project's own
student, the effect was total -- 61% cover at temperature 0 and 0% with 899/900 invalid actions
at 0.3. See docs/STABILITY.md.

``--kl-coef`` guards against that by pulling every completion token toward the frozen base
model's own distribution. The base distribution comes from the SAME weights with the LoRA
adapter switched off, so it costs one extra forward pass and no extra parameters.
``--kl-direction`` chooses what is penalised:

* ``reverse`` (default) -- KL(student || base), mode-seeking: penalises probability mass where
  the base model has none, which is exactly the junk tail that breaks sampling, while leaving
  the student free to sharpen on the correct token.
* ``forward`` -- KL(base || student), mass-covering: penalises the student for withdrawing mass
  from anything the base found plausible. That fights the cross-entropy directly; measured at
  coefficient 0.1 it fixed the calibration completely and cost most of the task (61% -> 29%
  cover). Use it only deliberately.

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
import time
from pathlib import Path

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # project root -> import tgd/agentsim

import tgd  # noqa: F401
from tgd.io import load_jsonl
from tgd.logging_utils import setup_logger, write_json


def kl_term(student_logits, base_logits, direction: str, target_ids=None):
    """KL between the student's and the frozen base's next-token distributions.

    `forward` is KL(base || student): mass-covering, it pushes the student to keep
    probability everywhere the base has some, which directly opposes the cross-entropy
    term and in our runs cost most of the task gain. `reverse` is KL(student || base):
    mode-seeking, it only penalises mass the student puts where the base has none, which
    is exactly the flat tail that makes a fine-tuned model unsamplable. See docs/STABILITY.md.

    Pass `target_ids` to exclude the supervised token itself, so the KL shapes the tail
    without fighting the label.
    """
    import torch    # deferred so --help stays instant

    if direction not in ("forward", "reverse"):
        raise ValueError(f"kl direction must be 'forward' or 'reverse', got {direction!r}")
    if target_ids is not None:
        rows = torch.arange(student_logits.shape[0], device=student_logits.device)
        student_logits = student_logits.clone()
        base_logits = base_logits.clone()
        student_logits[rows, target_ids] = -1e4
        base_logits[rows, target_ids] = -1e4
    log_s = torch.log_softmax(student_logits, dim=-1)
    log_b = torch.log_softmax(base_logits, dim=-1)
    # F.kl_div(input=log q, target=log p) computes KL(p || q), so the base goes in the
    # target slot for forward and in the input slot for reverse.
    if direction == "forward":
        return torch.nn.functional.kl_div(log_s, log_b, log_target=True, reduction="batchmean")
    return torch.nn.functional.kl_div(log_b, log_s, log_target=True, reduction="batchmean")


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
    ap.add_argument("--kl-coef", type=float, default=0.0,
                    help="strength of the KL toward the frozen base (0 = plain SFT). 0.03-0.1 is the "
                         "range explored here; higher values trade task performance for calibration")
    ap.add_argument("--kl-direction", choices=["reverse", "forward"], default="reverse",
                    help="reverse = KL(student||base), mode-seeking (recommended); "
                         "forward = KL(base||student), mass-covering (fights the task objective)")
    ap.add_argument("--kl-mask-target", action="store_true",
                    help="exclude the target token from the KL, so only the shape of the alternatives "
                         "is regularised and confidence on the correct token is entirely free")
    ap.add_argument("--kl-max-positions", type=int, default=512,
                    help="cap on completion positions used for the KL each step (bounds memory)")
    ap.add_argument("--health-every", type=int, default=0,
                    help="every N steps, sample --health-prompts held-out prompts at "
                         "--health-temperature and log how many parse as JSON (0 = off)")
    ap.add_argument("--health-prompts", type=int, default=8)
    ap.add_argument("--health-temperature", type=float, default=0.7)
    ap.add_argument("--limit", type=int, default=None, help="cap training examples")
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
    limit = 64 if args.smoke else args.limit
    train_rows = [{"prompt": r["prompt"], "completion": r["completion"]} for r in load_jsonl(args.train_file, limit)]
    dev_rows = ([{"prompt": r["prompt"], "completion": r["completion"]} for r in load_jsonl(args.dev_file, 32 if args.smoke else None)]
                if args.dev_file else [])
    log.info(f"loaded {len(train_rows)} train / {len(dev_rows)} dev examples")

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    # bf16 needs a GPU. Falling back to fp32 on CPU keeps `--smoke` usable as a
    # pipeline check on a laptop; real training always runs on a GPU.
    on_gpu = torch.cuda.is_available()
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16 if on_gpu else torch.float32)
    log.info(f"model loaded in {time.time() - t0:.1f}s | cuda={torch.cuda.is_available()} "
             f"gpus={torch.cuda.device_count()}")

    peft_config = LoraConfig(r=args.lora_r, lora_alpha=args.lora_alpha, lora_dropout=args.lora_dropout,
                             target_modules="all-linear", task_type="CAUSAL_LM")
    do_eval = bool(dev_rows) and not args.smoke

    class CalibratedSFTTrainer(SFTTrainer):
        """SFT loss plus a KL toward the adapter-disabled base on completion tokens."""

        def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
            loss, outputs = super().compute_loss(model, inputs, return_outputs=True,
                                                 num_items_in_batch=num_items_in_batch)
            labels = inputs.get("labels")
            if args.kl_coef <= 0 or labels is None or getattr(outputs, "logits", None) is None:
                return (loss, outputs) if return_outputs else loss
            shift_labels = labels[..., 1:]
            mask = shift_labels != -100
            if not bool(mask.any()):
                return (loss, outputs) if return_outputs else loss
            idx = mask.nonzero(as_tuple=False)
            if idx.shape[0] > args.kl_max_positions:      # bound memory: sample positions
                idx = idx[torch.randperm(idx.shape[0], device=idx.device)[:args.kl_max_positions]]
            rows_i, cols_i = idx[:, 0], idx[:, 1]
            tgt = shift_labels[rows_i, cols_i]
            unwrapped = self.accelerator.unwrap_model(model)
            with torch.no_grad():
                with unwrapped.disable_adapter():
                    base_logits = unwrapped(input_ids=inputs["input_ids"],
                                            attention_mask=inputs.get("attention_mask")).logits[..., :-1, :]
                base_sel = base_logits[rows_i, cols_i].float()
            stud_sel = outputs.logits[..., :-1, :][rows_i, cols_i].float()
            kl = kl_term(stud_sel, base_sel, args.kl_direction,
                         target_ids=tgt if args.kl_mask_target else None)
            if not torch.isfinite(kl):                   # never let one bad batch poison a run
                log.warning(f"non-finite KL at step {self.state.global_step}; skipped this step")
                return (loss, outputs) if return_outputs else loss
            with torch.no_grad():
                p = torch.softmax(stud_sel, dim=-1)
                self._last_kl = float(kl)
                self._last_entropy = float(-(p * torch.log(p.clamp_min(1e-12))).sum(-1).mean())
                self._last_top1 = float(p.max(-1).values.mean())
            return ((loss + args.kl_coef * kl, outputs) if return_outputs
                    else loss + args.kl_coef * kl)

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
                                                         add_generation_prompt=True)
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
            with (out / "health_checks.jsonl").open("a") as fh:
                fh.write(json.dumps(rec) + "\n")
            log.info(f"HEALTH step {state.global_step}: {ok}/{len(self.prompts)} parseable "
                     f"at T={args.health_temperature}")

    cfg = SFTConfig(
        output_dir=str(out / "checkpoints"),
        num_train_epochs=args.epochs,
        max_steps=8 if args.smoke else -1,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_ratio=args.warmup_ratio,
        max_length=args.max_length,
        bf16=on_gpu,
        use_cpu=not on_gpu,
        gradient_checkpointing=True,
        logging_steps=1 if args.smoke else 10,
        eval_strategy="steps" if do_eval else "no",
        eval_steps=args.eval_steps,
        save_strategy="no" if args.smoke else "steps",
        save_steps=args.save_steps,
        save_total_limit=2,
        seed=args.seed,
        report_to=[],
        completion_only_loss=True,
        # TRL's default chunked cross-entropy returns no logits, which the KL term needs.
        **({"loss_type": "nll"} if args.kl_coef > 0 else {}),
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
                "kl": {k: getattr(trainer, f"_last_{k}", None)
                       for k in ("kl", "entropy", "top1")} if args.kl_coef > 0 else None,
            })

    trainer_cls = CalibratedSFTTrainer if args.kl_coef > 0 else SFTTrainer
    trainer = trainer_cls(
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
    for i, batch in enumerate(probe):
        if i >= 4:
            break
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

    if args.health_every:
        trainer.add_callback(Health(trainer, (dev_rows or train_rows)[:args.health_prompts]))
    if trainer.is_world_process_zero():
        write_json(out / "train_config.json", {"args": vars(args), "trl_config": cfg.to_dict()})

    ckpts = sorted(glob.glob(str(out / "checkpoints" / "checkpoint-*")),
                   key=lambda p: int(p.rsplit("-", 1)[1]))
    resume = ckpts[-1] if ckpts and not args.smoke else None
    log.info(f"training ... {'resuming from ' + resume if resume else 'from scratch'}"
             + (f" | KL {args.kl_direction} coef={args.kl_coef} mask_target={args.kl_mask_target}"
                if args.kl_coef > 0 else " | plain SFT (no KL)"))
    result = trainer.train(resume_from_checkpoint=resume)
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
        with open(out / "trainer_state.json", "w") as f:
            json.dump(trainer.state.log_history, f, indent=2)
        done.write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        log.info(f"adapter saved: {adapter_dir}")
        print(json.dumps({"out": str(out), "adapter": str(adapter_dir),
                          **{k: v for k, v in final.items() if isinstance(v, (int, float))}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
