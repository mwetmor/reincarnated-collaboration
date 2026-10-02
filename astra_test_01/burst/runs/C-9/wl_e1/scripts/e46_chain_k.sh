#!/bin/bash
# E1 STAGE K (R-C9-123): the NARROWED BASE + the MIXAMO GREAT-SWORD set, as a CANDIDATE body for review (not yet shipped).
#   1  rig     the pass-2 narrowed body (e41) re-rigged via model_url -> builds/wl_rigged3.glb (+ the rig's free walk/run)
#   2  bones   weapon bones -> export/wb3/
#   3  clips   Mixamo family A (great sword idle / walk / run / attack), war cry <- power up, hit <- impact, death <- two-handed
#              death, plus idle_alt <- great sword idle (4); the unarmed set <- Idle 1 (re-fetched on rig 3, 3 cr) + free walk/run;
#              e40b (rest-aligned world-space), + head lift on the idles if their chin is down (measured first, not assumed)
#   4  joint lint (fixed native reference: hit, warcry) + 63 fixes; mace re-seated in the two-hand grip per clip (e12)
#   5  gear    helm/pauldrons/chest/cape refitted on rig 3 from the pass-2 isolations (e13 --iso-suffix _narrow_n2, cape fit-back)
#   6  painted + VALUE-GRADED texture embedded (e42 + e43), scale to 1.96 (e19) -> export/final_k_cand/
set -e
cd "$(dirname "$0")/.."
STEP=${1:-all}
if [ $STEP = all -o $STEP = rig ]; then
  python3 scripts/08_meshy.py rigfile builds/body_narrow2.glb 1.96 | tail -2
  python3 - <<'PY'
import json, subprocess
d = json.load(open('work/res_rig_tripo.json')); r = d['result']
subprocess.run(['curl', '-s', '-L', '-o', 'builds/wl_rigged3.glb', r['rigged_character_glb_url']], check=True)
for k in ('walking', 'running'): subprocess.run(['curl', '-s', '-L', '-o', 'anims/free3_%s.glb' % k, r['basic_animations']['%s_glb_url' % k]], check=True)
json.dump(d, open('work/res_rig_tripo_v3.json', 'w'), indent=1)
cs = json.load(open('work/clip_sources.json')); cs['body_rig_v2'] = cs['body_rig']
cs['body_rig'] = dict(meshy_rig_task=d['id'], glb='builds/wl_rigged3.glb', note='R-C9-123 pass 2: the narrowed base (e41 x2), re-rigged via model_url')
cs['clips'] = {}; json.dump(cs, open('work/clip_sources.json', 'w'), indent=1); print('rig3', d['id'])
PY
  cp work/res_rig_tripo_v1.json work/res_rig_tripo.json
  mkdir -p export/wb3; python3 scripts/52_weapon_bones.py --out export/wb3 builds/wl_rigged3.glb --json work/wb3.json | tail -1
  RIG=$(python3 -c "import json;print(json.load(open('work/clip_sources.json'))['body_rig']['meshy_rig_task'])")
  mkdir -p anims/rig3; ( cd anims/rig3 && ln -sf ../free3_walking.glb free_walking.glb && ln -sf ../free3_running.glb free_running.glb )
  python3 scripts/31_meshy_fetch.py $RIG idle11r3:11 | tail -2
fi
if [ $STEP = all -o $STEP = clips ]; then
  M=mixamo/glb
  python3 scripts/e40b_mixamo_graft.py graft export/wb3/wl_rigged3.glb work/k_c0.glb idle=$M/great_sword_idle.glb+loop+deroot \
    walk=$M/great_sword_walk.glb+loop+deroot run=$M/great_sword_run_2.glb+loop+deroot attack=$M/great_sword_slash_3.glb \
    warcry=$M/great_sword_power_up.glb+deroot hit=$M/great_sword_impact.glb+deroot death=$M/two_handed_sword_death.glb \
    idle_alt=$M/great_sword_idle_4.glb+deroot --json work/k_graft_mx.json | grep -c "graft:"
  python3 scripts/55_clip_graft.py graft work/k_c0.glb work/k_c1.glb idle_unarmed=anims/idle11r3.glb+loop+deroot \
    walk_unarmed=anims/free3_walking.glb+loop+deroot run_unarmed=anims/free3_running.glb+loop+deroot --json work/k_graft_unarmed.json | grep -c "graft:"
fi
if [ $STEP = all -o $STEP = finish ]; then
  ALL=idle,walk,run,attack,warcry,hit,death,idle_alt,idle_unarmed,walk_unarmed,run_unarmed
  python3 ../nb_join/scripts/j_joint_lint.py work/k_c1.glb --clips $ALL --ref hit,warcry --retargets none --layers work/layers_none.json --json work/k_joint_ref.json | grep "^MOVE" | cut -c1-48
  cp work/k_c1.glb work/k_c2.glb
  for c in $(python3 -c "import json;d=json.load(open('work/k_joint_ref.json'))['moves'];print(' '.join(k for k,v in d.items() if v['verdict']=='FAIL'))"); do
    python3 scripts/63_joint_fix.py work/k_c2.glb work/k_c2.glb work/k_joint_ref.json $c --dev-max 38 --json work/k_fix_$c.json | head -1
  done
  python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 -- blender -b -noaudio --python scripts/e10_mace_mount.py -- work/k_c2.glb builds/mace.glb pieces/mace_rh3.glb \
     --clip idle --t 1.0 --rgrip ${E1_RGRIP:-0.64} --faces 60000 --tex 1024 --json work/k_mace_mount.json | grep -c DECIMATE
  E1_RGRIP=${E1_RGRIP:-0.64} python3 scripts/e12_weapon.py work/k_c2.glb pieces/mace_rh3.glb work/k_c3.glb pieces/mace3.glb --json work/k_weapon.json | grep -E '"ASSERT"|head_bearing'
  python3 - <<'PY'
import sys, shutil, os; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre'); W = __import__('52_weapon_bones')
W.snap('pieces/mace3.glb'); os.makedirs('export/k', exist_ok=True)
js, b = L.load_glb('work/k_c3.glb'); js['animations'] = [a for a in js['animations'] if not a['name'].startswith('Armature|')]
R.write_glb('export/k/wl_body.glb', js, bytearray(b)); shutil.copy('pieces/mace3.glb', 'export/k/wl_mace.glb')
PY
  python3 scripts/e42_embed_tex.py export/k/wl_body.glb export/k/wl_body.glb work/tex_final_graded.png
  python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 -- blender -b -noaudio --python scripts/e13_gear.py -- export/k/wl_body.glb export/k --pieces helm,pauldrons,chest,cape \
     --iso-suffix _narrow_n2 --flare 0.20 --side 0.10 --thigh 0.65 --ramp hem --shin 0.4 --gap 0.03 --fit-back --clear 0.010 --top-drop 0.02 --json work/k_gear.json | grep -c "^GEAR"
  python3 scripts/e14_piece_mount.py export/k/wl_helm.glb export/k/wl_pauldrons.glb export/k/wl_chest.glb export/k/wl_cape.glb | grep -v "^  52"
  for c in violet ice; do python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 -- blender -b -noaudio --python scripts/e38_eye_glow.py -- export/k/wl_helm.glb export/k/wl_helm_$c.glb --strength 6 --band 0.12 | grep -c "^EYE"; done
fi
