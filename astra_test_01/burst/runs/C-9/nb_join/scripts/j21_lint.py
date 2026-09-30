# nb_join's EXPORT LINT: nb_d2's 21_lint_export.py (the scene drax's, read-only here), run UNCHANGED against THIS
# lane's provenance registry. The new rows -- SOURCE FIDELITY, SOURCE GRID, LOOP SEAM (56_clip_fidelity) -- judge
# only the clips the registry they read names, and 56 reads nb_d2/work/clip_sources.json by default, which names
# none of the JOIN moves: run bare, the lint would pass them WITHOUT LOOKING. So the registry default is pointed at
# nb_join/work/clip_sources.json for this process, and the lint is called exactly as it stands (no row re-written).
# The WEAPON REST row reads the weapon_mount.json beside the file, as it always does.
#
#   python3 scripts/j21_lint.py <x.glb> [--json f]
import importlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB_D2 = os.path.join(os.path.dirname(ROOT), "nb_d2", "scripts")
sys.path.insert(0, NB_D2)
REG = os.path.join(ROOT, "work", "clip_sources.json")
F = importlib.import_module("56_clip_fidelity")
F.REGISTRY = REG
F.registry.__defaults__ = (REG,)
L = importlib.import_module("21_lint_export")
out = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None
a = [x for x in sys.argv[1:] if not x.startswith('--') and x != out]
res = []
for p in a:
    r = L.lint(p)
    res.append(r)
    print("=== %s (registry %s)" % (p, os.path.relpath(REG, ROOT)))
    for f in r['fails']:
        print("  FAIL  %s" % f)
    for w in r['warns']:
        print("  WARN  %s" % w)
    print("  VERDICT: %s" % r['verdict'])
# the rows themselves, row by row, so a clip that was NOT judged is visible as such
reg = F.registry(REG)
for p in a:
    fid = {r['clip']: r for r in F.check(p, reg)}
    sms = {r['clip']: r for r in F.seams(p, reg)}
    for clip in sorted(reg.get('clips', {})):
        f_ = fid.get(clip); s_ = sms.get(clip)
        print("  %-10s SOURCE FIDELITY %-9s %s" % (clip, f_['status'] if f_ else "NOT IN FILE",
              ("max %.4f hips-to-head (limit %.2f), rest match %.5f" % (f_['err_max'], F.LIMIT, f_['rest_match'])) if f_ and 'err_max' in f_ else (f_ or {}).get('note', '')))
        if s_:
            print("  %-10s SOURCE GRID     %-9s %s" % (clip, s_['grid_status'], s_.get('grid_note', '')))
            print("  %-10s LOOP SEAM       %-9s closure %.5f m (%s) / %.3f deg, first interval %.2f of the median"
                  % (clip, s_['seam_status'], s_['closure_m'], s_['closure_joint'], s_['closure_deg'], s_['first_frac']))
    res[a.index(p)]['rows'] = dict(fidelity=list(fid.values()), seams=list(sms.values()))
if out:
    json.dump(res, open(out, 'w'), indent=1, default=str)
sys.exit(1 if any(x['fails'] for x in res) else 0)
