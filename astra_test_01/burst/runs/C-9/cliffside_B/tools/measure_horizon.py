#!/usr/bin/env python3
"""C-9 R-C9-41: where each parallax layer actually lands ON SCREEN, in A and in B.

Matt: "the horizon is far too large; match it to the other cliffside." The offsets that
build_b_assets.py computes are in LAYER pixels; what Matt sees is a SCREEN row, and the
two are only the same number if the Parallax2D maths does what you assume it does. So
this does not assume it: it renders each layer ALONE at a named camera (shot_bridge.gd's
SHOT_ONLY), finds the row where that layer's coverage crosses 50 % -- its ridge, its
treeline -- and reports A against B on the same screen.

    python3 tools/measure_horizon.py                     both cameras, all four layers
    python3 tools/measure_horizon.py --cams bridge       one camera

Writes frames/horizon_rows.json.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

PROJ = Path(__file__).resolve().parent.parent
OUT = PROJ / "frames" / "horizon_rows.json"
GODOT = os.environ.get("GODOT", "/Applications/Godot.app/Contents/MacOS/Godot")
LOCK = os.environ.get(
    "HEAVY_LOCK",
    str(Path.home() / "Games/reincarnated-collaboration/astra_test_01/burst/runs/"
        "C-7/conductor_scripts/heavy_lock.py"))

# The two cameras the brief names. The bridge value is the one the earlier far-layer
# framing was measured at, kept so the numbers stay comparable.
#
# The PLATEAU is the west plateau's northern lip, NOT the far-plateau clearing across
# the bridge. The clearing was the obvious reading of "plateau" -- it is the one the
# C-7 README names -- and it is the wrong camera for this question: standing in it you
# are looking at meadow, the far layer is a sliver in one corner, and in A there is no
# cathedral there at all. The conductor's test for the right camera was "in A the
# cathedral reads top-left", and that is this one.
CAMS = {"bridge": (2700, 1500), "plateau": (2200, 2000)}
LAYERS = ["far_ruins", "forest_valley", "sky", "mist"]


def shoot(out_dir, name, style, pos, only=""):
    env = dict(os.environ)
    env.update({"SHOT_OUT": str(out_dir), "SHOT_NAME": name, "SHOT_STYLE": style,
                "SHOT_POS": "%g,%g" % pos, "SHOT_ONLY": only})
    subprocess.run([sys.executable, LOCK, "C-9", "--", GODOT, "--path", str(PROJ),
                    "--resolution", "1920x1080", "--script", "tools/shot_bridge.gd"],
                   env=env, check=True, capture_output=True)
    return Image.open(Path(out_dir) / (name + ".png")).convert("RGB")


def rows(img, tol=12):
    """First row whose non-background coverage crosses 50 %, and the first row that has
    ANY. With one layer visible the rest of the frame is the clear colour, so 'not the
    clear colour' is exactly 'this layer'.

    The background is READ from the frame's own top-left corner rather than assumed to
    be black -- and the HUD is hidden by shot_bridge.gd, because a full-width panel on
    row 0 makes every layer's 'first row' 0 and the measure returns nothing but zeros.
    """
    a = np.asarray(img).astype(np.int16)
    bg = a[2, 2]
    m = (np.abs(a - bg).max(2) > tol)
    cov = m.mean(1)
    solid = int(np.argmax(cov > 0.5)) if (cov > 0.5).any() else -1
    first = int(np.argmax(cov > 0.002)) if (cov > 0.002).any() else -1
    return first, solid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cams", nargs="*", default=list(CAMS))
    a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp(prefix="c9_horizon_"))
    rep = {}
    print("%-9s %-14s %-6s %8s %8s" % ("camera", "layer", "style", "first", "solid"))
    for cam in a.cams:
        pos = CAMS[cam]
        rep[cam] = {"camera_px": list(pos), "layers": {}}
        for layer in LAYERS:
            rep[cam]["layers"][layer] = {}
            for style in ("A", "B"):
                img = shoot(tmp, "%s_%s_%s" % (cam, layer, style), style, pos, layer)
                f, s = rows(img)
                rep[cam]["layers"][layer][style] = {"first_row": f, "solid_row": s}
                print("%-9s %-14s %-6s %8d %8d" % (cam, layer, style, f, s))
            A = rep[cam]["layers"][layer]["A"]
            B = rep[cam]["layers"][layer]["B"]
            rep[cam]["layers"][layer]["delta_solid_B_minus_A"] = B["solid_row"] - A["solid_row"]
            rep[cam]["layers"][layer]["delta_first_B_minus_A"] = B["first_row"] - A["first_row"]
            print("%-9s %-14s %-6s %8s %8d   <-- B minus A"
                  % ("", "", "delta", rep[cam]["layers"][layer]["delta_first_B_minus_A"],
                     rep[cam]["layers"][layer]["delta_solid_B_minus_A"]))
    OUT.write_text(json.dumps(
        {"note": "C-9 R-C9-41: on-screen rows of each parallax layer, measured by "
                 "rendering it alone (tools/shot_bridge.gd SHOT_ONLY) rather than "
                 "derived from the Parallax2D scroll maths. 1920x1080.",
         "cameras": rep}, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    sys.exit(main())
