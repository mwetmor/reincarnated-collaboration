from pathlib import Path
from PIL import Image
import numpy as np,json,math
r=Path(__file__).parent
def load_image(p):
 return Image.open(p if p.exists()else p.with_suffix('.webp'))
for batch in ['batch-01','batch-02','batch-03']:
 out=r/'evidence'/batch
 if not(out/'validation.json').exists():continue
 v=json.loads((out/'validation.json').read_text());rows=[];lights=[]
 if not any(x.get('name','').endswith('-ids')for x in v['records']):continue
 for rec in v['records']:
  if not rec['name'].endswith('-ids'):continue
  a=np.array(load_image(out/(rec['name']+'.png')))[:,:,:3]
  for w in rec['witnesses']:
   p=[x*rec['resolution']for x in w['adapter_pixel']];actual=a[int(p[1]),int(p[0])].astype(int);expected=rec['idColors'][w['first_object']];error=int(abs(actual-np.array(expected)).max());rows.append({'case':rec['name'],'witness':w['id'],'expected_object':w['first_object'],'actual_rgb':actual.tolist(),'expected_rgb':expected,'error':error,'pass':error<=2})
 for f in ['F01','F02']:
  records={x['name']:x for x in v['records']};p=records[f+'-open-warm']['receiver']['screen'];res=records[f+'-open-warm']['resolution'];x,y=[int(z*res)for z in p]
  samples={state+'-'+mode:np.array(load_image(out/(f+'-'+state+'-'+mode+'.png')))[y,x,:3].astype(int).tolist()for state in ['open','closed']for mode in ['neutral','warm','cool']}
  lights.append({'faction':f,'point':[3,0,0],'samples':samples,'closed_blocks':samples['closed-warm']==samples['closed-neutral'] and samples['closed-cool']==samples['closed-neutral'],'open_changes':samples['open-warm']!=samples['open-neutral'] and samples['open-cool']!=samples['open-neutral']})
 record=next(x for x in v['records']if x['name']=='F01-closed-ids');a=np.array(load_image(out/'F01-closed-ids.png'))[:,:,:3];bad=np.array(load_image(out/'bad-order.png'))[:,:,:3];w=next(w for w in record['witnesses']if w['id']=='near-interior');p=[int(x*record['resolution'])for x in w['adapter_pixel']];bad_order=bool(np.any(a[p[1],p[0]]!=bad[p[1],p[0]]))
 b=np.array(load_image(out/'bad-ignore-leaf.png'))[:,:,:3];good=np.array(load_image(out/'F01-closed-warm.png'))[:,:,:3];p=[int(x*record['resolution'])for x in record['receiver']['screen']];bad_light=bool(np.any(b[p[1],p[0]]!=good[p[1],p[0]]))
 c=record['idColors']['east-leaf'];goodmask=np.max(abs(a.astype(int)-c),2)<=2;shift=np.array(load_image(out/'bad-shift.png'))[:,:,:3];badmask=np.max(abs(shift.astype(int)-c),2)<=2;gy,gx=np.where(goodmask);by,bx=np.where(badmask);shift_centroid=math.hypot(gx.mean()-bx.mean(),gy.mean()-by.mean())/record['resolution']*1.6
 result={'geometry_witnesses':rows,'lights':lights,'bad_shift_centroid_source_px':shift_centroid,'controls':{'bad_order_detected':bad_order,'ignore_leaf_detected':bad_light,'shift_detected':bool(shift_centroid>3)},'checks':{'source_gpu_occlusion':all(x['pass']for x in rows),'closed_light':all(x['closed_blocks']for x in lights),'open_light':all(x['open_changes']for x in lights),'bad_order':bad_order,'bad_light':bad_light,'bad_shift':bool(shift_centroid>3)}}
 (out/'pixel-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(batch,result['checks'],'shift_centroid',shift_centroid,'lights',lights)
