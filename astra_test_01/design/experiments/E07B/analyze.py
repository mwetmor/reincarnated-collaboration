from pathlib import Path
from PIL import Image
import numpy as np,json,sys
p=Path(__file__).resolve().parent;resolution=int(sys.argv[1] if len(sys.argv)>1 else 1);out=p/f'evidence/batch-0{2 if resolution==1 else 3}';oracle=json.loads((p/'evidence/shadow-oracle.json').read_text());capture=json.loads((out/'validation.json').read_text());completion=json.loads((out/'validation-completion.json').read_text())if(out/'validation-completion.json').exists()else {'records':[]};records=[r for r in capture['records']if r.get('capture',{}).get('rgba_lossless_verified')]+completion['records'];names={r['case']['name'] for r in records};assert len(records)==40 and len({r['name']for r in records})==40;rows=[];controls=[];material=[]
def im(name):return np.array(Image.open(out/(name+'.webp')).convert('RGB')).astype(int)
for c in oracle['records']:
 if c['resolution']!=resolution or c['name'] not in names:continue
 n=c['name'];a=im(n+'-diagnostic');positive=[];negative=[]
 for w in c['witnesses']:
  x,y=w['pixel'];expected=[0,255,0] if w['shadow'] else [0,0,0];error=int(abs(a[y,x]-expected).max());rows.append({'name':n,'pixel':[x,y],'shadow':w['shadow'],'actual_rgb':a[y,x].tolist(),'error':error,'pass':error<=2});(positive if w['shadow'] else negative).append((x,y))
 for label in ['bad-missing','bad-stale']:
  b=im(n+'-'+label);failures=sum(abs(b[y,x]-[0,255,0]).max()>2 for x,y in positive);controls.append({'name':n,'control':label,'positive_failures':int(failures),'pass':bool(failures>0)})
 on,off=im(n+'-on'),im(n+'-off');delta=np.array([off[y,x]-on[y,x] for x,y in positive]);unchanged=np.array([off[y,x]-on[y,x] for x,y in negative]);material.append({'name':n,'mean_shadow_darkening':delta.mean(0).tolist(),'min_shadow_darkening':int(delta.min()),'max_lit_difference':int(abs(unchanged).max()),'pass':bool(delta.mean()>1 and delta.min()>=0 and abs(unchanged).max()<=2)})
r={'resolution':resolution,'rows':rows,'controls':controls,'material':material,'checks':{'shadow_lit_witnesses':all(x['pass'] for x in rows),'missing_stale_controls':all(x['pass'] for x in controls),'material_response':all(x['pass'] for x in material)}};(out/'pixel-validation.json').write_text(json.dumps(r,indent=2)+'\n');print({'checks':r['checks'],'witnesses':len(rows),'failures':sum(not x['pass'] for x in rows),'controls':controls,'material':material})
