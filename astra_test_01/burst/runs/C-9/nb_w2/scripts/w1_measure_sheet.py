# Measure a three-view sword sheet on #00ff00: per view, blade (crossguard top -> point), grip
# (crossguard bottom -> pommel top), pommel, guard -- in pixels, and the blade/grip ratio.
#
#   python3 scripts/w1_measure_sheet.py <sheet.png> [--matte matte.png] [--json out.json] [--png overlay.png]
#
# Parts are found by WIDTH along the sword's own axis, not by colour: the crossguard is the widest
# row band, the grip the narrow band below it, and the pommel the next widening. The edge-on view
# has a foreshortened guard, so it is measured as total length only, for the views to agree on.
import json, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
a = sys.argv[1:]
SRC = a[0]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
OUTP = a[a.index('--png') + 1] if '--png' in a else None
MATTE = a[a.index('--matte') + 1] if '--matte' in a else None
im = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
H, W, _ = im.shape
if MATTE:
    # a BiRefNet matte (RGBA): the edit came back on a dark gradient, which no colour key can cut
    mask = np.asarray(Image.open(MATTE).convert('RGBA'))[..., 3] > 128
else:
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    green = (g > 150) & (g - np.maximum(r, b) > 70)
    mask = ~green
mask = ndimage.binary_opening(mask, np.ones((3, 3)))
lab, n = ndimage.label(mask)
sizes = ndimage.sum(mask, lab, range(1, n + 1))
keep = [i + 1 for i in np.argsort(sizes)[::-1][:3] if sizes[i] > 0.002 * H * W]
views = []
for i in keep:
    ys, xs = np.nonzero(lab == i)
    views.append(dict(label=i, x0=int(xs.min()), x1=int(xs.max()), y0=int(ys.min()), y1=int(ys.max())))
views.sort(key=lambda v: v['x0'])
names = ["front", "edge", "back"] if len(views) == 3 else ["v%d" % k for k in range(len(views))]
rep = dict(source=SRC, size=[W, H], views={})
for nm, v in zip(names, views):
    m = lab[v['y0']:v['y1'] + 1, v['x0']:v['x1'] + 1] == v['label']
    w = m.sum(1).astype(float)                                   # width per row, top (point) to bottom (pommel)
    L = len(w)
    ws = ndimage.uniform_filter1d(w, 5)
    guard_rows = np.nonzero(ws > 0.75 * ws.max())[0]
    # the crossguard is the widest band in the middle 30-85% of the length (the pommel may be wide too)
    mid = guard_rows[(guard_rows > 0.3 * L) & (guard_rows < 0.85 * L)]
    rec = dict(total_px=int(L), width_max_px=int(ws.max()))
    if nm != "edge" and len(mid):
        gt, gb = int(mid.min()), int(mid.max())
        below = ws[gb + 1:]
        grip_w = float(np.median(below[: max(5, len(below) // 3)]))
        # pommel top: first row below the guard, past the grip's upper collar, where the width
        # climbs above 1.35x the grip's median width and stays there to the end
        pt = None
        for k in range(len(below)):
            if below[k] > 1.35 * grip_w and np.all(below[k:k + 8] > 1.25 * grip_w) and k > 0.4 * len(below):
                pt = gb + 1 + k; break
        rec.update(blade_px=gt, guard_px=gb - gt + 1, grip_px=(pt - gb - 1) if pt else None,
                   pommel_px=(L - pt) if pt else None, grip_width_px=round(grip_w, 1))
        if pt:
            rec["blade_over_grip"] = round(gt / (pt - gb - 1), 3)
    rep["views"][nm] = rec
    print("  %-5s total %4d px | blade %s | guard %s | grip %s | pommel %s | blade/grip %s"
          % (nm, L, rec.get("blade_px"), rec.get("guard_px"), rec.get("grip_px"), rec.get("pommel_px"), rec.get("blade_over_grip")))
    v["rec"] = rec
tot = [rep["views"][k]["total_px"] for k in rep["views"]]
rep["views_total_spread_pct"] = round(100 * (max(tot) - min(tot)) / max(tot), 2)
print("  views agree on total length within %.2f%%" % rep["views_total_spread_pct"])
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
if OUTP:
    o = Image.open(SRC).convert('RGB'); d = ImageDraw.Draw(o)
    for nm, v in zip(names, views):
        rr = v["rec"]; x0, x1, y0 = v['x0'], v['x1'], v['y0']
        for key, col in (("blade_px", (255, 0, 0)),):
            if rr.get(key) is not None:
                d.line([(x1 + 6, y0), (x1 + 6, y0 + rr["blade_px"])], fill=(255, 0, 0), width=3)
                gb = y0 + rr["blade_px"] + rr["guard_px"]
                if rr.get("grip_px"):
                    d.line([(x1 + 12, gb), (x1 + 12, gb + rr["grip_px"])], fill=(0, 0, 255), width=3)
    o.save(OUTP)
