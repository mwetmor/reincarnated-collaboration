#!/usr/bin/env python3
"""§ 52 (b): FULL-SITE P11 v3 as pre-registered at 7d47a498d (R-C9-331 / Gate-2 H-4).
  derive  -> the id-level class mapping (R1 PT's stated cls_of where non-null; R2 the LV class through the § 52 table;
             R3 R-C9-171 name families cliff / wreck / sea_), DERIVED masks for the 24 site stills in p11/site_masks/
             (each still COPIED byte for byte beside its <name>.classes.png/.json; PT's files untouched)
  phase   -> PH's own § 50 (a) measurement on the r328 painting (constructed check first); +-0.10 px of T[k mod 6]
  build   -> p11_abx3.build3(seed 331, rule_exclusion) with EXCLUDED = the derived set; < 40 scored = VOID (no judge)
  site_p11.py all -> results/site/p11_mapping.json, p11_phase.json, p11v3_build.json; set p11/abx3_site_v1_vs_site/"""
import importlib.util
import json
import os
import shutil
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from common import *  # noqa

ST = FID / "pt/site/stills"
MD = PH / "p11/site_masks"
OUT = PH / "results/site"
PAINT = FID / "pt/ph3/final/painting_ph3_r328_full.png"
U0, V1 = -33.57573954303182, 22.36993715728635
TARGETS = [("barrow_door", 0.222, 0.840), ("mere", 0.438, 0.587), ("outcrop_field", 0.251, 0.897),
           ("shore", 0.668, 0.177), ("start", 0.373, 0.666), ("stone_ring", 0.219, 0.943)]
TABLE = {"snow": "snow", "mound": "snow", "path": "snow", "rock": "rock", "shrub": "heather", "wood": "wood",
         "ice": "ice", "ice_mid": "ice", "shore_ice": "ice", "tide_ice": "ice", "stream": "ice",
         "reed": "reed", "sea": "sea", "lead": "sea", "char": "char", "ash": "ash", "passage_dark": "passage_dark",
         "shingle": "shingle", "wet_rock": "wet_rock", "rime": "rime", "none": None}
ALLOWED = ("snow", "rock", "standing_stone", "heather", "wood")
EXCLUDED = ("sea", "wreck", "hall", "cliff", "char", "ash", "passage_dark", "shingle", "wet_rock", "rime")   # + ice, reed by rule
SCHEMA = ["rock", "standing_stone", "wood", "sea", "wreck", "hall", "cliff", "snow", "ice", "heather", "reed",
          "char", "ash", "passage_dark", "shingle", "wet_rock", "rime"]
VAL = {c: i + 1 for i, c in enumerate(SCHEMA)}
GROUND = {"cliff": "R-C9-171", "wreck": "R-C9-171", "hall": "R-C9-171", "sea": "R-C9-171 / R-C9-240 (lead)",
          "char": "R-C9-171 (s22)", "ash": "R-C9-171 (s22)", "passage_dark": "R-C9-171 (s22)", "shingle": "rule (a)",
          "wet_rock": "rule (a)", "rime": "rule (a)", "ice": "rule (b) R-C9-203/255/262", "reed": "rule (a)"}


def pt_cls_of():
    spec = importlib.util.spec_from_file_location("pcm_src", FID / "pt/tools/pilot_class_masks.py")
    src = (FID / "pt/tools/pilot_class_masks.py").read_text()
    body = src[src.index("def cls_of"):src.index("tab = json.load")]
    ns = {}
    exec(body, ns)                                    # the stated function only (the module's top level writes files)
    return ns["cls_of"], hashlib_sha(FID / "pt/tools/pilot_class_masks.py")


def hashlib_sha(p):
    import hashlib
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def derive():
    cls_of, sha_tool = pt_cls_of()
    tab = jload(ST / "ids_table.json")["ids"]
    m, rows, unmapped = {}, {}, {}
    for k, v in tab.items():
        iid, lv = v["id"], v["class"]
        r1 = cls_of(iid)
        if r1 is not None:
            c, rule = r1, "R1 (PT cls_of)"
        else:
            c, rule = TABLE[lv], "R2 (LV class %s)" % lv
            unmapped.setdefault(lv, []).append(iid)
            if "cliff" in iid:
                c, rule = "cliff", "R3 (cliff family)"
            elif "wreck" in iid:
                c, rule = "wreck", "R3 (wreck family)"
            elif iid.startswith("sea_"):
                c, rule = "sea", "R3 (sea_ family)"
        m[int(k)] = c
        rows[iid] = {"value": int(k), "lv_class": lv, "pt_class": r1, "p11_class": c, "rule": rule,
                     "status": "other" if c is None else ("ALLOWED" if c in ALLOWED else "EXCLUDED: " + GROUND.get(c, "?"))}
    lut = np.zeros(256, np.uint8)
    for k, c in m.items():
        if c:
            lut[k] = VAL[c]
    MD.mkdir(parents=True, exist_ok=True)
    shares = {}
    for f in sorted(ST.glob("site_[0-9][0-9].ids.png")):
        nm = f.name[:-8]
        A = np.asarray(Image.open(f).convert("RGB")).astype(np.int32)
        is_pl = A[..., 2] > 100
        idx = np.where(is_pl, np.clip(np.round((A[..., 1] - 8) / 16.0), 0, 15).astype(np.int32) * 16
                       + np.clip(np.round((A[..., 0] - 8) / 16.0), 0, 15).astype(np.int32), 0)
        M = lut[np.clip(idx, 0, 255)]
        Image.fromarray(M, "L").save(MD / (nm + ".classes.png"))
        sh = {c: round(float((M == VAL[c]).mean()), 4) for c in SCHEMA}
        shares[nm] = sh
        dump({"ids": VAL, "share": sh, "other_share": round(float((M == 0).mean()), 4), "source": str(f.relative_to(FID)),
              "_mapping": "fid/ph/harness/site_p11.py derive (s52 (b))"}, str(MD / (nm + ".classes.json")))
        shutil.copyfile(ST / (nm + ".png"), MD / (nm + ".png"))
    out = {"_what": "s52 (b) derived P11 class mapping (R-C9-331)", "pt_cls_of_tool_sha256": sha_tool,
           "ids_table_sha256": hashlib_sha(ST / "ids_table.json"), "class_table": TABLE, "allowed": ALLOWED,
           "excluded": {c: GROUND[c] for c in EXCLUDED + ("ice", "reed")}, "schema": VAL,
           "ids": rows, "unmapped_under_pt_masks_by_lv_class": unmapped, "derived_shares": shares}
    dump(out, str(OUT / "p11_mapping.json"))
    print("unmapped (PT null) by LV class:", {k: len(v) for k, v in unmapped.items()})
    return out


def phase():
    import capture_phase as CP
    views = jload(FID / "pt/site/stills_views.json")["views"]
    vs = views if isinstance(views, list) else [dict(v, name=k) for k, v in views.items()]
    vs = sorted(vs, key=lambda v: v["name"])
    P = load_rgb(PAINT)
    cc = CP.constructed_check(PAINT, U0, V1, vs[0]["camera_centre_ground_uv"])
    rows, bad = {}, []
    for k, v in enumerate(vs):
        nm = v["name"]
        tn, tx, ty = TARGETS[k % 6]
        r = CP.phase_of(ST / (nm + ".png"), P, U0, V1, v["camera_centre_ground_uv"])
        cd = lambda a, b: min(abs(a - b), 1 - abs(a - b))
        dx, dy = cd(r["phase_x"], tx), cd(r["phase_y"], ty)
        ok = r.get("n", 0) >= 10 and dx <= 0.10 and dy <= 0.10
        rows[nm] = {"phase_x": r["phase_x"], "phase_y": r["phase_y"], "n": r.get("n"), "target": [tn, tx, ty],
                    "pt_target": v.get("phase_target"), "dx": round(dx, 3), "dy": round(dy, 3), "accepted": ok}
        if not ok:
            bad.append(nm)
    out = {"constructed_check": cc, "constructed_pass": all(c["ok"] for c in cc), "views": rows, "not_accepted": bad}
    dump(out, str(OUT / "p11_phase.json"))
    print("constructed", out["constructed_pass"], "not accepted", bad)
    return out


def build():
    import p11_abx as X
    import p11_abx3 as X3
    ph = jload(OUT / "p11_phase.json")
    assert ph["constructed_pass"], "constructed phase check failed -> STOP"
    st = [MD / (nm + ".png") for nm in sorted(ph["views"]) if ph["views"][nm]["accepted"]]
    X._centres()
    for v in jload(FID / "pt/site/stills_views.json")["views"]:
        X._CENTRES[v["name"] + ".png"] = tuple(v["camera_centre_ground_uv"])
    saved = X.EXCLUDED
    X.EXCLUDED = EXCLUDED
    try:
        r = X3.build3("site_v1_vs_site", st, seed=331, rule_exclusion=True)
    finally:
        X.EXCLUDED = saved
    r = dict(r, stills=[p.name for p in st], stills_not_accepted=ph["not_accepted"],
             excluded=list(EXCLUDED) + ["ice", "reed"], key="fid/ph/p11/keys/abx3_site_v1_vs_site.json",
             verdict_before_judge="VOID (fewer than 40 scored trials drawable)" if r["scored"] < 40 else "judge-ready")
    dump(r, str(OUT / "p11v3_build.json"))
    print({k: r[k] for k in ("scored", "repeats", "catches", "images", "by_class", "catch_by_class", "UNDERPOWERED", "verdict_before_judge")})
    return r


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("derive", "all"):
        derive()
    if cmd in ("phase", "all"):
        phase()
    if cmd in ("build", "all"):
        build()
