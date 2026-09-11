import bpy,json,hashlib
from pathlib import Path
r=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E07S');source=r.parent/'E07R';layout=json.loads((source/'inputs/layout.json').read_text());result={'schema_version':1,'layout':layout,'factions':{},'geometry_source':'../E07R/inputs/','qualification':'Geometry/material proof only'}
for faction in ['F01','F02']:
 p=source/f'inputs/{faction}-guide.blend';bpy.ops.wm.open_mainfile(filepath=str(p));objects=[];actors=[]
 for o in bpy.data.objects:
  if o.type!='MESH':continue
  if o.name.startswith('scale-'):actors.append({'id':o.name[6:],'source_probe':o.name});continue
  if o.name in ['east-open-leaf','west-open-leaf','internal-gate-raised']:continue
  vertices=[[float(p[0]),float(-p[1]),float(p[2])]for p in [o.matrix_world@v.co for v in o.data.vertices]];lo=[min(v[i]for v in vertices)for i in range(3)];hi=[max(v[i]for v in vertices)for i in range(3)]
  mat=o.data.materials[0].name;material_id='timber'if mat=='blackened timber'else'rock'if mat=='carved reservoir rock'else'soil'if mat=='interior earth'else'iron'if mat=='iron bronze'else'stone'
  role='floor'if o.name in ['interior-stone','interior-soil','west-apron','east-apron']else'prop'if o.name in ['chest','crate']else'structure'
  objects.append({'id':o.name,'role':role,'material_id':material_id,'bounds':[lo,hi],'faces':[[vertices[i]for i in p.vertices]for p in o.data.polygons]})
 result['factions'][faction]={'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'objects':objects,'actors':actors}
 assert sorted(a['id']for a in actors)==['mage','monster','npc']
 assert {o['id']for o in objects if o['role']=='prop'}=={'chest','crate'}
(r/'inputs/scene.json').write_text(json.dumps(result,indent=2)+'\n')
print('EXPORTED',[(k,len(v['objects']))for k,v in result['factions'].items()])
