#!/bin/zsh
# BV2F PT R-C9-384 NORTH BAND: ONE band chunk -> stage -> brief -> refs_guard (frozen) -> wave.sh (frozen) -> exit /
# usage-limit check -> image count. Disk >= 21 GiB; a usage-limit message HALTs (exit 7); a non-zero burst exit stops (2);
# the tranche cap (BV2F-N1, 10 images) is checked BEFORE firing: a burst may use 2 images, so it fires only if used + 2 <= 10
# (exit 6 otherwise: report before going over).
#   zsh fid/pt/tools/north_fire.sh <c 0..4> [SUF e.g. -r1]
set -u
FID=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
T=$FID/pt/tools; RG=$FID/v1tools/tierA/conductor_scripts/refs_guard.py; WAVE=$FID/v1tools/tierA/conductor_scripts/wave.sh
C=${1:?chunk}; SUF=${2:-}; BID=BV2F-N1-${C}_N$SUF; L=$HOME/astra-burst/logs/C-9; CAP=12   # R-C9-386: 10 -> 12 for 4_N
F=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ $F -ge 21 ] || { echo "HALT: disk ${F} GiB < 21"; exit 9; }
USED=$(python3 -c "import json;L=json.load(open('$B/runs/C-9/ledger.json'));print(sum(b.get('image_calls',0) for b in L['bursts'] if str(b.get('id','')).startswith('BV2F-N1-')))")
echo "disk ${F} GiB; images BV2F-N1 used $USED / $CAP"
[ $((USED + 2)) -le $CAP ] || { echo "STOP: $BID could take the tranche past $CAP ($USED used) -- report first"; exit 6; }
python3 $T/north_band.py stage $C $SUF || exit 3
python3 $T/north_band.py brief $C $SUF || exit 3
cd $B; source ~/.zshrc > /dev/null 2>&1
python3 $RG briefs/C-9/$BID.task.json || { echo "HALT: refs_guard $BID"; exit 3; }
zsh $WAVE BV2F-N1_w$(date +%s) $BID:GENERATE
ex=$(python3 -c "import json;print(json.load(open('$L/${BID}_run.json'))['exit'])" 2>/dev/null)
echo "$BID exit=$ex"
grep -qiE "usage limit|rate limit|weekly limit|quota|too many requests|limit reached" $L/${BID}_run.json $L/${BID}_run.err $HOME/astra-burst/runs/C-9/${BID}/events.jsonl 2>/dev/null && { echo "HALT USAGE LIMIT $BID"; exit 7; }
python3 -c "import json;L=json.load(open('$B/runs/C-9/ledger.json'));print('images BV2F-N1:',sum(b.get('image_calls',0) for b in L['bursts'] if str(b.get('id','')).startswith('BV2F-N1-')))"
[ "$ex" = "0" ] || { echo "STOP: $BID exit $ex"; exit 2; }
ls -la $B/runs/C-9/artifacts/$BID/ 2>/dev/null
