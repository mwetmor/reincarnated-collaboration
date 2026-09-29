"""C-9 T10-1b: render a model's silhouette round a yaw sweep, and report its topology.

    blender --background --python 54_kit_probe.py -- <in.glb> <outdir> [pitch_deg] [step_deg] [px]

Two jobs, one import, because the import is the slow part.

1. SILHOUETTES. Orthographic, Workbench, transparent film: the alpha channel IS the
   silhouette, with no lighting to argue about. The sweep is over AZIMUTH in the glTF /
   Godot frame, defined here once so nothing downstream has to infer it:

       azimuth A puts the camera at (sin A, 0, cos A) from the object, up = +Y, looking in.
       A = 0 is the glTF front view. Rotating a model by +A about +Y moves whatever faced
       azimuth 0 to azimuth A.

   Blender is Z-up and the glTF importer maps (x, y, z) -> (x, -z, y), so that camera
   direction becomes (sin A cos P, -cos A cos P, sin P) here. Written out rather than
   derived at the call site: a sign error in this line renders perfectly and is wrong,
   which is the whole reason T9 measured yaw instead of calculating it.

2. TOPOLOGY. Triangles, loose parts, non-manifold edges, and whether the mesh is closed.
   `islands` counts loose parts because the elk sheet has three ribs drawn detached from
   the skull -- three islands there is the object, not a fault, and the number is only
   readable if something counts it. `watertight` is (non-manifold edges == 0), which is
   also what decides `snow_bed_ok`: a drift can only be banked against a closed base.
"""
import json
import math
import os
import sys

import bmesh
import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT = argv[0], argv[1]
PITCH = float(argv[2]) if len(argv) > 2 else 0.0
STEP = float(argv[3]) if len(argv) > 3 else 15.0
PX = int(argv[4]) if len(argv) > 4 else 512
NAME = os.path.splitext(os.path.basename(SRC))[0]
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
for o in meshes:
    o.data.calc_loop_triangles()

# --- topology, on a joined copy so loose parts across objects count as one population ---
bm = bmesh.new()
for o in meshes:
    m = o.data.copy()
    m.transform(o.matrix_world)
    bm.from_mesh(m)
    bpy.data.meshes.remove(m)
tris = sum(len(o.data.loop_triangles) for o in meshes)
raw_verts = len(bm.verts)
# WELD FIRST OR THE NUMBERS ARE THE EXPORTER'S, NOT THE MESH'S. glTF duplicates a vertex
# at every UV and normal seam, so a closed Tripo mesh imports as tens of thousands of
# "boundary" edges and dozens of "islands" -- 28,694 and 62 on the rock cluster, all of
# them seams. Merging coincident vertices first is what makes `islands` mean loose parts
# and `watertight` mean closed. Measured after the merge; both counts reported.
bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
bm.verts.ensure_lookup_table()
nonman = sum(1 for e in bm.edges if not e.is_manifold)
boundary = sum(1 for e in bm.edges if len(e.link_faces) < 2)
seen, islands = set(), 0
for v in bm.verts:
    if v.index in seen:
        continue
    islands += 1
    stack = [v]
    seen.add(v.index)
    while stack:
        c = stack.pop()
        for e in c.link_edges:
            o = e.other_vert(c)
            if o.index not in seen:
                seen.add(o.index)
                stack.append(o)
stats = {"name": NAME, "tris": tris, "verts": len(bm.verts),
         "verts_before_weld": raw_verts, "edges": len(bm.edges),
         "islands": islands, "nonmanifold_edges": nonman, "boundary_edges": boundary,
         "watertight": nonman == 0 and boundary == 0}
bm.free()

# --- world AABB, in glTF axes (x, y=up, z) ---
lo = [1e9] * 3
hi = [-1e9] * 3
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ __import__("mathutils").Vector(c)
        for i in range(3):
            lo[i] = min(lo[i], w[i])
            hi[i] = max(hi[i], w[i])
# Blender (x, y, z) came from glTF (x, z, -y): invert to report in glTF axes
g_lo = [lo[0], lo[2], -hi[1]]
g_hi = [hi[0], hi[2], -lo[1]]
stats["aabb_min_gltf"] = [round(v, 6) for v in g_lo]
stats["aabb_max_gltf"] = [round(v, 6) for v in g_hi]
stats["size_gltf"] = [round(g_hi[i] - g_lo[i], 6) for i in range(3)]
ctr = [(lo[i] + hi[i]) / 2 for i in range(3)]
rad = max(math.dist(ctr, [lo[0] if a & 1 else hi[0], lo[1] if a & 2 else hi[1],
                          lo[2] if a & 4 else hi[2]]) for a in range(8))

# --- render setup ---
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.render.film_transparent = True
sc.render.resolution_x = sc.render.resolution_y = PX
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_mode = "RGBA"
sh = sc.display.shading
sh.light = "FLAT"
sh.color_type = "SINGLE"
sh.single_color = (1.0, 1.0, 1.0)
sh.show_object_outline = False
sh.show_specular_highlight = False

cam_d = bpy.data.cameras.new("cam")
cam_d.type = "ORTHO"
cam_d.ortho_scale = rad * 2.06
cam = bpy.data.objects.new("cam", cam_d)
sc.collection.objects.link(cam)
sc.camera = cam

P = math.radians(PITCH)
n = int(round(360.0 / STEP))
for k in range(n):
    A = math.radians(k * STEP)
    d = (math.sin(A) * math.cos(P), -math.cos(A) * math.cos(P), math.sin(P))
    R = rad * 4.0
    cam.location = (ctr[0] + d[0] * R, ctr[1] + d[1] * R, ctr[2] + d[2] * R)
    cam.rotation_mode = "XYZ"
    cam.rotation_euler = (math.pi / 2 - P, 0.0, A)
    cam_d.clip_start = 0.01
    cam_d.clip_end = R * 3
    sc.render.filepath = os.path.join(OUT, "%s_az%03d.png" % (NAME, int(round(k * STEP))))
    bpy.ops.render.render(write_still=True)

stats["pitch_deg"] = PITCH
stats["step_deg"] = STEP
stats["px"] = PX
stats["ortho_scale"] = round(cam_d.ortho_scale, 6)
with open(os.path.join(OUT, "%s_stats.json" % NAME), "w") as f:
    json.dump(stats, f, indent=1)
print("[probe] %s tris %d islands %d nonmanifold %d boundary %d watertight %s size %s"
      % (NAME, tris, islands, nonman, boundary, stats["watertight"], stats["size_gltf"]))
