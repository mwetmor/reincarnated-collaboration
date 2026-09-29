#!/bin/zsh
# T8 barbarian B (R-C9-70): matte -> place views -> Meshy multi-image -> look renders at 52.95 and 0 deg.
source ~/.zshrc >/dev/null 2>&1; cd ${0:a:h}
python3 01_matte_views.py b && python3 01b_place_views.py b && python3 02_meshy_model.py b && mkdir -p look_b && \
/Applications/Blender.app/Contents/MacOS/Blender -b -P 03_render_views.py -- nb_b.glb look_b 52.95354112560294 S,SE,E,NE,N,NW,W,SW > render53_b.log 2>&1 && \
/Applications/Blender.app/Contents/MacOS/Blender -b -P 03_render_views.py -- nb_b.glb look_b 0 S,E,N,W > render0_b.log 2>&1 && echo "B DONE"
