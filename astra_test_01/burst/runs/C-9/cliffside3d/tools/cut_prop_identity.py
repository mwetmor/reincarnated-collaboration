#!/usr/bin/env python3
"""C-9 T9-1a: the identity plates for the bridge-slice prop model sheets.

Each plate is the PAINTED sprite(s) of one sheet, cut out on flat #00ff00, standing on a
common baseline, sized so the props' RELATIVE TRUE SCALE is what the picture shows. It is
a reference, not a canvas: nothing here is painted over. It exists so a four-view model
sheet is a sheet of THIS object, at the size this object really is.

TRUE SCALE, and where each number comes from. The painting and the geometry disagree
about how big a prop is, by a factor that is measurable rather than guessed: the four rail
posts exist in BOTH -- 0.22 x 1.20 x 0.22 m in cliffside_blockout.gd:659, and 110 sprite
px in the plate, which under (h/PPM)/cos(pitch) is 1.81 m. The painting draws its props
**1.512x** larger than the geometry they stand on. That factor, applied to the props that
have no blockout counterpart, is an INFERENCE from one measured class -- stated, not
hidden, so it can be overruled.

The raven is the exception and it is not close: the painted bird is 55 px of ink, 0.91 m
tall. Divided by 1.512 that is still 0.60 m -- a raven is 0.28 m perched. For an animal
the authority is the animal, so the raven is scaled from life and the factor is not used.
"""
import json
import pathlib

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent.parent
PROPS = HERE / "godot" / "props"
OUT = HERE / "t9_1a"

PPM = 100.617553710938
PITCH_COS = 0.602462407085
OVERSCALE = 1.512          # measured: painted rail post 1.81 m vs blockout 1.20 m
GREEN = (0, 255, 0)

# sheet -> rows; each row is (prop ids on that row, true height in metres, note key)
SHEETS = {
    "T9P-A": {"title": "the scorched snag",
              "rows": [(["bridge_obj_01_a"], 2.80)]},
    "T9P-B": {"title": "the rail post and the burnt stump",
              "rows": [(["bridge_post_0", "bridge_post_1", "bridge_post_2",
                         "bridge_post_3"], 1.20),
                       (["bridge_obj_01_c"], 0.80)]},
    "T9P-C": {"title": "the coiled rope and the perched raven",
              "rows": [(["bridge_obj_02_a"], 0.22),     # a coil lying flat: 0.62 m across
                       (["raven_perched"], 0.28)]},
}
# props whose size is set across, not up (a coil on the ground)
ACROSS = {"bridge_obj_02_a": 0.62}

PLATE_W, PLATE_H = 1536, 1024
PAD = 48


def ink_crop(path: pathlib.Path) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im)
    ys, xs = np.nonzero(a[..., 3] > 40)
    return im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = json.loads((PROPS / "props.json").read_text())
    assets = {a["name"]: a for a in data["assets"]}
    manifest = {"px_per_m_note": "PPM %.6f, cos(pitch) %.6f, painted/true prop factor %.3f"
                                 % (PPM, PITCH_COS, OVERSCALE),
                "sheets": {}}

    for sid, spec in SHEETS.items():
        rows = spec["rows"]
        # one px-per-metre for the whole plate, so the rows are honestly comparable
        tallest = max(h for _, h in rows)
        band = (PLATE_H - PAD * (len(rows) + 1)) / len(rows)
        k = min(band / tallest, 900.0)
        crops, meta = [], []
        for ids, true_h in rows:
            row = []
            for pid in ids:
                c = ink_crop(PROPS / assets[pid]["file"])
                if pid in ACROSS:
                    w = ACROSS[pid] * k
                    scale = w / c.width
                else:
                    scale = (true_h * k) / c.height
                r = c.resize((max(1, round(c.width * scale)),
                              max(1, round(c.height * scale))), Image.LANCZOS)
                row.append(r)
                painted_h = (c.height / PPM) / PITCH_COS
                meta.append({"prop": pid, "sprite_px": list(Image.open(PROPS / assets[pid]["file"]).size),
                             "ink_px": [c.width, c.height],
                             "painted_implied_m": round(painted_h, 2),
                             "true_m": ACROSS.get(pid, true_h),
                             "axis": "across" if pid in ACROSS else "height"})
            crops.append(row)

        plate = Image.new("RGBA", (PLATE_W, PLATE_H), GREEN + (255,))
        y = PAD
        for row in crows_iter(crops):
            rh = max(r.height for r in row)
            gap = (PLATE_W - sum(r.width for r in row)) // (len(row) + 1)
            x = gap
            for r in row:
                plate.alpha_composite(r, (x, y + rh - r.height))
                x += r.width + gap
            y += rh + PAD

        p = OUT / ("%s_identity.png" % sid)
        plate.convert("RGB").save(p)
        manifest["sheets"][sid] = {"title": spec["title"],
                                   "identity_plate": str(p.relative_to(HERE)),
                                   "px_per_m": round(k, 1), "props": meta}
        print("%s -> %s  (%.1f px/m)  %s" % (sid, p.name, k,
              ", ".join("%s %.2f m" % (m["prop"], m["true_m"]) for m in meta)))

    (OUT / "t9_prop_sheets.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print("manifest -> %s" % (OUT / "t9_prop_sheets.json"))


def crows_iter(rows):
    for r in rows:
        yield r


if __name__ == "__main__":
    main()
