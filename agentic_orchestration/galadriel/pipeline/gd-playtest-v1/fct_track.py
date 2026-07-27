#!/usr/bin/env python3
"""Track FCT instances across 60 fps frames and emit one record per DAMAGE
INSTANCE (not per frame).

F-3 restated: an FCT number lives ~0.4-0.6 s and moves. At 60 fps that is
25-35 frames of the SAME damage instance. Counting per-frame blobs would
inflate the hit count ~30x. Instances are therefore linked frame-to-frame by
centroid proximity and only the peak-size observation of each track is kept
for reading.

Per track we emit every observation's glyph bitmaps at the largest scale seen,
so the OCR stage can read once per instance rather than once per frame.
"""
import argparse
import json
import pickle
import subprocess
import sys

import numpy as np

from fct_detect import WORLD, fct_mask, components, group_glyphs

W, H = 1920, 1080
LINK_DX = 26      # px: an instance drifts slowly sideways
LINK_DY_UP = 26   # px: it drifts UP; allow a little down for spawn jitter
LINK_DY_DN = 10


def stream(video, ss, t, fps):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-hwaccel", "videotoolbox", "-ss", str(ss), "-i", video, "-t", str(t),
           "-vf", f"fps={fps}", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    n = W * H * 3
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 2)
    i = 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield i, np.frombuffer(b, dtype=np.uint8).reshape(H, W, 3)
        i += 1
    p.stdout.close()
    p.wait()


def detect(frame):
    m = fct_mask(frame)
    comps = [c for c in components(m, 8)
             if 5 <= (c["y1"] - c["y0"] + 1) <= 26
             and 2 <= (c["x1"] - c["x0"] + 1) <= 22]
    out = []
    for g in group_glyphs(comps):
        if len(g["parts"]) < 1:
            continue
        h = g["y1"] - g["y0"] + 1
        w = g["x1"] - g["x0"] + 1
        if h < 6 or w < 4:
            continue
        crop = m[g["y0"]:g["y1"] + 1, g["x0"]:g["x1"] + 1]
        out.append(dict(x0=g["x0"], x1=g["x1"], y0=g["y0"], y1=g["y1"],
                        k=len(g["parts"]), h=h, w=w,
                        cx=(g["x0"] + g["x1"]) / 2, cy=(g["y0"] + g["y1"]) / 2,
                        bmp=crop.copy(),
                        parts=[(p["x0"], p["x1"], p["y0"], p["y1"]) for p in g["parts"]]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--ss", type=float, required=True)
    ap.add_argument("--t", type=float, required=True)
    ap.add_argument("--fps", type=float, default=60.0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    tracks = []      # active
    done = []
    for i, frame in stream(args.video, args.ss, args.t, args.fps):
        pts = args.ss + i / args.fps
        dets = detect(frame)
        used = set()
        for tr in tracks:
            best, bd = None, 1e9
            for j, d in enumerate(dets):
                if j in used:
                    continue
                dx = abs(d["cx"] - tr["cx"])
                dy = tr["cy"] - d["cy"]        # positive = moved up
                if dx <= LINK_DX and -LINK_DN_OK(tr) <= dy <= LINK_DY_UP:
                    sc = dx + abs(dy)
                    if sc < bd:
                        best, bd = j, sc
            if best is None:
                tr["miss"] += 1
            else:
                d = dets[best]
                used.add(best)
                tr["miss"] = 0
                tr["cx"], tr["cy"] = d["cx"], d["cy"]
                tr["n"] += 1
                tr["last_pts"] = pts
                if d["h"] * d["w"] > tr["best"]["h"] * tr["best"]["w"]:
                    tr["best"] = d
        for j, d in enumerate(dets):
            if j not in used:
                tracks.append(dict(cx=d["cx"], cy=d["cy"], n=1, miss=0,
                                   first_pts=pts, last_pts=pts, best=d,
                                   x_spawn=d["x0"], y_spawn=d["y0"]))
        keep = []
        for tr in tracks:
            (keep if tr["miss"] <= 3 else done).append(tr)
        tracks = keep
        if i % 600 == 0:
            print(f"  {pts:.1f}s tracks={len(tracks)} done={len(done)}",
                  file=sys.stderr, flush=True)
    done += tracks

    out = [t for t in done if t["n"] >= 3]
    with open(args.out, "wb") as fh:
        pickle.dump(out, fh)
    print(f"{len(done)} raw tracks, {len(out)} kept (n>=3) -> {args.out}")
    print(json.dumps(dict(n_tracks=len(out),
                          window=[args.ss, args.ss + args.t])))


def LINK_DN_OK(tr):
    return LINK_DY_DN


if __name__ == "__main__":
    main()
