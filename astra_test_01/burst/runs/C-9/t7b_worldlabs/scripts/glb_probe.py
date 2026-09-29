#!/usr/bin/env python3
"""T7-B: minimal GLB reader + geometry probe for Marble's collider mesh.

No trimesh/pygltflib on this Mac, so the container is parsed by hand: a GLB is a
12-byte header then length-prefixed chunks, the first JSON and the second BIN.

Reports the things that decide "is this usable as a game floor": triangle count,
extents, the height histogram, and a per-triangle slope census (a floor is the set
of triangles whose normal is within N degrees of up).  Coordinates are converted
from Marble's `marble_raw_opencv` (+x left, +y down, +z forward) to a Y-up frame,
the same conversion render_splats.py applies.
"""
import argparse
import json
import struct
import sys

import numpy as end_np  # noqa: F401  (kept explicit: numpy is the only dependency)
import numpy as np

COMP = {5120: ("<i1", 1), 5121: ("<u1", 1), 5122: ("<i2", 2), 5123: ("<u2", 2),
        5125: ("<u4", 4), 5126: ("<f4", 4)}
NCOMP = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


def read_glb(path):
    with open(path, "rb") as f:
        magic, ver, total = struct.unpack("<4sII", f.read(12))
        if magic != b"glTF":
            sys.exit(f"{path}: not a GLB")
        js, bindata = None, b""
        while f.tell() < total:
            hdr = f.read(8)
            if len(hdr) < 8:
                break
            ln, kind = struct.unpack("<I4s", hdr)
            blob = f.read(ln)
            if kind == b"JSON":
                js = json.loads(blob)
            elif kind == b"BIN\x00":
                bindata = blob
    return js, bindata


def accessor(js, bin_, i):
    acc = js["accessors"][i]
    bv = js["bufferViews"][acc["bufferView"]]
    dt, sz = COMP[acc["componentType"]]
    n = NCOMP[acc["type"]]
    off = bv.get("byteOffset", 0) + acc.get("byteOffset", 0)
    stride = bv.get("byteStride") or (sz * n)
    cnt = acc["count"]
    if stride == sz * n:
        a = np.frombuffer(bin_, dtype=dt, count=cnt * n, offset=off).reshape(cnt, n)
    else:
        raw = np.frombuffer(bin_, dtype="u1", count=stride * cnt, offset=off).reshape(cnt, stride)
        a = raw[:, :sz * n].copy().view(dt).reshape(cnt, n)
    return a.astype(np.float64) if acc["componentType"] == 5126 else a.astype(np.int64)


def node_matrix(node):
    if "matrix" in node:
        return np.array(node["matrix"], dtype=np.float64).reshape(4, 4).T  # glTF is column-major
    M = np.eye(4)
    if "scale" in node:
        M = np.diag(list(node["scale"]) + [1.0]) @ M
    if "rotation" in node:
        x, y, z, w = node["rotation"]
        R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
                      [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
                      [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]])
        T = np.eye(4); T[:3, :3] = R
        M = T @ M
    if "translation" in node:
        T = np.eye(4); T[:3, 3] = node["translation"]
        M = T @ M
    return M


def gather(js, bin_):
    """Walk the default scene, applying node transforms; return (verts, tris)."""
    V, F, base = [], [], 0
    nodes = js.get("nodes", [])
    scene = js["scenes"][js.get("scene", 0)]

    def walk(ni, parent):
        nonlocal base
        node = nodes[ni]
        M = parent @ node_matrix(node)
        if "mesh" in node:
            for prim in js["meshes"][node["mesh"]].get("primitives", []):
                if prim.get("mode", 4) != 4:
                    continue
                p = accessor(js, bin_, prim["attributes"]["POSITION"])
                p = (M @ np.c_[p, np.ones(len(p))].T).T[:, :3]
                idx = (accessor(js, bin_, prim["indices"]).ravel()
                       if "indices" in prim else np.arange(len(p)))
                V.append(p); F.append(idx.reshape(-1, 3) + base); base += len(p)
        for c in node.get("children", []):
            walk(c, M)

    for ni in scene.get("nodes", []):
        walk(ni, np.eye(4))
    return np.vstack(V), np.vstack(F)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("glb")
    ap.add_argument("--convert", default="opencv", choices=["opencv", "none"])
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    js, bin_ = read_glb(a.glb)
    V, F = gather(js, bin_)
    if a.convert == "opencv":
        V = V * np.array([1.0, -1.0, -1.0])      # -> Y up
    p0, p1, p2 = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    n = np.cross(p1 - p0, p2 - p0)
    area = 0.5 * np.linalg.norm(n, axis=1)
    nz = np.linalg.norm(n, axis=1)
    good = nz > 1e-12
    up = np.abs(n[good, 1] / nz[good])           # |cos| to +Y, sign-agnostic
    tilt = np.degrees(np.arccos(np.clip(up, 0, 1)))
    ctr = (p0 + p1 + p2) / 3.0
    r = np.linalg.norm(ctr[:, [0, 2]], axis=1)
    rep = {
        "file": a.glb,
        "vertices": int(len(V)), "triangles": int(len(F)),
        "materials": len(js.get("materials", [])),
        "has_vertex_colors": any("COLOR_0" in p.get("attributes", {})
                                 for m in js.get("meshes", []) for p in m.get("primitives", [])),
        "has_uv": any("TEXCOORD_0" in p.get("attributes", {})
                      for m in js.get("meshes", []) for p in m.get("primitives", [])),
        "images": len(js.get("images", [])),
        "bbox_min": [round(float(v), 3) for v in V.min(0)],
        "bbox_max": [round(float(v), 3) for v in V.max(0)],
        "total_area_units2": round(float(area.sum()), 1),
        "tri_area_p50": round(float(np.percentile(area, 50)), 5),
        "tri_area_p99": round(float(np.percentile(area, 99)), 5),
        "slope_census_by_area_pct": {
            "within_10deg_of_horizontal": round(float(area[good][tilt < 10].sum() / area.sum() * 100), 1),
            "within_30deg": round(float(area[good][tilt < 30].sum() / area.sum() * 100), 1),
            "within_45deg": round(float(area[good][tilt < 45].sum() / area.sum() * 100), 1),
            "steeper_than_60deg": round(float(area[good][tilt > 60].sum() / area.sum() * 100), 1),
        },
        "tri_centroid_radius_units": {p: round(float(np.percentile(r, p)), 2)
                                      for p in (50, 90, 99)},
        "y_percentiles": {p: round(float(np.percentile(V[:, 1], p)), 2)
                          for p in (1, 5, 25, 50, 75, 95, 99)},
    }
    # near-field floor: nearly-horizontal area inside successive radii
    flat = good.copy(); flat[good] = tilt < 30
    for R in (3, 5, 10, 20, 40):
        m = flat & (r < R)
        rep[f"flat_area_within_{R}u"] = round(float(area[m].sum()), 1)
    print(json.dumps(rep, indent=1))
    if a.out:
        with open(a.out, "w") as f:
            json.dump(rep, f, indent=1)


if __name__ == "__main__":
    main()
