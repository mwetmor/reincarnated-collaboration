#!/usr/bin/env python3
"""RECON pass on the TRUE referent (R-29) -- run BEFORE any anchor number.

Answers four questions the R-27 instrument silently assumed on the old
(wrong) referent, and which this referent may answer differently:

  Q1  Is the scene/effect hue histogram BIMODAL?  (R-27's hue-sector
      segmentation is only well-posed if it is.  The D3 clip was teal-scene /
      fire-effect.  This one is a warm sandstone dungeon with a red-orange
      effect -- the sector test may be vacuous here.)
  Q2  Where is the HUD?  (D4 draws a red health globe, a gold resource orb, a
      skill bar, party frames, a minimap and a boss health bar.  Several of
      those are large, saturated and WARM -- i.e. exactly what a warm-hue mask
      selects.  Fixed-position => derivable from temporal statistics.)
  Q3  Does the camera translate?  (Determines whether a temporal-median
      background is available as an alternative segmentation.)
  Q4  What does the warm mask actually land on?  (Pictures, not statistics.)

Nothing here produces an anchor constant.  It produces the facts the
segmentation choice has to be made from.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vfx_lap2_battery import luma, sat_val  # noqa: E402

# --- the three fixed-position black masks the conductor applied -------------
# (x, y, w, h) in 1920x1080 image space, per provenance-card.md § 1
BLACK_MASKS = [
    ("facecam", 0, 760, 400, 320),
    ("branding", 0, 0, 240, 160),
    ("watermark", 1540, 900, 380, 180),
]


def valid_map(h, w, pad=4):
    """Pixels that are SCENE.  The three black rectangles are fill, not scene,
    and must not enter any pixel statistic (they would drag P20 to zero and
    make every ratio meaningless).  Padded outward because the mask edges
    carry codec ringing."""
    V = np.ones((h, w), bool)
    for _, x, y, ww, hh in BLACK_MASKS:
        V[max(0, y - pad):min(h, y + hh + pad), max(0, x - pad):min(w, x + ww + pad)] = False
    return V


def hue_sat(f):
    a = f.astype(np.float32) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(2), a.min(2)
    c = mx - mn
    hh = np.zeros_like(mx)
    nz = c > 1e-6
    i = (mx == r) & nz
    hh[i] = ((g - b)[i] / c[i]) % 6
    i = (mx == g) & nz
    hh[i] = ((b - r)[i] / c[i]) + 2
    i = (mx == b) & nz
    hh[i] = ((r - g)[i] / c[i]) + 4
    s = np.where(mx > 1e-6, c / np.maximum(mx, 1e-6), 0.0)
    return hh * 60.0, s


def frames(path, w, h, stride=1, limit=None):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    i = 0
    out = 0
    while True:
        buf = p.stdout.read(n)
        if not buf or len(buf) < n:
            break
        if i % stride == 0:
            yield i, np.frombuffer(buf, np.uint8).reshape(h, w, 3)
            out += 1
            if limit and out >= limit:
                break
        i += 1
    p.stdout.close()
    p.kill()
    p.wait()


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,r_frame_rate,codec_name,pix_fmt,nb_frames",
         "-of", "json", path], capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return int(s["width"]), int(s["height"]), float(num) / float(den), s["codec_name"], s["pix_fmt"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--stride", type=int, default=6)
    a = ap.parse_args()

    w, h, fps, codec, pix = probe(a.clip)
    V = valid_map(h, w)
    res = {"clip": a.clip, "tag": a.tag,
           "video": {"w": w, "h": h, "fps": fps, "codec": codec, "pix_fmt": pix},
           "valid_frac": float(V.mean()),
           "black_masks": [{"name": n, "x": x, "y": y, "w": ww, "h": hh}
                           for n, x, y, ww, hh in BLACK_MASKS]}

    # ---- accumulate ------------------------------------------------------
    HB = np.zeros(72)            # L-weighted hue histogram, 5-deg bins
    HB_S = np.zeros(72)          # count of saturated pixels per hue bin
    n_frames = 0
    Lsum = None
    Lsq = None
    meanL = []
    warm_area = []
    idxs = []
    keep_small = []              # downscaled luma for camera-motion test
    black_check = []

    for i, f in frames(a.clip, w, h, stride=a.stride):
        L = luma(f)
        hh, s = hue_sat(f)
        m = V & (s > 0.15) & (L > 0.05)
        bins = np.clip((hh[m] / 5.0).astype(int), 0, 71)
        np.add.at(HB, bins, L[m])
        np.add.at(HB_S, bins, 1.0)
        if Lsum is None:
            Lsum = np.zeros((h, w), np.float64)
            Lsq = np.zeros((h, w), np.float64)
        Lsum += L
        Lsq += L.astype(np.float64) ** 2
        meanL.append(float(L[V].mean()))
        warm_area.append(int((V & ((hh < 60) | (hh >= 330)) & (s > 0.35) & (L > 0.10)).sum()))
        idxs.append(i)
        keep_small.append(L[::8, ::8].astype(np.float32))
        # verify the black masks really ARE black (the crop is asserted, not measured)
        blk = []
        for nm, x, y, ww, hh_ in BLACK_MASKS:
            blk.append(float(L[y + 8:y + hh_ - 8, x + 8:x + ww - 8].mean()))
        black_check.append(blk)
        n_frames += 1

    res["n_frames_sampled"] = n_frames
    res["black_mask_mean_luma"] = {
        BLACK_MASKS[k][0]: {"mean": float(np.mean([b[k] for b in black_check])),
                            "max": float(np.max([b[k] for b in black_check]))}
        for k in range(len(BLACK_MASKS))}

    # ---- Q1 hue histogram ------------------------------------------------
    res["hue_hist_L_weighted"] = (HB / max(HB.sum(), 1)).round(5).tolist()
    res["hue_hist_counts"] = (HB_S / max(HB_S.sum(), 1)).round(5).tolist()
    res["hue_bins_deg"] = [k * 5 for k in range(72)]
    warm_share = float(HB[np.r_[0:12, 66:72]].sum() / max(HB.sum(), 1))
    res["warm_sector_share_of_chromatic_L"] = warm_share

    # ---- Q2 static structure (HUD) --------------------------------------
    Lmean = Lsum / n_frames
    Lstd = np.sqrt(np.maximum(Lsq / n_frames - Lmean ** 2, 0))
    res["static_probe"] = {}
    for thr in (0.005, 0.010, 0.020, 0.030):
        cand = V & (Lstd < thr)
        res["static_probe"]["std_lt_%.3f" % thr] = {
            "px": int(cand.sum()), "frac": float(cand.sum() / V.sum())}
    np.save(str(Path(a.out).parent / ("Lstd_%s.npy" % a.tag)), Lstd.astype(np.float32))
    np.save(str(Path(a.out).parent / ("Lmean_%s.npy" % a.tag)), Lmean.astype(np.float32))

    # ---- Q3 camera motion ------------------------------------------------
    K = np.stack(keep_small)
    d = np.abs(np.diff(K, axis=0)).mean(axis=(1, 2))
    res["camera_probe"] = {
        "mean_abs_interframe_dL_downscaled": float(d.mean()),
        "p90": float(np.percentile(d, 90)),
        "note": "downscaled 8x; a static camera on a mostly-static dungeon would "
                "read near the codec floor; a following camera reads high",
    }
    # cross-correlation shift on the frame corner farthest from the action
    corner = K[:, 2:14, -16:]
    res["camera_probe"]["corner_std_over_time"] = float(corner.std(0).mean())

    # ---- curves ----------------------------------------------------------
    res["curves"] = {"frame": idxs, "mean_luma": np.round(meanL, 5).tolist(),
                     "warm_area_px": warm_area}

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=1))

    # ---- Q4 pictures -----------------------------------------------------
    from PIL import Image
    ev = Path(a.evidence)
    ev.mkdir(parents=True, exist_ok=True)
    Image.fromarray((np.clip(Lstd * 8, 0, 1) * 255).astype(np.uint8)).save(
        ev / ("recon-%s-Lstd.png" % a.tag))
    Image.fromarray((np.clip(Lmean, 0, 1) * 255).astype(np.uint8)).save(
        ev / ("recon-%s-Lmean.png" % a.tag))

    top = np.argsort(HB)[::-1][:8]
    print("[%s] %dx%d %.2ffps %s  n=%d  valid=%.3f" % (a.tag, w, h, fps, codec, n_frames, V.mean()))
    print("  black-mask luma:", {k: round(v["mean"], 4) for k, v in res["black_mask_mean_luma"].items()})
    print("  top hue bins (deg, L-share):", [(int(t * 5), round(HB[t] / HB.sum(), 4)) for t in top])
    print("  warm-sector share of chromatic L: %.4f" % warm_share)
    print("  static px (std<0.01): %d (%.4f of valid)" % (
        res["static_probe"]["std_lt_0.010"]["px"], res["static_probe"]["std_lt_0.010"]["frac"]))
    print("  camera interframe |dL| mean %.5f p90 %.5f  corner-std %.5f" % (
        d.mean(), np.percentile(d, 90), res["camera_probe"]["corner_std_over_time"]))
    print("  warm_area px: median %d  min %d  max %d" % (
        int(np.median(warm_area)), min(warm_area), max(warm_area)))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
