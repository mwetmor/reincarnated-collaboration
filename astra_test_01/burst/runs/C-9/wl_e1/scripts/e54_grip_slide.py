# GRIP SLIDE for named clips (R-C9-132, the DK extended spin): the haft SLID OUTWARD through his fists by S metres along
# weapon_r's own +Y, as a weapon_r TRANSLATION track keyed on the clip's existing weapon_r rotation keys. Why: with his fists
# 0.80 m out, the stock grip (pommel 0.64 m behind the right fist) puts the pommel at ~0.16 m from his axis -- in his chest.
# Sliding moves the whole mace, so the effect's tip read (weapon_r origin + tip along +Y) stays exact; weapon_r's ORIGIN is then
# S metres head-ward of the right fist in these clips only (the rest/mount is unchanged).
#   python3 e54_grip_slide.py <in.glb> <out.glb> --slide 0.20 --clips eor_spin_start,eor_spin_loop [--H 1.96]
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre'); CH = __import__('54_weapon_channel')
a = sys.argv[1:]; IN, OUT = a[0], a[1]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
S = float(opt('--slide')); CL = opt('--clips').split(','); HT = float(opt('--H', '1.96'))
js, b0 = L.load_glb(IN); bn = bytearray(b0); nd = {n.get('name'): i for i, n in enumerate(js['nodes'])}
G0, _ = W.globals_(js); mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
K = HT / float(np.ptp(W.skin_rest(js, bytes(bn), mn, G0)[:, 1]))
par = next(i for i, n in enumerate(js['nodes']) if nd['weapon_r'] in n.get('children', []))
ps = float(np.cbrt(np.linalg.det(G0[par][:3, :3])))
t_rest = np.array(js['nodes'][nd['weapon_r']].get('translation', [0, 0, 0]), float); s_loc = S / K / ps
def q2m(q):
    x, y, z, w = q; return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
rep = {}
for an in js['animations']:
    if an['name'] not in CL: continue
    rc = next(c for c in an['channels'] if c['target']['node'] == nd['weapon_r'] and c['target']['path'] == 'rotation')
    sm = an['samplers'][rc['sampler']]; qs = L.read_accessor(js, bytes(bn), sm['output']).reshape(-1, 4)
    tr = np.array([t_rest + q2m(q)[:, 1] * s_loc for q in qs])
    an['channels'] = [c for c in an['channels'] if not (c['target']['node'] == nd['weapon_r'] and c['target']['path'] == 'translation')]
    an['samplers'].append({"input": sm['input'], "output": CH.add_accessor(js, bn, tr, "VEC3"), "interpolation": "LINEAR"})
    an['channels'].append({"sampler": len(an['samplers']) - 1, "target": {"node": nd['weapon_r'], "path": "translation"}}); rep[an['name']] = len(qs)
js['buffers'][0]['byteLength'] = len(bn) + (-len(bn) % 4); R_.write_glb(OUT, js, bn)
print(json.dumps(dict(slide_m=S, slide_local=round(s_loc, 4), keyed=rep)))
