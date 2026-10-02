#!/bin/zsh
# EN-E2: one body's painted-texture stage, the D7 method, as one runner (run under heavy_lock for the Blender steps):
#   zsh scripts/en32_tex.sh <g> canvasA            -> work/<g>_canvas_A.png (+ surface A, flat tex)
#   zsh scripts/en32_tex.sh <g> canvasB <Apaint>   -> bake A, canvas tex, work/<g>_canvas_B.png (+ surface AB)
#   zsh scripts/en32_tex.sh <g> bake <Apaint> <Bpaint>  -> work/<g>_tex_final.png
cd "$(dirname "$0")/.."; g=$1; S=$2
case $S in
canvasA)
  blender -b -noaudio --python scripts/t5_01_paint_sheet.py -- work/${g}_static.glb x --name ${g}A --yaw 180 --plan work/plan_A.json 2>&1 | grep "PAINT SHEET"
  python3 scripts/02_compose.py ${g}A work/${g}_canvas_A.png | grep -c coverage
  blender -b -noaudio --python scripts/06a_surface.py -- work/${g}_static.glb work/surface_${g}A.npz --sheets ${g}A 2>&1 | grep wrote
  blender -b -noaudio --python scripts/13_dump_tex.py -- work/${g}_static.glb $PWD/work/${g}_flat_tex.png 2>&1 | grep wrote ;;
canvasB)
  python3 scripts/06b_bake.py work/surface_${g}A.npz work/${g}_tex_A.png --sheet ${g}A:$3 2>&1 | tail -1
  python3 scripts/14_canvas_tex.py work/${g}_tex_A.png work/${g}_flat_tex.png work/${g}_canvas_tex_B.png | head -1
  blender -b -noaudio --python scripts/t5_01_paint_sheet.py -- work/${g}_static.glb x --name ${g}B --yaw 180 --plan work/plan_B.json --tex work/${g}_canvas_tex_B.png 2>&1 | grep "PAINT SHEET"
  python3 scripts/02_compose.py ${g}B work/${g}_canvas_B.png | grep -c coverage
  blender -b -noaudio --python scripts/06a_surface.py -- work/${g}_static.glb work/surface_${g}AB.npz --sheets ${g}A,${g}B 2>&1 | grep wrote ;;
bake)
  python3 scripts/06b_bake.py work/surface_${g}AB.npz work/${g}_tex_AB.png --sheet ${g}A:$3 --sheet ${g}B:$4 2>&1 | tail -1
  python3 scripts/14_canvas_tex.py work/${g}_tex_AB.png work/${g}_flat_tex.png work/${g}_tex_final.png | head -1 ;;
esac
