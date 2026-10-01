# R-C9-98 stage 1c (Matt: GS-BCH_b's chest piece, helm and shoulder are liked; too nude; no weapons on the character).
# ONE brief GS-BCH2, EDIT of GS-BCH_b, image_cap 2 (variants a/b; the 2-call cap leaves no retry).
import json, pathlib
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
t = ("GENERATE BURST GS-BCH2 -- Run C-9 Phase 2, new armour sets (Matt R-C9-98, his third look): the freed champion gladiator, "
     "LESS BARE at the hips and thighs, and carrying NO weapon. task_id \"GS-BCH2\".\n\n"
     "IMAGE 1 is his armoured four-view sheet (1024x1536 portrait, 2x2 grid: top-left FRONT, top-right his RIGHT side facing the "
     "viewer's right, bottom-left BACK, bottom-right his LEFT side facing the viewer's left): a huge red-bearded man in a plain gilded "
     "front-and-back chest plate open at the sides, a gilded brimmed helmet, a large lion pauldron and segmented manica on his right "
     "arm, studded leather wrist guards, a broad bronze-plated belt (balteus) with a short skirt of red leather straps edged in gilt, a "
     "white loincloth, bare thighs, linen wraps at the knees and shins, gilded greaves, brown shoes, and a wooden practice sword at his "
     "left hip. IMAGE 2 is his approved base body sheet (the registration master). IMAGE 3 is a STYLE reference ONLY.\n"
     "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1024x1536 sheet: the SAME four views, the SAME grid, the SAME pose. "
     "REGISTRATION IS THE FIRST RULE: in every view his head, hands, shoes and soles stay on EXACTLY the same pixels as in IMAGE 1 and "
     "IMAGE 2 -- the same height, ground lines, positions and scale. Nothing may move, raise, lower or shrink him.\n"
     "KEEP EXACTLY AS IMAGE 1: the helmet, the chest plates, the lion pauldron and manica, the wrist guards, the balteus, the linen "
     "wraps, the greaves, the shoes, his face, beard, hair, braid and skin.\n"
     "CHANGE ONLY THESE:\n"
     "1. LONGER STRAP SKIRT: the red leather straps edged in gilt (pteruges) hanging from the balteus now reach to about MID-THIGH, all "
     "the way round, front, sides and back -- the same straps, the same red and gilt, only longer.\n"
     "2. AN UNDER-LAYER: beneath the strap skirt, close-fitting DARK BROWN LEATHER SHORT BREECHES that cover the hips and thighs down to "
     "just ABOVE THE KNEE, so no bare thigh shows anywhere above the knee wraps, in any view. The loincloth is no longer seen.\n"
     "3. NO WEAPON: REMOVE the wooden practice sword from his left hip entirely. No sword, dagger, scabbard or weapon anywhere on him.\n"
     "Paint in IMAGE 1's hand. Soft even light, no cast shadows, no ground, no text, no labels.\n"
     "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
     "Two image_gen EDIT calls: variants a and b. NO RETRIES (the image budget is fixed): if a variant has a fault, deliver it anyway and "
     "NAME it in concerns -- he moved, rose, sank or changed scale in any view, bare thigh showing above the knee wraps, the strap skirt "
     "not reaching mid-thigh, any weapon left on him, the helmet, chest plates, pauldron or greaves changed, or a view missing or changed "
     "facing. Copy outputs to out/GS-BCH2_a.png and out/GS-BCH2_b.png with sha256. No code. No other files. No web.\n"
     "RETURN: receipt task_id \"GS-BCH2\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE "
     "number of image_gen calls; status; concerns. Never PASS/FAIL.")
task = dict(text=t, references=[
    dict(path=A + 'GS-BCH/GS-BCH_b.png', role="IMAGE 1 -- his armoured sheet to EDIT (GS-BCH variant b, R-C9-98; Matt likes its chest piece, helm and shoulder)"),
    dict(path=A + 'NB-1/NB-1_b.png', role="IMAGE 2 -- his approved base-body sheet (NB-1 variant b, R-C9-70): the registration master only"),
    dict(path=A + 'inputs/nb_style_ref_matt.png', role="IMAGE 3 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose")],
    image_cap=2, minutes_cap=15, tool_call_cap=12, outputs=['out/GS-BCH2_a.png', 'out/GS-BCH2_b.png'], effort='high', add_dirs=[],
    experiment='R-C9-98-gear-sets')
p = BURST / 'briefs/C-9/GS-BCH2.task.json'
assert not p.exists()
p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p)
