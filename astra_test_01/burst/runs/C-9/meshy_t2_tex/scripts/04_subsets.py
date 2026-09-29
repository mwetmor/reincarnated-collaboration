# How much of the second elevation's benefit does a SUBSET of it buy, and how
# big does the FACE actually land on a whole-creature sheet? Both decide the
# layout, and both are measurements rather than preferences.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
AZI = {"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225, "W": 270, "SW": 315}
bpy.ops.wm.open_mainfile(filepath=a[0])
sc = bpy.context.scene
ob = next(o for o in sc.objects if o.type == 'MESH')
dg = bpy.context.evaluated_depsgraph_get()
me = ob.evaluated_get(dg).to_mesh(); me.calc_loop_triangles()
M = ob.matrix_world
V = np.array([list(M @ v.co) for v in me.vertices])
TRI = np.array([list(t.vertices) for t in me.loop_triangles])
A, B, C = V[TRI[:, 0]], V[TRI[:, 1]], V[TRI[:, 2]]
cen = (A + B + C) / 3.0
n = np.cross(B - A, C - A); ar = 0.5 * np.linalg.norm(n, axis=1)
n = n / np.maximum(np.linalg.norm(n, axis=1)[:, None], 1e-12)
bvh = BVHTree.FromObject(ob, dg); inv = M.inverted()
fac = {}
for el_deg in (19.77, 52.95):
    el = math.radians(el_deg)
    for d in DIRS:
        Ar = math.radians(AZI[d])
        v = np.array([math.sin(Ar) * math.cos(el), math.cos(Ar) * math.cos(el),
                      math.sin(el)])
        f = n @ v; vis = f > 0.05
        for i in np.where(vis)[0]:
            o = Vector((cen[i] + n[i] * 0.002).tolist())
            if bvh.ray_cast(inv @ o, inv.to_3x3() @ Vector(v.tolist()), 50.0)[0] is not None:
                vis[i] = False
        fac[(el_deg, d)] = np.where(vis, f, -1.0)
r1 = [(19.77, d) for d in DIRS]


def q(keys):
    bf = np.max(np.stack([fac[k] for k in keys]), 0); ok = bf > 0
    return (100 * ar[ok & (bf < 0.70)].sum() / ar.sum(),
            float((ar[ok] * bf[ok] ** 4).sum() / ar[ok].sum()))


print("SECOND-RING SUBSETS  (baseline = 19.77 ring alone)")
base = q(r1)
print("  %-26s grazing<0.70 %5.2f%%   mean weight %.4f" % ("19.77 ring alone",) + ("",) if 0 else
      "  %-26s grazing<0.70 %5.2f%%   mean weight %.4f" % ("19.77 ring alone", base[0], base[1]))
for sub in (["S"], ["S", "N"], ["E", "W"], ["SE", "NW"], ["S", "E", "N", "W"],
            ["SE", "NE", "NW", "SW"], DIRS):
    g, w = q(r1 + [(52.95, d) for d in sub])
    print("  + 52.95 %-18s grazing<0.70 %5.2f%%   mean weight %.4f  (%+.2f pp, %+.1f%% weight)"
          % (",".join(sub), g, w, g - base[0], 100 * (w / base[1] - 1)))

# ---- how big is the FACE? --------------------------------------------------
# head = the mesh above the withers break and forward of it; approximated as the
# top 18% of height at the +Y end, which is where this creature's human head is
zmax, zmin = V[:, 2].max(), V[:, 2].min()
ymax = V[:, 1].max()
head = (V[:, 2] > zmin + 0.80 * (zmax - zmin)) & (V[:, 1] > ymax - 0.45 * (ymax - V[:, 1].min()))
H = V[head]
print("\nFACE / HEAD BLOCK: %d verts, bbox %s m" %
      (head.sum(), np.round(H.max(0) - H.min(0), 4).tolist()))
hw = float(max(H[:, 0].max() - H[:, 0].min(), H[:, 1].max() - H[:, 1].min()))
hh = float(H[:, 2].max() - H[:, 2].min())
print("  head box about %.3f x %.3f m" % (hw, hh))
for ppm, nm in ((224.24, "whole-creature sheet, 8 views packed"),
                (158.6, "whole-creature sheet, 16 views packed"),
                (700.0, "a dedicated head cell at 700 px/m")):
    print("    at %6.1f px/m (%-38s) the head is %3.0f x %3.0f px"
          % (ppm, nm, hw * ppm, hh * ppm))
json.dump(dict(head_box_m=[round(hw, 4), round(hh, 4)]),
          open(os.path.join(ROOT, "work", "headbox.json"), "w"), indent=1)
