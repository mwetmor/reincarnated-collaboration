import bpy,json,hashlib,struct
from pathlib import Path
HERE=Path(__file__).resolve().parent;col=bpy.data.collections['Wizard_Character'];rig=bpy.data.objects['WizardRig'];mapping=json.loads((HERE.parent/'E05T/inputs/texture-projection.json').read_text());names=['Tailored shoulder L','Tailored shoulder R'];mat=bpy.data.materials['E05T generated painted cloth'];actions=[a.name for a in bpy.data.actions]
def geometry():
 h=hashlib.sha256()
 for o in sorted([o for o in col.objects if o.type=='MESH'],key=lambda o:o.name):
  h.update(o.name.encode())
  for v in o.data.vertices:
   h.update(struct.pack('3d',*v.co))
   for g in v.groups:h.update(struct.pack('id',g.group,g.weight))
 return h.hexdigest()
before=geometry();records=[]
for name in names:
 o=bpy.data.objects[name];old=[m.name for m in o.data.materials];uv=o.data.uv_layers.new(name='E05TProjected');polys=mapping['maps'][name];assert len(polys)==len(o.data.polygons)
 for p,d in zip(o.data.polygons,polys):
  assert len(p.loop_indices)==len(d['uvs'])
  for li,value in zip(p.loop_indices,d['uvs']):uv.data[li].uv=value
 for i in range(len(o.data.materials)):o.data.materials[i]=mat
 records.append({'object':name,'old_materials':old,'new_material':mat.name,'uv_source':'../E05T/inputs/texture-projection.json'})
assert geometry()==before;assert actions==[a.name for a in bpy.data.actions];bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/part-painted-gear-v2.blend'));(HERE/'evidence/author-v2.json').write_text(json.dumps({'geometry_weights_unchanged':geometry()==before,'before_sha256':before,'after_sha256':geometry(),'actions_unchanged':True,'changes':records,'scope':'Material/UV repair only for two residual royal-plum starter shoulders. No body silhouette, hair or animation art pass.'},indent=2));print('E05U_V2_PASS')
