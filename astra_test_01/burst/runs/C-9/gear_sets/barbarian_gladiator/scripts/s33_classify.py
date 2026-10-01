# R-C9-105: LABEL every vertex of the fitted armoured build (s21_features.py npz) as BODY or one of 8 champion pieces.
#   python3 s33_classify.py work/arm_feat.npz work/arm_labels.npz
# His palette is all WARM (skin, gold, tawny fur, leather), so colour is used where it is decisive and REGION + DISTANCE
# elsewhere (probe: gold g/r 0.72-0.80; skin 0.60-0.69; linen sat < 0.35 & bright; hair/red leather g/r < 0.56; the kilt
# stands 3.4 cm (median) off the thighs).
# BODY: shoes (Foot/ToeBase, or Leg below zf 0.075), hair (orange: g/r < 0.58, sat > 0.55, val > 0.45, on Head/neck or the
# braid down the back), skin (g/r 0.56-0.70, sat 0.40-0.64, val > 0.55) where no piece stands off it (dist < 1.2 cm).
# SEEDS (first rule wins), then every remaining COSTUME vertex takes the label of its nearest seed over the mesh graph:
#   0 helm        Head bone, gold, or above zf 0.955 (the bowl over the hair)
#   1 chest       gold or red leather on Spine/Spine01/Spine02/neck/Shoulders, zf 0.62-0.86, NOT on the right arm
#   2 pauldron    RightShoulder/RightArm/RightForeArm, gold or red leather, outboard of 15 cm (v2)
#   3 wrists      ForeArm/Hand bones, leather (g/r 0.45-0.68, val < 0.62), zf 0.495-0.57 (cuffs; hands below are body, v2)
#   4 girdle      Hips/Spine02, zf 0.545-0.625, gold or red leather (the riveted plates + lion plaque)
#   5 kilt        Hips/UpLeg, zf 0.33-0.585, dist > 1.2 cm, not skin, not gold (the lion pelt)
#   6 wraps       Leg/UpLeg, linen (sat < 0.36, val > 0.60), zf 0.12-0.36
#   7 greaves     Leg, gold or red strap, zf 0.06-0.31
import json, sys
import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import dijkstra, connected_components
F = np.load(sys.argv[1]); OUT = sys.argv[2]
P, VC, zf, Bn, E, dist = F["P"], F["VC"], F["zf"], F["bone"], F["edges"], F["dist"]
bones = [str(b) for b in F["bones"]]; bn = np.array(bones)[Bn]; mid = F["base_mid"]
r, g, b = VC[:, 0], VC[:, 1], VC[:, 2]
mx, mn = VC.max(1), VC.min(1)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0); gr = g / np.maximum(r, 1e-6)
isin = lambda *n: np.isin(bn, n)
gold = (gr > 0.70) & (sat > 0.42) & (mx > 0.45)
redl = (gr < 0.56) & (sat > 0.55) & (mx < 0.55)
skin = (gr > 0.56) & (gr < 0.70) & (sat > 0.40) & (sat < 0.64) & (mx > 0.55)
hair = (gr < 0.58) & (sat > 0.55) & (mx > 0.45)
linen = (sat < 0.36) & (mx > 0.60)
leather = (gr > 0.45) & (gr < 0.68) & (mx < 0.62) & (sat > 0.35)
hd = isin("Head"); hc = np.median(P[hd], axis=0)
front = P[:, 1] < hc[1]
shoes = isin("LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase") | (isin("LeftLeg", "RightLeg") & (zf < 0.075))
hairb = hair & (isin("Head", "neck") | (isin("Spine", "Spine01", "Spine02") & (np.abs(P[:, 0] - mid[0]) < 0.07) & ~front))
skinb = skin & (dist < 0.012)
# v2: the HANDS below the cuff line are his (they were filled into the wrist guards by propagation: the skin rule misses
# their shaded palms)
hands = isin("LeftHand", "RightHand") & (zf < 0.495) & ~leather
body = shoes | (hairb & ~(isin("Head") & (zf > 0.955))) | skinb | hands
lab = np.full(len(P), -2, np.int8); lab[body] = -1
c = ~body
seeds = [
    c & isin("Head") & (gold | (zf > 0.955)),
    c & (gold | redl) & isin("Spine", "Spine01", "Spine02", "neck", "LeftShoulder") & (zf > 0.62) & (zf < 0.86),
    c & (gold | redl) & isin("RightShoulder", "RightArm", "RightForeArm") & (P[:, 0] < mid[0] - 0.15),   # v2: outboard only

    c & leather & isin("LeftForeArm", "RightForeArm", "LeftHand", "RightHand") & (zf > 0.495) & (zf < 0.57),
    c & (gold | redl) & isin("Hips", "Spine02") & (zf > 0.545) & (zf < 0.625),
    c & isin("Hips", "LeftUpLeg", "RightUpLeg") & (zf > 0.33) & (zf < 0.585) & (dist > 0.012) & ~skin & ~gold,
    c & linen & isin("LeftLeg", "RightLeg", "LeftUpLeg", "RightUpLeg") & (zf > 0.12) & (zf < 0.36),
    c & (gold | redl) & isin("LeftLeg", "RightLeg") & (zf > 0.06) & (zf < 0.31),
]
NAMES = ["helm", "chest", "pauldron", "wrists", "girdle", "kilt", "wraps", "greaves"]
taken = np.zeros(len(P), bool)
for k, s in enumerate(seeds):
    s = s & ~taken; lab[s] = k; taken |= s
nseed = {NAMES[k]: int((lab == k).sum()) for k in range(8)}
# propagate over the COSTUME subgraph: each unlabeled costume vertex takes its graph-nearest seed's label
e0, e1 = E[:, 0], E[:, 1]
cm = lab != -1
sel = cm[e0] & cm[e1]
L = np.linalg.norm(P[e0[sel]] - P[e1[sel]], axis=1) + 1e-9
n = len(P)
Gm = sparse.coo_matrix((L, (e0[sel], e1[sel])), shape=(n, n)).tocsr()
unl = np.where(lab == -2)[0]
if len(unl):
    src = np.where(lab >= 0)[0]
    # multi-source: add a virtual node connected to every seed at 0 cost per label is expensive; do it per label instead
    best = np.full(n, np.inf); bl = np.full(n, -2, np.int8)
    for k in range(8):
        sk = np.where(lab == k)[0]
        if not len(sk):
            continue
        dd = dijkstra(Gm, directed=False, indices=sk, min_only=True, limit=0.25)
        upd = dd < best; best[upd] = dd[upd]; bl[upd] = k
    fill = (lab == -2) & (bl >= 0)
    lab[fill] = bl[fill]
    lab[(lab == -2)] = -1            # costume islands no seed reaches within 25 cm: left on the body (none expected)
final = {NAMES[k]: int((lab == k).sum()) for k in range(8)}; final["body"] = int((lab == -1).sum())
np.savez_compressed(OUT, lab=lab, names=np.array(NAMES))
rep = dict(classes=dict(gold=int(gold.sum()), red_leather=int(redl.sum()), skin=int(skin.sum()), hair=int(hair.sum()),
                        linen=int(linen.sum()), leather=int(leather.sum())),
           body=dict(shoes=int(shoes.sum()), hair=int(hairb.sum()), skin_on_body=int(skinb.sum())), seeds=nseed, final=final)
json.dump(rep, open(OUT.replace('.npz', '.json'), 'w'), indent=1)
print(json.dumps(rep))
