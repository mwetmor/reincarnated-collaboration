# Cut the four views out of the chosen base-body sheet for Tripo multiview.
#
#   python3 scripts/s2_cutouts.py <sheet.png> <tag>
#
# The barbarian's sheet had lost its plate, so T8 bought a BiRefNet matte from
# fal. This one sits on flat chroma GREEN, so a key is free, deterministic and
# better on a flat plate than a learned matte. Despill is the part that matters:
# without it the hair and skin edges keep a green fringe, and Tripo bakes that
# fringe into the texture it projects.
#
# Placement copies T8 (01b): main blob only, one common height, soles on one
# baseline, white 1024x1024 -- so the four views agree on scale and ground.
import json, hashlib, sys
import numpy as np
from PIL import Image
from scipy import ndimage

src, tag = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
R, G, B = im[..., 0], im[..., 1], im[..., 2]
# alpha: how much greener than the stronger of R and B, mapped to 0..1
spill = G - np.maximum(R, B)
alpha = 1.0 - np.clip((spill - 30.0) / 90.0, 0.0, 1.0)
# despill: never let G exceed max(R, B) on the figure
Gd = np.minimum(G, np.maximum(R, B) + 6.0)
rgb = np.stack([R, Gd, B], -1).clip(0, 255).astype(np.uint8)
rgba = np.dstack([rgb, (alpha * 255).astype(np.uint8)])
H, W = alpha.shape
quads = dict(front=(0, 0), right=(1, 0), back=(0, 1), left=(1, 1))
TARGET, BASE = int(0.88 * 1024), int(1024 * 0.94)
meta, sheet = {}, Image.new('RGB', (2048, 512), (255, 255, 255))
for i, (nm, (c, r)) in enumerate(quads.items()):
    q = rgba[r * H // 2:(r + 1) * H // 2, c * W // 2:(c + 1) * W // 2]
    m = q[..., 3] > 128
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    keep = lab == 1 + int(np.argmax(sizes))
    q = q.copy()
    q[..., 3] = np.where(ndimage.binary_dilation(keep, iterations=2), q[..., 3], 0)
    ys, xs = np.nonzero(keep)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    fig = Image.fromarray(q[y0:y1, x0:x1], 'RGBA')
    w, h = fig.size
    S = TARGET / h
    fig = fig.resize((round(w * S), TARGET), Image.LANCZOS)
    can = Image.new('RGB', (1024, 1024), (255, 255, 255))
    px, py = (1024 - fig.size[0]) // 2, BASE - TARGET
    can.paste(fig, (px, py), fig)
    can.save('work/so_%s_%s.jpg' % (tag, nm), quality=95)
    sheet.paste(can.resize((512, 512)), (i * 512, 0))
    # residual green on the figure after despill -- should be ~0
    fa = np.asarray(fig)
    on = fa[..., 3] > 200
    g_ex = float(np.mean(np.clip(fa[on][:, 1].astype(int) - np.maximum(fa[on][:, 0], fa[on][:, 2]).astype(int), 0, None))) if on.any() else 0.0
    meta[nm] = dict(src_box=[int(x0), int(y0), int(x1), int(y1)], height_px_src=int(h),
                    scale=round(S, 4), blobs=int(n), green_excess_after_despill=round(g_ex, 3))
    print("  %-6s src h %4d  scale %.3f  blobs %2d  residual green %.3f" % (nm, h, S, n, g_ex))
sheet.save('work/so_%s_views_check.png' % tag)
json.dump(dict(sheet=src, sha256=hashlib.sha256(open(src, 'rb').read()).hexdigest(),
               matte='chroma key + despill (no fal spend)', views=meta),
          open('work/views_%s.json' % tag, 'w'), indent=1)
print("  heights spread: %d px" % (max(v['height_px_src'] for v in meta.values())
                                     - min(v['height_px_src'] for v in meta.values())))
