#!/usr/bin/env python3
"""T7-B: render a Marble Gaussian-splat PLY through OUR game camera.

R-C9-68 fixes the view: ORTHOGRAPHIC, pitch 52.95354112560294 deg, yaw 47 deg -- the
`player_lock` camera of reincarnated-godot/scripts/cliffside_blockout.gd.  The basis
here is that file's _build_camera_law(), line for line:

    hb  = (sin yaw, 0, cos yaw)
    fwd = normalize(-hb*cos(pitch) + DOWN*sin(pitch))
    upc = normalize(-hb*sin(pitch) + UP*cos(pitch))
    rgt = cross(fwd, upc)

Godot is Y-up; at yaw=0, pitch=0 this gives fwd=(0,0,-1), upc=(0,1,0), rgt=(1,0,0).
Ortho scale follows _measure()'s `_mcam.size = RES.y / ortho_ppm` with KEEP_HEIGHT:
the VERTICAL world extent in view is `size` metres, so ppm = height_px / size.

No CUDA on this Mac, so the rasteriser is numba-JIT CPU: exact 3D-covariance splatting
(EWA), depth-sorted back-to-front alpha compositing, per-splat footprint bounded at 3
sigma.  Orthographic projection is LINEAR, so the 2D covariance needs no perspective
Jacobian -- it is just the world covariance rotated into the view basis and scaled.

Marble PLY is 3DGS-standard: x y z, f_dc_0..2 (SH band 0), opacity (logit),
scale_0..2 (log), rot_0..3 (quaternion, w first).  Marble's native frame is
`marble_raw_opencv` (+x left, +y down, +z forward); --convert opencv maps it to the
Y-up frame our camera law assumes.
"""
import argparse
import json
import math
import struct
from pathlib import Path

import numpy as np
from numba import njit, prange

PL_PITCH_DEG = 52.95354112560294
PL_YAW_DEG = 47.0
SH_C0 = 0.28209479177387814


# ---------------------------------------------------------------- PLY reading
def read_ply(path):
    with open(path, "rb") as f:
        magic = f.readline()
        if magic.strip() != b"ply":
            raise SystemExit(f"{path}: not a PLY")
        fmt, count, props, hdr = None, 0, [], [magic]
        while True:
            line = f.readline()
            hdr.append(line)
            t = line.split()
            if not t:
                continue
            if t[0] == b"format":
                fmt = t[1].decode()
            elif t[0] == b"element" and t[1] == b"vertex":
                count = int(t[2])
            elif t[0] == b"property" and len(t) == 3:
                props.append((t[1].decode(), t[2].decode()))
            elif t[0] == b"end_header":
                break
        if fmt != "binary_little_endian":
            raise SystemExit(f"{path}: unsupported PLY format {fmt}")
        np_t = {"float": "<f4", "float32": "<f4", "double": "<f8", "uchar": "u1",
                "uint8": "u1", "int": "<i4", "uint": "<u4", "short": "<i2",
                "ushort": "<u2"}
        dt = np.dtype([(n, np_t[t]) for t, n in props])
        arr = np.frombuffer(f.read(count * dt.itemsize), dtype=dt, count=count)
    return arr, [n for _, n in props]


def load_gaussians(path, convert="opencv"):
    arr, names = read_ply(path)
    need = ["x", "y", "z", "opacity", "scale_0", "scale_1", "scale_2",
            "rot_0", "rot_1", "rot_2", "rot_3", "f_dc_0", "f_dc_1", "f_dc_2"]
    missing = [n for n in need if n not in names]
    if missing:
        raise SystemExit(f"{path}: PLY is missing {missing}; got {names[:24]}")
    xyz = np.stack([arr["x"], arr["y"], arr["z"]], 1).astype(np.float64)
    scale = np.exp(np.stack([arr[f"scale_{i}"] for i in range(3)], 1).astype(np.float64))
    quat = np.stack([arr[f"rot_{i}"] for i in range(4)], 1).astype(np.float64)  # w,x,y,z
    quat /= np.linalg.norm(quat, axis=1, keepdims=True) + 1e-12
    op = 1.0 / (1.0 + np.exp(-arr["opacity"].astype(np.float64)))
    col = np.clip(0.5 + SH_C0 * np.stack([arr[f"f_dc_{i}"] for i in range(3)], 1)
                  .astype(np.float64), 0.0, 1.0)
    if convert == "opencv":
        # marble_raw_opencv (+x left, +y down, +z forward) -> Godot-style Y-up.
        # Negate y and z; a reflection on two axes is a rotation (det +1), so the
        # quaternion transforms as (w, x, y, z) -> (w, x, -y, -z) and scales are
        # unchanged.  This is the 180-deg rotation about X that Marble's own viewer
        # applies to generated SPZ assets.
        xyz = xyz * np.array([1.0, -1.0, -1.0])
        quat = quat * np.array([1.0, 1.0, -1.0, -1.0])
    return xyz, scale, quat, op, col


# ---------------------------------------------------------------- camera law
def player_lock_basis(yaw_deg=PL_YAW_DEG, pitch_deg=PL_PITCH_DEG):
    yaw, p = math.radians(yaw_deg), math.radians(pitch_deg)
    hb = np.array([math.sin(yaw), 0.0, math.cos(yaw)])
    fwd = -hb * math.cos(p) + np.array([0.0, -1.0, 0.0]) * math.sin(p)
    fwd /= np.linalg.norm(fwd)
    upc = -hb * math.sin(p) + np.array([0.0, 1.0, 0.0]) * math.cos(p)
    upc /= np.linalg.norm(upc)
    rgt = np.cross(fwd, upc)
    assert abs(float(np.dot(fwd, upc))) < 1e-9, "player_lock basis is not orthogonal"
    return fwd, upc, rgt


def cov3d(scale, quat):
    w, x, y, z = quat[:, 0], quat[:, 1], quat[:, 2], quat[:, 3]
    R = np.empty((len(quat), 3, 3))
    R[:, 0, 0] = 1 - 2 * (y * y + z * z); R[:, 0, 1] = 2 * (x * y - w * z); R[:, 0, 2] = 2 * (x * z + w * y)
    R[:, 1, 0] = 2 * (x * y + w * z); R[:, 1, 1] = 1 - 2 * (x * x + z * z); R[:, 1, 2] = 2 * (y * z - w * x)
    R[:, 2, 0] = 2 * (x * z - w * y); R[:, 2, 1] = 2 * (y * z + w * x); R[:, 2, 2] = 1 - 2 * (x * x + y * y)
    M = R * scale[:, None, :]          # R @ diag(s)
    return M @ np.transpose(M, (0, 2, 1))


# ---------------------------------------------------------------- rasteriser
@njit(cache=True, fastmath=True)
def _raster(cx, cy, a, b, c, col, alpha, order, W, H, out, acc_T):
    """Back-to-front over-compositing of 2D Gaussians.

    (a,b,c) is the INVERSE 2D covariance: p = exp(-0.5*(a dx^2 + 2b dx dy + c dy^2)).
    `order` is back-to-front. acc_T carries remaining transmittance per pixel.
    """
    n = order.shape[0]
    for i in range(n):
        s = order[i]
        A, B, C = a[s], b[s], c[s]
        det = A * C - B * B
        if det <= 1e-12:
            continue
        # 3-sigma extent of the ellipse from the inverse-covariance form
        ex = math.sqrt(3.0 * 3.0 * C / det)
        ey = math.sqrt(3.0 * 3.0 * A / det)
        x0 = int(cx[s] - ex); x1 = int(cx[s] + ex) + 1
        y0 = int(cy[s] - ey); y1 = int(cy[s] + ey) + 1
        if x1 <= 0 or y1 <= 0 or x0 >= W or y0 >= H:
            continue
        if x0 < 0: x0 = 0
        if y0 < 0: y0 = 0
        if x1 > W: x1 = W
        if y1 > H: y1 = H
        r, g, bl = col[s, 0], col[s, 1], col[s, 2]
        al = alpha[s]
        for py in range(y0, y1):
            dy = py + 0.5 - cy[s]
            for px in range(x0, x1):
                dx = px + 0.5 - cx[s]
                e = A * dx * dx + 2.0 * B * dx * dy + C * dy * dy
                if e > 9.0:
                    continue
                w = al * math.exp(-0.5 * e)
                if w < 1.0 / 255.0:
                    continue
                if w > 0.999:
                    w = 0.999
                out[py, px, 0] = out[py, px, 0] * (1.0 - w) + r * w
                out[py, px, 1] = out[py, px, 1] * (1.0 - w) + g * w
                out[py, px, 2] = out[py, px, 2] * (1.0 - w) + bl * w
                acc_T[py, px] *= (1.0 - w)


def render(xyz, scale, quat, op, col, center, size_m, res, yaw_deg=PL_YAW_DEG,
           pitch_deg=PL_PITCH_DEG, bg=(0.06, 0.07, 0.10), zmin=None, zmax=None):
    """zmin/zmax clip in VIEW-SPACE FORWARD metres relative to `center`.

    A Marble world is a closed bubble around one viewpoint, so a camera looking DOWN
    at it from outside sees only the sky dome.  zmin is this renderer's near plane:
    Camera3D.near does the same job in cliffside_blockout.gd (_mcam.near = 1.0).
    """
    W, H = res
    fwd, upc, rgt = player_lock_basis(yaw_deg, pitch_deg)
    Rv = np.stack([rgt, upc, fwd])              # world -> view rows
    ppm = H / size_m                            # KEEP_HEIGHT, like _mcam.size
    d = xyz - center
    v = d @ Rv.T                                # (right, up, forward) in metres
    cxp = W * 0.5 + v[:, 0] * ppm
    cyp = H * 0.5 - v[:, 1] * ppm               # screen y down
    depth = v[:, 2]

    S = cov3d(scale, quat)
    S2 = (Rv @ S @ Rv.T)[:, :2, :2] * (ppm * ppm)   # orthographic: linear, no Jacobian
    S2[:, 0, 0] += 0.3                              # low-pass, as in 3DGS
    S2[:, 1, 1] += 0.3
    det = S2[:, 0, 0] * S2[:, 1, 1] - S2[:, 0, 1] ** 2
    ok = (det > 1e-9) & np.isfinite(det) & np.isfinite(cxp) & np.isfinite(cyp)
    # cull anything whose 3-sigma box misses the frame
    rad = 3.0 * np.sqrt(np.maximum(S2[:, 0, 0], S2[:, 1, 1]))
    ok &= (cxp + rad > 0) & (cxp - rad < W) & (cyp + rad > 0) & (cyp - rad < H)
    if zmin is not None:
        ok &= depth > zmin
    if zmax is not None:
        ok &= depth < zmax
    idx = np.nonzero(ok)[0]
    inv = 1.0 / det[idx]
    a = (S2[idx, 1, 1] * inv)
    b = (-S2[idx, 0, 1] * inv)
    c = (S2[idx, 0, 0] * inv)
    order = np.argsort(-depth[idx])             # far first (fwd grows away from camera)

    out = np.empty((H, W, 3), np.float64)
    out[:] = np.array(bg)
    accT = np.ones((H, W), np.float64)
    _raster(np.ascontiguousarray(cxp[idx]), np.ascontiguousarray(cyp[idx]),
            np.ascontiguousarray(a), np.ascontiguousarray(b), np.ascontiguousarray(c),
            np.ascontiguousarray(col[idx]), np.ascontiguousarray(op[idx]),
            np.ascontiguousarray(order.astype(np.int64)), W, H, out, accT)
    stats = {"splats_total": int(len(xyz)), "splats_drawn": int(len(idx)),
             "ppm": ppm, "size_m": size_m, "zmin": zmin, "zmax": zmax,
             "coverage_frac": float((accT < 0.5).mean()),
             "empty_frac": float((accT > 0.95).mean())}
    return np.clip(out, 0, 1), stats


def autoframe(xyz, op, pct=2.0):
    """Centre and vertical extent from the solid bulk of the cloud (percentile box)."""
    m = op > 0.3
    p = xyz[m] if m.sum() > 1000 else xyz
    lo = np.percentile(p, pct, axis=0)
    hi = np.percentile(p, 100 - pct, axis=0)
    return (lo + hi) * 0.5, float(np.max(hi - lo))


def main():
    from PIL import Image
    ap = argparse.ArgumentParser()
    ap.add_argument("ply")
    ap.add_argument("--out", required=True)
    ap.add_argument("--res", default="1920x1080")
    ap.add_argument("--size", type=float, default=0.0, help="vertical world extent (m)")
    ap.add_argument("--center", default="", help="x,y,z; default = auto")
    ap.add_argument("--yaw", type=float, default=PL_YAW_DEG)
    ap.add_argument("--pitch", type=float, default=PL_PITCH_DEG)
    ap.add_argument("--convert", default="opencv", choices=["opencv", "none"])
    ap.add_argument("--scale-factor", type=float, default=1.0)
    ap.add_argument("--ground-offset", type=float, default=0.0)
    ap.add_argument("--zmin", type=float, default=None,
                    help="near clip, view-space forward metres from centre")
    ap.add_argument("--zmax", type=float, default=None, help="far clip")
    ap.add_argument("--stats", default="")
    a = ap.parse_args()

    xyz, scale, quat, op, col = load_gaussians(a.ply, a.convert)
    if a.scale_factor != 1.0:
        xyz *= a.scale_factor
        scale *= a.scale_factor
    if a.ground_offset:
        xyz[:, 1] += a.ground_offset
    ctr, ext = autoframe(xyz, op)
    if a.center:
        ctr = np.array([float(v) for v in a.center.split(",")])
    size_m = a.size if a.size > 0 else ext
    W, H = (int(v) for v in a.res.lower().split("x"))
    img, st = render(xyz, scale, quat, op, col, ctr, size_m, (W, H), a.yaw, a.pitch,
                     zmin=a.zmin, zmax=a.zmax)
    st.update({"center": list(map(float, ctr)), "yaw_deg": a.yaw, "pitch_deg": a.pitch,
               "ply": a.ply, "res": [W, H], "auto_extent_m": ext})
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray((img * 255 + 0.5).astype(np.uint8)).save(a.out)
    if a.stats:
        Path(a.stats).write_text(json.dumps(st, indent=1))
    print(json.dumps(st, indent=1))


if __name__ == "__main__":
    main()
