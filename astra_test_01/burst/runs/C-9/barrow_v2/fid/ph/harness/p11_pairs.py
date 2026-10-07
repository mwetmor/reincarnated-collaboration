#!/usr/bin/env python3
"""P11 -- BLIND PAIR TEST: the crop-pair generator, the answer key and the scorer. PH NEVER JUDGES (charter § 9 C-3):
the conductor spawns a fresh galadriel instance and hands it ONLY the judge directory (pair images + JUDGE.md).

Design (Gate-1 I-1):
  * n = 40 pairs: 30 TEST pairs (one v1 crop, one candidate crop) + 10 NULL pairs (two v1 crops from different
    places). Sides randomised (seeded). Every crop 256 x 256 px (2.5 m) at PLAY ZOOM (100.6 screen px/m: every play-camera
    capture of barrow_full.gd has cam.size = rows / PPM), SAME CLASS within a pair.
  * Classes by the crop's own pixels (Lab, 0.05 m smoothing): snow (>= 75% of px L >= 78 and b >= -6); rock (>= 30% of
    px 25 <= L < 70 and chroma < 22); ice (>= 30% of px b < -10 and L >= 45). A crop that is none of these is not used.
  * Crops never include the middle of the frame (he stands there: x 0.30-0.66, y 0.30-0.80 of the frame excluded),
    never cross the frame edge; PNGs written by PIL with NO text chunks; files named pair_NN.png (L | 16 px gap | R)
    and nothing else -- no source name, size or class survives into the judge's directory.
  * The KEY (keys/<set>.json, never given to the judge): per pair, type, class, which side is the candidate, sources
    and rects.
SCORING (p11_pairs.py score <set> <answers.json>; answers = {"pair_NN": "LEFT" | "RIGHT" | "SAME"}):
  identification = TEST pairs where the judge names the candidate side / 30   (SAME counts as not identified);
  null false-alarm = NULL pairs not answered SAME / 10.
  PASS (the candidate is indistinguishable from v1): identification <= 65% (plan § 4 P11). Calibration expectation:
  v1 vs R-C9-159 ~ 100%. A judge whose null false-alarm exceeds 30% is reported as UNRELIABLE (the row is re-run).
POWER: printed on the row -- P(identification <= 19/30 | true rate p) for p in 0.5 .. 1.0 (binomial, n = 30).
"""
import argparse
import math
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

CROP = 256
STRIDE = 64
N_TEST, N_NULL = 30, 10
BAR = 0.65
OVERLAP = 0.5        # max shared area between two crops of one source (0.25 when PT's v1 stills enlarge the pool)
P11 = PH / "p11"

# v1 PAINTED play-camera stills only. NOT barrow_full/captures/still_*.png: those are the step-1 BLOCKOUT (greybox)
# stills (checked by eye at calibration -- grey primitives, flat tints). PT's fresh v1 stills (fid/pc/v1_stills/,
# Gate-1 path) join the pool automatically when they land.
V1_STILLS = sorted((B2 / "section_v1cam/v1ref").glob("V1_*.png")) + sorted((FID / "pc/v1_stills").glob("*.png"))
SETS = {"cal_v1_vs_159": sorted((B2 / "section_v1cam/stills").glob("*.png")),
        "cal_v1_vs_158": sorted((B2 / "section_sw/stills_painted").glob("*.png"))}


def classify(crop):
    lab = rgb_to_lab(ndimage.gaussian_filter(crop, (2.5, 2.5, 0)))
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    ch = np.hypot(a, b)
    if ((L >= 78) & (b >= -6)).mean() >= 0.75:
        return "snow"
    if ((b < -10) & (L >= 45)).mean() >= 0.30:
        return "ice"
    if ((L >= 25) & (L < 70) & (ch < 22)).mean() >= 0.30:
        return "rock"
    return None


def crops_of(path):
    img = load_rgb(path)
    H, W = img.shape[:2]
    out = []
    for y in range(0, H - CROP + 1, STRIDE):
        for x in range(0, W - CROP + 1, STRIDE):
            cx0, cx1, cy0, cy1 = 0.30 * W, 0.66 * W, 0.30 * H, 0.80 * H
            if x < cx1 and x + CROP > cx0 and y < cy1 and y + CROP > cy0:
                continue
            c = img[y:y + CROP, x:x + CROP]
            k = classify(c)
            if k:
                out.append({"src": str(path), "rect": [x, y, CROP, CROP], "class": k})
    return out


def pick_far(pool, rng, used):
    """a crop not overlapping one already used from the same source by more than 25%"""
    idx = rng.permutation(len(pool))
    for i in idx:
        c = pool[i]
        ok = True
        for u in used:
            if u["src"] == c["src"]:
                ox = max(0, min(u["rect"][0] + CROP, c["rect"][0] + CROP) - max(u["rect"][0], c["rect"][0]))
                oy = max(0, min(u["rect"][1] + CROP, c["rect"][1] + CROP) - max(u["rect"][1], c["rect"][1]))
                if ox * oy > OVERLAP * CROP * CROP:
                    ok = False
                    break
        if ok:
            used.append(c)
            return c
    return None


def build(set_name, cand_paths, seed=11):
    rng = np.random.default_rng(seed)
    v1 = [c for p in V1_STILLS if p.exists() for c in crops_of(p)]
    cd = [c for p in cand_paths for c in crops_of(p)]
    by = lambda pool, k: [c for c in pool if c["class"] == k]
    classes = [k for k in ("snow", "rock", "ice") if by(v1, k) and by(cd, k)]
    used_v1, used_cd = [], []
    pairs = []
    # TEST pairs: round-robin over the classes both sides have, weighted by the candidate's own class counts
    w = np.array([len(by(cd, k)) for k in classes], float)
    w /= w.sum()
    tries = 0
    while len([p for p in pairs if p["type"] == "test"]) < N_TEST and tries < 2000:
        tries += 1
        k = classes[rng.choice(len(classes), p=w)]
        a = pick_far(by(v1, k), rng, used_v1)
        b = pick_far(by(cd, k), rng, used_cd)
        if a is None or b is None:
            continue
        pairs.append({"type": "test", "class": k, "v1": a, "cand": b})
    nclasses = [k for k in ("snow", "rock", "ice") if len(by(v1, k)) >= 2]
    tries = 0
    while len([p for p in pairs if p["type"] == "null"]) < N_NULL and tries < 2000:
        tries += 1
        k = nclasses[rng.integers(len(nclasses))]
        a = pick_far(by(v1, k), rng, used_v1)
        b = pick_far([c for c in by(v1, k) if a is None or c["src"] != a["src"]], rng, used_v1)
        if a is None or b is None:
            continue
        pairs.append({"type": "null", "class": k, "v1": a, "cand": b})
    order = rng.permutation(len(pairs))
    jd = P11 / ("judge_" + set_name)
    jd.mkdir(parents=True, exist_ok=True)
    for f in jd.glob("pair_*.png"):
        f.unlink()
    key = {"_what": "P11 answer key -- NEVER given to the judge", "set": set_name, "seed": seed, "n_test": N_TEST,
           "n_null": N_NULL, "crop_px": CROP, "pairs": {}}
    for n, i in enumerate(order):
        p = pairs[i]
        left_is_cand = bool(rng.integers(2))
        ca = _crop(p["cand"])
        va = _crop(p["v1"])
        L, R = (ca, va) if left_is_cand else (va, ca)
        comp = np.full((CROP, 2 * CROP + 16, 3), 255, np.uint8)
        comp[:, :CROP] = L
        comp[:, CROP + 16:] = R
        name = "pair_%02d" % (n + 1)
        Image.fromarray(comp).save(jd / (name + ".png"), optimize=False)       # PIL writes no text chunks
        key["pairs"][name] = {"type": p["type"], "class": p["class"],
                              "candidate_side": ("LEFT" if left_is_cand else "RIGHT") if p["type"] == "test" else None,
                              "left": (p["cand"] if left_is_cand else p["v1"]), "right": (p["v1"] if left_is_cand else p["cand"])}
    (jd / "JUDGE.md").write_text(JUDGE_MD)
    (P11 / "keys").mkdir(parents=True, exist_ok=True)
    dump(key, str(P11 / "keys" / (set_name + ".json")))
    cnt = {}
    for p in pairs:
        cnt[(p["type"], p["class"])] = cnt.get((p["type"], p["class"]), 0) + 1
    return {"set": set_name, "pairs": len(pairs), "by_type_class": {"%s/%s" % k: v for k, v in cnt.items()},
            "v1_pool": len(v1), "cand_pool": len(cd), "judge_dir": str(jd)}


_IMG = {}


def _crop(c):
    if c["src"] not in _IMG:
        _IMG[c["src"]] = load_rgb(c["src"]).astype(np.uint8)
    x, y, w, h = c["rect"]
    return _IMG[c["src"]][y:y + h, x:x + w]


JUDGE_MD = """# Blind pair test

You are given 40 images, `pair_01.png` .. `pair_40.png`. Each shows two square crops side by side (LEFT | RIGHT)
from a hand-painted 3D game level, seen from the same fixed high camera at the same zoom.

In SOME pairs both crops come from the SAME build of the level. In the others, one crop comes from a different
build whose painting and rendering may be of different quality (for example: a different painter's hand,
blotchy or patchwork texture, magnified/blurry texels, painted light lit a second time, mismatched colour).

For each pair answer exactly one of:
- `SAME`  -- you cannot tell them apart as builds (content may differ; judge the painting and rendering quality);
- `LEFT`  -- the LEFT crop is from the different, lower-fidelity build;
- `RIGHT` -- the RIGHT crop is from the different, lower-fidelity build.

Judge only what you see in the images. Return a JSON object {"pair_01": "...", ..., "pair_40": "..."} and, per
pair, one short sentence naming the visual evidence for your answer.
"""


def binom_le(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


def power_table():
    k = int(math.floor(BAR * N_TEST + 1e-9))
    return {"pass_if_identified_le": k, "of": N_TEST,
            "P(pass | true identification rate p)": {("%.2f" % p): round(binom_le(k, N_TEST, p), 4)
                                                     for p in (0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 1.0)}}


def score(set_name, answers_path):
    key = jload(P11 / "keys" / (set_name + ".json"))
    ans = jload(answers_path)
    t = [k for k, v in key["pairs"].items() if v["type"] == "test"]
    nl = [k for k, v in key["pairs"].items() if v["type"] == "null"]
    ident = sum(ans.get(k, "").upper() == key["pairs"][k]["candidate_side"] for k in t) / len(t)
    fa = sum(ans.get(k, "").upper() != "SAME" for k in nl) / len(nl)
    return {"identification": round(ident, 3), "null_false_alarm": round(fa, 3), "pass": ident <= BAR,
            "judge_reliable": fa <= 0.30, "threshold": "identification <= %.0f%%" % (100 * BAR), "power": power_table()}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    b = sub.add_parser("build")
    b.add_argument("--set", default="all")
    s = sub.add_parser("score")
    s.add_argument("set")
    s.add_argument("answers")
    a = ap.parse_args()
    if a.cmd == "score":
        r = score(a.set, a.answers)
        print(json.dumps(r, indent=1))
    else:
        out = {"power": power_table(), "sets": {}}
        # the CONSTRUCTED failing candidate: v1's own stills at HALF texel density (0.5x then 2x, bilinear) -- the
        # magnification a 50 px/m painting shows at play zoom. Sources kept outside the judge's directory.
        cdir = P11 / "_constructed_src"
        cdir.mkdir(parents=True, exist_ok=True)
        cpaths = []
        for p in sorted((B2 / "section_v1cam/v1ref").glob("V1_*.png")):
            im = Image.open(p).convert("RGB")
            im.resize((im.width // 2, im.height // 2), Image.BILINEAR).resize(im.size, Image.BILINEAR).save(cdir / ("half_" + p.name))
            cpaths.append(cdir / ("half_" + p.name))
        SETS["cal_v1_vs_constructed_halfdensity"] = cpaths
        for k, paths in SETS.items():
            if a.set in ("all", k):
                out["sets"][k] = build(k, paths)
                print("P11 %s: %s" % (k, out["sets"][k]))
        print("power:", out["power"])
        dump(out, str(PH / "results/p11_build.json"))
