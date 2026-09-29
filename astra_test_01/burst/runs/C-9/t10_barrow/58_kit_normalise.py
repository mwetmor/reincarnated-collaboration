#!/usr/bin/env python3
"""C-9 T10-1b: put the six kit props at true scale and write kit_assets.json.

    python3 58_kit_normalise.py [object ...]

NO PITCH CORRECTION. The barrow's nine assets are each squat by cos(52.95) = 0.602 and get
a 1.660 Y stretch, because their sheets were cut out of a painting made at 52.95 degrees.
These six were painted from WORDS, straight-on, so there is nothing to undo -- `pitch_correct`
is false and the stretch is not applied. The same number applied to the wrong provenance
makes every prop in this kit 66% too tall, which is why it is stated here rather than
inherited.

WHICH DIMENSION A UNIFORM SCALE HONOURS. Four of the six sheets were given two measurements
and drew a third ratio. Measured on the painted cells:

    rocks   drawn across:height 0.99   brief 1.1 / 0.5  = 2.20
    stump   drawn across:height 0.89   brief 1.2 / 0.55 = 2.18
    log     drawn length:trunk  4.13   brief 2.6 / 0.3  = 8.67
    shield  drawn height:disc   1.81   brief 1.9 / 0.85 = 2.24

The first three miss by a factor of 2.1 to 2.4 in the SAME direction -- every object drawn
to fill a roughly square cell regardless of the proportion the words asked for. One uniform
scale cannot satisfy two numbers that disagree by 2.2x, so the rule here is stated once and
applied to all six: ANCHOR ON THE DIMENSION THE BRIEF NAMES FIRST, and report what the
others came out as. That is a rule rather than six judgements, and the misses are in the
manifest as `brief_secondary_m` against `measured_secondary_m`.

ONE EXCEPTION, AND ITS CONDITION. The log gets a second scale on its two transverse axes so
its trunk lands at 0.3 m. A log is defined by length and diameter, both given; its cross
section is circular; scaling Y and Z TOGETHER leaves it circular and changes only the ratio
the sheet got wrong. The precedent is T10's birch, forced from 2.39 m wide to 1.38 m --
"defensible on a tree, stated not hidden". The condition it turns on: a non-uniform scale is
allowed only where the two transverse axes can move together, so no cross-section distorts.
The rocks and the stump FAIL that condition and do not get one -- their miss is not axial
but COMPOSITIONAL. The brief asked for three rocks spread across 1.1 m and a stump with
roots reaching 1.2 m; the painter stacked the rocks into a pile and drew the roots tight.
Stretching a pile sideways by 2.2 gives a squashed pile, not three spread rocks. That needs
a second sheet, not a scale factor.
"""
import json
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE / "kit_work"
KIT = HERE / "kit"
PLAY_YAW = 47.0
PLAY_PITCH = 52.95354112560294
SNOW_BED_MIN = 0.60

# anchor: which measured dimension the brief's FIRST number is fixed to.
#   height   canonical Y extent          across   canonical X extent
#   disc     widest row of the front silhouette, as a fraction of its X extent
#   length   canonical X extent, with a transverse scale on Y and Z (see the docstring)
SPEC = {
    "rocks":  {"anchor": "height", "m": 0.50, "what": "largest of three snow-capped rocks",
               "brief": "largest ~0.5 m high, cluster ~1.1 m across",
               "secondary": ("across", 1.10)},
    "stump":  {"anchor": "height", "m": 0.55, "what": "frost-covered birch stump",
               "brief": "~0.55 m high, roots ~1.2 m across",
               "secondary": ("across", 1.20)},
    "log":    {"anchor": "length", "m": 2.60, "what": "fallen birch log",
               "brief": "~2.6 m long, ~0.3 m thick", "transverse_m": 0.30,
               "secondary": ("trunk", 0.30)},
    "cairn":  {"anchor": "height", "m": 1.00, "what": "cairn of stacked flat stones",
               "brief": "~1.0 m high", "secondary": None},
    "skull":  {"anchor": "across", "m": 1.30, "what": "elk skull with wide antlers, three ribs",
               "brief": "~1.3 m antler span", "secondary": None},
    "shield": {"anchor": "disc",   "m": 0.85, "what": "split round shield on two crossed spears",
               "brief": "shield ~0.85 m, spears ~1.9 m", "secondary": ("spear", 1.90)},
}


def sil(p: pathlib.Path) -> np.ndarray:
    a = np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128
    ys, xs = np.nonzero(a)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def disc_frac(m: np.ndarray) -> float:
    """Shield diameter as a fraction of the silhouette's width: its widest row."""
    return float(m.sum(1).max()) / m.shape[1]


def trunk_frac(m: np.ndarray) -> float:
    """Trunk diameter as a fraction of the silhouette's height: the median column height
    over the central 60% of the length, which excludes the flared and torn ends."""
    c = m.sum(0)[int(m.shape[1] * 0.2):int(m.shape[1] * 0.8)]
    return float(np.median(c)) / m.shape[0]


def area_png(p: pathlib.Path) -> int:
    return int((np.asarray(Image.open(p).convert("RGBA"))[..., 3] > 128).sum())


def canon_size(glb: pathlib.Path, a0: float) -> list:
    pj = WORK / "params_probe.json"
    pj.write_text(json.dumps({"a0": a0, "yaw": 0, "sx": 1, "sy": 1, "sz": 1,
                              "measure_only": True}))
    r = subprocess.run(["blender", "--background", "--python", str(HERE / "57_kit_bake.py"),
                        "--", str(glb), str(WORK / "unused.glb"), str(pj)],
                       check=True, capture_output=True, text=True)
    line = [l for l in r.stdout.splitlines() if l.startswith("[canon]")][0]
    return json.loads(line[len("[canon] "):])["size_m_gltf"]


def main() -> int:
    want = sys.argv[1:] or list(SPEC)
    KIT.mkdir(exist_ok=True)
    meas = json.loads((WORK / "kit_measure.json").read_text())
    out = {}
    man = KIT / "kit_assets.json"
    if man.exists():
        out = json.loads(man.read_text()).get("models", {})
    for obj in want:
        sp = SPEC[obj]
        m = meas[obj]
        a0 = m["front_azimuth_deg"]
        red = WORK / "red8k" / ("%s.glb" % obj)
        Lx, Ly, Lz = canon_size(red, a0)
        front = sil(WORK / "probe2" / ("%s_red_p0" % obj) / ("%s_az%03d.png" % (obj, a0)))

        note = None
        if sp["anchor"] == "height":
            s = sp["m"] / Ly
            sx = sy = sz = s
        elif sp["anchor"] == "across":
            s = sp["m"] / Lx
            sx = sy = sz = s
        elif sp["anchor"] == "disc":
            d_units = disc_frac(front) * Lx
            s = sp["m"] / d_units
            sx = sy = sz = s
            note = "scaled so the shield disc (widest row of the front silhouette, %.3f of " \
                   "its width) measures %.2f m" % (disc_frac(front), sp["m"])
        elif sp["anchor"] == "length":
            sx = sp["m"] / Lx
            t_units = trunk_frac(front) * Ly
            sy = sz = sp["transverse_m"] / t_units
            note = "non-uniform: length %.3f, both transverse axes %.3f, so the trunk " \
                   "(median section over the central 60%%, %.3f of the silhouette height) " \
                   "measures %.2f m and the section stays circular" \
                   % (sx, sy, trunk_frac(front), sp["transverse_m"])

        # The yaw is simply the play camera's azimuth: canonicalising already put the
        # painted front at azimuth 0, so turning by 47 puts it at 47 -- facing the camera.
        pj = WORK / ("params_%s.json" % obj)
        pj.write_text(json.dumps({"a0": a0, "yaw": PLAY_YAW, "sx": sx, "sy": sy, "sz": sz}))
        glb = KIT / ("%s.glb" % obj)
        r = subprocess.run(["blender", "--background", "--python", str(HERE / "57_kit_bake.py"),
                            "--", str(red), str(glb), str(pj)],
                           check=True, capture_output=True, text=True)
        bake = json.loads([l for l in r.stdout.splitlines()
                           if l.startswith("[bake]")][0][len("[bake] "):])
        stem = str(glb)[:-4]
        cov = area_png(pathlib.Path(stem + "_slab.png")) / max(
            1, area_png(pathlib.Path(stem + "_full.png")))
        sx_m, sy_m, sz_m = bake["size_m_gltf"]

        sec = None
        if sp["secondary"]:
            kind, want_m = sp["secondary"]
            if kind == "across":
                got = max(sx_m, sz_m)
            elif kind == "trunk":
                got = trunk_frac(front) * Ly * sy
            elif kind == "spear":
                got = sy_m          # spear tip height above the ground it is stuck in
            sec = {"what": kind, "brief_m": want_m, "measured_m": round(got, 3),
                   "ratio": round(got / want_m, 3)}

        out[obj] = {
            "glb": "res://models/barrow/kit/%s.glb" % obj,
            "what": sp["what"], "brief": sp["brief"],
            "height_m": round(sy_m, 4), "axis": "height",
            "yaw_deg": 0.0, "pitch_correct": False, "width_m": None,
            "size_m": [round(v, 4) for v in bake["size_m_gltf"]],
            "_size_m_note": "the object's OWN size, measured before the yaw. An AABB is "
                            "world-axis-aligned, so the turned box below is 2.6 m in "
                            "neither axis for a 2.6 m log.",
            "world_aabb_after_yaw_m": bake["world_aabb_after_yaw_m"],
            "footprint_radius_m": round(bake["footprint_radius_m"], 4),
            "snow_bed_ok": bool(cov >= SNOW_BED_MIN),
            "base_coverage": round(cov, 3), "base_slab_m": bake["slab_m"],
            "anchor": sp["anchor"], "anchor_m": sp["m"],
            "brief_secondary": sec,
            "scale_note": note,
            "variant": m["variant"], "mirror_iou": m["mirror_iou"],
            "sheet_iou": m["sheet_iou_reduced"],
            "sheet_iou_mean": m["sheet_iou_reduced_mean"],
            "front_azimuth_deg_before_bake": a0,
            "yaw_baked_deg": PLAY_YAW,
            "scale_baked": [round(sx, 6), round(sy, 6), round(sz, 6)],
            "transform_baked": True,
            "raw_aabb_m": m["size_gltf_reduced"],
            "tris": m["tris"]["reduced"],
            "islands": m["islands"]["reduced"],
            "nonmanifold_edges": m["nonmanifold_edges"]["reduced"],
            "watertight": m["watertight"]["reduced"],
            "thin_recall_vs_sheet": m["thin_recall_vs_sheet"]["reduced"],
            "thin_recall_vs_sheet_tol4px": m["thin_recall_vs_sheet"]["reduced_tol4px"],
            "thin_width_px": {"sheet": m["thin_width"]["sheet"]["median_w"],
                              "model": m["thin_width"]["red"]["median_w"]},
            "reduce_silhouette_iou": m["reduce_loss_play_pitch"]["mean"],
        }
        print("%-7s %s -> %s m  footprint r %.3f  base cov %.2f  snow_bed %s%s"
              % (obj, sp["anchor"], [round(v, 3) for v in bake["size_m_gltf"]],
                 bake["footprint_radius_m"], cov, out[obj]["snow_bed_ok"],
                 ("  %s %.2f m vs brief %.2f" % (sec["what"], sec["measured_m"],
                                                 sec["brief_m"])) if sec else ""))
    man.write_text(json.dumps({
        "_what": "C-9 T10-1b scatter kit: six props from the T10K sheets, built by Tripo "
                 "H3.1 multiview, reduced to ~8k tris, at true scale. Same shape as "
                 "barrow_assets.json, plus footprint_radius_m and snow_bed_ok.",
        "_transform": "SCALE, YAW AND ORIGIN ARE BAKED INTO THE GLB. height_m is what the "
                      "model measures and yaw_deg is 0, so a reader that applies this "
                      "manifest the way barrow_assets.json is applied applies identity. "
                      "yaw_baked_deg and scale_baked record what was applied.",
        "_origin": "base at y = 0, XZ origin at the centre of the footprint AABB.",
        "_yaw_convention": "azimuth A places the camera at (sin A, 0, cos A) from the "
                           "object, up +Y. The painted FRONT view of each prop was turned "
                           "to azimuth %.0f, the play camera's, so yaw 0 shows the face the "
                           "sheet drew. pitch %.5f." % (PLAY_YAW, PLAY_PITCH),
        "_snow_bed_ok": "base_coverage >= %.2f, where base_coverage is the top-down "
                        "silhouette area of the bottom 0.10 m of the model over the "
                        "silhouette area of the whole -- how much of its own footprint "
                        "the prop fills at ground level. The slab is 0.10 m, an absolute "
                        "depth rather than a share of the height, because a drift's toe is "
                        "a physical thing: a share would judge a 0.43 m log against a "
                        "0.064 m slab and a 1.6 m spear against a 0.24 m one, and call the "
                        "log the worse bed." % SNOW_BED_MIN,
        "_pitch_correct": "FALSE for every prop in this kit. These sheets were painted from "
                          "words, not cut from the 52.95-degree concept, so the barrow's "
                          "1.660 Y stretch does not apply and is not applied.",
        "models": out}, indent=1) + "\n")
    print("-> %s" % man)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
