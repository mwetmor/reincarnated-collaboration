from pathlib import Path
from PIL import Image
import numpy as np,json
p=Path(__file__).resolve().parent;b=p/'evidence/batch-01';records=json.loads((b/'validation.json').read_text())['records'];rows=[]
def image(name):return np.array(Image.open(b/(name+('.png' if (b/(name+'.png')).exists() else '.webp'))).convert('RGB')).astype(int)
def measure(a,c):
 m=np.any(a!=[48,57,64],2)|np.any(c!=[48,57,64],2);e=abs(a-c)[m];return {'pixels':int(m.sum()),'mae':float(e.mean())if e.size else None,'fraction_gt8':float((e.max(1)>8).mean())if e.size else None,'pass':bool(e.size and e.mean()<=1 and (e.max(1)>8).mean()<=.02)}
for row in records:
 if row.get('sourceMode')!='skin':continue
 ref=row['name'][:-4]+'oracle';rows.append({**row,**measure(image(row['name']),image(ref))})
controls=[]
for res in [1,3]:
 for bad in ['shift','wrong-pose','normals']:controls.append({'resolution':res,'bad':bad,**measure(image(f'r{res}-control-{bad}'),image(f'r{res}-x3.4-p180-h135-advanced-head-warm-oracle'))})
r={'records':rows,'controls':controls,'checks':{'all864_comparisons':len(rows)==864 and all(x['pass']for x in rows),'nonempty':all(x['pixels']>100 for x in rows),'shift_wrong_pose_detected':all(not x['pass']for x in controls if x['bad']!='normals')},'normal_ablation_detected':all(not x['pass']for x in controls if x['bad']=='normals'),'failures':sum(not x['pass']for x in rows),'worst_mae':max(x['mae']for x in rows),'worst_fraction':max(x['fraction_gt8']for x in rows)};(b/'pixel-validation.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items()if k!='records'})
