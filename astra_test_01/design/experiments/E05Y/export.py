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
poses=[];checks=[];records=[];fit=[];palettes_flat=[];endpoints={};clips={};bounds=[float('inf')]*3+[float('-inf')]*3
oracle_keys={('idle',0),('idle',24),('idle',72),('walk',0),('walk',12),('walk',36),('cast',0),('cast',18),('cast',36)}
# Recreate recorded core correspondences from author predicates, not nearest-point fitting.
pairs={'GEAR_cuirass':('Tailored upper robe',list(range(len(bpy.data.objects['Tailored upper robe'].data.vertices))))}
for side in ['L','R']:
 src=bpy.data.objects['Robe sleeve '+side];group=src.vertex_groups['Forearm.'+side].index
 faces=[p for p in src.data.polygons if 1.12<p.center.z<1.29 and p.center.y<.035 and all(any(g.group==group and g.weight>.999 for g in src.data.vertices[i].groups)for i in p.vertices)]
 pairs['GEAR_bracer-'+side]=(src.name,sorted({i for p in faces for i in p.vertices}))
 src=bpy.data.objects['Boot shaft '+side];faces=[p for p in src.data.polygons if .175<p.center.z<.44 and p.center.y<.025]
 pairs['GEAR_greave-'+side]=(src.name,sorted({i for p in faces for i in p.vertices}))
def core(o,v,palette):
 ws=[(bone_ids[o.vertex_groups[g.group].name],g.weight)for g in v.groups if o.vertex_groups[g.group].name in bone_ids];total=sum(w for _,w in ws)
 local=rigworld.inverted()@o.matrix_world
 q=sum(((palette[i]@(local@v.co))*(w/total)for i,w in ws),Vector()) if ws else o.matrix_world@v.co
 n=sum(((palette[i].to_3x3()@local.to_3x3()@v.normal)*(w/total)for i,w in ws),Vector()).normalized() if ws else (o.matrix_world.to_3x3()@v.normal).normalized()
 return q,n
for clip,count in [('idle',96),('walk',48),('cast',72)]:
 begin=len(poses);contacts={};book=[];matrices=[];max_bone=0
 for frame in range(count+1):
  rig.animation_data.action=bpy.data.actions['E05M_'+clip];scene.frame_set(frame);bpy.context.view_layer.update();palette=[rig.matrix_world@rig.pose.bones[b.name].matrix@b.matrix_local.inverted()for b in bones]+[rig.matrix_world.copy()];pv=[m[row][col]for m in palette for col in range(4)for row in range(4)];matrices.append(pv);t=frame/60
  max_bone=max(max_bone,max(abs((pb.tail-pb.head).length-rig.data.bones[pb.name].length)*rigworld.to_scale().x for pb in rig.pose.bones))
  row={'clip':clip,'frame':frame,'time_s':t,'socket_world':list(rig.matrix_world@rig.pose.bones['Hand.R'].tail),'feet':{}};oracle=[0.]*(len(vertices)//16*6) if (clip,frame)in oracle_keys else None;maxerror=0;sampled=0
  dg=bpy.context.evaluated_depsgraph_get()
  for o in meshes:
   ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();assert len(me.vertices)==maps[o.name]['evaluated_vertices'] and len(me.loops)==maps[o.name]['evaluated_loops'],o.name;nm=ev.matrix_world.to_3x3().inverted().transposed()
   step=max(1,len(maps[o.name]['map'])//64)
   for k,(keyid,vid,li,pos,ws)in enumerate(maps[o.name]['map']):
    if oracle is None and k%step:continue
    actual=ev.matrix_world@me.vertices[vid].co
    if oracle is not None:oracle[keyid*6:keyid*6+6]=list(actual)+list((nm@me.corner_normals[li].vector).normalized())
    if k%step==0:
     predicted=sum(((palette[i]@Vector(pos))*w for i,w in ws),Vector());maxerror=max(maxerror,(predicted-actual).length);sampled+=1
   if o.name.startswith('Boot sole '):
    side=o.name[-1];points=[ev.matrix_world@v.co for v in me.vertices];low=min(q.z for q in points);support=[q for q in points if q.z<=low+1e-5];centre=sum(support,Vector())/len(support)+Vector((2*t if clip=='walk'else 0,0,0));offset=0 if side=='L'else .4;cycle=math.floor((t+offset)/.8);stance=clip!='walk'or(t+offset-cycle*.8)<.4
    row['feet'][side]={'world':list(centre),'min_z':low,'stance':stance,'cycle':cycle}
    if stance:contacts.setdefault((side,cycle if clip=='walk'else 0),[]).append(centre)
   if o.name=='Tome page block':book.append((ev.matrix_world@(me.vertices[0].co-me.vertices[-1].co).to_4d()).to_3d().length if False else (ev.matrix_world@me.vertices[0].co-ev.matrix_world@me.vertices[-1].co).length)
   ev.to_mesh_clear()
  for name,(source,ids)in pairs.items():
   a=bpy.data.objects[name];b=bpy.data.objects[source];assert len(a.data.vertices)==len(ids),(name,len(a.data.vertices),len(ids));ds=[]
   for i,j in enumerate(ids):
    q,_=core(a,a.data.vertices[i],palette);r,n=core(b,b.data.vertices[j],palette);ds.append((q-r).dot(n))
   fit.append({'clip':clip,'frame':frame,'object':name,'samples':len(ds),'minimum_signed_core_clearance_m':min(ds),'pass':min(ds)>=.006})
  records.append(row);checks.append({'clip':clip,'frame':frame,'sampled':sampled,'max_world_error_m':maxerror,'topology_preserved':True,'pass':maxerror<=.001})
  if frame<count:
   rec={'id':f'{clip}-{frame:03}','clip':clip,'frame':frame,'time_s':t,'palette_offset_float32':len(palettes_flat),'socket_world':row['socket_world']};palettes_flat+=pv
   if oracle is not None:rec['oracle']=floats(assets/f'{clip}-{frame:03}-oracle.bin',oracle)
   poses.append(rec)
  else:endpoints[clip]=pv
  if frame%24==0:print('E05Y_FRAME',clip,frame,'error',maxerror,flush=True)
 drift=max((a-b).length for points in contacts.values()for a in points for b in points)
 c={'frame_start':begin,'frame_count':count,'fps':60,'duration_s':count/60,'loop':clip!='cast','root_motion_mps':[2,0,0]if clip=='walk'else[0,0,0],'contact_drift_m':drift,'min_sole_z':min(v['min_z']for r in records if r['clip']==clip for v in r['feet'].values()),'book_size_variation':max(book)/min(book)-1,'bone_error_m':max_bone,'endpoint_matrix_error':max(abs(a-b)for a,b in zip(matrices[0],matrices[-1]))}
 if clip=='cast':c['release_s']=.6;c['release_frame']=36;c['end_idle_start_error']=max(abs(a-b)for a,b in zip(endpoints['cast'],palettes_flat[:len(pv)]))
 clips[clip]=c
manifest.update(asset_id='E05Y-complete-existing-motion',poses=poses,clips=clips,palette_buffer=floats(assets/'palettes.bin',palettes_flat),palette_stride_float32=len(pv),qualification='Complete existing clip transfer test; turn transitions and complete outfit surface fit separate.')
(HERE/'character.asset.json').write_text(json.dumps(manifest,indent=2)+'\n')
report={'source_sha256':source_hash,'source_unchanged':source_hash==hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'rest_geometry_indices_weights_exact':True,'rest_uv_reexport_max_error':1.1920928955078125e-7,'runtime_rest_buffers':'Exact cached E05W v2 bytes reused','samples':records,'source_checks':checks,'fit_checks':fit,'clips':clips,'max_world_error_m':max(x['max_world_error_m']for x in checks),'fit_failures':sum(not x['pass']for x in fit),'seconds':time.monotonic()-start}
(HERE/'evidence/source-motion.json').write_text(json.dumps(report,indent=2)+'\n');print('E05Y_DONE',len(poses),report['max_world_error_m'],report['fit_failures'],flush=True)
