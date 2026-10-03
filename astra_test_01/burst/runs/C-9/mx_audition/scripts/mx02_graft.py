# MX audition (R-C9-149): graft Mixamo clips (mxglb/, rig-named by e40a) onto a COPY of a shipped final body, next to its own
# clips of record, with en_e2's e40b (55_clip_graft world-space transfer + T->A rest alignment). The shipped body is only READ;
# the audition GLB goes to work/aud_<tag>.glb (gitignored). Window = [first key + 1/30 s, last key] -- the EN-E2 convention
# (d_graft.json: every clip windowed from 0.0333 s). Self-check (run once, fleshhulk): re-grafting axe_unarmed_walk_forward
# onto final_d reproduces the shipped 'walk' to 0.0000 m (scripts/mx_cmp.py), so the audition clips are transferred exactly
# as the clips of record were.
#   python3 scripts/mx02_graft.py <body.glb> <tag> name=<mxglb file>[+loop][+deroot][@t0:t1] ...
import sys, os, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__)); EN = os.path.join(HERE, '..', '..', 'en_e2', 'scripts'); sys.path.insert(0, EN)
L = __import__('21_lint_export')
body, tag, specs = sys.argv[1], sys.argv[2], sys.argv[3:]
out = []
for s in specs:
    name, rest = s.split('=', 1); parts = rest.split('+'); src = parts[0]; flags = parts[1:]
    if '@' not in src:
        js, b = L.load_glb(src); an = js['animations'][0]
        T = max(float(js['accessors'][sm['input']]['max'][0]) for sm in an['samplers'])
        src = '%s@%.6f:%.6f' % (src, 1 / 30, T)
    out.append('%s=%s%s' % (name, src, ''.join('+' + f for f in flags)))
cmd = ['python3', os.path.join(EN, 'e40b_mixamo_graft.py'), 'graft', body, 'work/aud_%s.glb' % tag] + out + ['--json', 'work/aud_%s_graft.json' % tag]
r = subprocess.run(cmd, capture_output=True, text=True)
for ln in (r.stdout + r.stderr).splitlines():
    if not ln.startswith('WARNING: SOURCE ON ANOTHER RIG'): print(ln[:230])
