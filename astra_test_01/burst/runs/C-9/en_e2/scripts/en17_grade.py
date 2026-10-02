# EN-E2 REGION GRADE (the conductor, 2026-10-02, defect 7: "the male reads almost uniformly grey-brown at play scale; the lapis and
# brass are gone"). The champion's s43 method -- a grade on the painted atlas, no paint calls, masked by region -- carried to a
# monolithic body: the regions are not separate piece GLBs here, so they are classified ONCE on the shipped (pre-grade) atlas and
# frozen into a REGION-ID texture, and SKIN comes from the body's own UVs (en11's rule) so the ashen grade is never touched.
#   regions: en16.classify_lab (v2, Lab) on the pre-grade atlas -- the HSV rule below was round 0 and is superseded:
#     lapis  cool cloth: h 180-275, s > 0.05, v < 0.85            (the atlas blue is low-chroma: s ~0.15, so the sheet rule's 0.10 misses most)
#     brass  h 20-62, s > 0.30, v > 0.20                           (gears, bracer, circlet, clock disc, embroidery)
#     ivory  warm or neutral, s < 0.30, v > 0.55, not brass         (under-robe, alb)
#     skin   UV mask (Head/neck/headfront/head_end/hands weight > 0.5) -- NOT graded
#     other  everything else (leggings, shoes, cord, hood shadow) -- NOT graded
#   grade, per graded region, in CIE Lab: L' = mean_L + (L - mean_L) * kL + dL ; (a', b') = (a, b) * kC + (da, db)
#   parameters come from --params <json> {region: {dL, da, db, kL, kC}} (the iteration is recorded in work/<g>_grade_iter.json).
#   python3 scripts/en17_grade.py <m|f> ids                      -> work/<g>_regions.png (R lapis, G ivory, B brass, white skin)
#   python3 scripts/en17_grade.py <m|f> grade <in.png> <out.png> --params <json>
import json, sys, os
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('en16_colourlib'); L = __import__('21_lint_export')
g, cmd = sys.argv[1], sys.argv[2]
SRC_ATLAS = 'work/%s_tex_final%s.png' % (g, '_ashen' if g == 'f' else '')
def skin_mask(size):
    js, b = L.load_glb('work/%s_static.glb' % g)
    mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
    pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]
    rd = lambda i: np.asarray(L.read_accessor(js, b, i))
    uv = rd(pr['attributes']['TEXCOORD_0']); J = rd(pr['attributes']['JOINTS_0']).astype(int); Wt = rd(pr['attributes']['WEIGHTS_0'])
    idx = rd(pr['indices']).astype(int).reshape(-1, 3)
    names = [js['nodes'][j]['name'] for j in js['skins'][js['nodes'][mn]['skin']]['joints']]
    want = [names.index(n) for n in ('Head', 'neck', 'headfront', 'head_end', 'LeftHand', 'RightHand') if n in names]
    w = sum(np.where(np.isin(J[:, k], want), Wt[:, k], 0.0) for k in range(J.shape[1]))
    im = Image.new('L', (size, size), 0); d = ImageDraw.Draw(im)
    for t in idx[(w[idx] > 0.5).all(1)]:
        d.polygon([(float(uv[v, 0]) * size, float(uv[v, 1]) * size) for v in t], fill=255)
    return np.asarray(im) > 0
if cmd == 'ids':
    a = np.asarray(Image.open(SRC_ATLAS).convert('RGB')).astype(float) / 255
    sk = skin_mask(a.shape[0]); R = C.classify_lab(C.rgb2lab(a))
    lapis = R['lapis'] if g == 'm' else R['lapis'] & ~sk   # HIS hood is head-weighted: graded inside the head mask; HER ash hair is not cloth
    brass = R['brass'] & ~sk; ivory = R['ivory'] & ~sk   # skin and hair (head/hands, not lapis) are never graded
    sk = sk & ~lapis
    out = np.zeros(a.shape, np.uint8); out[lapis] = (255, 0, 0); out[ivory] = (0, 255, 0); out[brass] = (0, 0, 255); out[sk] = (255, 255, 255)
    Image.fromarray(out).save('work/%s_regions.png' % g)
    rep = {k: round(float(m.mean()), 4) for k, m in dict(lapis=lapis, ivory=ivory, brass=brass, skin=sk).items()}
    json.dump(dict(source_atlas=SRC_ATLAS, fractions=rep), open('work/%s_regions.json' % g, 'w'), indent=1); print('REGIONS', g, rep)
else:
    IN, OUT = sys.argv[3], sys.argv[4]; P = json.load(open(sys.argv[sys.argv.index('--params') + 1]))
    a = np.asarray(Image.open(IN).convert('RGB')).astype(float) / 255
    ids = np.asarray(Image.open('work/%s_regions.png' % g).convert('RGB'))
    masks = dict(lapis=(ids[..., 0] == 255) & (ids[..., 1] == 0), ivory=(ids[..., 1] == 255) & (ids[..., 0] == 0), brass=(ids[..., 2] == 255) & (ids[..., 0] == 0))
    lab = C.rgb2lab(a); out = lab.copy(); rep = {}
    for k, m in masks.items():
        p = dict(dict(dL=0, da=0, db=0, kL=1, kC=1), **P.get(k, {}))
        mL = lab[..., 0][m].mean()
        out[..., 0][m] = mL + (lab[..., 0][m] - mL) * p['kL'] + p['dL']
        out[..., 1][m] = lab[..., 1][m] * p['kC'] + p['da']; out[..., 2][m] = lab[..., 2][m] * p['kC'] + p['db']
        rep[k] = dict(params=p, texels=int(m.sum()), mean_before=lab[m].mean(0).round(2).tolist(), mean_after=out[m].mean(0).round(2).tolist())
    res = a.copy(); sel = np.zeros(a.shape[:2], bool)
    for m in masks.values(): sel |= m
    res[sel] = C.lab2rgb(out[sel])
    Image.fromarray((res * 255 + 0.5).astype(np.uint8)).save(OUT); print('GRADE', g, json.dumps(rep))
    json.dump(rep, open(OUT.replace('.png', '.json'), 'w'), indent=1)
