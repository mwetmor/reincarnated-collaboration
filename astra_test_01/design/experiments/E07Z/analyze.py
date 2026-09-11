from pathlib import Path
from PIL import Image
import numpy as np,json
r=Path(__file__).parent;out=r/'evidence/batch-02';v=json.loads((out/'validation.json').read_text());oracle=json.loads((r/'evidence/part-oracle.json').read_text());records=[]
for rec in v['records']:
 if not rec['name'].endswith('-ids'):continue
 a=np.array(Image.open(out/(rec['name']+'.png'))).astype(int);rows=[]
 for w in oracle['witnesses']:
  x,y=w['pixel'];actual=a[y,x,:3];expected=rec['idColors'][w['part']];error=int(np.max(abs(actual-np.array(expected))));rows.append({'part':w['part'],'pixel':w['pixel'],'actual_rgb':actual.tolist(),'expected_rgb':expected,'error':error,'pass':error<=2})
 records.append({'name':rec['name'],'rows':rows,'passing':sum(x['pass']for x in rows),'total':len(rows)})
by={x['name']:x for x in records};checks={'depth_forward_matches_source':by['depth-forward-ids']['passing']==len(oracle['witnesses']),'depth_reverse_matches_source':by['depth-reverse-ids']['passing']==len(oracle['witnesses']),'bad_painter_forward_caught':by['painter-forward-ids']['passing']<len(oracle['witnesses']),'bad_painter_reverse_caught':by['painter-reverse-ids']['passing']<len(oracle['witnesses'])};(out/'pixel-validation.json').write_text(json.dumps({'records':records,'checks':checks},indent=2)+'\n');print(checks,[(x['name'],x['passing'],x['total'])for x in records])
