# EN-E2 round 4: build a clip by CONCATENATING two grafted clips on their own keys (pure glTF edit; no resampling inside either part).
#   python3 scripts/en29_concat.py <in.glb> <out.glb> <new_name> <clipA>@<t0>:<t1> <clipB>[@<t0>:<t1>] [--drop clipA,clipB] [--blend n]
# Part A's window [t0, t1] (its own key times inside it), then all of part B shifted to start one key interval (1/30 s) after A's end,
# with B's first --blend keys (default 4) cross-faded from A's last pose (slerp / lerp), so the joint has no pop. Channels present in only
# one part are held at that part's value through the other. Used for the brute's EMERGE: crouch idle (held) -> crouch to standing idle.
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre'); G55 = __import__('55_clip_graft')
a = sys.argv[1:]; IN, OUT, NEW, SA, SB = a[:5]
BL = int(a[a.index('--blend') + 1]) if '--blend' in a else 4
DROP = a[a.index('--drop') + 1].split(',') if '--drop' in a else []
js, b = L.load_glb(IN); bn = bytearray(b)
an = {x['name']: x for x in js['animations']}
ca, win = SA.split('@'); t0, t1 = (float(x) for x in win.split(':'))
cb, wb = (SB.split('@') + [None])[:2]                       # round 5: part B may carry its own window too (clipB@t0:t1)
b0, b1 = (float(x) for x in wb.split(':')) if wb else (-1e9, 1e9)
TA = G55.tracks(js, bn, an[ca]); TB = G55.tracks(js, bn, an[cb])
keysA = sorted({float(x) for d in TA.values() for t, _, _ in d.values() for x in t if t0 - 1e-6 <= x <= t1 + 1e-6})
keysB = sorted({float(x) for d in TB.values() for t, _, _ in d.values() for x in t if b0 - 1e-6 <= x <= b1 + 1e-6})
dt = 1 / 30.0; off = keysA[-1] - keysA[0] + dt - keysB[0]
times = [k - keysA[0] for k in keysA] + [k + off for k in keysB]
targets = {(n, p) for d in (TA, TB) for n, dd in d.items() for p in dd}
def acc(arr, typ):
    arr = np.asarray(arr, np.float32); data = arr.tobytes(); o = W.append(bn, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": o, "byteLength": len(data)})
    d = {"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(arr.shape[0]), "type": typ}
    if typ == "SCALAR": d["min"] = [float(arr.min())]; d["max"] = [float(arr.max())]
    js['accessors'].append(d); return len(js['accessors']) - 1
ti = acc(np.array(times), "SCALAR"); ch, sm = [], []
def val(T, n, p, t, fallback):
    return G55.sample(T[n][p], t, p) if n in T and p in T[n] else fallback
for (n, p) in sorted(targets):
    rest = {'rotation': js['nodes'][n].get('rotation', [0, 0, 0, 1]), 'translation': js['nodes'][n].get('translation', [0, 0, 0]),
            'scale': js['nodes'][n].get('scale', [1, 1, 1])}[p]
    va = [val(TA, n, p, k, np.array(rest, float)) for k in keysA]
    vb = [val(TB, n, p, k, np.array(rest, float)) for k in keysB]
    last = va[-1]
    for i in range(min(BL, len(vb))):
        u = (i + 1) / (BL + 1); s = u * u * (3 - 2 * u)
        vb[i] = G55.slerp(last, vb[i], s) if p == 'rotation' else last + s * (vb[i] - last)
    v = np.array(va + vb)
    if p == 'rotation':
        for j in range(1, len(v)):
            if np.dot(v[j], v[j - 1]) < 0: v[j] = -v[j]
    sm.append({"input": ti, "output": acc(v, {"rotation": "VEC4", "translation": "VEC3", "scale": "VEC3"}[p]), "interpolation": "LINEAR"})
    ch.append({"sampler": len(sm) - 1, "target": {"node": n, "path": p}})
js['animations'] = [x for x in js['animations'] if x['name'] != NEW and x['name'] not in DROP] + [{"name": NEW, "channels": ch, "samplers": sm}]
js['buffers'][0]['byteLength'] = len(bn); R_.write_glb(OUT, js, bn)
print('CONCAT %s = %s[%.3f..%.3f] (%d keys) + %s (%d keys, first %d blended): %.4f s; dropped %s' % (NEW, ca, t0, t1, len(keysA), SB, len(keysB), BL, times[-1], DROP))
if '--json' in a: json.dump(dict(new=NEW, a=SA, b=SB, keys=len(times), length_s=round(times[-1], 4), blend=BL), open(a[a.index('--json') + 1], 'w'), indent=1)
