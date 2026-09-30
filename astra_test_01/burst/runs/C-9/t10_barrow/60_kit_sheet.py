#!/usr/bin/env python3
"""C-9 T10-1b: crop, label and caption the scatter-kit contact sheet for review.

    python3 60_kit_sheet.py

The render is the measurement; this only makes it readable. Two things it does not guess:

  * THE CROP comes from the alpha pass 59_kit_contact.py renders alongside the beauty pass
    -- same camera, same frame -- so the sheet is trimmed to where the props actually are.
    Reading a crop off a preview is how a shadow or a spear tip ends up outside the picture
    that was supposed to show whether the spear tip survived.
  * THE SCALE BAR is exact rather than drawn to taste. The camera is orthographic and the
    props are laid along the ground's screen-right axis, so one metre on that axis is
    exactly `resolution_x / ortho_scale` pixels -- 246.0 here -- and the bar is that wide.
"""
import json
import pathlib

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE / "kit_work" / "contact"
KIT = HERE / "kit"
DEST = pathlib.Path.home() / "Desktop" / "Astra Burst Review - 2026-09-26" / "C-9 barrow" / "scatter kit.png"
PAD = 46
STRIP = 158
HEAD = 82


def font(sz, bold=False):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else
              "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    im = Image.open(WORK / "raw.png").convert("RGB")
    a = np.asarray(Image.open(WORK / "raw_alpha.png").convert("RGBA"))[..., 3] > 8
    meta = json.loads((WORK / "meta.json").read_text())
    man = json.loads((KIT / "kit_assets.json").read_text())["models"]
    ys, xs = np.nonzero(a)
    box = (max(0, xs.min() - PAD), max(0, ys.min() - PAD),
           min(im.width, xs.max() + PAD), min(im.height, ys.max() + PAD))
    im = im.crop(box)
    W = im.width

    out = Image.new("RGB", (W, im.height + STRIP + HEAD), (240, 241, 244))
    out.paste(im, (0, HEAD))
    d = ImageDraw.Draw(out)
    f_t, f_h, f_b, f_s = font(27, True), font(20, True), font(16), font(15)
    d.rectangle([0, 0, W, HEAD - 1], fill=(30, 33, 40))
    # The title counts the cast rather than asserting a number. It said "six props" for a
    # sheet showing three, which is the same class of error as a stale dispatch header:
    # the work changed and the label did not follow.
    shown = [i["name"] for i in meta["items"] if i["name"] != "barbarian"]
    pend = [k for k, v in man.items() if v.get("status") != "keep"]
    d.text((PAD, 12), "C-9 T10-1b  scatter kit — %d prop%s at true scale, play camera "
                      "(orthographic, pitch 52.954°, yaw 47°)"
           % (len(shown), "" if len(shown) == 1 else "s"), font=f_t, fill=(238, 240, 246))
    sub = ("Tripo H3.1 multiview from painted sheets: T10K-* painted from words; T10P-F/G "
           "painted from plates cut out of the concept (no pitch stretch -- the sheets "
           "measured un-squat). Welded reduction 8-10k tris. Painted FRONT faces the camera; "
           "base at y = 0.")
    if pend:
        sub += ("   NOT SHOWN: %s — %s." % (", ".join(sorted(pend)),
                "retired or superseded, not shipped"))
    d.text((PAD, 50), sub, font=f_s, fill=(162, 168, 182))
    y0 = im.height + HEAD

    ppm = meta["px_per_m"]
    bx, by = PAD, y0 + STRIP - 22
    d.line([bx, by, bx + ppm, by], fill=(40, 44, 52), width=4)
    for x in (bx, bx + ppm):
        d.line([x, by - 9, x, by + 9], fill=(40, 44, 52), width=4)
    d.text((bx, by - 33), "1 m on the ground (%.1f px)" % ppm, font=f_s, fill=(40, 44, 52))

    for it in meta["items"]:
        x = it["screen_x_px"] - box[0]
        if it["name"] == "barbarian":
            lines = [("barbarian", (30, 33, 40)),
                     ("1.85 m — scale reference", (70, 74, 84)),
                     ("nb-body.glb, bind pose", (110, 114, 124))]
        else:
            m = man[it["name"]]
            s = m["size_m"]
            sec = m["brief_secondary"]
            lines = [(it["name"], (30, 33, 40)),
                     ("%.2f × %.2f × %.2f m  (w·h·d)" % (s[0], s[1], s[2]),
                      (70, 74, 84)),
                     ("footprint r %.2f m · %s · %d tris"
                      % (m["footprint_radius_m"],
                         "snow bed" if m["snow_bed_ok"] else "no snow bed", m["tris"]),
                      (110, 114, 124))]
            if sec and sec["ratio"] < 0.9:
                lines.append(("%s %.2f m vs brief %.2f m" % (sec["what"], sec["measured_m"],
                                                             sec["brief_m"]), (176, 88, 60)))
        for i, (t, col) in enumerate(lines):
            fo = f_h if i == 0 else f_b
            w = d.textlength(t, font=fo)
            d.text((min(max(4, x - w / 2), W - w - 4), y0 + 10 + i * 24), t, font=fo, fill=col)

    DEST.parent.mkdir(parents=True, exist_ok=True)
    out.save(DEST)
    print("-> %s  %dx%d" % (DEST, out.width, out.height))


if __name__ == "__main__":
    main()
