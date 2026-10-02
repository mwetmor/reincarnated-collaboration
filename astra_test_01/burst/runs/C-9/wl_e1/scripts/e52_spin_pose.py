# R-C9-132/133 EXTENDED-ARM SPIN POSE -- the reference (reincarnated-godot wwcr_whirlwind.gd, 'ww-native-eor1'): the weapon held
# OUT, grip radius R_GRIP_SWEEP 0.8449 m (= shoulder offset 0.2141 + arm 0.6308: the arm straight out) and the sweep plane at
# SWEEP_Y 1.20 m, for a 1.85 m character; scaled here by height. ONE frame of the character's stance, then NAMED EDITS per arm,
# each a single computed rotation (no iteration, no solver):
#   1. ELBOW OPENING  the forearm turned about the elbow's own hinge (the arm-plane normal) so shoulder->fist = |target - shoulder|
#   2. SHOULDER AIM   the upper arm turned by the shortest arc taking shoulder->fist onto shoulder->target (flexion + abduction)
#   3. WRIST (opt.)   --blade-out: the hand turned so its WEAPON bone's +Y lies along the outward radial (horizontal), clamped
#                     to the joint-limit envelope later by 63_joint_fix
# Each target is a FIST point: radius r (m) at azimuth az (deg, 0 = his forward, + toward his RIGHT), height h (m). The pose is
# written as a 2-key clip `spin_pose`; e48 spins it rigidly.
#   python3 e52_spin_pose.py <body.glb> <out.glb> --base <clip>@<t> --R r,az,h --L r,az,h [--H 1.96] [--elbow-max deg]
#                            [--blade-out [--roll] [--wrist-max deg] [--reaim]] [--json f]
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
CH = __import__('54_weapon_channel')
a = sys.argv[1:]; IN, OUT = a[0], a[1]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
bc, bt = opt('--base').split('@'); bt = float(bt); HT = float(opt('--H', '1.96')); BLADE = '--blade-out' in a
ROLL = '--roll' in a; REAIM = '--reaim' in a; WMAX = float(opt('--wrist-max', '180')); TRAIL = set((opt('--roll-trail') or '').split(','))   # e.g. Left: that arm takes the root whose blade TRAILS
rot = lambda M: M[:3, :3] / np.cbrt(np.linalg.det(M[:3, :3]))
js, b0 = L.load_glb(IN); bn = bytearray(b0); m = C.model(IN); nid = m['nid']; nodes = m['nodes']
root = [i for i in range(len(nodes)) if m['parent'].get(i) is None][0]
G = C.globals_at(m, bc, bt); RootI = np.linalg.inv(G[root]); Gm = {i: RootI @ G[i] for i in G}   # model space (rig units)
Vb = None
jb, bb = L.load_glb(IN); G0, _ = W.globals_(jb); mn = next(i for i, nd in enumerate(jb['nodes']) if 'skin' in nd and 'mesh' in nd)
V0 = W.skin_rest(jb, bb, mn, G0); Hrig = float(np.ptp((V0 @ np.linalg.inv(G0[root])[:3, :3].T)[:, 1]))  # rig-unit height
K = HT / Hrig                                                                           # metres per rig unit
hips = Gm[nid['Hips']][:3, 3]
cfist = {s: W.hand_points(jb, bb, s + 'Hand', 0.6)[0].mean(0) for s in ('Right', 'Left')}
def fist_pt(Gx, s): return (Gx[nid[s + 'Hand']] @ np.r_[cfist[s], 1.0])[:3]
def target(spec):
    r, az, h = [float(x) for x in spec.split(',')]; az = math.radians(az)
    d = np.array([-math.sin(az), 0.0, math.cos(az)])                                     # his right is -X, forward +Z
    p = np.array([hips[0], 0.0, hips[2]]) + d * (r / K); p[1] = (h / K) + float(V0[:, 1].min() * 0 + 0)  # height above the floor
    floor = float((V0 @ np.linalg.inv(G0[root])[:3, :3].T)[:, 1].min()); p[1] = floor + h / K
    return p, d
def axis_angle(ax, ang): return W.axis_angle(ax / np.linalg.norm(ax), ang)
local = {i: (np.array(m['rest'][i][0]), np.array(m['rest'][i][1])) for i in range(len(nodes))}
for (n_, p_) in m['anims'][bc]:
    pass
def node_local_rot(i):
    k = (i, 'rotation')
    if k in m['anims'][bc]:
        tt, vv = m['anims'][bc][k]; j = int(np.argmin(np.abs(tt - bt))); return np.array(vv[j], float)
    return np.array(m['rest'][i][1], float)
newq = {}; rep = dict(base='%s@%.4f' % (bc, bt), height_m=HT, rig_unit_m=K, arms={})
def recompute():
    # world (model) rotations with the edits so far: rebuild Gm for the arm chain from the edited locals
    pass
for side, spec in (('Right', opt('--R')), ('Left', opt('--L'))):
    T, dirv = target(spec)
    S = Gm[nid[side + 'Arm']][:3, 3]; E = Gm[nid[side + 'ForeArm']][:3, 3]; Wr = Gm[nid[side + 'Hand']][:3, 3]; F = fist_pt(Gm, side)
    a_ = np.linalg.norm(E - S); b_ = np.linalg.norm(F - E); d_ = min(np.linalg.norm(T - S), a_ + b_ - 1e-4)
    # 1. ELBOW: interior angle at the elbow for the wanted reach
    g0 = math.acos(np.clip(np.dot(S - E, F - E) / (a_ * b_), -1, 1)); g1 = math.acos(np.clip((a_ * a_ + b_ * b_ - d_ * d_) / (2 * a_ * b_), -1, 1))
    g1 = min(g1, math.radians(float(opt('--elbow-max', '180'))))                        # cap: the shoulder-elbow-FIST line is not the hinge's own straight (lint reads -11 at 180)
    hinge = np.cross(E - S, F - E); hinge = hinge / max(np.linalg.norm(hinge), 1e-9)
    Rel = axis_angle(hinge, -(g1 - g0))                                                   # opening the elbow by (g1 - g0)
    # apply to the forearm's WORLD rotation (and carry the hand + weapons rigidly)
    for j in (side + 'ForeArm',):
        Gm[nid[j]] = np.block([[Rel @ Gm[nid[j]][:3, :3], (E + Rel @ (Gm[nid[j]][:3, 3] - E))[:, None]], [np.zeros((1, 3)), np.ones((1, 1))]])
    def carry(jname, R, pivot):
        idx = nid[jname]; stack = [c for c in nodes[idx].get('children', [])]
        while stack:
            c = stack.pop(); Mc = Gm[c]
            Gm[c] = np.block([[R @ Mc[:3, :3], (pivot + R @ (Mc[:3, 3] - pivot))[:, None]], [np.zeros((1, 3)), np.ones((1, 1))]]); stack += nodes[c].get('children', [])
    carry(side + 'ForeArm', Rel, E)
    F1 = fist_pt(Gm, side)
    # 2. SHOULDER AIM: shortest arc taking shoulder->fist onto shoulder->target
    Rsh = W.arc(F1 - S, T - S)
    Gm[nid[side + 'Arm']] = np.block([[Rsh @ Gm[nid[side + 'Arm']][:3, :3], S[:, None]], [np.zeros((1, 3)), np.ones((1, 1))]])
    carry(side + 'Arm', Rsh, S)
    F2 = fist_pt(Gm, side)
    rec = dict(target_m=(np.round(T * K, 3)).tolist(), elbow_open_deg=round(math.degrees(g1 - g0), 1), shoulder_turn_deg=round(math.degrees(math.acos(np.clip((np.trace(Rsh) - 1) / 2, -1, 1))), 1),
               reach_limited=bool(np.linalg.norm(T - S) > a_ + b_ - 1e-4))
    # 3. WRIST: weapon bone +Y onto the outward radial (horizontal)
    wb = 'weapon_r' if side == 'Right' else 'weapon_l'
    if BLADE and wb in nid:
        if ROLL:
            # 3a. ARM ROLL (R-C9-133): the whole straight-ish arm turned about its own shoulder->fist axis -- the fist does not
            # move -- by the closed-form angle that lays the blade HORIZONTAL (y-component zero), choosing the root whose blade
            # leads the CCW spin (his right arm sweeps toward his front when spinning CCW from above).
            Fa = fist_pt(Gm, side); u = (Fa - S) / np.linalg.norm(Fa - S); y0 = rot(Gm[nid[wb]])[:, 1]
            par_ = u * (y0 @ u); perp = y0 - par_; e1 = perp; e2 = np.cross(u, perp)      # y(th) = par_ + cos th e1 + sin th e2
            A_, B_, C_ = e1[1], e2[1], par_[1]; Rm = math.hypot(A_, B_)
            tang = np.cross([0, 1.0, 0], dirv)                                                # CCW-from-above direction of travel
            best = None
            if Rm > 1e-9 and abs(C_) <= Rm:
                ph = math.atan2(B_, A_); base_ = math.acos(-C_ / Rm)
                for th in (ph + base_, ph - base_):
                    yv = par_ + math.cos(th) * e1 + math.sin(th) * e2; sc = (yv @ tang) * (-1 if side in TRAIL else 1)
                    if best is None or sc > best[1]: best = (th, sc)
            if best is not None:
                Rr = axis_angle(u, best[0])
                for j in (side + 'Arm',):
                    Gm[nid[j]] = np.block([[Rr @ Gm[nid[j]][:3, :3], S[:, None]], [np.zeros((1, 3)), np.ones((1, 1))]])
                carry(side + 'Arm', Rr, S); rec['arm_roll_deg'] = round(math.degrees((best[0] + math.pi) % (2 * math.pi) - math.pi), 1)
        y = rot(Gm[nid[wb]])[:, 1]; Rw = W.arc(y, dirv); ang = math.acos(np.clip((np.trace(Rw) - 1) / 2, -1, 1))
        if ang > math.radians(WMAX):                                                       # 3b. clamp the wrist's share
            ax_ = np.cross(y, dirv); Rw = axis_angle(ax_, math.radians(WMAX))
        Hn = side + 'Hand'; P = Gm[nid[Hn]][:3, 3]
        Gm[nid[Hn]] = np.block([[Rw @ Gm[nid[Hn]][:3, :3], P[:, None]], [np.zeros((1, 3)), np.ones((1, 1))]]); carry(Hn, Rw, P)
        rec['wrist_turn_deg'] = round(math.degrees(min(ang, math.radians(WMAX))), 1)
        if REAIM:
            # 3c. SHOULDER RE-AIM: one more shortest arc, the fist (moved by the wrist turn) back onto the target bearing
            F4 = fist_pt(Gm, side); Rs2 = W.arc(F4 - S, T - S)
            Gm[nid[side + 'Arm']] = np.block([[Rs2 @ Gm[nid[side + 'Arm']][:3, :3], S[:, None]], [np.zeros((1, 3)), np.ones((1, 1))]])
            carry(side + 'Arm', Rs2, S); rec['reaim_deg'] = round(math.degrees(math.acos(np.clip((np.trace(Rs2) - 1) / 2, -1, 1))), 1)
        yb = rot(Gm[nid[wb]])[:, 1]; yb = yb / np.linalg.norm(yb)
        rec['blade_vs_radial_deg'] = round(math.degrees(math.acos(np.clip(yb @ dirv, -1, 1))), 1); rec['blade_pitch_deg'] = round(math.degrees(math.asin(np.clip(yb[1], -1, 1))), 1)
    F3 = fist_pt(Gm, side); rad = np.linalg.norm((F3 - hips)[[0, 2]]) * K
    rec.update(fist_radius_m=round(float(rad), 4), fist_height_m=round(float((F3[1] - (V0 @ np.linalg.inv(G0[root])[:3, :3].T)[:, 1].min()) * K), 4))
    rep['arms'][side] = rec
# back to LOCAL rotations for the edited chains
edited = [s + j for s in ('Right', 'Left') for j in ('Arm', 'ForeArm', 'Hand')] + [w for w in ('weapon_r', 'weapon_l') if w in nid]
q = {}
for jn in edited:
    i = nid[jn]; p = m['parent'][i]; q[jn] = W.m2q(rot(Gm[p]).T @ rot(Gm[i]))
# the clip: every joint at the base frame, the edited ones at q, two keys (0 and 1/30)
an_src = next(x for x in js['animations'] if x['name'] == bc)
times = np.array([0.0, 1 / 30.0]); tin = CH.add_accessor(js, bn, times, "SCALAR"); ch, sm = [], []
skin_joints = {js['nodes'][j]['name'] for j in js['skins'][0]['joints']}
for jn in sorted(skin_joints):
    i = nid[jn]; qq = q.get(jn, node_local_rot(i)); qs = np.tile(qq, (2, 1))
    sm.append({"input": tin, "output": CH.add_accessor(js, bn, qs, "VEC4"), "interpolation": "LINEAR"}); ch.append({"sampler": len(sm) - 1, "target": {"node": i, "path": "rotation"}})
hk = (nid['Hips'], 'translation'); htr = m['anims'][bc][hk][1][int(np.argmin(np.abs(m['anims'][bc][hk][0] - bt)))] if hk in m['anims'][bc] else m['rest'][nid['Hips']][0]
sm.append({"input": tin, "output": CH.add_accessor(js, bn, np.tile(htr, (2, 1)), "VEC3"), "interpolation": "LINEAR"}); ch.append({"sampler": len(sm) - 1, "target": {"node": nid['Hips'], "path": "translation"}})
js['animations'] = [x for x in js['animations'] if x['name'] != 'spin_pose'] + [{"name": "spin_pose", "channels": ch, "samplers": sm}]
js['buffers'][0]['byteLength'] = len(bn) + (-len(bn) % 4); R_.write_glb(OUT, js, bn)
print(json.dumps(rep, indent=1))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
