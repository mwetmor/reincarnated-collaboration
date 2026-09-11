import bpy,json,math,sys,time,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05B');profile=json.loads((HERE.parent/'E03/inputs/projection-candidates.json').read_text())[2];scene=bpy.context.scene;rig=bpy.data.objects['WizardRig'];started=time.monotonic();batch=sys.argv[sys.argv.index('--')+1]if'--'in sys.argv else'batch-01';out=HERE/'evidence'/batch
if out.exists():raise RuntimeError('Refuse overwrite')
out.mkdir();scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.render.resolution_x=2880;scene.render.resolution_y=1920;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8';scene.render.image_settings.compression=70
for o in bpy.data.objects:
 if o.type=='LIGHT' or (o.type=='MESH'and o.name not in bpy.data.collections['Wizard_Character'].objects):o.hide_render=True
world=bpy.data.worlds.new('E05B neutral authoring world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.65,.65,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5;scene.world=world
light=bpy.data.lights.new('E05B key','AREA');light.energy=400;light.shape='DISK';light.size=4;lo=bpy.data.objects.new('E05B key',light);scene.collection.objects.link(lo);lo.location=(-4,-1,6);lo.rotation_euler=(Vector((0,0,1))-lo.location).to_track_quat('-Z','Y').to_euler()
camdata=bpy.data.cameras.new('E05B camera C');cam=bpy.data.objects.new('E05B camera C',camdata);scene.collection.objects.link(cam);scene.camera=cam;e=math.radians(profile['elevation_deg']);y=math.radians(profile['yaw_deg']);D=profile['distance_m'];cam.location=(math.sin(y)*D*math.cos(e),math.cos(y)*D*math.cos(e),D*math.sin(e));cam.rotation_euler=(-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='PERSP';camdata.sensor_fit='VERTICAL';camdata.sensor_height=36;f=202.5/math.tan(math.radians(profile['vertical_fov_deg'])/2)*4;camdata.lens=f/1920*36
bpy.context.view_layer.update()
def pixel(p):
 v=world_to_camera_view(scene,cam,Vector(p));return[v.x*2880,(1-v.y)*1920]
base=pixel((0,0,0));camdata.shift_x=.01;dx=[a-b for a,b in zip(pixel((0,0,0)),base)];camdata.shift_x=0;camdata.shift_y=.01;dy=[a-b for a,b in zip(pixel((0,0,0)),base)];camdata.shift_y=0;target=[v*4 for v in profile['anchor']];rhs=[a-b for a,b in zip(target,base)];det=dx[0]*dy[1]-dx[1]*dy[0];camdata.shift_x=.01*(rhs[0]*dy[1]-rhs[1]*dy[0])/det;camdata.shift_y=.01*(dx[0]*rhs[1]-dx[1]*rhs[0])/det
checks=[]
for u,v,h in [(0,0,0),(0,0,2),(1,0,0),(0,1,0),(-1,-1,1)]:
 depth=math.sin(y)*u+math.cos(y)*v;factor=f/(D-math.cos(e)*depth-math.sin(e)*h);expected=[target[0]+factor*(math.cos(y)*u-math.sin(y)*v),target[1]+factor*(math.sin(e)*depth-math.cos(e)*h)];actual=pixel((u,v,h));checks.append({'world':[u,v,h],'actual':actual,'expected':expected,'error_px':math.dist(actual,expected)})
assert max(c['error_px']for c in checks)<.01,checks
crop=[1187,600,512,512];scene.render.use_border=True;scene.render.use_crop_to_border=True;scene.render.border_min_x=crop[0]/2880;scene.render.border_max_x=(crop[0]+crop[2])/2880;scene.render.border_min_y=(1920-crop[1]-crop[3])/1920;scene.render.border_max_y=(1920-crop[1])/1920
frames=[0]if batch=='batch-01'else list(range(0,96,2));records=[];reserved=2000000*len(frames);existing=sum(p.stat().st_size for p in HERE.rglob('*')if p.is_file());assert existing+reserved<=100000000,('capacity',existing,reserved)
for frame in frames:
 if time.monotonic()-started>540:raise RuntimeError('Stop before10min render batch cap')
 scene.frame_set(frame);bpy.context.view_layer.update();name='walk-'+str(frame).zfill(3)+'.png';scene.render.filepath=str(out/name);t=time.monotonic();bpy.ops.render.render(write_still=True);elapsed=time.monotonic()-t;size=(out/name).stat().st_size;records.append({'frame':frame,'t':frame/120,'file':name,'bytes':size,'render_seconds':elapsed,'sha256':hashlib.sha256((out/name).read_bytes()).hexdigest()});assert sum(p.stat().st_size for p in HERE.rglob('*')if p.is_file())<100000000
(out/'render.json').write_text(json.dumps({'profile':profile,'camera_projection_checks':checks,'crop_full_buffer':crop,'native_buffer':[2880,1920],'sprite_root':[target[0]-crop[0],target[1]-crop[1]],'physical_height_m':2,'source_frame_body_height_px':target[1]-pixel((0,0,2))[1],'reserved_bytes':reserved,'records':records,'elapsed_seconds':time.monotonic()-started,'source':'inputs/controlled-wizard-v2.blend','style_status':'UNQUALIFIED; original local3D textured wizard, not approved painted mage'},indent=2));print('RENDER_DONE',len(records),time.monotonic()-started)
