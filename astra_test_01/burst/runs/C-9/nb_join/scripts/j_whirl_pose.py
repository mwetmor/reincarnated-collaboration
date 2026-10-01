# WHIRLWIND, THE POSE (nb_join, the conductor's JOIN-moves dispatch, 2026-09-30): the weapon research's method --
# ONE CONSTANT local pose, turned by a uniform single-revolution yaw (j_whirl_clip.py). This authors that pose.
#
#   python3 scripts/j_whirl_pose.py <body.glb> <out.json> [--stance idle@0.5] [--seat-l seat.json] [--sense ccw]
#
# THE POSE ASKED FOR: both arms out at about chest height; both blades LEVEL with their EDGES LEADING along the
# tangential travel (cos >= 0.8 at every frame -- a constant pose under a rigid yaw makes that one number); knees
# bent in a stance; 0 penetration; counter-clockwise for a right-hander (Matt 2026-09-21).
# THE LEGS AND HIPS come from a library stance frame (default: the idle at 0.5 s, knees 41 deg, feet 0.78 m apart).
# THE TORSO is squared: the stance's chest is turned ~20 deg (a bladed fighting stance), and a whirlwind carries both
# arms symmetric about the spin, so Spine02 takes the counter-yaw that squares the shoulder line.
# THE ARMS are SOLVED (scipy): Arm, ForeArm and Hand on each side, as rotation deltas on the stance's own arm, so
#   blade (weapon +Y)          level: (Y . up)^2 -> 0
#                              radial: pointing OUT from the spin axis (vertical, through the hips)
#   edge  (weapon +Z)          along the CCW tangent t = up x r (his right hand travels FORWARD, his left BACKWARD)
#   grip                       at chest height (between Spine and the shoulders), out >= 0.50 m from the axis
#   wrist                      within 35 deg of the stance's own hand (the T12 seat keeps the haft in the fist's
#                              channel with the wrist near neutral; a whirlwind cannot ask more of it than a guard does)
#   elbow                      bent 10-80 deg, never hyperextended
#   clearance                  blade points >= 0.30 m from the spin axis and the head
# The weapon frames are the BODY's weapon bones (the seat); the pieces follow them by their own IBMs (the glTF rule).
# --seat-l: weapon_l's rest in LeftHand local (a 4x4, glTF units) for when the body's is not yet the axe's seat; the
# default is the body's own weapon_l rest. Units: glTF world metres, +Y up, he faces +Z, his right is -X.
import json, math, os, sys
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts"))
sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts"))
C = __import__('s17_loop_closure')
W = __import__('52_weapon_bones')

a = sys.argv[1:]
BODY, OUT = a[0], a[1]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
ST_CLIP, ST_T = opt('--stance', 'idle@0.5').split('@'); ST_T = float(ST_T)
SEAT_L = opt('--seat-l')
SENSE = opt('--sense', 'ccw')
# --baseball LEAD (v2, Matt 2026-09-30: "a double baseball swing"): BOTH blades point out along ONE radial -- the chest's
# forward turned LEAD deg toward the spin (his left for ccw) -- level, side by side, the edges along that radial's CCW
# tangent; the grips in front at chest height, reach measured along that radial; the two blades >= --sep m apart.
# Without it: v1's pose (each blade radial on its own side).
BASEBALL = opt('--baseball')
SEP = float(opt('--sep', '0.20'))
# --grip-side M (v3, Matt 2026-09-30: the weapon hands out toward shoulder width, not crossed in): each grip at least M m
# to its own side of his centreline (the midpoint of his shoulders)
GSIDE = float(opt('--grip-side', '0')) if opt('--grip-side') else None
GSMAX = float(opt('--grip-side-max', '0.30'))
GSW = float(opt('--side-w', '60'))
RADW = float(opt('--radial-w', '10'))
BUTT = float(opt('--butt-clear', '0'))           # m: the butt's least distance from the forearm (0 = off)
BUTTW = 2000.0
# v4 (Matt 2026-09-30, on v3: "the blades of the weapons need to be pointed more upwards like a normal prepared battle
# stance, maybe half way between how outstretched they are now and a normal battle stance"; "the tilt of the blades made
# the elbow joints bend backwards"):
PITCH = math.radians(float(opt('--blade-pitch', '0')))   # the blade's rise above horizontal (v1-v3: 0, level)
REACH_MAX = float(opt('--reach-max', '9'))         # m: the grip no further forward than this (half-extended arms)
GRIP_Y = opt('--grip-y')                           # m: the grip height target (default: chest height)
HINGE_COS = float(opt('--hinge-cos', '-2'))        # each elbow bends the way the STANCE's elbow bends: the cosine between
                                                   # the two bend directions (in the upper arm's own frame) >= this             # the weight on the blade's heading (1 - cos)                # the weight on the side band       # ... and no further out than this: in FRONT of him, not out to the side
# with --grip-side the reach is measured straight FORWARD (his +Z): held out in front, as if attacking head-on
WRIST_MAX = float(opt('--wrist-max', '35'))       # deg: the hand's turn off the stance's own hand
REACH_MIN = float(opt('--reach-min', '0.50'))     # m: the grip's distance from the spin axis
ELBOW_MAX = float(opt('--elbow-max', '80'))       # deg of elbow bend
ARM_DROP_MAX = float(opt('--arm-drop-max', '90')) # deg: the upper arm below horizontal ("arms out")
U = np.array([0.0, 1.0, 0.0])
m = C.model(BODY); nid = m['nid']; P = m['parent']


def q_of(Rm):
    return np.array(W.m2q(Rm), float)


def m_of(q):
    return W.q2m(q)


def rv(v):
    ang = float(np.linalg.norm(v))
    return np.eye(3) if ang < 1e-12 else W.axis_angle(v / ang, ang)


# the stance's locals (TRS per node), every joint the stance keys, rest for the rest (the glTF rule)
loc0 = {}
for i in range(len(m['nodes'])):
    tr, q, s = m['rest'][i]; loc0[i] = [np.array(tr, float), np.array(q, float), np.array(s, float)]
for (n_, p_), (tt, vv) in m['anims'][ST_CLIP].items():
    k = int(np.searchsorted(tt, ST_T - 1e-6)); k = min(max(k, 0), len(tt) - 1)
    if 0 < k and tt[k] > ST_T:
        u = (ST_T - tt[k - 1]) / (tt[k] - tt[k - 1]); v0, v1 = vv[k - 1], vv[k]
        if p_ == 'rotation':
            if np.dot(v0, v1) < 0: v1 = -v1
            v = (1 - u) * v0 + u * v1; v = v / np.linalg.norm(v)
        else:
            v = (1 - u) * v0 + u * v1
    else:
        v = vv[k]
    loc0[n_][{'translation': 0, 'rotation': 1, 'scale': 2}[p_]] = np.array(v, float)
if SEAT_L:
    S = np.array(json.load(open(SEAT_L))['WL'] if 'WL' in json.load(open(SEAT_L)) else json.load(open(SEAT_L))['G'])
    wl = nid['weapon_l']; loc0[wl][0] = S[:3, 3].copy(); loc0[wl][1] = q_of(S[:3, :3]); loc0[wl][2] = np.ones(3)


def globals_of(loc):
    G = {}
    def g(i):
        if i in G: return G[i]
        tr, q, s = loc[i]; M = np.eye(4); M[:3, :3] = m_of(q) * s; M[:3, 3] = tr
        G[i] = M if P.get(i) is None else g(P[i]) @ M
        return G[i]
    for i in range(len(m['nodes'])): g(i)
    return G


def unit(v):
    return v / np.linalg.norm(v)


# the hips over the axis, the chest squared
G0 = globals_of(loc0)
hips = nid['Hips']
Gp = G0[P[hips]]; Pi = np.linalg.inv(Gp)
hw = G0[hips][:3, 3].copy(); hw_axis = np.array([0.0, hw[1], 0.0])       # the hips straight over the ground origin
loc0[hips][0] = (Pi @ np.append(hw_axis, 1.0))[:3]
G0 = globals_of(loc0)
sh = G0[nid['LeftArm']][:3, 3] - G0[nid['RightArm']][:3, 3]
yaw_chest = math.degrees(math.atan2(-sh[2], sh[0]))                          # the shoulder line off his X axis (he faces +Z)
s02 = nid['Spine02']; Gs = G0[s02]; Rs = Gs[:3, :3] / np.linalg.norm(Gs[:3, :3], axis=0)
# v3 fix: the turn back is -yaw (v1/v2 turned it by +yaw and DOUBLED the twist: 20 deg -> 40 deg, shoulders left-forward)
Rfix_world = rv(U * math.radians(-yaw_chest))                                # turn the chest back about world up
Rpar = G0[P[s02]][:3, :3] / np.linalg.norm(G0[P[s02]][:3, :3], axis=0)
Rloc_new = Rpar.T @ Rfix_world @ Rs
loc0[s02][1] = q_of(Rloc_new)
G0 = globals_of(loc0)
sh2 = G0[nid['LeftArm']][:3, 3] - G0[nid['RightArm']][:3, 3]
assert abs(math.degrees(math.atan2(sh2[2], sh2[0]))) < 1.0, ('chest not squared', sh2)

SIDES = {'r': dict(chain=["RightArm", "RightForeArm", "RightHand"], weapon="weapon_r", out=np.array([-1.0, 0, 0]), blade_mid=0.42),
         'l': dict(chain=["LeftArm", "LeftForeArm", "LeftHand"], weapon="weapon_l", out=np.array([1.0, 0, 0]), blade_mid=0.30)}
VARS = [(s, b) for s in ('r', 'l') for b in SIDES[s]['chain']]
q0 = {b: loc0[nid[b]][1].copy() for _, b in VARS}
chest_y = 0.5 * (G0[nid['Spine']][1, 3] + G0[nid['RightArm']][1, 3])
head = nid['Head']


def pose_from(x):
    loc = {i: list(v) for i, v in loc0.items()}
    for k, (s, b) in enumerate(VARS):
        Rb = m_of(q0[b]) @ rv(x[3 * k: 3 * k + 3])
        loc[nid[b]] = [loc0[nid[b]][0], q_of(Rb), loc0[nid[b]][2]]
    return loc


def frames(G, s):
    Gw = G[nid[SIDES[s]['weapon']]]; R = Gw[:3, :3] / np.linalg.norm(Gw[:3, :3], axis=0)
    return Gw[:3, 3], R[:, 0], R[:, 1], R[:, 2]


def terms(x):
    G = globals_of(pose_from(x))
    hd = G[head][:3, 3]
    out = {}
    for s in ('r', 'l'):
        g, X, Y, Z = frames(G, s)
        mid = g + SIDES[s]['blade_mid'] * Y
        r = mid.copy(); r[1] = 0; r = unit(r)
        if BASEBALL is not None:
            la = math.radians(float(BASEBALL)) * (1 if SENSE == 'ccw' else -1)
            la = la + math.radians(SPLAY) * (1 if s == 'l' else -1)    # v6: each blade splayed OUT to its own side (a shallow V)
            r = np.array([math.sin(la), 0.0, math.cos(la)])
        t = np.cross(U, r) if SENSE == 'ccw' else -np.cross(U, r)
        Yh = Y.copy(); Yh[1] = 0; nyh = float(np.linalg.norm(Yh))
        ch = G[nid[SIDES[s]['chain'][1]]][:3, 3]; sh_ = G[nid[SIDES[s]['chain'][0]]][:3, 3]
        up_arm = unit(ch - sh_); fore = unit(g - ch)
        elbow = math.degrees(math.acos(max(-1, min(1, float(up_arm @ fore)))))
        wrist = math.degrees(float(np.linalg.norm(x[3 * VARS.index((s, SIDES[s]['chain'][2])): 3 * VARS.index((s, SIDES[s]['chain'][2])) + 3])))
        pts = [g + f * Y for f in (0.15, 0.3, SIDES[s]['blade_mid'], 0.6)]
        clear_axis = min(float(np.hypot(p[0], p[2])) for p in pts)
        clear_head = min(float(np.linalg.norm(p - hd)) for p in pts)
        drop = math.degrees(math.asin(max(-1, min(1, float(-up_arm @ U)))))
        out[s] = dict(level=float(Y @ U) - math.sin(PITCH), radial=float((Yh / max(nyh, 1e-9)) @ r), edge=abs(float(Z @ t)) if (DBL_R and s == 'r') else float(Z @ t), grip_y=float(g[1]),
                      reach=float(np.hypot(g[0], g[2])) if BASEBALL is None else (float(g[2]) if GSIDE is not None else float(g @ r)), elbow=elbow, wrist=wrist, arm_drop=drop,
                      clear_axis=clear_axis, clear_head=clear_head, side=float((g[0] - 0.5 * (G[nid['LeftArm']][0, 3] + G[nid['RightArm']][0, 3])) * (-1 if s == 'r' else 1)))
        # the BUTT (v3): the weapon's end below the fist, kept off his own forearm -- a wrist turned far enough to level a
        # blade drives the haft's butt back into it (v3 trial: 25 axe vertices at local y -0.10 inside the left forearm)
        hj = G[nid[SIDES[s]['chain'][2]]][:3, 3]
        def segd(pt, a_, b_):
            ab = b_ - a_; u_ = max(0.0, min(1.0, float((pt - a_) @ ab) / float(ab @ ab))); return float(np.linalg.norm(pt - (a_ + u_ * ab)))
        Ru_ = G[nid[SIDES[s]['chain'][0]]][:3, :3]; Ru_ = Ru_ / np.linalg.norm(Ru_, axis=0)
        bd = Ru_.T @ fore; ua = Ru_.T @ up_arm; bd = bd - (bd @ ua) * ua
        out[s]['_bend'] = bd / max(float(np.linalg.norm(bd)), 1e-9)
        spg = G[nid['Spine']]; sax = (spg[:3, :3] / np.linalg.norm(spg[:3, :3], axis=0)) @ np.array([-1.0 if s == 'r' else 1.0, 0, 0])
        hw_ = float((G[nid[SIDES[s]['chain'][0]]][:3, 3] - spg[:3, 3]) @ sax)
        out[s]['fist_frac'] = float((g - spg[:3, 3]) @ sax) / max(hw_, 1e-6)
        # v6 (the conductor: "each hand at about his shoulder half-width out from his centre, measured along the shoulder
        # line ... forearms roughly parallel, never converging"): the wrist and the elbow off the shoulder midpoint along
        # the LEVELLED shoulder line (scripts/j_cross_check.py's frame), each on its own side
        La_, Ra_ = G[nid['LeftArm']][:3, 3], G[nid['RightArm']][:3, 3]; md_ = (La_ + Ra_) / 2; lt_ = La_ - Ra_; lt_[1] = 0; lt_ /= np.linalg.norm(lt_)
        sg_ = 1.0 if s == 'l' else -1.0
        out[s]['wrist_side'] = float((G[nid[SIDES[s]['chain'][2]]][:3, 3] - md_) @ lt_) * sg_
        out[s]['elbow_side'] = float((G[nid[SIDES[s]['chain'][1]]][:3, 3] - md_) @ lt_) * sg_
        out[s]['half_w'] = float(np.linalg.norm((La_ - Ra_)[[0, 2]])) / 2
        if JAX:
            hb_ = nid[SIDES[s]['chain'][2]]; qh = pose_from(x)[hb_][1]
            Rl = m_of(np.array(m['rest'][hb_][1], float)).T @ m_of(qh)
            sw_ = swing_of(Rl); k_ = 'wrist_R' if s == 'r' else 'wrist_L'
            out[s]['wrist_flex'] = math.degrees(float(sw_ @ np.array(JAX['wrist'][k_]['flex'])))
            out[s]['wrist_dev'] = math.degrees(float(sw_ @ np.array(JAX['wrist'][k_]['dev'])))
            fb_ = nid[SIDES[s]['chain'][1]]; Rf = m_of(np.array(m['rest'][fb_][1], float)).T @ m_of(pose_from(x)[fb_][1])
            out[s]['forearm_twist'] = twist_of(Rl) + twist_of(Rf)
        out[s]['butt_clear'] = min(segd(g - f * Y, ch, hj) for f in (0.06, 0.10, 0.14))
        out[s]['_pts'] = pts
    sep = min(float(np.linalg.norm(p - q)) for p in out['r']['_pts'] for q in out['l']['_pts'])
    for s in out:
        del out[s]['_pts']; out[s]['sep'] = sep
        b_ = out[s].pop('_bend'); _LASTB[s] = b_; out[s]['hinge_cos'] = float(b_ @ BEND0[s]) if BEND0 else 1.0
    return out


BEND0 = None
_LASTB = {}
# --fist-frac F (v4, the JOIN hold v2's FIST row, attack_lab/t12/godot/tools/join_accept.gd): the grip's offset from the
# chest joint (Spine, the HIGHEST spine bone) along the Spine basis's own +-X, over the same side's shoulder ball joint's
FIST = float(opt('--fist-frac')) if opt('--fist-frac') else None
WSIDE = float(opt('--wrist-side')) if opt('--wrist-side') else None   # v6: the wrist at this fraction of the shoulder half-width
SPLAY = float(opt('--splay', '0'))                                   # v6: deg each blade turns OUT to its own side
# --joint-axes f (v4): scripts/j_joint_lint.py's learned wrist axes; the wrist kept inside the lint's own limits
JAX = json.load(open(opt('--joint-axes')))['learned']['axes'] if opt('--joint-axes') else None
WFLEX, WDEV = float(opt('--wrist-flex-max', '70')), float(opt('--wrist-dev-max', '32'))


def swing_of(Rl):
    y2 = Rl @ U; ax = np.cross(U, y2); sn = float(np.linalg.norm(ax))
    return np.zeros(3) if sn < 1e-9 else ax / sn * math.atan2(sn, float(U @ y2))


def twist_of(Rl):
    sw = swing_of(Rl); ang = float(np.linalg.norm(sw))
    Sw = np.eye(3) if ang < 1e-9 else W.axis_angle(sw / ang, ang)
    Tw = Sw.T @ Rl; return math.degrees(math.atan2(Tw[0, 2] - Tw[2, 0], Tw[0, 0] + Tw[2, 2]))


EDGE_MIN = float(opt('--edge-min')) if opt('--edge-min') else None   # v4: the edge only kept above this (the contract's 0.8 + margin), not maximised
TWMAX = float(opt('--forearm-twist-max', '80'))
# the SWORD is double-edged (nb_w2/scripts/w5_measure.py: "double-edged, so its sign is taken nearest his forward"): with
# --double-edged-r either edge (+-Z) may lead; the axe has one edge (+Z)
DBL_R = '--double-edged-r' in a   # the forearm's twist (forearm + hand off rest): pronation / supination


def cost(x):
    T = terms(x); c = 0.0
    for s, v in T.items():
        c += 40 * v['level'] ** 2 + RADW * (1 - v['radial']) + (30 * (1 - v['edge']) if EDGE_MIN is None else 300 * max(0.0, EDGE_MIN - v['edge']) ** 2)
        c += 20 * (v['grip_y'] - (float(GRIP_Y) if GRIP_Y else chest_y)) ** 2 + 30 * max(0.0, REACH_MIN - v['reach']) ** 2
        c += 30 * max(0.0, v['reach'] - REACH_MAX) ** 2 + 200 * max(0.0, HINGE_COS - v['hinge_cos']) ** 2
        c += 0.02 * max(0.0, v['wrist'] - WRIST_MAX) ** 2
        c += 0.02 * max(0.0, 10.0 - v['elbow']) ** 2 + 0.02 * max(0.0, v['elbow'] - ELBOW_MAX) ** 2
        c += 0.02 * max(0.0, v['arm_drop'] - ARM_DROP_MAX) ** 2
        c += 60 * max(0.0, 0.30 - v['clear_axis']) ** 2 + 60 * max(0.0, 0.30 - v['clear_head']) ** 2
        if BASEBALL is not None:
            c += 60 * max(0.0, SEP - v['sep']) ** 2
        if GSIDE is not None:
            c += GSW * max(0.0, GSIDE - v['side']) ** 2 + GSW * max(0.0, v['side'] - GSMAX) ** 2
        c += BUTTW * max(0.0, BUTT - v['butt_clear']) ** 2
        if WSIDE is not None:
            c += 600 * (v['wrist_side'] - WSIDE * v['half_w']) ** 2 + 600 * max(0.0, v['wrist_side'] - v['elbow_side'] - 0.04) ** 2 \
                 + 600 * max(0.0, v['elbow_side'] - v['wrist_side'] - 0.08) ** 2
        if FIST is not None:
            c += GSW * (v['fist_frac'] - FIST) ** 2 * 0.04
        if JAX:
            c += 0.05 * max(0.0, abs(v['wrist_flex']) - WFLEX) ** 2 + 0.05 * max(0.0, abs(v['wrist_dev']) - WDEV) ** 2
            c += 0.05 * max(0.0, abs(v['forearm_twist']) - TWMAX) ** 2
    c += 0.02 * float(np.sum(x ** 2))
    return c


x0 = np.zeros(3 * len(VARS))
terms(x0); BEND0 = dict(_LASTB)                      # the stance's own elbow bend directions

best = None
for seed in range(12):
    rng = np.random.default_rng(seed)
    xs = x0 if seed == 0 else rng.normal(0, 0.6, x0.shape)
    r_ = minimize(cost, xs, method='L-BFGS-B', options=dict(maxiter=3000))
    if best is None or r_.fun < best.fun:
        best = r_
T = terms(best.x)
loc = pose_from(best.x)
rep = dict(stance=dict(clip=ST_CLIP, t=ST_T), sense=SENSE, baseball_lead_deg=BASEBALL, sep_min_m=SEP if BASEBALL else None, grip_side_min_m=GSIDE, limits=dict(wrist_max=WRIST_MAX, reach_min=REACH_MIN, elbow_max=ELBOW_MAX, arm_drop_max=ARM_DROP_MAX), chest_counter_yaw_deg=round(yaw_chest, 2),
           shoulder_line_after_deg=round(math.degrees(math.atan2(-sh2[2], sh2[0])), 3), chest_height_m=round(float(chest_y), 4),
           seat_l=SEAT_L or "the body's own weapon_l rest", cost=round(float(best.fun), 5),
           terms={s: {k: round(v, 4) for k, v in d.items()} for s, d in T.items()},
           locals={m['nodes'][i].get('name'): dict(t=[float(v) for v in loc[i][0]], r=[float(v) for v in loc[i][1]], s=[float(v) for v in loc[i][2]])
                   for i in range(len(m['nodes'])) if m['nodes'][i].get('name') in set(nd.get('name') for nd in m['nodes'])})
rep['v4'] = dict(blade_pitch_deg=math.degrees(PITCH), reach_max_m=REACH_MAX if REACH_MAX < 9 else None, grip_y_m=float(GRIP_Y) if GRIP_Y else None,
                hinge_cos_min=HINGE_COS if HINGE_COS > -2 else None, fist_frac=FIST, joint_axes=opt('--joint-axes'),
                wrist_flex_max_deg=WFLEX if JAX else None, wrist_dev_max_deg=WDEV if JAX else None, forearm_twist_max_deg=TWMAX if JAX else None, edge_min=EDGE_MIN, double_edged_r=DBL_R, wrist_side_frac=WSIDE, splay_deg=SPLAY, argv=a[2:])
json.dump(rep, open(OUT, 'w'), indent=1)
for s, d in T.items():
    print("  %s: level %+.3f  radial %.3f  EDGE cos %.3f  grip y %.3f (chest %.3f)  reach %.2f  elbow %.0f  wrist %.0f  arm drop %.0f  clear axis %.2f head %.2f  sep %.2f  side %.2f  butt %.3f  hinge %.2f  fist %.2f  wflex %.0f wdev %.0f twist %.0f  wrist side %.3f elbow side %.3f (half %.3f)"
          % (s, d['level'], d['radial'], d['edge'], d['grip_y'], chest_y, d['reach'], d['elbow'], d['wrist'], d['arm_drop'], d['clear_axis'], d['clear_head'], d['sep'], d['side'], d['butt_clear'], d['hinge_cos'], d['fist_frac'], d.get('wrist_flex', 0), d.get('wrist_dev', 0), d.get('forearm_twist', 0), d['wrist_side'], d['elbow_side'], d['half_w']))
print("  chest squared by %.1f deg; cost %.4f -> %s" % (yaw_chest, best.fun, OUT))
