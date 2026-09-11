# exp11 — Is LoRA the ceiling?

**Tier 3.** Every result uses one LoRA configuration and one learning rate. Two questions
follow, and both are cheap to answer:

1. **Does adapter capacity limit the gain?** If rank 32 beats rank 16, a reviewer will ask
   why you stopped there. If it does not, you can write one sentence retiring the question.
2. **Is the recipe tuned, or just the first thing that worked?** Learning rate and epoch
   count are the two knobs that matter most; showing a small sweep is enough.

A full fine-tune is the strongest version of question 1 but needs far more memory than the
3B reference peak of ~26 GB. Run it only if a large card is free; the rank sweep answers
most of the objection.

## Run

```bash
export PARTITION=<gpu-partition>
bash run.sh rank      # lora-r 8 / 16 / 32 / 64, alpha tracking r
bash run.sh lr        # 1e-4 / 2e-4 / 5e-4
bash run.sh epochs    # 1 / 2 / 3
bash run.sh eval
bash run.sh judge
```

Each variant trains from the same split with the same seed, so the knob is the only change.

## Reporting

A single table with the default configuration highlighted. The useful sentence is
"performance is flat across ranks 16-64, so adapter capacity is not the binding
constraint" -- if that is what you find. If a bigger rank does help, retrain the headline
model at the better setting before writing the paper, not after.

Watch the loss-path guard in every run. It is the check that caught a student which decoded
correctly and sampled junk (`docs/STABILITY.md`), and a knob sweep is exactly where an
unusual configuration might trip it.
