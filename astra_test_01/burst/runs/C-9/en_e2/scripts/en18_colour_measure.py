# EN-E2 colour measure: each region's mean CIE Lab on the SHEET (all four matted views of EN2-<G>_a, classified by en17's rule)
# against the SAME region in the PLAY-CAMERA render (beauty pixels whose class-pass pixel -- the body drawn UNSHADED with the
# frozen region-ID texture, nearest filter -- names that region). Exact correspondence: no colour guess on the render side.
#   python3 scripts/en18_colour_measure.py <m|f> <stills_dir> [--json out]
import json, sys, os, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('en16_colourlib')
g, D = sys.argv[1], sys.argv[2]
def classify(a):
    return C.classify_lab(C.rgb2lab(a))
sheet = {k: [] for k in ('lapis', 'ivory', 'brass')}
for vw in ('front', 'right', 'back', 'left'):
    a = np.asarray(Image.open('views/%s_%s/%s.jpg' % (g, dict(w='b').get(g, 'a'), vw)).convert('RGB')).astype(float) / 255
    fig = a.min(2) < 0.94
    if g == 'f':                                   # her hair and face are NOT graded (skin/hair UV mask on the render side): drop the head band
        ys = np.nonzero(fig.any(1))[0]; top, hgt = ys.min(), ys.max() - ys.min()
        fig[: int(top + hgt * (0.32 if vw == 'back' else 0.16))] = False
    for k, m in classify(a).items(): sheet[k].append(C.rgb2lab(a[m & fig]))
S = {k: np.concatenate(v).mean(0) for k, v in sheet.items()}
R = {k: [] for k in S}
for bf in sorted(glob.glob(os.path.join(D, '*_beauty.png'))):
    cf = bf.replace('_beauty.png', '_class.png')
    if not os.path.exists(cf): continue
    b = np.asarray(Image.open(bf).convert('RGB')).astype(float) / 255; c = np.asarray(Image.open(cf).convert('RGB'))
    ids = dict(lapis=(c[..., 0] > 200) & (c[..., 1] < 50) & (c[..., 2] < 50), ivory=(c[..., 1] > 200) & (c[..., 0] < 50) & (c[..., 2] < 50),
               brass=(c[..., 2] > 200) & (c[..., 0] < 50) & (c[..., 1] < 50))
    for k, m in ids.items(): R[k].append(C.rgb2lab(b[m]))
out = {}
for k in S:
    r = np.concatenate(R[k]) if R[k] else np.zeros((0, 3))
    rm = r.mean(0) if len(r) else np.array([np.nan] * 3)
    out[k] = dict(sheet_lab=S[k].round(2).tolist(), render_lab=rm.round(2).tolist(), dE=round(C.dE(S[k], rm), 2), render_px=int(len(r)))
print('COLOUR', g, json.dumps(out))
if '--json' in sys.argv: json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
