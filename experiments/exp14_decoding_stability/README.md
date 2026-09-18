# E14 — Decoding stability

Can the trained student be sampled? Measures next-token distributions and sampled accuracy.

Status and result: `experiments/REGISTRY.md`, `results/E14_decoding_stability/README.md`.

```bash
sbatch -p <gpu-partition> slurm/eval_stability.sbatch <adapter> <arm>
# background: docs/STABILITY.md
```
