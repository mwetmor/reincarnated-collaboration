import bpy,json,hashlib,collections
from pathlib import Path
p=Path(__file__).resolve().parent;source=Path(bpy.data.filepath);before=hashlib.sha256(source.read_bytes()).hexdigest();rig=bpy.data.objects['WizardRig'];inventory=[];keys_before=[]
for clip in ['stop_00','start_00','stop_12','stop_24','start_24','stop_36']:
 a=bpy.data.actions['E05M_'+clip];curves=[f for layer in a.layers for strip in layer.strips for bag in strip.channelbags for f in bag.fcurves];old=collections.Counter()
 for f in curves:
  for k in f.keyframe_points:keys_before.append([clip,f.data_path,f.array_index,*k.co]);old[k.interpolation]+=1;k.interpolation='LINEAR'
 inventory.append({'clip':clip,'old':dict(old),'new':dict(collections.Counter(k.interpolation for f in curves for k in f.keyframe_points))})
keys_after=[]
for clip in ['stop_00','start_00','stop_12','stop_24','start_24','stop_36']:
 for layer in bpy.data.actions['E05M_'+clip].layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for f in bag.fcurves:
     for k in f.keyframe_points:keys_after.append([clip,f.data_path,f.array_index,*k.co])
assert keys_before==keys_after;out=p/'inputs/linear-channels-v1.blend';assert not out.exists();bpy.ops.wm.save_as_mainfile(filepath=str(out),check_existing=False);r={'source':str(source),'source_sha256':before,'new_source_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'keys_exact':keys_before==keys_after,'key_count':len(keys_before),'key_values_sha256':hashlib.sha256(json.dumps(keys_before,separators=(',',':')).encode()).hexdigest(),'source_unchanged':hashlib.sha256(source.read_bytes()).hexdigest()==before,'inventory':inventory,'bone_conventions':[{'name':b.name,'parent':b.parent.name if b.parent else None,'inherit_scale':b.inherit_scale,'use_inherit_rotation':b.use_inherit_rotation,'use_local_location':b.use_local_location,'rotation_mode':rig.pose.bones[b.name].rotation_mode,'constraints':[c.type for c in rig.pose.bones[b.name].constraints]}for b in rig.data.bones]};(p/'evidence/author-v1.json').write_text(json.dumps(r,indent=2)+'\n');print('E05F_AUTHOR',r['keys_exact'],r['key_count'],r['source_unchanged'],r['bone_conventions'])
