# EN-E2 copy of nb_join/scripts/j_runtime_resample.py (probe run from en_e2/film_rt). DOES THE RUNTIME PATH RE-SAMPLE? (the scene drax, 2026-09-30: Godot's EDITOR importer bakes every animation at
# animation/fps = 30, so a track keyed at 24 fps plays re-sampled.) The JOIN renderer does not use the editor importer:
# render_cells.gd loads each GLB at runtime with GLTFDocument.append_from_file + generate_scene(state). This runs that
# exact call (film/j_fps_probe.gd, headless) on the export and compares every track's key times with the GLB's own.
#
#   python3 scripts/j_runtime_resample.py [<glb>] [--clips a,b,...] [--out f] [--index matrix_index.json | --raw raw.json --kit kit.json]
#        -> work/runtime_resample.json; with a pack, also the difference AT ITS OWN FRAME TIMES
import json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); RUNS = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); L = __import__('21_lint_export')
GODOT = "/Applications/Godot.app/Contents/MacOS/Godot"
A = sys.argv[1:]; opt = lambda k, d=None: A[A.index(k) + 1] if k in A else d
GLB = A[0] if A and not A[0].startswith('--') else os.path.join(ROOT, "export", "nb-body_join.glb")
OUT = opt('--out', os.path.join(ROOT, "work", "runtime_resample.json"))
CLIPS = opt('--clips', '').split(',') if opt('--clips') else ["whirlwind", "shout", "hit", "death", "shout_raise", "idle_guard", "walk", "run", "walk_armed", "run_armed",
         "join_guard_R_idle", "join_guard_L_idle", "attack"]
dump = os.path.join(ROOT, "work", "_godot_tracks.json")
subprocess.run([GODOT, "--headless", "--path", os.path.join(ROOT, "film_rt"), "--script", "j_fps_probe.gd", "--",
                os.path.abspath(GLB), dump, ",".join(CLIPS)], check=True, capture_output=True)
g = json.load(open(dump))
js, b = L.load_glb(GLB); nodes = js['nodes']
TT = {'translation': '1', 'rotation': '2', 'scale': '3'}           # Godot Animation.TrackType: POSITION_3D 1, ROTATION_3D 2, SCALE_3D 3


def slerp(q0, q1, u):
    if np.dot(q0, q1) < 0: q1 = -q1
    d = float(np.clip(np.dot(q0, q1), -1, 1))
    if d > 0.9995: q = (1 - u) * q0 + u * q1; return q / np.linalg.norm(q)
    th = np.arccos(d); return (np.sin((1 - u) * th) * q0 + np.sin(u * th) * q1) / np.sin(th)


def qang(q1, q2):                               # the angle between two rotations, from UNIT quaternions: the file's are float32,
    q1 = q1 / np.linalg.norm(q1); q2 = q2 / np.linalg.norm(q2)     # and a 1e-7 norm error reads as 0.03 deg through acos
    return 2 * float(np.degrees(np.arccos(min(1.0, abs(float(np.dot(q1, q2)))))))


def ev(t, v, x):
    k = int(np.searchsorted(t, x, side='right')) - 1; k = min(max(k, 0), len(t) - 2)
    u = min(max((x - t[k]) / (t[k + 1] - t[k]), 0), 1); return slerp(v[k], v[k + 1], u)


out = dict(godot=g["godot"], call="GLTFDocument.append_from_file + generate_scene(state) -- render_cells.gd's own, no editor import",
           gltf_state_bake_fps=g["state_bake_fps"], glb=os.path.basename(GLB), clips={})
for an in js['animations']:
    nm = an['name']
    if nm not in CLIPS: continue
    ga = g["anims"][nm]; gd = ga["tracks"]
    rec = dict(length_glb=None, length_godot=round(ga["length"], 5), tracks=0, exact=0, two_key=0, resampled=[], dropped=[])
    Tg = 0.0
    for c in an['channels']:
        s = an['samplers'][c['sampler']]; t = L.read_accessor(js, b, s['input']).ravel().astype(float); Tg = max(Tg, float(t.max()))
        bn = nodes[c['target']['node']]['name']; path = c['target']['path']; rec["tracks"] += 1
        key = next((k for k in gd if k.split('|')[0].endswith(':' + bn) and k.split('|')[1] == TT[path]), None)
        if key is None:
            rec["dropped"].append("%s.%s" % (bn, path)); continue
        gt = np.array(gd[key]["times"])
        if len(t) == len(gt) and np.abs(gt - t).max() < 1e-4:
            rec["exact"] += 1; continue
        if len(t) <= 2:
            v = L.read_accessor(js, b, s['output']).astype(float).reshape(len(t), -1)
            rec["two_key"] += 1
            if s.get('interpolation') == 'STEP' and len(t) == 2 and np.abs(v[0] - v[1]).max() > 1e-6:
                rec["resampled"].append(dict(track="%s.%s" % (bn, path), note="STEP with two different values: baked keys interpolate between them"))
            continue
        row = dict(track="%s.%s" % (bn, path), keys_glb=len(t), spacing_glb=round(float(np.median(np.diff(t))), 5), keys_godot=len(gt))
        if path == 'rotation':
            v = L.read_accessor(js, b, s['output']).reshape(-1, 4).astype(float)
            gv = np.array([ev(t, v, x) for x in gt]); fine = np.linspace(0, t[-1], 2000)
            row["worst_deg"] = round(max(qang(ev(t, v, x), ev(gt, gv, x)) for x in fine), 3)
        rec["resampled"].append(row)
    rec["length_glb"] = round(Tg, 5)
    out["clips"][nm] = rec
    print("  %-18s %2d tracks: %2d key-for-key, %2d two-key (a line or a constant, re-keyed at 1/30 on the same line), re-sampled %s, dropped %s"
          % (nm, rec["tracks"], rec["exact"], rec["two_key"], [r["track"] + (" %.3f deg" % r["worst_deg"] if "worst_deg" in r else "") for r in rec["resampled"]], rec["dropped"]))
# --index <matrix_index.json>: the pack's OWN frame times -- how far the baked curve is from the GLB's AT THE RENDERED FRAMES
IDX = opt('--index'); RAW = opt('--raw')
if IDX or RAW:
    if IDX:
        ix = json.load(open(IDX))
    else:                                            # --raw <render raw json> --kit <kit>: before the index exists
        kit_ = json.load(open(opt('--kit'))); raw_ = json.load(open(RAW))
        ix = dict(states={st: dict(clip=dict(animation=sd["clip"]), t_s=raw_["cells"]["%s/S" % st]["t_s"]) for st, sd in kit_["states"].items()})
    at = {}
    for st, rec_ in ix["states"].items():
        nm = rec_["clip"]["animation"]; an = next(a for a in js['animations'] if a['name'] == nm); gd = g["anims"].get(nm, {}).get("tracks", {})
        worst = (0.0, None, None); worst_mm = (0.0, None, None)
        for c in an['channels']:
            s = an['samplers'][c['sampler']]; t = L.read_accessor(js, b, s['input']).ravel().astype(float)
            bn = nodes[c['target']['node']]['name']; path = c['target']['path']
            key = next((k for k in gd if k.split('|')[0].endswith(':' + bn) and k.split('|')[1] == TT[path]), None)
            if key is None or len(t) < 3: continue
            gt = np.array(gd[key]["times"])
            if len(t) == len(gt) and np.abs(gt - t).max() < 1e-4: continue
            v = L.read_accessor(js, b, s['output']).astype(float).reshape(len(t), -1)
            for x in rec_["t_s"]:
                if path == 'rotation':
                    gv = ev(t, v, x); bq = ev(gt, np.array([ev(t, v, y) for y in gt]), x)
                    d_ = qang(gv, bq)
                    if d_ > worst[0]: worst = (round(d_, 3), "%s.%s" % (bn, path), x)
                elif path == 'translation':
                    lin = lambda tt, vv, xx: np.array([np.interp(xx, tt, vv[:, i]) for i in range(vv.shape[1])])
                    bv = np.array([lin(t, v, y) for y in gt]); d_ = float(np.linalg.norm(lin(t, v, x) - lin(gt, bv, x)))
                    if d_ > worst_mm[0]: worst_mm = (round(d_, 5), "%s.%s" % (bn, path), x)
        at[st] = dict(clip=nm, frames=len(rec_["t_s"]), worst_deg=worst[0], worst_track=worst[1], worst_at_t=worst[2],
                      worst_translation_units=worst_mm[0], worst_translation_track=worst_mm[1])
        ri = rec_.get("release_index")
        if ri is not None:                           # the RELEASE frame: every rotation track, the forearms named
            tr_ = float(rec_["t_s"][ri]); rel_ = {}
            for c in an['channels']:
                if c['target']['path'] != 'rotation': continue
                s_ = an['samplers'][c['sampler']]; t = L.read_accessor(js, b, s_['input']).ravel().astype(float)
                bn = nodes[c['target']['node']]['name']
                key = next((k for k in gd if k.split('|')[0].endswith(':' + bn) and k.split('|')[1] == TT['rotation']), None)
                if key is None or len(t) < 2: continue
                v = L.read_accessor(js, b, s_['output']).astype(float).reshape(len(t), -1); gt = np.array(gd[key]["times"])
                bq = ev(gt, np.array([ev(t, v, y) for y in gt]), tr_)
                rel_[bn] = round(qang(ev(t, v, tr_), bq), 3)
            at[st]["release_frame"] = dict(index=ri, t_s=tr_, forearms_deg={k: rel_.get(k) for k in ("LeftForeArm", "RightForeArm")},
                                           worst_deg=max(rel_.values()) if rel_ else None,
                                           worst_track=max(rel_, key=rel_.get) if rel_ else None)
            print("  the release frame of %-13s (frame %d, t %.4f): forearms L %.3f / R %.3f deg; worst track %s %.3f deg"
                  % (st, ri, tr_, rel_.get("LeftForeArm", 0), rel_.get("RightForeArm", 0), at[st]["release_frame"]["worst_track"],
                     at[st]["release_frame"]["worst_deg"] or 0))
        print("  at the pack's frames: %-14s worst %.3f deg (%s at t %s); translation %s units (%s)" % (st, worst[0], worst[1], worst[2], worst_mm[0], worst_mm[1]))
    out["at_pack_frames"] = dict(index=os.path.abspath(IDX or RAW), states=at,
                                 what="per state, over the pack's own t_s: the largest angle between the GLB's curve and the baked "
                                      "one on any rotation track, and the largest translation difference (the GLB's units)")
out["reading"] = ("the runtime path DOES re-sample: generate_scene bakes every transform track at GLTFState.bake_fps (%s) -- keys at "
                  "1/30 steps plus one at the clip's end. A track already on that grid comes through key-for-key; a 2-key track is "
                  "re-keyed along its own line; only a multi-key track off the grid changes (listed under resampled, with the worst "
                  "angle between the GLB's curve and the baked one). 'dropped' = a rest-valued track removed by the importer "
                  "(remove_immutable_tracks), which is why the layers filter from all_clips." % g["state_bake_fps"])
json.dump(out, open(OUT, "w"), indent=1)
print("wrote %s (Godot %s, bake_fps %s)" % (OUT, g["godot"], g["state_bake_fps"]))
