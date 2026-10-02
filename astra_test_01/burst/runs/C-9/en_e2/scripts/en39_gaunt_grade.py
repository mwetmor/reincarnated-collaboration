# EN-E2 round 5, THE FROST-GAUNT'S VALUE GRADE (the conductor: "it reads too close to the revenant (bone-white skeleton). Separate it by
# VALUE and silhouette, not a new sheet: grade the body to dark, frostbitten blue-grey sinew (L* well below the revenant's bone), keeping
# the antlers and skull pale so the head pops, with a frost rime only on the edges. Deepen the hide to a dark matted brown-grey.").
# Regions from the body's OWN geometry (rest pose), never from colour alone:
#   HEAD     triangles weighted > 0.5 to Head/neck/headfront/head_end -> kept PALE (skull + antlers): L* + 4, a cool lift (b* -2)
#   HIDE     non-head texels that are warm, chromatic and DARK (hue angle 40-100 deg, C* > 7, L* < 58): L* x --hide (0.55), C* x 0.6 -> dark matted brown-grey
#   SINEW    every other non-head texel: L* mapped to --sinew-l (34) +- 0.45 x its own deviation, a* -1.5, b* --sinew-b (-16: frostbitten blue-grey; -9 rendered neutral under the warm play light)
#   RIME     texels on UP-FACING surfaces (rest normal . up > --rime-up, 0.72: the tops of the shoulders, forearms, knees, feet) pulled 45 % toward a
#            pale blue-white (the "edges" a 53 deg camera sees as the figure's upper contour)
# Writes the graded atlas and a region-ID texture for the play-camera measure (R sinew, G head, B hide).
#   python3 scripts/en39_gaunt_grade.py <static.glb> <in.png> <out.png> <regions_out.png> [--json f]
import json, sys, os
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('en16_colourlib'); L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; BODY, IN, OUT, ROUT = a[:4]
o = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
SL, HIDE, RUP, SB = o('--sinew-l', 34.0), o('--hide', 0.55), o('--rime-up', 0.72), o('--sinew-b', -16.0)   # b: -9 rendered neutral under the warm sun (round 5 measure)
js, b = L.load_glb(BODY); G, _ = W.globals_(js)
mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]
rd = lambda i: np.asarray(L.read_accessor(js, b, i))
uv = rd(pr['attributes']['TEXCOORD_0']); J = rd(pr['attributes']['JOINTS_0']).astype(int); Wt = rd(pr['attributes']['WEIGHTS_0'])
idx = rd(pr['indices']).astype(int).reshape(-1, 3); V = W.skin_rest(js, b, mn, G)
names = [js['nodes'][j]['name'] for j in js['skins'][js['nodes'][mn]['skin']]['joints']]
head = [names.index(n) for n in ('Head', 'neck', 'headfront', 'head_end') if n in names]
w_head = sum(np.where(np.isin(J[:, k], head), Wt[:, k], 0.0) for k in range(J.shape[1]))
fn = np.cross(V[idx[:, 1]] - V[idx[:, 0]], V[idx[:, 2]] - V[idx[:, 0]]); fn /= np.maximum(np.linalg.norm(fn, axis=1, keepdims=True), 1e-12)
im = np.asarray(Image.open(IN).convert('RGB')).astype(float) / 255; S = im.shape[0]
def raster(vals_tri, sel):
    img = Image.new('F', (S, S), -9.0); d = ImageDraw.Draw(img)
    for t, v in zip(idx[sel], vals_tri[sel]):
        d.polygon([(float(uv[k, 0]) * S, float(uv[k, 1]) * S) for k in t], fill=float(v))
    return np.asarray(img)
allt = np.ones(len(idx), bool)
used = raster(np.ones(len(idx)), allt) > -1
headm = raster(np.ones(len(idx)), (w_head[idx] > 0.5).all(1)) > 0
up = raster(fn[:, 1], allt)
lab = C.rgb2lab(im); Lc, A_, B_ = lab[..., 0].copy(), lab[..., 1].copy(), lab[..., 2].copy()
ch = np.hypot(A_, B_); hue = np.degrees(np.arctan2(B_, A_)) % 360
hide = used & ~headm & (hue > 40) & (hue < 100) & (ch > 7) & (Lc < 58)   # round-5 fix: the pale warm SKIN (L* > 58) is sinew, not hide
sinew = used & ~headm & ~hide
mL = Lc[sinew].mean()
Lc[sinew] = np.clip(SL + 0.45 * (Lc[sinew] - mL), 0, 100); A_[sinew] = A_[sinew] * 0.4 - 1.5; B_[sinew] = B_[sinew] * 0.4 + SB
Lc[hide] *= HIDE; A_[hide] *= 0.6; B_[hide] *= 0.6
Lc[headm] = np.clip(Lc[headm] + 4, 0, 100); B_[headm] -= 2
rime = used & ~headm & (up > RUP); r = 0.45
Lc[rime] = Lc[rime] * (1 - r) + 90 * r; A_[rime] = A_[rime] * (1 - r) - 2 * r; B_[rime] = B_[rime] * (1 - r) - 8 * r
out = C.lab2rgb(np.stack([Lc, A_, B_], -1)); out[~used] = im[~used]
Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(OUT)
ids = np.zeros(im.shape, np.uint8); ids[sinew & ~rime] = (255, 0, 0); ids[headm] = (0, 255, 0); ids[hide] = (0, 0, 255)
Image.fromarray(ids).save(ROUT)
rep = dict(params=dict(sinew_L=SL, sinew_b=SB, hide=HIDE, rime_up=RUP), texels=dict(sinew=int(sinew.sum()), head=int(headm.sum()), hide=int(hide.sum()), rime=int(rime.sum())),
           sinew_L_before=round(float(mL), 2))
print('GAUNT', json.dumps(rep))
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
