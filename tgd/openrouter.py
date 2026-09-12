"""OpenRouter request options, in one place.

Routing and reasoning were built independently in the client and in the pre-flight check,
and they drifted: the check kept asking to disable reasoning after the client had learned
that some models refuse it, so the check failed with HTTP 400 and would have aborted the
collection job it exists to protect. Both now call these helpers.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

#: Values ``OPENROUTER_REASONING`` accepts.
OFF = ("off", "0", "false", "none")
EFFORTS = ("minimal", "low", "medium", "high")


def provider_payload(only: Optional[str]) -> Optional[Dict[str, Any]]:
    """Pin routing to one or more upstream providers, or None to let OpenRouter choose.

    ``allow_fallbacks`` is False on purpose: without it OpenRouter silently reroutes on
    error, and a long run would mix backends with different prices and different sampling
    behaviour partway through a dataset.
    """
    names = [p.strip() for p in (only or "").split(",") if p.strip()]
    if not names:
        return None
    return {"only": names, "allow_fallbacks": False}


def reasoning_payload(mode: Optional[str]) -> Optional[Dict[str, Any]]:
    """Translate a reasoning mode into the request field, or None for the model default.

    ``off`` is a request, not a guarantee: glm-5.3-flash answers 400 "Reasoning is
    mandatory for this endpoint and cannot be disabled" on every provider that serves it,
    so ``low`` is the cheapest setting such a model actually allows. Reasoning tokens bill
    at the output rate, and ``exclude`` only hides them from the response -- they are still
    generated and still charged.
    """
    m = (mode or "").strip().lower()
    if m in OFF:
        return {"enabled": False}
    if m in EFFORTS:
        return {"effort": m}
    if m == "exclude":
        return {"exclude": True}
    return None
