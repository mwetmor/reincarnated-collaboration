# bm_mx DEFECT REPAIR (stage 3, 2026-10-02): a file whose morph-target accessors were broken by bm01's first compaction (sparse
# bufferViews dropped / not remapped) gets the mesh's morph targets RE-COPIED from the untouched source body: for each primitive (same
# mesh, asserted by vertex counts), every target accessor -- dense or sparse -- is appended with its own bufferViews, and the primitive's
# targets point at the copies. Nothing else changes. Verified by decoding every target from both files (sparse expanded) and comparing.
#   python3 bm13_fix_sparse.py <broken.glb> <source_body.glb> <out.glb>
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
BR, SRC, OUT = sys.argv[1:4]
jb, bb = L.load_glb(BR); bb = bytearray(bb); js, bs = L.load_glb(SRC)
def copy_bv(i):
    bv = js['bufferViews'][i]; o = bv.get('byteOffset', 0); off = W.append(bb, bs[o:o + bv['byteLength']])
    nb = dict(bv); nb['byteOffset'] = off; nb['buffer'] = 0; jb['bufferViews'].append(nb); return len(jb['bufferViews']) - 1
def copy_acc(i):
    a = json.loads(json.dumps(js['accessors'][i]))
    if 'bufferView' in a: a['bufferView'] = copy_bv(a['bufferView'])
    if 'sparse' in a:
        for k in ('indices', 'values'): a['sparse'][k]['bufferView'] = copy_bv(a['sparse'][k]['bufferView'])
    jb['accessors'].append(a); return len(jb['accessors']) - 1
def dec(j, b, i):
    a = j['accessors'][i]; n = a['count']; comp = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}[a['type']]
    out = L.read_accessor(j, b, i).astype(float) if 'bufferView' in a else np.zeros((n, comp))
    if 'sparse' in a:
        sp = a['sparse']; ib = j['bufferViews'][sp['indices']['bufferView']]; vb = j['bufferViews'][sp['values']['bufferView']]
        dt = {5121: np.uint8, 5123: np.uint16, 5125: np.uint32}[sp['indices']['componentType']]
        idx = np.frombuffer(b, dt, sp['count'], ib.get('byteOffset', 0) + sp['indices'].get('byteOffset', 0))
        val = np.frombuffer(b, np.float32, sp['count'] * comp, vb.get('byteOffset', 0) + sp['values'].get('byteOffset', 0)).reshape(-1, comp)
        out[idx] = val
    return out
n = 0
for mb, ms in zip(jb['meshes'], js['meshes']):
    for pb, ps in zip(mb['primitives'], ms['primitives']):
        assert jb['accessors'][pb['attributes']['POSITION']]['count'] == js['accessors'][ps['attributes']['POSITION']]['count']
        if 'targets' in ps:
            pb['targets'] = [{k: copy_acc(v) for k, v in t.items()} for t in ps['targets']]; n += len(ps['targets'])
jb['buffers'][0]['byteLength'] = len(bb) + (-len(bb) % 4); R_.write_glb(OUT, jb, bb)
j2, b2 = L.load_glb(OUT); worst = 0.0
for m2, ms in zip(j2['meshes'], js['meshes']):
    for p2, ps in zip(m2['primitives'], ms['primitives']):
        for t2, ts in zip(p2.get('targets', []), ps.get('targets', [])):
            for k in ts: worst = max(worst, float(np.abs(dec(j2, b2, t2[k]) - dec(js, bs, ts[k])).max()))
r = L.lint(OUT); print('re-copied %d targets -> %s; largest decoded difference vs the source %.3g; lint %s %s' % (n, os.path.basename(OUT), worst, r['verdict'], r['fails'][:2]))
