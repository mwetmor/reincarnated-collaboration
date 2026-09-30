# Append a POSE CLIP (2-key STEP, every named bone's local rotation) to a body GLB -- a binary patch, every other byte kept.
#
#   python3 scripts/j_pose_clip.py <body.glb> <out.glb> <name> (--from <clip>[@t] [--bones a,b,..] [--mirror] | --locals-json f)
#
# --mirror carries the RIGHT arm's locals onto the LEFT arm across his sagittal plane: q -> (x, -y, -z, w), the rig's
# own left/right convention (the arm chain's rests match that mirror within 2.5 deg: measured). Used for the
# PROVISIONAL left guard (a mirror of axe_guard_R) until the scene drax's join_guard_L lands.
import json, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts"))
L = __import__('21_lint_export'); C = __import__('s17_loop_closure')
a = sys.argv[1:]; BODY, OUT, NAME = a[0], a[1], a[2]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
MIR = '--mirror' in a
m = C.model(BODY)
loc = {}
if opt('--locals-json'):
    # --locals-json f: a solver's output {"locals": {bone: {"r": [x, y, z, w]}}} -- the pose written as it was solved
    src = opt('--locals-json')
    for bnm, v in json.load(open(src))['locals'].items():
        loc[bnm] = np.array(v['r'], float)
    bones = list(loc)
else:
    src = opt('--from'); sc, st = (src.split('@') + ['0'])[:2]; st = float(st)
    bones = opt('--bones').split(',') if opt('--bones') else [m['nodes'][n]['name'] for (n, p) in m['anims'][sc] if p == 'rotation']
    for (n, p), (tt, vv) in m['anims'][sc].items():
        if p != 'rotation': continue
        k = int(np.searchsorted(tt, st - 1e-6)); k = min(max(k, 0), len(tt) - 1)
        loc[m['nodes'][n]['name']] = np.array(vv[k], float)
js, b0 = L.load_glb(BODY); bn = bytearray(b0); nid = {nd.get('name'): i for i, nd in enumerate(js['nodes'])}
def put(data):
    while len(bn) % 4: bn.append(0)
    o = len(bn); bn.extend(data); return o
def acc(arr, typ, mm=False):
    arr = np.ascontiguousarray(arr, np.float32)
    js['bufferViews'].append(dict(buffer=0, byteOffset=put(arr.tobytes()), byteLength=arr.nbytes))
    ac = dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=int(arr.shape[0]), type=typ)
    if mm: ac['min'] = [float(v) for v in np.atleast_1d(arr.min(0))]; ac['max'] = [float(v) for v in np.atleast_1d(arr.max(0))]
    js['accessors'].append(ac); return len(js['accessors']) - 1
ti = acc(np.array([[0.0], [1.0 / 24]]), 'SCALAR', True)
samplers, channels, done = [], [], []
for bnm in bones:
    q = loc[bnm]; tgt = bnm
    if MIR:
        q = np.array([q[0], -q[1], -q[2], q[3]]); tgt = bnm.replace('Right', 'Left') if 'Right' in bnm else bnm.replace('Left', 'Right')
    samplers.append(dict(input=ti, output=acc(np.array([q, q]), 'VEC4'), interpolation='STEP'))
    channels.append(dict(sampler=len(samplers) - 1, target=dict(node=nid[tgt], path='rotation'))); done.append(tgt)
js['animations'] = [x for x in js['animations'] if x.get('name') != NAME] + [dict(name=NAME, samplers=samplers, channels=channels)]
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn))); f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
print(json.dumps(dict(name=NAME, source=src, mirror=MIR, bones=done)))
