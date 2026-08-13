#!/usr/bin/env python3
"""KC2-PM3 Lap C -- video instrument for the EoR-Warlord reference run. READ-ONLY on the capture.

SUBSTRATE
  /Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/
      eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4
  1920x1080, h264, 60/1 fps, duration 1034.100 s.

INSTRUMENT SCHEMA (declared; every downstream number asserts this basis)
  IS-V1  Frame basis. A single decode pass `-ss 400 -t 540 -vf fps=1` yields 540 JPEGs,
         s_0001..s_0540, with s_NNNN sampling video second (399 + NNNN). Sampling is
         1 Hz; NOTHING shorter-lived than 1 s is observable by this instrument, and every
         timestamp it emits carries +/- 1 s quantisation. Wave banners in Grim Dawn's
         Crucible persist ~2-3 s, so 1 Hz is above Nyquist for them but NOT for the
         sub-second transitions; a banner's FIRST observed second is an upper bound on
         its true onset (true onset in [t-1, t]).
  IS-V2  Wall-clock anchor. The game HUD prints a real wall clock at (16,8)-(120,26).
         At video t=470 it reads 9:45:15 PM; the capture filename stamps 21:37:25.
         21:37:25 + 470 s = 21:45:15 EXACTLY -> video time is 1x real time with zero
         drift at that anchor, and video_t = wallclock - 21:37:25.
  IS-V3  Region boxes are stated in FULL-RES pixel coordinates (x, y, w, h) on the
         1920x1080 frame, measured by crop-and-look, not assumed:
             TRIBUTE  (1348,  99,  70, 26)   survival-pane tribute counter
             TIMER    (1460,  99, 110, 26)   survival-pane wave timer (mm:ss)
             SCORE    (1200,  40, 240, 40)   survival-pane score
             BANNER   ( 560, 150, 800, 130)  centre-screen wave-announce band
             DIALOG   ( 460, 380, 780, 460)  NPC/defense-site dialog band
             HPGLOBE  ( 100, 990, 200,  40)  player life text
  IS-V4  Change detection is mean-absolute-difference on the 8-bit greyscale crop
         between consecutive 1 Hz frames. A "change point" is a frame whose MAD exceeds
         the stated threshold. MAD is a DETECTOR, never a reader: every quantity this lap
         reports as measured was read by eye off the full-res crop at the detected frame.
         Thresholds are reported with the frame counts they select (NOTE-9 basis).

NO OCR is used anywhere. Digits are read by a human-equivalent eye pass on upscaled crops.
"""
import sys
import pathlib
import numpy as np
from PIL import Image

SCRATCH = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                       "legolas/scratch/2026-08-12-kc2-pm3-lapc")
FPS1 = SCRATCH / "fps1"
T0 = 399  # s_NNNN  ->  video second T0 + NNNN

BOX = {
    "tribute": (1348, 99, 70, 26),
    "timer":   (1460, 99, 110, 26),
    "score":   (1200, 40, 240, 40),
    "banner":  (600, 125, 760, 70),
    "dialog":  (460, 380, 780, 460),
    "hpglobe": (100, 990, 200, 40),
}


def tsec(idx):
    return T0 + idx


def load(idx):
    p = FPS1 / f"s_{idx:04d}.jpg"
    return Image.open(p) if p.exists() else None


def crop_gray(im, name):
    x, y, w, h = BOX[name]
    return np.asarray(im.crop((x, y, x + w, y + h)).convert("L"), dtype=np.float32)


def mad_series(name, lo, hi):
    """[(video_t, MAD_vs_previous_frame)] over sample indices lo..hi inclusive."""
    prev = None
    out = []
    for i in range(lo, hi + 1):
        im = load(i)
        if im is None:
            continue
        c = crop_gray(im, name)
        if prev is not None and prev.shape == c.shape:
            out.append((tsec(i), float(np.abs(c - prev).mean())))
        prev = c
    return out


def ink_series(name, lo, hi, thresh=170):
    """[(video_t, bright_pixel_fraction)] -- text-presence proxy for the banner band."""
    out = []
    for i in range(lo, hi + 1):
        im = load(i)
        if im is None:
            continue
        c = crop_gray(im, name)
        out.append((tsec(i), float((c > thresh).mean())))
    return out


def dump(name, lo, hi, outdir, idxs, scale=6):
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    x, y, w, h = BOX[name]
    for i in idxs:
        im = load(i)
        if im is None:
            continue
        c = im.crop((x, y, x + w, y + h)).resize((w * scale, h * scale), Image.LANCZOS)
        c.save(outdir / f"{name}_t{tsec(i):04d}.png")


def sheet(name, idxs, out, cols=1, scale=5, label=True):
    """Vertical/grid contact sheet of one region across the given sample indices."""
    from PIL import ImageDraw
    x, y, w, h = BOX[name]
    W, H = w * scale, h * scale
    lab = 0
    rows = (len(idxs) + cols - 1) // cols
    sheet_im = Image.new("RGB", (cols * (W + 90), rows * (H + 4)), (20, 20, 20))
    d = ImageDraw.Draw(sheet_im)
    for n, i in enumerate(idxs):
        im = load(i)
        if im is None:
            continue
        c = im.crop((x, y, x + w, y + h)).resize((W, H), Image.LANCZOS)
        cx = (n % cols) * (W + 90)
        cy = (n // cols) * (H + 4)
        sheet_im.paste(c, (cx + 88, cy))
        if label:
            d.text((cx + 4, cy + H // 2 - 6), f"t={tsec(i)}", fill=(255, 220, 120))
    sheet_im.save(out)
    print(out, sheet_im.size, len(idxs), "tiles")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "mad"
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    if cmd == "mad":
        name = sys.argv[4]
        thr = float(sys.argv[5]) if len(sys.argv) > 5 else 2.0
        s = mad_series(name, lo, hi)
        hits = [t for t, v in s if v > thr]
        print(f"# region={name} basis={len(s)} consecutive-pairs  thr={thr}  hits={len(hits)}")
        for t, v in s:
            if v > thr:
                print(f"{t:5d}  {v:8.3f}")
    elif cmd == "ink":
        name = sys.argv[4]
        for t, v in ink_series(name, lo, hi):
            print(f"{t:5d}  {v:.5f}")
