import bpy,json,hashlib,math,struct,sys,time
from pathlib import Path
from array import array
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;rig=bpy.data.objects['WizardRig'];scene=bpy.context.scene;meshes=[o for o in bpy.data.collections['Wizard_Character'].objects if o.type=='MESH'];bones=list(rig.data.bones);bone_ids={b.name:i for i,b in enumerate(bones)};identity_id=len(bones);rigworld=rig.matrix_world.copy();source_hash=hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest();assets=HERE/'assets';start=time.monotonic();materials=[];mat_ids={};images={}
def floats(path,values,code='f'):
 a=array(code,values)
 if sys.byteorder!='little':a.byteswap()
 path.write_bytes(a.tobytes());return {'path':str(path.relative_to(HERE)),'dtype':'float32'if code=='f'else'uint32','byte_order':'little','elements':len(a),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def mat(m):
 if m.name in mat_ids:return mat_ids[m.name]
 bs=next((n for n in m.node_tree.nodes if n.bl_idname=='ShaderNodeBsdfPrincipled'),None);assert bs,m.name;links=list(bs.inputs['Base Color'].links);texture=None;uv=None
 if links:
  assert len(links)==1 and links[0].from_node.bl_idname=='ShaderNodeTexImage',m.name
  node=links[0].from_node;im=node.image;assert im
  if im.name not in images:
   if im.packed_file:data=bytes(im.packed_file.data)
   else:data=Path(bpy.path.abspath(im.filepath)).read_bytes()
   sha=hashlib.sha256(data).hexdigest();f=assets/(sha[:16]+'.png');f.write_bytes(data);images[im.name]={'path':str(f.relative_to(HERE)),'sha256':sha,'dimensions':list(im.size),'bytes':len(data),'source_name':im.name,'colorspace':im.colorspace_settings.name}
  texture=images[im.name]['path'];vlinks=list(node.inputs['Vector'].links)
  if vlinks:assert len(vlinks)==1 and vlinks[0].from_node.bl_idname=='ShaderNodeUVMap',m.name;uv=vlinks[0].from_node.uv_map
 color=list(bs.inputs['Base Color'].default_value)[:3];color=[12.92*x if x<=.0031308 else 1.055*x**(1/2.4)-.055 for x in color]
 i=len(materials);mat_ids[m.name]=i;materials.append({'id':i,'name':m.name,'texture_path':texture,'uv_layer':uv,'color_srgb':[1,1,1]if texture else color,'roughness':bs.inputs['Roughness'].default_value,'metallic':bs.inputs['Metallic'].default_value,'emissive_mask_path':None,'alpha':'opaque geometry; texture alpha not silhouette'});return i
# Export evaluated non-armature modifiers in rest coordinates, retaining weights.
armatures=[m for o in meshes for m in o.modifiers if m.type=='ARMATURE'];oldflags=[m.show_viewport for m in armatures]
for m in armatures:m.show_viewport=False
bpy.context.view_layer.update();vertices=[];indices=[];parts=[];maps={};max_dropped=0;unweighted=0
for o in meshes:
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();local=rigworld.inverted()@ev.matrix_world;normalmat=local.to_3x3().inverted().transposed();groups={g.index:g.name for g in o.vertex_groups};lookup={};mapping=[];tri_by_mat={};vertex_start=len(vertices)//16
 for tri in me.loop_triangles:
  mid=mat(o.data.materials[tri.material_index]);mrec=materials[mid];uvlayer=me.uv_layers.get(mrec['uv_layer'])if mrec['uv_layer']else me.uv_layers.active
  assert not mrec['texture_path']or uvlayer,(o.name,mrec)
  for li,vid in zip(tri.loops,tri.vertices):
   v=me.vertices[vid];normal=(normalmat@me.corner_normals[li].vector).normalized();uv=list(uvlayer.data[li].uv)if uvlayer else[0,0];key=(vid,tuple(round(x,7)for x in normal),tuple(round(x,7)for x in uv));keyid=lookup.get(key)
   if keyid is None:
    ws=sorted([(bone_ids[groups[g.group]],g.weight)for g in v.groups if groups.get(g.group)in bone_ids and g.weight>0],key=lambda x:-x[1]);dropped=sum(w for _,w in ws[4:]);max_dropped=max(max_dropped,dropped);ws=ws[:4]
    if not ws:ws=[(identity_id,1)];unweighted+=1
    total=sum(w for _,w in ws);ws=[(i,w/total)for i,w in ws];joints=[i for i,w in ws]+[0]*(4-len(ws));weights=[w for i,w in ws]+[0]*(4-len(ws));pos=local@v.co;keyid=len(vertices)//16;lookup[key]=keyid;vertices+=list(pos)+list(normal)+[uv[0],1-uv[1]]+joints+weights;mapping.append((keyid,vid,li,list(pos),ws))
   tri_by_mat.setdefault(mid,[]).append(keyid)
 for mid,ids in tri_by_mat.items():
  category='gear'if o.name.startswith('GEAR_')else'hair'if o.get('asset_category')=='hair' or 'hair'in o.name.lower()else'body';parts.append({'object':o.name,'category':category,'slot':o.get('gear_slot'),'material':mid,'index_start':len(indices),'index_count':len(ids)});indices+=ids
 maps[o.name]={'map':mapping,'evaluated_vertices':len(me.vertices),'evaluated_loops':len(me.loops)};ev.to_mesh_clear()
for m,v in zip(armatures,oldflags):m.show_viewport=v
bpy.context.view_layer.update();assert max_dropped<=1e-6,max_dropped
vf=floats(assets/'vertices.bin',vertices);ix=floats(assets/'indices.bin',indices,'I');poses=[];checks=[]
for clip,frame in [('idle',0),('walk',12),('cast',36)]:
 rig.animation_data.action=bpy.data.actions['E05M_'+clip];scene.frame_set(frame);bpy.context.view_layer.update();palette=[rig.matrix_world@rig.pose.bones[b.name].matrix@b.matrix_local.inverted()for b in bones]+[rig.matrix_world.copy()];palette_values=[m[row][col]for m in palette for col in range(4)for row in range(4)];oracle=[0.]*(len(vertices)//16*6);maxerror=0;sampled=0;topology=True
 for o in meshes:
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();topology=topology and len(me.vertices)==maps[o.name]['evaluated_vertices']and len(me.loops)==maps[o.name]['evaluated_loops'];assert topology,o.name;normalmat=ev.matrix_world.to_3x3().inverted().transposed()
  for k,(keyid,vid,li,pos,ws)in enumerate(maps[o.name]['map']):
   actual=ev.matrix_world@me.vertices[vid].co;normal=(normalmat@me.corner_normals[li].vector).normalized();oracle[keyid*6:keyid*6+6]=list(actual)+list(normal)
   if k%max(1,len(maps[o.name]['map'])//64)==0:
    predicted=sum(((palette[i]@Vector(pos))*w for i,w in ws),Vector((0,0,0)));error=(predicted-actual).length;maxerror=max(maxerror,error);sampled+=1
  ev.to_mesh_clear()
 pf=floats(assets/f'{clip}-{frame:03}-palette.bin',palette_values);of=floats(assets/f'{clip}-{frame:03}-oracle.bin',oracle);poses.append({'id':f'{clip}-{frame:03}','clip':clip,'frame':frame,'time_s':frame/60,'palette':pf,'oracle':of});checks.append({'pose':poses[-1]['id'],'sampled':sampled,'max_world_error_m':maxerror,'topology_preserved':topology,'pass':maxerror<=.001 and topology})
manifest={'schema_version':1,'asset_id':'E05W-base-material-hair','coordinate_system':'right handed Blender world metres; C adapter maps worldY to -v','vertex_buffer':vf,'vertex_stride_float32':16,'attributes':{'position':[0,3],'normal':[3,3],'uv':[6,2],'joint_indices':[8,4],'joint_weights':[12,4]},'index_buffer':ix,'parts':parts,'materials':materials,'images':list(images.values()),'bones':[b.name for b in bones]+['__static_rig_transform__'],'poses':poses,'fps':60,'directions':[0,45,90,135,180,225,270,315],'anchor_world':[0,0,0],'hitbox':{'height_m':2,'radius_m':.26},'atlas':None,'visibility':{'head_visible':{'exclude_category':['hair']},'head_hidden':{'exclude_slot':['head']}},'qualification':'Sparse source/representation test only; no full painted pilot or production animation qualification'}
(HERE/'character.asset.json').write_text(json.dumps(manifest,indent=2)+'\n');(HERE/'evidence/export-validation.json').write_text(json.dumps({'checks':checks,'max_dropped_weight':max_dropped,'unweighted_vertices':unweighted,'export_vertices':len(vertices)//16,'triangles':len(indices)//3,'parts':len(parts),'source_sha256':source_hash,'source_file_unchanged':source_hash==hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'seconds':time.monotonic()-start},indent=2)+'\n');print('E05U_EXPORT',len(vertices)//16,len(indices)//3,checks);assert all(x['pass']for x in checks)
