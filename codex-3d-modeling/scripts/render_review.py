import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path('/Users/admin/Games/reincarnated-collaboration/codex-3d-modeling')
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.samples=24
scene.render.resolution_x=900
scene.render.resolution_y=1000
camera=scene.camera
for name,loc in [('front',(0,-5,1.04)),('three_quarter',(2.6,-5,2.3)),('rear',(2.5,5,2.1))]:
    camera.location=loc
    camera.rotation_euler=(Vector((0,0,.96))-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(ROOT/'renders'/f'wizard_{name}.png')
    bpy.ops.render.render(write_still=True)
print('Review renders saved')
