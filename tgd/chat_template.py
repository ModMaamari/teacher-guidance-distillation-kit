"""Make the prompt a student is trained to continue identical to the one inference hands it.

Training renders ``prompt + completion`` through the chat template and supervises the
completion tokens. Inference renders ``prompt`` with ``add_generation_prompt=True`` and asks
the model to continue. Those two renderings are *assumed* to share a prefix. For reasoning
models they do not, and nothing in a training run says so.

granite-4.2-3b is the worked example. Its template opens a thinking block in the generation
prompt, but folds an empty one into a completed assistant turn::

    generation prompt   ...<|im_start|>assistant\\n<think>\\n
    prompt + completion ...<|im_start|>assistant\\n<think></think>{"thought": ...

So the student is trained to emit its JSON action straight after ``<think></think>`` and
then, at evaluation, is handed ``<think>\\n`` -- an open channel inviting chain-of-thought.
It duly writes prose, and a step that spends its whole generation budget reasoning never
emits a parseable action. Measured on the untrained student here: 0 of 300 outputs began
with a JSON object and 0 of 100 episodes ever produced a valid ``finish``.

The check is exact and needs no per-model knowledge: **the full rendering must start with
the generation-prompt rendering.** When it does not, ``alignment_kwargs`` looks for a chat
template keyword that makes it so -- granite and Qwen spell it ``enable_thinking=False``,
which renders ``<think></think>`` in the generation prompt too. Callers pass the result
wherever they render, and train and eval agree by construction.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

#: Keywords chat templates use for "do not open a reasoning block", most common first.
CANDIDATE_KWARGS: Tuple[Dict[str, Any], ...] = (
    {"enable_thinking": False},
    {"thinking": False},
    {"reasoning": False},
    {"add_thinking": False},
)

#: Reasoning marker pairs, used only to name what went wrong in a log line.
REASONING_MARKERS = (
    ("<think>", "</think>"),
    ("<reasoning>", "</reasoning>"),
    ("<|thinking|>", "<|/thinking|>"),
    ("<|begin_of_thought|>", "<|end_of_thought|>"),
)

PROBE_PROMPT: List[Dict[str, str]] = [{"role": "user", "content": "probe"}]
PROBE_COMPLETION: List[Dict[str, str]] = [{"role": "assistant", "content": '{"probe": 1}'}]


def render_prompt(tokenizer, messages: Optional[Sequence[Dict[str, str]]] = None, **kwargs) -> str:
    """What inference will ask the model to continue, or ``""`` if it cannot be rendered."""
    try:
        return tokenizer.apply_chat_template(
            list(messages or PROBE_PROMPT), tokenize=False, add_generation_prompt=True, **kwargs)
    except Exception:                       # noqa: BLE001 -- a probe never breaks a run
        return ""


def render_full(tokenizer, prompt: Optional[Sequence[Dict[str, str]]] = None,
                completion: Optional[Sequence[Dict[str, str]]] = None, **kwargs) -> str:
    """What training renders and supervises."""
    try:
        return tokenizer.apply_chat_template(
            list(prompt or PROBE_PROMPT) + list(completion or PROBE_COMPLETION),
            tokenize=False, **kwargs)
    except Exception:                       # noqa: BLE001
        return ""


def aligned(tokenizer, prompt=None, completion=None, **kwargs) -> bool:
    """Does the trained rendering begin with the rendering inference produces?"""
    p = render_prompt(tokenizer, prompt, **kwargs)
    full = render_full(tokenizer, prompt, completion, **kwargs)
    return bool(p) and bool(full) and full.startswith(p)


def alignment_kwargs(tokenizer, prompt=None, completion=None) -> Dict[str, Any]:
    """Chat-template keywords that make training and inference render the same prefix.

    ``{}`` when none are needed *and* when none of the candidates work -- callers should
    re-check with :func:`aligned` and say something rather than train through a mismatch.
    """
    if aligned(tokenizer, prompt, completion):
        return {}
    for candidate in CANDIDATE_KWARGS:
        if aligned(tokenizer, prompt, completion, **candidate):
            return dict(candidate)
    return {}


def divergence(tokenizer, prompt=None, completion=None, **kwargs) -> Optional[str]:
    """The tail of the generation prompt that the trained rendering does not share."""
    p = render_prompt(tokenizer, prompt, **kwargs)
    full = render_full(tokenizer, prompt, completion, **kwargs)
    if not p or not full or full.startswith(p):
        return None
    common = 0
    for a, b in zip(p, full):
        if a != b:
            break
        common += 1
    shared = p[max(0, common - 24):common]
    return (f"the two renderings agree up to {shared!r}, then the generation prompt has "
            f"{p[common:]!r} while training has {full[common:common + 24]!r}")


def opens_reasoning(text: str) -> Optional[str]:
    """The reasoning opener left unclosed in ``text``, for diagnostics."""
    for opener, closer in REASONING_MARKERS:
        if text.count(opener) > text.count(closer):
            return opener
    return None


def describe(tokenizer, kwargs: Optional[Dict[str, Any]] = None,
             prompt=None, completion=None) -> str:
    """One log line: whether the two renderings agree, and what was done about it."""
    if aligned(tokenizer, prompt, completion):
        return "chat template: training and inference render the same prompt prefix"
    if kwargs and aligned(tokenizer, prompt, completion, **kwargs):
        marker = opens_reasoning(render_prompt(tokenizer, prompt))
        because = f" (its generation prompt opens {marker})" if marker else ""
        return (f"chat template: inference and training rendered different prompts{because}; "
                f"passing {kwargs} so they agree")
    return f"chat template: MISMATCH -- {divergence(tokenizer, prompt, completion, **(kwargs or {}))}"
