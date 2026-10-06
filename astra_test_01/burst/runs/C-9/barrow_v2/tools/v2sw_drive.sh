#!/bin/zsh
# barrow_v2 SW level ground paint (lane BS, drax, R-C9-159) = section_sw_drive.sh re-pointed: cfg paint/v1cam/cfg_v2sw.json, prefix BV2L, painter v2sw_paint.py (master crop), lane cap 60 (BV2L + BVM-wreck2)
# with the lane's guards): stage -> brief -> refs_guard -> wave.sh (parallel) -> check.
#   * one retry per chunk (SUF=-r1), a second (-r2) only while the lane cap allows; a third failure HALTs
#   * LANE CAP: Astra images used by BVP-* bursts (read from the ledger) + 2 per queued burst must stay <= CAP (150, R-C9-149a)
#   * USAGE LIMIT: any burst whose output/err mentions a usage/rate limit HALTs the drive at once (exit 7)
#   * disk gate 21 GiB; WAVE_MAX bursts per wave
# usage: bvp_drive.sh [max_waves]
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst; C=$B/runs/C-9/conductor_scripts
T=$B/runs/C-9/barrow_v2/tools; CFG=$B/runs/C-9/barrow_v2/paint/v1cam/cfg_v2sw.json
L=$HOME/astra-burst/logs/C-9; mkdir -p $L; LOG=$L/bv2l_drive.log
CAP=${CAP:-60}; WAVE_MAX=${WAVE_MAX:-8}; MAXW=${1:-999}
PFX=$(python3 -c "import json;print(json.load(open('$CFG'))['prefix'])")
cd $B; echo "$(date -u +%FT%TZ) BV2L DRIVE START cap=$CAP" >> $LOG; typeset -A tried; w=0
used() { python3 -c "import json;d=json.load(open('$B/runs/C-9/ledger.json'));print(sum(b.get('image_calls',0) for b in d['bursts'] if b['id'].split('-')[0] in ('BV2L','BV2M') or b['id']=='BVM-wreck2'))"; }
while [ $w -lt $MAXW ]; do
  FREE=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}')
  [ $FREE -lt 21 ] && { echo "$(date -u +%FT%TZ) HALT disk ${FREE} GiB < 21" >> $LOG; exit 9; }
  ready=($(ONLY="$ONLY" python3 $T/v2sw_paint.py $CFG ready))
  [ ${#ready} -eq 0 ] && { echo "$(date -u +%FT%TZ) BV2L DRIVE DONE (nothing ready) used=$(used)" >> $LOG; break; }
  ready=(${ready[1,$WAVE_MAX]})
  U=$(used); [ $(( U + 2 * ${#ready} )) -gt $CAP ] && { echo "$(date -u +%FT%TZ) HALT lane cap: used $U + 2x${#ready} > $CAP" >> $LOG; exit 8; }
  specs=()
  for k in $ready; do suf=""; [ -n "${tried[$k]}" ] && suf="-r${tried[$k]}"
    SUF=$suf python3 $T/v2sw_paint.py $CFG stage $k >> $LOG 2>&1; SUF=$suf python3 $T/v2sw_paint.py $CFG brief $k >> $LOG 2>&1
    python3 $C/refs_guard.py briefs/C-9/$PFX-$k$suf.task.json >> $LOG 2>&1 || { echo "$(date -u +%FT%TZ) HALT H-guard $PFX-$k$suf" >> $LOG; exit 3; }
    specs+=("$PFX-$k$suf:GENERATE"); done
  zsh $C/wave.sh bv2l_w$(date +%s) ${specs[@]}; w=$((w+1))
  for s in $specs; do bid=${s%%:*}; k=${bid#$PFX-}; k=${k%-r[0-9]}
    ex=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['exit'])" $L/${bid}_run.json 2>/dev/null)
    echo "$(date -u +%FT%TZ) $bid exit=$ex used=$(used)" >> $LOG
    if grep -qiE "usage limit|rate limit|weekly limit|quota|too many requests|limit reached" $L/${bid}_run.json $L/${bid}_run.err 2>/dev/null; then
      echo "$(date -u +%FT%TZ) HALT USAGE LIMIT seen in $bid" >> $LOG; exit 7; fi
    if [ "$ex" != "0" ]; then n=${tried[$k]:-0}; n=$((n+1)); [ $n -ge 3 ] && { echo "$(date -u +%FT%TZ) HALT: $k failed 3x" >> $LOG; exit 2; }; tried[$k]=$n; fi
  done
done
echo "$(date -u +%FT%TZ) BV2L DRIVE STOP after $w waves used=$(used)" >> $LOG
