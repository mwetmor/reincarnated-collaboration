#!/usr/bin/env python3
"""T7-B: reproduce the Godot B-register ("Illuminated") cliffside frame in Python.

WHY NOT RENDER IT IN GODOT.  shot_bridge.gd can do it, but every Godot invocation
rewrites runs/C-9/cliffside_B/.godot/{uid_cache.bin,editor/filesystem_cache10} -- a
write outside this test's own directory, in a run where other sessions are live.  So
the frame is composited here instead, and the parallax maths is VALIDATED against
frames/horizon_rows.json, which was measured by rendering each layer alone through
the real engine (R-C9-41).  Validation lives in validate_parallax.py; the hard-edged
far_ruins layer agrees to 0.2 px at both measured cameras.

WHAT THE B REGISTER ACTUALLY SHOWS (scripts/style_toggle.gd):
  visible : Layer_sky, Layer_far_ruins (+ Landmark_cathedral, Landmark_tower),
            Layer_forest_valley, Layer_mist, Foreground_0, Foreground_1
  hidden  : Shadows, Overhead, Near_0, Air, and Actors/{Prop_,Glow_,Swarm_}*
  excluded here : Keeper/knight and the two still figures (angel, demon) -- T7-B
            needs the scene with NO characters.
So the composite is exactly plate + parallax + the two B-only far landmarks.

PARALLAX.  Parallax2D overwrites its own position each frame, so the authored
`position` in the .tscn is dead; only scroll_offset and scroll_scale matter.  A layer's
top-left lands on screen at

    screen = scroll_offset - scroll_scale * C + b_offset

with C the camera's world top-left and b_offset the per-style shift that
style_toggle.gd puts on the layer's own Sprite2D (layers_b/offsets.json; A is 0).
The landmarks are SIBLINGS of that Sprite2D under the Parallax2D, so they take the
parallax term but NOT b_offset.

CAMERA.  Camera2D follows the Keeper with offset (-2,-55) so the Keeper lands on the
anchor (962,595) of the 1920x1080 view:  C = keeper - (962,595), clamped by
camera_limits [2,55,5378,4151].  That anchor fraction (0.50104, 0.55093) is the same
pair as PL_ANCHOR_FX/FY in reincarnated-godot/scripts/cliffside_blockout.gd.
"""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

PROJ = Path("/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/cliffside_B")
CANVAS = (5376, 4096)
VIEW = (1920, 1080)
ANCHOR = (962.0, 595.0)
LIMITS = (2, 55, 5378, 4151)  # left, top, right, bottom

# (node, scroll_scale, scroll_offset) in .tscn z order, back to front
LAYERS = [
    ("sky", 0.12, (0, 0)),
    ("far_ruins", 0.25, (0, -416)),
    ("forest_valley", 0.45, (0, 537)),
    ("mist", 0.7, (0, 568)),
]
# children of Layer_far_ruins, by z_index: (file, local position, scale)
LANDMARKS = [
    ("tower.png", (1241.966, 687.910), 0.351724),      # z_index 2
    ("cathedral.png", (461.013, 850.405), 0.759494),   # z_index 3
]
TILES = [("tile_0_0.png", (0, 0)), ("tile_4096_0.png", (4096, 0))]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def camera_topleft(keeper, view):
    """Camera2D world top-left for a Keeper position, clamped by camera_limits."""
    x = keeper[0] - ANCHOR[0]
    y = keeper[1] - ANCHOR[1]
    x = min(max(x, LIMITS[0]), LIMITS[2] - view[0])
    y = min(max(y, LIMITS[1]), LIMITS[3] - view[1])
    return (x, y)


def compose(keeper, view=VIEW, register="B"):
    """Return (RGB frame, manifest dict). `view` may be wider than the game's 1920x1080."""
    lay_dir = PROJ / "parallax" / ("layers_b" if register == "B" else "layers")
    tile_dir = PROJ / "parallax" / ("tiles_b" if register == "B" else "tiles")
    off = {k: 0.0 for k, _, _ in LAYERS}
    offx = dict(off)
    if register == "B":
        j = json.loads((lay_dir / "offsets.json").read_text())
        off = j["offsets"]
        offx = j.get("offsets_x", offx)

    C = camera_topleft(keeper, view)
    used = []
    # Godot clears to default_clear_color before anything draws.
    frame = Image.new("RGBA", view, (23, 31, 43, 255))  # Color(0.09,0.12,0.17)

    def paste(img, x, y):
        # alpha_composite wants a same-size overlay, so place the crop on a blank frame.
        tmp = Image.new("RGBA", view, (0, 0, 0, 0))
        xi, yi = int(round(x)), int(round(y))
        sx, sy = max(0, -xi), max(0, -yi)
        if sx >= img.width or sy >= img.height:
            return
        crop = img.crop((sx, sy, min(img.width, sx + view[0]), min(img.height, sy + view[1])))
        tmp.paste(crop, (xi + sx, yi + sy))
        frame.alpha_composite(tmp)

    for name, s, so in LAYERS:
        p = lay_dir / f"{name}.png"
        img = Image.open(p).convert("RGBA")
        used.append(str(p))
        lx = so[0] - s * C[0]            # Parallax2D own transform (screen space)
        ly = so[1] - s * C[1]
        paste(img, lx + offx.get(name, 0.0), ly + off.get(name, 0.0))
        if name == "far_ruins" and register == "B":
            for fn, lpos, sc in LANDMARKS:
                lp = PROJ / "sprites_landmarks" / fn
                li = Image.open(lp).convert("RGBA")
                used.append(str(lp))
                li = li.resize((max(1, round(li.width * sc)), max(1, round(li.height * sc))),
                               Image.LANCZOS)
                paste(li, lx + lpos[0], ly + lpos[1])

    for fn, wpos in TILES:                # z_index 0, world space, nearest filter
        p = tile_dir / fn
        img = Image.open(p).convert("RGBA")
        used.append(str(p))
        paste(img, wpos[0] - C[0], wpos[1] - C[1])

    man = {
        "register": register,
        "keeper_px": list(keeper),
        "camera_topleft_px": list(C),
        "view_px": list(view),
        "sources": [{"path": u, "sha256": sha256(u)} for u in used],
    }
    return frame.convert("RGB"), man


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keeper", required=True, help="x,y Keeper world position")
    ap.add_argument("--view", default="1920x1080")
    ap.add_argument("--register", default="B", choices=["A", "B"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--manifest", default="")
    a = ap.parse_args()
    kx, ky = (float(v) for v in a.keeper.split(","))
    vw, vh = (int(v) for v in a.view.lower().split("x"))
    frame, man = compose((kx, ky), (vw, vh), a.register)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    frame.save(a.out)
    man["output"] = a.out
    man["output_sha256"] = sha256(a.out)
    if a.manifest:
        Path(a.manifest).write_text(json.dumps(man, indent=1))
    print(json.dumps({k: v for k, v in man.items() if k != "sources"}, indent=1))


if __name__ == "__main__":
    main()
