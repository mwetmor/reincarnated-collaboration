#!/bin/zsh
# BV2F Phase 2' pilot paint launcher (lane PT, R-C9-191). Gates, then the FROZEN driver, under a cap/failure watcher.
#   zsh fid/pt/tools/pilot_paint.sh
# Gates (any failure -> no burst): disk >= 21 GiB; pilot_pins_check; cfg_check; verify.sh (the driver runs the last two again).
# Watcher: the frozen driver retries a failed chunk once (v1's two-attempt rule) and has no image cap. The Ph2' cap is
# 18 images = 9 chunks x 2, so a driver-level retry cannot fit: on the FIRST non-zero burst exit the watcher stops the
# driver (between waves) and HALTs (exit 6). Usage limit -> the driver's own exit 7. Images are read from the ledger.
FID=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid
CFG=${1:-$FID/pt/pilot/cfg_bv2a_pilot.json}; DRV=$FID/v1tools/tierB/conductor_scripts/t10bf_drive.sh
LED=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/ledger.json
PFX=$(python3 -c "import json;print(json.load(open('$CFG'))['prefix'])")   # BV2F-PR for the Phase 2'' repaint (R-C9-210)
L=$HOME/astra-burst/logs/C-9; DLOG=$L/${PFX}_drive.log; CAP=${2:-18}   # R-C9-245: cap as the 2nd arg (PS3: 24)
source ~/.zshrc > /dev/null 2>&1
used() { python3 -c "import json;print(sum(b.get('image_calls',0) for b in json.load(open('$LED'))['bursts'] if str(b.get('id','')).startswith('$PFX-')))"; }
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ $FREE -ge 21 ] || { echo "HALT: disk ${FREE} GiB < 21"; exit 9; }
python3 $FID/pt/tools/pilot_pins_check.py || { echo "HALT: pins"; exit 10; }
python3 $FID/v1tools/cfg_check.py $CFG || { echo "HALT: cfg_check"; exit 9; }
bash $FID/v1tools/verify.sh || { echo "HALT: verify"; exit 8; }
echo "images used by $PFX before: $(used) (cap $CAP)"
mkdir -p $L; START=$(wc -l < $DLOG 2>/dev/null || echo 0)
zsh $DRV $CFG &
PID=$!
while kill -0 $PID 2>/dev/null; do
  if tail -n +$((START+1)) $DLOG 2>/dev/null | grep -E "$PFX-[0-9]_[0-9](-r1)? exit=" | grep -vq 'exit=0$'; then
    kill $PID 2>/dev/null; wait $PID 2>/dev/null
    echo "HALT: a pilot burst exited non-zero; driver stopped before any retry (cap $CAP). images used: $(used)"
    tail -n +$((START+1)) $DLOG | grep -E 'exit=|HALT'; exit 6
  fi
  u=$(used); if [ $u -gt $CAP ]; then kill $PID; echo "HALT: images $u > cap $CAP"; exit 6; fi
  sleep 3
done
wait $PID; rc=$?
echo "driver exit=$rc; images used by $PFX: $(used) (cap $CAP)"
tail -n +$((START+1)) $DLOG | grep -E 'exit=|HALT|DONE'
exit $rc
