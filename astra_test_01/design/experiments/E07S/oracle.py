import bpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
r=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E07S');content=json.loads((r/'inputs/scene.json').read_text());data={}
for faction in ['F01','F02']:
 bpy.ops.wm.open_mainfile(filepath=str(r.parent/f'E07R/inputs/{faction}-guide.blend'));scene=bpy.context.scene;cam=scene.camera
 for o in list(bpy.data.objects):
  if o.name.startswith('scale-'):bpy.data.objects.remove(o,do_unlink=True)
 def vec(p):return Vector((p[0],-p[1],p[2]))
 def pixel(p):
  q=world_to_camera_view(scene,cam,vec(p));return[q.x*1536,(1-q.y)*1024]
 def objname(o):return o.name.replace('-open-leaf','-leaf')if o else None
 records=[]
 for state in ['open','closed']:
  for ex in content['layout']['exits']:
   x,y=ex['leaf']['hinge'];ang=math.radians(ex['leaf']['open_angle_deg']if state=='open'else 0);u=-math.sin(ang)*2.5;v=math.cos(ang)*2.5;lo=[min(x,x+u)-.06,min(y,y+v)-.06,0];hi=[max(x,x+u)+.06,max(y,y+v)+.06,2.45];o=bpy.data.objects[ex['id']+'-open-leaf'];o.location=((lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,1.225);o.dimensions=(hi[0]-lo[0],hi[1]-lo[1],2.45)
  bpy.context.view_layer.update()
  witnesses=[]
  for key,point in [('near-interior',[4.5,-.3,0]),('near-exterior',[6.2,0,0]),('far-exterior',[-5.7,-.6,0]),('light-receiver',[3,0,0])]:
   d=vec(point)-cam.location;hit,loc,n,idx,o,m=scene.ray_cast(bpy.context.evaluated_depsgraph_get(),cam.location,d.normalized());witnesses.append({'id':key,'point':point,'source_pixel':pixel(point),'first_object':objname(o)if hit else None})
  point=vec([3,0,.01]);light=vec([5.8,-.6,2]);d=light-point;hit,loc,n,idx,o,m=scene.ray_cast(bpy.context.evaluated_depsgraph_get(),point,d.normalized(),distance=d.length);records.append({'state':state,'witnesses':witnesses,'receiver_light_blocked':bool(hit),'light_occluder':objname(o)if hit else None})
 data[faction]={'records':records}
(r/'evidence/source-oracle.json').write_text(json.dumps(data,indent=2)+'\n')
print('ORACLE',[(f,[(x['state'],x['receiver_light_blocked'],[w['first_object']for w in x['witnesses']])for x in v['records']])for f,v in data.items()])
