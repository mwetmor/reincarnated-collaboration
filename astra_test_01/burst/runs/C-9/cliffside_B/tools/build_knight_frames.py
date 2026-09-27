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

WALK TIMING -- MATCHED TO THE KEEPER (changed 2026-09-27 on Matt's play note:
"the knight's steps are too slow -- seemingly about half time motion of the keeper").

The knight's walk cadence is now read from the KEEPER'S OWN SpriteFrames in this build
(frames/keeper.tres) rather than derived from the source clips.  Her walk is 12 frames
at 20.7 fps -- 0.5797 s per stride -- and identical in all eight directions, so each
knight walk_<D> gets

    fps_D = 12 / keeper_walk_stride_seconds_D

which lands on the same 20.7 fps.  This is read, not hardcoded: if her cadence is ever
re-tuned, or ever differs per direction, the knight follows it.

WHAT THIS DELIBERATELY DISCARDS.  The previous build played each cell at its own
painted timing, fps_D = 12*24/stride_native_frames (3.130 W .. 6.545 N), so the
footfalls matched the painting.  Those clips are cinematic: 1.83 s to 3.83 s per
stride, against the Keeper's 0.58 s.  That is 3.2x to 6.6x slower than the character
standing beside him in the other register, which is what Matt saw.  Matching her
cadence is a 3.2x-6.6x speed-up and it FLATTENS the per-direction differences the
painter put in -- every direction now plays at one rate because hers does.  The
manifest's stride_native_frames is still recorded per cell in knight_fit.json so the
painted timing is recoverable; it no longer drives playback.

Idle is unchanged: 12 frames over the 2.0 s breath = 6 fps.  The knight has no
run/cast/jump cells; the scene maps run -> walk and cast/jump -> idle for style B and
says so on the HUD.
"""
import json
import re
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
KEEPER_TRES = "frames/keeper.tres"            # the walk cadence the knight must match
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


def keeper_walk_cadence():
    """-> {direction: seconds per walk stride}, read from the Keeper's SpriteFrames.

    The knight must move at the tempo of the character he stands in for, not at the
    tempo of the clip he was painted from, so this is READ from the build rather than
    hardcoded -- re-tune her and he follows.
    """
    text = (PROJ / KEEPER_TRES).read_text()
    body = text[text.index("[resource]"):]
    out = {}
    # Match EVERY animation block, then filter by name. Restricting the name inside the
    # pattern lets the non-greedy .*? run across the blocks that do not match, so a
    # walk_<D> preceded by run_<D>/idle_<D> absorbs their frames: walk_E came out as 332
    # frames / 16.04 s / 0.748 fps instead of 12 / 0.580 s / 20.7. It did not error -- it
    # returned a number, for seven of eight directions correctly, and would have shipped
    # a walk_E taking sixteen seconds per stride.
    pattern = r'\{"frames": \[(.*?)\], "loop": \w+, "name": &"([^"]+)", "speed": ([0-9.]+)\}'
    for frames, name, speed in re.findall(pattern, body, re.S):
        if not name.startswith("walk_"):
            continue
        n = frames.count("ExtResource")
        out[name[5:]] = n / float(speed)
    missing = [d for d in DIRS if d not in out]
    if missing:
        raise SystemExit(f"{KEEPER_TRES}: no walk animation for {missing}")
    return out


def measure(path, report=None):
    """-> (head_row, sole_row, body_centre_x) in source pixels.

    CROWN RULE, corrected 2026-09-27.  The 1xN horizontal opening deletes the pollaxe
    SHAFT and, in doing so, correctly disconnects the AXE BLADE from the figure.  The
    old rule then READMITTED the blade: it kept every component at least 5% of the
    largest, and the blade clears that easily.  For idle_E it returned head row 188 --
    the top of the axe blade -- where the helm crowns at 201, and every E-ish cell came
    out ~7% too tall.  The check ran, returned cleanly, and returned the wrong answer,
    because "the largest component and everything comparable to it" is not the same
    claim as "the figure".

    The 5% clause was there for a real reason -- a leg that splits off at the crotch
    must still count towards the body's centre -- so it is kept, with the one
    qualification that closes the defect: a component may join the body only if it
    starts BELOW the body's own crown.  A split leg does; a blade held over the helm
    does not.  The crown itself is read from the largest component alone.
    """
    a = np.asarray(Image.open(path).convert("RGBA"))[..., 3] > 8
    opened = ndimage.binary_opening(a, structure=np.ones((1, OPEN_W), bool))
    lab, n = ndimage.label(opened)
    if n == 0:
        ys = np.nonzero(a.sum(1))[0]
        return int(ys.min()), int(ys.max()), a.shape[1] / 2.0
    sizes = ndimage.sum(opened, lab, range(1, n + 1))
    main = int(np.argmax(sizes)) + 1
    head = int(np.nonzero(lab == main)[0].min())
    keep = [main]
    for i, s in enumerate(sizes):
        tag = i + 1
        if tag == main or s < 0.05 * sizes.max():
            continue
        if int(np.nonzero(lab == tag)[0].min()) > head:
            keep.append(tag)
    body = np.isin(lab, keep)
    cx = float(np.nonzero(body)[1].mean())
    w = np.array([_widest_run(a[y]) for y in range(a.shape[0])])
    sole = int(np.nonzero(w >= SOLE_MIN_RUN)[0].max())
    if report is not None:
        old_keep = [i + 1 for i, s in enumerate(sizes) if s >= 0.05 * sizes.max()]
        old_head = int(np.nonzero(np.isin(lab, old_keep))[0].min())
        report.append((path.name if hasattr(path, "name") else str(path),
                       old_head, head, sole))
    return head, sole, cx


def main():
    man = json.loads(MANIFEST.read_text())
    cells = man["cells"]
    keeper_stride = keeper_walk_cadence()
    print("keeper walk cadence (read from %s):" % KEEPER_TRES)
    for d in DIRS:
        print(f"  walk_{d:<3} {keeper_stride[d]:.4f} s per 12-frame stride "
              f"= {12.0 / keeper_stride[d]:.3f} fps")

    # ---- measure the Keeper ------------------------------------------------
    keeper_h = []
    crown_report = []
    for d in DIRS:
        h, s, _ = measure(PROJ / "sprites" / "idle" / d / f"idle_{d}_00.png", crown_report)
        keeper_h.append(s - h + 1)
    keeper_src = float(np.mean(keeper_h))
    keeper_canvas = keeper_src * KEEPER_SCALE

    # ---- measure the knight ------------------------------------------------
    knight_h, knight_sole, knight_cx, per_cell = [], [], [], {}
    for d in DIRS:
        for st in ("walk", "idle"):
            rest = RUNS_ROOT / cells[f"{st}_{d}"]["rest"][0]
            h, s, cx = measure(rest, crown_report)
            knight_h.append(s - h + 1)
            knight_sole.append(s)
            knight_cx.append(cx)
            per_cell[f"{st}_{d}"] = {"head": h, "sole": s, "figure_h": s - h + 1}
    knight_src = float(np.mean(knight_h))
    scale = keeper_canvas / knight_src
    pivot_y = float(np.mean(knight_sole))
    pivot_x = float(np.mean(knight_cx))

    moved = [r for r in crown_report if r[1] != r[2]]
    print("crown rule (largest component only, + >=5%% components starting below it):")
    print("  %d of %d measured frames had a component ABOVE the figure readmitted by the"
          % (len(moved), len(crown_report)))
    print("  old >=5%% clause -- the pollaxe blade.  old head -> new head (sole, height):")
    for name, oh, nh, so in moved:
        print("    %-16s %3d -> %3d   sole %3d   height %3d -> %3d"
              % (name, oh, nh, so, so - oh + 1, so - nh + 1))
    if not moved:
        print("    (none)")

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
                painted_fps = 12.0 * cell.get("fps_source", 24) / nf
                fps = 12.0 / keeper_stride[d]          # match the Keeper, not the clip
                note = (f"matched to keeper walk_{d} ({keeper_stride[d]:.4f} s/stride); "
                        f"painted stride was {nf} native frames = {nf / 24.0:.3f} s "
                        f"({painted_fps:.3f} fps), {fps / painted_fps:.2f}x slower than her")
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
        "keeper_walk_stride_seconds": {d: round(keeper_stride[d], 6) for d in DIRS},
        "walk_cadence_source": ("frames/keeper.tres -- the knight matches the Keeper's "
                                "walk stride duration, NOT his own clips' painted timing "
                                "(changed 2026-09-27; see the module docstring)"),
        "painted_walk_fps_superseded": {
            f"walk_{d}": round(12.0 * cells[f"walk_{d}"].get("fps_source", 24)
                               / int(cells[f"walk_{d}"]["stride_native_frames"]), 6)
            for d in DIRS},
        "stride_native_frames": {f"walk_{d}": int(cells[f"walk_{d}"]["stride_native_frames"])
                                 for d in DIRS},
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
