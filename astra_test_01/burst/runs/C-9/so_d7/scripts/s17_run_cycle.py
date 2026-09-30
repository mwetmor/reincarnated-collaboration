# THE RUN'S LOOP SEAM, fixed at its source (JOIN-1 pack review, conductor 2026-09-30).
#
#   python3 scripts/s17_run_cycle.py <export so-body.glb> <source run.glb> <out so-body.glb> [--json f]
#
# The seam: rendered at the port's camera, run(T) differed from run(0) by 35.7 in-figure (73% of her
# pixels) -- joints 4.3 cm and the hips 1.5 deg apart, so the loop popped at the wrap, in the pack
# and in the 3D game alike. THE CAUSE is a window, not a pose: Meshy's run (anims/run.glb) closes
# EXACTLY -- its keys run 0.0333 .. 0.7667 s at 30 fps and pose(0.0333) == pose(0.7667) -- but the
# D7 merge took Blender frames 0..18 at 24 fps, i.e. clip time 0 .. 0.75 s: it started 1/30 s early
# (a clamped hold on the first key) and ended 1/60 s before the cycle closes.
# THE FIX re-cuts the clip on the source's own cycle: every channel re-sampled at the SOURCE'S keys
# (no resampling error), shifted to start at 0 -- 23 keys, 0 .. 0.7333 s -- the last key set equal
# to the first (it is, to 2 um; now to the bit). The Hips translation keeps the export's hygiene
# (the re-ground and recentre offset, constant; the de-root trend was an artifact of the incomplete
# cycle and a closed cycle has no net travel to remove). weapon_r's one-key rest tracks (s13) are kept.
# A binary patch: only the `run` animation is replaced; every other clip, mesh and joint is untouched
# (checked: the other accessors' bytes are compared before and after).
import hashlib, json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export')
a = sys.argv[1:]
EXP, SRC, OUT = a[0], a[1], a[2]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
js, b0 = L.load_glb(EXP); bn = bytearray(b0)
sj, sb = L.load_glb(SRC)
enid = {n.get('name'): i for i, n in enumerate(js['nodes'])}
san = sj['animations'][0]
chan = {}
for ch in san['channels']:
    s = san['samplers'][ch['sampler']]
    chan[(sj['nodes'][ch['target']['node']].get('name'), ch['target']['path'])] = (
        L.read_accessor(sj, sb, s['input'])[:, 0].astype(float), L.read_accessor(sj, sb, s['output']).astype(float), s.get('interpolation', 'LINEAR'))
tsrc = max((c[0] for c in chan.values()), key=len)                 # the source's own key times (30 fps)
T0, T1 = float(tsrc[0]), float(tsrc[-1])
tnew = tsrc - T0


def sample(tt, vv, interp, t, path):
    if len(tt) == 1 or t <= tt[0]:
        return vv[0]
    if t >= tt[-1]:
        return vv[-1]
    k = int(np.searchsorted(tt, t)); a0, a1 = tt[k - 1], tt[k]
    if interp == 'STEP':
        return vv[k - 1]
    w = (t - a0) / (a1 - a0)
    v0, v1 = vv[k - 1], vv[k]
    if path == 'rotation':
        if np.dot(v0, v1) < 0:
            v1 = -v1
        v = (1 - w) * v0 + w * v1
        return v / np.linalg.norm(v)
    return (1 - w) * v0 + w * v1


ean = next(an for an in js['animations'] if an.get('name') == 'run')
eidx = js['animations'].index(ean)
# the export's Hips translation offset over the old run (its re-ground/recentre), for the new keys
old = {}
for ch in ean['channels']:
    s = ean['samplers'][ch['sampler']]
    old[(js['nodes'][ch['target']['node']].get('name'), ch['target']['path'])] = (
        L.read_accessor(js, bn, s['input'])[:, 0].astype(float), L.read_accessor(js, bn, s['output']).astype(float), s)
ht, hv, _ = old[('Hips', 'translation')]
st_, sv_, si_ = chan[('Hips', 'translation')]
offs = np.array([hv[k] - sample(st_, sv_, si_, ht[k], 'translation') for k in range(len(ht))])
OFF = offs.mean(0)


def put(data):
    while len(bn) % 4: bn.append(0)
    off = len(bn); bn.extend(data); return off


def add_acc(arr, typ, mm=False):
    arr = np.ascontiguousarray(arr, np.float32)
    js['bufferViews'].append(dict(buffer=0, byteOffset=put(arr.tobytes()), byteLength=arr.nbytes))
    acc = dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=int(arr.shape[0]), type=typ)
    if mm:
        acc['min'] = [float(v) for v in np.atleast_1d(arr.min(0))]; acc['max'] = [float(v) for v in np.atleast_1d(arr.max(0))]
    js['accessors'].append(acc); return len(js['accessors']) - 1


def acc_bytes(jj, bb, i):
    ac = jj['accessors'][i]
    if 'bufferView' not in ac:                                      # zero-filled (sparse/morph) accessors: nothing to compare
        return None
    bv = jj['bufferViews'][ac['bufferView']]; o = bv.get('byteOffset', 0)
    return bytes(bb[o: o + bv['byteLength']])


before = {i: acc_bytes(js, bn, i) for i in range(len(js['accessors']))}
tin = add_acc(tnew.reshape(-1, 1), 'SCALAR', mm=True)
samplers, channels, worst = [], [], 0.0
for (name, path), (tt, vv, interp) in chan.items():
    if name not in enid:
        continue
    vals = np.array([sample(tt, vv, interp, t, path) for t in tsrc])
    if path == 'translation' and name == 'Hips':
        vals = vals + OFF
    gap = float(np.max(np.abs(vals[-1] - vals[0]))); worst = max(worst, gap if path != 'rotation' else 0.0)
    vals[-1] = vals[0]                                              # the cycle closes to the bit
    if path == 'rotation':
        for k in range(1, len(vals)):                               # continuous for slerp
            if np.dot(vals[k], vals[k - 1]) < 0:
                vals[k] = -vals[k]
    samplers.append(dict(input=tin, output=add_acc(vals, 'VEC4' if path == 'rotation' else 'VEC3'), interpolation='LINEAR'))
    channels.append(dict(sampler=len(samplers) - 1, target=dict(node=enid[name], path=path)))
for (name, path), (tt, vv, s) in old.items():                       # weapon_r's rest tracks (s13), kept as they were
    if name in ('weapon_r', 'weapon_l'):
        if tt.max() > tnew[-1] + 1e-4:
            # a Blender re-export (s10_combine) writes them as 2-key CONSTANT tracks over the OLD 0..0.75 s --
            # kept as they are, they would stretch the clip back to 0.75 s. Constant -> one key; else refuse.
            if float(np.ptp(vv, axis=0).max()) > 1e-4:
                raise SystemExit("%s.%s moves during the run -- not a rest track; refusing to re-time it" % (name, path))
            samplers.append(dict(input=add_acc(np.zeros((1, 1)), 'SCALAR', mm=True),
                                 output=add_acc(vv[:1], 'VEC4' if path == 'rotation' else 'VEC3'), interpolation='STEP'))
        else:
            samplers.append(dict(input=s['input'], output=s['output'], interpolation=s.get('interpolation', 'STEP')))
        channels.append(dict(sampler=len(samplers) - 1, target=dict(node=enid[name], path=path)))
js['animations'][eidx] = dict(name='run', samplers=samplers, channels=channels)
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn)))
    f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
# every accessor that existed before is byte-identical after (the old run's are simply no longer used)
nj, nb = L.load_glb(OUT)
same = all(acc_bytes(nj, nb, i) == v for i, v in before.items())
other = [an['name'] for an in js['animations'] if an['name'] != 'run']
Lr = L.lint(OUT)
rep = dict(cause="the D7 merge cut 0..0.75 s (24 fps frames 0..18) from a source whose cycle is 0.0333..0.7667 s: 1/30 s of clamped hold at the start, 1/60 s short at the end",
           source=dict(file=os.path.basename(SRC), cycle_s=[round(T0, 4), round(T1, 4)], period_s=round(T1 - T0, 4), keys=len(tsrc)),
           new=dict(duration_s=round(float(tnew[-1]), 6), keys=len(tnew), channels=len(channels)),
           hips_offset_units=[round(float(v), 4) for v in OFF], source_cycle_gap_before_snap=round(worst, 6),
           other_clips_untouched=other, prior_accessors_byte_identical=bool(same), lint=dict(verdict=Lr['verdict'], fails=Lr['fails']))
print(json.dumps(rep))
if OUTJ:
    json.dump(rep, open(OUTJ, 'w'), indent=1)
