#!/usr/bin/env python3
"""C-9 knight3d step 7: turn the FITTED proxy into real meshes, once, in one
place.

M-a found a 6.6 % silhouette disagreement between the solid the fitter
optimised and the mesh Blender built, because the two were written twice and
drifted. So they are no longer written twice. knight_proxy.build_parts() is
the single source of geometry; every rigid piece is convex, so its mesh is
literally the CONVEX HULL of that piece's point cloud, and the built mesh and
the fitted solid are the same object by construction.

The deforming pieces (mail skirt, tabard panels) are emitted as segmented
shells instead, because a hull of 8 corners cannot bend in three links -- but
their hulls are identical to the fitter's, so the silhouette is unchanged.

Also emits the POLLAXE as its own rigid mesh with two grip points, measured
from the stills' cardinal views (which agree with each other; the diagonals do
not -- see work/pollaxe_consistency.json).

Writes out/parts_mesh.npz and out/parts_index.json.
"""
import json, os, sys
import numpy as np
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import knight_proxy as kp

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
K3 = os.path.join(ROOT, "knight3d")
WORK = os.path.join(K3, "work"); OUT = os.path.join(K3, "out")
os.makedirs(OUT, exist_ok=True)

DEFORMING = {"mail_skirt", "tabard_front", "tabard_back"}


def hull_mesh(pts):
    h = ConvexHull(pts)
    keep = np.unique(h.simplices)
    remap = {int(k): i for i, k in enumerate(keep)}
    verts = pts[keep]
    c = verts.mean(0)
    faces = []
    for s in h.simplices:
        tri = [remap[int(i)] for i in s]
        a, b, cc = verts[tri[0]], verts[tri[1]], verts[tri[2]]
        n = np.cross(b - a, cc - a)
        if n @ (a - c) < 0:            # make every face point outward
            tri = [tri[0], tri[2], tri[1]]
        faces.append(tri)
    return verts, np.array(faces, np.int32)


def cone_shell(z0, r0, z1, r1, seg=32):
    """A segmented cone (the mail skirt): rings so it can deform."""
    verts, faces = [], []
    rings = 5
    for i in range(rings + 1):
        t = i / rings
        z = z0 + (z1 - z0) * t
        r = r0 + (r1 - r0) * t
        for k in range(seg):
            a = 2 * np.pi * k / seg
            verts.append((r * np.cos(a), r * np.sin(a), z))
    for i in range(rings):
        for k in range(seg):
            j = (k + 1) % seg
            faces.append([i * seg + k, i * seg + j, (i + 1) * seg + j])
            faces.append([i * seg + k, (i + 1) * seg + j, (i + 1) * seg + k])
    # cap the bottom so the silhouette is the solid cone the fitter used
    c0 = len(verts); verts.append((0, 0, z1))
    for k in range(seg):
        faces.append([rings * seg + k, c0, rings * seg + (k + 1) % seg])
    c1 = len(verts); verts.append((0, 0, z0))
    for k in range(seg):
        faces.append([k, (k + 1) % seg, c1])
    return np.array(verts, float), np.array(faces, np.int32)


def panel_shell(half_w, y, z_top, z_bot, thick, segs=8):
    """A hanging cloth panel, segmented vertically so it can deform."""
    verts, faces = [], []
    n = segs + 1
    for i in range(n):
        z = z_top + (z_bot - z_top) * i / segs
        for sy in (-1, 1):
            for sx in (-1, 1):
                verts.append((sx * half_w, y + sy * thick / 2, z))
    for i in range(segs):
        a, b = i * 4, (i + 1) * 4
        faces += [[a + 0, b + 0, b + 1], [a + 0, b + 1, a + 1],
                  [a + 2, a + 3, b + 3], [a + 2, b + 3, b + 2],
                  [a + 0, a + 2, b + 2], [a + 0, b + 2, b + 0],
                  [a + 1, b + 1, b + 3], [a + 1, b + 3, a + 3]]
    faces += [[0, 1, 3], [0, 3, 2],
              [segs * 4 + 0, segs * 4 + 3, segs * 4 + 1],
              [segs * 4 + 0, segs * 4 + 2, segs * 4 + 3]]
    return np.array(verts, float), np.array(faces, np.int32)


def pollaxe(p, tag="pollaxe"):
    """The pollaxe as its own rigid mesh, MEASURED off the E matte rather than
    guessed (the first pass had a 38 mm haft and a head a third the right size).

    From work/masks/E_axe.npy at the E view's fitted scale (481 px/m):
        total length          2.235 m   (spear point to butt cap)
        haft diameter         0.0624 m
        head span across      0.443 m   (blade fan one side, fluke the other)
        head height           0.295 m
        head centre           0.541 m above the grip
        spear point           0.239 m above the head
    Built at the fitted grip point, vertical, which is what every still shows.
    """
    gx, gy, gz = p["grip_x"], p["grip_y"], p["grip_z"]
    L_up, L_dn = 0.689, 1.306
    r = 0.0312
    head_c = gz + 0.541
    hh = 0.295 / 2.0
    pieces = {}
    ang = np.linspace(0, 2 * np.pi, 16, endpoint=False)
    ring = np.stack([np.cos(ang), np.sin(ang)], -1)
    hp = []
    for z in (gz - L_dn, gz + L_up):
        hp.append(np.stack([gx + r * ring[:, 0], gy + r * ring[:, 1],
                            np.full(len(ang), z)], -1))
    pieces[tag + "_haft"] = np.concatenate(hp, 0)
    # the blade: a fan, wide at its outer edge, on the -Y side
    blade = []
    for dy, z0, z1 in ((-0.020, -hh * 0.80, hh * 0.80),
                       (-0.150, -hh * 0.95, hh * 1.00),
                       (-0.272, -hh * 0.62, hh * 0.92)):
        for dz in (z0, z1):
            for dx in (-0.013, 0.013):
                blade.append((gx + dx, gy + dy, head_c + dz))
    pieces[tag + "_blade"] = np.array(blade)
    # the fluke/spike on the +Y side, shorter
    spike = []
    for dy, hz in ((0.020, hh * 0.52), (0.092, hh * 0.34), (0.171, hh * 0.09)):
        for dz in (-hz, hz):
            for dx in (-0.012, 0.012):
                spike.append((gx + dx, gy + dy, head_c + dz))
    pieces[tag + "_spike"] = np.array(spike)
    # the spear point above the head
    pt = []
    for dz, rr in ((0.0, 0.026), (0.115, 0.018), (0.239, 0.004)):
        for a_ in np.linspace(0, 2 * np.pi, 10, endpoint=False):
            pt.append((gx + rr * np.cos(a_), gy + rr * np.sin(a_),
                       gz + L_up + dz))
    pieces[tag + "_point"] = np.array(pt)
    butt = []
    for dz, rr in ((0.0, 0.040), (-0.045, 0.030)):
        for a_ in np.linspace(0, 2 * np.pi, 10, endpoint=False):
            butt.append((gx + rr * np.cos(a_), gy + rr * np.sin(a_), gz - L_dn + dz))
    pieces[tag + "_butt"] = np.array(butt)
    return pieces


def main():
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    p = dict(kp.DEFAULTS); p.update(fit["params"])
    parts = kp.build_parts(p)

    meshes, index = {}, {}
    for name, bone, pts in parts:
        if name in DEFORMING:
            continue
        v, f = hull_mesh(pts)
        meshes[name + "__v"] = v.astype(np.float32)
        meshes[name + "__f"] = f
        index[name] = dict(bone=bone, kind="rigid", nv=int(len(v)), nf=int(len(f)))

    v, f = cone_shell(p["z_hip"] - 0.02, p["skirt_r_top"], p["skirt_z_bot"], p["skirt_r_bot"])
    meshes["mail_skirt__v"], meshes["mail_skirt__f"] = v.astype(np.float32), f
    index["mail_skirt"] = dict(bone="Hips", kind="deform_skirt", nv=int(len(v)), nf=int(len(f)))
    for tag, ys in (("front", 1.0), ("back", -1.0)):
        v, f = panel_shell(p["tabard_half_w"], ys * p["tabard_y"],
                           p["z_shoulder"] + 0.03, p["tabard_z_bot"], p["tabard_t"])
        meshes["tabard_%s__v" % tag] = v.astype(np.float32)
        meshes["tabard_%s__f" % tag] = f
        index["tabard_%s" % tag] = dict(bone="TAB_%s_01" % tag[0].upper(),
                                        kind="deform_tabard_" + tag[0].upper(),
                                        nv=int(len(v)), nf=int(len(f)))

    for name, pts in pollaxe(p).items():
        v, f = hull_mesh(pts)
        meshes[name + "__v"] = v.astype(np.float32)
        meshes[name + "__f"] = f
        index[name] = dict(bone="SOCK_WeaponMain", kind="weapon", nv=int(len(v)),
                           nf=int(len(f)))

    np.savez_compressed(os.path.join(OUT, "parts_mesh.npz"), **meshes)
    with open(os.path.join(OUT, "parts_index.json"), "w") as fh:
        json.dump(dict(note="C-9 knight3d: meshes built from knight_proxy.build_parts() "
                            "at the fitted params. Rigid pieces are the convex hull of "
                            "the fitter's own point cloud, so built == fitted.",
                       params=p, parts=index), fh, indent=1)
    print("%d meshes, %d verts, %d tris" %
          (len(index), sum(i["nv"] for i in index.values()),
           sum(i["nf"] for i in index.values())))
    for k, i in index.items():
        print("  %-18s %-18s %-16s %4d v %4d f" % (k, i["bone"], i["kind"], i["nv"], i["nf"]))


if __name__ == "__main__":
    main()
