# T8 step 1: remove the mirrored tattoo from his LEFT upper arm, in the BASE
# TEXTURE.
#
#   python3 scripts/06_fix_tattoo.py work work/base_texture_fixed.png
#
# Fixed at the source rather than masked per canvas. Masking would have to be
# repeated in every canvas of every sheet -- the base body now, each gear piece
# in D2 -- and any canvas that missed it comes back from Astra with the tattoo
# faithfully painted on. One texture, fixed once, and everything downstream is
# clean by construction.
#
# THE BAND IS FOUND AS A 3D CLUSTER, not by a coordinate threshold. Two earlier
# versions failed here and both passed their own checks:
#
#   * a z-range taken from his RIGHT arm, where the tattoo is correct, applied
#     to the LEFT. The arms hang at different A-pose angles, so the mirrored
#     band sits ~0.03 lower and the bottom of it survived.
#   * an |x| > 0.30 "arm" mask. The band wraps the upper arm and STRADDLES that
#     plane: the outer half was removed and the inner half stayed, which is
#     what a diagnostic render showed as half-red, half-blue.
#
# Both times the verification said the left arm was clean, because the
# verification was scoped to the region the fix had defined. A check that can
# only see where you already looked cannot tell you that you looked in the
# wrong place.
#
# The ink is replaced by his OWN skin, nearest in 3D. Nearest in UV is not the
# same thing on a fragmented Meshy atlas -- the first version used it and
# pulled washed-out [0.745,0.606,0.518] onto skin that should read
# [0.93,0.63,0.46], because the closest texel in the chart was across a seam.
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage, sparse
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components

W, OUT = sys.argv[1], sys.argv[2]
S = np.load(os.path.join(W, "surface.npz"))
P = S["tex_pos"].astype(np.float32); ON = S["tex_on"]
lo, hi = S["bbox"]; rsign = float(np.sign(S["right"][0]))
H = float(hi[2] - lo[2])
T = np.array(Image.open(os.path.join(W, "base_texture.png")).convert("RGB"),
             np.float32)[::-1] / 255.0
mx, mn = T.max(2), T.min(2)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
notskin = (mx < 0.70) | (sat < 0.25)
on_left = (P[..., 0] * rsign) < 0

# candidate ink anywhere on his left side in the upper-body height range
cand = ON & on_left & notskin & (P[..., 2] > lo[2] + 0.62 * H) & (P[..., 2] < lo[2] + 0.80 * H)
cy, cx = np.where(cand)
pts = P[cy, cx].astype(np.float64)
print("left-side ink candidates in the upper-body band: %d" % len(pts))
tree = cKDTree(pts)
pairs = np.array(list(tree.query_pairs(r=0.012))) if len(pts) > 1 else np.zeros((0, 2), int)
g = sparse.coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])),
                      shape=(len(pts), len(pts)))
ncomp, lab3 = connected_components(g, directed=False)
print("  %d 3D clusters" % ncomp)
keep = None
for c in range(ncomp):
    m = lab3 == c
    if m.sum() < 200:
        continue
    q = pts[m]
    ax = float(np.abs(q[:, 0]).mean())
    print("     cluster %d: %6d texels, mean |x| %.3f, z %.3f..%.3f"
          % (c, int(m.sum()), ax, q[:, 2].min(), q[:, 2].max()))
    # the ARM band is the outboard one; the chest, beard and nipples sit near
    # the midline and must survive
    if ax > 0.22 and (keep is None or m.sum() > (lab3 == keep).sum()):
        keep = c
assert keep is not None, "no outboard ink cluster found on his left arm"
sel = lab3 == keep
kill = np.zeros_like(ON)
kill[cy[sel], cx[sel]] = True
print("  band cluster %d selected: %d texels, |x| %.3f..%.3f, z %.3f..%.3f"
      % (keep, int(sel.sum()), np.abs(pts[sel][:, 0]).min(),
         np.abs(pts[sel][:, 0]).max(), pts[sel][:, 2].min(), pts[sel][:, 2].max()))

# GROW THE KILL, AND PUSH THE SOURCES CLEAR OF IT. Ink does not end at the
# last texel the classifier calls ink: there is an antialiased rim a few
# millimetres wide that is bright enough to pass as skin and dark enough to
# see. Replacing the ink but sourcing from that rim produced a patch reading
# [0.75,0.555,0.448] against skin at [0.939,0.646,0.468] -- a 0.211 delta, a
# visible grey band exactly where the tattoo had been. So the halo is killed
# too, and no source may come from within it.
GROW, CLEAR = 0.010, 0.022        # metres
band_pts = pts[sel]
btree = cKDTree(band_pts)
oy, ox = np.where(ON)
dall, _ = btree.query(P[oy, ox].astype(np.float64), k=1)
grow = np.zeros_like(ON)
grow[oy[dall < GROW], ox[dall < GROW]] = True
kill = (kill | (grow & ON & on_left)) & ON
print("  grown by %.0f mm to take the halo: %d texels" % (1000 * GROW, int(kill.sum())))
far = np.zeros_like(ON)
far[oy[dall > CLEAR], ox[dall > CLEAR]] = True

# --- replace with his own skin, nearest in 3D -------------------------------
skin = ON & ~notskin & ~kill & far
sy, sx = np.where(skin)
spts = P[sy, sx].astype(np.float64)
stree = cKDTree(spts)
ky, kx = np.where(kill)
d, idx = stree.query(P[ky, kx].astype(np.float64), k=8)
out = T.copy()
wgt = 1.0 / np.maximum(d, 1e-4)
col = (T[sy[idx], sx[idx]] * wgt[..., None]).sum(1) / wgt.sum(1)[:, None]
out[ky, kx] = col
print("  replaced %d texels from 3D-nearest skin (median distance %.4f m)"
      % (len(ky), float(np.median(d[:, 0]))))
Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)[::-1]).save(OUT)

# --- verify on the WRITTEN FILE, over a region the fix did not define -------
T2 = np.array(Image.open(OUT).convert("RGB"), np.float32)[::-1] / 255.0
mx2, mn2 = T2.max(2), T2.min(2)
sat2 = np.where(mx2 > 1e-6, (mx2 - mn2) / np.maximum(mx2, 1e-6), 0.0)
ns2 = (mx2 < 0.70) | (sat2 < 0.25)
# a GENEROUS independent region: his whole left upper arm, by 3D distance from
# the band's centroid, not by the mask that was killed
ctr = pts[sel].mean(0)
dist = np.linalg.norm(P - ctr, axis=2)
region = ON & on_left & (dist < 0.22)
ring = ON & on_left & (dist > 0.22) & (dist < 0.32) & ~notskin
print("VERIFY, on the written file, over his whole left upper arm (r<0.22 of "
      "the band centre) -- a region the fix did not define:")
print("   ink texels: %d before -> %d after" % (int((region & notskin).sum()),
                                                int((region & ns2).sum())))
print("   patch colour %s vs surrounding skin %s  (delta %.3f)"
      % (np.round(T2[kill].mean(0), 3), np.round(T2[ring].mean(0), 3),
         float(np.linalg.norm(T2[kill].mean(0) - T2[ring].mean(0)))))
bandR = ON & ~on_left & notskin & (P[..., 2] > lo[2] + 0.62 * H) & (P[..., 2] < lo[2] + 0.80 * H)
print("   his RIGHT arm ink: %d before -> %d after  (must be UNCHANGED)"
      % (int(bandR.sum()), int((bandR & ns2).sum())))
json.dump(dict(removed=int(kill.sum()),
               left_ink_before=int((region & notskin).sum()),
               left_ink_after=int((region & ns2).sum()),
               patch_rgb=[round(float(v), 4) for v in T2[kill].mean(0)],
               ring_rgb=[round(float(v), 4) for v in T2[ring].mean(0)],
               colour_delta=round(float(np.linalg.norm(
                   T2[kill].mean(0) - T2[ring].mean(0))), 4),
               right_ink_before=int(bandR.sum()),
               right_ink_after=int((bandR & ns2).sum())),
          open(os.path.join(W, "tattoo_fix.json"), "w"), indent=1)
