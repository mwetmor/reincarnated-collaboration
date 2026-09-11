import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05C')
source=Path(bpy.data.filepath);source_hash=hashlib.sha256(source.read_bytes()).hexdigest();changes=[]
for o in bpy.data.collections['Wizard_Character'].objects:
 if o.type!='MESH':continue
 panel=o.name.startswith(('Split robe ','Panel piping ','Panel hem '))
 tabard=o.name.startswith(('Central pointed tabard','Tabard edging'))
 if panel or tabard:
  before=[v.co.z for v in o.data.vertices]
  for v in o.data.vertices:
   if v.co.z<1.104:v.co.z=1.104+(v.co.z-1.104)*(.42 if panel else .50)
  changes.append({'object':o.name,'old_min_z':min(before),'new_min_z':min(v.co.z for v in o.data.vertices),'vertices':len(before)})
# Material probe only: retain face/hair reference and geometry, replace cloth slots.
cloth=bpy.data.materials.new('E05C clean slate cloth');cloth.use_nodes=True
bs=cloth.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.12,.17,.23,1);bs.inputs['Roughness'].default_value=.83
for o in bpy.data.collections['Wizard_Character'].objects:
 if o.type=='MESH'and o.name.startswith(('Tailored upper robe','Robe sleeve','High collar','Split robe','Central pointed tabard')):
  for i in range(len(o.data.materials)):o.data.materials[i]=cloth
gold=bpy.data.materials.get('Antique gold | raised piping')
if gold:
 p=gold.node_tree.nodes.get('Principled BSDF')
 if p:p.inputs['Roughness'].default_value=.5;p.inputs['Metallic'].default_value=.5
# No inherited image or pose changed.
bpy.context.scene.frame_set(0);bpy.context.view_layer.update()
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/short-garment-v1.blend'))
(HERE/'evidence/authoring-v1.json').write_text(json.dumps({'source':str(source),'source_sha256':source_hash,'changes':changes,'output_sha256':hashlib.sha256((HERE/'inputs/short-garment-v1.blend').read_bytes()).hexdigest(),'material':'clean matte slate probe; not hand-painted artwork'},indent=2))
print('E05C_AUTHORED',len(changes))
