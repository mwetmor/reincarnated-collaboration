#!/usr/bin/env python3
"""C-9 meshy_t2 step 11: assemble the painted sprites, and gate them.

    python3 scripts/15_assemble.py [--chosen work/chosen.json]

Reads the variant choices gandalf sends (work/chosen.json), takes the
cut-back paint from paint_<variant>/{state}/{dir}/, and writes
    sprites_t2/{state}/{dir}/{state}_{dir}_NN.png
plus sprites_t2/manifest.json.

TWO GATES, because the failure this pipeline actually has is not a bad
painting, it is a MISSING MATTE. Astra loses the green plate on roughly two
firings in five right now and returns the cell as a dark gradient -- it will
assemble, it will not error, and it will look like a sprite in a listing.

  MATTE gate    painted opaque pixels divided by the RENDER'S OWN mask area
                for that exact frame. A ratio, not an absolute.
  POSE gate     IoU of the painted alpha against the same render mask. The
                paint is allowed to move the silhouette a little -- it is a
                painting, not a filter -- but a cell cut back with the wrong
                layout, or painted off the pose, falls off a cliff. Refused
                under 0.80, warned under 0.90.

The MATTE gate was first written as "opaque fraction of the 512 frame > 25 %",
on the assumption that a lost plate arrives as a full-frame rectangle at alpha
255. MEASURED, it does not: the cut-back already strips the darkest part of
the gradient, so a plate-loss cell comes back at 10-16 % of the frame, sails
under a 25 % threshold, and is caught only by IoU. The real signature is
AREA RELATIVE TO THE RENDER -- 5.16x and 3.68x on the two known-bad cells
against 1.04x on a good one -- so that is what is measured. Both failures
show up in IoU either way; the ratio is what tells gandalf WHICH failure it
is, a fat matte or a drifted pose, and those need different re-fires.

Both gates are per FRAME, not per sheet: one bad cell in twelve is the case
worth catching, and a sheet-level average hides exactly that.
"""
import argparse, json, os, shutil, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
SPR = os.path.join(ROOT, "sprites_t2")
FRAME = 512
MATTE_MAX_AREA_RATIO = 1.60      # measured: good 1.04, plate-lost 3.68 and 5.16
POSE_MIN = 0.80
POSE_WARN = 0.90
CLIPS = {"idle": 12, "walk": 12, "run": 8, "attack": 12}


def render_mask(clip, d, i):
    p = os.path.join(OUT, clip, "guides_mask", d, "mask_%s_%02d.png" % (d, i))
    if not os.path.exists(p):
        return None
    return np.array(Image.open(p).convert("RGBA").getchannel("A")) > 128


def grade(png, clip, d, i):
    im = Image.open(png).convert("RGBA")
    a = np.array(im.getchannel("A"))
    opaque = a > 128
    frac = float(opaque.mean())
    m = render_mask(clip, d, i)
    iou = None; ratio = None
    if m is not None:
        inter = float((opaque & m).sum()); union = float((opaque | m).sum())
        iou = inter / max(union, 1.0)
        ratio = float(opaque.sum()) / max(float(m.sum()), 1.0)
    verdict = "ok"
    if ratio is not None and ratio > MATTE_MAX_AREA_RATIO:
        verdict = "MATTE_FAT"
    elif iou is not None and iou < POSE_MIN:
        verdict = "POSE_FAIL"
    elif iou is not None and iou < POSE_WARN:
        verdict = "pose_warn"
    return dict(opaque_frac=round(frac, 4),
                area_ratio=(round(ratio, 4) if ratio is not None else None),
                iou=(round(iou, 4) if iou is not None else None),
                verdict=verdict)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chosen", default=os.path.join(ROOT, "work", "chosen.json"))
    ap.add_argument("--source", default=None,
                    help="override the paint root (e.g. a re-matted tree)")
    args = ap.parse_args()
    chosen = json.load(open(args.chosen))
    man = dict(note="C-9 meshy_t2 painted sprites",
               frame_px=FRAME, px_per_m=110.1852, sole_row=398,
               elevation_deg=19.77,
               azimuths={"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180,
                         "NW": 225, "W": 270, "SW": 315},
               gates=dict(matte_max_area_ratio=MATTE_MAX_AREA_RATIO,
                          pose_min_iou=POSE_MIN, pose_warn_iou=POSE_WARN),
               source={}, states={})
    refused = []
    for clip, dirs in sorted(chosen.items()):
        if clip.startswith("_") or clip not in CLIPS:
            continue                       # notes and comments live in the file too
        n = CLIPS[clip]
        for d, variant in sorted(dirs.items()):
            if variant is None:
                continue
            src_root = args.source or os.path.join(ROOT, "paint_%s" % variant)
            sd = os.path.join(src_root, clip, d)
            rows, ok = [], True
            for i in range(n):
                p = os.path.join(sd, "%s_%s_%02d.png" % (clip, d, i))
                if not os.path.exists(p):
                    rows.append(dict(frame=i, verdict="MISSING")); ok = False
                    continue
                g = grade(p, clip, d, i)
                g["frame"] = i
                rows.append(g)
                if g["verdict"] in ("MATTE_FAT", "POSE_FAIL", "MISSING"):
                    ok = False
            bad = [r for r in rows if r["verdict"] in
                   ("MATTE_FAT", "POSE_FAIL", "MISSING")]
            warn = [r for r in rows if r["verdict"] == "pose_warn"]
            ious = [r["iou"] for r in rows if r.get("iou") is not None]
            entry = dict(variant=variant, source=os.path.relpath(sd, ROOT),
                         frames=n, kind="painted",
                         iou_min=round(min(ious), 4) if ious else None,
                         iou_mean=round(float(np.mean(ious)), 4) if ious else None,
                         opaque_frac_max=round(max(r["opaque_frac"] for r in rows
                                                   if "opaque_frac" in r), 4),
                         area_ratio_max=round(max(r["area_ratio"] for r in rows
                                                  if r.get("area_ratio")), 4),
                         bad_frames=[r["frame"] for r in bad],
                         warn_frames=[r["frame"] for r in warn],
                         per_frame=rows)
            if not ok:
                refused.append("%s/%s (variant %s): %s"
                               % (clip, d, variant,
                                  ", ".join("f%02d %s" % (r["frame"], r["verdict"])
                                            for r in bad)))
                entry["assembled"] = False
                man["states"].setdefault(clip, {})[d] = entry
                print("  REFUSED %-6s %-3s variant %s  -> %s"
                      % (clip, d, variant,
                         ", ".join("f%02d %s" % (r["frame"], r["verdict"]) for r in bad[:4])))
                continue
            dd = os.path.join(SPR, clip, d)
            os.makedirs(dd, exist_ok=True)
            for i in range(n):
                shutil.copy(os.path.join(sd, "%s_%s_%02d.png" % (clip, d, i)),
                            os.path.join(dd, "%s_%s_%02d.png" % (clip, d, i)))
            entry["assembled"] = True
            man["states"].setdefault(clip, {})[d] = entry
            print("  %-6s %-3s variant %s  IoU %.3f..%.3f  area x%.2f  %s"
                  % (clip, d, variant, min(ious), max(ious),
                     entry["area_ratio_max"],
                     ("%d warn" % len(warn)) if warn else "clean"))
    man["source"] = {k: v for k, v in chosen.items() if not k.startswith("_")}
    man["refused"] = refused
    done = sum(1 for c in man["states"].values() for e in c.values() if e["assembled"])
    man["totals"] = dict(directions_assembled=done,
                         directions_expected=sum(8 for _ in CLIPS),
                         frames_assembled=sum(e["frames"] for c in man["states"].values()
                                              for e in c.values() if e["assembled"]))
    os.makedirs(SPR, exist_ok=True)
    json.dump(man, open(os.path.join(SPR, "manifest.json"), "w"), indent=1)
    print("assembled %d of 32 directions (%d frames); refused %d"
          % (done, man["totals"]["frames_assembled"], len(refused)))
    for r in refused:
        print("   refused:", r)


if __name__ == "__main__":
    main()
