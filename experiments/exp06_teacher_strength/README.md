# exp06 — Is the effect specific to one teacher?

**Tier 2.** The reference teacher is `DeepSeek-V4-Flash`. A reviewer will ask whether
"teacher guidance" names a real mechanism or one lucky pairing. Two extra teachers answer
it, and a *weaker* teacher that still helps is the stronger result: it separates guidance
from raw capability transfer.

## The two teachers to collect with

Both verified live against our OpenAI-compatible gateway on 2026-09-06:

| Role | Model | Params | Why |
|---|---|---|---|
| **stronger** | `mistralai/Mistral-Medium-3.5-128B` | 128B | clearly above the reference teacher |
| **weaker** | `RedHatAI/Mistral-Small-3.2-24B-Instruct-2506-FP8` | 24B | ~5x smaller, same family |

**Same family on purpose.** Medium and Small share a training recipe, so the pair isolates
*scale* rather than confounding it with vendor, data and post-training. With DeepSeek as a
third point from a different family you get both a scale axis and a family check.

Both were probed and both are plain chat models: no `reasoning_content`, so no risk of the
token budget being eaten by chain-of-thought before the critique appears.

### Rejected, and why

| Model | Reason |
|---|---|
| `moonshotai/Kimi-K2.6` | it is the **judge**. Using it as teacher lets the teacher grade its own student. |
| `gpt-oss-120b` | excluded by project rule. |
| `MiniMaxAI/MiniMax-M3-MXFP8` | listed by the API but returns "team not allowed to access model". |
| `deepseek-ai/DeepSeek-V4-Flash` | the reference teacher, and **currently down** at the provider (its serving backend refuses connections). `DeepSeek-V4-Flash-0731` is up and is the drop-in replacement, but note it *does* emit `reasoning_content`, so give it a large `--teacher-max-tokens`. |

Backup if the primary gateway is unstable: `qwen3-next-80b-a3b-instruct` (80B,
non-reasoning, verified live on a second endpoint). Serving the same experiment from two
gateways adds a confound, so prefer it only as a fallback.

## Collect the two datasets (in `teacher-guidence`, not here)

Point the collector at each teacher in turn, keeping the student, questions, budget and
temperatures identical to the reference run:

```bash
# in teacher-guidence/
python scripts/run_tgv1_collection.py --all --num-samples 2000 \
    --teacher oai-teacher/mistralai/Mistral-Medium-3.5-128B     # strong
python scripts/run_tgv1_collection.py --all --num-samples 2000 \
    --teacher oai-teacher/RedHatAI/Mistral-Small-3.2-24B-Instruct-2506-FP8   # weak
```

Then copy the consolidated episodes here as:

```
data/episodes_tstrong/episodes.jsonl.gz
data/episodes_tweak/episodes.jsonl.gz
```

## Run

```bash
bash 00_probe_teachers.sh                 # confirm both endpoints answer, before spending
export PARTITION=<gpu-partition>
bash run.sh splits && bash run.sh train && bash run.sh eval && bash run.sh judge
```

## Reading it

Report guidance yield per teacher (correct episodes / collected) next to downstream
accuracy. The interesting shapes:

- **Weak teacher still lifts the student well above base.** Guidance is doing the work,
  not capability transfer. This is the best outcome for the paper.
- **Accuracy tracks teacher strength closely.** The method is distillation with extra
  steps; say so, and pivot the contribution to cost.
- **Yield tracks strength but accuracy does not.** Worth its own paragraph: it means the
  filter, not the critique, is carrying the method, which is exp01's question again.
