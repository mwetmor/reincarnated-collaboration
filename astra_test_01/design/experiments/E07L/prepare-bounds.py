from pathlib import Path
import json,numpy as np,hashlib
p=Path(__file__).resolve().parent;base=p.parent/'E05J';a=json.loads((base/'character.asset.json').read_text());records=[]
for pose in a['poses']:
 x=base/pose['oracle']['path'];v=np.frombuffer(x.read_bytes(),dtype='<f4').reshape(-1,6)[:,:3].astype(float);records.append({'source':str(x.relative_to(base)),'sha256':hashlib.sha256(x.read_bytes()).hexdigest(),'radius_m':float(np.hypot(v[:,0],v[:,1]).max()),'z_min_m':float(v[:,2].min()),'z_max_m':float(v[:,2].max())})
b={'radius_m':max(r['radius_m'] for r in records),'z_min_m':min(r['z_min_m'] for r in records),'z_max_m':max(r['z_max_m'] for r in records),'scope':'Conservative all-source-vertices envelope across three existing sparse poses; invariant to heading; includes hidden hair/gear for safe overestimate. Not animation inventory proof.'};s=json.loads((p/'shadow.json').read_text());s['conservative_caster_bounds']=b;(p/'shadow.json').write_text(json.dumps(s,indent=2)+'\n');(p/'evidence/bounds-preparation.json').write_text(json.dumps({'sources':records,'envelope':b},indent=2)+'\n');print(b)
