import bpy,json,hashlib,sys
from pathlib import Path
from array import array
p=Path(__file__).resolve().parent;rig=bpy.data.objects['WizardRig'];checks={}
for packet,clips in [('E05N',[('idle',96),('walk',48),('cast',72)]),('E05I',[('turn_left',36),('turn_right',36)])]:
 data=[]
 for clip,count in clips:
  rig.animation_data.action=bpy.data.actions['E05M_'+clip]
  for frame in range(count):
   bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();matrices=[rig.matrix_world@rig.pose.bones[b.name].matrix@b.matrix_local.inverted()for b in rig.data.bones]+[rig.matrix_world.copy()];data.extend(m[r][c]for m in matrices for c in range(4)for r in range(4))
 a=array('f',data)
 if sys.byteorder!='little':a.byteswap()
 raw=(p.parent/packet/'assets/palettes.bin').read_bytes();checks[packet]={'exact':a.tobytes()==raw,'sha256':hashlib.sha256(a.tobytes()).hexdigest(),'bytes':len(raw)}
(p/'evidence/inherited-validation.json').write_text(json.dumps({'checks':checks},indent=2)+'\n');print(checks);assert all(x['exact']for x in checks.values())
