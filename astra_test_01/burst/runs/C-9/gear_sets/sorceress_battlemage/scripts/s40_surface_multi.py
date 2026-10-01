# R-C9-105 paint pass: D7's 06a_surface for MANY meshes sharing ONE atlas, occluded by EVERY mesh in the scene.
#   blender -b -noaudio --python s40_surface_multi.py -- <scene.glb> <out.npz> --target <prefix> --sheets a,b [--size 2048]
# --target   objects whose name starts with this prefix are rasterised into ONE UV texel map (they share an atlas: the eight
#            champion pieces were cut from one Tripo build); "B_" = the champion body alone.
# occlusion  per sheet cell, a triangle is visible if it faces the camera and a ray toward the camera hits NOTHING -- in
#            any mesh of the scene (the body hides under plates, a plate under the pauldron). helmet_on = 1 on the body
#            when the scene holds the helm, as it is worn.
# Output keys are 06b_bake's: tex_tri, tex_pos, tex_nrm, uv_area, V, TRI, size, vis_<sheet>_<cell>.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
SCENE, OUT = a[0], a[1]
TGT = a[a.index("--target") + 1]
SHEETS = a[a.index("--sheets") + 1].split(",")
SIZE = int(a[a.index("--size") + 1]) if "--size" in a else 2048
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SCENE)
sc = bpy.context.scene
for ar in [o for o in sc.objects if o.type == 'ARMATURE']:
    if ar.animation_data:
        ar.animation_data.action = None
    for pb in ar.pose.bones:
        pb.matrix_basis.identity()
meshes = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.data.vertices) > 200]
helm_present = any(o.name.startswith("P_helm") for o in meshes)
for o in meshes:
    if o.data.shape_keys:
        for k in o.data.shape_keys.key_blocks:
            k.value = 1.0 if ((k.name == "helmet_on" and helm_present) or (k.name.startswith("under_") and len(meshes) > 1)) else 0.0
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()


def evaluated(o):
    oe = o.evaluated_get(dg); me = oe.to_mesh(); me.calc_loop_triangles()
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
    M = np.array(o.matrix_world); V = co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
    tri = np.array([list(t.vertices) for t in me.loop_triangles], np.int64)
    tl = np.array([list(t.loops) for t in me.loop_triangles], np.int64)
    uvl = me.uv_layers.active.data if me.uv_layers.active else None
    UV = None
    if uvl is not None:
        UV = np.empty(len(uvl) * 2); uvl.foreach_get("uv", UV); UV = UV.reshape(-1, 2)
    oe.to_mesh_clear()
    return V, tri, tl, UV


allV, allT, off = [], [], 0
tV, tTRI, tTUV, toff = [], [], [], 0
names = []
for o in meshes:
    V, tri, tl, UV = evaluated(o)
    allV.append(V); allT.append(tri + off); off += len(V)
    if o.name.startswith(TGT):
        tV.append(V); tTRI.append(tri + toff); tTUV.append(UV[tl]); toff += len(V); names.append(o.name)
assert names, "no object starts with %r" % TGT
bvh = BVHTree.FromPolygons([Vector(p) for p in np.vstack(allV).tolist()], np.vstack(allT).tolist())
V = np.vstack(tV); TRI = np.vstack(tTRI); TUV = np.vstack(tTUV)
print("target %s: %d meshes %s, %d verts, %d tris; occluders %d meshes; helmet_on %s"
      % (TGT, len(names), names, len(V), len(TRI), len(meshes), helm_present))
# per-vertex normals (area-weighted from faces)
fn = np.cross(V[TRI[:, 1]] - V[TRI[:, 0]], V[TRI[:, 2]] - V[TRI[:, 0]])
NV = np.zeros_like(V)
for k in range(3):
    np.add.at(NV, TRI[:, k], fn)
NV /= np.maximum(np.linalg.norm(NV, axis=1)[:, None], 1e-12)
fnn = fn / np.maximum(np.linalg.norm(fn, axis=1)[:, None], 1e-12)
TP = TUV * np.array([SIZE, SIZE])
tex_pos = np.zeros((SIZE, SIZE, 3), np.float32); tex_nrm = np.zeros((SIZE, SIZE, 3), np.float32)
tex_tri = np.full((SIZE, SIZE), -1, np.int64)
A3, B3, C3 = V[TRI[:, 0]], V[TRI[:, 1]], V[TRI[:, 2]]
NA, NB, NC = NV[TRI[:, 0]], NV[TRI[:, 1]], NV[TRI[:, 2]]
for i in range(len(TRI)):
    p = TP[i]
    x0 = max(int(np.floor(p[:, 0].min())), 0); x1 = min(int(np.ceil(p[:, 0].max())) + 1, SIZE)
    y0 = max(int(np.floor(p[:, 1].min())), 0); y1 = min(int(np.ceil(p[:, 1].max())) + 1, SIZE)
    if x1 <= x0 or y1 <= y0:
        continue
    X, Y = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
    d = (p[1, 1] - p[2, 1]) * (p[0, 0] - p[2, 0]) + (p[2, 0] - p[1, 0]) * (p[0, 1] - p[2, 1])
    if abs(d) < 1e-12:
        continue
    l0 = ((p[1, 1] - p[2, 1]) * (X - p[2, 0]) + (p[2, 0] - p[1, 0]) * (Y - p[2, 1])) / d
    l1 = ((p[2, 1] - p[0, 1]) * (X - p[2, 0]) + (p[0, 0] - p[2, 0]) * (Y - p[2, 1])) / d
    l2 = 1.0 - l0 - l1
    m = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
    if not m.any():
        continue
    yy, xx = np.where(m); Yg, Xg = yy + y0, xx + x0
    w0, w1, w2 = l0[m][:, None], l1[m][:, None], l2[m][:, None]
    tex_pos[Yg, Xg] = w0 * A3[i] + w1 * B3[i] + w2 * C3[i]
    n = w0 * NA[i] + w1 * NB[i] + w2 * NC[i]
    tex_nrm[Yg, Xg] = n / np.maximum(np.linalg.norm(n, axis=1)[:, None], 1e-12)
    tex_tri[Yg, Xg] = i
ON = tex_tri >= 0
print("  uv coverage: %.2f%% of texels lie on the target meshes" % (100 * ON.mean()))
uv_area = np.maximum(0.5 * np.abs((TP[:, 1, 0] - TP[:, 0, 0]) * (TP[:, 2, 1] - TP[:, 0, 1]) -
                                  (TP[:, 2, 0] - TP[:, 0, 0]) * (TP[:, 1, 1] - TP[:, 0, 1])), 1e-9)
cen = (A3 + B3 + C3) / 3.0
out = dict(tex_tri=tex_tri.astype(np.int32), tex_pos=tex_pos, tex_nrm=tex_nrm, uv_area=uv_area.astype(np.float32),
           V=V.astype(np.float32), TRI=TRI.astype(np.int32), size=np.array([SIZE]))
for name in SHEETS:
    L = json.load(open(os.path.join(ROOT, "work", "layout_%s.json" % name)))
    for d, c in L["cells"].items():
        vdir = np.array(c["view_dir"])                      # the stored camera, once (t5_01's rule)
        vis = (fnn @ vdir) > 0.05
        nf = int(vis.sum())
        for i in np.where(vis)[0]:
            o = Vector((cen[i] + fnn[i] * 0.002).tolist())
            if bvh.ray_cast(o, Vector(vdir.tolist()), 50.0)[0] is not None:
                vis[i] = False
        out["vis_%s_%s" % (name, d)] = vis
        print("   %-6s %-8s %7d tris face it, %7d unoccluded" % (name, d, nf, int(vis.sum())))
np.savez(OUT, **out)
json.dump(dict(target=TGT, meshes=names, verts=int(len(V)), tris=int(len(TRI)), size=SIZE, helmet_on=helm_present,
               uv_coverage_pct=round(100 * float(ON.mean()), 3)), open(OUT.replace(".npz", ".json"), "w"), indent=1)
print("wrote", OUT)
