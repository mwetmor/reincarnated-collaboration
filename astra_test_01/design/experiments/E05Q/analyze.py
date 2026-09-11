from pathlib import Path
import numpy as np,json,struct,math
from PIL import Image
p=Path(__file__).resolve().parent;out=p/'evidence/batch-02-wide';rows=[]
for pose in[0,2]:
 for head in ['head','hidden']:
  for bg,c in [('dark',[24,35,49]),('light',[230,223,209])]:
   suffix=f'{pose}-{head}-{bg}';large=np.array(Image.open(out/f'C-{suffix}.png').convert('RGB')).astype(float);height,width=large.shape[0]//3,large.shape[1]//3;ref=large.reshape(height,3,width,3,3).mean((1,3));values={}
   for method in ['A','B']:
    im=np.array(Image.open(out/f'{method}-{suffix}.png').convert('RGB')).astype(float);mask=np.any(im!=c,2)|np.any(abs(ref-c)>.01,2);e=abs(im-ref)[mask];values[method]={'mae':float(e.mean()),'rmse':float(np.sqrt((e**2).mean())),'fraction_gt8':float((e.max(1)>8).mean())}
   rows.append({'pose':pose,'head':head,'bg':bg,'metrics':values,'B_reduces_mae':values['B']['mae']<values['A']['mae']})
asset=json.loads((p.parent/'E05J/character.asset.json').read_text());profile=json.loads((p.parent/'E03/inputs/projection-candidates.json').read_text())[2];e=math.radians(profile['elevation_deg']);y=math.radians(profile['yaw_deg']);f=202.5/math.tan(math.radians(profile['vertical_fov_deg'])/2)*4;bounds=[]
for pose in asset['poses']:
 points=np.fromfile(p.parent/'E05J'/pose['oracle']['path'],dtype='<f4').reshape(-1,6)[:,:3].astype(float)
 for i,h in enumerate(asset['directions']):
  a=math.radians(-h);xyz=points@np.array([[math.cos(a),math.sin(a),0],[-math.sin(a),math.cos(a),0],[0,0,1]]);u=xyz[:,0];v=-xyz[:,1];z=xyz[:,2];along=math.sin(y)*u+math.cos(y)*v;factor=f/(profile['distance_m']-math.cos(e)*along-math.sin(e)*z);off=np.stack([factor*(math.cos(y)*u-math.sin(y)*v),factor*(math.sin(e)*along-math.cos(e)*z)],axis=1)
  for height,rootY in [(50,100),(150,360)]:
   xy=off*height/153.89987636063665+np.array([90+i*180,rootY]);lo=xy.min(0);hi=xy.max(0);bounds.append({'pose':pose['id'],'heading':h,'height':height,'minimum':lo.tolist(),'maximum':hi.tolist(),'required_pose':pose['clip']in ['idle','cast'],'margin_at_least5':bool(lo[0]>=5 and lo[1]>=5 and hi[0]<=1435 and hi[1]<=455)})
r={'records':rows,'B_improves_cases':sum(x['B_reduces_mae']for x in rows),'numerical_pass':sum(x['B_reduces_mae']for x in rows)>=6,'reference':'Fresh3xMSAA/no-mips; exact3x3channel mean measurement only','full_geometry_bounds':bounds,'full_geometry_margin_pass':all(x['margin_at_least5']for x in bounds),'required_pose_margin_pass':all(x['margin_at_least5']for x in bounds if x['required_pose']),'supplemental_walk_margin_pass':all(x['margin_at_least5']for x in bounds if not x['required_pose']),'visual_scope':'No obvious ivory/brass/blue boundary bleed in inspected native controls. Full art/temporal shimmer remain unqualified.','selected':'B'};(out/'sampling-validation.json').write_text(json.dumps(r,indent=2)+'\n');print({'improved':r['B_improves_cases'],'margin_checks':len(bounds),'margins_pass':r['full_geometry_margin_pass'],'worst_B_mae':max(x['metrics']['B']['mae']for x in rows),'worst_A_mae':max(x['metrics']['A']['mae']for x in rows)})
