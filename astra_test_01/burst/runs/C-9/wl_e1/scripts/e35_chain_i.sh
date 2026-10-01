#!/bin/bash
# E1 STAGE I/J clip chain (J adds the unarmed set): stage H's chain (e31, through the attack joint fix -> work/h_c2.glb), then
#   head_lift  idle: neck +9 deg, head +13 deg about his lateral axis (e33; chin -19 -> +3)
#   re-seat    the haft turned in the fists about the right fist, per clip (e12 E1_RESEAT): idle +2, run +10 deg
set -e
cd "$(dirname "$0")/.."
bash scripts/e31_chain_h.sh >/dev/null
python3 scripts/e33_head_lift.py work/h_c2.glb work/i_c2a.glb idle 9 13 --json work/i_head_lift.json
# STAGE J (3c): the UNARMED set, WHOLE (arms included, no carry): idle_unarmed <- Meshy 11 Idle 1 (+ the same head lift),
# walk_unarmed / run_unarmed <- the rig's own free walking / running
python3 scripts/55_clip_graft.py graft work/i_c2a.glb work/i_c2b.glb idle_unarmed=anims/idle11.glb+loop+deroot walk_unarmed=anims/free_walking.glb+loop+deroot \
  run_unarmed=anims/free_running.glb+loop+deroot --json work/j_graft_unarmed.json | grep -c "graft:"
python3 scripts/e33_head_lift.py work/i_c2b.glb work/i_c2.glb idle_unarmed 9 13 --json work/j_head_lift_unarmed.json
export E1_RGRIP=0.64 E1_RESEAT=idle:2,run:10
python3 scripts/e12_weapon.py work/i_c2.glb pieces/mace_rh.glb work/i_c3.glb pieces/mace.glb --json work/weapon.json | grep -E '"ASSERT"'
python3 - <<'PY'
import sys, shutil; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre'); W = __import__('52_weapon_bones')
W.snap('pieces/mace.glb')
js, b = L.load_glb('work/i_c3.glb'); js['animations'] = [a for a in js['animations'] if not a['name'].startswith('Armature|')]
R.write_glb('export/wl_body.glb', js, bytearray(b)); shutil.copy('pieces/mace.glb', 'export/wl_mace.glb')
for f in ['export/wl_body.glb', 'export/wl_mace.glb']:
    r = L.lint(f); print(f, r['verdict'], r['fails'])
F = __import__('56_clip_fidelity'); reg = F.registry()
print('FIDELITY', [(r['clip'], r['status']) for r in F.check('export/wl_body.glb', reg)])
print('SEAMS', [(r['clip'], r['grid_status'], r['seam_status'], round(r['closure_m'], 4)) for r in F.seams('export/wl_body.glb', reg)])
PY
python3 ../nb_join/scripts/j_joint_lint.py export/wl_body.glb --clips idle,walk,run,attack,hit,death,warcry --ref hit,warcry --retargets none --layers work/layers_none.json --json work/joint_lint_final.json --neg | grep -E "^MOVE|NEGATIVE" | cut -c1-60
# STAGE J: the unarmed run's right wrist (the free running's own: deviation 41 deg at one key) -> 38 (63_joint_fix), then all rows again
python3 ../nb_join/scripts/j_joint_lint.py export/wl_body.glb --clips idle_unarmed,walk_unarmed,run_unarmed --ref hit,warcry --retargets none --layers work/layers_none.json --json work/joint_lint_unarmed.json > /dev/null
python3 scripts/63_joint_fix.py export/wl_body.glb work/j_c4.glb work/joint_lint_unarmed.json run_unarmed --dev-max 38 --json work/j_fix_run_unarmed.json | tail -1
cp work/j_c4.glb export/wl_body.glb
python3 ../nb_join/scripts/j_joint_lint.py export/wl_body.glb --clips idle,walk,run,attack,hit,death,warcry,idle_unarmed,walk_unarmed,run_unarmed --ref hit,warcry --retargets none --layers work/layers_none.json --json work/joint_lint_final.json --neg | grep -E "^MOVE|NEGATIVE" | cut -c1-60
python3 scripts/e42_embed_tex.py export/wl_body.glb export/wl_body.glb work/tex_final.png   # stage J defect fix: the painted bake INTO the body
