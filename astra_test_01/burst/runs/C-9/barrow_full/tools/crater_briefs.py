#!/usr/bin/env python3
"""C-9 CRATER v4 (R-C9-109), layer 2 -- the Astra briefs: one guided EDIT paint-over per crater variant (over its guide
render at the game camera, godot/tools/crater_guide.gd), then one painted EMISSION MASK per variant (over the
paint-over's result). drax.

  python3 tools/crater_briefs.py paint SEED      -> briefs/C-9/VF-crater-v4-SEED.task.json
  python3 tools/crater_briefs.py mask SEED       -> briefs/C-9/VF-crater-v4-SEED-emit.task.json (needs the paint)
Fire with lane/run_burst.py --run C-9 --burst-id <id> --type GENERATE --task briefs/C-9/<id>.task.json
"""
import json
import pathlib
import sys

B = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst")
BF = B / "runs/C-9/barrow_full"
A9 = B / "runs/C-9/artifacts"
CONCEPT = A9 / "T10C-barrow/T10C-barrow_a.png"
TAIL = ("\nRETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE "
        "number of image_gen calls; status; concerns. Never PASS/FAIL.")


SURF = {
    "snow": None,
    "ice": ("R-C9-118 (b): the ICE variant", "a frozen tarn: the meteor struck the ICE",
            "a shallow SHATTERED dish in the ice (it barely dents: ice breaks, it does not bowl), its broken plates tilted and lifted "
            "a little at the rim, MANY radiating FRACTURES running out through the ice exactly where the clay draws them (pale "
            "white-blue edges, dark blue-black depth in each fracture where the water shows), a frosted, steam-whitened skirt "
            "fading back into the clean painted ice; a few sharp ice shards lying on the surface by the rim; the very centre a "
            "dark, wet, broken hole. The ICE'S own palette (lapis and cold blue-whites), not earth or snow"),
    "earth": ("R-C9-118 (b): the EARTH variant", "a moor of heather and thin snow: the blast went through the snow to the "
              "frozen earth and stone beneath",
              "the bowl of SCORCHED EARTH and broken grey STONE (no snow inside it), darker toward the charred centre; the broken "
              "rim of torn turf, dark peat and split rocks, lit on its upper-LEFT faces by the painting's one winter sun (upper "
              "LEFT, 55 degrees up) with short soft blue-violet shadows inside the bowl on the sun's side; the FAULT-LINE CRACKS "
              "exactly where the clay draws them, as dark fissures in earth and stone with the painting's thin warm dark-brown "
              "ink line; the skirt as soot, singed heather stubs and blackened earth fading back into the heather and snow with a "
              "torn, painterly edge; NO snow clods"),
}


def paint_surface(seed, surf):
    run, struck, what = SURF[surf]
    bid = f"VF-crater-v5-{seed}"
    guide = A9 / "inputs" / f"crater_v5_guide_{seed}.png"
    text = (f"GENERATE BURST {bid} — Run C-9, METEOR CRATER v5 ({run}; Matt R-C9-118: the crater \"looks no different in ice or "
            f"on plants\"): a guided EDIT paint-over of a 3D crater rendered on the painted Barrow at the game camera, exactly as "
            f"the Barrow's own chunks were painted. task_id \"{bid}\".\n\n"
            "IMAGE 1 is the canvas to EDIT (1536x1024): the PAINTED Frost King's Barrow at the game camera (orthographic, about 53 "
            f"degrees down; 100 px = 1 m across), with a GREYBOX CLAY 3D IMPACT CRATER in the middle — {struck}: the clay shows the "
            "crater's shape (about 2.2 m across), dark FAULT-LINE CRACKS radiating from the centre (the dark lines drawn on the "
            "clay) with a few running out past the rim, and a soft grey SKIRT where the blast scorched the ground around it.\n"
            "Use image_gen in EDIT mode on IMAGE 1 and paint ONLY the crater (the clay and its soft grey skirt) as a freshly struck, "
            f"already-cooling impact in the painting's own hand: {what}. Keep the crater's position, size and outline EXACTLY as "
            "the clay (it is projected back onto that 3D mesh: anything moved will not match). Everything OUTSIDE the clay and its "
            "skirt stays exactly as it is.\n"
            "NO fire, NO glow, NO orange or red light, NO smoke, NO steam clouds, NO embers — the cracks and centre are painted COLD "
            "and dark (the fire is a separate runtime layer). Palette and hand of IMAGE 2 (the approved Frost King's Barrow "
            "concept): watercolour washes with pen detail, one thin warm dark-brown ink line of the same weight everywhere. No "
            "text, UI, border or characters.\n\n"
            "One image_gen EDIT call. ONE retry only if the crater moved or changed size, anything outside the skirt changed, fire or "
            "glow appears, or grey clay remains unpainted — name the reason. Copy the output to out/crater_v5_" + str(seed) + ".png "
            "with sha256. No code. No other files. No web." + TAIL.format(bid=bid))
    refs = [{"path": str(guide), "role": "IMAGE 1 — the canvas to EDIT (the painted Barrow with the greybox clay crater)"},
            {"path": str(CONCEPT), "role": "IMAGE 2 — the APPROVED Frost King's Barrow concept: palette, light and painted hand ONLY, not its layout"}]
    return bid, text, refs, f"out/crater_v5_{seed}.png"


def paint(seed):
    bid = f"VF-crater-v4-{seed}"
    guide = A9 / "inputs" / f"crater_v4_guide_{seed}.png"      # (a copy of work/v4/guide_SEED/guide.png: refs live under artifacts/)
    text = (f"GENERATE BURST {bid} — Run C-9, METEOR CRATER v4 (Matt R-C9-109: \"painted + real 3d + particle VFX ... the "
            f"natural extension from our scene and character pipeline but for VFX\"): a guided EDIT paint-over of a 3D crater "
            f"rendered on the painted Barrow at the game camera, exactly as the Barrow's own chunks were painted. task_id \"{bid}\".\n\n"
            "IMAGE 1 is the canvas to EDIT (1536x1024): the PAINTED Frost King's Barrow at the game camera (orthographic, about 53 "
            "degrees down; 100 px = 1 m across), with a GREYBOX CLAY 3D IMPACT CRATER in the middle — a meteor has just struck the "
            "snow: a shallow BOWL (about 2.2 m across), a RAISED, BROKEN RIM of thrown-up earth, dark FAULT-LINE CRACKS radiating "
            "from the centre (the dark lines drawn on the clay), one or two cracks running out past the rim, and a soft grey "
            "SKIRT where the blast scorched and melted the snow around it.\n"
            "Use image_gen in EDIT mode on IMAGE 1 and paint ONLY the crater (the clay and its soft grey skirt) as a freshly struck, "
            "already-cooling IMPACT CRATER in the painting's own hand: the bowl of scorched frozen earth and ash, darker toward the "
            "centre; the broken rim of dark wet earth, ash and clods of snow, lit on its upper-LEFT faces by the painting's one winter "
            "sun (upper LEFT, 55 degrees up) with short soft blue-violet shadows inside the bowl on the sun's side; the FAULT-LINE "
            "CRACKS exactly where the clay draws them, as deep dark fissures with the painting's thin warm dark-brown ink line; the "
            "very centre a darker, charred hollow; the skirt as soot and slush and melted snow fading back into the clean snow with "
            "a torn, painterly edge. Keep the crater's position, size and outline EXACTLY as the clay (it is projected back onto "
            "that 3D mesh: anything moved will not match). Everything OUTSIDE the clay and its skirt stays exactly as it is.\n"
            "NO fire, NO glow, NO orange or red light, NO smoke, NO embers — the cracks and centre are painted COLD and dark (the fire "
            "is a separate runtime layer). Palette and hand of IMAGE 2 (the approved Frost King's Barrow concept): watercolour washes "
            "with pen detail, one thin warm dark-brown ink line of the same weight everywhere. No text, UI, border or characters.\n\n"
            "One image_gen EDIT call. ONE retry only if the crater moved or changed size, anything outside the skirt changed, fire or "
            "glow appears, or grey clay remains unpainted — name the reason. Copy the output to out/crater_v4_" + str(seed) + ".png "
            "with sha256. No code. No other files. No web." + TAIL.format(bid=bid))
    refs = [{"path": str(guide), "role": "IMAGE 1 — the canvas to EDIT (the painted Barrow with the greybox clay crater)"},
            {"path": str(CONCEPT), "role": "IMAGE 2 — the APPROVED Frost King's Barrow concept: palette, light and painted hand ONLY, not its layout"}]
    return bid, text, refs, f"out/crater_v4_{seed}.png"


def mask(seed):
    v = "v5" if seed >= 100 else "v4"
    bid = f"VF-crater-{v}-{seed}-emit"
    painted = A9 / f"VF-crater-{v}-{seed}" / f"crater_{v}_{seed}.png"
    guide = A9 / "inputs" / f"crater_{v}_cracks_screen_{seed}.png"
    text = (f"GENERATE BURST {bid} — Run C-9, METEOR CRATER v4 (Matt R-C9-109): the EMISSION MASK for a painted impact crater. "
            f"task_id \"{bid}\".\n\n"
            "IMAGE 1 is the PAINTED crater on the Barrow (1536x1024, the game camera). IMAGE 2 (same size, same framing) marks in "
            "white where its fault-line cracks and its centre are.\n"
            "Use image_gen in EDIT mode on IMAGE 1 to make a TECHNICAL EMISSION MASK of exactly the same size and framing: "
            "PURE BLACK everywhere, except: (1) every painted FAULT-LINE CRACK of the crater in IMAGE 1 (follow the painted fissures "
            "exactly, guided by IMAGE 2), painted as a THIN LIGHT line, brightest (near white) in the crack's deepest middle and "
            "falling to mid grey toward its ends, a few px wide, uneven along its length like a crack that glows more in some "
            "places than others; (2) the crater's CENTRE as an irregular soft-edged light grey patch (smouldering embers), about "
            "a fifth of the bowl's width, brightest in the middle. Nothing else: the rim, the bowl, the skirt, the snow and the "
            "stones are all BLACK. Greyscale only, no colour, no text.\n\n"
            "EXACTLY ONE image_gen EDIT call, NO retry (the image budget is spent to the call): report any defect in concerns "
            "instead. Copy the output to "
            "out/crater_" + v + "_" + str(seed) + "_emit.png with sha256. No code. No other files. No web." + TAIL.format(bid=bid))
    refs = [{"path": str(painted), "role": "IMAGE 1 — the painted crater (the canvas to EDIT into its emission mask)"},
            {"path": str(guide), "role": "IMAGE 2 — where the cracks and the centre are (white on black), same framing"}]
    return bid, text, refs, f"out/crater_{v}_{seed}_emit.png"


def main():
    kind, seed = sys.argv[1], int(sys.argv[2])
    if kind == "paint5":
        bid, text, refs, out = paint_surface(seed, sys.argv[3])
    else:
        bid, text, refs, out = (paint if kind == "paint" else mask)(seed)
    cap = 1 if kind == "mask" else 2
    for r in refs:
        assert pathlib.Path(r["path"]).is_file(), r["path"]
    json.dump({"text": text, "references": refs, "image_cap": cap, "minutes_cap": 15, "tool_call_cap": 20, "outputs": [out],
               "effort": "high", "add_dirs": [], "experiment": "C9-VFX-crater-v4"},
              open(B / "briefs/C-9" / f"{bid}.task.json", "w"), indent=1, ensure_ascii=False)
    print(bid, "brief ok")


if __name__ == "__main__":
    main()
