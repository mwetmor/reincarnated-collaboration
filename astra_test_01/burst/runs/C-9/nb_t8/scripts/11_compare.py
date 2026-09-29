# T8: choose the generator by measurement.
#
#   python3 scripts/11_compare.py <tag> [<tag> ...]
#
# Silhouette IoU against the four painted NB-1_b plates, height-normalised, at
# elevation 0 -- the plates are flat paintings and must be met in their own
# projection.
#
# ORIENTATION IS FITTED FROM PAINT, NOT FROM SILHOUETTE. A first version scored
# the assignment by silhouette IoU and put BOTH models' front plate against
# their back render: a standing human's front and back outlines are the same
# outline, so the best assignment beat the runner-up by 0.003, which is noise.
# T6 made the same point about mirror and answered it the same way -- the front
# has a face and a beard, the back has a braid, and only COLOUR can see that.
#
# The model COMPARISON survived the wrong assignment, and that is worth stating
# rather than hiding: every assignment scores within 0.003 of every other, so
# the 0.125 between the two models is not an artifact of choosing one.
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/astra_test_01/"
                   "burst/runs/C-9/fal_t6/scripts")
from maskutil import input_mask, render_mask, colour_sim

PLATES = ["front", "right", "back", "left"]
AZ = [0, 90, 180, 270]


def norm(m, size=512):
    ys, xs = np.where(m)
    if not len(ys):
        return np.zeros((size, size), bool)
    h = ys.max() - ys.min() + 1
    s = (size * 0.9) / h
    im = Image.fromarray((m * 255).astype(np.uint8))
    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
    b = np.array(im) > 127
    ys2, xs2 = np.where(b)
    out = np.zeros((size, size), bool)
    ch, cw = (ys2.min() + ys2.max()) // 2, (xs2.min() + xs2.max()) // 2
    y0, x0 = size // 2 - ch, size // 2 - cw
    ys3, xs3 = ys2 + y0, xs2 + x0
    ok = (ys3 >= 0) & (ys3 < size) & (xs3 >= 0) & (xs3 < size)
    out[ys3[ok], xs3[ok]] = True
    return out


def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 0.0


def arm_gap(m):
    """Widest background gap between an arm and the torso, in normalised px.
    A model whose arms are fused to the body has no gap; T6 measured 48 px for
    Tripo against 13 for Meshy on the knight."""
    ys, xs = np.where(m)
    y0, y1 = ys.min(), ys.max()
    best = 0
    for y in range(y0 + int(0.35 * (y1 - y0)), y0 + int(0.70 * (y1 - y0))):
        row = m[y]
        idx = np.where(row)[0]
        if len(idx) < 2:
            continue
        gaps = np.diff(idx)
        g = gaps.max() - 1 if len(gaps) else 0
        best = max(best, int(g))
    return best


def normc(m, c, size=512):
    """mask and colour through the same normalisation"""
    ys, xs = np.where(m)
    if not len(ys):
        return np.zeros((size, size), bool), np.zeros((size, size, 3), np.float32)
    sc = (size * 0.9) / (ys.max() - ys.min() + 1)
    w, h = max(1, int(m.shape[1] * sc)), max(1, int(m.shape[0] * sc))
    mm = np.array(Image.fromarray((m * 255).astype(np.uint8)).resize((w, h),
                                                                    Image.BILINEAR)) > 127
    cc = np.array(Image.fromarray(c.astype(np.uint8)).resize((w, h), Image.BILINEAR),
                  np.float32)
    ys2, xs2 = np.where(mm)
    om = np.zeros((size, size), bool); oc = np.zeros((size, size, 3), np.float32)
    y0 = size // 2 - (ys2.min() + ys2.max()) // 2
    x0 = size // 2 - (xs2.min() + xs2.max()) // 2
    ys3, xs3 = ys2 + y0, xs2 + x0
    ok = (ys3 >= 0) & (ys3 < size) & (xs3 >= 0) & (xs3 < size)
    om[ys3[ok], xs3[ok]] = True
    oc[ys3[ok], xs3[ok]] = cc[ys2[ok], xs2[ok]]
    return om, oc


plates, platec = {}, {}
for p in PLATES:
    mk, cl = input_mask("nb_b_%s.jpg" % p)
    plates[p], platec[p] = normc(mk, cl)
rep = {}
for tag in sys.argv[1:]:
    st = json.load(open("work/cmp/%s_stats.json" % tag))
    ren, renc = {}, {}
    for az in AZ:
        mk, cl = render_mask("work/cmp/%s_az%03d.png" % (tag, az))
        ren[az], renc[az] = normc(mk, cl)
    # ---- assignment by COLOUR ------------------------------------------
    cands = []
    for shift in range(4):
        for flip in (False, True):
            cs, ious, per = [], [], {}
            for i, p in enumerate(PLATES):
                rm, rc = ren[AZ[(i + shift) % 4]], renc[AZ[(i + shift) % 4]]
                if flip:
                    rm, rc = rm[:, ::-1], rc[:, ::-1]
                cs.append(colour_sim(plates[p], platec[p], rm, rc))
                v = iou(plates[p], rm)
                ious.append(v); per[p] = round(v, 4)
            cands.append((float(np.mean(cs)), float(np.mean(ious)), shift, flip, per))
    cands.sort(reverse=True)
    colour_margin = cands[0][0] - cands[1][0]
    _, m, shift, flip, per = cands[0]
    iou_all = sorted((c[1] for c in cands), reverse=True)
    allm = iou_all
    print("   assignment chosen by colour: %.4f vs runner-up %.4f (margin %.4f); "
          "silhouette could only separate them by %.4f"
          % (cands[0][0], cands[1][0], colour_margin, iou_all[0] - iou_all[1]))
    gap = arm_gap(ren[AZ[shift % 4]])
    rep[tag] = dict(iou_mean=round(m, 4),
                    iou_spread_over_assignments=round(float(iou_all[0] - iou_all[-1]), 4),
                    colour_margin=round(float(colour_margin), 4),
                    per_plate=per, shift=shift, flip=flip, arm_gap_px=gap,
                    tris=st["tris"], verts=st["verts"], islands=st["islands"],
                    island_sizes=st["island_sizes"],
                    boundary_edges=st["boundary_edges"],
                    non_manifold_edges=st["non_manifold_edges"],
                    watertight=st["watertight"], height=st["height"])
    print("%-14s IoU mean %.4f at the colour-chosen assignment  per plate %s"
          % (tag, m, per))
    print("   tris %-9d verts %-8d islands %-4d boundary %-6d non-manifold %-5d "
          "watertight %s" % (st["tris"], st["verts"], st["islands"],
                             st["boundary_edges"], st["non_manifold_edges"],
                             st["watertight"]))
    print("   arm-to-torso gap %d px (normalised)   shift %d flip %s"
          % (gap, shift, flip))
json.dump(rep, open("work/compare.json", "w"), indent=1)
