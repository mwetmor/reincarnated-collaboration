# R-C9-105 (barbarian stage 2): the CHAMPION BODY sheet -- an EDIT of Matt's pick GS-BCH4 that REMOVES every armour piece,
# so the bare body (bare legs, loincloth, shoes) can be built and the armour isolated against it, D2's way. Registered by
# construction. image_cap 2 = one call + one retry ONLY on drift.
import json, pathlib
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
t = ("GENERATE BURST GS-BCHB -- Run C-9 Phase 2 (Matt R-C9-105, the champion's armour build): his CHAMPION BODY with the armour "
     "TAKEN OFF, as the base model sheet the armour will be fitted onto. task_id \"GS-BCHB\".\n\n"
     "IMAGE 1 is his armoured four-view sheet (1024x1536 portrait, 2x2 grid: top-left FRONT, top-right his RIGHT side facing the "
     "viewer's right, bottom-left BACK, bottom-right his LEFT side facing the viewer's left). IMAGE 2 is his approved base body "
     "sheet: his bare torso, arms and the knotwork tattoo on his RIGHT upper arm. IMAGE 3 is a STYLE reference ONLY.\n"
     "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1024x1536 sheet: the SAME four views, the SAME grid, the SAME pose. "
     "REGISTRATION IS THE FIRST RULE: in every view his head, hands, shoes and soles stay on EXACTLY the same pixels as in IMAGE 1 "
     "-- the same height, ground lines, positions and scale.\n"
     "REMOVE EVERY ARMOUR PIECE, showing the man beneath exactly where it was: the helmet (his braided red hair and the top of his "
     "head as in IMAGE 2), the chest plates and their straps (his bare chest, belly and back as in IMAGE 2), the lion pauldron and "
     "segmented manica (his bare right arm with the knotwork band tattoo as in IMAGE 2), the leather wrist guards (bare wrists), the "
     "girdle with the lion plaque and the lion-pelt kilt, the linen leg wraps and the greaves (his BARE muscled thighs, knees and "
     "calves).\n"
     "KEEP: his face, beard and ring, hair and braid, skin, his brown SHOES, and a plain dark wrapped LOINCLOTH at the hips, with a "
     "simple narrow dark cloth band at the waist holding it -- nothing else on him. Not nude in any view.\n"
     "Paint in IMAGE 1's hand. Soft even light, no cast shadows, no ground, no text, no labels.\n"
     "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
     "ONE image_gen EDIT call. ONE RETRY ONLY if the result DRIFTS: he moved, rose, sank or changed scale in any view (compare the "
     "soles and the crown with IMAGE 1), or his pose or limbs changed -- name the reason and deliver BOTH images. NAME any other fault "
     "in concerns (an armour piece left on him, the tattoo missing, bare groin). Copy the output to out/GS-BCHB.png (a retry to "
     "out/GS-BCHB_r1.png) with sha256. No code. No other files. No web.\n"
     "RETURN: receipt task_id \"GS-BCHB\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the "
     "TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
task = dict(text=t, references=[
    dict(path=A + 'GS-BCH4/GS-BCH4.png', role="IMAGE 1 -- Matt's pick (GS-BCH4, R-C9-105): the armoured sheet to EDIT; take every armour piece off"),
    dict(path=A + 'NB-1/NB-1_b.png', role="IMAGE 2 -- his approved base-body sheet (NB-1 variant b, R-C9-70): his bare torso, arms and tattoo"),
    dict(path=A + 'inputs/nb_style_ref_matt.png', role="IMAGE 3 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose")],
    image_cap=2, minutes_cap=15, tool_call_cap=12, outputs=['out/GS-BCHB.png'], effort='high', add_dirs=[],
    experiment='R-C9-105-gear-sets')
p = BURST / 'briefs/C-9/GS-BCHB.task.json'
assert not p.exists()
p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p)
