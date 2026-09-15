"""Conductor glue for v11 (R-C3-101): from v10 — remove glows/emitters whose owning prop instance is gone; restore the
extracted shadow sprites (from v9) boosted, masked to prop vicinity; cow keeps its synthetic shadow. Run when no TOOLING burst runs."""
import json, shutil, pathlib
import numpy as np
from PIL import Image
from scipy import ndimage
A = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-3/artifacts')
DST = A / 'CS-props-v11'; assert not DST.exists(); shutil.copytree(A / 'CS-props-v10', DST)
p = json.load(open(DST / 'props.json')); am = {a['name']: a for a in p['assets']}
# (1) ownership: a glow / crack emitter belongs to the instance whose sprite bbox contains it; orphans are dropped
boxes = []
for inst in p['instances']:
    a = am[inst['asset']]; im = Image.open(DST / a['file']); x, y = inst['position']; ax, ay = a['anchor']
    boxes.append((x - ax, y - ay, x - ax + im.width, y - ay + im.height))
def owned(px, py): return any(bx0 <= px <= bx1 and by0 <= py <= by1 for bx0, by0, bx1, by1 in boxes)
g0, q0 = len(p['glows']), len(p['particles'])
p['glows'] = [g for g in p['glows'] if g.get('z_parent', 'actors') != 'actors' or owned(*g['position'])]
p['particles'] = [q for q in p['particles'] if not q['name'].startswith('crack') or owned((q['rect'][0] + q['rect'][2]) / 2, (q['rect'][1] + q['rect'][3]) / 2)]
print('orphans removed: glows', g0 - len(p['glows']), 'emitters', q0 - len(p['particles']))
# (2) shadows: extracted sprites from v9, boosted, masked to prop vicinity
for sh in p['shadows']:
    if not sh['file'].endswith('cow_carcass.png') and (DST / sh['file']).exists(): (DST / sh['file']).unlink()
cow_shadow = [sh for sh in p['shadows'] if sh['file'].endswith('cow_carcass.png')]
v9 = json.load(open(A / 'CS-props-v9/props.json')); new = []
for sh in v9['shadows']:
    src = A / 'CS-props-v9' / sh['file']; arr = np.array(Image.open(src).convert('RGBA')).astype(np.float32); al = arr[..., 3] / 255.0
    ox, oy = sh['position']; H, W = al.shape
    keep = np.zeros((H, W), bool)
    for inst in p['instances']:
        a = am[inst['asset']]; im = Image.open(DST / a['file']); x, y = inst['position']; ax, ay = a['anchor']
        tall = im.height > 200; r = int(im.width * 0.75 + 60) if tall else int(max(im.width, 60) * 0.8 + 30)
        cx, cy = x - ox, y - oy
        if -r <= cx <= W + r and -r <= cy <= H + r:
            yy, xx = np.ogrid[0:H, 0:W]; e = ((xx - cx) / r) ** 2 + ((yy - cy + (r * 0.35 if tall else 0)) / (r * 0.7)) ** 2
            keep |= e <= 1.0
    soft = ndimage.gaussian_filter(keep.astype(np.float32), 18)
    al = np.clip(al * soft, 0, 1); al = np.clip(al ** 0.72 * 1.6, 0, 0.85)          # more pronounced
    arr[..., 3] = al * 255; out = 'shadows/' + pathlib.Path(sh['file']).name
    Image.fromarray(arr.astype(np.uint8), 'RGBA').save(DST / out)
    new.append({'file': out, 'position': sh['position'], 'opacity': 1.0}); print(out, 'kept alpha mean', round(float(al.mean()), 3))
p['shadows'] = new + cow_shadow
json.dump(p, open(DST / 'props.json', 'w'), indent=1)
print('shadows', len(p['shadows']), 'glows', len(p['glows']), 'particles', len(p['particles']))
