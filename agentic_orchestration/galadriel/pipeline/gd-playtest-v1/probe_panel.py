#!/usr/bin/env python3
"""Read the PlayStats panel at a list of arbitrary video offsets (single-frame
seeks). Used for bracketing events (deaths, level-ups, gear changes) without
streaming a whole window."""
import argparse
import json
import subprocess

import numpy as np

from panel_ocr import PanelReader

W, H = 1920, 1080


def grab(video, t):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-ss", str(t), "-i", video, "-frames:v", "1",
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    b = subprocess.run(cmd, capture_output=True).stdout
    if len(b) < W * H * 3:
        return None
    return np.frombuffer(b[:W * H * 3], dtype=np.uint8).reshape(H, W, 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--times", required=True, help="comma list or a:b:step")
    args = ap.parse_args()
    r = PanelReader(args.model)
    if ":" in args.times:
        a, b, s = (float(x) for x in args.times.split(":"))
        ts = list(np.arange(a, b, s))
    else:
        ts = [float(x) for x in args.times.split(",")]
    for t in ts:
        f = grab(args.video, t)
        if f is None:
            print(json.dumps(dict(pts_s=t, status="NO_FRAME")))
            continue
        rec = r.read(f.astype(np.int16))
        rec.pop("skills", None)
        rec["pts_s"] = t
        print(json.dumps({k: (float(v) if isinstance(v, np.floating) else v)
                          for k, v in rec.items()}))


if __name__ == "__main__":
    main()
