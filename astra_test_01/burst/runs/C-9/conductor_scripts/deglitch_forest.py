# C-9 Matt R-C9-42: remove the digital-glitch treatment from the burning forest band (L11_layer_forest).
# usage: deglitch_forest.py briefs | assemble
# 3x3 crops of 1536x1024 at step 1280x768 over the 4096x2560 layer; each is an EDIT that repaints only the glitch
# artefacts as ordinary painted flame; reassembly feathers every 256 px overlap linearly.
import json, sys, hashlib, pathlib
import numpy as np
from PIL import Image
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A9 = B/'runs/C-9/artifacts'; S = A9/'CS9-guides'; SRC = A9/'CS9-assembly/L11_layer_forest.png'
ANCHOR = A9/'S1-ink/S1-ink_b.png'
ids = [(c, r) for r in range(3) for c in range(3)]
bid = lambda c, r: f'FX12-{c}_{r}'
def out(c, r):
    for s in ('-r1', ''):
        p = A9/f'{bid(c,r)}{s}'/f'{bid(c,r)}.png'
        if p.exists(): return p
if sys.argv[1] == 'briefs':
    im = Image.open(SRC).convert('RGB'); m = json.loads((S/'manifest.json').read_text())
    for c, r in ids:
        p = S/f'fx12_{c}_{r}_canvas.png'; im.crop((c*1280, r*768, c*1280+1536, r*768+1024)).save(p)
        m[p.name] = hashlib.sha256(p.read_bytes()).hexdigest(); i = bid(c, r)
        text = (f"GENERATE BURST {i} — Run C-9, burning-forest parallax layer: REMOVE THE GLITCH EFFECT from the fire (Matt R-C9-42). task_id \"{i}\".\n\n"
          "IMAGE 1 is a 1536x1024 crop of a finished painted parallax layer: a valley forest seen from far above, a wide band of forest fire, scorched land behind it, one river, flat pure #00ff00 above the treeline. "
          "The flames were painted with a DIGITAL-GLITCH treatment that is now rejected: blocky rectangular fragments at the flame tips, horizontal slices of fire shifted sideways, thin horizontal tear or scan lines, stepped/stair-cased flame edges, and cyan or magenta fringes. "
          "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 image that is IMAGE 1 with EVERY such glitch artefact repainted as ORDINARY hand-painted flame in the same place: soft licking tongues of orange-gold fire with a darker red edge, ragged and organic, rising from the trees, in the same line and wash as the rest of the image; embers as small round glowing dots. "
          "Keep the fire where it is, as big and as wide as it is (same front edge, same burning area), and keep EVERYTHING ELSE exactly as it is: every tree, the smoke, the scorched land, the river, the hills, the colours, the #00ff00 above the treeline. Do not restyle, recolour, sharpen or move anything. No text, figures, buildings, border or vignette.\n"
          "STYLE: the REGISTER CARD above; IMAGE 2 only as the approved painted style of this level (not its content).\n\n"
          f"One image_gen call. ONE retry only if glitch artefacts clearly remain, the fire shrank or moved, or the rest of the image was visibly altered — name the reason. "
          f"Copy the output from $CODEX_HOME/generated_images/... to out/{i}.png with sha256. No code. No other files. No web.\n"
          f"RETURN: receipt task_id \"{i}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
        refs = [{"path": str(p), "role": "IMAGE 1 — the canvas to EDIT (C-9 forest layer crop)"},
                {"path": str(ANCHOR), "role": "IMAGE 2 — the approved painted STYLE of this level (not its content)"}]
        json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20, "outputs": [f"out/{i}.png"],
                   "effort": "high", "add_dirs": [], "experiment": "P5-forest-deglitch"}, open(B/'briefs/C-9'/f'{i}.task.json', 'w'), indent=1, ensure_ascii=False)
    (S/'manifest.json').write_text(json.dumps(m, indent=1)); print('9 briefs ok')
elif sys.argv[1] == 'assemble':
    W, H = 4096, 2560; acc = np.zeros((H, W, 3)); wsum = np.zeros((H, W, 1))
    ramp = lambda n, lo, hi: np.minimum(np.minimum(np.arange(n) + 1, 256) if lo else np.full(n, 256), (np.minimum(np.arange(n)[::-1] + 1, 256) if hi else np.full(n, 256))) / 256.0
    for c, r in ids:
        p = out(c, r); assert p, f'missing {bid(c, r)}'
        t = np.asarray(Image.open(p).convert('RGB').resize((1536, 1024), Image.LANCZOS)).astype(float)
        w = ramp(1024, r > 0, r < 2)[:, None] * ramp(1536, c > 0, c < 2)[None, :]
        acc[r*768:r*768+1024, c*1280:c*1280+1536] += t * w[..., None]; wsum[r*768:r*768+1024, c*1280:c*1280+1536] += w[..., None]
    o = (acc / wsum).clip(0, 255).astype(np.uint8)
    # the keyed sky must stay the ORIGINAL flat plate: restore it wherever the source was plate
    src = np.asarray(Image.open(SRC).convert('RGB')).astype(int); plate = (src[..., 1] - np.maximum(src[..., 0], src[..., 2])) > 200
    o[plate] = src[plate]
    Image.fromarray(o).save(A9/'CS9-assembly/L12_layer_forest.png'); print('L12_layer_forest.png written; plate restored px', int(plate.sum()))
