"""Make stdout/stderr able to carry the characters these scripts actually print.

Several scripts print set notation and typographic marks -- ``qid∩=0``, ``Δ pts``, ``—``.
On a console whose encoding cannot represent them (the Windows default code page is
cp1252) ``print`` raises ``UnicodeEncodeError``, and the failure lands wherever the first
such character happens to be. ``scripts/check_leakage.py`` printed its per-split lines
*before* writing ``leakage_report.json``, so ``make data`` died after minutes of work with
a traceback that said nothing about encodings.

``enable()`` switches the streams to UTF-8 where the platform allows it and, failing that,
to ``errors="replace"`` on the existing encoding -- so output degrades to ``?`` instead of
taking the process down. It is called on ``import tgd``; nothing else has to remember.
"""
from __future__ import annotations

import sys

_PROBE = "∩≈—Δ✓"
_done = False


def _can_encode(stream) -> bool:
    enc = getattr(stream, "encoding", None)
    if not enc:
        return False
    try:
        _PROBE.encode(enc)
        return True
    except (LookupError, UnicodeEncodeError):
        return False


def enable() -> bool:
    """Returns True if a stream had to be reconfigured. Safe to call repeatedly."""
    global _done
    if _done:
        return False
    _done = True
    changed = False
    for stream in (sys.stdout, sys.stderr):
        if stream is None or _can_encode(stream):
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:                    # captured/replaced stream: leave it alone
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
            changed = True
        except Exception:                          # noqa: BLE001 -- last resort, never fatal
            try:
                reconfigure(errors="replace")
                changed = True
            except Exception:                      # noqa: BLE001
                pass
    return changed
