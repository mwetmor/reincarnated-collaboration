# C-9 generic guided layer painter (generalises forest_paint.py). usage: guided_paint.py <cfg.json> ready | stage <c_r> | brief <c_r>
# A conductor LAYOUT GUIDE fixes where every landmark, fire and river is, so nothing can repeat across panels (Matt R-C9-21/29).
import json, sys, pathlib, hashlib, os
from PIL import Image
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A9 = B/'runs/C-9/artifacts'; S = A9/'CS9-guides'
cfg = json.load(open(sys.argv[1])); P = cfg['prefix']; GUIDE = Image.open(cfg['guide']).convert('RGB'); COLS, ROWS = cfg['cols'], cfg['rows']
ORDER = [(c, r) for r in range(ROWS) for c in range(COLS)]
def src(k):
    for s_ in cfg.get('src_suffixes', []):   # BV2F R-C9-295: later repaints (cfg src_suffixes, e.g. ['-r3', '-r2']) tried first; absent = v1
        if (A9/f'{P}-{k}{s_}'/f'{P}-{k}.png').exists(): return A9/f'{P}-{k}{s_}'/f'{P}-{k}.png'   # BV2F
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
# BV2F-BEGIN DEV-28 (R-C9-257 (c)): GUIDE SHADOW SMOOTHING before the canvas is cut (stage only; brief never reads pixels).
# BV2F_DEV28=1 fills and softens the renderer's PCF shadow dither (fid/v1tools/dev28.py), guarded by the guide's own ID render
# cfg['dev28_ids'] (sha-pinned in cfg['dev28_ids_sha256']); unset = v1's guide byte for byte.
if os.environ.get('BV2F_DEV28') == '1' and cmd == 'stage':
    _ids = pathlib.Path(cfg['dev28_ids'])
    if hashlib.sha256(_ids.read_bytes()).hexdigest() != cfg['dev28_ids_sha256']:
        sys.exit('DEV-28 HALT: %s is not the pinned ID render' % _ids)
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); import dev28
    GUIDE, _rep = dev28.smooth(GUIDE, Image.open(_ids)); print('DEV-28', json.dumps(_rep))
# BV2F-END
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
# BV2F-BEGIN DEV-29 (R-C9-299): CONTEXT PATCH. DEV-24 repairs the PAINTING after the stitch, so a pilot canvas pasted as
# context still carries the pre-repair geometry. With cfg['context_patch'] = {"painting": the DEV-24-patched painting
# (plate px), "painting_sha256", "mask": a plate-px PNG of the patches' support, "mask_sha256"}, every PASTED canvas
# pixel inside the mask is replaced by the patched painting's pixel; pasted pixels outside it, and all unpasted pixels,
# are untouched. Absent = v1's canvas byte for byte.
if cfg.get('context_patch') and kept:
    _cp = cfg['context_patch']
    for _f, _s in ((_cp['painting'], _cp['painting_sha256']), (_cp['mask'], _cp['mask_sha256'])):
        if hashlib.sha256(pathlib.Path(_f).read_bytes()).hexdigest() != _s:
            sys.exit('DEV-29 HALT: %s is not the pinned file' % _f)
    import numpy as _np
    _PP = _np.asarray(Image.open(_cp['painting']).convert('RGB')); _MM = _np.asarray(Image.open(_cp['mask'])) > 127
    _pz = _np.zeros((1024, 1536), bool)
    for (nc, nr) in [(c-1, r), (c, r-1), (c+1, r-1), (c-1, r-1)]:
        if nc < 0 or nr < 0 or nc >= COLS or not done(f'{nc}_{nr}'): continue
        dx, dy = (nc - c) * 1280, (nr - r) * 768
        _pz[max(0, dy):min(1024, dy + 1024), max(0, dx):min(1536, dx + 1536)] = True
    _sub = _np.zeros((1024, 1536), bool); _src = _np.zeros((1024, 1536, 3), _np.uint8)
    _x1, _y1 = min(ox + 1536, _MM.shape[1], _PP.shape[1]), min(oy + 1024, _MM.shape[0], _PP.shape[0])
    if _x1 > ox and _y1 > oy:
        _sub[:_y1 - oy, :_x1 - ox] = _MM[oy:_y1, ox:_x1]; _src[:_y1 - oy, :_x1 - ox] = _PP[oy:_y1, ox:_x1]
    _sub &= _pz
    _a = _np.asarray(canvas).copy(); _a[_sub] = _src[_sub]; canvas = Image.fromarray(_a)
    print(k, 'DEV-29 context patch px', int(_sub.sum()))
# BV2F-END
# BV2F-BEGIN DEV-25c (R-C9-278): INNER-128 PASTE. For a chunk listed in cfg['dev25c_chunks'] with BV2F_DEV25C=1, only the
# 128 px of each painted overlap next to the canvas EDGE are kept as pasted context (columns 0..127 under a painted left
# neighbour, rows 0..127 under a painted top / top-left / top-right neighbour): PH's half E. The rest of v1's 256-px
# strip goes back to the GUIDE, so the chunk paints it itself (half C, where the stitch's cut then runs between two fresh
# paints). The brief names 128-px strips. Unset = v1's canvas and brief.
if os.environ.get('BV2F_DEV25C') == '1' and k in cfg.get('dev25c_chunks', []):
    import numpy as _np
    _g = _np.asarray(GUIDE.crop((ox, oy, ox + 1536, oy + 1024)))
    _a = _np.asarray(canvas).copy()
    _left = c > 0 and done(f'{c-1}_{r}')
    _top = r > 0 and any(0 <= c + d < COLS and done(f'{c+d}_{r-1}') for d in (-1, 0, 1))
    _inner = _np.zeros((1024, 1536), bool)
    if _left: _inner[:, :128] = True
    if _top: _inner[:128, :] = True
    _pasted = _np.zeros((1024, 1536), bool)
    if _left: _pasted[:, :256] = True
    if _top: _pasted[:256, :] = True
    _a[_pasted & ~_inner] = _g[_pasted & ~_inner]
    canvas = Image.fromarray(_a)
    kept = [s_.replace('256x256', '128x128').replace('256', '128') for s_ in kept]
    print(k, 'DEV-25c inner-128: pasted px', int((_pasted & _inner).sum()), 'returned to the guide', int((_pasted & ~_inner).sum()))
# BV2F-END
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
if cfg.get('chunk_notes', {}).get(k): text += "\n\n" + cfg['chunk_notes'][k]   # BV2F DEV-10: per-chunk notes generated from the ID render (fid/pt/tools/chunk_notes.py); absent = v1 brief
refs = [{"path": str(cp), "role": "IMAGE 1 — the canvas to EDIT (painted neighbour strips + layout guide)"}] + [{"path": p, "role": f"IMAGE {i+2} — {role}"} for i, (p, role) in enumerate(cfg['refs'])]
text += (f"\n\nOne image_gen EDIT call. ONE retry only if a painted strip was altered, a join remains, anything appears that the guide does not put there (an extra landmark, fire, river or any town), {RETRY_EXTRA}or {UNPAINTED} — name the reason. "
         f"Copy the output to out/{P}-{k}.png with sha256. No code. No other files. No web.\nRETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20, "outputs": [f"out/{P}-{k}.png"], "effort": "high", "add_dirs": [], "experiment": cfg['experiment']},
          open(B/'briefs'/'C-9'/f'{bid}.task.json', 'w'), indent=1, ensure_ascii=False)
print(bid, 'brief ok')
