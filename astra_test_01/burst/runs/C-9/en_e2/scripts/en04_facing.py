# EN-E2: which way does the Tripo build face? (so_d7's s4_facing, re-cued for the acolytes)
#   blender -b -noaudio --python scripts/en04_facing.py -- <tripo.glb> <out.json> --band 0.42,0.62 [--off 0.10]
# Two cues, and they must agree:
#   MARKER  the BRASS asymmetry marker is on the figure's LEFT only (his bracer on the left forearm, her clock-face disc at the
#           left hip). Brass = hue 25-55 deg, saturation > 0.30, value > 0.25, inside the marker's height band and off the
#           body's centre line. Facing +X with +Z up, the left is Z x X = +Y; facing -X it is -Y.
#   TOES    the feet: the toes stick out further forward than the heels behind, so the lowest 4 % of the figure reaches further
#           along its forward axis than backward (sign of the X extent asymmetry of the foot band).
import bpy, json, sys, colorsys
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUT = a[0], a[1]
lo, hi = (float(x) for x in a[a.index('--band') + 1].split(',')) if '--band' in a else (0.42, 0.62)
OFF = float(a[a.index('--off') + 1]) if '--off' in a else 0.10
HUE = [float(x) for x in a[a.index('--hue') + 1].split(',')] if '--hue' in a else [25.0, 55.0, 0.30]   # lo,hi,sat_min (the wraith's marker is a LAPIS strip: 190,250,0.15)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
ob = max([o for o in bpy.context.scene.objects if o.type == 'MESH'], key=lambda o: len(o.data.vertices))
me = ob.data
img = next(n.image for s in ob.material_slots if s.material and s.material.node_tree for n in s.material.node_tree.nodes
           if n.type == 'TEX_IMAGE' and n.image)
W, H = img.size
px = np.array(img.pixels[:], dtype=np.float32).reshape(H, W, 4)[..., :3]
uvl = me.uv_layers.active.data
M = np.array(ob.matrix_world)
co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
V = co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
li = np.empty(len(me.loops), np.int64); me.loops.foreach_get("vertex_index", li)
uv = np.empty(len(me.loops) * 2); uvl.foreach_get("uv", uv); uv = uv.reshape(-1, 2)
first = np.full(len(me.vertices), -1, np.int64); first[li[::-1]] = np.arange(len(li))[::-1]
ok = first >= 0
x = np.clip((uv[first[ok], 0] * W).astype(int), 0, W - 1); y = np.clip((uv[first[ok], 1] * H).astype(int), 0, H - 1)
vcol = np.zeros((len(me.vertices), 3), np.float32); vcol[ok] = px[y, x]
z0, z1 = V[:, 2].min(), V[:, 2].max(); Hm = z1 - z0
hsv = np.array([colorsys.rgb_to_hsv(*c) for c in vcol])
brass = (hsv[:, 0] * 360 > HUE[0]) & (hsv[:, 0] * 360 < HUE[1]) & (hsv[:, 1] > HUE[2]) & (hsv[:, 2] > 0.25)
band = (V[:, 2] > z0 + lo * Hm) & (V[:, 2] < z0 + hi * Hm)
span = V[:, 1].max() - V[:, 1].min()
off = np.abs(V[:, 1] - np.median(V[:, 1])) > OFF * span
t = brass & band & off
ty = V[t, 1] - np.median(V[:, 1])
npos, nneg = int((ty > 0).sum()), int((ty < 0).sum())
left_sign = +1 if npos > nneg else -1
mk_face = left_sign            # left +Y <=> faces +X
feet = V[:, 2] < z0 + 0.04 * Hm
fx = V[feet, 0]; cx = np.median(V[:, 0])
toe_face = +1 if (fx.max() - cx) > (cx - fx.min()) else -1
agree = mk_face == toe_face
fwd = "+X" if mk_face > 0 else "-X"
yaw = -90.0 if mk_face > 0 else 90.0
rep = dict(marker=dict(n=int(t.sum()), pos=npos, neg=nneg, left_sign=left_sign, band=[lo, hi], off=OFF),
           toes=dict(fwd_extent=float(fx.max() - cx), back_extent=float(cx - fx.min()), sign=toe_face),
           agree=bool(agree), faces=fwd, yaw=yaw, height_units=float(Hm))
print("FACING", json.dumps(rep))
json.dump(rep, open(OUT, "w"), indent=1)
