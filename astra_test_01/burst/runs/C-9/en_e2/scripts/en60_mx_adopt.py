# EN-E2 C-9 Phase 2 (R-C9-150 Matt-approved MX audition picks; R-C9-157): ADOPT Mixamo Creature Pack clips onto a body's clip set of
# record. Grafts each pick with e40b exactly as the MX lane did (mx02: window [1/30 s, end], +loop+deroot for loops, +deroot for
# one-shots) under a temporary name, then REPLACES the record clip of that name (or adds it). Every other clip of record is kept
# byte-for-byte (same accessors). The graft record goes to <json>.
#   python3 scripts/en60_mx_adopt.py <in_c1.glb> <out.glb> --json <graft.json> name=<mxglb>[+loop][+deroot] ...
import sys, os, json, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); R = __import__('49_recentre')
a = sys.argv[1:]; IN, OUT = a[0], a[1]; JS = a[a.index('--json') + 1]; specs = [s for s in a[2:] if '=' in s]
tmp = tempfile.mktemp(suffix='.glb', dir=os.path.dirname(OUT)); out = []
for s in specs:
    name, rest = s.split('=', 1); parts = rest.split('+'); src = parts[0]
    sj, sb = L.load_glb(src); an = sj['animations'][0]
    T = max(float(sj['accessors'][sm['input']]['max'][0]) for sm in an['samplers'])
    out.append('__mx_%s=%s@%.6f:%.6f%s' % (name, src, 1 / 30, T, ''.join('+' + f for f in parts[1:])))
r = subprocess.run(['python3', os.path.join(HERE, 'e40b_mixamo_graft.py'), 'graft', IN, tmp] + out + ['--json', JS], capture_output=True, text=True)
print('\n'.join(l[:200] for l in (r.stdout + r.stderr).splitlines() if l.startswith(('lint', 'graft'))))
assert r.returncode == 0 and os.path.exists(tmp), r.stderr[-800:]
js, b = L.load_glb(tmp); new = {a['name'][5:] for a in js['animations'] if a['name'].startswith('__mx_')}
js['animations'] = [a for a in js['animations'] if a['name'] not in new]
for a in js['animations']:
    if a['name'].startswith('__mx_'): a['name'] = a['name'][5:]
R.write_glb(OUT, js, bytearray(b)); os.remove(tmp)
print('ADOPT', os.path.basename(OUT), 'replaced/added', sorted(new), 'clips', [a['name'] for a in js['animations']])
