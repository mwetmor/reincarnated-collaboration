from pathlib import Path
from PIL import Image
import numpy as np,json,sys
p=Path(__file__).resolve().parent;resolution=int(sys.argv[1] if len(sys.argv)>1 else 1);out=p/f'evidence/batch-0{1 if resolution==1 else 2}';oracle=json.loads((p/'evidence/door-oracle.json').read_text());r=json.loads((out/'validation.json').read_text());by={x['name']:x for x in r['records']};rows=[];bad=[];lights=[]
def image(name):return np.array(Image.open(out/(name+'.png')).convert('RGB')).astype(int)
for c in oracle['records']:
 if c['resolution']!=resolution:continue
 f=c['faction'];color=by[f+'-closed-ids']['receipt']['idColors']['internal-leaf']
 for label in ['closed-ids','closed-reverse','closing-ids']:
  im=image(f+'-'+label)
  for w in c['witnesses']:
   x,y=w['pixel'];err=int(abs(im[y,x]-color).max());rows.append({'name':f+'-'+label,'pixel':[x,y],'expected_rgb':color,'actual_rgb':im[y,x].tolist(),'error':err,'pass':err<=2})
 opened=image(f+'-open-ids');stale=image(f+'-open-bad-stale');open_changes=sum(abs(opened[w['pixel'][1],w['pixel'][0]]-color).max()>2 for w in c['witnesses']);stale_closed=sum(abs(stale[w['pixel'][1],w['pixel'][0]]-color).max()<=2 for w in c['witnesses']);bad.append({'faction':f,'open_witnesses_changed':int(open_changes),'stale_closed_witnesses':int(stale_closed),'pass':bool(open_changes==len(c['witnesses']) and stale_closed==len(c['witnesses']))})
 if resolution==1:
  mage=by[f+'-closed-ids']['receipt']['idColors']['mage'];mask=(abs(image(f+'-closed-ids')-mage).max(2)<=2)&(abs(opened-mage).max(2)<=2);stable=mask.copy()
  for dx in [-1,0,1]:
   for dy in [-1,0,1]:stable&=np.roll(mask,(dy,dx),(0,1))
  samples={d+'-'+l:image(f+'-'+d+'-'+l)[stable] for d in ['closed','open'] for l in ['neutral','warm','cool']};bad_light=image(f+'-closed-bad-light')[stable];checks={'enough_visible_pilot_pixels':bool(stable.sum()>=6),'closed_warm_equal_neutral':bool(np.array_equal(samples['closed-warm'],samples['closed-neutral'])),'closed_cool_equal_neutral':bool(np.array_equal(samples['closed-cool'],samples['closed-neutral'])),'open_warm_changes':bool(np.mean(abs(samples['open-warm']-samples['open-neutral']))>.5),'open_cool_changes':bool(np.mean(abs(samples['open-cool']-samples['open-neutral']))>.5),'ignore_leaf_detected':bool(np.mean(abs(bad_light-samples['closed-warm']))>.5)};lights.append({'faction':f,'stable_pixels':int(stable.sum()),'means':{k:v.mean(0).tolist() for k,v in samples.items()},'checks':checks})
s={'resolution':resolution,'rows':rows,'stale_visual_controls':bad,'lighting':lights,'checks':{'all_closed_leaf_witnesses':all(x['pass'] for x in rows),'open_and_stale_controls':all(x['pass'] for x in bad),'light_controls':all(all(x['checks'].values()) for x in lights)}};(out/'pixel-validation.json').write_text(json.dumps(s,indent=2)+'\n');print({'checks':s['checks'],'witnesses':len(rows),'failures':sum(not x['pass'] for x in rows),'controls':bad,'lighting':lights})
