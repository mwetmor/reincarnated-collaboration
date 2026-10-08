# R-C9-233 step 1: a LINING for the hood. The hood (and R-C9-152's crown cap) is an open, single-sided shell, and the
# Barrow's character shader culls back faces -- so seen through the face opening, the hood's own inside does not exist and
# whatever is behind it (her hair, the dark interior) reads as the opening. A lining is the shell's faces again, turned
# inward (winding reversed, normals negated), set LINING_M inside the shell, skinned with the shell's own joints and
# weights, and given ONE light fabric colour from the hood's own atlas (the texel whose colour is nearest --target RGB,
# among the colours the hood's vertices already wear). It adds a primitive per source primitive; the shell is untouched.
#   python3 r233_05_lining.py <hood.glb> <out.glb> [--target 190,112,92] [--inset 0.0025] [--report out.json]
import sys, os, io, json, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
IN, OUT = sys.argv[1], sys.argv[2]
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
TARGET = np.array([float(x) for x in arg('--target', '190,112,92').split(',')])
INSET = float(arg('--inset', 0.0025))
js, b = L.load_glb(IN); b = bytearray(b)
bv = js['bufferViews'][js['images'][0]['bufferView']]
T = np.asarray(Image.open(io.BytesIO(bytes(b[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']]))).convert('RGB')).astype(float)
H, Wd = T.shape[:2]
mesh = js['meshes'][0]
src = list(mesh['primitives'])


def acc(arr, ctype, typ, minmax=False):
    a = np.ascontiguousarray(arr)
    raw = a.tobytes(); o = W.append(b, raw)
    js['bufferViews'].append({"buffer": 0, "byteOffset": o, "byteLength": len(raw)})
    d = {"bufferView": len(js['bufferViews']) - 1, "componentType": ctype, "count": int(a.shape[0]), "type": typ}
    if minmax:
        d["min"] = a.min(0).tolist(); d["max"] = a.max(0).tolist()
    js['accessors'].append(d)
    return len(js['accessors']) - 1


# the lining's colour: the vertex-worn hood colour nearest the target
best = None
for pr in src:
    UV = L.read_accessor(js, bytes(b), pr['attributes']['TEXCOORD_0'])
    c = T[np.clip((UV[:, 1] % 1 * H).astype(int), 0, H - 1), np.clip((UV[:, 0] % 1 * Wd).astype(int), 0, Wd - 1)]
    d = np.linalg.norm(c - TARGET, axis=1); i = int(np.argmin(d))
    if best is None or d[i] < best[0]:
        best = (float(d[i]), UV[i].astype(np.float32), c[i])
uv0 = best[1]
rep = {"in": IN, "out": OUT, "inset_m": INSET, "target_rgb": TARGET.tolist(), "lining_rgb": best[2].tolist(), "lining_uv": uv0.tolist(), "prims": []}
for pr in src:
    at = pr['attributes']
    P = L.read_accessor(js, bytes(b), at['POSITION']).astype(np.float32)
    N = L.read_accessor(js, bytes(b), at['NORMAL']).astype(np.float32)
    Jc = js['accessors'][at['JOINTS_0']]['componentType']
    Jt = L.read_accessor(js, bytes(b), at['JOINTS_0']).astype({5121: np.uint8, 5123: np.uint16}[Jc])
    Wt = L.read_accessor(js, bytes(b), at['WEIGHTS_0']).astype(np.float32)
    I = L.read_accessor(js, bytes(b), pr['indices']).astype(np.uint32).reshape(-1, 3)
    Nn = N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)
    P2 = (P - INSET * Nn).astype(np.float32); N2 = (-Nn).astype(np.float32)
    I2 = I[:, [0, 2, 1]].reshape(-1).astype(np.uint32)
    UV2 = np.tile(uv0, (len(P), 1)).astype(np.float32)
    new = {"attributes": {"POSITION": acc(P2, 5126, "VEC3", True), "NORMAL": acc(N2, 5126, "VEC3"),
                          "TEXCOORD_0": acc(UV2, 5126, "VEC2"), "JOINTS_0": acc(Jt, Jc, "VEC4"), "WEIGHTS_0": acc(Wt, 5126, "VEC4")},
           "indices": acc(I2, 5125, "SCALAR"), "material": pr.get('material', 0), "mode": 4}
    mesh['primitives'].append(new)
    rep["prims"].append({"verts": int(len(P)), "tris": int(len(I))})
js['buffers'][0]['byteLength'] = len(b)
R_.write_glb(OUT, js, b)
print(json.dumps(rep))
if '--report' in sys.argv:
    json.dump(rep, open(arg('--report', ''), 'w'), indent=1)
