import bpy,json,hashlib,sys
from pathlib import Path
from array import array
p=Path(__file__).resolve().parent;rig=bpy.data.objects['WizardRig'];data=[]
for clip,count in [('idle',96),('walk',48),('cast',72)]:
 rig.animation_data.action=bpy.data.actions['E05M_'+clip]
 for frame in range(count):
  bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();matrices=[rig.matrix_world@rig.pose.bones[b.name].matrix@b.matrix_local.inverted()for b in rig.data.bones]+[rig.matrix_world.copy()];data.extend(m[r][c]for m in matrices for c in range(4)for r in range(4))
a=array('f',data)
if sys.byteorder!='little':a.byteswap()
source=(p.parent/'E05N/assets/palettes.bin').read_bytes();r={'inherited216palettes_exact':a.tobytes()==source,'sha256':hashlib.sha256(a.tobytes()).hexdigest(),'bytes':len(source)};(p/'evidence/inherited-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r);assert r['inherited216palettes_exact']
