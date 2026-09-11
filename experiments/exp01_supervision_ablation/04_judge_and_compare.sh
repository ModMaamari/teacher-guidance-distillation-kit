#!/usr/bin/env bash
# Judge every episode, then build the results table with paired tests between arms.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
banner "exp01: judge + compare"
submit_cpu "$KIT/slurm/judge.sbatch" "$JUDGE"
cat <<'TXT'

When the judge job finishes, the comparison you care about is in
runs/results/results.md -- the paired rows:

    sup_selfdist  -> sup_guided     does guidance beat the correctness filter?
    sup_teachdist -> sup_guided     does guidance beat plain distillation?

Each row carries a paired bootstrap 95% CI and an exact McNemar test.
If a CI crosses zero, say so plainly; a null here is a real finding about the method.
TXT
