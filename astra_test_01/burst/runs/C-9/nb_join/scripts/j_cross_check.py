# NO CROSSED ARMS (the conductor, on Matt's look at war cry v4, 2026-09-30: "his arms are crossed now"): at every key of
# a clip, on the SHIPPED pose (the clip, its state's layers by Godot's mixer, un-keyed = rest -- scripts/j_joint_lint.py's
# own pose code, read from that file so the two can never disagree), each WRIST and each WEAPON TIP is measured across
# his body's SAGITTAL PLANE in the CHEST's frame: the plane through the midpoint of his shoulders (Left/RightArm) normal to
# the shoulder line, levelled. side > 0 = on its OWN side (left hand to his left, right hand to his right).
# FAIL if any wrist is on the wrong side (side < 0); the weapon tips are reported (a blade leaning across his centreline
# is what reads as "crossed" from the play camera), and FAIL too with --tips.
#
#   python3 scripts/j_cross_check.py <body.glb> [--clip shout] [--layers work/layers_moves.json] [--tips] [--json f]
#   NEGATIVE CONTROL: --neg swaps the two wrists' sides in the report's arithmetic (a crossed pose by construction): FAIL.
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]; BODY = a[0]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
CLIP = opt('--clip', 'shout'); LAY = opt('--layers', os.path.join(os.path.dirname(HERE), 'work', 'layers_moves.json'))
NEG, TIPS, OUTJ = '--neg' in a, '--tips' in a, opt('--json')   # read BEFORE the exec below: it rebinds `a` and `opt`
_src = open(os.path.join(HERE, 'j_joint_lint.py')).read()
sys.argv = [os.path.join(HERE, 'j_joint_lint.py'), BODY, '--layers', LAY]
exec(compile(_src[:_src.index('# ---- LEARN')], 'j_joint_lint.py', 'exec'))
TIP = {'weapon_r': 0.7768, 'weapon_l': 0.8089}
import math
_p = math.radians(52.95354112560294); VIEWS = []
for _b in (90, 135, 180, 225, 270, 315, 0, 45):                      # S SW W NW N NE E SE (j_whirl_check.py's views)
    _th = math.radians(90 - _b); _c, _s = math.cos(_th), math.sin(_th)
    VIEWS.append((_b, np.array([[_c, 0, _s], [0, 1, 0], [-_s, 0, _c]]).T @ np.array([0.0, -math.sin(_p), -math.cos(_p)])))
PAIRS = [('fore_L', 'fore_R'), ('fore_L', 'blade_R'), ('fore_R', 'blade_L'), ('blade_L', 'blade_R')]


def seg_x(p1, p2, q1, q2):
    d = lambda a_, b_, c_: (b_[0] - a_[0]) * (c_[1] - a_[1]) - (b_[1] - a_[1]) * (c_[0] - a_[0])
    return (d(p1, p2, q1) * d(p1, p2, q2) < 0) and (d(q1, q2, p1) * d(q1, q2, p2) < 0)
rows = []
for t in frames_of(CLIP):
    G = globals_of(pose_locals(CLIP, t))
    Lp, Rp = G[nid['LeftArm']][:3, 3], G[nid['RightArm']][:3, 3]; mid = (Lp + Rp) / 2; lat = Lp - Rp; lat[1] = 0; lat /= np.linalg.norm(lat)
    side = lambda p, sgn: float((p - mid) @ lat) * sgn
    tip = lambda w: G[nid[w]][:3, 3] + TIP[w] * (G[nid[w]][:3, :3] / np.linalg.norm(G[nid[w]][:3, :3], axis=0))[:, 1]
    P_ = lambda b: G[nid[b]][:3, 3]
    r = dict(t=round(t, 4), wrist_L=side(P_('LeftHand'), 1), wrist_R=side(P_('RightHand'), -1),
             elbow_L=side(P_('LeftForeArm'), 1), elbow_R=side(P_('RightForeArm'), -1),
             tip_axe_L=side(tip('weapon_l'), 1), tip_sword_R=side(tip('weapon_r'), -1))
    # v2 (the conductor, on whirlwind v5: "your j_cross_check PASSED this"): the SCREEN test -- the play camera
    # (orthographic, pitch 52.95 deg) at the 8 contract headings; the forearms (elbow -> wrist) and the blades (grip ->
    # tip) projected to 2D; FAIL if any pair crosses: the two forearms, a forearm and the OTHER side's blade, the two blades
    SEG = dict(fore_L=(P_('LeftForeArm'), P_('LeftHand')), fore_R=(P_('RightForeArm'), P_('RightHand')),
               blade_L=(P_('weapon_l'), tip('weapon_l')), blade_R=(P_('weapon_r'), tip('weapon_r')))
    hits = []
    for hd, v in VIEWS:
        u_ = np.cross(v, [0.0, 1, 0]); u_ /= np.linalg.norm(u_); w_ = np.cross(u_, v)
        pr = {k: [np.array([p_ @ u_, p_ @ w_]) for p_ in sg] for k, sg in SEG.items()}
        for a_, b_ in PAIRS:
            if seg_x(*pr[a_], *pr[b_]): hits.append('%s x %s @%d' % (a_, b_, hd))
    r['screen_crossings'] = hits
    if NEG: r['wrist_L'], r['wrist_R'] = -r['wrist_L'], -r['wrist_R']
    rows.append(r)
mins = {k: min(rows, key=lambda r: r[k]) for k in ('wrist_L', 'wrist_R', 'elbow_L', 'elbow_R', 'tip_axe_L', 'tip_sword_R')}
fail_s = [(r['t'], r['screen_crossings']) for r in rows if r['screen_crossings']]
fail_w = [r['t'] for r in rows if r['wrist_L'] < 0 or r['wrist_R'] < 0]
fail_t = [r['t'] for r in rows if r['tip_axe_L'] < 0 or r['tip_sword_R'] < 0]
fail_e = [r['t'] for r in rows if r['elbow_L'] < 0 or r['elbow_R'] < 0]
verdict = 'FAIL' if fail_w or fail_e or fail_s or (TIPS and fail_t) else 'PASS'
rep = dict(instrument='scripts/j_cross_check.py', body=os.path.basename(BODY), clip=CLIP, keys=len(rows), verdict=verdict,
           negative_control=NEG, wrists_crossed_at_t=fail_w, elbows_crossed_at_t=fail_e, tips_crossed_at_t=fail_t,
           screen_crossings=fail_s, screen_frames_failing=len(fail_s),
           least_side_m={k: dict(m=round(v[k], 3), t=v['t']) for k, v in mins.items()},
           definition="side of his sagittal plane (shoulder midpoint, normal = the levelled shoulder line), metres, > 0 = own side")
if OUTJ: json.dump(rep, open(OUTJ, 'w'), indent=1)
print("%s %s: %s -- least side (m): %s; wrists crossed at %s; tips crossed at %s; SCREEN crossings at %d of %d keys: %s"
      % (CLIP, 'NEG' if NEG else '', verdict, {k: (round(v[k], 3), v['t']) for k, v in mins.items()}, fail_w[:6], fail_t[:6], len(fail_s), len(rows), fail_s[:3]))
