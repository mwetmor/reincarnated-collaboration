# R-C9-71: close the hands around the weapons.
#
#   blender -b -noaudio --python scripts/18_grip.py -- <base.glb> <tex> <out.json>
#     [--still <dir>] [--flesh 0.010]
#
# Matt named ONE AI tell: the weapons are not snapped to his grip. Two causes,
# and only one of them was the binding:
#
#   the binding is already right -- axe 100% RightHand, shield 100% LeftHand,
#   zero vertices with more than one group, minimum weight 1.0000. Verified by
#   reading the exported GLBs back before changing anything.
#
#   the HAND is the problem. This rig has 24 bones and NO FINGERS, so the hand
#   cannot be posed, and Meshy ships it open and flat from the A-pose. An open
#   flat hand cannot hold anything, however perfectly the weapon is bound to it.
#
# So the hands are closed with morph targets, grip_R and grip_L, driven to 1
# while the weapon is equipped -- the same mechanism as helmet_on.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("18_grip.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BASE, TEX, OUTJ = a[0], a[1], a[2]
STILL = a[a.index("--still") + 1] if "--still" in a else None
FLESH = float(a[a.index("--flesh") + 1]) if "--flesh" in a else 0.010
ROOT = os.path.dirname(HERE)
SPECS = dict(axe=dict(axis_world=(0, 0, 1), face_world=(0, -1, 0)),
             shield=dict(axis_world=(0.50, -0.87, 0.0), face_world=(0, 0, 1),
                         offset_world=(0.02, -0.06, 0.0), anchor="normal"))

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BASE)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
img = bpy.data.images.load(os.path.abspath(TEX))
for o in body:
    for s_ in o.material_slots:
        if s_.material and s_.material.node_tree:
            for nd in s_.material.node_tree.nodes:
                if nd.type == 'TEX_IMAGE':
                    nd.image = img; nd.image.colorspace_settings.name = 'sRGB'
CARRY = json.load(open(os.path.join(ROOT, "work", "carry_pose.json")))


def pose_carry(on):
    for bn, flat in CARRY.items():
        arm.pose.bones[bn].matrix_basis = (
            Matrix([flat[i * 4:(i + 1) * 4] for i in range(4)]) if on
            else Matrix.Identity(4))
    bpy.context.view_layer.update()


made = {}
for nm, bone, ln, gr in (("axe", "RightHand", 0.89, 0.22),
                         ("shield", "LeftHand", 0.82, 0.50)):
    if nm == "shield":
        pose_carry(True)
    before = set(sc.objects)
    pc = G.import_piece(os.path.join(ROOT, "builds", "%s.glb" % nm), before)
    G.decimate(pc, 9000)
    G.socket_weapon2(pc, arm, bone, ln, gr, **SPECS[nm])
    G.align_space(pc, body[0])
    bpy.context.view_layer.update()
    if nm == "axe":
        off = G.centre_shaft_on_fist(pc, body[0], arm, bone)
        print("axe: shaft axis moved %.4f m to pass through the fist" % off)
    made[nm] = (pc, bone)
    if nm == "shield":
        pose_carry(False)

rep = {}
for nm, key in (("axe", "grip_R"), ("shield", "grip_L")):
    pc, bone = made[nm]
    if nm == "shield":
        pose_carry(True)
    # the channel comes from the HAND, the radius from the weapon's shaft
    c, chan, along, palm = G.hand_frame(body[0], arm, bone)
    if nm == "axe":
        rad, _ = G.shaft_radius(pc, arm, bone)
        rad = float(min(max(rad, 0.012), 0.028))
    else:
        rad = 0.016                       # a shield's grip bar
    k, moved, mx = G.grip_key(body[0], arm, bone, c, chan, rad + FLESH, key)
    if k:
        k.value = 1.0
    print("%s: shaft radius %.4f m -> fist closes to %.4f m; %d vertices moved, "
          "max %.4f m" % (key, rad, rad + FLESH, moved, mx))
    rep[key] = dict(weapon=nm, bone=bone, channel=[round(float(v), 4) for v in chan],
                    shaft_radius_m=round(rad, 5),
                    close_to_m=round(rad + FLESH, 5), moved=moved,
                    max_move_m=round(mx, 5))
    if nm == "shield":
        pose_carry(False)

# ---- measure the gap, with the keys on and off -----------------------------
from mathutils.bvhtree import BVHTree


def gap(nm, keyname, val):
    pc, bone = made[nm]
    body[0].data.shape_keys.key_blocks[keyname].value = val
    if nm == "shield":
        pose_carry(True)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    eb = body[0].evaluated_get(dg); me = eb.to_mesh()
    cv = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", cv)
    BW = (cv.reshape(-1, 3) @ np.array(eb.matrix_world.to_3x3()).T
          + np.array(eb.matrix_world.translation))
    eb.to_mesh_clear()
    gi = body[0].vertex_groups[bone].index
    hand = np.array([v.index for v in body[0].data.vertices
                     if any(g.group == gi and g.weight > 0.30 for g in v.groups)])
    eo = pc.evaluated_get(dg); m2 = eo.to_mesh()
    wv = np.empty(len(m2.vertices) * 3); m2.vertices.foreach_get("co", wv)
    WV = (wv.reshape(-1, 3) @ np.array(eo.matrix_world.to_3x3()).T
          + np.array(eo.matrix_world.translation))
    eo.to_mesh_clear()
    wt = BVHTree.FromPolygons([Vector(p) for p in WV.tolist()],
                              [[i, (i + 1) % len(WV), (i + 2) % len(WV)]
                               for i in range(0, len(WV) - 2, 3)])
    ds = []
    for q in BW[hand][::3]:
        h = wt.find_nearest(Vector(q.tolist()))
        if h[0] is not None:
            ds.append(float((h[0] - Vector(q.tolist())).length))
    if nm == "shield":
        pose_carry(False)
    return float(np.min(ds)), float(np.median(ds)), len(ds)


for nm, key in (("axe", "grip_R"), ("shield", "grip_L")):
    off = gap(nm, key, 0.0)
    on = gap(nm, key, 1.0)
    label = "haft to right fist" if nm == "axe" else "grip bar to left fist"
    print("   %-22s open hand: min %.4f median %.4f | CLOSED: min %.4f "
          "median %.4f  (%d hand vertices)"
          % (label, off[0], off[1], on[0], on[1], on[2]))
    rep[key].update(gap_open=dict(min_m=round(off[0], 5), median_m=round(off[1], 5)),
                    gap_closed=dict(min_m=round(on[0], 5), median_m=round(on[1], 5)),
                    hand_vertices=on[2])
# ---- close the left gap by moving the SHIELD, not the hand -----------------
# Closing the left fist around a channel pulls it off the shield: the disc has
# no bar where the hand is, so the fingers close on air and the minimum gap
# goes 0.0000 -> 0.0152 m. The hand is now the correct shape, so it is the
# shield that should come to meet it -- 15 mm, far too small to disturb the
# torso clearance the carry layer was tuned for.
pc, bone = made["shield"]
body[0].data.shape_keys.key_blocks["grip_L"].value = 1.0
pose_carry(True)
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
eb = body[0].evaluated_get(dg); me = eb.to_mesh()
cv = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", cv)
BW = (cv.reshape(-1, 3) @ np.array(eb.matrix_world.to_3x3()).T
      + np.array(eb.matrix_world.translation))
eb.to_mesh_clear()
gi = body[0].vertex_groups[bone].index
hand = np.array([v.index for v in body[0].data.vertices
                 if any(g.group == gi and g.weight > 0.30 for g in v.groups)])
fist = BW[hand]
# BOTH SIDES POSED. The first version compared the shield's BIND-pose vertex
# data against the POSED fist and computed a 0.9 mm correction for a 15 mm gap
# -- it was measuring the distance between two different moments. The shield is
# rigidly bound to LeftHand, so a world step in the posed state comes back to
# the bind state through the inverse of that bone's pose rotation.
eo = pc.evaluated_get(dg); m2 = eo.to_mesh()
sv = np.empty(len(m2.vertices) * 3); m2.vertices.foreach_get("co", sv)
SWp = (sv.reshape(-1, 3) @ np.array(eo.matrix_world.to_3x3()).T
       + np.array(eo.matrix_world.translation))
eo.to_mesh_clear()
d = np.linalg.norm(SWp[::4, None, :] - fist[None, ::12, :], axis=2)
i, j = np.unravel_index(np.argmin(d), d.shape)
delta_posed = fist[::12][j] - SWp[::4][i]
pbL = arm.pose.bones["LeftHand"]
Rp = (arm.matrix_world.to_3x3() @ pbL.matrix.to_3x3())
Rr = (arm.matrix_world.to_3x3() @ pbL.bone.matrix_local.to_3x3())
step = np.array((Rr @ Rp.inverted() @ Vector(delta_posed.tolist())).to_tuple()) * 0.92
co = np.empty(len(pc.data.vertices) * 3)
pc.data.vertices.foreach_get("co", co)
SP = co.reshape(-1, 3)
SW = SP @ np.array(pc.matrix_world.to_3x3()).T + np.array(pc.matrix_world.translation)
print("   shield nudged %.4f m to meet the closed fist" % float(np.linalg.norm(step)))
Mi = pc.matrix_world.inverted()
SW2 = SW + step
SP2 = SW2 @ np.array(Mi.to_3x3()).T + np.array(Mi.translation)
pc.data.vertices.foreach_set("co", SP2.ravel())
pc.data.update()
bpy.context.view_layer.update()
rep["shield_nudge_m"] = round(float(np.linalg.norm(step)), 5)
on = gap("shield", "grip_L", 1.0)
print("   grip bar to left fist AFTER nudge: min %.4f median %.4f" % (on[0], on[1]))
rep["grip_L"]["gap_closed_after_nudge"] = dict(min_m=round(on[0], 5),
                                               median_m=round(on[1], 5))
pose_carry(False)

# ---- close-range stills ----------------------------------------------------
if STILL:
    os.makedirs(STILL, exist_ok=True)
    for ob in body + [made[k][0] for k in made]:
        for sl in ob.material_slots:
            m_ = sl.material
            if not m_ or not m_.node_tree:
                continue
            nt = m_.node_tree
            b_ = next((x for x in nt.nodes if x.type == 'BSDF_PRINCIPLED'), None)
            o_ = next(x for x in nt.nodes if x.type == 'OUTPUT_MATERIAL')
            em = nt.nodes.new('ShaderNodeEmission')
            L_ = b_.inputs['Base Color'].links if b_ else []
            if L_:
                nt.links.new(L_[0].from_socket, em.inputs['Color'])
            nt.links.new(em.outputs['Emission'], o_.inputs['Surface'])
    eng = [e.identifier for e in
           bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
    sc.render.engine = ('BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng
                        else 'BLENDER_EEVEE')
    sc.render.resolution_x = sc.render.resolution_y = 420
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.color_mode = 'RGBA'
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
    sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = 'ORTHO'
    acts2 = {x.name: x for x in bpy.data.actions}
    shots = [("idle", None, 0), ("walk_pass", "walk", 6), ("attack_strike", "attack", 16)]
    el_ = math.radians(35.0)
    for pname, act, fr in shots:
        for bone, tag in (("RightHand", "R_axe"), ("LeftHand", "L_shield")):
            arm.animation_data.action = acts2[act] if act else None
            if act:
                sc.frame_set(int(acts2[act].frame_range[0]) + fr)
            else:
                for pbx in arm.pose.bones:
                    pbx.matrix_basis = Matrix.Identity(4)
            if bone == "LeftHand" or (act is None):
                pose_carry(True)
            bpy.context.view_layer.update()
            ctr2 = Vector((arm.matrix_world @ arm.pose.bones[bone].head).to_tuple())
            cam.data.ortho_scale = 0.55          # ~3x on a 1.85 m figure
            for nmf, az_ in (("S", 0), ("SE", 45), ("E", 90), ("W", 270)):
                az = math.radians((360 - az_) % 360)
                pos = ctr2 + Vector((math.sin(az) * math.cos(el_),
                                     -math.cos(az) * math.cos(el_),
                                     math.sin(el_))) * 6.0
                cam.location = pos
                cam.rotation_euler = (ctr2 - pos).to_track_quat('-Z', 'Y').to_euler()
                sc.render.filepath = os.path.join(
                    STILL, "%s_%s_%s.png" % (pname, tag, nmf))
                bpy.ops.render.render(write_still=True)
            if bone == "LeftHand" or (act is None):
                pose_carry(False)
    print("stills in %s" % STILL)
json.dump(rep, open(OUTJ, "w"), indent=1)
