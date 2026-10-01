# E1 base body: an EDIT of the chosen armoured sheet that REMOVES the four modular pieces (helm, pauldrons, breastplate+backplate,
# cape) -- registered by construction (GS-BCHB's method). Plus, for A1, an EDIT removing ONLY the cape (the chest/pauldron
# backs the long cape hides in the full build).  python3 e05_brief_base.py <DK-A1|DK-A2> <sheet path>
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent)); import importlib; B = importlib.import_module('e01_briefs_A')
tid_src, sheet = sys.argv[1], sys.argv[2]
REF1 = dict(path=sheet, role="IMAGE 1 -- the knight's approved armoured four-view sheet (%s) to EDIT" % tid_src)
STY = dict(B.STYLE, role="IMAGE 2 -- " + B.STYLE['role'])
HEAD = ("IMAGE 1 is his armoured four-view sheet (1024x1536 portrait, 2x2 grid: top-left FRONT, top-right his RIGHT side facing the viewer's right, "
        "bottom-left BACK, bottom-right his LEFT side facing the viewer's left). IMAGE 2 is a STYLE reference ONLY.\n"
        "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1024x1536 sheet: the SAME four views, the SAME grid, the SAME pose. "
        "REGISTRATION IS THE FIRST RULE: in every view his hands, feet, soles, legs and arms stay on EXACTLY the same pixels as in IMAGE 1 -- the same "
        "height, ground lines, positions and scale.\n")
TAIL = ("Paint in IMAGE 1's own hand and colours. Soft even light, no cast shadows, no ground, no text, no labels.\n"
        "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
        "ONE image_gen EDIT call. ONE RETRY ONLY if the result DRIFTS: he moved, rose, sank or changed scale in any view (compare the soles and hands with "
        "IMAGE 1), his pose or limbs changed, or a piece named above is left on -- name the reason and deliver BOTH images. Copy the output to out/%s.png "
        "(a retry to out/%s_r1.png) with sha256. No code. No other files. No web.\n"
        "RETURN: receipt task_id \"%s\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen "
        "calls; status; concerns. Never PASS/FAIL.")
base = ("GENERATE BURST DK-BASE -- Run C-9 Phase 2 (Matt R-C9-112/113): the dark knight's BASE BODY, with four armour pieces TAKEN OFF, as the base model "
        "sheet those pieces will be fitted back onto. task_id \"DK-BASE\".\n\n" + HEAD +
        "REMOVE exactly these four pieces, showing what he wears beneath exactly where they were:\n"
        "- the HELM with its horns and visor: beneath it, his HEAD -- a pale, gaunt, stern man of about forty, close-cropped black hair, clean-shaven, "
        "mouth closed, eyes open looking straight ahead; a plain near-black padded collar at his throat. The head is SMALL for his height, as the sheet's "
        "proportions require (he is about eight and a half heads tall);\n"
        "- both PAULDRONS: beneath them, the rounded shoulders of a near-black quilted ARMING DOUBLET;\n"
        "- the BREASTPLATE and BACKPLATE: beneath them, the same near-black quilted arming doublet over the chest, belly and back, fitted close to the body, "
        "with fine violet stitching; KEEP the belt where it is;\n"
        "- the CAPE: gone completely, front, sides and back (nothing hangs behind him).\n"
        "KEEP, unchanged: the arm plates and articulated gauntlets, the broad GOLD filigree band on his LEFT forearm only, the plated fauld and tassets over "
        "the hips, the leg plates and pointed sabatons, the belt.\n" + TAIL % ("DK-BASE", "DK-BASE", "DK-BASE"))
nocape = ("GENERATE BURST DK-NOCAPE -- Run C-9 Phase 2 (Matt R-C9-112/113): the dark knight with ONLY his CAPE taken off, so the backplate and pauldron "
          "backs it hides can be built. task_id \"DK-NOCAPE\".\n\n" + HEAD +
          "REMOVE the CAPE completely -- front, sides and back; nothing hangs behind him -- and show beneath it the rest of his armour exactly as it continues: "
          "the BACKPLATE (near-black steel with violet sheen and fine gold filigree, matching the breastplate), the backs of the pauldrons, the backs of the "
          "fauld and leg plates. CHANGE NOTHING ELSE: helm, horns, visor, pauldrons, breastplate, arms, gauntlets, the gold band on his LEFT forearm, legs and "
          "sabatons stay exactly as in IMAGE 1.\n" + TAIL % ("DK-NOCAPE", "DK-NOCAPE", "DK-NOCAPE"))
for tid, text in (('DK-BASE', base), ('DK-NOCAPE', nocape)):
    if tid == 'DK-NOCAPE' and tid_src != 'DK-A1':
        continue
    B.lane_guard(text)
    task = dict(text=text, references=[REF1, STY], image_cap=2, minutes_cap=15, tool_call_cap=12, outputs=['out/%s.png' % tid], effort='high',
                add_dirs=[], experiment='R-C9-112-third-character')
    p = B.BURST / ('briefs/C-9/%s.task.json' % tid); assert not p.exists(), p
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p)
