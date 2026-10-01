# E1 two-handed HOLD (a carry layer, baked): the idle's and run's ARM CHAIN rotations replaced by the armed walk's held
# pose (Meshy 21 "Walk Fight Forward": hands 0.19-0.21 m apart all cycle, at the waist -- the only library clip in the
# set whose hands stay together, i.e. the one that can hold a two-handed haft). A binary glTF patch: a new constant output
# accessor per arm rotation channel on the clip's own input keys (no resample, the loop seam untouched).
#   python3 e09_hold.py <in.glb> <out.glb> --from walk[@t] --clips idle,run [--json f]
import json, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export')
ARMS = ("LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand", "RightShoulder", "RightArm", "RightForeArm", "RightHand")
a = sys.argv[1:]; SRC, DST = a[0], a[1]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
fr = opt('--from', 'walk'); fname, ft = (fr.split('@') + [None])[:2]
CLIPS = opt('--clips', 'idle,run').split(',')
js, b0 = L.load_glb(SRC); bn = bytearray(b0); nodes = js['nodes']
name = {i: n.get('name') for i, n in enumerate(nodes)}
def chans(an):
    out = {}
    for ch in an['channels']:
        s = an['samplers'][ch['sampler']]
        out[(name[ch['target']['node']], ch['target']['path'])] = (ch, s)
    return out
fa = next(x for x in js['animations'] if x['name'] == fname); fc = chans(fa)
# the held pose: the key nearest t (default: the cycle's middle key)
hold = {}
for j in ARMS:
    ch, s = fc[(j, 'rotation')]
    t = L.read_accessor(js, bn, s['input']).reshape(-1); v = L.read_accessor(js, bn, s['output'])
    k = len(t) // 2 if ft is None else int(np.argmin(np.abs(t - float(ft))))
    hold[j] = v[k].astype(np.float32); hold['_t'] = float(t[k])
rep = dict(source=fname, key_t=hold.pop('_t'), clips={})
for cn in CLIPS:
    an = next(x for x in js['animations'] if x['name'] == cn); cc = chans(an); n_ch = 0
    for j in ARMS:
        if (j, 'rotation') not in cc: continue
        ch, s = cc[(j, 'rotation')]
        nkeys = js['accessors'][s['input']]['count']
        data = np.tile(hold[j], (nkeys, 1)).astype('<f4').tobytes()
        while len(bn) % 4: bn.append(0)
        off = len(bn); bn += data
        js['bufferViews'].append(dict(buffer=0, byteOffset=off, byteLength=len(data)))
        js['accessors'].append(dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=nkeys, type='VEC4'))
        s['output'] = len(js['accessors']) - 1; n_ch += 1
    rep['clips'][cn] = dict(arm_channels_replaced=n_ch)
js['buffers'][0]['byteLength'] = len(bn)
L.save_glb(js, bytes(bn), DST) if hasattr(L, 'save_glb') else None
if not hasattr(L, 'save_glb'):
    jb = json.dumps(js, separators=(',', ':')).encode()
    while len(jb) % 4: jb += b' '
    while len(bn) % 4: bn.append(0)
    with open(DST, 'wb') as f:
        f.write(struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(bn)))
        f.write(struct.pack('<II', len(jb), 0x4E4F534A)); f.write(jb)
        f.write(struct.pack('<II', len(bn), 0x004E4942)); f.write(bytes(bn))
print(rep)
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
