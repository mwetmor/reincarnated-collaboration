# HAFT RE-SEAT (T12_12c, the conductor on R-C9-115, from the JOIN lane's finding): pitch the weapon's tip toward his aim by
# turning the haft IN THE CLOSED FIST -- no joint changes. The weapon bone's rest and every one of its rotation keys, in every
# clip, are post-multiplied by one rotation about the weapon's own local X (across the haft, +Y, and the edge, +Z) through
# the grip (the bone's origin): the tip goes toward the edge's side by R deg, the butt the other way. A constant transform
# in the hand, so every clip -- holds and strikes -- carries it alike.
#
#   python3 scripts/64_haft_reseat.py <in.glb> <out.glb> <deg> [--bone weapon_r] [--mount in_mount.json out_mount.json]
#           [--json f]
#
# --mount rewrites the recorded mount's W (the bone's rest, read by 21_lint_export's WEAPON REST row) to the re-seated rest,
# so the lint checks the new seat rather than failing it; G and the rest of the record are kept.
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
C54 = __import__('54_weapon_channel')


def qn(q):
    q = np.asarray(q, float); return q / np.linalg.norm(q)


def main():
    a = sys.argv[1:]
    src, dst, deg = a[0], a[1], float(a[2])
    bone = a[a.index('--bone') + 1] if '--bone' in a else 'weapon_r'
    outj = a[a.index('--json') + 1] if '--json' in a else None
    js, b0 = L.load_glb(src); bin_ = bytearray(b0); nodes = js['nodes']
    wi = [i for i, n in enumerate(nodes) if n.get('name') == bone][0]
    Rs = W.axis_angle(np.array([1.0, 0.0, 0.0]), math.radians(deg))
    nd = nodes[wi]
    r0 = W.q2m(qn(nd.get('rotation', [0, 0, 0, 1])))
    nd['rotation'] = [float(x) for x in qn(W.m2q(r0 @ Rs))]
    rep = dict(bone=bone, deg=deg, axis="the bone's local +X (across haft +Y and edge +Z), through its origin (the grip)",
               rest_before=[float(x) for x in W.m2q(r0)], rest_after=nd['rotation'], clips={})
    for an in js['animations']:
        for ch in an['channels']:
            if ch['target']['node'] != wi or ch['target']['path'] != 'rotation': continue
            s = an['samplers'][ch['sampler']]
            vv = L.read_accessor(js, bin_, s['output']).astype(float)
            q = np.array([qn(W.m2q(W.q2m(qn(x)) @ Rs)) for x in vv])
            for i in range(1, len(q)):
                if np.dot(q[i], q[i - 1]) < 0: q[i] = -q[i]
            an['samplers'].append({"input": s['input'], "output": C54.add_accessor(js, bin_, q, "VEC4"),
                                   "interpolation": s.get('interpolation', 'LINEAR')})
            ch['sampler'] = len(an['samplers']) - 1
            rep['clips'][an['name']] = len(q)
    js['buffers'][0]['byteLength'] = len(bin_) + (-len(bin_) % 4)
    if '--mount' in a:
        mi, mo = a[a.index('--mount') + 1], a[a.index('--mount') + 2]
        m = json.load(open(mi)); Wm = np.array(m['W'], float)
        Wm[:3, :3] = Wm[:3, :3] @ Rs
        m['W'] = Wm.tolist(); m['reseat_deg'] = deg
        m['written_by'] = m.get('written_by', '') + " ; 64_haft_reseat.py %+.1f deg about the bone's local X" % deg
        json.dump(m, open(mo, 'w'), indent=1)
        if os.path.dirname(os.path.abspath(mo)) != os.path.dirname(os.path.abspath(dst)):
            print("note: the mount record is not beside %s; the lint will read another" % dst)
    R_.write_glb(dst, js, bin_)
    res = L.lint(dst)
    print("haft re-seat %+.1f deg on %s: rest + %d clips' keys -> %s; lint %s, %d fails"
          % (deg, bone, len(rep['clips']), os.path.basename(dst), res['verdict'], len(res['fails'])))
    for f in res['fails']: print("  FAIL", f)
    if outj: json.dump(rep, open(outj, 'w'), indent=1)


if __name__ == "__main__":
    main()
