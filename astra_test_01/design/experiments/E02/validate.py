"""Validate independent references, runtime results and preserved source bytes."""
from pathlib import Path
import hashlib
import json
import math
from PIL import Image

P=Path(__file__).resolve().parent
analysis=json.loads((P/'evidence/analysis.json').read_text())
pixi=json.loads((P/'evidence/runtime-pixi-v2.json').read_text())
sources=json.loads((P/'INPUTS.json').read_text())
checks=[]
def record(name,passed,**detail):
    checks.append(dict(name=name,passed=bool(passed),**detail))

for source in sources:
    digest=hashlib.sha256((P/source['snapshot']).read_bytes()).hexdigest()
    record('source_hash:'+source['snapshot'],digest==source['sha256'])
record('independent_geometry_controls',all(analysis['checks'].values()))
record('browser_controls',all(pixi['controls'].values()) and not pixi['errors'])
worst=0
for policy in ['fixed','tracking']:
    godot=json.loads((P/f'evidence/runtime-{policy}-v2.json').read_text())
    for g in godot['checks']:
        reference=next(r for r in analysis['samples'] if r['id']==('center' if policy=='tracking' else g['sample']))
        p=next(r for r in pixi['records'] if r['sample']==g['sample'] and r['tracking']==(policy=='tracking'))
        errors={engine:{key:math.dist(row[key],reference[key]) for key in ['root_px','top_px']}
                for engine,row in [('Godot',g),('Pixi',p)]}
        maximum=max(e for engine in errors.values() for e in engine.values());worst=max(worst,maximum)
        record(policy+':'+g['sample']+':projection',maximum<=.5,errors_px=errors)
        record(policy+':'+g['sample']+':attachment',max(g['socket_error_px'],p['socket_error_px'])<=.5)
        record(policy+':'+g['sample']+':bad_controls',g['bad_root_error_px']>.5 and g['bad_socket_error_px']>.5)
        for file in [f'{policy}-v2-{g["sample"]}.png',f'pixi-v2-{policy}-{g["sample"]}.png']:
            im=Image.open(P/'evidence'/file)
            record('capture:'+file,im.size==(1440,1000) and len(im.getcolors(2000000) or [])>100)
result={'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL',
        'checks_passed':sum(c['passed'] for c in checks),'checks_total':len(checks),
        'max_runtime_reference_error_px':worst,'checks':checks,
        'scope':'Projection, hierarchy attachment, input integrity, controls and capture presence only. Not art/motion/VFX/whole-G2 acceptance.'}
(P/'evidence/validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
assert result['status']=='PASS'
