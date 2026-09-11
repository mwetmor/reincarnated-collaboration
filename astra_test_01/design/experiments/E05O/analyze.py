from pathlib import Path
from PIL import Image
import numpy as np,json
p=Path(__file__).resolve().parent;out=p/'evidence/batch-03';records=[];colors={'dark':[24,35,49],'light':[230,223,209],'blue':[20,81,163]}
def measure(a,b,bg):
 mask=np.any(a!=bg,axis=2)|np.any(b!=bg,axis=2);e=abs(a.astype(int)-b.astype(int))[mask];return{'occupied_pixels':int(mask.sum()),'mae':float(e.mean()),'fraction_gt8':float((e.max(1)>8).mean()),'pass':bool(e.mean()<=1 and (e.max(1)>8).mean()<=.02)}
for method in ['partition-native','over-native','over-direct']:
 for head in ['head','hidden']:
  for bg,c in colors.items():
   a=np.array(Image.open(out/f'{head}-{bg}-{method}.png').convert('RGB'));b=np.array(Image.open(out/f'{head}-{bg}-reference.png').convert('RGB'))
   for row,(height,y0,y1)in enumerate([(50,0,130),(150,130,460)]):
    for i in range(8):records.append({'method':method,'head':head,'background':bg,'height':height,'heading':i*45,**measure(a[y0:y1,i*100:(i+1)*100],b[y0:y1,i*100:(i+1)*100],c)})
b=np.array(Image.open(out/'head-dark-reference.png').convert('RGB'));bad={}
for name in ['bad-shift','bad-mask']:
 a=np.array(Image.open(out/f'{name}.png').convert('RGB'));bad[name]=measure(a,b,colors['dark']);bad[name]['detected']=not bad[name]['pass']
summaries={method:{'cases':96,'failures':sum(not r['pass']for r in records if r['method']==method),'worst_mae':max(r['mae']for r in records if r['method']==method),'worst_fraction':max(r['fraction_gt8']for r in records if r['method']==method)}for method in ['partition-native','over-native','over-direct']}
r={'records':records,'summaries':summaries,'controls':bad,'checks':{'partition_all96':summaries['partition-native']['failures']==0,'over_native_all96':summaries['over-native']['failures']==0,'bad_shift_detected':bad['bad-shift']['detected'],'bad_mask_detected':bad['bad-mask']['detected']},'thresholds':{'mae':1,'fraction_gt8':.02},'mask':'Actual GPU foreground union; no background padding','scope':'Eight idle directions,2head states,3backgrounds,2scales; no motion or lighting qualification'}
(out/'pixel-validation.json').write_text(json.dumps(r,indent=2)+'\n');print({'summaries':summaries,'controls':bad,'checks':r['checks']})
