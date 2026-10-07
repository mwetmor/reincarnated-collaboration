#!/usr/bin/env python3
"""R-C9-188/189 (2): the play-camera stills PH needs from the Phase 2' pilot for a 40-trial content-controlled P11 ABX,
written to fid/ph/pilot_p11_spec.json, and VERIFIED here by running the fixed generator's selection logic on exactly
these 12 frames (classes from LV's class map + ID render, as W-4(2), p11_window.py)."""
import sys
from collections import Counter

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p11_window as W
import p11_pairs as P
import p11_abx as X

WIN = (0, 0, 4096, 2560)            # R-C9-188: cols 0-2, rows 0-2 of the bv2art 5x5 grid (plate px)
CX = [960, 1685, 2411, 3136]        # 4 x 3 frames of 1920 x 1080, wholly inside the painted window, ~38 % overlap
CY = [540, 1280, 2020]


def frames_pool(I, frames):
    seen, pool = set(), []
    for (sx, sy) in frames:
        cx0, cx1, cy0, cy1 = sx + 0.30 * 1920, sx + 0.66 * 1920, sy + 0.30 * 1080, sy + 0.80 * 1080
        for y in range(sy, sy + 1080 - P.CROP + 1, P.STRIDE):
            for x in range(sx, sx + 1920 - P.CROP + 1, P.STRIDE):
                if x < cx1 and x + P.CROP > cx0 and y < cy1 and y + P.CROP > cy0:
                    continue
                if (x, y) in seen:
                    continue
                seen.add((x, y))
                k = W.crop_class(I, x, y)
                if k:
                    pool.append({"src": "cand_window.png", "rect": [x, y, P.CROP, P.CROP], "class": k})
    return pool


if __name__ == "__main__":
    cls, names, ids, ex, man = W.class_and_ids()
    I = W.classify_cells(cls, names, ids, ex)
    env = man["envelope"]
    u0, v1 = env["u"][0], env["v"][1]
    stills, frames = [], []
    n = 0
    for j, cy in enumerate(CY):
        for i, cx in enumerate(CX):
            n += 1
            cu, cv = u0 + cx / PPM_V1, v1 - cy / 80.3076
            frames.append((cx - 960, cy - 540))
            stills.append({"name": "pilot_%02d" % n, "frame_px_in_plate": [cx - 960, cy - 540, cx + 960, cy + 540],
                           "camera_centre_ground_uv": [round(cu, 4), round(cv, 4)],
                           "knight_uv": [round(cu, 4), round(cv - 0.685, 4)], "facing": "S"})
    v1pool = [c for p in P.V1_STILLS if p.exists() for c in X.crops_controlled(p)]
    pool = frames_pool(I, frames)
    t, rp, bc = W.simulate(v1pool, pool)
    spec = {
        "_what": "PH -> LV/PT: the play-camera stills of the Phase 2' PILOT that P11 (40-trial content-controlled ABX) needs "
                 "(R-C9-188/189; generator harness/p11_abx.py with the R-C9-171 fixes). 12 stills.",
        "pilot_window": {"grid": "bv2art 5x5", "cols": [0, 2], "rows": [0, 2], "plate_px": list(WIN)},
        "capture": {
            "recipe": "IDENTICAL to PT's v1 stills (fid/pc/tools/pc_stills.gd -> fid/pc/v1_stills/views.json): the PAINTED, BUILT "
                      "pilot level as played (take + heather/snow/life), play camera (orthographic, pitch 52.95354, yaw 47, "
                      "ortho_size = 1080 / 100.6176 m), 1920 x 1080, MSAA 4x, Forward+, HUD off; him standing at knight_uv facing S "
                      "(the generator excludes the frame centre where he stands), as PT's v1 stills do. Same settings as v1 or "
                      "the test compares capture settings, not builds.",
            "frames_wholly_inside_the_painted_window": True,
            "write": "fid/pt/pilot_stills/<name>.png + views.json (camera block as fid/pc/v1_stills/views.json)"},
        "class_masks": {
            "need": "for EVERY still, the ID render at the same camera (v1 capture_ids / LV's guide ID tool), mapped to classes:",
            "files": "fid/pt/pilot_stills/<name>.classes.png (8-bit, one value per class, 0 = other) + <name>.classes.json",
            "json_schema": {"ids": {"rock": "int", "standing_stone": "int", "wood": "int", "sea": "int", "wreck": "int",
                                    "hall": "int", "cliff": "int", "snow": "int", "ice": "int", "heather": "int"}},
            "why": "p11_abx.classify_controlled EXCLUDES any crop with sea / wreck / hall / cliff pixels from the mask (R-C9-171 "
                   "content control); without masks only the pixel classes are drawn and the exclusions rely on colour alone"},
        "stills": stills,
        "verification": {"method": "the fixed generator's selection (p11_window.simulate) on these 12 frames, candidate classes "
                                   "from guide_art class/ID maps, v1 pool = v1ref + PT's 6 HEAD stills",
                         "trials": t, "repeats": rp, "by_class": bc, "cand_pool": dict(Counter(c["class"] for c in pool)),
                         "enough": t >= X.N_TRIALS and rp >= X.N_REPEAT,
                         "caveat": "re-run p11_abx.py build on the REAL painted stills; the UNDERPOWERED guard applies before any judge"},
    }
    dump(spec, str(PH / "pilot_p11_spec.json"))
    print(t, rp, bc, dict(Counter(c["class"] for c in pool)))
