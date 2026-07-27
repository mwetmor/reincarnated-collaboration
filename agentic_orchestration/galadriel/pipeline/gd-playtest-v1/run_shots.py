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
from PIL import Image

from panel_ocr import PanelReader

VIDEO_START_EPOCH = 1785096216.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--epoch", type=float, default=VIDEO_START_EPOCH)
    args = ap.parse_args()

    reader = PanelReader(args.model)
    files = glob.glob(os.path.join(args.dir, "Screenshot (*).png"))

    def num(p):
        m = re.search(r"\((\d+)\)", os.path.basename(p))
        return int(m.group(1)) if m else -1

    files.sort(key=num)
    print(f"{len(files)} screenshots")

    with open(args.out, "w") as fh:
        for i, p in enumerate(files):
            mt = os.path.getmtime(p)
            rgb = np.asarray(Image.open(p).convert("RGB")).astype(np.int16)
            rec = reader.read(rgb)
            rec["shot"] = num(p)
            rec["mtime"] = mt
            rec["pts_s"] = round(mt - args.epoch, 3)
            rec["i"] = i
            fh.write(json.dumps(rec) + "\n")
            if i % 50 == 0:
                print(f"  {i}/{len(files)} shot={rec['shot']} "
                      f"pts={rec['pts_s']:.1f} play_time={rec.get('play_time')} "
                      f"kills={rec.get('kills')}", flush=True)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
