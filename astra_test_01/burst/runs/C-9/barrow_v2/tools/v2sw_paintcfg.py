#!/usr/bin/env python3
"""barrow_v2 SW level (R-C9-159, lane BS): the GROUND-ONLY paint at v1's camera.

    v2sw_paintcfg.py master     -> stage + brief BV2L-master (ONE Astra image: the whole section, colour and light)
    v2sw_paintcfg.py tiles      -> paint/v1cam/cfg_v2sw.json for tools/v2sw_paint.py (8 tiles, each fed its painted
                                   neighbours' overlap and the master's matching area)
The guide is section_v1cam/guide2/v2sw_guide.png (barrow_full tools/v2sw_run.gd -- guide): the ground only, the
models' shadows on it, no plants, no models, at half plate density.
"""
import json, sys, pathlib, hashlib
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
ROOT = pathlib.Path(__file__).resolve().parents[1]
B = ROOT.parents[2]                      # astra_test_01/burst
A9 = B / "runs/C-9/artifacts"
S = A9 / "CS9-guides"
PD = ROOT / "paint/v1cam"
PD.mkdir(parents=True, exist_ok=True)
GUIDE = ROOT / "section_v1cam/guide2/v2sw_guide.png"
LVL = json.load(open(ROOT.parent / "barrow_full/godot/data/barrow_v2_sw/level.json"))
F = LVL["frame"]["paint"]
V1REF = str(A9 / "T10BF-0_1/T10BF-0_1.png")
SKA = str(A9 / "BV3r2-A/BV3r2-A.png")

GEO = ("a RENDER of the GROUND of a real 3D game level -- the south-west coast of a snowy northern headland -- seen from "
       "the game's fixed high three-quarter ORTHOGRAPHIC camera (53 degrees down). ONLY THE GROUND IS IN IT: every cliff, "
       "standing rock, cairn, standing stone, driftwood log, the wrecked ship and every plant are SEPARATE 3D OBJECTS that "
       "stand on this ground in the game and are NOT in this picture -- only their SHADOWS fall on it (the soft dark "
       "blue-grey shapes). WHAT IS WHAT: the large flat pale ground = open snow on the headland's flat top; the PALE BLUE "
       "ribbon = a frozen stream; the round pale blue area = a frozen mere (flat ice); the grey-brown speckled slope = a "
       "shingle beach of grey pebbles under patchy snow; the WHITE irregular PLATES = sea ice, broken floes and shore-fast "
       "ice plates, with small loose ice blocks; the DARK NAVY between them = open water; the grey vertical walls = the "
       "hidden backs of sea cliffs (rock in deep shadow); the dark flat shapes = cast shadows.")
RULES = ("Paint this GROUND, and only the ground, in the hand of IMAGE 2 (the approved first Barrow: its cream-white "
         "granular snow, its soft transparent watercolour washes, its paper grain, its lapis ice with pale cell cracks, its "
         "warm grey rock) -- IMAGE 2's PLANTS, ROCKS AND STONES ARE NOT TO BE COPIED: this picture has NONE. Keep every shape, "
         "edge and shadow exactly where the render puts them (the 3D world is built from this same render). Snow: cream-white "
         "like IMAGE 2, NOT peach and NOT grey, with soft blue-violet shadows exactly where the render's shadows are. Ice: "
         "white-and-lapis plates with ragged edges and a little snow; water between them dark blue-black with small wavelets. "
         "Shingle: grey pebbles with snow in the hollows. Rock walls: dark weathered rock. A SOFT HAND: watercolour wash and "
         "paper texture, at most a very thin, faint pencil line -- NO heavy ink outlines (the game draws its own ink). "
         "ABSOLUTELY NO PLANTS (no heather, no grass, no shrubs, no tufts), NO standing rocks, boulders, cairns, stones, logs, "
         "ships, footprints of creatures, buildings, people or text: ground surfaces only. No sky, no horizon, no border.")


def stage(name, img):
    p = S / name
    img.save(p)
    m = S / "manifest.json"
    d = json.loads(m.read_text()) if m.exists() else {}
    d[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    m.write_text(json.dumps(d, indent=1))
    return p


if sys.argv[1] == "master":
    g = Image.open(GUIDE).convert("RGB")
    h = round(1024 * g.height / g.width)
    can = Image.new("RGB", (1024, 1536), (0, 255, 0))
    can.paste(g.resize((1024, h), Image.LANCZOS), (0, (1536 - h) // 2))
    cp = stage("BV2L-master_canvas.png", can)
    text = ("GENERATE BURST BV2L-master — Run C-9 Phase 2 lane BS (Matt R-C9-159): the MASTER painting of a whole section, "
            "small, for colour and light. task_id \"BV2L-master\".\n\nIMAGE 1 is the canvas to EDIT (1024x1536 portrait): "
            f"its middle band is {GEO} The flat pure #00ff00 bands above and below are NOT part of the picture: leave them "
            f"flat #00ff00.\nUse image_gen in EDIT mode on IMAGE 1 and paint over the render, in place. {RULES}\n\n"
            "One image_gen EDIT call. ONE retry only if anything stands on the ground that the render does not have (a plant, "
            "a rock, a ship, a building), a shape has moved, the snow came out peach or grey, or render areas remain unpainted "
            "-- name the reason. Copy the output to out/BV2L-master.png with sha256. No code. No other files. No web.\n"
            "RETURN: receipt task_id \"BV2L-master\"; images = the file with prompt, references and elapsed_s; calls_used = the "
            "TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
    refs = [{"path": str(cp), "role": "IMAGE 1 — the canvas to EDIT (the ground-only render of the whole section)"},
            {"path": V1REF, "role": "IMAGE 2 — the APPROVED first Barrow's painting (a panel of it): its hand, snow colour, ice and wash ONLY -- not its plants or rocks"},
            {"path": SKA, "role": "IMAGE 3 — the chosen sketch of THIS site (Matt's pick): its mood and its sea, ice and shingle colours ONLY -- not its layout, plants or objects"}]
    json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20,
               "outputs": ["out/BV2L-master.png"], "effort": "high", "add_dirs": [], "experiment": "R-C9-159-v2sw-ground"},
              open(B / "briefs/C-9/BV2L-master.task.json", "w"), indent=1, ensure_ascii=False)
    print("BV2L-master brief ok; guide in canvas at", (1024, h))
    sys.exit()

if sys.argv[1] == "master_extract":
    m = Image.open(A9 / "BV2L-master/BV2L-master.png").convert("RGB")
    g = Image.open(GUIDE)
    h = round(1024 * g.height / g.width)
    sy = m.height / 1536.0
    # inset 8 px top and bottom: the painter feathers the #00ff00 bands a few px into the picture
    band = m.crop((0, int((1536 - h) // 2 * sy) + 8, m.width, int(((1536 - h) // 2 + h) * sy) - 8))
    band.resize((1024, h), Image.LANCZOS).save(PD / "master.png")
    print("master.png", band.size)
    sys.exit()

cfg = {
    "prefix": "BV2M", "name": "barrow_v2 SW at the first Barrow's camera: the GROUND ONLY, painted over its 3D render",
    "guide": str(GUIDE), "cols": F["cols"], "rows": F["rows"], "skip": [],
    "experiment": "R-C9-159-v2sw-ground", "run_tag": "Run C-9 Phase 2 lane BS", "ruling": "R-C9-159",
    "geo": "IMAGE 1 is " + GEO, "rules": RULES,
    "refs": [[V1REF, "the APPROVED first Barrow's painting (a panel of it): its hand, snow colour, ice and wash ONLY -- not its plants or rocks"]],
    "fill_phrase": "paint over the ground render, in place",
    "retry_extra": "anything stands on the ground that the render does not have (a plant, a rock, a ship), the colour departs from the master, ",
    "unpainted_phrase": "render areas remain unpainted",
    "master": {"image": str(PD / "master.png"),
               "role": "the MASTER painting of this whole section, cropped to this panel's place and enlarged: MATCH ITS COLOUR, VALUES AND LIGHT exactly (the panels are joined into one picture)"},
    "chunk_notes": {},
}
json.dump(cfg, open(PD / "cfg_v2sw.json", "w"), indent=1, ensure_ascii=False)
print("cfg ok", F["cols"] * F["rows"], "tiles")
