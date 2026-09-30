# T8 step 1: which way does he face, which side is his right, and where on the
# surface is the tattoo?
#
#   blender -b -noaudio --python scripts/04_surface.py -- <glb> <outdir>
#
# FACING IS MEASURED, NOT INHERITED. A note in an earlier script says the model
# faces -Y; that is the east/west check itself, and the whole tattoo defect is
# a sidedness error, so it is the one claim in this pipeline that must not be
# taken on trust. Two independent features are used and they have to agree:
# the toes (a foot points forward) and the face (nose and beard protrude).
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUT = a[0], a[1]
SIZE = int(a[a.index("--size") + 1]) if "--size" in a else 2048
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
objs = [o for o in sc.objects if o.type == 'MESH']
ob = max(objs, key=lambda o: len(o.data.vertices))
me = ob.data
me.calc_loop_triangles()
M = ob.matrix_world
co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
V = co.reshape(-1, 3) @ np.array(M.to_3x3()).T + np.array(M.translation)
lo, hi = V.min(0), V.max(0)
H = hi[2] - lo[2]
print("mesh %s: %d verts, %d tris, bbox %s .. %s (H %.4f)"
      % (ob.name, len(V), len(me.loop_triangles), np.round(lo, 4), np.round(hi, 4), H))

# Both features must be referenced to the LIMB THEY HANG OFF, not to their own
# midpoint. Measured about its own median a foot is nearly symmetric -- it is a
# foot's LENGTH, heel to toe -- and so is a skull, front to back. The first
# version of this check did exactly that and returned +0.1713/-0.1742 and
# +0.1211/-0.1206: two clean numbers, both 50/50, neither answering the
# question. The asymmetry is the foot against the ANKLE and the nose against
# the SKULL.
#
# --- instrument 1: the foot against the leg above it ------------------------
# The horizontal axis is SEARCHED, not assumed to be Y. Tripo delivers the
# model yawed 90 degrees, so a probe hard-coded to Y would measure the width of
# a foot instead of its length and return a coin flip.
shin = V[(V[:, 2] > lo[2] + 0.10 * H) & (V[:, 2] < lo[2] + 0.20 * H)]
feet = V[V[:, 2] < lo[2] + 0.04 * H]
cands = []
for ax in (0, 1):
    c = float(np.median(shin[:, ax]))
    reach = (feet[:, ax].max() - c, c - feet[:, ax].min())
    cands.append((abs(reach[0] - reach[1]), ax, 1 if reach[0] > reach[1] else -1, c, reach))
cands.sort(reverse=True)
asym, FAX, toe_dir, c, reach = cands[0]
# THE FOOT PROBE MUST CLEAR A MARGIN OR STAND DOWN. On the Meshy build it won
# 3:1 and was right. On the Tripo build it won 1.3:1 (0.118 against 0.089) and
# was WRONG -- that figure wears boots, and a boot is far more symmetric than a
# bare foot, so the toe no longer carries the asymmetry. A ratio that close is
# not a measurement, it is a coin flip with a decimal point. --face overrides
# it when the answer is known from paint (see scripts/11_compare.py, which
# decides orientation by colour because silhouette cannot).
FACE_ARG = a[a.index("--face") + 1] if "--face" in a else None
if FACE_ARG:
    FAX = "XY".index(FACE_ARG[1]); toe_dir = 1 if FACE_ARG[0] == "+" else -1
    print("  foot probe OVERRIDDEN by --face %s" % FACE_ARG)
elif asym < 1.5 * cands[1][0]:
    raise SystemExit(
        "foot probe cannot decide: %s asymmetry %.4f vs %s %.4f, ratio %.2f "
        "(needs 1.5). Pass --face +X / -Y / ... from the colour-fitted "
        "orientation." % ("XY"[FAX], asym, "XY"[cands[1][1]], cands[1][0],
                          asym / max(cands[1][0], 1e-9)))
print("  foot:  %d verts; axis %s wins with asymmetry %.4f (other axis %.4f)"
      % (len(feet), "XY"[FAX], asym, cands[1][0]))
print("         leg axis %s=%.4f, foot reaches +%.4f / -%.4f  -> front is %s%s"
      % ("XY"[FAX], c, reach[0], reach[1], "+" if toe_dir > 0 else "-", "XY"[FAX]))

# --- instrument 2: the nose at the midline, against the skull ---------------
head = V[V[:, 2] > lo[2] + 0.88 * H]
SAX = 1 - FAX
xc = float(np.median(head[:, SAX]))
mid = head[np.abs(head[:, SAX] - xc) < 0.015 * H]
y_sk = float(np.median(head[:, FAX]))
my = mid[:, FAX]
face_dir = 1 if (my.max() - y_sk) > (y_sk - my.min()) else -1
print("  nose:  %d midline verts, skull y %.4f, midline reaches +%.4f / -%.4f"
      "  -> front is %sY" % (len(mid), y_sk, my.max() - y_sk, y_sk - my.min(),
                             "+" if face_dir > 0 else "-"))
# The foot decides. It is 3:1 asymmetric about the leg axis and a foot cannot
# point backwards. The nose test is KEPT AND REPORTED but is not allowed a
# vote on this character: long hair behind and a full beard in front balance
# the midline almost exactly (+0.1211 / -0.1206), so it is not measuring a
# face, it is measuring a hairstyle. An instrument that cannot discriminate
# must say so rather than cast a coin-flip vote.
nose_discriminates = abs((my.max() - y_sk) - (y_sk - my.min())) > 0.02 * H
print("  nose test discriminates on this character: %s (asymmetry %.4f, needs "
      "> %.4f)" % (nose_discriminates,
                   abs((my.max() - y_sk) - (y_sk - my.min())), 0.02 * H))
if nose_discriminates:
    assert toe_dir == face_dir, ("foot and nose disagree about which way he "
                                 "faces (%+d vs %+d)" % (toe_dir, face_dir))
fwd = np.zeros(3); fwd[FAX] = float(toe_dir)
up = np.array([0.0, 0.0, 1.0])
right = np.cross(fwd, up)          # facing f with up u, a person's right is f x u
RAX = int(np.argmax(np.abs(right)))
print("  FACING %s%s, up +Z  =>  his RIGHT is %s%s"
      % ("+" if toe_dir > 0 else "-", "XY"[FAX],
         "+" if right[RAX] > 0 else "-", "XY"[RAX]))

# --- the texture, and where each texel sits on him --------------------------
img = None
for s in ob.material_slots:
    if s.material and s.material.node_tree:
        for n in s.material.node_tree.nodes:
            if n.type == 'TEX_IMAGE' and n.image:
                img = n.image
assert img is not None, "no image texture on the mesh"
print("  texture %s %dx%d" % (img.name, img.size[0], img.size[1]))
img.filepath_raw = os.path.join(OUT, "base_texture.png")
img.file_format = 'PNG'
img.save()

uvl = me.uv_layers.active.data
UVL = np.empty(len(uvl) * 2); uvl.foreach_get("uv", UVL)
UVL = UVL.reshape(-1, 2)
TRI = np.array([list(t.vertices) for t in me.loop_triangles], np.int64)
TL = np.array([list(t.loops) for t in me.loop_triangles], np.int64)
TP = UVL[TL] * np.array([SIZE, SIZE])
A3, B3, C3 = V[TRI[:, 0]], V[TRI[:, 1]], V[TRI[:, 2]]
tex_pos = np.zeros((SIZE, SIZE, 3), np.float32)
tex_on = np.zeros((SIZE, SIZE), bool)
for i in range(len(TRI)):
    p = TP[i]
    x0 = max(int(np.floor(p[:, 0].min())), 0); x1 = min(int(np.ceil(p[:, 0].max())) + 1, SIZE)
    y0 = max(int(np.floor(p[:, 1].min())), 0); y1 = min(int(np.ceil(p[:, 1].max())) + 1, SIZE)
    if x1 <= x0 or y1 <= y0:
        continue
    X, Y = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
    d = ((p[1, 1] - p[2, 1]) * (p[0, 0] - p[2, 0]) + (p[2, 0] - p[1, 0]) * (p[0, 1] - p[2, 1]))
    if abs(d) < 1e-12:
        continue
    l0 = ((p[1, 1] - p[2, 1]) * (X - p[2, 0]) + (p[2, 0] - p[1, 0]) * (Y - p[2, 1])) / d
    l1 = ((p[2, 1] - p[0, 1]) * (X - p[2, 0]) + (p[0, 0] - p[2, 0]) * (Y - p[2, 1])) / d
    l2 = 1.0 - l0 - l1
    m = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
    if not m.any():
        continue
    yy, xx = np.where(m)
    tex_pos[yy + y0, xx + x0] = (l0[m][:, None] * A3[i] + l1[m][:, None] * B3[i]
                                 + l2[m][:, None] * C3[i])
    tex_on[yy + y0, xx + x0] = True
np.savez(os.path.join(OUT, "surface.npz"), tex_pos=tex_pos.astype(np.float16),
         tex_on=tex_on, bbox=np.stack([lo, hi]), fwd=fwd, right=right,
         size=np.array([SIZE]))
json.dump(dict(facing_axis=("+" if toe_dir > 0 else "-") + "XY"[FAX],
               right_axis=("+" if right[RAX] > 0 else "-") + "XY"[RAX],
               yaw_vs_minusY_deg=int(round(math.degrees(math.atan2(
                   -fwd[0], -fwd[1])))) % 360,
               height_m=round(float(H), 5),
               bbox_lo=[round(float(v), 5) for v in lo],
               bbox_hi=[round(float(v), 5) for v in hi],
               texture=[img.size[0], img.size[1]],
               verts=int(len(V)), tris=int(len(TRI)),
               uv_coverage_pct=round(100 * float(tex_on.mean()), 3)),
          open(os.path.join(OUT, "surface.json"), "w"), indent=1)
print("  uv coverage %.2f%%; wrote %s" % (100 * tex_on.mean(), OUT))
