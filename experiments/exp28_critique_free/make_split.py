#!/usr/bin/env python
"""E28: the self-guided split with the critique removed from every target.

Same examples, same inputs, same order; each target loses its "teacher_guidance" field and keeps
everything else byte for byte (the remaining JSON is re-serialised the way the split builder wrote
it, which is checked on every example). Planning examples carry no such field and are unchanged.

    python experiments/exp28_critique_free/make_split.py --src data/splits_self --out data/splits_self_nocrit
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def strip(content: str) -> tuple[str, bool]:
    obj = json.loads(content)
    for ascii_ in (True, False):
        if json.dumps(obj, ensure_ascii=ascii_) == content:
            break
    else:
        raise SystemExit(f"cannot reproduce the serialisation of: {content[:120]}")
    had = obj.pop("teacher_guidance", None) is not None
    return json.dumps(obj, ensure_ascii=ascii_), had


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="data/splits_self")
    ap.add_argument("--out", default="data/splits_self_nocrit")
    a = ap.parse_args()
    src, out = Path(a.src), Path(a.out)
    (out / "uniform").mkdir(parents=True, exist_ok=True)
    for f in ("stats.json", "pools.json"):
        shutil.copy2(src / f, out / f)
    if (src / "test").exists() and not (out / "test").exists():
        shutil.copytree(src / "test", out / "test")
    shutil.copy2(src / "uniform" / "manifest.json", out / "uniform" / "manifest.json")
    report = {}
    for part in ("train", "dev"):
        n = stripped = 0
        with open(src / "uniform" / f"{part}.jsonl", encoding="utf-8") as fi, \
             open(out / "uniform" / f"{part}.jsonl", "w", encoding="utf-8") as fo:
            for line in fi:
                if not line.strip():
                    continue
                r = json.loads(line)
                msg = r["completion"][0]
                msg["content"], had = strip(msg["content"])
                r["metadata"]["critique_removed"] = had
                n += 1
                stripped += had
                fo.write(json.dumps(r, ensure_ascii=False) + "\n")
        report[part] = {"examples": n, "critique_removed": stripped}
        print(f"{part}: {n:,} examples, critique removed from {stripped:,}")
    (out / "uniform" / "critique_free.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
