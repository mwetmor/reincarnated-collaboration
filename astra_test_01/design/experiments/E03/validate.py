from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image
p=Path(__file__).resolve().parent;d=json.loads((p/'scenes.json').read_text());checks={};scope={};residuals=[]
for name,a in d['assets'].items():checks['source_hash:'+name]=hashlib.sha256((p/a['path']).read_bytes()).hexdigest()==a['sha256']
for engine in ['godot','pixi','phaser']:
 tag='phaser-v2' if engine=='phaser' else engine
 r=json.loads((p/'evidence'/f'{tag}-runtime.json').read_text());checks[engine+':complete']=len(r['cases'])==len(d['scenes']);checks[engine+':runtime_errors']=not r.get('errors',[])
 for frame,result in zip(d['scenes'],r['cases']):
  k=engine+':'+frame['id'];expected=[c for c in frame['commands'] if c['type']=='image'];actual=result['images'];checks[k+':order']= [a['id'] for a in actual]==[c['id'] for c in expected]
  err=max([max(abs(a[key]-c[key]) for key in ['x','y','scale']) for a,c in zip(actual,expected)],default=0);residuals.append(err);checks[k+':transform']=err<=.5
  im=Image.open(p/'evidence'/f'{tag}-{frame["id"]}.png');checks[k+':native_capture']=im.size==(960,640)
 def image(id):return np.array(Image.open(p/'evidence'/f'{tag}-{id}.png').convert('RGB'),dtype=int)
 for bad,good in [('bad-order','behind'),('bad-root-shift','center'),('bad-floor-shift','floor-overlay')]:
  changed=int(np.sum(np.max(np.abs(image(bad)-image(good)),axis=2)>15));checks[engine+':visible_fault:'+bad]=changed>15
 # Independent outside-silhouette probes detect ignored masks even when transforms pass.
 light=image('alpha-light');frame=next(x for x in d['scenes'] if x['id']=='alpha-light')
 for command in [x for x in frame['commands'] if x.get('id') in ['pillar','mage']]:
  for j,pt in enumerate([[50,50],[250,700]]):
   x=round(command['x']+pt[0]*command['scale']);y=round(command['y']+pt[1]*command['scale'])
   checks[engine+':mask_background:'+command['id']+str(j)]=int(np.max(np.abs(light[y,x]-[230,223,212])))<=3
 if engine!='godot':checks[engine+':ui_next']=r['ui_next']
 scope[engine]={'placement':'PASS' if all(v for k,v in checks.items() if k.startswith(engine+':')) else 'FAIL','native_alpha':'FAIL for generated pillar and mage','runtime_mask':'Requires native and enlarged visual review; not recovered alpha','performance':'NOT_PROFILED'}
# Independent reconstruction of actual actor root from renderer position/scale + annotated source root.
for engine in ['godot','pixi','phaser']:
 tag='phaser-v2' if engine=='phaser' else engine
 r=json.loads((p/'evidence'/f'{tag}-runtime.json').read_text())
 for frame,result in zip(d['scenes'],r['cases']):
  for c,a in zip([x for x in frame['commands'] if x['type']=='image'],result['images']):
   if c['id']!='mage':continue
   root=d['assets']['mage']['root'];measured=[a['x']+root[0]*a['scale'],a['y']+root[1]*a['scale']];error=math.dist(measured,c['root']);checks[engine+':root_gate:'+frame['id']]=(error>.5 if frame['expected_bad']=='root' else error<=.5)
result={'experiment':'E03/E03M','checks':checks,'passed':sum(checks.values()),'total':len(checks),'max_transform_residual_px':max(residuals),'engines':scope,'full_G3':'PENDING Matt visual target; native alpha failed, runtime-mask alternate scoped separately','mask_annotation_uncertainty_native_px':{'pillar':4*max(c['scale'] for f in d['scenes'] for c in f['commands'] if c.get('id')=='pillar'),'mage':8*max(c['scale'] for f in d['scenes'] for c in f['commands'] if c.get('id')=='mage')}}
(p/'evidence/validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2));assert all(checks.values()),[k for k,v in checks.items() if not v]
