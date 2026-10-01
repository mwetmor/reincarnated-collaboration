# A LOOK, NOT A CLIP CHANGE: a one-shot as the JOIN runtime would play it under the D2 timing packet's law (collab
# b0f9d77fa) -- TOTAL game ticks at 25/s, the release on tick ACTION, the port's TWO-SEGMENT WARP (contract § 1.2):
# [0, release_s] of the authored clip -> [0, ACTION ticks]; [release_s, T] -> [ACTION, TOTAL ticks].
#
#   python3 scripts/j_law_retime.py <body.glb> <out.glb> <clip> <release_s> <total_ticks> <action_tick> [--layers in.json --layers-out out.json]
#
# Writes <clip>_law beside <clip> (keys on the 30 fps grid, each sampled from the authored clip at its warped time: slerp
# for rotations, lerp otherwise -- glTF LINEAR), and, with --layers, a copy of the layer list whose layers for <clip> also
# name <clip>_law, their weight-curve key times warped the same way.
import json, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); B = __import__('j_blend')
a = sys.argv[1:]; BODY, OUT, CLIP = a[:3]; RS, TT, AT = float(a[3]), int(a[4]), int(a[5])
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
js, b0 = L.load_glb(BODY); bn = bytearray(b0)
an = next(x for x in js['animations'] if x.get('name') == CLIP)
T = max(float(L.read_accessor(js, b0, s['input']).max()) for s in an['samplers'])
TS, TA = TT * 0.04, AT * 0.04


def src_t(tau):
    return tau / TA * RS if tau <= TA else RS + (tau - TA) / (TS - TA) * (T - RS)


def out_t(t):
    return t / RS * TA if t <= RS else TA + (t - RS) / (T - RS) * (TS - TA)


grid = np.unique(np.round(np.append(np.arange(0, TS, 1 / 30.0), TS), 6))
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
ti = acc(grid.reshape(-1, 1), 'SCALAR', True); samplers, channels = [], []
for c in an['channels']:
    s = an['samplers'][c['sampler']]; t = L.read_accessor(js, b0, s['input'])[:, 0].astype(float)
    v = L.read_accessor(js, b0, s['output']).astype(float); v = v.reshape(len(v), -1); rot = c['target']['path'] == 'rotation'
    out = []
    for tau in grid:
        x = src_t(float(tau))
        if len(t) == 1 or x <= t[0]: out.append(v[0]); continue
        if x >= t[-1]: out.append(v[-1]); continue
        k = int(np.searchsorted(t, x, side='right')) - 1; u = (x - t[k]) / max(t[k + 1] - t[k], 1e-12)
        out.append(B.slerp(v[k], v[k + 1], u) if rot else (1 - u) * v[k] + u * v[k + 1])
    out = np.array(out, float)
    if rot:
        for k in range(1, len(out)):
            if out[k] @ out[k - 1] < 0: out[k] = -out[k]
    samplers.append(dict(input=ti, output=acc(out, TYP[out.shape[1]]), interpolation='LINEAR'))
    channels.append(dict(sampler=len(samplers) - 1, target=dict(c['target'])))
NAME = CLIP + '_law'
js['animations'] = [x for x in js['animations'] if x.get('name') != NAME] + [dict(name=NAME, samplers=samplers, channels=channels)]
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn))); f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
if opt('--layers'):
    Ls = json.load(open(opt('--layers'))); add = []
    for ly in Ls:
        if CLIP in ly.get('states', []):
            n = json.loads(json.dumps(ly)); n['name'] = ly['name'] + '_law'; n['states'] = [NAME]
            if 'weight_curve' in n: n['weight_curve']['keys'] = [[round(out_t(min(k[0], T)), 4), k[1]] for k in n['weight_curve']['keys']]
            add.append(n)
    json.dump(Ls + add, open(opt('--layers-out'), 'w'), indent=1)
print(json.dumps(dict(clip=CLIP, authored_T=round(T, 4), release_s=RS, law=dict(total_ticks=TT, action_tick=AT, T_s=TS, release_s=TA),
                      head_speedup=round(RS / TA, 3), tail_speedup=round((T - RS) / (TS - TA), 3), keys=len(grid))))
