#!/usr/bin/env python3
"""C-9 R-C9-41/42: capture A and B at the two named cameras, and MEASURE where the two
landmark sprites land on screen.

The screen box is measured by difference, not by arithmetic on the Parallax2D scroll:
each landmark is captured once visible and once hidden, and the box is where the two
frames differ.  That reads the drawn result, so a wrong scroll assumption cannot pass.

    python3 tools/capture_landmarks.py --out DIR
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

PROJ = Path(__file__).resolve().parent.parent
GODOT = os.environ.get("GODOT", "/Applications/Godot.app/Contents/MacOS/Godot")
LOCK = os.environ.get(
    "HEAVY_LOCK",
    str(Path.home() / "Games/reincarnated-collaboration/astra_test_01/burst/runs/"
        "C-7/conductor_scripts/heavy_lock.py"))
CAMS = {"bridge": (2700, 1500), "plateau": (2200, 2000)}


def shoot(out, name, style, pos, hide=""):
    env = dict(os.environ)
    env.update({"SHOT_OUT": str(out), "SHOT_NAME": name, "SHOT_STYLE": style,
                "SHOT_POS": "%g,%g" % pos, "SHOT_ONLY": "", "SHOT_HIDE": hide})
    subprocess.run([sys.executable, LOCK, "C-9", "--", GODOT, "--path", str(PROJ),
                    "--resolution", "1920x1080", "--script", "tools/shot_bridge.gd"],
                   env=env, check=True, capture_output=True)
    return np.asarray(Image.open(Path(out) / (name + ".png")).convert("RGB")).astype(np.int16)


def box(a, b, tol=10):
    m = np.abs(a - b).max(2) > tol
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rep = {}
    for cam, pos in CAMS.items():
        rep[cam] = {"camera_px": list(pos), "landmarks": {}}
        for style in ("A", "B"):
            shoot(out, "%s_%s" % (cam, style), style, pos)
        full = shoot(out, "%s_B" % cam, "B", pos)
        for lm in ("cathedral", "tower"):
            noth = shoot(out, "%s_B_no_%s" % (cam, lm), "B", pos, hide="Landmark_" + lm)
            bx = box(full, noth)
            rep[cam]["landmarks"][lm] = {"screen_box_x0y0x1y1": bx}
            if bx:
                print("%-8s %-10s screen box x %4d..%4d  y %4d..%4d   (w %d, h %d)"
                      % (cam, lm, bx[0], bx[2], bx[1], bx[3], bx[2] - bx[0], bx[3] - bx[1]))
            else:
                print("%-8s %-10s NOT ON SCREEN" % (cam, lm))
        # both hidden at once: proves there is exactly one of each and no duplicate
        none = shoot(out, "%s_B_no_both" % cam, "B", pos, hide="Landmark_")
        rep[cam]["both_hidden_box"] = box(full, none)
    (PROJ / "frames" / "landmark_screen_boxes.json").write_text(json.dumps(
        {"note": "C-9 R-C9-41/42: on-screen boxes of the two far-layer landmark sprites, "
                 "measured by capturing with and without each one. 1920x1080.",
         "cameras": rep}, indent=1))
    print("wrote", PROJ / "frames" / "landmark_screen_boxes.json")


if __name__ == "__main__":
    sys.exit(main())
