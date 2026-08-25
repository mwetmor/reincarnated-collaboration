#!/usr/bin/env python3
"""eor_cooldown.py — did the referent CAST A DISCRETE SKILL here?

galadriel / visual-perception seam.  MD-B4app-2b.

Grim Dawn draws a large saturated-red NUMERAL over a skill icon for as long as
that skill is on cooldown.  The numeral is the only surface on camera that
publishes a discrete skill activation: the world view is swamped by combat VFX,
the HUD energy readout is a scalar that cannot name a skill, and the input
device is not on camera at all.

The detector deliberately does NOT box the slots.  Several icons are themselves
red (the right-mouse icon is a red swirl; slots 2 and 7 are orange-red), so a
naive red count is dominated by icon art.  Instead a per-pixel BASELINE map of
"how often is this pixel red" is built from frames sampled across the whole
window, and only red pixels OUTSIDE that baseline are counted.  A cooldown
numeral lights pixels that are almost never red, and its COLUMN says which slot.

Ground truth used to fix the thresholds (eye-read, magnified x2.5):
    t = 744.30  slot 4 shows a red "1"      -> detector must fire
    t = 744.90  slot 4 clean, all slots idle -> detector must not fire
Both frames are kept as evidence.

  baseline <video> <t0> <t1> <out.npz>          per-pixel red frequency
  trace    <video> <t0> <t1> <baseline.npz> <out.json> <hz>   REJECTED -- see note
  slots    <video> <t0> <t1> <out.json> <hz>                  per-slot dimming
"""
import sys, json, subprocess
import numpy as np

BOX = (700, 1040, 540, 38)      # x, y, w, h — the skill-bar ICON CELLS ONLY.
# A first pass used y 1020..1080 and was CONTAMINATED: that box also contains the
# gold experience bar and the bottom of the BUFF-ICON ROW, whose icons are red and
# animate, which manufactured 0.1-0.4 s "cooldown" bursts that no cooldown can
# produce. Caught by eye-reading t=732.27, where the detector's column pointed at
# slot 7 and the eye found slot 7 idle and a red buff icon above the bar. The box
# is now the icon cells alone; the numerals sit inside them.
#
# The detector counts RED numerals only. Grim Dawn also draws WHITE numerals on
# icons (buff/toggle remaining duration -- e.g. slot 4 reads a white "13" at
# t=732.27). White fails the G/B ceiling below, so buff timers are excluded by
# construction, which is the intent: a buff timer is not a cast.
R_MIN, GB_MAX = 150, 90         # the cooldown numeral's colour: bright R, dark G/B
BASE_FREQ = 0.05                # a pixel red in >5 % of baseline frames is icon art
MIN_PX = 12                     # novel-red pixels needed to call a numeral present


def _stream(video, t0, t1, hz):
    x, y, w, h = BOX
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.6f}", "-t", f"{t1 - t0:.6f}",
           "-i", video, "-vf", f"fps={hz},crop={w}:{h}:{x}:{y}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)
    fsz = w * h * 3
    k = 0
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        yield t0 + k / hz, np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        k += 1
    p.wait()


def redmask(fr):
    a = fr.astype(np.int16)
    return (a[:, :, 0] > R_MIN) & (a[:, :, 1] < GB_MAX) & (a[:, :, 2] < GB_MAX)


def baseline(video, t0, t1, out):
    acc = None; n = 0
    for _, fr in _stream(video, float(t0), float(t1), 2.0):
        m = redmask(fr)
        acc = m.astype(np.float32) if acc is None else acc + m
        n += 1
    freq = acc / n
    art = freq > BASE_FREQ
    np.savez_compressed(out, freq=freq, art=art, n=n)
    print(f"baseline: {n} frames, {int(art.sum())} px classed icon-art "
          f"of {art.size} ({100*art.mean():.1f} %)")


def trace(video, t0, t1, basep, out, hz):
    z = np.load(basep); art = z["art"]
    rows = []
    for t, fr in _stream(video, float(t0), float(t1), float(hz)):
        novel = redmask(fr) & ~art
        n = int(novel.sum())
        col = int(np.argmax(novel.sum(axis=0))) if n else -1
        rows.append({"t": round(t, 4), "novel_red": n, "col": col,
                     "cd": bool(n >= MIN_PX)})
    json.dump({"video": video, "t0": float(t0), "t1": float(t1), "hz": float(hz),
               "box": BOX, "min_px": MIN_PX, "rows": rows}, open(out, "w"))
    on = sum(1 for r in rows if r["cd"])
    print(f"cooldown: {len(rows)} frames, numeral present in {on} "
          f"({100.0*on/max(1,len(rows)):.1f} %)")




# ===========================================================================
#  Per-slot DIMMING -- the instrument that survived
# ===========================================================================
#
# The red-numeral detector above is REJECTED for measurement (see the note):
# a numeral drawn over red icon art falls inside the art baseline and is not
# counted, so slots 2, 7 and R are structurally blind. Grim Dawn also DIMS a
# skill's icon for the whole cooldown, which is a large, slot-local, art-
# independent signal -- and it is present on every slot including the red ones.
#
# Slot boxes were read off a x2 magnified contact sheet of the icon strip and
# are listed with the slot's key label. Slots 1, 5, 6, 8, 9 and 0 are EMPTY on
# this build and are carried only as a null channel.
SLOTS = {"1": (701, 737), "2": (742, 777), "3": (784, 819), "4": (827, 862),
         "5": (869, 904), "L": (917, 954), "R": (962, 999), "6": (1007, 1042),
         "7": (1049, 1084), "8": (1092, 1127), "9": (1134, 1169), "0": (1177, 1212)}
SY = (1042, 1076)
SBOX = (700, 1042, 540, 34)


def slots(video, t0, t1, out, hz):
    x, y, w, h = SBOX
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{float(t0):.6f}", "-t", f"{float(t1)-float(t0):.6f}",
           "-i", video, "-vf", f"fps={hz},crop={w}:{h}:{x}:{y}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)
    fsz, k, rows = w * h * 3, 0, []
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(h, w, 3).astype(np.float32)
        v = fr.max(axis=2)
        rows.append({"t": round(float(t0) + k / float(hz), 4),
                     **{s: round(float(v[:, a - x:b - x].mean()), 2)
                        for s, (a, b) in SLOTS.items()}})
        k += 1
    p.wait()
    json.dump({"video": video, "t0": float(t0), "t1": float(t1), "hz": float(hz),
               "box": SBOX, "slots": SLOTS, "rows": rows}, open(out, "w"))
    print(f"slots: {len(rows)} frames x {len(SLOTS)} cells")


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "baseline":
        baseline(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif c == "slots":
        slots(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    elif c == "trace":
        trace(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    else:
        sys.exit(__doc__)
