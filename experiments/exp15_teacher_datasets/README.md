# E15 — Teacher-guided datasets compared

Collect the same questions with different teachers (including the student itself), judge them, compare.

Status and result: `experiments/REGISTRY.md`, `results/E15_teacher_datasets/README.md`.

```bash
# collection: slurm/collect_local.sbatch (self-teaching) or slurm/collect_api.sbatch
# comparison: python scripts/compare_teachers.py --arm self=... --arm deepseek=... --baseline self --out runs/compare_teachers
# full commands: docs/TG_DATASETS.md, 'Reproducing the comparison'
```
