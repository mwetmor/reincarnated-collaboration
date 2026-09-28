#!/usr/bin/env python3
"""C-9 knight3d: EbSynth GUIDE passes for the fitted cycles (R-C9-60).

    python3 scripts/23_guides.py [walk|run|all]

A colour guide cannot carry correspondence -- it says what a pixel LOOKS like,
not what part of the body it IS -- which is why the naive test smeared within
three frames. These four say where each pixel comes from:

  uv    R = u, G = v of the painted atlas, B = 0. The exact texture coordinate
        the projection paint used, so a pixel's guide value is its address on
        the body's texture.
  part  a flat distinct colour per piece, in parts_index order round a hue
        wheel. Coarse but unambiguous: it never lets a knee match an elbow.
  pos   the REST-POSE (bind) position of the surface point under each pixel,
        with the body's bind bbox normalised to 0..1. Rasterised through the
        POSED geometry but interpolating the REST coordinates, so it is
        invariant to the animation -- the StyLit-style "where on the body"
        guide. This is the one that should hold a cycle together.
  mask  white on black.

Rendered at 512 with NO supersampling and nearest-value interpolation
semantics: these are look-up tables, not pictures, and averaging two sides of
a silhouette edge invents a coordinate that is on neither. The 1 px difference
against the anti-aliased colour frames is the intended cost.

Camera, scale and ground calibration are read from render_{gait}_fit.json, so
the guides sit on exactly the pixels out/sprites_fit/{gait}/E/ does.

PARAMETER CONVENTION, and a bug found by checking that:
10_render.py poses with the RAW fitted params (kp.joints(p)); 09_anim.py and
20_apply_motion.py pose with the LAYERED ones (kp.joints(kp.layered(p))), and
07_export_parts.py builds the mesh from the RAW ones. layered() moves
tabard_y from 0.1425 to 0.1980, so those two conventions put the tabard 8.7 px
apart -- which is exactly the 8 px crescent the mask check found along the
tabard's edge. This script deliberately follows 10_render's convention,
because its job is to align with the colour frames Astra has already painted
over; the inconsistency itself is reported, not silently fixed, because
rebuilding the mesh now would invalidate that in-flight paint pass.
"""
import colorsys, json, os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import knight_proxy as kp
import pose as PS
from raster import raster

K3 = os.path.dirname(HERE); OUT = os.path.join(K3, "out"); WORK = os.path.join(K3, "work")
FRAME = 512
AZI_E = 90.0


def part_palette(n):
    cols = []
    for i in range(n):
        # a hue wheel, but stepped by a co-prime stride so neighbouring piece
        # indices (which are often neighbouring pieces on the body) do not get
        # neighbouring hues
        h = ((i * 7) % max(n, 1)) / max(n, 1)
        s = 0.85 + 0.15 * ((i % 3) / 2.0)
        v = 0.70 + 0.30 * ((i % 2))
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        cols.append((int(round(r * 255)), int(round(g * 255)), int(round(b * 255))))
    return np.array(cols, np.uint8)


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    gaits = ["walk", "run"] if which == "all" else [which]
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    theta = fit["theta_elevation_deg"]
    p = dict(kp.DEFAULTS); p.update(fit["params"])
    pl = p            # 10_render's convention -- see the note above
    idx = json.load(open(os.path.join(OUT, "parts_index.json")))
    A = np.load(os.path.join(OUT, "mesh_atlas.npz"), allow_pickle=True)
    tri_v0 = A["tri_v"].astype(np.float64)
    tri_uv = A["tri_uv"].astype(np.float64)
    tri_id = A["tri_id"]
    names = [str(n) for n in A["names"]]
    pb = {n: idx["parts"][n]["bone"] for n in names}
    pk = {n: idx["parts"][n]["kind"] for n in names}
    Jr = kp.joints(pl)
    pal = part_palette(len(names))

    # the bind bbox, shared by every gait and every frame so `pos` means the
    # same thing everywhere
    lo = tri_v0.reshape(-1, 3).min(0)
    hi = tri_v0.reshape(-1, 3).max(0)
    span = np.maximum(hi - lo, 1e-6)

    rep = {"note": __doc__.strip().splitlines()[0], "frame": FRAME,
           "bind_bbox_min": [round(float(v), 5) for v in lo],
           "bind_bbox_span": [round(float(v), 5) for v in span],
           "parts_order": names,
           "part_colours": {names[i]: [int(c) for c in pal[i]] for i in range(len(names))},
           "gaits": {}}

    for gait in gaits:
        rj = json.load(open(os.path.join(OUT, "render_%s_fit.json" % gait)))
        scale = rj["px_per_m"]
        tx = FRAME / 2.0
        ty = rj["sole_y"] + rj["ground_calibration_px"]
        z = np.load(os.path.join(OUT, "anim_fit_%s.npz" % gait), allow_pickle=True)
        nm = [str(x) for x in z["names"]]; rn = [str(x) for x in z["rot_names"]]
        N = int(z["frames"])
        d = os.path.join(OUT, "guides_fit", gait, "E")
        os.makedirs(d, exist_ok=True)
        r_, u_ = kp.basis(AZI_E, theta); c_ = kp.cam_dir(AZI_E, theta)
        stats = []
        for i in range(N):
            J = {k: z["joints"][i][j] for j, k in enumerate(nm)}
            ov = {k: z["rots"][i][j].astype(np.float64) for j, k in enumerate(rn)}
            T = PS.bone_transforms(Jr, J, ov)
            V = PS.pose_tris(tri_v0, tri_id, names, pb, pk, T, pl)
            flat = V.reshape(-1, 3)
            xy = np.stack([flat @ r_ * scale + tx, -(flat @ u_) * scale + ty], -1)
            xy = xy.reshape(len(V), 3, 2)
            zz = (-(flat @ c_)).reshape(len(V), 3)
            # attributes: atlas u, v, then the REST position (3), interpolated
            at = np.zeros((len(V), 3, 5))
            at[:, :, 0:2] = tri_uv
            at[:, :, 2:5] = (tri_v0 - lo) / span
            zb, ib, ab, _ = raster(xy, zz, at, FRAME, FRAME)
            solid = ib >= 0
            pid = np.where(solid, tri_id[np.clip(ib, 0, len(V) - 1)], -1)

            uv = np.zeros((FRAME, FRAME, 3), np.uint8)
            uv[..., 0] = np.where(solid, np.clip(ab[..., 0] * 255, 0, 255), 0)
            uv[..., 1] = np.where(solid, np.clip(ab[..., 1] * 255, 0, 255), 0)
            Image.fromarray(uv).save(os.path.join(d, "uv_%02d.png" % i))

            part = np.zeros((FRAME, FRAME, 3), np.uint8)
            part[solid] = pal[pid[solid]]
            Image.fromarray(part).save(os.path.join(d, "part_%02d.png" % i))

            pos = np.zeros((FRAME, FRAME, 3), np.uint8)
            for k in range(3):
                pos[..., k] = np.where(solid, np.clip(ab[..., 2 + k] * 255, 0, 255), 0)
            Image.fromarray(pos).save(os.path.join(d, "pos_%02d.png" % i))

            Image.fromarray((solid * 255).astype(np.uint8)).convert("RGB").save(
                os.path.join(d, "mask_%02d.png" % i))
            stats.append(dict(frame=i, solid_px=int(solid.sum()),
                              pieces_visible=int(len(np.unique(pid[solid])))))
            print("  %s %02d  solid %6d px  %2d pieces"
                  % (gait, i, stats[-1]["solid_px"], stats[-1]["pieces_visible"]))
        rep["gaits"][gait] = dict(frames=N, dir=d, px_per_m=scale,
                                  ty=ty, tx=tx, theta=theta, per_frame=stats)
    with open(os.path.join(OUT, "guides_index.json"), "w") as f:
        json.dump(rep, f, indent=1)
    print("wrote", os.path.join(OUT, "guides_index.json"))


if __name__ == "__main__":
    main()
