# bm_mx (R-C9-127): ROLL the maul about its HAFT -- the great maul's head has two striking faces along one axis (it is not a
# round mace), and e10 lays the head's roll arbitrarily. Every vertex of the piece is skinned 1.0 to weapon_r, whose rest frame
# is the grip (origin on the haft axis at the right fist, +Y along the haft -- bm_e12_weapon.py), so the roll is a rotation
# about weapon_r's local +Y:   v' = IBM^-1 . Ry(deg) . IBM . v   (normals by the linear part, renormalised). Binary patch:
# new POSITION/NORMAL accessors, everything else byte-identical. The angle comes from bm03_maul_measure.py's SWING roll_deg.
#   python3 bm05_roll.py <in_piece.glb> <out_piece.glb> <deg>
import sys, os, math, json, struct, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
IN, OUT, DEG = sys.argv[1], sys.argv[2], float(sys.argv[3])
js, b = L.load_glb(IN); b = bytearray(b)
sk = js['skins'][0]; names = [js['nodes'][j]['name'] for j in sk['joints']]; ibm = W.mat_list(js, bytes(b), sk['inverseBindMatrices'])
M = ibm[names.index('weapon_r')]; Mi = np.linalg.inv(M)
c, s = math.cos(math.radians(DEG)), math.sin(math.radians(DEG))
Ry = np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1.0]])
T = Mi @ Ry @ M; A = T[:3, :3]
def add(arr, typ, mm=False):
    arr = np.ascontiguousarray(arr, np.float32); off = W.append(b, arr.tobytes())
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes})
    a = {"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(arr.shape[0]), "type": typ}
    if mm: a["min"] = arr.min(0).tolist(); a["max"] = arr.max(0).tolist()
    js['accessors'].append(a); return len(js['accessors']) - 1
n = 0
for mn in [i for i, nd in enumerate(js['nodes']) if 'skin' in nd and 'mesh' in nd]:
    for pr in js['meshes'][js['nodes'][mn]['mesh']]['primitives']:
        J = L.read_accessor(js, b, pr['attributes']['JOINTS_0']).astype(int); Wt = L.read_accessor(js, b, pr['attributes']['WEIGHTS_0'])
        assert np.all((J[:, 0] == names.index('weapon_r')) & (Wt[:, 0] > 0.999)), "every vertex must ride weapon_r alone"
        V = L.read_accessor(js, b, pr['attributes']['POSITION']).astype(float)
        V2 = (np.c_[V, np.ones(len(V))] @ T.T)[:, :3]; pr['attributes']['POSITION'] = add(V2, "VEC3", True); n += len(V)
        if 'NORMAL' in pr['attributes']:
            N = L.read_accessor(js, b, pr['attributes']['NORMAL']).astype(float) @ np.linalg.inv(A).T
            pr['attributes']['NORMAL'] = add(N / np.linalg.norm(N, axis=1, keepdims=True), "VEC3")
        if 'TANGENT' in pr['attributes']:
            Tg = L.read_accessor(js, b, pr['attributes']['TANGENT']).astype(float); t3 = Tg[:, :3] @ A.T
            pr['attributes']['TANGENT'] = add(np.c_[t3 / np.linalg.norm(t3, axis=1, keepdims=True), Tg[:, 3]], "VEC4")
js['buffers'][0]['byteLength'] = len(b) + (-len(b) % 4); R_.write_glb(OUT, js, b)
r = L.lint(OUT); print('rolled %d verts by %.1f deg about weapon_r +Y -> %s | lint %s %s' % (n, DEG, os.path.basename(OUT), r['verdict'], r['fails'][:2]))
