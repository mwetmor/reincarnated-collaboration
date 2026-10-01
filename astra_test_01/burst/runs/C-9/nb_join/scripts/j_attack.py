# THE NORMAL ATTACK (D2 A1 1SS; the timing packet b0f9d77fa: 16 frames, 15 ticks, the hit on tick 7). Route 1 (the conductor,
# 2026-10-01): 0 credits, the source already on his JOIN body -- chop_overhead_92 (Meshy 92 "Double Combo Attack", the
# overhead-chop window T12 grafted on his own rig; it passes the joint lint).
#
#   python3 scripts/j_attack.py <body.glb> <out.glb> [--src chop_overhead_92] [--cut 0.6333] [--end 0.9] [--name attack_a1] [--json f]
#
# A SINGLE STRIKE. The source window holds the overhead chop (the sword raised to 2.23 m, brought down to 0.92 m at 0.567 s,
# the tip at 20 m/s) and then the START of the combo's second blow (from 0.633 s: up to 1.52 m and down again at 19.6 m/s).
# The clip takes the source's keys from 0 to --cut (the chop and its end, where the tip has slowed to 2.3 m/s) and HOLDS that
# last key to --end, so the guard layers (layers.list guard_*_attack, the JOIN hold v3's idle guard) can bring the arms home:
# no second motion. Every key is the source's own (no resample); the hold re-keys the last pose on the 30 fps grid.
# CONTACT (casts.attack.release_s): the key where the sword's tip is lowest in the downswing -- the blow landing.
import json, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts"))
L = __import__('21_lint_export'); C = __import__('s17_loop_closure')
a = sys.argv[1:]; BODY, OUT = a[0], a[1]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
SRC = opt('--src', 'chop_overhead_92'); CUT = float(opt('--cut', '0.6333')); TEND = float(opt('--end', '0.9')); NAME = opt('--name', 'attack_a1')
js, b0 = L.load_glb(BODY); bn = bytearray(b0)
an = next(x for x in js['animations'] if x.get('name') == SRC)
grid = np.round(np.arange(0, TEND + 1e-6, 1 / 30.0), 6)
def put(data):
    while len(bn) % 4: bn.append(0)
    o = len(bn); bn.extend(data); return o
def acc(arr, typ, mm=False):
    arr = np.ascontiguousarray(arr, np.float32)
    js['bufferViews'].append(dict(buffer=0, byteOffset=put(arr.tobytes()), byteLength=arr.nbytes))
    ac = dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=int(arr.shape[0]), type=typ)
    if mm: ac['min'] = [float(v) for v in np.atleast_1d(arr.min(0))]; ac['max'] = [float(v) for v in np.atleast_1d(arr.max(0))]
    js['accessors'].append(ac); return len(js['accessors']) - 1
TYP = {1: 'SCALAR', 3: 'VEC3', 4: 'VEC4'}
samplers, channels, src_keys = [], [], None
for c in an['channels']:
    s = an['samplers'][c['sampler']]
    t = L.read_accessor(js, b0, s['input'])[:, 0].astype(float); v = L.read_accessor(js, b0, s['output']).astype(float); v = v.reshape(len(v), -1)
    keep = t <= CUT + 1e-4
    tt, vv = t[keep], v[keep]
    if len(tt) > 1: src_keys = len(tt)
    hold = grid[grid > tt[-1] + 1e-4]
    tt = np.concatenate([tt, hold]); vv = np.concatenate([vv, np.repeat(vv[-1:], len(hold), 0)])
    samplers.append(dict(input=acc(tt.reshape(-1, 1), 'SCALAR', True), output=acc(vv, TYP[vv.shape[1]]), interpolation=s.get('interpolation', 'LINEAR')))
    channels.append(dict(sampler=len(samplers) - 1, target=dict(c['target'])))
js['animations'] = [x for x in js['animations'] if x.get('name') != NAME] + [dict(name=NAME, samplers=samplers, channels=channels)]
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn))); f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
# the contact: the sword tip's lowest point in the downswing (after its highest)
m = C.model(OUT); nid = m['nid']; ks = np.round(np.arange(0, CUT + 1e-6, 1 / 30.0), 6)
def tip(G):
    R = G[nid['weapon_r']][:3, :3]; R = R / np.linalg.norm(R, axis=0); return G[nid['weapon_r']][:3, 3] + 0.7768 * R[:, 1]
P = np.array([tip(C.globals_at(m, NAME, float(t))) for t in ks]); ktop = int(np.argmax(P[:, 1])); kc = ktop + int(np.argmin(P[ktop:, 1]))
sp = np.linalg.norm(np.diff(P, axis=0), axis=1) * 30
rep = dict(clip=NAME, source=SRC, cut_s=CUT, end_s=TEND, keys=len(grid), source_keys_kept=src_keys,
           contact=dict(key=kc, t_s=round(float(ks[kc]), 4), tip_y_m=round(float(P[kc, 1]), 3), top_t_s=round(float(ks[ktop]), 4), top_y_m=round(float(P[ktop, 1]), 3),
                        definition="the key where the sword tip is lowest after its highest: the blow landing"),
           tip_speed_m_s=[round(float(x), 1) for x in sp], tip_y_m=[round(float(x), 2) for x in P[:, 1]])
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
print(json.dumps({k: rep[k] for k in ('clip', 'keys', 'contact')}))
