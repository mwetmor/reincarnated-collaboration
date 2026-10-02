# EN-E2 round 3, THE WRAITH'S SPIRIT GRADE (the conductor, 2026-10-02: "a cooler, paler, slightly translucent-reading grade (desaturated
# shroud, a blue-white rim on the edges, darker eye sockets), so at play scale it reads as a SPIRIT and not another robed acolyte. A
# grade, no new sheet."). No paint call. On the painted atlas, in CIE Lab, by the body's OWN geometry (never by guessing from colour alone):
#   SHROUD   every texel NOT in the head/hands UV mask, PLUS the hood (head-mask texels L* > 55 and b* > 4, warm pale cloth): chroma x --kc (0.45), b* --db (-5, cooler), L* + --dl (4, paler)
#   WISPS    the tail's lower half fades toward a pale BLUE-WHITE (the rim): weight = smoothstep over the texel's REST HEIGHT, from the
#            hips (0) down to the tail tips (--rim, 0.55 at the tips) -- the trailing strips read as cold light thinning out (the
#            "translucent" read without alpha, which the cells and the runtime material do not carry)
#   CLAWS    the hands (UV mask) get the shroud's chroma / cool / pale treatment, without the rim (conductor, after round 3)
#   EYES     in the head mask, texels darker than L* 45 go x --eye (0.70) (deeper hollows); the pale eye points (L* > 75) are untouched
#   python3 scripts/en26_spirit_grade.py <static.glb> <in.png> <out.png> [--json f]
import json, sys, os
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('en16_colourlib'); L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; BODY, IN, OUT = a[0], a[1], a[2]
o = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
KC, DB, DL, RIM, EYE = o('--kc', 0.45), o('--db', -5.0), o('--dl', 4.0), o('--rim', 0.55), o('--eye', 0.70)
js, b = L.load_glb(BODY); G, _ = W.globals_(js)
mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]
rd = lambda i: np.asarray(L.read_accessor(js, b, i))
uv = rd(pr['attributes']['TEXCOORD_0']); J = rd(pr['attributes']['JOINTS_0']).astype(int); Wt = rd(pr['attributes']['WEIGHTS_0'])
idx = rd(pr['indices']).astype(int).reshape(-1, 3)
V = W.skin_rest(js, b, mn, G); y = V[:, 1]
names = [js['nodes'][j]['name'] for j in js['skins'][js['nodes'][mn]['skin']]['joints']]
hips_y = float(G[js['skins'][0]['joints'][names.index('Hips')]][1, 3]); y0 = float(y.min())
head = [names.index(n) for n in ('Head', 'neck', 'headfront', 'head_end') if n in names]
hands = [names.index(n) for n in ('LeftHand', 'RightHand')]
wsum = lambda js_: sum(np.where(np.isin(J[:, k], js_), Wt[:, k], 0.0) for k in range(J.shape[1]))
w_head, w_hand = wsum(head), wsum(hands)
im = np.asarray(Image.open(IN).convert('RGB')).astype(float) / 255; S = im.shape[0]
def raster(vals, sel):
    img = Image.new('F', (S, S), -1.0); d = ImageDraw.Draw(img)
    for t in idx[sel]:
        d.polygon([(float(uv[v, 0]) * S, float(uv[v, 1]) * S) for v in t], fill=float(vals[t].mean()))
    return np.asarray(img)
is_head = (w_head[idx] > 0.5).all(1); is_hand = (w_hand[idx] > 0.5).all(1)
hmap = raster(np.where(np.ones(len(y), bool), y, 0), np.ones(len(idx), bool))      # rest height per texel (-1 = unused)
headm = raster(np.ones(len(y)), is_head) > 0; handm = raster(np.ones(len(y)), is_hand) > 0
used = hmap > -0.5
lab = C.rgb2lab(im); Lc, A_, B_ = lab[..., 0].copy(), lab[..., 1].copy(), lab[..., 2].copy()
hood = headm & (Lc > 55) & (B_ > 4)                     # FIX (cells r3): the HOOD is head-weighted; warm pale cloth in the head mask is shroud, not face
shroud = (used & ~headm & ~handm) | hood
A_[shroud] *= KC; B_[shroud] = B_[shroud] * KC + DB; Lc[shroud] = np.clip(Lc[shroud] + DL, 0, 100)
claws = used & handm & ~headm                          # round 3 fix (conductor): the claws read warm tan -- the same cool, pale treatment, no rim
A_[claws] *= KC; B_[claws] = B_[claws] * KC + DB; Lc[claws] = np.clip(Lc[claws] + DL, 0, 100)
u = np.clip((hips_y - hmap) / max(hips_y - y0, 1e-6), 0, 1); wgt = (u * u * (3 - 2 * u)) * RIM * shroud
rim_lab = np.array([93.0, -2.0, -9.0])                                                # pale blue-white
Lc = Lc * (1 - wgt) + rim_lab[0] * wgt; A_ = A_ * (1 - wgt) + rim_lab[1] * wgt; B_ = B_ * (1 - wgt) + rim_lab[2] * wgt
eye = headm & (Lc < 45); Lc[eye] *= EYE
out = C.lab2rgb(np.stack([Lc, A_, B_], -1)); out[~used] = im[~used]
Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(OUT)
rep = dict(params=dict(kc=KC, db=DB, dl=DL, rim=RIM, eye=EYE), texels=dict(shroud=int(shroud.sum()), hood=int(hood.sum()), claws=int(claws.sum()), head=int(headm.sum()), hands=int(handm.sum()),
           wisp_weighted=int((wgt > 0.05).sum()), eye_darkened=int(eye.sum())), hips_y=round(hips_y, 4), tail_tip_y=round(y0, 4))
print('SPIRIT', json.dumps(rep))
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
