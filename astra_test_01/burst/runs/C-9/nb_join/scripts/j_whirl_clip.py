# WHIRLWIND, THE CLIP: one constant local pose (j_whirl_pose.py) turned by a UNIFORM SINGLE-REVOLUTION YAW about
# the vertical through his hips -- the weapon research's method. Closure is exact by construction: the last key is
# the first turned by 360 deg, which is the same orientation.
#
#   python3 scripts/j_whirl_clip.py <body.glb> <pose.json> <out.glb> [--name whirlwind] [--T 0.6667] [--keys 16] [--json f]
#
# The Hips rotation carries the turn, 1 key per 360/keys deg (22.5 at 16: one octant = 2 frames, the contract's
# pin), so glTF's slerp between keys IS the uniform turn. Every other joint the pose names is keyed CONSTANT (two
# keys, 0 and T), so the clip owns its whole pose and nothing leaks in from rest or another clip. The Hips
# translation is constant, straight over the ground origin: the spin stays in place and the root is stripped.
# Weapon bones get NO track -- the weapons ride their mounts, as in every Meshy clip on this body (the scene drax's
# rule, and the glTF rule for an un-keyed channel). The sense is the pose's: counter-clockwise seen from above,
# a positive turn about +Y (he turns to his LEFT) -- revolution_deg < 0 in the port's bearing (Matt 2026-09-21).
# A binary patch: the animation is APPENDED; every other byte of the body is kept (checked).
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts"))
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')
a = sys.argv[1:]
BODY, POSE, OUT = a[0], a[1], a[2]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
NAME = opt('--name', 'whirlwind'); T = float(opt('--T', str(16 / 24.0))); K = int(opt('--keys', '16'))
OUTJ = opt('--json')
js, b0 = L.load_glb(BODY); bn = bytearray(b0)
pose = json.load(open(POSE))
sense = pose.get('sense', 'ccw')
nodes = js['nodes']; nid = {n.get('name'): i for i, n in enumerate(nodes)}
parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
skin_joints = set(js['skins'][0]['joints'])
hips = nid['Hips']


def glob(i):
    n = nodes[i]; M = np.eye(4); M[:3, :3] = W.q2m(n.get('rotation', [0, 0, 0, 1])) * np.array(n.get('scale', [1, 1, 1])); M[:3, 3] = n.get('translation', [0, 0, 0])
    return M if parent.get(i) is None else glob(parent[i]) @ M


Gp = glob(parent[hips]); Rp = Gp[:3, :3] / np.linalg.norm(Gp[:3, :3], axis=0)
lh = pose['locals']['Hips']
Rh_local = W.q2m(lh['r']); Rh_world = Rp @ Rh_local


def put(data):
    while len(bn) % 4: bn.append(0)
    off = len(bn); bn.extend(data); return off


def acc(arr, typ, mm=False):
    arr = np.ascontiguousarray(arr, np.float32)
    js['bufferViews'].append(dict(buffer=0, byteOffset=put(arr.tobytes()), byteLength=arr.nbytes))
    ac = dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=int(arr.shape[0]), type=typ)
    if mm:
        ac['min'] = [float(v) for v in np.atleast_1d(arr.min(0))]; ac['max'] = [float(v) for v in np.atleast_1d(arr.max(0))]
    js['accessors'].append(ac); return len(js['accessors']) - 1


sgn = 1.0 if sense == 'ccw' else -1.0
tk = np.array([T * i / K for i in range(K + 1)]).reshape(-1, 1)
t2 = np.array([[0.0], [T]])
ti_k, ti_2 = acc(tk, 'SCALAR', True), acc(t2, 'SCALAR', True)
samplers, channels = [], []
qs = []
for i in range(K + 1):
    th = sgn * 2 * math.pi * i / K
    Ry = W.axis_angle(np.array([0.0, 1.0, 0.0]), th)
    qs.append(np.array(W.m2q(Rp.T @ Ry @ Rh_world), float))
for i in range(1, len(qs)):                                                    # continuous for slerp: 22.5 deg per interval
    if np.dot(qs[i], qs[i - 1]) < 0: qs[i] = -qs[i]
samplers.append(dict(input=ti_k, output=acc(np.array(qs), 'VEC4'), interpolation='LINEAR'))
channels.append(dict(sampler=0, target=dict(node=hips, path='rotation')))
samplers.append(dict(input=ti_2, output=acc(np.array([lh['t'], lh['t']]), 'VEC3'), interpolation='LINEAR'))
channels.append(dict(sampler=1, target=dict(node=hips, path='translation')))
keyed = ['Hips']
for nm, lc in pose['locals'].items():
    i = nid.get(nm)
    if i is None or i == hips or i not in skin_joints or nm in ('weapon_r', 'weapon_l'):
        continue
    samplers.append(dict(input=ti_2, output=acc(np.array([lc['r'], lc['r']]), 'VEC4'), interpolation='LINEAR'))
    channels.append(dict(sampler=len(samplers) - 1, target=dict(node=i, path='rotation')))
    keyed.append(nm)
js['animations'] = [an for an in js['animations'] if an.get('name') != NAME]
js['animations'].append(dict(name=NAME, samplers=samplers, channels=channels))
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn)))
    f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
# every accessor that existed before is byte-identical after
nj, nb = L.load_glb(OUT)
def ab(jj, bb, i):
    ac = jj['accessors'][i]
    if 'bufferView' not in ac: return None
    bv = jj['bufferViews'][ac['bufferView']]; o = bv.get('byteOffset', 0); return bytes(bb[o:o + bv['byteLength']])
same = all(ab(nj, nb, i) == ab(js, b0, i) for i in range(len(L.load_glb(BODY)[0]['accessors'])))
rep = dict(name=NAME, T=T, keys=K + 1, deg_per_key=360.0 / K, sense=sense, keyed_joints=len(keyed), weapons="un-keyed (their mounts)",
           prior_accessors_byte_identical=bool(same), pose=os.path.basename(POSE))
print(json.dumps(rep))
if OUTJ:
    json.dump(rep, open(OUTJ, 'w'), indent=1)
