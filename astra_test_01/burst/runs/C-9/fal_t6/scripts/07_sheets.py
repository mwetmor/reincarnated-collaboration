# T6 step 6 -- the contact sheets. Rows are the Meshy baseline then the five
# fal generators; columns are directions. Mid-grey ground, never green, so the
# painted ink edge still reads.
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from sheet import sheet, _font, BG, PANEL, INK, LBL
from PIL import ImageDraw
from maskutil import input_mask

T6 = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/fal_t6/'
B = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/'
GENS = [('meshy', 'MESHY (baseline)'), ('hunyuan3d_31_pro', 'hunyuan3d 3.1 pro'),
        ('rodin_25', 'rodin v2.5'), ('tripo_h31_mv', 'tripo h3.1 mv'),
        ('trellis2', 'trellis 2'), ('hi3d_v3', 'hi3d v3.0')]
EL = '52.95°'
io = json.load(open(T6 + 'compare/iou_rig.json'))['iou']
orient = json.load(open(T6 + 'compare/orientation.json'))['models']

def rowlabel(s, g, label):
    m = json.load(open(f'{T6}work/metrics/{s}_{g}.json'))
    h = io[f'{s}_{g}']['p0_100']
    o = orient[f'{s}_{g}']
    yaw = int(o['yaw_deg'])
    return (f"{label}\n{m['tris_welded']:,} tri\nIoU {h['mean_iou']:.3f}\n"
            f"islands {m['islands']}\nyaw {yaw}°")

for s in ('knight', 'manticore'):
    rows = [(rowlabel(s, g, lb), f'{s}_{g}') for g, lb in GENS]
    # (a) unlit, 8 directions
    sheet(rows, [(d, d) for d in ('S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW')],
          lambda r, c: f'{T6}work/out/unlit/{r}_{c}.png',
          f'{T6}compare/{s}_unlit.png',
          title=f'T6 bake-off — {s.upper()} — UNLIT BASE COLOUR, ortho, elevation {EL} (Matt R-C9-68). '
                f'Row label: welded triangles / mean silhouette IoU vs the painted plates / mesh islands / yaw applied.',
          cell=512, lblw=240, hdr=46)
    # (b) lit clay, 4 directions
    sheet(rows, [(d, d) for d in ('S', 'E', 'N', 'SE')],
          lambda r, c: f'{T6}work/out/clay/{r}_{c}.png',
          f'{T6}compare/{s}_clay.png',
          title=f'T6 bake-off — {s.upper()} — LIT CLAY (texture stripped, one soft key upper-left + ambient), '
                f'elevation {EL}. Geometry only: no texture to flatter or hide it.',
          cell=512, lblw=240, hdr=46)
    # (c) heads -- one row of six, because faces are compared side by side
    sheet([('head close-up\nunlit, from S\nelevation ' + EL, 'head')],
          [(lb, f'{s}_{g}') for g, lb in GENS],
          lambda r, c: f'{T6}work/out/head/{c}_S.png',
          f'{T6}compare/{s}_heads.png',
          title=f'T6 bake-off — {s.upper()} — HEAD CLOSE-UP, unlit, from S at elevation {EL}. '
                + ('The helm is the identity read.' if s == 'knight' else 'The human face is the identity read.'),
          cell=512, lblw=210, hdr=46)

# (d) extra: the silhouette basis of the IoU, painted plate on top
for s in ('knight', 'manticore'):
    os.makedirs(T6 + 'work/plates', exist_ok=True)
    for v in ('front', 'right', 'back', 'left'):
        src = (B + 'meshy_t1/knight_%s.jpg' if s == 'knight' else B + 'meshy_t2/manticore_%s.jpg') % v
        m, rgb = input_mask(src)
        a = np.dstack([rgb.astype(np.uint8), (m * 255).astype(np.uint8)])
        Image.fromarray(a, 'RGBA').save(f'{T6}work/plates/{s}_{v}.png')
    rows = [('PAINTED PLATE\n(the input)\nthe reference', 'plate')] + \
           [(rowlabel(s, g, lb) + f"\nIoU/view below", f'{s}_{g}') for g, lb in GENS]
    def cp(r, c):
        return f'{T6}work/plates/{s}_{c}.png' if r == 'plate' else f'{T6}work/out/silh/{r}_{c}.png'
    sheet(rows, [(v, v) for v in ('front', 'right', 'back', 'left')], cp,
          f'{T6}compare/{s}_silhouette.png',
          title=f'T6 bake-off — {s.upper()} — elevation 0, the painted plates’ own projection. '
                f'This is what the silhouette IoU is measured on; top row is the painted input.',
          cell=512, lblw=240, hdr=46)

# stamp per-view IoU onto the silhouette sheets
for s in ('knight', 'manticore'):
    p = f'{T6}compare/{s}_silhouette.png'
    im = Image.open(p); d = ImageDraw.Draw(im); f = _font(22)
    for i, (g, lb) in enumerate(GENS):
        h = io[f'{s}_{g}']['p0_100']
        for j, v in enumerate(('front', 'right', 'back', 'left')):
            # row 0 is the painted plate, so generator i is row i+1; the stamp
            # must sit at the bottom of ROW i+1, not row i -- the first version
            # put every score one row up, under the plate it was scored against
            x, y = 240 + j * 512 + 8, 46 + (i + 2) * 512 - 34
            d.rectangle([x - 4, y - 4, x + 128, y + 26], fill=(20, 20, 24))
            d.text((x, y), f"IoU {h[v]['iou']:.3f}", font=f, fill=(255, 226, 120))
    im.save(p)
print('sheets written to', T6 + 'compare/')
for f in sorted(os.listdir(T6 + 'compare')):
    print('  ', f)
