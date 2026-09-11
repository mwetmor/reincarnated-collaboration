import bpy,json,hashlib,struct,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05H');source=HERE.parent/'E05G/inputs/gear-v1.blend';original_sha=hashlib.sha256(source.read_bytes()).hexdigest();head=bpy.data.objects['Sculpted head'];hair=bpy.data.objects['Swept hair mass'];objects=[o for o in bpy.data.collections['Wizard_Character'].objects if o.type=='MESH']
def geometry(objects):
 h=hashlib.sha256()
 for o in sorted(objects,key=lambda o:o.name):
  h.update(o.name.encode())
  for v in o.data.vertices:
   h.update(struct.pack('3d',*v.co))
   for g in v.groups:h.update(struct.pack('id',g.group,g.weight))
 return h.hexdigest()
others=[o for o in objects if o!=hair];before=geometry(others);hair_before=geometry([hair]);bvh=BVHTree.FromPolygons([v.co.copy()for v in head.data.vertices],[list(p.vertices)for p in head.data.polygons],all_triangles=False);tohead=head.matrix_world.inverted()@hair.matrix_world;tohair=tohead.inverted();changes=[]
for v in hair.data.vertices:
 p=tohead@v.co;origin=Vector((0,.012,p.z));delta=p-origin;r=delta.length
 if r<.00001:continue
 direction=delta.normalized();hit,normal,index,distance=bvh.ray_cast(origin,direction,1)
 if hit is None:continue
 if r<distance+.004:
  q=origin+direction*(distance+.004);new=tohair@q;changes.append({'index':v.index,'before':list(v.co),'after':list(new),'displacement_m':(new-v.co).length});v.co=new
hair.data.update();assert changes;assert geometry(others)==before;assert original_sha==hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/head-shell-v1.blend'))
(HERE/'evidence/repair-v1.json').write_text(json.dumps({'source_sha256':original_sha,'output_sha256':hashlib.sha256((HERE/'inputs/head-shell-v1.blend').read_bytes()).hexdigest(),'non_hair_sha256_before':before,'non_hair_sha256_after':geometry(others),'hair_before':hair_before,'hair_after':geometry([hair]),'changed_vertices':len(changes),'maximum_vertex_displacement_m':max(x['displacement_m']for x in changes),'changes':changes},indent=2));print('HAIR_REPAIR',len(changes),max(x['displacement_m']for x in changes))
