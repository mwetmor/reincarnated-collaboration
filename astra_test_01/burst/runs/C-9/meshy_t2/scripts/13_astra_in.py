#!/usr/bin/env python3
"""C-9 meshy_t2 step 10: the Astra paint canvases.

    python3 scripts/13_astra_in.py

Schema-identical to meshy_t1/astra_in (the knight's, built by the parallel T1
session) so ONE cut-back implementation serves both: 1536 x 1024 plate of pure
#00ff00, 4 columns x 3 rows, cell 384 x 341 with row heights [341, 341, 342],
and a per-sheet `_sheet_layout.json` whose cells each carry
`crop = [x, y, w, h]`, `scale` and `source`. Cut-back is the stated inverse:
crop the painted cell, resize to crop[2] x crop[3], paste at (crop[0],
crop[1]) into a 512 x 512 frame.

Sheets, per clip:
  mc_<clip>_E     every frame of the E view    (D+1, Astra paints each cell)
  mc_<clip>_SE    every frame of the SE view   (D+1)
  mc_keys_pN      12 cells of the OTHER SIX directions x 2 keys (D+2; EbSynth
                  propagates the remaining frames from these)
The run has 8 frames, so its E and SE sheets fill 8 of the 12 cells and the
layout names only the cells that are used.

THE CROP IS PER SHEET, computed from that sheet's own silhouettes and then
widened to the cell's 384:341 aspect. It is LANDSCAPE here, where the knight's
was portrait (175 x 114 for a man): this manticore is 1.82 m long and 1.20 m
tall, so a portrait window would either cut the tail off or paint the animal
at a third of the available resolution.
"""
import json, os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
ASTRA = os.path.join(ROOT, "astra_in")
PLATE = (0, 255, 0)
SHEET = (1536, 1024)
COLS, ROWS = 4, 3
CELL = (384, 341)
ROW_H = [341, 341, 342]
FRAME_PX = 512
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
FULL_DIRS = ["E", "SE"]
# R-C9-66: Matt chose per-frame paint as the PRIMARY method, so every
# direction now needs a full 4x3 cycle sheet, not two keys.
ALL_FULL = DIRS
KEY_DIRS = [d for d in DIRS if d not in FULL_DIRS]
CLIPS = [("walk", 12), ("run", 8), ("idle", 12), ("attack", 12)]
PREFIX = "mc"                     # manticore, so the sheets cannot be confused
                                  # with meshy_t1's knight sheets in a burst


def colour_path(clip, d, i):
    return os.path.join(OUT, clip, "colour", d, "%s_%s_%02d.png" % (clip, d, i))


def mask_path(clip, d, i):
    return os.path.join(OUT, clip, "guides_mask", d, "mask_%s_%02d.png" % (d, i))


def srgb(x):
    x = np.clip(np.asarray(x, dtype=np.float64), 0.0, 1.0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(x, 1 / 2.4) - 0.055)


# WHICH WAY THE HEAD FACES IS SETTLED BY THE AZIMUTH, not by colour. The rig
# faces +Y and S is the camera at 0 deg, so the geometry is exact and needs no
# measuring. A bare-skin threshold cannot do it: measured over all 128 cells,
# N spans 0.017-0.078 and NE/NW span 0.048-0.121, so they OVERLAP across
# 0.048-0.078 and no single cut separates them. Labelling by colour put walk N
# and idle N -- which are plainly the back of a head -- in the same class as
# the rear three-quarters.
#
# The measurement still earns its place, for the thing the azimuth cannot
# know: the head TURNS within a clip. So the nominal view comes from the
# direction and the per-cell number flags the cells where the turn has moved
# the head off it.
NOMINAL_VIEW = {"S": "face", "SE": "face", "SW": "face",
                "E": "profile", "W": "profile",
                "NE": "edge", "NW": "edge", "N": "back"}
TURN_TOL = 0.28          # fractional deviation from the direction's own median
FACE_MEANING = {
    "face": "the man's face is square to the camera - eyes, nose, mouth all visible",
    "profile": "the face is in profile - one eye, the nose line, the full beard",
    "edge": "REAR THREE-QUARTER: mostly the back of the head and hair, with only "
            "a sliver of cheek and the edge of the beard. Do NOT draw a full face here",
    "back": "THE BACK OF THE HEAD: hair only. No eye, no nose, no mouth",
}


def face_visibility(clip, d, i):
    """How much of the man's face this cell shows, from the render itself."""
    rp = json.load(open(os.path.join(OUT, clip, "render_%s.json" % clip)))
    col = srgb(np.array(rp["guides"]["bone_colours"]["head"], dtype=np.float64))
    a = np.asarray(Image.open(os.path.join(
        OUT, clip, "guides_part", d, "part_%s_%02d.png" % (d, i))).convert("RGBA")
    ).astype(np.float64)
    hit = (a[..., 3] > 128) & (np.abs(a[..., :3] / 255.0 - col).max(-1) < 0.02)
    if hit.sum() < 20:
        return 0.0, "back"
    ys, xs = np.nonzero(hit)
    bb = (max(0, xs.min() - 10), max(0, ys.min() - 10),
          min(FRAME_PX, xs.max() + 11), min(FRAME_PX, ys.max() + 11))
    im = np.asarray(Image.open(os.path.join(
        OUT, clip, "colour", d, "%s_%s_%02d.png" % (clip, d, i))).convert("RGBA")
    ).astype(np.float64)
    sub = im[bb[1]:bb[3], bb[0]:bb[2]]
    al = sub[..., 3] > 128
    rgb = sub[..., :3] / 255.0
    sel = al & ((rgb[..., 0] - rgb[..., 2]) > 0.20) & (rgb.mean(-1) > 0.62)
    return round(float(sel.sum()) / max(int(al.sum()), 1), 4)


def cell_box(k):
    col, row = k % COLS, k // COLS
    return col, row, col * CELL[0], sum(ROW_H[:row]), CELL[0], ROW_H[row]


def silhouette_bbox(paths, pad=8):
    lo = [10 ** 9, 10 ** 9]; hi = [-1, -1]
    for p in paths:
        q = p[1] if os.path.exists(p[1]) else p[0]
        if not os.path.exists(q):
            continue
        al = Image.open(q).convert("RGBA").getchannel("A")
        bb = al.point(lambda v: 255 if v > 100 else 0).getbbox()
        if not bb:
            continue
        lo[0] = min(lo[0], bb[0]); lo[1] = min(lo[1], bb[1])
        hi[0] = max(hi[0], bb[2]); hi[1] = max(hi[1], bb[3])
    if hi[0] < 0:
        return None
    x0, y0, x1, y1 = lo[0] - pad, lo[1] - pad, hi[0] + pad, hi[1] + pad
    aspect = CELL[0] / CELL[1]
    w, h = x1 - x0, y1 - y0
    if w / h < aspect:
        need = aspect * h - w
        x0 -= need / 2.0; x1 += need / 2.0
    else:
        need = w / aspect - h
        y0 -= need / 2.0; y1 += need / 2.0
    x0 = max(0, int(round(x0))); y0 = max(0, int(round(y0)))
    x1 = min(FRAME_PX, int(round(x1))); y1 = min(FRAME_PX, int(round(y1)))
    return [x0, y0, x1 - x0, y1 - y0]


def build(cells, crop, path, sheet_name):
    """cells: list of (src_png|None, meta). Writes the plate and the layout."""
    sheet = Image.new("RGB", SHEET, PLATE)
    lay_cells = []
    sx = CELL[0] / crop[2]
    for k, (src, meta) in enumerate(cells):
        col, row, x, y, w, h = cell_box(k)
        if src and os.path.exists(src):
            im = Image.open(src).convert("RGBA").crop(
                (crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3]))
            flat = Image.new("RGBA", im.size, PLATE + (255,))
            flat.alpha_composite(im)
            sheet.paste(flat.convert("RGB").resize((w, h), Image.LANCZOS), (x, y))
        lay_cells.append(dict(cell=k, col=col, row=row, x=x, y=y, w=w, h=h,
                              crop=list(crop), frame_px=FRAME_PX,
                              scale=round(sx, 5),
                              source=(os.path.relpath(src, ROOT) if src else None),
                              **meta))
    sheet.save(path)
    lay = dict(sheet=sheet_name, sheet_px=list(SHEET), cell_px=list(CELL),
               row_heights=ROW_H, cols=COLS, rows=ROWS, game_frame_px=FRAME_PX,
               plate="#00ff00",
               cut_back="for each cell: crop the painted cell, resize to "
                        "crop[2]xcrop[3], paste at (crop[0], crop[1]) into a "
                        "512x512 frame",
               n_cells=sum(1 for c in cells if c[0]),
               cells=lay_cells)
    json.dump(lay, open(path.replace(".png", "_sheet_layout.json"), "w"), indent=1)
    return lay


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", default=None,
                    help="directions to emit as FULL cycle sheets "
                         "(default: E,SE only)")
    ap.add_argument("--no-keys", action="store_true",
                    help="skip the two-key plates (superseded by full sheets)")
    args = ap.parse_args()
    os.makedirs(ASTRA, exist_ok=True)
    sheets = []

    for clip, n in CLIPS:
        for d in (args.dirs.split(",") if args.dirs else FULL_DIRS):
            paths = [(colour_path(clip, d, i), mask_path(clip, d, i)) for i in range(n)]
            crop = silhouette_bbox(paths)
            if crop is None:
                print("  SKIP %s %s (no frames rendered)" % (clip, d)); continue
            fvs = [face_visibility(clip, d, i) for i in range(n)]
            med = float(np.median(fvs))
            cells = []
            for i in range(12):
                if i < n:
                    dev = (fvs[i] - med) / max(med, 1e-6)
                    turn = ("more face than the rest of this sheet"
                            if dev > TURN_TOL else
                            ("less face than the rest of this sheet"
                             if dev < -TURN_TOL else None))
                    cells.append((colour_path(clip, d, i),
                                  dict(state=clip, dir=d, frame=i,
                                       face_visibility=fvs[i],
                                       head_view=NOMINAL_VIEW[d],
                                       head_turn=turn)))
                else:
                    cells.append((None, dict(state=clip, dir=d, frame=None)))
            name = "%s_%s_%s.png" % (PREFIX, clip, d)
            build(cells, crop, os.path.join(ASTRA, name), name)
            views = {NOMINAL_VIEW[d]: list(range(n))}
            turned = {c[1]["frame"]: c[1]["head_turn"] for c in cells[:n]
                      if c[1].get("head_turn")}
            sheets.append(dict(file=name, kind="full", state=clip, dir=d, part=0,
                               cells=n, crop=crop,
                               scale=round(CELL[0] / crop[2], 5),
                               head_view=NOMINAL_VIEW[d],
                               head_view_meaning=FACE_MEANING[NOMINAL_VIEW[d]],
                               head_turn_cells=turned,
                               face_visibility_median=round(med, 4),
                               face_visibility=[c[1]["face_visibility"] for c in cells[:n]]))
            print("  %-22s %2d cells  %-8s med %.3f%s"
                  % (name, n, NOMINAL_VIEW[d], med,
                     ("   TURN: " + "; ".join("f%d %s" % (k, v)
                                              for k, v in sorted(turned.items())))
                     if turned else ""))

    # key sheets: every clip x the six non-painted directions x 2 keys,
    # packed 12 to a plate exactly as meshy_t1 does
    key_cells = []
    for clip, n in ([] if args.no_keys else CLIPS):
        for d in KEY_DIRS:
            for kf in (0, n // 2):
                key_cells.append((colour_path(clip, d, kf),
                                  dict(state=clip, dir=d, frame=kf)))
    for part in range((len(key_cells) + 11) // 12):
        chunk = key_cells[part * 12:(part + 1) * 12]
        paths = [(c[0], mask_path(c[1]["state"], c[1]["dir"], c[1]["frame"]))
                 for c in chunk]
        crop = silhouette_bbox(paths)
        if crop is None:
            continue
        while len(chunk) < 12:
            chunk.append((None, dict(state=None, dir=None, frame=None)))
        name = "%s_keys_p%d.png" % (PREFIX, part)
        build(chunk, crop, os.path.join(ASTRA, name), name)
        sheets.append(dict(file=name, kind="keys", part=part,
                           cells=sum(1 for c in chunk if c[0]), crop=crop,
                           scale=round(CELL[0] / crop[2], 5),
                           contents=[dict(c[1]) for c in chunk if c[0]]))
        print("  %-22s %2d cells  crop %s" % (name, sum(1 for c in chunk if c[0]), crop))

    manifest = dict(
        note="C-9 meshy_t2 step 10: Astra paint canvases for the MANTICORE "
             "(Rochester Bestiary, c.1230), quadruped rig built and animated in "
             "Blender because the Meshy API rig is biped-only.",
        schema="identical to meshy_t1/astra_in so one cut-back serves both",
        sheet_px=list(SHEET), cell_px=list(CELL), row_heights=ROW_H,
        game_frame_px=FRAME_PX, grid=[COLS, ROWS], plate="#00ff00",
        px_per_m=110.1852, px_per_m_source="the knight's 198.333 px / 1.80 m; "
                                           "the manticore renders at the same WORLD "
                                           "scale and so comes out ~132 px tall",
        sole_row=398, elevation_deg=19.77,
        azimuths={"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225,
                  "W": 270, "SW": 315},
        full_paint_dirs=(args.dirs.split(",") if args.dirs else FULL_DIRS),
        key_dirs=KEY_DIRS,
        nominal_view=NOMINAL_VIEW,
        head_turn_tolerance=TURN_TOL,
        face_meaning=FACE_MEANING,
        face_note="head_view is fixed by the AZIMUTH -- the rig faces +Y and "
                  "S is the camera at 0 deg, so it is exact. face_visibility is "
                  "the bare-skin fraction of the head box measured on the "
                  "render; it is NOT used to classify (N spans 0.017-0.078 and "
                  "NE/NW span 0.048-0.121, so they overlap and no threshold "
                  "separates them) but it does catch the head TURNING inside a "
                  "clip, which the azimuth cannot know. head_turn_cells names "
                  "the frames that sit more than 28 % off their own sheet's "
                  "median -- those are the cells where a uniform instruction "
                  "would be wrong.",
        clips={c: dict(frames=n, keys=[0, n // 2]) for c, n in CLIPS},
        sheets=sheets,
        totals=dict(sheets=len(sheets),
                    full=sum(1 for s in sheets if s["kind"] == "full"),
                    key=sum(1 for s in sheets if s["kind"] == "keys"),
                    key_cells=len(key_cells)),
        guides={c: dict(
            pos="out/%s/guides_pos/{dir}/pos_{dir}_{NN}.png" % c,
            part="out/%s/guides_part/{dir}/part_{dir}_{NN}.png" % c,
            mask="out/%s/guides_mask/{dir}/mask_{dir}_{NN}.png" % c,
            colour="out/%s/colour/{dir}/%s_{dir}_{NN}.png" % (c, c),
            frames=n) for c, n in CLIPS},
        ebsynth_weights=dict(pos=4.0, part=2.0, mask=2.0,
                             ref="knight3d/scripts/24_ebsynth.py"),
        next_steps=[
            "gandalf fires the Astra bursts on astra_in/mc_*.png",
            "drax cuts each painted sheet back with its _sheet_layout.json",
            "EbSynth propagates the six two-key directions, guides pos(4) part(2) mask(2)",
            "assemble sprites_t2/{state}/{dir}/{state}_{dir}_NN.png plus a manifest"])
    json.dump(manifest, open(os.path.join(ASTRA, "manifest.json"), "w"), indent=1)
    print("wrote %s - %d sheets (%d full, %d key, %d key cells)"
          % (os.path.join(ASTRA, "manifest.json"), len(sheets),
             manifest["totals"]["full"], manifest["totals"]["key"], len(key_cells)))


if __name__ == "__main__":
    main()
