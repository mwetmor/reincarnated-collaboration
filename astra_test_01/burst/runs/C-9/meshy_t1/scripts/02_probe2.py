# C-9 meshy_t1: per-mesh probe -- which meshes are SKINNED to the rig, where the
# strays are, the character's true height, and the ground speed implied by the
# clip's own foot motion.
import bpy, json, math, sys, os
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
srcs, outp = a[:-1], a[-1]


def bbox(o, dg):
    ev = o.evaluated_get(dg); me = ev.to_mesh()
    lo = Vector((1e9, 1e9, 1e9)); hi = -lo
    for v in me.vertices:
        w = o.matrix_world @ v.co
        for i in range(3):
            lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
    ev.to_mesh_clear()
    return [round(x, 4) for x in lo], [round(x, 4) for x in hi]


rep = {"files": {}}
for src in srcs:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)
    sc = bpy.context.scene
    arm = next((o for o in sc.objects if o.type == 'ARMATURE'), None)
    meshes = [o for o in sc.objects if o.type == 'MESH']
    dg = bpy.context.evaluated_depsgraph_get()
    info = {}
    for o in meshes:
        skinned = any(m.type == 'ARMATURE' and m.object == arm for m in o.modifiers)
        lo, hi = bbox(o, dg)
        info[o.name] = dict(skinned=bool(skinned), verts=len(o.data.vertices),
                            bbox_lo=lo, bbox_hi=hi,
                            n_vgroups=len(o.vertex_groups))
    d = {"meshes": info, "fps": sc.render.fps}
    skin = [o for o in meshes if info[o.name]["skinned"]]
    if skin:
        lo = min(info[o.name]["bbox_lo"][2] for o in skin)
        hi = max(info[o.name]["bbox_hi"][2] for o in skin)
        d["character_z"] = [round(lo, 4), round(hi, 4)]
        d["character_height"] = round(hi - lo, 4)
    act = arm.animation_data.action if arm and arm.animation_data else None
    if act and arm:
        f0, f1 = int(act.frame_range[0]), int(act.frame_range[1])
        d["action"] = act.name; d["frame_range"] = [f0, f1]
        # FOOT TRACKS. A Meshy library clip arrives IN PLACE, so the travel
        # speed is not in the root -- it is in the feet: while a foot is
        # planted it slides BACKWARD under the body at exactly the ground
        # speed. Track both toes and read the speed off the stance phases.
        toes = [b for b in arm.pose.bones if 'toe' in b.name.lower()]
        feet = [b for b in arm.pose.bones if b.name.lower().endswith('foot')]
        track = {}
        for b in (toes + feet):
            pts = []
            for f in range(f0, f1 + 1):
                sc.frame_set(f)
                w = arm.matrix_world @ b.head
                pts.append([round(w.x, 5), round(w.y, 5), round(w.z, 5)])
            track[b.name] = pts
        d["foot_tracks"] = track
        # lowest skinned vertex per frame, so the ground row can be set off the
        # character rather than off a stray object
        lows = []
        for f in range(f0, f1 + 1):
            sc.frame_set(f)
            dg = bpy.context.evaluated_depsgraph_get()
            lo = 1e9
            for o in skin:
                ev = o.evaluated_get(dg); me = ev.to_mesh()
                for v in me.vertices:
                    lo = min(lo, (o.matrix_world @ v.co).z)
                ev.to_mesh_clear()
            lows.append(round(lo, 5))
        d["char_lowest_z_per_frame"] = lows
    rep["files"][os.path.basename(src)] = d
    print(os.path.basename(src), {k: (v["skinned"], v["verts"]) for k, v in info.items()},
          "char h", d.get("character_height"))
json.dump(rep, open(outp, "w"), indent=1)
print("wrote", outp)
