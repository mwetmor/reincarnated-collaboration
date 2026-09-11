import bpy,json
from pathlib import Path
p=Path(__file__).resolve().parent;rows=[]
for o in bpy.data.collections['Wizard_Character'].objects:
 if o.type!='MESH':continue
 rows.append({'name':o.name,'vertices':len(o.data.vertices),'bounds':[[min(v.co[i]for v in o.data.vertices),max(v.co[i]for v in o.data.vertices)]for i in range(3)],'groups':[g.name for g in o.vertex_groups],'materials':[m.name for m in o.data.materials],'uvs':[u.name for u in o.data.uv_layers],'modifiers':[(m.name,m.type)for m in o.modifiers]})
(p/'evidence/source-inspection.json').write_text(json.dumps({'objects':rows,'bones':[b.name for b in bpy.data.objects['WizardRig'].data.bones],'actions':[a.name for a in bpy.data.actions]},indent=2))
print(json.dumps([r for r in rows if any(w in r['name'].lower()for w in ['boot','forearm','cuff','wrist','shin','gear','sleeve'])],indent=2))
