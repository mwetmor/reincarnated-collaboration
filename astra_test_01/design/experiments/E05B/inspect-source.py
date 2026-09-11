import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
out=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05B/inputs');c=bpy.data.collections['Wizard_Character'];r={'objects':[],'source_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()}
rig=bpy.data.objects['WizardRig'];rig.animation_data.action=None
for t in rig.animation_data.nla_tracks:t.mute=True
for b in rig.pose.bones:b.matrix_basis.identity()
bpy.context.view_layer.update()
for o in c.objects:
 if o.type=='MESH':
  coords=[o.matrix_world@Vector(p)for p in o.bound_box];r['objects'].append({'name':o.name,'vertices':len(o.data.vertices),'materials':[s.material.name if s.material else None for s in o.material_slots],'bounds':[[min(v[i]for v in coords),max(v[i]for v in coords)]for i in range(3)],'groups':[g.name for g in o.vertex_groups],'parent':o.parent.name if o.parent else None})
r['bounds']=[[min(o['bounds'][i][0]for o in r['objects']),max(o['bounds'][i][1]for o in r['objects'])]for i in range(3)];(out/'source-structure.json').write_text(json.dumps(r,indent=2));print('SOURCE',json.dumps({'bounds':r['bounds'],'boot_objects':[o['name']for o in r['objects']if'boot'in o['name'].lower()],'book_objects':[o['name']for o in r['objects']if any(x in o['name'].lower()for x in ['book','tome'])]}))
