#!/bin/zsh
# EN-E2: re-render ONE state's 8 cells of a pack (render_cells.gd J1_ONLY), merge into the pack's raw (merge_raw.py, pass record), re-index.
#   zsh scripts/en41_partial.sh <kit_id> <state> <pass> "<why>"        (run under heavy_lock)
cd "$(dirname "$0")/.."; K=$1; ST=$2; PS=$3; WHY=$4; C9=$(cd .. && pwd)
ONLY=$(for d in S SW W NW N NE E SE; do printf "%s/%s," $ST $d; done | sed 's/,$//')
cp work/raw_$K.json work/raw_${K}_pre_$PS.json
J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_${K}_$PS.json J1_CLOSURE=$PWD/work/closure_$K J1_ONLY=$ONLY \
  perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "rendered|ERROR"
python3 - $K $PS "$WHY" <<'PY'
import json, hashlib, datetime, sys
K, PS, WHY = sys.argv[1:4]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); kit = json.load(open('../join1_render/kits/%s.json' % K))
json.dump({"base": {"pass": "prev", "why": "the pack before this pass"}, "new": {"pass": PS, "body_sha256": sha(kit['source']['body']), "kit_sha256": sha('../join1_render/kits/%s.json' % K),
           "tool_sha256": sha('../join1_render/scripts/render_cells.gd'), "ts": datetime.datetime.now().isoformat(timespec='seconds'), "why": WHY}}, open('work/passes_%s_%s.json' % (K, PS), 'w'), indent=1)
PY
python3 ../join1_render/scripts/merge_raw.py work/raw_${K}_pre_$PS.json work/raw_${K}_$PS.json work/raw_$K.json work/passes_${K}_$PS.json | tail -1
python3 ../join1_render/scripts/index_cells.py ../join1_render/kits/$K.json ../join1_pack/$K work/raw_$K.json work/closure_$K --sheet ../join1_pack/${K}_contact_sheet_1x.png 2>&1 | tail -1 | cut -c1-60
