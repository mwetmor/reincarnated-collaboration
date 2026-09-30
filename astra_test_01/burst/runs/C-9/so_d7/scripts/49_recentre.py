# Put every clip back over the rig origin -- horizontally -- as a BINARY ACCESSOR PATCH.
#
#   python3 scripts/49_recentre.py <in.glb> <out.glb> [--json f]
#
# THE DEFECT, found by the scene (attack_lab, 2026-09-29): three clips stand a metre or two
# away from the point the body stands on.
#
#     idle_armed   hips 1.102 m from the origin on average, never nearer than 0.834
#     run_armed    1.830 m, never nearer than 1.764
#     attack_chop  0.487 m at its first frame, never nearer than 0.367
#
# every other clip keeps its hips within 0.15 m and passes within 0.07 m of the origin.
# A consumer stands the body at the origin, so a displaced clip is DRAWN a metre from its
# own capsule -- and every blend into or out of it drags the whole figure across the
# ground by the difference. Out of idle_armed into the slash that is a 1.32 m lurch in
# the 0.10 s fade-in: Matt's "glitch in the chop and attack".
#
# HOW IT GOT THERE. 45_deroot_trim.py removes drift by subtracting the first-to-last line
# and then ADDING BACK FIT[0] -- the clip's own first-frame position. That kills the travel
# and keeps wherever the clip happened to start: Meshy's Axe Stance starts 1.1 m off, and
# run_armed was trimmed out of the middle of a travelling take, 1.87 m along it.
# attack_chop is KEEP_ROOT and was never touched. The lint never saw any of it: it checks
# whether a clip MOVES (first to last), and a de-rooted clip does not move -- it just
# stands somewhere else.
#
# THE FIX IS A CONSTANT, so it is a patch, not a rebuild. A horizontal offset on the Hips
# translation moves the whole body rigidly and changes nothing about the pose, so it needs
# no Blender round-trip -- which resamples, and has already cost this file a 30->24 fps
# resample of attack_chop. Only the Hips translation accessors of the displaced clips are
# rewritten; the script proves every other byte of the BIN chunk is unchanged.
#
#   loops (idle/walk/run/strafe)  shifted so their MEAN hips sit over the rest position
#   one-shots (attack/chop/bash)  shifted so their FIRST FRAME does -- a strike starts
#                                 where the idle stands him, and a lunge then carries him
#
# Only clips that never bring the hips within ROOT_OFFSET_TOL of the rest position are
# touched; the same test is the new FAIL in 21_lint_export.py.
import json, struct, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
L = __import__('21_lint_export')

ROOT_OFFSET_TOL = 0.25
ONE_SHOT_WORDS = ('attack', 'chop', 'bash', 'block', 'push', 'strike')


def write_glb(path, js, bin_):
    j = json.dumps(js, separators=(',', ':')).encode('utf-8')
    j += b' ' * (-len(j) % 4)
    b = bytes(bin_) + b'\x00' * (-len(bin_) % 4)
    total = 12 + 8 + len(j) + 8 + len(b)
    with open(path, 'wb') as f:
        f.write(struct.pack('<4sII', b'glTF', 2, total))
        f.write(struct.pack('<II', len(j), 0x4E4F534A)); f.write(j)
        f.write(struct.pack('<II', len(b), 0x004E4942)); f.write(b)


def main():
    a = sys.argv[1:]
    src, dst = a[0], a[1]
    outj = a[a.index('--json') + 1] if '--json' in a else None
    js, bin_ = L.load_glb(src)
    bin_ = bytearray(bin_)
    orig = bytes(bin_)
    nodes = js['nodes']
    parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
    joints = {j for sk in js.get('skins', []) for j in sk.get('joints', [])}
    roots = [j for j in joints if parent.get(j) not in joints]
    assert len(roots) == 1, "expected one skeleton root, found %s" % roots
    hips = roots[0]
    rest = np.array(nodes[hips].get('translation', [0, 0, 0]), dtype=np.float64)
    mpu, k = 1.0, parent.get(hips)
    while k is not None:
        mpu *= float(nodes[k].get('scale', [1, 1, 1])[1])
        k = parent.get(k)
    # which accessor carries each clip's root translation -- and is it SHARED? A shared
    # accessor would move every clip that uses it, so refuse rather than guess.
    uses = {}
    for an in js['animations']:
        for s in an['samplers']:
            uses[s['output']] = uses.get(s['output'], 0) + 1
    rep, patched = {}, []
    for an in js['animations']:
        cn = an.get('name', '?')
        for ch in an['channels']:
            t = ch['target']
            if t.get('node') != hips or t.get('path') != 'translation':
                continue
            acc_i = an['samplers'][ch['sampler']]['output']
            v = L.read_accessor(js, bytes(bin_), acc_i)
            hz = np.hypot(v[:, 0] - rest[0], v[:, 2] - rest[2]) * mpu
            row = dict(closest_m=round(float(hz.min()), 4), mean_m=round(float(hz.mean()), 4),
                       first_m=round(float(hz[0]), 4))
            if hz.min() <= ROOT_OFFSET_TOL:
                row['action'] = 'none -- passes within %.2f m of the rest position' % ROOT_OFFSET_TOL
                rep[cn] = row
                continue
            assert uses[acc_i] == 1, "clip %s: root accessor %d is shared by %d samplers" % (cn, acc_i, uses[acc_i])
            one_shot = any(w in cn.lower() for w in ONE_SHOT_WORDS)
            ref = v[0] if one_shot else v.mean(axis=0)
            off = np.array([ref[0] - rest[0], 0.0, ref[2] - rest[2]])
            acc = js['accessors'][acc_i]
            assert acc['componentType'] == 5126 and acc['type'] == 'VEC3'
            bv = js['bufferViews'][acc['bufferView']]
            base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
            stride = bv.get('byteStride') or 12
            for i in range(acc['count']):
                x, y, z = struct.unpack_from('<3f', bin_, base + i * stride)
                struct.pack_into('<3f', bin_, base + i * stride, x - off[0], y, z - off[2])
            patched.append((base, base + (acc['count'] - 1) * stride + 12))
            if 'min' in acc and 'max' in acc:
                nv = L.read_accessor(js, bytes(bin_), acc_i)
                acc['min'] = [float(x) for x in nv.min(axis=0)]
                acc['max'] = [float(x) for x in nv.max(axis=0)]
            v2 = L.read_accessor(js, bytes(bin_), acc_i)
            hz2 = np.hypot(v2[:, 0] - rest[0], v2[:, 2] - rest[2]) * mpu
            row.update(action='recentred on its %s' % ('FIRST FRAME (one-shot)' if one_shot else 'MEAN (loop)'),
                       shift_m=round(float(np.hypot(off[0], off[2]) * mpu), 4),
                       shift_units=[round(float(off[0]), 4), 0.0, round(float(off[2]), 4)],
                       after=dict(closest_m=round(float(hz2.min()), 4), mean_m=round(float(hz2.mean()), 4),
                                  first_m=round(float(hz2[0]), 4)),
                       keys=int(acc['count']))
            rep[cn] = row
            print("  %-28s %s by %.3f m: closest %.3f -> %.3f m, first %.3f -> %.3f m"
                  % (cn, row['action'], row['shift_m'], row['closest_m'], row['after']['closest_m'],
                     row['first_m'], row['after']['first_m']))
    # PROOF OF SURGERY: nothing outside the patched accessors may differ
    changed = [i for i in range(len(orig)) if orig[i] != bin_[i]]
    outside = [i for i in changed if not any(a0 <= i < a1 for a0, a1 in patched)]
    assert not outside, "%d changed bytes lie OUTSIDE the patched accessors" % len(outside)
    write_glb(dst, js, bin_)
    # and the output must pass the lint's own offset rule
    res = L.lint(dst)
    off_fails = [f for f in res['fails'] if 'stands' in f]
    print("wrote %s: %d accessors patched, %d BIN bytes changed, 0 outside them; lint %s (%d fails, %d warns)"
          % (dst, len(patched), len(changed), res['verdict'], len(res['fails']), len(res['warns'])))
    assert not off_fails, off_fails
    summary = dict(tolerance_m=ROOT_OFFSET_TOL, metres_per_unit=mpu, rest_units=rest.tolist(),
                   clips=rep, accessors_patched=len(patched), bin_bytes_changed=len(changed),
                   bin_bytes_changed_outside_patches=0, lint_verdict=res['verdict'],
                   lint_fails=res['fails'], lint_warns=res['warns'])
    if outj:
        json.dump(summary, open(outj, 'w'), indent=1)
    return summary


if __name__ == '__main__':
    main()
