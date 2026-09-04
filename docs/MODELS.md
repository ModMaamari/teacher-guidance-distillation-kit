# Students

Any instruction-tuned causal LM works. Point `--model` (or `STUDENT_MODEL`) at an HF id or a
local path and the pipeline adapts: the chat template comes from the model, the loss path and
micro-batch are chosen from its config, and the diagnostics report what it does with its logits.

```bash
STUDENT_MODEL=<hf-id> bash slurm/run_pipeline.sh          # whole pipeline
python scripts/train_sft.py --model <hf-id> ...           # one stage
```

## What the kit checks for you

| Concern | Handled by |
|---|---|
| Model is not a plain causal LM (ships as a vision-language / conditional-generation architecture) | `tgd/models.py` tries each auto class and reports which one loaded |
| Language settings nested under `config.text_config` | every config check reads the nested config as well as the top level |
| Architecture rescales logits, breaking TRL's chunked loss | detected from the config *and* measured against the model's own forward pass; the run stops rather than producing an unsamplable model (`docs/STABILITY.md`) |
| Larger vocabulary makes the logits tensor too big | micro-batch traded for gradient accumulation, effective batch preserved |
| Embedding matrix padded past the tokenizer length | the memory estimate takes the larger of the two |

None of this needs configuring. If a model needs something the kit cannot infer, it stops with
an explanation instead of training a broken student.

## Candidates checked

Configuration and tokenizer verified for each of the following; **none has been trained
end-to-end here** — those numbers are the point of running them.

| Model | Architecture | Vocab | Logit rescaling | Notes |
|---|---|---|---|---|
| `ibm-granite/granite-4.2-3b` | `GraniteForCausalLM` | 100,352 | `logits_scaling` present but **1.0** — a no-op | Loads as a causal LM. Unlike 4.1, which sets it to 10.0, this one is unaffected by the chunked-loss issue |
| `openbmb/MiniCPM5-1B` | `LlamaForCausalLM` | 130,560 | none | Reports `model_type: llama`, so it needs no special support |
| `ai9stars/G9v3-3B` | `LlamaForCausalLM` | 130,560 | none | As above |
| `Nanbeige/Nanbeige4.1-3B` | `LlamaForCausalLM` | 166,144 | none | Largest vocabulary of the set: expect the micro-batch guard to trigger sooner |
| `LiquidAI/LFM2.5-2.6B` | `Lfm2ForCausalLM` | 128,000 | none | Embedding matrix is padded past the tokenizer (125,017 tokens) |
| `Qwen/Qwen3.5-2B` | `Qwen3_5ForConditionalGeneration` | in `text_config` | none | **Not in the causal-LM auto mapping** — `AutoModelForCausalLM` fails on it. The kit loads it through the image-text-to-text class and trains its text stack. Its language settings are nested under `text_config` |

Every one of these ships a chat template, which the kit requires.

## Before you trust a new student

Two commands, in this order:

```bash
# 1. a 2-minute pipeline check: does it load, tokenize, and train at all?
python scripts/train_sft.py --model <hf-id> --train-file data/splits/uniform/train.jsonl \
    --out runs/train/smoke --smoke

# 2. after a real run: can it be sampled, or only decoded greedily?
sbatch -p <gpu-partition> slurm/eval_stability.sbatch runs/train/<name>/adapter <name>
```

The first prints the model's logit rescaling, the loss path it chose, the micro-batch it
settled on, and whether the training loss matches the model's own forward pass. If that last
check fails, stop: the model would decode correctly at greedy and produce junk when sampled,
and no headline evaluation would show it.

The second is the one people skip. `docs/STABILITY.md` explains why it matters more than it
looks like it should.

## If a new student misbehaves

`docs/TROUBLESHOOTING.md` leads with the failures that produce no error — a model that is
perfect at greedy and unusable when sampled is the one to know about before you trust any
numbers from a new student.

## Library support

Checked against the pinned versions: `granite`, `llama`, `lfm2` and `qwen3_5` all resolve.
A model whose `model_type` your transformers does not know needs a newer version or
`trust_remote_code`, which this kit does not enable for you — read the model's code first.
