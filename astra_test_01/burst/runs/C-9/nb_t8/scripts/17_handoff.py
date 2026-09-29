# T8 step 4: one GLB for the 3D cliffside -- painted texture, four clips, at
# the declared height.
#
#   blender -b -noaudio --python scripts/17_handoff.py -- <rigged.glb>
#          <tex.png> <out.glb> --clips walk:nbt_walk.glb,run:... [--height 1.85]
#
# Meshy delivers one GLB per clip, each carrying its own copy of the rig. This
# takes the base rig once and lifts each clip's ACTION onto it, so the consumer
# gets one skeleton with four named animations instead of four skeletons.
# The bone names are identical across the clips by construction (same rig task),
# and that is ASSERTED rather than assumed.
#
# SCALE. Meshy's `character_height` does not set the delivered scale -- 1.85 was
# asked for and 1.70 came back -- and the stray Icosphere it ships makes a
# naive bbox read 2.70. So the height is measured on the SKINNED mesh only, and
# the figure is scaled to the declared height here, once, so the cliffside's
# rule has a real number to multiply.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index('--') + 1:]
RIG, TEX, OUT = a[0], a[1], a[2]
CLIPS = [c.split(":", 1) for c in a[a.index("--clips") + 1].split(",")]
HGT = float(a[a.index("--height") + 1]) if "--height" in a else 1.85
WORLD_SCALE = 1.25178          # T7-A: a 1.80 m body is 2.2532 m in the world

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=RIG)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
stray = [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]
for o in stray:
    print("dropping unskinned stray %s (%d verts)" % (o.name, len(o.data.vertices)))
    bpy.data.objects.remove(o, do_unlink=True)
base_bones = {b.name for b in arm.data.bones}
print("rig %s: %d bones, %d skinned mesh(es)" % (arm.name, len(base_bones), len(body)))

# ---- the painted texture ---------------------------------------------------
img = bpy.data.images.load(os.path.abspath(TEX))
img.colorspace_settings.name = 'sRGB'
n = 0
for o in body:
    for s in o.material_slots:
        if s.material and s.material.node_tree:
            for nd in s.material.node_tree.nodes:
                if nd.type == 'TEX_IMAGE':
                    nd.image = img; n += 1
assert n, "no image texture node to carry the paint"
print("painted texture on %d node(s)" % n)

# ---- lift each clip's action onto this rig --------------------------------
acts = []
for name, path in CLIPS:
    before = set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=path)
    new_objs = [o for o in sc.objects if o.type == 'ARMATURE' and o is not arm]
    newacts = [x for x in bpy.data.actions if x not in before]
    assert newacts, "%s carried no action" % path
    act = newacts[0]
    src_arm = new_objs[0]
    missing = {b.name for b in src_arm.data.bones} ^ base_bones
    assert not missing, ("%s has a different skeleton: %s"
                         % (path, sorted(missing)[:6]))
    act.name = name
    act.use_fake_user = True
    acts.append(act)
    # Blender 5.x moved an Action's curves under layers/strips (slotted
    # actions); len(act.fcurves) is gone. Count whichever exists.
    try:
        ncur = len(act.fcurves)
    except AttributeError:
        ncur = 0
        for lay in act.layers:
            for st in lay.strips:
                for cb in getattr(st, "channelbags", []):
                    ncur += len(getattr(cb, "fcurves", []))
    print("  %-7s <- %-18s %d curves, frames %s"
          % (name, os.path.basename(path), ncur,
             [int(v) for v in act.frame_range]))
    for o in list(sc.objects):
        if o is not arm and o not in body:
            bpy.data.objects.remove(o, do_unlink=True)

# ---- sweep, right before export -------------------------------------------
# Every clip import brings its OWN copy of Meshy's unskinned Icosphere and the
# base rig carries an action of its own. Removing them once at the top is not
# enough: the first version did exactly that and still exported a sphere and a
# fifth action, which put the file's bbox at 2.85 m with "feet" at z = -1.0
# while the BODY was a correct 1.85. Sweep at the end, and assert the sweep.
for o in [x for x in sc.objects if x.type == 'MESH' and not x.vertex_groups]:
    print("  sweeping stray %s (%d verts)" % (o.name, len(o.data.vertices)))
    bpy.data.objects.remove(o, do_unlink=True)
keep = {x.name for x in acts}
for x in list(bpy.data.actions):
    if x.name not in keep:
        print("  dropping foreign action %s" % x.name)
        x.use_fake_user = False
        bpy.data.actions.remove(x)
assert not [x for x in sc.objects if x.type == 'MESH' and not x.vertex_groups], \
    "an unskinned stray survived the sweep"
assert len(bpy.data.actions) == len(CLIPS), \
    "expected %d actions, have %s" % (len(CLIPS), [x.name for x in bpy.data.actions])

# ---- stack them as NLA tracks so the exporter emits all four --------------
if not arm.animation_data:
    arm.animation_data_create()
arm.animation_data.action = None
for act in acts:
    tr = arm.animation_data.nla_tracks.new()
    tr.name = act.name
    tr.strips.new(act.name, int(act.frame_range[0]), act)

# ---- scale to the declared height, measured on the SKINNED mesh -----------
dg = bpy.context.evaluated_depsgraph_get()
V = []
for o in body:
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    V.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
             + np.array(o.matrix_world.translation))
V = np.vstack(V); H0 = float(V[:, 2].max() - V[:, 2].min())
s = HGT / H0
for o in list(sc.objects):
    if o.parent is None:
        o.matrix_world = Matrix.Scale(s, 4) @ o.matrix_world
bpy.context.view_layer.update()
V = []
for o in body:
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    V.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
             + np.array(o.matrix_world.translation))
V = np.vstack(V); H1 = float(V[:, 2].max() - V[:, 2].min())
print("height %.4f -> %.4f m (x%.5f); feet at z=%.4f" % (H0, H1, s, V[:, 2].min()))
assert abs(H1 - HGT) < 1e-3, "scale did not take: %.4f" % H1

# EXPORT WHAT IS SELECTED, not "everything minus what I removed". Removing the
# strays was not enough: the sweep above found nothing left in sc.objects and
# the exporter still wrote an Icosphere, so it reaches the file by a path the
# scene listing does not show. Naming the two objects that belong in the file
# is a positive statement and cannot be defeated that way.
print("BEFORE EXPORT -- bpy.data.objects: %s"
      % [(o.name, o.type, o.parent.name if o.parent else None,
          o.name in sc.objects) for o in bpy.data.objects])
bpy.ops.object.select_all(action='DESELECT')
for o in body + [arm]:
    o.select_set(True)
bpy.context.view_layer.objects.active = arm
print("exporting %s" % [o.name for o in body + [arm]])
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
                          export_animations=True, export_animation_mode='ACTIONS',
                          export_image_format='AUTO')
note = dict(
    glb=os.path.basename(OUT), declared_height_m=HGT,
    measured_height_m=round(H1, 5), feet_z=round(float(V[:, 2].min()), 5),
    facing="-Y", his_right="-X", up="+Z",
    clips=[dict(name=n, frames=int(x.frame_range[1] - x.frame_range[0]),
                fps=sc.render.fps) for (n, _), x in zip(CLIPS, acts)],
    world_scale_rule=dict(
        factor=WORLD_SCALE,
        world_height_m=round(HGT * WORLD_SCALE, 5),
        note=("T7-A: figure scale %.5f, so a 1.80 m body is %.4f m in the world "
              "to meet 150.2135 px. This figure is declared %.2f m, so he is "
              "%.4f m in the world and reads %.1f px -- %.1f%% taller than a "
              "1.80 m body, which is the point of a big Norseman. Declare 1.80 "
              "instead if he must match exactly."
              % (WORLD_SCALE, 1.80 * WORLD_SCALE, HGT, HGT * WORLD_SCALE,
                 150.2135 * HGT / 1.80, 100 * (HGT / 1.80 - 1)))))
json.dump(note, open(OUT.replace(".glb", ".json"), "w"), indent=1)
print("wrote %s (%.1f MB)" % (OUT, os.path.getsize(OUT) / 1e6))
