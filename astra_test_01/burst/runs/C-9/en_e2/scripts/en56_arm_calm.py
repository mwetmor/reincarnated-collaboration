# EN-E2 (C-9 Phase 2, R-C9-135 boss paint pass): how CALM is a locomotion/idle clip's arm carriage? Per clip, over every key:
# each upper arm's elevation from hanging straight down (deg; 0 = at the side, 90 = level, >90 = above the shoulder) and each
# hand's height above its shoulder joint (m, negative = below). The caster set's raised forearm reads wrong on plate; this
# picks the calmest source by measurement, not by eye.
#   python3 scripts/en56_arm_calm.py <clip.glb>[:<anim>] ...      (Mixamo-renamed GLBs from e40a, or a body GLB with :clip)
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); C = __import__('s17_loop_closure')
for spec in sys.argv[1:]:
    path, _, clip = spec.partition(':'); m = C.model(path); clip = clip or next(iter(m['anims']))
    T = sorted({float(t) for ch in m['anims'][clip].values() for t in ch[0]}); nid = m['nid']
    up = None; out = {}
    for side in ('Left', 'Right'):
        el, hh, fe = [], [], []
        for t in T:
            G = C.globals_at(m, clip, t)
            if up is None:
                hp, hd = G[nid['Hips']][:3, 3], G[nid['Head']][:3, 3]; up = (hd - hp) / np.linalg.norm(hd - hp)   # the body's own up at frame 0
            a, f, h = (G[nid[side + n]][:3, 3] for n in ('Arm', 'ForeArm', 'Hand'))
            d = (f - a) / np.linalg.norm(f - a); el.append(np.degrees(np.arccos(np.clip(-d @ up, -1, 1))))
            hh.append((h - a) @ up); L = np.linalg.norm(f - a) + np.linalg.norm(h - f); fe.append(hh[-1] / L)
        out[side] = (max(el), float(np.mean(el)), max(fe), float(np.mean(fe)))
    print('CALM %-40s %-22s keys %3d | L arm elev max %5.1f mean %5.1f hand/arm max %+.2f mean %+.2f | R arm elev max %5.1f mean %5.1f hand/arm max %+.2f mean %+.2f'
          % (os.path.basename(path), clip[:22], len(T), *out['Left'], *out['Right']))
