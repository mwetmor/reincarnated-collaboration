#!/usr/bin/env python3
"""BV2F lane LV, Phase 1.2 (model kit v3): the two MODEL SHEET briefs C7 needs rebuilt.

    python3 fid/lv/tools/lv_sheets.py      -> fid/lv/briefs/BV2F-LV-wreck.task.json, BV2F-LV-barrow.task.json

Method = lane BVP's (barrow_v2/models/tools/bvm_sheets.py, R-C9-155: ALBEDO model sheet on #00ff00 -> cells ->
Tripo H3.1 multiview), with the Phase-1 changes the charter asks for:
  * a 53-degree TOP VIEW cell in every sheet (charter § 5 Phase 1.2) -- the asset must read from the play camera;
  * TRUE PROPORTIONS written in metres, so the build is placed by ONE uniform scale (C7: no per-axis normalise,
    no per-slot stretch; <= 10 % per-axis tolerance);
  * ONE variant per sheet, at most one retry (image_cap 2 each; Phase-1 Astra cap 4, charter § 6).
Identity plates are the already-registered BVM plates (refs_guard: CS9-guides manifest): sketch A's wreck
(bvm_wreck2_identity.png) and the approved chunk-test barrow door (bvm_barrow_identity.png). IMAGE 2 = Matt's
style reference (inputs/nb_style_ref_matt.png), as for every BVM sheet.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
LV = HERE.parent
C9 = LV.parent.parent.parent
G = C9 / "artifacts" / "CS9-guides"
STYLE = C9 / "artifacts" / "inputs" / "nb_style_ref_matt.png"

HEAD = """GENERATE BURST {bid} -- Run C-9 Phase 2 workstream BV2F, lane LV (charter Phase 1.2, model kit v3): MODEL SHEET for a 3D hero asset of the Fjord Headland barrow site, painted as ALBEDO. task_id "{bid}".

IMAGE 1 is the identity plate: {ident}. IMAGE 2 is a STYLE reference ONLY: copy its hand, never its subject.

**Why this sheet exists.** A 3D model is built from the four eye-level views ONCE, placed at its exact place and TRUE size in a snowbound game level, and seen there from a FIXED camera 53 degrees above the ground; it is lit there by a real sun and then the level is painted over it. So the object must READ FROM ABOVE: the fifth cell shows it exactly as that camera sees it.

**One object in five views, not five objects.** The same silhouette, the same timber or stone, the same every mark, from every side. The two side views are each other's mirror -- the one constraint a drawing cannot fake and a multiview build cannot recover from. Keep its TRUE PROPORTIONS exactly as the measurements below say (the model is placed by one uniform scale, never stretched).

**Paint the surface, not the lighting.** Soft, even, shadowless light from nowhere in particular. No key, no bright side and dark side, no rim light, no cast shadow, no shadow on the ground. Tone comes from the object's own colours and from the pen hatching. Snow is painted as surface colour (cream-white, granular, with the pen line around it) where it lies on tops, ledges and inside.

**SHEET.** ONE 1536x1024 landscape sheet of 3 columns x 2 rows of 512 x 512 cells. TOP ROW, left to right: FRONT (the face named below, square to the viewer), RIGHT SIDE (seen square-on from the object's right-hand end), BACK. BOTTOM ROW: LEFT SIDE (square-on from its left-hand end), then the TOP VIEW (the object seen from the FRONT side but from 53 degrees above the ground, looking down at it, no perspective -- as a high fixed game camera sees it), then an EMPTY cell. The four eye-level views are seen from straight ahead at eye level with no perspective tilt, all at exactly the same scale, on one ground line, each filling most of its cell; nothing touches a cell edge. Flat pure #00ff00 everywhere else, and the whole last cell flat #00ff00. No ground, no shadow, no text, no labels, no cell borders, no other objects, nothing overlapping.

**STYLE:** paint in IMAGE 2's hand -- warm dark-brown ink line of varying weight, transparent washes that pool and granulate, fine hatching, cream paper highlights -- in the cold winter palette of IMAGE 1.

---

"""
TAIL = """

Deliver ONE 1536x1024 landscape sheet.
BACKGROUND: keep flat pure #00ff00. If the image model returns a darker or gradient background anyway, DO NOT spend a retry on it (the views are cut out afterwards).

ONE image_gen call. At most ONE retry, and only if a view is missing or has the wrong facing, the object differs between its views, the top view is not seen from above, a view carries a cast shadow or a strong light direction, a view is cut by a cell edge, or {extra} -- name the reason. Never retry for the background colour. Copy the output to out/{bid}.png with sha256. No code. No other files. No web.
RETURN: receipt task_id "{bid}"; images = the file with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL."""

SHEETS = {
    "wreck": dict(plate=G / "bvm_wreck2_identity.png",
                  identw="the wreck as drawn in the chosen site sketch (its look ONLY; seen there from above)",
                  extra="the ship is upright and whole, or ice or a ground mound is painted under it",
                  obj="""**THE OBJECT -- THE WRECK, as IMAGE 1 draws it (R-C9-162: rebuilt to read from 53 degrees above).** An old clinker-built northern longship, 13 m long and 3.6 m in the beam, driven ashore long ago and HALF-SUNK: heeled over about twenty-five degrees toward the viewer in FRONT, so that side's rail lies low near the keel line and the inside of the hull opens toward the viewer and toward the sky. Seen from above it must read at once as a SHIP: the open hull with its row of thwarts and the deck boards, the bare curved RIBS standing up out of the broken after half like a ribcage (some snapped short), the forward half still planked, sprung and gapped; a tall CARVED DRAGON-HEAD PROW rising in a curl at the bow (weathered red-brown and grey, scaled neck, open jaw), a lower broken stern post; the MAST SNAPPED at about 4 m, the stump standing RAKED back, a short torn rag of frozen sail and a trailing stay. Timber weathered grey-brown with darker wet seams; snow lying INSIDE the hull, on the thwarts and along the gunwales as surface colour. NO ICE, NO SNOW MOUND, NO GROUND UNDER IT: the hull ends at its keel line (it will be set half-down into the shore ice in the level).
FRONT = the low, heeled side (the whole 13 m length across the cell, the open hull, ribs and the low broken rail toward the viewer). BACK = the high side (the outside of the planking). RIGHT SIDE = the bow end (the dragon prow). LEFT SIDE = the stern end. TOP VIEW = from the front side, 53 degrees above: the open hull, thwarts, ribs, the prow's curl and the mast stump all clearly visible."""),
    "barrow": dict(plate=G / "bvm_barrow_identity.png",
                   identw="the barrow door as painted in the approved chunk test (its look ONLY; seen there from above)",
                   extra="the door opening is not dark and open, or the opening is wider than it is tall",
                   obj="""**THE OBJECT -- THE FRONT OF THE KING'S BARROW, WITH ITS MONUMENTAL DOOR (R-C9-154).** The carved stone front set into a great burial mound, 18 m wide, 9 m deep (front to back), rising to 9.5 m at its back edge: in the middle the DOOR -- two colossal carved stone uprights 1.4 m wide and a massive carved lintel 1.3 m thick with a capstone above, framing a clear opening exactly 5.0 m wide and 6.5 m high (TALLER THAN IT IS WIDE, 1.3 to 1), with a deep, dark, stone-lined passage behind it; a giant could walk out of it. Interlace and knotwork carved on the uprights and the lintel, rime in the carving. Either side of the door the mound's front slope comes down to a stepped kerb of big weathered stones that curves back at both ends; earth and dead winter grass under wind-drifted snow on the slopes and on top; a few rust heather tufts. Flat stone threshold at ground level. The back is the mound's slope continuing (it will merge into the hill in the level).
FRONT = the door face (all 18 m across the cell). BACK = the rounded back of the slope (snow, grass, no door). RIGHT/LEFT SIDE = the front in profile: the kerb, the slope rising back to 9.5 m, the door frame's edge at the front. TOP VIEW = from the front, 53 degrees above: the dark door opening, the lintel and capstone, the kerb arms and the snowy slope all visible."""),
    "hall": dict(plate=G / "bvm_hall_identity.png",
                 identw="the burnt longhall and its grand porch as painted in the approved chunk test (their look ONLY; seen there from above)",
                 extra="a second doorway appears, the porch doors are shut, or the porch is not on the long wall",
                 obj="""**THE OBJECT -- THE BURNT LONGHALL WITH ITS GRAND PORCH, as ONE building (C7: built at true proportions, never stretched).** A long old northern timber hall 30 m long and 8 m wide; walls of upright split-log planks 3 m high on a low fieldstone footing; a steep thatch-and-turf roof whose ridge is 6.5 m above the ground. It burned: the half of the roof toward the RIGHT end (as seen from the front) has fallen in -- there the charred rafters stand bare and black like ribs, snow lying along them; the left half is still thatched and snow-covered; scorched blackened wall planks, a few posts leaning; carved dragon-head ends on the surviving ridge.
On the FRONT long wall, about ONE FIFTH of the way along from the LEFT end, stands the GRAND PORCH, built against the wall and part of the same building: 8 m wide along the wall and only 4 m deep out from it; carved dark timber side walls; eaves 5.1 m high and a very steep gabled roof whose ridge, 8.5 m high, runs OUT from the hall and stands clearly ABOVE the hall's roofline; two long CARVED FINIALS (stylised beast heads) crossing above its gable peak; carved bargeboards. In the porch front, a great DOUBLE DOORWAY 4.5 m wide and 4.5 m high, its two heavy studded oak leaves standing OPEN, folded back flat against the inside of the porch walls; a dark interior with a dull ember glow deep inside. This is the hall's ONLY door: no other door, window or opening anywhere. Snow on the roofs and finials.
FRONT = the long wall with the porch (the whole 30 m across the cell, the porch toward the left). RIGHT SIDE = the right gable end (8 m wide) with the porch's profile sticking out at the far side. BACK = the other long wall (no door; the porch's roof peeping over at the right). LEFT SIDE = the left gable end, the porch's profile near this end. TOP VIEW = from the front side, 53 degrees above: the long roof (thatched half, burnt rafter half), the porch roof rising above it, the open doorway."""),
}


def main():
    out = []
    import sys
    only = sys.argv[1:]
    for k, sh in SHEETS.items():
        if only and k not in only:
            continue
        bid = f"BV2F-LV-{k}"
        text = HEAD.format(bid=bid, ident=sh["identw"]) + sh["obj"] + TAIL.format(bid=bid, extra=sh["extra"])
        refs = [{"path": str(sh["plate"]), "role": f"IMAGE 1 -- identity plate for {bid}: {sh['identw']}"},
                {"path": str(STYLE), "role": "IMAGE 2 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand the barbarian was painted in"}]
        p = LV / "briefs" / f"{bid}.task.json"
        json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 12,
                   "outputs": [f"out/{bid}.png"], "effort": "high", "add_dirs": [],
                   "experiment": "BV2F-P1-model-kit-v3"}, open(p, "w"), indent=1, ensure_ascii=False)
        out.append(str(p))
    print("\n".join(out))


if __name__ == "__main__":
    main()
