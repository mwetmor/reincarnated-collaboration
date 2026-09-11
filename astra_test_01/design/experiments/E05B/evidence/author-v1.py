import bpy,math,json,hashlib,sys,time
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05B');source=Path(bpy.data.filepath);source_hash=hashlib.sha256(source.read_bytes()).hexdigest();structure=json.loads((HERE/'inputs/source-structure.json').read_text());S=2/(structure['bounds'][2][1]-structure['bounds'][2][0]);ZMIN=structure['bounds'][2][0];rig=bpy.data.objects['WizardRig'];scene=bpy.context.scene
for track in rig.animation_data.nla_tracks:track.mute=True
rig.animation_data.action=None
rig.matrix_world=Matrix.Translation((0,0,-ZMIN*S))@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Scale(S,4)
for p in rig.pose.bones:p.rotation_mode='QUATERNION';p.matrix_basis.identity()
rest={b.name:b.matrix_local.copy()for b in rig.data.bones};qrest={n:m.to_quaternion()for n,m in rest.items()};cycle=.8;speed=2;stance=.4

def orient(name,delta=None,head=None):
 pb=rig.pose.bones[name];bone=rig.data.bones[name]
 inherited=pb.parent.matrix@rest[pb.parent.name].inverted()@rest[name] if pb.parent else rest[name]
 loc=Vector(head) if head is not None else inherited.translation
 rot=(delta or Quaternion((1,0,0,0)))@qrest[name]
 pb.matrix=Matrix.Translation(loc)@rot.to_matrix().to_4x4()
def solve_pose(t,bad=None):
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
 for name in ['Spine','Chest','Neck','Head']:orient(name)
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

# Qualify actual evaluated sole meshes and rigid accessory, independently of solver target output.
measure={'source_sha256':source_hash,'uniform_scale':S,'source_height_m':2/S,'physical_height_m':2,'samples':[],'checks':{}};contacts={};book_lengths=[];body_heights=[];maxbone=0;minz=1e9
for i in range(192):
 t=i/120;f=solve_pose(t);book=mesh_positions('Tome page block');book_lengths.append((book[0]-book[-1]).length)
 sample={'t':t,'feet':{}}
 for side in ['L','R']:
  points=mesh_positions('Boot sole '+side);low=min(p.z for p in points);support=[p for p in points if p.z<=low+1e-5];centre=sum(support,Vector())/len(support);world=centre+Vector((speed*t,0,0));minz=min(minz,low);sf=f[side];sample['feet'][side]={'world':list(world),'sole_min_z':low,'support':sf['support'],'cycle':sf['cycle'],'support_vertices':len(support)}
  if sf['support']:contacts.setdefault((side,sf['cycle']),[]).append(world.copy())
  for bn in ['Thigh.','Shin.']:
   pb=rig.pose.bones[bn+side];maxbone=max(maxbone,abs((pb.tail-pb.head).length-rig.data.bones[bn+side].length)*S)
 measure['samples'].append(sample)
measure['max_contact_drift_m']=max((a-b).length for points in contacts.values()for a in points for b in points);measure['min_sole_z']=minz;measure['max_bone_length_error_m']=maxbone;measure['book_landmark_relative_variation']=max(book_lengths)/min(book_lengths)-1;measure['checks']={'actual_sole_contact':measure['max_contact_drift_m']<=.02,'no_ground_penetration':minz>=-.005,'bone_lengths':maxbone<=.001,'rigid_book':measure['book_landmark_relative_variation']<=.01}
# Known-bad root speed reuses measured mesh positions, changing only the supplied root translation.
wrong={}
for s in measure['samples']:
 for side,f in s['feet'].items():
  if f['support']:wrong.setdefault((side,f['cycle']),[]).append(Vector(f['world'])+Vector((.3*s['t'],0,0)))
measure['bad_root_drift_m']=max((a-b).length for points in wrong.values()for a in points for b in points);measure['checks']['sliding_control_caught']=measure['bad_root_drift_m']>.02
measure['status']='MECHANICAL_PREFLIGHT_PASS'if all(measure['checks'].values())else'FAIL';(HERE/'evidence/authoring-v1.json').write_text(json.dumps(measure,indent=2));print('AUTHOR',json.dumps({k:v for k,v in measure.items()if k!='samples'}))
if not all(measure['checks'].values()):raise RuntimeError('Mechanical preflight failed; do not render')
scene.render.fps=120;scene.frame_start=0;scene.frame_end=96;action=bpy.data.actions.new('E05B_Walk_2mps');rig.animation_data.action=action
for i in range(97):
 scene.frame_set(i);solve_pose(i/120)
 for pb in rig.pose.bones:
  pb.keyframe_insert(data_path='location',frame=i,group=pb.name);pb.keyframe_insert(data_path='rotation_quaternion',frame=i,group=pb.name);pb.keyframe_insert(data_path='scale',frame=i,group=pb.name)
action.use_fake_user=True;scene.frame_set(0);solve_pose(0)
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'inputs/controlled-wizard-v1.blend'))
