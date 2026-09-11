import bpy,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05M');source=Path(bpy.data.filepath);source_hash=hashlib.sha256(source.read_bytes()).hexdigest();structure=json.loads((HERE.parent/'E05B/inputs/source-structure.json').read_text());S=2/(structure['bounds'][2][1]-structure['bounds'][2][0]);ZMIN=structure['bounds'][2][0];rig=bpy.data.objects['WizardRig'];scene=bpy.context.scene
for track in rig.animation_data.nla_tracks:track.mute=True
rig.animation_data.action=None
rig.matrix_world=Matrix.Translation((0,0,-ZMIN*S))@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Scale(S,4)
for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis.identity()
rest={b.name:b.matrix_local.copy()for b in rig.data.bones};qrest={n:m.to_quaternion()for n,m in rest.items()};cycle=.8;speed=2;stance=.4

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
  pt=t+offset;n=math.floor(pt/cycle);phase=pt-n*cycle;support=phase<stance;plant=(n*cycle-offset)*speed+speed*stance/2
  if not support:
   q=(phase-stance)/(cycle-stance);plant+=cycle*speed*q*q*(3-2*q);lift=.14*math.sin(math.pi*q)**2
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
source_geometry={o.name:[tuple(v.co)for v in o.data.vertices]for o in bpy.data.collections['Wizard_Character'].objects if o.type=='MESH'}
results={'clips':{},'checks':{},'source':str(source),'source_sha256':source_hash};scene.render.fps=60;idle0=None
for kind,duration in [('idle',1.6),('walk',.8),('cast',1.2)]:
 count=round(duration*60);records=[];contacts={};book=[];maxbone=0;poses=[]
 action=bpy.data.actions.new('E05M_'+kind);rig.animation_data.action=action
 for i in range(count+1):
  scene.frame_set(i);t=i/60
  if kind=='walk':f=solve_pose(t)
  else:stationary(t,kind)
  ps=signature();poses.append(ps);row={'frame':i,'time_s':t,'feet':{},'socket_world':list(rig.matrix_world@rig.pose.bones['Hand.R'].tail)}
  for side in ['L','R']:
   points=mesh_positions('Boot sole '+side);low=min(p.z for p in points);support=[p for p in points if p.z<=low+1e-5];centre=sum(support,Vector())/len(support)+Vector((2*t if kind=='walk'else 0,0,0));stance=True if kind!='walk'else f[side]['support'];cycleindex=0 if kind!='walk'else f[side]['cycle'];row['feet'][side]={'world':list(centre),'min_z':low,'stance':stance}
   if stance:contacts.setdefault((side,cycleindex),[]).append(centre)
  for pb in rig.pose.bones:
   maxbone=max(maxbone,abs((pb.tail-pb.head).length-rig.data.bones[pb.name].length)*S)
   pb.keyframe_insert(data_path='location',frame=i,group=pb.name);pb.keyframe_insert(data_path='rotation_quaternion',frame=i,group=pb.name);pb.keyframe_insert(data_path='scale',frame=i,group=pb.name)
  points=mesh_positions('Tome page block');book.append((points[0]-points[-1]).length);records.append(row)
 action.use_fake_user=True;drift=max((a-b).length for points in contacts.values()for a in points for b in points);minimum=min(f['min_z']for r in records for f in r['feet'].values());loop_error=error(poses[0],poses[-1])
 if kind=='idle':idle0=poses[0]
 r={'action':action.name,'duration_s':duration,'fps':60,'frame_count':count,'samples':records,'contact_drift_m':drift,'min_sole_z':minimum,'book_size_variation':max(book)/min(book)-1,'bone_error_m':maxbone,'endpoint_matrix_error':loop_error}
 results['checks'][kind+'_contacts']=drift<=(.02 if kind=='walk'else .001)
 results['checks'][kind+'_penetration']=minimum>=-.001;results['checks'][kind+'_book']=r['book_size_variation']<=.01;results['checks'][kind+'_bones']=maxbone<=.001
 if kind!='cast':results['checks'][kind+'_loop']=loop_error<=1e-5
 else:r['cast_end_idle_start_error']=error(poses[-1],idle0);results['checks']['cast_returns_idle']=r['cast_end_idle_start_error']<=1e-5
 results['clips'][kind]=r
assert all(source_geometry[o.name]==[tuple(v.co)for v in o.data.vertices]for o in bpy.data.collections['Wizard_Character'].objects if o.type=='MESH')
results['checks']['source_geometry_unchanged']=True
results['status']='PASS'if all(results['checks'].values())else'FAIL';(HERE/'evidence/source-motion.json').write_text(json.dumps(results,indent=2))
print('E05M_SOURCE',json.dumps({'checks':results['checks'],'metrics':{k:{q:r[q]for q in ['contact_drift_m','min_sole_z','bone_error_m','endpoint_matrix_error']}for k,r in results['clips'].items()}}))
if not all(results['checks'].values()):raise RuntimeError('Source preflight failed; no render')
rig.animation_data.action=bpy.data.actions['E05M_idle'];scene.frame_set(0)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/motion-v1.blend'))
