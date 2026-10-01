# E1 HEIGHT: Meshy's rigging returned him at 1.70 m (the base was prepped at 1.96 m, and character_height 1.96 was posted --
# found by measuring the rigged skin at rest, not assumed). He is the TOWERING one (R-C9-113), so the Armature root of the
# body and of EVERY piece is scaled by the same factor; joints, IBMs, clips and the weapon mount are untouched (a skinned mesh
# draws at joint-global x IBM, so a root scale scales the drawn figure about the origin, feet stay on the floor).
#   python3 e19_height.py <target_m> <in.glb> ... --out <dir>
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
a = sys.argv[1:]; out = a[a.index('--out') + 1]; files = [x for x in a[1:] if x != out and x != '--out']; tgt = float(a[0])
os.makedirs(out, exist_ok=True)
js, b = L.load_glb(files[0]); G, _ = W.globals_(js); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
V = W.skin_rest(js, b, mn, G); h0 = float(V[:, 1].max() - V[:, 1].min()); k = tgt / h0
rep = dict(measured_height_m=round(h0, 4), target_m=tgt, factor=round(k, 6), files={})
for f in files:
    js, b = L.load_glb(f); par = {c for n in js['nodes'] for c in n.get('children', [])}
    root = [i for i in js['scenes'][0]['nodes']]
    for i in root:
        s = js['nodes'][i].get('scale', [1, 1, 1]); js['nodes'][i]['scale'] = [float(x * k) for x in s]
    p = os.path.join(out, os.path.basename(f)); R_.write_glb(p, js, bytearray(b))
    js2, b2 = L.load_glb(p); G2, _ = W.globals_(js2); m2 = next(i for i, n in enumerate(js2['nodes']) if 'skin' in n and 'mesh' in n)
    V2 = W.skin_rest(js2, b2, m2, G2); r = L.lint(p)
    rep['files'][os.path.basename(f)] = dict(height_after=round(float(V2[:, 1].max() - V2[:, 1].min()), 4), floor=round(float(V2[:, 1].min()), 4), lint=r['verdict'], fails=r['fails'])
    print(os.path.basename(f), rep['files'][os.path.basename(f)])
json.dump(rep, open(os.path.join(out, 'height.json'), 'w'), indent=1)
