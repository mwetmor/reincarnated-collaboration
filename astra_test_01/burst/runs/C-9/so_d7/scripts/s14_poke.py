# BODY POKE-THROUGH under the garments, per clip, on the pose the player sees (the staff layer).
#
#   blender -b -noaudio --python scripts/s14_poke.py -- <full.glb> <staff_carry.json> <out.json> [--step 4]
#
# The pass-2 speckle stills, posed through the staff layer and over five clips, found thin red
# slivers inside blue in the ID pass -- body seen where garment should be -- in the Fire Ball, the
# run and the idle. Two mechanisms draw that identically: a HOLE in the garment, or the BODY IN
# FRONT of the garment (poke-through). This separates them.
#   COVERED   a body vertex whose outward normal, in the REST pose, meets a garment within 4 cm:
#             under cloth by design. A vertex at a designed opening (the robe's front split) meets
#             nothing and is never counted.
#   POKE      the body vertex has passed OUTSIDE the very garment point that covered it at rest.
#             At rest the outward ray lands on a garment TRIANGLE at barycentric (u,v,w); posed, that
#             same material point is g = u*A + v*B + w*C of the posed triangle, and
#                 s = (g - b) . n_b          (b the posed body vertex, n_b its posed normal)
#             is the clearance: ~the push-off offset at rest, NEGATIVE when the body is through the
#             cloth, by -s. Tracking the material point is what makes this a poke test and not a
#             tube test. Two earlier versions were wrong and are recorded so nobody repeats them:
#               (1) signing the NEAREST garment point by its face normal flagged a quarter of every
#                   covered vertex at the 3 cm cap -- the tripo garments are thick shells and the
#                   nearest face is often a hem's inner wall, which faces the body by construction;
#               (2) a BACKWARD ray from a vertex whose forward ray missed piled the histogram against
#                   whatever reach it was given (3 cm, then 6 cm) -- it was hitting the FAR wall of a
#                   sleeve or bracer through the arm, i.e. measuring the arm's diameter.
#   SLID      the tracked point is > 2 cm off its own face's normal line through the body vertex:
#             the cloth slid, s is not a clearance any more; counted apart, never as a poke.
#   v4        s is taken along the tracked garment FACE's normal (oriented away from the body at
#             rest), not the body normal, and HIDDEN vertices the outward ray misses (the inner
#             thigh under a skirt) are tracked too -- see HEMI below.
# Verified against the stills: the Godot ID pass with the body HIDDEN shows garment BEHIND every
# remaining dot pixel (8 of 8), i.e. the dots are pokes, not gaps.
# The composite pose is the staff layer's (film/staff_layer.gd): the carry's nine bones for
# idle/walk/run, the staff arm only for the Fire Ball, the clip alone for the Meteor.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("s14_poke.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
SRC, CARRY, OUT = a[0], a[1], a[2]
STEP = int(a[a.index('--step') + 1]) if '--step' in a else 4
REACH = 0.04
BACK = float(a[a.index('--back') + 1]) if '--back' in a else 0.06    # backward reach: a poke deeper than
# this reads as UNCOVERED, so it is set well past the deepest poke seen (the first run capped at 3 cm
# and the histogram piled up against the cap)
DUMP = a[a.index('--dump') + 1] if '--dump' in a else None          # per-vertex max depth, for s9 --under
KEYS_ON = '--keys-on' in a                                          # verify: every under_* body key at 1
car = json.load(open(CARRY))
CB = {b: Matrix([m[i * 4:(i + 1) * 4] for i in range(4)]) for b, m in car["bones"].items()}
ARM = ("RightShoulder", "RightArm", "RightForeArm", "RightHand")
LAYER = {"idle": "full", "walk": "full", "run": "full", "cast_fireball": "arm", "cast_meteor": "none"}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
meshes = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
body = next(o for o in meshes if o.name.startswith("char1"))
GARM = [o for o in meshes if o.name.split(".")[0] in ("robe", "mantle", "belt") or o.name.startswith("tripo_node_eb709101")]
gname = lambda o: "bracers" if o.name.startswith("tripo_node") else o.name.split(".")[0]
gi = {g.index: g.name for g in body.vertex_groups}
if KEYS_ON and body.data.shape_keys:
    on = [k.name for k in body.data.shape_keys.key_blocks if k.name.startswith("under_")]
    for k in on:
        body.data.shape_keys.key_blocks[k].value = 1.0
    print("body keys ON:", on)
BD = np.array([gi.get(max(v.groups, key=lambda x: x.weight).group, "?") if v.groups else "?" for v in body.data.vertices])


def tris(o):
    o.data.calc_loop_triangles()
    return np.array([tuple(lt.vertices) for lt in o.data.loop_triangles], dtype=np.int64)


TG = {o.name: tris(o) for o in GARM}


def bvh_world(o, W=None):
    W = G.world_verts(o) if W is None else W
    return BVHTree.FromPolygons([Vector(p) for p in W.tolist()], TG[o.name].tolist())


def bary(p, A, B, C):
    v0, v1, v2 = B - A, C - A, p - A
    d00, d01, d11, d20, d21 = v0 @ v0, v0 @ v1, v1 @ v1, v2 @ v0, v2 @ v1
    den = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / den; w = (d00 * d21 - d01 * d20) / den
    return np.array([1 - v - w, v, w])


# ---- rest: which body vertices are under which garment, and WHERE on it -------------------------
arm.data.pose_position = 'REST'
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
ev = body.evaluated_get(dg); me = ev.to_mesh()
M = np.array(body.matrix_world); N3 = np.linalg.inv(M[:3, :3]).T
co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
nm = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("normal", nm)
BV0 = co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
BN0 = nm.reshape(-1, 3) @ N3.T; BN0 /= np.linalg.norm(BN0, axis=1, keepdims=True) + 1e-12
ev.to_mesh_clear()
GW0 = {o.name: G.world_verts(o) for o in GARM}
trees = {o.name: bvh_world(o, GW0[o.name]) for o in GARM}
cover = np.full(len(BV0), -1)
cover_d = np.full(len(BV0), np.inf)
tri_of = np.zeros(len(BV0), dtype=np.int64)
bc = np.zeros((len(BV0), 3))
for gi_, o in enumerate(GARM):
    t = trees[o.name]; W0 = GW0[o.name]; T = TG[o.name]
    for i in range(len(BV0)):
        h = t.ray_cast(Vector((BV0[i] + BN0[i] * 1e-4).tolist()), Vector(BN0[i].tolist()), REACH)
        if h[0] is not None and h[3] < cover_d[i]:
            cover[i] = gi_; cover_d[i] = h[3]; tri_of[i] = h[2]
            A, B, C = W0[T[h[2]]]
            bc[i] = bary(np.array(h[0]), A, B, C)
n_ray = int((cover >= 0).sum())
via_ray = cover >= 0
# HIDDEN, NOT FACING CLOTH (v4). The fireball's back view showed a poke through the skirt at the
# INNER THIGH, which the outward-ray rule never tracks: that normal points at the other leg, not
# at cloth. So a vertex the ray rule missed is also tracked when it is HIDDEN at rest -- no ray
# over its outward hemisphere (HEMI directions) escapes past body and garments -- against the
# NEAREST garment point within NEAR_R. A vertex any ray escapes from is visible (a face, a hand,
# the underdress in the robe's front split) and is never tracked, so it can never be moved.
HEMI, NEAR_R = 14, 0.06
if '--no-hidden' not in a:
    import bmesh as _bm_
    allv = [Vector(q) for q in BV0.tolist()]
    body.data.calc_loop_triangles()
    BT_ = np.array([tuple(lt.vertices) for lt in body.data.loop_triangles], dtype=np.int64)
    occ_v = list(BV0.tolist()); occ_t = BT_.tolist(); base = len(occ_v)
    for o in GARM:
        occ_v += GW0[o.name].tolist(); occ_t += (TG[o.name] + base).tolist(); base = len(occ_v)
    occ = BVHTree.FromPolygons([Vector(q) for q in occ_v], occ_t)
    gold = np.pi * (3 - np.sqrt(5))
    dirs_local = []
    for k in range(HEMI):
        z = 1.0 - (k + 0.5) / HEMI * 0.95; r = np.sqrt(max(0.0, 1 - z * z)); th = gold * k
        dirs_local.append((r * np.cos(th), r * np.sin(th), z))
    dirs_local = np.array(dirs_local)
    near = {o.name: trees[o.name] for o in GARM}
    added = 0
    for i in np.nonzero(cover < 0)[0]:
        n_ = BN0[i]
        a_ = np.array([1.0, 0, 0]) if abs(n_[0]) < 0.9 else np.array([0, 1.0, 0])
        u_ = np.cross(n_, a_); u_ /= np.linalg.norm(u_); v_ = np.cross(n_, u_)
        o_ = Vector((BV0[i] + n_ * 2e-4).tolist())
        esc = False
        for dl in dirs_local:
            d_ = dl[0] * u_ + dl[1] * v_ + dl[2] * n_
            if occ.ray_cast(o_, Vector(d_.tolist()), 1.0)[0] is None:
                esc = True; break
        if esc:
            continue
        best = None
        for gi_, o in enumerate(GARM):
            q, nq, fi, dd = near[o.name].find_nearest(Vector(BV0[i].tolist()), NEAR_R)
            if q is not None and (best is None or dd < best[3]):
                best = (gi_, q, fi, dd)
        if best is None:
            continue
        gi_, q, fi, dd = best
        A, B, C = GW0[GARM[gi_].name][TG[GARM[gi_].name][fi]]
        # only when the body vertex lies roughly ALONG that face's normal (|cos| >= 0.5): a nearest
        # point off to the side of its face gives a plane test that flips with any small slide
        nf0 = np.cross(B - A, C - A); nf0 /= np.linalg.norm(nf0) + 1e-12
        dv0 = np.array(q) - BV0[i]
        if abs(float(nf0 @ dv0)) < 0.5 * float(np.linalg.norm(dv0)):
            continue
        cover[i] = gi_; cover_d[i] = dd; tri_of[i] = fi; bc[i] = bary(np.array(q), A, B, C)
        added += 1
    print("hidden-at-rest verts tracked to their nearest garment point: %d" % added)
cov = np.nonzero(cover >= 0)[0]
# the tracked garment face's normal, oriented AWAY from its body vertex at rest: the poke test is
# "has the body vertex crossed that face's plane", which holds for a skirt panel beside a thigh as
# well as for cloth straight out along the body normal
def tri_normals(W, T):
    n = np.cross(W[T[:, 1]] - W[T[:, 0]], W[T[:, 2]] - W[T[:, 0]])
    return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
sgn = np.zeros(len(BV0))
for gk, o in enumerate(GARM):
    idx = cov[cover[cov] == gk]
    if not len(idx):
        continue
    W0 = GW0[o.name]; T = TG[o.name]
    g0 = np.einsum('ij,ijk->ik', bc[idx], W0[T[tri_of[idx]]])
    n0 = tri_normals(W0, T[tri_of[idx]])
    sgn[idx] = np.where(np.einsum('ij,ij->i', n0, g0 - BV0[idx]) >= 0, 1.0, -1.0)
print("body verts %d, tracked %d (outward ray %d) (%s)" % (len(BV0), len(cov), n_ray,
      {gname(o): int((cover == k).sum()) for k, o in enumerate(GARM)}))
arm.data.pose_position = 'POSE'


def bind(act):
    arm.animation_data.action = act
    if len(getattr(act, "slots", [])):
        arm.animation_data.action_slot = act.slots[0]


rep = {"covered_verts": int(len(cov)), "reach_m": REACH, "back_m": BACK, "keys_on": KEYS_ON, "clips": {}}
VMAX = np.zeros(len(BV0))
allmax = 0.0
for cn, lay in LAYER.items():
    act = bpy.data.actions[cn]
    bind(act)
    f0, f1 = (int(round(v)) for v in act.frame_range)
    frames = sorted(set(list(range(f0, f1 + 1, STEP)) + [min(f1, f0 + 24)]))
    worst = dict(n=0, depth=0.0, frame=None, parts={}, garments={})
    for f in frames:
        sc.frame_set(f)
        if lay != "none":
            for b, m in CB.items():
                if lay == "arm" and b not in ARM:
                    continue
                arm.pose.bones[b].matrix_basis = m.copy()
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        ev = body.evaluated_get(dg); me = ev.to_mesh()
        Mb = np.array(body.matrix_world); Nb = np.linalg.inv(Mb[:3, :3]).T
        co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
        nm = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("normal", nm)
        ev.to_mesh_clear()
        BV = co.reshape(-1, 3) @ Mb[:3, :3].T + Mb[:3, 3]
        BN = nm.reshape(-1, 3) @ Nb.T; BN /= np.linalg.norm(BN, axis=1, keepdims=True) + 1e-12
        n = 0; unc = 0; dmax = 0.0; parts = {}; gar = {}; deep = []
        for gk, o in enumerate(GARM):
            idx = cov[cover[cov] == gk]
            if not len(idx):
                continue
            W = G.world_verts(o); T = TG[o.name]
            g = np.einsum('ij,ijk->ik', bc[idx], W[T[tri_of[idx]]])
            dv = g - BV[idx]
            # the outward-ray verts keep the v3 test (clearance along the BODY normal, proven on the
            # stills); only the hidden verts, tracked to a nearest point, use the face's plane
            nf = np.where(via_ray[idx, None], BN[idx], tri_normals(W, T[tri_of[idx]]) * sgn[idx, None])
            s = np.einsum('ij,ij->i', dv, nf)
            lat = np.linalg.norm(dv - s[:, None] * nf, axis=1)
            slid = lat > 0.02
            unc += int(slid.sum())
            pk = (~slid) & (s < -0.0005)
            for i, d in zip(idx[pk], -s[pk]):
                n += 1; dmax = max(dmax, float(d)); deep.append(float(d))
                VMAX[i] = max(VMAX[i], float(d))
                parts[BD[i]] = parts.get(BD[i], 0) + 1
                gar[gname(o)] = gar.get(gname(o), 0) + 1
        if n > worst["n"]:
            worst = dict(n=n, uncovered=unc, depth=round(dmax, 4), depth_p95=round(float(np.percentile(deep, 95)), 4) if deep else 0.0,
                         frame=f, t=round((f - f0) / sc.render.fps, 3),
                         parts=dict(sorted(((str(k), v) for k, v in parts.items()), key=lambda kv: -kv[1])[:6]), garments=gar)
        worst["depth_max_any_frame"] = round(max(worst.get("depth_max_any_frame", 0.0), dmax), 4)
        hist = worst.setdefault("depth_hist_all_frames_mm", {"<2": 0, "2-5": 0, "5-10": 0, "10-20": 0, ">=20": 0})
        for d in deep:
            k = "<2" if d < 0.002 else "2-5" if d < 0.005 else "5-10" if d < 0.010 else "10-20" if d < 0.020 else ">=20"
            hist[k] += 1
    allmax = max(allmax, worst["depth_max_any_frame"])
    rep["clips"][cn] = worst
    print("  %-14s layer %-4s | worst frame %s (t=%s): %d covered verts THROUGH their garment (p95 %.4f, max %.4f m; any frame %.4f), %s slid | %s | %s | depth hist (all frames) %s"
          % (cn, lay, worst["frame"], worst.get("t"), worst["n"], worst.get("depth_p95", 0.0), worst["depth"], worst["depth_max_any_frame"],
             worst.get("uncovered"), worst["garments"], worst["parts"], worst.get("depth_hist_all_frames_mm")))
rep["depth_max_m"] = allmax
rep["verts_poking_any_frame"] = int((VMAX > 0).sum())
print("verts that poke in ANY sampled frame of ANY clip: %d; depth max %.4f m" % (rep["verts_poking_any_frame"], allmax))
if DUMP:
    np.savez(DUMP, rest_pos=BV0, rest_nrm=BN0, cover=cover, depth=VMAX, garments=np.array([gname(o) for o in GARM]))
    print("dumped", DUMP)
json.dump(rep, open(OUT, "w"), indent=1)
