import bpy,json,hashlib,math,struct,sys,time
from pathlib import Path
from array import array
from mathutils import Vector,Matrix,Quaternion
HERE=Path(__file__).resolve().parent;rig=bpy.data.objects['WizardRig'];scene=bpy.context.scene;meshes=[o for o in bpy.data.collections['Wizard_Character'].objects if o.type=='MESH'];bones=list(rig.data.bones);bone_ids={b.name:i for i,b in enumerate(bones)};identity_id=len(bones);rigworld=rig.matrix_world.copy();source_hash=hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest();assets=HERE/'assets';assets.mkdir(exist_ok=True);start=time.monotonic();materials=[];mat_ids={};images={}
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
  category='gear'if o.name.startswith('GEAR_')else'hair'if o.get('asset_category')=='hair' or 'hair'in o.name.lower()else'body';parts.append({'object':o.name,'category':category,'slot':o.get('gear_slot'),'material':mid,'default_visible':bool(o.get('default_visible',True)),'index_start':len(indices),'index_count':len(ids)});indices+=ids
 maps[o.name]={'map':mapping,'evaluated_vertices':len(me.vertices),'evaluated_loops':len(me.loops)};ev.to_mesh_clear()
for m,v in zip(armatures,oldflags):m.show_viewport=v
bpy.context.view_layer.update();assert max_dropped<=1e-6,max_dropped
# Reconstructed rest buffers must match the accepted source export exactly.
reference=json.loads((HERE.parent/'E05W/v2/character.asset.json').read_text())
rest_v=floats(assets/'check-vertices.bin',vertices);rest_i=floats(assets/'check-indices.bin',indices,'I')
cached=array('f');cached.frombytes((HERE.parent/'E05W/v2'/reference['vertex_buffer']['path']).read_bytes())
if sys.byteorder!='little':cached.byteswap()
assert len(cached)==len(vertices)
assert all(abs(a-b)<=2e-7 if i%16 in [6,7] else struct.pack('<f',a)==struct.pack('<f',b) for i,(a,b)in enumerate(zip(vertices,cached)))
# UV save/reload rounding only; rendering reuses exact cached accepted buffers.
assert rest_i['sha256']==reference['index_buffer']['sha256']
(assets/'check-vertices.bin').unlink();(assets/'check-indices.bin').unlink()
# Reuse native material/mesh bytes by neutral relative references.
for im in list(assets.glob('*.png')):im.unlink()
manifest=json.loads(json.dumps(reference))
for key in ['vertex_buffer','index_buffer']:manifest[key]['path']='../E05W/v2/'+manifest[key]['path']
for m in manifest['materials']:
 if m['texture_path']:m['texture_path']='../E05W/v2/'+m['texture_path']
for im in manifest['images']:im['path']='../E05W/v2/'+im['path']
import numpy as np
original=json.loads((HERE.parent/'E05N/evidence/source-motion.json').read_text());assert source_hash==json.loads((HERE/'evidence/author-v1.json').read_text())['new_source_sha256'],'Different revised source';accepted=json.loads((HERE.parent/'E05N/character.asset.json').read_text());data=np.frombuffer((HERE.parent/'E05N'/accepted['palette_buffer']['path']).read_bytes(),dtype='<f4').reshape(-1,len(bones)+1,4,4).transpose(0,1,3,2);rest=np.asarray(cached,dtype=np.float32).reshape(-1,16);pos=np.c_[rest[:,:3],np.ones(len(rest),dtype=np.float32)];joints=rest[:,8:12].astype(np.int32);weights=rest[:,12:16];integer={};local_basis={};integer_checks=[]
for clip,count in [('idle',96),('walk',48),('cast',72)]:
 rig.animation_data.action=bpy.data.actions['E05M_'+clip];rows=[];basis_rows=[]
 for frame in range(count+1):
  scene.frame_set(frame);bpy.context.view_layer.update();m=[rig.matrix_world@rig.pose.bones[b.name].matrix@b.matrix_local.inverted()for b in bones]+[rig.matrix_world.copy()];rows.append(np.asarray([list(x)for x in m],dtype=np.float32));basis_rows.append([(rig.pose.bones[b.name].location.copy(),rig.pose.bones[b.name].rotation_quaternion.copy(),rig.pose.bones[b.name].scale.copy())for b in bones])
 integer[clip]=rows;local_basis[clip]=basis_rows;integer_checks.append({'clip':clip,'active_palettes_exact':bool(np.array_equal(np.array(rows[:-1]),data[accepted['clips'][clip]['frame_start']:accepted['clips'][clip]['frame_start']+count]))})
assert all(x['active_palettes_exact']for x in integer_checks)
conventions=json.loads((HERE/'evidence/author-v1.json').read_text())['bone_conventions'];assert all(x['inherit_scale']=='FULL'and x['use_inherit_rotation']and x['use_local_location']and x['rotation_mode']=='QUATERNION'and not x['constraints']for x in conventions),'Unsupported bone conventions'
flat=[];channel_clips={}
for clip in ['idle','walk','cast']:
 channel_clips[clip]={'frame_start':len(flat)//(len(bones)*10),'frame_count':accepted['clips'][clip]['frame_count'],'stored_frames':len(local_basis[clip]),'fps':60,'duration_s':accepted['clips'][clip]['duration_s'],'loop':accepted['clips'][clip]['loop'],'integer_palette_start':accepted['clips'][clip]['frame_start'],'endpoint_palette_index':0 if clip=='cast'else accepted['clips'][clip]['frame_start']}
 for frame in local_basis[clip]:
  for loc,quat,scale in frame:flat.extend([*loc,*quat,*scale])
channel_buffer=floats(assets/'local-channels.bin',flat)
column=lambda m:[m[r][c]for c in range(4)for r in range(4)]
contract={'schema_version':1,'asset_id':'e05f-explicit-local-interpolation','source_sha256':source_hash,'base_asset':'../E05N/character.asset.json','channels':channel_buffer,'channel_stride_float32':10,'channel_fields':['location_xyz','quaternion_wxyz','scale_xyz'],'interpolation':'linear raw channels then normalized quaternion components; exact integer palette fallback','clips':channel_clips,'rig_world_matrix':column(rigworld),'bones':[{'name':b.name,'parent':bone_ids[b.parent.name]if b.parent else None,'rest_relative_matrix':column(b.parent.matrix_local.inverted()@b.matrix_local if b.parent else b.matrix_local),'inverse_rest_matrix':column(b.matrix_local.inverted()),'convention':conventions[i]}for i,b in enumerate(bones)],'static_palette_index':len(bones),'normal_policy':'Unqualified fractional presentation pending source-oracle raster tests; original integer sparse corrections retained.'}
contract.update({'sampler': 'linear_channels_nlerp_v1', 'base_asset_sha256': '6c672743dc19ae986198972d9b195118dab4bb8811183e638f01835f8e0cfc22', 'base_vertex_sha256': '3337fa3fb386d14b180d093977eb95fac0f995a7d7a8a8d9418418a3bb3e9b94', 'base_palette_sha256': '1b15b2b5adc8056ca6e6647b4121086589a4ba27d42400b57e10bbeaec95aa3a'});(HERE/'motion.asset.json').write_text(json.dumps(contract,indent=2)+'\n');fractional_palettes=[]

# Declared paired gear cores, same author predicates as E05N.
pairs={'GEAR_cuirass':('Tailored upper robe',list(range(len(bpy.data.objects['Tailored upper robe'].data.vertices))))}
for side in ['L','R']:
 src=bpy.data.objects['Robe sleeve '+side];group=src.vertex_groups['Forearm.'+side].index;faces=[p for p in src.data.polygons if 1.12<p.center.z<1.29 and p.center.y<.035 and all(any(g.group==group and g.weight>.999 for g in src.data.vertices[i].groups)for i in p.vertices)];pairs['GEAR_bracer-'+side]=(src.name,sorted({i for p in faces for i in p.vertices}));src=bpy.data.objects['Boot shaft '+side];faces=[p for p in src.data.polygons if .175<p.center.z<.44 and p.center.y<.025];pairs['GEAR_greave-'+side]=(src.name,sorted({i for p in faces for i in p.vertices}))
def core(o,v,palette):
 ws=[(bone_ids[o.vertex_groups[g.group].name],g.weight)for g in v.groups if o.vertex_groups[g.group].name in bone_ids];total=sum(w for _,w in ws);local=rigworld.inverted()@o.matrix_world;q=sum(((palette[i]@(local@v.co))*(w/total)for i,w in ws),Vector())if ws else o.matrix_world@v.co;n=sum(((palette[i].to_3x3()@local.to_3x3()@v.normal)*(w/total)for i,w in ws),Vector()).normalized()if ws else(o.matrix_world.to_3x3()@v.normal).normalized();return q,n
mapping={};contacts={};source_contacts={};book=[];records=[];oracles=[]
for o in meshes:
 items=maps[o.name]['map'];keyids=np.array([x[0]for x in items]);vids=np.array([x[1]for x in items]);loops=np.array([x[2]for x in items]);_,unique=np.unique(vids,return_index=True);mapping[o.name]=(keyids,vids,loops,unique)
for row in original['samples']:
 for side,foot in row['feet'].items():
  if foot['stance']:
   key=(row['clip'],side,foot['cycle']if row['clip']=='walk'else 0);contacts.setdefault(key,[]).append(np.array(foot['world']));source_contacts.setdefault(key,[]).append(np.array(foot['world']))
probe={('walk',.5),('walk',12.5),('walk',23.5),('walk',47.5),('idle',24.5),('cast',36.5)}
for clip,count in [('idle',96),('walk',48),('cast',72)]:
 rig.animation_data.action=bpy.data.actions['E05M_'+clip]
 for frame in range(count):
  for alpha in ([.25,.5,.75]if clip=='walk'else[.5]):
   at=frame+alpha;scene.frame_set(frame,subframe=alpha);bpy.context.view_layer.update();pose_matrices={};pm=[]
   for i,b in enumerate(bones):
    l0,q0,s0=local_basis[clip][frame][i];l1,q1,s1=local_basis[clip][frame+1][i];q=Quaternion([q0[k]*(1-alpha)+q1[k]*alpha for k in range(4)]);q.normalize();basis=Matrix.LocRotScale(l0.lerp(l1,alpha),q,s0.lerp(s1,alpha))
    if b.parent:result=b.convert_local_to_pose(basis,b.matrix_local,parent_matrix=pose_matrices[b.parent.name],parent_matrix_local=b.parent.matrix_local)
    else:result=b.convert_local_to_pose(basis,b.matrix_local)
    pose_matrices[b.name]=result;pm.append(rigworld@result@b.matrix_local.inverted())
   pm.append(rigworld.copy());palette=np.asarray([list(x)for x in pm],dtype=np.float32);pred=sum(np.einsum('vij,vj->vi',palette[joints[:,k]],pos)*weights[:,k,None]for k in range(4))[:,:3];oracle=np.zeros((len(rest),6),dtype=np.float32)if(clip,at)in probe else None;maxerr=0;worst='';maxbone=0;minimum_sole=1e9;source_sole=1e9
   for i,b in enumerate(bones):
    head=palette[i]@np.array([*b.head_local,1]);tail=palette[i]@np.array([*b.tail_local,1]);maxbone=max(maxbone,abs(np.linalg.norm(tail[:3]-head[:3])-b.length*rigworld.to_scale().x))
   for o in meshes:
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();ids,vids,loops,unique=mapping[o.name];coords=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',coords);coords=coords.reshape(-1,3);mat=np.asarray(ev.matrix_world,dtype=np.float64);actual=coords@mat[:3,:3].T+mat[:3,3];errors=np.linalg.norm(pred[ids]-actual[vids],axis=1)
    if o.get('default_visible',True)and errors.max()>maxerr:maxerr=float(errors.max());worst=o.name
    if oracle is not None:
     normals=np.empty(len(me.corner_normals)*3,dtype=np.float32);me.corner_normals.foreach_get('vector',normals);normals=normals.reshape(-1,3);normalmat=np.linalg.inv(mat[:3,:3]).T;normal=normals[loops]@normalmat.T;normal/=np.linalg.norm(normal,axis=1)[:,None];oracle[ids,:3]=actual[vids];oracle[ids,3:]=normal
    if o.name.startswith('Boot sole '):
     side=o.name[-1];q=pred[ids[unique]];low=float(q[:,2].min());minimum_sole=min(minimum_sole,low);centre=q[q[:,2]<=low+1e-5].mean(0).astype(float);source_low=float(actual[:,2].min());source_sole=min(source_sole,source_low);actual_centre=actual[actual[:,2]<=source_low+1e-5].mean(0);t=at/60;cycle=math.floor((t+(0 if side=='L'else .4))/.8);stance=clip!='walk'or(t+(0 if side=='L'else .4)-cycle*.8)<.4
     if clip=='walk':centre[0]+=2*t;actual_centre[0]+=2*t
     if stance:
      key=(clip,side,cycle if clip=='walk'else 0);contacts.setdefault(key,[]).append(centre);source_contacts.setdefault(key,[]).append(actual_centre)
    if o.name=='Tome page block':
     first=np.where(vids==0)[0][0];last=np.where(vids==len(me.vertices)-1)[0][0];book.append(float(np.linalg.norm(pred[ids[first]]-pred[ids[last]])))
    ev.to_mesh_clear()
   fractional_palettes.extend(float(palette[i,r,c])for i in range(len(palette))for c in range(4)for r in range(4));matrices=[Matrix(x.tolist())for x in palette];clearance=1e9
   for name,(src,ids)in pairs.items():
    a=bpy.data.objects[name];b=bpy.data.objects[src]
    for i,j in enumerate(ids):
     q,_=core(a,a.data.vertices[i],matrices);v,n=core(b,b.data.vertices[j],matrices);clearance=min(clearance,(q-v).dot(n))
   row={'clip':clip,'frame':at,'max_world_error_m':maxerr,'worst_object':worst,'bone_error_m':float(maxbone),'minimum_sole_z':minimum_sole,'source_minimum_sole_z':source_sole,'minimum_core_clearance_m':clearance,'pass':bool(maxerr<=.001 and maxbone<=.001 and minimum_sole>=-.001 and source_sole>=-.001 and clearance>=.006)};records.append(row)
   if oracle is not None:
    name=f'{clip}-{at:05.1f}'.replace('.','_');path=assets/(name+'-oracle.bin');path.write_bytes(oracle.astype('<f4').tobytes());oracles.append({'id':name,'clip':clip,'frame':at,'pose0':accepted['clips'][clip]['frame_start']+frame,'pose1':accepted['clips'][clip]['frame_start']+frame+1 if frame+1<count else(0 if clip=='cast'else accepted['clips'][clip]['frame_start']),'alpha':alpha,'oracle':{'path':str(path.relative_to(HERE)),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}})
   if len(records)%24==0:print('E05E_PROGRESS',len(records),row,flush=True)
def contact_rows(groups):
 out=[]
 for key,points in groups.items():
  a=np.array(points);drift=float(np.max(np.linalg.norm(a[:,None]-a[None,:],axis=2)));out.append({'clip':key[0],'side':key[1],'cycle':key[2],'samples':len(a),'maximum_pairwise_drift_m':drift,'pass':drift<=.02})
 return out
fractional_buffer=floats(assets/'fractional-palettes.bin',fractional_palettes);cr=contact_rows(contacts);sr=contact_rows(source_contacts);book_variation=max(book)/min(book)-1;checks={'all312_source_samples':len(records)==312 and all(x['pass']for x in records),'all216_integer_palettes_exact':all(x['active_palettes_exact']for x in integer_checks),'candidate_contacts':all(x['pass']for x in cr),'source_contacts':all(x['pass']for x in sr),'book_variation':book_variation<=.01,'source_unchanged':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==source_hash};report={'candidate':'LINEAR source channels / raw quaternion nlerp','source_sha256':source_hash,'checks':checks,'records':records,'candidate_contacts':cr,'source_fractional_contacts':sr,'book_size_variation':book_variation,'integer_checks':integer_checks,'oracles':oracles,'max_world_error_m':max(x['max_world_error_m']for x in records),'max_bone_error_m':max(x['bone_error_m']for x in records),'fractional_palette_buffer':fractional_buffer,'seconds':time.monotonic()-start};(HERE/'evidence/preflight-v1.json').write_text(json.dumps(report,indent=2)+'\n');print('E05E_DONE',checks,report['max_world_error_m'],report['max_bone_error_m'],flush=True)
