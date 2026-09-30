# Two-handed Meteor candidates, measured before anything is built.
#
#   python3 meteor2/scripts/m2_measure.py <export so-body.glb> <candidate.glb> [...] [--json f]
#
# Kinematics only (pure glTF evaluation, s16's evaluator): her joints from the candidate clip,
# the staff on weapon_r at its SHIPPED rest (the T12 seat), per frame:
#   off-hand   the left palm (wrist + 7 cm along the hand) to the nearest point of the SHAFT
#              (the staff's own extent, -0.871 .. +0.877 m along weapon_r +Y). <= 0.10 m and the
#              off-hand IK closes it (pass 2 proved the solver lands the palm exactly in reach).
#   two-hand   the angle between the seated shaft and the line right fist -> left palm: how far
#              the staff would have to turn in the right hand to pass through BOTH hands.
#   plant      at the slam (the hands' lowest point after their highest), the shaft's tilt from
#              vertical, the butt's height over the ground (her lowest toe over the clip), and
#              the staff's angle from SCREEN vertical at the play camera, heading 25 (three-
#              quarter front, the film's Meteor heading) -- a plant reads near-vertical on screen.
#   release    the instant of peak DOWNWARD hand speed after the highest point (D7's definition),
#              and how clean it is: the second-highest separate speed peak as a share of the first.
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))
src = open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts", "s16_clip_fidelity.py")).read()
ns = {"__file__": os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts", "s16_clip_fidelity.py")}
exec(compile(src[:src.index("JOINTS = [")], "s16", "exec"), ns)
model, globals_at, W = ns["model"], ns["globals_at"], ns["W"]
a = sys.argv[1:]
EXP = a[0]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
cands = [x for x in a[1:] if x.endswith(".glb")]
BUTT, CROWN, PALM = -0.8713, 0.8765, 0.07
me = model(EXP)
wr_t, wr_q, wr_s = me['rest'][me['nid']['weapon_r']]
WR_LOCAL = np.eye(4); WR_LOCAL[:3, :3] = W.q2m(wr_q) * wr_s; WR_LOCAL[:3, 3] = wr_t      # weapon_r under RightHand
p, y_ = math.radians(52.95354112560294), math.radians(47.0)
f = np.array([-math.sin(y_) * math.cos(p), -math.sin(p), -math.cos(y_) * math.cos(p)])
rt = np.cross(f, [0, 1, 0]); rt /= np.linalg.norm(rt); up = np.cross(rt, f)
hd = math.radians(25.0)
Ry = np.array([[math.cos(hd), 0, math.sin(hd)], [0, 1, 0], [-math.sin(hd), 0, math.cos(hd)]])
rep = {}
for c in cands:
    m = model(c)
    clip = next(iter(m['anims']))
    tt = np.unique(np.concatenate([v[0] for v in m['anims'][clip].values()]))
    n = m['nid']
    rows = []
    for t in tt:
        G = globals_at(m, clip, t)
        Wg = G[n['RightHand']] @ WR_LOCAL
        su = float(np.linalg.norm(G[n['RightHand']][:3, 0]))        # metres per local unit
        R = Wg[:3, :3] / np.linalg.norm(Wg[:3, :3], axis=0)
        s = R @ np.array([0, 1.0, 0]); grip = Wg[:3, 3]
        lh = G[n['LeftHand']]; lhR = lh[:3, :3] / np.linalg.norm(lh[:3, :3], axis=0)
        palm = lh[:3, 3] + lhR @ np.array([0, PALM, 0])
        u = float(np.clip((palm - grip) @ s, BUTT, CROWN))
        d_off = float(np.linalg.norm(palm - (grip + u * s)))
        v2 = palm - grip; dist_hands = float(np.linalg.norm(v2))
        ang2 = math.degrees(math.acos(abs(float(np.clip(v2 @ s / max(dist_hands, 1e-9), -1, 1))))) if dist_hands > 0.03 else None
        toes = min(G[n[k]][1, 3] for k in ("LeftToeBase", "RightToeBase"))
        sh = Ry @ s
        rows.append(dict(t=float(t), grip=grip, s=s, palm=palm, d_off=d_off, u=u, dist_hands=dist_hands, ang2=ang2,
                         toe=float(toes), fist_y=float(grip[1]), palm_y=float(palm[1]),
                         tilt=math.degrees(math.acos(abs(float(s[1])))), crown_up=bool(s[1] > 0),
                         screen_deg=math.degrees(math.atan2(abs(float(sh @ rt)), abs(float(sh @ up))))))
    ground = min(r['toe'] for r in rows) - 0.03            # toe joint sits ~3 cm over the sole
    hy = np.array([(r['fist_y'] + r['palm_y']) / 2 for r in rows]); T = np.array([r['t'] for r in rows])
    top = int(np.argmax(hy)); low = top + int(np.argmin(hy[top:]))
    vy = np.gradient(hy, T)
    rel = top + int(np.argmin(vy[top:low + 1])) if low > top else top
    # cleanliness: another separate downward-speed peak (>= 0.15 s away) as a share of the main one
    others = [abs(vy[k]) for k in range(len(vy)) if abs(T[k] - T[rel]) >= 0.15 and vy[k] < 0]
    clean = round(max(others) / max(abs(vy[rel]), 1e-9), 3) if others else 0.0
    sl = rows[low]
    butt_s = sl['grip'] + sl['s'] * BUTT; crown_s = sl['grip'] + sl['s'] * CROWN
    lowend = butt_s if butt_s[1] < crown_s[1] else crown_s
    near = [r for r in rows if r['d_off'] <= 0.10]
    rep[os.path.basename(c)] = dict(
        clip=clip, seconds=round(float(T[-1] - T[0]), 3), frames=len(rows),
        off_hand_within_0_10m=f"{len(near)} of {len(rows)} frames",
        off_hand_to_shaft_m=dict(min=round(min(r['d_off'] for r in rows), 3), median=round(float(np.median([r['d_off'] for r in rows])), 3),
                                 at_top=round(rows[top]['d_off'], 3), at_release=round(rows[rel]['d_off'], 3), at_slam=round(sl['d_off'], 3)),
        hands_apart_m=dict(median=round(float(np.median([r['dist_hands'] for r in rows])), 3), at_slam=round(sl['dist_hands'], 3)),
        turn_to_pass_both_hands_deg=dict(at_top=None if rows[top]['ang2'] is None else round(rows[top]['ang2'], 1),
                                         at_slam=None if sl['ang2'] is None else round(sl['ang2'], 1)),
        top_t=round(float(T[top]), 3), release_t=round(float(T[rel]), 3), slam_t=round(float(T[low]), 3),
        release_speed_m_s=round(float(-vy[rel]), 2), release_second_peak_share=clean,
        slam=dict(tilt_deg=round(sl['tilt'], 1), crown_up=sl['crown_up'], screen_deg_from_vertical_h25=round(sl['screen_deg'], 1),
                  low_end_height_m=round(float(lowend[1] - ground), 3), fist_height_m=round(float(sl['fist_y'] - ground), 3)))
    r = rep[os.path.basename(c)]
    print("%s (%s, %.2f s): off-hand <=0.10 m of the shaft in %s; min %.3f, at top %.3f, release %.3f, slam %.3f m | hands apart median %.3f m | "
          "release t=%.2f s %.2f m/s (2nd peak %.0f%%) | SLAM t=%.2f: shaft tilt %.1f deg (%s), %.1f deg off screen vertical at h25, low end %.3f m over the ground, fist %.2f m"
          % (os.path.basename(c), clip, r['seconds'], r['off_hand_within_0_10m'], r['off_hand_to_shaft_m']['min'], r['off_hand_to_shaft_m']['at_top'],
             r['off_hand_to_shaft_m']['at_release'], r['off_hand_to_shaft_m']['at_slam'], r['hands_apart_m']['median'], r['release_t'],
             r['release_speed_m_s'], 100 * r['release_second_peak_share'], r['slam_t'], r['slam']['tilt_deg'],
             "crown up" if r['slam']['crown_up'] else "CROWN DOWN", r['slam']['screen_deg_from_vertical_h25'], r['slam']['low_end_height_m'], r['slam']['fist_height_m']))
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
