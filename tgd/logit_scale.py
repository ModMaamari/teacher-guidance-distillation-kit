"""Logit rescaling: one place, because getting it wrong is invisible until you sample.

Some architectures divide their logits by a constant before the softmax — Granite by
``config.logits_scaling`` (10.0), Gemma by ``config.final_logit_softcapping``. The model's
own ``forward()`` applies it, so anything that calls the model normally is correct.

Two things bypass ``forward()`` and must be checked:

1. **TRL's memory-chunked cross-entropy** (``loss_type="chunked_nll"``, its default) computes
   the loss straight from hidden states and applies its own scaling, read from
   ``config.logit_scale``. For a model whose field is named anything else that lookup misses
   and silently defaults to 1.0, so training optimises logits at a different scale than
   inference produces.
2. **A merge that loses the field.** Merging an adapter writes a fresh ``config.json``; if a
   scaling field did not survive, every later inference runs at the wrong scale.

Both are invisible to greedy evaluation. Dividing logits by a constant cannot reorder them,
so the argmax — and therefore greedy accuracy — is *identical* either way. Only sampling
sees it, and it sees it catastrophically: measured here, a student went from 61 % task cover
at greedy to 0 % at temperature 0.3, with 899 of 900 actions invalid.

See ``docs/STABILITY.md`` for the full diagnosis.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

# Fields an architecture may use to rescale logits, and the one TRL's chunked path reads.
SCALING_FIELDS = ("logits_scaling", "logit_scale", "final_logit_softcapping")
TRL_CHUNKED_READS = "logit_scale"

# Above this, the logits tensor alone is a large fraction of a mid-range GPU; the softmax
# needs a second buffer of the same size, so the practical ceiling is roughly half of it.
MAX_LOGIT_TENSOR_GB = 4.0


def scaling_fields(config) -> Dict[str, float]:
    """The rescaling fields this config actually sets to something other than 1.0."""
    found = {}
    for f in SCALING_FIELDS:
        v = getattr(config, f, None)
        if v is not None and v != 1.0:
            found[f] = v
    return found


def chunked_loss_conflict(config) -> Optional[str]:
    """Message if TRL's chunked cross-entropy would train at the wrong logit scale."""
    present = scaling_fields(config)
    if not present or TRL_CHUNKED_READS in present:
        return None      # nothing to rescale, or TRL reads the field itself
    field, value = next(iter(present.items()))
    return (f"this model rescales logits via config.{field}={value}, but TRL's chunked "
            f"cross-entropy reads config.{TRL_CHUNKED_READS} (absent here, so it uses 1.0). "
            f"Training would optimise logits {value}x the ones inference produces.")


def merge_lost_scaling(base_config, merged_config) -> Optional[str]:
    """Message if a merged model dropped or changed a rescaling field the base had."""
    before, after = scaling_fields(base_config), scaling_fields(merged_config)
    lost = {f: v for f, v in before.items() if after.get(f) != v}
    if not lost:
        return None
    field, value = next(iter(lost.items()))
    # Report what the merged config literally holds, not the filtered view: a field set to
    # 1.0 is "lost" for our purposes but saying "None" would send someone hunting a missing
    # key that is actually present.
    actual = getattr(merged_config, field, None)
    return (f"the merged model lost config.{field} (base has {value}, merged has "
            f"{actual!r}). Every inference on it would run at the wrong logit "
            f"scale: greedy would look fine and sampling would produce junk.")


def autoscale_batch(batch_size: int, grad_accum: int, max_length: int, vocab: int):
    """Trade micro-batch for accumulation when the full logit tensor would be too large.

    The chunked path exists to avoid materialising ``[batch, seq, vocab]`` logits; without
    it that tensor is real, and at a typical micro-batch it is large enough to OOM partway
    through an epoch — when the first batch of full-length sequences arrives, not at step 0.

    Returns ``(batch_size, grad_accum, gb)`` with the effective batch preserved. ``gb`` is
    the tensor size at the ORIGINAL micro-batch, for the log line.
    """
    gb = batch_size * max_length * vocab * 4 / 1024 ** 3
    if batch_size > 1 and gb > MAX_LOGIT_TENSOR_GB:
        return 1, grad_accum * batch_size, gb
    return batch_size, grad_accum, gb


def describe(config) -> str:
    """One line for a startup log: what this model does with its logits."""
    present = scaling_fields(config)
    if not present:
        return "logit rescaling: none"
    return "logit rescaling: " + ", ".join(f"config.{f}={v}" for f, v in present.items())
