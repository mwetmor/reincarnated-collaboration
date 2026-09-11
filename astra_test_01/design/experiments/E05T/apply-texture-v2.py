import bpy,json,hashlib,struct
from pathlib import Path
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05T')
mapping=json.loads((HERE/'inputs/texture-projection.json').read_text());rig=bpy.data.objects['WizardRig'];action=rig.animation_data.action
def geometry():
 h=hashlib.sha256()
 for o in bpy.data.collections['Wizard_Character'].objects:
  if o.type!='MESH':continue
  h.update(o.name.encode())
  for v in o.data.vertices:
   h.update(struct.pack('3d',*v.co))
   for g in v.groups:h.update(struct.pack('id',g.group,g.weight))
 return h.hexdigest()
before=geometry();changed=[];image=bpy.data.images.load(str(HERE/'art/texture-v2.png'));mat=bpy.data.materials.new('E05T generated painted cloth');mat.use_nodes=True
bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.83;tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image;tex.interpolation='Linear';uvnode=mat.node_tree.nodes.new('ShaderNodeUVMap');uvnode.uv_map='E05TProjected';mat.node_tree.links.new(uvnode.outputs['UV'],tex.inputs['Vector']);mat.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
prefix=('Tailored upper robe','Robe sleeve','High collar','Split robe','Central pointed tabard','Trouser','Boot foot ','Boot shaft ')
for name,polys in mapping['maps'].items():
 o=bpy.data.objects[name]
 if not name.startswith(prefix):continue
 uv=o.data.uv_layers.new(name='E05TProjected')
 for poly,data in zip(o.data.polygons,polys):
  for index,value in zip(poly.loop_indices,data['uvs']):uv.data[index].uv=value
 for i in range(len(o.data.materials)):o.data.materials[i]=mat
 changed.append(name)
after=geometry();assert before==after;assert rig.animation_data.action==action
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/painted-texture-v2.blend'))
(HERE/'evidence/texture-application-v2.json').write_text(json.dumps({'geometry_weights_sha256_before':before,'geometry_weights_sha256_after':after,'unchanged_action':action.name,'changed_material_objects':changed,'source_texture_sha256':hashlib.sha256((HERE/'art/texture-v2.png').read_bytes()).hexdigest(),'limitations':'Orthographic projected textures can stretch on sides or retain occluded material; no style pass inferred.'},indent=2))
print('TEXTURE_APPLIED',len(changed))
