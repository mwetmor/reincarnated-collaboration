# C-9 P5 conductor driver for the cliffside v4 chunk grid (ported from runs/C-3/conductor_scripts/grid_paint_v4.py).
# usage: grid_paint_c9.py ready | stage <cx_cy> | brief <cx_cy>
# Geometry (guides, dependency order) is C-3's v4.1 grid, unchanged. Style = the C-9 register card (prepended by the lane)
# + the M1 anchor S1-ink_b. Every staged canvas is recorded by sha in CS9-guides/manifest.json for refs_guard.
import json, sys, pathlib, hashlib, os
from PIL import Image
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
G3 = B/'runs/C-3/artifacts/CS-guides-v4'
A9 = B/'runs/C-9/artifacts'; S = A9/'CS9-guides'; S.mkdir(parents=True, exist_ok=True)
ANCHOR = A9/'S1-ink/S1-ink_b.png'
TRH = A9/'refs/trh-07-july-bridge.jpg'
J = json.load(open(G3/'chunks_v4.json'))
CH = {}
for e in J['paint_order']:
    k = f"{e['index'][0]}_{e['index'][1]}"
    CH[k] = {'origin': e['origin_px'], 'guide': G3/f"chunk_{e['index'][0]}_{e['index'][1]}_guide.png",
             'after': [a['chunk'].replace('chunk_', '') for a in e['paint_after']] + [a['chunk'].replace('chunk_', '') for a in e['corner_overlaps_already_painted']],
             'step': e['step']}
SUF = os.environ.get('SUF', '')

def src(k):
    for d in (f'CS9-{k}-r1', f'CS9-{k}'):
        p = A9/d/f'chunk_{k}.png'
        if p.exists(): return p
    return None
done = lambda k: src(k) is not None

def manifest_add(p):
    m = S/'manifest.json'; d = json.loads(m.read_text()) if m.exists() else {}
    d[p.name] = hashlib.sha256(p.read_bytes()).hexdigest(); m.write_text(json.dumps(d, indent=1))

cmd = sys.argv[1]
if cmd == 'ready':
    print(' '.join(k for k, c in sorted(CH.items(), key=lambda kv: kv[1]['step']) if not done(k) and all(done(n) for n in c['after'])))
    sys.exit()
k = sys.argv[2]; c = CH[k]; ox, oy = c['origin']
canvas = Image.open(c['guide']).convert('RGB'); kept = set()
for n, nc in CH.items():
    if n == k or not done(n): continue
    nx, ny = nc['origin']
    x0, y0 = max(ox, nx), max(oy, ny); x1, y1 = min(ox + 1536, nx + 1536), min(oy + 1024, ny + 1024)
    if x1 <= x0 or y1 <= y0: continue
    canvas.paste(Image.open(src(n)).convert('RGB').crop((x0 - nx, y0 - ny, x1 - nx, y1 - ny)), (x0 - ox, y0 - oy))
    side = ('LEFT' if nx < ox and ny == oy else 'TOP' if ny < oy and nx == ox else 'corner')
    kept.add({'LEFT': 'the LEFT 256 columns (from the chunk to its left)', 'TOP': 'the TOP 256 rows (from the chunk above)',
              'corner': 'a 256x256 corner square (from a diagonal neighbour)'}[side])
kept = sorted(kept)
if cmd == 'stage':
    p = S/f'chunk_{k}_canvas{SUF}.png'; canvas.save(p); manifest_add(p); print(k, 'staged', kept); sys.exit()

bid = f'CS9-{k}{SUF}'
geo = ("OLIVE GREEN = grassy ground on the cliff top (manuscript grass tufts, moss, small flowers, bare rock patches; NO boulders, NO props); "
       "TAN = a worn pale beaten-earth path/clearing inside the grass, the BRIGHTEST and CALMEST area (a few pebbles and faint ruts only), its edges soft, earth breaking into grass; "
       "LIGHT GREY band = the rocky verge right at the rim; GREY planes (dark grey with lighter ribs) = cliff faces dropping toward the viewer: stylised stacked manuscript rock, "
       "faceted blocks in warm ochre and grey modelled with pen hatching and a second wash, continuous all the way down to where they meet the green, slightly hazier toward their lowest part, "
       "no ledge or bottom edge drawn; BROWN planks + posts = a wooden bridge deck; MAGENTA plank = one loose bridge plank (a cracked, loose plank); PURE GREEN #00ff00 = empty void")
style = ("Orthographic view: no perspective shrinking toward the top. Scale: a person standing here is 130 px tall. "
         "STYLE: the REGISTER CARD above, matched to IMAGE 2 (the approved painted style of this level: same line, hatching, washes and palette). "
         "ACCENTS: as on a manuscript page (IMAGE 3 shows how), put rich colour in small places OFF the path: clusters of wildflowers (vermilion, lapis, white, gold) in the grass and along the verge, "
         "a little verdigris moss and ochre lichen on the rock; the path itself stays calm and pale. "
         "No characters, creatures, text, UI, border or vignette.")
if kept:
    text = (f"GENERATE BURST {bid} — Run C-9 P5, cliffside chunk {k} by OUTPAINTING (the C-3 v4.1 grid; Matt M1 R-C9-8/9). task_id \"{bid}\".\n\n"
            "IMAGE 1 is the canvas to EDIT (1536x1024). In it, " + '; '.join(kept) + " are ALREADY PAINTED — real finished pixels from neighbouring chunks. "
            "Everything else in IMAGE 1 is a flat-shaded ORTHOGRAPHIC GEOMETRY GUIDE: " + geo + ".\n"
            "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 image in which: (a) the painted strip(s) stay as they are; (b) every flat guide area is replaced by painting that "
            "CONTINUES the painted strip(s) seamlessly (same colours, line, hatching, washes, stones, grass, rock) so no join is visible; no straight line may appear at the inner edge of a painted strip; "
            "(c) every guide boundary stays exactly where it is; (d) every green pixel stays flat pure #00ff00.\n" + style)
else:
    text = (f"GENERATE BURST {bid} — Run C-9 P5, cliffside chunk {k}, no painted neighbours yet, painted over its orthographic guide (the C-3 v4.1 grid). task_id \"{bid}\".\n\n"
            "IMAGE 1 is a flat-shaded ORTHOGRAPHIC GEOMETRY GUIDE: " + geo + ".\nDeliver ONE 1536x1024 painting that follows IMAGE 1 exactly: keep every boundary where it is; paint every green "
            "pixel as flat pure #00ff00; paint every other pixel as scenery.\n" + style)
refs = [{"path": str(S/f'chunk_{k}_canvas{SUF}.png'), "role": "IMAGE 1 — the canvas to EDIT (painted strips + geometry guide)"},
        {"path": str(ANCHOR), "role": "IMAGE 2 — the approved painted STYLE of this level (Matt M1: GO / INK / ACCENTS)"},
        {"path": str(TRH), "role": "IMAGE 3 — manuscript page: how rich colour sits in small places (accents only; not its layout or content)"}]
text += (f"\n\nOne image_gen call. ONE retry only if a painted strip was altered, a boundary moved, the green was painted over, or a join line remains — name the reason. "
         f"Copy the output from $CODEX_HOME/generated_images/... to out/chunk_{k}.png with sha256. No code. No other files. No web.\n"
         f"RETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
json.dump({"text": text, "references": refs, "image_cap": 2, "minutes_cap": 15, "tool_call_cap": 20, "outputs": [f"out/chunk_{k}.png"], "effort": "high", "add_dirs": [], "experiment": "P5-cliffside"},
          open(B/'briefs'/'C-9'/f'{bid}.task.json', 'w'), indent=1, ensure_ascii=False)
print(bid, 'brief ok')
