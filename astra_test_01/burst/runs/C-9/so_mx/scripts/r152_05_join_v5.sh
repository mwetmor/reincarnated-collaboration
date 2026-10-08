#!/bin/zsh
# R-C9-152: the JOIN-1 pack re-rendered from ss152b as a NEW root, join1_pack_v5/d2-fire-sorc-bm (v4 untouched),
# with the shared renderer (join1_render, unchanged), then the indexer + contact sheet, the socket validator, the manifest lint
# with its negative controls. Heavy lock for the render.
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9; J=$C9/join1_render; K=d2-fire-sorc-bm
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ "$FREE" -ge 20 ] || { echo "HALT: under 20 GiB"; exit 9; }
[ -e $C9/join1_pack_v5/$K ] && { echo "REFUSED: pack root exists (roots are immutable)"; exit 2; }
mkdir -p $C9/join1_pack_v5/$K $J/work/closure_${K}_v5
echo "{\"ev\":\"start\",\"step\":\"J1-v5-$K\",\"t\":$(date +%s)}" >> $J/work/timing.jsonl
python3 $C9/../C-7/conductor_scripts/heavy_lock.py C-9 -- env J1_KIT=$J/kits/${K}_v5.json J1_OUT=$C9/join1_pack_v5/$K J1_RAW=$J/work/raw_${K}_v5.json J1_CLOSURE=$J/work/closure_${K}_v5 \
  GG_TIMEOUT_S=2700 $C9/so_mx/scripts/r152_06_godot_guard.py --path $J --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG|heavy_lock" | tail -14
echo "{\"ev\":\"end\",\"step\":\"J1-v5-$K\",\"t\":$(date +%s)}" >> $J/work/timing.jsonl
cd $J
python3 scripts/index_cells.py kits/${K}_v5.json $C9/join1_pack_v5/$K work/raw_${K}_v5.json work/closure_${K}_v5 --sheet $C9/join1_pack_v5/${K}_contact_sheet_1x.png 2>&1 | tail -25
python3 scripts/validate_sockets.py work/raw_${K}_v5.json kits/${K}_v5.json work/validate_${K}_v5.json 2>&1 | tail -8
echo J1_V5_DONE
