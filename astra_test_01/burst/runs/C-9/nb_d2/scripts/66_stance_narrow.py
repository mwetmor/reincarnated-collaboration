# STANCE NARROW (R-C9-122, Matt: "both the barbarian and the dark knight have wide legged stances generally, and I think it
# would be better to take the legs in a bit"). A NAMED, MEASURED EDIT, not a solve: on each named clip the two feet are moved
# toward his midline by a stated lateral distance, constant over the clip, and the legs are re-posed to reach them --
#   * the HIP joints (UpLeg) do not move; the thigh turns in (HIP ADDUCTION, reported in degrees, median and max per clip);
#   * the knee is re-placed by two-bone geometry with the segment lengths of that frame and the knee kept in its own bend
#     plane's side (the pole: the knee's offset from the hip->ankle line), so the knee bend changes only as much as the new
#     hip->ankle distance requires (KNEE FLEXION change reported);
#   * the FOOT keeps its WORLD orientation and its height, so a planted foot stays planted and flat exactly as it was; the toe
#     is the foot's child and follows it.
# The shift is ONE constant world vector per foot per clip, along the clip's MEAN pelvis lateral (the horizontal hip-joint
# line averaged over the clip), so no foot slides: a planted foot's travel along his forward -- the foot-lock speed -- is
# unchanged to the bit.
#
#   python3 scripts/66_stance_narrow.py <in.glb> <out.glb> --frac 0.25 [--clips idle,idle_guard,walk,run] [--target 1.0]
#           [--json f]
#
# THE AMOUNT: width W (65_stance_gait.py: a standing clip's heel-to-heel lateral distance in the pelvis frame, median; a gait's
# step width -- the two support lines' spacing) against TARGET x hip width (the hip joints' distance; target 1.0 = feet at
# hip width). EXCESS = W - target x hip; the edit removes FRAC of it: each foot moves FRAC x EXCESS / 2 toward the midline.
# A clip already at or inside the target is left alone. Written on the clip's own key grid (the UpLeg/Leg/Foot channels'
# times); every other channel and clip is byte-for-byte the input's. The JOIN body gets the same rule: nothing here names
# the barbarian.
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
C54 = __import__('54_weapon_channel'); G65 = __import__('65_stance_gait'); S17 = G65.S17
LEGS = dict(L=("LeftUpLeg", "LeftLeg", "LeftFoot"), R=("RightUpLeg", "RightLeg", "RightFoot"))


def rot(M):
    R = M[:3, :3]; return R / np.linalg.norm(R, axis=0)[None, :]


def frame(a, p):
    a = a / np.linalg.norm(a); b = p - (p @ a) * a; b = b / np.linalg.norm(b)
    return np.stack([a, b, np.cross(a, b)], axis=1)


def width(m, clip, flat):
    r = G65.measure(m, clip, flat, 60.0)
    return r, (r['stance_width_m'] if r['kind'] == 'stand' else r['step_width_m'])


def ik(H, K, A, A2):
    """two-bone: the knee for an ankle at A2, the segment lengths and the knee's pole side of this frame"""
    l1, l2 = np.linalg.norm(K - H), np.linalg.norm(A - K)
    ax0 = (A - H) / np.linalg.norm(A - H)
    pole = (K - H) - ((K - H) @ ax0) * ax0
    if np.linalg.norm(pole) < 1e-6: pole = np.array([0.0, 0.0, 1.0])
    d = float(np.clip(np.linalg.norm(A2 - H), abs(l1 - l2) + 1e-6, l1 + l2 - 1e-6))
    u = (A2 - H) / np.linalg.norm(A2 - H)
    p = pole - (pole @ u) * u; p = p / np.linalg.norm(p)
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d); h = math.sqrt(max(l1 * l1 - a * a, 0.0))
    return H + u * a + p * h, pole, p


def knee_flex(H, K, A):
    u, v = (K - H) / np.linalg.norm(K - H), (A - K) / np.linalg.norm(A - K)
    return math.degrees(math.acos(max(-1.0, min(1.0, float(u @ v)))))


def main():
    a = sys.argv[1:]
    src, dst = a[0], a[1]
    frac = float(a[a.index('--frac') + 1])
    clips = a[a.index('--clips') + 1].split(',') if '--clips' in a else ['idle', 'idle_guard', 'walk', 'run']
    target = float(a[a.index('--target') + 1]) if '--target' in a else 1.0
    outj = a[a.index('--json') + 1] if '--json' in a else None
    m = S17.model(src)
    flat = G65.flat_ref(m, 'idle')
    js, b0 = L.load_glb(src); bin_ = bytearray(b0); nodes = js['nodes']
    nid = {n.get('name'): i for i, n in enumerate(nodes)}
    parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
    rep = dict(rule="66_stance_narrow.py: FRAC x (W - TARGET x hip) removed, half per foot, along the clip's mean pelvis lateral; "
                    "hips fixed, knee by two-bone geometry in its own bend plane, foot world orientation and height kept",
               frac=frac, target_x_hip=target, clips={})
    for clip in clips:
        before, Wd = width(m, clip, flat)
        hipw = before['hip_width_m']
        excess = Wd - target * hipw
        if excess <= 0:
            rep['clips'][clip] = dict(skipped="width %.3f m is inside %.2f x hip %.3f m" % (Wd, target, hipw)); continue
        delta = frac * excess / 2.0
        an = [x for x in js['animations'] if x['name'] == clip][0]
        chans = {}
        for ch in an['channels']:
            n = ch['target']['node']; p = ch['target']['path']
            if p == 'rotation' and nodes[n].get('name') in LEGS['L'] + LEGS['R']:
                chans[nodes[n]['name']] = ch
        grid = np.asarray(G65.own_keys(m, clip), float)
        # the clip's mean pelvis lateral (constant world direction)
        lats = []
        for t in grid:
            Gm = S17.globals_at(m, clip, float(t))
            hl = Gm[nid['LeftUpLeg']][:3, 3] - Gm[nid['RightUpLeg']][:3, 3]; hl[1] = 0.0; lats.append(hl / np.linalg.norm(hl))
        lat = np.mean(lats, axis=0); lat[1] = 0.0; lat = lat / np.linalg.norm(lat)
        shift = dict(L=-lat * delta, R=lat * delta)
        newq = {nm: [] for nm in LEGS['L'] + LEGS['R']}
        add, kflex, resid = {'L': [], 'R': []}, {'L': [], 'R': []}, []
        for t in grid:
            Gm = S17.globals_at(m, clip, float(t))
            for s, (up, kn, ft) in LEGS.items():
                H, K, A = (Gm[nid[j]][:3, 3] for j in (up, kn, ft))
                RU, RK, RF = rot(Gm[nid[up]]), rot(Gm[nid[kn]]), rot(Gm[nid[ft]])
                RP = rot(Gm[parent[nid[up]]])
                A2 = A + shift[s]
                K2, pole, p2 = ik(H, K, A, A2)
                D1 = frame(K2 - H, p2) @ frame(K - H, pole).T
                RU2 = D1 @ RU
                D2 = frame(A2 - K2, p2) @ frame(A - K, pole).T
                RK2 = D2 @ RK
                newq[up].append(W.m2q(RP.T @ RU2)); newq[kn].append(W.m2q(RU2.T @ RK2)); newq[ft].append(W.m2q(RK2.T @ RF))
                # the hip adduction: the thigh's turn in the pelvis frontal plane (about his forward), signed toward the midline
                fwd = np.cross(np.array([0.0, 1.0, 0.0]), lat)
                th0, th1 = K - H, K2 - H
                ang = lambda v: math.degrees(math.atan2(float(v @ lat), float(-v[1])))
                add[s].append((ang(th0) - ang(th1)) * (1 if s == 'L' else -1))
                kflex[s].append(knee_flex(H, K2, A2) - knee_flex(H, K, A))
        # write the six channels on the grid
        ti = C54.add_accessor(js, bin_, grid.reshape(-1), "SCALAR")
        for nm, q in newq.items():
            q = np.array([x / np.linalg.norm(x) for x in q])
            for i in range(1, len(q)):
                if np.dot(q[i], q[i - 1]) < 0: q[i] = -q[i]
            an['samplers'].append({"input": ti, "output": C54.add_accessor(js, bin_, q, "VEC4"), "interpolation": "LINEAR"})
            if nm in chans:
                chans[nm]['sampler'] = len(an['samplers']) - 1
            else:
                an['channels'].append({"sampler": len(an['samplers']) - 1, "target": {"node": nid[nm], "path": "rotation"}})
        rep['clips'][clip] = dict(width_before_m=round(Wd, 4), hip_width_m=hipw, width_before_x_hip=round(Wd / hipw, 3),
                                  excess_m=round(excess, 4), per_foot_shift_m=round(delta, 4), keys=len(grid),
                                  mean_pelvis_lateral=[round(float(x), 4) for x in lat],
                                  hip_adduction_deg={s: dict(median=round(float(np.median(v)), 2), max=round(float(np.max(np.abs(v))), 2)) for s, v in add.items()},
                                  knee_flexion_change_deg={s: dict(median=round(float(np.median(v)), 2), max_abs=round(float(np.max(np.abs(v))), 2)) for s, v in kflex.items()})
    js['buffers'][0]['byteLength'] = len(bin_) + (-len(bin_) % 4)
    R_.write_glb(dst, js, bin_)
    # VERIFY on the written file: the ankles where they were sent, the feet's world orientation kept, the widths after
    m2 = S17.model(dst)
    for clip, r in rep['clips'].items():
        if 'skipped' in r: continue
        grid = np.asarray(G65.own_keys(m2, clip), float)
        ep, eo = 0.0, 0.0
        lat = np.array(r['mean_pelvis_lateral'])
        for t in grid:
            g0, g1 = S17.globals_at(m, clip, float(t)), S17.globals_at(m2, clip, float(t))
            for s, (up, kn, ft) in LEGS.items():
                want = g0[nid[ft]][:3, 3] + (-lat if s == 'L' else lat) * r['per_foot_shift_m']
                ep = max(ep, float(np.linalg.norm(g1[nid[ft]][:3, 3] - want)))
                c = (np.trace(rot(g0[nid[ft]]) @ rot(g1[nid[ft]]).T) - 1) / 2
                eo = max(eo, math.degrees(math.acos(max(-1.0, min(1.0, c)))))
        after, Wa = width(m2, clip, flat)
        r.update(ankle_error_max_mm=round(ep * 1000, 3), foot_orientation_error_max_deg=round(eo, 4),
                 width_after_m=round(Wa, 4), width_after_x_hip=round(Wa / r['hip_width_m'], 3))
        if after['kind'] == 'gait' and 'roll' in after: r['roll_after'] = after['roll']
        print("%-12s width %.3f -> %.3f m (%.2f -> %.2f x hip %.3f) | each foot %.1f cm in | hip adduction L %.1f (max %.1f) R %.1f (max %.1f) deg"
              " | knee flex change L %+.1f R %+.1f deg | ankle err %.2f mm, foot orient err %.3f deg"
              % (clip, r['width_before_m'], Wa, r['width_before_x_hip'], r['width_after_x_hip'], r['hip_width_m'], 100 * r['per_foot_shift_m'],
                 r['hip_adduction_deg']['L']['median'], r['hip_adduction_deg']['L']['max'], r['hip_adduction_deg']['R']['median'],
                 r['hip_adduction_deg']['R']['max'], r['knee_flexion_change_deg']['L']['median'], r['knee_flexion_change_deg']['R']['median'],
                 r['ankle_error_max_mm'], r['foot_orientation_error_max_deg']))
    res = L.lint(dst)
    print("lint %s, %d fails %s" % (res['verdict'], len(res['fails']), res['fails'][:3]))
    rep['lint'] = dict(verdict=res['verdict'], fails=res['fails'])
    if outj: json.dump(rep, open(outj, 'w'), indent=1)


if __name__ == "__main__":
    main()
