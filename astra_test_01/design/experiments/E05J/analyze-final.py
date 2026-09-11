from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
p=Path(__file__).resolve().parent;out=p/'evidence/batch-04';rows=[];colors={'dark':[24,35,49],'light':[230,223,209],'blue':[20,81,163]}
def load(name):return np.array(Image.open(out/(name+'.png')).convert('RGB'))
def measure(a,b,bg):
 mask=np.any(a!=bg,2)|np.any(b!=bg,2);e=abs(a.astype(int)-b.astype(int))[mask];return{'pixels':int(mask.sum()),'mae':float(e.mean()),'fraction_gt8':float((e.max(1)>8).mean()),'pass':bool(e.mean()<=1 and (e.max(1)>8).mean()<=.02)}
for pose in range(3):
 for head in ['head','hidden']:
  for bg,c in colors.items():
   a=load(f'{pose}-{head}-{bg}-skin');b=load(f'{pose}-{head}-{bg}-oracle')
   for height,y0,y1 in [(50,0,130),(150,130,460)]:
    for i in range(8):rows.append({'pose':pose,'head':head,'bg':bg,'height':height,'heading':i*45,**measure(a[y0:y1,100*i:100*(i+1)],b[y0:y1,100*i:100*(i+1)],c)})
ref=load('2-head-dark-oracle');controls={k:measure(load(k),ref,colors['dark'])for k in ['bad-shift','bad-pose']};reverse_exact=bool(np.array_equal(load('reverse'),load('2-head-dark-skin')));checks={'all288comparisons':all(x['pass']for x in rows),'bad_shift_detected':not controls['bad-shift']['pass'],'wrong_palette_detected':not controls['bad-pose']['pass'],'reverse_depth_exact':reverse_exact};report={'records':rows,'controls':controls,'checks':checks,'failures':sum(not x['pass']for x in rows),'worst_mae':max(x['mae']for x in rows),'worst_fraction':max(x['fraction_gt8']for x in rows),'thresholds':{'mae':1,'fraction_gt8':.02},'reference':'Independent Blender-evaluated world positions/normals, same adapter material policy; not Cycles lighting equivalence'};(out/'pixel-validation.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k!='records'})
sheet=Image.new('RGB',(800,1380));
for i,pose in enumerate(range(3)):sheet.paste(Image.open(out/f'{pose}-hidden-dark-skin.png'),(0,460*i))
sheet.save(out/'three-pose-contact.png')
