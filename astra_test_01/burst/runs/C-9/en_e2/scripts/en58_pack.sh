#!/bin/zsh
# EN-E2 C-9 Phase 2: ONE kit end to end after its kit file exists -- cells (en21) -> index + contact sheet -> fit (en53) -> sockets ->
# manifest lint (+ negative controls) -> runtime resample -> stills + films (en12) -> stills8 sheet into artifacts/.
# Refuses to start below the conductor's disk floor (21 GiB). Heavy steps take the heavy lock themselves.
#   zsh scripts/en58_pack.sh <g> <kit_id> <vfx_id> <clips,csv> "<film_cfg>" <film_shots,csv> "<title>"
cd "$(dirname "$0")/.."; g=$1; K=$2; V=$3; CL=$4; FC=$5; FS=$6; TI=$7; HL="python3 ../conductor_scripts/heavy_lock.py C-9 --"
F=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}'); [ $F -lt 21 ] && { echo "DISK HALT: $F GiB < 21"; exit 3; }
${=HL} zsh scripts/en21_cells.sh $g $K 2>&1 | grep -E "rendered|ERROR|WATCHDOG"
cd ..
python3 join1_render/scripts/index_cells.py join1_render/kits/$K.json join1_pack/$K en_e2/work/raw_$K.json en_e2/work/closure_$K --sheet join1_pack/${K}_contact_sheet_1x.png 2>&1 | grep -iE "release|closure|error" | tr -s ' ' | tr '\n' ';'; echo
python3 en_e2/scripts/en53_fit.py join1_pack/$K
python3 join1_render/scripts/validate_sockets.py en_e2/work/raw_$K.json join1_render/kits/$K.json en_e2/work/sockets_$K.json 2>&1 | tail -1
cd en_e2
zsh scripts/en22_manifest_lint.sh $g $K 2>&1 | grep -E "^exit|exit [0-9]" | tr '\n' ' '; echo
${=HL} python3 scripts/j_runtime_resample.py export/final_$g/en_${g}_body.glb --clips $CL --out work/runtime_resample_$K.json --index ../join1_pack/$K/matrix_index.json 2>&1 | grep -E "worst [1-9]|wrote" | cut -c1-90
python3 scripts/en35_film_cfg.py $g "$FC" $FS >/dev/null
${=HL} zsh scripts/en12_godot_all.sh $g $V 2>&1 | grep -cE "film /"
python3 scripts/en13_stills_sheet.py views/stills_$g artifacts/en_${g}_stills8.png "$TI" 2>&1 | tail -1
du -sh ../join1_pack/$K views/stills_$g film/en_${g}_*.mp4 | tr '\n' ' '; echo
