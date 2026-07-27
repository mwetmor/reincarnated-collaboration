#!/usr/bin/env python3
"""
T-A, screenshot arm: read the PlayStats panel from all 313 native PNGs.

These are the SAME ledger as the video tier but on the better instrument --
native 1920x1080 PNG, no h264 quantisation. They are sparse (313 samples over
6816 s, ~22 s apart) but they are the reference against which the video arm's
error rate is measured, and per gandalf's D-2 ruling they are PREFERRED
wherever a screenshot covers the same play_time as a video sample.

Timeline placement is arithmetic, per the verification note §2:
    pts_s = mtime(shot) - video_start_epoch,  video_start_epoch = 1785096216.5
No sync pass is required and none is performed.
"""

import argparse
import glob
import json
import os
import re

import numpy as np
from PIL import Image, ImageDraw

from panel_ocr import PanelReader

VIDEO_START_EPOCH = 1785096216.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--epoch", type=float, default=VIDEO_START_EPOCH)
    ap.add_argument("--contact-sheet", default=None,
                    help="also emit tiled contact sheets of every shot. This is "
                         "how the 313-shot set becomes navigable: UI screens "
                         "(character sheet, skill tree, devotion/constellation) "
                         "are visually distinct from gameplay at thumbnail size, "
                         "so a screen can be LOCATED here and then READ at native "
                         "resolution. Nothing is ever read off the sheet itself -- "
                         "it is an index, not an instrument (D-1).")
    ap.add_argument("--sheet-cols", type=int, default=8)
    ap.add_argument("--sheet-rows", type=int, default=5)
    ap.add_argument("--sheet-tile-w", type=int, default=240)
    args = ap.parse_args()

    reader = PanelReader(args.model)
    files = glob.glob(os.path.join(args.dir, "Screenshot (*).png"))

    def num(p):
        m = re.search(r"\((\d+)\)", os.path.basename(p))
        return int(m.group(1)) if m else -1

    files.sort(key=num)
    print(f"{len(files)} screenshots")

    tw = args.sheet_tile_w
    th = tw * 9 // 16
    per_sheet = args.sheet_cols * args.sheet_rows
    sheet = None
    sheet_idx = 0
    if args.contact_sheet:
        os.makedirs(args.contact_sheet, exist_ok=True)

    def flush_sheet():
        nonlocal sheet, sheet_idx
        if sheet is not None:
            out = os.path.join(args.contact_sheet, f"sheet_{sheet_idx:02d}.png")
            sheet.save(out)
            print(f"  contact sheet -> {out}", flush=True)
            sheet_idx += 1
            sheet = None

    with open(args.out, "w") as fh:
        for i, p in enumerate(files):
            mt = os.path.getmtime(p)
            img = Image.open(p).convert("RGB")
            rgb = np.asarray(img).astype(np.int16)
            rec = reader.read(rgb)
            rec["shot"] = num(p)
            rec["mtime"] = mt
            rec["pts_s"] = round(mt - args.epoch, 3)
            rec["i"] = i
            fh.write(json.dumps(rec) + "\n")

            if args.contact_sheet:
                if i % per_sheet == 0:
                    flush_sheet()
                    sheet = Image.new("RGB", (tw * args.sheet_cols,
                                              (th + 14) * args.sheet_rows), (0, 0, 0))
                k = i % per_sheet
                sheet.paste(img.resize((tw, th), Image.LANCZOS),
                            ((k % args.sheet_cols) * tw,
                             (k // args.sheet_cols) * (th + 14)))
                ImageDraw.Draw(sheet).text(
                    ((k % args.sheet_cols) * tw + 3,
                     (k // args.sheet_cols) * (th + 14) + th + 1),
                    f"{rec['shot']}  pt={rec.get('play_time')}", fill=(255, 230, 60))

            if i % 50 == 0:
                print(f"  {i}/{len(files)} shot={rec['shot']} "
                      f"pts={rec['pts_s']:.1f} play_time={rec.get('play_time')} "
                      f"kills={rec.get('kills')}", flush=True)
    flush_sheet()
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
