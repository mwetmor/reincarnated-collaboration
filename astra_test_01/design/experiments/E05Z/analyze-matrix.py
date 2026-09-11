from pathlib import Path
from PIL import Image
import numpy as np,json
p=Path(__file__).resolve().parent;out=p/'evidence/batch-01';a=json.loads((p/'character.asset.json').read_text());colors={'dark':[24,35,49],'light':[230,223,209],'blue':[20,81,163]};rows=[]
def load(n):return np.array(Image.open(out/(n+'.png')).convert('RGB'))
def measure(a,b,c):
 mask=np.any(a!=c,2)|np.any(b!=c,2);err=abs(a.astype(int)-b.astype(int))[mask];return{'pixels':int(mask.sum()),'mae':float(err.mean()),'fraction_gt8':float((err.max(1)>8).mean()),'pass':bool(err.mean()<=1 and (err.max(1)>8).mean()<=.02)}
for pose in [x['id']for x in a['poses']if x.get('oracle')]:
 for outfit,heads in [('starter',['hidden']),('advanced',['head','hidden'])]:
  for head in heads:
   for bg,color in colors.items():
    a,b=load(f'{pose}-{outfit}-{head}-{bg}-skin-valid'),load(f'{pose}-{outfit}-{head}-{bg}-oracle-valid')
    for height,y0,y1 in [(50,0,150),(150,150,500)]:
     for i in range(8):rows.append({'pose':pose,'outfit':outfit,'head':head,'bg':bg,'height':height,'heading':45*i,**measure(a[y0:y1,i*300:(i+1)*300],b[y0:y1,i*300:(i+1)*300],color)})
controls={bad:measure(load('walk-012-advanced-head-dark-skin-'+bad),load('walk-012-advanced-head-dark-oracle-valid'),colors['dark'])for bad in ['shift','wrong-pose']};r={'records':rows,'controls':controls,'checks':{'all576comparisons':len(rows)==576 and all(x['pass']for x in rows),'bad_controls_detected':all(not x['pass']for x in controls.values())},'failures':sum(not x['pass']for x in rows),'worst_mae':max(x['mae']for x in rows),'worst_fraction':max(x['fraction_gt8']for x in rows),'reference':'Independent Blender-evaluated positions/normals under identical diagnostic Pixi diffuse policy. No Cycles lighting equivalence or complete motion/gear surface art pass.'};(out/'pixel-validation.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items()if k!='records'})
