#!/usr/bin/env python3
"""P11 v2 -- BLIND ABX TEST (R-C9-168 re-instrumentation of the directional pair test, p11_pairs.py).

Why: in v0.1 the brief asked which crop was "lower-fidelity". Judge B told R-C9-158 from v1 (warm peach against cool
white) but named v1's register the lower-fidelity one, so a build it COULD distinguish scored as a PASS. The quality
word carried a prior about which build was better. ABX asks only for identity, so it carries no direction.

Design:
  * CONTENT CONTROL (R-C9-171): trials are drawn only from classes v1 has (snow, rock, standing stone, ice,
    heather/shrub, wood), class-matched; crops with build-specific content (open sea, wreck, hall, cliff faces) are
    excluded. Without a class mask only snow, ice and heather-on-snow are drawn (classify_controlled).
    The R-C9-171 calibration sets were built BEFORE this control and before the repeat fix; they stand as evidence.
  * a TRIAL is one image: three 256 x 256 crops at play zoom (100.6 screen px/m), side by side, A | B | X, 24 px white
    gaps, no text. A and B come from the two builds (v1 and the candidate; which build is A is randomised per trial,
    seeded). X is a THIRD crop from one of the two builds, same class as A and B (snow / rock / ice, p11_pairs.classify),
    at a different location: no crop in a set shares more than OVERLAP of its area with any other crop of the same
    LOCATION (a degraded copy of a v1 still counts as that still's location).
  * 40 trials: X from v1 in 20, from the candidate in 20. Plus 10 RELIABILITY repeats: the same A and B crops as 10 of
    the 40 trials, sides exchanged, and a DIFFERENT X from the same build (same class, new location) -- cross-crop
    consistency, not recall (fixed after the R-C9-168 round; the calibration sets judged then used the identical X). 50 images, shuffled, named trial_01..trial_50.png; PIL writes no text chunks.
    Nothing in the judge's directory names a source, a build or a class.
  * The brief (JUDGE.md) asks: "is X from the same build as A, or as B?" -- answer A or B. No quality words.
SCORING (p11_abx.py score <set> <answers.json>; answers = {"trial_NN": "A" | "B"}):
  accuracy = correct identifications over the 40 trials. Reliability = over the 10 repeat pairs, the share whose two
  answers name DIFFERENT builds for X (the two X crops share a build, so a consistent judge names the same build); more than 25% (3 or more of 10) VOIDS the judge (re-run with a fresh one).
  PASS (the candidate is indistinguishable from v1): accuracy <= 65% (pass if <= 26/40). Chance = 50%.
POWER: P(pass | true accuracy p) for p in 0.5..1.0, binomial n = 40 -- printed on the row.
"""
import argparse
import math
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p11_pairs as P

N_TRIALS, N_REPEAT = 40, 10
BAR = 0.65
GAP = 24
OVERLAP = 0.5        # max shared area between two crops of one LOCATION (0.25 once PT's v1 stills enlarge the pool)
X_OVERLAP = 0.25     # an X crop shares <= 25% of its area with any OTHER X crop (G2-B2 refinement: an X near another
                     # trial's A/B leaks nothing -- the judge never learns A's build -- so only X-vs-X is guarded)
                     # (first fix: with ANY crop already used (v0 allowed 50%: trials 06 and 43
                     # of the half-density set had X crops 128 px apart -- near-duplicates a judge can recall)
OUT = P.P11


# ---- CONTENT CONTROL (R-C9-171 (2)): the 158 judge found foliage TYPE and water TYPE always fell on opposite sides --
# content was a build cue. Trials are drawn only from classes v1 HAS, class-matched within a trial, and crops with
# build-specific content are excluded:
ALLOWED = ("snow", "rock", "standing_stone", "ice", "heather", "wood")      # classes v1 has (shrub folds into heather)
EXCLUDED = ("sea", "wreck", "hall", "cliff")                                 # build-specific content: never in a trial
# Pixel rules (no class mask): only snow, ice and heather-on-snow are separable from pixels alone; rock, standing stone
# and wood are drawn ONLY from stills that ship a class mask (<still>.classes.png, ids per <still>.classes.json:
# {"ids": {"rock": 1, ...}}), because pixels cannot tell v1's outcrops from barrow_v2's cliff faces, crags or hull.


def _tufts(c):
    f = c.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    lum = f.mean(-1)
    sat = (f.max(-1) - f.min(-1)) / np.maximum(f.max(-1), 1.0)
    heather = (r > g) & (g > b) & (r - b > 42) & (sat > 0.24) & (lum < 212)      # v1's step-3 tuft classifier
    shrub = (lum < 128) & (b < r + 6) & (g >= r - 12) & ~heather
    return heather | shrub


def classify_controlled(crop, mask_ids=None, ids=None):
    lab = rgb_to_lab(ndimage.gaussian_filter(crop, (2.5, 2.5, 0)))
    L, b = lab[..., 0], lab[..., 2]
    sea = ((L < 40) & (b < -3)).mean()
    if sea > 0.01:
        return None
    if mask_ids is not None:
        inv = {v: k for k, v in ids.items()}
        sh = {inv.get(int(v), "other"): float((mask_ids == v).mean()) for v in np.unique(mask_ids)}
        if any(sh.get(k, 0) > 0 for k in EXCLUDED):
            return None
        best = max((k for k in sh if k in ALLOWED), key=lambda k: sh[k], default=None)
        if best in ("rock", "standing_stone", "wood") and sh[best] >= 0.30:
            return best
    tu = _tufts(crop).mean()
    snowy = ((L >= 70) & (b >= -6)).mean()
    dark = (L < 55).mean()
    if tu >= 0.12 and snowy >= 0.40:
        return "heather"
    if tu < 0.01 and dark < 0.01 and ((L >= 78) & (b >= -6)).mean() >= 0.80:
        return "snow"
    if tu < 0.01 and ((b < -10) & (L >= 45)).mean() >= 0.40:
        return "ice"
    return None


def crops_controlled(path):
    img = load_rgb(path)
    H, W = img.shape[:2]
    mp = pathlib.Path(str(path).replace(".png", ".classes.png"))
    mask, ids = None, None
    if mp.exists():
        mask = np.asarray(Image.open(mp))
        ids = jload(str(mp).replace(".png", ".json"))["ids"]
    out = []
    for y in range(0, H - P.CROP + 1, P.STRIDE):
        for x in range(0, W - P.CROP + 1, P.STRIDE):
            cx0, cx1, cy0, cy1 = 0.30 * W, 0.66 * W, 0.30 * H, 0.80 * H
            if x < cx1 and x + P.CROP > cx0 and y < cy1 and y + P.CROP > cy0:
                continue
            k = classify_controlled(img[y:y + P.CROP, x:x + P.CROP], None if mask is None else mask[y:y + P.CROP, x:x + P.CROP], ids)
            if k:
                out.append({"src": str(path), "rect": [x, y, P.CROP, P.CROP], "class": k})
    return out


# WORLD-LOCATION GUARD (G2-B2), WITHIN A TRIAL: different stills of v1 can show the same place (v1ref V1_ring / PT
# stone_ring). Each still with a known camera centre maps a crop to ground (u, v); within one trial, two crops whose
# ground centres are within WORLD_SEP_M count as the same place and are never paired. v1ref centres: v2sw_run.gd _v1stills park_camera(uv) (look_at_world centres the aim);
# PT's: fid/pc/v1_stills/views.json camera.centre_ground_uv.
WORLD_SEP_M = 3.5          # a 256 px crop spans 2.5 m across, 3.2 m of ground up-screen; its diagonal ~ 4 m
_CENTRES = None


def _centres():
    global _CENTRES
    if _CENTRES is None:
        _CENTRES = {"V1_tarn.png": (-6.0, -7.0), "V1_ring.png": (2.0, 1.0), "V1_door.png": (0.0, 6.5)}
        vj = FID / "pc/v1_stills/views.json"
        if vj.exists():
            for k, v in jload(vj)["views"].items():
                _CENTRES[v["png"]] = tuple(v["camera"]["centre_ground_uv"])
    return _CENTRES


def _uv(c):
    n = _loc(c)
    cen = _centres().get(n)
    if cen is None:
        return None
    if "_wh" not in c:
        with Image.open(c["src"]) as im:
            c["_wh"] = im.size
    W, H = c["_wh"]
    x, y = c["rect"][0] + P.CROP / 2, c["rect"][1] + P.CROP / 2
    return (cen[0] + (x - W / 2) / PPM_V1, cen[1] - (y - H / 2) / 80.3076)


def _loc(c):
    """the still a crop's LOCATION comes from: a constructed source (half_<name>) shares its original's location space,
    so a v1 crop and a degraded crop of the same place never meet in one trial"""
    n = pathlib.Path(c["src"]).name
    return n[5:] if n.startswith("half_") else n


def _same_place(a, b):
    """WITHIN A TRIAL only: A, B and X are never the same place, even when seen in different stills (then content,
    not build, would decide the answer). Across trials the per-still overlap rules apply (as calibrated)."""
    if a is None or b is None:
        return False
    if _loc(a) == _loc(b):
        return _ov(a, b) > 0.0
    ua, ub = _uv(a), _uv(b)
    return ua is not None and ub is not None and math.hypot(ua[0] - ub[0], ua[1] - ub[1]) < WORLD_SEP_M


def _ov(a, b):
    if _loc(a) != _loc(b):
        return 0.0
    ox = max(0, min(a["rect"][0] + P.CROP, b["rect"][0] + P.CROP) - max(a["rect"][0], b["rect"][0]))
    oy = max(0, min(a["rect"][1] + P.CROP, b["rect"][1] + P.CROP) - max(a["rect"][1], b["rect"][1]))
    return ox * oy / (P.CROP * P.CROP)


def _pick(pool, rng, avoid, limit=None, trial=()):
    limit = OVERLAP if limit is None else limit
    for i in rng.permutation(len(pool)):
        c = pool[i]
        if all(_ov(c, u) <= limit for u in avoid) and not any(_same_place(c, t) for t in trial):
            return c
    return None


def build(set_name, cand_paths, seed=168, out_root=None, v1_paths=None):
    rng = np.random.default_rng(seed)
    v1 = [c for p in (v1_paths or P.V1_STILLS) if p.exists() for c in crops_controlled(p)]
    cd = [c for p in cand_paths for c in crops_controlled(p)]
    by = lambda pool, k: [c for c in pool if c["class"] == k]
    classes = [k for k in ALLOWED if len(by(v1, k)) >= 2 and len(by(cd, k)) >= 2]
    w = np.array([min(len(by(v1, k)), len(by(cd, k))) for k in classes], float)
    w /= w.sum()
    used_v1, used_cd = [], []          # A/B crops (OVERLAP among themselves, as calibrated)
    used_x = []                        # X crops: <= X_OVERLAP against every other X (recall is about X), and never the
                                       # same place as their own trial's A or B (the within-trial guard)
    trials = []
    xs = ["v1"] * (N_TRIALS // 2) + ["cand"] * (N_TRIALS // 2)
    rng.shuffle(xs)
    tries = 0
    while len(trials) < N_TRIALS and tries < 5000:
        tries += 1
        k = classes[rng.choice(len(classes), p=w)]
        a = _pick(by(v1, k), rng, used_v1 + used_cd)
        b = _pick(by(cd, k), rng, used_v1 + used_cd + [a] if a else used_cd, trial=(a,))
        if a is None or b is None:
            continue
        xsrc = xs[len(trials)]
        x = _pick(by(v1, k) if xsrc == "v1" else by(cd, k), rng, used_x, X_OVERLAP, trial=(a, b))
        if x is None:
            continue
        used_v1.append(a)
        used_cd.append(b)
        used_x.append(x)
        v1_is_A = bool(rng.integers(2))
        trials.append({"class": k, "v1": a, "cand": b, "x": x, "x_from": xsrc, "v1_is_A": v1_is_A, "repeat_of": None})
    # REPEATS (fix after the R-C9-168 calibration round): the same A and B crops with sides SWAPPED, and a DIFFERENT X
    # from the same build (same class, a new location clear of every crop already used). The v0 generator re-used the
    # identical X, so a judge could answer the repeat from memory (the half-density judge said it did): reliability
    # measured recall, not perception. Now it is CROSS-CROP CONSISTENCY.
    reps = []
    for i in rng.permutation(len(trials)):
        if len(reps) >= N_REPEAT:
            break
        t = dict(trials[i])
        pool = by(v1, t["class"]) if t["x_from"] == "v1" else by(cd, t["class"])
        x2 = _pick(pool, rng, used_x, X_OVERLAP, trial=(t["v1"], t["cand"], t["x"]))
        if x2 is None:
            continue
        used_x.append(x2)
        t["x"] = x2
        t["v1_is_A"] = not t["v1_is_A"]
        t["repeat_of"] = int(i)
        reps.append(t)
    allt = trials + reps
    order = rng.permutation(len(allt))
    jd = (out_root or OUT) / ("abx_" + set_name)
    jd.mkdir(parents=True, exist_ok=True)
    for f in jd.glob("trial_*.png"):
        f.unlink()
    key = {"_what": "P11 ABX key -- NEVER given to the judge", "set": set_name, "seed": seed, "n_trials": N_TRIALS,
           "n_repeats": N_REPEAT, "crop_px": P.CROP, "trials": {}}
    name_of = {}
    for n, i in enumerate(order):
        t = allt[i]
        A, B = (t["v1"], t["cand"]) if t["v1_is_A"] else (t["cand"], t["v1"])
        comp = np.full((P.CROP, 3 * P.CROP + 2 * GAP, 3), 255, np.uint8)
        for j, c in enumerate((A, B, t["x"])):
            comp[:, j * (P.CROP + GAP):j * (P.CROP + GAP) + P.CROP] = P._crop(c)
        nm = "trial_%02d" % (n + 1)
        name_of[i] = nm
        Image.fromarray(comp).save(jd / (nm + ".png"))
        x_is = ("A" if (t["x_from"] == "v1") == t["v1_is_A"] else "B")
        key["trials"][nm] = {"class": t["class"], "x_from": t["x_from"], "v1_is": "A" if t["v1_is_A"] else "B",
                             "correct": x_is, "A": A, "B": B, "X": t["x"], "repeat_of_index": t["repeat_of"]}
    for i, t in enumerate(allt):
        if t["repeat_of"] is not None:
            key["trials"][name_of[i]]["repeat_of"] = name_of[t["repeat_of"]]
    (jd / "JUDGE.md").write_text(JUDGE_MD.format(n=len(allt)))
    kd = (out_root or OUT) / "keys"
    kd.mkdir(parents=True, exist_ok=True)
    dump(key, str(kd / ("abx_" + set_name + ".json")))
    return {"set": set_name, "trials": len(trials), "repeats": len(reps), "images": len(allt),
            "UNDERPOWERED": len(trials) < N_TRIALS,      # do not hand to a judge: add stills (or class masks) first
            "by_class": {k: sum(t["class"] == k for t in trials) for k in classes}, "judge_dir": str(jd)}


JUDGE_MD = """# Image matching test

There are {n} images, `trial_01.png` .. `trial_{n:02d}.png`. Each shows three square crops side by side, separated by white
gaps. From left to right they are **A**, **B** and **X**.

Every crop comes from one of two versions ("builds") of the same hand-painted 3D game level, seen from the same fixed
high camera at the same zoom. In each image, A and B come from different builds. X comes from the same build as either
A or B, but from a different place in the level.

For each image, answer only: **is X from the same build as A, or from the same build as B?** Base the answer on how
the images are painted and rendered, not on what objects they show. Every image needs an answer, A or B; if you
cannot tell, give your best guess.

Return a JSON object {{"trial_01": "A" or "B", ..., "trial_{n:02d}": "A" or "B"}}. For each trial, add one short sentence
naming the visual evidence for the answer.
"""


def binom_le(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


def power_table():
    k = int(math.floor(BAR * N_TRIALS + 1e-9))
    return {"pass_if_correct_le": k, "of": N_TRIALS, "chance": 0.5,
            "P(pass | true ABX accuracy p)": {("%.2f" % p): round(binom_le(k, N_TRIALS, p), 4)
                                              for p in (0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 1.0)}}


def score(set_name, answers_path):
    key = jload(OUT / "keys" / ("abx_" + set_name + ".json"))["trials"]
    ans = {k: str(v).strip().upper()[:1] for k, v in jload(answers_path).items()}
    main = [k for k, v in key.items() if v.get("repeat_of") is None]
    acc = sum(ans.get(k) == key[k]["correct"] for k in main) / len(main)
    incons = 0
    reps = [k for k, v in key.items() if v.get("repeat_of")]
    for k in reps:
        o = key[k]["repeat_of"]
        build = lambda nm: (("v1" if key[nm]["v1_is"] == ans.get(nm) else "cand") if ans.get(nm) in ("A", "B") else None)
        if build(k) is None or build(o) is None or build(k) != build(o):
            incons += 1
    inc = incons / max(len(reps), 1)
    return {"abx_accuracy": round(acc, 3), "correct": int(round(acc * len(main))), "of": len(main),
            "repeat_inconsistency": round(inc, 3), "judge_void": inc > 0.25,
            "pass": (acc <= BAR) if inc <= 0.25 else None, "threshold": "ABX accuracy <= 65%% (<= %d/%d); void if repeat inconsistency > 25%%" % (int(BAR * N_TRIALS), N_TRIALS),
            "power": power_table()}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    b = sub.add_parser("build")
    b.add_argument("--set", default="all")
    s = sub.add_parser("score")
    s.add_argument("set")
    s.add_argument("answers")
    b.add_argument("--g2", action="store_true", help="build the two G2-B2 v1-GREEN sets")
    b.add_argument("--out", help="build into this root instead of fid/ph/p11 (e.g. a dry run; the calibration sets stand)")
    a = ap.parse_args()
    if a.cmd == "score":
        print(json.dumps(score(a.set, a.answers), indent=1))
    else:
        if a.g2:
            # G2-B2 (charter § 13): v1 GREEN on the FIXED generator. (i) record-time v1 (v1ref) vs HEAD v1 (PT);
            # (ii) all v1 stills vs their half-density copies. UNDERPOWERED (< 40 trials) = VOID: not handed out.
            cdir = OUT / "_constructed_src"
            cdir.mkdir(parents=True, exist_ok=True)
            for p in P.V1_STILLS:
                if p.exists() and not (cdir / ("half_" + p.name)).exists():
                    im = Image.open(p).convert("RGB")
                    im.resize((im.width // 2, im.height // 2), Image.BILINEAR).resize(im.size, Image.BILINEAR).save(cdir / ("half_" + p.name))
            rec = sorted((B2 / "section_v1cam/v1ref").glob("V1_*.png"))
            head = sorted((FID / "pc/v1_stills").glob("*.png"))
            out = {"power": power_table(), "sets": {}}
            out["sets"]["g2_v1rec_vs_v1head"] = build("g2_v1rec_vs_v1head", head, seed=173, v1_paths=rec)
            out["sets"]["g2_v1_vs_halfdensity"] = build("g2_v1_vs_halfdensity", sorted(cdir.glob("half_*.png")), seed=174)
            for k, v in out["sets"].items():
                print("P11-ABX", v)
            dump(out, str(PH / "results/p11_abx_g2_build.json"))
            sys.exit(0)
        cdir = OUT / "_constructed_src"           # v1 stills at half texel density (0.5x then 2x, bilinear), as p11_pairs
        cdir.mkdir(parents=True, exist_ok=True)
        for p in P.V1_STILLS:                  # every v1 still in the pool (v1ref + PT's fid/pc/v1_stills)
            if p.exists() and not (cdir / ("half_" + p.name)).exists():
                im = Image.open(p).convert("RGB")
                im.resize((im.width // 2, im.height // 2), Image.BILINEAR).resize(im.size, Image.BILINEAR).save(cdir / ("half_" + p.name))
        sets = {"cal_v1_vs_159": P.SETS["cal_v1_vs_159"], "cal_v1_vs_158": P.SETS["cal_v1_vs_158"],
                "cal_v1_vs_constructed_halfdensity": sorted(cdir.glob("half_*.png"))}
        out = {"power": power_table(), "sets": {}}
        for k, paths in sets.items():
            if a.set in ("all", k):
                out["sets"][k] = build(k, paths, out_root=pathlib.Path(a.out) if a.out else None)
                print("P11-ABX", out["sets"][k])
        print("power:", out["power"])
        if not a.out:
            dump(out, str(PH / "results/p11_abx_build.json"))
