#!/usr/bin/env python3
"""GD-PARITY — side-by-side parity plate.

Both panels are resampled so that ONE PANEL PIXEL = ONE 720p FRAME-HEIGHT PIXEL.
A subject therefore compares directly by eye: whatever is taller on the plate is
taller as a fraction of the frame. Measured screen-heights are drawn as bars with
their px and %-of-frame-height labels.
"""
import json
from PIL import Image, ImageDraw

REF_H = 720          # common normalisation: fraction-of-frame-height in 720 units
PANEL_W, PANEL_H = 300, 360
ZOOM = 3

def panel(src, src_h, cx, cy, top, bot, left, right, title, sub, colour):
    """cx,cy,top,bot,left,right are in SOURCE pixels of `src` (height src_h)."""
    im = Image.open(src).convert("RGB")
    s = REF_H / src_h
    im = im.resize((int(im.size[0] * s), REF_H), Image.LANCZOS)
    cx, cy = cx * s, cy * s
    x0, y0 = int(cx - PANEL_W / 2), int(cy - PANEL_H / 2)
    x0 = max(0, min(im.size[0] - PANEL_W, x0)); y0 = max(0, min(REF_H - PANEL_H, y0))
    c = im.crop((x0, y0, x0 + PANEL_W, y0 + PANEL_H)).resize(
        (PANEL_W * ZOOM, PANEL_H * ZOOM), Image.NEAREST)
    d = ImageDraw.Draw(c)
    t = (top * s - y0) * ZOOM; b = (bot * s - y0) * ZOOM
    l = (left * s - x0) * ZOOM; r = (right * s - x0) * ZOOM
    d.rectangle([l, t, r, b], outline=colour, width=3)
    bx = max(6, l - 26)
    d.line([(bx, t), (bx, b)], fill=colour, width=5)
    d.line([(bx - 9, t), (bx + 9, t)], fill=colour, width=5)
    d.line([(bx - 9, b), (bx + 9, b)], fill=colour, width=5)
    h720 = (bot - top) * s
    d.rectangle([0, 0, PANEL_W * ZOOM, 62], fill=(12, 12, 16))
    d.text((10, 8), title, fill=(255, 235, 180))
    d.text((10, 26), sub, fill=(190, 210, 255))
    d.text((10, 44), f"screen height {h720:.0f} px @720  =  {100*h720/REF_H:.1f}% of frame height",
           fill=colour)
    return c

L = panel("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots/Screenshot (87).png",
          1080, 962, 530, 449, 611, 878, 1040,
          "GRIM DAWN  ref  Screenshot (87)  1920x1080",
          "player, Lycanthropy (werewolf) form, LongIdle",
          (255, 90, 90))
R = panel("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/"
          "captures/2026-07-31-gd-parity/ours/frames/leg_014.png",
          720, 641, 380, 357, 398, 608, 652,
          "OURS  VFXBO_legacy_full_NOHUD_CAMLOCK f=14  1280x720",
          "player werewolf, RIG_PLAYER_H = 1.80 m, CAM-LOCK",
          (120, 230, 255))

W = PANEL_W * ZOOM
out = Image.new("RGB", (W * 2 + 24, PANEL_H * ZOOM + 74), (10, 10, 14))
out.paste(L, (8, 8)); out.paste(R, (W + 16, 8))
d = ImageDraw.Draw(out)
d.text((10, PANEL_H * ZOOM + 16),
       "SAME CAMERA (CAM-LOCK = GAL-CAM measured operands: pitch 52.95 deg, fov_v 31.79 deg, "
       "stand-off 34.82 m; decision surface identical to GAL-CAM sec.4).",
       fill=(220, 220, 220))
d.text((10, PANEL_H * ZOOM + 34),
       "Both panels normalised so 1 plate pixel = 1 pixel of a 720-high frame. "
       "GD 15.0% vs ours 5.7% of frame height  ->  2.63x.",
       fill=(255, 210, 120))
d.text((10, PANEL_H * ZOOM + 52),
       "galadriel GD-PARITY 2026-07-31 - boxes are measured silhouette bounding boxes, "
       "read on ruler crops (gp_ruler.py) with gp_seg.py as bracket.",
       fill=(150, 150, 160))
out.save("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/"
         "captures/2026-07-31-gd-parity/plates/PLATE_gd_parity_player.png")
print("wrote plate", out.size)
