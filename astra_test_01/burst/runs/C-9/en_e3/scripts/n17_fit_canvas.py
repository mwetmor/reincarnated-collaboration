# EN-E3: the largest uniform scale at which a creature's every clip, at every one of the 8 contract headings, clears the JOIN-1 canvas
# edge (768 px, anchor (384, 448), ppm_render 151.337, pitch 52.954) with a margin. Run on the SHIPPED GLB; prints s_max.
#   blender -b -noaudio --python scripts/n17_fit_canvas.py -- <glb> [margin=0.05]
# Port projection (contract 2.1/2.3): u = 384 + ppm*x, v = 448 + ppm*(sin a * y - cos a * z), y toward the camera. Blender: x = X,
# y_port = -Y (the model faces -Y = toward the camera at S), z = Z; the 8 headings rotate the model by multiples of 45 deg.
import bpy, sys, math, json
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
GLB = a[0]; MARGIN = float(a[1]) if len(a) > 1 else 0.05
PPM = 151.33680669505316; AL = math.radians(52.9535411256029); CA, SA = math.cos(AL), math.sin(AL)
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.context.scene.render.fps = 30
bpy.ops.import_scene.gltf(filepath=GLB)
sc = bpy.context.scene; arm = next(o for o in sc.objects if o.type == 'ARMATURE'); body = next(o for o in sc.objects if o.type == 'MESH')
for t in arm.animation_data.nla_tracks: t.mute = True
worst = (1e9, None)
for act in bpy.data.actions:
    arm.animation_data.action = act
    try:
        if act.slots and arm.animation_data.action_slot is None: arm.animation_data.action_slot = act.slots[0]
    except Exception: pass
    n = int(round(act.frame_range[1]))
    for f in range(n + 1):
        sc.frame_set(f); dg = bpy.context.evaluated_depsgraph_get(); e = body.evaluated_get(dg); m = e.to_mesh()
        co = np.empty(len(m.vertices) * 3); m.vertices.foreach_get('co', co); e.to_mesh_clear()
        P = co.reshape(-1, 3) @ np.array(body.matrix_world.to_3x3()).T + np.array(body.matrix_world.translation)
        for k in range(8):
            th = math.radians(45 * k); c, s = math.cos(th), math.sin(th)
            x = c * P[:, 0] - s * P[:, 1]; yb = s * P[:, 0] + c * P[:, 1]; yp = -yb
            du = PPM * x; dv = PPM * (SA * yp - CA * P[:, 2])
            lim = []
            if du.max() > 0: lim.append(382.0 / du.max())
            if du.min() < 0: lim.append(-383.0 / du.min())
            if dv.max() > 0: lim.append(318.0 / dv.max())
            if dv.min() < 0: lim.append(-446.0 / dv.min())
            sm = min(lim)
            if sm < worst[0]: worst = (sm, '%s f%d heading%d' % (act.name, f, k))
print(json.dumps(dict(glb=GLB, s_fit=round(worst[0], 4), s_with_margin=round(worst[0] / (1 + MARGIN), 4), binding=worst[1], margin=MARGIN)))
