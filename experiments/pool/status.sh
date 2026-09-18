#!/usr/bin/env bash
# One-screen view of the experiment pool. Read-only and quick: fine on a login node.
#   bash experiments/pool/status.sh          # summary
#   bash experiments/pool/status.sh <task>   # also the tail of that task's latest log
cd "$(dirname "$0")/../.."
Q=runs/pool/queue
total=$(grep -vc '^#' experiments/pool/tasks.tsv)
n() { find "$Q/$1" -mindepth 1 -maxdepth 1 2>/dev/null | wc -l; }
echo "== pool $(date -u +%FT%TZ): $total tasks | done $(n done) | running $(n claim) | dead $(n dead) | failed attempts $(n fail)"
echo "-- workers"
squeue -u "$USER" -n tgd-gpu,tgd-short,tgd-cpu,tgd-keeper -o "%.9i %.10j %.8T %.10M %.9l %.8P %R" 2>/dev/null
echo "-- running"
for c in "$Q"/claim/*/; do
  [ -d "$c" ] || continue
  t=$(basename "$c"); o=$(cat "$c/owner" 2>/dev/null)
  log=$(ls -t runs/pool/logs/task_"${t}"_*.log 2>/dev/null | head -1)
  printf '   %-22s job %-9s %s\n' "$t" "$o" "$( [ -n "$log" ] && tail -c 2000 "$log" | tr '\r' '\n' | grep -v '^\s*$' | tail -1 | cut -c1-110)"
done
echo "-- evaluation progress (runs/eval/*/*/status.json, unfinished)"
for s in runs/eval/*/*/status.json; do
  [ -f "$s" ] || continue; d=$(dirname "$s"); [ -f "$d/.done" ] && continue
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(f\"   {sys.argv[2]:<40} {d.get('done')}/{d.get('total')}  eta {d.get('eta_min')} min\")" "$s" "${d#runs/eval/}" 2>/dev/null
done
echo "-- dead (failed MAX_FAIL times; see runs/pool/queue/fail and the task logs)"
ls "$Q/dead" 2>/dev/null | sed 's/^/   /'
echo "-- recently done"
ls -t "$Q/done" 2>/dev/null | head -8 | while read -r t; do printf '   %-22s %s\n' "$t" "$(cat "$Q/done/$t")"; done
if [ -n "${1:-}" ]; then
  log=$(ls -t runs/pool/logs/task_"$1"_*.log 2>/dev/null | head -1)
  echo "-- $log"; [ -n "$log" ] && tail -25 "$log"
fi
exit 0
