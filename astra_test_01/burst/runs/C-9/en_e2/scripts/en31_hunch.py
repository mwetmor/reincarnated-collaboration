# EN-E2 round 4, a NAMED EDIT over every clip: the bog-wretch's FERAL HUNCH (the conductor: "a forward spine hunch, a named edit applied
# over the clips as you did with the head lift"). Pure glTF edit; every clip keeps its own keys.
#   python3 scripts/en31_hunch.py <in.glb> <out.glb> --spine 14 --chest 12 --neck -16 [--clips a,b] [--json f]
# Each named bone gets a CONSTANT extra bend about its own rest-frame axis that is world +X at rest (the figure's right->left axis), applied
# AFTER the clip's own rotation (q' = q_clip * delta, delta in the bone's own frame): positive = bend FORWARD (measured below: the head moves
# toward +Z, the facing). spine = Spine01 (mid back), chest = Spine (upper back), neck = neck (negative lifts the head back up so the gaze
# stays forward over a rounded back). Un-keyed bones get a constant track. The death (whose body ends lying down) takes it too: the hunch
# is the creature's shape, not a pose.
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre'); G55 = __import__('55_clip_graft')
a = sys.argv[1:]; IN, OUT = a[0], a[1]
o = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
BEND = {'Spine01': o('--spine', 14.0), 'Spine': o('--chest', 12.0), 'neck': o('--neck', -16.0)}
js, b = L.load_glb(IN); bn = bytearray(b)
G0, _ = G55.world_rest(js); idx = {n.get('name'): i for i, n in enumerate(js['nodes'])}
def qmul(p, q):
    x1, y1, z1, w1 = p; x2, y2, z2, w2 = q
    return np.array([w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2, w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2])
delta = {}
for nm, deg in BEND.items():
    Rw = G0[idx[nm]][:3, :3]; Rw = Rw / np.linalg.norm(Rw, axis=0)
    ax = Rw.T @ np.array([1.0, 0.0, 0.0]); ax /= np.linalg.norm(ax); th = np.radians(deg)
    delta[nm] = np.concatenate([ax * np.sin(th / 2), [np.cos(th / 2)]])
def acc(arr, typ):
    arr = np.asarray(arr, np.float32); data = arr.tobytes(); off = W.append(bn, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    d = {"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(arr.shape[0]), "type": typ}
    if typ == "SCALAR": d["min"] = [float(arr.min())]; d["max"] = [float(arr.max())]
    js['accessors'].append(d); return len(js['accessors']) - 1
CLIPS = a[a.index('--clips') + 1].split(',') if '--clips' in a else None
rep = dict(bend_deg=BEND, clips=[])
for an in js['animations']:
    if an['name'].startswith('Armature|') or (CLIPS and an['name'] not in CLIPS): continue
    for nm, dq in delta.items():
        n = idx[nm]; ch = next((c for c in an['channels'] if c['target']['node'] == n and c['target']['path'] == 'rotation'), None)
        if ch is not None:
            s = an['samplers'][ch['sampler']]; q = np.asarray(L.read_accessor(js, bn, s['output']))
            s['output'] = acc(np.array([qmul(x, dq) for x in q]), "VEC4")
        else:
            t = sorted({float(x) for c in an['channels'] for x in L.read_accessor(js, bn, an['samplers'][c['sampler']]['input']).reshape(-1)})
            qr = np.array(js['nodes'][n].get('rotation', [0, 0, 0, 1]), float)
            an['samplers'].append({"input": acc(np.array([t[0], t[-1]]), "SCALAR"), "output": acc(np.array([qmul(qr, dq)] * 2), "VEC4"), "interpolation": "LINEAR"})
            an['channels'].append({"sampler": len(an['samplers']) - 1, "target": {"node": n, "path": "rotation"}})
    rep['clips'].append(an['name'])
js['buffers'][0]['byteLength'] = len(bn); R_.write_glb(OUT, js, bn)
C = __import__('s17_loop_closure'); m = C.model(OUT)
hd = [i for i in m['joints'] if m['nodes'][i].get('name') == 'Head'][0]; hp = [i for i in m['joints'] if m['nodes'][i].get('name') == 'Hips'][0]
t0 = min(float(t) for v in m['anims']['idle'].values() for t in v[0]); Gx = C.globals_at(m, 'idle', t0)
rep['idle_head_forward_of_hips_m'] = round(float(Gx[hd][2, 3] - Gx[hp][2, 3]), 4)
print('HUNCH', json.dumps(rep))
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
