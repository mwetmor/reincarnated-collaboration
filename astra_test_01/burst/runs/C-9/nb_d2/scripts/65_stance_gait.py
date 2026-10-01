# STANCE WIDTH AND FOOT ROLL (R-C9-122, Matt: "both the barbarian and the dark knight have wide legged stances generally, and I
# think it would be better to take the legs in a bit so they don't walk flat-footed"). Read from the glTF (s17's evaluator, no
# importer in the loop), in HIS frame: forward +Z, lateral X, up Y.
#
#   python3 scripts/65_stance_gait.py <body.glb> [idle_guard,idle,walk,run,...] [--hz 60] [--json f]
#
# HIP WIDTH   the distance between the two hip joints (LeftUpLeg / RightUpLeg), the clip's median (0.272 m on the barbarian).
# STANCE / STEP WIDTH  the heels' lateral distance as a fraction of hip width. The HEEL is the foot joint (the ankle) carried
#             down to the ground plane -- its lateral position; the ankle sits over the heel on this rig. A standing clip: the
#             median over the clip of |x_L - x_R|. A gait: each foot's lateral position averaged over its own STANCE samples,
#             then |mean_L - mean_R| (the step width as gait analysis states it: the lateral spacing of the two support lines).
#             1.00 = feet at hip width.
# CONTACT     the scene's rule (57_footlock.py): a foot is on the ground while its TOE is within 3 cm of that toe's lowest OR its
#             ANKLE is within 3 cm of that ankle's lowest (the heel-strike end of the step is ankle-low with the toe still up).
# FOOT PITCH  the angle of the ankle->toe vector above the horizontal. Two references: GROUND-FLAT = that foot's pitch standing
#             (the median over the unarmed idle, or --flat-clip); PLANTED = the clip's own median pitch over that foot's contact
#             samples (the attitude the foot holds while it bears weight). + = toe up (a heel strike), - = heel up (a toe-off).
# PER STEP    each contiguous contact interval: HEEL-STRIKE = the largest toe-up pitch off PLANTED in its first 25%; TOE-OFF =
#             the largest heel-up pitch off PLANTED in its last 25%; RIGID % = the share of the interval within +-5 deg of
#             PLANTED (the foot held as one plank -- what reads as flat-footed); PLANTED OFF GROUND-FLAT = the heel's hold while
#             it bears weight (- = heel held up).
#             A visible heel-to-toe roll, as stated here: heel strike >= 10 deg AND toe-off >= 15 deg AND rigid <= 50%.
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "so_d7", "scripts"))
S17 = __import__('s17_loop_closure')
CONTACT_M = 0.03
FLAT_DEG = 5.0
SIDES = dict(L=("LeftUpLeg", "LeftFoot", "LeftToeBase"), R=("RightUpLeg", "RightFoot", "RightToeBase"))
GAITS = ('walk', 'run', 'walk_armed', 'run_armed', 'strafe_L_armed', 'strafe_R_armed')


def own_keys(m, clip):
    by = {}
    for (tt, vv) in m['anims'][clip].values():
        if len(tt) > 2: by.setdefault(len(tt), []).append(tt)
    return max(by.items(), key=lambda kv: (len(kv[1]), kv[0]))[1][0] if by else [0.0]


def sample(m, clip, hz):
    ks = np.asarray(own_keys(m, clip), float); T = float(ks[-1])
    ts = np.arange(0.0, T + 1e-9, 1.0 / hz) if T > 0 else np.array([0.0])
    P = {s: {j: [] for j in v} for s, v in SIDES.items()}
    for t in ts:
        G = S17.globals_at(m, clip, float(t))
        for s, v in SIDES.items():
            for j in v: P[s][j].append(G[m['nid'][j]][:3, 3].copy())
    return ts, {s: {j: np.array(x) for j, x in d.items()} for s, d in P.items()}


def pitch(P, s):
    _, ank, toe = SIDES[s]; d = P[s][toe] - P[s][ank]
    return np.degrees(np.arctan2(d[:, 1], np.hypot(d[:, 0], d[:, 2])))


def contact(P, s):
    _, ank, toe = SIDES[s]
    a = P[s][ank][:, 1]; t = P[s][toe][:, 1]
    return (t <= t.min() + CONTACT_M) | (a <= a.min() + CONTACT_M)


def runs(mask):
    out, i, n = [], 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j + 1 < n and mask[j + 1]: j += 1
            out.append((i, j)); i = j + 1
        else: i += 1
    # a loop: an interval touching both ends is one step
    if len(out) > 1 and out[0][0] == 0 and out[-1][1] == n - 1:
        out = [(out[-1][0], out[0][1] + n)] + out[1:-1]
    return out


def frame(P):
    hl = P['L']['LeftUpLeg'] - P['R']['RightUpLeg']
    lat = hl * np.array([1.0, 0.0, 1.0]); lat = lat / np.linalg.norm(lat, axis=1)[:, None]
    fwd = np.cross(np.array([0.0, 1.0, 0.0]), lat)
    return np.linalg.norm(hl, axis=1), lat, fwd


def measure(m, clip, flat, hz=60.0):
    ts, P = sample(m, clip, hz)
    hw, lat, fwd = frame(P); hipw = float(np.median(hw))
    rec = dict(clip=clip, T_s=round(float(ts[-1]), 4), samples=len(ts), hip_width_m=round(hipw, 4))
    mid = 0.5 * (P['L']['LeftUpLeg'] + P['R']['RightUpLeg'])
    xl = np.einsum('ij,ij->i', P['L']['LeftFoot'] - mid, lat); xr = np.einsum('ij,ij->i', P['R']['RightFoot'] - mid, lat)
    zl = np.einsum('ij,ij->i', P['L']['LeftFoot'] - mid, fwd); zr = np.einsum('ij,ij->i', P['R']['RightFoot'] - mid, fwd)
    if clip in GAITS:
        cl, cr = contact(P, 'L'), contact(P, 'R')
        w = abs(float(xl[cl].mean()) - float(xr[cr].mean())) if cl.any() and cr.any() else float('nan')
        rec.update(kind='gait', step_width_m=round(w, 4), step_width_frac=round(w / hipw, 3),
                   support_lines_m=dict(L=round(float(xl[cl].mean()), 4), R=round(float(xr[cr].mean()), 4)))
        steps = []; planted = {}
        for s, c in (('L', cl), ('R', cr)):
            praw = pitch(P, s); n = len(praw)
            pl = float(np.median(praw[c])); planted[s] = round(pl - flat[s], 1)
            p = praw - pl
            for (i, j) in runs(c):
                idx = np.arange(i, j + 1) % n; L = len(idx)
                if L < 3: continue
                q = max(1, int(math.ceil(0.25 * L)))
                pp = p[idx]
                steps.append(dict(side=s, t0=round(float(ts[idx[0]]), 3), dur_s=round(L / hz, 3),
                                  heel_strike_deg=round(float(pp[:q].max()), 1), toe_off_deg=round(float(-pp[-q:].min()), 1),
                                  rigid_pct=round(100.0 * float((np.abs(pp) <= FLAT_DEG).mean()), 1),
                                  ground_flat_pct=round(100.0 * float((np.abs(praw[idx] - flat[s]) <= FLAT_DEG).mean()), 1)))
        rec['steps'] = steps; rec['planted_off_ground_flat_deg'] = planted
        if steps:
            md = lambda k: round(float(np.median([x[k] for x in steps])), 1)
            rec['roll'] = dict(heel_strike_med=md('heel_strike_deg'), toe_off_med=md('toe_off_deg'), rigid_pct_med=md('rigid_pct'),
                               ground_flat_pct_med=md('ground_flat_pct'))
            r = rec['roll']; r['rolls'] = bool(r['heel_strike_med'] >= 10 and r['toe_off_med'] >= 15 and r['rigid_pct_med'] <= 50)
    else:
        d = np.abs(xl - xr)
        rec.update(kind='stand', stance_width_m=round(float(np.median(d)), 4), stance_width_frac=round(float(np.median(d)) / hipw, 3),
                   stance_width_range_frac=[round(float(d.min()) / hipw, 3), round(float(d.max()) / hipw, 3)],
                   stagger_m=round(float(np.median(zl - zr)), 4),
                   pitch_off_flat_deg=dict(L=round(float(np.median(pitch(P, 'L') - flat['L'])), 1), R=round(float(np.median(pitch(P, 'R') - flat['R'])), 1)),
                   toe_heights_m=dict(L=round(float(np.median(P['L']['LeftToeBase'][:, 1])), 4), R=round(float(np.median(P['R']['RightToeBase'][:, 1])), 4)))
    return rec


def flat_ref(m, clip, hz=30.0):
    ts, P = sample(m, clip, hz)
    return {s: float(np.median(pitch(P, s))) for s in SIDES}


if __name__ == '__main__':
    a = sys.argv[1:]
    body = a[0]
    clips = a[1].split(',') if len(a) > 1 and not a[1].startswith('--') else ['idle', 'idle_guard', 'walk', 'run']
    hz = float(a[a.index('--hz') + 1]) if '--hz' in a else 60.0
    fc = a[a.index('--flat-clip') + 1] if '--flat-clip' in a else 'idle'
    m = S17.model(body)
    flat = flat_ref(m, fc)
    out = dict(body=body, flat_clip=fc, flat_pitch_deg={k: round(v, 2) for k, v in flat.items()}, clips={})
    for c in clips:
        r = measure(m, c, flat, hz); out['clips'][c] = r
        if r['kind'] == 'stand':
            print("%-16s STAND hip %.3f m | heels %.3f m = %.2f x hip (%.2f..%.2f) | stagger %+.3f m | feet off flat L %+.1f R %+.1f deg"
                  % (c, r['hip_width_m'], r['stance_width_m'], r['stance_width_frac'], *r['stance_width_range_frac'], r['stagger_m'],
                     r['pitch_off_flat_deg']['L'], r['pitch_off_flat_deg']['R']))
        else:
            ro = r.get('roll', {})
            print("%-16s GAIT  hip %.3f m | step width %.3f m = %.2f x hip | %d steps: heel strike %.1f, toe-off %.1f deg, rigid %.0f%%, ground-flat %.0f%% | planted heel L %+.1f R %+.1f -> %s"
                  % (c, r['hip_width_m'], r['step_width_m'], r['step_width_frac'], len(r['steps']), ro.get('heel_strike_med', float('nan')),
                     ro.get('toe_off_med', float('nan')), ro.get('rigid_pct_med', float('nan')), ro.get('ground_flat_pct_med', float('nan')),
                     r['planted_off_ground_flat_deg']['L'], r['planted_off_ground_flat_deg']['R'], 'ROLLS' if ro.get('rolls') else 'FLAT-FOOTED'))
    if '--json' in a: json.dump(out, open(a[a.index('--json') + 1], 'w'), indent=1)
