#!/bin/zsh
# R-C9-138/140: the kit of record (ss134f) -> ss138a: calmer idle (spine pitch), the orb staff aimed along her facing by the
# hand + forearm twist (the grip untouched), the Fire Ball's orb leading, idle_ss4 (Mixamo sword-and-shield idle 4) as the
# alternate idle, and the hood_hair morph. Pieces copied byte-identical from ss134f.
set -e
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/so_mx; cd $R
IDLES=${IDLES:-work/r138_idles.glb}
PITCH=(Spine02:12 neck:-10 Head:-12)
OPS=(copy=idle_ss4:${IDLES}:ss4)
for c in idle block_idle block; do for p in $PITCH; do OPS+=(pitch=${c}:${p}); done; done
OPS+=(aim=idle:loop:30 aim=idle_ss4:loop:30 aim=walk:loop:30 aim=run:loop:25 aim=hit:loop:20 aim=block:loop:30 aim=block_idle:loop:30)
OPS+=(aim=cast_fireball_m:lead:45:0.12:0.25:1.04:1.04 aim=cast_meteor:lead::1.55:1.72:2.97:2.97)
mkdir -p export/ss138a
python3 scripts/r138_02_edit.py export/ss134f/so-body_ss134.glb work/ss138a_pre.glb export/ss134f/orbstaff.glb $OPS --json work/r138_edit_ss138a.json
python3 scripts/r140_03_hood_morph.py work/ss138a_pre.glb export/ss138a/so-body_ss138.glb work/r140_hair_mask.npy
for p in breastplate gauntlets gown hood legs orbstaff shield under_legs; do cp -p export/ss134f/$p.glb export/ss138a/; done
python3 scripts/r138_01_grip_measure.py export/ss138a/so-body_ss138.glb export/ss138a/orbstaff.glb --json work/r138_measure_ss138a.json
python3 scripts/e30_posture.py export/ss138a/so-body_ss138.glb all --json work/r138_posture_ss138a.json
