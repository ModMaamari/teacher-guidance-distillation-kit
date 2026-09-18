# exp18 — Does answer form move the ranking?

**Why.** Students trained on the student's own trajectories (self-guided, unguided, GLM-guided)
answer in about 20 words (median). Students trained on DeepSeek-guided trajectories answer in 2.
Exact match separates them sharply (9.9 % vs 35.3 %); the judge ranks the verbose ones higher.
E03 validated the judge against a human only on concise E00 answers, so a reviewer can fairly
ask whether verbosity inflates the judge.

## Design

Re-grade every E01/E06/E17 arm (`E18_ARMS` in `experiments/pool/run_task.sh`) three more ways:
- **`kimi`, `qwen`:** the two swap judges from E03, with the standard prompt.
- **`strict`:** the primary judge with `strict_judge_prompt.txt`, which counts an answer as
  correct only if it commits to one answer (lists and hedges are incorrect).

`report.py` prints each arm's accuracy under every judge, and the paired differences for the
comparisons the paper makes. If self-guided > DeepSeek-guided holds under the strict rubric and
both swap judges, verbosity does not explain it.

## Run

Pool tasks `judge_e18_strict`, `judge_e18_kimi`, `judge_e18_qwen`, `e18_report`.
