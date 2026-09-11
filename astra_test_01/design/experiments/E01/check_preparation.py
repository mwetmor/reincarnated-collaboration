"""Independent logical-layout checks; no runtime or visual acceptance implied."""
from pathlib import Path
from collections import deque
import json,math
import numpy as np
P=Path(__file__).resolve().parent
layout=json.loads((P/'chamber-layout.draft.json').read_text())
profiles=json.loads((P/'projection-candidates.json').read_text())
checks=[]
def check(name,ok,detail):
 checks.append(dict(name=name,pass_=bool(ok),detail=detail))
def solids(opened,extra=None):
 result={b['id']:b['rect'] for b in layout['static_blocks']}
 result.update({b['id']:b['rect'] for b in layout['objects'] if b['id']!='door' or not opened})
 if extra:result.update(extra)
 return result

def hit(a,b,rect,r):
 # Slab interval intersection against conservative Minkowski AABB expansion.
 lo=[rect[0]-r,rect[1]-r];hi=[rect[2]+r,rect[3]+r];t0,t1=0.,1.
 for i in (0,1):
  d=b[i]-a[i]
  if abs(d)<1e-12:
   if a[i]<lo[i] or a[i]>hi[i]:return False
  else:
   e,f=sorted(((lo[i]-a[i])/d,(hi[i]-a[i])/d));t0=max(t0,e);t1=min(t1,f)
   if t0>t1:return False
 return True

def route(start,end,r,opened):
 rects=solids(opened);bounds=layout['bounds'];step=.25
 def free(a,b):
  if not(bounds[0]+r<=b[0]<=bounds[2]-r and bounds[1]+r<=b[1]<=bounds[3]-r):return False
  return not any(hit(a,b,rect,r) for rect in rects.values())
 start=tuple(round(x/step) for x in start);end=tuple(round(x/step) for x in end)
 world=lambda p:tuple(x*step for x in p)
 if not free(world(start),world(start)) or not free(world(end),world(end)):return None
 q=deque([start]);prev={start:None}
 while q:
  a=q.popleft()
  if a==end:
   out=[]
   while a is not None:out.append(world(a));a=prev[a]
   return out[::-1]
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   b=(a[0]+dx,a[1]+dy)
   if b not in prev and free(world(a),world(b)):prev[b]=a;q.append(b)
 return None
for r in [.35,.65]:
 left=(-4.25,0);right=(4.25,0)
 check(f'closed door forbids east, r={r}',route(left,right,r,False) is None,'Partition reaches room bounds; no route around it.')
 path=route(left,right,r,True)
 check(f'open door permits east, r={r}',path is not None,{'nodes':len(path) if path else 0})
 for obj in layout['objects']:
  for approach in obj['approaches']:
   check(f'open approach {obj["id"]} {approach}, r={r}',route(left,approach,r,True) is not None,'From west exit approach; grid-snapped declared point.')
 check(f'bad straight route caught, r={r}',hit((1,2),(3,2),layout['static_blocks'][1]['rect'],r),'Endpoints alone are insufficient; segment crosses partition.')
s=solids(True,{'overlap-crate':layout['static_blocks'][2]['rect']});del s['overlap-crate']
check('blocker ownership survives removal','pillar' in s and hit((-2,-1.5),(-2,-1.5),s['pillar'],.35),'Removing coincident dynamic owner leaves static pillar.')
for p in profiles:
 t=math.radians(p['elevation_deg']);y=math.radians(p['yaw_deg']);st,ct=math.sin(t),math.cos(t);sy,cy=math.sin(y),math.cos(y)
 anchor=np.array(p['anchor']);persp=p['type']=='pinhole'
 # Independent homogeneous matrix representation; solve inverse by matrix inversion.
 if persp:
  f=p['screen'][1]/2/math.tan(math.radians(p['vertical_fov_deg'])/2);d=p['distance_m']
  m=np.array([[f*cy,-f*sy,0],[f*st*sy,f*st*cy,0],[-ct*sy,-ct*cy,d]])
 else:
  f=p['uniform_scale_px_per_m'];m=np.array([[f*cy,-f*sy,0],[f*st*sy,f*st*cy,0],[0,0,1]])
 inv=np.linalg.inv(m);errors=[];bad=[]
 for u in np.linspace(-5,5,11):
  for v in np.linspace(-4,4,9):
   a=m@np.array([u,v,1]);xy=a[:2]/a[2];b=inv@np.r_[xy,1];uv=b[:2]/b[2];errors.append(float(np.linalg.norm(uv-[u,v])));bad.append(float(np.linalg.norm(uv+[.25,0]-[u,v])))
 check(p['id']+' ground roundtrip',max(errors)<1e-9,{'points':99,'max_m':max(errors)})
 check(p['id']+' shifted inverse rejected',min(bad)>1e-9,{'min_m':min(bad)})
 a=m@np.array([0,0,1]);check(p['id']+' projected origin',float(np.linalg.norm(a[:2]/a[2]))<1e-9,'Origin maps to separately applied registered screen anchor.')
result={'scope':'G2 independent preparation only; no runtime/art pass','checks':checks,'all_pass':all(c['pass_'] for c in checks)}
(P/'preparation-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['all_pass']
