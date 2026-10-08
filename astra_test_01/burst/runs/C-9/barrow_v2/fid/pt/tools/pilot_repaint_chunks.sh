#!/bin/zsh
# BV2F PT (R-C9-242): REPAINT named chunks, in the order given, each as the frozen driver paints a retry (SUF=-r1:
# stage -> brief -> refs_guard -> wave.sh, the FROZEN copies only), so guided_paint/guided_stitch's src() then reads the
# -r1 canvas. One chunk at a time (each repaint is the next one's context). Gates as pilot_paint.sh; cap counted from the
# ledger by prefix; usage-limit text -> exit 7 (HALT); a non-zero burst -> exit 6 (no second attempt).
#   zsh fid/pt/tools/pilot_repaint_chunks.sh <cfg.json> <cap> <k> [<k> ...]
set -u
FID=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid
V=$FID/v1tools; A=$V/tierA/conductor_scripts
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
LED=$B/runs/C-9/ledger.json
CFG=$1; CAP=$2; shift 2
source ~/.zshrc > /dev/null 2>&1
P=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['prefix'])" $CFG)
L=$HOME/astra-burst/logs/C-9; mkdir -p $L; LOG=$L/${P}_repaint.log
used() { python3 -c "import json;print(sum(b.get('image_calls',0) for b in json.load(open('$LED'))['bursts'] if str(b.get('id','')).startswith('$P-')))"; }
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ $FREE -ge 21 ] || { echo "HALT: disk ${FREE} GiB < 21"; exit 9; }
python3 $FID/pt/tools/pilot_pins_check.py || { echo "HALT: pins"; exit 10; }
python3 $V/cfg_check.py $CFG || { echo "HALT: cfg_check"; exit 9; }
bash $V/verify.sh || { echo "HALT: verify"; exit 8; }
cd $B
for k in "$@"; do
  u=$(used); [ $u -lt $CAP ] || { echo "HALT: images $u >= cap $CAP before $k"; exit 6; }
  echo "$(date -u +%FT%TZ) $P-$k-r1 REPAINT (images before: $u, cap $CAP)" | tee -a $LOG
  SUF=-r1 python3 $V/tierB/conductor_scripts/guided_paint.py $CFG stage $k >> $LOG 2>&1 || { echo "HALT: stage $k"; exit 4; }
  SUF=-r1 python3 $V/tierB/conductor_scripts/guided_paint.py $CFG brief $k >> $LOG 2>&1 || { echo "HALT: brief $k"; exit 4; }
  python3 $A/refs_guard.py briefs/C-9/$P-$k-r1.task.json >> $LOG 2>&1 || { echo "HALT: refs_guard $k"; exit 3; }
  zsh $A/wave.sh "${P}_rp$(date +%s)" "$P-$k-r1:GENERATE"
  bid=$P-$k-r1
  ex=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['exit'])" $L/${bid}_run.json 2>/dev/null)
  echo "$(date -u +%FT%TZ) $bid exit=$ex" | tee -a $LOG
  if grep -qiE "usage limit|rate limit|weekly limit|quota|too many requests|limit reached" $L/${bid}_run.json $L/${bid}_run.err 2>/dev/null; then
    echo "HALT USAGE LIMIT seen in $bid" | tee -a $LOG; exit 7; fi
  [ "$ex" = "0" ] || { echo "HALT: $bid exit $ex"; exit 6; }
done
echo "DONE; images used by $P: $(used) (cap $CAP)"
