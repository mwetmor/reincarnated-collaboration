# EN-E2 round 3, THE WRAITH'S MOTION: it floats, so its grafted Pro Magic clips are turned into HOVER clips by a pure glTF edit.
#   python3 scripts/en24_hover.py <in.glb> <out.glb> --lift 0.25 --bob 0.035 [--json f]
# Per clip (every clip in the file except Meshy's own 'Armature|...'):
#   LEGS   every leg channel (Left/Right UpLeg, Leg, Foot, ToeBase) is DROPPED, so glTF plays the legs at REST: they hang straight inside
#          the shroud's tail and never kick it about (the Pro Magic legs walk and brace; a shroud has nothing to walk with).
#   HOVER  the Hips rise by --lift metres (world up) plus a bob of --bob metres, sin(2 pi t / P): P = the clip length for loops
#          (one bob per cycle, so the loop still closes to the bit), 1.8 s for one-shots.
# NEW CLIPS (30 fps keys, built from the grafted ones):
#   glide   = idle's own keys, the whole figure leant FORWARD --lean deg about the hips (world right axis) + the bob; in place
#             (the runtime translates it). It serves the roster's walk AND run (both are its glide/run clip).
#   emerge  = 0.8667 s (the roster's spawn clip length, 26 intervals): the figure UNFOLDS UP FROM THE FLOOR -- hips from --emerge-hips
#             (0.35 m) above the floor, leant --emerge-lean (55 deg) forward (the shroud lying along the floor), to the idle's first pose at hover height, smoothstep.
#             It never passes below the floor (the cells have no floor to hide it); a fade-in is the runtime's.
#   death   = the source death clip's upper body, the hips sinking to --death-hips (0.40 m) and a forward slump to 35 deg by the end:
#             the wraith sinks to the floor and crumples (legs folded back to keep the tail above the floor); the DISSIPATE (fade) is the runtime's alpha ramp on the held last frame (nothing baked).
# Units: metres in WORLD (pre-e19 scale); Hips translation is written in its parent's frame (inverse of the parent's world matrix).
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre'); G55 = __import__('55_clip_graft')
a = sys.argv[1:]; IN, OUT = a[0], a[1]
opt = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
LIFT, BOB, LEAN = opt('--lift', 0.25), opt('--bob', 0.035), opt('--lean', 14.0)
DEATH_HIPS, EM_HIPS, EM_LEAN = opt('--death-hips', 0.40), opt('--emerge-hips', 0.35), opt('--emerge-lean', 55.0)
LEGS = {s + p for s in ('Left', 'Right') for p in ('UpLeg', 'Leg', 'Foot', 'ToeBase')}
js, b = L.load_glb(IN); bn = bytearray(b)
name_of = {i: n.get('name') for i, n in enumerate(js['nodes'])}; idx = {v: k for k, v in name_of.items()}
hips = idx['Hips']
G0, par = G55.world_rest(js); P = G0[par[hips]]; Pinv = np.linalg.inv(P); P3 = P[:3, :3]
Rp = P3 / np.linalg.norm(P3, axis=0)                     # the parent's world ROTATION (columns normalised)
up_local = Pinv[:3, :3] @ np.array([0.0, 1.0, 0.0])      # one world metre up, in the Hips' parent frame
q_rest_h = np.array(js['nodes'][hips].get('rotation', [0, 0, 0, 1]), float)
t_rest_h = np.array(js['nodes'][hips].get('translation', [0, 0, 0]), float)
def qmul(p, q):
    x1, y1, z1, w1 = p; x2, y2, z2, w2 = q
    return np.array([w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2, w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2])
def lean_q(deg):
    """the Hips' LOCAL rotation that leans the whole figure forward by deg (world: about +X, which tips +Y toward +Z = forward)"""
    th = np.radians(deg); Rx = np.array([[1, 0, 0], [0, np.cos(th), -np.sin(th)], [0, np.sin(th), np.cos(th)]])
    return W.m2q(Rp.T @ Rx @ Rp)
def acc(arr, typ):
    arr = np.asarray(arr, np.float32); data = arr.tobytes(); off = W.append(bn, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    d = {"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(arr.shape[0]), "type": typ}
    if typ == "SCALAR": d["min"] = [float(arr.min())]; d["max"] = [float(arr.max())]
    js['accessors'].append(d); return len(js['accessors']) - 1
def get(anim):
    trk = G55.tracks(js, bn, anim)
    return {name_of[n]: {p: (t.copy(), v.copy()) for p, (t, v, _) in d.items()} for n, d in trk.items()}
def put(name, trk):
    ch, sm = [], []
    for nm, d in trk.items():
        if nm in LEGS and not d.get('_keep'): continue
        d = {k: v for k, v in d.items() if k != '_keep'}
        for p, (t, v) in d.items():
            if p == 'rotation':
                v = np.array(v)
                for j in range(1, len(v)):
                    if np.dot(v[j], v[j - 1]) < 0: v[j] = -v[j]
            sm.append({"input": acc(np.asarray(t).reshape(-1), "SCALAR"), "output": acc(v, {"rotation": "VEC4", "translation": "VEC3", "scale": "VEC3"}[p]), "interpolation": "LINEAR"})
            ch.append({"sampler": len(sm) - 1, "target": {"node": idx[nm], "path": p}})
    js['animations'] = [x for x in js['animations'] if x.get('name') != name] + [{"name": name, "channels": ch, "samplers": sm}]
def hips_track(trk, times):
    """Hips rotation/translation sampled at `times` (falling back to rest where un-keyed)"""
    d = trk.get('Hips', {})
    rot = np.array([G55.sample((d['rotation'][0], d['rotation'][1], 'LINEAR'), t, 'rotation') if 'rotation' in d else q_rest_h for t in times])
    tr = np.array([G55.sample((d['translation'][0], d['translation'][1], 'LINEAR'), t, 'translation') if 'translation' in d else t_rest_h for t in times])
    return rot, tr
def resample(trk, times):
    out = {}
    for nm, d in trk.items():
        out[nm] = {p: (np.array(times), np.array([G55.sample((t, v, 'LINEAR'), x, p) for x in times])) for p, (t, v) in d.items()}
    return out

LLEG = float(G0[hips][1, 3])                              # rest hips height = the shroud's length below the hips (the mesh is grounded at rest)
def fold_legs(trk, times, rot_h, tr_h, lean_deg):
    """keep the shroud's tail ABOVE the floor while the hips are low and leant: per frame, the leg's actual world direction (the
    rest hips->toe offset carried by the Hips' world rotation) is turned further about world +X (the sense that lifts it behind)
    by the smallest delta (0.5-deg scan) that keeps the toe at least 0.03 m above the floor. lean_deg is unused (kept for the log)."""
    out = {}
    Ghi = np.linalg.inv(G0[hips])
    for side in ('Left', 'Right'):
        nm = side + 'UpLeg'; qr = np.array(js['nodes'][idx[nm]].get('rotation', [0, 0, 0, 1]), float); qs = []
        toe_h = (Ghi @ G0[idx[side + 'ToeBase']])[:3, 3]; hip_ul = (Ghi @ G0[idx[nm]])[:3, 3]
        for q_h, t_h in zip(rot_h, tr_h):
            hw = (P @ np.append(t_h, 1.0))[:3]; Rhw = Rp @ W.q2m(q_h); Rhw = Rhw / np.linalg.norm(Rhw, axis=0)
            sc = np.linalg.norm(G0[hips][:3, :3], axis=0).mean()
            base = hw + Rhw @ (hip_ul * sc); v = Rhw @ ((toe_h - hip_ul) * sc)
            d = 0.0
            for dd in np.arange(0.0, 120.5, 0.5):
                th = np.radians(dd); y = v[1] * np.cos(th) - v[2] * np.sin(th)
                if base[1] + y >= 0.03: d = dd; break
            else: d = 120.0
            th = np.radians(d); Rx = np.array([[1, 0, 0], [0, np.cos(th), -np.sin(th)], [0, np.sin(th), np.cos(th)]])
            qs.append(qmul(W.m2q(Rhw.T @ Rx @ Rhw), qr))
        out[nm] = {'rotation': (np.array(times), np.array(qs))}
    return out
LEGS_KEEP = set()
anims = [x for x in js['animations'] if not x['name'].startswith('Armature|')]
src = {x['name']: get(x) for x in anims}
rep = dict(lift_m=LIFT, bob_m=BOB, lean_deg=LEAN, clips={})
LOOPS = ('idle', 'walk', 'run')
for name, trk in src.items():
    if name in ('walk', 'run'): continue           # the wraith has no legs to walk on: glide replaces both (below)
    times = sorted({float(x) for d in trk.values() for t, _ in d.values() for x in t})
    T = times[-1] - times[0]; Pb = T if name in LOOPS else 1.8
    trk = resample(trk, times); rot, tr = hips_track(trk, times)
    t0 = np.array(times) - times[0]
    if name == 'death':
        u = np.clip(t0 / max(T, 1e-9), 0, 1); s = u * u * (3 - 2 * u)
        hy = np.array([float((P @ np.append(x, 1.0))[1]) for x in tr])     # the clip's own hips height (grounded)
        lift = (LIFT + BOB * np.sin(2 * np.pi * t0 / Pb)) * (1 - s) + s * (DEATH_HIPS - hy)   # sink to a crumpled pile, hips at DEATH_HIPS
        rot = np.array([qmul(lean_q(35.0 * s_), q) for s_, q in zip(s, rot)])
    else:
        lift = LIFT + BOB * np.sin(2 * np.pi * t0 / Pb)
    tr = tr + lift[:, None] * up_local[None, :]
    trk['Hips'] = {'rotation': (np.array(times), rot), 'translation': (np.array(times), tr)}
    if name == 'death':
        for k, v in fold_legs(trk, times, rot, tr, 35.0 * s).items(): trk[k] = dict(v, _keep=True)
    put(name, trk); rep['clips'][name] = dict(keys=len(times), length_s=round(T, 4), bob_period_s=round(Pb, 4), legs='rest (channels dropped)')
# glide: idle + lean + bob (bob period = the idle's length so the loop closes)
it = src['idle']; times = sorted({float(x) for d in it.values() for t, _ in d.values() for x in t}); T = times[-1] - times[0]
g = resample(it, times); rot, tr = hips_track(g, times); t0 = np.array(times) - times[0]
lq = lean_q(LEAN); rot = np.array([qmul(lq, q) for q in rot])
tr = tr + (LIFT + BOB * np.sin(2 * np.pi * t0 / T))[:, None] * up_local[None, :]
g['Hips'] = {'rotation': (np.array(times), rot), 'translation': (np.array(times), tr)}
put('glide', g); rep['clips']['glide'] = dict(keys=len(times), length_s=round(T, 4), lean_deg=LEAN, from_='idle', in_place=True)
# emerge: idle's FIRST pose held, the hips path from floor + 0.15 m leant 70 deg to hover height upright
times = [i / 30.0 for i in range(27)]; T = times[-1]
e = {nm: {p: (np.array(times), np.repeat(G55.sample((t, v, 'LINEAR'), it_t0 := min(float(x) for x in t), p)[None, :], len(times), 0)) for p, (t, v) in d.items()} for nm, d in it.items()}
rot0, tr0 = hips_track(it, [min(float(x) for d in it.values() for t, _ in d.values() for x in t)])
G_hips_y = float((P @ np.append(tr0[0], 1.0))[1])           # the hips' world height in the idle's first pose (grounded)
u = np.array(times) / T; s = u * u * (3 - 2 * u)
start_drop = (G_hips_y + LIFT) - EM_HIPS                        # from hips at 0.15 m above the floor ...
lift = LIFT - start_drop * (1 - s)                           # ... to hover height
rot = np.array([qmul(lean_q(EM_LEAN * (1 - s_)), rot0[0]) for s_ in s])
tr = tr0[0][None, :] + lift[:, None] * up_local[None, :]
e['Hips'] = {'rotation': (np.array(times), rot), 'translation': (np.array(times), tr)}
for k, v in fold_legs(e, times, rot, tr, EM_LEAN * (1 - s)).items(): e[k] = dict(v, _keep=True)
put('emerge', e); rep['clips']['emerge'] = dict(keys=len(times), length_s=round(T, 4), start_hips_above_floor_m=EM_HIPS, start_lean_deg=EM_LEAN,
                                                 note='roster spawn clip 0.8667 s (wraith_spawn_a01, 27 frames); p05 hero members; a fade-in is the runtime\'s')
js['animations'] = [x for x in js['animations'] if x['name'] not in ('walk', 'run')]
js['buffers'][0]['byteLength'] = len(bn); R_.write_glb(OUT, js, bn)
res = L.lint(OUT); rep['lint'] = dict(verdict=res['verdict'], fails=res['fails'])
print('HOVER', json.dumps(rep))
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
