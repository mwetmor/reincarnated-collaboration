# The pairing's FIRST LOOK only: his bearded axe in the LEFT hand, on weapon_l, for one still.
# NOT an off-hand hold (that is designed after the scene drax's strikes land): the axe's shipped
# right-hand placement, mirrored across his sagittal plane, bound 100% to weapon_l.
#
#   python3 scripts/w7_axe_left.py <t12_5_guard/axe.glb> <body.glb> <out axe_l.glb> [--json f]
#
# In-place binary patch of a copy: positions and normals mirrored (glTF x -> -x, his right is -X),
# triangle winding reversed (a mirror turns faces inside out), JOINTS_0 moved to weapon_l. The
# mirror is exact only if his REST is symmetric, which is measured and reported (hands and
# shoulders, left against mirrored right).
import json, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "so_d7", "scripts"))
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')
a = sys.argv[1:]
SRC, BODY, DST = a[0], a[1], a[2]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
js, b0 = L.load_glb(SRC)
bn = bytearray(b0)
nodes = js['nodes']
pr = js['meshes'][0]['primitives'][0]


def span(acc_i):
    acc = js['accessors'][acc_i]; bv = js['bufferViews'][acc['bufferView']]
    off = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
    return acc, bv, off


for key in ('POSITION', 'NORMAL'):
    acc, bv, off = span(pr['attributes'][key])
    assert bv.get('byteStride', 12) == 12
    v = np.frombuffer(bytes(bn[off:off + 12 * acc['count']]), np.float32).reshape(-1, 3).copy()
    v[:, 0] *= -1
    bn[off:off + 12 * acc['count']] = v.tobytes()
    if key == 'POSITION':
        acc['min'] = [float(x) for x in v.min(0)]; acc['max'] = [float(x) for x in v.max(0)]
acc, bv, off = span(pr['indices'])
dt = {5121: np.uint8, 5123: np.uint16, 5125: np.uint32}[acc['componentType']]
ix = np.frombuffer(bytes(bn[off:off + np.dtype(dt).itemsize * acc['count']]), dt).reshape(-1, 3)[:, ::-1].copy()
bn[off:off + ix.nbytes] = ix.tobytes()
sk = js['skins'][0]
names = [nodes[j].get('name') for j in sk['joints']]
jr, jl = names.index('weapon_r'), names.index('weapon_l')
acc, bv, off = span(pr['attributes']['JOINTS_0'])
J = np.frombuffer(bytes(bn[off:off + 4 * acc['count']]), np.uint8).reshape(-1, 4).copy()
moved = int((J[:, 0] == jr).sum()); J[J == jr] = jl
bn[off:off + J.nbytes] = J.tobytes()
for n in nodes:
    if n.get('name') == 'axe':
        n['name'] = 'axe_l'
    if n.get('name') == 'axe_edge':
        n['name'] = 'axe_edge_R_unused'            # the right-hand marker; the left hold has none yet
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(DST, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn)))
    f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
# symmetry of the REST, from the body
bj, bb = L.load_glb(BODY)
bn_ = bj['nodes']; par = {c: i for i, nd in enumerate(bn_) for c in nd.get('children', [])}
def local(i):
    n = bn_[i]; M = np.eye(4)
    M[:3, :3] = W.q2m(n.get('rotation', [0, 0, 0, 1])) * np.array(n.get('scale', [1, 1, 1]))
    M[:3, 3] = n.get('translation', [0, 0, 0]); return M
def glob(i):
    M = local(i)
    while i in par:
        i = par[i]; M = local(i) @ M
    return M
nid = {n.get('name'): i for i, n in enumerate(bn_)}
asym = {s: round(float(np.linalg.norm(glob(nid['Left' + s])[:3, 3] - glob(nid['Right' + s])[:3, 3] * np.array([-1, 1, 1]))), 4)
        for s in ('Shoulder', 'Arm', 'ForeArm', 'Hand')}
Lr = L.lint(DST)
rep = dict(verts_moved_to_weapon_l=moved, rest_asymmetry_m=asym, lint=dict(verdict=Lr['verdict'], fails=Lr['fails']))
print(json.dumps(rep))
if OUTJ:
    json.dump(rep, open(OUTJ, 'w'), indent=1)
