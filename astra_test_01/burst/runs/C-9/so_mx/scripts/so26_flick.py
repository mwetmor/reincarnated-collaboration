# so_mx R-C9-134 flick check: the orb staff's AXIS (weapon_r frame: grip -> tip) per key, its angular speed (deg/s) and the
# same for the HAND (RightHand's own rotation), on two bodies (before/after the clamp) over a window.
#   so26_flick.py <clip> <t0> <t1> <body.glb> [<body.glb>]
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure')
TIP = np.array(json.load(open(os.path.join(HERE, '..', 'pieces', 'm2', 'mount.json')))['orbstaff']['tip_in_weapon_r_local'])
clip, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
for body in sys.argv[4:]:
    m = C.model(body); ts = np.round(np.arange(t0, t1 + 1e-9, 1 / 120.0), 5)
    ax, hx = [], []
    for x in ts:
        G = C.globals_at(m, clip, float(x)); R = G[m['nid']['weapon_r']][:3, :3]; a = R @ TIP; ax.append(a / np.linalg.norm(a))
        Rh = G[m['nid']['RightHand']][:3, :3]; hx.append(Rh / np.linalg.norm(Rh, axis=0))
    ax = np.array(ax); w = np.degrees(np.arccos(np.clip((ax[1:] * ax[:-1]).sum(1), -1, 1))) * 120
    wh = [np.degrees(np.arccos(np.clip((np.trace(hx[i].T @ hx[i + 1]) - 1) / 2, -1, 1))) * 120 for i in range(len(hx) - 1)]
    print("== %s" % os.path.relpath(body))
    print("  t      staff deg/s   hand deg/s   staff-minus-hand")
    for i in range(len(w)): print("  %.4f  %8.0f   %8.0f   %8.0f" % (ts[i + 1], w[i], wh[i], w[i] - wh[i]))
