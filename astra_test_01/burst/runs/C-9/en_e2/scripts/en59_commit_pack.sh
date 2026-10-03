#!/bin/zsh
# EN-E2: commit ONE rendered pack's records (JSON/text only; never PNG/GLB/MP4) with --only, verify before/after, then append a
# run-ledger milestone. zsh scripts/en59_commit_pack.sh <g> <kit_id> "<subject>" "<milestone note>"
setopt NULL_GLOB
g=$1; K=$2; SUBJ=$3; NOTE=$4; C=~/Games/reincarnated-collaboration; R=astra_test_01/burst/runs/C-9; E=$R/en_e2
P=($R/join1_pack/$K/matrix_index.json $R/join1_render/kits/$K.json $R/join1_render/manifests/${K}_clips.json $E/work/raw_$K.json $E/work/sockets_$K.json
   $E/work/runtime_resample_$K.json $E/work/manifest_lint_$K.txt $E/work/stills_$g.json $E/work/film_$g.json $E/scripts/en58_pack.sh $E/scripts/en59_commit_pack.sh
   $E/work/radius_$K.json $E/scripts/en60_mx_adopt.py $E/scripts/en61_merge_graft.py $E/scripts/en62_radius_check.py $E/work/radius_en-fleshshaper.json $E/work/radius_en-ascended.json $E/work/wt_x.json $E/work/x_bridge_cut.json $E/work/${g}_mx_graft.json $E/work/${g}_graft.json $E/work/${g}_graft_rec.json $E/work/${g}_joint_mx.json $E/work/${g}_idle_blend.json
   $E/export/final_$g/en_${g}_measure.json $E/export/final_$g/height.json $E/work/${g}_tips.json $E/work/${g}_true_size.json $E/work/${g}_size_call.json $E/scripts/en33_kit_r4.py)
Q=(); for f in $P; do [ -e $C/$f ] && Q+=($f); done
git -C $C status --porcelain -- $Q
git -C $C add -- $Q && git -C $C commit -q --only $Q -m "$SUBJ" -m "$NOTE" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01FhV1VwxWAUupmAY9s5dLqz"
git -C $C show --stat HEAD | tail -1; SHA=$(git -C $C log -1 --format=%h); echo SHA $SHA
python3 - "$K" "$SHA" "$NOTE" <<'PY'
import json, fcntl, datetime, sys
K, sha, note = sys.argv[1:]; P = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/ledger.json'
with open(P.replace('ledger.json', '.ledger.lock'), 'a') as lk:
    fcntl.flock(lk, fcntl.LOCK_EX); d = json.load(open(P))
    d['milestones'].append(dict(id='M-C9-EN2-P2-%s' % K.upper().replace('EN-', ''), ts=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                                note='EN-E2 Phase 2 (collab %s): join1_pack/%s -- %s' % (sha, K, note)))
    with open(P, 'w') as f: json.dump(d, f, indent=2, ensure_ascii=False); f.write('\n')
print('ledger ok')
PY
