#!/usr/bin/env python3
"""
blade_bearing.py — galadriel, 2026-08-25.

INSTRUMENT
  The King's greatsword is the only large blue-grey object on a uniformly warm
  (orange/brown) stage, so it segments on a single colour predicate:
      B - R > BR_MIN  and  V > V_MIN
  Its centroid, minus the caster's screen midpoint (emitted by the harness, not
  estimated), is the blade's screen-space BEARING from the body axis.

QUESTION IT ANSWERS
  "Which way, in screen space, does the caster's held weapon point?"
  The weapon is authored in the KING'S BODY FRAME (king_rig.gd CHANGE 1,
  Matt 2026-06-22): from body-UP, pitched 75 deg toward BODY-FORWARD, yawed
  12 deg toward body-LEFT. So the blade bearing is a proxy for BODY-FORWARD.

WHY IT IS NOT CIRCULAR
  It is measured at THREE DIFFERENT YAWS (0, +35, -50 deg -- the harness's own
  reported caster yaw). The two competing hypotheses (rig fronts +Z vs rig
  fronts -Z) predict bearings that are EXACT NEGATIONS of each other at every
  yaw, and both predictions ROTATE with yaw. A lighting or shadow artefact
  cannot rotate correctly through three yaws; only the body can.

WHAT WOULD REFUTE IT
  Blade bearing failing to rotate with yaw, or matching neither prediction.
  Both outcomes are reported rather than suppressed.
"""
import json, math, os
import numpy as np
from PIL import Image

SRC = os.path.expanduser(
    "~/Library/Application Support/Godot/app_userdata/"
    "reincarnated-godot-spike/s2c12")
CS = json.load(open("/tmp/gal/caster_screen.json"))
J = np.load("/tmp/gal/J.npy")

BOX = 72
BR_MIN = 12      # B - R, 8-bit
V_MIN = 28       # max(R,G,B), 8-bit -- reject near-black


def predict(yaw_deg):
    """Blade world direction under each hypothesis -> screen bearing."""
    a = math.radians(yaw_deg)
    out = {}
    for name, fwd in (("+Z-front", np.array([math.sin(a), 0, math.cos(a)])),
                      ("-Z-front", np.array([-math.sin(a), 0, -math.cos(a)]))):
        w = 0.259 * np.array([0, 1.0, 0]) + 0.966 * fwd   # 75 deg down from up
        s = J @ w
        out[name] = s / np.linalg.norm(s)
    return out


def measure(arm, mark, yaw_deg, label):
    d = CS[arm][mark]
    fx, fy = d["screen_foot"]
    hx, hy = d["screen_head"]
    cx, cy = (fx + hx) / 2.0, (fy + hy) / 2.0
    im = Image.open(os.path.join(SRC, "%s_%s.png" % (arm, mark))).convert("RGB")
    x0, y0 = int(round(cx - BOX / 2)), int(round(cy - BOX / 2))
    a = np.asarray(im.crop((x0, y0, x0 + BOX, y0 + BOX)), dtype=np.int16)
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    mask = ((B - R) > BR_MIN) & (a.max(axis=2) > V_MIN)
    n = int(mask.sum())
    if n < 12:
        print("%-26s yaw=%+4d  BLADE PIXELS n=%d -- BELOW FLOOR, no bearing"
              % (label, yaw_deg, n))
        return None
    ys, xs = np.nonzero(mask)
    bx, by = xs.mean() + x0, ys.mean() + y0
    v = np.array([bx - cx, by - cy])
    v = v / np.linalg.norm(v)
    p = predict(yaw_deg)
    ang = lambda u: math.degrees(math.acos(max(-1, min(1, float(np.dot(u, v))))))
    dp, dm = ang(p["+Z-front"]), ang(p["-Z-front"])
    print("%-26s yaw=%+4d  n=%4d  measured=(%+.3f,%+.3f)  "
          "d(+Z)=%5.1f deg  d(-Z)=%5.1f deg  ->  %s"
          % (label, yaw_deg, n, v[0], v[1], dp, dm,
             "+Z-FRONT" if dp < dm else "-Z-FRONT"))
    return dp, dm


if __name__ == "__main__":
    print("Predicted blade screen bearings (unit vectors, +x right, +y DOWN):")
    for y in (0, 35, -50):
        p = predict(y)
        print("  yaw=%+4d  +Z-front=(%+.3f,%+.3f)   -Z-front=(%+.3f,%+.3f)"
              % (y, p["+Z-front"][0], p["+Z-front"][1],
                 p["-Z-front"][0], p["-Z-front"][1]))
    print()
    jobs = [
        ("da_arena_static",           "00-pre",          0,   "arena rest (static)"),
        ("da_cathedral_static",       "00-pre",          0,   "cath  rest (static)"),
        ("da_arena_novfx",            "03b-contact-mid", 0,   "arena mid-dash"),
        ("da_cathedral_novfx",        "03b-contact-mid", 0,   "cath  mid-dash"),
        ("da_arena_novfx",            "04-arrive",       0,   "arena arrive"),
        ("da_cathedral_novfx",        "04-arrive",       0,   "cath  arrive"),
        ("da_arena_aim35_novfx",      "04-arrive",      35,   "arena arrive aim+35"),
        ("da_cathedral_aim35_novfx",  "04-arrive",      35,   "cath  arrive aim+35"),
        ("da_arena_aimn50_novfx",     "04-arrive",     -50,   "arena arrive aim-50"),
        ("da_cathedral_aimn50_novfx", "04-arrive",     -50,   "cath  arrive aim-50"),
    ]
    for arm, mark, yaw, label in jobs:
        measure(arm, mark, yaw, label)
