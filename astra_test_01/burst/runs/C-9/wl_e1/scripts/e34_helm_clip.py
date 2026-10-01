# Helm vs pauldrons/chest: helm vertices INSIDE a pauldron or the chest (nearest vertex within 1 cm and behind its normal), and the
# minimum helm-to-pauldron distance, per key of a clip.  python3 e34_helm_clip.py <body.glb> <geardir> <clips> [--json f]
import sys, os, json, numpy as np
from scipy.spatial import cKDTree
sys.argv = [sys.argv[0], sys.argv[1], 'export/wl_mace.glb', sys.argv[2]] + sys.argv[3:]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
src = open(os.path.join(HERE, 'e25_carry_measure.py')).read().split("B = load(BODY)")[0]
exec(src)
CL = sys.argv[4].split(','); B = load(BODY); HELM = load(os.path.join(GD, 'wl_helm.glb'))
OTH = {p: load(os.path.join(GD, 'wl_%s.glb' % p)) for p in ('pauldrons', 'chest')}
rep = {}
for c in CL:
    tt = sorted({float(t) for v in m['anims'][c].values() for t in v[0]}); rows = []
    for t in tt[::2]:
        G = C.globals_at(m, c, t); HV, HN = pose(HELM, G, 2); r = dict(t=t)
        for p, P in OTH.items():
            OV, ON = pose(P, G, 2); d, i = cKDTree(OV).query(HV)
            r[p + '_inside'] = float(((d < 0.01) & (((HV - OV[i]) * ON[i]).sum(1) < 0)).mean()); r[p + '_min_m'] = float(d.min())
        rows.append(r)
    rep[c] = {k: [round(min(x[k] for x in rows), 4), round(max(x[k] for x in rows), 4)] for k in rows[0] if k != 't'}
    print(c, rep[c])
if '--json' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
