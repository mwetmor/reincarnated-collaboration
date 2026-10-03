#!/bin/zsh
# E1b R-C9-141: render the NEW pack root join1_pack/gd-eor-warlord-eor3 from wl_e1/export/final_k_eor3 (every cell), index, validate
# sockets, runtime-resample check, manifest lint (+ the three negative controls), then an ICE-variant probe (idle + spin loop, 8
# headings) into wl_e1/work/n/ice_probe (NOT a pack). Run under heavy_lock.
set -e
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9; K=gd-eor-warlord-eor3; KD=$C9/join1_render; WK=$KD/work
cd $C9/wl_e1
mkdir -p $C9/join1_pack/$K $WK/closure_$K
[ -e $C9/join1_pack/$K/cells ] && { echo "pack root has cells already -- refusing (immutable)"; exit 3; }
J1_KIT=$KD/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$WK/raw_$K.json J1_CLOSURE=$WK/closure_$K \
  perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $KD --resolution 320x180 res://render_cells.tscn > $WK/render_$K.log 2>&1 || true
grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" $WK/render_$K.log | tail -3
python3 $KD/scripts/index_cells.py $KD/kits/$K.json $C9/join1_pack/$K $WK/raw_$K.json $WK/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | tail -8
python3 $KD/scripts/validate_sockets.py $WK/raw_$K.json $KD/kits/$K.json $WK/validate_$K.json 2>&1 | tail -2
python3 $C9/nb_join/scripts/j_runtime_resample.py export/final_k_eor3/wl_body.glb --clips idle,walk,run,attack,warcry,hit,death,eor_spin_start,eor_spin_loop --out $WK/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | tail -3
# ice probe: same kit, helm -> wl_helm_ice, eye colour -> ice, a subset, a scratch out dir
python3 - <<'PY'
import json
C9='/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9'
k=json.load(open(C9+'/join1_render/kits/gd-eor-warlord-eor3.json'))
k['kit']='probe-eor3-ice'; k['source']['pieces']=[p.replace('/wl_helm.glb','/wl_helm_ice.glb') for p in k['source']['pieces']]
k['eyes']['color']='#7fd8ff'; k.pop('supersedes',None)
json.dump(k,open(C9+'/wl_e1/work/n/probe_ice_kit.json','w'),indent=1)
PY
mkdir -p work/n/ice_probe work/n/ice_closure
ONLY=$(python3 -c "print(','.join('%s/%s'%(s,d) for s in ('idle','eor_spin_loop') for d in ('S','SW','W','NW','N','NE','E','SE')))")
J1_KIT=$PWD/work/n/probe_ice_kit.json J1_OUT=$PWD/work/n/ice_probe J1_RAW=$PWD/work/n/ice_raw.json J1_CLOSURE=$PWD/work/n/ice_closure J1_ONLY=$ONLY \
  perl -e 'alarm shift; exec @ARGV' 900 /Applications/Godot.app/Contents/MacOS/Godot --path $KD --resolution 320x180 res://render_cells.tscn > work/n/ice_probe.log 2>&1 || true
grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" work/n/ice_probe.log | tail -2
echo CHAIN_DONE
