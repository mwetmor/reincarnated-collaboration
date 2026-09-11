import bpy,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05I');source=Path(bpy.data.filepath);source_hash=hashlib.sha256(source.read_bytes()).hexdigest();structure=json.loads((HERE.parent/'E05B/inputs/source-structure.json').read_text());S=2/(structure['bounds'][2][1]-structure['bounds'][2][0]);ZMIN=structure['bounds'][2][0];rig=bpy.data.objects['WizardRig'];scene=bpy.context.scene
for track in rig.animation_data.nla_tracks:track.mute=True
rig.animation_data.action=None
rig.matrix_world=Matrix.Translation((0,0,-ZMIN*S))@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Scale(S,4)
for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis.identity()
rest={b.name:b.matrix_local.copy()for b in rig.data.bones};qrest={n:m.to_quaternion()for n,m in rest.items()};cycle=.8;speed=2;STANCE_SECONDS=.4

desired_matrices={}
def orient(name,delta=None,head=None):
 pb=rig.pose.bones[name];bone=rig.data.bones[name]
 inherited=desired_matrices[pb.parent.name]@rest[pb.parent.name].inverted()@rest[name] if pb.parent else rest[name]
 loc=Vector(head) if head is not None else inherited.translation
 rot=(delta or Quaternion((1,0,0,0)))@qrest[name]
 desired_matrices[name]=Matrix.Translation(loc)@rot.to_matrix().to_4x4()
 pb.matrix_basis=inherited.inverted()@desired_matrices[name]
def solve_pose(t,bad=None):
 desired_matrices.clear()
 for pb in rig.pose.bones:pb.matrix_basis.identity()
 feet={};limits=[]
 for side,offset in [('L',0),('R',.4)]:
  if bad=='repeat-lead':offset=0
  pt=t+offset;n=math.floor(pt/cycle);phase=pt-n*cycle;support=phase<STANCE_SECONDS;plant=(n*cycle-offset)*speed+speed*STANCE_SECONDS/2
  if not support:
   q=(phase-STANCE_SECONDS)/(cycle-STANCE_SECONDS);plant+=cycle*speed*q*q*(3-2*q);lift=.14*math.sin(math.pi*q)**2
  else:lift=0
  ankle=rig.data.bones['Foot.'+side].head_local.copy();ankle.y+=(speed*t-plant)/S;ankle.z+=lift/S
  hip=rig.data.bones['Thigh.'+side].head_local;L1=rig.data.bones['Thigh.'+side].length;L2=rig.data.bones['Shin.'+side].length;horiz=(ankle.x-hip.x)**2+(ankle.y-hip.y)**2
  limits.append(ankle.z+math.sqrt(max(0,(L1+L2-.015/S)**2-horiz)));feet[side]={'ankle':ankle,'support':support,'cycle':n,'lengths':(L1,L2)}
 smoothmin=lambda a,b:.5*(a+b-math.sqrt((a-b)**2+(.03/S)**2));hip_z=smoothmin(1.045,smoothmin(*limits));drop=hip_z-1.045
 orient('Root');orient('Hips',head=rig.data.bones['Hips'].head_local+Vector((0,0,drop)))
 twist=.10*math.sin(t/cycle*2*math.pi)
 for name in ['Spine','Chest','Neck','Head']:
  angle=twist if name in ['Spine','Chest']else twist*.25
  orient(name,Quaternion(Vector((0,0,1)),angle)@Quaternion(Vector((1,0,0)),.025))

 for side,sgn,offset in [('L',1,0),('R',-1,.4)]:
  swing=math.sin((t+offset)/cycle*2*math.pi);angle=.22*swing;arm=Quaternion(Vector((1,0,0)),angle)@Quaternion(Vector((0,1,0)),sgn*.49);fore=Quaternion(Vector((1,0,0)),angle-.17)@Quaternion(Vector((0,1,0)),sgn*.49)
  orient('UpperArm.'+side,arm);orient('Forearm.'+side,fore);orient('Hand.'+side,fore)
  for finger in ['Index','Middle','Ring','Little','Thumb']:orient(finger+'.'+side,fore)
  f=feet[side];hip=rig.data.bones['Thigh.'+side].head_local+Vector((0,0,drop));ankle=f['ankle'];delta=ankle-hip;distance=delta.length;unit=delta.normalized();l1,l2=f['lengths'];a=(l1*l1-l2*l2+distance*distance)/(2*distance);bend=Vector((0,-1,0));bend=(bend-unit*bend.dot(unit)).normalized();knee=hip+unit*a+bend*math.sqrt(max(0,l1*l1-a*a))
  assert distance<=l1+l2+1e-6
  for name,head,tail in [('Thigh.'+side,hip,knee),('Shin.'+side,knee,ankle)]:
   bone=rig.data.bones[name];orient(name,(bone.tail_local-bone.head_local).rotation_difference(tail-head),head=head)
  orient('Foot.'+side,head=ankle);orient('Toe.'+side)
  for prefix,ang in [('Front',min(-.04,math.atan2(knee.y-hip.y,hip.z-knee.z)-.12)),('Back',max(.04,math.atan2(ankle.y,1.10-ankle.z)+.08))]:orient('Coat.'+prefix+'.'+side,Quaternion(Vector((1,0,0)),ang)@Quaternion(Vector((0,1,0)),-sgn*.055))
 orient('Tabard',Quaternion(Vector((1,0,0)),-.12-.06*abs(math.sin(t/cycle*2*math.pi))))
 if bad=='bag-swell':bpy.data.objects['Tome page block'].scale=(1.2,1.2,1.2)
 else:bpy.data.objects['Tome page block'].scale=(1,1,1)
 bpy.context.view_layer.update();return feet

def mesh_positions(name):
 obj=bpy.data.objects[name].evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=obj.to_mesh();points=[obj.matrix_world@v.co for v in mesh.vertices];obj.to_mesh_clear();return points

# Stationary actions preserve the source feet and geometry.
def stationary(t,kind):
 desired_matrices.clear()
 for pb in rig.pose.bones:pb.matrix_basis.identity()
 smooth=lambda x:(max(0,min(1,x)))**2*(3-2*max(0,min(1,x)))
 if kind=='cast':
  q=smooth(t/.6)if t<=.6 else 1-smooth((t-.6)/.6)
  breath=0
 else:q=0;breath=math.sin(t/1.6*2*math.pi)
 orient('Root');orient('Hips')
 for name in ['Spine','Chest','Neck','Head']:
  orient(name,Quaternion(Vector((1,0,0)),(.06*q+.012*breath)if name in ['Spine','Chest']else 0))
 for side,sgn in [('L',1),('R',-1)]:
  angle=-q*(.95 if side=='R'else .30)+.02*breath
  arm=Quaternion(Vector((1,0,0)),angle)@Quaternion(Vector((0,1,0)),sgn*.49)
  fore=Quaternion(Vector((1,0,0)),angle-.17-q*.16)@Quaternion(Vector((0,1,0)),sgn*.49)
  orient('UpperArm.'+side,arm);orient('Forearm.'+side,fore);orient('Hand.'+side,fore)
  for finger in ['Index','Middle','Ring','Little','Thumb']:orient(finger+'.'+side,fore)
  for name in ['Thigh.','Shin.','Foot.','Toe.']:orient(name+side)
  for part in ['Front','Back']:orient('Coat.'+part+'.'+side)
 orient('Tabard')
 bpy.context.view_layer.update()
def signature():return {p.name:[v for row in p.matrix for v in row]for p in rig.pose.bones}
def error(a,b):return max(abs(v-w)for name,vs in a.items()for v,w in zip(vs,b[name]))
# Preserve old action data and all source meshes; author only turn actions.
import struct
col=bpy.data.collections['Wizard_Character']
def source_signature():
 h=hashlib.sha256()
 for o in sorted([o for o in col.objects if o.type=='MESH'],key=lambda x:x.name):
  h.update(o.name.encode())
  for v in o.data.vertices:
   h.update(struct.pack('<3d',*v.co))
   for g in v.groups:h.update(struct.pack('<id',g.group,g.weight))
  for uv in o.data.uv_layers:
   for x in uv.data:h.update(struct.pack('<2d',*x.uv))
  for m in o.data.materials:h.update(m.name.encode())
 return h.hexdigest()
before=source_signature();rig.animation_data.action=None;stationary(0,'idle');idle_mats={pb.name:pb.matrix.copy()for pb in rig.pose.bones};idle_hip=(rig.matrix_world@rig.pose.bones['Hips'].head).z
smooth=lambda x:(max(0,min(1,x)))**2*(3-2*max(0,min(1,x)))
def turn_pose(t,sign):
 desired_matrices.clear()
 for pb in rig.pose.bones:pb.matrix_basis.identity()
 theta=sign*math.pi/4*smooth(t/.6);rot=Matrix.Rotation(theta,3,'Z');qbody=Quaternion(Vector((0,0,1)),theta);end=Matrix.Rotation(sign*math.pi/4,3,'Z');feet={};limits=[]
 for side,begin in [('R',0),('L',.3)]:
  q=max(0,min(1,(t-begin)/.3));swing=0<q<1;start=rig.data.bones['Foot.'+side].head_local.copy();target=end@start;ankle=start.lerp(target,smooth(q));ankle.z+=.08/S*math.sin(math.pi*q)**2;angle=sign*math.pi/4*smooth(q);hip=rot@rig.data.bones['Thigh.'+side].head_local;L1=rig.data.bones['Thigh.'+side].length;L2=rig.data.bones['Shin.'+side].length;reach=L1+L2-.003/S*math.sin(math.pi*t/.6)**2;horiz=(ankle.x-hip.x)**2+(ankle.y-hip.y)**2;limits.append(ankle.z+math.sqrt(max(0,reach*reach-horiz)));feet[side]={'ankle':ankle,'angle':angle,'stance':not swing,'group':1 if q>=1 else 0,'lengths':(L1,L2)}
 drop=min(0,min(limits)-rig.data.bones['Hips'].head_local.z)
 orient('Root',qbody);orient('Hips',qbody,head=rot@rig.data.bones['Hips'].head_local+Vector((0,0,drop)))
 for name in ['Spine','Chest','Neck','Head']:orient(name,qbody)
 for side,sgn in [('L',1),('R',-1)]:
  arm=qbody@Quaternion(Vector((0,1,0)),sgn*.49);fore=qbody@Quaternion(Vector((1,0,0)),-.17)@Quaternion(Vector((0,1,0)),sgn*.49)
  orient('UpperArm.'+side,arm);orient('Forearm.'+side,fore);orient('Hand.'+side,fore)
  for finger in ['Index','Middle','Ring','Little','Thumb']:orient(finger+'.'+side,fore)
  f=feet[side];hip=rot@rig.data.bones['Thigh.'+side].head_local+Vector((0,0,drop));ankle=f['ankle'];delta=ankle-hip;distance=delta.length;unit=delta.normalized();l1,l2=f['lengths'];a=(l1*l1-l2*l2+distance*distance)/(2*distance);bend=rot@rig.data.bones['Shin.'+side].head_local-hip;bend=(bend-unit*bend.dot(unit)).normalized();knee=hip+unit*a+bend*math.sqrt(max(0,l1*l1-a*a));assert distance<=l1+l2+1e-6
  for name,head,tail in [('Thigh.'+side,hip,knee),('Shin.'+side,knee,ankle)]:
   b=rig.data.bones[name];orient(name,(b.tail_local-b.head_local).rotation_difference(tail-head),head=head)
  qfoot=Quaternion(Vector((0,0,1)),f['angle']);orient('Foot.'+side,qfoot,head=ankle);orient('Toe.'+side,qfoot)
  for part in ['Front','Back']:orient('Coat.'+part+'.'+side,qbody)
 orient('Tabard',qbody);bpy.context.view_layer.update();return feet
results={'checks':{},'clips':{},'source_sha256':source_hash,'source_geometry_weights_uv_material_before':before};scene.render.fps=60
for name,sign in [('turn_left',1),('turn_right',-1)]:
 action=bpy.data.actions.new('E05M_'+name);action.use_fake_user=True;rig.animation_data.action=action;rows=[];contacts={};books=[];joints=[];poses=[];bone_error=0
 for frame in range(37):
  scene.frame_set(frame);feet=turn_pose(frame/60,sign);row={'frame':frame,'time_s':frame/60,'feet':{},'heading_delta_deg':sign*45*smooth(frame/36),'hips_z':(rig.matrix_world@rig.pose.bones['Hips'].head).z,'socket_world':list(rig.matrix_world@rig.pose.bones['Hand.R'].tail)}
  for side in ['L','R']:
   pts=mesh_positions('Boot sole '+side);low=min(q.z for q in pts);bottom=[q for q in pts if q.z<=low+1e-5];centre=sum(bottom,Vector())/len(bottom);f=feet[side];row['feet'][side]={'world':list(centre),'min_z':low,'stance':f['stance'],'group':f['group']}
   if f['stance']:contacts.setdefault((side,f['group']),[]).append(centre)
  pts=mesh_positions('Tome page block');books.append((pts[0]-pts[-1]).length);joints.append({pb.name:rig.matrix_world@pb.head for pb in rig.pose.bones});poses.append({pb.name:pb.matrix.copy()for pb in rig.pose.bones})
  for pb in rig.pose.bones:
   bone_error=max(bone_error,abs((pb.tail-pb.head).length-rig.data.bones[pb.name].length)*S);pb.keyframe_insert(data_path='location',frame=frame,group=pb.name);pb.keyframe_insert(data_path='rotation_quaternion',frame=frame,group=pb.name);pb.keyframe_insert(data_path='scale',frame=frame,group=pb.name)
  rows.append(row)
 rotend=Matrix.Rotation(sign*math.pi/4,4,'Z');start_error=max(abs(poses[0][n][i][j]-m[i][j])for n,m in idle_mats.items()for i in range(4)for j in range(4));end_error=max(abs(poses[-1][n][i][j]-(rotend@m)[i][j])for n,m in idle_mats.items()for i in range(4)for j in range(4));drift=max((a-b).length for ps in contacts.values()for a in ps for b in ps);step=max((row[n]-joints[i-1][n]).length for i,row in enumerate(joints)if i for n in row);hips=[r['hips_z']for r in rows];lift=min(rows[9]['feet']['R']['min_z'],rows[27]['feet']['L']['min_z']);bad=max((rotend.to_3x3()@Vector(rows[0]['feet'][s]['world'])-Vector(rows[0]['feet'][s]['world'])).length for s in ['L','R']);checks={'contact_drift':drift<=.02,'penetration':min(f['min_z']for r in rows for f in r['feet'].values())>=-.001,'mid_swing_lift':lift>=.04,'bone_lengths':bone_error<=.001,'book_stability':max(books)/min(books)-1<=.01,'hips_min':min(hips)>=idle_hip*.85,'hips_excursion':max(hips)-min(hips)<=.12,'start_idle':start_error<=1e-5,'end_rotated_idle':end_error<=1e-5,'joint_continuity':step<=.05,'instant_turn_bad_detected':bad>.02};results['clips'][name]={'fps':60,'duration_s':.6,'frame_count':36,'heading_delta_deg':sign*45,'samples':rows,'checks':checks,'contact_drift_m':drift,'start_idle_matrix_error':start_error,'end_idle_matrix_error':end_error,'max_joint_step_m':step,'hip_excursion_m':max(hips)-min(hips),'mid_swing_lift_m':lift,'bad_instant_turn_drift_m':bad};print('E05I_TURN',name,checks,drift,start_error,end_error,step,flush=True)
results['checks']['source_geometry_weights_uv_material_unchanged']=before==source_signature();results['status']='PASS'if all(results['checks'].values())and all(all(c['checks'].values())for c in results['clips'].values())else'FAIL';(HERE/'evidence/author-motion.json').write_text(json.dumps(results,indent=2)+'\n');rig.animation_data.action=bpy.data.actions['E05M_idle'];scene.frame_set(0);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/turns-v1.blend'));print('E05I_AUTHOR',results['status'],flush=True)
