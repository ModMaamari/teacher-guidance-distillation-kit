#!/usr/bin/env python
"""Convert two external multi-hop benchmarks into the kit's question/corpus format.

The kit's agent retrieves with BM25 over *the current question's own documents*, so a dataset is
usable here only if every question comes with a candidate document set. Neither benchmark ships one
directly, so this builds it:

  multihoprag  MultiHop-RAG (news articles, 609 documents, 2,556 queries). A question's candidates
               are the articles its evidence cites plus distractors drawn from the same corpus,
               preferring the same news category so the distractors are plausible. Unanswerable
               queries (``null_query``) are dropped: the agent protocol assumes an answer exists.
  framesqa     FRAMES (Wikipedia, 824 questions). A question's candidates are the Wikipedia
               articles it links plus distractors drawn from other questions' articles. Article
               text comes from the Wikipedia API and is cached under data/_cache/wiki.

Both write data/questions/<ds>/<ds>_{questions,corpus}.jsonl.gz and an evaluation file at
data/splits/test/newtest_<ds>_questions.jsonl. Documents are truncated to keep episodes close in
size to the kit's existing datasets, and every question keeps its gold documents marked, so doc
recall stays measurable.

    python experiments/exp27_new_benchmarks/build_datasets.py multihoprag --limit 600
    python experiments/exp27_new_benchmarks/build_datasets.py framesqa --limit 600
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import random
import re
import sys
import time
from pathlib import Path
from urllib.parse import unquote

import httpx

KIT = Path(__file__).resolve().parents[2]
RAW = KIT / "data" / "_raw"
CACHE = KIT / "data" / "_cache" / "wiki"
DOCS_PER_QUESTION = 10
MAX_DOC_CHARS = 6000
WIKI = "https://en.wikipedia.org/w/api.php"


def sentences_of(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", text.strip())
    return [p.strip() for p in parts if p.strip()]


def write_dataset(ds: str, rows: list[dict], docs: dict[str, list[dict]], limit: int | None) -> None:
    """rows: question records without doc wiring; docs: qid -> [{title, text, gold}]."""
    if limit:
        rows = rows[:limit]
    keep = {r["id"] for r in rows}
    qdir = KIT / "data" / "questions" / ds
    qdir.mkdir(parents=True, exist_ok=True)
    n_docs = n_gold = 0
    with gzip.open(qdir / f"{ds}_corpus.jsonl.gz", "wt", encoding="utf-8") as fh:
        for qid, ds_docs in docs.items():
            if qid not in keep:
                continue
            for i, d in enumerate(ds_docs):
                text = d["text"][:MAX_DOC_CHARS].strip()
                sents = sentences_of(text)
                n_docs += 1
                n_gold += int(d["gold"])
                fh.write(json.dumps({
                    "doc_id": f"{qid}::doc{i}", "qid": qid, "title": d["title"], "text": text,
                    "sentences": sents, "is_gold_doc": bool(d["gold"]),
                    "gold_sent_ids": list(range(len(sents))) if d["gold"] else [],
                    "source": ds, "split": "test"}, ensure_ascii=False) + "\n")
    out_rows = []
    for r in rows:
        mine = docs[r["id"]]
        ids = [f"{r['id']}::doc{i}" for i in range(len(mine))]
        gold_ids = [f"{r['id']}::doc{i}" for i, d in enumerate(mine) if d["gold"]]
        r = {**r, "source": ds, "split": "test",
             "gold": {**r["gold"], "gold_doc_ids": gold_ids},   # tgd reads gold.gold_doc_ids for doc recall
             "retrieval_scope": {"backend": "hotpot_local", "qid": r["id"], "candidate_doc_ids": ids}}
        out_rows.append(r)
    with gzip.open(qdir / f"{ds}_questions.jsonl.gz", "wt", encoding="utf-8") as fh:
        for r in out_rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    test = KIT / "data" / "splits" / "test" / f"newtest_{ds}_questions.jsonl"
    test.parent.mkdir(parents=True, exist_ok=True)
    with test.open("w", encoding="utf-8") as fh:
        for r in out_rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{ds}: {len(out_rows)} questions, {n_docs} documents ({n_gold} gold, "
          f"{n_docs / max(len(out_rows), 1):.1f} per question) -> {qdir} and {test.relative_to(KIT)}")


def build_multihoprag(a) -> int:
    queries = json.loads((RAW / "MultiHopRAG.json").read_text(encoding="utf-8"))
    corpus = json.loads((RAW / "corpus.json").read_text(encoding="utf-8"))
    by_title = {c["title"]: c for c in corpus}
    by_cat: dict[str, list[dict]] = {}
    for c in corpus:
        by_cat.setdefault(c.get("category", ""), []).append(c)
    rng = random.Random(27)
    rows, docs = [], {}
    for i, q in enumerate(queries):
        if q.get("question_type") == "null_query":      # unanswerable by construction
            continue
        gold_titles, seen = [], set()
        for e in q.get("evidence_list") or []:
            t = e.get("title")
            if t in by_title and t not in seen:
                seen.add(t)
                gold_titles.append(t)
        if not gold_titles:
            continue
        qid = f"mhrag_{i:05d}"
        cat = (q["evidence_list"][0] or {}).get("category", "")
        pool = [c for c in by_cat.get(cat, corpus) if c["title"] not in seen] or \
               [c for c in corpus if c["title"] not in seen]
        distractors = rng.sample(pool, min(max(DOCS_PER_QUESTION - len(gold_titles), 0), len(pool)))
        chosen = [{"title": t, "text": by_title[t]["body"], "gold": True} for t in gold_titles] + \
                 [{"title": c["title"], "text": c["body"], "gold": False} for c in distractors]
        rng.shuffle(chosen)
        ans = str(q["answer"]).strip()
        rows.append({"id": qid, "query": q["query"], "answer": ans,
                     "type": q.get("question_type", ""), "level": "hard", "num_hops": str(len(gold_titles)),
                     "answer_type": "bool" if ans.lower() in ("yes", "no") else "span",
                     "gold_granularity": "document",
                     "gold": {"answer": ans, "answer_aliases": [], "supporting_titles": gold_titles}})
        docs[qid] = chosen
    rng.shuffle(rows)
    write_dataset("multihoprag", rows, docs, a.limit)
    return 0


def wiki_text(title: str, client: httpx.Client) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (re.sub(r"[^A-Za-z0-9_.-]", "_", title)[:150] + ".txt")
    if f.exists():
        return f.read_text(encoding="utf-8")
    for attempt in range(4):
        try:
            r = client.get(WIKI, params={"action": "query", "prop": "extracts", "explaintext": 1,
                                         "format": "json", "redirects": 1, "titles": title}, timeout=30)
            pages = r.json().get("query", {}).get("pages", {})
            text = next(iter(pages.values())).get("extract", "") if pages else ""
            f.write_text(text, encoding="utf-8")
            return text
        except Exception:
            time.sleep(2 * (attempt + 1))
    f.write_text("", encoding="utf-8")
    return ""


def build_framesqa(a) -> int:
    rows_in = list(csv.DictReader((RAW / "test.tsv").open(encoding="utf-8"), delimiter="\t"))
    rng = random.Random(27)
    if a.limit:                       # fetch only what we publish
        rng.shuffle(rows_in)
        rows_in = rows_in[: a.limit]
    titles_of = []
    for r in rows_in:
        links = []
        try:
            links = [str(x) for x in eval(r.get("wiki_links") or "[]")]   # the column is a list literal
        except Exception:
            links = [v for k, v in r.items() if k.startswith("wikipedia_link") and v]
        ts = []
        for u in links:
            t = unquote(u.rsplit("/", 1)[-1]).replace("_", " ").strip()
            if t and t not in ts:
                ts.append(t)
        titles_of.append(ts)
    need = sorted({t for ts in titles_of for t in ts})
    print(f"framesqa: fetching {len(need)} Wikipedia articles (cached under {CACHE.relative_to(KIT)})")
    texts = {}
    with httpx.Client(headers={"User-Agent": "research-kit/1.0 (multi-hop QA benchmark build)"}) as cl:
        for i, t in enumerate(need, 1):
            texts[t] = wiki_text(t, cl)
            if i % 200 == 0:
                print(f"  {i}/{len(need)}")
    rows, docs = [], {}
    all_titles = [t for t in need if texts.get(t)]
    for i, (r, ts) in enumerate(zip(rows_in, titles_of)):
        gold = [t for t in ts if texts.get(t)]
        if not gold:
            continue
        qid = f"frames_{i:05d}"
        pool = [t for t in all_titles if t not in set(ts)]
        distractors = rng.sample(pool, min(max(DOCS_PER_QUESTION - len(gold), 0), len(pool)))
        chosen = [{"title": t, "text": texts[t], "gold": True} for t in gold] + \
                 [{"title": t, "text": texts[t], "gold": False} for t in distractors]
        rng.shuffle(chosen)
        ans = str(r["Answer"]).strip()
        rows.append({"id": qid, "query": r["Prompt"].strip(), "answer": ans,
                     "type": (r.get("reasoning_types") or "").strip(), "level": "hard",
                     "num_hops": str(len(gold)),
                     "answer_type": "bool" if ans.lower() in ("yes", "no") else "span",
                     "gold_granularity": "document",
                     "gold": {"answer": ans, "answer_aliases": [], "supporting_titles": gold}})
        docs[qid] = chosen
    write_dataset("framesqa", rows, docs, None)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dataset", choices=("multihoprag", "framesqa"))
    ap.add_argument("--limit", type=int, default=None, help="publish at most this many questions")
    a = ap.parse_args()
    return {"multihoprag": build_multihoprag, "framesqa": build_framesqa}[a.dataset](a)


if __name__ == "__main__":
    raise SystemExit(main())
