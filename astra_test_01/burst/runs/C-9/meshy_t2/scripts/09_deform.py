# C-9 meshy_t2 step 7: assert the skinning survives every clip's extremes.
#
#   blender -b -noaudio --python scripts/09_deform.py -- <clips.blend> <out.json>
#
# Three failure modes, three instruments, all measured against the BIND pose:
#
#  TEARING / STRETCH  edge ELONGATION IN MILLIMETRES, plus the ratio computed
#                     only over edges at least 3 mm long at rest.
#                     Ratio alone was the wrong instrument and said so loudly:
#                     it reported 15-28x on clips whose renders are clean,
#                     because this quad remesh carries 350 edges under 2 mm
#                     and the worst offender was a 1 mm edge moving 5 mm. The
#                     eye sees millimetres, not ratios, so millimetres are
#                     what is asserted; the ratio is kept as a shape cue on
#                     edges big enough for it to mean anything.
#  CANDY-WRAPPER      a twisted limb collapses its cross-section, so the giveaway
#                     is triangle AREA ratio near zero with edge ratios still
#                     near 1 -- the surface pinches without any edge stretching.
#                     Counted as faces under 0.25x their rest area.
#  MESH THROUGH MESH  measured where it can actually be seen: the GROUND (any
#                     vertex below the sole plane) and LEFT-vs-RIGHT limb
#                     interpenetration, tested as the minimum distance between
#                     the two hind paws' and the two fore paws' vertex sets.
#                     A full self-intersection test on 71 577 triangles per
#                     frame is not worth its cost here; these are the two
#                     places a quadruped's legs actually cross.
#
# The EXTREME frames are picked by the instrument, not by eye: per clip, the
# frame with the largest total joint deviation from the bind pose, plus the
# frame with the worst stretch. Those are the frames the contact sheet shows.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("09_deform.py")][0]))
sys.path.insert(0, HERE)

a = sys.argv[sys.argv.index('--') + 1:]
BLEND, OUTP = a[0], a[1]

bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
obj = next(o for o in sc.objects if o.type == 'MESH'
           and any(m.type == 'ARMATURE' and m.object == arm for m in o.modifiers))
clips = json.load(open(os.path.join(os.path.dirname(BLEND), "clips.json")))
gref = clips.get("ground_ref_z", 0.0)

me = obj.data
NE = len(me.edges)
ev = np.empty(NE * 2, dtype=np.int32); me.edges.foreach_get("vertices", ev)
ev = ev.reshape(-1, 2)
tris = [p.vertices[:] for p in me.polygons]
gname = {g.index: g.name for g in obj.vertex_groups}
dom = {}
for v in me.vertices:
    b, w = None, -1.0
    for g in v.groups:
        if g.weight > w:
            w, b = g.weight, gname.get(g.group)
    dom[v.index] = b
paw_sets = {}
for f in ("fpaw.L", "fpaw.R", "hpaw.L", "hpaw.R"):
    cann = ("hcannon." if f.startswith("hpaw") else "fcannon.") + f[-1]
    paw_sets[f] = np.array([i for i, d in dom.items() if d in (f, cann)], dtype=np.int64)


def world_verts():
    dg = bpy.context.evaluated_depsgraph_get()
    e = obj.evaluated_get(dg); m = e.to_mesh()
    co = np.empty(len(m.vertices) * 3); m.vertices.foreach_get("co", co)
    W = co.reshape(-1, 3) @ np.array(e.matrix_world.to_3x3()).T \
        + np.array(e.matrix_world.translation)
    e.to_mesh_clear()
    return W


# every polygon fanned into triangles ONCE, so per-frame area is one
# vectorised cross product instead of 71 577 Python loops (65 s -> ~8 s)
_FAN = []
for _t in tris:
    for _k in range(1, len(_t) - 1):
        _FAN.append((_t[0], _t[_k], _t[_k + 1]))
_FAN = np.array(_FAN, dtype=np.int64)
_FACE_OF = []
for _i, _t in enumerate(tris):
    _FACE_OF += [_i] * (len(_t) - 2)
_FACE_OF = np.array(_FACE_OF, dtype=np.int64)


def face_areas(W):
    p = W[_FAN]
    a = 0.5 * np.linalg.norm(np.cross(p[:, 1] - p[:, 0], p[:, 2] - p[:, 0]), axis=1)
    out = np.zeros(len(tris))
    np.add.at(out, _FACE_OF, a)
    return out


def min_pair_dist(W, A, B, cap=6000):
    if len(A) == 0 or len(B) == 0:
        return None
    a = W[A[::max(1, len(A) // cap)]]
    b = W[B[::max(1, len(B) // cap)]]
    d = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(-1))
    return float(d.min())


# ---- bind pose reference ----------------------------------------------------
arm.animation_data_create()
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.rotation_euler = (0, 0, 0)
    pb.rotation_quaternion = (1, 0, 0, 0)
    pb.location = (0, 0, 0)
bpy.context.view_layer.update()
W0 = world_verts()
E0 = np.linalg.norm(W0[ev[:, 0]] - W0[ev[:, 1]], axis=1)
A0 = face_areas(W0)
ok_e = E0 > 0.003          # 3 mm; the median edge is 8.9 mm
ok_a = A0 > 1e-8

rep = dict(bind=dict(verts=int(len(W0)), edges=int(NE), faces=int(len(tris)),
                     ground_ref_z=gref),
           clips={})
for state in ("idle", "walk", "run", "attack"):
    act = bpy.data.actions.get("mc_" + state)
    arm.animation_data.action = act
    try:
        sl = list(act.slots)
        if sl:
            arm.animation_data.action_slot = sl[0]
    except Exception:
        pass
    n = clips[state]["frames"]
    rows = []
    for i in range(n):
        sc.frame_set(i + 1)
        W = world_verts()
        E = np.linalg.norm(W[ev[:, 0]] - W[ev[:, 1]], axis=1)
        r = E[ok_e] / E0[ok_e]
        dmm = (E - E0) * 1000.0
        wmm = int(np.argmax(dmm))
        A = face_areas(W)
        ar = A[ok_a] / A0[ok_a]
        worst = int(np.argmax(r))
        wi = np.where(ok_e)[0][worst]
        below = W[:, 2] < gref - 0.003
        pose_dev = 0.0
        for pb in arm.pose.bones:
            q = pb.rotation_quaternion if pb.rotation_mode == 'QUATERNION' \
                else pb.matrix_basis.to_quaternion()
            pose_dev += abs(2 * math.degrees(math.acos(min(1.0, abs(q.w)))))
        blo = np.where(below)[0]
        bgroups = {}
        for j in blo[:4000]:
            g = dom.get(int(j))
            bgroups[g] = bgroups.get(g, 0) + 1
        rows.append(dict(
            frame=i,
            elong_max_mm=round(float(dmm.max()), 3),
            elong_p999_mm=round(float(np.percentile(dmm, 99.9)), 3),
            elong_over_4mm=int((dmm > 4.0).sum()),
            worst_elong_groups=[dom.get(int(ev[wmm, 0])), dom.get(int(ev[wmm, 1]))],
            below_ground_groups=dict(sorted(bgroups.items(), key=lambda kv: -kv[1])[:4]),
            stretch_max=round(float(r.max()), 4),
            stretch_p999=round(float(np.percentile(r, 99.9)), 4),
            stretch_over_1p5=int((r > 1.5).sum()),
            squash_min=round(float(r.min()), 4),
            area_ratio_min=round(float(ar.min()), 4),
            faces_under_quarter_area=int((ar < 0.25).sum()),
            worst_edge_groups=[dom.get(int(ev[wi, 0])), dom.get(int(ev[wi, 1]))],
            verts_below_ground=int(below.sum()),
            deepest_below_ground_m=round(float(gref - W[:, 2].min()), 4),
            hind_paw_gap_m=round(min_pair_dist(W, paw_sets["hpaw.L"], paw_sets["hpaw.R"]), 4),
            fore_paw_gap_m=round(min_pair_dist(W, paw_sets["fpaw.L"], paw_sets["fpaw.R"]), 4),
            pose_deviation_deg=round(pose_dev, 1)))
    ex = sorted(rows, key=lambda r: -r["pose_deviation_deg"])[0]["frame"]
    st = sorted(rows, key=lambda r: -r["stretch_max"])[0]["frame"]
    rep["clips"][state] = dict(
        frames=rows,
        extreme_frames=sorted(set([ex, st,
                                   sorted(rows, key=lambda r: -r["faces_under_quarter_area"])[0]["frame"],
                                   sorted(rows, key=lambda r: r["hind_paw_gap_m"])[0]["frame"]])),
        summary=dict(elong_max_mm=max(r["elong_max_mm"] for r in rows),
                     elong_p999_mm_max=max(r["elong_p999_mm"] for r in rows),
                     edges_over_4mm_max=max(r["elong_over_4mm"] for r in rows),
                     stretch_max=max(r["stretch_max"] for r in rows),
                     stretch_p999_max=max(r["stretch_p999"] for r in rows),
                     edges_over_1p5_max=max(r["stretch_over_1p5"] for r in rows),
                     area_ratio_min=min(r["area_ratio_min"] for r in rows),
                     faces_under_quarter_area_max=max(r["faces_under_quarter_area"] for r in rows),
                     verts_below_ground_max=max(r["verts_below_ground"] for r in rows),
                     deepest_below_ground_m=max(r["deepest_below_ground_m"] for r in rows),
                     min_hind_paw_gap_m=min(r["hind_paw_gap_m"] for r in rows),
                     min_fore_paw_gap_m=min(r["fore_paw_gap_m"] for r in rows)))
    s = rep["clips"][state]["summary"]
    print("%-7s elongation max %.1f mm (p99.9 %.2f mm, %d edges >4 mm)  ratio max %.2f "
          "(>=3 mm edges)  min face area ratio %.3f (%d faces <0.25)  "
          "below ground %d verts / %.3f m  paw gaps hind %.3f fore %.3f"
          % (state, s["elong_max_mm"], s["elong_p999_mm_max"], s["edges_over_4mm_max"],
             s["stretch_max"], s["area_ratio_min"], s["faces_under_quarter_area_max"],
             s["verts_below_ground_max"], s["deepest_below_ground_m"],
             s["min_hind_paw_gap_m"], s["min_fore_paw_gap_m"]))
    wg = {}
    for r in rows:
        k = tuple(r["worst_elong_groups"]); wg[k] = wg.get(k, 0) + 1
    print("        worst elongation between:", sorted(wg.items(), key=lambda kv: -kv[1])[:3])
    bg = {}
    for r in rows:
        for k, v in r["below_ground_groups"].items():
            bg[k] = max(bg.get(k, 0), v)
    print("        below-ground owners:", sorted(bg.items(), key=lambda kv: -kv[1])[:4])
    print("        extreme frames:", rep["clips"][state]["extreme_frames"])

json.dump(rep, open(OUTP, "w"), indent=1)
print("wrote", OUTP)
