#!/usr/bin/env python3
"""barrow_v2 hero models (lane BVP, drax; R-C9-155, the v1 method): MODEL SHEET briefs, one hero per sheet.

    python3 models/tools/bvm_sheets.py            -> briefs/C-9/BVM-<sheet>.task.json + identity plates in CS9-guides

The lane route of the first Barrow (t10_barrow T10K/T10P, t9_props T9P): an Astra four-view MODEL SHEET painted as
ALBEDO on flat #00ff00 -> BiRefNet matte -> cells -> Tripo H3.1 multiview on fal -> reduce -> normalise to the
layout's metres. Each hero is built ONCE. Sizes are layout_v2.json's (v5; v6 slots adjust them by scale only).

Identity plates (IMAGE 1) are crops of what Matt has already seen and liked: the chunk re-test (BVR) for the hall,
porch and barrow door; sketch A for the wreck and the cliffs. IMAGE 2 is the barbarian's hand (inputs/nb_style_ref_matt.png).
"""
import hashlib, json, os, pathlib
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

HERE = pathlib.Path(__file__).resolve().parent
BV2 = HERE.parent.parent
C9 = BV2.parent
B = C9.parent.parent
S = C9 / "artifacts" / "CS9-guides"
STYLE = C9 / "artifacts" / "inputs" / "nb_style_ref_matt.png"


def manifest_add(p):
    m = S / "manifest.json"; d = json.loads(m.read_text()) if m.exists() else {}
    d[p.name] = hashlib.sha256(p.read_bytes()).hexdigest(); m.write_text(json.dumps(d, indent=1))


def plate(name, src, box):
    p = S / f"bvm_{name}_identity.png"
    Image.open(src).convert("RGB").crop(box).save(p)
    manifest_add(p)
    return p


T2A = BV2 / "paint" / "test" / "T2a_hall_stitched.png"
T2B = BV2 / "paint" / "test" / "T2b_barrow_stitched.png"
SKA = BV2 / "sites" / "BV3r2-A.png"

HEAD = """GENERATE BURST {bid} — Run C-9 Phase 2, lane BVP (Matt R-C9-155, the first Barrow's method): MODEL SHEET for a 3D hero asset of the Fjord Headland barrow site, painted as ALBEDO. task_id "{bid}".

IMAGE 1 is the identity plate: {ident}. IMAGE 2 is a STYLE reference ONLY: copy its hand, never its subject.

**Why this sheet exists.** A 3D model is built from these four views ONCE, placed at its exact place and size in a snowbound game level, seen from above at a steep angle, and **lit there by a real sun**; then the level is painted over it. So:

**One object in four views, not four objects.** The same silhouette, the same timber or stone, the same every mark, seen from four sides. The two side views are each other's mirror -- the one constraint a drawing cannot fake and a multiview build cannot recover from.

**Paint the surface, not the lighting.** Soft, even, shadowless light from nowhere in particular. No key, no bright side and dark side, no rim light, no cast shadow, no shadow on the ground. Tone comes from the object's own colours and from the pen hatching. Snow is painted as surface colour (cream-white, granular, with the pen line around it) where it lies on roofs, ledges and tops.

**SHEET.** ONE 1536x1024 landscape sheet, {layout}. Flat pure #00ff00 everywhere else. The views of one object at exactly the same scale, on one ground line, each filling most of its cell, nothing touching a cell edge. No ground, no shadow, no text, no labels, no cell borders, no other objects, nothing overlapping.

**STYLE:** paint in IMAGE 2's hand -- warm dark-brown ink line of varying weight, transparent washes that pool and granulate, fine hatching, cream paper highlights -- in the cold winter palette of IMAGE 1.

---

"""
TAIL = """

Deliver ONE 1536x1024 landscape sheet per variant.
BACKGROUND: keep flat pure #00ff00. If the image model returns a darker or gradient background anyway, DO NOT spend a retry on it (the views are cut out afterwards).

Two image_gen calls: variants a and b. ONE retry per variant only if a view is missing or has the wrong facing, the object differs between its views, a view carries a cast shadow or a strong light direction, a view is cut by a cell edge, or {extra} -- name the reason. Never retry for the background colour. Copy outputs to out/{bid}_a.png and out/{bid}_b.png with sha256. No code. No other files. No web.
RETURN: receipt task_id "{bid}"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL."""

L2x2 = "2 x 2 cells of 768 x 512 for ONE object: TOP-LEFT = FRONT (the face named below, square to the viewer), TOP-RIGHT = RIGHT SIDE (seen square-on from the object's right-hand end), BOTTOM-LEFT = BACK, BOTTOM-RIGHT = LEFT SIDE (seen square-on from its left-hand end); all four seen from straight ahead at eye level, no perspective tilt"
L4x2 = "4 columns x 2 rows of 384 x 512 cells: TOP ROW = the first object, BOTTOM ROW = the second; each row is ONE object in four views at one scale, columns left to right FRONT, RIGHT SIDE, BACK, LEFT SIDE, all seen from straight ahead at eye level; the two rows need not share a scale"

SHEETS = {
    "hall": dict(layout=L2x2, ident=lambda: plate("hall", T2A, (0, 0, 2816, 2560)),
                 identw="the burnt longhall as painted in the approved chunk test (its look ONLY; it is seen there from above)",
                 extra="a second doorway appears",
                 obj="""**THE OBJECT -- THE BURNT LONGHALL (the body only, without its porch).** A long old northern timber hall, 28.5 m long, 8 m wide; walls of upright split-log planks about 3 m high, on a low fieldstone footing; a steep thatch-and-turf roof whose ridge is 6.1 m above the ground. It burned: about HALF of the roof has fallen in -- in that half the charred rafters stand bare and black against the sky like ribs, snow lying along them, the rest of the roof still thatched and snow-covered; scorched blackened wall planks, some fallen, a few posts leaning. Carved dragon-head ends on the ridge where it survives.
FRONT = the LONG side wall (the whole 28.5 m length across the view). It has exactly ONE doorway, a tall dark opening 4.5 m wide and 4.5 m high, centred about three fifths of the way along from the left end (a porch will be fitted over it). No other door, window or opening anywhere on the hall. RIGHT SIDE and LEFT SIDE = the two narrow gable ends (8 m wide), their gables standing; BACK = the other long wall, with no door."""),
    "porch": dict(layout=L2x2, ident=lambda: plate("porch", T2A, (1150, 0, 2250, 1300)),
                  identw="the hall's grand porch as painted in the approved chunk test (its look ONLY; seen there from above)",
                  extra="the doors are shut",
                  obj="""**THE OBJECT -- THE HALL'S GRAND PORCH.** A tall gabled timber porch that stands against a hall's long wall (its back is open, where it joins the hall). 6.4 m wide, 3.0 m deep; walls of carved dark timber; eaves 5.1 m high and a very steep roof whose ridge is 7.8 m high, running from the back to the front; the ridge ends at the front in two long CARVED FINIALS (stylised beast heads) that cross above the gable peak. The gable front carries carved bargeboards and interlace panels. In it, a great DOUBLE DOOR opening 4.5 m wide and 5.1 m high, its two heavy studded oak leaves standing OPEN, swung outward against the front wall; a dark interior with a dull ember glow deep inside. Snow on the roof slopes and on the finials.
FRONT = the gable front with the open doors. BACK = the open back (where it meets the hall): the roof and side walls seen from behind, the doorway's dark shape through it. RIGHT/LEFT SIDE = the long roof slope and side wall in profile, the finials sticking up at the front end."""),
    "gable": dict(layout=L2x2, ident=lambda: plate("gable", T2A, (0, 1300, 1700, 2560)),
                  identw="the hall's collapsed end as painted in the approved chunk test (its look ONLY; seen there from above)",
                  extra="the ruin reads as an intact building",
                  obj="""**THE OBJECT -- THE COLLAPSED END OF THE BURNT HALL.** A ruin 8 m wide and 6 m deep, no more than 2.8 m high anywhere: the end gable wall of a timber hall has FALLEN OUTWARD and lies tilted on a heap of its own rubble -- charred split-log planks still pegged together, broken rafters, scorched thatch, scattered fieldstones of the footing, ash and a few dying embers; two stumps of corner posts still stand. Snow in drifts over part of the heap.
FRONT = the side the gable fell toward (its face lying down toward the viewer). BACK = the open end where it broke from the rest of the hall: the broken rafter ends. RIGHT/LEFT SIDE = the heap in profile, low and ragged."""),
    "barrow": dict(layout=L2x2, ident=lambda: plate("barrow", T2B, (1350, 0, 3250, 1300)),
                   identw="the barrow door as painted in the approved chunk test (its look ONLY; seen there from above)",
                   extra="the door opening is not dark and open",
                   obj="""**THE OBJECT -- THE FRONT OF THE KING'S BARROW, WITH ITS MONUMENTAL DOOR.** A section of a great burial mound 20 m wide and 13.5 m deep, rising to 10.5 m: a steep grassy mound of earth and dead winter grass under wind-drifted snow, ringed at its foot by a stepped kerb of big weathered stones. Cut into its front, a stone-lined forecourt 2.6 m deep with flagstones, and at its back the DOOR: two colossal carved stone uprights and a massive carved lintel with a capstone above, framing a clear opening 5.0 m wide and 6.5 m high -- a giant could walk out of it -- and behind it a deep, dark, stone-lined passage. Interlace and knotwork carved on the uprights and the lintel, rime in the carving. A few standing stones and rocks on the mound's flanks.
FRONT = the door face. BACK = the round back of the mound (snow, grass, kerb stones; no door). RIGHT/LEFT SIDE = the mound in profile with the door frame's edge at the front."""),
    "wreck": dict(layout=L2x2, ident=lambda: plate("wreck", SKA, (20, 300, 330, 560)),
                  identw="the wreck as drawn in the chosen site sketch (its look ONLY; seen there from above, far smaller)",
                  extra="the ship is upright and whole",
                  obj="""**THE OBJECT -- THE WRECK.** An old clinker-built northern longship, 17 m long and 4.6 m in the beam, run aground and frozen fast in shore ice: heeled over about twenty degrees toward its LEFT side (the side that faces the viewer in FRONT), so that side's rail is low; planks sprung and missing, ribs showing through, the high carved prow (a dragon head) and stern posts weathered grey-brown; a broken mast 8 m tall standing raked back, with a torn frozen rag of sail and a trailing stay; snow in the hull, ice and broken ice blocks heaped around the waterline.
FRONT = the low, heeled side (the whole 17 m length across the view, its rail low and broken). BACK = the high side. RIGHT/LEFT SIDE = the bow and the stern ends."""),
    "cliffs": dict(layout=L4x2, ident=lambda: plate("cliffs", SKA, (330, 560, 800, 960)),
                   identw="the sea cliff, sea cave and stair as drawn in the chosen site sketch (their look ONLY; seen there from above, far smaller)",
                   extra="the cave or the stair is missing",
                   obj="""**TOP ROW -- THE SEA-CAVE CLIFF.** A section of sea cliff 14 m wide and 7.5 m high, of columnar, fractured grey-brown rock with snow on its ledges and rust heather at the top edge; at its foot a HUGE dark SEA-CAVE MOUTH, 9.5 m wide and 6.9 m high, framed by rough rock with a thick rock lintel above, on a rock ledge at the waterline with ice blocks. FRONT = the cliff face with the cave mouth; BACK = the cliff's rough back (the headland behind it); RIGHT/LEFT SIDE = the cliff in profile, the cave's depth showing as a notch at the foot.

**BOTTOM ROW -- THE STAIR CLIFF.** A section of the same cliff 10.4 m wide and 7.5 m high, with a broad rough-cut stone STAIR 5 m wide climbing ACROSS its face from the lower LEFT (a rock ledge at the water) to the upper RIGHT (the cliff top), about 35 degrees, open on its outer edge, the cliff face its inner wall; snow on the treads. FRONT = the face with the stair; BACK = the rough back; RIGHT/LEFT SIDE = profiles showing the stair's slope."""),
    "rocks": dict(layout=L4x2, ident=lambda: plate("rocks", SKA, (700, 620, 1300, 1000)),
                  identw="the sea cliff and its rocks as drawn in the chosen site sketch (their look ONLY; seen there from above, far smaller)",
                  extra="a row is not one rock mass",
                  obj="""**TOP ROW -- A PLAIN CLIFF SECTION.** A straight section of sea cliff 8 m wide and 7.5 m high, columnar fractured grey-brown rock, ledges, snow caps on the column tops, rust heather on the top edge, a scree foot. No opening. FRONT = the face; BACK = rough back; SIDES = profiles.

**BOTTOM ROW -- A ROCK OUTCROP.** A weathered crag of stratified grey granite about 4 m wide and 3 m tall, in three or four stepped irregular layers, cracked, with pale and rust lichen, snow caps on its ledges, a few boulders at its foot. FRONT = its broadest face; BACK, SIDES = the same crag from the other sides."""),
}


def main():
    out = []
    for k, sh in SHEETS.items():
        bid = f"BVM-{k}"
        ip = sh["ident"]()
        text = HEAD.format(bid=bid, ident=sh["identw"], layout=sh["layout"]) + sh["obj"] + TAIL.format(bid=bid, extra=sh["extra"])
        refs = [{"path": str(ip), "role": f"IMAGE 1 — identity plate for {bid}: {sh['identw']}"},
                {"path": str(STYLE), "role": "IMAGE 2 — STYLE reference ONLY (Matt-supplied, R-C9-69): the hand the barbarian was painted in"}]
        json.dump({"text": text, "references": refs, "image_cap": 4, "minutes_cap": 15, "tool_call_cap": 20,
                   "outputs": [f"out/{bid}_a.png", f"out/{bid}_b.png"], "effort": "high", "add_dirs": [],
                   "experiment": "R-C9-155-barrow-v2-heroes"},
                  open(B / "briefs" / "C-9" / f"{bid}.task.json", "w"), indent=1, ensure_ascii=False)
        out.append(bid)
    print(" ".join(out))


if __name__ == "__main__":
    main()
