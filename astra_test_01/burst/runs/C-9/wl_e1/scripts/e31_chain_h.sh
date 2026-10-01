#!/bin/bash
# E1 STAGE H clip chain (supersedes e24): the UPRIGHT BODY. idle <- Meshy 11 "Idle 1", walk <- the rig's own free "walking",
# run <- the rig's own free "running" (legs, hips, spine, head: the most upright sources measured, e30_posture); the ARMS in
# WORLD space from the G1 carry (e32_world_hold: the G1 body's idle@0.8 / walk@0.5 / run@0.3, kept in work/G1_body.glb).
# attack (Meshy 4 window), hit, death, war cry unchanged from stage G.
set -e
cd "$(dirname "$0")/.."
export E1_RGRIP=0.64   # stage H: 0.64 -- the upright idle holds the fists 0.56 m apart (at 0.50 the left fist was off the butt)
python3 scripts/55_clip_graft.py graft export/wb/wl_rigged.glb work/h_c0.glb idle=anims/idle11.glb+loop+deroot walk=anims/free_walking.glb+loop+deroot \
  run=anims/free_running.glb+loop+deroot "attack=anims/attack4.glb@0.333:2.333" hit=anims/hit178.glb+deroot death=anims/death189.glb \
  "warcry=anims/shout101.glb@0.517:1.767+deroot" --json work/h_graft0.json | grep -c "graft:"
python3 scripts/e32_world_hold.py work/h_c0.glb work/h_c1a.glb work/G1_body.glb idle@0.8 idle --json work/h_hold_idle.json
python3 scripts/e32_world_hold.py work/h_c1a.glb work/h_c1b.glb work/G1_body.glb walk@0.5 walk --json work/h_hold_walk.json
python3 scripts/e32_world_hold.py work/h_c1b.glb work/h_c1.glb work/G1_body.glb run@0.3 run --json work/h_hold_run.json
python3 ../nb_join/scripts/j_joint_lint.py work/h_c1.glb --clips idle,walk,run,attack,hit,death,warcry --ref hit,warcry --retargets none --layers work/layers_none.json --json work/h_joint_ref.json | grep "^MOVE" | cut -c1-48
python3 scripts/63_joint_fix.py work/h_c1.glb work/h_c2.glb work/h_joint_ref.json attack --dev-max 38 --json work/h_fix_attack.json | tail -1
python3 scripts/e12_weapon.py work/h_c2.glb pieces/mace_rh.glb work/h_c3.glb pieces/mace.glb --json work/weapon.json | grep -E '"ASSERT"|head_bearing|head_height'
python3 - <<'PY'
import sys, shutil; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre'); W = __import__('52_weapon_bones')
W.snap('pieces/mace.glb')
js, b = L.load_glb('work/h_c3.glb'); js['animations'] = [a for a in js['animations'] if not a['name'].startswith('Armature|')]
R.write_glb('export/wl_body.glb', js, bytearray(b)); shutil.copy('pieces/mace.glb', 'export/wl_mace.glb')
for f in ['export/wl_body.glb', 'export/wl_mace.glb']:
    r = L.lint(f); print(f, r['verdict'], r['fails'])
F = __import__('56_clip_fidelity'); reg = F.registry()
print('FIDELITY', [(r['clip'], r['status']) for r in F.check('export/wl_body.glb', reg)])
print('SEAMS', [(r['clip'], r['grid_status'], r['seam_status'], round(r['closure_m'], 4)) for r in F.seams('export/wl_body.glb', reg)])
PY
python3 ../nb_join/scripts/j_joint_lint.py export/wl_body.glb --clips idle,walk,run,attack,hit,death,warcry --ref hit,warcry --retargets none --layers work/layers_none.json --json work/joint_lint_final.json --neg | grep -E "^MOVE|NEGATIVE" | cut -c1-60
