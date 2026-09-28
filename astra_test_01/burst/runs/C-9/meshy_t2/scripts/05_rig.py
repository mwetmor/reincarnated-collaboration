# C-9 meshy_t2 step 4b: fit a quadruped skeleton to the Meshy manticore and skin
# it. Meshy's own auto-rig is BIPED-ONLY, so this is the "Opus rigs in Blender"
# route applied to a creature.
#
#   blender -b -noaudio --python scripts/05_rig.py -- <model.glb> <rigmeas.json>
#                                                     <out.blend> <out.json>
#
# The landmark table below carries a `src` for every joint:
#   "measured"    read straight off the mesh (step 4a)
#   "derived"     computed from measured points (belly line, topline, midline)
#   "anatomical"  a canine proportion applied to measured endpoints, because
#                 the joint is buried in solid muscle and no surface statistic
#                 finds it (the hip and the shoulder joint are the only two).
#
# NO JAW. Measured, not assumed: the head render at work/head_*.png shows a
# painted closed mouth under a full moustache and beard, with the beard fused
# continuously into the chest ruff. There is no mouth opening and no jaw seam,
# so a jaw bone would tear the beard rather than open a mouth. Reported instead
# of faked.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("05_rig.py")][0]))
sys.path.insert(0, HERE)
import t2lib as T

a = sys.argv[sys.argv.index('--') + 1:]
SRC, MEAS, OUTBLEND, OUTP = a[0], a[1], a[2], a[3]

# ---------------------------------------------------------------- landmarks
# (x, y, z) in metres, canonical frame, withers = 1.00
LM = {
    # spine, from the midline profile: z = belly + 0.75 * (back - belly)
    "sacrum":     ((0.000, -0.100, 0.755), "derived"),
    "lumbar":     ((0.000,  0.070, 0.750), "derived"),
    "thorax_mid": ((0.000,  0.240, 0.748), "derived"),
    "thorax_fwd": ((0.000,  0.410, 0.775), "derived"),
    "withers":    ((0.000,  0.530, 0.830), "derived"),
    "neck_base":  ((0.000,  0.620, 0.900), "derived"),
    "atlas":      ((0.000,  0.700, 0.965), "derived"),
    "skull_top":  ((0.000,  0.755, 1.175), "measured"),
    "tail_root":  ((0.000, -0.280, 0.672), "derived"),
    # hind limb, right side; mirrored for the left
    "hip":        ((0.092, -0.235, 0.662), "anatomical"),
    "stifle":     ((0.125, -0.190, 0.470), "derived"),
    "hock":       ((0.150, -0.373, 0.119), "measured"),
    "h_heel":     ((0.150, -0.320, 0.028), "measured"),
    "h_toe":      ((0.150, -0.238, 0.010), "measured"),
    # fore limb, right side
    "scap_top":   ((0.070,  0.520, 0.880), "derived"),
    "shoulder":   ((0.105,  0.645, 0.680), "anatomical"),
    "elbow":      ((0.105,  0.590, 0.450), "measured"),
    "carpus":     ((0.100,  0.593, 0.105), "measured"),
    "f_heel":     ((0.112,  0.630, 0.028), "measured"),
    "f_toe":      ((0.115,  0.742, 0.010), "measured"),
}
N_TAIL = 7


def mirror(p):
    return (-p[0], p[1], p[2])


def tail_curve(meas):
    """Sample the measured tail centreline, extended into the rump by the
    midline profile, at N_TAIL+1 equal-arclength stations."""
    pts = []
    for y, zb, zt, n in meas["midline_profile"]["data"]:
        if -0.46 < y < -0.27:
            pts.append((y, (zb + zt) / 2.0))
    for y, x, z, r, n in meas["tail_centreline"]["data"]:
        pts.append((y, z))
    pts = sorted(set(pts), reverse=True)          # from the root backwards
    pts = [LM["tail_root"][0][1:]] + [p for p in pts if p[0] < LM["tail_root"][0][1]]
    P = np.array(pts)
    d = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    tt = np.linspace(0, d[-1], N_TAIL + 1)
    ys = np.interp(tt, d, P[:, 0]); zs = np.interp(tt, d, P[:, 1])
    return [(0.0, float(y), float(z)) for y, z in zip(ys, zs)], float(d[-1])


def build_bones(amt, meas):
    L = {k: v[0] for k, v in LM.items()}
    tail_pts, tail_len = tail_curve(meas)
    spec = []           # (name, parent, head, tail, connected)
    spec.append(("root", None, (0.0, -0.100, 0.0), (0.0, 0.100, 0.0), False))
    spec.append(("hips", "root", L["sacrum"], L["tail_root"], False))
    for i in range(N_TAIL):
        spec.append(("tail_%02d" % (i + 1), "hips" if i == 0 else "tail_%02d" % i,
                     tail_pts[i], tail_pts[i + 1], i > 0))
    spec.append(("spine_01", "hips", L["sacrum"], L["lumbar"], False))
    spec.append(("spine_02", "spine_01", L["lumbar"], L["thorax_mid"], True))
    spec.append(("spine_03", "spine_02", L["thorax_mid"], L["thorax_fwd"], True))
    spec.append(("chest", "spine_03", L["thorax_fwd"], L["withers"], True))
    spec.append(("neck_01", "chest", L["withers"], L["neck_base"], True))
    spec.append(("neck_02", "neck_01", L["neck_base"], L["atlas"], True))
    spec.append(("head", "neck_02", L["atlas"], L["skull_top"], True))
    for s, f in (("R", lambda p: p), ("L", mirror)):
        spec += [
            ("shoulder." + s, "chest", f(L["scap_top"]), f(L["shoulder"]), False),
            ("upperarm." + s, "shoulder." + s, f(L["shoulder"]), f(L["elbow"]), True),
            ("forearm." + s, "upperarm." + s, f(L["elbow"]), f(L["carpus"]), True),
            ("fcannon." + s, "forearm." + s, f(L["carpus"]), f(L["f_heel"]), True),
            ("fpaw." + s, "fcannon." + s, f(L["f_heel"]), f(L["f_toe"]), True),
            ("thigh." + s, "hips", f(L["hip"]), f(L["stifle"]), False),
            ("shin." + s, "thigh." + s, f(L["stifle"]), f(L["hock"]), True),
            ("hcannon." + s, "shin." + s, f(L["hock"]), f(L["h_heel"]), True),
            ("hpaw." + s, "hcannon." + s, f(L["h_heel"]), f(L["h_toe"]), True),
        ]
    eb = amt.edit_bones
    for name, parent, h, t, conn in spec:
        b = eb.new(name)
        b.head = Vector(h); b.tail = Vector(t)
        if parent:
            b.parent = eb[parent]
            b.use_connect = bool(conn)
    # ROLL: every bone gets its local Z pointing at world +Z where it can, so
    # local X lands on world +X and one convention -- "rotate about local X,
    # positive swings the tail of the bone forward/up" -- holds for the whole
    # rig. Without this, roll comes out of Blender's default per-bone and the
    # same keyed number means a different motion on each limb.
    # A near-VERTICAL bone cannot align its local Z to world +Z -- Z must be
    # perpendicular to the bone, so for a bone pointing straight down every
    # roll is equally "close to +Z" and Blender falls back to an arbitrary
    # one. Vertical bones (every leg segment) therefore align to world +Y
    # instead, which is well-conditioned for them and lands local X on world
    # +X just the same.
    for b in eb:
        d = (b.tail - b.head).normalized()
        b.align_roll(Vector((0.0, 1.0, 0.0)) if abs(d.z) > 0.65
                     else Vector((0.0, 0.0, 1.0)))
    return spec, tail_len


def region_grow_head(me, C, P):
    """The man's head: seed on the strongly warm texels inside the head box,
    then grow over edges while the texel stays warm. A flat colour threshold
    alone returns 12 554 vertices spread over the whole animal (the manuscript
    palette is warm everywhere); the seed + grow returns the head."""
    d = C[:, 0] - C[:, 2]
    seed = (d > 0.28) & (P[:, 1] > 0.55) & (P[:, 2] > 0.82)
    grow_ok = (d > 0.16) & (P[:, 1] > 0.50) & (P[:, 2] > 0.78)
    ev = np.empty(len(me.edges) * 2, dtype=np.int32)
    me.edges.foreach_get("vertices", ev)
    ev = ev.reshape(-1, 2)
    adj = {}
    for u, v in ev:
        adj.setdefault(int(u), []).append(int(v))
        adj.setdefault(int(v), []).append(int(u))
    st = list(np.where(seed)[0])
    inside = set(int(i) for i in st)
    while st:
        x = st.pop()
        for y in adj.get(x, ()):
            if y not in inside and grow_ok[y]:
                inside.add(y); st.append(y)
    return np.array(sorted(inside), dtype=np.int64)


def main():
    meas = json.load(open(MEAS))
    sc, objs, info = T.load_canonical(bpy, SRC)
    obj = objs[0]
    P = T.verts_world(objs)
    C = T.vertex_colours_from_texture(obj)

    amt_data = bpy.data.armatures.new("manticore")
    arm = bpy.data.objects.new("manticore_rig", amt_data)
    sc.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    arm.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    spec, tail_len = build_bones(amt_data, meas)
    bpy.ops.object.mode_set(mode='OBJECT')

    # ---- WELD BEFORE SKINNING ---------------------------------------------
    # Bone heat needs a connected surface. The glTF importer splits a vertex
    # per UV/normal seam, so this 48 195-vertex mesh arrives as thousands of
    # coincident-but-separate vertices: V - E + F = 48195 - 119020 + 71577 =
    # 752, nothing like the 2 a closed surface gives. Heat then solves only
    # the shells it can reach.
    #
    # It does not say so. `parent_set(ARMATURE_AUTO)` returned without an
    # error and the rig posed and rendered; the failure only surfaced when the
    # deformation assert traced a 122 mm tear on the sternum back to vertices
    # carrying exactly one group at weight 1.0 -- and counting them gave
    # 35 996 of 48 195, three quarters of the animal, skinned by the fallback
    # rather than by heat. The operator succeeding is not the operator
    # working.
    #
    # Welding is safe for the look: UVs are per-LOOP in Blender, so the
    # texture seams survive the merge; only the duplicated vertices go.
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    n_before = len(obj.data.vertices)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=1e-4)
    bpy.ops.object.mode_set(mode='OBJECT')
    n_after = len(obj.data.vertices)
    print("weld: %d -> %d verts (%d duplicates removed)"
          % (n_before, n_after, n_before - n_after))

    # ---- skin: bone heat ---------------------------------------------------
    for o in bpy.context.selected_objects:
        o.select_set(False)
    obj.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    heat_ok = True
    try:
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    except RuntimeError as e:
        heat_ok = False
        print("bone heat FAILED:", e)
        bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')

    me = obj.data
    P = T.verts_world([obj])          # re-read: the weld renumbered vertices
    gi = {g.name: g.index for g in obj.vertex_groups}
    names = [b.name for b in amt_data.bones]

    # ---- FIX 1: no cross-body bleed ---------------------------------------
    # The paws pass within 0.23 m of each other and bone heat leaks across.
    # Any vertex clearly on one side loses every group belonging to the other.
    W = np.zeros((len(me.vertices), len(names)), dtype=np.float32)
    idx = {n: i for i, n in enumerate(names)}
    for v in me.vertices:
        for g in v.groups:
            nm = obj.vertex_groups[g.group].name
            if nm in idx:
                W[v.index, idx[nm]] = g.weight
    rcols = [i for n, i in idx.items() if n.endswith(".R")]
    lcols = [i for n, i in idx.items() if n.endswith(".L")]
    right = P[:, 0] > 0.03
    left = P[:, 0] < -0.03
    bled = float(W[right][:, lcols].sum() + W[left][:, rcols].sum())
    W[np.ix_(right, lcols)] = 0.0
    W[np.ix_(left, rcols)] = 0.0

    # ---- FIX 2: the man's head is RIGID -----------------------------------
    C = T.vertex_colours_from_texture(obj)      # re-sample after the weld
    head_idx = region_grow_head(me, C, P) if C is not None else np.array([], dtype=np.int64)
    hcol = idx["head"]
    if len(head_idx):
        W[head_idx, :] = 0.0
        W[head_idx, hcol] = 1.0
        # feather outward so the hair-to-ruff boundary is a blend, not a crease
        H = P[head_idx]
        tree_pts = H
        near = np.where((P[:, 1] > 0.40) & (P[:, 2] > 0.60))[0]
        near = np.array([i for i in near if i not in set(head_idx.tolist())])
        if len(near):
            d = np.sqrt(((P[near][:, None, :] - tree_pts[None, :, :]) ** 2).sum(-1)).min(1) \
                if len(tree_pts) * len(near) < 4e7 else None
            if d is None:
                d = np.array([np.sqrt(((tree_pts - P[i]) ** 2).sum(1)).min() for i in near])
            F = 0.055
            t = np.clip(1.0 - d / F, 0.0, 1.0)
            for k, i in enumerate(near):
                if t[k] <= 0:
                    continue
                W[i] *= (1.0 - t[k])
                W[i, hcol] += t[k]

    # ---- FIX 3: normalise, and cap at 4 influences ------------------------
    s = W.sum(1, keepdims=True)
    dead = (s[:, 0] < 1e-6)
    n_dead = int(dead.sum())
    if dead.any():
        # Vertices bone heat could not solve. These are real: this mesh's
        # BELLY MIDLINE between the front legs gets no heat at all.
        #
        # Giving each one the single NEAREST bone at weight 1.0 was a quiet
        # disaster. On the belly midline the four nearest bones are within
        # 11 mm of each other in distance -- upperarm.R 0.274, upperarm.L
        # 0.274, spine_03 0.283, spine_02 0.285 -- so a tie was broken by
        # rounding, and two ADJACENT belly vertices 10 mm apart ended up
        # rigid to OPPOSITE FRONT LEGS. When the legs scissored in the walk,
        # that 10 mm edge stretched to 122 mm. The deformation assert found
        # it: worst-elongation pairs came back as (upperarm.R, upperarm.L),
        # at x = +-0.002 on the sternum, with every one of those vertices
        # carrying exactly ONE group at weight 1.000.
        #
        # Inverse-square distance over the four nearest bones instead: on the
        # belly that yields ~0.25 each and the surface moves with their mean,
        # which is what a belly does.
        for i in np.where(dead)[0]:
            ds = []
            for j, n in enumerate(names):
                b = amt_data.bones[n]
                h, t = np.array(b.head_local), np.array(b.tail_local)
                v = t - h; L2 = float(v @ v) or 1e-9
                u = float(np.clip((P[i] - h) @ v / L2, 0, 1))
                ds.append((float(np.linalg.norm(P[i] - (h + u * v))), j))
            ds.sort()
            wsum = 0.0
            for dd, j in ds[:4]:
                w = 1.0 / max(dd, 1e-3) ** 2
                W[i, j] = w; wsum += w
            W[i] /= wsum
        s = W.sum(1, keepdims=True)
    order = np.argsort(-W, axis=1)
    mask = np.zeros_like(W, dtype=bool)
    rows = np.arange(len(W))[:, None]
    mask[rows, order[:, :4]] = True
    W = W * mask
    W /= np.maximum(W.sum(1, keepdims=True), 1e-9)

    for g in list(obj.vertex_groups):
        obj.vertex_groups.remove(g)
    groups = {n: obj.vertex_groups.new(name=n) for n in names}
    for j, n in enumerate(names):
        col = W[:, j]
        nz = np.where(col > 1e-4)[0]
        g = groups[n]
        for i in nz:
            g.add([int(i)], float(col[i]), 'REPLACE')

    rep = dict(canonical=info, bones=len(names), bone_names=names,
               n_tail_bones=N_TAIL, tail_length_m=round(tail_len, 4),
               bone_heat=heat_ok,
               landmarks={k: dict(p=[round(c, 4) for c in v[0]], src=v[1])
                          for k, v in LM.items()},
               head_island_verts=int(len(head_idx)),
               cross_body_weight_removed=round(bled, 3),
               bone_heat_unsolved_vertices=n_dead,
               vertices=int(len(me.vertices)),
               welded=dict(before=n_before, after=n_after,
                           removed=n_before - n_after),
               jaw=dict(built=False,
                        reason="closed painted mouth under a full beard; the beard is "
                               "continuous with the chest ruff -- no mouth opening and no "
                               "jaw seam exists to drive"),
               role_map=dict(hips="hips", spine="spine_02", chest="chest", neck="neck_01",
                             head="head", root="root",
                             l_foot="hpaw.L", r_foot="hpaw.R",
                             l_frontfoot="fpaw.L", r_frontfoot="fpaw.R",
                             feet=["fpaw.L", "fpaw.R", "hpaw.L", "hpaw.R"]),
               skinned_mesh=obj.name,
               character=dict(withers_m=T.TARGET_WITHERS_M,
                              head_top_m=round(float(P[:, 2].max()), 4),
                              length_m=round(float(P[:, 1].max() - P[:, 1].min()), 4),
                              width_m=round(float(P[:, 0].max() - P[:, 0].min()), 4)))
    bpy.ops.wm.save_as_mainfile(filepath=OUTBLEND)
    json.dump(rep, open(OUTP, "w"), indent=1)
    print("%d bones, %d verts, bone-heat=%s, head island %d verts, "
          "cross-body weight removed %.2f, tail %.3f m"
          % (len(names), len(me.vertices), heat_ok, len(head_idx), bled, tail_len))
    print("character:", rep["character"])


main()
