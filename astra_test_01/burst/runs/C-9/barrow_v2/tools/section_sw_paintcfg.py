#!/usr/bin/env python3
"""barrow_v2 SECTION SW (R-C9-158, lane BS): the guided paint-over config, v1 method (T10BF briefs adapted).

    section_sw_paintcfg.py   -> paint/section_sw/cfg_section_sw.json + frame_section_sw.json
Driven by tools/bvp_paint.py (unchanged: 1536 x 1024 canvases at a 1280 x 768 stride, painted neighbour strips
pasted in, one EDIT call per chunk, sketch-A detail per chunk) through tools/section_sw_drive.sh.
"""
import json, math, pathlib, hashlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
SEC = json.load(open(ROOT / "godot/data/section_sw/section.json"))
L = json.load(open(ROOT / "layout_v2.json"))
OUTD = ROOT / "paint/section_sw"
F = SEC["frame"]
PPM, SX0, SY0 = F["ppm"], F["sx0_m"], F["sy0_m"]
A = math.radians(F["pitch_deg"])
SA, CA = math.sin(A), math.cos(A)
GUIDE = OUTD / "section_sw_guide.png"
SKA = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts/BV3r2-A/BV3r2-A.png"
OLD = json.load(open(ROOT / "paint/cfg_barrow_v2.json"))


def scr(x, y, z=0.0):
    return x, SA * y - CA * z


ITEMS = [  # (name, the painter's words, screen points)
    ("wreck", "the beached WRECK: an old longship heeled over on the shingle, snow on its deck and ribs, its floor-side rail broken open, its raked mast", [scr(-47.2, 13.1, 1.0), scr(-49.0, 6.0, 1.0), scr(-45.5, 20.5, 1.0)]),
    ("cave", "the SEA CAVE: the dark arched mouth in the cliff face, a rock ledge at sea level in front of it", [scr(-1.8, 42.5, -4.0), scr(-6.0, 40.0, -4.0), scr(3.5, 44.5, -4.0)]),
    ("stair", "the STAIR: rough rock steps climbing the cliff face from the cave's ledge up to the cliff top, open on the sea side", [scr(13.3, 43.1, -3.7), scr(7.0, 45.0, -6.0), scr(18.0, 40.0, -1.0)]),
    ("spit", "the rocky SPIT running out west from the headland's corner: fractured rock with snow on top, its south face a low sea cliff", [scr(-41.5 - 0.94 * t, 26.8 + 0.34 * t, -0.5) for t in range(0, 22, 3)]),
    ("lagoon", "the LAGOON ICE: shore-fast ice plates with ragged edges and pale snow, dark leads of open water between some of them, PRESSURE RIDGES of tilted ice blocks where the ice meets the shingle", [scr(x, y, -1.3) for x in (-56, -52) for y in range(-4, 27, 4)]),
    ("beach", "the SHINGLE BEACH: grey pebbles and stones under patchy snow, driftwood logs, rust heather and dry grass at its top", [scr(x, y, -0.6) for x in (-50, -47) for y in range(-4, 26, 4)]),
    ("cliff", "the SEA CLIFF: tall weathered fractured rock columns with snow-capped ledges and rust lichen, bites and spurs, sea stacks at their feet", [scr(x, y, -3.0) for x, y in ((-36, 30), (-30, 33), (-24, 36), (-18, 38), (-12, 39), (21, 40))]),
    ("floes", "the SEA ICE below the cliff: broken white-and-lapis floes with ragged edges, dark blue-black open water between them", [scr(x, y, -7.5) for x in range(-56, 22, 6) for y in (36, 42, 48)]),
    ("stream", "the FROZEN STREAM: flat pale-blue ice with cracks, frosted banks, small stones and dry grass on its banks off the snow top", [scr(p[0], p[1], 0.0) for p in SEC["stream"]["polyline"]]),
    ("floor", "the FLAT SNOW TOP (the open fight ground): smooth low snow, at most faint footprints and wind ripples -- KEEP IT OPEN", [scr(x, y, 0.0) for x in range(-40, 20, 5) for y in range(0, 34, 4)]),
]
ONE = ("The section has exactly ONE ship, ONE sea cave and ONE stair: if a painted strip already shows one of them, "
       "continue it and never paint a second.")
notes = {}
for r in range(F["rows"]):
    for c in range(F["cols"]):
        x0, y0 = SX0 + c * 1280 / PPM - 0.5, SY0 + r * 768 / PPM - 0.5
        x1, y1 = x0 + 1536 / PPM + 1.0, y0 + 1024 / PPM + 1.0
        have = [words for name, words, pts in ITEMS if any(x0 <= p[0] <= x1 and y0 <= p[1] <= y1 for p in pts)]
        notes[f"{c}_{r}"] = "it shows " + "; ".join(have) + ". " + ONE if have else ONE

geo = ("IMAGE 1 is not a flat-colour layout: it is a RENDER of a real 3D game level -- the south-west coast of a snowy "
       "northern headland -- seen from the game's fixed high three-quarter ORTHOGRAPHIC camera (53 degrees down, NORTH AT THE "
       "TOP) at true scale: 1 metre = 100 px across, a person would stand about 115 px tall. Every form in it is a real 3D "
       "object standing at exactly this position and size. WHAT IS WHAT: the large flat WHITE ground = the open snow of the "
       "headland's flat top (the fight ground); the PALE BLUE ribbon = a frozen stream running from a frozen mere down to the "
       "shore; the grey-brown speckled slope = a SHINGLE BEACH (grey pebbles under patchy snow); small grey and brown lumps = "
       "pebbles and stones; the brown beached LONGSHIP = an old wreck heeled over on the shingle; long brown cylinders = "
       "driftwood logs; WHITE and pale-blue irregular PLATES = sea ice (broken floes and shore-fast ice plates) and the DARK "
       "BLUE between them = open dark water; small tilted pale blocks along the shoreline = pressure ridges of ice rubble; "
       "the TALL textured ROCK masses = real sea cliffs, a rocky spit and sea stacks; the cliff with the DARK ARCH = the sea "
       "cave; the rock with carved STEPS = the stair up the cliff face; small rust-brown mounds = low rust heather; thin "
       "straw strands = dry winter grass; small stacked stones = cairns; upright grey slabs = old standing stones.")
rules = ("Paint OVER the render in the hand, palette and mood of IMAGE 2 (the chosen sketch of this same site, Matt's pick; it "
         "shows the whole site far smaller, so paint at THIS scale). FOLLOW THE SHAPES IN THE GUIDE; INVENT NO STRUCTURES: every "
         "rock, cliff, floe, stone, log, the ship, the cave and the stair keeps EXACTLY its silhouette, position and size (the "
         "3D world is built from this same render, so anything moved will not match); add no buildings, ships, caves, stairs, "
         "walls, towers or figures. Shadows stay where the render puts them (one low winter sun from the upper LEFT, short "
         "soft blue-violet shadows touching their objects). Turn each rendered form into the painted thing it stands for: "
         "rock into fractured weathered granite with snow-capped ledges and rust lichen; ice into crisp white-and-lapis plates "
         "with ragged edges and thin snow, with dark blue-black open water and small wavelets between them; shingle into grey "
         "pebbles with snow in the hollows; heather into rust tufts; grass into pale straw. THE FLAT SNOW TOP STAYS OPEN: low "
         "smooth snow, at most faint footprints, wind ripples and a very few small tufts -- no rocks, logs, heather clumps or "
         "drifts on it. Rich small detail belongs on the beach, the cliff tops beyond the open snow, the stream's banks and "
         "among the ice. One thin warm dark-brown ink line on every contour, the SAME weight everywhere; transparent "
         "watercolour washes with pen detail; cold blue-white snow, warm grey granite, rust heather, lapis ice. No sky, no "
         "horizon, no text, labels, UI, border, grid, people, animals or characters.")
frame = {"px_per_m": PPM, "origin_px": [(0 - SX0) * PPM, (0 - SY0) * PPM], "pitch_deg": F["pitch_deg"],
         "_law": "plate_X = P*x + X0, plate_Y = P*sin(a)*y - P*cos(a)*z + Y0 (sim frame)"}
OUTD.mkdir(parents=True, exist_ok=True)
json.dump(frame, open(OUTD / "frame_section_sw.json", "w"), indent=1)
cfg = {
    "prefix": "BVSW",
    "name": "barrow_v2 SECTION SW (the wreck, the coast, the sea cave and stair): guided paint-over of the 3D section render at the game camera (plate density)",
    "guide": str(GUIDE), "cols": F["cols"], "rows": F["rows"], "skip": SEC["paint_skip"],
    "experiment": "R-C9-158-barrow-v2-section-sw-paintover",
    "run_tag": "Run C-9 Phase 2 lane BS", "ruling": "R-C9-158",
    "_guide_sha256": hashlib.sha256(GUIDE.read_bytes()).hexdigest() if GUIDE.exists() else None,
    "geo": geo, "rules": rules,
    "refs": [[SKA, "the CHOSEN SITE SKETCH of this same site (Matt's pick): the painted hand, palette, mood and finish to follow -- it is the whole site at a far smaller scale, NOT its layout"]],
    "fill_phrase": "paint over the 3D render, turning every rendered form into what it stands for, in place",
    "retry_extra": "an object has moved off its rendered silhouette, something stands on the flat snow top, ",
    "unpainted_phrase": "rendered (unpainted) areas remain",
    "sketch_detail": {"image": SKA, "frame": str(OUTD / "frame_section_sw.json"), "ties": OLD["sketch_detail"]["ties"], "crop_px": [384, 256],
                      "role": "a DETAIL of the chosen sketch (IMAGE 2) around this panel's place in the site, enlarged: match its DENSITY of small detail and its finish -- NOT its shapes, layout or scale (the layout is IMAGE 1's)"},
    "chunk_notes": notes,
}
json.dump(cfg, open(OUTD / "cfg_section_sw.json", "w"), indent=1, ensure_ascii=False)
print("cfg ok", len(notes), "chunks,", len(cfg["skip"]), "skipped")
