from pathlib import Path
from PIL import Image
import numpy as np,json
p=Path(__file__).resolve().parent;b=p/'evidence/batch-02';old=p.parent/'E07T/evidence/batch-01';rows=[]
for f in sorted(b.glob('*.png')):
 a=np.array(Image.open(f).convert('RGB')).astype(int);c=np.array(Image.open(old/f.name).convert('RGB')).astype(int);d=abs(a-c);rows.append({'name':f.name,'pixels_above2':int((d.max(2)>2).sum()),'maximum_channel_error':int(d.max()),'mae':float(d.mean()),'pass':bool(d.max()<=2)})
r={'records':rows,'checks':{'all64_images':len(rows)==64,'all_pixels_within2':all(x['pass']for x in rows)},'failures':sum(not x['pass']for x in rows)};(b/'source-comparison.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items()if k!='records'});print([x for x in rows if not x['pass']])
