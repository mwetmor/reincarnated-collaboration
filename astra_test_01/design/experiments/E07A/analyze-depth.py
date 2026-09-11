from pathlib import Path
from PIL import Image
import numpy as np,json
p=Path(__file__).resolve().parent;b=p/'evidence/batch-02';more=p/'evidence/batch-03';oracle=json.loads((p.parent/'E07T/evidence/door-oracle.json').read_text());records=json.loads((b/'validation.json').read_text())['records']+json.loads((more/'completion-validation.json').read_text())['records'];by={x['name']:x for x in records};rows=[]
def image(name):
 for folder in [b,more]:
  for ext in ['.png','.webp']:
   file=folder/(name+ext)
   if file.exists():return np.array(Image.open(file).convert('RGB')).astype(int)
 raise FileNotFoundError(name)
for f in ['F01','F02']:
 for res in [1,3]:
  name=f'{f}-r{res}-pilot-depth';a=image(name+'-valid');z=image(name+'-bad');rgb=by[name+'-valid']['receipt']['idColors']['internal-leaf'];w=next(x['witnesses']for x in oracle['records']if x['faction']==f and x['resolution']==res and x['time']==0);n=sum(abs(a[v['pixel'][1],v['pixel'][0]]-rgb).max()<=2 and abs(z[v['pixel'][1],v['pixel'][0]]-rgb).max()>2 for v in w);rows.append({'faction':f,'resolution':res,'forbidden_front_pixels':int(n),'detected':bool(n>0)})
r={'records':rows,'checks':{'all_depth_controls_detected':all(x['detected']for x in rows),'complete108_unique_cases':len(by)==108},'scope':'Current pilot always-front control versus independently ray-guarded door pixels; full character-surface occlusion is not exhaustively sampled.'};(more/'pilot-depth-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
