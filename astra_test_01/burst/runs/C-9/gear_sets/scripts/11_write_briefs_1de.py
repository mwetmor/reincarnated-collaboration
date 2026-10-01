# R-C9-103 (Matt): two more barbarian sheets, each ONE EDIT of GS-BCH2_a (image_cap 2 = one call + one retry ONLY on drift).
#   GS-BCH3  (1d, option 3 "without pants"): champion girdle, studded leather front apron, lion-pelt pieces at sides/back
#   GS-BCH4  (1e, option 1): title-belt girdle with a lion-face plaque, dark lion-pelt kilt split at both sides
# Both: no breeches, no strap skirt, a dark loincloth only where a gap would show skin, no weapon; the kept pieces and the
# registration exactly as GS-BCH2_a.
import json, pathlib
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
HEAD = ("IMAGE 1 is his armoured four-view sheet (1024x1536 portrait, 2x2 grid: top-left FRONT, top-right his RIGHT side facing "
        "the viewer's right, bottom-left BACK, bottom-right his LEFT side facing the viewer's left): a huge red-bearded man in a "
        "gilded brimmed helmet, a plain gilded front-and-back chest plate open at the sides, a large lion pauldron and segmented "
        "manica on his right arm, studded leather wrist guards, a bronze-plated belt with a long skirt of red leather straps edged "
        "in gilt, dark brown leather breeches to above the knee, linen wraps at the knees and shins, gilded greaves and brown "
        "shoes. IMAGE 2 is his approved base body sheet (the registration master). IMAGE 3 is a STYLE reference ONLY.\n"
        "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1024x1536 sheet: the SAME four views, the SAME grid, the SAME pose. "
        "REGISTRATION IS THE FIRST RULE: in every view his head, hands, shoes and soles stay on EXACTLY the same pixels as in IMAGE "
        "1 -- the same height, ground lines, positions and scale. Nothing may move, raise, lower or shrink him.\n"
        "KEEP EXACTLY AS IMAGE 1: the helmet, the chest plates, the lion pauldron and manica, the wrist guards, the linen wraps at "
        "the knees and shins, the greaves, the shoes, his face, beard, hair, braid and skin.\n"
        "REMOVE: the dark leather breeches and the red-and-gilt strap skirt, entirely. His upper thighs are BARE skin below the new "
        "hip-wear; the knee wraps and greaves stay below.\n")
TAIL = lambda tid, faults: (
    "UNDERNEATH: a dark wrapped LOINCLOTH, seen ONLY where a gap in the pieces above would otherwise show bare skin at the hips "
    "or groin. His hips and groin are fully covered in EVERY view; he is not nude anywhere.\n"
    "NO WEAPON anywhere on him: no sword, dagger, scabbard or club.\n"
    "Paint in IMAGE 1's hand. Soft even light, no cast shadows, no ground, no text, no labels.\n"
    "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
    "ONE image_gen EDIT call. ONE RETRY ONLY if the result DRIFTS: he moved, rose, sank or changed scale in any view (compare the "
    "soles and the crown with IMAGE 1), or the helmet, chest plates, lion pauldron, wrist guards, wraps or greaves changed -- name "
    f"the reason, and deliver BOTH images. Do not retry for anything else; NAME any other fault in concerns ({faults}). Copy the "
    f"output to out/{tid}.png (and a retry to out/{tid}_r1.png) with sha256. No code. No other files. No web.\n"
    f"RETURN: receipt task_id \"{tid}\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the "
    "TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
T = {}
T['GS-BCH3'] = (
    "GENERATE BURST GS-BCH3 -- Run C-9 Phase 2 (Matt R-C9-103, option 3): the freed champion gladiator with a CHAMPION GIRDLE, a "
    "studded leather FRONT APRON and LION-PELT pieces at the sides and back, no breeches. task_id \"GS-BCH3\".\n\n" + HEAD +
    "ADD, at his hips:\n"
    "1. THE GIRDLE: a WIDE champion's belt of riveted plates in the SAME polished gilded bronze as his chest plates, PLAIN -- no "
    "symbols, no emblems, no engraving.\n"
    "2. THE FRONT APRON: a heavy DARK LEATHER apron hanging from the girdle at the FRONT, between his legs, down to just ABOVE THE "
    "KNEE; about a hand's width wide at the top and slightly tapered toward its lower end; faced with rows of metal STUDS or small "
    "riveted plates. It is ONE separate flap hanging from the belt.\n"
    "3. THE PELTS: dark LION-PELT pieces (tawny-dark fur) hanging from the girdle at his SIDES and BACK, down to MID-THIGH, SPLIT at "
    "each hip so each thigh moves freely: a pelt over the outside of each hip and one over the buttocks at the back -- separate "
    "hanging pieces, not a closed skirt.\n" +
    TAIL('GS-BCH3', "the apron wider than a hand or reaching below the knee, the pelts joined into a closed skirt, any symbol on the girdle, "
                    "bare groin or buttocks in any view, breeches or strap skirt left on him"))
T['GS-BCH4'] = (
    "GENERATE BURST GS-BCH4 -- Run C-9 Phase 2 (Matt R-C9-103, option 1): the freed champion gladiator with a TITLE-BELT GIRDLE "
    "bearing a lion plaque, and a dark LION-PELT KILT, no breeches. task_id \"GS-BCH4\".\n\n" + HEAD +
    "ADD, at his hips:\n"
    "1. THE GIRDLE: a WIDE champion's title-belt of riveted plates in the SAME polished gilded bronze as his chest plates. At the "
    "FRONT, centred over his navel, a LARGE OVAL polished PLAQUE carrying a LION'S FACE in bold relief, matching the lion on his "
    "right shoulder in style and metal. Nothing else on the belt.\n"
    "2. THE KILT: a dark LION PELT (tawny-dark fur, its edges ragged) wrapped round his hips UNDER the girdle as a kilt, falling to "
    "MID-THIGH all round, SPLIT at BOTH SIDES so each thigh moves freely (a front panel and a back panel).\n" +
    TAIL('GS-BCH4', "the plaque missing or not a lion, the kilt longer than mid-thigh or unsplit at the sides, bare groin or buttocks in "
                    "any view, breeches or strap skirt left on him"))
for tid, text in T.items():
    task = dict(text=text, references=[
        dict(path=A + 'GS-BCH2/GS-BCH2_a.png', role="IMAGE 1 -- his armoured sheet to EDIT (GS-BCH2 variant a, R-C9-98 stage 1c): keep its helm, chest plates, lion pauldron, wrist guards, wraps and greaves"),
        dict(path=A + 'NB-1/NB-1_b.png', role="IMAGE 2 -- his approved base-body sheet (NB-1 variant b, R-C9-70): the registration master only"),
        dict(path=A + 'inputs/nb_style_ref_matt.png', role="IMAGE 3 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose")],
        image_cap=2, minutes_cap=15, tool_call_cap=12, outputs=[f'out/{tid}.png'], effort='high', add_dirs=[],
        experiment='R-C9-103-gear-sets')
    p = BURST / 'briefs/C-9' / f'{tid}.task.json'
    assert not p.exists(), f'{p} exists; never overwrite'
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p)
