"""Loading a student model, whatever shape its architecture comes in.

Most instruction-tuned students are plain causal LMs and load through
``AutoModelForCausalLM``. Some are not. A model published as a vision-language or
"conditional generation" architecture is registered under a different auto class and is
**not** in the causal-LM mapping at all, so the obvious call raises before training starts.
Qwen3.5-2B is one: ``Qwen3_5ForConditionalGeneration``, registered under
image-text-to-text. It has a perfectly good text stack underneath, which is what SFT uses.

Those models also nest their language settings under ``config.text_config``, so anything
inspecting the config — vocabulary size, logit rescaling — has to look there instead of at
the top level.

Both facts are handled here so no calling script has to care.
"""
from __future__ import annotations

from typing import Any, Optional

# Auto classes to try, in order. Causal LM first: it is the common case and the most
# specific fit for a text-only student.
_AUTO_CLASSES = ("AutoModelForCausalLM", "AutoModelForImageTextToText",
                 "AutoModelForMultimodalLM", "AutoModelForSeq2SeqLM")


def text_config(config) -> Any:
    """The sub-config carrying the language settings.

    Multimodal architectures keep ``vocab_size``, ``hidden_size`` and any logit rescaling
    under ``config.text_config``; text-only ones keep them at the top level.
    """
    return getattr(config, "text_config", None) or config


def vocab_size(config, tokenizer=None) -> Optional[int]:
    """Width of the output projection, from wherever this architecture keeps it.

    This is the dimension that sizes a logits tensor, so it must never be *under*-estimated:
    a model's embedding matrix is often padded past the tokenizer's length for kernel
    efficiency (one student here: 128,000 in the config against 125,017 tokens). Takes the
    larger of the config and the tokenizer for that reason.
    """
    sizes = []
    for c in (text_config(config), config):
        v = getattr(c, "vocab_size", None)
        if v:
            sizes.append(int(v))
    if tokenizer is not None:
        try:
            sizes.append(len(tokenizer))
        except TypeError:
            pass
    return max(sizes) if sizes else None


def render_chat(tokenizer, messages, close_reasoning: bool = True):
    """Render a chat prompt, closing an open reasoning block if the template opens one.

    Reasoning models end their generation prompt inside a ``<think>`` block, so the first
    token the model generates is the start of its reasoning — not the answer. Any diagnostic
    that inspects the first generated token then measures the wrong position, and reports
    that no probability sits on a valid answer token. That looks exactly like the
    catastrophic miscalibration these tools exist to detect, but it is normal behaviour.

    Most such templates accept ``enable_thinking=False``, which closes the block so the next
    token really is the answer. Returns ``(text, reasoning_open)``; when ``reasoning_open``
    is True the caller could not close it, and answer-token metrics are meaningless for this
    model even though entropy and top-1 remain valid.
    """
    def _render(**kw):
        return tokenizer.apply_chat_template(messages, tokenize=False,
                                             add_generation_prompt=True, **kw)

    text = _render()
    tail = text[-40:]
    opened = "<think>" in tail and "</think>" not in tail
    if opened and close_reasoning:
        for kw in ({"enable_thinking": False}, {"thinking": False}):
            try:
                alt = _render(**kw)
            except Exception:
                continue
            alt_tail = alt[-40:]
            if not ("<think>" in alt_tail and "</think>" not in alt_tail):
                return alt, False
    return text, opened


def load_lm(path: str, dtype=None, device_map=None, **kwargs):
    """Load a student for training or scoring, trying each auto class in turn.

    Returns ``(model, auto_class_name)``. Raises the *first* error if none succeed, since
    that one is about the causal-LM path a reader will expect to have been taken.
    """
    import transformers

    first_error = None
    for name in _AUTO_CLASSES:
        cls = getattr(transformers, name, None)
        if cls is None:
            continue
        try:
            model = cls.from_pretrained(path, dtype=dtype, device_map=device_map, **kwargs)
            return model, name
        except Exception as e:                     # wrong auto class for this architecture
            if first_error is None:
                first_error = e
    raise first_error if first_error else RuntimeError(f"could not load a model from {path}")
