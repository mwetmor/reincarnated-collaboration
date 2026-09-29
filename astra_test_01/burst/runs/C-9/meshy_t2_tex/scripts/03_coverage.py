# C-9 T5: what does each camera SET actually cover, and what does it leave bare?
#
#   blender -b -noaudio --python scripts/03_coverage.py -- <blend>
#
# The addendum asks for a second elevation so the bake covers the tops of the
# head and back. How many views that needs is a measurement, not a guess: if
# the 19.77 deg ring already covers 97% of the surface, a full second ring of
# eight costs half the paint resolution on the canvas to buy three percent.
#
# Measured per TRIANGLE, area-weighted, which is what a texture hole actually
# is -- a patch of SURFACE no camera saw. A triangle counts as seen by a camera
# when it faces it at all and the straight line to that camera is unobstructed.
# Facing alone would call the far side of the ribcage visible through the body.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index('--') + 1:]
BLEND = a[0]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
AZI = {"S": 0, "SE": 45, "E": 90, "NE": 135,
       "N": 180, "NW": 225, "W": 270, "SW": 315}
ELEVS = [19.77, 52.95]

bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
ob = next(o for o in sc.objects if o.type == 'MESH')
dg = bpy.context.evaluated_depsgraph_get()
me = ob.evaluated_get(dg).to_mesh()
me.calc_loop_triangles()
M = ob.matrix_world
V = np.array([list(M @ v.co) for v in me.vertices])
TRI = np.array([list(t.vertices) for t in me.loop_triangles])
A, B, C = V[TRI[:, 0]], V[TRI[:, 1]], V[TRI[:, 2]]
cen = (A + B + C) / 3.0
nrm = np.cross(B - A, C - A)
area = 0.5 * np.linalg.norm(nrm, axis=1)
nrm = nrm / np.maximum(np.linalg.norm(nrm, axis=1)[:, None], 1e-12)
print("mesh %s: %d verts, %d triangles, area %.4f m2"
      % (ob.name, len(V), len(TRI), area.sum()))

bvh = BVHTree.FromObject(ob, dg)
inv = M.inverted()
EPS = 0.002
seen, fac = {}, {}
for el_deg in ELEVS:
    el = math.radians(el_deg)
    for d in DIRS:
        Ar = math.radians(AZI[d])
        # direction FROM the surface TOWARDS the camera
        v = np.array([math.sin(Ar) * math.cos(el),
                      math.cos(Ar) * math.cos(el), math.sin(el)])
        face = nrm @ v
        vis = face > 0.05
        idx = np.where(vis)[0]
        for i in idx:
            o = Vector((cen[i] + nrm[i] * EPS).tolist())
            hit = bvh.ray_cast(inv @ o, inv.to_3x3() @ Vector(v.tolist()), 50.0)
            if hit[0] is not None:
                vis[i] = False
        seen[(el_deg, d)] = vis
        fac[(el_deg, d)] = np.where(vis, face, -1.0)
        print("  %4.2f deg %-3s : %5.1f%% of area" % (el_deg, d, 100 * area[vis].sum() / area.sum()))


def cover(keys):
    m = np.zeros(len(TRI), bool)
    for k in keys:
        m |= seen[k]
    return 100.0 * area[m].sum() / area.sum()


ring1 = [(19.77, d) for d in DIRS]
ring2 = [(52.95, d) for d in DIRS]
rep = dict(triangles=int(len(TRI)), total_area_m2=round(float(area.sum()), 5))
rep["ring_19.77_only"] = round(cover(ring1), 3)
rep["ring_52.95_only"] = round(cover(ring2), 3)
rep["both_rings"] = round(cover(ring1 + ring2), 3)
print("\nCOVERAGE (area-weighted, occlusion-tested)")
print("  19.77 ring alone        %6.2f%%   (unseen %.2f%%)"
      % (rep["ring_19.77_only"], 100 - rep["ring_19.77_only"]))
print("  52.95 ring alone        %6.2f%%   (unseen %.2f%%)"
      % (rep["ring_52.95_only"], 100 - rep["ring_52.95_only"]))
print("  both rings              %6.2f%%   (unseen %.2f%%)"
      % (rep["both_rings"], 100 - rep["both_rings"]))
print("  what the 2nd ring adds  %6.2f pp" % (rep["both_rings"] - rep["ring_19.77_only"]))
# and how much of that gain a SUBSET of the second ring buys
for sub in (["S"], ["S", "N"], ["SE", "SW"], ["S", "E", "N", "W"],
            ["SE", "NE", "NW", "SW"]):
    c = cover(ring1 + [(52.95, d) for d in sub])
    rep["ring1_plus_52.95_" + "_".join(sub)] = round(c, 3)
    print("  19.77 ring + 52.95 %-18s %6.2f%%  (+%4.2f pp)"
          % (",".join(sub), c, c - rep["ring_19.77_only"]))
# ---- SAMPLING QUALITY, which is the real question --------------------------
# Coverage says a camera SAW the surface. It does not say it saw it WELL. At
# 19.77 deg a horizontal back is hit at 19.77 deg of incidence: facing 0.338,
# and the projection blends by facing^4, so 0.013 -- covered, and contributing
# almost nothing. The top of the back is not missing from the 19.77 ring, it is
# badly sampled by it, and that is what a second elevation buys.
def best(keys):
    return np.max(np.stack([fac[k] for k in keys]), axis=0)


print("\nSAMPLING QUALITY (best incidence any camera in the set gets)")
rep["quality"] = {}
for nm, keys in (("19.77 ring", ring1), ("both rings", ring1 + ring2)):
    bf = best(keys)
    ok = bf > 0
    q = {}
    for thr in (0.34, 0.5, 0.7):
        frac = 100.0 * area[ok & (bf < thr)].sum() / area.sum()
        q["area_pct_below_%.2f" % thr] = round(float(frac), 3)
    q["mean_facing"] = round(float((area[ok] * bf[ok]).sum() / area[ok].sum()), 4)
    q["mean_weight_facing^4"] = round(
        float((area[ok] * bf[ok] ** 4).sum() / area[ok].sum()), 5)
    rep["quality"][nm] = q
    print("  %-11s mean facing %.3f, mean blend weight (facing^4) %.4f" % (
        nm, q["mean_facing"], q["mean_weight_facing^4"]))
    print("              area seen only at grazing angles: "
          "%5.2f%% below 0.34 (70 deg), %5.2f%% below 0.50 (60 deg), "
          "%5.2f%% below 0.70 (45 deg)" % (
              q["area_pct_below_0.34"], q["area_pct_below_0.50"],
              q["area_pct_below_0.70"]))
json.dump(rep, open(os.path.join(ROOT, "work", "coverage.json"), "w"), indent=1)
