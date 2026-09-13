# Seed canvas for edit-canvas loops (K3 geometry, K3-seed/canvas_idle_S_seed.json): the approved frame cropped to its alpha bbox,
# scaled uniformly to 470 px tall (75 % of the 627-px cell), pasted into SLOT 0 of a 1254² #00ff00 canvas with its sole on cell row 564
# (0.9 × 627) and centred at x = 313.5; the fixed registration transform (627 → 320 @ 0.5106, paste (96,112)) is copied beside it.
import sys, json, hashlib, pathlib, shutil
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from PIL import Image
import numpy as np
from gates import matte
src, label = pathlib.Path(sys.argv[1]), sys.argv[2]
ART = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts'); outd = ART/'K3p-seed'; outd.mkdir(exist_ok=True)
rgba, info = matte.extract(Image.open(src), alpha_floor=40)   # frozen character matte (green-excess); returns (RGBA image, info)
a = np.array(rgba)[..., 3]
ys, xs = np.where(a >= 128); x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1
H = y1 - y0; scale = 470 / H; W = round((x1 - x0) * scale)
fig = Image.open(src).convert('RGB').crop((x0, y0, x1, y1)).resize((W, 470), Image.LANCZOS)
cell = 627; canvas = Image.new('RGB', (2*cell, 2*cell), (0, 255, 0))
px, py = round(313.5 - W/2), 564 - 470
canvas.paste(fig, (px, py)); out = outd/f'canvas_{label}_seed.png'; canvas.save(out, 'PNG')
meta = {"seed": str(src), "figure_bbox_native": [x0, y0, x1, y1], "scale": round(scale, 4), "cell_px": cell, "figure_height_in_cell_px": 470,
        "slot0_paste": [px, py], "feet_line_cell_fraction": 0.9, "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "note": "uniform downscale + translation only (register card); 75 % cell height per run_03 convention; K3 geometry reused (K3-seed/canvas_idle_S_seed.json)"}
json.dump(meta, open(outd/f'canvas_{label}_seed.json', 'w'), indent=1)
shutil.copy(ART/'K3-seed'/'registration_transform.json', outd/'registration_transform.json')
print(json.dumps(meta, indent=1))
