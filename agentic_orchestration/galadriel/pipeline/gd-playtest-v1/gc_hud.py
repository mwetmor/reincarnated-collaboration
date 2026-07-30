#!/usr/bin/env python3
"""GAL-CAM: what the HUD covers, and where the player sits, by temporal stability.

WHY THIS MATTERS TO A CAMERA CELL
---------------------------------
The dispatch asks for the DECISION SURFACE -- what was within X metres of Matt in
every direction AS HE ACTUALLY EXPERIENCED IT. The frustum is only half of that.
Ground that is rendered underneath an opaque skill bar was not part of anyone's
decision. So the visible-ground box has to be cut twice: once by the frame edge,
once by the HUD.

METHOD
------
Over a window in which the player RUNS, world pixels change every frame and
screen-locked pixels do not. Per-pixel temporal MAD over such a window is
therefore an occlusion map: near-zero MAD = opaque screen-locked chrome.

The same map locates the player, because the player is also screen-locked -- it
is the low-MAD island in the middle of the play area rather than at the edges.
"""
import argparse
import json
import subprocess

import numpy as np
from PIL import Image, ImageDraw

VIDEO = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
W, H = 1920, 1080


def stream(ss, dur, gray=True):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
           "-ss", str(ss), "-i", VIDEO, "-t", str(dur),
           "-pix_fmt", "gray" if gray else "rgb24", "-f", "rawvideo", "-"]
    n = W * H * (1 if gray else 3)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 8)
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        a = np.frombuffer(b, dtype=np.uint8)
        yield a.reshape(H, W) if gray else a.reshape(H, W, 3)
    p.stdout.close()
    p.wait()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--starts", type=float, nargs="+", required=True)
    ap.add_argument("--dur", type=float, default=8.0)
    ap.add_argument("--step", type=int, default=3)
    ap.add_argument("--madthr", type=float, default=2.0)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    mads = []
    meds = []
    for ss in args.starts:
        fr = [g for i, g in enumerate(stream(ss, args.dur)) if i % args.step == 0]
        if len(fr) < 20:
            continue
        S = np.stack(fr).astype(np.float32)
        med = np.median(S, axis=0)
        mad = np.median(np.abs(S - med), axis=0)
        mads.append(mad)
        meds.append(med)
        print(f"ss={ss} frames={len(fr)} mad median={np.median(mad):.2f}")
    if not mads:
        print("no usable windows")
        return
    # a pixel is CHROME only if it is static in EVERY sampled window
    static = np.ones((H, W), bool)
    for m in mads:
        static &= (m < args.madthr)
    frac = static.mean(axis=1)

    print("\nrow-wise static fraction (chrome profile):")
    for y in range(0, H, 20):
        bar = "#" * int(frac[y] * 60)
        print(f"  y={y:4d} {frac[y]:.3f} {bar}")

    # top and bottom chrome bands: rows where >45% of the width is static
    heavy = frac > 0.45
    ytop = 0
    while ytop < H and heavy[ytop]:
        ytop += 1
    ybot = H - 1
    while ybot > 0 and heavy[ybot]:
        ybot -= 1
    # per-column free extent within the play area
    colfree = []
    for x in range(0, W, 10):
        col = static[:, x]
        lo = 0
        while lo < H and col[lo]:
            lo += 1
        hi = H - 1
        while hi > 0 and col[hi]:
            hi -= 1
        colfree.append((x, int(lo), int(hi)))

    # player: the static island inside the play area, away from the edges
    isl = static.copy()
    isl[:, :330] = False; isl[:, 1450:] = False
    isl[:200] = False; isl[900:] = False
    ys, xs = np.nonzero(isl)
    rec = dict(chrome_top_rows=int(ytop), chrome_bottom_row=int(ybot))
    if len(xs):
        # densest cluster
        hx, ex = np.histogram(xs, bins=np.arange(330, 1460, 20))
        cx = ex[np.argmax(hx)] + 10
        sel = np.abs(xs - cx) < 60
        rec.update(player_x=float(np.median(xs[sel])),
                   player_y_top=float(np.percentile(ys[sel], 2)),
                   player_y_bot=float(np.percentile(ys[sel], 98)),
                   player_npx=int(sel.sum()))
    print(f"\nchrome: solid top rows 0-{ytop}, solid bottom rows {ybot}-{H-1}")
    print("player island:", {k: v for k, v in rec.items() if k.startswith("player")})

    vis = (np.dstack([meds[0]] * 3)).astype(np.uint8)
    vis[static] = (vis[static] * 0.35 + np.array([0, 90, 0])).astype(np.uint8)
    im = Image.fromarray(vis)
    d = ImageDraw.Draw(im)
    for y in range(0, H, 100):
        d.line([0, y, W, y], fill=(60, 60, 60)); d.text((4, y + 2), str(y), fill=(200, 200, 200))
    for x in range(0, W, 160):
        d.line([x, 0, x, H], fill=(60, 60, 60)); d.text((x + 3, 4), str(x), fill=(200, 200, 200))
    im.save(f"{args.outdir}/chrome-map.jpg", quality=90)
    json.dump(dict(rec, colfree=colfree, madthr=args.madthr,
                   starts=args.starts, dur=args.dur),
              open(f"{args.outdir}/hud.json", "w"), indent=1)
    print("wrote", f"{args.outdir}/chrome-map.jpg")


if __name__ == "__main__":
    main()
