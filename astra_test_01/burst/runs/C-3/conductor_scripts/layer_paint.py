# Conductor driver for parallax layer panels (outpaint grids). usage: layer_paint.py ready | stage <id> | brief <id>
import json, sys, pathlib
from PIL import Image
B=pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A=B/'runs/C-3/artifacts'; G=A/'CS-layers'; G.mkdir(exist_ok=True)
LAY={
 'sky':   dict(cols=2, rows=1, bg=(128,128,128), key=False,
    desc="the SUNSET SKY layer — the farthest backdrop: a blazing sunset, the sun low near the LEFT edge of the full layer throwing long gold rays; huge sculpted clouds in bold graphic shapes (saturated orange, hot magenta, violet, gold); a few dark smoke plumes from the burning valley rising into the clouds on the right; near the bottom a soft band of violet haze. NO land at all.",
    part=lambda c,r: ["the LEFT half (the sun is here)","the RIGHT half (smoke plumes rising into the clouds)"][c]),
 'far_ruins': dict(cols=2, rows=2, bg=(128,128,128), key=True,
    desc="the FAR RUINS layer: a range of distant jagged mountain spires and, on a far hilltop plateau, the ruins of a RECENTLY DESTROYED TEMPLE — broken columns, a collapsed split dome, fallen statues, burnt banners, embers and thin smoke — all in cool violet atmospheric haze with warm sunset rim light from the left. The LAND's top silhouette (mountain tops and ruin tops) sits at about 38–48 % of the full layer's height; EVERYTHING ABOVE that silhouette is flat pure #00ff00 (the sky layer shows there); below the silhouette the land is fully painted down to the bottom edge, becoming hazier and simpler toward the bottom (hazy distant cliffs).",
    part=lambda c,r: [["upper-left (mostly green sky area; the mountain silhouette enters near the bottom of this panel)","upper-right (mostly green; mountain spires rising into the bottom part)"],["lower-left (the destroyed temple on its hilltop, with embers and smoke)","lower-right (distant cliffs and a second smaller ruin, hazy)"]][r][c]),
 'forest_valley': dict(cols=3, rows=2, bg=(128,128,128), key=True,
    desc="the CHARRED FOREST VALLEY layer — nearer than the ruins: a vast burnt forest filling a valley: black skeletal trunks and branches, grey ash ground, pockets of glowing orange embers and small lingering fires, smoke curling up, a winding river reflecting the sunset. Its top silhouette (the far ridge line of burnt treetops) sits at about 25–32 % of the full layer's height; EVERYTHING ABOVE that silhouette is flat pure #00ff00; below it the forest fills everything down to the bottom edge, denser and darker toward the bottom.",
    part=lambda c,r: [["upper-left","upper-middle","upper-right"],["lower-left","lower-middle (the river bends here)","lower-right"]][r][c]),
 'mist': dict(cols=2, rows=2, bg=(0,0,0), key=False,
    desc="the MIST layer: soft drifting banks of pale warm mist and low cloud lit by the sunset (peach, rose and lavender), painted as LIGHT on a PURE BLACK background (black = fully transparent in the game, brighter = more opaque mist). Mist is thin and wispy in the upper half and thickens into dense rolling cloud banks toward the bottom. No land, no trees, no sky colour on the black.",
    part=lambda c,r: [["upper-left (thin wisps)","upper-right (thin wisps)"],["lower-left (thick rolling banks)","lower-right (thick rolling banks)"]][r][c]),
}
def pid(l,c,r): return f'L-{l}-{c}_{r}'
def done(i): return (A/i/f'{i}.png').exists()
def panels():
    for l,d in LAY.items():
        for r in range(d['rows']):
            for c in range(d['cols']): yield l,c,r
cmd=sys.argv[1]
if cmd=='ready':
    out=[]
    for l,c,r in panels():
        i=pid(l,c,r)
        if done(i): continue
        need=[pid(l,c-1,r)] if c else []
        need+=[pid(l,c,r-1)] if r else []
        need+=[pid(l,c+1,r-1)] if r and c+1<LAY[l]['cols'] else []
        if all(done(n) for n in need): out.append(i)
    print(' '.join(out)); sys.exit()
i=sys.argv[2]; l=i.split('-')[1]; c,r=map(int,i.split('-')[2].split('_')); d=LAY[l]
canvas=Image.new('RGB',(1536,1024),d['bg']); kept=[]
for (nc,nr) in [(c-1,r),(c,r-1),(c+1,r-1),(c-1,r-1)]:
    if nc<0 or nr<0 or nc>=d['cols']: continue
    n=pid(l,nc,nr)
    if not done(n): continue
    im=Image.open(A/n/f'{n}.png').convert('RGB')
    dx,dy=(nc-c)*1280,(nr-r)*768
    x0,y0=max(0,dx),max(0,dy); x1,y1=min(1536,dx+1536),min(1024,dy+1024)
    if x1>x0 and y1>y0:
        canvas.paste(im.crop((x0-dx,y0-dy,x1-dx,y1-dy)),(x0,y0)); kept.append({(-1,0):'its LEFT 256 columns',(0,-1):'its TOP 256 rows',(1,-1):'its top-right 256×256 corner',(-1,-1):'its top-left 256×256 corner'}[(nc-c,nr-r)])
if cmd=='stage':
    canvas.save(G/f'{i}_canvas.png'); print(i,'staged',kept)
elif cmd=='brief':
    fill='flat mid-grey' if d['bg']!=(0,0,0) else 'flat black'
    geom=f"This image is one panel ({d['part'](c,r)}) of a {d['cols']}×{d['rows']} grid of 1536×1024 panels (neighbours overlap by 256 px) that together form ONE continuous painted parallax background layer for a hand-painted 2D game scene seen past a cliff edge at sunset. The whole layer is {d['desc']}"
    reg="REGISTER: the level's approved painted style (IMAGE 2): hand-drawn painted 2D, tapered dark contours (lighter and thinner with distance), painted planes, bold Hades-like jewel tones and graphic shapes, rich detail. No characters, creatures, text, UI, border or vignette."
    bid=i
    if kept:
        text=(f"GENERATE BURST {bid} — parallax background panel by OUTPAINTING (Matt R-C3-46/48). task_id \"{bid}\".\n\n{geom}\nIMAGE 1 is the canvas to EDIT: "+'; '.join(kept)+f" are ALREADY PAINTED (real pixels from neighbouring panels); the rest is {fill} placeholder. Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536×1024 image: keep the painted strips as they are and replace the placeholder with painting that CONTINUES them seamlessly (no visible join), following the layer description for this panel's position" + (" — any flat pure #00ff00 in the painted strips continues as flat pure #00ff00." if d['key'] else ".") + "\n" + reg)
        refs=[{"path":str(G/f'{i}_canvas.png'),"role":"IMAGE 1 — the canvas to EDIT (painted neighbour strips + placeholder)"}]
    else:
        text=(f"GENERATE BURST {bid} — parallax background panel, the FIRST panel of its layer (Matt R-C3-42/48). task_id \"{bid}\".\n\n{geom}\nDeliver ONE LANDSCAPE 1536×1024 image of this panel.\n"+reg)
        refs=[]
    refs.append({"path":str(A/'CS-vista-01'/'vista_01.png'),"role":"IMAGE 2 — the approved painted STYLE and story of this background (do not copy its layout)"})
    text+=(f"\n\nOne image_gen call. ONE retry only if a painted strip was altered, a join remains, the layer contains a cliff rim/characters/text, or (keyed layers) the area above the silhouette is not flat pure #00ff00 — name the reason. Copy the output from $CODEX_HOME/generated_images/... to out/{i}.png with sha256. No code. No other files. No web.\nRETURN: receipt task_id \"{bid}\"; images = the file with prompt, references and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
    json.dump({"text":text,"references":refs,"image_cap":2,"minutes_cap":15,"tool_call_cap":20,"outputs":[f"out/{i}.png"],"effort":"high","add_dirs":[],"experiment":"C3-cliffside-layers"},open(B/'briefs'/'C-3'/f'{bid}.task.json','w'),indent=1,ensure_ascii=False)
    print(bid,'brief ok')
