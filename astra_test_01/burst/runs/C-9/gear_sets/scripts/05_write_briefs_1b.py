# R-C9-98 stage 1b (Matt's look at GS-BGL / GS-BMAULL): two briefs, image_cap 2 each (4 calls; 2 held for a retry).
#   GS-BCH    the CHAMPION BODY + set v2: an EDIT of NB-1_b that REPLACES the trousers (bare legs, fasciae, subligaculum)
#             and dresses him in the revised set (no plume; lion pauldron; plain fitted front+back plates open at the sides).
#             REGISTRATION is the first rule: GS-BGL drifted 22-34 px (the plume wanted headroom; the plume is gone).
#   GS-BMAUL2 the great maul v2: an EDIT of GS-BMAULL, more ornate, a larger head, still a two-hander.
import json, pathlib
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
STYLE_ROLE = "STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose"

bch = (
    "GENERATE BURST GS-BCH -- Run C-9 Phase 2, new armour sets (Matt R-C9-98, his second look): the barbarian as the FREED CHAMPION "
    "GLADIATOR, on a CHAMPION BODY with bare legs. task_id \"GS-BCH\".\n\n"
    "IMAGE 1 is his APPROVED four-view sheet (1024x1536 portrait, 2x2 grid: top-left FRONT, top-right his RIGHT side facing the viewer's "
    "right, bottom-left BACK, bottom-right his LEFT side facing the viewer's left): a huge red-bearded man, bare-chested, braided red "
    "hair with one long braid down his back, a beard ring, a knotwork band tattoo on his RIGHT upper arm, baggy blue trousers, cream leg "
    "wraps, brown shoes. IMAGE 2 is an earlier draft of this armour, for the LOOK of the pieces named 'as IMAGE 2' below ONLY -- never "
    "its position, size or placement on the sheet (it drifted). IMAGE 3 is a STYLE reference ONLY.\n"
    "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1024x1536 sheet: the SAME four views, the SAME grid, the SAME pose. "
    "REGISTRATION IS THE FIRST RULE: in every view his head, hands, shoes and soles stay on EXACTLY the same pixels as in IMAGE 1 -- "
    "the same height, the same ground lines, the same positions, the same scale. A 3D body and armour will be built from these four "
    "views and fitted onto his existing 3D body, so NOTHING may move him, raise him, lower him or shrink him. Keep his face, beard and "
    "ring, hair and braid, skin, muscles and shoes exactly.\n"
    "CHANGE HIS LEGS (this is a new body, not armour): REMOVE the baggy blue trousers and the cream leg wraps entirely. In their place, "
    "his BARE, heavily muscled legs (thighs, knees and calves, the same skin as his arms), with padded linen FASCIAE (wrappings) bound "
    "round the knees and shins, and a white linen SUBLIGACULUM (loincloth) at the hips, under the belt. The legs stand exactly where the "
    "trousers stood and meet the same shoes.\n"
    "THE ARMOUR, over that body (gilded bronze, polished, made to awe):\n"
    "- HELM: a gilded GALEA with NO crest, NO plume, NO horsehair -- instead made more ornate and impressive in the metal itself: rich "
    "embossed relief over the bowl, a BROAD BRIM, and SCULPTED CHEEK GUARDS swept back so his WHOLE FACE stays open (eyes, nose, mouth, "
    "beard visible); his long braid still hangs down his back below it;\n"
    "- PAULDRON and MANICA: on his RIGHT arm only (his weapon arm), the segmented gilded MANICA from the shoulder to the wrist as IMAGE 2, "
    "crowned by a LARGE shoulder guard (pauldron) with a LION'S FACE carved into it, jutting out in bold relief from the shoulder; his "
    "LEFT arm stays bare;\n"
    "- CHEST PIECE: a real METAL chest piece -- a FRONT PLATE and a BACK PLATE only, buckled together over the shoulders and OPEN AT THE "
    "SIDES (his flanks and the sides of his ribs bare) so that movement is paramount. Each plate is shaped TIGHTLY to his own "
    "musculature -- the pectorals, the abdomen, the shoulder blades -- as if made for him, covering the chest and belly (front) and the "
    "back (back) far more than a round disc does. PLAIN polished gilded bronze matching the set: NO symbols, NO emblems, NO medallion, "
    "NO engraving, NO ornament on the plates;\n"
    "- KEEP as IMAGE 2: the BROAD BALTEUS (bronze plates over a red leather band) and the short skirt of red leather straps edged in gilt "
    "hanging from it front and back (over the loincloth); the LEATHER WRIST GUARDS with gilded studs on both wrists; and the gilded "
    "GREAVES over his shins, now strapped over the linen fasciae;\n"
    "- a RUDIS at his LEFT hip, tucked in the balteus: a plain WOODEN training sword, bare brown wood, NO scabbard, NO metal, NO gilding.\n"
    "Paint in IMAGE 1's hand (the STYLE reference's ink line, washes and hatching). Soft even light, no cast shadows, no ground, no text, "
    "no labels.\n"
    "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
    "Two image_gen EDIT calls: variants a and b. NO RETRIES (the image budget is fixed): if a variant has a fault, deliver it anyway and "
    "NAME the fault in concerns -- he moved, rose, sank or changed scale in any view (compare the soles and the crown with IMAGE 1), a "
    "view missing or changed facing, any trouser or blue cloth left on his legs, a plume or crest on the helmet, his face covered, any "
    "symbol or ornament on the chest plates, the chest piece closed at the sides, the lion pauldron on the wrong arm, or the rudis not "
    "plain wood. Copy outputs to out/GS-BCH_a.png and out/GS-BCH_b.png with sha256. No code. No other files. No web.\n"
    "RETURN: receipt task_id \"GS-BCH\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE "
    "number of image_gen calls; status; concerns. Never PASS/FAIL.")

maul = (
    "GENERATE BURST GS-BMAUL2 -- Run C-9 Phase 2 (Matt R-C9-98, his second look): the champion's two-handed GREAT MAUL, MORE ORNATE and "
    "with a LARGER HEAD. task_id \"GS-BMAUL2\".\n\n"
    "IMAGE 1 is the maul's current three-view model sheet for 3D: ONE war maul in THREE orthographic views side by side, head at the top "
    "-- LEFT the broad side, MIDDLE turned 90 degrees (a striking face toward the viewer), RIGHT the other broad side.\n"
    "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 sheet, the SAME three views in the SAME order side by side, at ONE "
    "common scale, the butts on one ground line near the bottom edge, the tops near the top edge, nothing overlapping:\n"
    "- A LARGER HEAD: the same heavy rectangular iron block with bevelled ends and a flat striking face at each end, now BIGGER -- about "
    "360 pixels long and 150 pixels tall in the broad-side views (it is about 300 by 118 now), about 150 pixels square in the middle view.\n"
    "- MORE ORNATE, as a champion's weapon made to awe: on each broad side of the head a gilded bronze LION'S HEAD in bold relief at the "
    "centre where the haft passes through, flanked by gilded LAUREL branches; broad gilded bronze bands with fine embossed borders round "
    "each end of the head; gilded bronze LANGETS running down the haft below the head; gilded collars on the grip sections; and a gilded "
    "bronze butt cap shaped as a knob of laurel leaves.\n"
    "- THE HAFT STAYS a slim two-handed haft: the SAME thickness as now (about 40 pixels), the SAME dark wood, the SAME TWO leather-"
    "wrapped grip sections (one at the butt, one at mid-haft, each about 145 pixels long); from the underside of the head down to the butt "
    "about 2.3 head-lengths. The whole maul about 980 pixels tall.\n"
    "Paint in IMAGE 1's own hand and colours. Soft even light, no glow, no cast shadows, no ground, no text, no labels. No hand, no "
    "person, no strap.\n"
    "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
    "Two image_gen EDIT calls: variants a and b. NO RETRIES (the image budget is fixed): if a variant has a fault, deliver it anyway and "
    "NAME it in concerns -- the head NOT larger than IMAGE 1's, the haft thicker than now, the haft below the head shorter than two "
    "head-lengths, a spike or blade added, a view missing, the views disagreeing, or a hand, person or text appearing. Copy outputs to "
    "out/GS-BMAUL2_a.png and out/GS-BMAUL2_b.png with sha256. No code. No other files. No web.\n"
    "RETURN: receipt task_id \"GS-BMAUL2\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE "
    "number of image_gen calls; status; concerns. Never PASS/FAIL.")

T = {
    'GS-BCH': dict(text=bch, references=[
        dict(path=A + 'NB-1/NB-1_b.png', role="IMAGE 1 -- the approved base-body sheet to EDIT (NB-1 variant b, R-C9-70; the D2 base): the registration master"),
        dict(path=A + 'GS-BGL/GS-BGL_a.png', role="IMAGE 2 -- the first draft of this set (GS-BGL variant a, R-C9-98): the look of the balteus, strap skirt, wrist guards, greaves and manica ONLY; never its position or scale"),
        dict(path=A + 'inputs/nb_style_ref_matt.png', role="IMAGE 3 -- " + STYLE_ROLE)]),
    'GS-BMAUL2': dict(text=maul, references=[
        dict(path=A + 'GS-BMAULL/GS-BMAULL.png', role="IMAGE 1 -- the maul's current three-view sheet to EDIT (GS-BMAULL, R-C9-98): larger head, more ornate, same slim haft")]),
}
for tid, t in T.items():
    task = dict(text=t['text'], references=t['references'], image_cap=2, minutes_cap=15, tool_call_cap=12,
                outputs=[f'out/{tid}_a.png', f'out/{tid}_b.png'], effort='high', add_dirs=[], experiment='R-C9-98-gear-sets')
    p = BURST / 'briefs/C-9' / f'{tid}.task.json'
    assert not p.exists(), f'{p} exists; never overwrite'
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n')
    print('wrote', p)
