import bpy,json,math,sys,time,hashlib
from pathlib import Path
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05O');profile=json.loads((HERE.parent/'E03/inputs/projection-candidates.json').read_text())[2];scene=bpy.context.scene;rig=bpy.data.objects['WizardRig'];started=time.monotonic();batch=sys.argv[sys.argv.index('--')+1]if'--'in sys.argv else'batch-01';out=HERE/'evidence'/batch
if out.exists():raise RuntimeError('Refuse overwrite')
out.mkdir(parents=True);scene.render.engine='CYCLES';scene.cycles.samples=128;scene.cycles.use_denoising=False;scene.render.resolution_x=2880;scene.render.resolution_y=1920;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8';scene.render.image_settings.compression=70
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


col=bpy.data.collections['Wizard_Character'];allmeshes=[o for o in col.objects if o.type=='MESH'];gear=[o for o in allmeshes if o.name.startswith('GEAR_')];body=[o for o in allmeshes if o not in gear];hair=[o for o in body if 'hair' in o.name.lower()];saved={o.name:list(o.data.materials)for o in allmeshes};indices={o.name:[p.material_index for p in o.data.polygons]for o in allmeshes};rays={o.name:{a:getattr(o,a)for a in ['visible_shadow','visible_diffuse','visible_glossy','visible_transmission','visible_volume_scatter']}for o in hair}
def simple(name,type):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.node_tree.nodes.clear();s=m.node_tree.nodes.new(type);out=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(s.outputs[0],out.inputs['Surface']);return m
hold=simple('E05O holdout','ShaderNodeHoldout');white=simple('E05O visibility white','ShaderNodeEmission');original=rig.matrix_world.copy();rig.animation_data.action=bpy.data.actions['E05M_idle'];scene.frame_set(0);records=[]
conditions=['raw','partition']if batch=='batch-01'else['partition'];headings=[45,225]if batch=='batch-01'else [h for h in range(0,360,45)if h not in [45,225]]
for condition in conditions:
 dest=out/condition;dest.mkdir()
 for o in hair:
  for a,v in rays[o.name].items():setattr(o,a,False if condition=='partition'else v)
 for degrees in headings:
  rig.matrix_world=Matrix.Rotation(math.radians(-degrees),4,'Z')@original;bpy.context.view_layer.update()
  modes=['full-hidden','full-head','base-nohair','hair-layer','armor-layer','head-layer']+(['body-mask-head','body-mask-hidden']if condition=='partition'else[])
  for mode in modes:
   for o in allmeshes:
    ish=o in hair;isg=o in gear;head=o.name=='GEAR_helmet';chosen=None;o.hide_render=False
    if mode in ['base-nohair','full-head','head-layer','armor-layer','body-mask-head'] and ish:o.hide_render=True
    if mode=='base-nohair'and isg:o.hide_render=True
    if mode in ['full-hidden','hair-layer','armor-layer','body-mask-hidden']and head:o.hide_render=True
    if mode.endswith('layer'):
     show=(ish if mode=='hair-layer'else isg and not head if mode=='armor-layer'else head)
     if not show:chosen=hold
     if condition=='raw'and isg and mode in ['hair-layer','head-layer']and not show:o.hide_render=True
    if mode.startswith('body-mask'):chosen=hold if isg or ish else white
    o.data.materials.clear()
    for m in ([chosen]*max(1,len(saved[o.name]))if chosen else saved[o.name]):o.data.materials.append(m)
    for poly,k in zip(o.data.polygons,indices[o.name]):poly.material_index=k
   name=f'idle-000-h{degrees:03}-{mode}.png';scene.render.filepath=str(dest/name)
   if time.monotonic()-started>720:raise RuntimeError('12 minute batch limit')
   assert sum(f.stat().st_size for f in HERE.rglob('*')if f.is_file())+2000000<50000000
   bpy.ops.render.render(write_still=True);records.append({'condition':condition,'heading':degrees,'mode':mode,'path':str((dest/name).relative_to(HERE)),'sha256':hashlib.sha256((dest/name).read_bytes()).hexdigest()})
(out/'render.json').write_text(json.dumps({'records':records,'samples':128,'denoise':False,'hair_secondary_rays':{'raw':'source unchanged','partition':False},'camera_checks':checks,'crop':crop,'pivot':[target[0]-crop[0],target[1]-crop[1]],'source_frame_vertical_body_height_px':target[1]-pixel((0,0,2))[1],'source':bpy.data.filepath,'source_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'seconds':time.monotonic()-started},indent=2));print('E05O_RENDER_DONE',len(records))
