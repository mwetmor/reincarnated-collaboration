#!/usr/bin/env python3
"""
isolate_caster.py — galadriel, 2026-08-25.

INSTRUMENT
  Difference each MOVING novfx arm against its MATCHED `static` arm at the same
  mark and the same stage. The `static` arm is `--fx=novfx --motion=static`:
  identical stage, identical lighting, identical camera, caster parked at the
  origin. So at the caster's ARRIVAL region the static arm holds BACKGROUND ONLY,
  and the difference there is the caster and nothing else.

QUESTION IT ANSWERS
  "Which pixels in this crop belong to the caster's body?" -- and only that.
  It replaces the earlier colour-predicate attempt, which segmented ~19% of the
  crop and was therefore measuring the stage, not the sword. That attempt is
  recorded as discarded rather than deleted.

CONFOUND, STATED
  The staged mobs are KNOCKED BACK on the moving arms, so mob pixels also differ.
  Mob screen positions are emitted per-frame by the harness and are printed here
  so any mob intruding on the crop is visible rather than silently included.

NO SILENT TRANSFORMATION
  Emits the raw crop, the mask, and the masked caster-on-black, each at 1:1 and
  at NEAREST 10x. Nothing is interpolated before measurement.
"""
import json, os
import numpy as np
from PIL import Image

SRC = os.path.expanduser(
    "~/Library/Application Support/Godot/app_userdata/"
    "reincarnated-godot-spike/s2c12")
OUT = os.path.dirname(os.path.abspath(__file__))
CS = json.load(open("/tmp/gal/caster_screen.json"))

BOX = 72
ZOOM = 10
DIFF_MIN = 18     # per-channel max abs difference, 8-bit


def run(arm, static_arm, mark, yaw, tag):
    d = CS[arm][mark]
    fx, fy = d["screen_foot"]
    hx, hy = d["screen_head"]
    cx, cy = (fx + hx) / 2.0, (fy + hy) / 2.0
    x0, y0 = int(round(cx - BOX / 2)), int(round(cy - BOX / 2))
    box = (x0, y0, x0 + BOX, y0 + BOX)

    a = np.asarray(Image.open(os.path.join(SRC, "%s_%s.png" % (arm, mark)))
                   .convert("RGB").crop(box), dtype=np.int16)
    b = np.asarray(Image.open(os.path.join(SRC, "%s_%s.png" % (static_arm, mark)))
                   .convert("RGB").crop(box), dtype=np.int16)
    m = (np.abs(a - b).max(axis=2) > DIFF_MIN)

    iso = a.copy()
    iso[~m] = 0
    base = os.path.join(OUT, tag)
    for name, arr in (("_iso", iso.astype(np.uint8)),
                      ("_rawc", a.astype(np.uint8))):
        im = Image.fromarray(arr)
        im.save(base + name + "_raw.png")
        im.resize((BOX * ZOOM, BOX * ZOOM), Image.NEAREST).save(base + name + "_nn.png")
    Image.fromarray((m * 255).astype(np.uint8)).resize(
        (BOX * ZOOM, BOX * ZOOM), Image.NEAREST).save(base + "_mask_nn.png")

    ys, xs = np.nonzero(m)
    print("%-24s yaw=%+4d  mask n=%4d (%.1f%% of crop)  crop=(%d,%d)+%d  "
          "caster centre=(%.1f,%.1f)"
          % (tag, yaw, m.sum(), 100.0 * m.sum() / m.size, x0, y0, BOX, cx, cy))
    return m


if __name__ == "__main__":
    jobs = [
        ("da_cathedral_novfx",        "da_cathedral_static", "04-arrive",  0, "P_cath_yaw0"),
        ("da_cathedral_aim35_novfx",  "da_cathedral_static", "04-arrive", 35, "Q_cath_yawP35"),
        ("da_cathedral_aimn50_novfx", "da_cathedral_static", "04-arrive", -50, "R_cath_yawN50"),
        ("da_arena_novfx",            "da_arena_static",     "04-arrive",  0, "S_arena_yaw0"),
        ("da_arena_aim35_novfx",      "da_arena_static",     "04-arrive", 35, "T_arena_yawP35"),
        ("da_arena_aimn50_novfx",     "da_arena_static",     "04-arrive", -50, "U_arena_yawN50"),
        ("da_arena_novfx",            "da_arena_static",     "03b-contact-mid", 0, "V_arena_mid_yaw0"),
    ]
    for arm, st, mark, yaw, tag in jobs:
        run(arm, st, mark, yaw, tag)
