#!/bin/zsh
# EN-E2 round 3, THE WRAITH's clip chain: weapon bones -> Pro Magic graft (e40b) -> HOVER edit (en24: legs at rest in the shroud, lift +
# bob, glide, emerge, sinking death) -> joint lint (ref hit) + 63 fixes -> body GLB in export/w.
#   idle <- standing idle (loop) | cast_bolt <- 1H magic attack 01 (the 12 % projectile) | claw <- 2H magic attack 02 (both hands
#   forward 1.0 m, hips forward 0.2 m: the clawing lunge, melee 49 %) | aura <- 2H magic area attack 02 (arms out, span 1.37 m: the aura
#   19 % / aoe 14 %) | hit <- react small from front | death <- react large from front (+ en24's sink)   [measured: work/_w_cand.glb]
set -e
cd "$(dirname "$0")/.."; M=mixamo/glb
mkdir -p work/wb_w; python3 scripts/52_weapon_bones.py --out work/wb_w builds/en_w_rigged.glb --json work/wb_w.json | tail -1
python3 scripts/e40b_mixamo_graft.py graft work/wb_w/en_w_rigged.glb work/w_c0.glb idle=$M/standing_idle.glb+loop+deroot \
  cast_bolt=$M/standing_1h_magic_attack_01.glb+deroot claw=$M/standing_2h_magic_attack_02.glb+deroot aura=$M/standing_2h_magic_area_attack_02.glb+deroot \
  hit=$M/standing_react_small_from_front.glb+deroot death=$M/standing_react_large_from_front.glb+deroot --json work/w_graft.json | grep -E "^lint"
python3 scripts/en24_hover.py work/w_c0.glb work/w_c0h.glb --lift 0.38 --bob 0.035 --lean 14 --emerge-lean 50 --json work/w_hover.json | cut -c1-120
ALL=idle,glide,cast_bolt,claw,aura,hit,death,emerge
python3 ../nb_join/scripts/j_joint_lint.py work/w_c0h.glb --clips $ALL --ref hit --retargets none --layers ../wl_e1/work/layers_none.json --json work/w_joint_ref.json | grep "^MOVE" | cut -c1-70 || true
cp work/w_c0h.glb work/w_c1.glb
for c in $(python3 -c "import json;d=json.load(open('work/w_joint_ref.json'))['moves'];print(' '.join(k for k,v in d.items() if v['verdict']=='FAIL'))"); do
  python3 scripts/63_joint_fix.py work/w_c1.glb work/w_c1.glb work/w_joint_ref.json $c --dev-max 38 --json work/w_fix_$c.json | head -1
done
