"""C-9 CRATER v4 (R-C9-109), layer 1 -- THE REAL 3D CRATER, built in Blender. drax.

  blender -b -noaudio --python tools/crater_mesh.py -- OUT_DIR SEED [R_M]

One impact crater at the Meteor's footprint (R_M, the bowl's rim radius, default 1.1 m = MIX v3's crater):
  a shallow BOWL (0.22 m deep), a RAISED, BROKEN RIM (up to 0.11 m, torn by noise into lumps and gaps),
  FAULT-LINE CRACKS cut as real V-grooves radiating from near the centre to past the rim (a Voronoi-seeded
  set of 7-9 radial fractures, wandering, branching once), one or two RUNNERS out across the skirt,
  and a FEATHERED SKIRT (1.3 R to 1.9 R) easing the ground back to level, its vertex alpha fading to 0 so the
  crater has no hard edge.
A square grid (4.2 cm), planar UVs (u = +x, v = +y across the skirt's square), vertex colour alpha = the skirt.
Writes OUT_DIR/crater_<SEED>.glb, OUT_DIR/crater_<SEED>_heights.npz (the height field, for the projection bake)
and OUT_DIR/crater_<SEED>_cracks.npy (the cracks + the centre in UV space, 1024^2 u8: the emission-mask guide).
Godot's axes: Blender X -> Godot X, Blender Y -> Godot -Z, Blender Z (up) -> Godot Y (the glTF exporter's +Y up).
"""
import math
import os
import sys

import bpy
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
SEED = int(argv[1])
R = float(argv[2]) if len(argv) > 2 else 1.1
PROFILE = argv[3] if len(argv) > 3 else "snow"      # R-C9-118 (b): snow (v4) | ice (shallow, more fractures) | earth
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(SEED)

ROUT = 1.9 * R
N = 101                                   # grid verts per side
D_BOWL = {"snow": 0.22, "ice": 0.07, "earth": 0.17}[PROFILE]
H_RIM = {"snow": 0.11, "ice": 0.025, "earth": 0.09}[PROFILE]
G_DEPTH = 0.045
G_HALF = 0.028                            # a groove's half width (m)


def vnoise(x, y, scale, seed):
    """smooth value noise (bilinear on a hashed lattice), 0..1"""
    r = np.random.default_rng(seed)
    lat = r.random((64, 64))
    gx, gy = x * scale + 17.0, y * scale + 29.0
    ix, iy = np.floor(gx).astype(int) % 63, np.floor(gy).astype(int) % 63
    fx, fy = gx - np.floor(gx), gy - np.floor(gy)
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b = lat[ix, iy], lat[ix + 1, iy]
    c, d = lat[ix, iy + 1], lat[ix + 1, iy + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


xs = np.linspace(-ROUT, ROUT, N)
X, Y = np.meshgrid(xs, xs, indexing="xy")
Rr = np.hypot(X, Y)
TH = np.arctan2(Y, X)
n1 = vnoise(X, Y, 1.4, SEED)
n2 = vnoise(X, Y, 4.5, SEED + 1)
rw = Rr / R + (n1 - 0.5) * 0.16                      # the torn rim line

# --- the bowl and the rim ---------------------------------------------------------------------------------
bowl = np.where(rw < 1.0, -D_BOWL * np.power(np.clip(1.0 - rw * rw, 0, 1), 0.8), 0.0)
rim_lump = 0.55 + 0.45 * vnoise(np.cos(TH) * 3, np.sin(TH) * 3, 1.0, SEED + 2)
rim_gap = np.clip((vnoise(np.cos(TH) * 2, np.sin(TH) * 2, 1.0, SEED + 3) - 0.28) * 4.0, 0.25, 1.0)    # broken in places
rim = H_RIM * rim_lump * rim_gap * np.exp(-((rw - 1.06) / 0.13) ** 2)
h = bowl + rim + (n2 - 0.5) * 0.02
# the skirt: whatever stands above level eases back to 0 between 1.3 R and 1.9 R
sk = np.clip((Rr / R - 1.3) / 0.6, 0.0, 1.0)
sk = sk * sk * (3 - 2 * sk)
h = h * (1.0 - sk)

# --- the fault lines: wandering radial fractures (Voronoi-seeded angles), one branch each, as V-grooves -------
n_cr = int(rng.integers(11, 15)) if PROFILE == "ice" else int(rng.integers(7, 10))
base = np.sort((np.arange(n_cr) + rng.uniform(-0.3, 0.3, n_cr)) / n_cr * 2 * math.pi)
paths = []                                            # polylines in metres
for k, a0 in enumerate(base):
    reach = R * rng.uniform(0.9, 1.25)
    pts, a, r, da = [], a0, R * rng.uniform(0.08, 0.2), 0.0
    while r < reach:
        pts.append((r * math.cos(a), r * math.sin(a)))
        da = 0.8 * da + rng.normal(0, 0.06)          # a wander with momentum: a fracture, not a zigzag
        a += da * 0.05 / max(r, 0.5)
        r += 0.05
    paths.append(pts)
    if rng.random() < 0.6 and len(pts) > 8:          # one branch off the middle
        j = int(len(pts) * rng.uniform(0.35, 0.6))
        bx, by = pts[j]
        ba = math.atan2(by, bx) + rng.choice([-1, 1]) * rng.uniform(0.25, 0.45)
        br = math.hypot(bx, by)
        bp = [(bx, by)]
        for _ in range(int(rng.integers(5, 10))):
            br += 0.05
            ba += rng.normal(0, 0.015)
            bp.append((br * math.cos(ba), br * math.sin(ba)))
        paths.append(bp)
n_run = (2 + int(rng.random() < 0.5)) if PROFILE == "ice" else (1 + int(rng.random() < 0.5))
for k in range(n_run):                               # the runners: out across the skirt
    a = rng.uniform(0, 2 * math.pi)
    r = R * 0.9
    pts = []
    while r < ROUT * rng.uniform(0.85, 0.97):
        pts.append((r * math.cos(a), r * math.sin(a)))
        a += rng.normal(0, 0.02) / r
        r += 0.05
    paths.append(pts)

P = np.stack([X.ravel(), Y.ravel()], 1)
dist = np.full(P.shape[0], 9.0)
width = np.full(P.shape[0], G_HALF)
for pts in paths:
    q = np.array(pts)
    for i in range(len(q) - 1):
        a, b = q[i], q[i + 1]
        ab = b - a
        t = np.clip(((P - a) @ ab) / max(ab @ ab, 1e-9), 0, 1)
        d = np.linalg.norm(P - (a + t[:, None] * ab), axis=1)
        rr = np.linalg.norm(a)
        w = G_HALF * (1.15 - 0.55 * min(rr / ROUT, 1.0))            # thinner as it runs out
        better = d < dist
        dist = np.where(better, d, dist)
        width = np.where(better, w, width)
dist = dist.reshape(X.shape)
width = width.reshape(X.shape)
groove = np.clip(1.0 - dist / width, 0, 1)
h = h - G_DEPTH * groove * (1.0 - 0.6 * sk)

alpha = 1.0 - sk
np.savez(os.path.join(OUT, f"crater_{SEED}_heights.npz"), x=xs, h=h.astype(np.float32), alpha=alpha.astype(np.float32),
         R=R, ROUT=ROUT, groove=groove.astype(np.float32), paths=np.array([len(p) for p in paths]))

# --- the emission guide in UV space (u = +x, v = -y: the image's rows run from +y down) ------------------------
S = 1024
us = np.linspace(-ROUT, ROUT, S)
GX, GY = np.meshgrid(us, us[::-1], indexing="xy")
PP = np.stack([GX.ravel(), GY.ravel()], 1)
dd = np.full(PP.shape[0], 9.0)
for pts in paths:
    q = np.array(pts)
    for i in range(len(q) - 1):
        a, b = q[i], q[i + 1]
        ab = b - a
        t = np.clip(((PP - a) @ ab) / max(ab @ ab, 1e-9), 0, 1)
        dd = np.minimum(dd, np.linalg.norm(PP - (a + t[:, None] * ab), axis=1))
dd = dd.reshape(GX.shape)
m = np.clip(1.0 - dd / G_HALF, 0, 1) * 0.8
centre = np.clip(1.0 - np.hypot(GX, GY) / (0.32 * R), 0, 1)
m = np.maximum(m, centre)
np.save(os.path.join(OUT, f"crater_{SEED}_cracks.npy"), (m * 255).astype(np.uint8))   # PNG made outside (no Pillow in Blender)

# --- the mesh ---------------------------------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
verts = [(float(X[j, i]), float(Y[j, i]), float(h[j, i])) for j in range(N) for i in range(N)]
faces = []
for j in range(N - 1):
    for i in range(N - 1):
        a = j * N + i
        faces.append((a, a + 1, a + N + 1, a + N))
me = bpy.data.meshes.new(f"crater_{SEED}")
me.from_pydata(verts, [], faces)
me.update()
uv = me.uv_layers.new(name="UVMap")
col = me.color_attributes.new(name="Col", type="FLOAT_COLOR", domain="POINT")
for k, v in enumerate(me.vertices):
    j, i = divmod(k, N)
    col.data[k].color = (1.0, 1.0, 1.0, float(alpha[j, i]))
for poly in me.polygons:
    for li in poly.loop_indices:
        vi = me.loops[li].vertex_index
        j, i = divmod(vi, N)
        uv.data[li].uv = (i / (N - 1), j / (N - 1))
for poly in me.polygons:
    poly.use_smooth = True
ob = bpy.data.objects.new(f"crater_{SEED}", me)
bpy.context.scene.collection.objects.link(ob)
mat = bpy.data.materials.new("crater")
ob.data.materials.append(mat)
me.color_attributes.active_color = col
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, f"crater_{SEED}.glb"), export_format="GLB", export_yup=True,
                          export_attributes=True, use_selection=False, export_vertex_color="ACTIVE",
                          export_active_vertex_color_when_no_material=True)
print(f"[crater_mesh] seed={SEED} R={R} verts={len(verts)} faces={len(faces)} cracks={len(paths)} runners={n_run} -> {OUT}")
