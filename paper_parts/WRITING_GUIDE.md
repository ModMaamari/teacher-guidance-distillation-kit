# Writing the ICLR paper: where everything is

Everything needed to write or revise the paper, as of 2026-09-24. All 254 experiment jobs are
finished; no result is pending.

## The two repositories

| Repository | Clone URL | Local path | What it holds |
|---|---|---|---|
| **Paper** (Overleaf-synced) | `git@github.com:ModMaamari/Self-Guidance-Self-Improvement-Using-KnowledgeDistillation-on-Self-Guided-Trajectories.git` | `/shared/al-maamari/DeKIS/self-guidance-overleaf` | LaTeX source, generated tables and figures, the built PDF |
| **Experiment kit** | `git@github.com:ModMaamari/teacher-guidance-distillation-kit.git` | `/shared/al-maamari/DeKIS/teacher-guidance-kit` | Code, every experiment's results and write-ups, the source material for the prose |

**The paper repository is connected to Overleaf.** Pull before any edit and push immediately after,
or Overleaf edits and local edits will conflict:

```bash
cd /shared/al-maamari/DeKIS/self-guidance-overleaf
git pull --rebase          # before editing
# ... edit main.tex ...
git commit -am "..." && git push
```

Commits in both repositories are authored as `ModMaamari <mamarih1@gmail.com>` with no
co-author or tool attribution lines.

---

## 1. The paper — `/shared/al-maamari/DeKIS/self-guidance-overleaf/`

| Path | What it is |
|---|---|
| `main.tex` | The whole paper: 9 pages of main text, then the required statements and five appendices |
| `main.pdf` | Current build (16 pages including appendices) |
| `references.bib` | Bibliography, including the verified model-card entries |
| `make_tables.py` | **Regenerates every table and figure dataset from the kit's published results** |
| `tables/*.tex` | The generated tables — never hand-edit: `main`, `seedpairs`, `matched`, `filter`, `lodo`, `robustness`, `forgetting`, `efficiency`, `judges`, `form` |
| `figures/pipeline.tex` | TikZ diagram of the method |
| `figures/scaling.tex`, `figures/budget.tex` | pgfplots figures (data-scaling curve, step-budget curve) |
| `data/*.csv`, `data/scaling_base.tex` | Figure data, also generated |
| `iclr2027_conference.sty`, `iclr2027_conference.bst`, `fancyhdr.sty`, `natbib.sty`, `math_commands.tex` | ICLR 2027 template files — leave untouched |
| `README.md` | How to rebuild and what remains for the authors |

**Rebuilding:**

```bash
cd /shared/al-maamari/DeKIS/self-guidance-overleaf
python make_tables.py --kit ../teacher-guidance-kit   # refresh tables/ and data/
latexmk -pdf main.tex                                 # build (TeX is on the login node only)
```

`make_tables.py` prints anything it could not find, and renders it in the PDF as a red **TBD**.
There are none at present.

**Two author tasks remain**, both marked `\todo{}` in `main.tex`:
1. Complete and verify the AI-use statement (required by ICLR).
2. Add the anonymous code link in the reproducibility statement.

**Page budget:** the main text ends exactly on page 9 of the 9 allowed; the statements and
appendices follow and do not count. Anything added needs a matching cut. Check with:

```bash
pdftotext -layout -f 9 -l 9 main.pdf - | tail -5     # the conclusion must still be here
```

---

## 2. Source material for the prose — `/shared/al-maamari/DeKIS/teacher-guidance-kit/paper_parts/`

| Path | What it is |
|---|---|
| `EXPERIMENTS.md` | All 28 experiments: question, numbers, caveats, and where a later experiment revised an earlier one |
| `FINDINGS.md` | 16 findings ranked by strength, each with its supporting experiments and the numbers behind it |
| `WRITING_GUIDE.md` | This file |

These are the best starting point: every number in them is traceable to a published result file.

---

## 3. The evidence — `/shared/al-maamari/DeKIS/teacher-guidance-kit/`

| Path | What it is |
|---|---|
| `results/E00_reference/` … `results/E27_new_benchmarks/` | One folder per experiment. Each has `README.md` (question, answer, protocol, caveats, history) and `kit/results.json`, `kit/RESULTS.md`, plus extras such as `summary.txt`, `train_cost.txt`, `provider_split.txt`, `reference.txt`, `leak_check.txt` |
| `experiments/REGISTRY.md` | One-page table of all 28 experiments mapped to folder, status, judge and paper section |
| `experiments/registry.yaml` | Machine-readable source of that table (`python experiments/status.py` regenerates the Markdown) |
| `experiments/exp00_reference/` … `exp27_new_benchmarks/` | Per-experiment design READMEs and analysis scripts |
| `results/README.md` | Index of published results |

**Most-cited result files:**

| Claim | File |
|---|---|
| Main comparison and seed pairs | `results/E19_self_guided_robustness/kit/` (`results.json`, `seeds.txt`, `seed_averaged.json`) |
| Matched-supervision ablation, three seeds | `results/E21_unguided_baselines/kit/summary.txt` |
| Six-seed decisive test | `results/E25_seed_power/kit/summary.txt` |
| Teacher rollouts at full scale | `results/E24_teacher_scale/kit/summary.txt` |
| Correctness filter | `results/E20_correctness_filter/kit/summary.txt`, `filter_vs_judge.txt` |
| Judge-based filter | `results/E22_judge_filter/kit/summary.txt` |
| End-to-end cost of every route | `results/E23_pipeline_cost/kit/pipeline_cost.txt` |
| Untrained reference configurations | `results/E26_oracle_guidance/kit/reference.txt` |
| External benchmarks | `results/E27_new_benchmarks/kit/summary_multihoprag.txt`, `summary_framesqa.txt`, `leak_check.txt` |
| Step budget | `results/E08_step_budget/kit/budget.txt` |
| Multiple-comparison correction | `results/E12_multiple_comparisons/kit/*.txt` |

---

## 4. Method and protocol details

| Path | What it is |
|---|---|
| `tgd/`, `agentsim/` | The harness: agent loop, guidance, leakage sanitiser, metrics |
| `scripts/build_splits.py` | The correctness filter and split construction (the `--keep` options behind E20 and E22) |
| `scripts/train_sft.py` | LoRA training (rank 32, alpha 64, lr 1e-4, 2 epochs, 8,192 tokens) |
| `scripts/eval.py`, `slurm/eval_student.sbatch` | Evaluation protocol |
| `scripts/judge.py` | The LLM judge, and the prompt quoted in the appendix |
| `experiments/exp16_judge_selection/`, `exp03_judge_validity/` | How the judge was chosen and validated |
| `experiments/exp27_new_benchmarks/build_datasets.py` | Converts MultiHop-RAG and FRAMES into the harness's format (the data itself is not tracked) |
| `experiments/pool/` | The Slurm job pool that ran every experiment — useful for the reproducibility statement |
| `docs/` | Longer design notes referenced by some experiment READMEs |

---

## 5. Rules that keep the paper honest

1. **Every number in a table or figure comes from `results/` through `make_tables.py`.** A number
   edited by hand in `tables/*.tex` is overwritten on the next regeneration. Numbers quoted in the
   running text were copied from the same files.
2. **Name the metric.** Unless stated otherwise, accuracy means judge-correct accuracy on the 747
   held-out questions, graded by Gemma-4-31B-it. Differences are percentage points.
3. **Say which comparison a p-value belongs to**, and whether it survives Holm or only
   Benjamini-Hochberg (E12 has the corrected values per table).
4. **Reference arms are upper bounds, not systems.** The live-critique, self-critique and
   teacher-alone rows all give their critic the gold answer at inference.
5. **Where a later experiment revised an earlier one, the paper says so** (E17 → E21 → E25 on the
   self-guided advantage; E00 → E08 on the teacher reference). Keep it that way.

---

## 6. State as of 2026-09-24

- All 28 experiments finished; nothing is running; no result is pending.
- Paper builds cleanly, main text ends on page 9, no TBDs.
- Last paper commit: `d755d20`. Last kit commit: `f5b212a`.
- Deadline: ICLR 2027 full paper, Friday 25 September, 23:59 AoE (Saturday 26 September, 13:59 CEST).
