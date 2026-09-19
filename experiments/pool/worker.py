"""Queue worker for the experiment pool. One Slurm job = one worker.

Tasks come from experiments/pool/tasks.tsv (re-read every cycle, so tasks can be added while
workers run). A GPU worker runs tasks with vram_gb > 0 and packs them onto its GPU; a CPU
worker (no GPU visible, or WORKER_KIND=cpu) runs tasks with vram_gb = 0 (API calls, splits,
tables). A worker starts a task when

  * it is not done, dead, or claimed by a live job,
  * its dependencies hold: ``done:<task>``, or ``file:<path>`` that exists and has not changed
    for 2 minutes (paths relative to the kit root),
  * it fits: summed VRAM (measured peaks replace the tsv guesses once known), host RAM and
    CPU slots (WORKER_THREADS per task), and a non-resumable task's estimate fits the
    remaining walltime (resumable tasks need 30 minutes).

Claims are atomic mkdirs in runs/pool/queue/claim/. A failed task is retried until it has
failed MAX_FAIL times (default 5), at least 2 minutes apart, then marked dead. Each task runs from a snapshot copy of
run_task.sh (runs/pool/snap/), so the script can be edited while workers run. On SIGUSR1 (Slurm, before the walltime) the worker stops its tasks and releases
their claims. A GPU worker exits after IDLE_EXIT seconds with nothing to run; a CPU worker
stays while any task of its kind is still pending, because upstream GPU work will unblock it.
MAX_EST_H skips tasks estimated longer than that (the 1-hour `short` workers run evals, and with
CHUNK_RESUMABLE=1 also resumable tasks, in chunks).

    python experiments/pool/worker.py --dry     # show what would start, start nothing
"""
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

POOL = Path(__file__).resolve().parent
KIT = POOL.parents[1]
Q = KIT / "runs" / "pool" / "queue"
LOGS = KIT / "runs" / "pool" / "logs"
for d in ("claim", "done", "fail", "dead"):
    (Q / d).mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)
JOB = os.environ.get("SLURM_JOB_ID", f"local{os.getpid()}")
DRY = "--dry" in sys.argv
THREADS = int(os.environ.get("WORKER_THREADS", "4"))
START = time.time()
WALL_S = float(os.environ.get("WORKER_WALL_H", "12")) * 3600
MAX_EST_H = float(os.environ.get("MAX_EST_H", "1e9"))
CHUNK = os.environ.get("CHUNK_RESUMABLE", "0") == "1"   # also take resumable tasks longer than MAX_EST_H
MAX_FAIL = int(os.environ.get("MAX_FAIL", "5"))
RETRY_AFTER_S = 120   # a failed task waits this long before a retry (transient storage or API stalls)
SNAP = KIT / "runs" / "pool" / "snap"
SNAP.mkdir(parents=True, exist_ok=True)
CPUS = int(os.environ.get("SLURM_CPUS_PER_TASK", "8"))
RAM_GB = int(os.environ.get("SLURM_MEM_PER_NODE", "65536")) / 1024
running = {}  # name -> dict(proc, vram, ram, t0, peak)
stopping = False


def log(*a):
    print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), f"[{JOB}]", *a, flush=True)


def gpu_info():
    if os.environ.get("WORKER_KIND") == "cpu":
        return "cpu", 0.0
    if DRY:
        return "DRY-GPU", float(os.environ.get("DRY_VRAM", "80"))
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        out = []
    if not out:
        return "cpu", 0.0
    name, mem = [x.strip() for x in out[0].split(",")]
    return name, float(mem) / 1024


def tasks():
    rows = []
    for line in open(POOL / "tasks.tsv", encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        name, vram, ram, est, res, deps = line.rstrip("\n").split("\t")
        rows.append(dict(name=name, vram=float(vram), ram=float(ram), est=float(est), resumable=res == "1",
                         deps=[] if deps == "-" else deps.split(",")))
    return rows


def measured():
    p, m = Q / "peaks.tsv", {}
    if p.exists():
        for line in open(p, encoding="utf-8"):
            n, g = line.split("\t")[:2]
            m[n] = max(m.get(n, 0.0), float(g))
    return m


def live_jobs():
    out = subprocess.run(["squeue", "-h", "-u", os.environ.get("USER", ""), "-t", "RUNNING", "-o", "%A"],
                         capture_output=True, text=True).stdout.split()
    return set(out)


_last_release = [0.0]


def release_stale():
    if time.time() - _last_release[0] < 300:   # squeue at most every 5 minutes per worker
        return
    _last_release[0] = time.time()
    alive = live_jobs()
    for c in (Q / "claim").iterdir():
        owner = (c / "owner").read_text(encoding="utf-8").strip() if (c / "owner").exists() else ""
        if owner and not owner.startswith("local") and owner not in alive and owner != JOB:
            log("releasing stale claim", c.name, "of job", owner)
            (c / "owner").unlink(missing_ok=True)
            try:
                c.rmdir()
            except OSError:
                pass


def deps_ok(t):
    for d in t["deps"]:
        kind, _, val = d.partition(":")
        if kind == "done" and not (Q / "done" / val).exists():
            return False
        if kind == "file":
            p = KIT / val
            if not p.exists() or time.time() - p.stat().st_mtime < 120:
                return False
    return True


def claim(name):
    try:
        (Q / "claim" / name).mkdir()
    except FileExistsError:
        return False
    (Q / "claim" / name / "owner").write_text(JOB, encoding="utf-8")
    return True


def unclaim(name):
    c = Q / "claim" / name
    (c / "owner").unlink(missing_ok=True)
    try:
        c.rmdir()
    except OSError:
        pass


def sample_peaks():
    if DRY or not running or GMEM == 0:
        return
    out = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,used_memory", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True).stdout
    by_pgid = {}
    for line in out.strip().splitlines():
        try:
            pid, mb = [int(x) for x in line.split(",")]
            g = os.getpgid(pid)
            by_pgid[g] = by_pgid.get(g, 0) + mb / 1024
        except (ValueError, ProcessLookupError, PermissionError):
            continue
    for r in running.values():
        r["peak"] = max(r["peak"], by_pgid.get(r["proc"].pid, 0.0))


def on_usr1(*_):
    global stopping
    stopping = True
    log("walltime signal: stopping tasks and releasing claims")
    for r in running.values():
        try:
            os.killpg(r["proc"].pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    time.sleep(30)
    for name, r in running.items():
        try:
            os.killpg(r["proc"].pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        unclaim(name)
    sys.exit(0)


def mine(t):
    """GPU workers take GPU tasks, CPU workers take CPU tasks."""
    return (t["vram"] > 0) == (GMEM > 0)


def main():
    global GMEM
    signal.signal(signal.SIGUSR1, on_usr1)
    gname, GMEM = gpu_info()
    idle_exit = float(os.environ.get("IDLE_EXIT", "1200"))
    log(f"worker start kind={'gpu' if GMEM else 'cpu'} gpu={gname} vram={GMEM:.0f}GB cpus={CPUS} "
        f"ram={RAM_GB:.0f}GB wall={WALL_S / 3600:.1f}h")
    idle_since = None
    while True:
        release_stale()
        sample_peaks()
        for name, r in list(running.items()):
            rc = r["proc"].poll()
            if rc is None:
                continue
            el = (time.time() - r["t0"]) / 3600
            with open(Q / "peaks.tsv", "a", encoding="utf-8") as fh:
                fh.write(f"{name}\t{r['peak']:.2f}\t{el:.3f}\t{gname}\t{JOB}\t{rc}\n")
            if rc == 0:
                (Q / "done" / name).write_text(json.dumps(dict(job=JOB, gpu=gname, hours=round(el, 3),
                                                               peak_gb=round(r["peak"], 2))), encoding="utf-8")
                log(f"done {name} in {el:.2f}h peak {r['peak']:.1f}GB")
            else:
                n = len(list((Q / "fail").glob(name + ".*"))) + 1
                (Q / "fail" / f"{name}.{n}").write_text(f"job {JOB} rc {rc} after {el:.2f}h\n", encoding="utf-8")
                if n >= MAX_FAIL:
                    (Q / "dead" / name).write_text(f"failed {n} times\n", encoding="utf-8")
                log(f"FAILED {name} rc={rc} attempt {n}{' -> dead' if n >= MAX_FAIL else ''}")
            unclaim(name)
            del running[name]

        left = WALL_S - (time.time() - START)
        peaks = measured()
        need = lambda t: max(t["vram"], 1.1 * peaks[t["name"]]) if t["name"] in peaks else t["vram"]  # noqa: E731
        used_v = sum(r["vram"] for r in running.values())
        used_r = sum(r["ram"] for r in running.values())
        todo = [t for t in tasks() if mine(t) and (t["est"] <= MAX_EST_H or (CHUNK and t["resumable"]))
                and not (Q / "done" / t["name"]).exists()
                and not (Q / "dead" / t["name"]).exists()]
        started = False
        n_run = len(running)
        for t in todo:
            if stopping or n_run >= max(1, CPUS // THREADS):
                break
            if t["name"] in running or (Q / "claim" / t["name"]).exists() or not deps_ok(t):
                continue
            fails = list((Q / "fail").glob(t["name"] + ".*"))
            if fails and time.time() - max(f.stat().st_mtime for f in fails) < RETRY_AFTER_S:
                continue
            v = need(t)
            if n_run and ((GMEM and used_v + v > GMEM - 2) or used_r + t["ram"] > RAM_GB - 4):
                if GMEM and v <= GMEM - 2:
                    break  # strict priority: wait for room rather than let lower tasks overtake
                continue
            if not t["resumable"] and 1.3 * t["est"] * 3600 > left:
                continue
            if t["resumable"] and left < 1800:
                continue
            if not claim(t["name"]):
                continue
            logf = LOGS / f"task_{t['name']}_{JOB}.log"
            log(f"start {t['name']} (vram {v:.0f}GB, ram {t['ram']:.0f}GB; in use {used_v:.0f}/{GMEM:.0f}GB)")
            used_v += v
            used_r += t["ram"]
            n_run += 1
            if DRY:
                unclaim(t["name"])
                continue
            env = dict(os.environ, OMP_NUM_THREADS=str(THREADS), MKL_NUM_THREADS=str(THREADS), POOL_TASK=t["name"],
                       POOL_KIT=str(KIT))
            snap = SNAP / f"run_task_{t['name']}_{JOB}.sh"
            snap.write_text((POOL / "run_task.sh").read_text(encoding="utf-8"), encoding="utf-8")
            proc = subprocess.Popen(["bash", str(snap), t["name"]], stdout=open(logf, "a", encoding="utf-8"),
                                    stderr=subprocess.STDOUT, env=env, start_new_session=True, cwd=str(KIT))
            running[t["name"]] = dict(proc=proc, vram=v, ram=t["ram"], t0=time.time(), peak=0.0)
            started = True
        if DRY:
            log("dry run finished")
            return
        if not todo and not running:
            log("nothing left for this kind of worker; exiting")
            return
        if running or started:
            idle_since = None
        elif GMEM:  # CPU workers wait for upstream GPU work instead of timing out
            idle_since = idle_since or time.time()
            if time.time() - idle_since > idle_exit:
                log("nothing runnable for", idle_exit, "s; exiting")
                return
        time.sleep(30)


GMEM = 0.0
if __name__ == "__main__":
    main()
