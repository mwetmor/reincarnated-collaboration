# R-C9-152: why the hood reads transparent at the top and back -- the hood piece's OPEN EDGES (boundary loops of the welded
# mesh), each loop's size, centre, extent and perimeter, and the hood material's culling. The hair used to fill these holes.
#   python3 r152_01_hood_holes.py <hood.glb> [--json out]
import sys, os, json, numpy as np
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
P = sys.argv[1]
js, b = L.load_glb(P); G, _ = W.globals_(js)
mi = next(i for i, n in enumerate(js['nodes']) if 'mesh' in n and 'skin' in n)
V = W.skin_rest(js, b, mi, G); pr = js['meshes'][js['nodes'][mi]['mesh']]['primitives'][0]
I = L.read_accessor(js, b, pr['indices']).astype(int).reshape(-1, 3)
key = np.round(V / 1e-5).astype(np.int64); _, wid = np.unique(key, axis=0, return_inverse=True); wid = wid.ravel(); T = wid[I]
Vw = np.zeros((wid.max() + 1, 3)); Vw[wid] = V
cnt = defaultdict(int); orient = {}
for t in T:
    for a, c in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
        cnt[(min(a, c), max(a, c))] += 1; orient[(a, c)] = True
bd = [e for e, n in cnt.items() if n == 1]
nxt = defaultdict(list)
for a, c in bd: nxt[a].append(c); nxt[c].append(a)
seen = set(); loops = []
for s in list(nxt):
    if s in seen: continue
    loop = [s]; seen.add(s); prev = None; cur = s
    while True:
        cand = [x for x in nxt[cur] if x != prev and x not in seen]
        if not cand: break
        prev, cur = cur, cand[0]; loop.append(cur); seen.add(cur)
    loops.append(loop)
rows = []
for lp in loops:
    p = Vw[lp]; per = float(np.linalg.norm(np.diff(np.vstack([p, p[:1]]), axis=0), axis=1).sum())
    rows.append(dict(n=len(lp), perimeter_m=round(per, 3), centre=p.mean(0).round(3).tolist(), ymin=round(float(p[:, 1].min()), 3),
                     ymax=round(float(p[:, 1].max()), 3), zmin=round(float(p[:, 2].min()), 3), zmax=round(float(p[:, 2].max()), 3), verts=[int(x) for x in lp]))
rows.sort(key=lambda r: -r['perimeter_m'])
mat = js['materials'][0]
print('material doubleSided:', mat.get('doubleSided', False), '| loops:', len(rows), '| boundary edges:', len(bd))
for r in rows[:25]:
    print('n %4d per %.3f m centre %s y %.3f..%.3f z %+.3f..%+.3f' % (r['n'], r['perimeter_m'], r['centre'], r['ymin'], r['ymax'], r['zmin'], r['zmax']))
if '--json' in sys.argv:
    json.dump(dict(file=P, double_sided=mat.get('doubleSided', False), loops=rows), open(sys.argv[sys.argv.index('--json') + 1], 'w'))
