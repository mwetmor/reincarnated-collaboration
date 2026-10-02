# EN-E2 round 7: CUT THE ARM-LEG BRIDGES. Tripo fuses a hanging hand (or a strap's end) to the thigh it touches in the A-pose; the
# fused triangles carry arm weights on one side and leg weights on the other, and any lifted arm pulls them into a long bar
# (measured, the Mind-Taker: a 0.94 m bar from the right hand to the right thigh at walk 0.3; rest extent 0.00-0.03 m). The cut
# removes the triangles whose three vertices' DOMINANT bones include both an arm-chain bone (Arm / ForeArm / Hand) and a
# leg-chain bone (UpLeg / Leg / Foot / ToeBase). Vertices are kept; on the cut faces' vertices the NON-dominant chain's weight is
# dropped and the rest renormalised (a vertex left blended hand+thigh still draws a sliver: measured 0.35 m after the face cut alone).
#   python3 scripts/en55_bridge_cut.py <body.glb> [--apply <out.glb>] [--json r.json]
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R = __import__('49_recentre')
a = sys.argv[1:]; SRC = a[0]; OUT = a[a.index('--apply') + 1] if '--apply' in a else None; JS = a[a.index('--json') + 1] if '--json' in a else None
js, b = L.load_glb(SRC); b = bytearray(b)
mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]; rd = lambda i: np.asarray(L.read_accessor(js, b, i))
J = rd(pr['attributes']['JOINTS_0']).astype(int); Wt = rd(pr['attributes']['WEIGHTS_0']); I = rd(pr['indices']).astype(np.int64).reshape(-1, 3)
names = [js['nodes'][j]['name'] for j in js['skins'][js['nodes'][mn]['skin']]['joints']]
dom = J[np.arange(len(J)), np.argmax(Wt, 1)]
arm = np.array([any(n.endswith(s) for s in ('Arm', 'ForeArm', 'Hand')) and not n.endswith('Shoulder') for n in names])
leg = np.array([any(n.endswith(s) for s in ('UpLeg', 'Leg', 'Foot', 'ToeBase')) for n in names])
fa = arm[dom[I]].any(1); fl = leg[dom[I]].any(1); cut = fa & fl
from collections import Counter
pairs = Counter(tuple(sorted({names[d] for d in dom[f]})) for f in I[cut])
rep = dict(body=SRC, faces=len(I), cut=int(cut.sum()), pairs={' + '.join(k): v for k, v in pairs.most_common(10)})
print('BRIDGE', os.path.basename(SRC), 'faces %d, arm-leg bridge faces %d' % (len(I), cut.sum()), dict(pairs.most_common(4)))
if OUT:
    vs = np.unique(I[cut].ravel()); Wn = Wt.astype(np.float32).copy(); fixed = 0
    for v in vs:
        other = leg if arm[dom[v]] else arm if leg[dom[v]] else None
        if other is None: continue
        z = other[J[v]] & (Wn[v] > 0)
        if z.any(): Wn[v, z] = 0; Wn[v] /= Wn[v].sum(); fixed += 1
    woff = W.append(b, Wn.tobytes()); js['bufferViews'].append(dict(buffer=0, byteOffset=woff, byteLength=Wn.nbytes, target=34962))
    wa = dict(js['accessors'][pr['attributes']['WEIGHTS_0']]); wa.update(bufferView=len(js['bufferViews']) - 1); wa.pop('byteOffset', None)
    js['accessors'].append(wa); pr['attributes']['WEIGHTS_0'] = len(js['accessors']) - 1; rep['verts_unblended'] = fixed
    keep = I[~cut].astype(np.uint32).ravel()
    off = W.append(b, keep.tobytes()); js['bufferViews'].append(dict(buffer=0, byteOffset=off, byteLength=keep.nbytes, target=34963))
    js['accessors'].append(dict(bufferView=len(js['bufferViews']) - 1, componentType=5125, count=int(len(keep)), type='SCALAR'))
    pr['indices'] = len(js['accessors']) - 1; js['buffers'][0]['byteLength'] = len(b)
    R.write_glb(OUT, js, b); rep['out'] = OUT; print('  wrote', OUT, '(%d faces; %d bridge vertices un-blended)' % (len(keep) // 3, fixed))
if JS: json.dump(rep, open(JS, 'w'), indent=1)
