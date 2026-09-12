"""A self-reordering provider ladder for OpenRouter.

Pinning one provider fails badly on a long run: DeepInfra served 3,487 episodes and then
rate-limited us out twice, ~90 minutes each time, and each cutoff meant stopping, pruning
losses and switching by hand. A ladder tries the healthiest provider first and steps down
on failure, so a throttled provider costs one request instead of a run.

Health is persisted, so a provider that misbehaves is demoted for *later* calls and later
runs, not just the current one -- the point of the ladder is that it learns. Failures decay
with a half-life, so a provider that recovers climbs back on its own rather than being
blacklisted forever.

The collector runs one process per shard, so state lives in a file and is written
atomically. Concurrent writers may lose an update; that is fine, the score is a hint and a
missed increment costs nothing.
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import random
import tempfile
import time
from typing import Dict, List

#: Default order, best-first, before any health is known.
#: Wafer is deliberately absent: measured at 2,077 output tokens and 243 s per call,
#: about 5x the cost and 30x the latency of the others. Because an untried provider
#: scores zero it would outrank a working one after a single blip, and a stretch on
#: it could drain the remaining credit.
DEFAULT_LADDER = ("DeepInfra", "Relace", "Morph")

#: A failure's weight halves after this long, so a recovered provider climbs back.
HALF_LIFE_S = float(os.environ.get("PROVIDER_HALF_LIFE_S", str(30 * 60)))

#: Where health is kept. Per project, not per run, so it survives restarts.
STATE_PATH = pathlib.Path(os.environ.get(
    "PROVIDER_STATE_PATH", "runs/provider_health.json"))


def ladder() -> List[str]:
    raw = os.environ.get("PROVIDER_LADDER", "")
    names = [p.strip() for p in raw.split(",") if p.strip()]
    return names or list(DEFAULT_LADDER)


def _load() -> Dict[str, dict]:
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save(state: Dict[str, dict]) -> None:
    try:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(STATE_PATH.parent), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2, sort_keys=True)
        os.replace(tmp, STATE_PATH)          # atomic; a lost race costs one update
    except Exception:
        pass


def _decayed(entry: dict, now: float) -> float:
    """Failure weight, halved every HALF_LIFE_S since it was last updated."""
    score = float(entry.get("score", 0.0))
    age = max(now - float(entry.get("updated", now)), 0.0)
    return score * math.pow(0.5, age / HALF_LIFE_S) if score else 0.0


def order(now: float | None = None) -> List[str]:
    """The ladder, healthiest first.

    Ties keep the configured order, so with no history this is exactly the ladder as
    written. A small jitter breaks ties between equally-sick providers, which stops every
    one of sixteen workers from stampeding the same second choice.
    """
    now = now or time.time()
    state = _load()
    base = ladder()
    def key(p: str):
        e = state.get(p) or {}
        return (round(_decayed(e, now), 3), base.index(p), random.random() * 0.001)
    return sorted(base, key=key)


def record(provider: str, ok: bool, *, weight: float = 1.0) -> None:
    """Note an outcome. Failures add weight; a success halves what is outstanding."""
    now = time.time()
    state = _load()
    e = state.get(provider) or {}
    score = _decayed(e, now)
    if ok:
        score *= 0.5
        # Recovery has to complete, or a provider that is working again never regains its
        # rung: an untried provider scores exactly 0, so any residue keeps a healed one
        # below it forever. Below this floor, treat it as healed.
        if score < 0.05:
            score = 0.0
        e["ok"] = int(e.get("ok", 0)) + 1
    else:
        score += weight
        e["fail"] = int(e.get("fail", 0)) + 1
        e["last_fail"] = now
    e["score"] = round(score, 4)
    e["updated"] = now
    state[provider] = e
    _save(state)


def summary() -> str:
    now = time.time()
    state = _load()
    rows = []
    for i, p in enumerate(order(now)):
        e = state.get(p) or {}
        rows.append(f"  {i + 1}. {p:<12} score {_decayed(e, now):6.2f}  "
                    f"ok {e.get('ok', 0):>6}  fail {e.get('fail', 0):>5}")
    return "\n".join(rows) or "  (no providers configured)"
