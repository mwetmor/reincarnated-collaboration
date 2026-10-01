# WHIRLWIND v2, CHECKED against the contract and Matt's asks, in pure glTF (the renderer's rule: un-keyed = rest).
#
#   python3 scripts/j_whirl_check.py <body.glb> [--clip whirlwind] [--hz 120] [--plan builder.json] [--json f]
#
#   revolution    main_tip's bearing in the PORT frame (x = X, y = Z; bearing = atan2(y, x)) accumulated over one cycle
#                 (the contract: one revolution, counter-clockwise = revolution_deg < 0)
#   closure       pose(0) against pose(T), every joint, world metres
#   stance slide  each foot's TOE joint while it is the stance foot (within 3 cm of its lowest -- the scene's feet rule):
#                 its horizontal speed in the in-place frame; the pivot on the ball keeps the toe put while the heel turns
#   hips orbit    the hips' horizontal path about his ground origin (the anchor): max and mean radius
#   head          the Head's world heading against the travel bearing (his forward, world yaw 0) over the cycle
#   edges         each blade's edge (+Z) against the tip's own direction of travel, at every sample where the tip moves
#   flats         |flat normal (weapon +X) . view| at the play camera's pitch, over the 8 contract directions and every
#                 sample: an edge-on blade reads as a line
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts")); C = __import__('s17_loop_closure')
a = sys.argv[1:]; BODY = a[0]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
CLIP = opt('--clip', 'whirlwind'); HZ = float(opt('--hz', '120'))
TIP = {'weapon_r': 0.7768, 'weapon_l': 0.8089}
# --double-edged weapon_r (v4): the sword is double-edged (nb_w2/scripts/w5_measure.py), so |Z . travel| for it; the axe's
# one edge stays signed. Recorded in the report.
DBL = set((opt('--double-edged') or '').split(',')) - {''}
m = C.model(BODY); nid = m['nid']
T = float(max(v[0].max() for v in m['anims'][CLIP].values()))
ts = np.arange(0.0, T + 1e-9, 1.0 / HZ); ts[-1] = T
Gs = [C.globals_at(m, CLIP, float(t)) for t in ts]
unit = lambda v: v / np.linalg.norm(v)
def R(G, b):
    X = G[nid[b]][:3, :3]; return X / np.linalg.norm(X, axis=0)
rep = dict(clip=CLIP, T=round(T, 4), samples=len(ts))
# revolution (port bearing of main_tip)
tip = np.array([G[nid['weapon_r']][:3, 3] + TIP['weapon_r'] * R(G, 'weapon_r')[:, 1] for G in Gs])
bear = np.degrees(np.arctan2(tip[:, 2], tip[:, 0])); d = (np.diff(bear) + 180) % 360 - 180
rep['revolution_deg'] = round(float(d.sum()), 2)
G0, G1 = Gs[0], Gs[-1]
rep['closure_m'] = round(float(max(np.linalg.norm(G0[j][:3, 3] - G1[j][:3, 3]) for j in m['joints'])), 5)
# stance slide
slide = {}
# the SCENE's stance rule (t12_10_feet): at each sample the stance foot is the LOWER toe, if within 3 cm of its own lowest
toes = {sd: np.array([G[nid[sd + 'ToeBase']][:3, 3] for G in Gs]) for sd in ('Left', 'Right')}
los = {sd: toes[sd][:, 1].min() for sd in toes}
for side in ('Left', 'Right'):
    other = 'Right' if side == 'Left' else 'Left'
    toe = toes[side]; lo = los[side]
    sp = np.linalg.norm(np.diff(toe[:, [0, 2]], axis=0), axis=1) * HZ
    low = toe[:-1, 1] <= toes[other][:-1, 1]
    st = low & (toe[:-1, 1] <= lo + 0.03) & (toe[1:, 1] <= lo + 0.03)
    slide[side] = dict(stance_share=round(float(st.mean()), 3), slide_median_m_s=round(float(np.median(sp[st])), 3) if st.any() else None,
                       slide_p90_m_s=round(float(np.percentile(sp[st], 90)), 3) if st.any() else None,
                       lift_max_m=round(float(toe[:, 1].max() - lo), 3))
rep['stance_slide'] = slide
if opt('--plan'):
    # the BUILDER's own contact schedule (scripts/j_whirl3.py keys[].mode): the paddle foot between two planted keys, the
    # pivot foot always -- the toe's horizontal speed there is the slide of a foot that is meant to stand still
    rows_ = json.load(open(opt('--plan')))['keys']; KT = T / (len(rows_) - 1)
    planted = {'Right': [r['mode'] == 'planted' for r in rows_], 'Left': [True] * len(rows_)}
    pl = {}

    def wander(toe, sel):                           # the widest the toe strays from where it stood, within each contiguous plant
        runs, cur = [], [sel[0]]
        for i in sel[1:]:
            if i == cur[-1] + 1: cur.append(i)
            else: runs.append(cur); cur = [i]
        runs.append(cur)
        return max(float(np.max(np.linalg.norm(toe[r][:, [0, 2]] - toe[r][:, [0, 2]].mean(0), axis=1))) for r in runs)
    for side in ('Left', 'Right'):
        toe = toes[side]; sp = np.linalg.norm(np.diff(toe[:, [0, 2]], axis=0), axis=1) * HZ
        sel = [i for i in range(len(ts) - 1) if planted[side][min(int(ts[i] / KT), len(rows_) - 2)] and planted[side][min(int(ts[i] / KT) + 1, len(rows_) - 1)]]
        pl[side] = dict(share=round(len(sel) / (len(ts) - 1), 3), slide_median_m_s=round(float(np.median(sp[sel])), 3),
                        slide_max_m_s=round(float(np.max(sp[sel])), 3),
                        wander_mm=round(1000 * wander(toe, sel), 1))
    rep['planted_slide'] = pl
hips = np.array([G[nid['Hips']][:3, 3] for G in Gs]); rr = np.hypot(hips[:, 0], hips[:, 2])
rep['hips_orbit_m'] = dict(max=round(float(rr.max()), 3), mean=round(float(rr.mean()), 3), height=[round(float(hips[:, 1].min()), 3), round(float(hips[:, 1].max()), 3)])
# head vs the travel bearing (world +Z)
hy = np.array([math.degrees(math.atan2(*(R(G, 'Head') @ np.array([0, 0, 1.0]))[[0, 2]])) for G in Gs])
rep['head_vs_travel_deg'] = dict(within_10=round(float(np.mean(np.abs(hy) <= 10)), 3), within_30=round(float(np.mean(np.abs(hy) <= 30)), 3),
                                 worst=round(float(np.abs(hy).max()), 1), median_abs=round(float(np.median(np.abs(hy))), 1))
# edges and flats
p = math.radians(52.95354112560294)
views = []
for b in (90, 135, 180, 225, 270, 315, 0, 45):            # S SW W NW N NE E SE: character turned 90 - bearing, camera fixed (yaw 0)
    th = math.radians(90 - b); c, s = math.cos(th), math.sin(th)
    Rc = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    v = np.array([0.0, -math.sin(p), -math.cos(p)])        # the camera looks along -Z, pitched down
    views.append(Rc.T @ v)                                  # the view direction in his own frame
edge, flat = {}, {}
for w in TIP:
    tp = np.array([G[nid[w]][:3, 3] + TIP[w] * R(G, w)[:, 1] for G in Gs]); vel = np.diff(tp, axis=0)
    Z = np.array([R(G, w)[:, 2] for G in Gs[:-1]]); X = np.array([R(G, w)[:, 0] for G in Gs])
    mv = np.linalg.norm(vel, axis=1) > 1e-4
    cs = np.sum(Z[mv] * (vel[mv] / np.linalg.norm(vel[mv], axis=1)[:, None]), axis=1)
    if w in DBL: cs = np.abs(cs)                            # a double-edged blade: either edge may lead
    edge[w] = dict(cos_min=round(float(cs.min()), 3), cos_median=round(float(np.median(cs)), 3), share_ge_0_8=round(float(np.mean(cs >= 0.8)), 3))
    fl = np.abs(np.array([[x @ v for v in views] for x in X]))
    flat[w] = dict(worst=round(float(fl.min()), 3), share_ge_0_5=round(float(np.mean(fl >= 0.5)), 3))
rep['edges'] = edge; rep['flats_to_camera'] = flat; rep['double_edged'] = sorted(DBL)
print(json.dumps(rep, indent=1))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
