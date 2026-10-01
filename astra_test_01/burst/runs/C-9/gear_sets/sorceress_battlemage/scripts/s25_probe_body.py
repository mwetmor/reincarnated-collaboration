# R-C9-98: read the shipped body's facts the assembler depends on (no writes): meshes, shape keys, bone heads, actions.
import bpy, sys, json
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=a[0])
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
arm.animation_data.action = None
for pb in arm.pose.bones: pb.matrix_basis.identity()
bpy.context.view_layer.update()
out = dict(meshes=[], bones={}, actions=[x.name for x in bpy.data.actions])
for o in sc.objects:
    if o.type == 'MESH':
        out["meshes"].append(dict(name=o.name, verts=len(o.data.vertices), groups=len(o.vertex_groups),
                                  keys=[k.name for k in o.data.shape_keys.key_blocks] if o.data.shape_keys else [],
                                  scale=list(o.matrix_world.to_scale())))
for b in ("Hips", "LeftUpLeg", "RightUpLeg", "LeftHand", "RightHand", "Head", "weapon_r", "weapon_l", "Spine02"):
    if b in arm.pose.bones:
        out["bones"][b] = [round(x, 4) for x in (arm.matrix_world @ arm.pose.bones[b].head)]
print("PROBE " + json.dumps(out))
