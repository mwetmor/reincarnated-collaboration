# R-C9-98: WHERE TO HANG THE GRIMOIRE. s29 found the first placement (outside the left hip, measured off the shift's flare)
# inside her in every idle frame (the thigh swings into it) and 2 mm from her left hand in the run.
#   blender -b -noaudio --python s30_book_search.py -- <body.glb> <out.npz> [--step 2]     (DUMP: per-frame Hips matrix and
#        the posed body vertices whose dominant bone is near the book's possible homes)
#   python3 s30_book_search.py --search <dump.npz> <out.json>                               (SEARCH in numpy)
# The book is rigid on Hips, so a candidate is a box in the Hips frame; per frame it moves with Hips. Score: body vertices
# inside the box grown by MARGIN (penetration + near-contact), worst over all frames, and the minimum hand clearance.
import sys, json
import numpy as np
MARGIN = 0.015
SIZE = np.array([0.064, 0.20, 0.26])     # thickness (x), width (y), height (z) of the 26 cm book in the rest frame
if "--search" in sys.argv:
    D = np.load(sys.argv[sys.argv.index("--search") + 1]); OUT = sys.argv[sys.argv.index("--search") + 2]
    Hr = D["hips_rest"]; Hf = D["hips"]; V = D["verts"]; fr = D["frame_clip"]; dom = D["dom"]; names = list(D["dom_names"])
    belt_z = float(D["belt_z"])
    handmask = np.isin(dom, [names.index(n) for n in ("LeftHand", "LeftForeArm") if n in names])
    best = []
    # candidates: centre (x out, y back, z below the belt) and a yaw about Z (0 = cover facing +X, out of her left hip)
    for x in (0.20, 0.23, 0.26):
        for y in (-0.02, 0.04, 0.08, 0.12, 0.16):
            for dz in (0.10, 0.14, 0.18):
                for yaw in (0, 30, 60, 90):
                    c = np.array([x, y, belt_z - dz]); t = np.radians(yaw)
                    R = np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])
                    worst, hand = 0, 9.0
                    for k in range(len(Hf)):
                        M = Hf[k] @ np.linalg.inv(Hr)          # rest world -> this frame's world, for anything rigid on Hips
                        Mi = np.linalg.inv(M)
                        P = V[k] @ Mi[:3, :3].T + Mi[:3, 3]      # body verts taken back into the rest frame of the book
                        L = (P - c) @ R                          # into the book's own axes
                        inn = np.all(np.abs(L) < SIZE / 2 + MARGIN, axis=1)
                        worst = max(worst, int((inn & ~handmask).sum()))
                        if handmask.any():
                            q = np.maximum(np.abs(L[handmask]) - SIZE / 2, 0)
                            hand = min(hand, float(np.linalg.norm(q, axis=1).min()))
                    best.append(dict(x=x, y=y, dz=dz, yaw=yaw, worst_inside=worst, hand_clear=round(hand, 4)))
    best.sort(key=lambda r: (r["worst_inside"] > 0, -min(r["hand_clear"], 0.06), r["worst_inside"], abs(r["y"])))
    json.dump(dict(margin=MARGIN, size=SIZE.tolist(), ranked=best), open(OUT, "w"), indent=1)
    for r in best[:12]:
        print("CAND", r)
    raise SystemExit(0)

import bpy
a = sys.argv[sys.argv.index('--') + 1:]
BODY, OUT = a[0], a[1]
STEP = int(a[a.index('--step') + 1]) if '--step' in a else 2
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = next(o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.data.vertices) > 1000)
gi = {g.index: g.name for g in body.vertex_groups}
domn = [gi[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else "" for v in body.data.vertices]
REG = ("Hips", "LeftUpLeg", "LeftLeg", "LeftHand", "LeftForeArm", "Spine", "Spine01") if "--right" not in a else ("Hips", "RightUpLeg", "RightLeg", "RightHand", "RightForeArm", "Spine", "Spine01")
names = list(REG)
sel = np.array([i for i, n in enumerate(domn) if n in REG])[::2]
dom = np.array([names.index(domn[i]) for i in sel])


def world(dg):
    oe = body.evaluated_get(dg); me = oe.to_mesh()
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); oe.to_mesh_clear()
    M = np.array(body.matrix_world); return (co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3])[sel]


arm.animation_data.action = None
for pb in arm.pose.bones: pb.matrix_basis.identity()
bpy.context.view_layer.update()
hips_rest = np.array(arm.matrix_world @ arm.pose.bones["Hips"].matrix)
co = np.empty(len(body.data.vertices) * 3); body.data.vertices.foreach_get("co", co)
Mb = np.array(body.matrix_world); BW = co.reshape(-1, 3) @ Mb[:3, :3].T + Mb[:3, 3]
H = BW[:, 2].max() - BW[:, 2].min(); belt_z = BW[:, 2].min() + 0.585 * H
hips, verts, fc = [], [], []
carry = None
if "--right" in a and "staff_carry_R" in bpy.data.actions:
    # the right arm UNDER THE CARRY LAYER (idle/walk/run in the scene): the carry action poses the spine + right arm; the
    # hand's position relative to Hips is then fixed while the legs walk. Dumped once, in the Hips frame.
    arm.animation_data.action = bpy.data.actions["staff_carry_R"]; sc.frame_set(0); bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get(); Wc = world(dg)
    Hc = np.array(arm.matrix_world @ arm.pose.bones["Hips"].matrix)
    Mi = np.linalg.inv(Hc @ np.linalg.inv(hips_rest)); carry = Wc @ Mi[:3, :3].T + Mi[:3, 3]
for act in bpy.data.actions:
    if act.name.startswith("staff_carry"):
        continue
    arm.animation_data.action = act
    f0, f1 = map(int, act.frame_range)
    for f in range(f0, f1 + 1, STEP):
        sc.frame_set(f); bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
        hips.append(np.array(arm.matrix_world @ arm.pose.bones["Hips"].matrix)); verts.append(world(dg)); fc.append("%s:%d" % (act.name, f))
np.savez_compressed(OUT, carry=carry if carry is not None else np.zeros((0, 3)), hips_rest=hips_rest, hips=np.array(hips), verts=np.array(verts, np.float32), frame_clip=np.array(fc),
                    dom=dom, dom_names=np.array(names), belt_z=belt_z)
print("DUMP %d frames, %d verts each, belt z %.3f" % (len(hips), len(sel), belt_z))
