#!/usr/bin/env python3
"""P11 v2 -- BLIND ABX TEST (R-C9-168 re-instrumentation of the directional pair test, p11_pairs.py).

Why: in v0.1 the brief asked which crop was "lower-fidelity". Judge B told R-C9-158 from v1 (warm peach against cool
white) but named v1's register the lower-fidelity one, so a build it COULD distinguish scored as a PASS. The quality
word carried a prior about which build was better. ABX asks only for identity, so it carries no direction.

Design:
  * a TRIAL is one image: three 256 x 256 crops at play zoom (100.6 screen px/m), side by side, A | B | X, 24 px white
    gaps, no text. A and B come from the two builds (v1 and the candidate; which build is A is randomised per trial,
    seeded). X is a THIRD crop from one of the two builds, same class as A and B (snow / rock / ice, p11_pairs.classify),
    at a different location: no crop in a set shares more than OVERLAP of its area with any other crop of the same
    LOCATION (a degraded copy of a v1 still counts as that still's location).
  * 40 trials: X from v1 in 20, from the candidate in 20. Plus 10 RELIABILITY repeats: the same three crops as 10 of
    the 40 trials, with A and B exchanged. 50 images, shuffled, named trial_01..trial_50.png; PIL writes no text chunks.
    Nothing in the judge's directory names a source, a build or a class.
  * The brief (JUDGE.md) asks: "is X from the same build as A, or as B?" -- answer A or B. No quality words.
SCORING (p11_abx.py score <set> <answers.json>; answers = {"trial_NN": "A" | "B"}):
  accuracy = correct identifications over the 40 trials. Reliability = over the 10 repeat pairs, the share whose two
  answers name DIFFERENT builds for X; more than 25% (3 or more of 10) VOIDS the judge (re-run with a fresh one).
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
OUT = P.P11


def _loc(c):
    """the still a crop's LOCATION comes from: a constructed source (half_<name>) shares its original's location space,
    so a v1 crop and a degraded crop of the same place never meet in one trial"""
    n = pathlib.Path(c["src"]).name
    return n[5:] if n.startswith("half_") else n


def _ov(a, b):
    if _loc(a) != _loc(b):
        return 0.0
    ox = max(0, min(a["rect"][0] + P.CROP, b["rect"][0] + P.CROP) - max(a["rect"][0], b["rect"][0]))
    oy = max(0, min(a["rect"][1] + P.CROP, b["rect"][1] + P.CROP) - max(a["rect"][1], b["rect"][1]))
    return ox * oy / (P.CROP * P.CROP)


def _pick(pool, rng, avoid):
    for i in rng.permutation(len(pool)):
        c = pool[i]
        if all(_ov(c, u) <= OVERLAP for u in avoid):
            return c
    return None


def build(set_name, cand_paths, seed=168):
    rng = np.random.default_rng(seed)
    v1 = [c for p in P.V1_STILLS if p.exists() for c in P.crops_of(p)]
    cd = [c for p in cand_paths for c in P.crops_of(p)]
    by = lambda pool, k: [c for c in pool if c["class"] == k]
    classes = [k for k in ("snow", "rock", "ice") if len(by(v1, k)) >= 2 and len(by(cd, k)) >= 2]
    w = np.array([min(len(by(v1, k)), len(by(cd, k))) for k in classes], float)
    w /= w.sum()
    used_v1, used_cd = [], []
    trials = []
    xs = ["v1"] * (N_TRIALS // 2) + ["cand"] * (N_TRIALS // 2)
    rng.shuffle(xs)
    tries = 0
    while len(trials) < N_TRIALS and tries < 5000:
        tries += 1
        k = classes[rng.choice(len(classes), p=w)]
        a = _pick(by(v1, k), rng, used_v1 + used_cd)
        b = _pick(by(cd, k), rng, used_v1 + used_cd + [a] if a else used_cd)
        if a is None or b is None:
            continue
        xsrc = xs[len(trials)]
        x = _pick(by(v1, k) if xsrc == "v1" else by(cd, k), rng, used_v1 + used_cd + [a, b])
        if x is None:
            continue
        used_v1.append(a)
        used_cd.append(b)
        (used_v1 if xsrc == "v1" else used_cd).append(x)
        v1_is_A = bool(rng.integers(2))
        trials.append({"class": k, "v1": a, "cand": b, "x": x, "x_from": xsrc, "v1_is_A": v1_is_A, "repeat_of": None})
    reps = []
    for i in rng.choice(len(trials), N_REPEAT, replace=False):
        t = dict(trials[i])
        t["v1_is_A"] = not t["v1_is_A"]
        t["repeat_of"] = int(i)
        reps.append(t)
    allt = trials + reps
    order = rng.permutation(len(allt))
    jd = OUT / ("abx_" + set_name)
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
    (jd / "JUDGE.md").write_text(JUDGE_MD)
    (OUT / "keys").mkdir(parents=True, exist_ok=True)
    dump(key, str(OUT / "keys" / ("abx_" + set_name + ".json")))
    return {"set": set_name, "trials": len(trials), "repeats": len(reps), "images": len(allt),
            "by_class": {k: sum(t["class"] == k for t in trials) for k in classes}, "judge_dir": str(jd)}


JUDGE_MD = """# Image matching test

There are 50 images, `trial_01.png` .. `trial_50.png`. Each shows three square crops side by side, separated by white
gaps. From left to right they are **A**, **B** and **X**.

Every crop comes from one of two versions ("builds") of the same hand-painted 3D game level, seen from the same fixed
high camera at the same zoom. In each image, A and B come from different builds. X comes from the same build as either
A or B, but from a different place in the level.

For each image, answer only: **is X from the same build as A, or from the same build as B?** Base the answer on how
the images are painted and rendered, not on what objects they show. Every image needs an answer, A or B; if you
cannot tell, give your best guess.

Return a JSON object {"trial_01": "A" or "B", ..., "trial_50": "A" or "B"}. For each trial, add one short sentence
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
    a = ap.parse_args()
    if a.cmd == "score":
        print(json.dumps(score(a.set, a.answers), indent=1))
    else:
        cdir = OUT / "_constructed_src"           # v1 stills at half texel density (0.5x then 2x, bilinear), as p11_pairs
        cdir.mkdir(parents=True, exist_ok=True)
        for p in sorted((B2 / "section_v1cam/v1ref").glob("V1_*.png")):
            if not (cdir / ("half_" + p.name)).exists():
                im = Image.open(p).convert("RGB")
                im.resize((im.width // 2, im.height // 2), Image.BILINEAR).resize(im.size, Image.BILINEAR).save(cdir / ("half_" + p.name))
        sets = {"cal_v1_vs_159": P.SETS["cal_v1_vs_159"], "cal_v1_vs_158": P.SETS["cal_v1_vs_158"],
                "cal_v1_vs_constructed_halfdensity": sorted(cdir.glob("half_*.png"))}
        out = {"power": power_table(), "sets": {}}
        for k, paths in sets.items():
            if a.set in ("all", k):
                out["sets"][k] = build(k, paths)
                print("P11-ABX", out["sets"][k])
        print("power:", out["power"])
        dump(out, str(PH / "results/p11_abx_build.json"))
