#!/usr/bin/env python3
"""T7-B: the decisive shot -- a Marble world at OUR game's actual on-screen scale.

Everything up to here framed the whole world, which flatters it. A player never sees
the whole world: the ratified ortho scale is PPM_ACCEPTED = 100.617553710938 px/m
(cliffside_blockout.gd, R-C3-44/48), so a 1080-row frame covers

    1080 / 100.617553710938 = 10.734 m

of world height. This renders exactly that much, centred on the world's OWN floor --
the area-weighted centroid of collider triangles that are within 30 deg of horizontal
and inside a given radius -- and puts the painted original beside it at the same
metric scale, so the two are honestly comparable.

Scale comes from splats.semantics_metadata.metric_scale_factor when the world has one
(marble-1.1 does; marble-1.0-draft does not, and is rendered in raw units with that
stated in the output).
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

import glb_probe
from render_splats import PL_PITCH_DEG, PL_YAW_DEG, load_gaussians, render

HERE = Path(__file__).resolve().parent
PPM_ACCEPTED = 100.617553710938          # R-C3-44, the game's ratified ortho px/m
PAINTED = HERE.parent / "input" / "cliffside_B_chasm_B_wide_2133x1200.png"


def floor_point(glb, radius_u=10.0, max_tilt=30.0):
    """Area-weighted centroid of the near-horizontal collider triangles."""
    js, bin_ = glb_probe.read_glb(glb)
    V, F = glb_probe.gather(js, bin_)
    V = V * np.array([1.0, -1.0, -1.0])
    p0, p1, p2 = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    n = np.cross(p1 - p0, p2 - p0)
    nl = np.linalg.norm(n, axis=1)
    ok = nl > 1e-12
    area = 0.5 * nl
    tilt = np.full(len(F), 90.0)
    tilt[ok] = np.degrees(np.arccos(np.clip(np.abs(n[ok, 1] / nl[ok]), 0, 1)))
    ctr = (p0 + p1 + p2) / 3.0
    r = np.linalg.norm(ctr[:, [0, 2]], axis=1)
    m = (tilt < max_tilt) & (r < radius_u) & ok
    if m.sum() < 10:
        m = (tilt < max_tilt) & ok
    w = area[m]
    return (ctr[m] * w[:, None]).sum(0) / w.sum(), float(w.sum()), int(m.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scale-factor", type=float, default=1.0,
                    help="metric_scale_factor; 1.0 means the world has none (raw units)")
    ap.add_argument("--res", default="1920x1080")
    a = ap.parse_args()
    wd, out = Path(a.dir), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    W, H = (int(v) for v in a.res.lower().split("x"))

    k = a.scale_factor
    fp, flat_area_u2, ntri = floor_point(wd / "collider.glb")
    view_h_m = H / PPM_ACCEPTED                     # 10.734 m at 1080 rows
    size_u = view_h_m / k                           # the same height in world units

    xyz, scale, quat, op, col = load_gaussians(str(wd / "splats_500k.ply"))
    img, st = render(xyz, scale, quat, op, col, fp, size_u, (W, H), zmin=-size_u * 1.5)
    Image.fromarray((img * 255 + .5).astype(np.uint8)).save(out / f"{a.tag}_gameframe.png")

    # the painting at the same metric scale: it is authored at PPM_ACCEPTED already,
    # so a 1080-row crop of it is 10.734 m -- no rescale, just a centre crop.
    p = Image.open(PAINTED).convert("RGB")
    left = p.crop(((p.width - W) // 2, (p.height - H) // 2,
                   (p.width - W) // 2 + W, (p.height - H) // 2 + H)) \
        if p.width >= W and p.height >= H else p.resize((W, H), Image.LANCZOS)
    right = Image.open(out / f"{a.tag}_gameframe.png").convert("RGB")
    sbs = Image.new("RGB", (W * 2 + 24, H), (12, 12, 16))
    sbs.paste(left, (0, 0)); sbs.paste(right, (W + 24, 0))
    sbs.save(out / f"{a.tag}_gameframe_sidebyside.png")

    rep = {"tag": a.tag, "ppm_accepted": PPM_ACCEPTED,
           "view_height_m": round(view_h_m, 4),
           "metric_scale_factor": k, "view_height_world_units": round(size_u, 4),
           "floor_point_world_units": [round(float(v), 3) for v in fp],
           "floor_tris_used": ntri,
           "flat_area_within_10u": round(flat_area_u2, 2),
           "flat_area_within_10u_m2": round(flat_area_u2 * k * k, 1),
           "render": st}
    (out / f"{a.tag}_gameframe.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
