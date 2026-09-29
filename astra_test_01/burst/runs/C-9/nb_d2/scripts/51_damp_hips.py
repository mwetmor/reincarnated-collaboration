# Damp one clip's HORIZONTAL hip excursion about the rest position, as a binary accessor patch.
#
#   python3 scripts/51_damp_hips.py <in.glb> <out.glb> --clip idle_armed --limit 0.10 [--json f]
#
# WHY (coordinator, 2026-09-29): an armed idle should stand planted, and the integration build
# measured the Axe Stance idle drawing his body up to 0.40 m from his node. Scaling the hips'
# horizontal offset from rest by k = limit / (its largest offset) keeps weight shifts within the
# limit. Vertical motion is untouched (the breathing and the crouch survive).
#
# MEASURED COST, attack_lab: none. A planted foot moves by -(1-k) x the hips' motion on the frames
# it is down, and the Axe Stance makes its big hip moves while a foot is in the air: planted-foot
# slide 35.8 -> 36.5 mm/frame median and 0.752 -> 0.740 m total (5 cm band), worst frame 72.1 ->
# 61.2. WHAT IT DOES NOT DO: make the Axe Stance planted. It is a footwork clip at source -- the
# thigh swings 130 deg in Meshy's own file -- and its feet still wander 1.37 m after this.
import json, struct, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
L = __import__('21_lint_export')
R = __import__('49_recentre')


def main():
    a = sys.argv[1:]
    src, dst = a[0], a[1]
    clip = a[a.index('--clip') + 1]
    limit = float(a[a.index('--limit') + 1])
    outj = a[a.index('--json') + 1] if '--json' in a else None
    js, bin_ = L.load_glb(src)
    bin_ = bytearray(bin_)
    orig = bytes(bin_)
    nodes = js['nodes']
    parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
    joints = {j for sk in js.get('skins', []) for j in sk.get('joints', [])}
    hips = [j for j in joints if parent.get(j) not in joints][0]
    rest = np.array(nodes[hips].get('translation', [0, 0, 0]), dtype=np.float64)
    mpu, k0 = 1.0, parent.get(hips)
    while k0 is not None:
        mpu *= float(nodes[k0].get('scale', [1, 1, 1])[1]); k0 = parent.get(k0)
    uses = {}
    for an in js['animations']:
        for s in an['samplers']:
            uses[s['output']] = uses.get(s['output'], 0) + 1
    an = next(x for x in js['animations'] if x.get('name') == clip)
    ch = next(c for c in an['channels'] if c['target'].get('node') == hips and c['target'].get('path') == 'translation')
    acc_i = an['samplers'][ch['sampler']]['output']
    assert uses[acc_i] == 1, "root accessor shared"
    v = L.read_accessor(js, bytes(bin_), acc_i)
    off = np.hypot(v[:, 0] - rest[0], v[:, 2] - rest[2]) * mpu
    k = min(1.0, limit / max(float(off.max()), 1e-9))
    acc = js['accessors'][acc_i]
    bv = js['bufferViews'][acc['bufferView']]
    base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
    stride = bv.get('byteStride') or 12
    for i in range(acc['count']):
        x, y, z = struct.unpack_from('<3f', bin_, base + i * stride)
        struct.pack_into('<3f', bin_, base + i * stride, rest[0] + (x - rest[0]) * k, y, rest[2] + (z - rest[2]) * k)
    if 'min' in acc and 'max' in acc:
        nv = L.read_accessor(js, bytes(bin_), acc_i)
        acc['min'] = [float(x) for x in nv.min(axis=0)]; acc['max'] = [float(x) for x in nv.max(axis=0)]
    v2 = L.read_accessor(js, bytes(bin_), acc_i)
    off2 = np.hypot(v2[:, 0] - rest[0], v2[:, 2] - rest[2]) * mpu
    span = (base, base + (acc['count'] - 1) * stride + 12)
    changed = [i for i in range(len(orig)) if orig[i] != bin_[i]]
    outside = [i for i in changed if not (span[0] <= i < span[1])]
    assert not outside, "%d bytes changed outside the patched accessor" % len(outside)
    R.write_glb(dst, js, bin_)
    res = L.lint(dst)
    rep = dict(clip=clip, limit_m=limit, k=round(k, 4), before_max_m=round(float(off.max()), 4),
               after_max_m=round(float(off2.max()), 4), keys=int(acc['count']), bin_bytes_changed=len(changed),
               bin_bytes_changed_outside=0, lint_verdict=res['verdict'], lint_fails=res['fails'], lint_warns=len(res['warns']))
    print("  %s: hips' horizontal offset from rest %.3f -> %.3f m (x%.4f), %d keys, %d bytes, 0 outside; lint %s (%d fails)"
          % (clip, off.max(), off2.max(), k, acc['count'], len(changed), res['verdict'], len(res['fails'])))
    if outj:
        json.dump(rep, open(outj, 'w'), indent=1)
    assert not res['fails'], res['fails']


if __name__ == '__main__':
    main()
