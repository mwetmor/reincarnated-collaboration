# Give her rig weapon_r and weapon_l FROM THE START (legolas, Part 6 rank 1).
#
#   blender -b -noaudio --python scripts/s4_weapon_bones.py -- <rigged.glb> <out.glb>
#
# Each is a child of its hand, head/tail/roll copied from the hand so it is
# coincident with it, use_connect False, use_deform TRUE (legolas: the glTF
# exporter's deform-bones-only path has open upstream bugs with non-deform
# bones, and a weapon skinned to a deform bone sidesteps them). The staff will
# be skinned 1.0 to weapon_r; rotating weapon_r then pivots the staff about the
# fist and the grip does not move (measured d = 0.0 on the barbarian's axe).
#
# FROM THE START because gear.gd binds pieces by comparing bone-name LISTS, in
# ORDER. Adding the bone later, or to the staff alone, splits the skeletons.
# So it goes on the base rig before a single piece is built, and every piece
# inherits the same 26 names in the same order.
import bpy, json, sys
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
SRC, DST = a[0], a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
stray = [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]
print("bones in: %d  %s" % (len(arm.data.bones), [b.name for b in arm.data.bones]))
print("skinned meshes: %s   unskinned (removed): %s"
      % ([o.name for o in body], [o.name for o in stray]))
for o in stray:
    bpy.data.objects.remove(o, do_unlink=True)


def world_verts():
    dg = bpy.context.evaluated_depsgraph_get()
    out = []
    for o in body:
        ev = o.evaluated_get(dg); me = ev.to_mesh()
        co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
        M = np.array(o.matrix_world)
        out.append(co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]); ev.to_mesh_clear()
    return np.vstack(out)


arm.animation_data_clear() if arm.animation_data else None
bpy.context.view_layer.update()
V0 = world_verts()
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='EDIT')
eb = arm.data.edit_bones
made = {}
for side, hand in (("weapon_r", "RightHand"), ("weapon_l", "LeftHand")):
    h = eb[hand]
    w = eb.new(side)
    w.head, w.tail, w.roll = h.head.copy(), h.tail.copy(), h.roll
    w.parent = h
    w.use_connect = False
    w.use_deform = True
    made[side] = dict(parent=hand, head=[round(x, 5) for x in w.head],
                      tail=[round(x, 5) for x in w.tail], roll=round(w.roll, 6))
bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.update()
V1 = world_verts()
moved = float(np.abs(V1 - V0).max())
names = [b.name for b in arm.data.bones]
print("bones out: %d  ...%s" % (len(names), names[-4:]))
for k, v in made.items():
    b = arm.data.bones[k]
    print("  %s parent=%s deform=%s connect=%s" % (k, b.parent.name, b.use_deform, b.use_connect))
print("rest-pose body displacement after adding the bones: %.3e m (must be 0)" % moved)
assert moved < 1e-6, "adding the bones moved the body"
bpy.ops.object.select_all(action='DESELECT')
for o in body + [arm]:
    o.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=DST, export_format='GLB', use_selection=True,
                          export_animations=False, export_image_format='AUTO')
json.dump(dict(bones=names, added=made, body_moved_m=moved),
          open(DST.replace('.glb', '_bones.json'), 'w'), indent=1)
print("wrote %s" % DST)
