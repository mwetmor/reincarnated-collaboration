#!/usr/bin/env python3
"""C-9 meshy_t2 step 11b: choose EbSynth keys per direction from N candidates.

    python3 scripts/19_pick_keys.py <clip> <layout.json> <cand1.png> [cand2.png ...]
                                    [--dest paint_keys_<clip>] [--apply]

T2K-idle failed at the lane: all four generations lost the green plate, so the
painter refused to deliver, and the conductor harvested the images anyway. The
paintings may be fine; only the background was. So each candidate is cut back
through the geometry-first matte (18_cutback_t2.py -> meshy_t1/14_cutback.py),
every cell is graded, and the choice is made PER DIRECTION.

BOTH KEYS OF A DIRECTION COME FROM THE SAME CANDIDATE. EbSynth blends its two
propagations by temporal distance, so the keys have to agree with each other
about what the creature looks like; two different generations of a bestiary
manticore will not. A direction whose best candidate fails either key is
reported as a re-fire, not patched from a second one.

THREE MEASURES per cell, because the flagged risk is one a silhouette gate
cannot see on its own:

  pose      IoU of the painted alpha against the render's own mask, best over
            eroding 0/1/2 px so the matte's ink band is not scored as drift.
  matte     painted area over render area; over 1.6 means the background came
            through.
  HEAD      the same IoU restricted to the head's own bounding box, found from
            the render's `part` pass by the head bone's flat colour. A head
            that rotates but keeps its area barely moves a whole-body IoU --
            the head is about 12 % of this creature's silhouette.
  FACE      bare-skin area inside that head box, as a RATIO to the render's.

FACE exists because HEAD was not enough, and that was found by looking rather
than by the number. The painter flagged rear three-quarter heads turning
toward profile. Head IoU scored 0.92-0.94 on every one of the 24 cells and
raised nothing -- correctly, because the drift is entirely INSIDE the
outline: the hair mass is the same shape whichever way the face points, and a
silhouette measure is structurally blind to an eye, a nose and a mouth
appearing where the render shows the back of a head. Opening the crops showed
all four NE candidates drawing a full profile face against a render that
shows almost none of one.

So the face is measured by how much BARE SKIN sits in the head box -- warm and
light, which separates it from both the blonde hair and the blue-grey ruff --
against the same figure from the render. Measured on the idle keys: NW 2.2-2.6x,
N 1.6-2.1x, NE 1.1-1.4x, against S/W/SW at 0.7-1.3x. The rear-facing half
drifts; the front-facing half does not.
"""
import argparse, json, os, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
POSE_MIN = 0.80
POSE_WARN = 0.90
HEAD_MIN = 0.70
HEAD_WARN = 0.82
FACE_MAX = 1.50          # ratio of bare-skin area to the render's
FACE_WARN = 1.25
MATTE_MAX = 1.60


def render_mask(clip, d, i):
    p = os.path.join(OUT, clip, "guides_mask", d, "mask_%s_%02d.png" % (d, i))
    return np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128


def _srgb(x):
    """Linear -> sRGB. The part pass stores the bone palette sRGB-ENCODED.

    `bone_colours` in render_<clip>.json are the linear floats that were fed
    to the emission shader; Blender writes the PNG through the sRGB transfer
    function, so head (1.00, 0.60, 0.15) linear arrives as (255, 203, 108),
    not (255, 153, 38). Comparing against the raw value matched nothing --
    and `head_box` then returned None, `grade` recorded head_iou=None, and the
    table printed a dash on all 24 cells. The head gate did not fail; it never
    ran, and it looked exactly like a column with no opinion. Verified against
    the pixels: sRGB-encoded palette (255.0, 203.4, 108.0) vs the rendered
    (255, 203, 108).
    """
    x = np.clip(x, 0.0, 1.0)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(x, 1 / 2.4) - 0.055)


def head_box(clip, d, i, pad=6):
    """The head's bounding box, from the render's flat per-bone part pass."""
    rp = json.load(open(os.path.join(OUT, clip, "render_%s.json" % clip)))
    col = _srgb(np.array(rp["guides"]["bone_colours"]["head"], dtype=np.float64))
    p = os.path.join(OUT, clip, "guides_part", d, "part_%s_%02d.png" % (d, i))
    a = np.asarray(Image.open(p).convert("RGBA")).astype(np.float64)
    rgb, al = a[..., :3] / 255.0, a[..., 3] > 128
    hit = al & (np.abs(rgb - col).max(-1) < 0.02)
    if hit.sum() < 20:
        raise RuntimeError(
            "head region not found in %s (%d px matched). The head gate must "
            "not be allowed to skip silently -- that is how it passed 24 cells "
            "without running." % (os.path.relpath(p, ROOT), int(hit.sum())))
    ys, xs = np.nonzero(hit)
    return (max(0, xs.min() - pad), max(0, ys.min() - pad),
            min(a.shape[1], xs.max() + pad + 1),
            min(a.shape[0], ys.max() + pad + 1)), int(hit.sum())


def flesh_frac(png, bb):
    """Bare-skin fraction of the head box: warm AND light, which is neither
    the blonde hair (warm, duller) nor the blue-grey ruff (cold)."""
    im = np.asarray(Image.open(png).convert("RGBA")).astype(np.float64)
    x0, y0, x1, y1 = bb
    sub = im[y0:y1, x0:x1]
    a = sub[..., 3] > 128
    if a.sum() < 10:
        return 0.0
    rgb = sub[..., :3] / 255.0
    warm = (rgb[..., 0] - rgb[..., 2]) > 0.20
    light = rgb.mean(-1) > 0.62
    return float((a & warm & light).sum()) / float(a.sum())


def best_iou(alpha, m):
    best = (-1.0, 0)
    for r in (0, 1, 2):
        e = alpha if r == 0 else ndi.binary_erosion(alpha, np.ones((2 * r + 1,) * 2))
        v = float((e & m).sum()) / max(float((e | m).sum()), 1.0)
        if v > best[0]:
            best = (v, r)
    return best


def grade(png, clip, d, i):
    alpha = np.asarray(Image.open(png).convert("RGBA"))[..., 3] > 128
    m = render_mask(clip, d, i)
    iou, er = best_iou(alpha, m)
    ratio = float(alpha.sum()) / max(float(m.sum()), 1.0)
    bb, npx = head_box(clip, d, i)
    x0, y0, x1, y1 = bb
    hiou, _ = best_iou(alpha[y0:y1, x0:x1], m[y0:y1, x0:x1])
    ref = flesh_frac(os.path.join(OUT, clip, "colour", d,
                                  "%s_%s_%02d.png" % (clip, d, i)), bb)
    face = flesh_frac(png, bb) / max(ref, 1e-3)
    verdict = "ok"
    if ratio > MATTE_MAX:
        verdict = "MATTE_FAT"
    elif iou < POSE_MIN:
        verdict = "POSE_FAIL"
    elif hiou < HEAD_MIN:
        verdict = "HEAD_FAIL"
    elif iou < POSE_WARN:
        verdict = "pose_warn"
    elif hiou < HEAD_WARN:
        verdict = "head_warn"
    elif face > FACE_MAX:
        verdict = "FACE_DRIFT"
    elif face > FACE_WARN:
        verdict = "face_warn"
    return dict(iou=round(iou, 4), erode_px=er, area_ratio=round(ratio, 4),
                head_iou=round(hiou, 4), face_ratio=round(face, 3),
                head_px=npx, verdict=verdict)


def mean_pose_frame(clip, d, candidates):
    """The candidate frame whose silhouette is nearest the clip's mean pose --
    the same rule 22_onekey.py uses to pick the key, so the two agree."""
    import numpy as _np
    n = {"idle": 12, "walk": 12, "run": 8, "attack": 12}[clip]
    allm = [np.asarray(Image.open(os.path.join(
        OUT, clip, "guides_mask", d, "mask_%s_%02d.png" % (d, i))).convert("RGBA"))[..., 3] > 128
        for i in range(n)]
    best, bi = -1.0, candidates[0]
    for c in candidates:
        mc = allm[c]
        v = float(_np.mean([(mc & m).sum() / max((mc | m).sum(), 1) for m in allm]))
        if v > best:
            best, bi = v, c
    return bi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("layout")
    ap.add_argument("cands", nargs="+")
    ap.add_argument("--dest", default=None)
    ap.add_argument("--single-key", action="store_true",
                    help="score each candidate ONLY on the frame that will be "
                         "used as the single EbSynth key")
    ap.add_argument("--apply", action="store_true",
                    help="write the choice into work/chosen.json")
    args = ap.parse_args()
    clip = args.clip
    lay = json.load(open(args.layout))
    cells = [c for c in lay["cells"] if c.get("frame") is not None and c.get("source")]
    dirs, keys = [], {}
    for c in cells:
        if c["dir"] not in dirs:
            dirs.append(c["dir"])
        keys.setdefault(c["dir"], []).append(c["frame"])

    roots = {}
    for k, cp in enumerate(args.cands, 1):
        dest = os.path.join(ROOT, "paint_k%d" % k)
        roots["k%d" % k] = dest
        print("== candidate k%d: %s" % (k, os.path.basename(cp)))
        subprocess.run([sys.executable, os.path.join(HERE, "18_cutback_t2.py"),
                        cp, args.layout, dest,
                        "--report", os.path.join(ROOT, "work",
                                                 "cut_%s_k%d.json" % (clip, k))],
                       check=True)

    rep = dict(clip=clip, layout=os.path.basename(args.layout),
               candidates={("k%d" % (i + 1)): os.path.basename(c)
                           for i, c in enumerate(args.cands)},
               thresholds=dict(pose_min=POSE_MIN, pose_warn=POSE_WARN,
                               head_min=HEAD_MIN, head_warn=HEAD_WARN,
                               matte_max=MATTE_MAX),
               dirs={})
    choice, refire = {}, []
    print("\n%-4s %-4s %s" % ("dir", "cand",
          "  key0 iou/head/face    key1 iou/head/face   verdict"))
    for d in dirs:
        per = {}
        for name, root in roots.items():
            rows = []
            for i in keys[d]:
                p = os.path.join(root, clip, d, "%s_%s_%02d.png" % (clip, d, i))
                rows.append(grade(p, clip, d, i) if os.path.exists(p)
                            else dict(verdict="MISSING", iou=0.0, head_iou=0.0))
            # FACE_DRIFT does not disqualify a candidate on its own -- every
            # candidate for a rear direction has it, so refusing them all
            # would leave the direction empty with no better option in hand.
            # It is scored against, and reported for gandalf to re-fire.
            ok = all(r["verdict"] not in ("MATTE_FAT", "POSE_FAIL", "HEAD_FAIL",
                                          "MISSING") for r in rows)
            per[name] = dict(frames=keys[d], rows=rows, acceptable=ok,
                             score=min(r["iou"] for r in rows)
                             + 0.5 * min(r["head_iou"] for r in rows)
                             - 0.5 * max(r["face_ratio"] for r in rows))
            print("%-4s %-4s  %s  %s"
                  % (d, name,
                     "  ".join("%.3f/%.3f/%.1fx" % (r["iou"], r["head_iou"],
                                                    r["face_ratio"]) for r in rows),
                     ("OK" if ok else "/".join(sorted({r["verdict"] for r in rows
                                                       if r["verdict"] != "ok"})))))
        if args.single_key:
            # ONE key ships, so only that key's numbers may choose it. Scoring
            # on the worst of both keys picked a sheet for a frame the
            # pipeline will never use: on NE the two-key score chose k3
            # (face 1.1 / 1.6) over k5, whose key0 -- the frame Y actually
            # takes -- is the better 1.0.
            kf = mean_pose_frame(clip, d, keys[d])
            ki = keys[d].index(kf)
            for name, v in per.items():
                r = v["rows"][ki]
                v["key_frame"] = kf
                v["acceptable"] = r["verdict"] not in (
                    "MATTE_FAT", "POSE_FAIL", "HEAD_FAIL", "MISSING")
                v["score"] = r["iou"] + 0.5 * r["head_iou"] - 0.5 * r["face_ratio"]
        good = {k: v for k, v in per.items() if v["acceptable"]}
        pick = max(good, key=lambda k: good[k]["score"]) if good else None
        rep["dirs"][d] = dict(candidates=per, chosen=pick, keys=keys[d])
        if pick:
            choice[d] = pick
        else:
            refire.append(d)
        print("  -> %s\n" % (("chose %s" % pick) if pick
                             else "NO CANDIDATE PASSES - needs a re-fire"))

    rep["choice"] = choice
    rep["refire"] = refire
    def _fr(d):
        c = rep["dirs"][d]["candidates"][choice[d]]
        if args.single_key and "key_frame" in c:
            return c["rows"][keys[d].index(c["key_frame"])]["face_ratio"]
        return max(r["face_ratio"] for r in c["rows"])
    drift = {d: round(_fr(d), 2) for d in choice}
    rep["face_drift_ratio"] = drift
    rep["face_drift_flagged"] = sorted([d for d, v in drift.items() if v > FACE_WARN])
    json.dump(rep, open(os.path.join(ROOT, "work", "keys_choice_%s.json" % clip), "w"),
              indent=1)
    print("chosen per direction: %s" % (choice or "none"))
    if refire:
        print("RE-FIRE NEEDED for: %s" % ", ".join(refire))
    if rep["face_drift_flagged"]:
        print("FACE DRIFT (chosen cells draw more of a face than the render "
              "shows; not disqualifying, but a re-fire target): %s"
              % ", ".join("%s x%.1f" % (d, drift[d])
                          for d in rep["face_drift_flagged"]))
    if args.apply and choice:
        cp = os.path.join(ROOT, "work", "chosen.json")
        ch = json.load(open(cp))
        ch.setdefault(clip, {})["keys"] = choice
        json.dump(ch, open(cp, "w"), indent=1)
        print("wrote choice into work/chosen.json")


if __name__ == "__main__":
    main()
