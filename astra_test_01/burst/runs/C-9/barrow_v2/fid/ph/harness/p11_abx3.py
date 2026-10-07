#!/usr/bin/env python3
"""P11 v3 -- ABX with EMBEDDED CATCH TRIALS (jack-ryan pilot Gate-2 (1), F-5; R-C9-205). Pre-registered in calibration.md § 38.

What changes from v2 (p11_abx.py, kept unchanged as the record of the calibrated/pilot sets):
  * 12 CATCH trials are interleaved, format-identical (A | B | X, 256 px crops, same gaps, same naming, shuffled among
    the others), drawn from a pre-calibrated, clearly discriminable pair: v1 against R-C9-159 (its own judge: 40/40).
    Catch content control and guards are the scored trials' own, set-wide (class-matched, EXCLUDED content never drawn,
    A/B <= OVERLAP against every A/B of the set, X <= X_OVERLAP against every X of the set, within-trial same-place guard).
    The catch answers are balanced: 6 correct "A", 6 correct "B"; X from v1 in 6, from 159 in 6.
  * VALIDITY: the judge is VALID iff >= 10 / 12 catches are correct. An always-A (or always-B) answer set scores 6/12:
    VOID by construction.
  * The 40 scored trials and the bar (PASS iff <= 26 / 40) are unchanged; the 10 repeats stay as a REPORTED, NON-BINDING
    diagnostic (repeat inconsistency).
  * JUDGE.md says "versions" without a count (a catch trial's builds differ from a scored trial's).
  build3(set_name, cand_paths, seed, v1_paths=None)  -> p11/abx3_<set>/ (62 images + JUDGE.md), key p11/keys/abx3_<set>.json
  score3(set_name, answers_path)
  operating_table()  -- the pre-registered Monte Carlo (§ 38 (a))
"""
import argparse
import math
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p11_abx as X
import p11_pairs as P

N_CATCH = 12
CATCH_VALID = 10
CATCH_PAIR = ("v1", "R-C9-159", sorted((B2 / "section_v1cam/stills").glob("*.png")))

JUDGE_MD3 = """# Image matching test

There are {n} images, `trial_01.png` .. `trial_{n:02d}.png`. Each shows three square crops side by side, separated by white
gaps. From left to right they are **A**, **B** and **X**.

Every crop comes from one of several versions ("builds") of the same hand-painted 3D game level, seen from the same
fixed high camera at the same zoom. In each image, A and B come from two different builds. X comes from the same build
as either A or B, but from a different place in the level.

For each image, answer only: **is X from the same build as A, or from the same build as B?** Base the answer on how
the images are painted and rendered, not on what objects they show. Every image needs an answer, A or B; if you
cannot tell, give your best guess.

Return a JSON object {{"trial_01": "A" or "B", ..., "trial_{n:02d}": "A" or "B"}}. For each trial, add one short sentence
naming the visual evidence for the answer.
"""


def _trials(v1, cd, rng, n, used_ab, used_x, xs_plan, max_tries=8000):
    """v2's trial construction (p11_abx.build): A/B guarded at OVERLAP against used_ab, X at X_OVERLAP against used_x
    (every X of the set, scored and catch), within-trial same-place guard"""
    by = lambda pool, k: [c for c in pool if c["class"] == k]
    classes = [k for k in X.ALLOWED if len(by(v1, k)) >= 2 and len(by(cd, k)) >= 2]
    w = np.array([min(len(by(v1, k)), len(by(cd, k))) for k in classes], float)
    w /= w.sum()
    out, tries = [], 0
    while len(out) < n and tries < max_tries:
        tries += 1
        k = classes[rng.choice(len(classes), p=w)]
        a = X._pick(by(v1, k), rng, used_ab)
        b = X._pick(by(cd, k), rng, used_ab + [a] if a else used_ab, trial=(a,))
        if a is None or b is None:
            continue
        xsrc = xs_plan[len(out)]
        x = X._pick(by(v1, k) if xsrc == "v1" else by(cd, k), rng, used_x, X.X_OVERLAP, trial=(a, b))
        if x is None:
            continue
        used_ab += [a, b]
        used_x.append(x)
        out.append({"class": k, "v1": a, "cand": b, "x": x, "x_from": xsrc})
    return out


def build3(set_name, cand_paths, seed, v1_paths=None, out_root=None):
    rng = np.random.default_rng(seed)
    v1 = [c for p in (v1_paths or P.V1_STILLS) if p.exists() for c in X.crops_controlled(p)]
    cd = [c for p in cand_paths for c in X.crops_controlled(p)]
    # ---- the 40 scored trials + 10 repeats: v2's construction (same guards)
    xs = ["v1"] * (X.N_TRIALS // 2) + ["cand"] * (X.N_TRIALS // 2)
    rng.shuffle(xs)
    used_ab, used_x = [], []
    main = _trials(v1, cd, rng, X.N_TRIALS, used_ab, used_x, xs)
    for t in main:
        t["v1_is_A"] = bool(rng.integers(2))
        t["repeat_of"] = None
        t["catch"] = False
    by = lambda pool, k: [c for c in pool if c["class"] == k]
    reps = []
    for i in rng.permutation(len(main)):
        if len(reps) >= X.N_REPEAT:
            break
        t = dict(main[i])
        pool = by(v1, t["class"]) if t["x_from"] == "v1" else by(cd, t["class"])
        x2 = X._pick(pool, rng, used_x, X.X_OVERLAP, trial=(t["v1"], t["cand"], t["x"]))
        if x2 is None:
            continue
        used_x.append(x2)
        t.update(x=x2, v1_is_A=not t["v1_is_A"], repeat_of=int(i))
        reps.append(t)
    # ---- the 12 catch trials: v1 vs R-C9-159, balanced (X source 6/6, correct letter 6/6), clear of every used crop
    cv1 = [c for c in v1]
    c159 = [c for p in CATCH_PAIR[2] for c in X.crops_controlled(p)]
    cx = ["v1"] * (N_CATCH // 2) + ["cand"] * (N_CATCH // 2)
    rng.shuffle(cx)
    catches = _trials(cv1, c159, rng, N_CATCH, used_ab, used_x, cx)   # same guards as the scored trials, set-wide
    corr = ["A"] * (N_CATCH // 2) + ["B"] * (N_CATCH // 2)
    rng.shuffle(corr)
    for t, c in zip(catches, corr):
        t["catch"] = True
        t["repeat_of"] = None
        # correct letter c: X's build sits on side c
        t["v1_is_A"] = (c == "A") == (t["x_from"] == "v1")
    allt = main + reps + catches
    order = rng.permutation(len(allt))
    jd = (out_root or X.OUT) / ("abx3_" + set_name)
    jd.mkdir(parents=True, exist_ok=True)
    for f in jd.glob("trial_*.png"):
        f.unlink()
    key = {"_what": "P11 v3 ABX key (catch trials) -- NEVER given to the judge", "set": set_name, "seed": seed,
           "n_trials": X.N_TRIALS, "n_repeats": len(reps), "n_catch": len(catches), "catch_pair": CATCH_PAIR[:2],
           "catch_valid_if_correct_ge": CATCH_VALID, "crop_px": P.CROP, "trials": {}}
    name_of = {}
    for n, i in enumerate(order):
        t = allt[i]
        A, B = (t["v1"], t["cand"]) if t["v1_is_A"] else (t["cand"], t["v1"])
        comp = np.full((P.CROP, 3 * P.CROP + 2 * X.GAP, 3), 255, np.uint8)
        for j, c in enumerate((A, B, t["x"])):
            comp[:, j * (P.CROP + X.GAP):j * (P.CROP + X.GAP) + P.CROP] = P._crop(c)
        nm = "trial_%02d" % (n + 1)
        name_of[i] = nm
        Image.fromarray(comp).save(jd / (nm + ".png"))
        x_is = "A" if (t["x_from"] == "v1") == t["v1_is_A"] else "B"
        key["trials"][nm] = {"kind": "catch" if t["catch"] else ("repeat" if t["repeat_of"] is not None else "scored"),
                             "class": t["class"], "x_from": t["x_from"], "v1_is": "A" if t["v1_is_A"] else "B",
                             "correct": x_is, "A": A, "B": B, "X": t["x"]}
    for i, t in enumerate(allt):
        if t["repeat_of"] is not None:
            key["trials"][name_of[i]]["repeat_of"] = name_of[t["repeat_of"]]
    (jd / "JUDGE.md").write_text(JUDGE_MD3.format(n=len(allt)))
    kd = (out_root or X.OUT) / "keys"
    kd.mkdir(parents=True, exist_ok=True)
    dump(key, str(kd / ("abx3_" + set_name + ".json")))
    cc = [v["correct"] for v in key["trials"].values() if v["kind"] == "catch"]
    return {"set": set_name, "scored": len(main), "repeats": len(reps), "catches": len(catches), "images": len(allt),
            "catch_correct_A": cc.count("A"), "catch_correct_B": cc.count("B"),
            "UNDERPOWERED": len(main) < X.N_TRIALS or len(catches) < N_CATCH,
            "by_class": {k: sum(t["class"] == k for t in main) for k in sorted({t["class"] for t in main})},
            "catch_by_class": {k: sum(t["class"] == k for t in catches) for k in sorted({t["class"] for t in catches})},
            "judge_dir": str(jd)}


def score3(set_name, answers_path, out_root=None):
    key = jload((out_root or X.OUT) / "keys" / ("abx3_" + set_name + ".json"))["trials"]
    ans = {k: str(v).strip().upper()[:1] for k, v in jload(answers_path).items()}
    kinds = lambda kd: [k for k, v in key.items() if v["kind"] == kd]
    main, cat, reps = kinds("scored"), kinds("catch"), kinds("repeat")
    correct = sum(ans.get(k) == key[k]["correct"] for k in main)
    cc = sum(ans.get(k) == key[k]["correct"] for k in cat)
    build = lambda nm: (("v1" if key[nm]["v1_is"] == ans.get(nm) else "cand") if ans.get(nm) in ("A", "B") else None)
    inc = sum(build(k) is None or build(key[k]["repeat_of"]) is None or build(k) != build(key[k]["repeat_of"]) for k in reps)
    valid = cc >= CATCH_VALID
    return {"scored_correct": correct, "of": len(main), "accuracy": round(correct / len(main), 3),
            "catch_correct": cc, "catch_of": len(cat), "valid": valid,
            "verdict": ("PASS" if correct <= int(X.BAR * X.N_TRIALS) else "FAIL") if valid else "VOID",
            "repeat_inconsistency_diagnostic": round(inc / max(len(reps), 1), 3),
            "rule": "VALID iff catch >= %d/%d; PASS iff scored <= %d/%d" % (CATCH_VALID, N_CATCH, int(X.BAR * X.N_TRIALS), X.N_TRIALS)}


def operating_table(n_mc=200000, seed=205):
    """§ 38 (a): binomial exact + Monte Carlo on the rule (catch >= 10/12 valid; scored <= 26/40 pass)"""
    rng = np.random.default_rng(seed)
    k = int(X.BAR * X.N_TRIALS)
    pv = lambda p: sum(math.comb(N_CATCH, i) * p ** i * (1 - p) ** (N_CATCH - i) for i in range(CATCH_VALID, N_CATCH + 1))
    pp = lambda q: X.binom_le(k, X.N_TRIALS, q)
    rows = {}
    for nm, pc, pm in (("guesser", 0.5, 0.5), ("attentive, builds indistinguishable", 0.95, 0.5),
                       ("attentive (catch 0.99), indistinguishable", 0.99, 0.5),
                       ("attentive, builds discriminable p=0.75", 0.95, 0.75), ("attentive, p=0.85", 0.95, 0.85)):
        mc_c = rng.binomial(N_CATCH, pc, n_mc) >= CATCH_VALID
        mc_m = rng.binomial(X.N_TRIALS, pm, n_mc) <= k
        rows[nm] = {"p_catch": pc, "p_scored": pm, "P(valid)": round(pv(pc), 4), "P(valid)_mc": round(float(mc_c.mean()), 4),
                    "P(VOID)": round(1 - pv(pc), 4), "P(valid & PASS)": round(pv(pc) * pp(pm), 4),
                    "P(valid & PASS)_mc": round(float((mc_c & mc_m).mean()), 4), "P(valid & FAIL)": round(pv(pc) * (1 - pp(pm)), 4)}
    rows["always-A"] = {"catch_correct": N_CATCH // 2, "valid": False, "verdict": "VOID (6/12 by the balanced key)"}
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("g2")
    sub.add_parser("table")
    s = sub.add_parser("score")
    s.add_argument("set")
    s.add_argument("answers")
    a = ap.parse_args()
    if a.cmd == "table":
        print(json.dumps(operating_table(), indent=1))
    elif a.cmd == "score":
        print(json.dumps(score3(a.set, a.answers), indent=1))
    elif a.cmd == "g2":
        cdir = X.OUT / "_constructed_src"
        rec = sorted((B2 / "section_v1cam/v1ref").glob("V1_*.png"))
        head = sorted((FID / "pc/v1_stills").glob("*.png"))
        out = {"operating_table": operating_table(), "sets": {}}
        out["sets"]["g2v3_v1rec_vs_v1head"] = build3("g2v3_v1rec_vs_v1head", head, seed=2051, v1_paths=rec)
        out["sets"]["g2v3_v1_vs_halfdensity"] = build3("g2v3_v1_vs_halfdensity", sorted(cdir.glob("half_*.png")), seed=2052)
        dump(out, str(PH / "results/p11_abx3_g2_build.json"))
        print(json.dumps(out["sets"], indent=1, default=str))
