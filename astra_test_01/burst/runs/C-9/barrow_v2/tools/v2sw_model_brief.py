#!/usr/bin/env python3
"""barrow_v2 SW level (R-C9-159, lane BS): the paint brief for ONE model's view sheet (tools/v2sw_model_bake.py views).
    v2sw_model_brief.py <name> "<what the object is>"   -> briefs/C-9/BV2L-m-<name>.task.json (canvas staged in CS9-guides)"""
import json, sys, pathlib, hashlib
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[1]
B = ROOT.parents[2]
A9 = B / "runs/C-9/artifacts"
S = A9 / "CS9-guides"
name, what = sys.argv[1], sys.argv[2]
bid = f"BV2L-m-{name}"
cp = S / f"{bid}_canvas.png"
Image.open(ROOT / f"paint/v1cam/models/{name}_views.png").convert("RGB").save(cp)
m = S / "manifest.json"; d = json.loads(m.read_text()); d[cp.name] = hashlib.sha256(cp.read_bytes()).hexdigest(); m.write_text(json.dumps(d, indent=1))
text = (f"GENERATE BURST {bid} — Run C-9 Phase 2 lane BS (Matt R-C9-159: each model painted once, on itself). task_id \"{bid}\".\n\n"
        f"IMAGE 1 is the canvas to EDIT (1536x1024): a MODEL SHEET -- FOUR VIEWS OF ONE 3D OBJECT ({what}), the same object seen "
        "from four sides (turned a quarter each time) from 53 degrees above, at one scale, on flat pure #00ff00. It is a plain "
        "render of the model's rough texture. Its painted surface will be wrapped back onto the model, so: paint OVER each view, "
        "keeping EVERY silhouette, crack, ledge and edge exactly where it is (nothing moved, nothing added outside a silhouette), "
        "and keep the #00ff00 flat and untouched.\n"
        "Paint it as ALBEDO, in the hand of IMAGE 2 (the approved first Barrow's painting): transparent watercolour washes, "
        "granular paper texture, a thin warm dark-brown pen line on the main edges; weathered warm-grey granite with fractured "
        "faces and a little rust and ochre lichen; cream-white snow (IMAGE 2's snow, NOT grey, NOT peach) lying ONLY on the tops "
        "and the ledges that face up. SOFT EVEN LIGHT: no cast shadows, no bright and dark side, no rim light (the game lights "
        "it with its own sun). ABSOLUTELY NO PLANTS on it: no heather, no grass, no moss clumps, no red or orange leafy patches -- "
        "where the render shows a patch, paint plain rock or snow. No ground, no text, no other objects.\n\n"
        "One image_gen EDIT call. ONE retry only if a view's silhouette moved or grew, plants appear, the views no longer show the "
        "same object, or a strong light direction or cast shadow appears -- name the reason. Never retry for the background "
        f"colour. Copy the output to out/{bid}.png with sha256. No code. No other files. No web.\n"
        f"RETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE "
        "number of image_gen calls; status; concerns. Never PASS/FAIL.")
refs = [{"path": str(cp), "role": "IMAGE 1 — the canvas to EDIT (the model's four views)"},
        {"path": str(A9 / "T10BF-0_1/T10BF-0_1.png"), "role": "IMAGE 2 — the APPROVED first Barrow's painting (a panel of it): its hand, rock and snow colour ONLY -- not its plants"}]
json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20, "outputs": [f"out/{bid}.png"],
           "effort": "high", "add_dirs": [], "experiment": "R-C9-159-v2sw-models"}, open(B / f"briefs/C-9/{bid}.task.json", "w"), indent=1, ensure_ascii=False)
print(bid, "brief ok")
