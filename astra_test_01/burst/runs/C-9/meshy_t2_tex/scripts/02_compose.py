# C-9 T5 step 1b: compose the rendered cells onto the matte key.
#
#   python3 scripts/02_compose.py <out.png>
#
# Kept out of Blender so the sheet can be recomposed without re-rendering, and
# so the alpha coverage can be MEASURED here rather than asserted: a creature
# that lands outside its own cell, or a cell that came back empty, is the one
# failure that would waste a whole Astra fire.
import json, os, sys
from PIL import Image
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = sys.argv[1] if len(sys.argv) > 1 else "a"
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    ROOT, "artifacts", "T5-paint-sheet-%s.png" % NAME)
L = json.load(open(os.path.join(ROOT, "work", "layout_%s.json" % NAME)))
CW, CH = L["canvas"]
sheet = Image.new("RGBA", (CW, CH), tuple(L["key_rgb"]) + (255,))
rep = {}
for d, c in L["cells"].items():
    x0, y0, w, h = c["rect"]
    p = os.path.join(ROOT, "work", "_cells_%s", "cell_%s.png") % (NAME, d)
    im = Image.open(p).convert("RGBA")
    assert im.size == (w, h), "%s rendered %s, cell is %s" % (d, im.size, (w, h))
    A = np.array(im)[:, :, 3]
    cov = float((A > 8).mean())
    # does the creature touch the cell edge? if it does it is CROPPED, and a
    # cropped view paints detail that has nowhere to project back to
    edge = max(float((A[0] > 8).mean()), float((A[-1] > 8).mean()),
               float((A[:, 0] > 8).mean()), float((A[:, -1] > 8).mean()))
    rep[d] = dict(coverage=round(cov, 4), edge_touch=round(edge, 4),
                  size=[w, h])
    sheet.alpha_composite(im, (x0, y0))
    assert x0 >= 0 and y0 >= 0 and x0 + w <= CW and y0 + h <= CH, \
        "%s cell %s falls off the canvas" % (d, c["rect"])
sheet.convert("RGB").save(OUT)
L["cell_report"] = rep
json.dump(L, open(os.path.join(ROOT, "work", "layout_%s.json" % NAME), "w"), indent=1)
print("wrote %s  (%dx%d, px/m %.2f)" % (OUT, CW, CH, L["px_per_m"]))
for d in L["cells"]:
    # a head close-up crops the body away at the cell edge BY DESIGN, so the
    # crop detector only applies to whole-body cells
    print("   %-9s coverage %5.1f%%   edge touch %5.1f%%%s"
          % (d, 100 * rep[d]["coverage"], 100 * rep[d]["edge_touch"],
             "  (head close-up: crop expected)"
             if L["cells"][d].get("subject") == "head" else ""))
