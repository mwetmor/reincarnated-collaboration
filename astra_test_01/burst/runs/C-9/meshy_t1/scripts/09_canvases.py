#!/usr/bin/env python3
"""C-9 meshy_t1 step 5: build the Astra paint canvases and their layout JSONs.

    python3 scripts/09_canvases.py

Two kinds of sheet, matching the two paint budgets in the pipeline review:

  FULL sheets (D+1) for E and SE, every clip: a 4x3 grid, so one sheet covers a
  12-frame cycle. The run's 8 frames leave four cells empty and the attack's 36
  take three sheets.

  KEY sheets (D+2) for the other six directions: two keys per clip, frames 0
  and N//2 -- the pair the EbSynth test measured best (2-key error 36.5 against
  1-key 47.0) -- packed twelve keys to a sheet.

Each cell is a CROP shared by every frame of that clip and direction, scaled
up to fill the cell. Pasting the whole 512x512 game frame is simpler, but the
knight only occupies about 200 px of it, so five sixths of the canvas would be
empty green and Astra would be painting a 200 px figure -- against the ~890 px
figures of the approved stills. One crop box per (state, direction), taken as
the union of that clip's own alpha bounds plus a margin, keeps the cut-back a
pure grid operation with a single recorded offset and scale, and roughly
doubles the painted resolution.

Background is flat #00ff00 per the register card's PLATE line, so the matte
comes back by keying exactly as the knight stills do.
"""
import json, os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
T1 = os.path.dirname(HERE)
OUT = os.path.join(T1, "out")
ASTRA = os.path.join(T1, "astra_in")
CELL = 512
COLS, ROWS = 4, 3
PLATE = (0, 255, 0)
FULL_DIRS = ["E", "SE"]
ALL_DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
STATES = ["walk", "run", "idle", "attack"]


def on_plate(path, box=None):
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, PLATE + (255,))
    bg.alpha_composite(im)
    rgb = bg.convert("RGB")
    if box:
        rgb = rgb.crop((box[0], box[1], box[0] + box[2], box[1] + box[3]))
        rgb = rgb.resize((CELL, CELL), Image.LANCZOS)
    return rgb


def union_box(paths, margin=14):
    """One crop shared by the whole clip+direction, so the cut-back needs a
    single offset and scale rather than one per cell."""
    lo = [10 ** 9, 10 ** 9]; hi = [-1, -1]
    for p in paths:
        a = np.asarray(Image.open(p).convert("RGBA"))
        m = a[..., 3] > 8
        if not m.any():
            continue
        ys, xs = np.where(m)
        lo[0] = min(lo[0], int(xs.min())); hi[0] = max(hi[0], int(xs.max()))
        lo[1] = min(lo[1], int(ys.min())); hi[1] = max(hi[1], int(ys.max()))
    if hi[0] < 0:
        return [0, 0, CELL, CELL]
    x0 = max(lo[0] - margin, 0); y0 = max(lo[1] - margin, 0)
    x1 = min(hi[0] + margin, CELL - 1); y1 = min(hi[1] + margin, CELL - 1)
    w = x1 - x0 + 1; h = y1 - y0 + 1
    side = max(w, h)                       # square, so the cell is not stretched
    cx = x0 + w / 2.0; cy = y0 + h / 2.0
    x0 = int(round(max(0, min(CELL - side, cx - side / 2.0))))
    y0 = int(round(max(0, min(CELL - side, cy - side / 2.0))))
    return [x0, y0, int(side), int(side)]


def sheet(cells, name, meta):
    im = Image.new("RGB", (CELL * COLS, CELL * ROWS), PLATE)
    lay = []
    for i, c in enumerate(cells):
        if i >= COLS * ROWS:
            break
        r, k = divmod(i, COLS)
        im.paste(on_plate(c["path"], c.get("box")), (k * CELL, r * CELL))
        lay.append(dict(cell=i, col=k, row=r,
                        x=k * CELL, y=r * CELL, w=CELL, h=CELL,
                        state=c["state"], dir=c["dir"], frame=c["frame"],
                        crop=c.get("box"),
                        scale=round(CELL / float(c["box"][2]), 5) if c.get("box") else 1.0,
                        source=os.path.relpath(c["path"], T1)))
    p = os.path.join(ASTRA, name + ".png")
    im.save(p)
    j = dict(sheet=name + ".png", cell=CELL, cols=COLS, rows=ROWS,
             plate="#00ff00", n_cells=len(lay), cells=lay, **meta)
    json.dump(j, open(os.path.join(ASTRA, name + "_sheet_layout.json"), "w"), indent=1)
    return p, j


def main():
    os.makedirs(ASTRA, exist_ok=True)
    man = {"note": __doc__.strip().splitlines()[0], "cell_px": CELL,
           "grid": [COLS, ROWS], "plate": "#00ff00",
           "full_paint_dirs": FULL_DIRS, "sheets": []}
    have = {}
    for st in STATES:
        rp = os.path.join(OUT, st, "render_%s.json" % st)
        if not os.path.exists(rp):
            print("  (skipping %s -- not rendered yet)" % st); continue
        r = json.load(open(rp))
        have[st] = r
    if not have:
        raise SystemExit("no renders found; run scripts/run_all.sh first")

    # ---- FULL sheets: E and SE, every clip ------------------------------
    for st, r in have.items():
        n = r["frames"]
        for d in FULL_DIRS:
            src = os.path.join(OUT, st, "colour", d)
            paths = [os.path.join(src, "%s_%s_%02d.png" % (st, d, i)) for i in range(n)]
            box = union_box(paths)
            cells = [dict(path=paths[i], state=st, dir=d, frame=i, box=box)
                     for i in range(n)]
            for s in range(0, len(cells), COLS * ROWS):
                part = cells[s:s + COLS * ROWS]
                idx = s // (COLS * ROWS)
                nm = "meshy_%s_%s%s" % (st, d, "" if len(cells) <= COLS * ROWS
                                        else "_p%d" % idx)
                p, j = sheet(part, nm, dict(kind="full", state=st, dir=d,
                                            fps=r["fps"], total_frames=n,
                                            part=idx))
                man["sheets"].append(dict(file=os.path.basename(p), kind="full",
                                          state=st, dir=d, part=idx,
                                          cells=len(part)))
                print("  full %-7s %-3s part %d -> %s (%d cells)"
                      % (st, d, idx, os.path.basename(p), len(part)))

    # ---- KEY sheets: the other six directions ---------------------------
    keys = []
    for st, r in have.items():
        n = r["frames"]
        ks = [0, n // 2]
        for d in ALL_DIRS:
            if d in FULL_DIRS:
                continue
            for f in ks:
                src = os.path.join(OUT, st, "colour", d)
                allp = [os.path.join(src, "%s_%s_%02d.png" % (st, d, i))
                        for i in range(n)]
                box = union_box(allp)
                keys.append(dict(path=os.path.join(src, "%s_%s_%02d.png" % (st, d, f)),
                                 state=st, dir=d, frame=f, box=box))
    for s in range(0, len(keys), COLS * ROWS):
        part = keys[s:s + COLS * ROWS]
        idx = s // (COLS * ROWS)
        nm = "meshy_keys_p%d" % idx
        p, j = sheet(part, nm, dict(kind="keys", part=idx))
        man["sheets"].append(dict(file=os.path.basename(p), kind="keys",
                                  part=idx, cells=len(part)))
        print("  keys part %d -> %s (%d cells: %s)"
              % (idx, os.path.basename(p), len(part),
                 ", ".join("%s/%s/%02d" % (c["state"], c["dir"], c["frame"])
                           for c in part)))
    man["totals"] = dict(sheets=len(man["sheets"]),
                         full=sum(1 for s in man["sheets"] if s["kind"] == "full"),
                         key=sum(1 for s in man["sheets"] if s["kind"] == "keys"),
                         key_cells=len(keys))
    json.dump(man, open(os.path.join(ASTRA, "manifest.json"), "w"), indent=1)
    print("\n%d sheets (%d full, %d key) -> %s"
          % (man["totals"]["sheets"], man["totals"]["full"], man["totals"]["key"], ASTRA))


if __name__ == "__main__":
    main()
