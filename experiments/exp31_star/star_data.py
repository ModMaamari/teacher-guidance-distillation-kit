#!/usr/bin/env python
"""STaR data plumbing (E31): which questions to collect, and how the collections combine.

STaR (Zelikman et al., 2022) trains on the model's own correct attempts plus *rationalizations*:
for every question the model got wrong, it is shown the correct answer as a hint and asked
again; the hinted episodes that end correct are kept, with the hint removed from the training
input. Here an attempt is one unguided agent episode, the hint is a prompt paragraph that
``scripts/collect_episodes.py --answer-hint`` adds, and ``tgd.episode_lib`` strips it and refuses
any hinted step that names the answer before retrieved evidence does.

  questions  write a question directory for a collection: every trainable question
             (``--mode all``) or only those whose episode in ``--episodes`` is not correct
             (``--mode failed``, the questions to rationalize)
  merge      combine an attempt collection with its rationalizations into one episode file
             (a failed attempt is replaced by its rationalization) and report the counts

Only the first ``--per-dataset`` questions of each dataset are considered, the same questions
every other collection in this kit covers; held-out questions are never collected.

    python experiments/exp31_star/star_data.py questions --mode failed \
        --episodes data/episodes_selfdist/episodes.jsonl.gz --out data/questions_star1_rat
    python experiments/exp31_star/star_data.py merge --attempts data/episodes_selfdist/episodes.jsonl.gz \
        --rationalized data/episodes_star1_rat/episodes.jsonl.gz --out data/episodes_star1
"""
from __future__ import annotations

import argparse
import collections
import gzip
import json
import os
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT))

from tgd import DATASETS  # noqa: E402
from tgd.io import corpus_file, question_file, read_jsonl  # noqa: E402
from tgd.splits import pool_of  # noqa: E402


def _episodes(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def _qid(row) -> str:
    """Question files key the id as ``id``; episodes carry it as ``qid``."""
    return str(row.get("qid") or row["id"])


def _correct(ep) -> bool:
    return bool((ep.get("final_metrics") or {}).get("answer_correct"))


def questions(a) -> int:
    solved = set()
    seen = set()
    if a.mode == "failed":
        for ep in _episodes(a.episodes):
            seen.add(str(ep.get("qid")))
            if _correct(ep):
                solved.add(str(ep.get("qid")))
    out = Path(a.out)
    total = 0
    for ds in DATASETS:
        rows = list(read_jsonl(question_file(a.questions, ds), a.per_dataset))
        keep = [r for r in rows if pool_of(_qid(r)) == "trainable"
                and (a.mode == "all" or _qid(r) not in solved)]
        if a.mode == "failed":
            missing = [_qid(r) for r in keep if _qid(r) not in seen]
            if len(missing) > 0.01 * max(len(keep), 1):
                print(f"!! {ds}: {len(missing)} trainable questions have no attempt in {a.episodes}")
                return 1
        d = out / ds
        d.mkdir(parents=True, exist_ok=True)
        with gzip.open(d / f"{ds}_questions.jsonl.gz", "wt", encoding="utf-8") as fh:
            for r in keep:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        link = d / f"{ds}_corpus.jsonl.gz"
        src = corpus_file(a.questions, ds).resolve()
        if link.is_symlink() or link.exists():
            link.unlink()
        os.symlink(src, link)
        print(f"  {ds:<16} {len(keep):>5} of {len(rows)} questions ({a.mode})")
        total += len(keep)
    print(f"wrote {total} questions -> {out}")
    return 0 if total else 1


def merge(a) -> int:
    rat = {}
    for ep in _episodes(a.rationalized):
        ep["star_rationalized"] = True
        rat[str(ep.get("qid"))] = ep
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    c = collections.Counter()
    with gzip.open(out / "episodes.jsonl.gz", "wt", encoding="utf-8") as fh:
        for ep in _episodes(a.attempts):
            q = str(ep.get("qid"))
            if q in rat:                     # a failed attempt, replaced by its rationalization
                c["attempt_replaced"] += 1
                continue
            c["attempt_correct" if _correct(ep) else "attempt_failed_kept"] += 1
            fh.write(json.dumps(ep, ensure_ascii=False) + "\n")
        for q, ep in rat.items():
            c["rationalized_correct" if _correct(ep) else "rationalized_failed"] += 1
            fh.write(json.dumps(ep, ensure_ascii=False) + "\n")
    stats = dict(c)
    (out / "merge_stats.json").write_text(json.dumps(stats, indent=1), encoding="utf-8")
    print(json.dumps(stats, indent=1))
    return 0 if c["rationalized_correct"] else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("questions")
    q.add_argument("--mode", choices=["all", "failed"], required=True)
    q.add_argument("--episodes", help="attempt episodes whose failures to collect (--mode failed)")
    q.add_argument("--questions", default="data/questions")
    q.add_argument("--per-dataset", type=int, default=2000)
    q.add_argument("--out", required=True)
    m = sub.add_parser("merge")
    m.add_argument("--attempts", required=True)
    m.add_argument("--rationalized", required=True)
    m.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.cmd == "questions" and a.mode == "failed" and not a.episodes:
        ap.error("--mode failed needs --episodes")
    return questions(a) if a.cmd == "questions" else merge(a)


if __name__ == "__main__":
    sys.exit(main())
