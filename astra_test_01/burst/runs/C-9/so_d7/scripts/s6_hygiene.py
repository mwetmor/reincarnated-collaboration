# Strip joint-scale tracks and re-ground every clip from its feet (min rule).
#
#   blender -b -noaudio --python scripts/s6_hygiene.py -- <in.glb> <out.glb> [--json f]
#
# Her idle AND her walk ("Walking Woman") both arrived with Meshy's constant Hips scale of
# 1.176471 -- the barbarian's defect, in two clips this time. The arrival lint recorded both
# as FAIL; the band rule isolates both. Stripping the scale leaves the feet in the air, so each
# stripped clip is re-grounded from its feet -- with the MIN rule (deepest foot on the floor),
# never the midpoint, which put a leaping clip 0.40 m underground in W1b.
import bpy, json, os, sys
from mathutils import Matrix
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("s6_hygiene.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
SRC, DST = a[0], a[1]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
rep = dict(stripped=G.strip_bone_scale(bpy.data.actions), grounded={})
print("stripped: %s" % json.dumps(rep["stripped"]))
masks = {o.name: G.foot_verts(o) for o in body}
for act in sorted(bpy.data.actions, key=lambda x: x.name):
    # bind the slot explicitly (Blender 5), or foot_track reads the rest pose
    arm.animation_data.action = act
    if len(getattr(act, "slots", [])):
        arm.animation_data.action_slot = act.slots[0]
    fz = G.foot_track(arm, body, act, masks)
    if abs(float(fz.min())) < 0.005:
        rep["grounded"][act.name] = dict(skipped="lowest foot already within 5 mm", feet=[round(float(fz.min()), 4), round(float(fz.max()), 4)])
        continue
    r = G.reground_from_feet(arm, body, act, mode='min')
    rep["grounded"][act.name] = r
    print("  %-14s %+.4f m: feet %+.4f..%+.4f -> %+.4f..%+.4f"
          % (act.name, r["dz"], r["before"]["min"], r["before"]["max"], r["after"]["min"], r["after"]["max"]))
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
for o in body + [arm]:
    o.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=DST, export_format='GLB', use_selection=True,
                          export_animations=True, export_morph=True, export_image_format='AUTO')
print("wrote %s" % DST)
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
