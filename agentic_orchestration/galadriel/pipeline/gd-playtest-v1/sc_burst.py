#!/usr/bin/env python3
"""SHADOW-CAL: pull a burst of consecutive frames at full resolution."""
import argparse
import os
import subprocess

SRC = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"


def burst(t0, n, out_dir, src=SRC, ext="png", crop=None, stride=1):
    os.makedirs(out_dir, exist_ok=True)
    pre = max(0.0, t0 - 3.0)
    vf = []
    if stride > 1:
        vf.append(f"select='not(mod(n\\,{stride}))'")
    if crop:
        vf.append("crop=%d:%d:%d:%d" % crop)   # w:h:x:y
    cmd = ["ffmpeg", "-v", "error", "-y",
           "-ss", f"{pre:.5f}", "-i", src,
           "-ss", f"{t0 - pre:.5f}"]
    if vf:
        cmd += ["-vf", ",".join(vf)]
    cmd += ["-vsync", "0", "-frames:v", str(n)]
    if ext == "jpg":
        cmd += ["-q:v", "2"]
    cmd += [os.path.join(out_dir, f"b%04d.{ext}")]
    subprocess.run(cmd, check=True)
    return sorted(os.path.join(out_dir, f) for f in os.listdir(out_dir)
                  if f.endswith("." + ext))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--t", type=float, required=True)
    ap.add_argument("--n", type=int, default=90)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ext", default="png")
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--crop", type=int, nargs=4, default=None)
    a = ap.parse_args()
    p = burst(a.t, a.n, a.out, ext=a.ext,
              crop=tuple(a.crop) if a.crop else None, stride=a.stride)
    print(f"{len(p)} frames -> {a.out}")
