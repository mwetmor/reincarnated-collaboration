#!/bin/zsh
cd "$(dirname "$0")"
until grep -q "DONE" out/run_ta.log 2>/dev/null; do
  pgrep -f run_ta.py >/dev/null || { echo "RUN-DIED"; exit 1; }
  sleep 30
done
echo "=== T-A COMPLETE: $(grep -c ' ok ' out/run_ta.log)/26 ==="
grep "ERR" out/run_ta.log || echo "no errors"
python3 impact_frames.py > out/impact_frames.log 2>&1
python3 finalize.py
echo "=== FINALIZED ==="
