# C-9 meshy_t2 step 1: measure the un-rigged Meshy manticore before touching it.
#
#   blender -b -noaudio --python scripts/01_probe.py -- <model.glb> <out.json>
#
# The task says: "glTF Y-up; after Blender import the body length runs along Y,
# so establish head/tail and up yourself." So nothing here is assumed. What is
# measured:
#
#  * the mesh objects, their transforms, vertex counts, materials;
#  * the world bbox and which axis is LONGEST (the body length) and which is
#    the true UP (the axis along which the four legs hang);
#  * head vs tail along the long axis, decided by CROSS-SECTION AREA -- a
#    manticore's head end carries the mane and the man's head, so it is bulky;
#    the tail end tapers to a whip. Slice the long axis into 40 bins and
#    compare the outer 15 % at each end by both vertex count and slab volume.
#  * a 40-bin profile of the mesh so the leg/torso/neck landmarks can be read
#    off it later rather than guessed.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUTP = a[0], a[1]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene

objs = [o for o in sc.objects if o.type == 'MESH']
arms = [o for o in sc.objects if o.type == 'ARMATURE']
rep = dict(source=os.path.basename(SRC),
           objects=[dict(name=o.name, type=o.type,
                         parent=o.parent.name if o.parent else None,
                         loc=[round(v, 5) for v in o.location],
                         rot=[round(math.degrees(v), 3) for v in o.rotation_euler],
                         scale=[round(v, 5) for v in o.scale])
                    for o in sc.objects],
           n_meshes=len(objs), n_armatures=len(arms))

# ---- every vertex, in world space --------------------------------------------
V = []
for o in objs:
    M = o.matrix_world
    co = np.empty(len(o.data.vertices) * 3, dtype=np.float64)
    o.data.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    co = co @ np.array(M.to_3x3()).T + np.array(M.translation)
    V.append(co)
    rep.setdefault("meshes", []).append(
        dict(name=o.name, verts=len(o.data.vertices), polys=len(o.data.polygons),
             materials=[s.material.name if s.material else None for s in o.material_slots],
             uv_layers=[l.name for l in o.data.uv_layers],
             colour_attrs=[c.name for c in o.data.color_attributes]))
V = np.vstack(V)
lo, hi = V.min(0), V.max(0)
span = hi - lo
rep["world_bbox"] = dict(lo=[round(v, 5) for v in lo], hi=[round(v, 5) for v in hi],
                         span=[round(v, 5) for v in span])
rep["n_verts_total"] = int(len(V))

long_axis = int(np.argmax(span))
rep["longest_axis"] = "XYZ"[long_axis]

# ---- which axis is UP? The four legs hang from the torso, so the axis whose
#      LOWER half is much sparser than its upper half (thin legs under a solid
#      body) is up. Measured as the ratio of vertex density in the bottom
#      third to the middle third, per candidate axis.
up_scores = {}
for ax in range(3):
    t = (V[:, ax] - lo[ax]) / max(span[ax], 1e-9)
    bot = float((t < 0.33).sum()); mid = float(((t >= 0.33) & (t < 0.66)).sum())
    up_scores["XYZ"[ax]] = dict(bottom_third=bot, middle_third=mid,
                                ratio=round(bot / max(mid, 1), 4), span=round(span[ax], 4))
rep["up_candidates"] = up_scores

# ---- profile along the long axis ---------------------------------------------
NB = 40
t = (V[:, long_axis] - lo[long_axis]) / max(span[long_axis], 1e-9)
b = np.clip((t * NB).astype(int), 0, NB - 1)
other = [i for i in range(3) if i != long_axis]
prof = []
for i in range(NB):
    m = b == i
    n = int(m.sum())
    if n:
        s = V[m][:, other]
        prof.append(dict(bin=i, n=n,
                         ext0=round(float(s[:, 0].max() - s[:, 0].min()), 4),
                         ext1=round(float(s[:, 1].max() - s[:, 1].min()), 4),
                         c0=round(float(s[:, 0].mean()), 4),
                         c1=round(float(s[:, 1].mean()), 4)))
    else:
        prof.append(dict(bin=i, n=0, ext0=0.0, ext1=0.0, c0=0.0, c1=0.0))
rep["long_axis_profile"] = prof

k = max(1, int(NB * 0.15))
lowend = sum(p["n"] for p in prof[:k]); highend = sum(p["n"] for p in prof[-k:])
lowbulk = sum(p["ext0"] * p["ext1"] for p in prof[:k])
highbulk = sum(p["ext0"] * p["ext1"] for p in prof[-k:])
rep["head_end"] = dict(bins_each_end=k,
                       low_verts=lowend, high_verts=highend,
                       low_bulk=round(lowbulk, 5), high_bulk=round(highbulk, 5),
                       head_at=("low" if lowbulk > highbulk else "high"),
                       note="bulky end = mane + man's head; tapering end = whip tail")

json.dump(rep, open(OUTP, "w"), indent=1)
print("verts %d  bbox span %s  longest %s  head at %s"
      % (len(V), [round(v, 3) for v in span], rep["longest_axis"], rep["head_end"]["head_at"]))
for nm, s in up_scores.items():
    print("  up? %s span %.3f bottom/middle density %.3f" % (nm, s["span"], s["ratio"]))
print("wrote", OUTP)
