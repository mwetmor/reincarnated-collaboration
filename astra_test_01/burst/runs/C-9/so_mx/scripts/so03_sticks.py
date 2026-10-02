# so_mx S2: stick-figure contact sheet of Mixamo clips (source rig), 8 samples per clip, FRONT (x,y) and SIDE (z,y) views,
# right side drawn red, left blue, so which hand leads and how high is visible at a glance.  python3 so03_sticks.py <out.png> <glb>...
import sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
G = __import__('55_clip_graft'); L = __import__('21_lint_export')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
BONES = [("Hips", "Spine02"), ("Spine02", "Spine01"), ("Spine01", "Spine"), ("Spine", "neck"), ("neck", "Head"),
         ("Spine", "LeftShoulder"), ("LeftShoulder", "LeftArm"), ("LeftArm", "LeftForeArm"), ("LeftForeArm", "LeftHand"),
         ("Spine", "RightShoulder"), ("RightShoulder", "RightArm"), ("RightArm", "RightForeArm"), ("RightForeArm", "RightHand"),
         ("Hips", "LeftUpLeg"), ("LeftUpLeg", "LeftLeg"), ("LeftLeg", "LeftFoot"), ("LeftFoot", "LeftToeBase"),
         ("Hips", "RightUpLeg"), ("RightUpLeg", "RightLeg"), ("RightLeg", "RightFoot"), ("RightFoot", "RightToeBase")]
OUT, files = sys.argv[1], sys.argv[2:]; N = 8
fig, axs = plt.subplots(len(files) * 2, N, figsize=(N * 1.6, len(files) * 2 * 1.9))
for r, p in enumerate(files):
    js, b = L.load_glb(p); nm = {n.get('name'): i for i, n in enumerate(js['nodes'])}
    an = js['animations'][0]; trk = G.tracks(js, b, an)
    T = sorted(set(float(t) for tr in trk.values() for (tt, _, _) in tr.values() for t in tt))
    for c, t in enumerate(np.linspace(0, T[-1], N)):
        Gw, _ = G.globals_from(js, G.local_mats(js, trk, t, True))
        X = {n: Gw[nm[n]][:3, 3] for n in nm if n in {x for bb in BONES for x in bb}}
        h = X['Hips']
        for v, (ix, lab) in enumerate(((0, 'front'), (2, 'side'))):
            ax = axs[r * 2 + v, c]; ax.set_aspect('equal'); ax.axis('off')
            for a_, b_ in BONES:
                col = 'r' if 'Right' in a_ + b_ else ('b' if 'Left' in a_ + b_ else 'k')
                ax.plot([X[a_][ix] - h[ix], X[b_][ix] - h[ix]], [X[a_][1], X[b_][1]], col, lw=1.2)
            ax.set_xlim(-110, 110) if abs(X['Head'][1]) > 10 else ax.set_xlim(-1.1, 1.1)
            if c == 0: ax.set_title("%s %s" % (os.path.basename(p)[:-4], lab), fontsize=7, loc='left')
            else: ax.set_title("%.2fs" % t, fontsize=6)
plt.tight_layout(); plt.savefig(OUT, dpi=70); print(OUT)
