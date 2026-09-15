# C-5 glue: assemble runs/C-5/artifacts/CS-props-v19/ = CS-props-v14 (v18 scene props) + dummy assets + placed props.json from CS-assets-clearing.
import shutil, json, pathlib, sys
B=pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
src=B/'runs/C-3/artifacts/CS-props-v14'; dst=B/'runs/C-5/artifacts/CS-props-v19'; A=B/'runs/C-5/artifacts/CS-assets-clearing'
if dst.exists(): shutil.rmtree(dst)
shutil.copytree(src,dst)
for p in (A/'assets').glob('*.png'): shutil.copy(p, dst/'assets'/p.name)
pj=json.load(open(A/'props_clearing.json'))
# normalise asset file paths to assets/<name>.png relative to the props dir
for a in pj['assets']:
    f=a.get('file','')
    if 'dummy' in a['name'] and not f.startswith('assets/'): a['file']='assets/'+pathlib.Path(f).name
json.dump(pj,open(dst/'props.json','w'),indent=1)
missing=[a['file'] for a in pj['assets'] if not (dst/a['file']).exists()]
print('assets',len(pj['assets']),'instances',len(pj['instances']),'missing files',missing)
print('dummies:',[ (i['asset'],[round(v) for v in i['position']]) for i in pj['instances'] if 'dummy' in i['asset']])
print('cow:',[ (i['asset'],[round(v) for v in i['position']]) for i in pj['instances'] if 'cow' in i['asset']])
