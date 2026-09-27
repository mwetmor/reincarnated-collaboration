#!/usr/bin/env python3
"""C-9: make the Illuminated knight the player sprite for style B.

Reads runs/C-9/artifacts/knight_cells_manifest.json (read-only) and writes, inside
this project:

    sprites_knight/<state>/<D>/<state>_<D>_<nn>.png   16 cells x 12 RGBA frames
    sprites_knight/rest/<state>_<D>.png               the 16 rest frames (reference)
    frames/knight.tres                                SpriteFrames, per-direction speed
    frames/knight_fit.json                            scale / pivot / fps / measurements

NO MIRRORING: all 8 directions exist as painted cells.

SCALE LAW.  The scene draws the Keeper's 512x512 cells at scale 0.6291667 with the
feet pivot at frame row 400 (scenes/cliffside.tscn: offset=(-256,-400)).  The knight's
cells are registered on the same 512x512 canvas by the frozen video_cut transform, but
he is painted SMALLER in-frame than the Keeper, so he needs his own scale.  Both
figures are measured the same way and the knight is scaled so his standing figure
height on the cliffside canvas equals hers.

MEASUREMENT.  "Figure height" = helm/head crown -> sole, in source pixels:

  * the silhouette is horizontally OPENED with a 1x11 structuring element.  This
    deletes the knight's halberd shaft (~6-8 px wide) while keeping the helm (~20 px)
    and the Keeper's neck (~14 px).  Without it the knight's bbox top is the halberd
    spike, which is 30-40 px above his head and would shrink him by ~15%.
  * head crown = top row of the largest surviving component (plus any component at
    least 5% of its area, so a leg that splits off at the crotch still counts).
  * sole      = bottom row of the ORIGINAL mask whose widest contiguous run is >= 12 px.
    The original mask is used because the opening erodes the boot toe; the 12 px floor
    rejects the halberd's butt ferrule, which in several cells reaches below the feet.

  Keeper: 8 idle cells, frame 0.   Knight: all 16 rest frames.

WALK TIMING.  The cells are 12 frames sampled across ONE stride of a 24 fps source
clip whose stride is stride_native_frames long, and that period differs per direction
(44..92 native frames).  Each walk_<D> animation therefore gets its own speed

    fps_D = 12 * 24 / stride_native_frames_D

so one loop takes exactly the stride the painter painted.  Idle is 12 frames over the
2.0 s breath (48 native frames) = 6 fps.  The knight has no run/cast/jump cells; the
scene maps run -> walk and cast/jump -> idle for style B and says so on the HUD.
"""
import json
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

PROJ = Path(__file__).resolve().parent.parent
RUNS_ROOT = PROJ.parents[2]                      # .../burst
MANIFEST = PROJ.parent / "artifacts" / "knight_cells_manifest.json"
OUT_SPRITES = PROJ / "sprites_knight"
OUT_FRAMES = PROJ / "frames"

DIRS = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
KEEPER_SCALE = 0.6291666666666667                # scenes/cliffside.tscn
KEEPER_PIVOT_Y = 400.0                           # offset=(-256,-400)
IDLE_SECONDS = 2.0
OPEN_W = 11                                      # horizontal opening: kills the shaft
SOLE_MIN_RUN = 12                                # a foot is wide; a ferrule is not


def _widest_run(row):
    xs = np.nonzero(row)[0]
    if len(xs) == 0:
        return 0
    best = 1
    s = p = xs[0]
    for x in xs[1:]:
        if x > p + 2:
            best = max(best, p - s + 1)
            s = x
        p = x
    return max(best, p - s + 1)


def measure(path):
    """-> (head_row, sole_row, body_centre_x) in source pixels."""
    a = np.asarray(Image.open(path).convert("RGBA"))[..., 3] > 8
    opened = ndimage.binary_opening(a, structure=np.ones((1, OPEN_W), bool))
    lab, n = ndimage.label(opened)
    if n == 0:
        ys = np.nonzero(a.sum(1))[0]
        return int(ys.min()), int(ys.max()), a.shape[1] / 2.0
    sizes = ndimage.sum(opened, lab, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if s >= 0.05 * sizes.max()]
    body = np.isin(lab, keep)
    ys, xs = np.nonzero(body)
    head = int(ys.min())
    cx = float(xs.mean())
    w = np.array([_widest_run(a[y]) for y in range(a.shape[0])])
    sole = int(np.nonzero(w >= SOLE_MIN_RUN)[0].max())
    return head, sole, cx


def main():
    man = json.loads(MANIFEST.read_text())
    cells = man["cells"]

    # ---- measure the Keeper ------------------------------------------------
    keeper_h = []
    for d in DIRS:
        h, s, _ = measure(PROJ / "sprites" / "idle" / d / f"idle_{d}_00.png")
        keeper_h.append(s - h + 1)
    keeper_src = float(np.mean(keeper_h))
    keeper_canvas = keeper_src * KEEPER_SCALE

    # ---- measure the knight ------------------------------------------------
    knight_h, knight_sole, knight_cx, per_cell = [], [], [], {}
    for d in DIRS:
        for st in ("walk", "idle"):
            rest = RUNS_ROOT / cells[f"{st}_{d}"]["rest"][0]
            h, s, cx = measure(rest)
            knight_h.append(s - h + 1)
            knight_sole.append(s)
            knight_cx.append(cx)
            per_cell[f"{st}_{d}"] = {"head": h, "sole": s, "figure_h": s - h + 1}
    knight_src = float(np.mean(knight_h))
    scale = keeper_canvas / knight_src
    pivot_y = float(np.mean(knight_sole))
    pivot_x = float(np.mean(knight_cx))

    print("scale law")
    print(f"  keeper figure height  {keeper_src:7.2f} src px  x {KEEPER_SCALE:.6f}"
          f"  = {keeper_canvas:6.2f} canvas px   (spread {min(keeper_h)}..{max(keeper_h)})")
    print(f"  knight figure height  {knight_src:7.2f} src px  (spread {min(knight_h)}..{max(knight_h)})")
    print(f"  knight sprite scale   {scale:.6f}   -> {knight_src * scale:6.2f} canvas px")
    print(f"  knight feet pivot     ({pivot_x:.1f}, {pivot_y:.1f}) src px"
          f"   -> offset ({-pivot_x:.2f}, {-pivot_y:.2f})")

    # ---- copy frames -------------------------------------------------------
    if OUT_SPRITES.exists():
        shutil.rmtree(OUT_SPRITES)
    (OUT_SPRITES / "rest").mkdir(parents=True)
    copied = 0
    anims = []
    for d in DIRS:
        for st in ("walk", "idle"):
            cell = cells[f"{st}_{d}"]
            dest = OUT_SPRITES / st / d
            dest.mkdir(parents=True, exist_ok=True)
            names = []
            for i, rel in enumerate(cell["frames"]):
                src = RUNS_ROOT / rel
                if not src.exists():
                    raise SystemExit(f"missing knight frame {src}")
                name = f"{st}_{d}_{i:02d}.png"
                shutil.copyfile(src, dest / name)
                names.append(f"sprites_knight/{st}/{d}/{name}")
                copied += 1
            shutil.copyfile(RUNS_ROOT / cell["rest"][0], OUT_SPRITES / "rest" / f"{st}_{d}.png")
            copied += 1
            if st == "walk":
                nf = int(cell["stride_native_frames"])
                fps = 12.0 * cell.get("fps_source", 24) / nf
                note = f"stride {nf} native frames @ {cell.get('fps_source', 24)} fps = {nf / 24.0:.3f} s"
            else:
                fps = 12.0 / IDLE_SECONDS
                note = f"breath {cell.get('breath_native_frames', 48)} native frames = {IDLE_SECONDS:.1f} s"
            anims.append({"name": f"{st}_{d}", "fps": fps, "frames": names, "note": note})
    print(f"copied {copied} knight pngs -> {OUT_SPRITES}")

    # ---- SpriteFrames ------------------------------------------------------
    ext, ids = [], {}
    for a in anims:
        for p in a["frames"]:
            if p not in ids:
                ids[p] = str(len(ids) + 1)
                ext.append(f'[ext_resource type="Texture2D" path="res://{p}" id="{ids[p]}"]')
    blocks = []
    for a in anims:
        fr = ",\n".join(f'{{"duration": 1.0, "texture": ExtResource("{ids[p]}")}}' for p in a["frames"])
        blocks.append('{"frames": [%s], "loop": true, "name": &"%s", "speed": %.6f}'
                      % (fr, a["name"], a["fps"]))
    OUT_FRAMES.mkdir(exist_ok=True)
    (OUT_FRAMES / "knight.tres").write_text(
        f"[gd_resource type=\"SpriteFrames\" load_steps={len(ext) + 1} format=3]\n\n"
        + "\n".join(ext)
        + "\n\n[resource]\nanimations = [" + ",\n".join(blocks) + "]\n")
    print(f"wrote {OUT_FRAMES / 'knight.tres'}  ({len(anims)} animations, {len(ids)} textures)")

    fit = {
        "note": "C-9 knight-as-player fit for style B. Written by tools/build_knight_frames.py.",
        "keeper": {"figure_h_src_px": keeper_src, "scale": KEEPER_SCALE,
                   "figure_h_canvas_px": keeper_canvas, "pivot_y_src_px": KEEPER_PIVOT_Y,
                   "per_direction_figure_h": dict(zip(DIRS, [int(v) for v in keeper_h]))},
        "knight": {"figure_h_src_px": knight_src, "scale": scale,
                   "figure_h_canvas_px": knight_src * scale,
                   "offset": [-pivot_x, -pivot_y], "per_cell": per_cell},
        "animation_fps": {a["name"]: round(a["fps"], 6) for a in anims},
        "animation_note": {a["name"]: a["note"] for a in anims},
        "state_map_b": {"walk": "walk", "idle": "idle", "run": "walk",
                        "cast": "idle", "jump": "idle"},
    }
    (OUT_FRAMES / "knight_fit.json").write_text(json.dumps(fit, indent=1))
    print(f"wrote {OUT_FRAMES / 'knight_fit.json'}")
    for a in anims:
        if a["name"].startswith("walk"):
            print(f"   {a['name']:<8} {a['fps']:6.3f} fps   ({a['note']})")


if __name__ == "__main__":
    sys.exit(main())
