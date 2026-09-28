#!/usr/bin/env python3
"""C-9 knight3d: build the knight in Blender from the FITTED parts.

    /opt/homebrew/bin/blender -b -noaudio --python scripts/04_build_blender.py \
        -- [--render] [--pose-fitted]

Geometry is NOT authored here. 07_export_parts.py emits out/parts_mesh.npz
from knight_proxy.build_parts() -- the same function the fitter optimises --
and this script only assembles it. That is the M-a lesson made structural: a
mesh written twice drifts from the solid that was fitted, and it did, by 6.6 %.

What it assembles
  * a STANDARD humanoid armature, Mixamo bone naming, so any humanoid clip
    retargets (Rigify map in out/skeleton.json);
  * every plate piece RIGID, parented to exactly one bone;
  * the sabaton split heel (Foot) / pointed toe (ToeBase) -- Matt defect 1;
  * mail skirt and tabard SKINNED; the tabard rigid above the waist over a
    3-link damped chain below it -- R-C9-36;
  * the POLLAXE as one rigid mesh on SOCK_WeaponMain, with SOCK_WeaponGripFar
    up the haft for the off hand to IK-lock to -- Matt defect 3, by construction;
  * one packed UV atlas across every piece, for the projection paint.

Exports out/mesh_atlas.npz (world-rest triangles + UVs + piece ids) so the
projector and the ink pass work on exactly this mesh.
"""
import json, math, os, sys

import bpy
import bmesh
import numpy as np
from mathutils import Vector, Matrix

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
K3 = os.path.join(ROOT, "knight3d")
WORK = os.path.join(K3, "work"); OUT = os.path.join(K3, "out")
sys.path.insert(0, os.path.join(K3, "scripts"))
import knight_proxy as kp

ARGV = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
os.makedirs(OUT, exist_ok=True)


def clear():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)


def make_armature(p):
    J = kp.joints(p)
    ad = bpy.data.armatures.new("KnightArmature")
    rig = bpy.data.objects.new("Knight_Rig", ad)
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="EDIT")
    eb = ad.edit_bones

    CHAIN = [("Hips", None, "Spine"), ("Spine", "Hips", "Spine1"),
             ("Spine1", "Spine", "Spine2"), ("Spine2", "Spine1", "Neck"),
             ("Neck", "Spine2", "Head"), ("Head", "Neck", "HeadTop_End"),
             ("HeadTop_End", "Head", None)]
    for s in ("Left", "Right"):
        CHAIN += [(s + "Shoulder", "Spine2", s + "Arm"),
                  (s + "Arm", s + "Shoulder", s + "ForeArm"),
                  (s + "ForeArm", s + "Arm", s + "Hand"),
                  (s + "Hand", s + "ForeArm", s + "HandEnd"),
                  (s + "HandEnd", s + "Hand", None),
                  (s + "UpLeg", "Hips", s + "Leg"),
                  (s + "Leg", s + "UpLeg", s + "Foot"),
                  (s + "Foot", s + "Leg", s + "ToeBase"),
                  (s + "ToeBase", s + "Foot", s + "Toe_End"),
                  (s + "Toe_End", s + "ToeBase", None)]
    made = {}
    for name, parent, tail in CHAIN:
        b = eb.new(name)
        b.head = Vector(J[name])
        if tail is not None:
            b.tail = Vector(J[tail])
        else:                                   # leaf bones (Mixamo has them)
            b.tail = Vector(J[name]) + Vector((0, 0, 0.04))
        if (b.tail - b.head).length < 1e-4:
            b.tail = b.head + Vector((0, 0, 0.02))
        made[name] = b
    for name, parent, _ in CHAIN:
        if parent:
            made[name].parent = made[parent]
            made[name].use_connect = (made[parent].tail - made[name].head).length < 1e-4

    def extra(name, parent, head, tail):
        b = eb.new(name); b.head = Vector(head); b.tail = Vector(tail)
        b.parent = made[parent]; made[name] = b

    z_waist, tzb = p["z_waist"], p["tabard_z_bot"]
    for tag, ys in (("F", 1.0), ("B", -1.0)):
        prev = "Hips"
        for i in range(3):
            a = z_waist + (tzb - z_waist) * i / 3.0
            b = z_waist + (tzb - z_waist) * (i + 1) / 3.0
            nm = "TAB_%s_%02d" % (tag, i + 1)
            extra(nm, prev, (0, ys * p["tabard_y"], a), (0, ys * p["tabard_y"], b))
            prev = nm
    for tag, (dx, dy) in (("F", (0, 1)), ("B", (0, -1)), ("L", (-1, 0)), ("R", (1, 0))):
        extra("SKIRT_%s" % tag, "Hips",
              (dx * p["skirt_r_top"] * 0.6, dy * p["skirt_r_top"] * 0.6, p["z_hip"] - 0.02),
              (dx * p["skirt_r_bot"] * 0.7, dy * p["skirt_r_bot"] * 0.7, p["skirt_z_bot"]))

    hand = Vector(J["RightHand"])
    extra("SOCK_WeaponMain", "RightHand", hand, hand + Vector((0, 0, 0.12)))
    # the far-hand grip socket, up the haft: the off hand IK-locks HERE, so the
    # two grips cannot drift apart (Matt defect 3)
    extra("SOCK_WeaponGripFar", "SOCK_WeaponMain", hand + Vector((0, 0, 0.30)),
          hand + Vector((0, 0, 0.42)))
    lh = Vector(J["LeftHand"])
    extra("SOCK_OffHand", "LeftHand", lh, lh + Vector((0, 0, 0.10)))
    bpy.ops.object.mode_set(mode="OBJECT")
    return rig, J


def add_mesh(name, verts, faces):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [list(map(int, f)) for f in faces])
    me.validate()
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob


def bone_parent(ob, rig, bone):
    """Parent to ONE bone and keep the world transform."""
    ob.parent = rig
    ob.parent_type = "BONE"
    ob.parent_bone = bone
    b = rig.data.bones[bone]
    ob.matrix_parent_inverse = (rig.matrix_world @ b.matrix_local
                                @ Matrix.Translation(Vector((0, b.length, 0)))).inverted()


def skin_skirt(ob, rig, p):
    m = ob.modifiers.new("Armature", "ARMATURE"); m.object = rig
    g = {t: ob.vertex_groups.new(name="SKIRT_" + t) for t in "FBLR"}
    g0 = ob.vertex_groups.new(name="Hips")
    z0, z1 = p["z_hip"] - 0.02, p["skirt_z_bot"]
    for i, v in enumerate(ob.data.vertices):
        t = max(0.0, min(1.0, (z0 - v.co.z) / max(z0 - z1, 1e-6)))
        g0.add([i], 1.0 - t, "REPLACE")
        ang = math.atan2(v.co.y, v.co.x)
        w = {"R": max(0.0, math.cos(ang)), "L": max(0.0, -math.cos(ang)),
             "F": max(0.0, math.sin(ang)), "B": max(0.0, -math.sin(ang))}
        tot = sum(w.values()) or 1.0
        for k, val in w.items():
            g[k].add([i], t * val / tot, "REPLACE")
    ob.parent = rig


def skin_tabard(ob, rig, p, tag):
    """R-C9-36: heavy wool. RIGID above the waist (weight 1.0 to Hips); below it
    a 3-link chain that the animator drives as a damped pendulum lagging
    0.08-0.12 s, 4-8 deg on walk, no flutter."""
    m = ob.modifiers.new("Armature", "ARMATURE"); m.object = rig
    gs = {i: ob.vertex_groups.new(name="TAB_%s_%02d" % (tag, i)) for i in (1, 2, 3)}
    g0 = ob.vertex_groups.new(name="Hips")
    z0, z1 = p["z_waist"], p["tabard_z_bot"]
    for i, v in enumerate(ob.data.vertices):
        if v.co.z >= z0:
            g0.add([i], 1.0, "REPLACE"); continue
        t = (z0 - v.co.z) / max(z0 - z1, 1e-6) * 3.0
        lo = int(math.floor(t)); f = t - lo
        lo = max(0, min(2, lo))
        a, b = lo + 1, min(3, lo + 2)
        if a == b:
            gs[a].add([i], 1.0, "REPLACE")
        else:
            gs[a].add([i], 1.0 - f, "REPLACE"); gs[b].add([i], f, "REPLACE")
    ob.parent = rig


def unwrap_all(objs):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    try:
        bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.006,
                                 correct_aspect=True, scale_to_bounds=False)
    except TypeError:
        bpy.ops.uv.smart_project(island_margin=0.006)
    bpy.ops.uv.select_all(action="SELECT")
    try:
        bpy.ops.uv.pack_islands(margin=0.004, rotate=True)
    except TypeError:
        bpy.ops.uv.pack_islands(margin=0.004)
    bpy.ops.object.mode_set(mode="OBJECT")


def export_atlas(objs, index):
    tri_v, tri_uv, tri_id, names = [], [], [], []
    for ob in objs:
        me = ob.data
        me.calc_loop_triangles()
        uvl = me.uv_layers.active.data
        M = ob.matrix_world
        co = {i: (M @ v.co) for i, v in enumerate(me.vertices)}
        pid = len(names); names.append(ob.name)
        for lt in me.loop_triangles:
            tri_v.append([list(co[vi]) for vi in lt.vertices])
            tri_uv.append([list(uvl[li].uv) for li in lt.loops])
            tri_id.append(pid)
    np.savez_compressed(
        os.path.join(OUT, "mesh_atlas.npz"),
        tri_v=np.array(tri_v, np.float32), tri_uv=np.array(tri_uv, np.float32),
        tri_id=np.array(tri_id, np.int32), names=np.array(names))
    return names, len(tri_v)


def setup_render(W, H):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.resolution_x = W; sc.render.resolution_y = H
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.display.shading.light = "FLAT"
    sc.display.shading.color_type = "SINGLE"
    sc.display.shading.single_color = (1, 1, 1)
    sc.display.render_aa = "OFF"


def place_camera(cam, alpha, theta, s, tx, ty, W, H):
    """Match knight_proxy's projection exactly:
       px = (p.r)*s + tx ,  py = -(p.u)*s + ty."""
    a = math.radians(alpha); t = math.radians(theta)
    r = Vector((-math.cos(a), math.sin(a), 0.0))
    u = Vector((-math.sin(t) * math.sin(a), -math.sin(t) * math.cos(a), math.cos(t)))
    c = Vector((math.sin(a) * math.cos(t), math.cos(a) * math.cos(t), math.sin(t)))
    aim = r * ((W / 2.0 - tx) / s) + u * ((ty - H / 2.0) / s)
    P = aim + c * 12.0
    cam.matrix_world = Matrix(((r.x, u.x, c.x, P.x), (r.y, u.y, c.y, P.y),
                               (r.z, u.z, c.z, P.z), (0.0, 0.0, 0.0, 1.0)))
    cam.data.type = "ORTHO"
    cam.data.sensor_fit = "VERTICAL"
    cam.data.ortho_scale = H / s
    cam.data.clip_start = 0.1; cam.data.clip_end = 60.0


def main():
    idx = json.load(open(os.path.join(OUT, "parts_index.json")))
    p = idx["params"]
    mesh = np.load(os.path.join(OUT, "parts_mesh.npz"))
    clear()
    rig, J = make_armature(p)

    objs = []
    for name, info in idx["parts"].items():
        ob = add_mesh(name, mesh[name + "__v"], mesh[name + "__f"])
        if info["kind"] == "deform_skirt":
            skin_skirt(ob, rig, p)
        elif info["kind"].startswith("deform_tabard"):
            skin_tabard(ob, rig, p, info["kind"][-1])
        else:
            bone_parent(ob, rig, info["bone"])
        objs.append(ob)

    unwrap_all(objs)
    names, ntri = export_atlas(objs, idx)

    meta = dict(
        note="C-9 knight3d: fitted knight, standard humanoid skeleton. Geometry "
             "comes from knight_proxy.build_parts() via 07_export_parts.py; this "
             "script only assembles it.",
        skeleton_standard="Mixamo humanoid naming (without the 'mixamorig:' "
                          "namespace); any Mixamo/Rigify humanoid clip retargets.",
        rigify_map={"Hips": "spine", "Spine": "spine.001", "Spine1": "spine.002",
                    "Spine2": "spine.003", "Neck": "spine.004", "Head": "spine.006",
                    "LeftShoulder": "shoulder.L", "LeftArm": "upper_arm.L",
                    "LeftForeArm": "forearm.L", "LeftHand": "hand.L",
                    "RightShoulder": "shoulder.R", "RightArm": "upper_arm.R",
                    "RightForeArm": "forearm.R", "RightHand": "hand.R",
                    "LeftUpLeg": "thigh.L", "LeftLeg": "shin.L", "LeftFoot": "foot.L",
                    "LeftToeBase": "toe.L", "RightUpLeg": "thigh.R",
                    "RightLeg": "shin.R", "RightFoot": "foot.R",
                    "RightToeBase": "toe.R"},
        non_standard_bones={
            "TAB_F_01..03 / TAB_B_01..03": "tabard pendulum below the waist "
                "(R-C9-36); above the waist the tabard is weighted 1.0 to Hips "
                "and is RIGID",
            "SKIRT_F/B/L/R": "mail-skirt quadrant links",
            "SOCK_WeaponMain": "weapon parent socket on the main (right) hand",
            "SOCK_WeaponGripFar": "far-hand grip socket up the haft; a child of "
                "SOCK_WeaponMain, so it travels with the weapon and the off hand "
                "IK-locks to it -- the two grips cannot drift apart",
            "SOCK_OffHand": "off-hand attachment"},
        bones=[b.name for b in rig.data.bones],
        rigid_pieces={n: i["bone"] for n, i in idx["parts"].items()
                      if i["kind"] in ("rigid", "weapon")},
        deforming_pieces=[n for n, i in idx["parts"].items()
                          if i["kind"].startswith("deform")],
        weapon_pieces=[n for n, i in idx["parts"].items() if i["kind"] == "weapon"],
        atlas_triangles=ntri, atlas_objects=names,
        joints={k: [round(float(v[0]), 4), round(float(v[1]), 4), round(float(v[2]), 4)]
                for k, v in J.items()},
        params=p)
    with open(os.path.join(OUT, "skeleton.json"), "w") as f:
        json.dump(meta, f, indent=1)

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "knight_body.blend"))
    print("saved knight_body.blend: %d bones, %d objects, %d atlas triangles"
          % (len(rig.data.bones), len(objs), ntri))

    if "--render" in ARGV:
        fit = json.load(open(os.path.join(WORK, "fit_result.json")))
        which = fit["pose_fitted"] if "--pose-fitted" in ARGV else fit["canonical"]
        cam_d = bpy.data.cameras.new("Cam")
        cam = bpy.data.objects.new("Cam", cam_d)
        bpy.context.collection.objects.link(cam)
        bpy.context.scene.camera = cam
        W, H = 1024, 1536
        setup_render(W, H)
        # the pollaxe is not part of the body silhouette the M-a gate measures
        for ob in objs:
            if idx["parts"][ob.name]["kind"] == "weapon":
                ob.hide_render = True
        outdir = os.path.join(OUT, "silhouettes"); os.makedirs(outdir, exist_ok=True)
        for d, v in which["views"].items():
            place_camera(cam, v["alpha"], fit["theta_elevation_deg"],
                         v["scale"] * fit["downsample"],
                         v["tx"] * fit["downsample"], v["ty"] * fit["downsample"], W, H)
            bpy.context.scene.render.filepath = os.path.join(outdir, "%s.png" % d)
            bpy.ops.render.render(write_still=True)
            print("rendered", d)


main()
