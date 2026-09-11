import bpy,json,hashlib,struct
from pathlib import Path
HERE=Path(__file__).resolve().parent;col=bpy.data.collections['Wizard_Character'];rig=bpy.data.objects['WizardRig']
def geometry():
 h=hashlib.sha256()
 for o in sorted([x for x in col.objects if x.type=='MESH'],key=lambda o:o.name):
  h.update(o.name.encode())
  for v in o.data.vertices:
   h.update(struct.pack('3d',*v.co))
   for g in v.groups:h.update(struct.pack('id',g.group,g.weight))
 return h.hexdigest()
before=geometry();actions=[a.name for a in bpy.data.actions];disabled=[]
for o in col.objects:
 if o.type=='MESH' and o.name.startswith('Swept hair lock'):
  o['default_visible']=False;o.hide_render=True;disabled.append(o.name)
assert len(disabled)==17;assert before==geometry();assert actions==[a.name for a in bpy.data.actions];bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/material-hair-v2.blend'));(HERE/'evidence/author-v2.json').write_text(json.dumps({'checks':{'geometry_weights_unchanged':before==geometry(),'actions_unchanged':True,'exact17legacy_locks_disabled':len(disabled)==17},'geometry_sha256':before,'disabled_objects':disabled,'active_hair_objects':[o.name for o in col.objects if o.get('asset_category')=='hair' and o.get('default_visible',True)],'scope':'Default hairstyle composition only; all legacy geometry retained. Same 23Head bindings, 6default active parts. No second generation.'},indent=2));print('E05W_HAIR_VARIANT',len(disabled))
