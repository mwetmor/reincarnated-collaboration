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
rows = []
for t in frames_of(CLIP):
    G = globals_of(pose_locals(CLIP, t))
    Lp, Rp = G[nid['LeftArm']][:3, 3], G[nid['RightArm']][:3, 3]; mid = (Lp + Rp) / 2; lat = Lp - Rp; lat[1] = 0; lat /= np.linalg.norm(lat)
    side = lambda p, sgn: float((p - mid) @ lat) * sgn
    tip = lambda w: G[nid[w]][:3, 3] + TIP[w] * (G[nid[w]][:3, :3] / np.linalg.norm(G[nid[w]][:3, :3], axis=0))[:, 1]
    r = dict(t=round(t, 4), wrist_L=side(G[nid['LeftHand']][:3, 3], 1), wrist_R=side(G[nid['RightHand']][:3, 3], -1),
             tip_axe_L=side(tip('weapon_l'), 1), tip_sword_R=side(tip('weapon_r'), -1))
    if NEG: r['wrist_L'], r['wrist_R'] = -r['wrist_L'], -r['wrist_R']
    rows.append(r)
mins = {k: min(rows, key=lambda r: r[k]) for k in ('wrist_L', 'wrist_R', 'tip_axe_L', 'tip_sword_R')}
fail_w = [r['t'] for r in rows if r['wrist_L'] < 0 or r['wrist_R'] < 0]
fail_t = [r['t'] for r in rows if r['tip_axe_L'] < 0 or r['tip_sword_R'] < 0]
verdict = 'FAIL' if fail_w or (TIPS and fail_t) else 'PASS'
rep = dict(instrument='scripts/j_cross_check.py', body=os.path.basename(BODY), clip=CLIP, keys=len(rows), verdict=verdict,
           negative_control=NEG, wrists_crossed_at_t=fail_w, tips_crossed_at_t=fail_t,
           least_side_m={k: dict(m=round(v[k], 3), t=v['t']) for k, v in mins.items()},
           definition="side of his sagittal plane (shoulder midpoint, normal = the levelled shoulder line), metres, > 0 = own side")
if OUTJ: json.dump(rep, open(OUTJ, 'w'), indent=1)
print("%s %s: %s -- least side (m): %s; wrists crossed at %s; tips crossed at %s"
      % (CLIP, 'NEG' if NEG else '', verdict, {k: (round(v[k], 3), v['t']) for k, v in mins.items()}, fail_w[:6], fail_t[:6]))
