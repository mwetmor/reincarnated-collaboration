import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05T');scene=bpy.context.scene;rig=bpy.data.objects['WizardRig'];rig.animation_data.action=None
for track in rig.animation_data.nla_tracks:track.mute=True
for bone in rig.pose.bones:bone.matrix_basis.identity()
bpy.context.view_layer.update()
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.render.resolution_x=768;scene.render.resolution_y=1024;scene.render.resolution_percentage=100;scene.render.use_border=False;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
for o in bpy.data.objects:
 if o.type=='LIGHT'or(o.type=='MESH'and o.name not in bpy.data.collections['Wizard_Character'].objects):o.hide_render=True
world=bpy.data.worlds.new('Neutral texture guide');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.8,.8,.8,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.world=world
cameras={}
for name,sign in [('front',1),('back',-1)]:
 ld=bpy.data.lights.new(name+' neutral guide light','AREA');ld.energy=250;ld.size=5;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.location=(sign*4,-3,5);lo.rotation_euler=(Vector((0,0,1))-lo.location).to_track_quat('-Z','Y').to_euler()
 cd=bpy.data.cameras.new(name+' orthographic texture guide');cam=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(cam);cam.location=(sign*6,0,1);cam.rotation_euler=(Vector((0,0,1))-cam.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=2.5;cameras[name]=cam
 scene.camera=cam;bpy.context.view_layer.update();scene.render.filepath=str(HERE/'inputs'/f'{name}-guide.png');bpy.ops.render.render(write_still=True)
# Store UV projection per actual source polygon corner. Material assignment is separate.
maps={}
for o in bpy.data.collections['Wizard_Character'].objects:
 if o.type!='MESH':continue
 data=[]
 for poly in o.data.polygons:
  normal=o.matrix_world.to_3x3()@poly.normal;name='front'if normal.x>=0 else'back';cam=cameras[name];uvs=[]
  for idx in poly.loop_indices:
   co=o.matrix_world@o.data.vertices[o.data.loops[idx].vertex_index].co;v=world_to_camera_view(scene,cam,co);uvs.append([(v.x+(0 if name=='front'else 1))/2,v.y])
  data.append({'polygon':poly.index,'view':name,'uvs':uvs})
 maps[o.name]=data
(HERE/'inputs/texture-projection.json').write_text(json.dumps({'source':'../E05C/inputs/short-garment-v1.blend','canvas':[1536,1024],'tile':[768,1024],'camera':'front/back orthographic; ortho_scale2.5; targetZ1','maps':maps},separators=(',',':')))
print('GUIDES_READY')
