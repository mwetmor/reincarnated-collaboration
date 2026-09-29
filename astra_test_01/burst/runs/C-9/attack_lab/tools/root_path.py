"""Each strike's Hips path, in metres: where it starts, where it ends, how far it goes.
A rooted one-shot that ENDS somewhere other than where it started snaps back on its fade-out
by exactly that much; a linear de-root turns the same displacement into a steady slide."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gltf_anim import clips
M_PER_UNIT = 0.0108823   # the armature node scale, from the file
for path, want in [a.split('::') for a in sys.argv[1:]]:
    C = clips(path)
    for clip in [c for c in want.split(',')]:
        t, v, _ = C[clip]['Hips']['translation']
        up = int(np.argmax(np.abs(v.mean(axis=0))))          # the axis carrying hip height
        hz = [i for i in range(3) if i != up]
        h = v[:, hz] * M_PER_UNIT
        rel = h - h[0]
        dist = np.linalg.norm(rel, axis=1)
        step = np.linalg.norm(np.diff(h, axis=0), axis=1)
        i_max = int(np.argmax(dist)); i_st = int(np.argmax(step))
        net = float(np.linalg.norm(rel[-1]))
        print("%-12s %5.2f s  net %.3f m | farthest %.3f m at t=%.2f s | fastest %.1f mm/key at t=%.2f s | height %.2f..%.2f m"
              % (clip, t[-1], net, dist[i_max], t[i_max], step[i_st] * 1000, t[i_st + 1],
                 v[:, up].min() * M_PER_UNIT, v[:, up].max() * M_PER_UNIT))
