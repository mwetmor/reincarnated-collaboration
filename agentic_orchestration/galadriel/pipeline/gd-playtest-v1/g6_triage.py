#!/usr/bin/env python3
"""
G-6 pass 1: TRIAGE the 313 play-test-v1 stills.

Goal: separate non-gameplay UI frames (skill/mastery window, character sheet,
inventory, devotion) from gameplay frames, cheaply, before any per-frame read.

METHOD (cheap-first, per galadriel methodology):
  1. Decode once at native res, emit a 320x180 thumbnail (cached to disk).
  2. Compute per-frame features from the thumbnail only:
       - global mean V (brightness) and mean S (saturation) in HSV
       - dark-and-desaturated fraction (GD UI panels are dark brown chrome)
       - column-brightness profile -> detect a wide, vertically-uniform
         low-variance band = a panel edge
       - "panel score" per half of the screen (GD opens character/skill on the
         left, inventory on the right, devotion near-fullscreen)
       - temporal self-similarity to neighbours (UI frames are near-static
         across consecutive presses; gameplay frames churn)
  3. Emit a CSV of features + contact sheets (40 frames/sheet, ID-labelled)
     for human/multimodal visual scan. NOTHING is classified by threshold
     alone -- the features RANK candidates; the eye confirms.

No image is destructively transformed: thumbnails are additive, originals are
never written. Every downstream crop records its source frame + pixel box.
"""
import csv
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-gd-playtest-v1-g6")
THUMBS = OUT / "thumbs"
SHEETS = OUT / "sheets"

TW, TH = 320, 180
FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def load_font(size):
    for p in FONT_PATHS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def frame_ids():
    ids = []
    for f in SRC.iterdir():
        n = f.name
        if n.startswith("Screenshot (") and n.endswith(").png"):
            ids.append(int(n[len("Screenshot ("):-len(").png")]))
    return sorted(ids)


def src_path(i):
    return SRC / f"Screenshot ({i}).png"


def thumb_path(i):
    return THUMBS / f"{i:04d}.png"


def build_thumbs(ids):
    meta = {}
    for i in ids:
        tp = thumb_path(i)
        sp = src_path(i)
        st = sp.stat()
        if not tp.exists():
            with Image.open(sp) as im:
                meta[i] = (im.width, im.height)
                im = im.convert("RGB").resize((TW, TH), Image.BILINEAR)
                im.save(tp)
        if i not in meta:
            with Image.open(sp) as im:
                meta[i] = (im.width, im.height)
        meta[i] = (meta[i][0], meta[i][1], st.st_mtime, st.st_size)
    return meta


def rgb_to_hsv_arr(a):
    a = a.astype(np.float32) / 255.0
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    v = mx
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
    return s, v


def features(ids):
    rows = []
    prev = None
    arrs = {}
    for i in ids:
        with Image.open(thumb_path(i)) as im:
            a = np.asarray(im.convert("RGB"))
        arrs[i] = a
        s, v = rgb_to_hsv_arr(a)
        # GD UI chrome: dark, low-saturation-to-brown, very flat
        dark_desat = float(((v < 0.30) & (s < 0.45)).mean())
        # per-half panel score: flatness of local 8x8 blocks in the dark range
        h, w = v.shape
        halves = {}
        for name, sl in (("L", slice(0, w // 2)), ("R", slice(w // 2, w))):
            vv = v[:, sl]
            ss = s[:, sl]
            halves[name + "_dark"] = float(((vv < 0.30) & (ss < 0.45)).mean())
            halves[name + "_v"] = float(vv.mean())
        # column profile: count columns whose vertical std is very low (flat panel bg)
        colstd = v.std(axis=0)
        flatcols = float((colstd < 0.10).mean())
        rowstd = v.std(axis=1)
        flatrows = float((rowstd < 0.10).mean())
        row = dict(
            id=i,
            mean_v=float(v.mean()),
            mean_s=float(s.mean()),
            dark_desat=dark_desat,
            flatcols=flatcols,
            flatrows=flatrows,
            **halves,
        )
        rows.append(row)
    # temporal delta
    for k, row in enumerate(rows):
        i = row["id"]
        d = []
        for j in (k - 1, k + 1):
            if 0 <= j < len(rows):
                a = arrs[i].astype(np.int16)
                b = arrs[rows[j]["id"]].astype(np.int16)
                d.append(float(np.abs(a - b).mean()))
        row["delta_min"] = min(d) if d else 999.0
    return rows


def contact_sheets(ids, cols=5, rows_per=8):
    font = load_font(22)
    per = cols * rows_per
    cw, ch = TW, TH + 26
    n = 0
    made = []
    for start in range(0, len(ids), per):
        chunk = ids[start:start + per]
        sheet = Image.new("RGB", (cols * cw, rows_per * ch), (12, 12, 14))
        d = ImageDraw.Draw(sheet)
        for k, i in enumerate(chunk):
            r, c = divmod(k, cols)
            with Image.open(thumb_path(i)) as im:
                sheet.paste(im.convert("RGB"), (c * cw, r * ch + 26))
            d.text((c * cw + 6, r * ch + 2), f"{i}", fill=(255, 230, 120), font=font)
        p = SHEETS / f"sheet-{n:02d}_{chunk[0]}-{chunk[-1]}.png"
        sheet.save(p)
        made.append(str(p))
        n += 1
    return made


def main():
    THUMBS.mkdir(parents=True, exist_ok=True)
    SHEETS.mkdir(parents=True, exist_ok=True)
    ids = frame_ids()
    print(f"frames: {len(ids)}  range {ids[0]}..{ids[-1]}", flush=True)
    meta = build_thumbs(ids)
    dims = {(m[0], m[1]) for m in meta.values()}
    print("resolutions:", dims, flush=True)
    rows = features(ids)
    for row in rows:
        m = meta[row["id"]]
        row["mtime"] = m[2]
        row["bytes"] = m[3]
    with open(OUT / "triage-features.csv", "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)
    sheets = contact_sheets(ids)
    print(f"sheets: {len(sheets)}")
    # rank UI candidates
    ranked = sorted(rows, key=lambda r: -(r["dark_desat"] * 2 + r["flatcols"] + r["flatrows"]))
    print("\ntop 40 UI-chrome candidates (id, dark_desat, flatcols, flatrows, L_dark, R_dark, delta_min):")
    for r in ranked[:40]:
        print(f'  {r["id"]:4d}  {r["dark_desat"]:.3f}  {r["flatcols"]:.3f}  {r["flatrows"]:.3f}  '
              f'{r["L_dark"]:.3f}  {r["R_dark"]:.3f}  {r["delta_min"]:.1f}')


if __name__ == "__main__":
    main()
