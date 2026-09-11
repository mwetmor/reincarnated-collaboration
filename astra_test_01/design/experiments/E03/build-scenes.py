from pathlib import Path
import json,math,hashlib
p=Path(__file__).resolve().parent
c=json.loads((p/'inputs/projection-candidates.json').read_text())[2];layout=json.loads((p/'inputs/chamber-layout.json').read_text());ann=json.loads((p/'annotations.json').read_text());t=math.radians(c['elevation_deg']);yaw=math.radians(c['yaw_deg']);f=202.5/math.tan(math.radians(c['vertical_fov_deg']/2));sy,cy=math.sin(yaw),math.cos(yaw)
def project(w,h=0):
 u,v=w;depth=sy*u+cy*v;s=f/(c['distance_m']-math.cos(t)*depth-math.sin(t)*h)
 return[(c['anchor'][0]+s*(cy*u-sy*v))*4/3,(c['anchor'][1]+s*(math.sin(t)*depth-math.cos(t)*h))*4/3]
assets={'floor':{'path':'art/floor-v1.png'},'pillar':ann['pillar'],'mage':ann['mage']}
for a in assets.values():a['sha256']=hashlib.sha256((p/a['path']).read_bytes()).hexdigest()
def item(id,w):
 a=assets[id];r=project(w);top=project(w,a['height_m']);s=(r[1]-top[1])/a['axis_height'];return{'type':'image','id':id,'asset':id,'x':r[0]-a['root'][0]*s,'y':r[1]-a['root'][1]*s,'scale':s,'root':r,'world':w}
pillar=ann['pillar']['world'];worlds={'center':[0,0],'near':[2.1940611049,2.04599508],'far':[-2.1940611049,-2.04599508],'left':[-2.04599508,2.1940611049],'right':[2.04599508,-2.1940611049],'behind':[pillar[0]-sy,pillar[1]-cy],'front':[pillar[0]+sy,pillar[1]+cy]}
scenes=[]
def add(id,w=None,overlay=False,hide=False,bg=None,bad=None):
 commands=[{'type':'rect','x':0,'y':0,'w':960,'h':640,'color':0x1c2125 if bg is None else bg}]
 if bg is None:commands.append({'type':'image','id':'floor','asset':'floor','x':8 if bad=='floor' else 0,'y':0,'scale':.625})
 nodes=[]
 if w is not None:
  if not hide:nodes.append(item('pillar',pillar))
  mage=item('mage',w)
  if bad=='root':mage['x']+=8
  nodes.append(mage);nodes.sort(key=lambda n:n['root'][1])
  if bad=='order':nodes.reverse()
  commands+=nodes
 if overlay:
  for obj in layout['surfaces']+layout['static_blocks']+layout['objects']:
   a,b,c1,d=obj['rect'];points=[project(q) for q in [(a,b),(c1,b),(c1,d),(a,d),(a,b)]];commands.append({'type':'line','points':points,'color':0x56ddd0,'width':1})
 scenes.append({'id':id,'label':id.replace('-',' '),'commands':commands,'expected_bad':bad,'world':w})
add('floor-only');add('floor-overlay',overlay=True)
for id,w in worlds.items():add(id,w)
add('prop-hidden',worlds['behind'],hide=True);add('alpha-light',[0,0],bg=0xe6dfd4);add('alpha-dark',[0,0],bg=0x101319)
add('bad-floor-shift',overlay=True,bad='floor');add('bad-root-shift',worlds['center'],bad='root');add('bad-order',worlds['behind'],bad='order')
(p/'scenes.json').write_text(json.dumps({'experiment':'E03M','size':[960,640],'assets':assets,'scenes':scenes},indent=2)+'\n');print('scenes',len(scenes))
