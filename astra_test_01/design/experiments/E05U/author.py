import bpy,json,hashlib,struct,math
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;rig=bpy.data.objects['WizardRig'];col=bpy.data.collections['Wizard_Character'];base=[o for o in col.objects if o.type=='MESH' and not o.name.startswith('GEAR_')]
def base_hash():
 h=hashlib.sha256()
 for o in sorted(base,key=lambda o:o.name):
  h.update(o.name.encode())
  for v in o.data.vertices:
   h.update(struct.pack('3d',*v.co))
   for g in v.groups:h.update(struct.pack('id',g.group,g.weight))
 return h.hexdigest()
before=base_hash();actions=[a.name for a in bpy.data.actions];image=bpy.data.images.load(str(HERE/'art/atlas-v1.png'));image.pack()
def material(name,color,rough,metal=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal;return m
atlas=material('E05U painted part atlas',(1,1,1),.62,.2);tex=atlas.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image;tex.interpolation='Linear';atlas.node_tree.links.new(tex.outputs['Color'],atlas.node_tree.nodes.get('Principled BSDF').inputs['Base Color']);uvnode=atlas.node_tree.nodes.new('ShaderNodeUVMap');uvnode.uv_map='E05U_parts';atlas.node_tree.links.new(uvnode.outputs['UV'],tex.inputs['Vector'])
brass=material('E05U continuous brass edging',(.48,.28,.095),.48,.6);blue=material('E05U navy steel edging',(.035,.05,.075),.58,.4);mats=[atlas,brass,blue];new=[];maps={}
def patch(name,source,bone,slot,accept,offset):
 src=bpy.data.objects[source];faces=[p for p in src.data.polygons if accept(p,src)];used=sorted({v for p in faces for v in p.vertices});remap={v:i for i,v in enumerate(used)};verts=[tuple(src.data.vertices[i].co+src.data.vertices[i].normal*offset)for i in used];mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],[tuple(remap[i]for i in p.vertices)for p in faces]);mesh.update();o=bpy.data.objects.new('GEAR_'+name,mesh);col.objects.link(o);o.parent=rig;o.matrix_parent_inverse=src.matrix_parent_inverse.copy()
 for g in src.vertex_groups:o.vertex_groups.new(name=g.name)
 for i,old in enumerate(used):
  for g in src.data.vertices[old].groups:o.vertex_groups[g.group].add([i],g.weight,'REPLACE')
 m=o.modifiers.new('Wizard deform','ARMATURE');m.object=rig;s=o.modifiers.new('Fitted plate thickness','SOLIDIFY');s.thickness=.003;s.offset=0;b=o.modifiers.new('Plate edge bevel','BEVEL');b.width=.0015;b.segments=2;o['gear_slot']=slot;o['bone']=bone;o['fit_family']='wizard-rig35-v1';maps[o.name]={'source':source,'vertices':used,'offset':offset};new.append(o);return o
for side in ['L','R']:
 def forearm(p,src):
  group=src.vertex_groups['Forearm.'+side].index
  return 1.12<p.center.z<1.29 and p.center.y<.035 and all(any(g.group==group and g.weight>.999 for g in src.data.vertices[i].groups)for i in p.vertices)
 patch('bracer-'+side,'Robe sleeve '+side,'Forearm.'+side,'forearm',forearm,.012)
 patch('greave-'+side,'Boot shaft '+side,'Shin.'+side,'shin',lambda p,src:.175<p.center.z<.44 and p.center.y<.025,.009)
gear=[o for o in col.objects if o.type=='MESH' and o.name.startswith('GEAR_')];uvrecords=[]
def tile_uv(tile,u,v):
 row,col=divmod(tile,3);u=max(0,min(1,u));v=max(0,min(1,v));return ((col+.06+.88*u)/3,1-(row+.06+.88*(1-v))/2)
for o in gear:
 me=o.data;oldids=[p.material_index for p in me.polygons] if o not in new else [0]*len(me.polygons);me.materials.clear()
 for m in mats:me.materials.append(m)
 uv=me.uv_layers.new(name='E05U_parts');lo=[min(v.co[i]for v in me.vertices)for i in range(3)];hi=[max(v.co[i]for v in me.vertices)for i in range(3)];tiles=set()
 for p,mid in zip(me.polygons,oldids):
  p.material_index=mid;p.use_smooth=not o.name.startswith('GEAR_pauldron')
  for li in p.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co
   if o.name=='GEAR_cuirass':
    front=p.center.y<=0;tile=0 if front else 1;angle=math.atan2(v.x,-v.y)if front else math.atan2(-v.x,v.y);u=.5+angle/math.pi;t=(v.z-lo[2])/(hi[2]-lo[2])
   elif o.name.startswith('GEAR_pauldron'):
    tile=2;u=(v.x-lo[0])/(hi[0]-lo[0]);u=1-u if o.name.endswith('R')else u;t=(v.y-lo[1])/(hi[1]-lo[1])
   elif o.name=='GEAR_helmet':
    tile=3;u=.5+math.atan2(v.x,-(v.y-.008))/(2*math.pi);t=(v.z-lo[2])/(hi[2]-lo[2])
   elif o.name.startswith('GEAR_bracer'):
    tile=4;axis=(rig.data.bones[o['bone']].tail_local-rig.data.bones[o['bone']].head_local).normalized();side=Vector((axis.z,0,-axis.x)).normalized();vals=[q.co.dot(side)for q in me.vertices];along=[q.co.dot(axis)for q in me.vertices];u=(v.dot(side)-min(vals))/(max(vals)-min(vals));t=(v.dot(axis)-min(along))/(max(along)-min(along))
   else:tile=5;u=(v.x-lo[0])/(hi[0]-lo[0]);t=(v.z-lo[2])/(hi[2]-lo[2])
   uv.data[li].uv=tile_uv(tile,u,t);tiles.add(tile)
 for mod in o.modifiers:
  if mod.type=='BEVEL':mod.segments=3
 for attr in ['visible_shadow','visible_diffuse','visible_glossy','visible_transmission','visible_volume_scatter']:setattr(o,attr,True)
 uvrecords.append({'object':o.name,'tiles':sorted(tiles),'vertices':len(me.vertices),'slot':o.get('gear_slot'),'bone':o.get('bone')})
assert before==base_hash();assert actions==[a.name for a in bpy.data.actions];assert all(len(o.data.polygons)>8 for o in new)
# Fitted core sample follows identical source weights. Disable only shell/bevel for indexed comparison.
checks=[]
for o in new:
 for m in o.modifiers:
  if m.type!='ARMATURE':m.show_viewport=False
for action,frame in [('idle',0),('walk',12),('cast',36)]:
 rig.animation_data.action=bpy.data.actions['E05M_'+action];bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
 for o in new:
  src=bpy.data.objects[maps[o.name]['source']];a=o.evaluated_get(dg);b=src.evaluated_get(dg);ma=a.to_mesh();mb=b.to_mesh();dist=[]
  for i,old in enumerate(maps[o.name]['vertices']):
   q=a.matrix_world@ma.vertices[i].co;r=b.matrix_world@mb.vertices[old].co;n=(b.matrix_world.to_3x3().inverted().transposed()@mb.vertices[old].normal).normalized();dist.append((q-r).dot(n))
  a.to_mesh_clear();b.to_mesh_clear();checks.append({'pose':action,'frame':frame,'object':o.name,'samples':len(dist),'minimum_signed_core_clearance_m':min(dist),'pass':min(dist)>.006})
for o in new:
 for m in o.modifiers:m.show_viewport=True
rig.animation_data.action=bpy.data.actions['E05M_idle'];bpy.context.scene.frame_set(0)
report={'base_sha256_before':before,'base_sha256_after':base_hash(),'base_unchanged':before==base_hash(),'actions_unchanged':actions==[a.name for a in bpy.data.actions],'parts':uvrecords,'fit_checks':checks,'scope':'New fitted bracer/greave core clearance; shell thickness3mm/bevel1.5mm. Existing head/torso/shoulder fit and complete art require visual check. Base geometry/weights/actions unchanged.'};(HERE/'evidence/author-v1.json').write_text(json.dumps(report,indent=2));assert all(c['pass']for c in checks),checks
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/part-painted-gear-v1.blend'));print('E05U_AUTHOR',report)
