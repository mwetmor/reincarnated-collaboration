#!/bin/bash
# C-9: cut the Grok RUN clips into 12-frame cells with the frozen oracle.video_cut,
# the same way the walks were cut. Conductor-authorised (queued run task).
#
# The tool auto-detects the stride period and, when it cannot evaluate one, emits a
# DIAGNOSTIC-ONLY strip and no game frames rather than guessing -- so a "success" exit
# code is not a successful cut, and this checks the emitted JSON, not $?. On a
# diagnostic-only result it retries with forced --period-frames candidates.
set -uo pipefail
BURST=$(cd "$(dirname "$0")/../../../.." && pwd)
cd "$BURST"
LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
DIRS=${DIRS:-"S SW NW N NE E SE"}
N=${N:-12}
FPS_OUT=${FPS_OUT:-24}
CANDS=${CANDS:-"48 40 36 32 56 64 28 44"}
for D in $DIRS; do
  CLIP="runs/C-9/xvideo/in/${D}_run.mp4"
  OUT="runs/C-9/p7/${D}_run"
  [ -f "$CLIP" ] || { echo "SKIP $D: no clip at $CLIP"; continue; }
  echo "== $D auto"
  R=$(python3 "$LOCK" C-9 -- python3 -m oracle.video_cut --clip "$CLIP" --kind run \
        --direction "$D" --n "$N" --fps-out "$FPS_OUT" --out "$OUT" 2>&1 | tail -1)
  echo "   $R"
  if echo "$R" | grep -q '"diagnostic_only": false'; then echo "   OK $D (auto)"; continue; fi
  DONE=0
  for P in $CANDS; do
    echo "== $D forced period $P"
    R=$(python3 "$LOCK" C-9 -- python3 -m oracle.video_cut --clip "$CLIP" --kind run \
          --direction "$D" --n "$N" --fps-out "$FPS_OUT" --out "${OUT}_p${P}" \
          --period-frames "$P" 2>&1 | tail -1)
    echo "   $R"
    if echo "$R" | grep -q '"diagnostic_only": false'; then
      echo "   OK $D (period $P)"; echo "$D $P" >> runs/C-9/cliffside_B/frames/run_cut_periods.txt; DONE=1; break
    fi
  done
  [ "$DONE" = 1 ] || echo "   *** $D UNCUT -- every candidate came back diagnostic-only"
done
echo "CUTS FINISHED"
