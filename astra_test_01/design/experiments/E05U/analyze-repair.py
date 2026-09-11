from pathlib import Path
from PIL import Image
import numpy as np,json
p=Path(__file__).resolve().parent;out=p/'evidence/batch-03';colors={'dark':[24,35,49],'light':[230,223,209],'blue':[20,81,163]};rows=[]
def load(n):return np.array(Image.open(out/(n+'.png')).convert('RGB'))
def measure(a,b,c):
 mask=np.any(a!=c,2)|np.any(b!=c,2);err=abs(a.astype(int)-b.astype(int))[mask];return{'pixels':int(mask.sum()),'mae':float(err.mean()),'fraction_gt8':float((err.max(1)>8).mean()),'pass':bool(err.mean()<=1 and (err.max(1)>8).mean()<=.02)}
for outfit,heads in [('starter',['hidden']),('advanced',['head','hidden'])]:
 for head in heads:
  for bg,color in colors.items():
   a,b=load(f'{outfit}-{head}-{bg}-skin'),load(f'{outfit}-{head}-{bg}-oracle')
   for height,y0,y1 in [(50,0,130),(150,130,460)]:
    for i in range(8):rows.append({'outfit':outfit,'head':head,'bg':bg,'height':height,'heading':45*i,**measure(a[y0:y1,i*200:(i+1)*200],b[y0:y1,i*200:(i+1)*200],color)})
bad=measure(load('bad-shift'),load('advanced-head-dark-oracle'),colors['dark']);r={'records':rows,'bad_attachment':bad,'checks':{'all144comparisons':all(x['pass']for x in rows),'bad_attachment_detected':not bad['pass']},'failures':sum(not x['pass']for x in rows),'worst_mae':max(x['mae']for x in rows),'worst_fraction':max(x['fraction_gt8']for x in rows),'reference':'Independent Blender-evaluated positions/normals under identical diagnostic Pixi diffuse policy. No Cycles lighting equivalence or full art pass.'};(out/'pixel-validation.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items()if k!='records'})
