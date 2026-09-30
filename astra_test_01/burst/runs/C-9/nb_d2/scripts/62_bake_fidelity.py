# FILE FIDELITY THROUGH THE IMPORT BAKE (T12_11): how far does the clip Godot PLAYS sit from the clip the GLB KEYS?
#
#   python3 scripts/62_bake_fidelity.py <body.glb> <bake_probe.json> <clip> [--json out]
#
# Godot bakes every imported animation on a 1/30 s grid (editor import: animation/fps 30; runtime GLTFDocument:
# GLTFState.bake_fps 30). A track keyed on that grid comes through key-for-key; a track keyed at 24 fps is
# re-sampled, and linear interpolation between the re-sampled keys cuts the corners of the file's own curve.
# The JOIN lane measured the slash (attack, 24 fps) this way at up to 8.9 deg (nb_join/scripts/j_runtime_resample.py,
# RightHand) -- modelling the bake as the file's curve sampled at Godot's key times. This reads Godot's OWN baked
# values (attack_lab/t12/godot/tools/bake_probe.gd: both import paths) and compares them with the file's curve on a
# 2000-point grid over the clip: per rotation track, the worst angle; and the model's prediction beside it.
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export')


def slerp(q0, q1, u):
    if np.dot(q0, q1) < 0: q1 = -q1
    d = float(np.clip(np.dot(q0, q1), -1, 1))
    if d > 0.9995:
        q = (1 - u) * q0 + u * q1; return q / np.linalg.norm(q)
    th = np.arccos(d); return (np.sin((1 - u) * th) * q0 + np.sin(u * th) * q1) / np.sin(th)


def qang(a, b):
    a = a / np.linalg.norm(a); b = b / np.linalg.norm(b)
    return 2 * float(np.degrees(np.arccos(min(1.0, abs(float(np.dot(a, b)))))))


def ev(t, v, x):
    if len(t) == 1: return v[0]
    k = int(np.searchsorted(t, x, side='right')) - 1; k = min(max(k, 0), len(t) - 2)
    u = min(max((x - t[k]) / (t[k + 1] - t[k]), 0), 1); return slerp(v[k], v[k + 1], u)


if __name__ == "__main__":
    glb, probe, clip = sys.argv[1], sys.argv[2], sys.argv[3]
    js, b = L.load_glb(glb); nodes = js['nodes']
    an = next(a for a in js['animations'] if a['name'] == clip)
    g = json.load(open(probe))
    res = dict(glb=os.path.basename(glb), clip=clip, godot=g.get("godot"), runtime_bake_fps=g.get("runtime_bake_fps"), paths={})
    for path in ("runtime", "editor"):
        gd = g[path][clip]["tracks"]
        rows = {}
        for c in an['channels']:
            if c['target']['path'] != 'rotation': continue
            s = an['samplers'][c['sampler']]
            t = L.read_accessor(js, b, s['input']).ravel().astype(float)
            v = L.read_accessor(js, b, s['output']).reshape(-1, 4).astype(float)
            bn = nodes[c['target']['node']]['name']
            if bn not in gd:
                rows[bn] = dict(note="dropped by this import (rest-valued)"); continue
            gt = np.array(gd[bn]["times"], float); gv = np.array(gd[bn]["vals"], float)
            fine = np.linspace(0, float(t[-1]), 2000)
            worst = max(qang(ev(t, v, x), ev(gt, gv, x)) for x in fine)
            model = np.array([ev(t, v, x) for x in gt])
            worst_model = max(qang(ev(t, v, x), ev(gt, model, x)) for x in fine)
            at_keys = max(qang(ev(t, v, x), q) for x, q in zip(gt, gv))
            rows[bn] = dict(keys_glb=len(t), keys_godot=len(gt), worst_deg=round(worst, 3), model_deg=round(worst_model, 3),
                            at_godot_keys_deg=round(at_keys, 4))
        w = max((r for r in rows.items() if "worst_deg" in r[1]), key=lambda r: r[1]["worst_deg"])
        res["paths"][path] = dict(worst_track=w[0], worst_deg=w[1]["worst_deg"], tracks=rows)
        print("  %-8s %s %s: worst %s %.3f deg (the bake-model reads %.3f); Godot's keys on the file's curve within %.4f deg"
              % (path, res["glb"], clip, w[0], w[1]["worst_deg"], w[1]["model_deg"], max(r["at_godot_keys_deg"] for r in rows.values() if "at_godot_keys_deg" in r)))
    if "--json" in sys.argv:
        json.dump(res, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
