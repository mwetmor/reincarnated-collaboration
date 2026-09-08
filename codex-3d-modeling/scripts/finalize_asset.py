import bpy
import json
import math
from pathlib import Path
ROOT=Path('/Users/admin/Games/reincarnated-collaboration/codex-3d-modeling')
char=bpy.data.collections['Wizard_Character']
corrections=[]
for obj in char.objects:
    if obj.type!='MESH':continue
    if obj.data.validate(clean_customdata=False):corrections.append(obj.name)
    assert all(math.isfinite(v) for vertex in obj.data.vertices for v in vertex.co)
rig=bpy.data.objects['WizardRig']
rig.animation_data.action=bpy.data.actions['Idle']
bpy.context.scene.frame_set(0)
bpy.ops.object.select_all(action='DESELECT')
for obj in char.objects:obj.select_set(True)
bpy.context.view_layer.objects.active=rig
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/purple_wizard.blend'))
bpy.ops.export_scene.gltf(filepath=str(ROOT/'godot/assets/purple_wizard.glb'),
    export_format='GLB',use_selection=True,export_animations=True,export_skins=True,
    export_yup=True,export_animation_mode='ACTIONS',export_force_sampling=True,
    export_frame_range=False)
print('Validated finite mesh coordinates; corrected meshes:',json.dumps(corrections))
