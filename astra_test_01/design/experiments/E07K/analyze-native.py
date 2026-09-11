from pathlib import Path
from PIL import Image
import numpy as np,json
p=Path(__file__).resolve().parent;out=p/'evidence/batch-01';oracle=json.loads((p/'evidence/occlusion-oracle.json').read_text());capture=json.loads((out/'validation.json').read_text());byname={r['name']:r for r in capture['records']};rows=[];bad=[];lights=[]
def image(name):return np.array(Image.open(out/(name+'.png')).convert('RGB')).astype(int)
for case in oracle['records']:
 if case['resolution']!=1:continue
 f=case['faction'];pos=case['position_name'];base=f+'-'+pos;names=[base+'-ids',base+'-reverse']if pos!='lamp'else[f+'-lamp-open-ids']
 for name in names:
  colors=byname[name]['receipt']['idColors'];im=image(name)
  for w in case['witnesses']:
   x,y=w['pixel'];actual=im[y,x];expected=colors[w['expected']];error=int(abs(actual-expected).max());rows.append({'name':name,'pixel':[x,y],'expected_id':w['expected'],'actual_rgb':actual.tolist(),'expected_rgb':expected,'error':error,'pass':error<=2})
 if pos=='behind':
  name=base+'-bad-depth';im=image(name);colors=byname[name]['receipt']['idColors'];failures=sum(abs(im[w['pixel'][1],w['pixel'][0]]-colors[w['expected']]).max()>2 for w in case['witnesses']);bad.append({'faction':f,'witnesses':len(case['witnesses']),'failures':int(failures),'detected':bool(failures>0)})
for faction in ['F01','F02']:
 name=faction+'-lamp-open-ids';im=image(name);color=byname[name]['receipt']['idColors']['mage'];mask=abs(im-color).max(2)<=2
 # Keep every3x3neighbor inside opaque pilot ID to exclude silhouette blending.
 stable=mask.copy()
 for dy in [-1,0,1]:
  for dx in[-1,0,1]:stable &= np.roll(mask,(dy,dx),(0,1))
 means={};samples={}
 for door in ['open','closed']:
  for light in ['neutral','warm','cool']:
   a=image(f'{faction}-lamp-{door}-{light}')[stable];means[door+'-'+light]=a.mean(0).tolist();samples[door+'-'+light]=a
 badlight=image(f'{faction}-lamp-closed-bad-light')[stable]
 checks={'closed_warm_equals_neutral':bool(np.array_equal(samples['closed-warm'],samples['closed-neutral'])),'closed_cool_equals_neutral':bool(np.array_equal(samples['closed-cool'],samples['closed-neutral'])),'open_warm_red_increase':bool(np.mean(samples['open-warm'][:,0]-samples['open-neutral'][:,0])>2),'open_cool_blue_increase':bool(np.mean(samples['open-cool'][:,2]-samples['open-neutral'][:,2])>2),'ignored_closed_leaf_detected':bool(np.mean(abs(badlight-samples['closed-warm']))>2)};lights.append({'faction':faction,'stable_pilot_pixels':int(stable.sum()),'mean_rgb':means,'checks':checks})
r={'witnesses':rows,'negative_depth':bad,'lighting':lights,'checks':{'all_native_witnesses':all(x['pass']for x in rows),'both_bad_depth_detected':all(x['detected']for x in bad),'all_pilot_light_controls':all(all(x['checks'].values())for x in lights)},'scope':'Pilot opaque geometry and shared point-light controls; no NPC/monster/VFX depth or pilot-cast floor shadows'};(out/'pixel-validation.json').write_text(json.dumps(r,indent=2)+'\n');print({'checks':r['checks'],'witness_count':len(rows),'failures':sum(not x['pass']for x in rows),'lighting':lights,'bad':bad})
