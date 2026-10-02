# STAGE J/R-C9-123 (B): a Mixamo FBX -> a GLB whose bones carry HIS rig's names, ready for e40b_mixamo_graft.py.
#   blender -b -noaudio --python e40a_mixamo_fbx.py -- <in.fbx> <out.glb> [--json f]
# MAPPING (Mixamo -> his 24 Meshy joints). NB his spine is named bottom-up the other way: Spine02 is the LOWEST (child of Hips),
# Spine the chest (parent of neck and both shoulders) -- verified on export/wl_body.glb. Fingers and HeadTop_End's siblings drop.
import bpy, json, os, re, sys
a = sys.argv[sys.argv.index('--') + 1:]; SRC, OUT = a[0], a[1]
MAP = {"Hips": "Hips", "Spine": "Spine02", "Spine1": "Spine01", "Spine2": "Spine", "Neck": "neck", "Head": "Head", "HeadTop_End": "head_end",
       "LeftShoulder": "LeftShoulder", "LeftArm": "LeftArm", "LeftForeArm": "LeftForeArm", "LeftHand": "LeftHand",
       "RightShoulder": "RightShoulder", "RightArm": "RightArm", "RightForeArm": "RightForeArm", "RightHand": "RightHand",
       "LeftUpLeg": "LeftUpLeg", "LeftLeg": "LeftLeg", "LeftFoot": "LeftFoot", "LeftToeBase": "LeftToeBase",
       "RightUpLeg": "RightUpLeg", "RightLeg": "RightLeg", "RightFoot": "RightFoot", "RightToeBase": "RightToeBase"}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC, automatic_bone_orientation=False, ignore_leaf_bones=True)
arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
ren, drop = {}, []
for b in arm.data.bones:
    base = re.sub(r'^mixamorig\d*:', '', b.name)
    if base in MAP: ren[b.name] = MAP[base]
    else: drop.append(b.name)
for old, new in ren.items(): arm.data.bones[old].name = new
for act in bpy.data.actions:                                     # keep the actions' bone paths in step with the renames
    pass
missing = sorted(set(MAP.values()) - set(ren.values()))
for o in [o for o in bpy.context.scene.objects if o.type == 'MESH']: o.select_set(False)
bpy.ops.object.select_all(action='DESELECT'); arm.select_set(True); bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_animations=True, export_force_sampling=True, export_frame_step=1)
rep = dict(src=os.path.basename(SRC), out=OUT, renamed=len(ren), dropped=len(drop), missing=missing, actions=[x.name for x in bpy.data.actions],
           fps=bpy.context.scene.render.fps)
print('MIXAMO', json.dumps(rep))
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
