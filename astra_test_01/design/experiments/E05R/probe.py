import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
out=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05R/evidence')
rig=bpy.data.objects.get('WizardRig');assert rig and rig.type=='ARMATURE'
scene=bpy.context.scene
result={'blender_version':bpy.app.version_string,'source_file':bpy.data.filepath,'source_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'bones':[{'name':b.name,'head':list(b.head_local),'tail':list(b.tail_local),'length':b.length,'parent':b.parent.name if b.parent else None}for b in rig.data.bones],'actions':[{'name':a.name,'frame_range':list(a.frame_range)}for a in bpy.data.actions],'fps':scene.render.fps,'mesh_vertices':sum(len(o.data.vertices)for o in bpy.data.objects if o.type=='MESH'),'samples':[],'source_written':False}
rig.animation_data.action=bpy.data.actions['Walk']
for track in rig.animation_data.nla_tracks:track.mute=True
for i in range(97):
 frame=i/4;scene.frame_set(int(frame),subframe=frame-int(frame));deps=bpy.context.evaluated_depsgraph_get();evaluated=rig.evaluated_get(deps);result['samples'].append({'t':frame/scene.render.fps,'bones':{n:{'head':list(evaluated.matrix_world@evaluated.pose.bones[n].head),'tail':list(evaluated.matrix_world@evaluated.pose.bones[n].tail)}for n in ['Hips','Foot.L','Foot.R','Toe.L','Toe.R']}})
result['measured_stance_drift_m']={}
for speed in [1.2,2.0]:
 groups={}
 for side,offset in [('L',0),('R',.5)]:
  samples=[s for s in result['samples'] if ((s['t']/.8+offset)%1)<.6 and s['t']<.8]
  # Keep support-cycle groups separate across phase wrap.
  for s in samples:
   n=math.floor(s['t']/.8+offset);p=s['bones']['Toe.'+side]['tail'];groups.setdefault((side,n),[]).append([p[0],p[1]-speed*s['t'],p[2]])
 drift=max(math.dist(a,b)for points in groups.values() for a in points for b in points)
 result['measured_stance_drift_m'][str(speed)]=drift
(out/'blender-rig-inspection.json').write_text(json.dumps(result,indent=2));print('RIG_PROBE',json.dumps({k:result[k]for k in ['blender_version','mesh_vertices','measured_stance_drift_m','source_written']}))
