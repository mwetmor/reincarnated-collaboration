#!/usr/bin/env python3
"""C-9 image bake-off, JOB 2: the helmet + bracers EDIT on NB-1_b (the NB-G1 brief).

    python3 05_score_j2.py

The edit is asked for two things at once: ADD a helmet and two bracers, and change NOTHING
else -- "the SAME pose, scale, ground lines and positions". So three numbers:

  OUTSIDE-GEAR IoU   Body silhouette against NB-1_b's, in the sheet's own frame (no
                     alignment -- pose and scale kept is the requirement, so a drift is a
                     miss), over everything OUTSIDE the gear zones. The zones are placed from
                     the BASE figure, per view, so an edit cannot move its own exemption:
                       head zone     from 10% of the figure's height ABOVE its top to 19%
                                     below it (the helmet sits on and above the head)
                       forearm band  36% to 60% of the height (elbow to hand in this A-pose)
  LEG SHIFT          The nb_d2/02_gear_register.py question -- did the uncovered body MOVE --
                     asked on the same region, the legs and boots (0.62-0.97 of each cell):
                     the integer shift within +-8 px that best aligns the edit's leg
                     silhouette to the base's.
  PLACEMENT          Where the paint changed: pixels inside either figure whose colour moved
                     more than 30/255 (sRGB distance / sqrt 3). PRECISION is the share of them
                     inside the gear zones; HEAD and ARMS are the changed share of each zone,
                     so a missing helmet or missing bracers shows as a low number.

Every edit is resized to the base's 1024x1536 frame first. Nano Banana returns 832x1248 (the
same 2:3) and Pro 1696x2528, which is 0.6% narrower than 2:3 -- under 2 px at a quarter's
centre, stated rather than corrected, since keeping the frame is part of what is scored.
"""
import json
import os
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
C9 = HERE.parent
os.environ["FAL_LEDGER"] = str(HERE / "fal_spend_R-C9-79.json")
os.environ["FAL_BUDGET"] = "5.00"
sys.path.insert(0, str(C9 / "t10_barrow"))
import fal_ledger  # noqa: E402

BASE_RGB = C9 / "artifacts/NB-1/NB-1_b.png"
BASE_MATTE = C9 / "nb_t8/nb1_b_rgba.png"
EDITS = {"astra_a": C9 / "artifacts/NB-G1/NB-G1_a.png", "astra_b": C9 / "artifacts/NB-G1/NB-G1_b.png",
         "nb_a": HERE / "out/J2_nb_a.png", "nb_b": HERE / "out/J2_nb_b.png",
         "nbp_a": HERE / "out/J2_nbp_a.png", "nbp_b": HERE / "out/J2_nbp_b.png"}
QUAD = [(0, 0), (1, 0), (0, 1), (1, 1)]      # front, right, back, left


def matte(src, dst):
    if dst.exists():
        return dst
    import fal_client
    fal_ledger.check("fal-ai/birefnet/v2")
    with fal_ledger.timed() as tm:
        url = fal_client.upload_file(str(src))
        r = fal_client.subscribe("fal-ai/birefnet/v2", arguments={
            "image_url": url, "model": "General Use (Heavy)", "operating_resolution": "2048x2048",
            "output_format": "png", "refine_foreground": True})
    subprocess.run(["curl", "-s", "-L", "-o", str(dst), r["image"]["url"]], check=True)
    tot = fal_ledger.record("fal-ai/birefnet/v2", "J2 matte %s" % src.name, tm.s)
    print("   matte %s  %.1f s  fal running $%.4f" % (src.name, tm.s, tot))
    return dst


def figs(alpha):
    """Largest component per quarter, in full-sheet coordinates."""
    H, W = alpha.shape
    out = np.zeros_like(alpha)
    for c, r in QUAD:
        q = alpha[r * H // 2:(r + 1) * H // 2, c * W // 2:(c + 1) * W // 2]
        lab, n = ndimage.label(q)
        if n:
            out[r * H // 2:(r + 1) * H // 2, c * W // 2:(c + 1) * W // 2] = \
                lab == 1 + int(np.argmax(ndimage.sum(q, lab, range(1, n + 1))))
    return out


def zones(base):
    H, W = base.shape
    head = np.zeros_like(base)
    arms = np.zeros_like(base)
    legs = np.zeros_like(base)
    for c, r in QUAD:
        y0, x0 = r * H // 2, c * W // 2
        q = base[y0:y0 + H // 2, x0:x0 + W // 2]
        ys = np.nonzero(q.any(1))[0]
        top, bot = ys.min(), ys.max()
        h = bot - top + 1
        head[y0 + max(0, int(top - 0.10 * h)):y0 + int(top + 0.19 * h), x0:x0 + W // 2] = True
        arms[y0 + int(top + 0.36 * h):y0 + int(top + 0.60 * h), x0:x0 + W // 2] = True
        legs[y0 + int(0.62 * H // 2):y0 + int(0.97 * H // 2), x0:x0 + W // 2] = True
    return head, arms, legs


def best_shift(a, b, R=8):
    best = (-1, 0, 0)
    for dy in range(-R, R + 1):
        for dx in range(-R, R + 1):
            s = np.roll(np.roll(b, dy, 0), dx, 1)
            u = (a | s).sum()
            v = (a & s).sum() / u if u else 0
            if v > best[0]:
                best = (v, dy, dx)
    return best


def main() -> None:
    (HERE / "mattes").mkdir(exist_ok=True)
    base_a = np.asarray(Image.open(BASE_MATTE).convert("RGBA"))[..., 3] > 128
    base = figs(base_a)
    H, W = base.shape
    base_rgb = np.asarray(Image.open(BASE_RGB).convert("RGB")).astype(np.float32)
    head, arms, legs = zones(base)
    gear = head | arms
    rep = {}
    for name, src in EDITS.items():
        mp = matte(src, HERE / "mattes" / ("J2_%s_rgba.png" % name))
        ea = np.asarray(Image.open(mp).convert("RGBA").resize((W, H), Image.BILINEAR))[..., 3] > 128
        edit = figs(ea)
        ergb = np.asarray(Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.float32)
        out = ~gear
        inter = (base & edit & out).sum()
        uni = ((base | edit) & out).sum()
        iou_out = inter / uni if uni else 0.0
        shifts = []
        for c, r in QUAD:
            sl = (slice(r * H // 2, (r + 1) * H // 2), slice(c * W // 2, (c + 1) * W // 2))
            v, dy, dx = best_shift(base[sl] & legs[sl], edit[sl] & legs[sl])
            shifts.append([dy, dx])
        mag = [float(np.hypot(*s)) for s in shifts]
        figu = base | edit
        d = np.linalg.norm(ergb - base_rgb, axis=2) / np.sqrt(3.0)
        changed = (d > 30) & figu
        prec = (changed & gear).sum() / max(changed.sum(), 1)
        head_cov = (changed & head & figu).sum() / max((head & figu).sum(), 1)
        arms_cov = (changed & arms & figu).sum() / max((arms & figu).sum(), 1)
        # PAINT KEPT, not only outline kept: "everything else stays exactly as IMAGE 1 paints
        # it". Mean colour distance over the body both sheets share, outside the gear zones.
        # A model that holds the silhouette and repaints the man in another hand passes the
        # IoU and fails here -- which is the case the eye found on Pro b.
        keep = base & edit & out
        paint_delta = float(d[keep].mean()) if keep.any() else float("nan")
        rep[name] = {"size": list(Image.open(src).size), "iou_outside_gear": round(float(iou_out), 4),
                     "paint_delta_outside_gear": round(paint_delta, 2),
                     "leg_shift_px": shifts, "leg_shift_max_px": round(max(mag), 2),
                     "changed_share_in_gear_zones": round(float(prec), 3),
                     "head_zone_changed": round(float(head_cov), 3),
                     "forearm_band_changed": round(float(arms_cov), 3),
                     "changed_px": int(changed.sum())}
        r = rep[name]
        print("%-8s IoU outside gear %.4f | paint delta outside %.1f | leg shift max %.1f px %s | change in gear zones %.2f, "
              "head %.2f, arms %.2f | %s"
              % (name, r["iou_outside_gear"], r["paint_delta_outside_gear"], r["leg_shift_max_px"], shifts,
                 r["changed_share_in_gear_zones"], r["head_zone_changed"],
                 r["forearm_band_changed"], r["size"]))
    np.save(HERE / "mattes" / "J2_gear_zone.npy", gear)
    (HERE / "score_j2.json").write_text(json.dumps(rep, indent=1) + "\n")


if __name__ == "__main__":
    main()
