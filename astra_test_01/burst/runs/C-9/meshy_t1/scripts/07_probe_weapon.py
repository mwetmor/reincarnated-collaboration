# C-9 meshy_t1: probe a weapon GLB -- long axis, which end is the head, grip zone.
import bpy, json, sys, os
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUTP = a[0], a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
ms = [o for o in sc.objects if o.type == 'MESH']
P = []
for o in ms:
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        P.append([w.x, w.y, w.z])
P = np.array(P)
lo, hi = P.min(0), P.max(0)
ext = hi - lo
axis = int(np.argmax(ext))
names = "xyz"
# slice along the long axis: radius profile tells head from butt
t = P[:, axis]
bins = np.linspace(t.min(), t.max(), 24)
prof = []
other = [i for i in range(3) if i != axis]
for i in range(len(bins) - 1):
    m = (t >= bins[i]) & (t < bins[i + 1])
    if m.sum() < 5:
        prof.append(0.0); continue
    q = P[m][:, other]
    prof.append(float(np.sqrt(((q - q.mean(0)) ** 2).sum(1)).mean()))
rep = dict(source=os.path.basename(SRC), meshes=[o.name for o in ms],
           verts=int(len(P)), bbox_lo=[round(float(v), 4) for v in lo],
           bbox_hi=[round(float(v), 4) for v in hi],
           extent=[round(float(v), 4) for v in ext],
           long_axis=names[axis], length=round(float(ext[axis]), 4),
           radius_profile=[round(v, 4) for v in prof],
           bin_edges=[round(float(v), 4) for v in bins])
half = len(prof) // 2
rep["head_end"] = "max" if sum(prof[half:]) > sum(prof[:half]) else "min"
# WHERE THE FAN POINTS, in the weapon's own frame. Same instrument as
# 15_blade_side: the head's bulk sits to one side of the haft axis, and its
# centroid offset from that axis is the fan's bearing. Needed to set the
# blade's 70 deg outboard bearing on the socket rather than by eye.
hz = [i for i, v in enumerate(prof) if v > 2.2 * np.median([x for x in prof if x > 0])]
if hz:
    z0 = bins[min(hz)]; z1 = bins[max(hz) + 1]
    m = (t >= z0) & (t <= z1)
    head = P[m]
    haft = P[(t > bins[2]) & (t < bins[min(hz) - 1])] if min(hz) > 3 else P
    ax = haft[:, other].mean(0)
    off = head[:, other].mean(0) - ax
    import math as _m
    rep["head_zone"] = [round(float(z0), 4), round(float(z1), 4)]
    rep["haft_axis_xy"] = [round(float(v), 5) for v in ax]
    rep["fan_offset_xy"] = [round(float(v), 5) for v in off]
    rep["fan_bearing_deg_from_+Y"] = round(float(_m.degrees(_m.atan2(off[0], off[1]))), 2)
    # reach each way, to confirm which side is the fan and which the fluke
    d = head[:, other] - ax
    u = off / max(float(np.linalg.norm(off)), 1e-9)
    proj = d @ u
    rep["fan_reach"] = round(float(proj.max()), 4)
    rep["fluke_reach"] = round(float(-proj.min()), 4)
json.dump(rep, open(OUTP, "w"), indent=1)
print("long axis %s length %.3f  head at the %s end" % (names[axis], ext[axis], rep["head_end"]))
print("radius profile:", [round(v, 3) for v in prof])
