# R-C9-98 stage 1: write the five Astra briefs (2 armour-set EDITs, 3 weapon model sheets) into briefs/C-9/
# (wave.sh reads briefs/C-9/<id>.task.json). Same format and rules as NB-G1 / SOG-robe / NB-W2: image_cap 2, minutes_cap 15, no retries.
import json, pathlib
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
STYLE_ROLE = "STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose"
STYLE = A + 'inputs/nb_style_ref_matt.png'
SO = A + 'CS9-guides/SO-1_b_harvest.png'   # sha ccdfe73e... = SO-1_b.png, the D7 base
NB = A + 'NB-1/NB-1_b.png'                 # sha 74ddcfd4..., the D2 base
COSA = A + 'CS9-guides/SO-C_a_left_costumeA.png'

GRID = ("(1024x1536 portrait, 2x2 grid: top-left FRONT, top-right the RIGHT side facing the viewer's right, "
        "bottom-left BACK, bottom-right the LEFT side facing the viewer's left)")
KEEP = ("Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1024x1536 sheet: the SAME four views, the SAME grid, the SAME pose, "
        "scale, ground lines and positions, the SAME person, with ONLY the armour below ADDED over the body. 3D models of this armour "
        "will be built from these four views and fitted onto the existing 3D body, so every piece must sit on the body exactly as the "
        "four views agree, and must NOT change the pose, proportions or outline anywhere it does not cover. Never move or shrink the "
        "figure to make room for anything.")


def sheet_tail(tid):
    return ("\nEverything else stays exactly as IMAGE 1 paints it. Paint in IMAGE 1's hand (the STYLE reference's ink line, washes and "
            "hatching). Soft even light, no cast shadows, no ground, no text, no labels.\n"
            "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
            "Two image_gen EDIT calls: variants a and b. NO RETRIES (the image budget is fixed): if a variant has a fault, deliver it "
            "anyway and NAME the fault in concerns -- a view missing or changed facing, the pose, proportions or outline changed where "
            "the armour does not cover, the armour differing between views, the face covered, or a piece named above missing. "
            f"Copy outputs to out/{tid}_a.png and out/{tid}_b.png with sha256. No code. No other files. No web.\n"
            f"RETURN: receipt task_id \"{tid}\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = "
            "the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")


def weapon_tail(tid, what, faults):
    return ("\nThe object is the same in every view (a 3D model will be built from them). Paint in the STYLE reference's hand (dark ink "
            "line, transparent washes, hatching), matched to IMAGE 1. Soft even light, no glow, no cast shadows, no ground, no text, no labels.\n"
            "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
            "Two image_gen calls: variants a and b. NO RETRIES (the image budget is fixed): if a variant has a fault, deliver it anyway "
            f"and NAME it in concerns -- a view missing, the {what} differing between views, {faults}, a hand or person appearing, or "
            f"text appearing. Copy outputs to out/{tid}_a.png and out/{tid}_b.png with sha256. No code. No other files. No web.\n"
            f"RETURN: receipt task_id \"{tid}\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = "
            "the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")


T = {}
T['GS-SBM'] = dict(experiment='R-C9-98-gear-sets', text=(
    "GENERATE BURST GS-SBM -- Run C-9 Phase 2, new armour sets (Matt R-C9-98): the fire sorceress in a STEEL PLATE BATTLE-MAGE SET, "
    "as ONE full set. task_id \"GS-SBM\".\n\n"
    f"IMAGE 1 is her APPROVED four-view sheet {GRID} on #00ff00: a lean athletic woman, long dark hair in one rear braid with the LEFT "
    "side of her head shaved, a plain sleeveless linen shift to the knee, a narrow brown belt, tall brown boots, small orange runes on her "
    "LEFT forearm. IMAGE 2 is her approved costume, for its ember-red colour ONLY. IMAGE 3 is a STYLE reference ONLY.\n"
    f"{KEEP} Keep her face, hair, braid, shaved side and boots exactly.\n"
    "THE ARMOUR TO ADD (a battle mage who wears steel; her fire identity kept in ember red):\n"
    "- HELM: an OPEN-FACED steel helm, a rounded skull with a brow band and short cheek plates; her WHOLE FACE shows (eyes, nose, mouth, "
    "chin uncovered); her braid hangs down her back from under its rear edge; no visor, no horns, no wings;\n"
    "- BODY ARMOUR: a quilted padded ARMING GOWN of dark charcoal cloth with a short MAIL skirt and mail sleeves showing below the plate, "
    "over the linen shift and covering it;\n"
    "- CHEST PIECE: a polished steel BREASTPLATE shaped to a woman's torso, with EMBER-RED RUNES ETCHED into the steel down its centre, "
    "and small steel shoulder plates (spaulders);\n"
    "- GAUNTLETS: steel plate GAUNTLETS with articulated fingers, and steel VAMBRACES on both forearms (the runes on her left forearm are "
    "covered by the vambrace);\n"
    "- PANTS: close-fitting dark LEGGINGS, with steel plate CUISSES over the thighs, KNEE COPS, and steel GREAVES over the shins, the "
    "greaves sitting over the tops of her boots;\n"
    "- FIRE ACCENTS: an ember-red cloth TABARD hanging front and back from under the breastplate to just above the knee, bordered with "
    "small gold runes like IMAGE 2's border, and an ember-red SASH tied at the left hip.\n"
    "NO weapon, NO staff, NO book, NO cloak, NO fur. The breastplate's runes are etched lines of ember red, not glowing light."
    + sheet_tail('GS-SBM')),
    references=[
        dict(path=SO, role="IMAGE 1 -- the approved base-body sheet to EDIT (SO-1 variant b, Matt G1-S; the D7 base)"),
        dict(path=COSA, role="IMAGE 2 -- her approved COSTUME A (SO-C_a left figure, Matt G1-S): ONLY its ember-red colour and gold-rune "
                             "border, for the tabard and sash; never its robe, fur, staff or pose"),
        dict(path=STYLE, role="IMAGE 3 -- " + STYLE_ROLE)])

T['GS-BGL'] = dict(experiment='R-C9-98-gear-sets', text=(
    "GENERATE BURST GS-BGL -- Run C-9 Phase 2, new armour sets (Matt R-C9-98): the barbarian as a FREED CHAMPION GLADIATOR of Rome, as "
    "ONE full set: the ultimate champion who has won his freedom and spends lavishly to awe the crowd. task_id \"GS-BGL\".\n\n"
    f"IMAGE 1 is his APPROVED four-view sheet {GRID}: a huge red-bearded man, bare-chested, braided red hair with one long braid down his "
    "back, a beard ring, a knotwork band tattoo on his RIGHT upper arm, baggy blue trousers, cream leg wraps, brown shoes, a brown belt. "
    "IMAGE 2 is a STYLE reference ONLY.\n"
    f"{KEEP} Keep his face, beard and ring, hair, braid, skin and shoes exactly.\n"
    "THE ARMOUR TO ADD (extravagant: gilded, polished, made for awe):\n"
    "- HELM: an ornate GILDED crested GALEA (a gladiator's helmet) with a broad brim and embossed reliefs, its face OPEN (no face grille; "
    "his whole face and beard show), and a TALL plume of CRIMSON horsehair rising from a gilded crest-holder and sweeping back over the "
    "crown; the plume stays inside each view's own cell and never covers another view; his long braid still hangs down his back below "
    "the helmet;\n"
    "- CHEST PIECE: a GILDED champion's HARNESS: crossed straps of red leather with a gilded embossed PECTORAL disc at the centre of his "
    "chest and gilded fittings, leaving most of his chest, abdomen and back muscle BARE and visible;\n"
    "- BODY ARMOUR: a MANICA, a segmented arm guard of overlapping gilded bronze bands, on his RIGHT arm (his weapon arm) from the "
    "shoulder to the wrist, covering the knotwork tattoo; his LEFT arm stays bare; and a BROAD BALTEUS, a wide belt of bronze plates over "
    "a red leather band, over his own belt;\n"
    "- GLOVES: LEATHER WRIST GUARDS on both wrists studded with GILDED studs;\n"
    "- PANTS: GREAVES (ocreae) of gilded bronze over his shins, strapped over thick PADDED WRAPS in place of his cream leg wraps, and "
    "hanging from the balteus a short skirt of red leather STRAPS edged in gilt over the top of his trousers, front and back;\n"
    "- a RUDIS, the small WOODEN SWORD given to a freed gladiator, tucked at his LEFT hip in the balteus, as a token.\n"
    "NO shield, NO other weapon, NO cape, NO fur."
    + sheet_tail('GS-BGL')),
    references=[
        dict(path=NB, role="IMAGE 1 -- the approved base-body sheet to EDIT (NB-1 variant b, R-C9-70; the D2 base)"),
        dict(path=STYLE, role="IMAGE 2 -- " + STYLE_ROLE)])

SOS = dict(path=SO, role="IMAGE 1 -- her approved base sheet (SO-1 variant b): the woman who carries this, for scale and hand")
NBS = dict(path=NB, role="IMAGE 1 -- his approved base sheet (NB-1 variant b): the man who wields this, for scale and hand")

T['GS-SWAND'] = dict(experiment='R-C9-98-gear-sets', text=(
    "GENERATE BURST GS-SWAND -- Run C-9 Phase 2 (Matt R-C9-98): the battle mage's WAND as a MODEL SHEET for 3D. task_id \"GS-SWAND\".\n\n"
    "IMAGE 1 is her approved character sheet (the woman who carries this wand in one hand; for scale and hand). IMAGE 2 is a STYLE "
    "reference ONLY.\n"
    "Deliver ONE 1536x1024 sheet on flat pure #00ff00 showing ONE object alone (no hands, no person, no belt), in THREE orthographic "
    "views side by side across the sheet, at ONE common scale, the butt of each view on one ground line near the bottom edge, the tip "
    "near the top edge, nothing overlapping:\n"
    "THE WAND, a SHORT battle-mage's wand, about 35 cm long, standing upright with its CRYSTAL at the TOP: a straight shaft of "
    "BLACKENED STEEL, slim and tapering slightly toward the top, with fine ember-red runes etched along it; a GRIP at the bottom about "
    "one hand-width long (about 10 cm), wrapped in dark leather and bound with steel rings, ending in a small round steel butt cap; at "
    "the top a slim steel claw-setting holding an EMBER CRYSTAL, a faceted orange-red crystal about the size of a thumb (about 4 cm tall).\n"
    "Proportions: the whole wand is about 9 times as long as the crystal is tall, and about 3.5 times as long as the grip; the shaft is "
    "about as thick as a finger.\n"
    "LEFT, the wand seen FRONT-ON; MIDDLE, TURNED 90 DEGREES; RIGHT, TURNED 180 DEGREES (the back of the crystal setting)."
    + weapon_tail('GS-SWAND', 'wand', 'it is curved, a staff (longer than an arm), or missing its crystal')),
    references=[SOS, dict(path=STYLE, role="IMAGE 2 -- " + STYLE_ROLE)])

T['GS-SBOOK'] = dict(experiment='R-C9-98-gear-sets', text=(
    "GENERATE BURST GS-SBOOK -- Run C-9 Phase 2 (Matt R-C9-98): the battle mage's STEEL-BOUND GRIMOIRE as a MODEL SHEET for 3D. "
    "task_id \"GS-SBOOK\".\n\n"
    "IMAGE 1 is her approved character sheet (the woman who carries this book in one hand; for scale and hand). IMAGE 2 is a STYLE "
    "reference ONLY.\n"
    "Deliver ONE 1536x1024 sheet on flat pure #00ff00 showing ONE object alone (no hands, no person, no chain, no strap), in FOUR "
    "orthographic views side by side across the sheet, at ONE common scale, the bottom of each view on one ground line, nothing "
    "overlapping:\n"
    "THE GRIMOIRE, CLOSED and standing upright: a thick book about 30 cm tall, 22 cm wide and 7 cm thick (a little taller than her hand "
    "is long); covers of dark oxblood leather BOUND IN STEEL: blackened steel CORNER PIECES on all eight corners, a steel band along the "
    "spine, and TWO steel CLASPS holding it shut across the fore-edge; on the front cover a steel boss set with a small EMBER CRYSTAL, "
    "orange-red, ringed with ember-red runes etched into the steel; the back cover plain leather with its steel corners and a small "
    "central steel boss.\n"
    "Proportions: height to width about 4 to 3; height to thickness about 4 to 1.\n"
    "FIRST (left), the FRONT COVER face-on; SECOND, TURNED 90 DEGREES to show the SPINE face-on; THIRD, TURNED 180 DEGREES, the BACK "
    "COVER face-on; FOURTH (right), TURNED 270 DEGREES to show the FORE-EDGE face-on (the cream page edges between the covers, the two "
    "clasps across them)."
    + weapon_tail('GS-SBOOK', 'book', 'it is open, the proportions are far from 4:3:1, or the clasps are missing')),
    references=[SOS, dict(path=STYLE, role="IMAGE 2 -- " + STYLE_ROLE)])

T['GS-BMAUL'] = dict(experiment='R-C9-98-gear-sets', text=(
    "GENERATE BURST GS-BMAUL -- Run C-9 Phase 2 (Matt R-C9-98): the champion's two-handed GREAT MAUL as a MODEL SHEET for 3D. "
    "task_id \"GS-BMAUL\".\n\n"
    "IMAGE 1 is his approved character sheet (the very big man who wields this with both hands; for scale and hand). IMAGE 2 is a STYLE "
    "reference ONLY.\n"
    "Deliver ONE 1536x1024 sheet on flat pure #00ff00 showing ONE object alone (no hands, no person, no strap), in THREE orthographic "
    "views side by side across the sheet, at ONE common scale, the butt of the haft of each view on one ground line near the bottom "
    "edge, nothing overlapping:\n"
    "THE GREAT MAUL, a TWO-HANDED war maul about 1.3 m long overall, standing upright with its HEAD at the TOP: a long straight HAFT of "
    "dark hardwood about 4.5 cm thick, with iron langets running down from the head, TWO leather-wrapped grip sections (one at the butt, "
    "one at mid-haft) and an iron butt cap; a HEAVY rectangular IRON HEAD about 34 cm long and 14 cm square across its flat striking "
    "faces, with bevelled edges, its sides INLAID with GILDED BRONZE in a band of laurel leaves around a small crest; the haft passes "
    "through the middle of the head.\n"
    "Proportions: the head is about one quarter of the whole length (34 of 130 cm), and about three times as thick as the haft; the haft "
    "is long and slim, NOT a short hammer handle.\n"
    "LEFT, the BROAD SIDE (the head seen full length across the haft, a striking face at each end, the inlay toward the viewer); MIDDLE, "
    "TURNED 90 DEGREES (looking straight at one striking face: the head seen as a square block on the haft); RIGHT, TURNED 180 DEGREES "
    "(the other broad side)."
    + weapon_tail('GS-BMAUL', 'maul', 'it is a short one-handed hammer, the head has a spike or an axe blade, or the haft is shorter than three head-lengths')),
    references=[NBS, dict(path=STYLE, role="IMAGE 2 -- " + STYLE_ROLE)])

for tid, t in T.items():
    task = dict(text=t['text'], references=t['references'], image_cap=2, minutes_cap=15, tool_call_cap=12,
                outputs=[f'out/{tid}_a.png', f'out/{tid}_b.png'], effort='high', add_dirs=[], experiment=t['experiment'])
    p = BURST / 'briefs/C-9' / f'{tid}.task.json'
    assert not p.exists(), f'{p} exists; never overwrite'
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n')
    print('wrote', p)
