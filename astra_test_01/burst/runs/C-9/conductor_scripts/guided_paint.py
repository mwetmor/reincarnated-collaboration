# C-9 generic guided layer painter (generalises forest_paint.py). usage: guided_paint.py <cfg.json> ready | stage <c_r> | brief <c_r>
# A conductor LAYOUT GUIDE fixes where every landmark, fire and river is, so nothing can repeat across panels (Matt R-C9-21/29).
import json, sys, pathlib, hashlib, os
from PIL import Image
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A9 = B/'runs/C-9/artifacts'; S = A9/'CS9-guides'
cfg = json.load(open(sys.argv[1])); P = cfg['prefix']; GUIDE = Image.open(cfg['guide']).convert('RGB'); COLS, ROWS = cfg['cols'], cfg['rows']
ORDER = [(c, r) for r in range(ROWS) for c in range(COLS)]
def src(k):
    for d in (f'{P}-{k}-r1', f'{P}-{k}'):
        p = A9/d/f'{P}-{k}.png'
        if p.exists(): return p
done = lambda k: src(k) is not None
def manifest_add(p):
    m = S/'manifest.json'; d = json.loads(m.read_text()) if m.exists() else {}
    d[p.name] = hashlib.sha256(p.read_bytes()).hexdigest(); m.write_text(json.dumps(d, indent=1))
cmd = sys.argv[2]
if cmd == 'ready':
    out = []
    for c, r in ORDER:
        k = f'{c}_{r}'
        if done(k): continue
        need = ([f'{c-1}_{r}'] if c else []) + ([f'{c}_{r-1}'] if r else []) + ([f'{c+1}_{r-1}'] if r and c + 1 < COLS else [])
        if all(done(n) for n in need): out.append(k)
    print(' '.join(out)); sys.exit()
k = sys.argv[3]; c, r = map(int, k.split('_')); ox, oy = c * 1280, r * 768; SUF = os.environ.get('SUF', '')
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
cp = S/f'{P}-{k}{SUF}_canvas.png'
if cmd == 'stage': canvas.save(cp); manifest_add(cp); print(k, 'staged', kept); sys.exit()
bid = f'{P}-{k}{SUF}'; geo = cfg['geo']; rules = cfg['rules']
RUN_TAG = cfg.get('run_tag', 'Run C-9 P5'); RULING = cfg.get('ruling', 'Matt R-C9-29')
FILL = cfg.get('fill_phrase', 'replace every flat guide colour with painting')
RETRY_EXTRA = cfg.get('retry_extra', 'the sky area is not flat pure #00ff00, '); UNPAINTED = cfg.get('unpainted_phrase', 'guide colours remain unpainted')
head = f"GENERATE BURST {bid} — {RUN_TAG}, {cfg['name']} panel {k} over a conductor LAYOUT GUIDE ({RULING}). task_id \"{bid}\".\n\n"
if kept:
    text = head + "IMAGE 1 is the canvas to EDIT (1536x1024): " + '; '.join(kept) + " are ALREADY PAINTED (real pixels from neighbouring panels); in the rest, " + geo + "\nUse image_gen in EDIT mode on IMAGE 1: keep the painted strips as they are and " + FILL + " that CONTINUES them seamlessly (no visible join). " + rules
else:
    text = head + "IMAGE 1 is the canvas to EDIT (1536x1024): " + geo + "\nUse image_gen in EDIT mode on IMAGE 1 and " + FILL + ". " + rules
refs = [{"path": str(cp), "role": "IMAGE 1 — the canvas to EDIT (painted neighbour strips + layout guide)"}] + [{"path": p, "role": f"IMAGE {i+2} — {role}"} for i, (p, role) in enumerate(cfg['refs'])]
text += (f"\n\nOne image_gen EDIT call. ONE retry only if a painted strip was altered, a join remains, anything appears that the guide does not put there (an extra landmark, fire, river or any town), {RETRY_EXTRA}or {UNPAINTED} — name the reason. "
         f"Copy the output to out/{P}-{k}.png with sha256. No code. No other files. No web.\nRETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20, "outputs": [f"out/{P}-{k}.png"], "effort": "high", "add_dirs": [], "experiment": cfg['experiment']},
          open(B/'briefs'/'C-9'/f'{bid}.task.json', 'w'), indent=1, ensure_ascii=False)
print(bid, 'brief ok')
