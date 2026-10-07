#!/usr/bin/env python3
"""P6a stage 2 -- the SCOPED BLIND JUDGE for openings inside declared dark structures (ruling R-C9-169, option (b)).

Pipeline (binding from R-C9-169):
  1. v0.1 (p6_geometry.openings, T = 32, no prior) generates the candidates; declared openings are matched and dropped.
  2. A candidate whose centroid lies OUTSIDE a declared dark-structure region FAILS THE CHUNK automatically.
  3. A candidate INSIDE one goes to a fresh blind judge: an ITEM image is the painting crop beside the guide crop at the
     same pixels (painting | 24 px gap | guide), and the only question is "does the painting show a doorway, opening or
     structure the guide does not?" "yes" fails the chunk.
     Declared dark-structure regions: Phase 1+ = the ID render's hall / porch / gable / palisade / char classes;
     calibration = the zone-map extrusion (p6_geometry.zonemap_dark_mask, layout-v5 heights).
If the calibration fails its acceptance, the fallback is (a): the conductor triages the stage-3 candidates by eye,
logged per chunk.

CALIBRATION SET (build): 20 items, shuffled, item_01..item_20.png (PIL, no text chunks), crops 512 x 512 plate px
(5.1 m across) centred on the candidate:
  positives:  R-C9-155's invented door, BVR hall plate (10311, 4925), with the BVR zone map;
              a stamped doorway on v1 (p6_geometry's constructed stamp, 2.2 x 2.6 m at uv (-6, 1)), with v1's guide;
  negatives:  v1's declared barrow door, with v1's guide (barrow_full/paint/barrow_full_guide.png, what v1's painter was given);
              the 17 BVR hall timber candidates (v0.1's other hall flags), with the BVR zone map.
ACCEPTANCE (R-C9-169): both positives "yes"; v1's declared door "no"; at most 2 "yes" on the 17 timber items.
SCORE: p6_judge.py score <answers.json>   answers = {"item_NN": "yes" | "no"}
"""
import argparse
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p6_geometry as G

CROP = 512
GAP = 24
OUT = PH / "p6_judge"


def _crop(img, x, y):
    H, W = img.shape[:2]
    x0 = int(min(max(x - CROP // 2, 0), W - CROP))
    y0 = int(min(max(y - CROP // 2, 0), H - CROP))
    return img[y0:y0 + CROP, x0:x0 + CROP], (x0, y0)


def items():
    out = []
    # BVR hall: the painting (stitched BVR blocks) and the zone map it was painted from, same plate pixels
    keys = G.BLOCKS["BVR hall (T2a, 7_5..8_7)"]
    paint, (bx0, by0) = G.bvr_block(keys)
    Z = np.asarray(Image.open(B2 / "paint/barrow_v2_zonemap.png").convert("RGB").crop(
        (bx0, by0, bx0 + paint.shape[1], by0 + paint.shape[0])), np.float32)
    rows = jload(PH / "results/p6.json")["invention"]["rows"]["BVR hall (T2a, 7_5..8_7)"]["inventions_xy_plate_px"]
    for x, y, a in rows:
        is_door = abs(x - 10311) < 80 and abs(y - 4925) < 80
        pc, (cx0, cy0) = _crop(paint, x - bx0, y - by0)
        gc, _ = _crop(Z, x - bx0, y - by0)
        out.append({"kind": "invented door (R-C9-155)" if is_door else "BVR timber candidate", "expect": "yes" if is_door else "no",
                    "source": "BVR hall T2a", "plate_xy": [x, y], "crop_plate_xy0": [cx0 + bx0, cy0 + by0], "paint": pc, "guide": gc})
    # v1: the painting, its stamped copy and the guide v1's painter was given
    P = load_rgb(BF / "paint/barrow_full_painted.png")
    Gd = load_rgb(BF / "paint/barrow_full_guide.png")
    sx, sy = G.v1_px(-6.0, 1.0, 1.3)
    w, h = 2.2 * PPM_V1, 2.6 * 60.6183
    C = P.copy()
    C[int(sy - h / 2):int(sy + h / 2), int(sx - w / 2):int(sx + w / 2)] = np.array([30, 27, 25], np.float32)
    pc, xy0 = _crop(C, sx, sy)
    out.append({"kind": "stamped doorway (constructed)", "expect": "yes", "source": "v1 + stamp", "plate_xy": [round(sx), round(sy)],
                "crop_plate_xy0": list(xy0), "paint": pc, "guide": _crop(Gd, sx, sy)[0]})
    for d in G.v1_declared():
        x, y = d["xy"]
        pc, xy0 = _crop(P, x, y)
        out.append({"kind": "v1 declared door: " + d["id"], "expect": "no", "source": "v1", "plate_xy": [round(x), round(y)],
                    "crop_plate_xy0": list(xy0), "paint": pc, "guide": _crop(Gd, x, y)[0]})
    return out


JUDGE_MD = """# Painting against its guide

Each image `item_NN.png` shows two squares side by side. LEFT: a crop of a painting. RIGHT: the guide the painter was
given, at exactly the same place.

For each item answer one question:

**Does the painting show a doorway, opening or structure that the guide does not?**

Answer `yes` or `no`. Return a JSON object {"item_01": "yes" or "no", ...} and, per item, one short sentence naming
what you see.
"""


def build(seed=169):
    rng = np.random.default_rng(seed)
    its = items()
    order = rng.permutation(len(its))
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("item_*.png"):
        f.unlink()
    key = {"_what": "P6a stage-2 judge key -- NEVER given to the judge (R-C9-169)", "seed": seed, "crop_px": CROP,
           "acceptance": "both positives yes; v1 declared door no; <= 2 yes on the BVR timber items", "items": {}}
    for n, i in enumerate(order):
        it = its[i]
        comp = np.full((CROP, 2 * CROP + GAP, 3), 255, np.uint8)
        comp[:, :CROP] = np.clip(it["paint"], 0, 255).astype(np.uint8)
        comp[:, CROP + GAP:] = np.clip(it["guide"], 0, 255).astype(np.uint8)
        nm = "item_%02d" % (n + 1)
        Image.fromarray(comp).save(OUT / (nm + ".png"))
        key["items"][nm] = {k: v for k, v in it.items() if k not in ("paint", "guide")}
    (OUT / "JUDGE.md").write_text(JUDGE_MD)
    (PH / "keys").mkdir(parents=True, exist_ok=True)
    dump(key, str(PH / "keys/p6_judge.json"))
    return {"dir": str(OUT), "items": len(its), "positives": sum(i["expect"] == "yes" for i in its),
            "timber": sum(i["kind"] == "BVR timber candidate" for i in its)}


def score(answers):
    key = jload(PH / "keys/p6_judge.json")["items"]
    ans = {k: str(v).strip().lower() for k, v in jload(answers).items()}
    yes = lambda k: ans.get(k, "").startswith("y")
    pos = [k for k, v in key.items() if v["expect"] == "yes"]
    v1d = [k for k, v in key.items() if v["kind"].startswith("v1 declared")]
    tim = [k for k, v in key.items() if v["kind"] == "BVR timber candidate"]
    r = {"positives_flagged": sum(yes(k) for k in pos), "positives": len(pos),
         "v1_declared_flagged": sum(yes(k) for k in v1d), "timber_yes": sum(yes(k) for k in tim), "timber": len(tim),
         "missing_answers": [k for k in key if k not in ans]}
    r["acceptance"] = r["positives_flagged"] == len(pos) and r["v1_declared_flagged"] == 0 and r["timber_yes"] <= 2 and not r["missing_answers"]
    r["fallback_if_failed"] = "(a) conductor triage by eye, logged per chunk (R-C9-169)"
    return r


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("build")
    s = sub.add_parser("score")
    s.add_argument("answers")
    a = ap.parse_args()
    if a.cmd == "score":
        print(json.dumps(score(a.answers), indent=1))
    else:
        r = build()
        print(r)
        dump(r, str(PH / "results/p6_judge_build.json"))
