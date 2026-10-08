#!/usr/bin/env python3
"""BV2F LV (R-C9-234): BEFORE | AFTER blockout stills of the 12 pilot views (fid/pt/pilot/stills_views.json = PH's P11
views; the frame is the plate crop, him at knight_uv facing S), at the play camera (tools/bv2f/m1_stills.gd), as sheets.

    python3 fid/lv/tools/lv_pilot12_sheet.py   -> fid/lv/M1pp/pilot12_sheet_{A,B,C}.jpg (4 pairs each, <= 2000 px wide)
    P12_BEFORE=pilot12_before_238 P12_TAG=238 P12_BEFORE_LABEL="aab3357eb" python3 ...  -> pilot12_238_sheet_{A,B,C}.jpg (R-C9-238)

BEFORE = M1pp/pilot12_before/ (LV 368cdf791, the blockout the BV2F-PS pilot was painted from); AFTER = M1pp/pilot12_after/.
"""
import json
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
LV = os.path.dirname(HERE)
M = os.path.join(LV, "M1pp")
CAP = {
    "pilot_01": "NW: the river's peninsula, the mere's W edge, the margin down to the sea (items 2, 4; river ribbon)",
    "pilot_02": "the mere: organic reed islands + reed beds (item 2)",
    "pilot_03": "the mere's N edge, reed fringe; the barrow's W flank (items 2, 6)",
    "pilot_04": "the barrow door set INTO its mound: front lobe, cutting, dry-stone walls, kerb (item 6)",
    "pilot_05": "the wreck: snapped mast + fallen spar; the mere -> sea margin (items 7, 4)",
    "pilot_06": "the margin's islands and leads; the shingle with snow drifts (items 4, 3)",
    "pilot_07": "the mere's S edge, the shingle's ragged top (items 3, 4)",
    "pilot_08": "the stone circle (fallen stones: weathered lumps, tile 2_1 remnant)",
    "pilot_09": "bottom-left sea ice: broken floes, no square pillars (item 5); the spar on the ice",
    "pilot_10": "the shingle by the wreck: ragged foot, ice bays, drifts (item 3)",
    "pilot_11": "the cliffs left of the cave (unchanged, passed)",
    "pilot_12": "the circle + the cave/stair (unchanged, passed)",
}


BEFORE = os.environ.get("P12_BEFORE", "pilot12_before")
TAG = os.environ.get("P12_TAG", "")
BLABEL = os.environ.get("P12_BEFORE_LABEL", "LV 368cdf791, painted as BV2F-PS")
if TAG == "239":
    CAP.update({"pilot_03": "the mound's W cut edge: smooth (R-C9-239 1)", "pilot_04": "the cutting's edges both sides: smooth, no sawtooth (R-C9-239 1)",
                "pilot_05": "no dark wedge along the shingle foot (R-C9-239 2)", "pilot_06": "rounded drifts on the shingle (R-C9-239 3)",
                "pilot_09": "the shingle foot by the wreck: no lead wedge (R-C9-239 2)", "pilot_10": "rounded wind-scalloped drifts (R-C9-239 3)"})
if TAG == "238":
    CAP.update({"pilot_04": "barrow door: smooth mound flank (8 px/m terrain), rough stone wall ends (R-C9-238 c, d)",
                "pilot_05": "wreck + margin: leads = gaps between rounded floes, widening to the sea (R-C9-238 b); no ripples (c)",
                "pilot_06": "margin + shingle: one continuous beach, small wind drifts (R-C9-238 a, b, c)",
                "pilot_09": "shingle foot by the wreck, drifts in its lee (R-C9-238 a)",
                "pilot_10": "the shingle: continuous, ragged foot, small drifts (R-C9-238 a)"})


def main():
    spec = json.load(open(os.path.join(M, "pilot12_spec.json")))
    names = [s["name"] for s in spec]
    pw, ph, cap_h = 960, 540, 30
    for si, part in enumerate(("A", "B", "C")):
        chunk = names[si * 4:(si + 1) * 4]
        sheet = Image.new("RGB", (2 * pw + 30, len(chunk) * (ph + cap_h) + 40), (246, 243, 236))
        d = ImageDraw.Draw(sheet)
        d.text((10, 12), "R-C9-%s blockout fix -- the 12 pilot views at the play camera: BEFORE (%s) | AFTER" % (TAG or "234", BLABEL), fill=(0, 0, 0))
        for k, nm in enumerate(chunk):
            y = 40 + k * (ph + cap_h)
            d.text((10, y + 8), "%s -- %s" % (nm, CAP.get(nm, "")), fill=(0, 0, 0))
            for j, sub in enumerate((BEFORE, "pilot12_after")):
                im = Image.open(os.path.join(M, sub, nm + ".png")).convert("RGB").resize((pw, ph), Image.LANCZOS)
                sheet.paste(im, (10 + j * (pw + 10), y + cap_h))
        out = os.path.join(M, ("pilot12_%s_sheet_%s.jpg" % (TAG, part)) if TAG else ("pilot12_sheet_%s.jpg" % part))
        sheet.save(out, quality=88)
        print(out, sheet.size)


if __name__ == "__main__":
    main()
