#!/usr/bin/env python3
"""player_lock STRUCTURE reader — separates hard-edged mesh from smooth wash.

Written for the SB1-WW3C-STILL-REGISTER cell (2026-08-14), where the WW-3B
flank-median instrument (br2w_rows.py) FAILS: the arena still under `player_lock`
carries a strong left-right smoke/shadow luminance gradient, so a per-row median
taken over flanking windows classifies smooth shadow as subject. Demonstrated on
that still: the flank rule reported a 26-column DARK run at y505-513 / x961-986
where this instrument reads G_max 4.72 — i.e. perfectly smooth.

Discriminator: local gradient magnitude of Rec.709 luma. A rendered mesh carries
silhouette edges and surface texture (G p50 10-16, max 80-93 on the SB1 arena
still); an FX smoke bed, a prop's cast shadow and a bloom interior are SMOOTH
(G max 4.7) REGARDLESS of their absolute luminance. That is the whole point: the
discriminator does not care how dark or bright the wash is.

Convention inherited from gd-parity (2026-07-31): the instrument BRACKETS the
read. The number of record is the adjudicated box. Calibrate first (`cal` mode),
print the map second (`scan` mode), adjudicate against printed evidence third.

Edge rule used by the SB1 cell: an edge row is the first/last row carrying a
contiguous run of >= RUN columns at G >= T. Both are arguments; both belong in
the receipt beside any number they produced.

  calibrate:  pl_struct.py cal  --src S --box x0 x1 y0 y1 --label "player body"
  scan:       pl_struct.py scan --src S --x0 .. --x1 .. --y0 .. --y1 .. -T 15 --run 3
"""
import argparse

import numpy as np
from PIL import Image


def load(src):
    a = np.asarray(Image.open(src).convert("RGB"), dtype=np.float64)
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    gy, gx = np.gradient(L)
    return a, L, np.hypot(gx, gy)


def runs(mask, x0, run):
    out, cur = [], 0
    for i, v in enumerate(mask):
        if v:
            cur += 1
        else:
            if cur >= run:
                out.append((x0 + i - cur, x0 + i - 1, cur))
            cur = 0
    if cur >= run:
        out.append((x0 + len(mask) - cur, x0 + len(mask) - 1, cur))
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["cal", "scan"])
    p.add_argument("--src", required=True)
    p.add_argument("--box", type=int, nargs=4, metavar=("X0", "X1", "Y0", "Y1"))
    p.add_argument("--label", default="")
    p.add_argument("--x0", type=int, default=0)
    p.add_argument("--x1", type=int, default=0)
    p.add_argument("--y0", type=int, default=0)
    p.add_argument("--y1", type=int, default=0)
    p.add_argument("-T", "--threshold", type=float, default=15.0)
    p.add_argument("--run", type=int, default=3)
    a = p.parse_args()

    _, L, G = load(a.src)
    H, W = L.shape

    if a.mode == "cal":
        x0, x1, y0, y1 = a.box
        g = G[y0:y1 + 1, x0:x1 + 1]
        print("%-30s x%4d-%-4d y%4d-%-4d  G: p50 %6.2f p90 %6.2f p99 %6.2f max %6.2f"
              % (a.label, x0, x1, y0, y1, np.percentile(g, 50), np.percentile(g, 90),
                 np.percentile(g, 99), g.max()))
        return

    print("src %s  %dx%d" % (a.src, W, H))
    print("read x %d-%d  y %d-%d   rule: contiguous run >= %d columns at G >= %.1f"
          % (a.x0, a.x1, a.y0, a.y1, a.run, a.threshold))
    print("%5s | %-56s | %4s %6s %6s" % ("y", "qualifying runs  x0-x1(n)", "nG", "Lmin", "Lmax"))
    first = last = None
    for y in range(a.y0, a.y1 + 1):
        m = G[y, a.x0:a.x1 + 1] >= a.threshold
        sp = runs(m, a.x0, a.run)
        if sp:
            first = y if first is None else first
            last = y
        print("%5d | %-56s | %4d %6.0f %6.0f"
              % (y, " ".join("%d-%d(%d)" % s for s in sp) or "-", int(m.sum()),
                 L[y, a.x0:a.x1 + 1].min(), L[y, a.x0:a.x1 + 1].max()))
    if first is None:
        print("\nNO qualifying row in the read window — a NEGATIVE result, not an absent one.")
        return
    print("\nfirst qualifying row %d   last %d   h_px %d   h_frac %.4f%% of %d"
          % (first, last, last - first, 100.0 * (last - first) / H, H))


if __name__ == "__main__":
    main()
