# so_mx R-C9-134 release check: the orb TIP (mount.json tip_in_weapon_r_local, on the clamped weapon_r channel) and the
# casting arm, per key of the shipped clip, pure glTF. Per key: tip forward velocity (+Z, her facing at rest), tip speed,
# tip height, arm extension = |RightArm -> RightHand| / its max over the clip, elbow angle.  so25_release_tip.py <body.glb> <clip>...
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure')
TIP = np.array(json.load(open(os.path.join(HERE, '..', 'pieces', 'm2', 'mount.json')))['orbstaff']['tip_in_weapon_r_local'] + [1.0])
m = C.model(sys.argv[1]); out = {}
for clip in sys.argv[2:]:
    t = np.unique(np.round(np.concatenate([v[0] for v in m['anims'][clip].values()]), 6))
    tip, sh, el, ha = [], [], [], []
    for x in t:
        G = C.globals_at(m, clip, float(x))
        tip.append((G[m['nid']['weapon_r']] @ TIP)[:3]); sh.append(G[m['nid']['RightArm']][:3, 3]); el.append(G[m['nid']['RightForeArm']][:3, 3]); ha.append(G[m['nid']['RightHand']][:3, 3])
    tip, sh, el, ha = map(np.array, (tip, sh, el, ha))
    dt = np.diff(t); v = np.diff(tip, axis=0) / dt[:, None]
    ext = np.linalg.norm(ha - sh, axis=1); ext = ext / ext.max()
    u1 = sh - el; u2 = ha - el
    elbow = np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / np.linalg.norm(u1, axis=1) / np.linalg.norm(u2, axis=1), -1, 1)))
    rows = [dict(i=i, t=round(float(t[i]), 4), tip_vfwd=round(float(v[i - 1, 2]), 2) if i else 0.0, tip_vdown=round(float(-v[i - 1, 1]), 2) if i else 0.0,
                 tip_speed=round(float(np.linalg.norm(v[i - 1])), 2) if i else 0.0, tip_y=round(float(tip[i, 1]), 3), tip_z=round(float(tip[i, 2]), 3),
                 ext=round(float(ext[i]), 3), elbow=round(float(elbow[i]), 1)) for i in range(len(t))]
    out[clip] = rows
    print("== %s  %d keys, %.4f s" % (clip, len(t), t[-1]))
    for r in rows: print("  %3d %.4f  vfwd %6.2f vdown %6.2f speed %6.2f  tip y %.3f z %+.3f  ext %.3f elbow %5.1f" % tuple(r[k] for k in ('i', 't', 'tip_vfwd', 'tip_vdown', 'tip_speed', 'tip_y', 'tip_z', 'ext', 'elbow')))
json.dump(out, open(os.path.join(HERE, '..', 'work', 'release_tip.json'), 'w'), indent=1)
