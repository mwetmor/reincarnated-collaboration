from pathlib import Path
from PIL import Image
import numpy as np,json
r=Path(__file__).parent
allrecords=[]
for batch,res in [('batch-01',1),('batch-02',3),('batch-03',1)]:
 out=r/'evidence'/batch
 if not(out/'validation.json').exists():continue
 v=json.loads((out/'validation.json').read_text());records=[]
 for bg in ['floor','dark','light','blue']:
  for t in [.6,.8,1.,1.2,1.5]:
   s=str(t).removesuffix('.0');a=np.array(Image.open(out/f'{bg}-{s}-on.png'))[:,:,:3].astype(int);b=np.array(Image.open(out/f'{bg}-{s}-off.png'))[:,:,:3].astype(int);d=abs(a-b).max(2)
   records.append({'bg':bg,'time':t,'effect_pixels_gt2':int((d>2).sum()),'viewport_fraction_gt2':float((d>2).mean()),'max_difference':int(d.max()),'coverage_pass':bool((d>2).mean()<=.1),'end_clear':bool(not d.any())if t==1.5 else None})
 markers=[]
 for name in ['socket-good','socket-bad']:
  a=np.array(Image.open(out/(name+'.png')))[:,:,:3];mask=(a[:,:,0]>220)&(a[:,:,1]<20)&(a[:,:,2]<20);yy,xx=np.where(mask);actual=[float((xx+.5).mean()),float((yy+.5).mean())];expected=[x*res for x in v[name]['release_anchor']];err=float(np.linalg.norm(np.array(actual)-expected)/res);markers.append({'case':name,'actual_physical':actual,'expected_physical':expected,'error_logical_px':err,'passes_good_tolerance':err<=.5})
 a=np.array(Image.open(out/'normal-blend.png'))[:,:,:3].astype(int);b=np.array(Image.open(out/'floor-0.8-off.png'))[:,:,:3].astype(int);dark=(b-a).max(2)>16
 result={'records':records,'socket_raster':markers,'normal_blend_darkened_pixels_gt16':int(dark.sum()),'checks':{'coverage':all(x['coverage_pass']for x in records),'final_clear':all(x['end_clear']for x in records if x['time']==1.5),'socket_good':markers[0]['passes_good_tolerance'],'socket_bad_rejected':not markers[1]['passes_good_tolerance'],'normal_blend_control_visible':bool(dark.sum()>0)}}
 (out/'pixel-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(batch,result['checks'],'max_coverage',max(x['viewport_fraction_gt2']for x in records),'socket_errors',[x['error_logical_px']for x in markers])
