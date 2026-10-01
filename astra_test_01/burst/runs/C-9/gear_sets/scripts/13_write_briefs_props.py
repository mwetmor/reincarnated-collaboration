# R-C9-119 (Matt, the battle mage's props): two model sheets for 3D, 2 calls each, no retries.
#   GS-SWAND2  the battle wand rebuilt bigger: ~0.52 m, shaft ~2.5 cm, crystal head ~6.5 cm, a proper grip and pommel,
#              in the battle mage's GOLD and STEEL (EDIT of GS-SWAND_a, so the design family is kept)
#   GS-SBOOK2  the grimoire OPEN as a spell-weapon, ~155 deg between the covers, painted spell glyphs with a faint ember glow
#              (EDIT of GS-SBOOK_a, so the covers are the same book)
import json, pathlib
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
STYLE = dict(path=A + 'inputs/nb_style_ref_matt.png', role="IMAGE 3 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose")
LOOK = dict(path=A + 'GS-SHOOD/GS-SHOOD.png', role="IMAGE 2 -- her battle-mage set (GS-SHOOD, Matt's pick): the steel, the gold borders and the ember red to match")
tail = lambda tid, faults: (
    "Paint in IMAGE 3's hand (dark ink line, transparent washes, hatching), matched to IMAGE 2. Soft even light, only the ember "
    "crystal glows faintly, no cast shadows, no ground, no text, no labels.\n"
    "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
    "Two image_gen EDIT calls: variants a and b. NO RETRIES: if a variant has a fault, deliver it anyway and NAME it in concerns -- "
    f"{faults}, a view missing, the object differing between views, a hand or person appearing, or text appearing. Copy outputs to "
    f"out/{tid}_a.png and out/{tid}_b.png with sha256. No code. No other files. No web.\n"
    f"RETURN: receipt task_id \"{tid}\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE "
    "number of image_gen calls; status; concerns. Never PASS/FAIL.")
T = {}
T['GS-SWAND2'] = dict(text=(
    "GENERATE BURST GS-SWAND2 -- Run C-9 Phase 2 (Matt R-C9-119): the battle mage's WAND, REBUILT LARGER, as a MODEL SHEET for 3D. "
    "task_id \"GS-SWAND2\".\n\n"
    "IMAGE 1 is the wand's earlier three-view sheet (ONE wand, three views side by side: front, turned 90 degrees, turned 180 "
    "degrees, crystal at the top). In her hand it read like a needle: too thin, too short, its crystal too small. IMAGE 2 is her "
    "battle-mage armour, for the metals and colours. IMAGE 3 is a STYLE reference ONLY.\n"
    "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 sheet on flat pure #00ff00: the SAME three views in the SAME "
    "order, side by side, at ONE common scale, the butt of each on one ground line near the bottom edge, the crystal near the top "
    "edge, nothing overlapping. THE NEW WAND -- a short battle-mage's WAND, NOT a staff -- about 52 cm long:\n"
    "- a STOUT shaft of polished STEEL, about 2.5 cm thick (the whole wand only about 21 times as long as it is thick), banded with "
    "GOLD rings and fine ember-red runes etched along it;\n"
    "- a proper GRIP at the bottom about 12 cm long, wrapped in dark leather between two GOLD collars, ending in a heavy GOLD POMMEL "
    "about 4 cm across;\n"
    "- at the top a GOLD claw-setting holding a LARGE faceted EMBER CRYSTAL, orange-red with a faint inner glow, about 6.5 cm tall "
    "and 4 cm wide (the whole wand about 8 times as long as the crystal is tall).\n"
    "In sizes on the 1024-pixel-tall sheet: the whole wand about 930 px tall, the shaft about 45 px thick, the crystal about 115 px "
    "tall and 70 px wide, the grip about 215 px long.\n"
    + tail('GS-SWAND2', "the wand thinner than about 35 px or shorter than about 850 px, the crystal smaller than about 90 px tall, "
                        "a staff (longer than an arm)")),
    references=[dict(path=A + 'GS-SWAND/GS-SWAND_a.png', role="IMAGE 1 -- the wand's earlier sheet to EDIT (GS-SWAND_a): keep its design family, rebuild it larger"),
                LOOK, STYLE])
T['GS-SBOOK2'] = dict(text=(
    "GENERATE BURST GS-SBOOK2 -- Run C-9 Phase 2 (Matt R-C9-119): the battle mage's GRIMOIRE held OPEN as a spell-weapon, as a "
    "MODEL SHEET for 3D. task_id \"GS-SBOOK2\".\n\n"
    "IMAGE 1 is the grimoire's earlier four-view sheet, CLOSED: oxblood leather covers bound in blackened steel corners, a steel "
    "spine band, a steel boss with an ember crystal on the front cover, cream page edges. IMAGE 2 is her battle-mage armour, for "
    "the style. IMAGE 3 is a STYLE reference ONLY.\n"
    "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 sheet on flat pure #00ff00 showing the SAME BOOK, now OPEN, "
    "alone (no hands, no stand, no person), in FOUR orthographic views in ONE row, at ONE common scale, their bottoms on one ground "
    "line, nothing overlapping. THE OPEN GRIMOIRE: the two covers and the page block splayed wide, about 155 degrees between the "
    "covers (almost flat, a shallow V), each cover about 26 cm tall and 20 cm wide, the whole open book about 42 cm across; the "
    "pages thick and cream, slightly curved up from the spine; both open pages painted with dark-ink SPELL GLYPHS, circles and runes, "
    "a few of them in ember red with a FAINT warm glow; one cloth ribbon marker. Its covers and steel fittings are IMAGE 1's.\n"
    "THE FOUR VIEWS, the book standing upright on its bottom edge with its SPINE VERTICAL at the centre:\n"
    "FIRST (left): the OPEN PAGES face-on, the spine vertical in the middle, both pages fully visible, about 42 cm wide;\n"
    "SECOND: turned 90 degrees -- the book EDGE-ON from its left side: the shallow V of the open covers seen from the side, narrow;\n"
    "THIRD: turned 180 degrees -- the OUTSIDE of both covers face-on, the steel spine band vertical in the middle;\n"
    "FOURTH (right): turned 270 degrees -- edge-on from its right side, the mirror of the second.\n"
    + tail('GS-SBOOK2', "the book closed or opened less than about 130 degrees, blank pages, the covers different from IMAGE 1")),
    references=[dict(path=A + 'GS-SBOOK/GS-SBOOK_a.png', role="IMAGE 1 -- the grimoire's earlier closed sheet to EDIT (GS-SBOOK_a): the same book, open"),
                LOOK, STYLE])
for tid, t in T.items():
    task = dict(text=t['text'], references=t['references'], image_cap=2, minutes_cap=15, tool_call_cap=12,
                outputs=[f'out/{tid}_a.png', f'out/{tid}_b.png'], effort='high', add_dirs=[], experiment='R-C9-119-props')
    p = BURST / 'briefs/C-9' / f'{tid}.task.json'
    assert not p.exists(), p
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p)
