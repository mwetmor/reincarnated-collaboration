# One GLB for the film: her body (with its clips) and every gear piece on ONE armature.
#   blender -b -noaudio --python scripts/s10_combine.py -- <exportdir> <out.glb>
# Every exported file carries the identical 26 joints (52_weapon_bones), so each piece's
# armature modifier is re-pointed at the body's armature and the piece's own copy removed.
# This stands in for gear.gd, which does the same binding at runtime in the play build.
import bpy, glob, os, sys
a = sys.argv[sys.argv.index('--') + 1:]
D, OUT = a[0], a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(D, "so-body.glb"))
sc = bpy.context.scene
body_arm = next(o for o in sc.objects if o.type == 'ARMATURE')
keep = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for p in sorted(glob.glob(os.path.join(D, "*.glb"))):
    if p.endswith("so-body.glb"):
        continue
    before = set(sc.objects)
    bpy.ops.import_scene.gltf(filepath=p)
    add = [o for o in sc.objects if o not in before]
    for o in add:
        if o.type == 'MESH' and o.vertex_groups:
            for m in o.modifiers:
                if m.type == 'ARMATURE':
                    m.object = body_arm
            mw = o.matrix_world.copy(); o.parent = body_arm; o.matrix_world = mw
            keep.append(o)
    for o in add:
        if o.type == 'ARMATURE' or (o.type == 'MESH' and not o.vertex_groups):
            bpy.data.objects.remove(o, do_unlink=True)
    for x in [x for x in bpy.data.actions if x.users == 0]:
        bpy.data.actions.remove(x)
print("meshes on the body armature: %d  clips: %s" % (len(keep), sorted(x.name for x in bpy.data.actions)))
bpy.ops.object.select_all(action='DESELECT')
for o in keep + [body_arm]:
    o.select_set(True)
bpy.context.view_layer.objects.active = body_arm
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
                          export_animations=True, export_morph=True, export_image_format='AUTO')
print("wrote %s (%.2f MB)" % (OUT, os.path.getsize(OUT) / 1e6))
