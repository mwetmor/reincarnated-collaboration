# C-9 Matt R-C9-50: paint MIST BANKS into the B far and forest layers (H1's valleys-in-violet-mist look), by EDIT.
# usage: mist_paint.py briefs <far|forest> | assemble <far|forest>
# Crops of 1536x1024 at step 1280x768; each is an EDIT that only ADDS mist; reassembly feathers every 256 px overlap
# linearly and restores the flat #00ff00 plate wherever the source was plate (the sky side stays the mist LAYER's job).
import json, sys, hashlib, pathlib
import numpy as np
from PIL import Image
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A9 = B/'runs/C-9/artifacts'; S = A9/'CS9-guides'; ANCHOR = A9/'S1-ink/S1-ink_b.png'
L = {'far': dict(src=A9/'CS9-assembly/L12_layer_far.png', out=A9/'CS9-assembly/L13_layer_far.png', grid=(2, 2), size=(2816, 1792),
        what="the FAR layer: distant rolling wooded hills and a winding river under a low sunset, a few small fires with smoke",
        mist="THICK banks of soft pale-violet mist lying IN THE VALLEYS between the hills and along the river, THICKEST toward the horizon (the top of the land) where whole ranges fade into violet haze with only their crests showing, thinning toward the bottom of the layer; hilltops and ridges rise OUT of the mist as dark silhouettes; where a fire burns, its glow shows warm through the mist"),
     'forest': dict(src=A9/'CS9-assembly/L12_layer_forest.png', out=A9/'CS9-assembly/L13_layer_forest.png', grid=(3, 3), size=(4096, 2560),
        what="the MID FOREST layer: a valley forest seen from far above, a wide band of forest fire, scorched land behind it, one river",
        mist="LIGHTER mist than the far distance: soft pale-violet banks and wisps lying in the hollows and along the river, and a violet smoky haze drifting from the fire front, strongest in the upper (farther) part of the layer and fading to almost none in the lower scorched land; the fire and its glow stay clearly visible, glowing warm through the haze")}
bid = lambda l, c, r: f'MF13-{l}-{c}_{r}'
def out(l, c, r):
    for s in ('-r1', ''):
        p = A9/f'{bid(l,c,r)}{s}'/f'{bid(l,c,r)}.png'
        if p.exists(): return p
cmd, l = sys.argv[1], sys.argv[2]; d = L[l]; cols, rows = d['grid']
ids = [(c, r) for r in range(rows) for c in range(cols)]
if cmd == 'briefs':
    im = Image.open(d['src']).convert('RGB'); assert im.size == d['size'], im.size
    m = json.loads((S/'manifest.json').read_text())
    for c, r in ids:
        p = S/f'mf13_{l}_{c}_{r}_canvas.png'; im.crop((c*1280, r*768, c*1280+1536, r*768+1024)).save(p)
        m[p.name] = hashlib.sha256(p.read_bytes()).hexdigest(); i = bid(l, c, r)
        text = (f"GENERATE BURST {i} — Run C-9, parallax layer: ADD MIST (Matt R-C9-50: \"paint it\"). task_id \"{i}\".\n\n"
          f"IMAGE 1 is a 1536x1024 crop of a finished painted parallax layer, {d['what']}; above the land it is flat pure #00ff00 (a keying plate; the sky is a separate layer). "
          f"Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 image that is IMAGE 1 with MIST ADDED: {d['mist']}. "
          "Paint the mist in the same hand as the image: transparent watercolor washes with soft uneven edges, never an airbrushed gradient or a flat grey fog; the mist is light violet-lavender (lit by the low sun it catches a little warm gold on its upper edges). "
          "The mist is ADDED ON TOP: every hill, tree, rock, river, fire and plume stays exactly where and what it is, only veiled where the mist lies. The flat pure #00ff00 above the land stays flat pure #00ff00 (no mist painted into it). "
          "No new buildings, fires, figures, text, border or vignette. Nothing repeats.\n"
          "STYLE: the REGISTER CARD above (PARALLAX LIGHT: a purple smoky haze thickening with distance); IMAGE 2 only as the approved painted style of this level (not its content).\n\n"
          f"One image_gen call. ONE retry only if the mist is missing or reads as flat fog, the land or fires moved or changed, or mist was painted over the #00ff00 plate — name the reason. "
          f"Copy the output from $CODEX_HOME/generated_images/... to out/{i}.png with sha256. No code. No other files. No web.\n"
          f"RETURN: receipt task_id \"{i}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
        refs = [{"path": str(p), "role": "IMAGE 1 — the canvas to EDIT (C-9 parallax layer crop)"},
                {"path": str(ANCHOR), "role": "IMAGE 2 — the approved painted STYLE of this level (not its content)"}]
        json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20, "outputs": [f"out/{i}.png"],
                   "effort": "high", "add_dirs": [], "experiment": "P5-mist-banks"}, open(B/'briefs/C-9'/f'{i}.task.json', 'w'), indent=1, ensure_ascii=False)
    (S/'manifest.json').write_text(json.dumps(m, indent=1)); print(len(ids), l, 'briefs ok:', ' '.join(bid(l, c, r) for c, r in ids))
elif cmd == 'assemble':
    W, H = d['size']; acc = np.zeros((H, W, 3)); wsum = np.zeros((H, W, 1))
    ramp = lambda n, lo, hi: np.minimum(np.minimum(np.arange(n) + 1, 256) if lo else np.full(n, 256), (np.minimum(np.arange(n)[::-1] + 1, 256) if hi else np.full(n, 256))) / 256.0
    for c, r in ids:
        p = out(l, c, r); assert p, f'missing {bid(l, c, r)}'
        t = np.asarray(Image.open(p).convert('RGB').resize((1536, 1024), Image.LANCZOS)).astype(float)
        w = ramp(1024, r > 0, r < rows-1)[:, None] * ramp(1536, c > 0, c < cols-1)[None, :]
        acc[r*768:r*768+1024, c*1280:c*1280+1536] += t * w[..., None]; wsum[r*768:r*768+1024, c*1280:c*1280+1536] += w[..., None]
    o = (acc / wsum).clip(0, 255).astype(np.uint8)
    src = np.asarray(Image.open(d['src']).convert('RGB')).astype(int); plate = (src[..., 1] - np.maximum(src[..., 0], src[..., 2])) > 200
    o[plate] = src[plate]
    Image.fromarray(o).save(d['out']); print(d['out'].name, 'written; plate restored px', int(plate.sum()))
