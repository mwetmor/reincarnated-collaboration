#!/usr/bin/env python3
"""C-9 image bake-off, JOB 1: the barbarian base sheet -- mirror IoU and view consistency.

    python3 03_score_j1.py

Same instrument as every sheet in this run (32_score_sheets.py / 51_kit_score.py), on the same
cut the T8 pipeline used for NB-1 (nb_t8/01_matte_views.py): the WHOLE sheet matted by fal
BiRefNet v2 (General Use Heavy, 2048), the 2x2 grid split at the halves -- top-left FRONT,
top-right RIGHT, bottom-left BACK, bottom-right LEFT, as the brief lays it out -- and the
largest component per quarter kept, so a stray label or border line cannot vote.

    mirror_iou   RIGHT against LEFT mirrored: the constraint a drawing cannot fake
    pair_iou     FRONT against BACK mirrored
    height_cv    spread of the four figure heights -- "one scale" as a number
    fill         figure height / quarter height; the brief asks for "most of its quarter"
    plate_green  share of plate pixels within 40 of pure #00ff00 -- the brief's plate

Astra's two sheets reuse the T8 pipeline's own mattes (nb_t8/nb1_{a,b}_rgba.png), so they are
scored on exactly the silhouettes their Tripo build was made from.
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
C9 = HERE.parent
os.environ["FAL_LEDGER"] = str(HERE / "fal_spend_R-C9-79.json")
os.environ["FAL_BUDGET"] = "5.00"
sys.path.insert(0, str(C9 / "t10_barrow"))
import fal_ledger  # noqa: E402

VIEWS = ["front", "right", "back", "left"]
QUAD = {"front": (0, 0), "right": (1, 0), "back": (0, 1), "left": (1, 1)}
SHEETS = {
    "astra_a": (C9 / "artifacts/NB-1/NB-1_a.png", C9 / "nb_t8/nb1_a_rgba.png"),
    "astra_b": (C9 / "artifacts/NB-1/NB-1_b.png", C9 / "nb_t8/nb1_b_rgba.png"),
    "nb_a": (HERE / "out/J1_nb_a.png", None), "nb_b": (HERE / "out/J1_nb_b.png", None),
    "nbp_a": (HERE / "out/J1_nbp_a.png", None), "nbp_b": (HERE / "out/J1_nbp_b.png", None),
}


def matte(src: pathlib.Path, dst: pathlib.Path) -> pathlib.Path:
    if dst.exists():
        return dst
    import fal_client
    fal_ledger.check("fal-ai/birefnet/v2")
    with fal_ledger.timed() as tm:
        url = fal_client.upload_file(str(src))
        r = fal_client.subscribe("fal-ai/birefnet/v2", arguments={
            "image_url": url, "model": "General Use (Heavy)", "operating_resolution": "2048x2048",
            "output_format": "png", "refine_foreground": True})
    subprocess.run(["curl", "-s", "-L", "-o", str(dst), r["image"]["url"]], check=True)
    tot = fal_ledger.record("fal-ai/birefnet/v2", "J1 matte %s" % src.name, tm.s)
    print("   matte %s  %.1f s  fal running $%.4f" % (src.name, tm.s, tot))
    return dst


def quarters(rgba):
    a = np.asarray(rgba)[..., 3] > 128
    H, W = a.shape
    out = {}
    for n, (c, r) in QUAD.items():
        q = a[r * H // 2:(r + 1) * H // 2, c * W // 2:(c + 1) * W // 2]
        lab, k = ndimage.label(q)
        if k == 0:
            out[n] = None
            continue
        m = lab == 1 + int(np.argmax(ndimage.sum(q, lab, range(1, k + 1))))
        out[n] = m
    return out, (H // 2, W // 2)


def crop(m):
    ys, xs = np.nonzero(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def iou(a, b, n=256):
    def fit(m):
        m = crop(m)
        s = n / max(m.shape)
        q = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize(
            (max(1, round(m.shape[1] * s)), max(1, round(m.shape[0] * s))), Image.BILINEAR)) > 127
        o = np.zeros((n, n), bool)
        y, x = (n - q.shape[0]) // 2, (n - q.shape[1]) // 2
        o[y:y + q.shape[0], x:x + q.shape[1]] = q
        return o
    A, B = fit(a), fit(b)
    u = (A | B).sum()
    return float((A & B).sum() / u) if u else 0.0


def plate_green(rgb, alpha):
    p = ~(alpha > 128)
    d = np.abs(rgb[..., :3].astype(int) - np.array([0, 255, 0])).max(-1)
    return float((d[p] <= 40).mean()) if p.any() else 0.0


def main() -> None:
    (HERE / "mattes").mkdir(exist_ok=True)
    rep = {}
    for name, (sheet, m) in SHEETS.items():
        mp = m or matte(sheet, HERE / "mattes" / ("J1_%s_rgba.png" % name))
        rgba = Image.open(mp).convert("RGBA")
        q, (qh, qw) = quarters(rgba)
        if any(q[v] is None for v in VIEWS):
            rep[name] = {"error": "a quarter has no figure"}
            print("%-8s a quarter has no figure" % name)
            continue
        s = {v: crop(q[v]) for v in VIEWS}
        hs = [s[v].shape[0] for v in VIEWS]
        ws = [s[v].shape[1] for v in VIEWS]
        src = np.asarray(Image.open(sheet).convert("RGB"))
        al = np.asarray(rgba)[..., 3]
        if src.shape[:2] != al.shape:
            src = np.asarray(Image.open(sheet).convert("RGB").resize(al.shape[::-1]))
        r = {"size": list(Image.open(sheet).size),
             "mirror_iou": round(iou(s["right"], s["left"][:, ::-1]), 3),
             "pair_iou": round(iou(s["front"], s["back"][:, ::-1]), 3),
             "height_cv": round(float(np.std(hs) / np.mean(hs)), 4),
             "width_cv": round(float(np.std(ws) / np.mean(ws)), 4),
             "fill": round(float(np.mean(hs)) / qh, 3),
             "plate_green": round(plate_green(src, al), 3),
             "heights_px": hs, "widths_px": ws, "matte": str(mp)}
        rep[name] = r
        print("%-8s mirror %.3f  pair %.3f  height_cv %.4f  fill %.2f  plate #00ff00 %.2f  %s"
              % (name, r["mirror_iou"], r["pair_iou"], r["height_cv"], r["fill"],
                 r["plate_green"], r["size"]))
    (HERE / "score_j1.json").write_text(json.dumps(rep, indent=1) + "\n")


if __name__ == "__main__":
    main()
