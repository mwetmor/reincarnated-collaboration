# Write the five D7 gear briefs: four DRESSED layers and one OBJECT sheet.
#
#   python3 scripts/s8_gear_briefs.py
#
# The same split as the barbarian's D2: garments go in dressed, EDITed onto the
# base-body sheet one layer at a time, so each can be isolated from its own
# Tripo build against the bare base; the weapon goes in alone, as an object
# sheet, and is socketed rather than isolated -- a staff is a thin pole next to
# a leg, and isolating one out of a dressed body would be a guess.
#
# D7 adds what D2 did not have: Matt's chosen COSTUME, the left figure of SO-C_a.
# It is a reference for the LOOK of each layer only, and the retry clause names
# the failure that makes it dangerous: every OTHER costume piece arriving too.
#
# Image budget is 20 for the whole deliverable. SOP-A and SOP-B are capped at 4
# each; these five are capped at 2 each, two variants, NO retry. Worst case 18.
# No franchise names: the guard does not look for the one this character is
# drawn in the manner of, so that is checked here.
import json, re
A = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts/"
BASE = dict(path=A + "CS9-guides/SO-1_b_harvest.png",
            role="IMAGE 1 -- the approved base-body sheet to EDIT (SO-1 variant b, Matt G1-S)")
COST = dict(path=A + "CS9-guides/SO-C_a_left_costumeA.png",
            role="IMAGE 2 -- her APPROVED COSTUME (SO-C_a, left figure, Costume A, Matt G1-S): the look of the ONE layer named, and nothing else")
STYLE = dict(path=A + "inputs/nb_style_ref_matt.png",
             role="IMAGE 3 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose")
SHEET = ("IMAGE 1 is her APPROVED four-view sheet (1024x1536 portrait, 2x2 grid on #00ff00: "
         "top-left FRONT, top-right her RIGHT side facing the viewer's right, bottom-left BACK, "
         "bottom-right her LEFT side facing the viewer's left), the woman's BASE BODY: a lean "
         "athletic woman, long dark hair in one rear braid with the left side of her head shaved, "
         "a plain sleeveless linen shift to the knee, a narrow brown belt, tall brown boots, and "
         "small orange runes on her LEFT forearm. IMAGE 2 is her APPROVED COSTUME, worn by the same "
         "woman. IMAGE 3 is a STYLE reference ONLY (the hand; never its character).")
LAYERS = [
    ("SOG-robe", "layer 1: the ROBE",
     "- ONLY the ROBE of IMAGE 2: an ember-red wool robe, long-sleeved with wide sleeves that end "
     "at mid-forearm, falling to the ankles, and SPLIT OPEN AT THE FRONT from the waist down so "
     "the linen shift and her legs show through the opening; a woven border of darker red with "
     "small gold runes along the hem, the front opening and the cuffs. It is worn over the linen "
     "shift. NO fur, NO belt or pouches, NO circlet, NO bracers, NO staff -- those are other layers.",
     "the robe is not split at the front, or any other costume piece appears"),
    ("SOG-mantle", "layer 2: the FUR MANTLE",
     "- ONLY the MANTLE of IMAGE 2: a short cape of thick grey WOLF FUR over both shoulders, "
     "reaching to the shoulder blades behind and the top of the chest in front, fastened at the "
     "collarbone with two small bronze discs. It is worn over the plain linen shift. NO robe, NO "
     "belt or pouches, NO circlet, NO bracers, NO staff -- those are other layers.",
     "the mantle reaches below the shoulder blades, or any other costume piece appears"),
    ("SOG-cb", "layer 3: the CIRCLET and BRACERS",
     "- ONLY two pieces of IMAGE 2: a slim BRONZE CIRCLET around her brow over the hair, a thin "
     "band with one small ember-red stone at the centre of the forehead; and RUNE-STAMPED LEATHER "
     "BRACERS laced on BOTH forearms from wrist to just below the elbow, dark brown leather with "
     "pressed rune patterns and small bronze rivets. The left bracer covers her forearm runes; "
     "that is correct. NO robe, NO fur, NO belt or pouches, NO staff -- those are other layers.",
     "a bracer is missing from either arm, or any other costume piece appears"),
    ("SOG-belt", "layer 4: the CORSET-BELT and POUCHES",
     "- ONLY the BELT of IMAGE 2: a wide dark-leather CORSET-BELT around her waist, from the "
     "lower ribs to the top of the hips, laced at the front, with BRONZE buckles and studs, and "
     "TWO small leather POUCHES hanging from it, one at each hip. It replaces the narrow belt. "
     "NO robe, NO fur, NO circlet, NO bracers, NO staff -- those are other layers.",
     "a pouch is missing, or any other costume piece appears"),
]
out = []
for tid, what, gear, extra_fault in LAYERS:
    text = ("GENERATE BURST {tid} -- Run C-9 Phase 2, D7 (Matt R-C9-80): MODULAR GEAR for the woman, "
            "{what}. task_id \"{tid}\".\n\n{sheet}\nUse image_gen in EDIT mode on IMAGE 1 and deliver ONE "
            "1024x1536 sheet: the SAME four views, the SAME grid, the SAME pose, scale, ground lines and "
            "positions, the SAME woman (face, hair, braid, shaved side, skin, linen shift, boots), with ONLY "
            "the gear below ADDED. A 3D model of this gear will be built from these four views and fitted onto "
            "her existing 3D body, so it must sit on the body exactly as the four views agree, and must NOT "
            "change her pose, proportions or outline anywhere it does not cover.\nTHE GEAR TO ADD:\n{gear}\n"
            "Everything else stays exactly as IMAGE 1 paints it. Paint in IMAGE 1's hand (IMAGE 3's ink line, "
            "washes and hatching). Soft even light, no cast shadows, no ground, no text, no labels.\n"
            "BACKGROUND: keep flat pure #00ff00. If the image model returns a darker or gradient background "
            "anyway, still deliver the image.\n\nTwo image_gen EDIT calls: variants a and b. NO RETRIES "
            "(the image budget is fixed): if a variant has a fault, deliver it anyway and NAME the fault in "
            "concerns -- a view missing or changed facing, her pose, proportions or outline changed where the "
            "gear does not cover her, the gear differing between views, or {ef}. Copy outputs to "
            "out/{tid}_a.png and out/{tid}_b.png with sha256. No code. No other files. No web.\nRETURN: "
            "receipt task_id \"{tid}\"; images = the files with prompt, references (role + path) and "
            "elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL."
            ).format(tid=tid, what=what, sheet=SHEET, gear=gear, ef=extra_fault)
    out.append((tid, dict(text=text, references=[BASE, COST, STYLE], image_cap=2, minutes_cap=15,
                          tool_call_cap=12, outputs=["out/%s_a.png" % tid, "out/%s_b.png" % tid],
                          effort="high", add_dirs=[], experiment="D7-gear")))
staff_text = """GENERATE BURST SOG-staff -- Run C-9 Phase 2, D7 (Matt R-C9-80): the woman's STAFF as a MODEL SHEET for 3D. task_id "SOG-staff".

IMAGE 1 is her APPROVED COSTUME, worn by the woman who carries this staff in her RIGHT hand (for scale and look). IMAGE 2 is a STYLE reference ONLY (the hand; never its character, and never its own staff).
Deliver ONE 1536x1024 sheet on flat pure #00ff00 showing ONE object alone (no hands, no person), in THREE orthographic views side by side, all at ONE common scale, the foot of the staff on one ground line, nothing overlapping:
THE STAFF of IMAGE 1: a tall walking staff of twisted BLACK WOOD, about as tall as the woman (1.75 m), standing upright, foot on the ground; its crown is an EMBER-STONE, a glowing orange-red stone the size of a fist, gripped in curling IRON CLAWS at the top; a few bands of bronze wire around the shaft where a hand would hold it. Left, the staff seen FRONT-ON; middle, TURNED 90 DEGREES (the claws seen from the side); right, TURNED 180 DEGREES (the back of the claws).
The object is the same in every view (a 3D model will be built from them). Paint in IMAGE 2's hand (dark ink line, transparent washes, hatching), matched to IMAGE 1. Soft even light, no cast shadows, no ground, no text, no labels.
BACKGROUND: keep flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.

Two image_gen calls: variants a and b. NO RETRIES (the image budget is fixed): if a variant has a fault, deliver it anyway and NAME it in concerns -- a view missing, the staff differing between views, a person or hand appearing, or the crown missing its stone or claws. Copy outputs to out/SOG-staff_a.png and out/SOG-staff_b.png with sha256. No code. No other files. No web.
RETURN: receipt task_id "SOG-staff"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL."""
out.append(("SOG-staff", dict(text=staff_text, references=[
    dict(path=COST["path"], role="IMAGE 1 -- her APPROVED COSTUME (SO-C_a, left figure, Costume A, Matt G1-S): the staff in her right hand, for look and scale"),
    dict(path=STYLE["path"], role="IMAGE 2 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose")],
    image_cap=2, minutes_cap=15, tool_call_cap=12,
    outputs=["out/SOG-staff_a.png", "out/SOG-staff_b.png"], effort="high", add_dirs=[],
    experiment="D7-gear")))
BAD = re.compile(r"diablo|\bd2\b|blizzard|sorceress|\bsorc\b|amazon", re.I)
for tid, t in out:
    hit = BAD.findall(t["text"])
    assert not hit, "%s: franchise term in text: %s" % (tid, hit)
    json.dump(t, open("/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/briefs/C-9/%s.task.json" % tid, "w"), indent=1)
    print("wrote %-10s %5d chars, cap %d images, %d refs" % (tid, len(t["text"]), t["image_cap"], len(t["references"])))
