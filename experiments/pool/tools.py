#!/usr/bin/env python3
"""Small helpers the pool tasks call (experiments/pool/run_task.sh). No models, no network.

    tools.py judged  --episodes '<glob>' --verdicts <file>   # exit 1 until every episode has a verdict
    tools.py view    --name E02 base=runs/eval/base seed13=runs/eval/seed13 ...
    tools.py publish <src-dir> <results-dir> [--only f1 f2]  # copy tables into results/, scrubbed
    tools.py pvalues --out results/E12_multiple_comparisons/kit

``view`` builds ``runs/views/<name>/<arm>`` as symlinks to evaluation directories (so one
test-set directory can appear under another arm name, e.g. ``base_b3`` -> ``runs/eval/base``)
and merges every primary-judge verdict file (``runs/judge/*/verdicts.jsonl``) into
``runs/views/<name>/verdicts.jsonl``; collect_results.py keys verdicts by the resolved episode
path, so the symlinks still find theirs.

``publish`` is the only way pool output reaches ``results/`` (which is committed). Provider
prefixes are stripped from model ids, and the copy is refused if a site identifier (an absolute
path, or a name listed in PUBLISH_FORBID) survives, because the kit is shareable.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
# Generic provider prefixes (docs/PROVIDERS.md) plus the site's own, from local.env, so that this
# tracked file names no site: PUBLISH_STRIP (extra prefixes to strip, a regex alternation) and
# PUBLISH_FORBID (names that must never reach results/: gateways, clusters, hosts).
_strip = "|".join(x for x in (r"oai-[\w-]+", "openrouter", "custom", os.environ.get("PUBLISH_STRIP", "")) if x)
PREFIX = re.compile(rf"\b(?:{_strip})/(?=[\w.-])")
_forbid = [r"(?<![\w.])/(?:home|shared|scratch|mnt|net|work|data)/[\w.-]+"]   # absolute site paths
if os.environ.get("PUBLISH_FORBID"):
    _forbid.append(rf"\b(?:{os.environ['PUBLISH_FORBID']})\b")
FORBIDDEN = re.compile("|".join(_forbid), re.I)


def judged(a) -> int:
    files = sorted(glob.glob(a.episodes))
    want = set()
    for f in files:
        for line in open(f, encoding="utf-8"):
            if line.strip():
                want.add((f, json.loads(line)["qid"]))
    have = set()
    if Path(a.verdicts).exists():
        for line in open(a.verdicts, encoding="utf-8"):
            if line.strip():
                r = json.loads(line)
                have.add((r["source"], r["qid"]))
    missing = want - have
    print(f"judged {len(want) - len(missing)}/{len(want)} episodes in {len(files)} files")
    if not files:
        print("!! no episode files match", a.episodes)
        return 1
    return 1 if missing else 0


def view(a) -> int:
    root = KIT / "runs" / "views" / a.name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    ok = True
    for spec in a.arms:
        arm, _, src = spec.partition("=")
        if not (KIT / src).is_dir():
            print(f"!! {src} does not exist (arm {arm})")
            ok = False
            continue
        os.symlink(KIT / src, root / arm)
    with open(root / "verdicts.jsonl", "w", encoding="utf-8") as out:
        for f in sorted((KIT / "runs" / "judge").glob("*/verdicts.jsonl")):
            out.write(f.read_text(encoding="utf-8"))
    print(f"view {root.relative_to(KIT)}: {len(a.arms)} arms")
    return 0 if ok else 1


def scrub(text: str) -> str:
    return PREFIX.sub("", text)


def publish(a) -> int:
    src, dest = KIT / a.src, KIT / a.dest
    names = a.only or [p.name for p in sorted(src.iterdir()) if p.is_file()
                       and p.suffix in (".json", ".md", ".txt", ".csv", ".jsonl")]
    staged = {}
    for n in names:
        p = src / n
        if not p.is_file():
            print(f"!! {p.relative_to(KIT)} missing")
            return 1
        text = scrub(p.read_text(encoding="utf-8"))
        bad = sorted({m.group(0) for m in FORBIDDEN.finditer(text)})
        if bad:
            print(f"!! {p.relative_to(KIT)} still names {bad}; not published")
            return 1
        staged[n] = text
    dest.mkdir(parents=True, exist_ok=True)
    for n, text in staged.items():
        (dest / n).write_text(text, encoding="utf-8")
    print(f"published {len(staged)} file(s) -> {dest.relative_to(KIT)}: {', '.join(staged)}")
    return 0


def pvalues(a) -> int:
    out = KIT / a.out
    out.mkdir(parents=True, exist_ok=True)
    found = sorted(KIT.glob("results/E*/*/results.json"))
    for f in found:
        tag = f"{f.parent.parent.name.split('_')[0]}_{f.parent.name}"
        r = subprocess.run([sys.executable, str(KIT / "experiments/exp12_multiple_comparisons/correct_pvalues.py"),
                            "--results", str(f)], capture_output=True, text=True, cwd=KIT)
        (out / f"{tag}.txt").write_text(scrub(r.stdout + r.stderr), encoding="utf-8")
        print(f"{tag}: rc={r.returncode}")
    return 0 if found else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("judged")
    p.add_argument("--episodes", required=True)
    p.add_argument("--verdicts", required=True)
    p = sub.add_parser("view")
    p.add_argument("--name", required=True)
    p.add_argument("arms", nargs="+", metavar="ARM=DIR")
    p = sub.add_parser("publish")
    p.add_argument("src")
    p.add_argument("dest")
    p.add_argument("--only", nargs="+")
    p = sub.add_parser("pvalues")
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    return {"judged": judged, "view": view, "publish": publish, "pvalues": pvalues}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
