#!/usr/bin/env python3
"""barrow_v2 paint lane (BVP, drax): guided chunk painter = conductor_scripts/guided_paint.py, unchanged in
method (1536 x 1024 canvas, 1280 x 768 stride, painted neighbour strips pasted into the canvas, one EDIT
call per chunk), extended by ONE thing: chunks the frame SKIPS (wholly outside the screen envelope,
paint/frame_bvp.json) count as done and paste nothing.

    bvp_paint.py <cfg.json> ready | stage <c_r> | brief <c_r> | status
SUF env var as in guided_paint.py (-r1, -r2 for retries).
"""
import json, sys, pathlib, hashlib, os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A9 = B/'runs/C-9/artifacts'; S = A9/'CS9-guides'
cfg = json.load(open(sys.argv[1])); P = cfg['prefix']; GUIDE = Image.open(cfg['guide']).convert('RGB'); COLS, ROWS = cfg['cols'], cfg['rows']
SKIP = set(cfg.get('skip', []))
ORDER = [(c, r) for r in range(ROWS) for c in range(COLS)]
def src(k):
    for d in (f'{P}-{k}-r3', f'{P}-{k}-r2', f'{P}-{k}-r1', f'{P}-{k}'):
        p = A9/d/f'{P}-{k}.png'
        if p.exists(): return p
# a chunk is ACCEPTED when its painted file exists and is not listed in cfg['rejected'] (a reviewed miss)
done = lambda k: k in SKIP or src(k) is not None
def manifest_add(p):
    m = S/'manifest.json'; d = json.loads(m.read_text()) if m.exists() else {}
    d[p.name] = hashlib.sha256(p.read_bytes()).hexdigest(); m.write_text(json.dumps(d, indent=1))
cmd = sys.argv[2]
if cmd == 'status':
    todo = [f'{c}_{r}' for c, r in ORDER if not done(f'{c}_{r}')]
    print(json.dumps({'painted': sum(1 for c, r in ORDER if src(f'{c}_{r}')), 'skipped': len(SKIP), 'todo': len(todo)})); sys.exit()
if cmd == 'ready':
    ONLY = set(os.environ.get('ONLY', '').split()) or None    # a test block: paint only these, in their own dependency order
    out = []
    for c, r in ORDER:
        k = f'{c}_{r}'
        if done(k) or (ONLY and k not in ONLY): continue
        need = ([f'{c-1}_{r}'] if c else []) + ([f'{c}_{r-1}'] if r else []) + ([f'{c+1}_{r-1}'] if r and c + 1 < COLS else [])
        if ONLY: need = [n for n in need if n in ONLY]
        if all(done(n) for n in need): out.append(k)
    print(' '.join(out)); sys.exit()
k = sys.argv[3]; c, r = map(int, k.split('_')); ox, oy = c * 1280, r * 768; SUF = os.environ.get('SUF', '')
assert k not in SKIP, f'{k} is a skipped chunk'
canvas = GUIDE.crop((ox, oy, ox + 1536, oy + 1024)); kept = []
# every PAINTED neighbour is pasted (the eight around it): a test block painted first is then honoured by the
# chunks painted around it later, on its right and bottom edges too
for (nc, nr) in [(c-1, r), (c, r-1), (c+1, r-1), (c-1, r-1), (c+1, r), (c, r+1), (c-1, r+1), (c+1, r+1)]:
    if nc < 0 or nr < 0 or nc >= COLS or nr >= ROWS: continue
    n = f'{nc}_{nr}'
    if n in SKIP or not done(n): continue
    im = Image.open(src(n)).convert('RGB'); dx, dy = (nc - c) * 1280, (nr - r) * 768
    x0, y0 = max(0, dx), max(0, dy); x1, y1 = min(1536, dx + 1536), min(1024, dy + 1024)
    if x1 > x0 and y1 > y0:
        canvas.paste(im.crop((x0 - dx, y0 - dy, x1 - dx, y1 - dy)), (x0, y0))
        kept.append({(-1, 0): 'its LEFT 256 columns', (0, -1): 'its TOP 256 rows', (1, -1): 'its top-right 256x256 corner', (-1, -1): 'its top-left 256x256 corner',
                     (1, 0): 'its RIGHT 256 columns', (0, 1): 'its BOTTOM 256 rows', (-1, 1): 'its bottom-left 256x256 corner', (1, 1): 'its bottom-right 256x256 corner'}[(nc - c, nr - r)])
cp = S/f'{P}-{k}{SUF}_canvas.png'
# R-C9-154: a DETAIL of sketch A around this panel's place in the site, enlarged toward the panel's scale, so the
# painter matches sketch A's DENSITY of ground cover. Sketch A is not to scale: its place is found by inverse-distance
# interpolation between the six anchors + the start, read off the spawn plan (sites/BV3r2-A_spawns.png).
SKA = cfg.get('sketch_detail')
dp = S/f'{P}-{k}{SUF}_skA.png'
def sketch_detail():
    import math
    sk = Image.open(SKA['image']).convert('RGB'); fr = json.load(open(SKA['frame']))
    Pp = fr['px_per_m']; X0, Y0 = fr['origin_px']; a = math.radians(fr['pitch_deg'])
    cx = (ox + 768 - X0) / Pp; cy = (oy + 512 - Y0) / (Pp * math.sin(a))
    ws = [(1.0 / ((cx - q[0]) ** 2 + (cy - q[1]) ** 2 + 4.0), q) for q in SKA['ties']]
    tw = sum(w for w, _ in ws)
    u = sum(w * q[2] for w, q in ws) / tw; v = sum(w * q[3] for w, q in ws) / tw
    cw, ch = SKA['crop_px']
    u = min(max(u, cw / 2), sk.width - cw / 2); v = min(max(v, ch / 2), sk.height - ch / 2)
    return sk.crop((int(u - cw / 2), int(v - ch / 2), int(u + cw / 2), int(v + ch / 2))).resize((1536, 1024), Image.LANCZOS)
if cmd == 'stage':
    canvas.save(cp); manifest_add(cp)
    if SKA: sketch_detail().save(dp); manifest_add(dp)
    print(k, 'staged', kept); sys.exit()
bid = f'{P}-{k}{SUF}'; geo = cfg['geo']; rules = cfg['rules']
# per-chunk notes: which named pieces fall in this chunk (cfg['chunk_notes'][k]), so the painter knows what it is looking at
note = cfg.get('chunk_notes', {}).get(k, '')
RUN_TAG = cfg.get('run_tag', 'Run C-9 Phase 2'); RULING = cfg.get('ruling', 'R-C9-145')
FILL = cfg.get('fill_phrase', 'replace every flat guide colour with painting')
RETRY_EXTRA = cfg.get('retry_extra', ''); UNPAINTED = cfg.get('unpainted_phrase', 'guide colours remain unpainted')
head = f"GENERATE BURST {bid} — {RUN_TAG}, {cfg['name']} panel {k} over a LAYOUT GUIDE ({RULING}). task_id \"{bid}\".\n\n"
where = (f"\nTHIS PANEL: {note}\n" if note else "\n")
if kept:
    text = head + "IMAGE 1 is the canvas to EDIT (1536x1024): " + '; '.join(kept) + " are ALREADY PAINTED (real pixels from neighbouring panels); in the rest, " + geo + where + "Use image_gen in EDIT mode on IMAGE 1: keep the painted strips as they are and " + FILL + " that CONTINUES them seamlessly (no visible join). " + rules
else:
    text = head + "IMAGE 1 is the canvas to EDIT (1536x1024): " + geo + where + "Use image_gen in EDIT mode on IMAGE 1 and " + FILL + ". " + rules
refs = [{"path": str(cp), "role": "IMAGE 1 — the canvas to EDIT (painted neighbour strips + layout guide)"}] + [{"path": p, "role": f"IMAGE {i+2} — {role}"} for i, (p, role) in enumerate(cfg['refs'])]
if SKA: refs.append({"path": str(dp), "role": f"IMAGE {len(refs)+1} — " + SKA['role']})
text += (f"\n\nOne image_gen EDIT call. ONE retry only if a painted strip was altered, a join remains, anything appears that the guide does not put there (an extra building, landmark, ship, figure or creature), {RETRY_EXTRA}or {UNPAINTED} — name the reason. "
         f"Copy the output to out/{P}-{k}.png with sha256. No code. No other files. No web.\nRETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20, "outputs": [f"out/{P}-{k}.png"], "effort": "high", "add_dirs": [], "experiment": cfg['experiment']},
          open(B/'briefs'/'C-9'/f'{bid}.task.json', 'w'), indent=1, ensure_ascii=False)
print(bid, 'brief ok')
