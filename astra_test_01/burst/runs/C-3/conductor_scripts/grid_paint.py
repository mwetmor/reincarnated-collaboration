# Conductor driver for the v3 chunk grid (staging + briefs + waves). usage: grid_paint.py stage <cx_cy> | brief <cx_cy> | ready
import json, sys, pathlib
from PIL import Image
B=pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A=B/'runs/C-3/artifacts'; G=A/'CS-guides-v3'
J=json.load(open(G/'chunks_v3.json'))
CH={}
for e in J['paint_order']:
    k=f"{e['index'][0]}_{e['index'][1]}"
    CH[k]={'origin':e['origin_px'],'after':[a['chunk'].replace('chunk_','') for a in e['paint_after']]+[a['chunk'].replace('chunk_','') for a in e['corner_overlaps_already_painted']],'step':e['step']}
import os
SUF=os.environ.get('SUF','')
EXTRA=os.environ.get('EXTRA','')
def src(k):
    for d in (f'CS-v3-{k}-r1', f'CS-v3-{k}'):
        if (A/d/f'chunk_{k}.png').exists(): return A/d/f'chunk_{k}.png'
    return None
def done(k): return src(k) is not None
cmd=sys.argv[1]
if cmd=='ready':
    print(' '.join(k for k,c in sorted(CH.items(), key=lambda kv: kv[1]['step']) if not done(k) and all(done(n) for n in c['after'])))
    sys.exit()
k=sys.argv[2]; c=CH[k]; ox,oy=c['origin']
guide=Image.open(G/f'chunk_{k}_guide.png').convert('RGB')
kept=set()
for n,nc in CH.items():
    if n==k or not done(n): continue
    nx,ny=nc['origin']
    x0,y0=max(ox,nx),max(oy,ny); x1,y1=min(ox+1536,nx+1536),min(oy+1024,ny+1024)
    if x1<=x0 or y1<=y0: continue
    npng=Image.open(src(n)).convert('RGB')
    guide.paste(npng.crop((x0-nx,y0-ny,x1-nx,y1-ny)),(x0-ox,y0-oy))
    side=('LEFT' if nx<ox and ny==oy else 'TOP' if ny<oy and nx==ox else 'corner')
    kept.add({'LEFT':'the LEFT 256 columns (from the chunk to its left)','TOP':'the TOP 256 rows (from the chunk above)','corner':'a 256×256 corner square (from a diagonal neighbour)'}[side])
kept=sorted(kept)
if cmd=='stage':
    guide.save(G/f'chunk_{k}_edit_canvas{SUF}.png'); print(k,'staged', kept)
elif cmd=='brief':
    bid=f'CS-v3-{k}{SUF}'
    geo=("TAN = packed-dirt cliff-top path; LIGHT GREY band = grassy/rocky verge along the rim; DARK GREY/BROWN plane = the vertical cliff face dropping toward the viewer (paint it as continuous rock all the way down to where it meets the green — it will fade into mist in the game, so keep its lowest part slightly hazier and darker, with no ledge or bottom edge drawn); dark blocks = boulder outcrops; BROWN planks = a wooden bridge deck; MAGENTA plank = one loose bridge plank (paint it as a cracked, loose plank); PURE GREEN #00ff00 = empty void")
    style=("Orthographic view: no perspective shrinking toward the top. Scale: a person standing here is 130 px tall. LIGHT: warm SUNSET key from the UPPER-LEFT, cool violet shadows. REGISTER: HAND-DRAWN painted 2D — confident tapered dark contours, painted planes, bold Hades-like jewel tones and graphic shadows — matching IMAGE 2 exactly. No characters, creatures, text, UI, border or vignette.")
    if kept:
        text=(f"GENERATE BURST {bid} — cliffside v3 chunk {k} by OUTPAINTING (Matt R-C3-46/48). task_id \"{bid}\".\n\n"+EXTRA+"IMAGE 1 is the canvas to EDIT (1536×1024). "+'In it, '+'; '.join(kept)+" are ALREADY PAINTED — real finished pixels from neighbouring chunks. Everything else in IMAGE 1 is a flat-shaded ORTHOGRAPHIC GEOMETRY GUIDE: "+geo+".\n"
          "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536×1024 image in which: (a) the painted strip(s) stay as they are; (b) every flat guide area is replaced by painting that CONTINUES the painted strip(s) seamlessly (same colours, textures, stones, grass, strata, light) so no join is visible; (c) every guide boundary stays exactly where it is; (d) every green pixel stays flat pure #00ff00.\n"+style)
        refs=[{"path":str(G/f'chunk_{k}_edit_canvas{SUF}.png'),"role":"IMAGE 1 — the canvas to EDIT (painted strips + geometry guide)"}]
    else:
        text=(f"GENERATE BURST {bid} — cliffside v3 chunk {k}, the FIRST chunk of the grid, painted over its orthographic guide (Matt R-C3-48). task_id \"{bid}\".\n\nIMAGE 1 is a flat-shaded ORTHOGRAPHIC GEOMETRY GUIDE: "+geo+".\nDeliver ONE 1536×1024 painting that follows IMAGE 1 exactly: keep every boundary where it is; paint every green pixel as flat pure #00ff00; paint every other pixel as scenery.\n"+style)
        refs=[{"path":str(G/f'chunk_{k}_guide.png'),"role":"IMAGE 1 — GEOMETRY GUIDE (exact boundaries; green = void)"}]
    refs.append({"path":str(A/'CS-chunk-A'/'chunk_A.png'),"role":"IMAGE 2 — the approved painted STYLE of this level (Matt: 'love the style and the chunks')"})
    text+=(f"\n\nOne image_gen call. ONE retry only if a painted strip was altered, a boundary moved, the green was painted over, or a join line remains — name the reason. Copy the output from $CODEX_HOME/generated_images/... to out/chunk_{k}.png with sha256. No code. No other files. No web.\nRETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
    json.dump({"text":text,"references":refs,"image_cap":2,"minutes_cap":15,"tool_call_cap":20,"outputs":[f"out/chunk_{k}.png"],"effort":"high","add_dirs":[],"experiment":"C3-cliffside-v3"},open(B/'briefs'/'C-3'/f'{bid}.task.json','w'),indent=1,ensure_ascii=False)
    print(bid,'brief ok')
