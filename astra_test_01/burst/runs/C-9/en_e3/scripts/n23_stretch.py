# EN-E3: skinning-defect vs foreshortening probe for one clip frame of a shipped GLB (the worm emerge f20 question).
#   blender -b -noaudio --python scripts/n23_stretch.py -- <glb> <clip> <frame> <out.json> [--rest_clip idle --rest_frame 0]
# For every mesh edge: deformed length / bind length, with the part of the change a UNIFORM scale explains divided out (the emerge
# grows the body by the Hips scale, so a rising worm at grow g has every edge at g x). A skinning defect = edges collapsing
# (ratio << 1 after the scale is divided out) or tearing (>> 1), clustered on the body; foreshortening = edges near 1.0 while the
# PROJECTED (game-camera) length shrinks because the part turned toward the camera. Both are measured, along the body by 10 % bins
# of the bind-pose long axis (head end = bin 0). Also: the angle each bin's surface normal makes with the camera's view direction.
import bpy, sys, json, math, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
GLB, CLIP, FR, OUT = a[0], a[1], int(a[2]), a[3]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
arm = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE'][0]
body = max((o for o in bpy.context.scene.objects if o.type == 'MESH'), key=lambda o: len(o.data.vertices))
acts = {x.name: x for x in bpy.data.actions}
act = acts.get(CLIP) or next(v for k, v in acts.items() if k.startswith(CLIP))
def coords(action, frame):
    arm.animation_data.action = action
    bpy.context.scene.frame_set(frame); dg = bpy.context.evaluated_depsgraph_get()
    e = body.evaluated_get(dg); m = e.to_mesh(); co = np.empty(len(m.vertices) * 3); m.vertices.foreach_get('co', co); e.to_mesh_clear()
    return co.reshape(-1, 3) @ np.array(body.matrix_world.to_3x3()).T + np.array(body.matrix_world.translation)
rest = np.array([v.co[:] for v in body.data.vertices]) @ np.array(body.matrix_world.to_3x3()).T + np.array(body.matrix_world.translation)
P = coords(act, FR)
E = np.array([e.vertices[:] for e in body.data.edges])
l0 = np.linalg.norm(rest[E[:, 0]] - rest[E[:, 1]], axis=1); l1 = np.linalg.norm(P[E[:, 0]] - P[E[:, 1]], axis=1)
ok = l0 > 1e-6; r = l1[ok] / l0[ok]; g = float(np.median(r)); rn = r / g
# game camera: pitch 52.954 deg down, looking from -Y (south) toward +Y; view dir d = (0, cos a, -sin a) in Blender (model faces -Y)
al = math.radians(52.9535411256029); d = np.array([0, math.cos(al), -math.sin(al)])
def proj(X): return np.stack([X[:, 0], X[:, 1] * math.sin(al) + X[:, 2] * math.cos(al)], 1)   # screen (u, v-up), ortho
p0 = np.linalg.norm(proj(rest)[E[:, 0]] - proj(rest)[E[:, 1]], axis=1)[ok]; p1 = np.linalg.norm(proj(P)[E[:, 0]] - proj(P)[E[:, 1]], axis=1)[ok]
y = rest[:, 1]; head_neg = True   # model faces -Y: the head end is min y
t = (y - y.min()) / (y.max() - y.min()); te = 0.5 * (t[E[ok, 0]] + t[E[ok, 1]])
bins = []
for b in range(10):
    s = (te >= b / 10) & (te < (b + 1) / 10 + (1e-9 if b == 9 else 0))
    if not s.any(): continue
    bins.append(dict(bin='%d-%d%%' % (b * 10, b * 10 + 10), edges=int(s.sum()),
        len_ratio_p05=round(float(np.quantile(rn[s], 0.05)), 3), len_ratio_med=round(float(np.median(rn[s])), 3), len_ratio_p95=round(float(np.quantile(rn[s], 0.95)), 3),
        collapsed_lt_0p6=int((rn[s] < 0.6).sum()), torn_gt_1p6=int((rn[s] > 1.6).sum()),
        screen_ratio_med=round(float(np.median(p1[s] / np.maximum(p0[s], 1e-9)) / g), 3)))
# centreline pitch of the head end: rise of the front 25 % relative to the rest
fr = t < 0.25
res = dict(glb=GLB, clip=act.name, frame=FR, uniform_scale_divided_out=round(g, 4),
           all_edges=dict(p01=round(float(np.quantile(rn, 0.01)), 3), p50=round(float(np.median(rn)), 3), p99=round(float(np.quantile(rn, 0.99)), 3),
                          collapsed_lt_0p6=int((rn < 0.6).sum()), torn_gt_1p6=int((rn > 1.6).sum()), n=int(rn.size)),
           front25_mean_z_rest=round(float(rest[fr, 2].mean()), 3), front25_mean_z_frame=round(float(P[fr, 2].mean()), 3),
           front25_max_z_frame=round(float(P[fr, 2].max()), 3), bins_head_first=bins)
# the front's lift angle: principal direction of the front 25 % verts vs horizontal
c = P[fr] - P[fr].mean(0); w_, v_ = np.linalg.eigh(c.T @ c); ax = v_[:, -1]; res['front25_axis_elev_deg'] = round(math.degrees(math.asin(abs(ax[2]))), 1)
json.dump(res, open(OUT, 'w'), indent=1); print(json.dumps(res)[:3000])
