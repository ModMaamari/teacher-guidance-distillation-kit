#!/usr/bin/env python3
"""Turn labels saved by label_app.html into the CSV that 03_agreement.py --human reads.

The app saves one document per sample, ``labels/s<NNN>``, holding
``{"label": "1" | "0" | "skip", "note": ..., "n": NNN}``. Export them as JSON files (for a
published copy, the artifact database read with an ``out_dir``; each file is one document),
then:

    python labels_to_csv.py --labels <dir of labels/*.json> --sample runs/e03/human_sample.csv \
        --out runs/e03/human_labels.csv

``human_correct`` becomes 1, 0, or blank ("can't tell" and unlabelled rows), which is what
03_agreement.py counts. The key file is copied next to the output under the name
03_agreement.py looks for.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--labels", required=True, help="directory holding one JSON document per label")
    ap.add_argument("--sample", default="runs/e03/human_sample.csv")
    ap.add_argument("--out", default="runs/e03/human_labels.csv")
    a = ap.parse_args()

    labels = {}
    for f in sorted(Path(a.labels).rglob("*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        body = doc.get("data", doc) if isinstance(doc.get("data"), dict) else doc
        n = body.get("n")
        if n is None and f.stem.startswith("s") and f.stem[1:].isdigit():
            n = int(f.stem[1:])
        if n is not None and body.get("label") in ("1", "0", "skip"):
            labels[int(n)] = body
    rows = list(csv.DictReader(open(a.sample, encoding="utf-8")))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    counts = {"1": 0, "0": 0, "skip": 0, "open": 0}
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["sample_id", "question", "gold_answer", "model_answer", "human_correct", "note"])
        for r in rows:
            lab = labels.get(int(r["sample_id"]))
            v = lab["label"] if lab else "open"
            counts[v] += 1
            w.writerow([r["sample_id"], r["question"], r["gold_answer"], r["model_answer"],
                        v if v in ("0", "1") else "", (lab or {}).get("note", "")])
    key = Path(a.sample).with_suffix(".key.json")
    if key.exists():
        shutil.copyfile(key, out.with_suffix(".key.json"))
    print(f"wrote {out}: {counts['1']} correct, {counts['0']} incorrect, {counts['skip']} can't tell, "
          f"{counts['open']} unlabelled")
    return 0 if counts["1"] + counts["0"] else 1


if __name__ == "__main__":
    sys.exit(main())
