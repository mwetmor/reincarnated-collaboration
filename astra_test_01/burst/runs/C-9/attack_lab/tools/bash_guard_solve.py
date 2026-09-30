"""T12_8: THE BASH GUARD -- the axe arm's pose through the shield bash, solved for the bash's own torso.

    python3 bash_guard_solve.py <body.glb> <axe.glb> <guard_pose.json> <out.json> [--clip shield_bash]

The bash is a strike whose swing is the SHIELD's: the axe arm holds a guard through it
(knight.gd strike_release.guard_throughout). The standing guard, riding the bash's torso -- which
turns ~85 deg and pitches forward through the lunge -- put the axe's butt end into his thigh on 13 of
59 frames; a guard solved at any ONE lunge frame's chest traded that for other frames (16-55).

So the pose is solved against the WHOLE lunge at once: RightArm and RightForeArm (RightShoulder the
walk's clavicle, the wrist neutral, the axe on its mount -- the standing guard's own construction)
minimising, over every frame of the clip, how far the axe's sample points reach inside a capsule
model of his body (thighs, shins, hips, torso, neck, head, the left arm and the right arm's upper
half, each bone a segment with a radius), plus a pull toward the standing guard so the arm stays a
guard and not a flourish. The capsules only steer the search; the verdict is the real mesh, in
Godot, with the acceptance's instrument (guard_accept.gd / guard_strike_exp.gd).
"""
import json, math, os, sys
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.normpath(os.path.join(HERE, "..", "..", "nb_d2", "scripts"))
sys.path.insert(0, SCR)
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')
G55 = __import__('55_clip_graft')

MPU = 0.010882345028221607            # metres per glTF unit (the Armature scale)
CAPS = [("LeftUpLeg", "LeftLeg", 0.175), ("LeftLeg", "LeftFoot", 0.11), ("RightUpLeg", "RightLeg", 0.175),
        ("RightLeg", "RightFoot", 0.11), ("Hips", "Spine02", 0.20), ("Spine02", "Spine", 0.19), ("Spine", "neck", 0.15),
        ("neck", "Head", 0.15), ("Head", "head_end", 0.12), ("LeftShoulder", "LeftArm", 0.11), ("LeftArm", "LeftForeArm", 0.11),
        ("LeftForeArm", "LeftHand", 0.075), ("RightShoulder", "RightArm", 0.11), ("RightArm", "RightForeArm", 0.11)]
# radii MEASURED from the body mesh (each bone's dominant vertices from its segment, at rest: the
# mean of p50 and p95 -- the thigh is 0.148/0.201 m, the baggy trousers; the hips 0.183/0.221)
MARGIN = 0.02


def rotvec_to_m(v):
    a = float(np.linalg.norm(v))
    return np.eye(3) if a < 1e-12 else W.axis_angle(v / a, a)


def seg_dist(p, a, b):
    ab = b - a; t = np.clip(((p - a) @ ab) / max(float(ab @ ab), 1e-12), 0.0, 1.0)
    return np.linalg.norm(p - (a[None, :] + t[:, None] * ab[None, :]), axis=1)


def main():
    body, axe, gpj, outp = sys.argv[1:5]
    clip = sys.argv[sys.argv.index('--clip') + 1] if '--clip' in sys.argv else "shield_bash"
    # --from/--to: only these clip times (the chop: the frames after its swing, where the arm is released to the guard)
    t_from = float(sys.argv[sys.argv.index('--from') + 1]) if '--from' in sys.argv else -1.0
    t_to = float(sys.argv[sys.argv.index('--to') + 1]) if '--to' in sys.argv else 1e9
    js, b = L.load_glb(body)
    nodes = js['nodes']
    idx = {n.get('name'): i for i, n in enumerate(nodes)}
    an = next(a for a in js['animations'] if a['name'] == clip)
    tr = G55.tracks(js, b, an)
    ts = sorted(set(float(x) for d in tr.values() for (tt, _, _) in d.values() for x in tt))
    ts = [x for x in ts if t_from - 1e-6 <= x <= t_to + 1e-6]
    ts = ts[::3] if len(ts) > 30 else ts
    A = None
    frames = []
    for t in ts:
        Gw = G55.body_world(js, tr, t)
        if A is None:
            A = Gw[idx['Armature']] if 'Armature' in idx else np.eye(4)
        Ai = np.linalg.inv(A)
        Gs = {n: Ai @ Gw[i] for n, i in idx.items()}                       # skeleton space (units)
        frames.append(dict(t=t, spine=Gs['Spine'], joints={n: Gs[n][:3, 3] for n in idx}))
    # the axe's points in weapon_r's frame, and which are in the fist (excluded)
    ajs, abin = L.load_glb(axe)
    sk = ajs['skins'][0]
    jn = [ajs['nodes'][j]['name'] for j in sk['joints']]
    ibm = [np.array(r, float).reshape(4, 4).T for r in L.read_accessor(ajs, abin, sk['inverseBindMatrices'])]
    wr = jn.index('weapon_r')
    mesh = next(nd for nd in ajs['nodes'] if 'mesh' in nd and 'skin' in nd)
    pos = np.concatenate([L.read_accessor(ajs, abin, pr['attributes']['POSITION']) for pr in ajs['meshes'][mesh['mesh']]['primitives']])
    P = (ibm[wr] @ np.hstack([pos, np.ones((len(pos), 1))]).T).T[:, :3][::60]
    grip = np.array([P[:, 0].mean(), 0.0, P[:, 2].mean()])
    keep = ~((np.abs(P[:, 1]) * MPU < 0.09) & (np.linalg.norm(P[:, [0, 2]] - grip[[0, 2]], axis=1) * MPU < 0.06))
    P = P[keep]
    Ph = np.hstack([P, np.ones((len(P), 1))])
    rest = {nm: W.trs(nodes[idx[nm]]) for nm in ["RightShoulder", "RightArm", "RightForeArm", "RightHand", "weapon_r"]}
    gp = json.load(open(gpj))["pose"]
    q_sh = W.q2m(np.array(gp["RightShoulder"], float))
    qa0 = W.q2m(np.array(gp["RightArm"], float)); qf0 = W.q2m(np.array(gp["RightForeArm"], float))

    def axe_points(fr, qa, qf):
        Xs = rest["RightShoulder"].copy(); Xs[:3, :3] = q_sh
        Xa = rest["RightArm"].copy(); Xa[:3, :3] = qa
        Xf = rest["RightForeArm"].copy(); Xf[:3, :3] = qf
        M = fr['spine'] @ Xs @ Xa @ Xf @ rest["RightHand"] @ rest["weapon_r"]
        elbow = (fr['spine'] @ Xs @ Xa)[:3, 3]
        return (M @ Ph.T).T[:, :3], elbow

    # every capsule of every frame as arrays, so one evaluation is a few vectorised operations
    CA = np.array([[fr['joints'][a_] for a_, b_, r_ in CAPS] for fr in frames])     # (nf, nc, 3)
    CB = np.array([[fr['joints'][b_] for a_, b_, r_ in CAPS] for fr in frames])
    CR = np.array([r_ for a_, b_, r_ in CAPS])
    ra_i = [k for k, (a_, b_, r_) in enumerate(CAPS) if a_ == "RightArm"][0]

    def cost(x, detail=False):
        qa = qa0 @ rotvec_to_m(x[:3]); qf = qf0 @ rotvec_to_m(x[3:])
        c = 0.0; worst = 0.0; bad = 0
        for fi, fr in enumerate(frames):
            pts, elbow = axe_points(fr, qa, qf)
            A_ = CA[fi].copy(); B_ = CB[fi].copy()
            B_[ra_i] = elbow                     # the right arm's own upper half, posed by the solve
            ab = B_ - A_                                                       # (nc, 3)
            ap = pts[:, None, :] - A_[None, :, :]                              # (np, nc, 3)
            tt = np.clip((ap * ab[None]).sum(-1) / np.maximum((ab * ab).sum(-1), 1e-12)[None], 0.0, 1.0)
            d = np.linalg.norm(ap - tt[..., None] * ab[None], axis=-1) * MPU   # (np, nc)
            pen = np.maximum(0.0, CR[None] + MARGIN - d)
            c += float((pen ** 2).sum())
            worst = max(worst, float(pen.max()))
            bad += 1 if (pen > MARGIN).any() else 0
        prior = float(np.linalg.norm(x[:3]) ** 2 + np.linalg.norm(x[3:]) ** 2)
        tot = 1e4 * c + 0.05 * prior
        return (tot, worst, bad) if detail else tot

    base = cost(np.zeros(6), True)
    print("the standing guard through %s (%d frames): capsule cost %.4g, deepest %.3f m, %d frames reaching in"
          % (clip, len(frames), base[0], base[1], base[2]))
    best, bx = None, None
    rng = np.random.default_rng(11)
    for trial in range(10):
        x0 = np.zeros(6) if trial == 0 else rng.normal(0, 0.5, 6)
        r = minimize(cost, x0, method="Nelder-Mead", options=dict(maxfev=2500, xatol=1e-4, fatol=1e-9))
        if best is None or r.fun < best:
            best, bx = r.fun, r.x
    tot, worst, bad = cost(bx, True)
    qa = qa0 @ rotvec_to_m(bx[:3]); qf = qf0 @ rotvec_to_m(bx[3:])
    print("solved: capsule cost %.4g, deepest %.3f m, %d frames reaching in; arm moved %.1f deg (upper) %.1f deg (fore) from the standing guard"
          % (tot, worst, bad, math.degrees(np.linalg.norm(bx[:3])), math.degrees(np.linalg.norm(bx[3:]))))
    out = dict(pose={"RightShoulder": list(map(float, gp["RightShoulder"])), "RightArm": list(map(float, W.m2q(qa))),
                     "RightForeArm": list(map(float, W.m2q(qf))), "RightHand": list(map(float, gp["RightHand"]))},
               clip=clip, frames=len(frames), capsules=CAPS, margin_m=MARGIN,
               standing=dict(cost=base[0], deepest_m=base[1], frames_in=base[2]),
               solved=dict(cost=tot, deepest_m=worst, frames_in=bad, upper_deg=math.degrees(np.linalg.norm(bx[:3])), fore_deg=math.degrees(np.linalg.norm(bx[3:]))),
               _note="the axe arm's pose through the shield bash (bash_guard_solve.py); verdict in Godot on the real mesh")
    json.dump(out, open(outp, "w"), indent=1)
    print("wrote %s" % outp)


if __name__ == "__main__":
    main()
