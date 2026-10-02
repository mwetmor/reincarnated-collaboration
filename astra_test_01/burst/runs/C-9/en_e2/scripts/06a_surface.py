# C-9 T5 step 2: project a painted sheet onto the model's UV texture.
#
#   blender -b -noaudio --python scripts/06a_surface.py -- <blend> <out.npz>
#          --sheets a,b [--size 2048]
#
# PART ONE, the half that needs Blender: where every texel sits on the surface,
# and which triangles each camera can actually see. Split from the bake because
# Blender ships no PIL, and because this half does not change when the paint
# does -- sheet B can be folded in later without re-rasterising anything.
#
# Nothing here knows what a manticore is. It takes sheets, each a layout JSON
# of per-cell cameras plus the painted image for it, and bakes them into one
# texture. A sheet may mix elevations, subjects and scales; a body painted in
# separate armour pieces is more sheets, not more code.
#
# WEIGHTING is texel density x facing^4. Facing alone cannot choose between two
# cameras pointed the same way, and that is exactly the case that matters: a
# head close-up and a whole-body view both see the face at the same angle, so
# facing would blend two independent paintings of it 50/50. Density -- screen
# pixels per texel -- is the thing that differs, and it is what "this camera
# saw the face better" actually means.
#
# THE MATTE IS THE RENDER'S OWN ALPHA, eroded. Astra's plate comes back lost
# often enough that segmenting the paint is not a dependency worth having, and
# the geometry already knows exactly where the creature is. Eroding also
# absorbs the ink line's own wander, measured at 2-3 px and scattering in
# direction rather than agreeing, which is what an outline drawn by hand does.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index('--') + 1:]
BLEND, OUTPNG = a[0], a[1]
SHEETS = a[a.index("--sheets") + 1].split(",")
SIZE = int(a[a.index("--size") + 1]) if "--size" in a else 2048
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# D7: the character arrives as a rigged GLB, not a canonicalised .blend. Loaded the
# same way the sheet builder loads it, so the two halves of the projection read one
# model -- and the mesh is chosen as the largest SKINNED mesh, never "the first mesh".
# After a glTF import the first mesh can be an Icosphere Blender INVENTED as a bone
# display shape (42 verts, no vertex groups); taking it would bake the paint onto a
# sphere. That trap has now cost this run a measurement three times before this.
if BLEND.lower().endswith((".glb", ".gltf")):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=BLEND)
else:
    bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
for _a in [o for o in sc.objects if o.type == 'ARMATURE']:
    if _a.animation_data:
        _a.animation_data.action = None       # REST, as the paint cameras were solved at rest
    for _pb in _a.pose.bones:
        _pb.matrix_basis.identity()
bpy.context.view_layer.update()
_sk = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.vertex_groups)]
ob = max(_sk or [o for o in sc.objects if o.type == 'MESH'], key=lambda o: len(o.data.vertices))
print("surface mesh: %s (%d verts, skinned=%s)" % (ob.name, len(ob.data.vertices), bool(_sk)))
dg = bpy.context.evaluated_depsgraph_get()
me = ob.data
me.calc_loop_triangles()
M = ob.matrix_world
Mn = np.array(M.to_3x3().inverted().transposed())
co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
VL = co.reshape(-1, 3)
V = VL @ np.array(M.to_3x3()).T + np.array(M.translation)
vn = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("normal", vn)
NV = vn.reshape(-1, 3) @ Mn.T
NV /= np.maximum(np.linalg.norm(NV, axis=1)[:, None], 1e-12)
uvl = me.uv_layers.active.data
UVL = np.empty(len(uvl) * 2); uvl.foreach_get("uv", UVL)
UVL = UVL.reshape(-1, 2)
TRI = np.array([list(t.vertices) for t in me.loop_triangles], np.int64)
TLOOP = np.array([list(t.loops) for t in me.loop_triangles], np.int64)
TUV = UVL[TLOOP]                                   # (n,3,2) in 0..1
print("mesh %s: %d tris, uv '%s', texture %dx%d"
      % (ob.name, len(TRI), me.uv_layers.active.name, SIZE, SIZE))

# ---- rasterise UV space: which texel is which point on the surface ---------
TP = TUV * np.array([SIZE, SIZE])                  # texel coords
tex_pos = np.zeros((SIZE, SIZE, 3), np.float32)
tex_nrm = np.zeros((SIZE, SIZE, 3), np.float32)
tex_tri = np.full((SIZE, SIZE), -1, np.int64)
A3, B3, C3 = V[TRI[:, 0]], V[TRI[:, 1]], V[TRI[:, 2]]
NA, NB, NC = NV[TRI[:, 0]], NV[TRI[:, 1]], NV[TRI[:, 2]]
for i in range(len(TRI)):
    p = TP[i]
    x0 = max(int(np.floor(p[:, 0].min())), 0); x1 = min(int(np.ceil(p[:, 0].max())) + 1, SIZE)
    y0 = max(int(np.floor(p[:, 1].min())), 0); y1 = min(int(np.ceil(p[:, 1].max())) + 1, SIZE)
    if x1 <= x0 or y1 <= y0:
        continue
    xs = np.arange(x0, x1) + 0.5; ys = np.arange(y0, y1) + 0.5
    X, Y = np.meshgrid(xs, ys)
    d = ((p[1, 1] - p[2, 1]) * (p[0, 0] - p[2, 0]) +
         (p[2, 0] - p[1, 0]) * (p[0, 1] - p[2, 1]))
    if abs(d) < 1e-12:
        continue
    l0 = ((p[1, 1] - p[2, 1]) * (X - p[2, 0]) + (p[2, 0] - p[1, 0]) * (Y - p[2, 1])) / d
    l1 = ((p[2, 1] - p[0, 1]) * (X - p[2, 0]) + (p[0, 0] - p[2, 0]) * (Y - p[2, 1])) / d
    l2 = 1.0 - l0 - l1
    m = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
    if not m.any():
        continue
    yy, xx = np.where(m)
    Yg, Xg = yy + y0, xx + x0
    w0, w1, w2 = l0[m][:, None], l1[m][:, None], l2[m][:, None]
    tex_pos[Yg, Xg] = w0 * A3[i] + w1 * B3[i] + w2 * C3[i]
    n = w0 * NA[i] + w1 * NB[i] + w2 * NC[i]
    tex_nrm[Yg, Xg] = n / np.maximum(np.linalg.norm(n, axis=1)[:, None], 1e-12)
    tex_tri[Yg, Xg] = i
ON = tex_tri >= 0
print("  uv coverage: %.2f%% of texels lie on the mesh" % (100 * ON.mean()))

# triangle area in texel units, for the density term
def tri_area(P2):
    return 0.5 * np.abs((P2[:, 1, 0] - P2[:, 0, 0]) * (P2[:, 2, 1] - P2[:, 0, 1]) -
                        (P2[:, 2, 0] - P2[:, 0, 0]) * (P2[:, 1, 1] - P2[:, 0, 1]))


uv_area = np.maximum(tri_area(TP), 1e-9)
cen = (A3 + B3 + C3) / 3.0
fn = np.cross(B3 - A3, C3 - A3)
fn /= np.maximum(np.linalg.norm(fn, axis=1)[:, None], 1e-12)
bvh = BVHTree.FromObject(ob, dg)
inv = M.inverted()


out = dict(tex_tri=tex_tri.astype(np.int32), tex_pos=tex_pos, tex_nrm=tex_nrm,
           uv_area=uv_area.astype(np.float32), V=V.astype(np.float32),
           TRI=TRI.astype(np.int32), size=np.array([SIZE]))
for name in SHEETS:
    L = json.load(open(os.path.join(ROOT, "work", "layout_%s.json" % name)))
    for d, c in L["cells"].items():
        el = math.radians(c.get("elevation_deg", L["elevation_deg"]))
        az = math.radians(c["azimuth_deg"])
        vdir = np.array([math.sin(az) * math.cos(el),
                         math.cos(az) * math.cos(el), math.sin(el)])
        vis = (fn @ vdir) > 0.05
        n_face = int(vis.sum())
        for i in np.where(vis)[0]:
            o = Vector((cen[i] + fn[i] * 0.002).tolist())
            if bvh.ray_cast(inv @ o, inv.to_3x3() @ Vector(vdir.tolist()),
                            50.0)[0] is not None:
                vis[i] = False
        out["vis_%s_%s" % (name, d)] = vis
        print("   %-4s %-9s %6d tris face it, %6d unoccluded"
              % (name, d, n_face, int(vis.sum())))
np.savez(OUTPNG, **out)
print("wrote %s" % OUTPNG)
