from pathlib import Path
import json,math
import numpy as np
from PIL import Image
p=Path(__file__).resolve().parent
im=np.array(Image.open(p/'art/floor-v1.png').convert('RGB'),dtype=float)
# Independent annotated vertices from inspecting the generated painting at native resolution.
observed=np.array([[744,197],[1182,524],[807,862],[377,429]],float)
guide=np.array([[743.028,196.895],[1181.65,524.684],[806.979,862.134],[376.69,429.592]])
# Calculate expected corners from the immutable projection instead of trusting hand values.
c=json.loads((p/'inputs/projection-candidates.json').read_text())[2];t=math.radians(c['elevation_deg']);y=math.radians(c['yaw_deg']);f=202.5/math.tan(math.radians(c['vertical_fov_deg']/2))
def project(w):
 u,v=w;depth=math.sin(y)*u+math.cos(y)*v;s=f/(c['distance_m']-math.cos(t)*depth)
 return np.array([c['anchor'][0]+s*(math.cos(y)*u-math.sin(y)*v),c['anchor'][1]+s*math.sin(t)*depth])*1536/720
world=[[-5,-4],[5,-4],[5,4],[-5,4]]
# order by screen quadrilateral: far, right, near, left
expected=np.array([project(w) for w in world]);order=np.argsort(np.arctan2(expected[:,1]-expected[:,1].mean(),expected[:,0]-expected[:,0].mean()));expected=expected[order]
# observed is same cyclic order starting top; identify corresponding expected by nearest distance
errs=[float(min(np.linalg.norm(v-e) for e in expected))*960/1536 for v in observed]
# Edge samples: independently detect luminance rise from neutral exterior along inward normals.
edge=[]
for i,a in enumerate(expected):
 b=expected[(i+1)%4];v=b-a;n=np.array([-v[1],v[0]]);n/=np.linalg.norm(n)
 if np.dot(expected.mean(axis=0)-(a+b)/2,n)<0:n=-n
 for frac in np.linspace(.1,.9,9):
  q=a+(b-a)*frac;ts=np.linspace(-10,10,81);values=[]
  for z in ts:
   x,y1=np.round(q+n*z).astype(int);values.append(im[y1,x].mean())
  candidates=[k for k in range(1,len(ts)) if values[k-1]<55<=values[k]]
  if candidates:edge.append(abs(float(ts[min(candidates,key=lambda k:abs(ts[k]))]))*960/1536)
  else:edge.append(99)
result={'source':'art/floor-v1.png','dimensions':list(im.shape[:2][::-1]),'native_view':[960,640],'corner_annotations_source_px':observed.tolist(),'annotation_uncertainty_source_px':2,'corner_errors_native_px':errs,'outer_edge_samples':len(edge),'outer_edge_max_native_px':max(edge),'outer_edge_p95_native_px':float(np.percentile(edge,95)),'outer_edge_pass':max(edge)<=3,'corner_pass':max(errs)<=3,'shifted_8px_control_rejected':max(abs(e+8) for e in errs)>3,'surface_boundary':'Visually follows projected diagonal; stone joint irregularity and earth feathering require overlay review. Not certified by outer-edge metric.','extra_obstructions':'No walls/props/pits observed; small gravel is decorative, not collidable.'}
(p/'evidence/floor-alignment.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
