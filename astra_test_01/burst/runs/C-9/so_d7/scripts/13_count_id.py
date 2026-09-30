# Count the helmet ID pass. Blender ships no PIL, so the render and the count
# are separate steps -- the same split the T5 bake needed.
#   python3 scripts/13_count_id.py <idpass_dir> <out.json> <label>
import json, os, sys
import numpy as np
from PIL import Image
D, OUTJ, LABEL = sys.argv[1], sys.argv[2], sys.argv[3]
rows = {}
for f in ("S", "SE", "E", "NE", "N", "NW", "W", "SW"):
    hp = os.path.join(D, "h_%s.png" % f)
    cp = os.path.join(D, "c_%s.png" % f)
    if not (os.path.exists(hp) and os.path.exists(cp)):
        continue
    ha = np.array(Image.open(hp).convert("RGBA"))
    ca = np.array(Image.open(cp).convert("RGBA"))
    sil = ha[..., 3] > 128
    red = (ca[..., 0] > 140) & (ca[..., 1] < 100) & (ca[..., 3] > 128)
    grn = (ca[..., 1] > 140) & (ca[..., 0] < 100) & (ca[..., 3] > 128)
    n = int(sil.sum())
    rows[f] = dict(silhouette_px=n,
                   dome_visible_pct=round(100 * float((sil & red).sum()) / max(n, 1), 2),
                   hair_through_pct=round(100 * float((sil & grn).sum()) / max(n, 1), 2))
    print("   %-3s silhouette %6d px  dome visible %6.2f%%  hair through %5.2f%%"
          % (f, n, rows[f]["dome_visible_pct"], rows[f]["hair_through_pct"]))
dv = float(np.mean([r["dome_visible_pct"] for r in rows.values()]))
ht = float(np.mean([r["hair_through_pct"] for r in rows.values()]))
print("%s MEAN over %d facings: dome visible %.2f%%, hair through %.2f%%"
      % (LABEL, len(rows), dv, ht))
json.dump(dict(label=LABEL, per_facing=rows, mean_dome_visible_pct=round(dv, 2),
               mean_hair_through_pct=round(ht, 2)), open(OUTJ, "w"), indent=1)
