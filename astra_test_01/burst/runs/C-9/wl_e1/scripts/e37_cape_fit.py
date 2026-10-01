# CAPE FIT (stage J 3a): over the cape's TOP THIRD (by height), each cape vertex's distance to the nearest point of the BACK (the
# body + the chest piece's backplate) -- the BACK PANEL only (within 0.20 m of the hips' x), median / p90 / max -- at rest and over idle and walk keys; and the cape's top edge height
# against his shoulder line (LeftArm/RightArm joints), metres at 1.96 m.   python3 e37_cape_fit.py <body> <cape> <chest> [--json f]
import sys, os, json, numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = [x for x in sys.argv[1:] if not x.startswith('--')]; BODY, CAPE, CHEST = a[:3]
src = open(os.path.join(HERE, 'e26_cape_poke.py')).read(); exec(src[src.index('def load('):src.index('B = load(BODY)')])
m = C.model(BODY); nid = m['nid']; K = 1.96 / 1.70
B = load(BODY); CP = load(CAPE); CH = load(CHEST)
G0, _ = W.globals_(L.load_glb(BODY)[0])
def meas(G):
    CV, _ = pose(CP, G); BV, _ = pose(B, G); HV, _ = pose(CH, G)
    u = 0.01 if np.ptp(CV[:, 1]) > 10 else 1.0; CV, BV, HV = CV * u * K, BV * u * K, HV * u * K
    fl = BV[:, 1].min(); top = CV[:, 1].max(); h = top - CV[:, 1].min(); sel = CV[:, 1] > top - h / 3
    hx = G[nid['Hips']][0, 3] * u * K; back = sel & (np.abs(CV[:, 0] - hx) < 0.20)   # the BACK PANEL's top third (|x| < 0.20 m)
    d = cKDTree(np.vstack([BV[::2], HV])).query(CV[back])[0]
    sh = (G[nid['LeftArm']][:3, 3] + G[nid['RightArm']][:3, 3]) / 2 * u * K
    return dict(gap_median_m=round(float(np.median(d)), 4), gap_p90_m=round(float(np.percentile(d, 90)), 4), gap_max_m=round(float(d.max()), 4),
                top_edge_m=round(float(top - fl), 4), shoulder_line_m=round(float(sh[1] - fl), 4), top_minus_shoulder_m=round(float(top - sh[1]), 4))
rep = dict(rest=meas(G0)); print('rest', rep['rest'])
for c in ('idle', 'walk'):
    tt = sorted({float(t) for v in m['anims'][c].values() for t in v[0]})[::4]; R = [meas(C.globals_at(m, c, t)) for t in tt]
    rep[c] = {k: [min(r[k] for r in R), max(r[k] for r in R)] for k in R[0]}; print(c, rep[c])
if '--json' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
