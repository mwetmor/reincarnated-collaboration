# T8 step 1: find the tattoo on the surface and say which arm each patch is on.
#
#   python3 scripts/05_tattoo.py work [--fix out.png]
#
# The defect: Meshy projected the back view mirrored, so the knotwork band that
# belongs on his RIGHT upper arm also appears on the back of his LEFT. It is
# found in 3D, not in the atlas: the UV layout is fragmented into dozens of
# islands and "which arm is this patch on" is not a question the atlas can
# answer, while a texel's own world position answers it directly.
import json, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = sys.argv[1]
S = np.load(os.path.join(W, "surface.npz"))
P = S["tex_pos"].astype(np.float32)
ON = S["tex_on"]
lo, hi = S["bbox"]
right = S["right"]
H = float(hi[2] - lo[2])
_im = Image.open(os.path.join(W, "base_texture.png")).convert("RGB")
if _im.size[0] != P.shape[0]:
    # the UV raster and the texture must share a grid; Tripo ships 4096 and
    # rasterising at 4096 would cost 200 MB per attribute for no gain -- the
    # paint never supports one sample per texel at that size anyway
    print("  texture %d -> %d to match the UV raster" % (_im.size[0], P.shape[0]))
    _im = _im.resize((P.shape[0], P.shape[0]), Image.LANCZOS)
T = np.array(_im, np.float32) / 255.0
# the texture is stored bottom-up relative to the UV raster
T = T[::-1]
mx = T.max(2); mn = T.min(2)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
val = mx
# ARM REGION: away from the midline, above the hips. In an A-pose the upper
# arm is the outer third of the span, in the top half of the body.
arm = ON & (np.abs(P[..., 0]) > 0.30) & (P[..., 2] > lo[2] + 0.55 * H)
print("arm texels: %d" % arm.sum())
print("  skin there: sat median %.3f, value median %.3f"
      % (np.median(sat[arm]), np.median(val[arm])))
# NOT-SKIN, rather than "pale". The first rule looked for the pale interlace
# and found 449 texels -- 0.21% of the arm -- because the knotwork sits on a
# DARK band and only its bright lines are pale. The ink is the band AND the
# lines; skin is the peachy, bright, saturated thing, and everything on the
# arm that is not that is what has to go.
skin_sat, skin_val = float(np.median(sat[arm])), float(np.median(val[arm]))
tat = arm & ((val < 0.70) | (sat < 0.25))
print("  skin reference sat %.3f val %.3f; NOT-SKIN on the arm "
      "(val<0.70 or sat<0.25): %d texels (%.2f%% of arm)"
      % (skin_sat, skin_val, tat.sum(), 100 * tat.sum() / max(arm.sum(), 1)))
xs = P[..., 0][tat]
rsign = float(np.sign(right[0]))
on_right = (xs * rsign) > 0
print("  on his RIGHT (%s X): %d texels    on his LEFT: %d texels"
      % ("+" if rsign > 0 else "-", int(on_right.sum()), int((~on_right).sum())))
for nm, sel in (("RIGHT", on_right), ("LEFT", ~on_right)):
    if sel.sum() == 0:
        continue
    z = P[..., 2][tat][sel]
    y = P[..., 1][tat][sel]
    print("     %-5s z %.3f..%.3f (%.0f%%..%.0f%% of height)   y %.3f..%.3f"
          % (nm, z.min(), z.max(), 100 * (z.min() - lo[2]) / H,
             100 * (z.max() - lo[2]) / H, y.min(), y.max()))
json.dump(dict(arm_texels=int(arm.sum()), tattoo_texels=int(tat.sum()),
               on_right=int(on_right.sum()), on_left=int((~on_right).sum()),
               right_axis="+X" if rsign > 0 else "-X"),
          open(os.path.join(W, "tattoo.json"), "w"), indent=1)
np.save(os.path.join(W, "tattoo_mask.npy"), tat)
