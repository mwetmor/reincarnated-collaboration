# R-C9-233 step 2: LIVE vs FIX stills for Matt, at the play camera (pitch 52.95354, the Barrow's zoom), from the probe's
# frames (barrow_full/godot/tools/probe_face_r233.gd -- the painted Barrow, web renderer). Rows: clip x {live, fix};
# columns: the headings. Each cell is centred on her face (live's footprint centroid at that zoom).
#   python3 r233_06_stills.py <probe dir> <fix variant> <out prefix> [--label "FIX G: ..."]
import sys, os, numpy as np
from PIL import Image, ImageDraw
D, FIX, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
LAB = sys.argv[sys.argv.index('--label') + 1] if '--label' in sys.argv else FIX
HEADS = ['S', 'SE', 'SW', 'E', 'W', 'N']
CLIPS = [('idle', 'idle'), ('walk', 'walk'), ('cast_fireball_m', 'Fire Ball (release)')]
for zoom, src, cell in ((1, 64, 256), (3, 170, 340)):
    W = 170 + cell * len(HEADS); H = 28 + cell * 2 * len(CLIPS)
    sh = Image.new('RGB', (W, H), (24, 24, 28)); d = ImageDraw.Draw(sh)
    for j, h in enumerate(HEADS):
        d.text((170 + j * cell + 6, 8), 'heading %s' % h, fill=(235, 235, 235))
    r = 0
    for clip, name in CLIPS:
        for v, vl in (('live', 'LIVE (as played)'), (FIX, LAB)):
            d.text((6, 28 + r * cell + 6), name, fill=(235, 235, 235)); d.text((6, 28 + r * cell + 22), vl, fill=(255, 210, 120) if v != 'live' else (200, 200, 200))
            for j, h in enumerate(HEADS):
                p = '%s/%s_%s_%s_z%d_beauty.png' % (D, v, clip, h, zoom); fp = '%s/live_%s_%s_z%d_foot.png' % (D, clip, h, zoom)
                if not os.path.exists(p): continue
                im = Image.open(p).convert('RGB'); f = np.asarray(Image.open(fp).convert('RGB')).astype(int)
                ys, xs = np.nonzero((f[..., 0] > 200) & (f[..., 1] < 55) & (f[..., 2] < 55))
                cx, cy = (xs.mean(), ys.mean() + src * 0.15) if len(xs) else (im.width / 2, im.height / 2)
                x0 = int(min(max(cx - src / 2, 0), im.width - src)); y0 = int(min(max(cy - src / 2, 0), im.height - src))
                sh.paste(im.crop((x0, y0, x0 + src, y0 + src)).resize((cell, cell), Image.NEAREST if zoom == 1 else Image.LANCZOS), (170 + j * cell, 28 + r * cell))
            r += 1
    sh.save('%s_z%d.jpg' % (OUT, zoom), quality=90)
    print('%s_z%d.jpg' % (OUT, zoom), sh.size)
