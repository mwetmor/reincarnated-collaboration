# R-C9-105: SPLICE the champion body mesh into a COPY of his JOIN body (nb_join/export/nb-body_join.glb, bd66432e) as a
# BINARY glTF patch: the skeleton, skin, every clip and channel stay byte-identical (verified), only the skinned mesh changes.
#   python3 s32_swap_body.py <old_body.glb> <champion_body_piece.glb> <out.glb> [--json f]
# 1. the new primitive's attributes (POSITION, NORMAL, TEXCOORD_0, JOINTS_0, WEIGHTS_0, indices) and morph targets are
#    copied; JOINTS_0 is REMAPPED by joint NAME from the piece's skin order to the old skin's order;
# 2. if the two files' bind matrices differ (joint world x inverse bind), positions/normals/morph deltas are taken into
#    the old file's mesh space so the old skin binds them exactly;
# 3. the material, its textures, images and samplers are copied;
# 4. the buffer is COMPACTED to the bufferViews still referenced (the old mesh's data is dropped).
import json, os, struct, sys
import numpy as np
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export'); R_ = __import__('49_recentre')
a = sys.argv[1:]
OLD, NEW, OUT = a[0], a[1], a[2]
OUTJ = a[a.index('--json') + 1] if '--json' in a else OUT.replace('.glb', '_swap.json')
CT = {5120: ('b', 1), 5121: ('B', 1), 5122: ('h', 2), 5123: ('H', 2), 5125: ('I', 4), 5126: ('f', 4)}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}
NP = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}


def node_world(js):
    par = {}
    for i, n in enumerate(js['nodes']):
        for c in n.get('children', []):
            par[c] = i
    loc = [L._trs(n) for n in js['nodes']]; W = [None] * len(js['nodes'])

    def w(i):
        if W[i] is None:
            W[i] = loc[i] if i not in par else w(par[i]) @ loc[i]
        return W[i]
    return [w(i) for i in range(len(js['nodes']))]


def acc_array(js, bin_, idx):
    acc = js['accessors'][idx]
    n, nc = acc['count'], NC[acc['type']]; dt = NP[acc['componentType']]; sz = np.dtype(dt).itemsize
    if 'bufferView' not in acc:                     # glTF: an accessor without a bufferView is all zeros
        return np.zeros((n, nc), dt)
    bv = js['bufferViews'][acc['bufferView']]
    base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0); stride = bv.get('byteStride') or nc * sz
    raw = np.frombuffer(bin_, dtype=np.uint8, count=(n - 1) * stride + nc * sz, offset=base)
    out = np.lib.stride_tricks.as_strided(raw, shape=(n, nc * sz), strides=(stride, 1)).copy().view(dt).reshape(n, nc)
    return out


def bind(js, bin_, skin_i):
    sk = js['skins'][skin_i]
    ibm = acc_array(js, bin_, sk['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)
    Wn = node_world(js)
    return Wn[sk['joints'][0]] @ ibm[0], [js['nodes'][j].get('name') for j in sk['joints']]


jo, bo = L.load_glb(OLD); jn, bn_ = L.load_glb(NEW)
anim_before = json.dumps(jo['animations'], sort_keys=True)
anim_arrays_before = [acc_array(jo, bo, s_['output']).tobytes() for an in jo['animations'] for s_ in an['samplers']]
on = next(i for i, n in enumerate(jo['nodes']) if 'mesh' in n and 'skin' in n)
nn = next(i for i, n in enumerate(jn['nodes']) if 'mesh' in n and 'skin' in n)
Mo, onames = bind(jo, bo, jo['nodes'][on]['skin']); Mn, nnames = bind(jn, bn_, jn['nodes'][nn]['skin'])
C = np.linalg.inv(Mo) @ Mn                                   # new mesh space -> old mesh space
corr = float(np.abs(C - np.eye(4)).max())
remap = np.array([onames.index(n) for n in nnames])
print("bind correction max |C-I| %.3e; joints remapped %s" % (corr, (remap != np.arange(len(remap))).sum()))
# --- new buffers, appended into a fresh list of (bytes) to be compacted at the end
new_views = []                                                  # (bytes, target) to append


def add_acc(arr, ctype, typ, target=None, minmax=False):
    data = np.ascontiguousarray(arr.astype(NP[ctype])).tobytes()
    jo['bufferViews'].append({"buffer": 0, "byteLength": len(data), "_new": len(new_views)})
    if target:
        jo['bufferViews'][-1]["target"] = target
    new_views.append(data)
    acc = {"bufferView": len(jo['bufferViews']) - 1, "componentType": ctype, "count": int(arr.shape[0]), "type": typ}
    if minmax:
        acc["min"] = arr.min(0).astype(float).tolist(); acc["max"] = arr.max(0).astype(float).tolist()
    jo['accessors'].append(acc); return len(jo['accessors']) - 1


# materials / textures / images / samplers
tex_map, img_map, smp_map, mat_map = {}, {}, {}, {}
for i, s_ in enumerate(jn.get('samplers', [])):
    jo.setdefault('samplers', []).append(dict(s_)); smp_map[i] = len(jo['samplers']) - 1
for i, im in enumerate(jn.get('images', [])):
    im2 = {k: v for k, v in im.items() if k != 'bufferView'}
    if 'bufferView' in im:
        bv = jn['bufferViews'][im['bufferView']]
        data = bytes(bn_[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']])
        jo['bufferViews'].append({"buffer": 0, "byteLength": len(data), "_new": len(new_views)}); new_views.append(data)
        im2['bufferView'] = len(jo['bufferViews']) - 1
    jo.setdefault('images', []).append(im2); img_map[i] = len(jo['images']) - 1
for i, t in enumerate(jn.get('textures', [])):
    t2 = dict(t)
    if 'source' in t2: t2['source'] = img_map[t2['source']]
    if 'sampler' in t2: t2['sampler'] = smp_map[t2['sampler']]
    jo.setdefault('textures', []).append(t2); tex_map[i] = len(jo['textures']) - 1


def retex(o):
    if isinstance(o, dict):
        return {k: (tex_map[v] if k == 'index' and isinstance(v, int) else retex(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [retex(x) for x in o]
    return o


for i, m in enumerate(jn.get('materials', [])):
    jo.setdefault('materials', []).append(retex(m)); mat_map[i] = len(jo['materials']) - 1
newprims = []
for p in jn['meshes'][jn['nodes'][nn]['mesh']]['primitives']:
    at = p['attributes']; q = {"attributes": {}}
    POS = acc_array(jn, bn_, at['POSITION']).astype(np.float64)
    POS = (POS @ C[:3, :3].T + C[:3, 3]).astype(np.float32)
    q['attributes']['POSITION'] = add_acc(POS, 5126, 'VEC3', 34962, True)
    if 'NORMAL' in at:
        N = acc_array(jn, bn_, at['NORMAL']).astype(np.float64) @ np.linalg.inv(C[:3, :3])
        N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)
        q['attributes']['NORMAL'] = add_acc(N.astype(np.float32), 5126, 'VEC3', 34962)
    for k in [k for k in at if k.startswith('TEXCOORD')]:
        q['attributes'][k] = add_acc(acc_array(jn, bn_, at[k]), jn['accessors'][at[k]]['componentType'], 'VEC2', 34962)
    J = acc_array(jn, bn_, at['JOINTS_0']); ct = jn['accessors'][at['JOINTS_0']]['componentType']
    q['attributes']['JOINTS_0'] = add_acc(remap[J.astype(np.int64)], ct, 'VEC4', 34962)
    q['attributes']['WEIGHTS_0'] = add_acc(acc_array(jn, bn_, at['WEIGHTS_0']), jn['accessors'][at['WEIGHTS_0']]['componentType'], 'VEC4', 34962)
    if 'indices' in p:
        I = acc_array(jn, bn_, p['indices']); q['indices'] = add_acc(I, jn['accessors'][p['indices']]['componentType'], 'SCALAR', 34963)
    if 'material' in p:
        q['material'] = mat_map[p['material']]
    if 'mode' in p:
        q['mode'] = p['mode']
    if 'targets' in p:
        q['targets'] = []
        for t in p['targets']:
            t2 = {}
            if 'POSITION' in t:
                D = (acc_array(jn, bn_, t['POSITION']).astype(np.float64) @ C[:3, :3].T).astype(np.float32)
                t2['POSITION'] = add_acc(D, 5126, 'VEC3', None, True)
            q['targets'].append(t2)
    newprims.append(q)
mo = jo['meshes'][jo['nodes'][on]['mesh']]
mn = jn['meshes'][jn['nodes'][nn]['mesh']]
mo['primitives'] = newprims
mo['weights'] = list(mn.get('weights', [0.0] * len(newprims[0].get('targets', []))))
mo['extras'] = dict(mo.get('extras', {})); mo['extras']['targetNames'] = list(mn.get('extras', {}).get('targetNames', []))
# --- compaction: keep only referenced bufferViews, rebuild the binary
refs = set()
for acc in jo['accessors']:
    if 'bufferView' in acc: refs.add(acc['bufferView'])
for im in jo.get('images', []):
    if 'bufferView' in im: refs.add(im['bufferView'])
# drop accessors no one references? (keep all accessors: the old mesh's become dangling -> remove them too)
used_acc = set()


def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('POSITION', 'NORMAL', 'TANGENT', 'JOINTS_0', 'WEIGHTS_0', 'indices', 'input', 'output', 'inverseBindMatrices') \
                    and isinstance(v, int):
                used_acc.add(v)
            elif k.startswith('TEXCOORD') or k.startswith('COLOR') or k.startswith('JOINTS') or k.startswith('WEIGHTS'):
                if isinstance(v, int): used_acc.add(v)
            walk(v)
    elif isinstance(o, list):
        for x in o: walk(x)


walk(jo['meshes']); walk(jo['animations']); walk(jo['skins'])
amap = {}; accs = []
for i, acc in enumerate(jo['accessors']):
    if i in used_acc:
        amap[i] = len(accs); accs.append(acc)


def reacc(o):
    if isinstance(o, dict):
        return {k: (amap[v] if isinstance(v, int) and (k in ('POSITION', 'NORMAL', 'TANGENT', 'indices', 'input', 'output', 'inverseBindMatrices')
                                                        or k.startswith(('TEXCOORD', 'COLOR', 'JOINTS', 'WEIGHTS'))) else reacc(v))
                for k, v in o.items()}
    if isinstance(o, list):
        return [reacc(x) for x in o]
    return o


jo['meshes'] = reacc(jo['meshes']); jo['animations'] = reacc(jo['animations']); jo['skins'] = reacc(jo['skins'])
jo['accessors'] = accs
refs = sorted({acc['bufferView'] for acc in accs if 'bufferView' in acc} | {im['bufferView'] for im in jo.get('images', []) if 'bufferView' in im})
vmap = {}; out = bytearray(); views = []
for v in refs:
    bv = dict(jo['bufferViews'][v])
    data = new_views[bv.pop('_new')] if '_new' in bv else bytes(bo[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']])
    while len(out) % 4: out.append(0)
    bv['byteOffset'] = len(out); bv['byteLength'] = len(data); out += data
    vmap[v] = len(views); views.append(bv)
for acc in jo['accessors']:
    if 'bufferView' in acc: acc['bufferView'] = vmap[acc['bufferView']]
for im in jo.get('images', []):
    if 'bufferView' in im: im['bufferView'] = vmap[im['bufferView']]
jo['bufferViews'] = views; jo['buffers'] = [{"byteLength": len(out)}]
R_.write_glb(OUT, jo, bytes(out))
j2, b2 = L.load_glb(OUT)
same_json = json.dumps([{k: v for k, v in an.items() if k != 'samplers'} for an in j2['animations']], sort_keys=True) == \
            json.dumps([{k: v for k, v in an.items() if k != 'samplers'} for an in json.loads(anim_before)], sort_keys=True)
anim_arrays_after = [acc_array(j2, b2, s_['output']).tobytes() for an in j2['animations'] for s_ in an['samplers']]
rep = dict(old=OLD, new_mesh=NEW, bind_correction_max=corr, joints_remapped=int((remap != np.arange(len(remap))).sum()),
           target_names=mo['extras']['targetNames'], animations=len(j2['animations']),
           animation_channels_identical=same_json, animation_sample_data_identical=anim_arrays_after == anim_arrays_before,
           verts=int(acc_array(j2, b2, j2['meshes'][j2['nodes'][on]['mesh']]['primitives'][0]['attributes']['POSITION']).shape[0]),
           mb=round(os.path.getsize(OUT) / 1e6, 2))
json.dump(rep, open(OUTJ, 'w'), indent=1)
print(json.dumps(rep))
