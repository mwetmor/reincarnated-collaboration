# T6 step 4 -- geometry metrics, per model, measured on the NORMALISED mesh.
#
# The vertex weld is not optional. glTF splits vertices at every UV seam and
# every hard normal, so the delivered index buffer is topologically shredded:
# Meshy's knight ships 89,553 vertices for 115,567 triangles where a closed
# manifold needs about 57,800. Counting islands or boundary edges on the
# delivered indices would report every seam as a hole and every shell as
# hundreds of pieces -- a clean-looking number that measures the exporter, not
# the mesh. The split copies carry bit-identical positions, so an exact
# position weld (no tolerance, no grid rounding, nothing that could fuse two
# genuinely distinct surfaces) restores the real topology.
#
# blender -b -noaudio --python 05a_dump.py -- SRC OUT YAW
# Blender has no scipy, so this half only NORMALISES and DUMPS; 05b_metrics.py
# does the topology with scipy in the system interpreter.
import bpy, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import t6lib as L

a = sys.argv[sys.argv.index('--') + 1:]
src, outdir, yaw = a[0], a[1], float(a[2])
os.makedirs(outdir, exist_ok=True)
name = os.path.splitext(os.path.basename(src))[0]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
sc = bpy.context.scene
objs = L.mesh_objects(sc)
norm = L.normalise(sc, objs, yaw_deg=yaw, flip_x=False, target_h=1.0)

# ---- gather world-space triangles ------------------------------------------
V, F, off = [], [], 0
for o in objs:
    M = np.array(o.matrix_world)
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    p = co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
    o.data.calc_loop_triangles()
    lt = np.empty(len(o.data.loop_triangles) * 3, dtype=np.int32)
    o.data.loop_triangles.foreach_get("vertices", lt)
    V.append(p); F.append(lt.reshape(-1, 3) + off); off += len(p)
V = np.vstack(V); F = np.vstack(F)
raw_v, raw_t = len(V), len(F)

np.savez_compressed(f'{outdir}/{name}.npz', V=V.astype(np.float64), F=F.astype(np.int64))
json.dump(dict(model=name, yaw_applied=yaw, flip_x=False, norm=norm,
               verts_delivered=int(raw_v), tris_delivered=int(raw_t)),
          open(f'{outdir}/{name}_dump.json','w'), indent=1)
print('DUMP', name, raw_v, raw_t)
