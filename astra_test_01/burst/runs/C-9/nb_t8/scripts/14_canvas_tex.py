# T8: the texture sheet B is painted OVER.
#
#   python3 scripts/14_canvas_tex.py <baked.png> <flat.png> <out.png>
#
# Sheet A's paint where A's cameras actually reached it, and the model's own
# flat texture everywhere else. Not the bake's island-fill: that is a guess
# spread from the nearest painted texel, and dressing a guess up as paint is
# how a second sheet gets asked to preserve something nobody drew. Flat render
# in the blind regions says plainly "no one has painted this yet".
#
# This is the T5 finding applied: when sheet B was painted independently there,
# the two sheets disagreed by 34/255 over their overlap, half of it features
# drawn in DIFFERENT PLACES. B cannot re-invent what A already placed if B's
# canvas already carries A's placement.
import sys
import numpy as np
from PIL import Image
BAKE, FLAT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
b = np.array(Image.open(BAKE).convert("RGB"), np.uint8)
f = np.array(Image.open(FLAT).convert("RGB").resize(
    (b.shape[1], b.shape[0]), Image.LANCZOS), np.uint8)
m = np.array(Image.open(BAKE.replace(".png", "_mask.png")).convert("L")) > 127
out = np.where(m[..., None], b, f)
Image.fromarray(out).save(OUT)
print("canvas texture: %.2f%% of texels carry sheet A's paint, %.2f%% fall back "
      "to flat render" % (100 * m.mean(), 100 * (~m).mean()))
# a diagnostic that is NOT the canvas: where the blind regions are
d = np.where(m[..., None], (b * 0.45 + 90).astype(np.uint8), np.array([255, 40, 40], np.uint8))
Image.fromarray(d).save(OUT.replace(".png", "_blind.png"))
print("wrote %s and its blind-region map" % OUT)
