#!/usr/bin/env python3
"""barrow_v2 hero models (lane BVP, drax; R-C9-155): sheet -> cells -> placed views -> Tripo -> reduced GLB.

    python3 models/tools/bvm_build.py cells <sheet> [a|b]     matte + cut the sheet's views  (BiRefNet on fal)
    python3 models/tools/bvm_build.py score                   view-consistency scores of every cut variant
    python3 models/tools/bvm_build.py place <obj> <a|b>       the chosen variant's four views on 1024 canvases
    python3 models/tools/bvm_build.py build <obj>             Tripo H3.1 multiview (fal), one build
    python3 models/tools/bvm_build.py reduce <obj> [tris]     Blender decimate + 1024 JPEG textures (t10_barrow/39_reduce.py)

The method of t10_barrow 31/32/33/34/39 unchanged (cut by a detail profile per band, matte per band, the four views at
one common scale, front/LEFT/back/RIGHT to Tripo -- THE ORDER IS THE TRAP), generalised to this lane's sheets:
2 x 2 sheets (one object) and 4 x 2 sheets (two objects, one per row). Every fal call goes through the spend ledger
(t10_barrow/fal_ledger.py) under this lane's own file and cap: models/fal_spend_R-C9-155.json, $5.00.
"""
import json, os, pathlib, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
M = HERE.parent
C9 = M.parent.parent
ART = C9 / "artifacts"
os.environ.setdefault("FAL_LEDGER", str(M / "fal_spend_R-C9-155.json"))
os.environ.setdefault("FAL_BUDGET", "5.00")
os.environ.setdefault("FAL_LEDGER_NOTE", "lane BVP hero models under R-C9-155 (Matt: fal up to $5)")
sys.path.insert(0, str(C9 / "t10_barrow"))
import fal_ledger as FL  # noqa: E402

VIEWS = ["front", "right", "back", "left"]
TRIPO_ORDER = ["front", "left", "back", "right"]
SHEETS = {"hall": ("2x2", ["hall"]), "porch": ("2x2", ["porch"]), "gable": ("2x2", ["gable"]),
          "barrow": ("2x2", ["barrow"]), "wreck": ("2x2", ["wreck"]), "wreck2": ("2x2", ["wreck2"]),
          "cliffs": ("4x2", ["cavecliff", "staircliff"]), "rocks": ("4x2", ["cliffplain", "crag"])}
for d in ("work", "cells", "placed", "builds", "reduced"):
    (M / d).mkdir(exist_ok=True)


def matte(img, dst):
    if not dst.exists():
        import fal_client
        tmp = dst.with_suffix(".src.png"); img.save(tmp)
        FL.check("fal-ai/birefnet/v2")
        with FL.timed() as t:
            url = fal_client.upload_file(str(tmp))
            r = fal_client.subscribe("fal-ai/birefnet/v2", arguments={
                "image_url": url, "model": "General Use (Heavy)", "operating_resolution": "2048x2048",
                "output_format": "png", "refine_foreground": True})
            subprocess.run(["curl", "-s", "-L", "-o", str(dst), r["image"]["url"]], check=True)
        FL.record("fal-ai/birefnet/v2", dst.name, t.s)
        tmp.unlink(missing_ok=True)
    return Image.open(dst).convert("RGBA")


def green_key(im):
    """The plate is #00ff00 when the painter kept it: key it out locally (free) before paying for a matte."""
    a = np.asarray(im.convert("RGB")).astype(np.int32)
    g = (a[..., 1] > 150) & (a[..., 1] - np.maximum(a[..., 0], a[..., 2]) > 70)
    frac = g.mean()
    return g, frac


def runs(profile, frac, min_len):
    on = profile > profile.max() * frac
    out, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = i
        elif not v and s is not None:
            if i - s >= min_len: out.append((s, i))
            s = None
    if s is not None and len(on) - s >= min_len: out.append((s, len(on)))
    return out


def widen(rs, lo, hi):
    out = []
    for i, (a, b) in enumerate(rs):
        out.append((lo if i == 0 else (rs[i - 1][1] + a) // 2, hi if i == len(rs) - 1 else (b + rs[i + 1][0]) // 2))
    return out


def cells(sheet, variants):
    kind, objs = SHEETS[sheet]
    meta = json.loads((M / "cells.json").read_text()) if (M / "cells.json").exists() else {}
    for v in variants:
        src = ART / f"BVM-{sheet}" / f"BVM-{sheet}_{v}.png"
        if not src.exists():
            print("missing", src); continue
        im = Image.open(src).convert("RGB")
        W, H = im.size
        g, frac = green_key(im)
        if frac > 0.25:
            alpha = ndimage.binary_opening(~g, iterations=2)
            rgba = np.dstack([np.asarray(im), (alpha * 255).astype(np.uint8)])
            full = Image.fromarray(rgba, "RGBA"); how = "green key"
        else:
            full = None; how = "matte"
        bands = [(0, H // 2), (H // 2, H)]
        names = [[("front", "right")], [("back", "left")]] if kind == "2x2" else None
        for bi, (y0, y1) in enumerate(bands):
            band_rgba = full.crop((0, y0, W, y1)) if full else matte(im.crop((0, y0, W, y1)), M / "work" / f"{sheet}_{v}_band{bi}.png")
            a = np.asarray(band_rgba)[..., 3] > 128
            ncol = 2 if kind == "2x2" else 4
            cr = widen(runs(a.sum(0).astype(np.float32), 0.04, W // (ncol * 5)), 0, W)
            if len(cr) != ncol:
                cr = [(W * i // ncol, W * (i + 1) // ncol) for i in range(ncol)]
                print(f"  {sheet}_{v} band {bi}: column runs disagree -> even split")
            if kind == "2x2":
                obj = objs[0]; vn = ["front", "right"] if bi == 0 else ["back", "left"]
            else:
                obj = objs[bi]; vn = VIEWS
            for ci, (x0, x1) in enumerate(cr):
                cell = band_rgba.crop((x0, 0, x1, y1 - y0))
                ca = np.asarray(cell)[..., 3] > 128
                lab, n = ndimage.label(ca)
                if n > 1:     # keep the main subject and anything sizable touching it; drop specks
                    sizes = ndimage.sum(ca, lab, range(1, n + 1))
                    keep = np.isin(lab, 1 + np.nonzero(sizes > sizes.max() * 0.02)[0])
                    arr = np.asarray(cell).copy(); arr[..., 3] = np.where(keep, arr[..., 3], 0); cell = Image.fromarray(arr, "RGBA"); ca = keep
                ys, xs = np.nonzero(ca)
                touch = bool(ys.min() == 0 or ys.max() == cell.size[1] - 1 or xs.min() == 0 or xs.max() == cell.size[0] - 1)
                cell.save(M / "cells" / f"{obj}_{v}_{vn[ci]}.png")
                meta.setdefault(obj, {}).setdefault(v, {})[vn[ci]] = {"bbox": [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)],
                                                                      "cut": how, "touches_edge": touch}
                print(f"  {obj} {v} {vn[ci]}: {how} bbox {meta[obj][v][vn[ci]]['bbox']}{'  TOUCHES EDGE' if touch else ''}")
    (M / "cells.json").write_text(json.dumps(meta, indent=1) + "\n")


def sil(p):
    a = np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128
    ys, xs = np.nonzero(a)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def iou(a, b, n=256):
    A = np.asarray(Image.fromarray(a).resize((n, n))) > 0; Bm = np.asarray(Image.fromarray(b).resize((n, n))) > 0
    return float((A & Bm).sum() / max((A | Bm).sum(), 1))


def score():
    meta = json.loads((M / "cells.json").read_text())
    res = {}
    for obj, vs in meta.items():
        for v in vs:
            try:
                s = {n: sil(M / "cells" / f"{obj}_{v}_{n}.png") for n in VIEWS}
            except Exception as e:
                continue
            hs = [x.shape[0] for x in s.values()]
            r = {"mirror_iou": round(iou(s["right"], s["left"][:, ::-1]), 3),
                 "front_back_mirror_iou": round(iou(s["front"], s["back"][:, ::-1]), 3),
                 "height_cv": round(float(np.std(hs) / np.mean(hs)), 3),
                 "front_w_over_h": round(s["front"].shape[1] / s["front"].shape[0], 3),
                 "side_w_over_h": round(s["right"].shape[1] / s["right"].shape[0], 3)}
            res.setdefault(obj, {})[v] = r
            print(obj, v, r)
    (M / "scores.json").write_text(json.dumps(res, indent=1) + "\n")


def place(obj, v, canvas=1024, fill=0.86, base=0.94):
    figs = {}
    for nm in VIEWS:
        im = Image.open(M / "cells" / f"{obj}_{v}_{nm}.png").convert("RGBA")
        a = np.asarray(im)[..., 3] > 128
        ys, xs = np.nonzero(a)
        figs[nm] = im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
    big = max(max(f.size) for f in figs.values())
    s = fill * canvas / big
    for nm, f in figs.items():
        r = f.resize((max(1, round(f.width * s)), max(1, round(f.height * s))), Image.LANCZOS)
        can = Image.new("RGB", (canvas, canvas), (255, 255, 255))
        can.paste(r, ((canvas - r.width) // 2, int(canvas * base) - r.height), r)
        can.save(M / "placed" / f"{obj}_{nm}.jpg", quality=95)
    pv = json.loads((M / "placed.json").read_text()) if (M / "placed.json").exists() else {}
    pv[obj] = {"variant": v, "scale": round(s, 4), "sizes": {k: list(f.size) for k, f in figs.items()}}
    (M / "placed.json").write_text(json.dumps(pv, indent=1) + "\n")
    print(obj, v, "placed at scale", round(s, 4))


def build(obj):
    import fal_client
    glb = M / "builds" / f"{obj}.glb"
    if glb.exists():
        print(obj, "already built"); return
    ep = "tripo3d/h3.1/multiview-to-3d"
    FL.check(ep)
    urls = [fal_client.upload_file(str(M / "placed" / f"{obj}_{n}.jpg")) for n in TRIPO_ORDER]
    with FL.timed() as t:
        r = fal_client.subscribe(ep, arguments={"image_urls": urls, "texture": True, "pbr": False, "texture_quality": "detailed"})
    FL.record(ep, f"build {obj}")
    url = (r.get("model_mesh") or {}).get("url") or next((x.get("url") for x in r.values() if isinstance(x, dict) and str(x.get("url", "")).endswith(".glb")), None)
    if not url:
        print(obj, "NO MESH", list(r)); return
    subprocess.run(["curl", "-s", "-L", "-o", str(glb), url], check=True)
    (M / "builds" / f"{obj}.json").write_text(json.dumps({"endpoint": ep, "view_order_sent": TRIPO_ORDER, "elapsed_s": round(t.s, 1), "result": r}, indent=1) + "\n")
    print(obj, "built", round(t.s, 1), "s", round(glb.stat().st_size / 1e6, 1), "MB; fal running $", FL.total())


def reduce(obj, tris="40000"):
    src, dst = M / "builds" / f"{obj}.glb", M / "reduced" / f"{obj}.glb"
    lock = C9.parent / "C-7" / "conductor_scripts" / "heavy_lock.py"
    subprocess.run(["python3", str(lock), "C-9", "--", "blender", "--background", "--python",
                    str(C9 / "t10_barrow" / "39_reduce.py"), "--", str(src), str(dst), str(tris), "1024"], check=True)


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "cells": cells(sys.argv[2], sys.argv[3:] or ["a", "b"])
    elif c == "score": score()
    elif c == "place": place(sys.argv[2], sys.argv[3])
    elif c == "build": [build(o) for o in sys.argv[2:]]
    elif c == "reduce": reduce(sys.argv[2], *(sys.argv[3:4]))
