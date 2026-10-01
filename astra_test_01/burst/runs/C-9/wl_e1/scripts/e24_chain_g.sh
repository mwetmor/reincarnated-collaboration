#!/bin/bash
# E1 STAGE G clip chain (supersedes e17 for the shipped body): the ready-diagonal CARRY and the re-sourced ATTACK.
#   carry  idle <- arm pose of Meshy 99 "Reaping Swing" @2.733 (grafted time); walk <- Meshy 4 "Attack" @0.333; run <- Meshy 4 @0.400 --
#          each the best of every key of 14 clips fetched on his rig, scored on tip-forward / head height / elevation /
#          fist spacing / no vertical stack (e23_carry_search.py; work/carry_search.json)
#   attack Meshy 4 "Attack" source window 0.333-2.333 s (contact ~40%; Heavy Hammer Swing landed at 96% with no follow-through)
set -e
export E1_RGRIP=0.50   # stage G: the right fist 0.50 m from the butt (e10 --rgrip 0.50)
cd "$(dirname "$0")/.."
python3 scripts/55_clip_graft.py graft export/wb/wl_rigged.glb work/g_c0.glb idle=anims/idle89.glb+loop+deroot walk=anims/walk21.glb+loop+deroot \
  run=anims/run14.glb+loop+deroot "attack=anims/attack4.glb@0.333:2.333" hit=anims/hit178.glb+deroot death=anims/death189.glb \
  "warcry=anims/shout101.glb@0.517:1.767+deroot" carry_r=anims/reap99.glb carry_a=anims/attack4.glb --json work/g_graft0.json | grep -c "graft:"
python3 scripts/e09_hold.py work/g_c0.glb work/g_c1a.glb --from carry_r@2.7333 --clips idle --json work/g_hold_idle.json
python3 scripts/e09_hold.py work/g_c1a.glb work/g_c1b.glb --from carry_a@0.3333 --clips walk --json work/g_hold_walk.json
python3 scripts/e09_hold.py work/g_c1b.glb work/g_c1.glb --from carry_a@0.4 --clips run --json work/g_hold_run.json
python3 - <<'PY'
import sys; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre')
js, b = L.load_glb('work/g_c1.glb'); js['animations'] = [a for a in js['animations'] if not (a['name'].startswith('Armature|') or a['name'].startswith('carry_'))]
R.write_glb('work/g_c1s.glb', js, bytearray(b)); print('clips', [a['name'] for a in js['animations']])
PY
python3 ../nb_join/scripts/j_joint_lint.py work/g_c1s.glb --clips idle,walk,run,attack,hit,death,warcry --ref hit,warcry --retargets none --layers work/layers_none.json --json work/g_joint_ref.json | grep "^MOVE" | cut -c1-48
python3 scripts/63_joint_fix.py work/g_c1s.glb work/g_c2a.glb work/g_joint_ref.json walk --dev-max 38 --json work/g_fix_walk.json | tail -1
python3 scripts/63_joint_fix.py work/g_c2a.glb work/g_c2.glb work/g_joint_ref.json attack --dev-max 38 --json work/g_fix_attack.json | tail -1
python3 scripts/e12_weapon.py work/g_c2.glb pieces/mace_rh.glb work/g_c3.glb pieces/mace.glb --json work/weapon.json | grep -A7 '"strike"'
python3 - <<'PY'
import sys, shutil; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre'); W = __import__('52_weapon_bones')
W.snap('pieces/mace.glb')
js, b = L.load_glb('work/g_c3.glb'); R.write_glb('export/wl_body.glb', js, bytearray(b)); shutil.copy('pieces/mace.glb', 'export/wl_mace.glb')
for f in ['export/wl_body.glb', 'export/wl_mace.glb']:
    r = L.lint(f); print(f, r['verdict'], r['fails'])
F = __import__('56_clip_fidelity'); reg = F.registry()
print('FIDELITY', [(r['clip'], r['status']) for r in F.check('export/wl_body.glb', reg)])
print('SEAMS', [(r['clip'], r['grid_status'], r['seam_status']) for r in F.seams('export/wl_body.glb', reg)])
PY
python3 ../nb_join/scripts/j_joint_lint.py export/wl_body.glb --clips idle,walk,run,attack,hit,death,warcry --ref hit,warcry --retargets none --layers work/layers_none.json --json work/joint_lint_final.json --neg | grep -E "^MOVE|NEGATIVE" | cut -c1-60
