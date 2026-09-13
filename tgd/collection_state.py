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


# (path, mtime_ns, size) -> whether the record file holds at least one non-error episode.
# The parent collector re-checks every shard every 30 s, so re-reading thousands of record
# files each time would be expensive; a file is re-read only when it changes.
_RECORD_OK: dict = {}


def _is_error_episode(ep: dict) -> bool:
    """Same rule consolidation uses (tgd.episodes.is_error)."""
    return str(ep.get("stop_reason", "")).startswith("error") or bool(ep.get("error"))


def record_has_good_episode(record_path) -> bool:
    """True if the episode file holds at least one episode that did not end in error.

    A retried question APPENDS to the same file, so a file can hold an errored attempt
    followed by a good one; any good line is enough.
    """
    import json
    rp = pathlib.Path(record_path)
    try:
        st = rp.stat()
    except OSError:
        return False
    key = (str(rp), st.st_mtime_ns, st.st_size)
    hit = _RECORD_OK.get(key)
    if hit is not None:
        return hit
    ok = False
    try:
        with rp.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    ep = json.loads(line)
                except ValueError:
                    continue
                if isinstance(ep, dict) and not _is_error_episode(ep):
                    ok = True
                    break
    except OSError:
        ok = False
    _RECORD_OK[key] = ok
    return ok


def sample_done(sample_dir, require_record: bool) -> bool:
    """Done = marker present and, for a teacher-guidance collection, an episode that did not
    end in error. An errored episode used to count as done, so the 8.6% of questions whose
    teacher calls failed were never retried."""
    s = pathlib.Path(sample_dir)
    if not (s / MARKER).exists():
        return False
    if not require_record:
        return True
    return record_has_good_episode(s / TG_RECORD)


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
