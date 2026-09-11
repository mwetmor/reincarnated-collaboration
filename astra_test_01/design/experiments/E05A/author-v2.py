import bpy,json,hashlib,struct,math
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;rig=bpy.data.objects['WizardRig'];col=bpy.data.collections['Wizard_Character'];base=[o for o in col.objects if o.type=='MESH' and not o.name.startswith('GEAR_')]
def geometry():
 h=hashlib.sha256()
 for o in sorted(base,key=lambda o:o.name):
  h.update(o.name.encode())
  for v in o.data.vertices:
   h.update(struct.pack('3d',*v.co))
   for g in v.groups:h.update(struct.pack('id',g.group,g.weight))
 return h.hexdigest()
before=geometry();actions=[a.name for a in bpy.data.actions];template=bpy.data.objects['Sculpted head'];oldbounds={o.name:[[min(v.co[i]for v in o.data.vertices),max(v.co[i]for v in o.data.vertices)]for i in range(3)]for o in col.objects if o.name.startswith('GEAR_') and o.type=='MESH'}
for o in list(col.objects):
 if o.name.startswith('GEAR_'):bpy.data.objects.remove(o,do_unlink=True)
image=bpy.data.images.load(str(HERE/'art/material-v1.png'));image.pack();mats=[]
for name,metal,rough in [('ivory enamel',.25,.53),('antique brass',.6,.44),('blue steel',.65,.56)]:
 m=bpy.data.materials.new('E05A '+name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough;tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image;tex.interpolation='Linear';m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);mats.append(m)
gear=[]
def make(name,verts,faces,bone,slot,material_indices=None,thickness=.003):
 mesh=bpy.data.meshes.new('E05A '+name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('GEAR_'+name,mesh);col.objects.link(o);o.parent=rig;o.matrix_parent_inverse=template.matrix_parent_inverse.copy();g=o.vertex_groups.new(name=bone);g.add(list(range(len(verts))),1,'REPLACE');a=o.modifiers.new('Armature','ARMATURE');a.object=rig
 for m in mats:mesh.materials.append(m)
 uv=mesh.uv_layers.new(name='E05A_material_uv');lo=[min(v[i]for v in verts)for i in range(3)];hi=[max(v[i]for v in verts)for i in range(3)]
 for p in mesh.polygons:
  k=material_indices[p.index]if material_indices else 0;p.material_index=k;p.use_smooth=False
  axes=sorted(range(3),key=lambda i:abs(p.normal[i]))[:2]
  for li in p.loop_indices:
   v=mesh.vertices[mesh.loops[li].vertex_index].co;u=(v[axes[0]]-lo[axes[0]])/max(hi[axes[0]]-lo[axes[0]],1e-5);t=(v[axes[1]]-lo[axes[1]])/max(hi[axes[1]]-lo[axes[1]],1e-5);uv.data[li].uv=((k+.05+.9*u)/3,.05+.9*t)
 if thickness:s=o.modifiers.new('Plate thickness','SOLIDIFY');s.thickness=thickness;s.offset=0
 b=o.modifiers.new('Soft bevel','BEVEL');b.width=.0015;b.segments=2
 for attr in ['visible_shadow','visible_diffuse','visible_glossy','visible_transmission','visible_volume_scatter']:setattr(o,attr,False)
 o['gear_slot']=slot;o['bone']=bone;o['fit_family']='wizard-rig35-v1';gear.append(o);return o
# Fitted open face segmented cap; source hair is a separately switchable component.
verts=[];faces=[];ids=[];N=16;J=10
for j in range(J):
 theta=.03+(1.8-.03)*j/(J-1)
 for i in range(N):
  phi=2*math.pi*i/N;verts.append((.098*math.sin(theta)*math.sin(phi),.008-.104*math.sin(theta)*math.cos(phi),1.667+.139*math.cos(theta)))
for j in range(J-1):
 for i in range(N):
  phi=2*math.pi*(i+.5)/N
  if j>=5 and math.cos(phi)>.35:continue
  faces.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i));ids.append(1 if j==J-2 or (i in [0,N-1]and j<5) else 0)
make('helmet',verts,faces,'Head','head',ids)
# Tapered shoulder shell with geometric brass edge strips, replacing round domes.
for side,sgn in [('L',1),('R',-1)]:
 verts=[];faces=[];ids=[]
 # Source cross sections: inner / crown / tapered outer plate.
 for x,z,w in [(.12,1.505,.065),(.20,1.548,.105),(.285,1.515,.102),(.328,1.435,.073)]:
  for y,dz in [(-w,-.006),(-w+.009,0),(w-.009,0),(w,-.006)]:verts.append((sgn*x,y,z+dz))
 for j in range(3):
  for i in range(3):
   face=(j*4+i,(j+1)*4+i,(j+1)*4+i+1,j*4+i+1)
   faces.append(face if sgn==1 else face[::-1]);ids.append(1 if i in [0,2] or j==2 else 0)
 make('pauldron-'+side,verts,faces,'UpperArm.'+side,'shoulder',ids,.006)
# Retain known-fitting cuirass surface, add a material border and centre ridge through face assignment.
old=bpy.data.objects['Tailored upper robe'];verts=[tuple(v.co+v.normal*.011)for v in old.data.vertices];faces=[tuple(p.vertices)for p in old.data.polygons];ids=[]
for p in old.data.polygons:
 c=p.center;ids.append(1 if c.z<1.135 or c.z>1.49 or abs(c.x)<.015 else 0)
cuirass=make('cuirass',verts,faces,'Chest','torso',ids)
# Flat shading conveys plate construction; geometry unchanged elsewhere.
hair=[o.name for o in base if 'hair' in o.name.lower()]
assert before==geometry();assert actions==[a.name for a in bpy.data.actions]
bounds={o.name:[[min(v.co[i]for v in o.data.vertices),max(v.co[i]for v in o.data.vertices)]for i in range(3)]for o in gear}
checks={'base_mesh_and_weights_immutable':before==geometry(),'actions_preserved':actions==[a.name for a in bpy.data.actions],'helmet_width':bounds['GEAR_helmet'][0][1]-bounds['GEAR_helmet'][0][0]<=.21,'helmet_top':bounds['GEAR_helmet'][2][1]<=1.82,'hair_preserved':len(hair)==19}
assert all(checks.values()),checks
rig.animation_data.action=bpy.data.actions['E05M_idle'];bpy.context.scene.frame_set(0)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/fitted-gear-v2.blend'))
(HERE/'evidence/author-v2.json').write_text(json.dumps({'checks':checks,'before_base_sha256':before,'after_base_sha256':geometry(),'old_bounds':oldbounds,'new_bounds':bounds,'hair_objects':hair,'material_source_sha256':hashlib.sha256((HERE/'art/material-v1.png').read_bytes()).hexdigest(),'actions':actions,'ray_visibility':'secondary rays disabled for isolated layer test; no gear-lighting qualification'},indent=2))
print('E05A_AUTHOR_PASS',checks)
