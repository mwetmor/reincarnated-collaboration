"""Conductor glue for v14 (R-C3-109): from v11 — drop the extracted ground-shadow layer entirely; no shadows at all (Matt: the cow's is one of the worst). Run when no TOOLING burst runs."""
import json, shutil, pathlib
A = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-3/artifacts')
DST = A / 'CS-props-v14'; assert not DST.exists(); shutil.copytree(A / 'CS-props-v11', DST)
p = json.load(open(DST / 'props.json'))
keep = []
for sh in p['shadows']:
    if sh not in keep and (DST / sh['file']).exists(): (DST / sh['file']).unlink()
p['shadows'] = keep; json.dump(p, open(DST / 'props.json', 'w'), indent=1)
print('shadows', [sh['file'] for sh in p['shadows']], 'glows', len(p['glows']), 'particles', len(p['particles']))
