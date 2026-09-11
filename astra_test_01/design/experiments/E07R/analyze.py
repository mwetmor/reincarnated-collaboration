from pathlib import Path
import json,math
r=Path(__file__).parent;geometry=json.loads((r/'evidence/batch-02/geometry.json').read_text());ann=json.loads((r/'evidence/annotations.json').read_text());out={}
def assess(expected,observed,uncertainty):
 error=math.dist(expected,observed);return{'error_px':error,'uncertainty_px':uncertainty,'lower_bound_px':max(0,error-uncertainty),'upper_bound_px':error+uncertainty,'verdict':'FAIL'if error-uncertainty>3 else'PASS'if error+uncertainty<=3 else'INDETERMINATE'}
for key,a in ann['candidates'].items():
 f=key[:3];rows=[]
 for p in geometry[f]['corners']:
  measured=a['corners'].get(p['id'])
  rows.append({'id':p['id'],'expected':p['pixel'],'observed':measured,'result':assess(p['pixel'],measured,ann['uncertainty_px'])if measured else{'verdict':'INDETERMINATE','reason':'Not directly observable with3pixel confidence; do not fit a hidden threshold corner'}})
 out[key]={'corners':rows,'verdict':'FAIL'if any(p['result']['verdict']=='FAIL'for p in rows)else'PASS'if all(p['result']['verdict']=='PASS'for p in rows)else'INDETERMINATE','side_semantics':a['side_semantics']}
expected=[p['pixel']for p in geometry['F01']['corners']]
controls={'identity_coordinates':[assess(p,p,0)for p in expected],'shifted40px':[assess(p,[p[0]+40,p[1]],0)for p in expected]}
checks={'identity_coordinate_instrument':all(p['verdict']=='PASS'for p in controls['identity_coordinates']),'shifted_annotation_detected':all(p['verdict']=='FAIL'for p in controls['shifted40px'])}
(r/'evidence/alignment.json').write_text(json.dumps({'candidates':out,'controls':controls,'checks':checks,'method':ann['method']},indent=2)+'\n')
for k,v in out.items():print(k,v['verdict'],[(x['id'],round(x['result'].get('lower_bound_px',0),1),x['result']['verdict'])for x in v['corners']])
