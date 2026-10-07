#!/usr/bin/env python3
"""BV2F lane LV, Phase 1.2: model sheet -> cells -> placed views -> Tripo -> reduced -> UNIFORM normalise.

    python3 fid/lv/tools/lv_build.py cells <obj>        cut the 3x2 sheet (FRONT RIGHT BACK / LEFT TOP -)
    python3 fid/lv/tools/lv_build.py score <obj>        view-consistency of the cut (mirror IoU, heights)
    python3 fid/lv/tools/lv_build.py place <obj>        the four eye-level views on 1024 canvases (one scale)
    python3 fid/lv/tools/lv_build.py build <obj>        Tripo H3.1 multiview on fal (ONE build, ledgered)
    python3 fid/lv/tools/lv_build.py reduce <obj>       Blender decimate + 1024 JPEG (t10_barrow/39_reduce.py)
    python3 fid/lv/tools/lv_build.py normalise <obj> <length_m> [yaw_fix]   UNIFORM scale (C7 fix) -> data/bv2f/models

Lane BVP's method (barrow_v2/models/tools/bvm_build.py) with the C7 fixes: the sheet carries a 53-deg TOP cell
(not sent to Tripo; it is the look reference for the play camera) and normalisation is ONE uniform scale -- the
build keeps its own proportions; the layout is fitted to the model, not the model to a slot.
fal: every paid call through t10_barrow/fal_ledger.py, this lane's own file fid/lv/fal_spend_BV2F.json, $8.00 cap.
"""
import json
import os
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
LV = HERE.parent
C9 = LV.parent.parent.parent
ART = C9 / "artifacts"
MD = LV / "models"
BF_DATA = C9 / "barrow_full" / "godot" / "data" / "bv2f" / "models"
LOCK = C9.parent / "C-7" / "conductor_scripts" / "heavy_lock.py"
os.environ.setdefault("FAL_LEDGER", str(LV / "fal_spend_BV2F.json"))
os.environ.setdefault("FAL_BUDGET", "8.00")
os.environ.setdefault("FAL_LEDGER_NOTE", "BV2F lane LV Phase 1.2 model kit v3 (charter s6: Phase 1 <= $8 fal)")
sys.path.insert(0, str(C9 / "t10_barrow"))
import fal_ledger as FL  # noqa: E402

VIEWS = ["front", "right", "back", "left"]
TRIPO_ORDER = ["front", "left", "back", "right"]          # THE ORDER IS THE TRAP (bvm_build.py)
for d in ("cells", "placed", "builds", "reduced", "work", "stills"):
    (MD / d).mkdir(parents=True, exist_ok=True)


def sheet_path(obj):
    return ART / f"BV2F-LV-{obj}" / f"BV2F-LV-{obj}.png"


def green_key(im):
    a = np.asarray(im.convert("RGB")).astype(np.int32)
    g = (a[..., 1] > 150) & (a[..., 1] - np.maximum(a[..., 0], a[..., 2]) > 70)
    return g, float(g.mean())


def matte(img, dst):
    if not dst.exists():
        import fal_client
        tmp = dst.with_suffix(".src.png")
        img.save(tmp)
        FL.check("fal-ai/birefnet/v2")
        with FL.timed() as t:
            url = fal_client.upload_file(str(tmp))
            r = fal_client.subscribe("fal-ai/birefnet/v2", arguments={
                "image_url": url, "model": "General Use (Heavy)", "operating_resolution": "2048x2048",
                "output_format": "png", "refine_foreground": True})
            subprocess.run(["curl", "-s", "-L", "-o", str(dst), r["image"]["url"]], check=True)
        FL.record("fal-ai/birefnet/v2", dst.name, t.s)
    return Image.open(dst).convert("RGBA")


def cells(obj):
    im = Image.open(sheet_path(obj)).convert("RGB")
    W, H = im.size
    cw, ch = W // 3, H // 2
    g, frac = green_key(im)
    if frac > 0.25:
        alpha = ndimage.binary_opening(~g, iterations=2)
        full = Image.fromarray(np.dstack([np.asarray(im), (alpha * 255).astype(np.uint8)]), "RGBA")
        how = "green key"
    else:
        full = matte(im, MD / "work" / f"{obj}_matte.png")
        how = "matte"
    meta = {"sheet": str(sheet_path(obj)), "green_frac": round(frac, 3), "cut": how, "views": {}}
    # The painter does not keep to the 512 grid (the TOP view of BV2F-LV-wreck spans two cells): cut by OBJECT,
    # not by cell -- the five largest connected blobs (dilated so a mast or stay joins its hull), row by the
    # blob's centre (top / bottom half), then left -> right: FRONT RIGHT BACK / LEFT TOP.
    A = np.asarray(full)[..., 3] > 128
    lab, n = ndimage.label(ndimage.binary_dilation(A, iterations=6))
    sizes = ndimage.sum(A, lab, range(1, n + 1))
    big = 1 + np.argsort(sizes)[::-1][:5]
    boxes = []
    for b in big:
        ys, xs = np.nonzero((lab == b) & A)
        boxes.append((int(b), xs.min(), ys.min(), xs.max() + 1, ys.max() + 1, (ys.min() + ys.max()) / 2, (xs.min() + xs.max()) / 2))
    top = sorted([b for b in boxes if b[5] < H / 2], key=lambda b: b[6])
    bot = sorted([b for b in boxes if b[5] >= H / 2], key=lambda b: b[6])
    if len(top) != 3 or len(bot) != 2:
        sys.exit(f"[lv_build] HALT: {obj} sheet has {len(top)} top-row / {len(bot)} bottom-row objects, expected 3 / 2")
    order = dict(zip(["front", "right", "back", "left", "top"], top + bot))
    for nm, (b, x0, y0, x1, y1, _, _) in order.items():
        pad = 8
        arr = np.asarray(full).copy()
        arr[..., 3] = np.where(lab == b, arr[..., 3], 0)
        cell = Image.fromarray(arr, "RGBA").crop((max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)))
        cw_, ch_ = cell.size
        ca = np.asarray(cell)[..., 3] > 128
        ys, xs = np.nonzero(ca)
        touch = bool(x0 == 0 or y0 == 0 or x1 == W or y1 == H)
        cell.save(MD / "cells" / f"{obj}_{nm}.png")
        meta["views"][nm] = {"bbox_sheet": [int(x0), int(y0), int(x1), int(y1)], "touches_edge": touch}
        print(f"  {obj} {nm}: {how} sheet bbox {meta['views'][nm]['bbox_sheet']}{'  TOUCHES EDGE' if touch else ''}")
    (MD / "cells" / f"{obj}.json").write_text(json.dumps(meta, indent=1) + "\n")


def sil(p):
    a = np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128
    ys, xs = np.nonzero(a)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def iou(a, b, n=256):
    A = np.asarray(Image.fromarray(a).resize((n, n))) > 0
    B = np.asarray(Image.fromarray(b).resize((n, n))) > 0
    return float((A & B).sum() / max((A | B).sum(), 1))


def score(obj):
    s = {n: sil(MD / "cells" / f"{obj}_{n}.png") for n in VIEWS}
    hs = [x.shape[0] for x in s.values()]
    r = {"mirror_iou_left_right": round(iou(s["right"], s["left"][:, ::-1]), 3),
         "front_back_mirror_iou": round(iou(s["front"], s["back"][:, ::-1]), 3),
         "height_cv": round(float(np.std(hs) / np.mean(hs)), 3),
         "front_w_over_h": round(s["front"].shape[1] / s["front"].shape[0], 3),
         "side_w_over_h": round(s["right"].shape[1] / s["right"].shape[0], 3),
         "front_w_over_side_w": round(s["front"].shape[1] / s["right"].shape[1], 3)}
    (MD / "cells" / f"{obj}_score.json").write_text(json.dumps(r, indent=1) + "\n")
    print(obj, r)


def place(obj, canvas=1024, fill=0.86, base=0.94):
    figs = {}
    for nm in VIEWS:
        im = Image.open(MD / "cells" / f"{obj}_{nm}.png").convert("RGBA")
        a = np.asarray(im)[..., 3] > 128
        ys, xs = np.nonzero(a)
        figs[nm] = im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
    big = max(max(f.size) for f in figs.values())
    s = fill * canvas / big
    for nm, f in figs.items():
        r = f.resize((max(1, round(f.width * s)), max(1, round(f.height * s))), Image.LANCZOS)
        can = Image.new("RGB", (canvas, canvas), (255, 255, 255))
        can.paste(r, ((canvas - r.width) // 2, int(canvas * base) - r.height), r)
        can.save(MD / "placed" / f"{obj}_{nm}.jpg", quality=95)
    (MD / "placed" / f"{obj}.json").write_text(json.dumps({"scale": round(s, 4), "sizes": {k: list(f.size) for k, f in figs.items()}}, indent=1) + "\n")
    print(obj, "placed at scale", round(s, 4))


def build(obj):
    import fal_client
    glb = MD / "builds" / f"{obj}.glb"
    if glb.exists():
        print(obj, "already built")
        return
    ep = "tripo3d/h3.1/multiview-to-3d"
    FL.check(ep)
    urls = [fal_client.upload_file(str(MD / "placed" / f"{obj}_{n}.jpg")) for n in TRIPO_ORDER]
    with FL.timed() as t:
        r = fal_client.subscribe(ep, arguments={"image_urls": urls, "texture": True, "pbr": False, "texture_quality": "detailed"})
    FL.record(ep, f"build {obj}")
    url = (r.get("model_mesh") or {}).get("url")
    if not url:
        print(obj, "NO MESH", list(r))
        return
    subprocess.run(["curl", "-s", "-L", "-o", str(glb), url], check=True)
    (MD / "builds" / f"{obj}.json").write_text(json.dumps({"endpoint": ep, "view_order_sent": TRIPO_ORDER, "elapsed_s": round(t.s, 1), "result": r}, indent=1) + "\n")
    print(obj, "built", round(t.s, 1), "s; fal running $", FL.total())


def reduce(obj, tris="40000"):
    subprocess.run(["python3", str(LOCK), "C-9", "--", "blender", "--background", "--python",
                    str(C9 / "t10_barrow" / "39_reduce.py"), "--", str(MD / "builds" / f"{obj}.glb"),
                    str(MD / "reduced" / f"{obj}.glb"), str(tris), "1024"], check=True)


def normalise(obj, length_m, yaw_fix="0"):
    BF_DATA.mkdir(parents=True, exist_ok=True)
    subprocess.run(["python3", str(LOCK), "C-9", "--", "blender", "--background", "--python",
                    str(HERE / "lv_normalise_blender.py"), "--", str(MD / "reduced" / f"{obj}.glb"),
                    str(BF_DATA / f"{obj}.glb"), str(length_m), str(yaw_fix), str(MD / "stills"), obj,
                    str(MD / "stills" / f"{obj}_dims.json")], check=True)


if __name__ == "__main__":
    c = sys.argv[1]
    {"cells": lambda: cells(sys.argv[2]), "score": lambda: score(sys.argv[2]), "place": lambda: place(sys.argv[2]),
     "build": lambda: build(sys.argv[2]), "reduce": lambda: reduce(sys.argv[2], *(sys.argv[3:4])),
     "normalise": lambda: normalise(sys.argv[2], sys.argv[3], *(sys.argv[4:5]))}[c]()
