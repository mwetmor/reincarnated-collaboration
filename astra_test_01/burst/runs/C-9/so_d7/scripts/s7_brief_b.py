# Sheet B's brief, its VIEW DESCRIPTION GENERATED FROM layout_B -- same reason as
# sheet A: the packer orders cells per model, and a hand-typed row order is a
# brief that names the wrong direction for every view.
#
#   python3 scripts/s7_brief_b.py <canvas.png> <task_id> <out.task.json>
#
# The "unpainted" share is MEASURED, not borrowed. T8P-B told the barbarian's
# painter "under a third of one percent of what you see is unpainted model"; for
# her it is read from work/sheetB_blind_share.json (sheet A's blind map rendered
# through sheet B's own cameras). 24.8% of her texture was unseen by sheet A, but
# only ~0.8% of what sheet B sees is -- the rest are surfaces no camera at this
# pitch sees either. So this pass is not hole-filling; it is detail on the tops
# that a low camera only grazed, which is what the text says.
import json, os, sys
CANVAS, TID, OUT = sys.argv[1:4]
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
L = json.load(open(os.path.join(ROOT, "work", "layout_B.json")))
SH = json.load(open(os.path.join(ROOT, "work", "sheetB_blind_share.json")))
WORD = dict(
    S="FACING THE VIEWER (south)", N="seen from BEHIND (north)",
    E="facing the viewer's RIGHT in profile (east)", W="facing the viewer's LEFT in profile (west)",
    SE="facing the lower right (south-east)", SW="facing the lower left (south-west)",
    NE="facing away to the upper right (north-east)", NW="facing away to the upper left (north-west)",
    face_S="a CLOSE-UP of her head from above and in front (the crown of dark hair, the face foreshortened below it)",
    face_SE="a CLOSE-UP of her head from above, lower right")
mid = L["canvas"][1] / 2
rows = {"Top": [], "Bottom": []}
for k, c in L["cells"].items():
    x, y, w, h = c["rect"]
    rows["Top" if y + h / 2 < mid else "Bottom"].append((x, k))
desc = " ".join("%s row, left to right: %s." % (rn, "; ".join(WORD[k] for _, k in sorted(rows[rn])))
                for rn in ("Top", "Bottom"))
pct = SH["overall_pct"]
text = """GENERATE BURST {tid} -- Run C-9 Phase 2, D7 (Matt R-C9-80): the PAINTED TEXTURE of the 3D woman, sheet 2 of 2, at the GAME CAMERA (looking down at 53 degrees). task_id "{tid}".

IMAGE 1 is the SAME WOMAN, ALREADY PAINTED, seen from the game's own camera looking steeply down: her painted surface (from IMAGE 2) projected onto the 3D model and re-rendered from above. {desc} Every OUTLINE, POSE, CROP and CAMERA in IMAGE 1 is fixed and must not change.
IMAGE 2 is the painting IMAGE 1 was made from (sheet 1, the same woman from ten low angles). IMAGE 3 is her approved character sheet (the look). IMAGE 4 is a STYLE reference ONLY: copy its HAND, never its character, clothing or staff.
Use image_gen in EDIT mode on IMAGE 1 and deliver ONE {cw}x{ch} sheet.
REPAINT THIS SURFACE; DO NOT PAINT A NEW VIEW. Everything already drawn on her in IMAGE 1 stays exactly where it is, at the same size and the same shape: the long dark braid down her back, the shaved left side of her head, the small orange runes on her LEFT forearm, the narrow belt and its buckle, the linen shift and its slit hem, and the boots. Do not move, redraw or re-invent any of them: this painting is blended with IMAGE 2 on one model, and a feature drawn in a different place becomes a double. Almost nothing here needs inventing: about {pct:.1f}% of what you see is unpainted model.
What this pass is FOR: the surfaces a steep camera sees properly and a low one only grazed -- the tops of the shoulders, the crown of the head and the braid from above, the upper back, the tops of the forearms and hands, the tops of the boots. They look smeared in IMAGE 1 because they were painted edge-on. Give them the detail and the hand of IMAGE 2 and IMAGE 4 (ink line, hatching, transparent washes); leave everything else as found, only cleaner. Take the look from the painting (IMAGE 2), never from any flat, smooth or smeared shading in IMAGE 1. She holds nothing and wears nothing IMAGE 3 does not show.
Paint the SURFACE, not the lighting: soft even light; no cast shadows, no dark side, no rim light. Stay inside every outline. The runes are on her LEFT forearm ONLY; never on the right.

BACKGROUND: keep the background flat pure #00ff00, as in IMAGE 1. If the image model returns a darker or gradient background anyway, DO NOT spend a retry on it and still deliver the image: the figures are cut out afterwards by their exact 3D outlines, so the background colour does not decide success. Spend retries ONLY on the faults named below.
STYLE: the REGISTER CARD above governs line, washes, light and plate; its manuscript-subject clause does not apply to this figure. Paint in IMAGE 4's hand with IMAGE 2's and IMAGE 3's look.

Two image_gen EDIT calls: variants a and b. ONE retry per variant only if a view's outline, pose, facing or position changed, a view is missing, a feature (braid, shaved side, runes, belt) moved, was redrawn elsewhere or disappeared, the runes are on the wrong arm, or she holds or wears something IMAGE 3 does not show -- name the reason. Never retry for the background colour. Copy outputs to out/{tid}_a.png and out/{tid}_b.png with sha256. No code. No other files. No web.
RETURN: receipt task_id "{tid}"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.""".format(
    tid=TID, desc=desc, cw=L["canvas"][0], ch=L["canvas"][1], pct=pct)
A = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts/"
task = dict(text=text, references=[
    dict(path=CANVAS, role="IMAGE 1 -- the sheet to EDIT (sheet A paint projected onto the rigged 3D woman, re-rendered at 52.95 deg; outlines, crops and cameras fixed)"),
    dict(path=A + "SOP-A/SOP-A_b.png", role="IMAGE 2 -- the painting IMAGE 1 was made from (SOP-A variant b, chosen by registration)"),
    dict(path=A + "CS9-guides/SO-1_b_harvest.png", role="IMAGE 3 -- her approved base-body sheet (SO-1 variant b, Matt G1-S): the look"),
    dict(path=A + "inputs/nb_style_ref_matt.png", role="IMAGE 4 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose")],
    image_cap=4, minutes_cap=15, tool_call_cap=20,
    outputs=["out/%s_a.png" % TID, "out/%s_b.png" % TID], effort="high", add_dirs=[],
    experiment="D7-texture")
import re
assert not re.findall(r"diablo|\bd2\b|blizzard|sorceress|\bsorc\b|amazon", text, re.I), "franchise term"
json.dump(task, open(OUT, "w"), indent=1)
print("wrote %s (%d chars); unpainted share stated: %.2f%%" % (OUT, len(text), pct))
print("  " + desc)
