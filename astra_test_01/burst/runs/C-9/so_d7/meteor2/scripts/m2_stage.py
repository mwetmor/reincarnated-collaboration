# Stage a library candidate ON her shipped body, for measurement only (never so_d7/export).
#   python3 meteor2/scripts/m2_stage.py <export so-body.glb> <candidate.glb> <new clip name> <out.glb>
# A binary append: the candidate's channels are re-targeted by bone NAME onto the body's nodes (her
# rig is the candidate's rig -- the clips were fetched for it -- so a straight copy is exact, s16),
# every other clip untouched, and weapon_r gets a one-key REST track in the new clip (Godot keeps a
# bone's last value when a clip has no track for it).
import json, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))
L = __import__('21_lint_export')
BODY, CAND, NAME, OUT = sys.argv[1:5]
js, b0 = L.load_glb(BODY); bn = bytearray(b0)
cj, cb = L.load_glb(CAND)
nid = {n.get('name'): i for i, n in enumerate(js['nodes'])}
can = cj['animations'][0]


def put(data):
    while len(bn) % 4: bn.append(0)
    off = len(bn); bn.extend(data); return off


def copy_acc(ai):
    acc = cj['accessors'][ai]; bv = cj['bufferViews'][acc['bufferView']]
    n = {5126: 4, 5125: 4, 5123: 2, 5121: 1}[acc['componentType']] * {'SCALAR': 1, 'VEC3': 3, 'VEC4': 4}[acc['type']]
    off = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
    stride = bv.get('byteStride', n)
    raw = b''.join(bytes(cb[off + k * stride: off + k * stride + n]) for k in range(acc['count']))
    js['bufferViews'].append(dict(buffer=0, byteOffset=put(raw), byteLength=len(raw)))
    na = {k: v for k, v in acc.items() if k not in ('bufferView', 'byteOffset')}
    na['bufferView'] = len(js['bufferViews']) - 1
    js['accessors'].append(na); return len(js['accessors']) - 1


samplers, channels, done = [], [], {}
for ch in can['channels']:
    nm = cj['nodes'][ch['target']['node']].get('name')
    if nm not in nid:
        continue
    s = can['samplers'][ch['sampler']]
    key = (s['input'], s['output'])
    if key not in done:
        ii = done.get(('in', s['input'])) or copy_acc(s['input']); done[('in', s['input'])] = ii
        oo = copy_acc(s['output'])
        samplers.append(dict(input=ii, output=oo, interpolation=s.get('interpolation', 'LINEAR'))); done[key] = len(samplers) - 1
    channels.append(dict(sampler=done[key], target=dict(node=nid[nm], path=ch['target']['path'])))
wr = nid['weapon_r']
t0 = js['accessors'][samplers[0]['input']]['min'][0]
ti = copy_acc_arr = None
tarr = np.array([[t0]], np.float32).tobytes(); js['bufferViews'].append(dict(buffer=0, byteOffset=put(tarr), byteLength=4))
js['accessors'].append(dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=1, type='SCALAR', min=[t0], max=[t0]))
qi = js['nodes'][wr].get('rotation', [0, 0, 0, 1])
qarr = np.array([qi], np.float32).tobytes(); js['bufferViews'].append(dict(buffer=0, byteOffset=put(qarr), byteLength=16))
js['accessors'].append(dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=1, type='VEC4'))
samplers.append(dict(input=len(js['accessors']) - 2, output=len(js['accessors']) - 1, interpolation='STEP'))
channels.append(dict(sampler=len(samplers) - 1, target=dict(node=wr, path='rotation')))
js['animations'].append(dict(name=NAME, samplers=samplers, channels=channels))
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn)))
    f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
print("staged %s as '%s': %d channels; lint %s" % (os.path.basename(CAND), NAME, len(channels), L.lint(OUT)['verdict']))
