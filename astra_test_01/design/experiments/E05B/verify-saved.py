import bpy,json,math
from pathlib import Path
from mathutils import Vector
HERE=Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E05B');scene=bpy.context.scene;rig=bpy.data.objects['WizardRig'];groups={};r={'checks':{},'samples':[]};book=[]
def points(name):
 obj=bpy.data.objects[name].evaluated_get(bpy.context.evaluated_depsgraph_get());m=obj.to_mesh();p=[obj.matrix_world@v.co for v in m.vertices];obj.to_mesh_clear();return p
for i in range(96):
 scene.frame_set(i);bpy.context.view_layer.update();t=i/120
 b=points('Tome page block');book.append((b[0]-b[-1]).length);sample={'t':t,'feet':{}}
 for side,offset in [('L',0),('R',.4)]:
  p=points('Boot sole '+side);z=min(v.z for v in p);support=[v for v in p if v.z<=z+1e-5];centre=sum(support,Vector())/len(support)+Vector((2*t,0,0));phase=(t+offset)%.8;stance=phase<.4;sample['feet'][side]={'world':list(centre),'stance':stance,'min_z':z}
  if stance:groups.setdefault((side,math.floor((t+offset)/.8)),[]).append(centre)
 r['samples'].append(sample)
r['max_saved_contact_drift_m']=max((a-b).length for ps in groups.values()for a in ps for b in ps);r['checks']['saved_mesh_contact']=r['max_saved_contact_drift_m']<=.02;r['checks']['saved_no_penetration']=min(f['min_z']for s in r['samples']for f in s['feet'].values())>=-.005;r['checks']['saved_rigid_book']=max(book)/min(book)-1<=.01
scene.frame_set(0);bpy.context.view_layer.update();base=points('Tome page block');dist=(base[0]-base[-1]).length;obj=bpy.data.objects['Tome page block'];old=obj.scale.copy();obj.scale*=1.2;bpy.context.view_layer.update();bad=points(obj.name);r['bad_book_relative_change']=(bad[0]-bad[-1]).length/dist-1;r['checks']['bag_swell_control_caught']=r['bad_book_relative_change']>.01;obj.scale=old
# Measured lead geometry must alternate in the actual saved clips, not only phase metadata.
f0=r['samples'][12]['feet'];f1=r['samples'][60]['feet'];d0=f0['L']['world'][0]-f0['R']['world'][0];d1=f1['L']['world'][0]-f1['R']['world'][0];r['checks']['saved_opposite_leads']=d0*d1<0;r['checks']['repeated_lead_control_caught']=not(d0*d0<0)
r['status']='PASS'if all(r['checks'].values())else'FAIL';(HERE/'evidence/saved-action-validation.json').write_text(json.dumps(r,indent=2));print('SAVED_ACTION',json.dumps({k:v for k,v in r.items()if k!='samples'}))
