# C-9 meshy_t1: probe a Meshy-rigged GLB -- bones, clips, root motion, scale.
# blender -b -noaudio --python scripts/01_probe_rig.py -- <glb> [<glb> ...] <out.json>
import bpy, json, math, sys, os
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
srcs, outp = a[:-1], a[-1]
rep = {"files": {}}
for src in srcs:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)
    sc = bpy.context.scene
    arms = [o for o in sc.objects if o.type == 'ARMATURE']
    meshes = [o for o in sc.objects if o.type == 'MESH']
    d = {"armatures": len(arms), "meshes": [o.name for o in meshes],
         "fps": sc.render.fps}
    if arms:
        arm = arms[0]
        d["bones"] = [b.name for b in arm.data.bones]
        d["n_bones"] = len(d["bones"])
        act = arm.animation_data.action if arm.animation_data else None
        d["action"] = act.name if act else None
        if act:
            f0, f1 = int(act.frame_range[0]), int(act.frame_range[1])
            d["frame_range"] = [f0, f1]
            d["n_frames"] = f1 - f0 + 1
            d["duration_s"] = (f1 - f0) / max(sc.render.fps, 1)
            # root motion: track the armature's root bone head in world space
            root = None
            for cand in ("Hips", "hips", "mixamorig:Hips", "Root", "root"):
                if cand in arm.pose.bones:
                    root = arm.pose.bones[cand]; break
            if root is None:
                root = arm.pose.bones[0]
            d["root_bone"] = root.name
            tr = []
            for f in range(f0, f1 + 1):
                sc.frame_set(f)
                w = arm.matrix_world @ root.head
                tr.append([round(w.x, 5), round(w.y, 5), round(w.z, 5)])
            d["root_track"] = tr
            xs = [p[0] for p in tr]; ys = [p[1] for p in tr]; zs = [p[2] for p in tr]
            d["root_span"] = dict(x=round(max(xs) - min(xs), 4),
                                  y=round(max(ys) - min(ys), 4),
                                  z=round(max(zs) - min(zs), 4))
            # per-frame lowest vertex (ground contact) and the whole-clip bbox
            lows, tops = [], []
            for f in range(f0, f1 + 1):
                sc.frame_set(f)
                dg = bpy.context.evaluated_depsgraph_get()
                lo, hi = 1e9, -1e9
                for o in meshes:
                    ev = o.evaluated_get(dg)
                    me = ev.to_mesh()
                    for v in me.vertices:
                        z = (o.matrix_world @ v.co).z
                        lo = min(lo, z); hi = max(hi, z)
                    ev.to_mesh_clear()
                lows.append(round(lo, 5)); tops.append(round(hi, 5))
            d["lowest_z_per_frame"] = lows
            d["highest_z_per_frame"] = tops
    # rest-pose height, measured on the mesh with the armature at rest
    if arms:
        arms[0].animation_data_clear()
    sc.frame_set(1)
    dg = bpy.context.evaluated_depsgraph_get()
    lo, hi = 1e9, -1e9
    for o in meshes:
        ev = o.evaluated_get(dg); me = ev.to_mesh()
        for v in me.vertices:
            z = (o.matrix_world @ v.co).z
            lo = min(lo, z); hi = max(hi, z)
        ev.to_mesh_clear()
    d["rest_bbox_z"] = [round(lo, 5), round(hi, 5)]
    d["rest_height_m"] = round(hi - lo, 5)
    rep["files"][os.path.basename(src)] = d
    print(os.path.basename(src), "bones", d.get("n_bones"), "action", d.get("action"),
          "frames", d.get("n_frames"), "height", d["rest_height_m"])
json.dump(rep, open(outp, "w"), indent=1)
print("wrote", outp)
