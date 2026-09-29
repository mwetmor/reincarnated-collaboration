# D2: slice a painted sheet into the four (or six) views Tripo wants.
#
#   python3 scripts/03_slice_views.py body  <sheet.png> <tag> [--matte green]
#   python3 scripts/03_slice_views.py object <sheet.png> <tag>
#
# BODY sheets are the NB-1_b 2x2 layout: front / right / back / left. OBJECT
# sheets are a free arrangement of blobs, so the pieces are found by connected
# components and assigned by position rather than by a hardcoded grid -- on
# NB-W1 the three axe views are not on even thirds.
#
# MATTE: the sheets do not share a background. G3 kept its green plate and is
# keyed exactly; the rest lost theirs to the usual dark gradient and go through
# BiRefNet, the same matte the base body used, so the gear views and the base
# views are cut the same way.
import json, os, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODE, SRC, TAG = sys.argv[1], sys.argv[2], sys.argv[3]
MATTE = sys.argv[sys.argv.index("--matte") + 1] if "--matte" in sys.argv else "birefnet"
OUT = os.path.join(ROOT, "views", TAG)
os.makedirs(OUT, exist_ok=True)


def alpha(path):
    if MATTE == "green":
        im = np.array(Image.open(path).convert("RGB"), np.int16)
        g = (im[..., 1] > 140) & (im[..., 0] < 130) & (im[..., 2] < 130)
        a = (~g).astype(np.uint8) * 255
        rgb = np.array(Image.open(path).convert("RGB"))
        return rgb, a
    import fal_client
    url = fal_client.upload_file(path)
    r = fal_client.subscribe('fal-ai/birefnet/v2', arguments={
        'image_url': url, 'model': 'General Use (Heavy)',
        'operating_resolution': '2048x2048', 'output_format': 'png',
        'refine_foreground': True})
    tmp = os.path.join(OUT, "_matte.png")
    subprocess.run(['curl', '-s', '-L', '-o', tmp, r['image']['url']], check=True)
    im = Image.open(tmp).convert("RGBA")
    arr = np.array(im)
    return arr[..., :3], arr[..., 3]


rgb, a = alpha(SRC)
m = a > 128
m = ndimage.binary_opening(m, np.ones((3, 3)))
print("%s: matte covers %.2f%% (%s)" % (TAG, 100 * m.mean(), MATTE))
H, W = m.shape
pieces = {}
if MODE == "body":
    quads = {'front': (0, 0), 'right': (1, 0), 'back': (0, 1), 'left': (1, 1)}
    for name, (c, r) in quads.items():
        sub = m[r * H // 2:(r + 1) * H // 2, c * W // 2:(c + 1) * W // 2]
        lab, n = ndimage.label(sub)
        if n > 1:
            sz = ndimage.sum(sub, lab, range(1, n + 1))
            sub = lab == (int(np.argmax(sz)) + 1)
        ys, xs = np.where(sub)
        pieces[name] = (c * W // 2 + xs.min(), r * H // 2 + ys.min(),
                        c * W // 2 + xs.max() + 1, r * H // 2 + ys.max() + 1)
else:
    lab, n = ndimage.label(m, np.ones((3, 3)))
    sz = ndimage.sum(m, lab, range(1, n + 1))
    keep = [i + 1 for i in range(n) if sz[i] > 0.004 * m.sum()]
    boxes = []
    for i in keep:
        ys, xs = np.where(lab == i)
        boxes.append((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1, int(sz[i - 1])))
    print("  %d blobs kept of %d" % (len(boxes), n))
    top = sorted([b for b in boxes if (b[1] + b[3]) / 2 < H / 2], key=lambda b: b[0])
    bot = sorted([b for b in boxes if (b[1] + b[3]) / 2 >= H / 2], key=lambda b: b[0])
    assert len(top) == 3 and len(bot) == 3, \
        "expected 3 blobs per row, found %d and %d" % (len(top), len(bot))
    for nm, b in zip(("axe_side", "axe_edge", "axe_other"), top):
        pieces[nm] = b[:4]
    for nm, b in zip(("shield_front", "shield_edge", "shield_back"), bot):
        pieces[nm] = b[:4]

hmax = max(b[3] - b[1] for b in pieces.values())
S = 0.88 * 1024 / hmax
meta = {}
src = Image.fromarray(np.dstack([rgb, a]).astype(np.uint8))
for name, (x0, y0, x1, y1) in pieces.items():
    fig = src.crop((x0, y0, x1, y1))
    w, h = fig.size
    fig = fig.resize((max(1, round(w * S)), max(1, round(h * S))), Image.LANCZOS)
    can = Image.new('RGB', (1024, 1024), (255, 255, 255))
    px = (1024 - fig.size[0]) // 2
    py = int(1024 * 0.94) - fig.size[1]
    can.paste(fig, (px, max(py, 0)), fig)
    can.save(os.path.join(OUT, "%s.jpg" % name), quality=95)
    meta[name] = dict(src_box=[int(v) for v in (x0, y0, x1, y1)],
                      h_src=int(y1 - y0), scale=round(S, 5),
                      placed=[px, max(py, 0), *fig.size])
    print("   %-13s src %4dx%-4d -> placed %s" % (name, x1 - x0, y1 - y0, meta[name]["placed"]))
json.dump(dict(sheet=SRC, mode=MODE, matte=MATTE, common_scale=round(S, 5),
               views=meta), open(os.path.join(OUT, "views.json"), "w"), indent=1)
