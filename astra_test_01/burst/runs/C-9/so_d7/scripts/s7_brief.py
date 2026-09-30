# Write a paint-sheet brief whose VIEW DESCRIPTION IS GENERATED FROM THE LAYOUT.
#
#   python3 scripts/s7_brief.py A <canvas.png> <task_id> <out.task.json>
#
# The barbarian's T8P-A text describes ITS canvas: "top row, left to right:
# west, east, south-west, south-east, north-west, north-east". The packer picks
# its own order per model, and this one's top row runs SE, E, SW, W, NE, NW, S.
# Copying that paragraph would have told the painter the wrong direction for
# every view -- the same class as the layout that carried the camera twice and
# put the barbarian's face on the back of his head. So the words come from the
# rects, and nothing about position is typed by hand.
import json, sys, hashlib, os
NAME, CANVAS, TID, OUT = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
L = json.load(open(os.path.join(ROOT, "work", "layout_%s.json" % NAME)))
T = json.load(open(os.path.join(ROOT, "work", "tattoo_cells_%s.json" % NAME)))
WORD = dict(
    S="FACING THE VIEWER (south)", N="seen from BEHIND (north)",
    E="facing the viewer's RIGHT in profile (east)",
    W="facing the viewer's LEFT in profile (west)",
    SE="facing the lower right (south-east)", SW="facing the lower left (south-west)",
    NE="facing away to the upper right (north-east)",
    NW="facing away to the upper left (north-west)",
    face_S="a CLOSE-UP of her FACE from the front",
    face_SE="a CLOSE-UP of her face from the lower right, three-quarter")
cells = L["cells"]
mid = L["canvas"][1] / 2
rows = {"Top": [], "Bottom": []}
for k, c in cells.items():
    x, y, w, h = c["rect"]
    rows["Top" if y + h / 2 < mid else "Bottom"].append((x, k))
desc = []
for rn in ("Top", "Bottom"):
    seq = [WORD[k] for _, k in sorted(rows[rn])]
    desc.append("%s row, left to right: %s." % (rn, "; ".join(seq)))
order = [k for rn in ("Top", "Bottom") for _, k in sorted(rows[rn])]
body_vis = [k for k in T["visible"] if not k.startswith("face")]
hidden = [k for k in cells if not k.startswith("face") and k not in body_vis]
nm = lambda ks: ", ".join(WORD[k].split("(")[-1].rstrip(")") if "(" in WORD[k] else k for k in ks)
text = """GENERATE BURST {tid} -- Run C-9 Phase 2, D7 (Matt R-C9-80): the PAINTED TEXTURE of the 3D woman, sheet 1 of 2. task_id "{tid}".

IMAGE 1 is a sheet of TEN renders of ONE 3D model of a woman standing in a relaxed A-pose, on flat pure #00ff00. {rows} They are renders of the model: every OUTLINE, POSE, POSITION and SIZE is correct and must not change; the surface is flat and too smooth.
IMAGE 2 is her APPROVED character sheet: a lean, athletic woman with weathered warm skin; long dark hair worn in one thick rear braid, the left side of her head shaved short; a plain sleeveless undyed-linen shift to the knee with a slit hem; a narrow brown leather belt with a small buckle; tall brown leather boots; and ONE set of small orange runes on her LEFT forearm. IMAGE 3 is a STYLE reference ONLY: copy its HAND (the warm dark-brown ink line that varies in weight, transparent watercolor washes that pool and granulate, fine hatching in the shadows, cream paper highlights); copy nothing else from it -- NOT its character, NOT its clothing, and NOT the staff it shows. She holds nothing.
Use image_gen in EDIT mode on IMAGE 1 and deliver ONE {cw}x{ch} sheet in which EVERY figure is repainted as the woman of IMAGE 2 seen from that direction, in IMAGE 3's hand, inside exactly that view's outline, position and size.
THIS PAINTING BECOMES THE MODEL'S TEXTURE: it will be projected back onto the 3D model from these ten cameras and blended into one texture. So:
1. ONE woman in ten views, not ten women: the same skin tone, the same hair colour and braid, the same shaved side, the same linen shift, belt and boots in every view. Any disagreement between views becomes a seam.
2. Paint the SURFACE, not the lighting: soft even light; no cast shadows, no dark side, no rim light, no shading that belongs to one viewpoint. Tone comes from her own colours and the pen hatching.
3. Stay inside the outlines: do not paint beyond a silhouette, do not change any outline, pose, hand or foot. Add NOTHING she does not wear in IMAGE 2: no robe, no cloak, no jewellery, no staff.
THE RUNES: they are on her LEFT forearm ONLY, exactly where IMAGE 1 shows them (they show in the {vis} views, and are hidden in the {hid} view). Never add them to her right arm; never drop them from her left.
THE TWO FACE CLOSE-UPS are her identity: the same face as IMAGE 2, larger -- a calm, level gaze, mouth closed, the braid and the shaved side. More detail is welcome; a different face is not.

BACKGROUND: keep the background flat pure #00ff00, as in IMAGE 1. If the image model returns a darker or gradient background anyway, DO NOT spend a retry on it and still deliver the image: the figures are cut out afterwards by their exact 3D outlines, so the background colour does not decide success. Spend retries ONLY on the faults named below.
STYLE: the REGISTER CARD above governs line, washes, light and plate; its manuscript-subject clause does not apply to this figure. Paint in IMAGE 3's hand with IMAGE 2's look.

Two image_gen EDIT calls: variants a and b. ONE retry per variant only if a view's outline, pose, facing or position changed, a view is missing, the woman differs between views, the runes are on the wrong arm or missing, she holds or wears something IMAGE 2 does not show, or a face close-up is a different face -- name the reason. Never retry for the background colour. Copy outputs to out/{tid}_a.png and out/{tid}_b.png with sha256. No code. No other files. No web.
RETURN: receipt task_id "{tid}"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.""".format(
    tid=TID, rows=" ".join(desc), cw=L["canvas"][0], ch=L["canvas"][1],
    vis=nm(body_vis), hid=nm(hidden) or "none")
A = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts/"
task = dict(text=text, references=[
    dict(path=CANVAS, role="IMAGE 1 -- the sheet to EDIT (8 body views at 19.77 deg + 2 face close-ups of the rigged 3D woman at rest; outlines correct, surface flat)"),
    dict(path=A + "CS9-guides/SO-1_b_harvest.png", role="IMAGE 2 -- her approved four-view base-body sheet (SO-1 variant b, Matt G1-S): the look"),
    dict(path=A + "inputs/nb_style_ref_matt.png", role="IMAGE 3 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the hand; never its character, costume, staff or pose")],
    image_cap=4, minutes_cap=15, tool_call_cap=20,
    outputs=["out/%s_a.png" % TID, "out/%s_b.png" % TID], effort="high", add_dirs=[],
    experiment="D7-texture")
json.dump(task, open(OUT, "w"), indent=1)
print("wrote %s  (%d chars)" % (OUT, len(text)))
print("  " + "\n  ".join(desc))
print("  runes visible: %s | hidden: %s" % (nm(body_vis), nm(hidden)))
print("  cell order as described:", order)
