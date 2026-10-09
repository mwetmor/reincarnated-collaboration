#!/bin/zsh
# BV2F PT SEA PASS (R-C9-321): ONE DEV-24 patch -> spec (base = the current sea-pass base) -> stage -> brief -> refs_guard
# -> wave.sh -> exit / usage-limit check -> paste (local_repaint) -> crops. Accept separately (sea_pass.py accept) after
# the by-eye read. Disk >= 21 GiB; a usage-limit message HALTs (exit 7); a non-zero burst exit stops (exit 2).
#   zsh fid/pt/tools/sea_fire.sh <name> [attempt=1] [image_cap=1]
set -u
FID=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
T=$FID/pt/tools; RG=$FID/v1tools/tierA/conductor_scripts/refs_guard.py; WAVE=$FID/v1tools/tierA/conductor_scripts/wave.sh
N=${1:?name}; ATT=${2:-1}; CAP=${3:-1}; BID=BV2F-LR4-$N-$ATT; SP=$FID/pt/dev24/spec_$N.json; L=$HOME/astra-burst/logs/C-9
F=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ $F -ge 21 ] || { echo "HALT: disk ${F} GiB < 21"; exit 9; }
echo "disk ${F} GiB"
python3 $T/sea_pass.py spec $N $ATT $CAP || exit 3
python3 $T/local_repaint.py $SP stage $ATT || exit 3
python3 $T/local_repaint.py $SP brief $ATT || exit 3
cd $B; source ~/.zshrc > /dev/null 2>&1
python3 $RG briefs/C-9/$BID.task.json || { echo "HALT: refs_guard $BID"; exit 3; }
zsh $WAVE BV2F-LR4sea_w$(date +%s) $BID:GENERATE
ex=$(python3 -c "import json;print(json.load(open('$L/${BID}_run.json'))['exit'])" 2>/dev/null)
echo "$BID exit=$ex"
grep -qiE "usage limit|rate limit|weekly limit|quota|too many requests|limit reached" $L/${BID}_run.json $L/${BID}_run.err $HOME/astra-burst/runs/C-9/${BID}/events.jsonl 2>/dev/null && { echo "HALT USAGE LIMIT $BID"; exit 7; }
[ "$ex" = "0" ] || { echo "STOP: $BID exit $ex"; exit 2; }
python3 $T/local_repaint.py $SP paste $ATT || exit 4
python3 $T/local_repaint.py $SP pin $ATT > /dev/null || exit 4
python3 -c "import json;L=json.load(open('$B/runs/C-9/ledger.json'));print('images BV2F-LR4:',sum(b.get('image_calls',0) for b in L['bursts'] if str(b.get('id','')).startswith('BV2F-LR4-')))"
