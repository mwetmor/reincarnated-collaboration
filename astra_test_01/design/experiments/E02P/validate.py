"""Check actual Phaser transforms against frozen independent E02 predictions."""
from pathlib import Path
import hashlib,json,math,sys
from PIL import Image
p=Path(__file__).resolve().parent
batch=sys.argv[1] if len(sys.argv)>1 else 'batch-01'
r=json.loads((p/'evidence'/batch/'runtime.json').read_text())
a=json.loads((p.parent/'E02/evidence/analysis.json').read_text())
lookup={s['id']:s for s in a['samples']}
checks={};residuals=[]
for dep in json.loads((p/'INPUTS.json').read_text())['dependencies']:
    checks['dependency:'+dep['path']]=hashlib.sha256((p.parent/dep['path']).read_bytes()).hexdigest()==dep['sha256']
checks['18_unique_cases']=len(r['cases'])==18 and len({(c['tracking'],c['sample']) for c in r['cases']})==18
checks['no_browser_errors']=not r['errors']
for c in r['cases']:
    key=('tracking' if c['tracking'] else 'fixed')+':'+c['sample']
    ref=lookup['center' if c['tracking'] else c['sample']]
    err=max(math.dist(c[k],ref[k]) for k in ['root_px','top_px']);residuals.append(err)
    checks[key+':independent_projection']=err<=.5
    checks[key+':engine_attachment']=max(c['root_error_px'],c['socket_error_px'])<=.5
    checks[key+':negative_root_socket']=c['controls']['runtime_shifted_root_rejected'] and c['controls']['runtime_shifted_socket_rejected']
    expected_scale=ref['body_height_px']/223.5
    checks[key+':scale_and_bad_control']=abs(c['source_scale']-expected_scale)*223.5<=.5 and abs(c['bad_scale']-expected_scale)*223.5>.5 and abs(c['bad_scale']/c['source_scale']-1.25)<1e-6
    with Image.open(p/'evidence'/batch/c['capture']) as im:
        checks[key+':capture']=im.size==(720,405) and len(im.convert('RGB').getcolors(1000000))>100
u=r['ui']
if u:
    checks['ui:position']=u['position']['sample']=='right' and math.dist(u['position']['root_px'],lookup['right']['root_px'])<=.5
    checks['ui:following']=u['following']['tracking'] and math.dist(u['following']['root_px'],lookup['center']['root_px'])<=.5
    checks['ui:bad_scale']=abs(u['bad']['source_scale']/u['following']['source_scale']-1.25)<1e-6
    checks['ui:translation_moves']=math.dist(u['motion_start']['world'],u['motion_end']['world'])>.1 and math.dist(u['motion_start']['root_px'],u['motion_end']['root_px'])>1
    checks['ui:pause_stops']=u['pause_start']['world']==u['pause_end']['world']
else: checks['ui:present']=False
out={'experiment':'E02P','batch':batch,'checks':checks,'passed':sum(checks.values()),'total':len(checks),'max_independent_projection_residual_px':max(residuals,default=None),'scope':'Projection/root/socket and basic UI foundation only; no painted-chamber, animation, gear, VFX or full G2 pass.'}
(p/'evidence'/batch/'validation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'}))
if not all(checks.values()):print('FAILED', [k for k,v in checks.items() if not v]);sys.exit(1)
