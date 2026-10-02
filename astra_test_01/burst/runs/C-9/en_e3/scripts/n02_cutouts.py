# Cut the four views out of a creature model sheet for Tripo multiview (EN-E3).
#   python3 scripts/n02_cutouts.py <sheet.png> <tag>
# Differs from s2_cutouts.py in two ways that a long, low body forces:
#  1. Views are found as the four largest BLOBS, not as fixed quarters: the front and back views are narrow and the side views
#     wide, so the sheet's own grid is not 2x2 equal quarters.
#  2. ONE scale for all four views (the sheet draws them at one scale), fitted so the WIDEST view fits 1024 px; s2 scaled each view
#     to a common HEIGHT, which for a creature 2.6x longer than tall would push the side views off the canvas.
# Key: chroma #00ff00 + despill (no fal spend). Soles on one baseline.
import json, hashlib, sys
import numpy as np
from PIL import Image
from scipy import ndimage

src, tag = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
R, G, B = im[..., 0], im[..., 1], im[..., 2]
spill = G - np.maximum(R, B)
alpha = 1.0 - np.clip((spill - 30.0) / 90.0, 0.0, 1.0)
Gd = np.minimum(G, np.maximum(R, B) + 6.0)
rgba = np.dstack([np.stack([R, Gd, B], -1).clip(0, 255).astype(np.uint8), (alpha * 255).astype(np.uint8)])
m = alpha > 0.5
lab, n = ndimage.label(ndimage.binary_closing(m, iterations=3))
sizes = ndimage.sum(m, lab, range(1, n + 1))
big = [1 + i for i in np.argsort(sizes)[::-1][:4]]
boxes = []
for L in big:
    ys, xs = np.nonzero(lab == L)
    boxes.append((L, xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
H = alpha.shape[0]
top = sorted([b for b in boxes if (b[2] + b[4]) / 2 < H / 2], key=lambda b: b[1])
bot = sorted([b for b in boxes if (b[2] + b[4]) / 2 >= H / 2], key=lambda b: b[1])
assert len(top) == 2 and len(bot) == 2, (len(top), len(bot))
views = dict(front=top[0], right=top[1], back=bot[0], left=bot[1])
wmax = max(b[3] - b[1] for b in boxes); hmax = max(b[4] - b[2] for b in boxes)
S = min(0.92 * 1024 / wmax, 0.80 * 1024 / hmax)
BASE = int(512 + hmax * S / 2)   # one baseline for all views, the tallest view centred
meta, strip = {}, Image.new('RGB', (2048, 512), (255, 255, 255))
for i, (nm, (L, x0, y0, x1, y1)) in enumerate(views.items()):
    q = rgba[y0:y1, x0:x1].copy()
    keep = ndimage.binary_dilation(lab[y0:y1, x0:x1] == L, iterations=2)
    q[..., 3] = np.where(keep, q[..., 3], 0)
    fig = Image.fromarray(q, 'RGBA')
    fig = fig.resize((round(fig.size[0] * S), round(fig.size[1] * S)), Image.LANCZOS)
    can = Image.new('RGB', (1024, 1024), (255, 255, 255))
    can.paste(fig, ((1024 - fig.size[0]) // 2, BASE - fig.size[1]), fig)
    can.save('work/cv_%s_%s.jpg' % (tag, nm), quality=95)
    strip.paste(can.resize((512, 512)), (i * 512, 0))
    meta[nm] = dict(src_box=[int(x0), int(y0), int(x1), int(y1)], w_px=int(x1 - x0), h_px=int(y1 - y0))
    print('  %-6s box %s  w %d h %d' % (nm, meta[nm]['src_box'], x1 - x0, y1 - y0))
strip.save('work/cv_%s_views_check.jpg' % tag, quality=88)
json.dump(dict(sheet=src, sha256=hashlib.sha256(open(src, 'rb').read()).hexdigest(), scale=round(S, 4),
               matte='chroma key + despill (no fal spend)', views=meta,
               height_spread_px=int(max(v['h_px'] for v in meta.values()) - min(v['h_px'] for v in meta.values())),
               side_length_spread_px=abs(meta['left']['w_px'] - meta['right']['w_px']),
               frontback_width_spread_px=abs(meta['front']['w_px'] - meta['back']['w_px'])),
          open('work/cv_%s.json' % tag, 'w'), indent=1)
print('  one scale %.4f; heights spread %d px' % (S, max(v['h_px'] for v in meta.values()) - min(v['h_px'] for v in meta.values())))
