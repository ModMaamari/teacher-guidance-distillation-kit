#!/usr/bin/env python3
"""One upkeep pass for the pool; keeper.sbatch runs it every 10 minutes (never on a login node).

Submits workers only for work that can start now, so no GPU is held while its tasks wait on
something else:

  * GPU workers (`tgd-gpu`, GPU_PARTITION, 12 h) up to min(GPU_WORKERS, GPU tasks that are
    runnable or running);
  * one `tgd-short` worker (SHORT_PARTITION, 1 h, evaluations only) whenever a GPU task
    estimated at <= 1 h is runnable, because that partition starts at once;
  * one CPU worker (`tgd-cpu`, CPU_PARTITION, 24 h) while any CPU/API task is pending.

    python experiments/pool/keeper.py             # one pass
    python experiments/pool/keeper.py --dry       # print what it would submit
    python experiments/pool/keeper.py --finished  # exit 0 iff every task is done or dead
"""
from __future__ import annotations

import collections
import os
import subprocess
import sys
import time
from pathlib import Path

POOL = Path(__file__).resolve().parent
sys.path.insert(0, str(POOL))
import worker as W  # noqa: E402  (shares the task table, queue layout and dependency check)

GPU_PARTITION = os.environ.get("GPU_PARTITION", "gpu")
SHORT_PARTITION = os.environ.get("SHORT_PARTITION", "short")
SHORT_GRES = os.environ.get("SHORT_GRES", "gpu:l40s:1")
CPU_PARTITION = os.environ.get("CPU_PARTITION", "general")
GPU_WORKERS = int(os.environ.get("GPU_WORKERS", "4"))


def say(*a):
    print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), *a, flush=True)


def jobs() -> collections.Counter:
    out = subprocess.run(["squeue", "-h", "-u", os.environ.get("USER", ""), "-o", "%j"],
                         capture_output=True, text=True).stdout.split()
    return collections.Counter(out)


def submit(name: str, args: list[str], env: str, dry: bool) -> None:
    cmd = ["sbatch", "-J", name, *args, f"--export=ALL,{env}", str(POOL / "worker.sbatch")]
    if dry:
        say("would run:", " ".join(cmd))
        return
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(W.KIT))
    say(name, (r.stdout or r.stderr).strip())


def main() -> int:
    dry = "--dry" in sys.argv
    rows = W.tasks()
    finished = lambda t: (W.Q / "done" / t["name"]).exists() or (W.Q / "dead" / t["name"]).exists()  # noqa: E731
    pending = [t for t in rows if not finished(t)]
    if "--finished" in sys.argv:
        return 0 if not pending else 1
    claimed = [t for t in pending if (W.Q / "claim" / t["name"]).exists()]
    runnable = [t for t in pending if t not in claimed and W.deps_ok(t)]
    gpu_run = [t for t in runnable if t["vram"] > 0]
    gpu_busy = [t for t in claimed if t["vram"] > 0]
    short_run = [t for t in gpu_run if t["est"] <= 1]
    cpu_pending = [t for t in pending if t["vram"] == 0]
    have = jobs()
    say(f"pending {len(pending)} (runnable gpu {len(gpu_run)}, short {len(short_run)}, running gpu "
        f"{len(gpu_busy)}, cpu pending {len(cpu_pending)}); workers gpu {have['tgd-gpu']} "
        f"short {have['tgd-short']} cpu {have['tgd-cpu']}")

    want_gpu = min(GPU_WORKERS, len(gpu_run) + len(gpu_busy))
    for _ in range(max(0, want_gpu - have["tgd-gpu"])) if gpu_run else ():
        submit("tgd-gpu", ["-p", GPU_PARTITION, "--gres=gpu:1", "-t", "12:00:00"], "WORKER_WALL_H=12", dry)
    if short_run and not have["tgd-short"]:
        submit("tgd-short", ["-p", SHORT_PARTITION, f"--gres={SHORT_GRES}", "-t", "01:00:00", "-c", "8",
                             "--mem=64G"], "WORKER_WALL_H=1,MAX_EST_H=1,IDLE_EXIT=300", dry)
    if cpu_pending and not have["tgd-cpu"]:
        submit("tgd-cpu", ["-p", CPU_PARTITION, "-c", "8", "--mem=32G", "-t", "1-00:00:00"],
               "WORKER_KIND=cpu,WORKER_WALL_H=24,WORKER_THREADS=1", dry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
