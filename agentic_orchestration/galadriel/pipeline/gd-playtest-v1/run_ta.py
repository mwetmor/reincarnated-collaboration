#!/usr/bin/env python3
"""
T-A ledger pass: stream the run at a fixed sample rate and OCR the PlayStats
panel on every sample.

Frames are piped from ffmpeg as raw RGB at NATIVE resolution, cropped to the
panel column only. Nothing is downscaled at any point (protocol §4.4 method
law, and D-1: a downscale-then-upscale path is exactly what produced gandalf's
"legible and wrong" first read).

Emits one JSONL record per sample with BOTH clocks:
  pts_s      video offset in seconds (camera clock)
  play_time  panel game-state clock in seconds (join key -- §3 ruling)
plus every field and its per-field glyph confidence.
"""

import argparse
import json
import subprocess
import sys

import numpy as np

from panel_ocr import PanelReader

CROP_X, CROP_W = 1320, 600
CROP_Y, CROP_H = 0, 540


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--fps", type=float, default=2.0)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ss", type=float, default=None)
    ap.add_argument("--t", type=float, default=None)
    args = ap.parse_args()

    reader = PanelReader(args.model)

    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-hwaccel", "videotoolbox"]
    if args.ss is not None:
        cmd += ["-ss", str(args.ss)]
    cmd += ["-i", args.video]
    if args.t is not None:
        cmd += ["-t", str(args.t)]
    cmd += ["-vf", f"fps={args.fps},crop={CROP_W}:{CROP_H}:{CROP_X}:{CROP_Y}",
            "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]

    nbytes = CROP_W * CROP_H * 3
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=nbytes * 4)

    t0 = args.ss or 0.0
    canvas = np.zeros((CROP_H, 1920, 3), dtype=np.int16)
    n = 0
    with open(args.out, "w") as fh:
        while True:
            buf = proc.stdout.read(nbytes)
            if len(buf) < nbytes:
                break
            frame = np.frombuffer(buf, dtype=np.uint8).reshape(CROP_H, CROP_W, 3)
            canvas[:, CROP_X:CROP_X + CROP_W, :] = frame
            rec = reader.read(canvas)
            rec["pts_s"] = round(t0 + n / args.fps, 3)
            rec["i"] = n
            fh.write(json.dumps(rec) + "\n")
            n += 1
            if n % 500 == 0:
                print(f"  {n} samples, pts={rec['pts_s']:.0f}s, "
                      f"play_time={rec.get('play_time')}, kills={rec.get('kills')}",
                      file=sys.stderr, flush=True)
    proc.stdout.close()
    proc.wait()
    print(f"wrote {args.out}: {n} samples")


if __name__ == "__main__":
    main()
