# C-9 P5 parallax driver (ported from runs/C-3/conductor_scripts/layer_paint.py; grid geometry unchanged).
# usage: layer_paint_c9.py ready | stage <id> | brief <id>     ids: L9-<layer>-<c>_<r>
# Content = Matt R-C9-13 (manuscript sky; far valley + domed temple + cathedral on its crag; manuscript forest; mist).
import json, sys, pathlib, hashlib
from PIL import Image
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A9 = B/'runs/C-9/artifacts'; S = A9/'CS9-guides'; S.mkdir(parents=True, exist_ok=True); REF = A9/'refs'
ANCHOR = A9/'S1-ink/S1-ink_b.png'
LAY = {
 'sky': dict(cols=2, rows=1, bg=(128, 128, 128), key=False, ref='trh-06-june-sainte-chapelle.jpg',
   desc="the MANUSCRIPT SKY layer, the farthest backdrop: a sky painted as a Book of Hours paints it — deep LAPIS BLUE at the top, lightening through softer blue to a band of PALE GOLD and cream at the horizon near the bottom (evening light, NOT a dramatic sunset: no orange blaze, no sun disc, no rays); a few small stylised clouds drawn with a pen line and a soft uneven wash; a scatter of tiny gold stars in the upper blue. NO land at all.",
   part=lambda c, r: ["the LEFT half", "the RIGHT half"][c]),
 'far': dict(cols=2, rows=2, bg=(128, 128, 128), key=True, ref='trh-09-september-saumur.jpg',
   desc="the FAR layer, painted as a Book of Hours calendar landscape: a wide distant VALLEY with a winding river, rolling hills in soft greens and ochres turning blue-grey with distance. On a hill toward the LEFT stands the Keepers' DOMED TEMPLE — a pale stone round temple with a shallow dome and a ring of columns, intact and serene, a touch of gold on the dome. Far to the RIGHT, on a steep rocky crag, a Gothic CATHEDRAL with a tall spire and a rose window, a thin column of grey smoke rising from its roof. The LAND's top silhouette (hilltops, the temple, the crag and the cathedral spire) sits at about 38–48 % of the full layer's height; EVERYTHING ABOVE that silhouette is flat pure #00ff00 (the sky layer shows there); below it the land is fully painted down to the bottom edge, hazier and simpler toward the bottom.",
   part=lambda c, r: [["upper-left (mostly green; the temple's dome and hilltops rise into the bottom of this panel)", "upper-right (mostly green; the crag and the cathedral spire rise into the bottom of this panel)"],
                      ["lower-left (the domed temple on its hill, the valley below)", "lower-right (the cathedral on its crag, the river winding below)"]][r][c]),
 'forest': dict(cols=3, rows=2, bg=(128, 128, 128), key=True, ref='trh-05-may-forest.jpg',
   desc="the MID FOREST layer, nearer than the far valley: a band of MANUSCRIPT FOREST filling the valley — rounded tree crowns painted in dabs of green with some ochre and a few red-brown, dark trunks, small meadows with tiny flowers and a stretch of the river between the trees, as a Book of Hours paints woodland. Its top silhouette (the line of treetops) sits at about 25–32 % of the full layer's height; EVERYTHING ABOVE that silhouette is flat pure #00ff00; below it the forest fills everything down to the bottom edge, denser toward the bottom.",
   part=lambda c, r: [["upper-left", "upper-middle", "upper-right"], ["lower-left", "lower-middle (the river bends here)", "lower-right"]][r][c]),
 'mist': dict(cols=2, rows=2, bg=(0, 0, 0), key=False, ref=None,
   desc="the MIST layer: soft drifting banks of pale mist painted as LIGHT on a PURE BLACK background (black = fully transparent in the game, brighter = more opaque mist): cream and pale blue-grey washes with soft, uneven watercolor edges. Thin and wispy in the upper half, thickening into low banks toward the bottom. No land, no trees, no sky colour on the black.",
   part=lambda c, r: [["upper-left (thin wisps)", "upper-right (thin wisps)"], ["lower-left (low banks)", "lower-right (low banks)"]][r][c]),
}
pid = lambda l, c, r: f'L9-{l}-{c}_{r}'
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
       + ("IMAGE 3 is a manuscript page: take from it how a Book of Hours paints this kind of subject (palette, simplification, the way distance is painted); not its layout, figures or text. " if d['ref'] else "")
       + "No characters, creatures, text, UI, border or vignette.")
if kept:
    text = (f"GENERATE BURST {bid} — Run C-9 P5 parallax panel by OUTPAINTING (Matt R-C9-13). task_id \"{bid}\".\n\n{geom}\nIMAGE 1 is the canvas to EDIT: " + '; '.join(kept)
            + f" are ALREADY PAINTED (real pixels from neighbouring panels); the rest is {fill} placeholder. Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 image: keep the painted strips as they are and replace the placeholder with painting that CONTINUES them seamlessly (no visible join), following the layer description for this panel's position"
            + (" — any flat pure #00ff00 in the painted strips continues as flat pure #00ff00." if d['key'] else ".") + "\n" + reg)
else:
    text = (f"GENERATE BURST {bid} — Run C-9 P5 parallax panel, the FIRST panel of its layer (Matt R-C9-13). task_id \"{bid}\".\n\n{geom}\nIMAGE 1 is a {fill} placeholder canvas of the right size; paint the whole panel. Deliver ONE LANDSCAPE 1536x1024 image of this panel.\n" + reg)
refs = [{"path": str(cp), "role": "IMAGE 1 — the canvas to EDIT (painted neighbour strips + placeholder)"},
        {"path": str(ANCHOR), "role": "IMAGE 2 — the approved painted STYLE of this level (line, hatching, washes; not its layout)"}]
if d['ref']: refs.append({"path": str(REF/d['ref']), "role": "IMAGE 3 — manuscript page: how this subject is painted (not its layout, figures or text)"})
text += (f"\n\nOne image_gen call. ONE retry only if a painted strip was altered, a join remains, the layer contains a cliff rim/characters/text, or (keyed layers) the area above the silhouette is not flat pure #00ff00 — name the reason. "
         f"Copy the output from $CODEX_HOME/generated_images/... to out/{i}.png with sha256. No code. No other files. No web.\nRETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20, "outputs": [f"out/{i}.png"], "effort": "high", "add_dirs": [], "experiment": "P5-parallax"},
          open(B/'briefs'/'C-9'/f'{bid}.task.json', 'w'), indent=1, ensure_ascii=False)
print(bid, 'brief ok')
