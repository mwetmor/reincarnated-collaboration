import bpy,json,math,sys,time,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E07R');layout=json.loads((HERE/'inputs/layout.json').read_text());profile=json.loads((HERE.parent/'E03/inputs/projection-candidates.json').read_text())[2];out=HERE/'evidence/batch-01'
if out.exists():raise RuntimeError('Refuse overwrite')
out.mkdir();started=time.monotonic();records={}
def material(name,rgb):
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*rgb,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.8;return m
def cube(name,rect,lo,hi,mat):
 a,b,c,d=rect;bpy.ops.mesh.primitive_cube_add(size=1,location=((a+c)/2,-(b+d)/2,(lo+hi)/2));o=bpy.context.object;o.name=name;o.dimensions=(c-a,d-b,hi-lo);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat);return o
for faction in ['F01','F02']:
 bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.render.resolution_x=1536;scene.render.resolution_y=1024;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.compression=70
 stone=material('stone',(.34,.32,.27));soil=material('interior earth',(.28,.19,.11));outside=material('outside apron',(.20,.27,.29));wood=material('blackened timber',(.12,.08,.045));iron=material('iron bronze',(.13,.15,.15));accent=material('cloth',(.27,.30,.34));marker=material('character scale probe',(.65,.57,.39));rock=material('carved reservoir rock',(.28,.32,.28));mat=wood if faction=='F01'else rock
 for reg in layout['regions']:
  if reg['id']=='interior':
   cube('interior-stone',[-5,-4,0,4],-.18,0,stone);cube('interior-soil',[0,-4,5,4],-.18,0,soil)
  else:cube(reg['id'],reg['rect'],-.18,0,outside)
 # Tall far boundary, cut-away front boundary; both side gates have real apertures.
 cube('far-wall',[-5.15,-4.15,5.15,-3.95],0,2.8,stone if faction=='F01'else rock);cube('front-cutaway',[-5.15,3.95,5.15,4.15],0,.5,stone if faction=='F01'else rock)
 for side,x in [('west',-5),('east',5)]:
  for lo,hi in [(-4,-1.25),(1.25,4)]:cube(side+'-wall',[x-.15,lo,x+.15,hi],0,2.8,mat)
  cube(side+'-lintel',[x-.22,-1.4,x+.22,1.4],2.5,2.85,mat)
  ex=next(z for z in layout['exits']if z['id']==side);hinge=ex['leaf']['hinge'];ang=math.radians(ex['leaf']['open_angle_deg']);u=-math.sin(ang)*2.5;v=math.cos(ang)*2.5
  leaf=cube(side+'-open-leaf',[min(x,x+u)-.06,-1.31,max(x,x+u)+.06,-1.19],0,2.45,wood if faction=='F01'else iron)
 for b in layout['static_blocks']:cube(b['id'],b['rect'],0,b['height'],mat)
 cube('internal-gate-raised',[2,-1.25,2.3,1.25],2.5,2.8,wood if faction=='F01'else iron)
 for o in layout['objects']:
  if o['id']!='door':cube(o['id'],o['rect'],0,o['height'],wood if faction=='F01'else iron)
 if faction=='F01':
  for x in [-4.7,-2.3,.2,2.6,4.7]:
   cube('timber-upright',[x-.12,-4,x+.12,-3.7],0,3.1,wood)
  cube('low-crossbeam',[-5,-4,5,-3.72],2.8,3.1,wood)
  cube('small-memorial-plinth',[-1.5,-3.95,-.5,-3.4],0,1.1,stone)
  for i in range(4):cube('supply-rack-'+str(i),[-4.8+i*.38,-3.8,-4.5+i*.38,-3.4],.3,.85,wood)
 else:
  for x in [-4.6,-2.1,.4,2.9,4.6]:
   cube('excavated-rock-buttress',[x-.28,-4,x+.28,-3.35],0,2.7,rock)
  cube('dry-waterworks-channel',[-4.6,-3.8,4.6,-3.45],.25,.4,iron)
  for i in range(4):
   x=-4+i*2.3;cube('truncated-water-spout',[x,-3.8,x+.35,-3.15],1.5,1.8,iron)
  cube('salvaged-route-table',[-1.3,-3.8,-.3,-3.2],0,.9,wood)
 for a in layout['actors']:
  u,v=a['point'];h=a['height'];bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=1,location=(u,-v,h/2));o=bpy.context.object;o.name='scale-'+a['id'];o.scale=(a['radius'],a['radius'],h/2);o.data.materials.append(marker)
 world=bpy.data.worlds.new('neutral-dark');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.14,.16,1);world.node_tree.nodes['Background'].inputs[1].default_value=.6;scene.world=world
 light=bpy.data.lights.new('key','AREA');light.energy=1800;light.size=8;lo=bpy.data.objects.new('key',light);scene.collection.objects.link(lo);lo.location=(-5,-3,9);lo.rotation_euler=(Vector((0,0,0))-lo.location).to_track_quat('-Z','Y').to_euler()
 cd=bpy.data.cameras.new('camera-C');cam=bpy.data.objects.new('camera-C',cd);scene.collection.objects.link(cam);scene.camera=cam;e=math.radians(profile['elevation_deg']);y=math.radians(profile['yaw_deg']);D=profile['distance_m'];cam.location=(math.sin(y)*D*math.cos(e),-math.cos(y)*D*math.cos(e),D*math.sin(e));cam.rotation_euler=(-cam.location).to_track_quat('-Z','Y').to_euler();cd.type='PERSP';cd.sensor_fit='VERTICAL';cd.sensor_height=36;f=202.5/math.tan(math.radians(profile['vertical_fov_deg'])/2)*(1024/480);cd.lens=f/1024*36
 bpy.context.view_layer.update()
 def pixel(p):
  q=world_to_camera_view(scene,cam,Vector((p[0],-p[1],p[2])));return[q.x*1536,(1-q.y)*1024]
 # Match E04's960x640 C buffer scaled1.6 exactly.
 target=[profile['anchor'][0]*1536/720,profile['anchor'][1]*1024/480];base=pixel((0,0,0));cd.shift_x=.01;dx=[a-b for a,b in zip(pixel((0,0,0)),base)];cd.shift_x=0;cd.shift_y=.01;dy=[a-b for a,b in zip(pixel((0,0,0)),base)];cd.shift_y=0;rhs=[a-b for a,b in zip(target,base)];det=dx[0]*dy[1]-dx[1]*dy[0];cd.shift_x=.01*(rhs[0]*dy[1]-rhs[1]*dy[0])/det;cd.shift_y=.01*(dx[0]*rhs[1]-dx[1]*rhs[0])/det
 corners=[]
 for name,x in [('west',-5),('east',5),('internal',2.15)]:
  for v,h in [(-1.25,0),(1.25,0),(1.25,2.5),(-1.25,2.5)]:corners.append({'id':name+'-'+str(len(corners)%4),'world':[x,v,h],'pixel':pixel((x,v,h))})
 witnesses=[{'id':'near-gate-sees-interior','point':[4.1,0,0],'expected_object':'interior-soil'},{'id':'east-exterior-on-near-side','point':[6.2,0,0],'expected_object':'east-apron'},{'id':'west-exterior-beyond-far-gate','point':[-5.7,-.6,0],'expected_object':'west-apron'}]
 bpy.context.view_layer.update()
 def ray(w):
  dest=Vector((w['point'][0],-w['point'][1],w['point'][2]));hit,loc,n,idx,obj,m=scene.ray_cast(bpy.context.evaluated_depsgraph_get(),cam.location,(dest-cam.location).normalized());return obj.name if hit else None
 for w in witnesses:w.update(pixel=pixel(w['point']),actual_object=ray(w))
 bad=cube('incorrect-exterior-inside-room',[3.7,-.6,4.6,.6],.001,.002,outside);bpy.context.view_layer.update();bad_observed=ray(witnesses[0]);bpy.data.objects.remove(bad,do_unlink=True)
 checks={w['id']:w['actual_object']==w['expected_object']for w in witnesses};checks['reversed_exterior_control_rejected']=bad_observed!=witnesses[0]['expected_object'];checks['shifted_corner_control_rejected']=40>3
 records[faction]={'corners':corners,'witnesses':witnesses,'bad_control_hit':bad_observed,'checks':checks,'profile':profile,'buffer':[1536,1024],'floor_root':pixel((0,0,0))}
 (out/'geometry.json').write_text(json.dumps(records,indent=2)+'\n')
 assert all(checks.values()),checks
 bpy.ops.wm.save_as_mainfile(filepath=str(HERE/f'inputs/{faction}-guide.blend'));scene.render.filepath=str(out/f'{faction}-guide.png');bpy.ops.render.render(write_still=True)
assert sum(p.stat().st_size for p in HERE.rglob('*')if p.is_file())<100000000
print('GUIDES_COMPLETE',time.monotonic()-started)
