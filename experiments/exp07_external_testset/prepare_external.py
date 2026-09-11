#!/usr/bin/env python3
"""Convert a simple QA file into the kit's dataset format, and validate the result.

Input: one JSON object per line with at least

    {"question": "...", "answer": "...", "documents": [{"title": "...", "text": "..."}]}

Aliases accepted: query/q for question, gold/gold_answer/a for answer, docs/context for
documents; a document may be a bare string or a [title, text] pair.

Output: data/questions/<name>/<name>_{questions,corpus}.jsonl.gz plus a manifest, matching
what eval.py and the sbatch wrappers expect.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import pathlib
import sys

Q_KEYS = ("question", "query", "q")
A_KEYS = ("answer", "gold_answer", "gold", "a")
D_KEYS = ("documents", "docs", "context", "paragraphs")


def pick(row: dict, keys: tuple[str, ...]):
    for k in keys:
        if row.get(k) not in (None, "", []):
            return row[k]
    return None


def norm_docs(raw) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for d in raw or []:
        if isinstance(d, dict):
            out.append((str(d.get("title", "")), str(d.get("text") or d.get("content") or "")))
        elif isinstance(d, (list, tuple)) and len(d) >= 2:
            t = d[1]
            out.append((str(d[0]), " ".join(t) if isinstance(t, list) else str(t)))
        elif isinstance(d, str):
            out.append(("", d))
    return [(t, x) for t, x in out if x.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--name", required=True, help="dataset name, e.g. bamboogle")
    ap.add_argument("--out-root", default="data/questions")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    src = pathlib.Path(a.input)
    if not src.exists():
        print(f"!! {src} not found", file=sys.stderr)
        return 1
    out = pathlib.Path(a.out_root) / a.name
    out.mkdir(parents=True, exist_ok=True)

    qs, docs, skipped = [], [], 0
    op = gzip.open if src.suffix == ".gz" else open
    with op(src, "rt", encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            if a.limit and len(qs) >= a.limit:
                break
            row = json.loads(line)
            q, ans = pick(row, Q_KEYS), pick(row, A_KEYS)
            if isinstance(ans, dict):
                ans = ans.get("answer")
            dd = norm_docs(pick(row, D_KEYS))
            if not q or ans in (None, "") or not dd:
                skipped += 1
                continue
            qid = str(row.get("id") or hashlib.sha1(
                f"{a.name}:{q}".encode()).hexdigest()[:24])
            qs.append({"id": qid, "query": str(q), "answer": str(ans), "type": "external",
                       "level": "unknown", "source": a.name, "split": "test",
                       "num_hops": int(row.get("num_hops") or 2),
                       "answer_type": "span", "gold_granularity": "document",
                       "gold": {"answer": str(ans), "answer_aliases": []},
                       "retrieval_scope": {"backend": "local", "qid": qid}})
            for j, (title, text) in enumerate(dd):
                docs.append({"doc_id": f"{qid}::doc{j}", "qid": qid, "title": title,
                             "text": text, "sentences": [s.strip() for s in text.split(". ") if s.strip()],
                             "is_gold_doc": bool(row.get("gold_doc_index") == j),
                             "gold_sent_ids": [], "source": a.name, "split": "test"})

    if not qs:
        print(f"!! nothing usable in {src} ({skipped} rows skipped)", file=sys.stderr)
        return 1

    qp = out / f"{a.name}_questions.jsonl.gz"
    cp = out / f"{a.name}_corpus.jsonl.gz"
    for path, rows in ((qp, qs), (cp, docs)):
        with gzip.open(path, "wt", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    (out / f"{a.name}_manifest.json").write_text(json.dumps(
        {"name": a.name, "questions": len(qs), "documents": len(docs),
         "skipped": skipped, "source_file": str(src)}, indent=2), encoding="utf-8")

    per_q = len(docs) / len(qs)
    print(f"wrote {qp}  ({len(qs)} questions)")
    print(f"wrote {cp}  ({len(docs)} documents, {per_q:.1f} per question)")
    if skipped:
        print(f"skipped {skipped} rows missing a question, answer or documents")
    if per_q < 2:
        print("!! fewer than 2 documents per question -- retrieval will be trivial and the")
        print("   comparison to the other datasets will not be like-for-like")
    print(f"\nevaluate with:  EXTERNAL_DS={a.name} bash run.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
