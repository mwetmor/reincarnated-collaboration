# T6 step 4b -- topology metrics on the dumped, normalised meshes (system
# python; Blender's bundled interpreter has no scipy).
#
# The vertex weld is not optional. glTF splits vertices at every UV seam and
# every hard normal, so the delivered index buffer is topologically shredded:
# Meshy's knight ships 89,553 vertices for 115,567 triangles where a closed
# manifold needs about 57,800. Counting islands or boundary edges on the
# delivered indices would report every seam as a hole and every shell as many
# pieces -- a clean number measuring the EXPORTER, not the mesh. Split copies
# carry bit-identical positions, so an EXACT position weld (no tolerance, no
# grid rounding, nothing that can fuse two genuinely distinct surfaces)
# restores the real topology.
import sys, os, json, glob
import numpy as np
from scipy import sparse
from scipy.sparse import csgraph

T6 = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/fal_t6/'
src = T6 + 'work/mesh'
out = T6 + 'work/metrics'
os.makedirs(out, exist_ok=True)

for npz in sorted(glob.glob(src + '/*.npz')):
    name = os.path.basename(npz)[:-4]
    d = np.load(npz)
    V, F = d['V'], d['F']
    raw_v, raw_t = len(V), len(F)
    uq, inv = np.unique(V, axis=0, return_inverse=True)
    F = inv[F.ravel()].reshape(-1, 3)
    F = F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]
    nv, nt = len(uq), len(F)

    e = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
    g = sparse.coo_matrix((np.ones(len(e), np.int8), (e[:, 0], e[:, 1])), shape=(nv, nv))
    ncomp, lab = csgraph.connected_components(g, directed=False)
    area = 0.5 * np.linalg.norm(np.cross(uq[F[:, 1]] - uq[F[:, 0]], uq[F[:, 2]] - uq[F[:, 0]]), axis=1)
    total = float(area.sum())
    cot = lab[F[:, 0]]
    abc = np.bincount(cot, weights=area, minlength=ncomp)
    tbc = np.bincount(cot, minlength=ncomp)
    live = np.where(tbc > 0)[0]
    frac = abc[live] / total
    order = np.argsort(-frac)

    ek = np.sort(e, axis=1)
    key = ek[:, 0].astype(np.int64) * nv + ek[:, 1]
    uek, cnt = np.unique(key, return_counts=True)
    boundary = int((cnt == 1).sum()); nonman = int((cnt > 2).sum()); nedge = int(len(uek))
    dk = e[:, 0].astype(np.int64) * nv + e[:, 1]
    _, dcnt = np.unique(dk, return_counts=True)

    # per-island watertightness: which islands are closed shells
    isl_bound = np.zeros(ncomp, np.int64)
    bnd = uek[cnt == 1]
    if len(bnd):
        np.add.at(isl_bound, lab[(bnd // nv).astype(np.int64)], 1)

    # WHAT the extra islands are, not just how many. "floating fragments under
    # 1% of area" is the brief's screen, and on this set it MISSES the two worst
    # defects in the run: Tripo's manticore tail is 1.87% and Hunyuan's two
    # shards are 1.82% and 0.92%, so all three sit just the wrong side of the
    # threshold and the column reads 0. Record every non-main island's size and
    # world bbox so a detached LIMB can be told from a speck of internal junk.
    det = []
    for c in order[1:6]:
        ci = live[c]
        if tbc[ci] == 0:
            continue
        P = uq[lab == ci]
        mn, mx = P.min(0), P.max(0)
        det.append(dict(area_pct=round(float(abc[ci] / total * 100), 4),
                        tris=int(tbc[ci]),
                        bbox_min=[round(float(v), 3) for v in mn],
                        bbox_max=[round(float(v), 3) for v in mx],
                        outside_main_body_xy=bool(mn[0] > 0.30 or mx[0] < -0.30
                                                  or mn[1] > 0.80 or mx[1] < -0.80)))

    dump = json.load(open(f'{src}/{name}_dump.json'))
    m = dict(model=name, yaw_applied=dump['yaw_applied'], flip_x=False, norm=dump['norm'],
             verts_delivered=raw_v, tris_delivered=raw_t,
             verts_welded=nv, tris_welded=nt, verts_merged_by_weld=int(raw_v - nv),
             islands=int(len(live)),
             main_island_area_frac=round(float(frac[order[0]]), 6),
             main_island_tris=int(tbc[live][order[0]]),
             floating_fragments_lt1pct=int((frac < 0.01).sum()),
             fragment_area_pct=round(float(frac[frac < 0.01].sum() * 100), 4),
             island_area_fracs_top8=[round(float(x), 6) for x in frac[order][:8]],
             edges=nedge, boundary_edges=boundary, nonmanifold_edges=nonman,
             duplicate_directed_edges=int((dcnt > 1).sum()),
             euler_characteristic=int(nv - nedge + nt),
             approx_watertight=bool(boundary == 0 and nonman == 0),
             main_island_watertight=bool(isl_bound[live[order[0]]] == 0),
             surface_area_m2=round(total, 5),
             detached_islands=det,
             detached_area_pct_total=round(float(sum(d['area_pct'] for d in det)), 4))
    json.dump(m, open(f'{out}/{name}.json', 'w'), indent=1)
    print(f"{name:30s} tris {nt:8d} weld-merged {raw_v-nv:8d} islands {m['islands']:5d} "
          f"frag<1% {m['floating_fragments_lt1pct']:5d} ({m['fragment_area_pct']:.3f}%) "
          f"bound {boundary:7d} nonman {nonman:6d} wt {m['approx_watertight']}")
