from pathlib import Path
import json,numpy as np
from PIL import Image
p=Path(__file__).resolve().parent/'evidence/batch-01';colors={'dark':[24,35,49],'light':[230,223,209],'blue':[20,81,163]};rows=[]
for bg,c in colors.items():
 b=np.array(Image.open(p/f'cast-036-starter-hidden-{bg}-oracle-valid.png').convert('RGB'))
 for mode in ['skin','normal-oracle','position-oracle']:
  a=np.array(Image.open(p/f'cast-036-starter-hidden-{bg}-{mode}-valid.png').convert('RGB'))
  for h,lo,hi in [(50,0,150),(150,150,500)]:
   for i in range(8):
    aa=a[lo:hi,i*300:(i+1)*300];bb=b[lo:hi,i*300:(i+1)*300];mask=np.any(aa!=c,2)|np.any(bb!=c,2);d=abs(aa.astype(int)-bb.astype(int))[mask];rows.append({'bg':bg,'mode':mode,'height':h,'heading':45*i,'mae':float(d.mean()),'fraction_gt8':float((d.max(1)>8).mean()),'pass':bool(d.mean()<=1 and(d.max(1)>8).mean()<=.02)})
s={m:{'failures':sum(not x['pass']for x in rows if x['mode']==m),'max_mae':max(x['mae']for x in rows if x['mode']==m),'max_fraction':max(x['fraction_gt8']for x in rows if x['mode']==m)}for m in ['skin','normal-oracle','position-oracle']};r={'summary':s,'checks':{'normal_only_passes':s['normal-oracle']['failures']==0,'position_only_retains_failures':s['position-oracle']['failures']==6,'skin_reproduces_six':s['skin']['failures']==6},'records':rows};(p/'cause-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(s,r['checks'])
