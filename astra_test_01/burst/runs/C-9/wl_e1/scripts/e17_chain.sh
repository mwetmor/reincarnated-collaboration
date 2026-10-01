#!/bin/bash
# E1 clip chain, end to end (binary patches only; no Blender round trip of the body):
#   graft on source keys -> two-handed hold (idle, run) -> joint fix (attack L wrist) -> mace mount + per-clip channel -> strip Meshy's clip0
set -e
cd "$(dirname "$0")/.."
python3 scripts/55_clip_graft.py graft export/wb/wl_rigged.glb work/wl_c0.glb idle=anims/idle89.glb+loop+deroot walk=anims/walk21.glb+loop+deroot \
  run=anims/run14.glb+loop+deroot attack=anims/atk128.glb hit=anims/hit178.glb+deroot death=anims/death189.glb \
  "warcry=anims/shout101.glb@0.517:1.767+deroot" --json work/graft0.json | tail -2
python3 scripts/e09_hold.py work/wl_c0.glb work/wl_c1.glb --from walk --clips idle,run --json work/hold.json
python3 scripts/63_joint_fix.py work/wl_c1.glb work/wl_c1f.glb work/joint_lint_final.json attack --dev-max 38 --json work/joint_fix_attack.json | tail -1
python3 scripts/e12_weapon.py work/wl_c1f.glb pieces/mace_rh.glb work/wl_c2.glb pieces/mace.glb --json work/weapon.json | grep -A7 '"strike"'
python3 - <<'PY'
import sys, shutil; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre'); W = __import__('52_weapon_bones')
W.snap('pieces/mace.glb')
js, b = L.load_glb('work/wl_c2.glb'); js['animations'] = [a for a in js['animations'] if not a['name'].startswith('Armature|')]
R.write_glb('export/wl_body.glb', js, bytearray(b)); shutil.copy('pieces/mace.glb', 'export/wl_mace.glb')
for f in ['export/wl_body.glb', 'export/wl_mace.glb']:
    r = L.lint(f); print(f, r['verdict'], r['fails'])
PY
# --- final pass (2026-10-01 03:15): the joint-limit lint learns from a FIXED native reference set (walk, hit, warcry -- clips no
# edit touches), so fixing a clip cannot move the axes it is judged on; then the fix, then the weapon re-solved on the fixed keys
python3 ../nb_join/scripts/j_joint_lint.py export/wl_body.glb --clips idle,walk,run,attack,hit,death,warcry --ref walk,hit,warcry --retargets none --layers work/layers_none.json --json work/joint_lint_ref.json >/dev/null
python3 scripts/63_joint_fix.py export/wl_body.glb work/_jf1.glb work/joint_lint_ref.json attack --dev-max 38 --json work/joint_fix_attack2.json | tail -1
python3 scripts/e12_weapon.py work/_jf1.glb pieces/mace_rh.glb work/wl_c3.glb pieces/mace.glb --json work/weapon.json >/dev/null
python3 - <<'PY'
import sys, shutil; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre'); W = __import__('52_weapon_bones')
W.snap('pieces/mace.glb'); js, b = L.load_glb('work/wl_c3.glb'); js['animations'] = [a for a in js['animations'] if not a['name'].startswith('Armature|')]
R.write_glb('export/wl_body.glb', js, bytearray(b)); shutil.copy('pieces/mace.glb', 'export/wl_mace.glb')
PY
python3 ../nb_join/scripts/j_joint_lint.py export/wl_body.glb --clips idle,walk,run,attack,hit,death,warcry --ref walk,hit,warcry --retargets none --layers work/layers_none.json --json work/joint_lint_final.json --neg | grep -E "^MOVE|NEGATIVE"
