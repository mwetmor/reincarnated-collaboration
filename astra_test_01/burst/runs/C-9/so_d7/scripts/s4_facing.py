# Which way does she face? Two features from the TEXTURE, and they must agree.
#
#   blender -b -noaudio --python scripts/s4_facing.py -- <tripo.glb>
#
# The geometric foot probe could not decide (asymmetry ratio 1.33, needs 1.5):
# her feet are close together and her boots are near-symmetric front to back.
# The bbox says she faces along +/-X -- the A-pose arms spread along Y -- but
# not which sign. The sheet gives two independent answers:
#   FACE     at head height, the front is skin and the back is her dark braid,
#            so the brighter, warmer extreme is the face.
#   TATTOO   orange runes on her LEFT forearm, in every view of SO-1. Facing +X
#            with +Z up, her left is Z x X = +Y; facing -X, it is -Y. So the
#            tattoo's Y sign fixes the facing sign.
# A sidedness error is the one defect this pipeline has already shipped once
# (the barbarian's tattoo on the wrong arm), so this is not taken from one cue.
import bpy, json, sys
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=a[0])
ob = max([o for o in bpy.context.scene.objects if o.type == 'MESH'],
         key=lambda o: len(o.data.vertices))
me = ob.data
img = None
for s in ob.material_slots:
    if s.material and s.material.node_tree:
        for n in s.material.node_tree.nodes:
            if n.type == 'TEX_IMAGE' and n.image:
                img = n.image
W, H = img.size
px = np.array(img.pixels[:], dtype=np.float32).reshape(H, W, 4)[..., :3]
uvl = me.uv_layers.active.data
M = np.array(ob.matrix_world)
co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
V = co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
# per-vertex colour via the first loop that uses it
vcol = np.zeros((len(me.vertices), 3), np.float32)
seen = np.zeros(len(me.vertices), bool)
for poly in me.polygons:
    for li in poly.loop_indices:
        vi = me.loops[li].vertex_index
        if seen[vi]:
            continue
        u, v = uvl[li].uv
        x = min(W - 1, max(0, int(u * W))); y = min(H - 1, max(0, int(v * H)))
        vcol[vi] = px[y, x]; seen[vi] = True
z0, z1 = V[:, 2].min(), V[:, 2].max(); Hm = z1 - z0
# FACE: head band, the X extremes
head = V[:, 2] > z0 + 0.90 * Hm
hx = V[head, 0]; hc = vcol[head]
lum = hc.mean(1)
front_pos = lum[hx > np.percentile(hx, 85)].mean()
front_neg = lum[hx < np.percentile(hx, 15)].mean()
face_sign = +1 if front_pos > front_neg else -1
print("FACE    head band: +X extreme luminance %.3f, -X %.3f -> faces %sX"
      % (front_pos, front_neg, "+" if face_sign > 0 else "-"))
# TATTOO: orange = strong R, mid G, low B, on the forearm band away from centre
r, g, b = vcol[:, 0], vcol[:, 1], vcol[:, 2]
orange = (r > 0.55) & (g > 0.20) & (g < 0.55) & (b < 0.22) & (r - b > 0.40)
arm_band = (V[:, 2] > z0 + 0.42 * Hm) & (V[:, 2] < z0 + 0.62 * Hm)
off_ctr = np.abs(V[:, 1]) > 0.10 * (V[:, 1].max() - V[:, 1].min())
t = orange & arm_band & off_ctr
ty = V[t, 1]
tat_side = +1 if (ty > 0).sum() > (ty < 0).sum() else -1
print("TATTOO  %d orange forearm verts: %d at +Y, %d at -Y -> her left is %sY"
      % (t.sum(), (ty > 0).sum(), (ty < 0).sum(), "+" if tat_side > 0 else "-"))
# her left = Z x forward. forward +X -> left +Y; forward -X -> left -Y
tat_face = tat_side
print("        so the tattoo says she faces %sX" % ("+" if tat_face > 0 else "-"))
agree = face_sign == tat_face
fwd = "+X" if face_sign > 0 else "-X"
yaw = -90.0 if face_sign > 0 else 90.0     # rotate her forward onto -Y
print("AGREE: %s   -> faces %s; yaw %+.0f puts her forward on -Y" % (agree, fwd, yaw))
json.dump(dict(face=dict(pos=float(front_pos), neg=float(front_neg), sign=face_sign),
               tattoo=dict(n=int(t.sum()), pos=int((ty > 0).sum()), neg=int((ty < 0).sum()),
                           left_sign=tat_side),
               agree=bool(agree), faces=fwd, yaw=yaw),
          open(a[1] if len(a) > 1 else "work/s4_facing.json", "w"), indent=1)
