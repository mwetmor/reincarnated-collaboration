from pathlib import Path
import json,hashlib,math,datetime
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;e=p.parent/'E02';files=['projection-candidates.json','chamber-layout.json']
for name in files:(p/'inputs'/name).write_bytes((e/'inputs'/name).read_bytes())
profiles=json.loads((p/'inputs/projection-candidates.json').read_text());layout=json.loads((p/'inputs/chamber-layout.json').read_text());c=profiles[2]
t=math.radians(c['elevation_deg']);yaw=math.radians(c['yaw_deg']);st,ct,sy,cy=math.sin(t),math.cos(t),math.sin(yaw),math.cos(yaw);f=202.5/math.tan(math.radians(c['vertical_fov_deg']/2))
def project(w,h=0):
 u,v=w;s=f/(c['distance_m']-ct*(sy*u+cy*v)-st*h)
 return ((c['anchor'][0]+s*(cy*u-sy*v))*1536/720,(c['anchor'][1]+s*(st*(sy*u+cy*v)-ct*h))*1536/720)
im=Image.new('RGB',(1536,1024),(28,33,37));draw=ImageDraw.Draw(im);mask=Image.new('L',im.size,0);md=ImageDraw.Draw(mask)
for i,s in enumerate(layout['surfaces']):
 a,b,c1,d=s['rect'];poly=[project(w) for w in [(a,b),(c1,b),(c1,d),(a,d)]];draw.polygon(poly,fill=(97,110,118) if i==0 else (117,94,68));md.polygon(poly,fill=i+1)
# Subtle geometry grid; no props, walls, shadows or lettering in the floor target.
for u in range(-5,6):draw.line([project((u,-4)),project((u,4))],fill=(137,143,142),width=2)
for v in range(-4,5):draw.line([project((-5,v)),project((5,v))],fill=(137,143,142),width=2)
im.save(p/'guides/floor-layout.png');mask.save(p/'guides/surface-labels.png')
(p/'INPUTS.json').write_text(json.dumps({'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[{'path':str(x.relative_to(p)),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in [*(p/'inputs').glob('*.json'),*(p/'guides').glob('*.png')]]},indent=2)+'\n')
