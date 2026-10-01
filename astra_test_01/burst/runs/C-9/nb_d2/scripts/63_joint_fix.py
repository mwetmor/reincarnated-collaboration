# JOINT LIMITS, FIXED ON THE KEYS (T12_12b): a clip's elbows out of hyperextension and its wrists inside their deviation range,
# measured exactly as the D2 lane's lint measures them (nb_join/scripts/j_joint_lint.py: the hinge's flexion against its
# LEARNED natural direction; the wrist's swing off rest along its LEARNED deviation axis) -- the learned axes are read from that
# lint's own --json report, so the fixer and the lint cannot disagree about which way a joint bends.
#
#   python3 scripts/63_joint_fix.py <in.glb> <out.glb> <lint.json> <clip> [--elbow-min -3] [--dev-max 38] [--json f]
#
# ELBOW: on every key whose flexion is under --elbow-min, the forearm is turned about the hinge (the axis across its natural
#   flexion plane, in the upper arm's frame) by the least angle that brings it to --elbow-min; nothing else moves.
# WRIST: on every key whose |deviation| exceeds --dev-max, the hand's swing off rest is cut along the deviation axis to
#   --dev-max (flexion and twist kept). The hand that HOLDS A WEAPON keeps the weapon still: weapon_r's key at that time is
#   counter-rotated by the same change, so the axe's world orientation -- and its edge -- is the one the gate measured.
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
C54 = __import__('54_weapon_channel')
Y = np.array([0.0, 1.0, 0.0])
HINGE = {'elbow_R': ('RightArm', 'RightForeArm', 'RightHand'), 'elbow_L': ('LeftArm', 'LeftForeArm', 'LeftHand')}
WRIST = {'wrist_R': ('RightForeArm', 'RightHand', 'weapon_r'), 'wrist_L': ('LeftForeArm', 'LeftHand', None)}


def qn(q):
    q = np.asarray(q, float); return q / np.linalg.norm(q)


def main():
    a = sys.argv[1:]
    src, dst, lintj, clip = a[0], a[1], a[2], a[3]
    emin = float(a[a.index('--elbow-min') + 1]) if '--elbow-min' in a else -3.0
    dmax = float(a[a.index('--dev-max') + 1]) if '--dev-max' in a else 38.0
    outj = a[a.index('--json') + 1] if '--json' in a else None
    lj = json.load(open(lintj))['learned']['axes']
    js, b0 = L.load_glb(src); bin_ = bytearray(b0); nodes = js['nodes']
    nid = {n.get('name'): i for i, n in enumerate(nodes)}
    parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
    an = [x for x in js['animations'] if x['name'] == clip][0]
    tracks = {}
    for ci, ch in enumerate(an['channels']):
        s = an['samplers'][ch['sampler']]
        tracks[(ch['target']['node'], ch['target']['path'])] = [ci, L.read_accessor(js, bin_, s['input']).ravel().astype(float),
                                                               L.read_accessor(js, bin_, s['output']).astype(float).copy()]
    rest = {i: (np.array(n.get('translation', [0, 0, 0]), float), qn(n.get('rotation', [0, 0, 0, 1])), np.array(n.get('scale', [1, 1, 1]), float))
            for i, n in enumerate(nodes)}

    def local(i, t):
        tr, q, sc = rest[i]
        for p in ('translation', 'rotation'):
            k = (i, p)
            if k in tracks:
                tt, vv = tracks[k][1], tracks[k][2]
                j = int(np.argmin(np.abs(tt - t)))
                assert abs(tt[j] - t) < 1e-4, "keys must coincide (a grafted clip)"
                if p == 'translation': tr = vv[j]
                else: q = qn(vv[j])
        M = np.eye(4); M[:3, :3] = W.q2m(q) * sc; M[:3, 3] = tr
        return M

    def glob(i, t):
        M = local(i, t)
        while parent.get(i) is not None:
            i = parent[i]; M = local(i, t) @ M
        return M

    def rot(M):
        X = M[:3, :3]; return X / np.linalg.norm(X, axis=0)

    def flex_of(k, t, Rfore_override=None):
        up, mid, lo = HINGE[k]
        Gu = glob(nid[up], t); Gm = glob(nid[mid], t)
        Lm = local(nid[mid], t); Ll = local(nid[lo], t)
        if Rfore_override is not None:
            Lm = Lm.copy(); Lm[:3, :3] = Rfore_override
            Gm = Gu @ Lm
        Gl = Gm @ Ll
        Ru = rot(Gu); d = Ru.T @ (Gl[:3, 3] - Gm[:3, 3]); d /= np.linalg.norm(d)
        ax = Ru.T @ (Gm[:3, 3] - Gu[:3, 3]); ax /= np.linalg.norm(ax)
        th = math.degrees(math.acos(max(-1, min(1, float(d @ ax)))))
        n = np.array(lj['hinge'][k], float); n = n - (n @ ax) * ax; n /= np.linalg.norm(n)
        dev = d - (d @ ax) * ax; nd = np.linalg.norm(dev)
        phi = 0.0 if nd < 1e-9 else math.atan2(float(np.cross(n, dev / nd) @ ax), float(n @ (dev / nd)))
        return th * math.cos(phi), ax, n

    rep = dict(clip=clip, elbow_min=emin, dev_max=dmax, changed=[])
    # ---- ELBOWS
    for k, (up, mid, lo) in HINGE.items():
        key = (nid[mid], 'rotation')
        if key not in tracks: continue
        ci, tt, vv = tracks[key]
        for j, t in enumerate(tt):
            f0, ax, n = flex_of(k, t)
            if f0 >= emin: continue
            h = np.cross(ax, n); h /= np.linalg.norm(h)        # the hinge axis, in the upper's frame
            Rm0 = W.q2m(qn(vv[j]))
            sgn = 1.0
            def f_at(dl):
                return flex_of(k, t, W.axis_angle(h, math.radians(dl)) @ Rm0)[0]
            if f_at(1.0) < f0: sgn = -1.0
            lo_, hi_ = 0.0, 60.0
            for _ in range(50):
                md = 0.5 * (lo_ + hi_)
                if f_at(sgn * md) < emin: lo_ = md
                else: hi_ = md
            dl = sgn * hi_
            vv[j] = W.m2q(W.axis_angle(h, math.radians(dl)) @ Rm0)
            rep['changed'].append(dict(joint=k, t=round(float(t), 4), was=round(f0, 2), now=round(f_at(dl), 2), turned_deg=round(abs(dl), 2)))
    # ---- WRISTS
    for k, (fa, hb, wb) in WRIST.items():
        key = (nid[hb], 'rotation')
        if key not in tracks: continue
        ci, tt, vv = tracks[key]
        fl = np.array(lj['wrist'][k]['flex'], float); dv = np.array(lj['wrist'][k]['dev'], float)
        r0 = W.q2m(rest[nid[hb]][1])
        for j, t in enumerate(tt):
            Rl = W.q2m(qn(vv[j])); Roff = r0.T @ Rl
            y2 = Roff @ Y; axv = np.cross(Y, y2); s = np.linalg.norm(axv); ang = math.atan2(s, float(Y @ y2))
            if s < 1e-9: continue
            sw = axv / s * ang
            dev = math.degrees(float(sw @ dv))
            if abs(dev) <= dmax: continue
            Sw = W.axis_angle(axv / s, ang); Tw = Sw.T @ Roff
            sw2 = sw - (sw @ dv) * dv + math.radians(math.copysign(dmax, dev)) * dv
            a2 = np.linalg.norm(sw2); Sw2 = W.axis_angle(sw2 / a2, a2) if a2 > 1e-9 else np.eye(3)
            Rl2 = r0 @ Sw2 @ Tw
            vv[j] = W.m2q(Rl2)
            item = dict(joint=k, t=round(float(t), 4), was=round(dev, 2), now=round(math.copysign(dmax, dev), 2))
            if wb is not None and (nid[wb], 'rotation') in tracks:
                cw, tw_, vw = tracks[(nid[wb], 'rotation')]
                jw = int(np.argmin(np.abs(tw_ - t)))
                if abs(tw_[jw] - t) < 1e-4:
                    vw[jw] = W.m2q(Rl2.T @ Rl @ W.q2m(qn(vw[jw])))       # the axe's world orientation kept
                    item['weapon_counter_rotated'] = True
            rep['changed'].append(item)
    # ---- write the changed tracks as new accessors
    for (node, path), (ci, tt, vv) in tracks.items():
        if path != 'rotation': continue
        ch = an['channels'][ci]; s = an['samplers'][ch['sampler']]
        old = L.read_accessor(js, bin_, s['output']).astype(float)
        if np.allclose(old, vv): continue
        q = np.array([qn(x) for x in vv])
        for i in range(1, len(q)):
            if np.dot(q[i], q[i - 1]) < 0: q[i] = -q[i]
        an['samplers'].append({"input": s['input'], "output": C54.add_accessor(js, bin_, q, "VEC4"), "interpolation": s.get('interpolation', 'LINEAR')})
        ch['sampler'] = len(an['samplers']) - 1
    js['buffers'][0]['byteLength'] = len(bin_) + (-len(bin_) % 4)
    R_.write_glb(dst, js, bin_)
    res = L.lint(dst)
    print("joint fix %s: %d keys changed -> %s; lint %s, %d fails" % (clip, len(rep['changed']), os.path.basename(dst), res['verdict'], len(res['fails'])))
    for c in rep['changed']: print("  ", c)
    if outj: json.dump(rep, open(outj, 'w'), indent=1)


if __name__ == "__main__":
    main()
