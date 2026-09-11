import bpy,json,hashlib,struct,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;rig=bpy.data.objects['WizardRig'];col=bpy.data.collections['Wizard_Character'];hair=bpy.data.objects['Swept hair mass'];head=bpy.data.objects['Sculpted head'];others=[o for o in col.objects if o.type=='MESH' and o!=hair]
def geometry(objects):
 h=hashlib.sha256()
 for o in sorted(objects,key=lambda o:o.name):
  h.update(o.name.encode())
  for v in o.data.vertices:
   h.update(struct.pack('3d',*v.co))
   for g in v.groups:h.update(struct.pack('id',g.group,g.weight))
 return h.hexdigest()
before=geometry(others);hair_before=geometry([hair]);actions=[a.name for a in bpy.data.actions];bones=[(b.name,list(b.head_local),list(b.tail_local))for b in rig.data.bones]
def bottom(phi):
 c=math.cos(phi);rear=(1-c)/2;return 1.717-.065*rear+.004*rear*math.sin(5*phi)+.002*rear*math.sin(9*phi)
n=64;rows=20;verts=[];faces=[]
for j in range(rows):
 t=j/rows
 for i in range(n):
  phi=2*math.pi*i/n;z=bottom(phi)+(1.790-bottom(phi))*math.sin(t*math.pi/2);r=math.cos(t*math.pi/2);wave=.0015*math.sin(11*phi)*math.sin(t*math.pi);verts.append(((.084*r+wave)*math.sin(phi),.012-(.082*r+wave)*math.cos(phi),z))
for j in range(rows-1):
 for i in range(n):a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
pole=len(verts);verts.append((0,.012,1.790))
for i in range(n):faces.append(((rows-1)*n+i,(rows-1)*n+(i+1)%n,pole))
mesh=bpy.data.meshes.new('E05W smooth hairline');mesh.from_pydata(verts,[],faces);mesh.update();hair.data=mesh
for g in list(hair.vertex_groups):hair.vertex_groups.remove(g)
hair.vertex_groups.new(name='Head').add(list(range(len(verts))),1,'REPLACE')
head_bvh=BVHTree.FromPolygons([v.co.copy()for v in head.data.vertices],[list(p.vertices)for p in head.data.polygons]);tohead=head.matrix_world.inverted()@hair.matrix_world;tohair=tohead.inverted();clamped=0;vertex_clearance=[]
for v in hair.data.vertices:
 p=tohead@v.co;origin=Vector((0,.012,p.z));d=p-origin;r=d.length
 if r<1e-6:continue
 direction=d.normalized();hit,normal,index,distance=head_bvh.ray_cast(origin,direction,1)
 if hit is None:continue
 if r<distance+.0041:v.co=tohair@(origin+direction*(distance+.0041));clamped+=1;r=distance+.0041
 vertex_clearance.append(r-distance)
hair.data.update();hair_bvh=BVHTree.FromPolygons([tohead@v.co for v in hair.data.vertices],[list(p.vertices)for p in hair.data.polygons]);surface=[]
for i in range(120):
 phi=2*math.pi*i/120;direction=Vector((math.sin(phi),-math.cos(phi),0));z0=bottom(phi)+.008
 for j in range(8):
  z=z0+(1.765-z0)*j/7;origin=Vector((0,.012,z));a=head_bvh.ray_cast(origin,direction,1);b=hair_bvh.ray_cast(origin,direction,1)
  if a[0]is None:continue
  surface.append({'phi_deg':i*3,'z':z,'clearance_m':b[3]-a[3]if b[0]is not None else None,'pass':b[0]is not None and b[3]-a[3]>=.002})
image=bpy.data.images.load(str(HERE/'art/materials-v1.png'));image.pack();mat=bpy.data.materials.new('E05W painted base materials');mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.78;tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image;tex.interpolation='Linear';uvn=mat.node_tree.nodes.new('ShaderNodeUVMap');uvn.uv_map='E05WMaterials';mat.node_tree.links.new(uvn.outputs['UV'],tex.inputs['Vector']);mat.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);changed=[];hair_names=[]
for o in col.objects:
 if o.type!='MESH' or o.name.startswith('GEAR_'):continue
 name=o.name;tile=None
 if 'hair' in name.lower() or name.startswith(('Temple loose lock','Nape loose lock')):tile=3;o['asset_category']='hair';hair_names.append(name)
 elif name.startswith(('Robe sleeve','Tailored shoulder','High collar','Central pointed tabard')):tile=0
 elif name.startswith(('Tailored upper robe','Split robe')):tile=1
 elif name.startswith(('Boot foot ','Boot shaft ','Leather wrist','Belt','Tome cover','Tome spine')) and 'buckle' not in name.lower():tile=2
 if tile is None:continue
 me=o.data;old=[m.name for m in me.materials];me.materials.clear();me.materials.append(mat);uv=me.uv_layers.new(name='E05WMaterials');lo=[min(v.co[i]for v in me.vertices)for i in range(3)];hi=[max(v.co[i]for v in me.vertices)for i in range(3)]
 for p in me.polygons:
  p.material_index=0;p.use_smooth=True
  for li in p.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co
   if tile==3:u=.5+math.atan2(v.x,-(v.y-.012))/(2*math.pi);t=(v.z-1.57)/.22
   else:
    axes=[0,2] if abs(p.normal.y)>=abs(p.normal.x) else [1,2]
    if abs(p.normal.z)>.8:axes=[0,1]
    u=(v[axes[0]]-lo[axes[0]])/max(hi[axes[0]]-lo[axes[0]],1e-6);t=(v[axes[1]]-lo[axes[1]])/max(hi[axes[1]]-lo[axes[1]],1e-6)
   u=max(0,min(1,u));t=max(0,min(1,t));row,column=divmod(tile,2);uv.data[li].uv=((column+.06+.88*u)/2,1-(row+.06+.88*(1-t))/2)
 changed.append({'object':name,'tile':tile,'old_materials':old})
for p in hair.data.polygons:p.use_smooth=True
head_bindings=[]
for name in hair_names:
 o=bpy.data.objects[name];groups={g.index:g.name for g in o.vertex_groups};ok=all(len(v.groups)==1 and groups[v.groups[0].group]=='Head' and abs(v.groups[0].weight-1)<1e-6 for v in o.data.vertices);head_bindings.append({'object':name,'head_binding_exact':ok})
checks={'non_hair_geometry_weights_unchanged':geometry(others)==before,'actions_unchanged':actions==[a.name for a in bpy.data.actions],'rig_bones_unchanged':bones==[(b.name,list(b.head_local),list(b.tail_local))for b in rig.data.bones],'vertex_clearance4mm':min(vertex_clearance)>=.004-1e-8,'surface_clearance2mm':all(x['pass']for x in surface),'all23hair_head_bindings':len(hair_names)==23 and all(x['head_binding_exact']for x in head_bindings)}
r={'checks':checks,'non_hair_before_sha256':before,'non_hair_after_sha256':geometry(others),'hair_before_sha256':hair_before,'hair_after_sha256':geometry([hair]),'hair_vertices':len(hair.data.vertices),'clamped_to_head_vertices':clamped,'minimum_vertex_radial_clearance_m':min(vertex_clearance),'surface_samples':surface,'hair_visibility_group':head_bindings,'material_changes':changed,'scope':'Hair mass geometry only; all other positions/weights and rig/actions unchanged. Four previously uncategorized temple/nape locks now explicit hair visibility.'};(HERE/'evidence/author-v1.json').write_text(json.dumps(r,indent=2));assert all(checks.values()),checks
rig.animation_data.action=bpy.data.actions['E05M_idle'];bpy.context.scene.frame_set(0);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/material-hair-v1.blend'));print('E05W_AUTHOR',checks,len(surface))
