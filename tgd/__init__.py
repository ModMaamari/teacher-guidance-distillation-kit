"""tgd -- teacher-guidance distillation toolkit (library code shared by scripts/).

Importing this package puts the project root on ``sys.path`` so ``agentsim`` (the
simulation harness) resolves regardless of the working directory, and makes stdout able
to carry the characters the scripts print (``tgd.console``).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Console output carries set notation and typographic marks; a console that cannot encode
# them must degrade, not abort a run. See tgd/console.py.
from tgd import console as _console  # noqa: E402

_console.enable()

DATASETS = ["hotpotqa", "2wikimultihopqa", "musique", "strategyqa"]
