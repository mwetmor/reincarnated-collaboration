#!/bin/bash
# E1 STAGE I clip chain: stage H's chain (e31, through the attack joint fix -> work/h_c2.glb), then
#   head_lift  idle: neck +9 deg, head +13 deg about his lateral axis (e33; chin -19 -> +3)
#   re-seat    the haft turned in the fists about the right fist, per clip (e12 E1_RESEAT): idle +2, run +10 deg
set -e
cd "$(dirname "$0")/.."
bash scripts/e31_chain_h.sh >/dev/null
python3 scripts/e33_head_lift.py work/h_c2.glb work/i_c2.glb idle 9 13 --json work/i_head_lift.json
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
