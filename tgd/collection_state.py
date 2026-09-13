"""What counts as a finished question in a collection run, decided in one place.

Four pieces of code used to answer this independently -- the worker's resume logic, the
parent collector's shard skip, the verifier and the watcher -- and they disagreed:

* The worker resumed only a checkpoint whose status was exactly "running". Anything else,
  including "completed" on a shard with gaps, started a brand-new run directory and re-ran
  every sample, because it looked for `_SUCCESS` only under the new, empty run.
* The parent counted raw `_SUCCESS` markers across all run directories, so duplicate runs
  inflated the count and could make it skip a shard that was still short.
* A marker is written even when the episode record is not (a run whose every model call
  failed), so markers alone overstate progress.

On one GLM collection that meant 1,318 duplicate episodes and $1.77 of a $10 budget spent
re-collecting questions that were already done.

A sample is done when its directory holds `_SUCCESS` and, for a teacher-guidance
collection, the episode record. Done-ness is judged across *every* run directory under a
shard, not just the current one.
"""
from __future__ import annotations

import pathlib
from typing import Set

MARKER = "_SUCCESS"
TG_RECORD = "teacher_guidance_episodes.jsonl"


def is_tg_output(output_dir) -> bool:
    """True once any teacher-guidance episode record exists under this output dir."""
    d = pathlib.Path(output_dir)
    return d.exists() and next(d.rglob(TG_RECORD), None) is not None


def sample_done(sample_dir, require_record: bool) -> bool:
    s = pathlib.Path(sample_dir)
    if not (s / MARKER).exists():
        return False
    return (s / TG_RECORD).exists() if require_record else True


def completed_on_disk(output_dir, dataset_name: str) -> Set[str]:
    """Sample names finished in ANY run under output_dir, for one dataset subdirectory."""
    d = pathlib.Path(output_dir)
    if not d.is_dir():
        return set()
    need = is_tg_output(d)
    done: Set[str] = set()
    for run in d.iterdir():
        sd = run / dataset_name
        if not sd.is_dir():
            continue
        for sample in sd.glob("sample_*"):
            if sample.is_dir() and sample_done(sample, need):
                done.add(sample.name)
    return done


def unique_done(output_dir) -> int:
    """Distinct finished samples under output_dir, however many runs repeated them."""
    d = pathlib.Path(output_dir)
    if not d.exists():
        return 0
    need = is_tg_output(d)
    names = set()
    for marker in d.rglob(MARKER):
        s = marker.parent
        if sample_done(s, need):
            names.add((s.parent.name, s.name))
    return len(names)
