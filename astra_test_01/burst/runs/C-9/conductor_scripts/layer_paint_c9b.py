# C-9 P5 parallax driver (ported from runs/C-3/conductor_scripts/layer_paint.py; grid geometry unchanged).
# usage: layer_paint_c9.py ready | stage <id> | brief <id>     ids: L9-<layer>-<c>_<r>
# Content = Matt R-C9-13 (manuscript sky; far valley + domed temple + cathedral on its crag; manuscript forest; mist).
import json, sys, pathlib, hashlib
from PIL import Image
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A9 = B/'runs/C-9/artifacts'; S = A9/'CS9-guides'; S.mkdir(parents=True, exist_ok=True); REF = A9/'refs'
ANCHOR = A9/'S1-ink/S1-ink_b.png'
LAY = {
 'sky': dict(cols=2, rows=2, bg=(128, 128, 128), key=False, ref=None, c3=('sky', lambda c, r: (c, 0)),
   desc="the SUNSET SKY layer, the farthest backdrop, painted in the manuscript register: the sun LOW near the LEFT edge of the full layer, a small pale-gold disc half-veiled by cloud; a warm band of gold, apricot and rose along the LOWER part of the sky, rising through soft violet to a dusky blue at the TOP; long thin stylised clouds drawn with a pen line and uneven washes, lit rose and gold from below, every cloud a different shape; two or three dark smoke plumes rising from the burning valley on the RIGHT, each different. NO stars, NOT a night sky, NO land.",
   part=lambda c, r: [["upper-left (the sky darker violet-blue, clouds lit from below)", "upper-right (violet-blue, smoke plumes rising into the clouds)"], ["lower-left (the low sun and the brightest gold band)", "lower-right (gold and rose band, smoke plumes rising from below the edge)"]][r][c]),
 'far': dict(cols=2, rows=2, bg=(128, 128, 128), key=True, ref='trh-09-september-saumur.jpg', c3=('far_ruins', lambda c, r: (c, r)),
   desc="the FAR layer, VERY DISTANT: a wide valley seen from high above and far away, ridges and hills turning blue-violet and hazy with distance, a river catching the sunset. Toward the LEFT, on a far hill, the KEEPERS' TOWER: ONE tall, slender stone tower with a pointed roof, BURNING — flames at its upper windows and a column of dark smoke. Far to the RIGHT, on a steep rocky crag, ONE GOTHIC CATHEDRAL with a tall spire and a rose window, BURNING — fire through its roof and smoke. Between them AT MOST ONE small walled town, far away. Everything is TINY: the tower and the cathedral are small silhouettes on the skyline, each well under a tenth of the full layer's height. NOTHING REPEATS: exactly one tower, one cathedral, at most one town, no copied hills, trees or buildings. The LAND's top silhouette sits at about 38-48 % of the full layer's height; EVERYTHING ABOVE that silhouette is flat pure #00ff00 (the sky layer shows there); below it the land is painted down to the bottom edge, hazier and simpler toward the bottom.",
   part=lambda c, r: [["upper-left (mostly green; the far hills and the burning Keepers' tower rise into the bottom of this panel)", "upper-right (mostly green; the crag and the burning cathedral's spire rise into the bottom of this panel)"],
                      ["lower-left (the tower's hill and the far valley, the river)", "lower-right (the cathedral's crag, the one small town, the river)"]][r][c]),
 'forest': dict(cols=3, rows=3, bg=(128, 128, 128), key=True, ref='trh-05-may-forest.jpg', c3=('forest_valley', lambda c, r: (c, min(r, 1))),
   desc="the MID FOREST layer: the valley floor FAR BELOW the cliff, hundreds of metres down, seen from high above: a vast manuscript forest in which each tree crown is TINY (from a few pixels up to about 20 px across), with meadows, fields and a winding river between. Two or three SEPARATE FIRES burn in the forest, each a different size and shape, with orange flames, dark burnt ground around them and smoke drifting up. NOTHING REPEATS: no two tree clumps, fields, fires or river bends alike. Its top silhouette (the far line of treetops) sits at about 25-32 % of the full layer's height; EVERYTHING ABOVE that silhouette is flat pure #00ff00; below it the forest fills everything down to the bottom edge.",
   part=lambda c, r: [["upper-left", "upper-middle", "upper-right"], ["middle-left (one fire burns here)", "centre (the river winds here)", "middle-right"], ["lower-left", "lower-middle (a second, smaller fire)", "lower-right"]][r][c]),
 'mist': dict(cols=2, rows=2, bg=(0, 0, 0), key=False, ref=None, c3=None,
   desc="the MIST layer: soft drifting banks of pale mist painted as LIGHT on a PURE BLACK background (black = fully transparent in the game, brighter = more opaque mist): cream, peach and pale lavender washes with soft, uneven watercolor edges, lit by the sunset. Thin and wispy in the upper half, thickening into low banks toward the bottom; no two banks alike. No land, no trees, no sky colour on the black.",
   part=lambda c, r: [["upper-left (thin wisps)", "upper-right (thin wisps)"], ["lower-left (low banks)", "lower-right (low banks)"]][r][c]),
}
C3A = B/'runs/C-3/artifacts'
pid = lambda l, c, r: f'L10-{l}-{c}_{r}'
def src(i):
    for d in (f'{i}-r1', i):
        p = A9/d/f'{i}.png'
        if p.exists(): return p
done = lambda i: src(i) is not None
def panels():
    for l, d in LAY.items():
        for r in range(d['rows']):
            for c in range(d['cols']): yield l, c, r
def manifest_add(p):
    m = S/'manifest.json'; d = json.loads(m.read_text()) if m.exists() else {}
    d[p.name] = hashlib.sha256(p.read_bytes()).hexdigest(); m.write_text(json.dumps(d, indent=1))
cmd = sys.argv[1]
if cmd == 'ready':
    out = []
    for l, c, r in panels():
        i = pid(l, c, r)
        if done(i): continue
        need = ([pid(l, c-1, r)] if c else []) + ([pid(l, c, r-1)] if r else []) + ([pid(l, c+1, r-1)] if r and c+1 < LAY[l]['cols'] else [])
        if all(done(n) for n in need): out.append(i)
    print(' '.join(out)); sys.exit()
i = sys.argv[2]; import os; SUF = os.environ.get('SUF', '')
l = i.split('-')[1]; c, r = map(int, i.split('-')[2].split('_')); d = LAY[l]
canvas = Image.new('RGB', (1536, 1024), d['bg']); kept = []
for (nc, nr) in [(c-1, r), (c, r-1), (c+1, r-1), (c-1, r-1)]:
    if nc < 0 or nr < 0 or nc >= d['cols']: continue
    n = pid(l, nc, nr)
    if not done(n): continue
    im = Image.open(src(n)).convert('RGB'); dx, dy = (nc-c)*1280, (nr-r)*768
    x0, y0 = max(0, dx), max(0, dy); x1, y1 = min(1536, dx+1536), min(1024, dy+1024)
    if x1 > x0 and y1 > y0:
        canvas.paste(im.crop((x0-dx, y0-dy, x1-dx, y1-dy)), (x0, y0))
        kept.append({(-1, 0): 'its LEFT 256 columns', (0, -1): 'its TOP 256 rows', (1, -1): 'its top-right 256x256 corner', (-1, -1): 'its top-left 256x256 corner'}[(nc-c, nr-r)])
cp = S/f'{i}{SUF}_canvas.png'
if cmd == 'stage':
    canvas.save(cp); manifest_add(cp); print(i, 'staged', kept); sys.exit()
bid = f'{i}{SUF}'
fill = 'flat mid-grey' if d['bg'] != (0, 0, 0) else 'flat black'
geom = (f"This image is one panel ({d['part'](c, r)}) of a {d['cols']}x{d['rows']} grid of 1536x1024 panels (neighbours overlap by 256 px) that together form ONE continuous painted "
        f"parallax background layer for a 2D game scene seen past a cliff edge. The whole layer is {d['desc']}")
reg = ("STYLE: the REGISTER CARD above; line, hatching and washes matched to IMAGE 2 (the approved painted style of this level), the pen line lighter and thinner with distance. "
       + ("The manuscript page (if attached) shows how a Book of Hours paints this kind of subject; the GEOMETRY-ONLY image sets the scale and distance. " if d['ref'] or d['c3'] else "")
       + "No characters, creatures, text, UI, border or vignette.")
if kept:
    text = (f"GENERATE BURST {bid} — Run C-9 P5 parallax panel by OUTPAINTING (Matt R-C9-21). task_id \"{bid}\".\n\n{geom}\nIMAGE 1 is the canvas to EDIT: " + '; '.join(kept)
            + f" are ALREADY PAINTED (real pixels from neighbouring panels); the rest is {fill} placeholder. Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 image: keep the painted strips as they are and replace the placeholder with painting that CONTINUES them seamlessly (no visible join), following the layer description for this panel's position"
            + (" — any flat pure #00ff00 in the painted strips continues as flat pure #00ff00." if d['key'] else ".") + "\n" + reg)
else:
    text = (f"GENERATE BURST {bid} — Run C-9 P5 parallax panel, the FIRST panel of its layer (Matt R-C9-21). task_id \"{bid}\".\n\n{geom}\nIMAGE 1 is a {fill} placeholder canvas of the right size; paint the whole panel. Deliver ONE LANDSCAPE 1536x1024 image of this panel.\n" + reg)
refs = [{"path": str(cp), "role": "IMAGE 1 — the canvas to EDIT (painted neighbour strips + placeholder)"},
        {"path": str(ANCHOR), "role": "IMAGE 2 — the approved painted STYLE of this level (line, hatching, washes; not its layout)"}]
if d['ref']: refs.append({"path": str(REF/d['ref']), "role": f"IMAGE {len(refs)+1} — manuscript page: how this subject is painted (not its layout, figures or text)"})
if d['c3']:
    cc, rr = d['c3'][1](c, r); c3p = C3A/f"L-{d['c3'][0]}-{cc}_{rr}"/f"L-{d['c3'][0]}-{cc}_{rr}.png"
    refs.append({"path": str(c3p), "role": f"IMAGE {len(refs)+1} — GEOMETRY-ONLY: the approved SCALE and DISTANCE for this part of the layer (how small and far things are, where the horizon sits); a different style and subject — copy NOTHING else"})
text += (f"\n\nOne image_gen call. ONE retry only if a painted strip was altered, a join remains, the layer contains a cliff rim/characters/text, or (keyed layers) the area above the silhouette is not flat pure #00ff00 — name the reason. "
         f"Copy the output from $CODEX_HOME/generated_images/... to out/{i}.png with sha256. No code. No other files. No web.\nRETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20, "outputs": [f"out/{i}.png"], "effort": "high", "add_dirs": [], "experiment": "P5-parallax-L10"},
          open(B/'briefs'/'C-9'/f'{bid}.task.json', 'w'), indent=1, ensure_ascii=False)
print(bid, 'brief ok')
