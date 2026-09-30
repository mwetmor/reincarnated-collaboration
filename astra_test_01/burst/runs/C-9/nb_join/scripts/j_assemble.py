# nb_join EXPORT: the barbarian's JOIN body with the four JOIN moves, from the scene drax's JOIN body -- every byte of
# his file kept, the moves APPENDED (two binary patches, no Blender round trip).
#
#   python3 scripts/j_assemble.py <base nb-body.glb> <base weapon_mount.json> <out.glb> <whirl pose.json>
#        --shout <src>[@t0:t1] --hit <src>[@t0:t1] --death <src>[@t0:t1] [--whirl-T 0.5333]
#
#   1. shout / hit / death: nb_d2/scripts/55_clip_graft.py graft (read-only use): Meshy clips fetched on HIS rig,
#      carried across in WORLD space, de-rooted, recentred on the first frame, grounded from the feet, no scale
#      tracks, no weapon-bone tracks (the weapons ride their mounts).
#   2. whirlwind: j_whirl_clip.py -- the authored pose under a uniform single-revolution yaw, keyed on the idle
#      source's own 30 fps grid (16 frames = 16/30 s), so the SOURCE GRID row reads it like any loop.
#   3. the mount record beside the export (21_lint's WEAPON REST row reads it there) and the provenance registry
#      (work/clip_sources.json, paths relative to nb_d2/ as 56_clip_fidelity resolves them).
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); RUNS = os.path.dirname(ROOT)
NB_D2 = os.path.join(RUNS, "nb_d2")
a = sys.argv[1:]
BASE, MOUNT, OUT, POSE = a[0], a[1], a[2], a[3]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
WT = float(opt('--whirl-T', str(16 / 30.0)))
specs = {k: opt('--' + k) for k in ('shout', 'hit', 'death')}
tmp = os.path.join(ROOT, "work", "_assemble_grafted.glb")
gargs = []
for name, sp in specs.items():
    gargs.append("%s=%s+deroot" % (name, sp))
r = subprocess.run([sys.executable, os.path.join(NB_D2, "scripts", "55_clip_graft.py"), "graft", BASE, tmp] + gargs +
                   ["--json", os.path.join(ROOT, "work", "graft_join.json")], capture_output=True, text=True)
print(r.stdout.strip()); print(r.stderr.strip()[-600:])
assert r.returncode == 0, "graft failed"
r = subprocess.run([sys.executable, os.path.join(HERE, "j_whirl_clip.py"), tmp, POSE, OUT, "--name", "whirlwind", "--T", str(WT),
                    "--json", os.path.join(ROOT, "work", "whirl_clip_join.json")], capture_output=True, text=True)
print(r.stdout.strip()); print(r.stderr.strip()[-600:])
assert r.returncode == 0, "whirlwind failed"
shutil.copyfile(MOUNT, os.path.join(os.path.dirname(os.path.abspath(OUT)), "weapon_mount.json"))
os.replace(tmp, os.path.join(ROOT, "work", "_assemble_grafted_last.glb"))       # kept (gitignored) for inspection
src_reg = json.load(open(os.path.join(NB_D2, "work", "clip_sources.json")))
rel = lambda p: os.path.relpath(os.path.abspath(p), NB_D2)
g = json.load(open(os.path.join(ROOT, "work", "graft_join.json")))["clips"]
fetch = json.load(open(os.path.join(ROOT, "work", "meshy_fetch.json")))["clips"]
def entry(name, sp):
    src, win = (sp.split('@') + [None])[:2]
    rec = next((v for v in fetch.values() if isinstance(v, dict) and v.get('file') and os.path.abspath(v['file']) == os.path.abspath(src)), {})
    e = dict(source=rel(src), path="55_clip_graft", action="Meshy %s" % rec.get('action_id'), rig=rec.get('rig'),
             fetched_task=rec.get('task'), flags=["deroot"], edits=["deroot", "recentre", "reground"] + (["trim"] if win else []))
    if win:
        e["window"] = [float(x) for x in win.split(':')]
    e["graft"] = g.get(name)
    return e
reg = dict(_note="PROVENANCE OF THE JOIN MOVES in nb_join/export (the barbarian's JOIN body + whirlwind, shout, hit, death), the "
                 "input of 21_lint_export's SOURCE FIDELITY / SOURCE GRID / LOOP SEAM rows as run by scripts/j21_lint.py. Same "
                 "schema as nb_d2/work/clip_sources.json; paths relative to nb_d2/ (56_clip_fidelity resolves them there).",
           body_rig=src_reg.get("body_rig"), edits=src_reg.get("edits"),
           clips={k: entry(k, sp) for k, sp in specs.items()})
reg["clips"]["whirlwind"] = dict(source=None, path="j_whirl_pose.py + j_whirl_clip.py (authored)", loop=True,
                                 grid_source="../nb_t8/nbt_idle.glb", grid_window=[0.0333, 0.5667],
                                 note="authored: the idle's stance (its source key at 0.5333 s), the chest squared, both arms solved "
                                      "(blades level and radial, edges along the CCW tangent), turned by a uniform single revolution "
                                      "keyed on the idle SOURCE's own 30 fps grid -- 17 keys, one per 22.5 deg")
json.dump(reg, open(os.path.join(ROOT, "work", "clip_sources.json"), "w"), indent=1)
print("wrote %s and work/clip_sources.json" % OUT)
