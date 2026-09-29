#!/usr/bin/env python3
"""C-9 meshy_t2 step 19: cut back both variants of a full sheet and choose one.

    python3 scripts/25_pick_sheets.py [--clips ...] [--dirs ...] [--apply]

R-C9-66 made per-frame paint the primary method, so every direction arrives as
a pair of full 4x3 sheets and one of them has to be chosen. The choice is per
SHEET (not per cell): a sheet is one Astra pass and its cells share a look, so
mixing halves of two variants would put two slightly different creatures in
one cycle.

Three gates per FRAME, the same ones as before plus the one the briefs were
written around:

  pose        IoU of the painted alpha against the render's own mask, best
              over eroding 0/1/2 px so the matte's ink band is not scored as
              drift. Refuse under 0.80.
  MATTE_FAT   painted area over the render's area. Over 1.6 means the
              background came through the matte.
  face excess bare skin in the head box, MINUS the render's own, as an
              absolute fraction. This is THE one to watch: the briefs carry the
              head-orientation wording by azimuth, and a face painted on a head
              turned away is the known failure.

              Written first as a RATIO to the render, it failed all four N
              sheets in both variants -- 3.2x to 6.5x, every cell -- and would
              have sent the conductor to re-fire four sheets that are correct.
              Opening the crops settled it: the painted N cells show the BACK
              OF A HEAD, hair only, exactly as briefed. Two things were wrong.
              First, "bare skin" was warm AND light, which counts bright blonde
              hair; the new sheets paint the hair lighter than the render, so
              the hair itself scored as skin. Skin is PINK and blonde hair is
              GOLDEN, so the test is now (R-G) > 0.15 AND (R-G) > 1.5*(G-B) --
              measured, a real face runs (R-G)/(G-B) 1.8-2.2 and this hair runs
              1.1-1.3. Second, and worse, a RATIO against the N view is a
              division by nearly zero: the render's own skin fraction there is
              0.0007-0.0057, so any paint at all divides to a huge number. The
              DIFFERENCE has no such failure mode. A real face fills 0.10-0.21
              of the head box, so an excess of 0.06 is about a third of a face
              and is where the refusal sits; 0.03 warns.

A sheet is ACCEPTABLE if no frame fails. Where both variants fail the same
cell, that is reported for the conductor to re-fire -- this script never
re-fires, the lane is conductor-owned.
"""
import argparse, json, os, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
ART = os.path.join(os.path.dirname(ROOT), "artifacts")
WORK = os.path.join(ROOT, "work")
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
CLIPS = {"idle": 12, "walk": 12, "run": 8, "attack": 12}
POSE_MIN, POSE_WARN = 0.80, 0.90
MATTE_MAX = 1.60
FACE_EXCESS_MAX, FACE_EXCESS_WARN = 0.060, 0.030


def srgb(x):
    x = np.clip(np.asarray(x, dtype=np.float64), 0.0, 1.0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(x, 1 / 2.4) - 0.055)


def head_box(clip, d, i, pad=10):
    rp = json.load(open(os.path.join(OUT, clip, "render_%s.json" % clip)))
    col = srgb(np.array(rp["guides"]["bone_colours"]["head"], dtype=np.float64))
    a = np.asarray(Image.open(os.path.join(
        OUT, clip, "guides_part", d, "part_%s_%02d.png" % (d, i))).convert("RGBA")
    ).astype(np.float64)
    hit = (a[..., 3] > 128) & (np.abs(a[..., :3] / 255.0 - col).max(-1) < 0.02)
    if hit.sum() < 20:
        return None
    ys, xs = np.nonzero(hit)
    return (max(0, xs.min() - pad), max(0, ys.min() - pad),
            min(512, xs.max() + pad + 1), min(512, ys.max() + pad + 1))


def flesh(png, bb):
    """Bare-skin fraction of the head box. PINK, not merely warm: blonde hair
    is golden (G-B comparable to R-G) and skin is pink (R-G dominant)."""
    im = np.asarray(Image.open(png).convert("RGBA")).astype(np.float64)
    x0, y0, x1, y1 = bb
    sub = im[y0:y1, x0:x1]
    al = sub[..., 3] > 128
    if al.sum() < 10:
        return 0.0
    rgb = sub[..., :3] / 255.0
    rg = rgb[..., 0] - rgb[..., 1]
    gb = rgb[..., 1] - rgb[..., 2]
    sel = al & (rg > 0.15) & (rg > 1.5 * gb) & (rgb.mean(-1) > 0.55)
    return float(sel.sum()) / float(al.sum())


def grade(png, clip, d, i):
    a = np.asarray(Image.open(png).convert("RGBA"))[..., 3] > 128
    m = np.asarray(Image.open(os.path.join(
        OUT, clip, "guides_mask", d, "mask_%s_%02d.png" % (d, i))).convert("RGBA"))[..., 3] > 128
    best = (-1.0, 0)
    for r in (0, 1, 2):
        e = a if r == 0 else ndi.binary_erosion(a, np.ones((2 * r + 1,) * 2))
        v = float((e & m).sum()) / max(float((e | m).sum()), 1.0)
        if v > best[0]:
            best = (v, r)
    iou, er = best
    ratio = float(a.sum()) / max(float(m.sum()), 1.0)
    bb = head_box(clip, d, i)
    fr = None; fpaint = fref = None
    if bb:
        fref = flesh(os.path.join(OUT, clip, "colour", d,
                                  "%s_%s_%02d.png" % (clip, d, i)), bb)
        fpaint = flesh(png, bb)
        fr = fpaint - fref
    v = "ok"
    if ratio > MATTE_MAX:
        v = "MATTE_FAT"
    elif iou < POSE_MIN:
        v = "POSE_FAIL"
    elif fr is not None and fr > FACE_EXCESS_MAX:
        v = "FACE_FAIL"
    elif iou < POSE_WARN:
        v = "pose_warn"
    elif fr is not None and fr > FACE_EXCESS_WARN:
        v = "face_warn"
    return dict(frame=i, iou=round(iou, 4), erode_px=er,
                area_ratio=round(ratio, 3),
                face_excess=(round(fr, 4) if fr is not None else None),
                skin_paint=(round(fpaint, 4) if fpaint is not None else None),
                skin_render=(round(fref, 4) if fref is not None else None),
                verdict=v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clips", default="walk,idle,run,attack")
    ap.add_argument("--dirs", default="S,SW,W,NW,N,NE")
    ap.add_argument("--variants", default="a,b")
    ap.add_argument("--skip-cutback", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    rep = dict(thresholds=dict(pose_min=POSE_MIN, pose_warn=POSE_WARN,
                               matte_max=MATTE_MAX,
                               face_excess_max=FACE_EXCESS_MAX,
                               face_excess_warn=FACE_EXCESS_WARN),
               sheets={}, refire=[])
    choice = {}
    print("%-7s %-4s %-3s %7s %7s %7s  %s"
          % ("clip", "dir", "var", "IoU min", "area", "face+max", "verdict"))
    for clip in args.clips.split(","):
        n = CLIPS[clip]
        for d in args.dirs.split(","):
            art = "T2P-%s-%s" % (clip, d)
            lay = os.path.join(ROOT, "astra_in", "mc_%s_%s_sheet_layout.json" % (clip, d))
            per = {}
            for v in args.variants.split(","):
                sheet = os.path.join(ART, art, "%s_%s.png" % (art, v))
                if not os.path.exists(sheet):
                    continue
                dest = os.path.join(ROOT, "paint_%s" % v)
                if not args.skip_cutback:
                    subprocess.run([sys.executable,
                                    os.path.join(HERE, "18_cutback_t2.py"),
                                    sheet, lay, dest, "--report",
                                    os.path.join(WORK, "cut_%s_%s.json" % (art, v))],
                                   check=True, capture_output=True)
                rows = [grade(os.path.join(dest, clip, d,
                                           "%s_%s_%02d.png" % (clip, d, i)), clip, d, i)
                        for i in range(n)]
                bad = [r for r in rows if r["verdict"] in
                       ("MATTE_FAT", "POSE_FAIL", "FACE_FAIL")]
                warn = [r for r in rows if r["verdict"].endswith("warn")]
                per[v] = dict(rows=rows, bad=[r["frame"] for r in bad],
                              warn=[r["frame"] for r in warn],
                              iou_min=min(r["iou"] for r in rows),
                              area_max=max(r["area_ratio"] for r in rows),
                              face_max=max((r["face_excess"] or 0) for r in rows),
                              acceptable=not bad,
                              score=(min(r["iou"] for r in rows)
                                     - 3.0 * max((r["face_excess"] or 0) for r in rows)
                                     - 0.05 * len(warn)))
                print("%-7s %-4s %-3s %7.3f %7.2f %7.2f  %s"
                      % (clip, d, v, per[v]["iou_min"], per[v]["area_max"],
                         per[v]["face_max"],
                         "OK" if per[v]["acceptable"]
                         else "/".join(sorted({r["verdict"] for r in bad}))
                              + " f" + ",".join(str(r["frame"]) for r in bad)))
            good = {k: v for k, v in per.items() if v["acceptable"]}
            pick = max(good, key=lambda k: good[k]["score"]) if good else None
            rep["sheets"]["%s/%s" % (clip, d)] = dict(variants=per, chosen=pick)
            if pick:
                choice.setdefault(clip, {})[d] = pick
            else:
                both = sorted(set.intersection(*[set(v["bad"]) for v in per.values()])) \
                    if per else []
                rep["refire"].append(dict(sheet="%s/%s" % (clip, d),
                                          cells_failing_in_every_variant=both,
                                          per_variant={k: v["bad"] for k, v in per.items()}))
            print("   -> %s\n" % (("chose %s" % pick) if pick else "NO VARIANT PASSES"))
    rep["choice"] = choice
    json.dump(rep, open(os.path.join(WORK, "sheet_choice.json"), "w"), indent=1)
    if args.apply and choice:
        cp = os.path.join(WORK, "chosen.json")
        ch = json.load(open(cp))
        for clip, ds in choice.items():
            ch.setdefault(clip, {}).update(ds)
        json.dump(ch, open(cp, "w"), indent=1)
        print("wrote choices into work/chosen.json")
    if rep["refire"]:
        print("RE-FIRE (conductor): %s"
              % ", ".join("%s cells %s" % (r["sheet"],
                                           r["cells_failing_in_every_variant"])
                          for r in rep["refire"]))


if __name__ == "__main__":
    main()
