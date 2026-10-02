#!/bin/zsh
# One-line test for the t5_01 rest-pose fix: the S cell rendered from the ANIMATED shipped body must equal (alpha IoU >= 0.999) the S
# cell rendered from the same body with its clips stripped. Before the fix the animated render was the first clip's pose (IoU ~0.6).
#   zsh tests/t5_rest_pose_test.sh <scripts_dir_with_t5_01>      (under heavy_lock; cells land in <scripts_dir>/../work)
# NEGATIVE CONTROL: zsh tests/t5_rest_pose_test.sh negctl/scripts  (the pre-fix script from 879e0a0a9) must FAIL.
cd "$(dirname "$0")/.."; S=${1:-scripts}; W=$(dirname $S)/work; mkdir -p $W; P=work/_t5test_plan.json; echo '[{"id":"S","dir":"S","elev":19.77,"subject":"body","scale":1.0}]' > $P
for v in anim:export/final_m/en_m_body.glb static:work/m_static.glb; do blender -b -noaudio --python $S/t5_01_paint_sheet.py -- $PWD/${v#*:} x --name _t5test_${v%%:*} --yaw 180 --plan $P >/dev/null 2>&1; done
python3 -c "
import numpy as np; from PIL import Image
a=np.asarray(Image.open('$W/_cells__t5test_anim/cell_S.png'))[...,3]>8; b=np.asarray(Image.open('$W/_cells__t5test_static/cell_S.png'))[...,3]>8
iou=(a&b).sum()/max((a|b).sum(),1); print('T5 REST-POSE TEST: S-cell alpha IoU animated vs static = %.4f -> %s' % (iou, 'PASS' if iou>=0.999 else 'FAIL')); raise SystemExit(0 if iou>=0.999 else 1)"
