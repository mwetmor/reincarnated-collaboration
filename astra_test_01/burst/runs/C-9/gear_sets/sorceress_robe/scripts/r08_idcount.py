# R-C9-120: BODY pixels visible (red in the stills' id pass) per shot -- a renderer-truth count of skin showing through
# or past the robe; compared folder against folder (feet, hands and face are in every folder alike).
#   python3 r08_idcount.py <dir> [<dir> ...]
import glob, os, sys
import numpy as np
from PIL import Image
for d in sys.argv[1:]:
    tot = 0; tsk = 0; rows = []
    for f in sorted(glob.glob(d + "/stack0_*_id.png")):
        a = np.array(Image.open(f).convert('RGB')); body = (a[..., 0] > 200) & (a[..., 1] < 50) & (a[..., 2] < 50); n = int(body.sum())
        # of those, how many read as bare SKIN in the beauty pass (bright, warm, low saturation) -- leggings and boots do not
        c = np.array(Image.open(f.replace('_id.png', '_beauty.png')).convert('RGB')).astype(float) / 255
        lum = c @ [0.299, 0.587, 0.114]; sat = (c.max(2) - c.min(2)) / np.maximum(c.max(2), 1e-6)
        sk = int((body & (lum > 0.5) & (c[..., 0] >= c[..., 1]) & (c[..., 1] >= c[..., 2] - 0.02) & (sat < 0.55)).sum())
        tot += n; tsk += sk; rows.append((os.path.basename(f)[7:-7], n, sk))
    print(d, "TOTAL body px", tot, "skin-coloured", tsk, " ".join("%s=%d/%d" % r for r in rows))
