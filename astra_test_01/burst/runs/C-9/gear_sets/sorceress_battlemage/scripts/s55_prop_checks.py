# R-C9-119 checks: the book and the wand against her BODY and her worn pieces (hood, breastplate, gauntlets) in every clip,
# with the book hold applied as the scene applies it -- book_carry_L REPLACING exactly LeftArm/LeftForeArm/LeftHand
# (an NLA strip of an action holding only those bones' curves) over each clip -- and the staff carry over idle/walk/run on
# the right arm (staff_carry_R, its nine bones). Grip morphs on (grip_R_wand, grip_L_book), under_battlemage on.
#   blender -b -noaudio --python s55_prop_checks.py -- <body.glb> <export_dir> <out.json> [--step 2]
# Per clip: prop vertices INSIDE a collider (nearest collider point + normal, inside and within 5 cm), and the minimum
# clearance; for the book also its lowest point relative to her hood and the spine's distance to the left palm centre.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
BODY, EXP, OUT = a[0], a[1], a[2]
STEP = int(a[a.index('--step') + 1]) if '--step' in a else 2
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = next(o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.data.vertices) > 1000)
for o in [o for o in sc.objects if o.type == 'MESH' and o is not body]:
    bpy.data.objects.remove(o, do_unlink=True)
pieces = {}
for p in ("hood", "breastplate", "gauntlets", "wand", "grimoire"):
    before = set(sc.objects); bpy.ops.import_scene.gltf(filepath=os.path.join(EXP, p + ".glb"))
    new = [o for o in sc.objects if o not in before]
    ms = [o for o in new if o.type == 'MESH' and len(o.data.vertices) > 150]   # not the rig's 42-vert Icosphere
    for o in ms:
        for m in o.modifiers:
            if m.type == 'ARMATURE': m.object = arm
        o.parent = body.parent; o.matrix_parent_inverse = body.matrix_parent_inverse.copy(); o.matrix_basis = body.matrix_basis.copy()
    for o in new:
        if o.type == 'ARMATURE': bpy.data.objects.remove(o, do_unlink=True)
    pieces[p] = ms
    print("PIECE", p, [(o.name, o.data.name, len(o.data.vertices)) for o in ms])
for o in [body] + pieces["gauntlets"]:
    if o.data.shape_keys:
        for k in o.data.shape_keys.key_blocks:
            k.value = 1.0 if k.name in ("grip_R_wand", "grip_L_book", "under_battlemage") else 0.0
# layer actions holding ONLY the filtered bones' curves
def sub_action(src, bones, name):
    """a COPY of src keeping only the curves of `bones` (Blender 5 slotted actions: prune each channel bag)"""
    act = src.copy(); act.name = name
    for layer in act.layers:
        for strip in layer.strips:
            for cb in strip.channelbags:
                for fc in [fc for fc in cb.fcurves if not any('"%s"' % b in fc.data_path for b in bones)]:
                    cb.fcurves.remove(fc)
    return act
BOOKB = ["LeftArm", "LeftForeArm", "LeftHand"]
CARRYB = ["Spine02", "Spine01", "Spine", "neck", "Head", "RightShoulder", "RightArm", "RightForeArm", "RightHand"]
book_act = sub_action(bpy.data.actions["book_carry_L"], BOOKB, "_book_layer")
carry_act = sub_action(bpy.data.actions["staff_carry_R"], CARRYB, "_carry_layer")
arm.animation_data_create()


def world(o, dg):
    oe = o.evaluated_get(dg); me = oe.to_mesh(); me.calc_loop_triangles()
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
    M = np.array(o.matrix_world); V = co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
    T = [list(t.vertices) for t in me.loop_triangles]; oe.to_mesh_clear(); return V, T


gi = {g.index: g.name for g in body.vertex_groups}
dom = np.array([gi[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else "" for v in body.data.vertices])
rep = {}; WHO = {}
CLIPS = a[a.index('--clips') + 1].split(',') if '--clips' in a else ["idle", "walk", "run", "cast_fireball_m", "cast_meteor", "hit", "death"]
for clip in CLIPS:
    act = bpy.data.actions.get(clip)
    if act is None: continue
    for tr in list(arm.animation_data.nla_tracks): arm.animation_data.nla_tracks.remove(tr)
    # the ACTIVE action evaluates ABOVE the NLA stack in Blender, so the clip goes in the NLA as the BOTTOM strip
    arm.animation_data.action = None
    t0 = arm.animation_data.nla_tracks.new(); s0 = t0.strips.new("clip", int(act.frame_range[0]), act); s0.blend_type = 'REPLACE'
    if hasattr(s0, "action_slot") and act.slots: s0.action_slot = act.slots[0]
    if clip in ("idle", "walk", "run"):
        t1 = arm.animation_data.nla_tracks.new(); s1 = t1.strips.new("carry", 0, carry_act); s1.blend_type = 'REPLACE'
        if hasattr(s1, "action_slot") and carry_act.slots: s1.action_slot = carry_act.slots[0]
    t2 = arm.animation_data.nla_tracks.new(); s2 = t2.strips.new("book", 0, book_act); s2.blend_type = 'REPLACE'
    if hasattr(s2, "action_slot") and book_act.slots: s2.action_slot = book_act.slots[0]
    f0, f1 = map(int, act.frame_range)
    for s_ in [t.strips[0] for t in arm.animation_data.nla_tracks if t.strips[0].name != "clip"]:
        s_.action_frame_start, s_.action_frame_end = 0, 1; s_.frame_start, s_.frame_end = f0, f1 + 1; s_.extrapolation = 'HOLD'
        s_.repeat = 1.0; s_.scale = 1.0
        s_.use_sync_length = False
    rows = []
    for f in range(f0, f1 + 1, STEP):
        sc.frame_set(f); bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
        BV, BT = world(body, dg)
        colliders = {"body": (BV, BT)}
        for p in ("hood", "breastplate", "gauntlets"):
            for o in pieces[p]:
                colliders[p] = world(o, dg)
        if f == f0 and clip == "idle":
            print("COLLIDERS", {k: (len(v), round(float(v[:, 2].min()), 3), round(float(v[:, 2].max()), 3)) for k, (v, t) in colliders.items()})
        # the body WITHOUT her hands: the wand is gripped in the right fist and the book's spine sits in the left palm by design
        keep_t = [t for t in BT if not any(dom[i] in ("RightHand", "LeftHand") for i in t)]
        colliders["body"] = (BV, keep_t)
        trees = {k: BVHTree.FromPolygons([Vector(x) for x in v.tolist()], t) for k, (v, t) in colliders.items()}
        row = dict(f=f)
        for prop in ("grimoire", "wand"):
            PV = np.vstack([world(o, dg)[0] for o in pieces[prop]])
            samp = PV[:: max(1, len(PV) // 1200)]
            for k, tr in trees.items():
                if prop == "wand" and k == "gauntlets":
                    continue                                        # the wand IS held in the gauntlet
                ins, dmin = 0, 9.0
                for p_ in samp:
                    h = tr.find_nearest(Vector(p_.tolist()))
                    if h[0] is None: continue
                    dd = (Vector(p_.tolist()) - h[0]).length; dmin = min(dmin, dd)
                    if (Vector(p_.tolist()) - h[0]).dot(h[1]) < 0 and dd < 0.05:
                        if k == "body" and "--who" in a:
                            vi = colliders["body"][1][h[2]][0]; WHO.setdefault((clip, prop), {}).setdefault(dom[vi], 0)
                            WHO[(clip, prop)][dom[vi]] += 1
                        # a wand vertex inside the RIGHT HAND's own fist is the grip, not a penetration
                        ins += 1
                row["%s_in_%s" % (prop, k)] = ins; row["%s_clear_%s" % (prop, k)] = round(dmin, 4)
        rows.append(row)
    keys = [k for k in rows[0] if k != 'f']
    rep[clip] = dict(frames=len(rows), **{k: (max(r[k] for r in rows) if "_in_" in k else min(r[k] for r in rows)) for k in keys},
                     frames_with_book_inside=sum(1 for r in rows if any(r[k] for k in keys if k.startswith("grimoire_in_"))))
    print("CHK %-16s " % clip + " ".join("%s=%s" % (k, rep[clip][k]) for k in sorted(rep[clip]) if k.startswith("grimoire_in") or k.startswith("wand_in") or k == "frames_with_book_inside"))
json.dump(rep, open(OUT, "w"), indent=1)
if WHO: print("WHO", {"%s/%s" % k: v for k, v in WHO.items()})
