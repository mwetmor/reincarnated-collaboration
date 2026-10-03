# EN-E3 painted-texture brief (the D7 method, sheet A) for a CREATURE. View words are GENERATED from the layout rects (the T8 lesson:
# never typed by hand). Stages the canvas into CS9-guides + its manifest (refs_guard rule).
#   python3 scripts/n07_paint_brief.py <name> <layout_name> <canvas.png> <TID> <look_sheet.png> "<look words>" "<marker words>"
import json, sys, os, hashlib, shutil, pathlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); import importlib; B = importlib.import_module('n01_briefs')
NAME, LNAME, CANVAS, T, LOOKP, LOOKW, MARK = sys.argv[1:8]
L = json.load(open(os.path.join(ROOT, "work", "layout_%s.json" % LNAME)))
WORD = dict(S="head-on, FACING THE VIEWER (south)", N="seen from BEHIND, tail toward the viewer (north)", E="in profile, head toward the viewer's RIGHT (east)",
            W="in profile, head toward the viewer's LEFT (west)", SE="turned toward the lower right (south-east)", SW="turned toward the lower left (south-west)",
            NE="turned away toward the upper right (north-east)", NW="turned away toward the upper left (north-west)")
# rows are CLUSTERED by cell centre y (a packed sheet can have 3 rows; a top/bottom split by the canvas middle merged the 2nd and
# 3rd rows on the maw's sheet A and listed them in the wrong order -- found after EN3-MWPA had fired)
cs = sorted(((c["rect"][1] + c["rect"][3] / 2, c["rect"][0], k) for k, c in L["cells"].items()))
rows_ = []
for cy, x, k in cs:
    if rows_ and abs(cy - rows_[-1][0][0]) < 120: rows_[-1].append((cy, x, k))
    else: rows_.append([(cy, x, k)])
RN = ["Top", "Middle", "Bottom"] if len(rows_) == 3 else ["Top", "Bottom"] if len(rows_) == 2 else ["Row %d" % (i + 1) for i in range(len(rows_))]
desc = " ".join("%s row, left to right: %s." % (rn, "; ".join(WORD[k] for _, _, k in sorted(r, key=lambda t: t[1]))) for rn, r in zip(RN, rows_))
G = pathlib.Path(B.A) / "CS9-guides"; dst = G / ("en3_canvas_%s.png" % LNAME); shutil.copy(CANVAS, dst)
man = json.load(open(G / "manifest.json")); man[dst.name] = hashlib.sha256(dst.read_bytes()).hexdigest()
json.dump(man, open(G / "manifest.json", "w"), indent=1)
n = len(L["cells"]); cw, ch = L["canvas"]
text = ("GENERATE BURST {t} -- Run C-9 Phase 2 (Matt R-C9-137): the PAINTED TEXTURE of a 3D CREATURE, sheet 1. task_id \"{t}\".\n\n"
        "IMAGE 1 is a sheet of {n} renders of ONE 3D model of " + os.environ.get("EN3_BODY", "a four-legged creature") + " standing still, seen from " + ("above, looking down at %.0f degrees" % L["elevation_deg"] if L["elevation_deg"] > 30 else "a low angle") + ", on flat pure #00ff00. " + desc +
        " They are renders of the model: every OUTLINE, POSE, POSITION and SIZE is correct and must not change; the surface is flat, smooth and blurry.\n"
        "IMAGE 2 is the creature's approved model sheet: " + LOOKW + ". IMAGE 3 is a STYLE reference ONLY: copy its HAND (the dark ink line that varies "
        "in weight, transparent watercolour washes that pool and granulate, fine hatching, cream paper highlights); copy nothing else from it -- it shows a person.\n"
        "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE {cw}x{ch} sheet in which EVERY view is repainted as the creature of IMAGE 2 seen from that "
        "direction, in IMAGE 3's hand, inside exactly that view's outline, position and size.\n"
        "THIS PAINTING BECOMES THE MODEL'S TEXTURE: it is projected back onto the 3D model from these cameras and blended into one texture. So: ONE creature "
        "in {n} views, not {n} creatures -- the same surface, the same plates, joints and claws in every view; any disagreement between views becomes a seam.\n"
        "Paint the SURFACE, not the lighting: soft even light; no cast shadows, no dark side, no rim light, no shading that belongs to one viewpoint. Tone "
        "comes from its own colours, the pen hatching and the washes. Stay inside every outline; change no outline, leg, claw, tail or tooth position. Add NOTHING "
        "IMAGE 2 does not show.\n" + MARK + "\n"
        "BACKGROUND: keep the background flat pure #00ff00, as in IMAGE 1. If the image model returns a darker or gradient background anyway, DO NOT spend a "
        "retry on it and still deliver the image: the views are cut out afterwards by their exact 3D outlines. Spend retries ONLY on the faults named below.\n\n"
        "Two image_gen EDIT calls: variants a and b. ONE retry per variant only if a view's outline, pose, facing or position changed, a view is missing, the "
        "creature differs between views, or the marker is on the wrong side or missing -- name the reason. Never retry for the background colour. Copy outputs "
        "to out/{t}_a.png and out/{t}_b.png with sha256. No code. No other files. No web.\n"
        "RETURN: receipt task_id \"{t}\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen "
        "calls; status; concerns. Never PASS/FAIL.").format(t=T, n=n, cw=cw, ch=ch)
refs = [dict(path=str(dst), role="IMAGE 1 -- the sheet to EDIT (%d views at %.2f deg of the 3D creature at rest; outlines correct, surface flat)" % (n, L["elevation_deg"])),
        dict(path=LOOKP, role="IMAGE 2 -- the creature's approved model sheet: the look"),
        dict(B.STYLE, role="IMAGE 3 -- STYLE reference ONLY (Matt-supplied): the HAND to copy; never its character, costume, staff, bag or pose")]
B.lane_guard(text)
task = dict(text=text, references=refs, image_cap=4, minutes_cap=15, tool_call_cap=20, outputs=["out/%s_a.png" % T, "out/%s_b.png" % T],
            effort='high', add_dirs=[], experiment='R-C9-137-alternates')
p = B.BURST / ('briefs/C-9/%s.task.json' % T); assert not p.exists(), p
p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p); print(desc)
