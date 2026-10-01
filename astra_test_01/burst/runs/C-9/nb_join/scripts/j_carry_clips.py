# CARRY CLIPS from one body GLB into another of the SAME rig (v4 rebase, the conductor 2026-09-30: "rebase your moves onto
# body 9346f3de", the JOIN hold v2 -- only its six guard clips differ from v1's). Every byte of the destination is kept;
# the named clips are APPENDED (replacing a clip of the same name), their keys copied value for value.
#
#   python3 scripts/j_carry_clips.py <src.glb> <dst.glb> <out.glb> <clip[=newname],clip,...>
#   (=newname: the clip is written under that name -- e.g. the JOIN hold v3's guards beside the body's own v2 ones)
#
# REFUSES unless the two files have the same nodes, by name AND index, with the same rest TRS and children: a channel
# targets a node by INDEX, so a clip carried onto a different layout would silently drive the wrong bones.
import json, struct, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); L = __import__('21_lint_export')
SRC, DST, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
CL = [(c.split('=') + [c])[:2] for c in sys.argv[4].split(',')]
sj, sb = L.load_glb(SRC); dj, db = L.load_glb(DST)
K = ('name', 'translation', 'rotation', 'scale', 'children')
if [{k: n.get(k) for k in K} for n in sj['nodes']] != [{k: n.get(k) for k in K} for n in dj['nodes']]:
    sys.exit("REFUSED: the node layouts differ (names, rest TRS or children)")
bn = bytearray(db)
def put(data):
    while len(bn) % 4: bn.append(0)
    o = len(bn); bn.extend(data); return o
def acc(arr, typ, mm=False):
    arr = np.ascontiguousarray(arr, np.float32)
    dj['bufferViews'].append(dict(buffer=0, byteOffset=put(arr.tobytes()), byteLength=arr.nbytes))
    a = dict(bufferView=len(dj['bufferViews']) - 1, componentType=5126, count=int(arr.shape[0]), type=typ)
    if mm: a['min'] = [float(v) for v in np.atleast_1d(arr.min(0))]; a['max'] = [float(v) for v in np.atleast_1d(arr.max(0))]
    dj['accessors'].append(a); return len(dj['accessors']) - 1
TYP = {1: 'SCALAR', 3: 'VEC3', 4: 'VEC4'}
done = []
for name, newname in CL:
    an = next((x for x in sj['animations'] if x.get('name') == name), None)
    if an is None: sys.exit("REFUSED: %s has no clip %s" % (SRC, name))
    samplers = []; cache = {}
    for s in an['samplers']:
        if s['input'] not in cache:
            t = L.read_accessor(sj, sb, s['input']).astype(np.float32).reshape(-1, 1); cache[s['input']] = acc(t, 'SCALAR', True)
        o = L.read_accessor(sj, sb, s['output']).astype(np.float32); o = o.reshape(len(o), -1)
        samplers.append(dict(input=cache[s['input']], output=acc(o, TYP[o.shape[1]]), interpolation=s.get('interpolation', 'LINEAR')))
    dj['animations'] = [x for x in dj['animations'] if x.get('name') != newname] + [dict(name=newname, samplers=samplers, channels=[dict(c) for c in an['channels']])]
    done.append((name if name == newname else '%s=%s' % (name, newname), len(an['channels'])))
while len(bn) % 4: bn.append(0)
dj['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(dj, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn))); f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
print("carried %s -> %s" % (done, OUT))
