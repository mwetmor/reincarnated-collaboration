# R-C9-98: probe exported pieces: world extent at rest and in a posed frame, and the longest edges (sliver hunt).
#   blender -b -noaudio --python s27_piece_probe.py -- <body.glb> <action> <frame> <piece.glb> ...
import bpy, sys, json
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
BODY, ACT, FR = a[0], a[1], int(a[2])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
for p in [x for x in a[3:] if not x.startswith("--")]:
    before = set(sc.objects)
    bpy.ops.import_scene.gltf(filepath=p)
    new = [o for o in sc.objects if o not in before]
    parm = next(o for o in new if o.type == 'ARMATURE')
    for o in new:
        if o.type == 'MESH':
            for m in o.modifiers:
                if m.type == 'ARMATURE': m.object = arm
            o.parent = arm.parent if arm.parent else None
            o.matrix_world = next(x for x in sc.objects if x.type == 'MESH' and x.name.startswith('char1')).matrix_world.copy()
    meshes = [o for o in new if o.type == 'MESH']
    for o in meshes:
        o.name = "PIECE_" + p.split('/')[-1].replace('.glb', '')
    for o in [o for o in new if o.type == 'ARMATURE']:
        bpy.data.objects.remove(o, do_unlink=True)
act = bpy.data.actions.get(ACT)
res = {}
for mode in ("rest", "pose"):
    if mode == "rest":
        arm.animation_data.action = None
        for pb in arm.pose.bones: pb.matrix_basis.identity()
    else:
        arm.animation_data.action = act; sc.frame_set(FR)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    for o in sc.objects:
        if o.type != 'MESH' or not o.name.startswith("PIECE_"): continue
        oe = o.evaluated_get(dg); me = oe.to_mesh()
        co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
        M = np.array(o.matrix_world); W = co @ M[:3, :3].T + M[:3, 3]
        e = np.empty(len(me.edges) * 2, int); me.edges.foreach_get("vertices", e); e = e.reshape(-1, 2)
        L = np.linalg.norm(W[e[:, 0]] - W[e[:, 1]], axis=1)
        oe.to_mesh_clear()
        res.setdefault(o.name, {})[mode] = dict(n=len(W), lo=np.round(W.min(0), 3).tolist(), hi=np.round(W.max(0), 3).tolist(),
                                                 edge_p999=round(float(np.percentile(L, 99.9)), 4), edge_max=round(float(L.max()), 4),
                                                 edges_over_5cm=int((L > 0.05).sum()))
print("PROBE " + json.dumps(res))
# --where: report WHERE the long posed edges are (rest-pose position of their midpoints, by height band and side)
if "--where" in a:
    arm.animation_data.action = None
    for pb in arm.pose.bones: pb.matrix_basis.identity()
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    rest = {}
    for o in sc.objects:
        if o.type == 'MESH' and o.name.startswith("PIECE_") and "." not in o.name:
            oe = o.evaluated_get(dg); me = oe.to_mesh(); co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
            M = np.array(o.matrix_world); rest[o.name] = co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]; oe.to_mesh_clear()
    arm.animation_data.action = act; sc.frame_set(FR); bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    for o in sc.objects:
        if o.name not in rest: continue
        oe = o.evaluated_get(dg); me = oe.to_mesh(); co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
        M = np.array(o.matrix_world); Wp = co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
        e = np.empty(len(me.edges) * 2, int); me.edges.foreach_get("vertices", e); e = e.reshape(-1, 2); oe.to_mesh_clear()
        R = rest[o.name]; Lp = np.linalg.norm(Wp[e[:, 0]] - Wp[e[:, 1]], axis=1); Lr = np.linalg.norm(R[e[:, 0]] - R[e[:, 1]], axis=1)
        bad = (Lp > 0.05) & (Lp > 2.0 * Lr)
        mid = (R[e[bad, 0]] + R[e[bad, 1]]) / 2
        print("WHERE %s: %d edges stretched >2x and >5 cm; rest midpoints z %s, |x| %s, x sign +%d/-%d" % (
            o.name, bad.sum(), np.round(np.percentile(mid[:, 2], [5, 50, 95]), 3).tolist() if bad.any() else None,
            np.round(np.percentile(np.abs(mid[:, 0]), [5, 50, 95]), 3).tolist() if bad.any() else None,
            int((mid[:, 0] > 0).sum()), int((mid[:, 0] <= 0).sum())))
