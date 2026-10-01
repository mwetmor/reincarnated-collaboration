# Silhouette IoU of a 3D build against the sheet's four cut-outs (T6's reading: both masks height-normalised,
# centred on the main blob's bbox centre, full mask scored).
#   python3 e04_iou.py <renderprefix> <cutout_tag> <map front=090,right=000,back=270,left=180> [out.json]
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage
pre, tag, mp = sys.argv[1], sys.argv[2], dict(x.split('=') for x in sys.argv[3].split(','))
def norm(m, H=600, W=600):
    lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n + 1)); mb = lab == 1 + int(np.argmax(sz))
    ys, xs = np.nonzero(mb); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    s = H / (y1 - y0); cx = (x0 + x1) / 2
    im = Image.fromarray((m * 255).astype(np.uint8)); w, h = im.size
    im = im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.NEAREST); a = np.asarray(im) > 127
    out = np.zeros((H + 40, W), bool); oy = -round(y0 * s) + 20; ox = round(W / 2 - cx * s)
    ys2, xs2 = np.nonzero(a); ys2 = ys2 + oy; xs2 = xs2 + ox
    k = (ys2 >= 0) & (ys2 < H + 40) & (xs2 >= 0) & (xs2 < W); out[ys2[k], xs2[k]] = True
    return out
res = {}
for v, y in mp.items():
    r = np.asarray(Image.open('%s_%s.png' % (pre, y)).convert('RGBA'))[..., 3] > 128
    c = np.asarray(Image.open('work/so_%s_%s.jpg' % (tag, v)).convert('RGB')).astype(int).min(2) < 235
    c = ndimage.binary_fill_holes(ndimage.binary_opening(c, np.ones((3, 3))))
    A, B = norm(r), norm(c); res[v] = round(float((A & B).sum() / (A | B).sum()), 4)
res['mean'] = round(float(np.mean([res[v] for v in mp])), 4)
print(tag, res)
if len(sys.argv) > 4: json.dump(res, open(sys.argv[4], 'w'), indent=1)
