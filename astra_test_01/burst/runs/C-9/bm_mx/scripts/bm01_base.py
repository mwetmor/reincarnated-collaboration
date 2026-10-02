# bm_mx STAGE 1 (R-C9-127): the BASE body for the barbarian's Mixamo 2H-hammer set -- a copy of the champion gladiator's
# GRADED body (gear_sets/barbarian_gladiator/body_graded, graded texture embedded, 26 JOIN joints, his ORIGINAL stance width)
# with ONLY his existing unarmed idle / walk / run kept, renamed idle_unarmed / walk_unarmed / run_unarmed; the other 32 JOIN
# clips are dropped (their accessors are compacted away by --compact). Nothing else changes: nodes, skin, IBMs, mesh, morphs.
#   python3 bm01_base.py <champion_body.glb> <out.glb> [--keep src:dst,src:dst]   (also: a one-clip SOURCE file for the registry)
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); R_ = __import__('49_recentre')
IN, OUT = sys.argv[1:3]
KEEP = {"idle": "idle_unarmed", "walk": "walk_unarmed", "run": "run_unarmed"}
if '--keep' in sys.argv: KEEP = dict(x.split(':') for x in sys.argv[sys.argv.index('--keep') + 1].split(','))
js, b = L.load_glb(IN)
anims = [a for a in js['animations'] if a['name'] in KEEP]
for a in anims: a['name'] = KEEP[a['name']]
js['animations'] = anims
# compact: rebuild the binary keeping only accessors still referenced
used = set()
def ref_acc(o):
    pass
for m in js['meshes']:
    for p in m['primitives']:
        used.update(p['attributes'].values())
        if 'indices' in p: used.add(p['indices'])
        for t in p.get('targets', []): used.update(t.values())
for s in js['skins']:
    if 'inverseBindMatrices' in s: used.add(s['inverseBindMatrices'])
for a in js['animations']:
    for s in a['samplers']: used.update([s['input'], s['output']])
bvs_used = {js['accessors'][i]['bufferView'] for i in used if 'bufferView' in js['accessors'][i]}
bvs_used |= {im['bufferView'] for im in js.get('images', []) if 'bufferView' in im}
nb = bytearray(); bvmap = {}
for i, bv in enumerate(js['bufferViews']):
    if i not in bvs_used: continue
    while len(nb) % 4: nb.append(0)
    o = bv.get('byteOffset', 0); d = b[o:o + bv['byteLength']]
    nbv = dict(bv); nbv['byteOffset'] = len(nb); nb += d; bvmap[i] = nbv
order = sorted(bvmap); newbv = {o: k for k, o in enumerate(order)}
js['bufferViews'] = [bvmap[o] for o in order]
acc_order = sorted(used); newacc = {o: k for k, o in enumerate(acc_order)}
accs = []
for o in acc_order:
    a = dict(js['accessors'][o])
    if 'bufferView' in a: a['bufferView'] = newbv[a['bufferView']]
    accs.append(a)
js['accessors'] = accs
for m in js['meshes']:
    for p in m['primitives']:
        p['attributes'] = {k: newacc[v] for k, v in p['attributes'].items()}
        if 'indices' in p: p['indices'] = newacc[p['indices']]
        if 'targets' in p: p['targets'] = [{k: newacc[v] for k, v in t.items()} for t in p['targets']]
for s in js['skins']:
    if 'inverseBindMatrices' in s: s['inverseBindMatrices'] = newacc[s['inverseBindMatrices']]
for a in js['animations']:
    for s in a['samplers']: s['input'] = newacc[s['input']]; s['output'] = newacc[s['output']]
for im in js.get('images', []):
    if 'bufferView' in im: im['bufferView'] = newbv[im['bufferView']]
js['buffers'][0]['byteLength'] = len(nb) + (-len(nb) % 4)
R_.write_glb(OUT, js, nb)
r = L.lint(OUT)
print('base', OUT, '%.2f MB' % (os.path.getsize(OUT) / 1e6), 'clips', [a['name'] for a in js['animations']], '| lint', r['verdict'], r['fails'][:3])
