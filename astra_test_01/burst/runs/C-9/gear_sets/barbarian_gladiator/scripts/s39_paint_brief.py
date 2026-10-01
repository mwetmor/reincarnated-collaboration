# R-C9-105 paint pass: a paint-sheet brief whose VIEW DESCRIPTION IS GENERATED FROM THE LAYOUT (D7's s7_brief rule: the
# packer orders cells per model, so the row order is read from the rects, never typed).
#   python3 s39_paint_brief.py <layout_name> <canvas.png> <task_id> <body|dressed> <A|B> [<a_canvas_note>]
import json, os, sys
NAME, CANVAS, TID, SUBJ, SHEET = sys.argv[1:6]
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
L = json.load(open(os.path.join(ROOT, "work", "layout_%s.json" % NAME)))
WORD = dict(S="FACING THE VIEWER (south)", N="seen from BEHIND (north)", E="facing the viewer's RIGHT in profile (east)",
            W="facing the viewer's LEFT in profile (west)", SE="facing the lower right (south-east)",
            SW="facing the lower left (south-west)", NE="facing away to the upper right (north-east)",
            NW="facing away to the upper left (north-west)", face_S="a CLOSE-UP of his HEAD from the front",
            face_SE="a CLOSE-UP of his head from the lower right, three-quarter")
cells = L["cells"]; mid = L["canvas"][1] / 2
rows = {"Top": [], "Bottom": []}
for k, c in cells.items():
    x, y, w, h = c["rect"]; rows["Top" if y + h / 2 < mid else "Bottom"].append((x, k))
desc = ["%s row, left to right: %s." % (rn, "; ".join(WORD[k] for _, k in sorted(rows[rn]))) for rn in ("Top", "Bottom")]
A = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts/"
ELEV = "seen from a little above (19.77 degrees)" if SHEET == "A" else "seen from HIGH above (52.95 degrees, the game camera's own angle)"
if SUBJ == "body":
    who = ("IMAGE 2 is his APPROVED champion body sheet: a huge, heavily muscled man with warm, LIGHT, sun-touched skin and "
           "freckles; bright copper-red hair braided close at the sides with one long braid down his back; a full copper-red "
           "beard with a small bronze ring; a knotwork BAND TATTOO in blue-grey ink round his RIGHT upper arm only; a plain "
           "DARK wrapped loincloth; brown leather shoes. Nothing else on him.")
    rules = ("THE COLOURS MUST STAY APART at a small size: LIGHT warm skin; COPPER-RED hair and beard; the DARK brown-grey "
             "loincloth; BROWN shoes. Do not tan the whole figure one colour.\n"
             "THE TATTOO: on his RIGHT upper arm ONLY (in the front view it is on the viewer's LEFT). Never on the left arm.\n"
             "ADD NOTHING he does not wear in IMAGE 2: no armour, no helmet, no belt, no weapon.")
    ref = dict(path=A + "GS-BCHB/GS-BCHB.png", role="IMAGE 2 -- his approved CHAMPION BODY sheet (GS-BCHB, R-C9-105): the look")
else:
    who = ("IMAGE 2 is his APPROVED armour sheet (the freed champion gladiator): over his light, freckled skin and copper-red "
           "hair, braid and beard he wears a POLISHED GILDED BRONZE brimmed helmet; a plain GILDED front-and-back chest plate on "
           "CRIMSON-RED leather shoulder straps; a large gilded LION pauldron and a segmented gilded manica on his RIGHT arm; "
           "studded DARK-BROWN leather wrist guards; a wide riveted gilded girdle with a LION-FACE plaque on a crimson-red band; "
           "a TAWNY lion-pelt kilt, darker in its streaks and ragged at the hem; CREAM linen wraps at the knees and shins; "
           "gilded greaves on crimson-red straps; brown shoes.")
    rules = ("THE COLOURS MUST STAY APART at a small size -- this is the reason for this painting: BRIGHT YELLOW GOLD with "
             "darker bronze in the recesses for every metal piece; CRIMSON RED for every strap and band; TAWNY-BROWN fur with "
             "dark streaks for the kilt; CREAM-WHITE linen for the wraps; LIGHT warm skin where he is bare (his left arm, his "
             "flanks between the plates, his face, his thighs above the wraps); COPPER-RED hair and beard. Gold, skin and fur "
             "must never merge into one tan.\n"
             "THE LION PAULDRON AND MANICA are on his RIGHT arm ONLY (in the front view, on the viewer's LEFT). His LEFT arm is "
             "bare skin.\n"
             "ADD NOTHING IMAGE 2 does not show: no weapon, no cape, no plume.")
    ref = dict(path=A + "GS-BCH4/GS-BCH4.png", role="IMAGE 2 -- his approved armour sheet (GS-BCH4, Matt's pick R-C9-105): the look")
canvas_kind = ("renders of ONE 3D model of a man standing in an A-pose, %s, on flat pure #00ff00. %s They are renders of the "
               "model: every OUTLINE, POSE, POSITION and SIZE is correct and must not change; the surface colour is the 3D "
               "model's own flat, muddy texture." % (ELEV, " ".join(desc)))
if SHEET == "B":
    canvas_kind += (" They ALREADY CARRY the first painting of him (from a lower camera), projected onto the model: keep every "
                    "feature where it already is and REFINE it -- the tops of the helmet, shoulders, plates and fur that a low "
                    "camera only grazed get the most new detail. Do not move or re-invent a feature the canvas already shows.")
text = ("GENERATE BURST {tid} -- Run C-9 Phase 2 (Matt R-C9-105): the PAINTED TEXTURE of the freed champion, {sub}, sheet {sh}. "
        "task_id \"{tid}\".\n\n"
        "IMAGE 1 is a sheet of TEN {ck}\n{who} IMAGE 3 is a STYLE reference ONLY: copy its HAND (the warm dark-brown ink line that "
        "varies in weight, transparent watercolour washes that pool and granulate, fine hatching in the shadows, cream paper "
        "highlights); copy nothing else from it.\n"
        "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE {cw}x{ch} sheet in which EVERY figure is repainted as the man of "
        "IMAGE 2 seen from that direction, in IMAGE 3's hand, inside exactly that view's outline, position and size.\n"
        "THIS PAINTING BECOMES THE MODEL'S TEXTURE: it is projected back onto the 3D model from these ten cameras and blended. So:\n"
        "1. ONE man in ten views, not ten men: the same colours and the same details in every view. Any disagreement becomes a seam.\n"
        "2. Paint the SURFACE, not the lighting: soft even light; no cast shadows, no dark side, no rim light. Tone comes from "
        "his own colours and the pen hatching.\n"
        "3. Stay inside the outlines: do not paint beyond a silhouette or change any outline, pose, hand or foot.\n"
        "{rules}\n"
        "THE TWO HEAD CLOSE-UPS are his identity: the same face as IMAGE 2, larger. More detail is welcome; a different face is not.\n\n"
        "BACKGROUND: keep it flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver "
        "the image: the figures are cut out by their exact 3D outlines.\n\n"
        "Two image_gen EDIT calls: variants a and b. ONE retry per variant only if a view's outline, pose, facing or position "
        "changed, a view is missing, the man differs between views, the colours merged into one tan, a piece is on the wrong arm, "
        "or a head close-up is a different face -- name the reason. Never retry for the background colour. Copy outputs to "
        "out/{tid}_a.png and out/{tid}_b.png with sha256. No code. No other files. No web.\n"
        "RETURN: receipt task_id \"{tid}\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = "
        "the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.").format(
    tid=TID, sub=("the bare champion body" if SUBJ == "body" else "his champion armour set"), sh=("1 of 2" if SHEET == "A" else "2 of 2"),
    ck=canvas_kind, who=who, rules=rules, cw=L["canvas"][0], ch=L["canvas"][1])
task = dict(text=text, references=[
    dict(path=CANVAS, role="IMAGE 1 -- the sheet to EDIT (%s; 8 body views + 2 head close-ups of the 3D model at rest)" % ELEV),
    ref, dict(path=A + "inputs/nb_style_ref_matt.png", role="IMAGE 3 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand")],
    image_cap=4, minutes_cap=15, tool_call_cap=20, outputs=["out/%s_a.png" % TID, "out/%s_b.png" % TID], effort="high",
    add_dirs=[], experiment="R-C9-105-paint")
OUT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/briefs/C-9/%s.task.json" % TID
assert not os.path.exists(OUT), OUT
json.dump(task, open(OUT, "w"), indent=1)
print("wrote", OUT, len(text), "chars;", " | ".join(desc))
