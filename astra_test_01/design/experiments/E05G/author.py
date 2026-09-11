import bpy,json,hashlib,struct,math
from pathlib import Path
from mathutils import Vector
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05G');rig=bpy.data.objects['WizardRig'];collection=bpy.data.collections['Wizard_Character'];base=[o for o in collection.objects if o.type=='MESH'];actions={a.name:a for a in bpy.data.actions}
def hash_base():
 h=hashlib.sha256()
 for o in base:
  h.update(o.name.encode())
  for v in o.data.vertices:
   h.update(struct.pack('3d',*v.co))
   for g in v.groups:h.update(struct.pack('id',g.group,g.weight))
 return h.hexdigest()
before=hash_base()
def material(name,color,metal):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.6;return m
ivory=material('E05G ivory ceramic probe',(.58,.54,.43),.15);brass=material('E05G brass probe',(.32,.21,.07),.6);gear=[]
def bind(o,bone,slot,mat):
 o.vertex_groups.clear();g=o.vertex_groups.new(name=bone);g.add(list(range(len(o.data.vertices))),1,'REPLACE');o.data.materials.clear();o.data.materials.append(mat)
 for p in o.data.polygons:p.material_index=0
 for attr in ['visible_shadow','visible_diffuse','visible_glossy','visible_transmission','visible_volume_scatter']:
  assert hasattr(o,attr),attr;setattr(o,attr,False)
 o['gear_slot']=slot;o['fit_family']='wizard-rig35-v1';o['bone']=bone;gear.append(o);return o
def clone(name,new,bone,slot,mat,scale=1,shift=(0,0,0),inflate=0):
 old=bpy.data.objects[name];o=old.copy();o.data=old.data.copy();o.name='GEAR_'+new;collection.objects.link(o);centre=sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices)
 for v in o.data.vertices:v.co=centre+(v.co-centre)*scale+Vector(shift)+v.normal*inflate
 return bind(o,bone,slot,mat)
clone('Tailored upper robe','cuirass','Chest','torso',ivory,inflate=.014)
for side,sgn in [('L',1),('R',-1)]:
 clone('Tailored shoulder '+side,'pauldron-upper-'+side,'UpperArm.'+side,'shoulder',ivory,1.22,(sgn*.015,0,.012))
 clone('Tailored shoulder '+side,'pauldron-lower-'+side,'UpperArm.'+side,'shoulder',brass,1.15,(sgn*.04,0,-.035))
verts=[];faces=[];rings=14;sides=32
for j in range(rings):
 theta=.01+(math.pi*.65-.01)*j/(rings-1)
 for i in range(sides):
  phi=2*math.pi*i/sides;verts.append((.14*math.sin(theta)*math.sin(phi),.02-.165*math.sin(theta)*math.cos(phi),1.73+.16*math.cos(theta)))
for j in range(rings-1):
 for i in range(sides):
  phi=2*math.pi*(i+.5)/sides;theta=.01+(math.pi*.65-.01)*(j+.5)/(rings-1)
  if theta>1.48 and math.cos(phi)>.25:continue
  faces.append((j*sides+i,j*sides+(i+1)%sides,(j+1)*sides+(i+1)%sides,(j+1)*sides+i))
mesh=bpy.data.meshes.new('E05G open helmet geometry');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('GEAR_helmet',mesh);collection.objects.link(o);o.parent=rig;o.matrix_parent_inverse=bpy.data.objects['Sculpted head'].matrix_parent_inverse.copy();mod=o.modifiers.new('Armature','ARMATURE');mod.object=rig
for p in mesh.polygons:p.use_smooth=True
solid=o.modifiers.new('Shell thickness','SOLIDIFY');solid.thickness=.005
bind(o,'Head','head',ivory)
assert before==hash_base();assert all(bpy.data.actions[name]==a for name,a in actions.items())
motion=json.loads((HERE.parent/'E05M/evidence/source-motion.json').read_text());samples={o.name:[]for o in gear}
for kind,clip in motion['clips'].items():
 rig.animation_data.action=bpy.data.actions[clip['action']]
 for i in range(clip['frame_count']):
  bpy.context.scene.frame_set(i);bpy.context.view_layer.update()
  for o in gear:
   obj=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=obj.to_mesh();inv=(rig.matrix_world@rig.pose.bones[o['bone']].matrix).inverted();ps=[inv@(obj.matrix_world@v.co)for v in m.vertices];obj.to_mesh_clear();c=sum(ps,Vector())/len(ps);rad=max((p-c).length for p in ps);samples[o.name].append((c,rad))
result={'base_hash_before':before,'base_hash_after':hash_base(),'unchanged_actions':list(actions),'gear':[],'checks':{}}
for o in gear:
 ss=samples[o.name];drift=max((c-ss[0][0]).length for c,r in ss);variation=max(r for c,r in ss)/min(r for c,r in ss)-1;result['gear'].append({'name':o.name,'slot':o['gear_slot'],'bone':o['bone'],'samples':len(ss),'attachment_drift_m':drift,'radius_variation':variation});result['checks'][o.name+'_attachment']=drift<=.001;result['checks'][o.name+'_rigid']=variation<=.01
result['checks']['base_immutable']=before==hash_base();result['checks']['actions_reused']=all(bpy.data.actions[name]==a for name,a in actions.items());(HERE/'evidence/source-gear.json').write_text(json.dumps(result,indent=2));print('GEAR_PREFLIGHT',result['checks']);assert all(result['checks'].values())
rig.animation_data.action=bpy.data.actions['E05M_idle'];bpy.context.scene.frame_set(0)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/gear-v1.blend'))
