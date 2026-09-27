# C-9 P5 forest layer painted over a conductor LAYOUT GUIDE (one river, three fires) so nothing can repeat (Matt R-C9-21).
# usage: forest_paint.py ready | stage <c_r> | brief <c_r>   ids FG10-<c>_<r>; grid 3x3 of 1536x1024, step 1280x768, over 4096x2560.
import json, sys, pathlib, hashlib, os
from PIL import Image
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A9 = B/'runs/C-9/artifacts'; G = A9/'FG10'; S = A9/'CS9-guides'
GUIDE = Image.open(G/'forest_guide.png').convert('RGB'); COLS, ROWS = 3, 3
ORDER = [(c, r) for r in range(ROWS) for c in range(COLS)]
def src(k):
    for d in (f'FG10-{k}-r1', f'FG10-{k}'):
        p = A9/d/f'FG10-{k}.png'
        if p.exists(): return p
done = lambda k: src(k) is not None
def manifest_add(p):
    m = S/'manifest.json'; d = json.loads(m.read_text()) if m.exists() else {}
    d[p.name] = hashlib.sha256(p.read_bytes()).hexdigest(); m.write_text(json.dumps(d, indent=1))
cmd = sys.argv[1]
if cmd == 'ready':
    out = []
    for c, r in ORDER:
        k = f'{c}_{r}'
        if done(k): continue
        need = ([f'{c-1}_{r}'] if c else []) + ([f'{c}_{r-1}'] if r else []) + ([f'{c+1}_{r-1}'] if r and c + 1 < COLS else [])
        if all(done(n) for n in need): out.append(k)
    print(' '.join(out)); sys.exit()
k = sys.argv[2]; c, r = map(int, k.split('_')); ox, oy = c * 1280, r * 768; SUF = os.environ.get('SUF', '')
canvas = GUIDE.crop((ox, oy, ox + 1536, oy + 1024)); kept = []
for (nc, nr) in [(c-1, r), (c, r-1), (c+1, r-1), (c-1, r-1)]:
    if nc < 0 or nr < 0 or nc >= COLS: continue
    n = f'{nc}_{nr}'
    if not done(n): continue
    im = Image.open(src(n)).convert('RGB'); dx, dy = (nc - c) * 1280, (nr - r) * 768
    x0, y0 = max(0, dx), max(0, dy); x1, y1 = min(1536, dx + 1536), min(1024, dy + 1024)
    if x1 > x0 and y1 > y0:
        canvas.paste(im.crop((x0 - dx, y0 - dy, x1 - dx, y1 - dy)), (x0, y0))
        kept.append({(-1, 0): 'its LEFT 256 columns', (0, -1): 'its TOP 256 rows', (1, -1): 'its top-right 256x256 corner', (-1, -1): 'its top-left 256x256 corner'}[(nc - c, nr - r)])
cp = S/f'FG10-{k}{SUF}_canvas.png'
if cmd == 'stage': canvas.save(cp); manifest_add(cp); print(k, 'staged', kept); sys.exit()
bid = f'FG10-{k}{SUF}'
geo = ("the flat colours are a LAYOUT GUIDE: DARK GREEN = dense manuscript forest seen from high above and far away (tiny tree crowns, a few pixels to about 20 px across, dabs of green with some ochre and red-brown, dark trunks); LIGHT OLIVE = an open meadow or field (each a different shape, tiny flowers); LIGHT BLUE line = the ONE river, catching the sunset (paint it exactly where the line runs, same width); ORANGE disc in a DARK ring = a forest FIRE — orange flames, burnt black ground around it, a column of smoke drifting up (paint a fire ONLY where a disc is, at that size); PURE GREEN #00ff00 = empty sky above the treeline (keep it flat pure #00ff00, with a clean treetop edge).")
rules = ("Follow the guide EXACTLY: no river, fire, meadow or clearing anywhere the guide does not put one; NOTHING repeats — no two clumps, meadows or fires alike. "
         "STYLE: the REGISTER CARD above; IMAGE 2 shows the painted look and tree scale to match (NOT its layout — it has extra rivers and fires that must NOT appear here). No characters, text, UI, border.")
if kept:
    text = (f"GENERATE BURST {bid} — Run C-9 P5, forest layer panel {k} by OUTPAINTING over a layout guide (Matt R-C9-21: nothing may repeat). task_id \"{bid}\".\n\n"
            "IMAGE 1 is the canvas to EDIT (1536x1024): " + '; '.join(kept) + " are ALREADY PAINTED (real pixels from neighbouring panels); in the rest, " + geo + "\n"
            "Use image_gen in EDIT mode on IMAGE 1: keep the painted strips as they are and replace every flat guide colour with painting that CONTINUES them seamlessly (no visible join). " + rules)
else:
    text = (f"GENERATE BURST {bid} — Run C-9 P5, forest layer panel {k} painted over a layout guide (Matt R-C9-21: nothing may repeat). task_id \"{bid}\".\n\n"
            "IMAGE 1 is the canvas to EDIT (1536x1024): " + geo + "\nUse image_gen in EDIT mode on IMAGE 1 and replace every flat guide colour with painting. " + rules)
refs = [{"path": str(cp), "role": "IMAGE 1 — the canvas to EDIT (painted neighbour strips + layout guide)"},
        {"path": str(A9/'L10-forest-1_1'/'L10-forest-1_1.png'), "role": "IMAGE 2 — painted look and tree scale ONLY (not its layout: its extra rivers and fires must not appear)"}]
text += (f"\n\nOne image_gen EDIT call. ONE retry only if a painted strip was altered, a join remains, a river/fire appears where the guide has none, the sky area is not flat pure #00ff00, or guide colours remain unpainted — name the reason. "
         f"Copy the output to out/FG10-{k}.png with sha256. No code. No other files. No web.\nRETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20, "outputs": [f"out/FG10-{k}.png"], "effort": "high", "add_dirs": [], "experiment": "P5-forest-guided"},
          open(B/'briefs'/'C-9'/f'{bid}.task.json', 'w'), indent=1, ensure_ascii=False)
print(bid, 'brief ok')
