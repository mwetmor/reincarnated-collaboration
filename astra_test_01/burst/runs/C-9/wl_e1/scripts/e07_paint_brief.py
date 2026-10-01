# E1 painted-texture briefs (D7's SOP-A / SOP-B, for the dark knight's BASE body). View words are GENERATED from the
# layout rects (the T8 lesson: never typed by hand). Stages the canvas into CS9-guides + its manifest (refs_guard rule).
#   python3 e07_paint_brief.py A <canvas.png>            -> DK-PA
#   python3 e07_paint_brief.py B <canvas.png> <A_paint>  -> DK-PB
import json, sys, os, hashlib, shutil, pathlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); import importlib; B = importlib.import_module('e01_briefs_A')
NAME, CANVAS = sys.argv[1], sys.argv[2]
L = json.load(open(os.path.join(ROOT, "work", "layout_%s.json" % NAME)))
WORD = dict(S="FACING THE VIEWER (south)", N="seen from BEHIND (north)", E="facing the viewer's RIGHT in profile (east)",
            W="facing the viewer's LEFT in profile (west)", SE="facing the lower right (south-east)", SW="facing the lower left (south-west)",
            NE="facing away to the upper right (north-east)", NW="facing away to the upper left (north-west)",
            face_S="a CLOSE-UP of his FACE from the front", face_SE="a CLOSE-UP of his face from the lower right, three-quarter")
mid = L["canvas"][1] / 2; rows = {"Top": [], "Bottom": []}
for k, c in L["cells"].items():
    x, y, w, h = c["rect"]; rows["Top" if y + h / 2 < mid else "Bottom"].append((x, k))
desc = " ".join("%s row, left to right: %s." % (rn, "; ".join(WORD[k] for _, k in sorted(rows[rn]))) for rn in ("Top", "Bottom"))
G = pathlib.Path(B.A) / "CS9-guides"; dst = G / ("wl_canvas_%s.png" % NAME); shutil.copy(CANVAS, dst)
man = json.load(open(G / "manifest.json")); man[dst.name] = hashlib.sha256(dst.read_bytes()).hexdigest()
json.dump(man, open(G / "manifest.json", "w"), indent=1)
LOOK = dict(path=B.A + "DK-BASE/DK-BASE.png", role="IMAGE %d -- his approved base-body sheet (DK-BASE, the base under the armour pieces): the look")
STY = dict(B.STYLE, role="IMAGE %d -- " + B.STYLE['role'])
KNIGHT = ("a tall, lean, pale, gaunt man of about forty with close-cropped black hair, clean-shaven; a near-black quilted arming doublet with fine violet "
          "stitching and a padded collar; near-black steel arm plates and articulated gauntlets with fine gold filigree edges; a plated fauld and tassets "
          "over the hips with a violet cloth panel at the front; a brown leather belt with a gilded buckle; near-black leg plates with gold filigree and "
          "pointed sabatons; and ONE broad GOLD filigree band around his LEFT forearm plate only")
RULES = ("Paint the SURFACE, not the lighting: soft even light; no cast shadows, no dark side, no rim light, no shading that belongs to one viewpoint. "
         "The steel is near-black with a deep violet-indigo sheen laid as layered transparent washes with pale paper highlights on its edges, never a flat black fill "
         "(R-C9-113 sets aside the register card's no-large-black clause for this figure). Stay inside every outline; change no outline, pose, hand or foot. "
         "Add NOTHING he does not wear in the look sheet: no helm, no pauldrons, no breastplate, no cape, no weapon.\n"
         "THE GOLD BAND is on his LEFT forearm ONLY, exactly where IMAGE 1 shows it; never add it to his right forearm, never drop it from his left.\n")
TAIL = ("BACKGROUND: keep the background flat pure #00ff00, as in IMAGE 1. If the image model returns a darker or gradient background anyway, DO NOT spend a retry "
        "on it and still deliver the image: the figures are cut out afterwards by their exact 3D outlines. Spend retries ONLY on the faults named below.\n\n"
        "Two image_gen EDIT calls: variants a and b. ONE retry per variant only if a view's outline, pose, facing or position changed, a view is missing, the man "
        "differs between views, the gold band is on the wrong arm or missing, he wears something the look sheet does not show, or a face close-up is a different "
        "face -- name the reason. Never retry for the background colour. Copy outputs to out/{t}_a.png and out/{t}_b.png with sha256. No code. No other files. No web.\n"
        "RETURN: receipt task_id \"{t}\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen calls; "
        "status; concerns. Never PASS/FAIL.")
if NAME == "A":
    T = "DK-PA"
    text = ("GENERATE BURST {t} -- Run C-9 Phase 2 (Matt R-C9-112/113): the PAINTED TEXTURE of the 3D dark knight's base body, sheet 1 of 2. task_id \"{t}\".\n\n"
            "IMAGE 1 is a sheet of TEN renders of ONE 3D model of a man standing in a relaxed A-pose, on flat pure #00ff00. " + desc +
            " They are renders of the model: every OUTLINE, POSE, POSITION and SIZE is correct and must not change; the surface is flat and too smooth.\n"
            "IMAGE 2 is his approved base-body sheet: " + KNIGHT + ". IMAGE 3 is a STYLE reference ONLY: copy its HAND (the ink line that varies in weight, "
            "transparent watercolour washes that pool and granulate, fine hatching, cream paper highlights); copy nothing else from it.\n"
            "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 sheet in which EVERY figure is repainted as the man of IMAGE 2 seen from that "
            "direction, in IMAGE 3's hand, inside exactly that view's outline, position and size.\n"
            "THIS PAINTING BECOMES THE MODEL'S TEXTURE: it is projected back onto the 3D model from these ten cameras and blended into one texture. So: ONE man "
            "in ten views, not ten men -- the same skin, hair, doublet, plates, belt and sabatons in every view; any disagreement between views becomes a seam.\n"
            + RULES + "THE TWO FACE CLOSE-UPS are his identity: the same face as IMAGE 2, larger -- stern, level gaze, mouth closed. More detail is welcome; a "
            "different face is not.\n" + TAIL).format(t=T)
    refs = [dict(path=str(dst), role="IMAGE 1 -- the sheet to EDIT (8 body views at 19.77 deg + 2 face close-ups of the rigged 3D man at rest; outlines correct, surface flat)"),
            dict(LOOK, role=LOOK['role'] % 2), dict(STY, role=STY['role'] % 3)]
else:
    T = "DK-PB"; APAINT = sys.argv[3]
    text = ("GENERATE BURST {t} -- Run C-9 Phase 2 (Matt R-C9-112/113): the PAINTED TEXTURE of the 3D dark knight's base body, sheet 2 of 2, at the GAME CAMERA "
            "(looking down at 53 degrees). task_id \"{t}\".\n\n"
            "IMAGE 1 is the SAME MAN, ALREADY PAINTED, seen from the game's own camera looking steeply down: his painted surface (from IMAGE 2) projected onto the 3D "
            "model and re-rendered from above. " + desc + " Every OUTLINE, POSE, CROP and CAMERA in IMAGE 1 is fixed and must not change.\n"
            "IMAGE 2 is the painting IMAGE 1 was made from (sheet 1, the same man from ten low angles). IMAGE 3 is his approved base-body sheet (the look): " + KNIGHT +
            ". IMAGE 4 is a STYLE reference ONLY: copy its HAND, never its character, clothing or staff.\n"
            "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 sheet.\n"
            "REPAINT THIS SURFACE; DO NOT PAINT A NEW VIEW. Everything already drawn on him in IMAGE 1 stays exactly where it is, at the same size and shape: the gold "
            "band on his LEFT forearm, the belt and its buckle, the fauld and its violet panel, the plate edges and their gold filigree, the hair. A feature drawn "
            "in a different place becomes a double. What this pass is FOR: the surfaces a steep camera sees properly and a low one only grazed -- the tops of the "
            "shoulders, the crown of the head, the upper back, the tops of the forearms, gauntlets and sabatons. Give them the detail and the hand of IMAGE 2 and "
            "IMAGE 4; leave everything else as found, only cleaner.\n" + RULES + TAIL).format(t=T)
    refs = [dict(path=str(dst), role="IMAGE 1 -- the sheet to EDIT (sheet A paint projected onto the rigged 3D man, re-rendered at 52.95 deg; outlines, crops and cameras fixed)"),
            dict(path=APAINT, role="IMAGE 2 -- the painting IMAGE 1 was made from (DK-PA, chosen by registration)"),
            dict(LOOK, role=LOOK['role'] % 3), dict(STY, role=STY['role'] % 4)]
B.lane_guard(text)
task = dict(text=text, references=refs, image_cap=4, minutes_cap=15, tool_call_cap=20, outputs=["out/%s_a.png" % T, "out/%s_b.png" % T],
            effort='high', add_dirs=[], experiment='R-C9-112-third-character')
p = B.BURST / ('briefs/C-9/%s.task.json' % T); assert not p.exists(), p
p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p); print(desc)
