# D7 assembly: her body with its clips and painted texture, plus every gear piece fitted,
# skinned and exported -- D2's sequence (15_export_scene), without the barbarian-specific
# morphs, carry poses and shield work.
#
#   blender -b -noaudio --python scripts/s9_assemble.py -- <body.glb> <tex.png> <outdir> [--json f]
#
#   deforming  robe, mantle, belt   isolated -> decimated -> pushed off the body -> skinned
#                                   (weights transferred from the nearest body point)
#   rigid      bracers              isolated -> bound to the forearms, one bone per side
#              circlet              PROCEDURAL, see below -> bound to Head
#   weapon     staff                socketed to RightHand, shaft centred through the fist;
#                                   52_weapon_bones later rebinds it to weapon_r
#
# LAYER OFFSETS are measured off the BODY, as D2's were. The belt goes on at 12 mm so it sits
# OUTSIDE the robe at the waist, where a belted robe is cinched to within about a centimetre.
#
# THE CIRCLET IS PROCEDURAL. It is part of the approved costume, and its Tripo isolation did
# not separate: a ~1 cm band pressed to the scalp came out either with her whole face attached
# (24,726 verts) or in fragments (1,455 verts, 3 components). At the play camera, 100.6 px/m,
# a 1 cm band is about ONE PIXEL. So it is realised directly -- a bronze band fitted to the
# MEASURED head cross-section at brow height, and a small ember stone at the front -- and the
# manifest says so. It is the one gear piece not built by the stated method.
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("s9_assemble.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODYGLB, TEX, OUT = a[0], a[1], a[2]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
ROOT = os.path.dirname(HERE)
os.makedirs(OUT, exist_ok=True)
rep = dict(pieces={})

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODYGLB)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
img = bpy.data.images.load(os.path.abspath(TEX))
for o in body:
    for s_ in o.material_slots:
        if s_.material and s_.material.node_tree:
            for nd in s_.material.node_tree.nodes:
                if nd.type == 'TEX_IMAGE':
                    nd.image = img
                    nd.image.colorspace_settings.name = 'sRGB'
# REST before fitting: bone heads are read POSED, and an import leaves an action active
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
BV, BT, names, W, tree = G.body_sampler(body[0])
H = float(BV[:, 2].max() - BV[:, 2].min())
print("body %.4f m, %d clips" % (H, len(bpy.data.actions)))
made = []

DEFORM = [("robe", 30000, 0.006), ("mantle", 22000, 0.010), ("belt", 14000, 0.012)]
for nm, faces, offs in DEFORM:
    before = set(sc.objects)
    pc = G.import_piece(os.path.join(ROOT, "pieces", "%s.glb" % nm), before)
    f0 = len(pc.data.polygons)
    G.decimate(pc, faces)
    P, pushed = G.clear_body(pc, tree, offs)
    ok = G.skin_to_body(pc, P, BV, BT, names, W, tree, arm)
    G.align_space(pc, body[0])
    pc.name = nm
    made.append((nm, [pc]))
    rep["pieces"][nm] = dict(mode="skin", faces=[f0, len(pc.data.polygons)], offset_m=offs,
                             pushed=int(pushed), skinned_verts=int(ok))
    print("  %-8s skinned: %d -> %d faces, pushed %d verts off the body by %.3f m"
          % (nm, f0, len(pc.data.polygons), pushed, offs))

before = set(sc.objects)
pc = G.import_piece(os.path.join(ROOT, "pieces", "bracers.glb"), before)
G.decimate(pc, 10000)
P, pushed = G.clear_body(pc, tree, 0.003)
parts = G.bone_bind(pc, arm, ["RightForeArm", "LeftForeArm"], True)
for o, _ in parts:
    G.align_space(o, body[0])
made.append(("bracers", [o for o, _ in parts]))
rep["pieces"]["bracers"] = dict(mode="bone", bones=["RightForeArm", "LeftForeArm"],
                                objects=[o.name for o, _ in parts])
print("  bracers  bound: %s" % [(o.name, b) for o, b in parts])

# ---- the circlet, procedural, fitted to the MEASURED head -------------------------
hb = arm.pose.bones["Head"]
hh = np.array(arm.matrix_world @ hb.head); ht = np.array(arm.matrix_world @ hb.tail)
zb = float(BV[:, 2].min()) + 0.955 * H                      # brow band, above the eyebrows
ax = np.array([hh[0], hh[1]])
near = (np.abs(BV[:, 2] - zb) < 0.006) & (np.linalg.norm(BV[:, :2] - ax, axis=1) < 0.16)
Rh = float(np.percentile(np.linalg.norm(BV[near][:, :2] - ax, axis=1), 85)) if near.sum() > 20 else 0.095
ctr = np.array([np.median(BV[near][:, 0]), np.median(BV[near][:, 1])]) if near.sum() > 20 else ax
# THE BAND FOLLOWS THE HEAD'S OUTLINE, not a circle. The first fit took ONE radius -- the 85th
# percentile of scalp distance at brow height, 0.1226 m -- and the band floated 2-4 cm clear of her
# head all round: a halo. A head is longer than it is wide and her hair bulks it unevenly, so no
# single radius fits. Here, for each of 64 directions, the OUTERMOST scalp/hair point at brow
# height (within +/-4 deg of that direction), smoothed round the loop, plus 4 mm.
slab = BV[near][:, :2] - ctr
ang = np.arctan2(slab[:, 1], slab[:, 0]); rad = np.linalg.norm(slab, axis=1)
N = 64; th = np.linspace(-np.pi, np.pi, N, endpoint=False); rr = np.zeros(N)
for k, t in enumerate(th):
    d = np.abs((ang - t + np.pi) % (2 * np.pi) - np.pi)
    m = d < np.radians(4)
    rr[k] = rad[m].max() if m.sum() else np.nan
ok_ = ~np.isnan(rr)
rr = np.interp(th, th[ok_], rr[ok_], period=2 * np.pi)
rr = np.convolve(np.r_[rr[-3:], rr, rr[:3]], np.ones(7) / 7, mode="valid")   # smooth, circular
rr = rr + 0.004
pts = [Vector((float(ctr[0] + r_ * math.cos(t)), float(ctr[1] + r_ * math.sin(t)), zb)) for t, r_ in zip(th, rr)]
me_c = bpy.data.meshes.new("circlet")
me_c.from_pydata(pts, [(i, (i + 1) % N) for i in range(N)], [])
ob_c = bpy.data.objects.new("circlet", me_c); sc.collection.objects.link(ob_c)
bpy.context.view_layer.objects.active = ob_c
mod = ob_c.modifiers.new("skin", 'SKIN')
for v in me_c.skin_vertices[0].data:
    v.radius = (0.0045, 0.0045)
bpy.ops.object.select_all(action='DESELECT'); ob_c.select_set(True)
bpy.ops.object.modifier_apply(modifier="skin")
Rh = float(np.median(rr))
_front = float(rr[np.argmin(np.abs(th - (-np.pi / 2)))])     # -Y is her front
# the ember stone at the front of the brow (she faces -Y)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.011,
                                      location=(float(ctr[0]), float(ctr[1]) - (_front + 0.006), zb))
stone = bpy.context.active_object; stone.name = "circlet_stone"
for o, col, em in ((ob_c, (0.62, 0.42, 0.20, 1), 0.0), (stone, (0.95, 0.30, 0.08, 1), 2.5)):
    m = bpy.data.materials.new(o.name + "_mat"); m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = col
    bs.inputs["Metallic"].default_value = 0.85 if o is ob_c else 0.0
    bs.inputs["Roughness"].default_value = 0.35
    if em:
        bs.inputs["Emission Color"].default_value = col; bs.inputs["Emission Strength"].default_value = em
    o.data.materials.append(m)
bpy.ops.object.select_all(action='DESELECT'); ob_c.select_set(True); stone.select_set(True)
bpy.context.view_layer.objects.active = ob_c
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.join()
g = ob_c.vertex_groups.new(name="Head")
g.add(list(range(len(ob_c.data.vertices))), 1.0, 'REPLACE')
mm = ob_c.modifiers.new('arm', 'ARMATURE'); mm.object = arm
G.align_space(ob_c, body[0])
made.append(("circlet", [ob_c]))
rep["pieces"]["circlet"] = dict(mode="bone", bones=["Head"], method="PROCEDURAL",
    band_height_m=round(zb, 4), band_radius_m=[round(float(rr.min()), 4), round(float(rr.max()), 4)],
    fit="the head's outline at brow height, 64 directions, +4 mm -- a single radius floated it as a halo",
    verts_in_slab=int(near.sum()),
    why=("Tripo isolation did not separate a ~1 cm band from the scalp: 24,726 verts with the whole "
         "face attached, or 1,455 verts in 3 fragments. At 100.6 px/m it is ~1 px in play."))
print("  circlet  PROCEDURAL: band at %.3f m following the head outline, radius %.4f-%.4f m (median %.4f), front %.4f, from %d scalp verts"
      % (zb, rr.min(), rr.max(), Rh, _front, near.sum()))

# ---- the staff ------------------------------------------------------------------
before = set(sc.objects)
pc = G.import_piece(os.path.join(ROOT, "builds", "staff.glb"), before)
G.decimate(pc, 9000)
info = G.socket_weapon2(pc, arm, "RightHand", 1.75, 0.55, axis_world=(0, 0, 1), face_world=(0, -1, 0))
moved = G.centre_shaft_on_fist(pc, body[0], arm, "RightHand")
G.align_space(pc, body[0])
pc.name = "staff"
made.append(("staff", [pc]))
rep["pieces"]["staff"] = dict(mode="socket", bone="RightHand", length_m=1.75, grip=0.55,
                              socket=info, shaft_centred_m=moved)
print("  staff    socketed to RightHand: %s; shaft centred %s" % (info.get("span_scaled_m"), moved))


def export(objs, path, anim=False):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True,
                              export_animations=anim, export_morph=True, export_image_format='AUTO')
    return round(os.path.getsize(path) / 1e6, 2)


for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
rep["files"] = {"so-body.glb": export(body, os.path.join(OUT, "so-body.glb"), anim=True)}
for nm, objs in made:
    rep["files"]["%s.glb" % nm] = export(objs, os.path.join(OUT, "%s.glb" % nm))
for k, v in rep["files"].items():
    print("wrote %-14s %6.2f MB" % (k, v))
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
