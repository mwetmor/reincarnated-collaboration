# R-C9-98 stage 2, step 2 of the isolation: LABEL every vertex of the fitted dressed build (s21_features.py's npz) as
# BODY (kept from her shipped body, never cut) or one of five gear pieces, in numpy so the rules can be iterated cheaply.
#
#   python3 s22_classify.py work/shood_feat.npz work/shood_labels.npz [--report work/shood_labels.json]
#
# Why not 07_isolate2's distance seed: this Tripo build made the armour a single TIGHT shell -- median distance to the
# base surface is 5-19 mm in every region, inside the build-to-build noise -- so distance separates nothing. COLOUR and
# the nearest base vertex's dominant BONE do. Classes (sRGB, measured per region first):
#   red    ember-red wool (hood, cape, tabard, sash)          g/r < 0.58, sat > 0.42
#   plate  polished steel                                     sat < 0.33, val > 0.50, g/r > 0.78
#   brown  boot leather                                       g/r 0.60-0.80, sat 0.36-0.62, val < 0.56
#   skin   her face                                           g/r 0.58-0.86, sat 0.16-0.60, val > 0.42
#   dark   hair, charcoal gown, leggings, mail shadow         val < 0.30
# BODY (excluded): boot feet (Foot/ToeBase bones, or the lower Leg below zf 0.19 in boot leather), the FACE (Head bone,
# skin, in front of the head centre), and the BRAID (dark, behind the neck, within 7 cm of the midline, zf 0.50-0.90).
# PIECES, first rule wins:
#   0 hood         Head or neck bone (not body), or red above zf 0.72 (the shoulder cape)
#   1 gauntlets    ForeArm or Hand bone
#   2 breastplate  plate on Spine/Spine01/Spine02/Shoulder/Arm bones above zf 0.60 (with the spaulders)
#   3 legs         UpLeg/Leg bones below zf 0.40, not red (leggings, cuisses, knee cops, greaves)
#   4 gown         every other costume vertex (arming gown, mail sleeves and skirt, tabard, sash, belt)
# CLEANUP: components smaller than MINFRAC of their piece are relabelled to their neighbours' majority (iterated), so a
# speck of plate on the gown's tabard does not become a floating island of the breastplate.
import json, sys
import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components

F = np.load(sys.argv[1]); OUT = sys.argv[2]
REP = sys.argv[sys.argv.index("--report") + 1] if "--report" in sys.argv else OUT.replace(".npz", ".json")
P, VC, zf, B, E = F["P"], F["VC"], F["zf"], F["bone"], F["edges"]
bones = [str(b) for b in F["bones"]]
mid = F["base_mid"]
bn = np.array(bones)[B]
r, g, b = VC[:, 0], VC[:, 1], VC[:, 2]
mx, mn = VC.max(1), VC.min(1)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
gr = g / np.maximum(r, 1e-6)
red = (gr < 0.58) & (sat > 0.42)
plate = (sat < 0.33) & (mx > 0.50) & (gr > 0.78)
brown = (gr > 0.60) & (gr < 0.80) & (sat > 0.36) & (sat < 0.62) & (mx < 0.56)
skin = (gr > 0.58) & (gr < 0.86) & (sat > 0.16) & (sat < 0.60) & (mx > 0.42)
dark = mx < 0.30
isin = lambda *names: np.isin(bn, names)

# the head centre and the front direction (she faces -Y in the base's frame: gearlib/s9 "she faces -Y")
hd = isin("Head")
hc = np.median(P[hd], axis=0) if hd.sum() else mid
front = P[:, 1] < hc[1]
behind = P[:, 1] > np.median(P[isin("neck")][:, 1]) if isin("neck").sum() else ~front
ax = np.abs(P[:, 0] - mid[0])

boots = isin("LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase") | (isin("LeftLeg", "RightLeg") & (zf < 0.19) & brown)
# FACE (v2): the skin rule alone kept ~6k verts and left most of her face in the hood (brows, eyes, lips and the
# wisps of hair at her temples are not skin-coloured). So: everything on the Head bone IN FRONT that is neither the
# hood's red wool nor steel/mail grey (low saturation, not dark).
steel_grey = (sat < 0.14) & (mx > 0.30)
face = hd & front & ~red & ~steel_grey
braid = dark & behind & (ax < 0.07) & (zf > 0.50) & (zf < 0.90) & ~red
body = boots | face | braid

lab = np.full(len(P), 4, np.int8)
lab[body] = -1
rest = ~body
hood = rest & (isin("Head", "neck") | (red & (zf > 0.72)))
gaunt = rest & ~hood & isin("LeftForeArm", "RightForeArm", "LeftHand", "RightHand")
# v2: the breastplate's pointed lower front sits on the Hips bone, below zf 0.60 -- include plate on Hips down to 0.57
bp = rest & ~hood & ~gaunt & plate & ((isin("Spine", "Spine01", "Spine02", "LeftShoulder", "RightShoulder", "LeftArm", "RightArm") & (zf > 0.60))
                                      | (isin("Hips") & (zf > 0.57)))
legs = rest & ~hood & ~gaunt & ~bp & isin("LeftUpLeg", "RightUpLeg", "LeftLeg", "RightLeg") & (zf < 0.40) & ~red
lab[hood] = 0; lab[gaunt] = 1; lab[bp] = 2; lab[legs] = 3
NAMES = ["hood", "gauntlets", "breastplate", "legs", "gown"]
raw = {NAMES[k]: int((lab == k).sum()) for k in range(5)}
raw["body"] = int((lab == -1).sum())

# cleanup on the mesh graph
n = len(P)
e0, e1 = E[:, 0], E[:, 1]
MINFRAC = 0.01
for it in range(6):
    changed = 0
    for k in range(5):
        m = lab == k
        if not m.any():
            continue
        sel = m[e0] & m[e1]
        G = sparse.coo_matrix((np.ones(sel.sum()), (e0[sel], e1[sel])), shape=(n, n))
        nc, cl = connected_components(G, directed=False)
        sizes = np.bincount(cl[m], minlength=nc)
        small = m & (sizes[cl] < MINFRAC * m.sum())
        if not small.any():
            continue
        # majority label among the small set's outside neighbours, per component
        idx = np.where(small)[0]
        comp = cl[idx]
        out_nb = {}
        for a_, b_ in ((e0, e1), (e1, e0)):
            s2 = small[a_] & (lab[b_] != k)
            for c_, l_ in zip(cl[a_[s2]], lab[b_[s2]]):
                out_nb.setdefault(c_, []).append(l_)
        for c_ in np.unique(comp):
            if c_ in out_nb:
                vals, cnts = np.unique(out_nb[c_], return_counts=True)
                newl = vals[np.argmax(cnts)]
                mm = small & (cl == c_)
                lab[mm] = newl; changed += int(mm.sum())
    if not changed:
        break
final = {NAMES[k]: int((lab == k).sum()) for k in range(5)}
final["body"] = int((lab == -1).sum())
np.savez_compressed(OUT, lab=lab, names=np.array(NAMES))
rep = dict(classes=dict(red=int(red.sum()), plate=int(plate.sum()), brown=int(brown.sum()), skin=int(skin.sum()), dark=int(dark.sum())),
           body=dict(boots=int(boots.sum()), face=int(face.sum()), braid=int(braid.sum())), raw=raw, after_cleanup=final,
           cleanup_iterations=it + 1)
json.dump(rep, open(REP, "w"), indent=1)
print(json.dumps(rep, indent=1))
