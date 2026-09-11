from pathlib import Path
from PIL import Image
import numpy as np,json
p=Path(__file__).resolve().parent/'evidence/batch-01';rows=[]
for i in range(48):
 a=np.array(Image.open(p/f'original-{i}.png')).astype(int);b=np.array(Image.open(p/f'atlas-{i}.png')).astype(int);delta=abs(a-b);changed=np.any(delta!=0,axis=2);rows.append({'frame':i,'max_channel_delta':int(delta.max()),'changed_fraction':float(changed.mean()),'pass':bool(delta.max()<=2 and changed.mean()<=.01)})
a=np.array(Image.open(p/'original-0.png')).astype(int);b=np.array(Image.open(p/'bad-pivot.png')).astype(int);d=abs(a-b);r={'frames':rows,'all_pass':all(x['pass']for x in rows),'bad_pivot':{'max_channel_delta':int(d.max()),'changed_fraction':float(np.any(d!=0,axis=2).mean()),'caught':bool(d.max()>2 or np.any(d!=0,axis=2).mean()>.01)},'threshold':{'max_channel_delta':2,'max_changed_fraction':.01}}
(p/'comparison.json').write_text(json.dumps(r,indent=2));print(json.dumps({'all_pass':r['all_pass'],'failed':[x for x in rows if not x['pass']],'worst_delta':max(x['max_channel_delta']for x in rows),'worst_fraction':max(x['changed_fraction']for x in rows),'bad':r['bad_pivot']}))
