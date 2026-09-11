from pathlib import Path
from PIL import Image
import numpy as np,json
p=Path(__file__).resolve().parent;b=p/'evidence/batch-02';o=json.loads((p.parent/'E07T/evidence/door-oracle.json').read_text());r=json.loads((b/'validation.json').read_text());by={x['name']:x for x in r['records']};rows=[];controls=[];clears=[]
def im(n):return np.array(Image.open(b/(n+'.png')).convert('RGB')).astype(int)
for c in o['records']:
 stem=f"{c['faction']}-r{c['resolution']}-t{c['time']:g}";rgb=by[stem+'-ids']['receipt']['idColors']['internal-leaf']
 for mode in ['ids','reverse']:
  a=im(stem+'-'+mode)
  for w in c['witnesses']:
   x,y=w['pixel'];e=int(abs(a[y,x]-rgb).max());rows.append({'name':stem+'-'+mode,'pixel':[x,y],'error':e,'pass':e<=2})
 if c['time']==.5:
  a=im(stem+'-ids');v=[bool(abs(a[w['pixel'][1],w['pixel'][0]]-rgb).max()>2)for w in c['clear']];clears.append({'name':stem,'count':len(v),'pass':all(v)})
 if c['time']==.25:
  a=im(stem+'-ids');z=im(stem+'-stale');closed=next(x for x in o['records']if x['faction']==c['faction']and x['resolution']==c['resolution']and x['time']==0);n=sum(abs(a[w['pixel'][1],w['pixel'][0]]-rgb).max()>2 and abs(z[w['pixel'][1],w['pixel'][0]]-rgb).max()<=2 for w in closed['witnesses']);controls.append({'name':stem,'stale_panel_pixels_detected':int(n),'pass':bool(n>=10)})
x={'rows':rows,'controls':controls,'aperture_clear':clears,'checks':{'all_panel_witnesses':all(v['pass']for v in rows),'stale_visual_detected':all(v['pass']for v in controls),'full_retraction_clear':all(v['pass']for v in clears)},'failures':sum(not v['pass']for v in rows)};(b/'pixel-validation.json').write_text(json.dumps(x,indent=2)+'\n');print({k:v for k,v in x.items()if k!='rows'})
