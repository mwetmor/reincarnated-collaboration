import bpy,json,math,sys,time,hashlib
from pathlib import Path
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05A');profile=json.loads((HERE.parent/'E03/inputs/projection-candidates.json').read_text())[2];scene=bpy.context.scene;rig=bpy.data.objects['WizardRig'];started=time.monotonic();batch=sys.argv[sys.argv.index('--')+1]if'--'in sys.argv else'batch-01';out=HERE/'evidence'/batch
if out.exists():raise RuntimeError('Refuse overwrite')
out.mkdir(parents=True);scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.render.resolution_x=2880;scene.render.resolution_y=1920;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8';scene.render.image_settings.compression=70
for o in bpy.data.objects:
 if o.type=='LIGHT' or (o.type=='MESH'and o.name not in bpy.data.collections['Wizard_Character'].objects):o.hide_render=True
world=bpy.data.worlds.new('E05M neutral authoring world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.65,.65,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5;scene.world=world
light=bpy.data.lights.new('E05M key','AREA');light.energy=400;light.shape='DISK';light.size=4;lo=bpy.data.objects.new('E05M key',light);scene.collection.objects.link(lo);lo.location=(-4,-1,6);lo.rotation_euler=(Vector((0,0,1))-lo.location).to_track_quat('-Z','Y').to_euler()
camdata=bpy.data.cameras.new('E05M camera C');cam=bpy.data.objects.new('E05M camera C',camdata);scene.collection.objects.link(cam);scene.camera=cam;e=math.radians(profile['elevation_deg']);y=math.radians(profile['yaw_deg']);D=profile['distance_m'];cam.location=(math.sin(y)*D*math.cos(e),-math.cos(y)*D*math.cos(e),D*math.sin(e));cam.rotation_euler=(-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='PERSP';camdata.sensor_fit='VERTICAL';camdata.sensor_height=36;f=202.5/math.tan(math.radians(profile['vertical_fov_deg'])/2)*4;camdata.lens=f/1920*36
bpy.context.view_layer.update()
def pixel(p):
 v=world_to_camera_view(scene,cam,Vector(p));return[v.x*2880,(1-v.y)*1920]
base=pixel((0,0,0));camdata.shift_x=.01;dx=[a-b for a,b in zip(pixel((0,0,0)),base)];camdata.shift_x=0;camdata.shift_y=.01;dy=[a-b for a,b in zip(pixel((0,0,0)),base)];camdata.shift_y=0;target=[v*4 for v in profile['anchor']];rhs=[a-b for a,b in zip(target,base)];det=dx[0]*dy[1]-dx[1]*dy[0];camdata.shift_x=.01*(rhs[0]*dy[1]-rhs[1]*dy[0])/det;camdata.shift_y=.01*(dx[0]*rhs[1]-dx[1]*rhs[0])/det
checks=[]
for u,v,h in [(0,0,0),(0,0,2),(1,0,0),(0,1,0),(-1,-1,1)]:
 depth=math.sin(y)*u+math.cos(y)*v;factor=f/(D-math.cos(e)*depth-math.sin(e)*h);expected=[target[0]+factor*(math.cos(y)*u-math.sin(y)*v),target[1]+factor*(math.sin(e)*depth-math.cos(e)*h)];actual=pixel((u,-v,h));checks.append({'world':[u,v,h],'actual':actual,'expected':expected,'error_px':math.dist(actual,expected)})
assert max(c['error_px']for c in checks)<.01,checks
crop=[1187,600,512,512];scene.render.use_border=True;scene.render.use_crop_to_border=True;scene.render.border_min_x=crop[0]/2880;scene.render.border_max_x=(crop[0]+crop[2])/2880;scene.render.border_min_y=(1920-crop[1]-crop[3])/1920;scene.render.border_max_y=(1920-crop[1])/1920


motion=json.loads((HERE.parent/'E05M/evidence/source-motion.json').read_text());poses=[('idle',0),('walk',12),('walk',24),('cast',18),('cast',36),('cast',54)]
body=[o for o in bpy.data.collections['Wizard_Character'].objects if o.type=='MESH'and not o.name.startswith('GEAR_')]
gear=[o for o in bpy.data.objects if o.name.startswith('GEAR_')and o.type=='MESH'];saved={o.name:list(o.data.materials) for o in body}
indices={o.name:[p.material_index for p in o.data.polygons]for o in body}
hold=bpy.data.materials.new('E05G body holdout');hold.use_nodes=True;nodes=hold.node_tree.nodes;nodes.clear();h=nodes.new('ShaderNodeHoldout');output=nodes.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],output.inputs['Surface'])
original_matrix=rig.matrix_world.copy();records=[];geometry_checks=[]
poses=[('idle',0)]
source_hash=hashlib.sha256((HERE.parent/'E05H/inputs/head-shell-v1.blend').read_bytes()).hexdigest()
def mesh_points():
 dg=bpy.context.evaluated_depsgraph_get();result={}
 for o in body+gear:
  ev=o.evaluated_get(dg);me=ev.to_mesh();indices=range(0,len(me.vertices),max(1,len(me.vertices)//64));result[o.name]=[list(ev.matrix_world@me.vertices[i].co)for i in indices];ev.to_mesh_clear()
 return result
for kind,frame in poses:
 rig.matrix_world=original_matrix;rig.animation_data.action=bpy.data.actions[motion['clips'][kind]['action']];scene.frame_set(frame);bpy.context.view_layer.update();baseline=mesh_points();base_socket=rig.matrix_world@rig.pose.bones['Hand.R'].tail
 for degrees in range(0,360,45):
  rotation=Matrix.Rotation(math.radians(-degrees),4,'Z');rig.matrix_world=rotation@original_matrix;bpy.context.view_layer.update();actual=mesh_points();inverse=rotation.inverted();residual=max(math.dist(inverse@Vector(p),q)for name,points in actual.items()for p,q in zip(points,baseline[name]));socket=rig.matrix_world@rig.pose.bones['Hand.R'].tail;socket_error=math.dist(socket,rotation@base_socket);assert residual<.00001 and socket_error<.00001,(degrees,residual,socket_error)
  geometry_checks.append({'clip':kind,'frame':frame,'canonical_heading_deg':degrees,'inverse_rotated_mesh_max_error_m':residual,'sampled_vertices':sum(map(len,actual.values())),'socket_rotation_error_m':socket_error,'socket_world_blender':list(socket),'socket_source_px':[v-crop[i]for i,v in enumerate(pixel(socket))]})
  for mode in (['full-hidden','full-head'] if batch=='batch-01' else ['full-hidden','full-head','base-nohair','hair-layer','armor-layer','head-layer','full-hair-bad']):
   for o in body:
    is_hair='hair' in o.name.lower()
    o.hide_render=is_hair and mode in ['full-head','base-nohair','armor-layer','head-layer']
    o.data.materials.clear()
    for m in ([hold]*max(1,len(saved[o.name]))if mode.endswith('layer') and not(mode=='hair-layer' and is_hair)else saved[o.name]):o.data.materials.append(m)
    for p,i in zip(o.data.polygons,indices[o.name]):p.material_index=i
   for o in gear:o.hide_render=(True if mode in ['base','base-nohair','hair-layer']else o.name=='GEAR_helmet'if mode in ['full-hidden','armor-layer']else o.name!='GEAR_helmet'if mode=='head-layer'else False)
   name=f'{kind}-{frame:03}-h{degrees:03}-{mode}.png';scene.render.filepath=str(out/name);t=time.monotonic()
   assert sum(p.stat().st_size for p in HERE.rglob('*')if p.is_file())+2000000<100000000
   if time.monotonic()-started>720:raise RuntimeError('Render batch12minute cap')
   bpy.ops.render.render(write_still=True)
   records.append({'clip':kind,'frame':frame,'heading_deg':degrees,'mode':mode,'file':name,'seconds':time.monotonic()-t,'sha256':hashlib.sha256((out/name).read_bytes()).hexdigest()})
assert source_hash==hashlib.sha256((HERE.parent/'E05H/inputs/head-shell-v1.blend').read_bytes()).hexdigest()
(out/'render.json').write_text(json.dumps({'records':records,'geometry_checks':geometry_checks,'camera_checks':checks,'crop':crop,'pivot':[target[0]-crop[0],target[1]-crop[1]],'source_frame_vertical_body_height_px':target[1]-pixel((0,0,2))[1],'elapsed_seconds':time.monotonic()-started,'lineage_source':'../E05H/inputs/head-shell-v1.blend','lineage_source_sha256':source_hash,'loaded_source':bpy.data.filepath,'loaded_source_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'limitation':'Sparse poses, gear ray visibility disabled; no full lighting/motion/art pass'},indent=2))
print('VIEW_RENDER_DONE',len(records),time.monotonic()-started)
