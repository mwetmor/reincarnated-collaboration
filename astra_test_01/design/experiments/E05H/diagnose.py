import bpy,json,math,sys,time,hashlib
from pathlib import Path
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05H');profile=json.loads((HERE.parent/'E03/inputs/projection-candidates.json').read_text())[2];scene=bpy.context.scene;rig=bpy.data.objects['WizardRig'];started=time.monotonic();batch=sys.argv[sys.argv.index('--')+1]if'--'in sys.argv else'batch-01';out=HERE/'evidence'/batch
if out.exists():raise RuntimeError('Refuse overwrite')
out.mkdir(parents=True);scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.render.resolution_x=11520;scene.render.resolution_y=7680;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8';scene.render.image_settings.compression=70
for o in bpy.data.objects:
 if o.type=='LIGHT' or (o.type=='MESH'and o.name not in bpy.data.collections['Wizard_Character'].objects):o.hide_render=True
world=bpy.data.worlds.new('E05M neutral authoring world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.65,.65,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5;scene.world=world
light=bpy.data.lights.new('E05M key','AREA');light.energy=400;light.shape='DISK';light.size=4;lo=bpy.data.objects.new('E05M key',light);scene.collection.objects.link(lo);lo.location=(-4,-1,6);lo.rotation_euler=(Vector((0,0,1))-lo.location).to_track_quat('-Z','Y').to_euler()
camdata=bpy.data.cameras.new('E05M camera C');cam=bpy.data.objects.new('E05M camera C',camdata);scene.collection.objects.link(cam);scene.camera=cam;e=math.radians(profile['elevation_deg']);y=math.radians(profile['yaw_deg']);D=profile['distance_m'];cam.location=(math.sin(y)*D*math.cos(e),-math.cos(y)*D*math.cos(e),D*math.sin(e));cam.rotation_euler=(-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='PERSP';camdata.sensor_fit='VERTICAL';camdata.sensor_height=36;f=202.5/math.tan(math.radians(profile['vertical_fov_deg'])/2)*16;camdata.lens=f/7680*36
bpy.context.view_layer.update()
def pixel(p):
 v=world_to_camera_view(scene,cam,Vector(p));return[v.x*11520,(1-v.y)*7680]
base=pixel((0,0,0));camdata.shift_x=.01;dx=[a-b for a,b in zip(pixel((0,0,0)),base)];camdata.shift_x=0;camdata.shift_y=.01;dy=[a-b for a,b in zip(pixel((0,0,0)),base)];camdata.shift_y=0;target=[v*16 for v in profile['anchor']];rhs=[a-b for a,b in zip(target,base)];det=dx[0]*dy[1]-dx[1]*dy[0];camdata.shift_x=.01*(rhs[0]*dy[1]-rhs[1]*dy[0])/det;camdata.shift_y=.01*(dx[0]*rhs[1]-dx[1]*rhs[0])/det
checks=[]
for u,v,h in [(0,0,0),(0,0,2),(1,0,0),(0,1,0),(-1,-1,1)]:
 depth=math.sin(y)*u+math.cos(y)*v;factor=f/(D-math.cos(e)*depth-math.sin(e)*h);expected=[target[0]+factor*(math.cos(y)*u-math.sin(y)*v),target[1]+factor*(math.sin(e)*depth-math.cos(e)*h)];actual=pixel((u,-v,h));checks.append({'world':[u,v,h],'actual':actual,'expected':expected,'error_px':math.dist(actual,expected)})
assert max(c['error_px']for c in checks)/4<.01,checks
crop=[1187,600,512,512];scene.render.use_border=True;scene.render.use_crop_to_border=True;scene.render.border_min_x=crop[0]/11520;scene.render.border_max_x=(crop[0]+crop[2])/11520;scene.render.border_min_y=(7680-crop[1]-crop[3])/7680;scene.render.border_max_y=(7680-crop[1])/7680


motion=json.loads((HERE.parent/'E05M/evidence/source-motion.json').read_text());rig.animation_data.action=bpy.data.actions[motion['clips']['idle']['action']];scene.frame_set(0);original_matrix=rig.matrix_world.copy()
head=[]
for o in bpy.data.collections['Wizard_Character'].objects:
 if o.type!='MESH':continue
 if not o.name.startswith('GEAR_')and any(g.name=='Head'for g in o.vertex_groups):head.append(o)
 else:o.hide_render=True
assert head
corners=[]
for deg in [45,135,225,315]:
 rig.matrix_world=Matrix.Rotation(math.radians(-deg),4,'Z')@original_matrix;bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 for o in head:
  ev=o.evaluated_get(dg);me=ev.to_mesh();corners += [pixel(ev.matrix_world@v.co)for v in me.vertices];ev.to_mesh_clear()
x0=math.floor(min(p[0]for p in corners))-16;y0=math.floor(min(p[1]for p in corners))-16;x1=math.ceil(max(p[0]for p in corners))+16;y1=math.ceil(max(p[1]for p in corners))+16;crop=[x0,y0,x1-x0,y1-y0]
if batch!='batch-01':
 crop=json.loads((HERE/'evidence/batch-01/render.json').read_text())['crop'];x0,y0,w,h=crop;x1=x0+w;y1=y0+h
scene.render.border_min_x=x0/11520;scene.render.border_max_x=x1/11520;scene.render.border_min_y=(7680-y1)/7680;scene.render.border_max_y=(7680-y0)/7680
saved={o.name:list(o.data.materials)for o in head};indices={o.name:[p.material_index for p in o.data.polygons]for o in head};categories={};idmaterials={}
for category,color in [('skin',(.0,1,1,1)),('hair',(1,0,1,1)),('nose',(0,1,0,1)),('ear',(1,1,0,1))]:
 m=bpy.data.materials.new('E05H ID '+category);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs['Color'].default_value=color;o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs['Surface']);idmaterials[category]=m
for o in head:categories[o.name]='nose'if'Nose'in o.name else'ear'if'Ear'in o.name else'skin'if o.name=='Sculpted head'else'hair'
records=[]
for deg in [45,135,225,315]:
 rig.matrix_world=Matrix.Rotation(math.radians(-deg),4,'Z')@original_matrix;bpy.context.view_layer.update()
 for mode in (['natural','ids','bad-hide-hair']if deg==225 and batch!='batch-01'else['natural','ids']):
  for o in head:
   o.hide_render=(mode=='bad-hide-hair'and categories[o.name]=='hair');o.data.materials.clear()
   for m in(saved[o.name]if mode=='natural'else[idmaterials[categories[o.name]]]*max(1,len(saved[o.name]))):o.data.materials.append(m)
   for p,i in zip(o.data.polygons,indices[o.name]):p.material_index=i
  name=f'head-h{deg:03}-{mode}.png';scene.render.filepath=str(out/name);bpy.ops.render.render(write_still=True);records.append({'heading':deg,'mode':mode,'path':name})
(out/'render.json').write_text(json.dumps({'records':records,'head_objects':categories,'crop':crop,'camera_checks':checks,'source_sampling_ratio':4,'loaded_source':bpy.data.filepath,'source':'../E05G/inputs/gear-v1.blend','source_sha256':hashlib.sha256((HERE.parent/'E05G/inputs/gear-v1.blend').read_bytes()).hexdigest()},indent=2));print('HEAD_DIAGNOSIS_RENDERED',len(records),crop)
