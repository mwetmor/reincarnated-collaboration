#!/usr/bin/env python3
"""C-9 T10-1b: measure each kit build against its sheet, and each reduction against its build.

    python3 56_kit_measure.py [object ...]

Four questions, four numbers, none of them "it looks right".

1. WHICH WAY IS THE MODEL FACING? There are no identity plates for this kit -- the sheets
   were painted from words, not cut from the concept -- so the reference for yaw is the
   sheet's own FRONT view. The model is rendered orthographically at pitch 0, every 5
   degrees of azimuth, and the azimuth whose silhouette best matches the FRONT cell is the
   model's front. Pitch 0 because the FRONT cell IS a pitch-0 elevation; matching it to a
   52.95-degree render would charge every candidate the same constant penalty and blunt the
   argmax for nothing. `front_iou_spread` is reported so a flat sweep cannot pass as a find.

2. DID THE BUILD KEEP THE SHEET? IoU of the model at front / +90 / +180 / +270 against the
   four sheet cells. The +90 assignment is tested BOTH ways round -- sheet-left at +90 and
   sheet-right at +90 -- because a multiview build fed a swapped pair comes back mirrored
   and entirely plausible, and the only thing that catches it is the pair that fits worse.

3. DID THE THIN PARTS SURVIVE? `thin_recall` is recall measured only on the parts of the
   sheet silhouette that a morphological OPENING removes -- that is, the parts thinner than
   2r px: spear shafts, antler tines, root fingers, branch stubs. Overall IoU cannot see
   these; they are a percent of the area. A number that drops here while IoU holds is
   exactly the failure this kit is at risk of. `min_run_px` is the second half: the
   narrowest horizontal run through the thin region, which says whether a shaft got thin or
   got FAT (a blob has a large min run and a small thin_recall; a vanished shaft has both
   small). One number could not tell those apart.

4. WHAT DID THE REDUCTION COST? IoU of reduced against unreduced through the same camera at
   24 azimuths, at pitch 0 and at the play camera's 52.95 degrees, plus thin_recall of the
   reduced silhouette against the unreduced one. Before-and-after through one camera, which
   is the only comparison in which "silhouette loss" means anything.
"""
import json
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE / "kit_work"
OBJECTS = ["rocks", "stump", "log", "cairn", "skull", "shield"]
VIEWS = ["front", "right", "back", "left"]
PLAY_PITCH = 52.95354112560294
R_THIN = 3          # opening radius in px: removes anything under ~6 px wide at 512


def sil_png(p: pathlib.Path) -> np.ndarray:
    return np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128


def crop(m: np.ndarray) -> np.ndarray:
    ys, xs = np.nonzero(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def fit(m: np.ndarray, n: int = 256) -> np.ndarray:
    m = crop(m)
    s = n / max(m.shape)
    im = Image.fromarray((m * 255).astype(np.uint8)).resize(
        (max(1, round(m.shape[1] * s)), max(1, round(m.shape[0] * s))), Image.BILINEAR)
    o = np.zeros((n, n), bool)
    q = np.asarray(im) > 127
    y, x = (n - q.shape[0]) // 2, (n - q.shape[1]) // 2
    o[y:y + q.shape[0], x:x + q.shape[1]] = q
    return o


def iou(a: np.ndarray, b: np.ndarray) -> float:
    A, B = fit(a), fit(b)
    u = (A | B).sum()
    return float((A & B).sum() / u) if u else 0.0


def thin_mask(m: np.ndarray, r: int = R_THIN) -> np.ndarray:
    """The parts of a silhouette a morphological opening removes: everything under 2r wide."""
    st = np.ones((2 * r + 1, 2 * r + 1), bool)
    return m & ~ndimage.binary_dilation(ndimage.binary_erosion(m, st), st)


def thin_recall(ref: np.ndarray, test: np.ndarray, r: int = R_THIN) -> tuple:
    A, B = fit(ref), fit(test)
    t = thin_mask(A, r)
    n = int(t.sum())
    # A FLOOR, BECAUSE THE MEASURE ANSWERS NOTHING BELOW IT. The rock cluster's front
    # silhouette is a blob: its opening residue is THREE pixels of contour noise, and the
    # recall on those three came back 0.000 -- which reads as "every thin part was lost"
    # about an object that has no thin parts. Under 50 px there is nothing to measure and
    # the honest return is None, not a number that invites a conclusion.
    if n < 50:
        return None, n
    return round(float((t & B).sum() / n), 3), n


def thin_width_px(m: np.ndarray, r: int = R_THIN) -> dict:
    """How WIDE the thin parts are, and how much of the silhouette they are.

    The first version of this took the MINIMUM run through the thin region and it did not
    discriminate: it returned 1 px for the sheet and 1 px for every model, because the
    narrowest run anywhere in a thin region is the tapering tip of something, always, in
    every picture. A measure that returns the same number for the thing being compared and
    the thing it is compared to is answering a question nobody asked.

    The median does discriminate, because a spear shaft is many rows of the same width and
    the tip is few. With `thin_frac` -- the thin region as a share of the whole silhouette --
    it separates the two ways a thin part can be lost, which one number cannot:

        BLOBBED   thin_frac falls, median width RISES, total area holds: the shaft is still
                  there and is now a club.
        VANISHED  thin_frac falls, total area falls: the shaft is gone.
    """
    M = fit(m)
    t = thin_mask(M, r)
    runs = []
    for y in np.nonzero(t.any(1))[0]:
        row, s = M[y], None
        for x, v in enumerate(row):
            if v and s is None:
                s = x
            elif not v and s is not None:
                if t[y, s:x].any():
                    runs.append(x - s)
                s = None
        if s is not None and t[y, s:].any():
            runs.append(len(row) - s)
    return {"median_w": int(np.median(runs)) if runs else 0,
            "p90_w": int(np.percentile(runs, 90)) if runs else 0,
            "thin_px": int(t.sum()), "area_px": int(M.sum()),
            "thin_frac": round(float(t.sum() / max(M.sum(), 1)), 4)}


def probe(glb: pathlib.Path, out: pathlib.Path, pitch: float, step: float, px: int):
    if out.exists() and list(out.glob("*_stats.json")):
        return json.loads(next(out.glob("*_stats.json")).read_text())
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run(["blender", "--background", "--python", str(HERE / "54_kit_probe.py"),
                    "--", str(glb), str(out), str(pitch), str(step), str(px)],
                   check=True, capture_output=True)
    return json.loads(next(out.glob("*_stats.json")).read_text())


def azims(d: pathlib.Path, name: str) -> dict:
    return {int(p.stem.split("az")[1]): p for p in sorted(d.glob("%s_az*.png" % name))}


def main() -> int:
    want = sys.argv[1:] or OBJECTS
    picks = json.loads((WORK / "choose_kit.json").read_text())["picks"]
    rep = {}
    for obj in want:
        v = picks[obj]["variant"]
        sheet = {n: sil_png(WORK / "cells" / ("%s_%s_%s.png" % (obj, v, n))) for n in VIEWS}
        raw, red = WORK / "builds" / ("%s.glb" % obj), WORK / "red8k" / ("%s.glb" % obj)
        s_raw = probe(raw, WORK / "probe2" / ("%s_raw_p0" % obj), 0, 5, 512)
        s_red = probe(red, WORK / "probe2" / ("%s_red_p0" % obj), 0, 5, 512)
        p_raw = probe(raw, WORK / "probe2" / ("%s_raw_pl" % obj), PLAY_PITCH, 15, 512)
        p_red = probe(red, WORK / "probe2" / ("%s_red_pl" % obj), PLAY_PITCH, 15, 512)

        # 1. front azimuth, from the reduced model (reduction does not turn a model, and
        #    the delivered asset is the one whose facing has to be right)
        a_red = azims(WORK / "probe2" / ("%s_red_p0" % obj), obj)
        sc = sorted(((iou(sil_png(p), sheet["front"]), a) for a, p in a_red.items()),
                    reverse=True)
        front_iou, A0 = sc[0]
        spread = front_iou - sc[-1][0]

        # 2. the four views, and the mirror test on the +/-90 pair
        a_raw = azims(WORK / "probe2" / ("%s_raw_p0" % obj), obj)

        def at(d, a):
            return sil_png(d[min(d, key=lambda k: min(abs(k - a % 360), 360 - abs(k - a % 360)))])

        def four(d):
            return {"front": round(iou(at(d, A0), sheet["front"]), 3),
                    "back": round(iou(at(d, A0 + 180), sheet["back"]), 3),
                    "left": round(iou(at(d, A0 + 90), sheet["left"]), 3),
                    "right": round(iou(at(d, A0 + 270), sheet["right"]), 3)}
        v_raw, v_red = four(a_raw), four(a_red)
        swapped = {"left": round(iou(at(a_red, A0 + 270), sheet["left"]), 3),
                   "right": round(iou(at(a_red, A0 + 90), sheet["right"]), 3)}
        asis = (v_red["left"] + v_red["right"]) / 2
        swp = (swapped["left"] + swapped["right"]) / 2

        # 3. thin parts, against the sheet's FRONT
        tr_raw, npx = thin_recall(sheet["front"], at(a_raw, A0))
        tr_red, _ = thin_recall(sheet["front"], at(a_red, A0))
        # RECALL WITH A TOLERANCE, because the overlay says the tines are DISPLACED, not
        # gone: every antler point and both spear shafts are in the model at the painted
        # width, turned a few degrees off where the sheet drew them. Strict recall scores a
        # present-but-rotated tine exactly as it scores a missing one. Dilating the model by
        # 4 px of a 256-px fit -- about 1.5% of the object -- separates the two: a part that
        # is there recovers, a part that is gone does not.
        st4 = np.ones((9, 9), bool)
        tr_raw4, _ = thin_recall(sheet["front"],
                                 ndimage.binary_dilation(fit(at(a_raw, A0)), st4))
        tr_red4, _ = thin_recall(sheet["front"],
                                 ndimage.binary_dilation(fit(at(a_red, A0)), st4))
        runs = {"sheet": thin_width_px(sheet["front"]), "raw": thin_width_px(at(a_raw, A0)),
                "red": thin_width_px(at(a_red, A0))}

        # 4. what the reduction cost, through one camera
        def loss(dr, dd):
            ks = sorted(set(dr) & set(dd))
            xs = [iou(sil_png(dr[k]), sil_png(dd[k])) for k in ks]
            return {"mean": round(float(np.mean(xs)), 4), "min": round(float(np.min(xs)), 4),
                    "worst_az": int(ks[int(np.argmin(xs))]), "n": len(ks)}
        l0 = loss(a_raw, a_red)
        lp = loss(azims(WORK / "probe2" / ("%s_raw_pl" % obj), obj),
                  azims(WORK / "probe2" / ("%s_red_pl" % obj), obj))
        tr_rr, nrr = thin_recall(at(a_raw, A0), at(a_red, A0))

        rep[obj] = {
            "variant": v, "mirror_iou": picks[obj]["mirror_iou"],
            "front_azimuth_deg": A0, "front_iou": round(front_iou, 3),
            "front_iou_spread_over_azimuth": round(spread, 3),
            "sheet_iou_tripo": v_raw, "sheet_iou_reduced": v_red,
            "sheet_iou_tripo_mean": round(float(np.mean(list(v_raw.values()))), 3),
            "sheet_iou_reduced_mean": round(float(np.mean(list(v_red.values()))), 3),
            "side_pair_asis": round(asis, 3), "side_pair_swapped": round(swp, 3),
            "mirrored": bool(swp > asis + 0.02),
            "thin_recall_vs_sheet": {"tripo": tr_raw, "reduced": tr_red, "thin_px": npx,
                                     "tripo_tol4px": tr_raw4, "reduced_tol4px": tr_red4},
            "thin_recall_reduced_vs_tripo": tr_rr, "thin_width": runs,
            "reduce_loss_pitch0": l0, "reduce_loss_play_pitch": lp,
            "tris": {"tripo": s_raw["tris"], "reduced": s_red["tris"]},
            "islands": {"tripo": s_raw["islands"], "reduced": s_red["islands"]},
            "nonmanifold_edges": {"tripo": s_raw["nonmanifold_edges"],
                                  "reduced": s_red["nonmanifold_edges"]},
            "boundary_edges": {"tripo": s_raw["boundary_edges"],
                               "reduced": s_red["boundary_edges"]},
            "watertight": {"tripo": s_raw["watertight"], "reduced": s_red["watertight"]},
            "size_gltf_tripo": s_raw["size_gltf"], "size_gltf_reduced": s_red["size_gltf"],
        }
        r = rep[obj]
        print("%-7s front az %3d IoU %.3f (spread %.3f) | sheet IoU tripo %.3f red %.3f | "
              "thin %s->%s (tol4 %s->%s) (sheet thin %d px, w %d->%d->%d px, frac %.3f->%.3f->%.3f) | "
              "reduce IoU p0 %.3f play %.3f | "
              "tris %d->%d islands %d->%d watertight %s->%s%s"
              % (obj, A0, front_iou, spread, r["sheet_iou_tripo_mean"],
                 r["sheet_iou_reduced_mean"], tr_raw, tr_red, tr_raw4, tr_red4, npx,
                 runs["sheet"]["median_w"], runs["raw"]["median_w"], runs["red"]["median_w"],
                 runs["sheet"]["thin_frac"], runs["raw"]["thin_frac"], runs["red"]["thin_frac"],
                 l0["mean"], lp["mean"], s_raw["tris"], s_red["tris"],
                 s_raw["islands"], s_red["islands"], s_raw["watertight"], s_red["watertight"],
                 "  MIRRORED?" if r["mirrored"] else ""))
    old = {}
    f = WORK / "kit_measure.json"
    if f.exists():
        old = json.loads(f.read_text())
    old.update(rep)
    f.write_text(json.dumps(old, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
