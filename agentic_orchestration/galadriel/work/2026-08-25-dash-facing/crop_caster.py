#!/usr/bin/env python3
"""
crop_caster.py — galadriel, 2026-08-25.
Dash-attack facing adjudication (s2c12, row 1 `dash_attack`).

INSTRUMENT: fixed-size crop centred on the caster's SCREEN MIDPOINT as emitted
by the harness itself ([s2a] CASTER_SCREEN@<mark>, foot/head unprojected through
the capture camera at that frame). The crop is NOT eyeballed and NOT derived
from a luma-diff centroid -- a luma-diff centroid on a mover row is biased by
the vacated position and by the shadow, which is why it is not used here.

QUESTION IT ANSWERS: "what does the caster's body look like, at a stated
magnification, at a stated frame, at a known yaw and a known travel direction."
It does NOT by itself answer "which way is he facing" -- that is a reading made
on the output, cross-checked across three yaws.

NO SILENT TRANSFORMATION: every crop is emitted twice --
  *_nn.png   NEAREST upsample (no interpolation; raw pixels, honest)
  *_lz.png   LANCZOS upsample (readable; interpolated -- do not measure on it)
Raw 1:1 crops are emitted as *_raw.png alongside.
"""
import json, os, sys
from PIL import Image

SRC = os.path.expanduser(
    "~/Library/Application Support/Godot/app_userdata/"
    "reincarnated-godot-spike/s2c12")
OUT = os.path.dirname(os.path.abspath(__file__))
CS = json.load(open("/tmp/gal/caster_screen.json"))

BOX = 72        # px, square, centred on caster screen midpoint
ZOOM = 10       # integer upsample factor


def midpoint(arm, mark):
    d = CS[arm][mark]
    fx, fy = d["screen_foot"]
    hx, hy = d["screen_head"]
    return (fx + hx) / 2.0, (fy + hy) / 2.0, d["screen_height_px"]


def crop(arm, mark, tag):
    cx, cy, h = midpoint(arm, mark)
    im = Image.open(os.path.join(SRC, "%s_%s.png" % (arm, mark))).convert("RGB")
    x0, y0 = int(round(cx - BOX / 2)), int(round(cy - BOX / 2))
    c = im.crop((x0, y0, x0 + BOX, y0 + BOX))
    base = os.path.join(OUT, tag)
    c.save(base + "_raw.png")
    c.resize((BOX * ZOOM, BOX * ZOOM), Image.NEAREST).save(base + "_nn.png")
    c.resize((BOX * ZOOM, BOX * ZOOM), Image.LANCZOS).save(base + "_lz.png")
    print("%-30s %-16s centre=(%.1f,%.1f) h=%.1fpx  crop=(%d,%d)+%dx%d  zoom=%dx"
          % (tag, mark, cx, cy, h, x0, y0, BOX, BOX, ZOOM))
    return c


if __name__ == "__main__":
    jobs = [
        # arm,                     mark,        tag
        ("da_arena_static",        "00-pre",    "A_yaw0_rest_arena"),
        ("da_cathedral_static",    "00-pre",    "B_yaw0_rest_cath"),
        ("da_arena_novfx",         "04-arrive", "C_yaw0_arrive_arena"),
        ("da_cathedral_novfx",     "04-arrive", "D_yaw0_arrive_cath"),
        ("da_arena_novfx",         "03b-contact-mid", "E_yaw0_mid_arena"),
        ("da_arena_aim35_novfx",   "04-arrive", "F_yawP35_arrive_arena"),
        ("da_cathedral_aim35_novfx", "04-arrive", "G_yawP35_arrive_cath"),
        ("da_arena_aimn50_novfx",  "04-arrive", "H_yawN50_arrive_arena"),
        ("da_cathedral_aimn50_novfx", "04-arrive", "I_yawN50_arrive_cath"),
    ]
    for arm, mark, tag in jobs:
        crop(arm, mark, tag)
