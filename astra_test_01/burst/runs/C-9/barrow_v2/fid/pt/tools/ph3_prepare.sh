#!/bin/zsh
# BV2F PT (R-C9-278): PHASE 3' preparation and the DEV-25c A/B on the first chunk (3_0). Run step by step on the
# conductor's release; every step that writes images/canvases waits for disk >= 21 GiB.
#   zsh fid/pt/tools/ph3_prepare.sh pins | copies | ab_stage | ab_fire | ab_promote <A|B>
set -u
FID=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst; A9=$B/runs/C-9/artifacts
CFG=$FID/pt/pilot/cfg_bv2a_ph3.json; GP=$FID/v1tools/tierB/conductor_scripts/guided_paint.py; RG=$FID/v1tools/tierA/conductor_scripts/refs_guard.py
WAVE=$FID/v1tools/tierA/conductor_scripts/wave.sh
disk() { F=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ $F -ge 21 ] || { echo "HALT: disk ${F} GiB < 21"; exit 9; }; }
case ${1:?step} in
  pins)   # B-2: guide + ID + class copies and the 25 tiles from LV b5894d440; the 9 pilot tiles must be unchanged
    python3 $FID/pt/tools/ph3_pin.py b5894d440 R-C9-278 && python3 $FID/pt/tools/pilot_pins_check.py ;;
  copies) # the 9 pilot canvases as BV2F-PH3-<k> byte copies (the frozen driver's done() and the stitch's src())
    disk
    python3 - <<PY
import json, hashlib, os, shutil
A='$A9'; m=json.load(open('$FID/pt/pilot/build_manifest_ps4.json'))
for k, v in m['chunks'].items():
    d = A + '/BV2F-PH3-' + k; os.makedirs(d, exist_ok=True); dst = d + '/BV2F-PH3-%s.png' % k
    shutil.copyfile(A + '/' + v['file'], dst); s = hashlib.sha256(open(dst, 'rb').read()).hexdigest(); assert s == v['sha256']
    json.dump({'_what': "R-C9-278: the KEPT pilot-4 canvas COPIED byte for byte (Phase 3' prefix); nothing painted here", 'copy_of': v['file'], 'sha256': s}, open(d + '/COPY.json', 'w'), indent=1)
print('9 pilot copies OK')
PY
    ;;
  ab_stage) # both arms of chunk 3_0: A = v1 paste (DEV-25c unset), B = inner-128 (BV2F_DEV25C=1); DEV-28 on (cfg dev28_ids)
    disk; cd $B
    python3 $FID/v1tools/cfg_check.py $CFG || exit 9
    SUF=-ab25cA BV2F_DEV28=1 python3 $GP $CFG stage 3_0 && SUF=-ab25cA python3 $GP $CFG brief 3_0
    SUF=-ab25cB BV2F_DEV28=1 BV2F_DEV25C=1 python3 $GP $CFG stage 3_0 && SUF=-ab25cB BV2F_DEV25C=1 python3 $GP $CFG brief 3_0
    python3 $RG briefs/C-9/BV2F-PH3-3_0-ab25cA.task.json briefs/C-9/BV2F-PH3-3_0-ab25cB.task.json ;;
  ab_fire)  # +2 images (one per arm; each keeps v1's one-retry rule inside the burst)
    disk; cd $B; source ~/.zshrc > /dev/null 2>&1
    zsh $WAVE BV2F-PH3ab_w$(date +%s) BV2F-PH3-3_0-ab25cA:GENERATE BV2F-PH3-3_0-ab25cB:GENERATE ;;
  ab_promote) # after the pre-registered rule is read (PH a1 band E, 1:1 crops, P6a): the winner becomes BV2F-PH3-3_0
    W=${2:?A or B}; disk
    mkdir -p $A9/BV2F-PH3-3_0; cp $A9/BV2F-PH3-3_0-ab25c$W/BV2F-PH3-3_0.png $A9/BV2F-PH3-3_0/BV2F-PH3-3_0.png
    python3 -c "
import json,hashlib;p='$A9/BV2F-PH3-3_0/BV2F-PH3-3_0.png';json.dump({'_what':'R-C9-278: DEV-25c A/B WINNER arm $W, byte copy','copy_of':'BV2F-PH3-3_0-ab25c$W','sha256':hashlib.sha256(open(p,'rb').read()).hexdigest()},open('$A9/BV2F-PH3-3_0/COPY.json','w'),indent=1)
c=json.load(open('$CFG'))
if '$W'=='A': c['dev25c_chunks']=[]
json.dump(c,open('$CFG','w'),indent=1,ensure_ascii=False); print('winner $W; dev25c_chunks', c['dev25c_chunks'])" ;;
  wave)   # ONE wave (the conductor releases wave by wave): the frozen driver's per-chunk steps -- guided_paint stage ->
          # brief -> refs_guard -> wave.sh (parallel) -> exit check; a non-zero exit gets ONE retry (-r1), a second HALTs;
          # a usage-limit message HALTs (exit 7). DEV-28 on (cfg dev28_ids); DEV-25c from the cfg list (empty = off).
    shift; disk; cd $B; source ~/.zshrc > /dev/null 2>&1
    python3 $FID/v1tools/cfg_check.py $CFG || exit 9
    bash $FID/v1tools/verify.sh > /dev/null || { echo "HALT: verify"; exit 8; }
    export BV2F_DEV28=1
    if python3 -c "import json,sys;sys.exit(0 if json.load(open('$CFG')).get('dev25c_chunks') else 1)"; then export BV2F_DEV25C=1; else unset BV2F_DEV25C; fi
    L=$HOME/astra-burst/logs/C-9
    for suf in "" "-r1"; do
      specs=()
      for k in $@; do
        if [ -n "$suf" ]; then ex=$(python3 -c "import json;print(json.load(open('$L/BV2F-PH3-$k''_run.json'))['exit'])" 2>/dev/null); [ "$ex" = "0" ] && continue; fi
        SUF=$suf python3 $GP $CFG stage $k && SUF=$suf python3 $GP $CFG brief $k || { echo "HALT: stage/brief $k$suf"; exit 3; }
        python3 $RG briefs/C-9/BV2F-PH3-$k$suf.task.json || { echo "HALT: refs_guard $k$suf"; exit 3; }
        specs+=("BV2F-PH3-$k$suf:GENERATE")
      done
      [ ${#specs} -eq 0 ] && break
      zsh $WAVE BV2F-PH3_w$(date +%s) ${specs[@]}
      for s in $specs; do bid=${s%%:*}
        ex=$(python3 -c "import json;print(json.load(open('$L/${bid}_run.json'))['exit'])" 2>/dev/null)
        echo "$bid exit=$ex"
        grep -qiE "usage limit|rate limit|weekly limit|quota|too many requests|limit reached" $L/${bid}_run.json $L/${bid}_run.err 2>/dev/null && { echo "HALT USAGE LIMIT $bid"; exit 7; }
        [ "$ex" != "0" ] && [ "$suf" = "-r1" ] && { echo "HALT: $bid failed twice"; exit 2; }
      done
    done
    python3 -c "import json;L=json.load(open('$B/runs/C-9/ledger.json'));print('images BV2F-PH3:',sum(b.get('image_calls',0) for b in L['bursts'] if str(b.get('id','')).startswith('BV2F-PH3-')))" ;;
esac
