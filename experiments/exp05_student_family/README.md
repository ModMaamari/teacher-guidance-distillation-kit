# exp05 — Does it work for students other than the one it was built on?

**Tier 2.** Your experiment 2. Use the best size from exp04 so data is not a confound.

## Candidates

| Model | Params | Note |
|---|---|---|
| `ibm-granite/granite-4.2-3b` | 3B | near-replicate of the reference student (4.1-3b). Report it as such: it is your sanity check, not a new data point. |
| `openbmb/MiniCPM5-2B` | 2B | |
| `openbmb/MiniCPM5-1B` | 1B | the small end; expect the biggest drop |
| `ai9stars/G9v3-3B` | 3B | |
| `Nanbeige/Nanbeige4.1-3B` | 3B | |
| `LiquidAI/LFM2.5-2.6B` | 2.6B | hybrid architecture; the most likely to need special handling |

## Probe before you train

`00_probe_students.sh` is cheap (tokenizer only, no weights) and catches the failures that
otherwise waste a GPU day:

- **no chat template** -- the whole pipeline renders prompts through one; without it the
  model cannot be used as an agent at all
- **a template that opens a reasoning block** -- this is the bug that made a healthy model
  look catastrophically broken last week. `tgd.chat_template` detects and closes it, but
  you want to know which models need that before interpreting any diagnostic.
- **unknown architecture** -- if `transformers` cannot resolve the config, neither vLLM
  nor the trainer will.

Then, on a GPU, run `scripts/diag_distributions.py` for each model **before** trusting any
accuracy number. A model whose valid-token mass is near zero is not being evaluated, it is
being mismeasured.

## Run

```bash
bash 00_probe_students.sh                 # cheap, no GPU, no weights
export PARTITION=<gpu-partition>
SIZE_SPLIT=data/splits/uniform bash run.sh train
bash run.sh eval
bash run.sh judge
```

Set `SIZE_SPLIT` to the winning split from exp04 (for example
`data/splits/uniform_ep4000`) so every student sees the same amount of supervision.

## Memory

The 3B reference peaks near 26 GB with LoRA at 8k context, so a 45 GB card fits it. If a
larger candidate will not fit, drop `--max-length` before dropping the batch size: the
context length is what drives the peak.

## Reporting

Report absolute accuracy *and* the lift over each model's own base arm. A weak model with a
large lift supports the method better than a strong model with a small one, and reviewers
read the lift column first.
