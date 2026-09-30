#!/usr/bin/env python3
"""C-9 T10-2 step 4 (B): bake every real-model hero's plate onto its own model, and report it.
drax.

    python3 tools/bake_heroes.py [--size 1024]

For each of the 25 real-model heroes (godot/tools/export_hero_meshes.gd must have run):
  1. tools/hero_surface.py builds work/surf_<id>.npz, work/layout_<id>.json and the matte;
  2. tools/t5_06b_bake.py -- the character's projection bake, BYTE-IDENTICAL to
     nb_t8/scripts/t5_06b_bake.py (checked by sha256 below) -- bakes work/bakes/<id>.png;
  3. the numbers, as the character bake reports them: UNSEEN before the fill, and what is
     still bare after the in-island fill ("unseen after fill"), plus the texels painted from
     ANOTHER piece's paint (the piece's geometry lies behind it; the camera never turns, so
     those texels are never on screen).
Writes take/build/bake_report.json.
"""
import hashlib, json, os, subprocess, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BF = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import hero_surface  # noqa: E402

CHAR_BAKE = os.path.join(BF, "..", "nb_t8", "scripts", "t5_06b_bake.py")
BAKE = os.path.join(HERE, "t5_06b_bake.py")
PAINT = os.path.join(BF, "paint", "barrow_full_painted.png")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    assert sha(CHAR_BAKE) == sha(BAKE), "tools/t5_06b_bake.py is not the character's bake, byte for byte"
    os.makedirs(os.path.join(BF, "work", "bakes"), exist_ok=True)
    ids = sorted(f[:-5] for f in os.listdir(hero_surface.MESH) if f.endswith(".json"))
    rep = {"_what": "C-9 T10-2 step 4 (B): the 25 real-model heroes' plates baked onto their own models",
           "bake_script": "tools/t5_06b_bake.py, sha256 %s (= nb_t8/scripts/t5_06b_bake.py)" % sha(BAKE),
           "texture_px": hero_surface.SIZE, "pieces": {}}
    for id_ in ids:
        s = hero_surface.surface(id_)
        out = os.path.join(BF, "work", "bakes", "%s.png" % id_)
        r = subprocess.run([sys.executable, BAKE, os.path.join("work", "surf_%s.npz" % id_), out,
                            "--sheet", "%s:%s" % (id_, PAINT), "--erode", "2"],
                           cwd=BF, capture_output=True, text=True)
        if r.returncode != 0:
            rep["pieces"][id_] = {"surface": s, "bake": "FAILED", "stderr": r.stderr[-600:]}
            print("%-18s BAKE FAILED: %s" % (id_, r.stderr.strip().splitlines()[-1]))
            continue
        br = json.load(open(os.path.join(BF, "work", "bake_report_%s.json" % id_)))
        S = np.load(os.path.join(BF, "work", "surf_%s.npz" % id_))
        on = int((S["tex_tri"] >= 0).sum())
        # texels whose paint came from the occluder: painted texels sampling under alpha 96
        L = json.load(open(os.path.join(BF, "work", "layout_%s.json" % id_)))["cells"]["guide"]
        x0, y0, w, h = L["rect"]
        al = np.array(Image.open(os.path.join(BF, "work", "_cells_%s" % id_, "cell_guide.png")).convert("RGBA"))[:, :, 3]
        painted = np.array(Image.open(out.replace(".png", "_mask.png")))[::-1] > 0     # the bake flips its output
        yy, xx = np.where(painted & (S["tex_tri"] >= 0))
        pw = S["tex_pos"][yy, xx].astype(np.float64)
        px = np.round((pw - L["aim"]) @ np.array(L["screen_right"]) * L["px_per_m"] + w / 2.0).astype(int)
        py = np.round(h / 2.0 - (pw - L["aim"]) @ np.array(L["screen_up"]) * L["px_per_m"]).astype(int)
        occ = int((al[np.clip(py, 0, h - 1), np.clip(px, 0, w - 1)] == 96).sum())
        test = [ln for ln in r.stdout.splitlines() if "self-test" in ln]
        rep["pieces"][id_] = {
            "surface": s,
            "self_test": test[0].split("self-test")[-1].strip() if test else "?",
            "texels_on_mesh": on,
            "unseen_before_fill_pct": br["unseen_pct"],
            "unseen_after_fill_pct": round(100.0 * br["still_bare"] / max(on, 1), 3),
            "filled_in_island": br["filled"], "islands": br["islands"],
            "painted_from_an_occluder_pct": round(100.0 * occ / max(on, 1), 3),
            "texture": os.path.relpath(out, BF)}
        print("%-18s self-test %-45s unseen %6.2f%% -> after fill %6.2f%%   from occluder %.2f%%"
              % (id_, rep["pieces"][id_]["self_test"], br["unseen_pct"],
                 rep["pieces"][id_]["unseen_after_fill_pct"], rep["pieces"][id_]["painted_from_an_occluder_pct"]))
    ok = [v for v in rep["pieces"].values() if v.get("bake") != "FAILED"]
    rep["summary"] = {"baked": len(ok), "failed": [k for k, v in rep["pieces"].items() if v.get("bake") == "FAILED"],
                      "unseen_after_fill_pct_median": round(float(np.median([v["unseen_after_fill_pct"] for v in ok])), 2) if ok else None,
                      "unseen_after_fill_pct_max": round(float(max(v["unseen_after_fill_pct"] for v in ok)), 2) if ok else None,
                      "_why_so_much_unseen": ("ONE camera, fixed: a stone's back and underside are painted by no one. They are "
                                              "also never on screen -- the play camera pans, it does not turn -- so what the "
                                              "fill leaves bare is geometry the player cannot see")}
    os.makedirs(os.path.join(BF, "take", "build"), exist_ok=True)
    json.dump(rep, open(os.path.join(BF, "take", "build", "bake_report.json"), "w"), indent=1)
    print("baked %d of %d; unseen after fill: median %s%%, max %s%%" % (
        len(ok), len(ids), rep["summary"]["unseen_after_fill_pct_median"], rep["summary"]["unseen_after_fill_pct_max"]))


if __name__ == "__main__":
    main()
