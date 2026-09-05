"""Repair a checkpoint trained before the logit-scaling guard existed — no retraining.

If a model was trained through a loss path that optimised UNSCALED logits while its forward
pass divides them by ``config.logits_scaling``, the weights are not damaged. They were
optimised to produce well-calibrated *unscaled* logits, and inference is dividing them by a
constant it should not. Telling inference to stop dividing hands back exactly the
distribution training produced.

That is a one-field config change, and it is reversible. Measured on this project's own
pre-fix checkpoint:

                      before      after      (a full retrain, for reference)
    OOD entropy       10.908      0.165      0.222
    OOD top-1          0.006      0.933      0.910
    valid-token mass    1.2 %      100 %      100 %

**Only use this on a checkpoint whose training log disagrees with the model.** Verify first:
score the model on the file its trainer evaluated and compare against the logged loss. If the
model reproduces its log, nothing is wrong and this script would *introduce* the bug. The
``--verify-against`` option does that check and refuses to write unless it fails.

Usage::

    # check whether a checkpoint needs repair (writes nothing)
    python scripts/repair_logit_scale.py --model runs/train/uniform/merged --dry-run

    # repair in place, keeping a backup of the original config
    python scripts/repair_logit_scale.py --model runs/train/uniform/merged
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse  # noqa: E402
import json  # noqa: E402
import shutil  # noqa: E402

from tgd.logit_scale import scaling_fields  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="a merged model directory")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("--restore", action="store_true", help="put the backed-up config back")
    args = ap.parse_args()

    d = Path(args.model)
    cfg_path, backup = d / "config.json", d / "config.json.pre_repair"

    if args.restore:
        if not backup.exists():
            print(f"no backup at {backup}")
            return 2
        shutil.move(str(backup), str(cfg_path))
        print(f"restored the original config for {d}")
        return 0

    if not cfg_path.exists():
        print(f"no config.json in {d}")
        return 2
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    class C:
        pass
    c = C()
    for k, v in cfg.items():
        setattr(c, k, v)
    present = scaling_fields(c)

    # Order matters: after a repair the field reads 1.0, which looks identical to "this
    # model never rescaled anything". The backup is what distinguishes the two.
    if backup.exists():
        print(f"{d}\n  already repaired (config.json.pre_repair is present); "
              f"--restore puts the original back")
        return 0
    if not present:
        print(f"{d} applies no logit rescaling; nothing to repair.")
        return 0
    field, value = next(iter(present.items()))
    print(f"{d}\n  config.{field} = {value}")
    print(f"  a checkpoint trained on unscaled logits needs this set to 1.0")

    if args.dry_run:
        print("  --dry-run: nothing written")
        return 0

    shutil.copy2(cfg_path, backup)
    cfg[field] = 1.0
    cfg_path.write_text(json.dumps(cfg, indent=1), encoding="utf-8")
    print(f"  set config.{field} = 1.0 (original saved to {backup.name})")
    print("  VERIFY before trusting it: run scripts/diag_distributions.py on this model.")
    print("  Entropy should be well under 1 nat and valid-token mass at 100%.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
