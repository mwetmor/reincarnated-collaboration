# so_mx R-C9-133/134 (Matt): the arena battle mage's two props, model sheets for 3D, 2 image calls each, no retries.
#   GS-SORBST  a SHORT STAFF ~0.75 m with a glowing fire-orange crystal ORB (~13 cm) in a gold cradle on top (EDIT of
#              GS-SWAND2_a, the wand she had, so the gold-and-steel design family carries over)
#   GS-SSHLD   a large ornate STEEL shield, tall with a gentle point at the base, gold trim, faint runes; front / edge / back
#              with a CENTRE GRIP (EDIT of NB-W1_a for the three-view layout ONLY -- a different shield entirely)
import json, pathlib
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
STYLE = dict(path=A + 'inputs/nb_style_ref_matt.png', role="IMAGE 3 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose")
LOOK = dict(path=A + 'GS-SHOOD/GS-SHOOD.png', role="IMAGE 2 -- her battle-mage set (GS-SHOOD, Matt's pick): the steel, the gold borders and the ember red to match")
tail = lambda tid, faults: (
    "Paint in IMAGE 3's hand (dark ink line, transparent washes, hatching), matched to IMAGE 2. Soft even light, only the ember "
    "crystal glows, no cast shadows, no ground, no text, no labels.\n"
    "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
    "Two image_gen EDIT calls: variants a and b. NO RETRIES: if a variant has a fault, deliver it anyway and NAME it in concerns -- "
    f"{faults}, a view missing, the object differing between views, a hand or person appearing, or text appearing. Copy outputs to "
    f"out/{tid}_a.png and out/{tid}_b.png with sha256. No code. No other files. No web.\n"
    f"RETURN: receipt task_id \"{tid}\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE "
    "number of image_gen calls; status; concerns. Never PASS/FAIL.")
T = {}
T['GS-SORBST'] = dict(text=(
    "GENERATE BURST GS-SORBST -- Run C-9 Phase 2 (Matt R-C9-134): the battle mage's ORB STAFF, a short one-handed staff, as a "
    "MODEL SHEET for 3D. task_id \"GS-SORBST\".\n\n"
    "IMAGE 1 is her earlier WAND's three-view sheet (one wand, three views side by side: front, turned 90 degrees, turned 180 "
    "degrees, crystal at the top): keep its design family -- the polished steel, the gold bands and collars, the leather grip, the "
    "gold claw-work. IMAGE 2 is her battle-mage armour, for the metals and colours. IMAGE 3 is a STYLE reference ONLY.\n"
    "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 sheet on flat pure #00ff00: the SAME three views in the SAME "
    "order, side by side, at ONE common scale, the butt of each on one ground line near the bottom edge, the orb near the top edge, "
    "nothing overlapping. THE NEW OBJECT -- a SHORT STAFF held in one hand, about 75 cm long:\n"
    "- an ornate SHAFT of polished STEEL about 3 cm thick, banded with GOLD rings and fine ember-red runes, with a dark leather GRIP "
    "about 14 cm long between two GOLD collars at the lower third, and a small GOLD butt-cap at the bottom;\n"
    "- at the top an ornate GOLD-AND-STEEL CRADLE of four curved claws holding a round glowing FIRE-ORANGE CRYSTAL ORB about 13 cm "
    "across, bright orange at its core shading to deep red at its edge, with a soft inner glow;\n"
    "- the orb sits centred on the shaft's axis, the cradle about 6 cm tall below it.\n"
    "In sizes on the 1024-pixel-tall sheet: the whole staff about 940 px tall, the shaft about 38 px thick, the orb about 165 px "
    "across, the grip about 175 px long.\n"
    + tail('GS-SORBST', "the staff shorter than about 850 px, the orb smaller than about 130 px or not round, the orb off the shaft's "
                        "axis, a long staff (taller than a person)")),
    references=[dict(path=A + 'GS-SWAND2/GS-SWAND2_a.png', role="IMAGE 1 -- her earlier wand sheet to EDIT (GS-SWAND2_a): keep its design family, rebuild it as a short orb staff"),
                LOOK, STYLE])
T['GS-SSHLD'] = dict(text=(
    "GENERATE BURST GS-SSHLD -- Run C-9 Phase 2 (Matt R-C9-133): the battle mage's SHIELD, as a MODEL SHEET for 3D. task_id "
    "\"GS-SSHLD\".\n\n"
    "IMAGE 1 is an earlier weapons sheet: use ONLY its LOWER ROW'S LAYOUT -- one shield in three views side by side (the FRONT face, "
    "the EDGE seen from the side, the BACK with its grip) -- and NOTHING of its objects: no axe, no wood, no round shield, no red "
    "and white. IMAGE 2 is her battle-mage armour, for the metals, the gold borders and the ember red. IMAGE 3 is a STYLE reference "
    "ONLY.\n"
    "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 sheet on flat pure #00ff00 with ONE shield in exactly THREE "
    "views in ONE row, at ONE common scale, each standing upright with its point at the bottom, nothing overlapping, no axe and "
    "nothing else on the sheet. THE SHIELD -- a LARGE ornate STEEL shield about 80 cm tall and 55 cm wide:\n"
    "- TALL, its sides gently convex, its top edge gently arched, narrowing at the base to a GENTLE POINT;\n"
    "- the face polished STEEL, slightly curved (convex), with a raised GOLD TRIM border about 4 cm wide all round, a central "
    "raised steel boss with a gold rim, and FAINT ember-red RUNES etched in a ring around the boss;\n"
    "- FIRST view (left): the FRONT face-on; SECOND (middle): the EDGE from the side -- a narrow shallow curve about 7 cm deep, the "
    "boss bulging forward; THIRD (right): the BACK face-on -- plain darker steel with a gold-trimmed rim, a single horizontal "
    "leather-wrapped GRIP bar across the CENTRE (behind the boss) and, above it, a leather FOREARM STRAP.\n"
    "In sizes on the 1024-pixel-tall sheet: each face view about 900 px tall and 620 px wide; the edge view about 900 px tall.\n"
    + tail('GS-SSHLD', "a round or square shield, wood, the axe or any IMAGE 1 object kept, the grip not across the centre, the "
                       "shield shorter than about 800 px")),
    references=[dict(path=A + 'NB-W1/NB-W1_a.png', role="IMAGE 1 -- the LAYOUT ONLY of its lower row (front / edge / back of one shield); none of its objects"),
                LOOK, STYLE])
for tid, t in T.items():
    task = dict(text=t['text'], references=t['references'], image_cap=2, minutes_cap=15, tool_call_cap=12,
                outputs=[f'out/{tid}_a.png', f'out/{tid}_b.png'], effort='high', add_dirs=[], experiment='R-C9-134-props')
    p = BURST / 'briefs/C-9' / f'{tid}.task.json'
    assert not p.exists(), p
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p)
