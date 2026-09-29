#!/usr/bin/env python3
"""T7-B: the capture set for one Marble world, at OUR game camera (R-C9-68).

Produces, into <world_dir>/../views/<tag>_*:
  <tag>_playerlock.png      splats, ortho, pitch 52.95354112560294 deg, yaw 47 deg
  <tag>_collider.png        collider mesh, same camera, vertex colours
  <tag>_slope.png           same camera, walkable-slope ramp
  <tag>_orbit.mp4           36 frames, yaw 0..350, pitch HELD at 52.95 deg
  <tag>_sidebyside.png      one frame beside the painted cliffside at the same framing

The orbit holds pitch and sweeps yaw, so it answers "is this a solid scene or a shell"
-- a shell shows its hollow back within a quarter turn.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

import glb_probe
import mesh_render  # noqa: F401  (imported for its njit rasteriser warm-up)
from render_splats import PL_PITCH_DEG, PL_YAW_DEG, autoframe, load_gaussians, render

HERE = Path(__file__).resolve().parent
PAINTED = HERE.parent / "input" / "cliffside_B_chasm_B_wide_2133x1200.png"


def collider_frame(glb):
    """Centre and vertical extent taken from the COLLIDER's bounds, not the splat
    cloud's: the splats include a far painted shell that would frame the world at
    ~63 units and put the camera outside the bubble."""
    js, bin_ = glb_probe.read_glb(glb)
    V, _ = glb_probe.gather(js, bin_)
    V = V * np.array([1.0, -1.0, -1.0])
    lo, hi = V.min(0), V.max(0)
    return (lo + hi) * 0.5, float(np.max(hi - lo))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="world dir with splats_500k.ply + collider.glb")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--res", default="1920x1080")
    ap.add_argument("--size", type=float, default=0.0)
    ap.add_argument("--zmin", type=float, default=None)
    ap.add_argument("--orbit-frames", type=int, default=36)
    a = ap.parse_args()
    wd, out = Path(a.dir), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    W, H = (int(v) for v in a.res.lower().split("x"))

    ply, glb = wd / "splats_500k.ply", wd / "collider.glb"
    ctr, ext = collider_frame(glb) if glb.exists() else (None, None)
    xyz, scale, quat, op, col = load_gaussians(str(ply))
    if ctr is None:
        ctr, ext = autoframe(xyz, op)
    size_m = a.size if a.size > 0 else ext * 1.05
    zmin = a.zmin if a.zmin is not None else -size_m * 0.5
    rep = {"tag": a.tag, "center": [round(float(x), 3) for x in ctr],
           "size_m": round(size_m, 3), "zmin": round(zmin, 3),
           "pitch_deg": PL_PITCH_DEG, "yaw_deg": PL_YAW_DEG, "res": [W, H]}

    img, st = render(xyz, scale, quat, op, col, ctr, size_m, (W, H), zmin=zmin)
    Image.fromarray((img * 255 + .5).astype(np.uint8)).save(out / f"{a.tag}_playerlock.png")
    rep["playerlock"] = st

    for mode in ("vcol", "slope"):
        subprocess.run([sys.executable, str(HERE / "mesh_render.py"), str(glb),
                        "--out", str(out / f"{a.tag}_{mode}.png"), "--res", a.res,
                        f"--center={ctr[0]},{ctr[1]},{ctr[2]}", "--size", str(size_m),
                        "--mode", mode], check=True, capture_output=True)

    # ---- orbit: yaw sweeps, pitch held at the game value
    fr = out / f"{a.tag}_orbit_frames"
    fr.mkdir(exist_ok=True)
    for i in range(a.orbit_frames):
        yaw = PL_YAW_DEG + 360.0 * i / a.orbit_frames
        im, _ = render(xyz, scale, quat, op, col, ctr, size_m, (960, 540),
                       yaw_deg=yaw, zmin=zmin)
        Image.fromarray((im * 255 + .5).astype(np.uint8)).save(fr / f"f{i:03d}.png")
    mp4 = out / f"{a.tag}_orbit.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "12",
                    "-i", str(fr / "f%03d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "20", str(mp4)], check=True)
    for f in fr.glob("*.png"):
        f.unlink()
    fr.rmdir()
    rep["orbit_mp4"] = str(mp4)

    # ---- side by side with the painted original at the same framing
    left = Image.open(PAINTED).convert("RGB").resize((W, H), Image.LANCZOS)
    right = Image.open(out / f"{a.tag}_playerlock.png").convert("RGB")
    sbs = Image.new("RGB", (W * 2 + 24, H), (12, 12, 16))
    sbs.paste(left, (0, 0)); sbs.paste(right, (W + 24, 0))
    sbs.save(out / f"{a.tag}_sidebyside.png")

    (out / f"{a.tag}_views.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
