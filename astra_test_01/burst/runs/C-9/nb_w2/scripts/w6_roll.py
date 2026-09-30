# The JOIN body: the T12_5_guard body COPY with weapon_r carrying the SWORD's mount -- the same seat
# (the fist channel, from the T12_5 mount) and the sword's own roll about the blade.
#
#   python3 scripts/w6_roll.py <t12_5_guard/nb-body.glb> <out nb-body_sword.glb> --roll <deg> [--json f]
#
# A binary patch (the 52_weapon_bones way: nothing re-exported through Blender, so nothing unnamed
# changes): weapon_r's rest rotation, EVERY weapon_r rotation key (the per-clip channel tracks are
# absolute local rotations, fitted on the axe's mount), and weapon_r's inverse bind matrix are each
# post-multiplied by the same turn about weapon_r's own +Y. Positions and every other joint are
# untouched, which is checked.
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "so_d7", "scripts"))
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')
a = sys.argv[1:]
SRC, DST = a[0], a[1]
ROLL = float(a[a.index('--roll') + 1])
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
if ROLL == 0.0:
    # ROLL 0 IS THE T12_5 MOUNT ITSELF (2026-09-30: the -39 fit was an instrument error, see w5_measure.py's
    # header): the body is issued BYTE-IDENTICAL to its source -- no re-normalised keys, no recomputed IBM.
    import hashlib, shutil
    shutil.copyfile(SRC, DST)
    rep = dict(roll_deg=0.0, identity=True, sha256=hashlib.sha256(open(DST, 'rb').read()).hexdigest(),
               source=os.path.basename(os.path.dirname(os.path.abspath(SRC))) + "/" + os.path.basename(SRC),
               note="roll 0 = the T12_5 mount: a byte copy of the source body")
    print(json.dumps(rep))
    if OUTJ:
        json.dump(rep, open(OUTJ, 'w'), indent=1)
    sys.exit(0)
js, b0 = L.load_glb(SRC)
bn = bytearray(b0)
nodes = js['nodes']
wr = next(i for i, n in enumerate(nodes) if n.get('name') == 'weapon_r')
qr = np.array([0.0, math.sin(math.radians(ROLL) / 2), 0.0, math.cos(math.radians(ROLL) / 2)])


def qmul(q1, q2):
    x1, y1, z1, w1 = q1; x2, y2, z2, w2 = q2
    return np.array([w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                     w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2, w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2])


q0 = np.array(nodes[wr].get('rotation', [0, 0, 0, 1]), float)
nodes[wr]['rotation'] = [float(v) for v in qmul(q0, qr) / np.linalg.norm(qmul(q0, qr))]
tracks = 0; keys = 0
done = set()
for an in js.get('animations', []):
    for ch in an['channels']:
        if ch['target'].get('node') != wr or ch['target']['path'] != 'rotation':
            continue
        acc_i = an['samplers'][ch['sampler']]['output']
        if acc_i in done:
            continue
        acc = js['accessors'][acc_i]; bv = js['bufferViews'][acc['bufferView']]
        off = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
        assert acc['componentType'] == 5126 and acc['type'] == 'VEC4' and bv.get('byteStride', 16) == 16
        arr = np.frombuffer(bytes(bn[off:off + 16 * acc['count']]), np.float32).reshape(-1, 4).astype(float)
        new = np.array([qmul(q, qr) for q in arr]); new /= np.linalg.norm(new, axis=1, keepdims=True)
        bn[off:off + 16 * acc['count']] = new.astype(np.float32).tobytes()
        done.add(acc_i); tracks += 1; keys += acc['count']
# the IBM: inverse of the new global rest, for every skin that lists weapon_r
parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
def local(i):
    n = nodes[i]; M = np.eye(4)
    M[:3, :3] = W.q2m(n.get('rotation', [0, 0, 0, 1])) * np.array(n.get('scale', [1, 1, 1]))
    M[:3, 3] = n.get('translation', [0, 0, 0]); return M
def glob(i):
    M = local(i)
    while i in parent:
        i = parent[i]; M = local(i) @ M
    return M
GWn = glob(wr)
ibms = 0
for sk in js['skins']:
    if wr not in sk['joints']:
        continue
    acc = js['accessors'][sk['inverseBindMatrices']]; bv = js['bufferViews'][acc['bufferView']]
    off = bv.get('byteOffset', 0) + acc.get('byteOffset', 0) + 64 * sk['joints'].index(wr)
    bn[off:off + 64] = np.linalg.inv(GWn).T.astype(np.float32).tobytes()
    ibms += 1
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(DST, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn)))
    f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
Lr = L.lint(DST)
rep = dict(roll_deg=ROLL, weapon_r_rest_before=[float(v) for v in q0], weapon_r_rest_after=nodes[wr]['rotation'],
           rotation_tracks_rolled=tracks, keys_rolled=keys, ibms_rewritten=ibms, lint=dict(verdict=Lr['verdict'], fails=Lr['fails']))
print(json.dumps(rep))
if OUTJ:
    json.dump(rep, open(OUTJ, 'w'), indent=1)
