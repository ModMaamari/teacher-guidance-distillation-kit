#!/usr/bin/env bash
# Re-judge every episode with two judges other than the primary one.
# Rule: the judge must never be the teacher, or "the teacher grades its own student".
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/../_common.sh"
SWAP_A="${SWAP_A:-oai-judge/mistralai/Mistral-Medium-3.5-128B}"
SWAP_B="${SWAP_B:-oai-judge/RedHatAI/gemma-4-31B-it-FP8-block}"
banner "exp03: judge swap"
echo "  primary : $JUDGE"
echo "  swap A  : $SWAP_A"
echo "  swap B  : $SWAP_B"
for m in "$TEACHER"; do
  case "$SWAP_A,$SWAP_B" in *"${m##*/}"*) echo "  !! swap judge shares a model with the teacher ($m)";; esac
done
echo
run_local $PY "$KIT/scripts/judge.py" --judge "$SWAP_A" \
    --episodes 'runs/eval/*/*/episodes.jsonl' --out runs/judge_swapA
run_local $PY "$KIT/scripts/judge.py" --judge "$SWAP_B" \
    --episodes 'runs/eval/*/*/episodes.jsonl' --out runs/judge_swapB
echo
echo "then: python 03_agreement.py --primary runs/judge/verdicts.jsonl \\"
echo "        --swap runs/judge_swapA/verdicts.jsonl runs/judge_swapB/verdicts.jsonl"
