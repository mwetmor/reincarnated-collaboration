# Clip duration, travel and speed read from the SHIPPED GLB -- no fps anywhere.
#
#   python3 scripts/46_clip_timing.py <x.glb> [clip ...]
#
# glTF animation sampler inputs are TIMES IN SECONDS. Frame counts and fps are
# an authoring-side detail that does not survive into the file, and assuming
# one is how the manifest came to claim 0.667 s for a clip that is 0.7917 s:
# I used FPS = 30.0 and Blender's scene is 24, and I divided by the KEY COUNT
# (20) where the duration spans the INTERVALS (19). Two errors, same direction,
# 19% of speed between them -- which is the foot slide the scene measured.
import json, struct, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
L = __import__('21_lint_export')


def timing(path, want=None):
    g, bin_ = L.load_glb(path)
    nodes = g.get('nodes', [])
    parent = {}
    for i, nd in enumerate(nodes):
        for c in nd.get('children', []):
            parent[c] = i
    joints = set()
    for sk in g.get('skins', []):
        joints.update(sk.get('joints', []))
    roots = [j for j in joints if parent.get(j) not in joints]
    MPU, k = 1.0, parent.get(roots[0]) if roots else None
    while k is not None:
        MPU *= float(nodes[k].get('scale', [1, 1, 1])[1])
        k = parent.get(k)
    out = {}
    for an in g.get('animations', []):
        cn = an.get('name', '?')
        if want and cn not in want:
            continue
        t0, t1, trav, keys = None, None, None, None
        for ch in an.get('channels', []):
            smp = an['samplers'][ch['sampler']]
            tt = L.read_accessor(g, bin_, smp['input'])[:, 0]
            if t0 is None or tt.min() < t0:
                t0 = float(tt.min())
            if t1 is None or tt.max() > t1:
                t1 = float(tt.max())
            t = ch.get('target', {})
            if t.get('node') in roots and t.get('path') == 'translation':
                v = L.read_accessor(g, bin_, smp['output'])
                trav = float(np.hypot(v[-1][0] - v[0][0], v[-1][2] - v[0][2])) * MPU
                keys = len(v)
                # horizontal excursion around the line of travel: the SWAY
                n = len(v)
                s = np.linspace(0, 1, n)
                res = []
                for ax in (0, 2):
                    fit = np.polyval(np.polyfit(s, v[:, ax], 1), s)
                    res.append(v[:, ax] - fit)
                out.setdefault(cn, {})['hip_sway_m'] = round(
                    float(np.hypot(*[np.ptp(r) for r in res])) * MPU, 4)
        dur = (t1 - t0) if (t0 is not None and t1 is not None) else 0.0
        rec = out.setdefault(cn, {})
        rec.update(seconds=round(dur, 4), root_keys=keys,
                   net_travel_m=(round(trav, 4) if trav is not None else None),
                   speed_m_s=(round(trav / dur, 3) if trav and dur > 1e-6 else None))
    return out, MPU


if __name__ == '__main__':
    p = sys.argv[1]
    want = set(sys.argv[2:]) or None
    out, mpu = timing(p, want)
    print("%s   (%.8f m per glTF unit)" % (p.split('/')[-1], mpu))
    print("  %-22s %9s %6s %11s %10s %10s" %
          ("clip", "seconds", "keys", "travel_m", "speed_m_s", "hip_sway_m"))
    for cn in sorted(out):
        r = out[cn]
        print("  %-22s %9.4f %6s %11s %10s %10s"
              % (cn, r["seconds"], r.get("root_keys", "-"),
                 r.get("net_travel_m", "-"), r.get("speed_m_s", "-"),
                 r.get("hip_sway_m", "-")))
