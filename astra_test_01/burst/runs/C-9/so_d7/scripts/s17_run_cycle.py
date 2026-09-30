# THE RUN'S LOOP SEAM, fixed at its source (JOIN-1 pack review, conductor 2026-09-30).
#
#   python3 scripts/s17_run_cycle.py <export so-body.glb> <source clip.glb> <out so-body.glb> [--clip run] [--json f]
#        [--oneshot] [--drop-weapon] [--hips-model auto|constant]
#
# --oneshot (2026-09-30, the sorceress v2: idle, hit, death and both casts re-cut the same way): a clip that does not
# loop -- re-cut on the source's own keys from its first to its last, shifted to start at 0, WITHOUT the loop's last-key
# snap. The D7 merge baked these at 24 fps from t = 0 (shipped time = source time), so each began with a clamped hold on
# the source's first key (its first key interval at a fifth of speed) and several ended before the source's last key.
# --drop-weapon: a weapon track that MOVES (the Meteor's baked staff, s13) is dropped rather than refused, for
# s13_meteor_track.py to bake again on the new keys; a constant one is kept as before.
# THE HIPS, two models, chosen by measurement on the OLD window (export against source at the export's keys):
#   constant   the offset is constant (std <= 1e-3 units): re-ground/recentre/start-shift -- re-applied as before
#   de-root    the offset is LINEAR in time: 45_deroot_trim's rule (the first-to-last line of the hips' horizontal path
#              taken out, the residual's mean on the rest position; vertical = the constant re-ground). Verified by
#              rebuilding the OLD export's hips from the source with that rule (<= 2e-3 units), then RE-DERIVED on the new
#              window -- transplanting the old offsets would leave the new window's net travel un-removed
# Every export channel must be accounted for (in the source, or a weapon track); anything else is refused.
#
# --clip (2026-09-30, the walk dispatch): any in-place loop, not only the run -- the walk carries the same
# merge window (a clamped hold on the first source key; its cycle is 0.0333 .. 1.0 s, 29 intervals at 30 fps).
# Each channel is CLASSIFIED against the export before it is re-cut, so the export's hygiene survives:
#   faithful         the export equals the source over the old window (<= 2e-3): re-cut from the source
#   hips offset      Hips translation: the export's constant re-ground/recentre offset is re-applied
#   export constant  constant in BOTH files but different (the walk's Hips SCALE: Meshy's 1.1765, stripped
#                    to 1 by the D7 hygiene) -- the export's value is kept; copying the source would undo it
#   anything else    refused: a processing step this script does not know how to carry
# The run's classes (Hips offset + 71 faithful) take exactly the code path they took before --channel
# order, values, accessors -- so re-running on export_p2k reproduces the run re-cut byte-for-byte (checked).
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
CLIP = a[a.index('--clip') + 1] if '--clip' in a else 'run'
ONESHOT = '--oneshot' in a
# --hips-model auto|constant: auto picks the de-root rule when the old offset is not constant (the default since the
# sorceress v2); constant is the model the run's and the walk's re-cuts shipped with (the run's offset has a 1.3 mm std
# that the constant model averaged) and reproduces those re-cuts byte-for-byte
HMODEL = a[a.index('--hips-model') + 1] if '--hips-model' in a else 'auto'
DROPW = '--drop-weapon' in a
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


ean = next(an for an in js['animations'] if an.get('name') == CLIP)
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
TOL = 2e-3
HIPS = dict(model='constant', offset_std_units=[round(float(v), 4) for v in offs.std(0)])
if HMODEL == 'auto' and float(offs.std(0).max()) > 1e-3:
    # DE-ROOTED (45_deroot_trim): export_h = source_h - FIT + ANCHOR on the OLD window, FIT the first-to-last line over its
    # keys; vertical = source + a constant. The Hips' parent frame's vertical axis, from the parent's world rotation:
    par = {c: i for i, nd in enumerate(js['nodes']) for c in nd.get('children', [])}
    def gmat(i):
        nd = js['nodes'][i]; M = np.eye(4)
        if 'matrix' in nd:
            M = np.array(nd['matrix'], float).reshape(4, 4).T
        else:
            x, y, z, w = nd.get('rotation', [0, 0, 0, 1]); S = np.array(nd.get('scale', [1, 1, 1]), float)
            R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                          [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                          [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
            M[:3, :3] = R * S; M[:3, 3] = nd.get('translation', [0, 0, 0])
        return M if par.get(i) is None else gmat(par[i]) @ M
    hid = enid['Hips']
    Rp = gmat(par[hid])[:3, :3] if par.get(hid) is not None else np.eye(3)
    upl = Rp.T @ np.array([0.0, 1.0, 0.0]); upl = upl / np.linalg.norm(upl)
    VAX = int(np.argmax(np.abs(upl)))
    if abs(upl[VAX]) < 0.99:
        raise SystemExit("REFUSED -- the Hips' parent frame is not axis-aligned with world up (%s)" % upl)
    HAX = [i for i in range(3) if i != VAX]
    Hs_old = np.array([sample(st_, sv_, si_, t, 'translation') for t in ht])
    u_old = (ht - ht[0]) / (ht[-1] - ht[0])
    FIT_old = Hs_old[0] + (Hs_old[-1] - Hs_old[0]) * u_old[:, None]
    A_ = hv - (Hs_old - FIT_old)                                   # the anchor at every old key: constant if the rule holds
    ANCH = A_.mean(0)
    dev = float(np.abs(A_[:, HAX] - ANCH[HAX]).max())
    vstd = float(offs[:, VAX].std())
    if dev > TOL or vstd > 1e-3:
        raise SystemExit("REFUSED -- the Hips offset is neither constant nor 45_deroot_trim's line (anchor deviates %.5f, "
                         "vertical std %.5f)" % (dev, vstd))
    REST_H = ANCH[HAX] + (Hs_old - FIT_old)[:, HAX].mean(0)       # 45's anchor: the residual's mean sits on the rest
    HIPS = dict(model='de-root (45_deroot_trim, re-derived on the new window)', offset_std_units=HIPS['offset_std_units'],
                old_window_rebuilt_worst_units=round(dev, 6), vertical_axis=VAX, vertical_offset_units=round(float(OFF[VAX]), 4),
                rest_h_units=[round(float(v), 4) for v in REST_H],
                hips_node_rest_h_units=[round(float(js['nodes'][hid].get('translation', [0, 0, 0])[i]), 4) for i in HAX])
cls, worst_faithful, refused = {}, 0.0, []
for (name, path), (tt, vv, interp) in chan.items():
    if name not in enid:
        continue
    if (name, path) not in old:
        cls[(name, path)] = 'dropped (not in the export)'; continue
    et, ev, _ = old[(name, path)]
    sv = np.array([sample(tt, vv, interp, t, path) for t in et])
    if path == 'rotation':
        sv = np.array([x if np.dot(x, y) >= 0 else -x for x, y in zip(sv, ev)])
    d = float(np.abs(ev - sv).max())
    if (name, path) == ('Hips', 'translation'):
        cls[(name, path)] = 'hips offset'
    elif d <= TOL:
        cls[(name, path)] = 'faithful'; worst_faithful = max(worst_faithful, d)
    elif float(np.ptp(ev, axis=0).max()) <= 1e-6 and float(np.ptp(vv, axis=0).max()) <= 1e-6:
        cls[(name, path)] = 'export constant'
    else:
        refused.append("%s.%s differs from the source by %.4f and is not constant" % (name, path, d))
for (name, path), (tt, vv, s) in old.items():                       # every export channel accounted for
    if (name, path) not in chan and name not in ('weapon_r', 'weapon_l'):
        refused.append("%s.%s is in the export's clip but not in the source, and is not a weapon track" % (name, path))
if refused:
    raise SystemExit("REFUSED -- the export processed these channels in a way this script cannot carry:\n  " + "\n  ".join(refused))


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
    if cls.get((name, path), '').startswith('dropped'):
        continue
    vals = np.array([sample(tt, vv, interp, t, path) for t in tsrc])
    if path == 'translation' and name == 'Hips' and HIPS['model'] != 'constant':
        un = (tsrc - tsrc[0]) / (tsrc[-1] - tsrc[0])
        FIT = vals[0] + (vals[-1] - vals[0]) * un[:, None]
        RES = vals - FIT
        new = vals + OFF                                            # vertical: the constant re-ground
        new[:, HAX] = RES[:, HAX] - RES[:, HAX].mean(0) + REST_H     # horizontal: 45's rule on the new window
        HIPS['net_travel_units_after'] = round(float(np.linalg.norm(new[-1, HAX] - new[0, HAX])), 5)
        HIPS['net_travel_units_source'] = round(float(np.linalg.norm(vals[-1, HAX] - vals[0, HAX])), 4)
        vals = new
    elif path == 'translation' and name == 'Hips':
        vals = vals + OFF
    elif cls[(name, path)] == 'export constant':                    # the export's hygiene value, at every new key
        vals = np.repeat(old[(name, path)][1][:1], len(tsrc), axis=0)
    gap = float(np.max(np.abs(vals[-1] - vals[0]))); worst = max(worst, gap if path != 'rotation' else 0.0)
    if not ONESHOT:
        vals[-1] = vals[0]                                          # the cycle closes to the bit
    if path == 'rotation':
        for k in range(1, len(vals)):                               # continuous for slerp
            if np.dot(vals[k], vals[k - 1]) < 0:
                vals[k] = -vals[k]
    samplers.append(dict(input=tin, output=add_acc(vals, 'VEC4' if path == 'rotation' else 'VEC3'), interpolation='LINEAR'))
    channels.append(dict(sampler=len(samplers) - 1, target=dict(node=enid[name], path=path)))
dropped_w = []
for (name, path), (tt, vv, s) in old.items():                       # weapon_r's rest tracks (s13), kept as they were
    if name in ('weapon_r', 'weapon_l'):
        if len(vv) > 1 and float(np.ptp(vv, axis=0).max()) > 1e-4:
            # a MOVING weapon track (the Meteor's baked staff) is keyed on the OLD time base: kept as it is, it would play
            # 1/30 s late against the re-cut body (and a second bake would target the same channel twice). Dropped for
            # s13 to bake again on the new keys, or refused.
            if DROPW:
                dropped_w.append("%s.%s" % (name, path)); continue
            raise SystemExit("%s.%s moves during the %s -- not a rest track; refusing to re-time it" % (name, path, CLIP))
        if tt.max() > tnew[-1] + 1e-4:
            # a Blender re-export (s10_combine) writes them as 2-key CONSTANT tracks over the OLD 0..0.75 s --
            # kept as they are, they would stretch the clip back to 0.75 s. Constant -> one key.
            samplers.append(dict(input=add_acc(np.zeros((1, 1)), 'SCALAR', mm=True),
                                 output=add_acc(vv[:1], 'VEC4' if path == 'rotation' else 'VEC3'), interpolation='STEP'))
        else:
            samplers.append(dict(input=s['input'], output=s['output'], interpolation=s.get('interpolation', 'STEP')))
        channels.append(dict(sampler=len(samplers) - 1, target=dict(node=enid[name], path=path)))
js['animations'][eidx] = dict(name=CLIP, samplers=samplers, channels=channels)
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
other = [an['name'] for an in js['animations'] if an['name'] != CLIP]
Lr = L.lint(OUT)
ot = old[('Hips', 'rotation')][0] if ('Hips', 'rotation') in old else next(iter(old.values()))[0]
efps, sfps = 1.0 / float(np.median(np.diff(ot))), 1.0 / float(np.median(np.diff(tsrc)))
cause = ("the D7 merge cut %.4f..%.4f (%d keys at %.0f fps) from a source whose cycle is %.4f..%.4f (%d keys at %.0f fps) and "
         "closes there: it began %.4f before the source's first key (a clamped hold) and ended %s"
         % (ot.min(), ot.max(), len(ot), efps, T0, T1, len(tsrc), sfps, T0 - ot.min(),
            ("%.4f before its close" % (T1 - ot.max())) if ot.max() < T1 - 1e-4 else
            (("%.4f after its close" % (ot.max() - T1)) if ot.max() > T1 + 1e-4 else "exactly at its close")))
if ONESHOT:
    cause = ("the D7 merge baked %.4f..%.4f (%d keys at %.0f fps) with shipped time = source time from a source keyed %.4f..%.4f "
             "(%d keys at %.0f fps): the first %.4f s held the source's first pose (a clamped hold), and it ended %s"
             % (ot.min(), ot.max(), len(ot), efps, T0, T1, len(tsrc), sfps, T0 - ot.min(),
                ("%.4f before the source's last key" % (T1 - ot.max())) if ot.max() < T1 - 1e-4 else
                (("%.4f after it" % (ot.max() - T1)) if ot.max() > T1 + 1e-4 else "exactly at the source's last key")))
if CLIP == 'run':                                                   # the run's record keeps its first wording
    cause = "the D7 merge cut 0..0.75 s (24 fps frames 0..18) from a source whose cycle is 0.0333..0.7667 s: 1/30 s of clamped hold at the start, 1/60 s short at the end"
counts = {}
for v in cls.values():
    counts[v] = counts.get(v, 0) + 1
rep = dict(clip=CLIP, mode='one-shot (no loop snap)' if ONESHOT else 'loop', hips=HIPS,
           weapon_tracks_dropped_for_rebake=dropped_w, cause=cause,
           channels_classified=dict(counts=counts, faithful_worst=round(worst_faithful, 6), tolerance=TOL,
                                    hips_offset_std_units=[round(float(v), 4) for v in offs.std(0)],
                                    not_faithful={"%s.%s" % k: v for k, v in cls.items() if v != 'faithful'}),
           source=dict(file=os.path.basename(SRC), cycle_s=[round(T0, 4), round(T1, 4)], period_s=round(T1 - T0, 4), keys=len(tsrc)),
           new=dict(duration_s=round(float(tnew[-1]), 6), keys=len(tnew), channels=len(channels)),
           hips_offset_units=[round(float(v), 4) for v in OFF], source_cycle_gap_before_snap=round(worst, 6),
           other_clips_untouched=other, prior_accessors_byte_identical=bool(same), lint=dict(verdict=Lr['verdict'], fails=Lr['fails']))
print(json.dumps(rep))
if OUTJ:
    json.dump(rep, open(OUTJ, 'w'), indent=1)
