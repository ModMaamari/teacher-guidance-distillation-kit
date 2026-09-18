# E09 — Forgetting

**Question.** What does training cost in general ability?

**Answer.** Little. The trained student (E02 seed 13, kit-trained with the fixed loss path) against
the base weights, same items and same server, greedy:

| Benchmark | Items | Base | Trained | Δ points | McNemar p |
|---|---|---|---|---|---|
| MMLU | 1,710 | 63.51 % | 63.27 % | −0.23 | 0.76 |
| GSM8K | 1,319 | 89.16 % | 88.40 % | −0.76 | 0.39 |
| HellaSwag | 1,500 | 75.27 % | 73.67 % | −1.60 | 0.029 |
| Pooled | 4,529 | 74.87 % | 74.03 % | −0.84 | 0.037 |

Only HellaSwag loses a significant amount, 1.6 points. Report: `kit/REPORT.md`, numbers:
`kit/stats.json`.

**Protocol.** `slurm/eval_forgetting.sbatch` with base and adapter behind one vLLM server, one
greedy run (RUNS=1), strict answer parsing. Pool task `forget_seed13`.

**Caveats.** One greedy run and one seed, so the per-benchmark SDs are not estimated; the
item-level McNemar test is the significance check.

## History

- **2026-09-18:** rerun on the kit-trained student, whose loss path is fixed (E14). It loses less
  than the earlier research adapter did: pooled −0.84 (p 0.037) vs −1.4 (p 0.001); GSM8K −0.8
  (n.s.) vs −2.2.
- **Earlier:** the original all-4 research adapter, trained through the loss path later fixed,
  scored MMLU −0.9, GSM8K −2.2 (p 0.007), HellaSwag −1.1, pooled −1.4 (p 0.001)
  (`docs/FORGETTING.md`).
