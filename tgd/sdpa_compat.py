"""Keep scaled-dot-product attention on a memory-efficient kernel.

Transformers asks PyTorch to handle grouped-query attention itself (``enable_gqa=True``)
whenever there is no attention mask, instead of repeating the key/value heads. That is the
right call where a fused kernel implements it. Where it is not implemented, PyTorch does not
fail and does not warn -- it falls back to the *math* backend, which materialises the full
``[batch, heads, seq, seq]`` score matrix.

The cost is invisible in any correctness check and enormous in practice. Measured here on
one attention op, 40 heads x 2,560 tokens, bfloat16:

    memory-efficient kernel   0.13 GiB
    math backend              4.03 GiB

At 8 GB that is the difference between training and paging to host memory, which presents
purely as a GPU running five times slower than it should.

``apply()`` makes transformers repeat the key/value heads instead, which puts the same
computation back on the memory-efficient kernel. It is a no-op on builds that do implement
GQA in a fused kernel: the probe below only disables the flag when the kernel is genuinely
missing. Call it before loading a model.
"""
from __future__ import annotations

_applied = False


def _gqa_kernel_available() -> bool:
    """Does a non-math SDPA kernel accept enable_gqa on this build? Ask, do not assume."""
    import torch
    from torch.nn.attention import SDPBackend, sdpa_kernel

    if not torch.cuda.is_available():
        return True                                   # nothing to fix off-GPU
    q = torch.zeros(1, 4, 8, 16, device="cuda", dtype=torch.bfloat16)
    kv = torch.zeros(1, 2, 8, 16, device="cuda", dtype=torch.bfloat16)
    try:
        with sdpa_kernel([SDPBackend.EFFICIENT_ATTENTION, SDPBackend.FLASH_ATTENTION]):
            torch.nn.functional.scaled_dot_product_attention(q, kv, kv, is_causal=True,
                                                             enable_gqa=True)
        return True
    except RuntimeError:
        return False
    finally:
        del q, kv


def apply(log=None) -> bool:
    """Returns True if the fallback was disabled (i.e. this build needed the fix)."""
    global _applied
    if _applied:
        return False
    _applied = True
    try:
        from transformers.integrations import sdpa_attention
    except ImportError:
        return False
    if _gqa_kernel_available():
        return False
    sdpa_attention.use_gqa_in_sdpa = lambda attention_mask, key, value: False
    msg = ("SDPA: this torch build has no fused grouped-query kernel, so transformers' "
           "enable_gqa path would silently select the math backend and its full "
           "[heads, seq, seq] score matrix. Repeating key/value heads instead.")
    (log.info if log else print)(msg)
    return True
