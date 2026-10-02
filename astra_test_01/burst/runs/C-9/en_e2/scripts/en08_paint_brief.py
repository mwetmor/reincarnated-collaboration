# EN-E2 painted-texture briefs (D7's SOP-A / SOP-B via wl_e1's e07, re-worded for the acolytes). View words GENERATED from the
# layout rects (never typed by hand). The canvas is staged into CS9-guides + its manifest (the refs_guard rule, as e07 does).
#   python3 en08_paint_brief.py <m|f> A <canvas.png>            -> EN2-<G>PA
#   python3 en08_paint_brief.py <m|f> B <canvas.png> <A_paint>  -> EN2-<G>PB
import json, sys, os, hashlib, shutil, pathlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); import importlib; B = importlib.import_module('en01_briefs')
G, NAME, CANVAS = sys.argv[1], sys.argv[2], sys.argv[3]
L = json.load(open(os.path.join(ROOT, "work", "layout_%s%s.json" % (G, NAME))))
P = dict(m=("his", "him", "he", "man"), f=("her", "her", "she", "woman"))[G]
WORD = dict(S="FACING THE VIEWER (south)", N="seen from BEHIND (north)", E="facing the viewer's RIGHT in profile (east)",
            W="facing the viewer's LEFT in profile (west)", SE="facing the lower right (south-east)", SW="facing the lower left (south-west)",
            NE="facing away to the upper right (north-east)", NW="facing away to the upper left (north-west)",
            face_S="a CLOSE-UP of %s HEAD from the front" % P[0], face_SE="a CLOSE-UP of %s head from the lower right, three-quarter" % P[0])
mid = L["canvas"][1] / 2; rows = {"Top": [], "Bottom": []}
for k, c in L["cells"].items():
    x, y, w, h = c["rect"]; rows["Top" if y + h / 2 < mid else "Bottom"].append((x, k))
desc = " ".join("%s row, left to right: %s." % (rn, "; ".join(WORD[k] for _, k in sorted(rows[rn]))) for rn in ("Top", "Bottom"))
GD = pathlib.Path(B.A) / "CS9-guides"; dst = GD / ("en2_%s_canvas_%s.png" % (G, NAME)); shutil.copy(CANVAS, dst)
man = json.load(open(GD / "manifest.json")); man[dst.name] = hashlib.sha256(dst.read_bytes()).hexdigest()
json.dump(man, open(GD / "manifest.json", "w"), indent=1)
TID = dict(m="EN2-M", f="EN2-F")[G]
LOOK = dict(path=B.A + "%s/%s_a.png" % (TID, TID), role="IMAGE %%d -- %s approved model sheet (%s_a): the look" % (P[0], TID))
STY = dict(B.STYLE, role="IMAGE %d -- STYLE reference ONLY (Matt-supplied, R-C9-69): the HAND to copy; never its character, costume, hood, robe, staff or pose")
WHO = dict(
    m=("a possessed acolyte: a deep lapis-blue hood bound in tarnished brass, the face inside it a dim cool-grey hatched shadow with two small pale "
       "blue-white eyes; a faded lapis hooded robe over an ivory under-robe, split to the knee and ragged at the hem and cuffs, a plain cord belt; "
       "broken brass gear-wheels at the throat and hanging from the belt; dark grey-brown leggings and soft wrapped shoes; thin bare hands, pale "
       "grey-blue going to pale blue-white at the fingertips; and ONE broad BRASS BRACER engraved with an hour-ring on his LEFT forearm only"),
    f=("a possessed acolyte: an ashen grey-blue face, gaunt and calm, pale blue-white eyes with no pupils, long straight ash-grey hair, a thin tarnished "
       "brass circlet with a small broken clock-face at the brow; an ivory knee-length alb under a sleeveless lapis-blue chasuble bordered with faded "
       "brass hour-mark embroidery, ragged at the hems; a narrow lapis stole down the front with a broken brass gear near each end; dark grey "
       "leggings and soft wrapped shoes; thin bare hands, ashen grey-blue going to pale blue-white at the fingertips; and ONE cracked brass "
       "CLOCK-FACE disc hanging at her LEFT hip only"))[G]
MARK = dict(m="THE BRASS BRACER is on his LEFT forearm ONLY", f="THE CLOCK-FACE DISC hangs at her LEFT hip ONLY")[G]
SKIN = dict(m="", f="Her skin is ASHEN: a cold grey-blue, the colour of the dead, never warm or rosy (the conductor's note); ")[G]
RULES = ("Paint the SURFACE, not the lighting: soft even light; no cast shadows, no dark side, no rim light, no glow, no shading that belongs to one "
         "viewpoint. " + SKIN + "The darks are hatching and layered transparent washes with pale paper highlights, never a flat black fill. Brass is a "
         "tarnished ochre-brown wash with pale highlights. Stay inside every outline; change no outline, pose, hand or foot. Add NOTHING the look sheet "
         "does not show: no staff, no book, no weapon, nothing held.\n" + MARK + ", exactly where IMAGE 1 shows it; never on the right side.\n")
TAIL = ("BACKGROUND: keep the background flat pure #00ff00, as in IMAGE 1. If the image model returns a darker or gradient background anyway, DO NOT spend a retry "
        "on it and still deliver the image: the figures are cut out afterwards by their exact 3D outlines. Spend retries ONLY on the faults named below.\n\n"
        "Two image_gen EDIT calls: variants a and b. ONE retry per variant only if a view's outline, pose, facing or position changed, a view is missing, the "
        "figure differs between views, the brass marker is on the wrong side or missing, something is added that the look sheet does not show, or a head "
        "close-up is a different face -- name the reason. Never retry for the background colour. Copy outputs to out/{t}_a.png and out/{t}_b.png with sha256. "
        "No code. No other files. No web.\n"
        "RETURN: receipt task_id \"{t}\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen calls; "
        "status; concerns. Never PASS/FAIL.")
if NAME == "A":
    T = TID + "PA"
    text = ("GENERATE BURST {t} -- Run C-9 Phase 2 (Matt, R-C9-132/133): the PAINTED TEXTURE of a 3D enemy for the cathedral arena, sheet 1 of 2. task_id \"{t}\".\n\n"
            "IMAGE 1 is a sheet of TEN renders of ONE 3D model standing in a relaxed A-pose, on flat pure #00ff00. " + desc +
            " They are renders of the model: every OUTLINE, POSE, POSITION and SIZE is correct and must not change; the surface is flat and too smooth.\n"
            "IMAGE 2 is the approved model sheet: " + WHO + ". IMAGE 3 is a STYLE reference ONLY: copy its HAND (the ink line that varies in weight, "
            "transparent watercolour washes that pool and granulate, fine hatching, cream paper highlights); copy nothing else from it.\n"
            "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 sheet in which EVERY figure is repainted as the figure of IMAGE 2 seen from that "
            "direction, in IMAGE 3's hand, inside exactly that view's outline, position and size.\n"
            "THIS PAINTING BECOMES THE MODEL'S TEXTURE: it is projected back onto the 3D model from these ten cameras and blended into one texture. So: ONE "
            "figure in ten views, not ten figures -- the same cloth, brass, hands and shoes in every view; any disagreement between views becomes a seam.\n"
            + RULES + "THE TWO HEAD CLOSE-UPS are the identity: the same head as IMAGE 2, larger. More detail is welcome; a different face or hood is not.\n"
            + TAIL).format(t=T)
    refs = [dict(path=str(dst), role="IMAGE 1 -- the sheet to EDIT (8 body views at 19.77 deg + 2 head close-ups of the rigged 3D model at rest; outlines correct, surface flat)"),
            dict(LOOK, role=LOOK['role'] % 2), dict(STY, role=STY['role'] % 3)]
else:
    T = TID + "PB"; APAINT = sys.argv[4]
    text = ("GENERATE BURST {t} -- Run C-9 Phase 2 (Matt, R-C9-132/133): the PAINTED TEXTURE of a 3D enemy for the cathedral arena, sheet 2 of 2, at the GAME "
            "CAMERA (looking down at 53 degrees). task_id \"{t}\".\n\n"
            "IMAGE 1 is the SAME FIGURE, ALREADY PAINTED, seen from the game's own camera looking steeply down: its painted surface (from IMAGE 2) projected onto "
            "the 3D model and re-rendered from above. " + desc + " Every OUTLINE, POSE, CROP and CAMERA in IMAGE 1 is fixed and must not change.\n"
            "IMAGE 2 is the painting IMAGE 1 was made from (sheet 1, the same figure from ten low angles). IMAGE 3 is the approved model sheet (the look): " + WHO +
            ". IMAGE 4 is a STYLE reference ONLY: copy its HAND, never its character, clothing or staff.\n"
            "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 sheet.\n"
            "REPAINT THIS SURFACE; DO NOT PAINT A NEW VIEW. Everything already drawn in IMAGE 1 stays exactly where it is, at the same size and shape: the "
            "brass pieces, the belt, the hems and borders, the hair or hood. A feature drawn in a different place becomes a double. What this pass is FOR: the "
            "surfaces a steep camera sees properly and a low one only grazed -- the tops of the shoulders, the crown of the head or hood, the upper back, the "
            "tops of the forearms and shoes. Give them the detail and the hand of IMAGE 2 and IMAGE 4; leave everything else as found, only cleaner.\n"
            + RULES + TAIL).format(t=T)
    refs = [dict(path=str(dst), role="IMAGE 1 -- the sheet to EDIT (sheet A paint projected onto the rigged 3D model, re-rendered at 52.95 deg; outlines, crops and cameras fixed)"),
            dict(path=APAINT, role="IMAGE 2 -- the painting IMAGE 1 was made from (sheet A, chosen by registration)"),
            dict(LOOK, role=LOOK['role'] % 3), dict(STY, role=STY['role'] % 4)]
B.lane_guard(text); [B.lane_guard(r['role']) for r in refs]
task = dict(text=text, references=refs, image_cap=4, minutes_cap=15, tool_call_cap=20, outputs=["out/%s_a.png" % T, "out/%s_b.png" % T],
            effort='high', add_dirs=[], experiment='R-C9-132-crucible-enemies')
p = B.BURST / ('briefs/C-9/%s.task.json' % T); assert not p.exists(), p
p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p); print(desc)
