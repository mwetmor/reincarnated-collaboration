#!/usr/bin/env python3
"""C-9 knight3d step 4 (GATE M-a deliverable): build the knight in Blender.

Run headless:
    /opt/homebrew/bin/blender -b -noaudio \
        --python scripts/04_build_blender.py -- [--render]

What it builds
  * a STANDARD humanoid armature with Mixamo bone naming, so any humanoid clip
    retargets onto it (Rigify mapping is written into knight3d/out/skeleton.json);
  * every plate piece as a RIGID mesh parented to exactly ONE bone;
  * the sabaton split into a heel section (Foot) and a toe section (ToeBase),
    so the foot can break at the toe -- Matt's defect 1;
  * the mail skirt and the tabard as DEFORMING meshes, skinned;
  * the tabard's below-the-waist bone chain for R-C9-36 (rigid above the waist,
    a damped pendulum below it, 0.08-0.12 s lag, 4-8 deg on walk, no flutter);
  * a grip socket on the weapon for the far hand, and a weapon socket on the
    main hand, so the two grips cannot drift apart -- Matt's defect 3.

Dimensions come from knight3d/work/fit_result.json (the fit against the eight
approved stills), so the body that is BUILT is the body that was FITTED.
"""
import json, math, os, sys

import bpy
import bmesh
from mathutils import Vector, Matrix

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
K3 = os.path.join(ROOT, "knight3d")
WORK = os.path.join(K3, "work")
OUT = os.path.join(K3, "out")
os.makedirs(OUT, exist_ok=True)

ARGV = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

# ---------------------------------------------------------------- parameters

FALLBACK = dict(
    z_crown=1.800, z_neck=1.470, z_shoulder=1.350, z_elbow=1.185,
    z_waist=1.040, z_hip=0.941, z_knee=0.565, z_ankle=0.146,
    helm_rx=0.112, helm_ry=0.132, helm_rz=0.130, helm_y=0.010,
    visor_r=0.068, visor_y=0.095, gorget_r=0.112, gorget_h=0.085,
    chest_rx=0.190, chest_ry=0.132, chest_rz=0.175,
    waist_rx=0.152, waist_ry=0.112,
    fauld_r_top=0.172, fauld_r_bot=0.205, fauld_z_bot=0.860,
    skirt_r_top=0.198, skirt_r_bot=0.240, skirt_z_bot=0.745,
    tabard_half_w=0.185, tabard_y=0.150, tabard_z_bot=0.800, tabard_t=0.022,
    shoulder_x=0.205, pauldron_r=0.104,
    uparm_r=0.062, forearm_r=0.053, gauntlet_r=0.068,
    arm_len_upper=0.300, arm_len_fore=0.275,
    hip_x=0.098, thigh_r=0.090, shin_r=0.070, poleyn_r=0.082,
    foot_len=0.310, foot_w=0.100, foot_h=0.100, toe_frac=0.38, foot_heel_back=0.25,
    arm_L_pitch=6.0, arm_L_roll=7.0, fore_L_pitch=10.0,
    grip_x=0.351, grip_y=0.292, grip_z=1.259,
    leg_L_pitch=0.0, leg_L_splay=4.0, foot_L_yaw=14.0,
    leg_R_pitch=0.0, leg_R_splay=4.0, foot_R_yaw=-14.0,
    knee_L_pitch=0.0, knee_R_pitch=0.0,
)


def load_params():
    f = os.path.join(WORK, "fit_result.json")
    if os.path.exists(f):
        with open(f) as fh:
            r = json.load(fh)
        p = dict(FALLBACK); p.update(r["params"])
        return p, r
    return dict(FALLBACK), None


# ------------------------------------------------------------------ helpers

def rotz(deg):
    return Matrix.Rotation(math.radians(deg), 4, "Z")


def rotx(deg):
    return Matrix.Rotation(math.radians(deg), 4, "X")


def roty(deg):
    return Matrix.Rotation(math.radians(deg), 4, "Y")


def ik2(root, target, l1, l2, pole):
    root = Vector(root); target = Vector(target); pole = Vector(pole)
    d = target - root
    L = max(min(d.length, (l1 + l2) * 0.999), abs(l1 - l2) * 1.001)
    n = d.normalized()
    a = (l1 * l1 - l2 * l2 + L * L) / (2 * L)
    h = math.sqrt(max(l1 * l1 - a * a, 0.0))
    pv = pole - n * pole.dot(n)
    pv.normalize()
    return root + n * a + pv * h, root + n * L


def new_mesh(name, verts, faces):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob


def prim_sphere(name, centre, radii, mat=None, seg=20, ring=12):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=1.0)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    M = Matrix.Translation(Vector(centre)) @ (mat or Matrix.Identity(4)) \
        @ Matrix.Diagonal(Vector(radii).to_4d())
    ob.data.transform(M)
    return ob


def prim_cone(name, z0, r0, z1, r1, seg=24, centre_xy=(0.0, 0.0)):
    verts, faces = [], []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        verts.append((centre_xy[0] + r0 * math.cos(a), centre_xy[1] + r0 * math.sin(a), z0))
    for i in range(seg):
        a = 2 * math.pi * i / seg
        verts.append((centre_xy[0] + r1 * math.cos(a), centre_xy[1] + r1 * math.sin(a), z1))
    for i in range(seg):
        j = (i + 1) % seg
        faces.append([i, j, seg + j, seg + i])
    faces.append(list(range(seg - 1, -1, -1)))
    faces.append(list(range(seg, 2 * seg)))
    return new_mesh(name, verts, faces)


def prim_capsule(name, a, b, ra, rb, seg=16):
    a = Vector(a); b = Vector(b)
    w = (b - a)
    L = w.length
    w = w.normalized()
    tmp = Vector((0, 0, 1)) if abs(w.z) < 0.9 else Vector((1, 0, 0))
    e1 = w.cross(tmp).normalized()
    e2 = w.cross(e1)
    verts, faces = [], []
    rings = [(a - w * ra * 0.65, ra * 0.55), (a, ra), (b, rb), (b + w * rb * 0.65, rb * 0.55)]
    for c, r in rings:
        for i in range(seg):
            t = 2 * math.pi * i / seg
            verts.append(tuple(c + (e1 * math.cos(t) + e2 * math.sin(t)) * r))
    for k in range(len(rings) - 1):
        for i in range(seg):
            j = (i + 1) % seg
            faces.append([k * seg + i, k * seg + j, (k + 1) * seg + j, (k + 1) * seg + i])
    faces.append(list(range(seg - 1, -1, -1)))
    faces.append(list(range(3 * seg, 4 * seg)))
    return new_mesh(name, verts, faces)


def prim_box(name, centre, half, mat=None):
    hx, hy, hz = half
    v = [(sx * hx, sy * hy, sz * hz) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    f = [[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6],
         [0, 2, 6, 4], [1, 5, 7, 3]]
    ob = new_mesh(name, v, f)
    ob.data.transform(Matrix.Translation(Vector(centre)) @ (mat or Matrix.Identity(4)))
    return ob


def prim_wedge(name, centre, fw, fl, fh, mat=None):
    """The pointed sabaton toe: a box at the heel end tapering to a point."""
    v = [(-fw / 2, -fl / 2, -fh * 0.40), (fw / 2, -fl / 2, -fh * 0.40),
         (-fw / 2, -fl / 2, fh * 0.42), (fw / 2, -fl / 2, fh * 0.42),
         (-fw * 0.07, fl / 2, -fh * 0.34), (fw * 0.07, fl / 2, -fh * 0.34),
         (-fw * 0.07, fl / 2, fh * 0.02), (fw * 0.07, fl / 2, fh * 0.02)]
    f = [[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6],
         [0, 2, 6, 4], [1, 5, 7, 3]]
    ob = new_mesh(name, v, f)
    ob.data.transform(Matrix.Translation(Vector(centre)) @ (mat or Matrix.Identity(4)))
    return ob


def prim_panel(name, half_w, y, z_top, z_bot, thick, segs=6):
    """A hanging cloth panel, segmented vertically so it can deform."""
    verts, faces = [], []
    n = segs + 1
    for i in range(n):
        z = z_top + (z_bot - z_top) * i / segs
        for sx in (-1, 1):
            for sy in (-1, 1):
                verts.append((sx * half_w, y + sy * thick / 2, z))
    for i in range(segs):
        a = i * 4; b = (i + 1) * 4
        faces += [[a + 0, a + 2, b + 2, b + 0], [a + 1, b + 1, b + 3, a + 3],
                  [a + 0, b + 0, b + 1, a + 1], [a + 2, a + 3, b + 3, b + 2]]
    faces += [[0, 1, 3, 2], [(n - 1) * 4 + 2, (n - 1) * 4 + 3, (n - 1) * 4 + 1, (n - 1) * 4 + 0]]
    return new_mesh(name, verts, faces)


# --------------------------------------------------------------- the build

def build(p):
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)

    z_crown, z_neck = p["z_crown"], p["z_neck"]
    z_sh, z_waist, z_hip = p["z_shoulder"], p["z_waist"], p["z_hip"]
    z_knee, z_ank = p["z_knee"], p["z_ankle"]

    # ---- joint positions (the skeleton's rest pose) ----------------------
    J = {}
    J["Hips"] = Vector((0, 0, z_hip))
    J["Spine"] = Vector((0, 0, z_hip + 0.09))
    J["Spine1"] = Vector((0, 0, z_waist))
    J["Spine2"] = Vector((0, 0, 0.5 * (z_waist + z_sh) + 0.02))
    J["Neck"] = Vector((0, 0, z_sh + 0.055))
    J["Head"] = Vector((0, 0, z_neck))
    J["HeadTop_End"] = Vector((0, 0, z_crown))
    for side, sx in (("Left", -1.0), ("Right", 1.0)):
        J[side + "Shoulder"] = Vector((sx * 0.045, 0, z_sh + 0.045))
        sh = Vector((sx * p["shoulder_x"], 0.0, z_sh))
        J[side + "Arm"] = sh
        if side == "Right":
            el, wr = ik2(sh, Vector((p["grip_x"], p["grip_y"], p["grip_z"])),
                         p["arm_len_upper"], p["arm_len_fore"], Vector((0.35, -0.45, -1.0)))
        else:
            R1 = rotz(-sx * p["arm_L_roll"]) @ rotx(p["arm_L_pitch"])
            el = sh + (R1 @ Vector((0, 0, -p["arm_len_upper"])))
            R2 = R1 @ rotx(p["fore_L_pitch"])
            wr = el + (R2 @ Vector((0, 0, -p["arm_len_fore"])))
        J[side + "ForeArm"] = el
        J[side + "Hand"] = wr
        d = (wr - el).normalized()
        J[side + "HandEnd"] = wr + d * 0.115
        # legs
        hip = Vector((sx * p["hip_x"], 0.0, z_hip))
        S = "L" if side == "Left" else "R"
        Rl = roty(sx * p["leg_%s_splay" % S]) @ rotx(p["leg_%s_pitch" % S])
        knee = hip + (Rl @ Vector((0, 0, -(z_hip - z_knee))))
        Rk = Rl @ rotx(p["knee_%s_pitch" % S])
        ank = knee + (Rk @ Vector((0, 0, -(z_knee - z_ank))))
        fy = rotz(p["foot_%s_yaw" % S])
        fl, tf = p["foot_len"], p["toe_frac"]
        hb = p["foot_heel_back"]
        toe = ank + (fy @ Vector((0, fl * (1 - tf - hb), -(z_ank - p["foot_h"] * 0.5))))
        J[side + "UpLeg"] = hip
        J[side + "Leg"] = knee
        J[side + "Foot"] = ank
        J[side + "ToeBase"] = toe
        J[side + "Toe_End"] = toe + (fy @ Vector((0, fl * tf, -p["foot_h"] * 0.18)))

    # ---- armature ---------------------------------------------------------
    arm_data = bpy.data.armatures.new("KnightArmature")
    rig = bpy.data.objects.new("Knight_Rig", arm_data)
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm_data.edit_bones

    CHAIN = [
        ("Hips", None, "Spine"),
        ("Spine", "Hips", "Spine1"), ("Spine1", "Spine", "Spine2"),
        ("Spine2", "Spine1", "Neck"), ("Neck", "Spine2", "Head"),
        ("Head", "Neck", "HeadTop_End"),
    ]
    for side in ("Left", "Right"):
        CHAIN += [
            (side + "Shoulder", "Spine2", side + "Arm"),
            (side + "Arm", side + "Shoulder", side + "ForeArm"),
            (side + "ForeArm", side + "Arm", side + "Hand"),
            (side + "Hand", side + "ForeArm", side + "HandEnd"),
            (side + "UpLeg", "Hips", side + "Leg"),
            (side + "Leg", side + "UpLeg", side + "Foot"),
            (side + "Foot", side + "Leg", side + "ToeBase"),
            (side + "ToeBase", side + "Foot", side + "Toe_End"),
        ]
    made = {}
    for name, parent, tail_key in CHAIN:
        b = eb.new(name)
        b.head = J[name]
        b.tail = J[tail_key]
        if (b.tail - b.head).length < 1e-4:
            b.tail = b.head + Vector((0, 0, 0.02))
        made[name] = b
    for name, parent, _ in CHAIN:
        if parent:
            made[name].parent = made[parent]
            made[name].use_connect = (made[parent].tail - made[name].head).length < 1e-4

    # non-standard bones: prefixed so a humanoid retarget ignores them
    def extra(name, parent, head, tail):
        b = eb.new(name); b.head = Vector(head); b.tail = Vector(tail)
        b.parent = made[parent] if isinstance(parent, str) else parent
        made[name] = b
        return b

    # tabard: rigid above the waist, a 3-link damped pendulum below it (R-C9-36)
    tz0, tz1 = z_waist, p["tabard_z_bot"]
    for tag, ysign in (("F", 1.0), ("B", -1.0)):
        prev = "Hips"
        for i in range(3):
            a = tz0 + (tz1 - tz0) * i / 3.0
            b = tz0 + (tz1 - tz0) * (i + 1) / 3.0
            extra("TAB_%s_%02d" % (tag, i + 1), prev,
                  (0, ysign * p["tabard_y"], a), (0, ysign * p["tabard_y"], b))
            prev = "TAB_%s_%02d" % (tag, i + 1)
    # mail skirt: four quadrant links off the hips
    for tag, (dx, dy) in (("F", (0, 1)), ("B", (0, -1)), ("L", (-1, 0)), ("R", (1, 0))):
        extra("SKIRT_%s" % tag, "Hips",
              (dx * p["skirt_r_top"] * 0.6, dy * p["skirt_r_top"] * 0.6, z_hip - 0.02),
              (dx * p["skirt_r_bot"] * 0.7, dy * p["skirt_r_bot"] * 0.7, p["skirt_z_bot"]))
    # sockets
    hand = J["RightHand"]
    extra("SOCK_WeaponMain", "RightHand", hand, hand + Vector((0, 0, 0.12)))
    extra("SOCK_WeaponGripFar", "RightHand", hand + Vector((0, 0, 0.34)),
          hand + Vector((0, 0, 0.46)))
    lh = J["LeftHand"]
    extra("SOCK_OffHand", "LeftHand", lh, lh + Vector((0, 0, 0.10)))

    bpy.ops.object.mode_set(mode="OBJECT")

    # ---- meshes -----------------------------------------------------------
    rigid = []          # (object, bone)  -- parented to ONE bone, no skinning
    deform = []         # (object, [(bone, weight_rule)])

    hrz = p["helm_rz"]; hz = z_crown - hrz
    rigid.append((prim_sphere("helm", (0, p["helm_y"], hz),
                              (p["helm_rx"], p["helm_ry"], hrz)), "Head"))
    rigid.append((prim_sphere("visor", (0, p["visor_y"], hz - 0.012),
                              (p["visor_r"] * 0.85, p["visor_r"], p["visor_r"] * 0.78)), "Head"))
    rigid.append((prim_cone("gorget", z_neck - p["gorget_h"] / 2, p["gorget_r"] * 0.86,
                            z_neck + p["gorget_h"] / 2, p["gorget_r"]), "Neck"))
    z_chest = 0.5 * (z_sh + z_waist) + 0.02
    rigid.append((prim_sphere("breastplate", (0, 0.008, z_chest),
                              (p["chest_rx"], p["chest_ry"], p["chest_rz"])), "Spine2"))
    rigid.append((prim_sphere("waist_plate", (0, 0.0, z_waist - 0.02),
                              (p["waist_rx"], p["waist_ry"], 0.085)), "Spine"))
    rigid.append((prim_cone("fauld", z_hip + 0.055, p["fauld_r_top"],
                            p["fauld_z_bot"], p["fauld_r_bot"]), "Hips"))

    skirt = prim_cone("mail_skirt", z_hip - 0.02, p["skirt_r_top"],
                      p["skirt_z_bot"], p["skirt_r_bot"], seg=32)
    deform.append((skirt, "skirt"))
    for tag, ysign in (("front", 1.0), ("back", -1.0)):
        pan = prim_panel("tabard_" + tag, p["tabard_half_w"], ysign * p["tabard_y"],
                         z_sh + 0.03, p["tabard_z_bot"], p["tabard_t"])
        deform.append((pan, "tabard_" + ("F" if ysign > 0 else "B")))

    for side, sx, S in (("Left", -1.0, "L"), ("Right", 1.0, "R")):
        sh = J[side + "Arm"]; el = J[side + "ForeArm"]; wr = J[side + "Hand"]
        rigid.append((prim_sphere("pauldron_" + S, sh + Vector((sx * 0.03, 0, 0.015)),
                                  (p["pauldron_r"], p["pauldron_r"] * 1.10,
                                   p["pauldron_r"] * 0.95)), side + "Arm"))
        rigid.append((prim_capsule("rerebrace_" + S, sh, el, p["uparm_r"],
                                   p["uparm_r"] * 0.86), side + "Arm"))
        rigid.append((prim_sphere("couter_" + S, el, (p["uparm_r"] * 0.95,) * 3),
                      side + "ForeArm"))
        rigid.append((prim_capsule("vambrace_" + S, el, wr, p["forearm_r"],
                                   p["forearm_r"] * 0.82), side + "ForeArm"))
        d = (wr - el).normalized()
        rigid.append((prim_sphere("gauntlet_" + S, wr + d * 0.055,
                                  (p["gauntlet_r"] * 0.8, p["gauntlet_r"],
                                   p["gauntlet_r"] * 1.05)), side + "Hand"))
        hip = J[side + "UpLeg"]; knee = J[side + "Leg"]; ank = J[side + "Foot"]
        rigid.append((prim_capsule("cuisse_" + S, hip, knee, p["thigh_r"],
                                   p["thigh_r"] * 0.80), side + "UpLeg"))
        rigid.append((prim_sphere("poleyn_" + S, knee, (p["poleyn_r"], p["poleyn_r"] * 0.95,
                                                        p["poleyn_r"] * 0.88)), side + "Leg"))
        rigid.append((prim_capsule("greave_" + S, knee, ank, p["shin_r"] * 1.02,
                                   p["shin_r"] * 0.72), side + "Leg"))
        fy = rotz(p["foot_%s_yaw" % S])
        fl, fw, fh, tf = p["foot_len"], p["foot_w"], p["foot_h"], p["toe_frac"]
        hb = p["foot_heel_back"]
        heel_c = ank + (fy @ Vector((0, fl * ((1 - tf) / 2 - hb), 0))) \
            - Vector((0, 0, z_ank - fh / 2))
        rigid.append((prim_box("sabaton_" + S, heel_c,
                               (fw / 2, fl * (1 - tf) / 2, fh / 2), fy), side + "Foot"))
        toe_c = J[side + "ToeBase"] + (fy @ Vector((0, fl * tf / 2, 0)))
        rigid.append((prim_wedge("sabaton_toe_" + S, toe_c, fw, fl * tf, fh, fy),
                      side + "ToeBase"))

    # ---- attach -----------------------------------------------------------
    for ob, bone in rigid:
        ob.parent = rig
        ob.parent_type = "BONE"
        ob.parent_bone = bone
        # keep the world transform: bone parenting puts the child at the tail
        b = rig.data.bones[bone]
        ob.matrix_parent_inverse = (rig.matrix_world @ b.matrix_local
                                    @ Matrix.Translation(Vector((0, b.length, 0)))).inverted()

    for ob, kind in deform:
        mod = ob.modifiers.new("Armature", "ARMATURE")
        mod.object = rig
        if kind == "skirt":
            groups = {t: ob.vertex_groups.new(name="SKIRT_" + t) for t in "FBLR"}
            groups["Hips"] = ob.vertex_groups.new(name="Hips")
            for i, v in enumerate(ob.data.vertices):
                t = max(0.0, min(1.0, (z_hip - 0.02 - v.co.z) / max(z_hip - 0.02 - p["skirt_z_bot"], 1e-6)))
                groups["Hips"].add([i], 1.0 - t, "REPLACE")
                ang = math.atan2(v.co.y, v.co.x)
                w = {"R": max(0.0, math.cos(ang)), "L": max(0.0, -math.cos(ang)),
                     "F": max(0.0, math.sin(ang)), "B": max(0.0, -math.sin(ang))}
                tot = sum(w.values()) or 1.0
                for k, val in w.items():
                    groups[k].add([i], t * val / tot, "REPLACE")
        else:
            tag = kind.split("_")[1]
            g = {i: ob.vertex_groups.new(name="TAB_%s_%02d" % (tag, i)) for i in (1, 2, 3)}
            g0 = ob.vertex_groups.new(name="Hips")
            tz0, tz1 = z_waist, p["tabard_z_bot"]
            for i, v in enumerate(ob.data.vertices):
                if v.co.z >= tz0:                       # RIGID above the waist
                    g0.add([i], 1.0, "REPLACE"); continue
                t = (tz0 - v.co.z) / max(tz0 - tz1, 1e-6) * 3.0
                k = min(3, max(1, int(math.ceil(t)) or 1))
                g[k].add([i], 1.0, "REPLACE")
        ob.parent = rig

    return rig, J, [(o.name, b) for o, b in rigid], [o.name for o, _ in deform]


# ---------------------------------------------------------------- rendering

def setup_render(W, H):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.resolution_x = W
    sc.render.resolution_y = H
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.display.shading.light = "FLAT"
    sc.display.shading.color_type = "SINGLE"
    sc.display.shading.single_color = (1, 1, 1)
    sc.display.render_aa = "OFF"


def place_camera(cam, alpha, theta, s, tx, ty, W, H):
    """Match knight_proxy's projection exactly: px = (p.r)s + tx, py = -(p.u)s + ty."""
    a = math.radians(alpha); t = math.radians(theta)
    r = Vector((-math.cos(a), math.sin(a), 0.0))
    u = Vector((-math.sin(t) * math.sin(a), -math.sin(t) * math.cos(a), math.cos(t)))
    c = Vector((math.sin(a) * math.cos(t), math.cos(a) * math.cos(t), math.sin(t)))
    uc = (W / 2.0 - tx) / s
    vc = (ty - H / 2.0) / s
    aim = r * uc + u * vc
    cam.matrix_world = Matrix((
        (r.x, u.x, c.x, (aim + c * 12.0).x),
        (r.y, u.y, c.y, (aim + c * 12.0).y),
        (r.z, u.z, c.z, (aim + c * 12.0).z),
        (0.0, 0.0, 0.0, 1.0)))
    cam.data.type = "ORTHO"
    cam.data.sensor_fit = "VERTICAL"
    cam.data.ortho_scale = H / s
    cam.data.clip_start = 0.1
    cam.data.clip_end = 60.0


def main():
    p, fit = load_params()
    if "--pose-fitted" in ARGV and fit is not None:
        pass          # the per-view pose is applied per render, below
    rig, J, rigid_pairs, deform_names = build(p)

    meta = dict(
        note="C-9 knight3d M-a: fitted knight proxy, standard humanoid skeleton.",
        skeleton_standard="Mixamo humanoid (bone names as emitted by Mixamo without "
                          "the 'mixamorig:' namespace); any Mixamo/Rigify humanoid "
                          "clip retargets onto it.",
        rigify_map={
            "Hips": "spine", "Spine": "spine.001", "Spine1": "spine.002",
            "Spine2": "spine.003", "Neck": "spine.004", "Head": "spine.006",
            "LeftShoulder": "shoulder.L", "LeftArm": "upper_arm.L",
            "LeftForeArm": "forearm.L", "LeftHand": "hand.L",
            "RightShoulder": "shoulder.R", "RightArm": "upper_arm.R",
            "RightForeArm": "forearm.R", "RightHand": "hand.R",
            "LeftUpLeg": "thigh.L", "LeftLeg": "shin.L", "LeftFoot": "foot.L",
            "LeftToeBase": "toe.L", "RightUpLeg": "thigh.R", "RightLeg": "shin.R",
            "RightFoot": "foot.R", "RightToeBase": "toe.R"},
        non_standard_bones={
            "TAB_F_01..03 / TAB_B_01..03":
                "tabard pendulum below the waist (R-C9-36); above the waist the "
                "tabard is weighted 1.0 to Hips and is RIGID",
            "SKIRT_F/B/L/R": "mail-skirt quadrant links",
            "SOCK_WeaponMain": "weapon parent socket on the main (right) hand",
            "SOCK_WeaponGripFar": "far-hand grip socket up the haft; the off hand "
                                  "IK-locks to it so it cannot drift (Matt defect 3)",
            "SOCK_OffHand": "off-hand attachment"},
        bones=[b.name for b in rig.data.bones],
        rigid_pieces={n: b for n, b in rigid_pairs},
        deforming_pieces=deform_names,
        joints={k: [round(v.x, 4), round(v.y, 4), round(v.z, 4)] for k, v in J.items()},
        params=p,
    )
    with open(os.path.join(OUT, "skeleton.json"), "w") as f:
        json.dump(meta, f, indent=1)

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "knight_body.blend"))
    print("saved", os.path.join(OUT, "knight_body.blend"))

    if "--render" in ARGV and fit is not None:
        cam_d = bpy.data.cameras.new("Cam")
        cam = bpy.data.objects.new("Cam", cam_d)
        bpy.context.collection.objects.link(cam)
        bpy.context.scene.camera = cam
        W, H = 1024, 1536
        setup_render(W, H)
        outdir = os.path.join(OUT, "silhouettes")
        os.makedirs(outdir, exist_ok=True)
        which = fit["pose_fitted"] if "--pose-fitted" in ARGV else fit["canonical"]
        for d, v in which["views"].items():
            if "--pose-fitted" in ARGV and v.get("delta"):
                pv = dict(p)
                for k, dv in v["delta"].items():
                    pv[k] = p[k] + dv
                build(pv)
                cam_d = bpy.data.cameras.new("Cam")
                cam = bpy.data.objects.new("Cam", cam_d)
                bpy.context.collection.objects.link(cam)
                bpy.context.scene.camera = cam
                setup_render(W, H)
            place_camera(cam, v["alpha"], fit["theta_elevation_deg"],
                         v["scale"] * fit["downsample"],
                         v["tx"] * fit["downsample"], v["ty"] * fit["downsample"], W, H)
            bpy.context.scene.render.filepath = os.path.join(outdir, "%s.png" % d)
            bpy.ops.render.render(write_still=True)
            print("rendered", d)


main()
