# R-C9-140 (Matt): "when she wears the hood, the hair should be invisible." A GEAR-STATE MORPH, hood_hair, on her body
# (char1 is one shell: the hair cannot be switched off as a mesh). At 1.0 every hair vertex (r140_02's mask: the crown,
# the face-framing strands, the braid) is pulled INSIDE her, onto the segment between its dominant bone and that bone's
# child (the skull's centre for the head's hair, the neck/spine axis for the braid), so the hair's triangles degenerate
# inside the body and the hood. knight.gd's morph_rules drive it like grip_R: {"hood_hair": "hood"} -- 1 while the hood
# is worn, 0 when it is off (gear cycling shows the hair again). Appended as a SPARSE target (POSITION + zero NORMAL),
# the existing targets, clips and skin untouched.
#   python3 r140_03_hood_morph.py <in.glb> <out.glb> <mask.npy> [--name hood_hair]
import sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
IN, OUT, MASK = sys.argv[1], sys.argv[2], sys.argv[3]
NAME = sys.argv[sys.argv.index('--name') + 1] if '--name' in sys.argv else 'hood_hair'
CHILD = {"Head": "head_end", "neck": "Head", "Spine": "neck", "Spine01": "Spine", "Spine02": "Spine01", "Hips": "Spine02",
         "LeftShoulder": "neck", "RightShoulder": "neck"}
js, b = L.load_glb(IN); b = bytearray(b)
G, _ = W.globals_(js)
mi = next(i for i, n in enumerate(js['nodes']) if 'mesh' in n and 'skin' in n)
mesh = js['meshes'][js['nodes'][mi]['mesh']]; pr = mesh['primitives'][0]
names = mesh.get('extras', {}).get('targetNames', [])
assert NAME not in names, '%s already present' % NAME
sk = js['skins'][js['nodes'][mi]['skin']]; jn = [js['nodes'][j]['name'] for j in sk['joints']]
ibm = W.mat_list(js, bytes(b), sk['inverseBindMatrices'])
V = L.read_accessor(js, bytes(b), pr['attributes']['POSITION'])
J = L.read_accessor(js, bytes(b), pr['attributes']['JOINTS_0']).astype(int)
Wt = L.read_accessor(js, bytes(b), pr['attributes']['WEIGHTS_0'])
mask = np.load(MASK); assert len(mask) == len(V), (len(mask), len(V))
nid = {n.get('name'): i for i, n in enumerate(js['nodes'])}
idx = np.nonzero(mask)[0]
D = np.zeros((len(idx), 3)); per_bone = {}
for k, v in enumerate(idx):
    Mv = sum(Wt[v, c] * (G[sk['joints'][J[v, c]]] @ ibm[J[v, c]]) for c in range(4))
    pw = (Mv @ np.append(V[v], 1))[:3]
    dom = jn[J[v, int(np.argmax(Wt[v]))]]
    a = G[nid[dom]][:3, 3]; c_ = G[nid[CHILD.get(dom, dom)]][:3, 3]
    tgt = a + 0.5 * (c_ - a)                          # the middle of the bone: inside the skull / neck / chest
    D[k] = np.linalg.solve(Mv[:3, :3], tgt - pw)       # back into the mesh's own (bind) space
    per_bone[dom] = per_bone.get(dom, 0) + 1


def add_sparse(vals):
    ii = idx.astype(np.uint32).tobytes(); vv = np.asarray(vals, np.float32).tobytes()
    oi = W.append(b, ii); js['bufferViews'].append({"buffer": 0, "byteOffset": oi, "byteLength": len(ii)})
    bi = len(js['bufferViews']) - 1
    ov = W.append(b, vv); js['bufferViews'].append({"buffer": 0, "byteOffset": ov, "byteLength": len(vv)})
    bv = len(js['bufferViews']) - 1
    full = np.zeros((len(V), 3), np.float32); full[idx] = vals
    js['accessors'].append({"componentType": 5126, "count": int(len(V)), "type": "VEC3",
                            "min": full.min(0).tolist(), "max": full.max(0).tolist(),
                            "sparse": {"count": int(len(idx)), "indices": {"bufferView": bi, "componentType": 5125},
                                       "values": {"bufferView": bv}}})
    return len(js['accessors']) - 1


for p in mesh['primitives']:
    p.setdefault('targets', []).append({"POSITION": add_sparse(D), "NORMAL": add_sparse(np.zeros_like(D))})
mesh.setdefault('extras', {})['targetNames'] = names + [NAME]
if 'weights' in mesh: mesh['weights'] = list(mesh['weights']) + [0.0]
js['buffers'][0]['byteLength'] = len(b)
R_.write_glb(OUT, js, b)
print('%s: %d hair vertices -> inside, by bone %s; |delta| (bind units) max %.2f' % (NAME, len(idx), per_bone, float(np.linalg.norm(D, axis=1).max())))
print('targets now', mesh['extras']['targetNames'])
