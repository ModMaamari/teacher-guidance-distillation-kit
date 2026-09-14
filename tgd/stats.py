"""Paired significance tests for two arms answering the same questions."""
from __future__ import annotations

import math
import random
from typing import List


def paired_bootstrap(a: List[int], b: List[int], iters=10000, seed=13):
    """Mean of ``b - a`` over questions with a percentile-bootstrap 95% CI."""
    rnd = random.Random(seed)
    n = len(a)
    diffs = [b[i] - a[i] for i in range(n)]
    obs = sum(diffs) / n
    boots = sorted(sum(diffs[rnd.randrange(n)] for _ in range(n)) / n for _ in range(iters))
    return {"diff": round(obs, 4), "ci95": [round(boots[int(0.025 * iters)], 4), round(boots[int(0.975 * iters) - 1], 4)], "n": n}


def mcnemar_exact(a: List[int], b: List[int]):
    """Exact two-sided McNemar test on the questions where exactly one arm is right."""
    b01 = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    b10 = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    m = b01 + b10
    if m == 0:
        return {"b_wins": 0, "a_wins": 0, "p": 1.0}
    k = min(b01, b10)
    p = min(1.0, 2 * sum(math.comb(m, i) for i in range(k + 1)) / 2 ** m)
    return {"b_wins": b01, "a_wins": b10, "p": round(p, 6)}
