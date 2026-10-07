#!/usr/bin/env python3
"""Assemble the P1-P11 calibration from results/*.json -> fid/ph/calibration.json + the table in calibration.md
(between the CALIBRATION-TABLE markers; the prose around it is hand-written and kept).
Run after the row scripts (README.md: run order)."""
import datetime
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

RES = PH / "results"


def j(name):
    p = RES / name
    return jload(p) if p.exists() else {}


def pf(b):
    return "—" if b is None else ("PASS" if b else "FAIL")


def rows():
    out = []
    p1 = j("p1.json")
    out.append({"row": "P1", "kind": "quality", "neg": "R-C9-159",
                "metric": "displayed texel density ratio (play-camera px/m ÷ painted-source px/m), worst static surface",
                "threshold": "≤ 1.05 on every static surface", "threshold_source": "plan § 4 P1; v1 = 1.000 by construction (projection at the play camera, PPM 100.6176)",
                "cells": {k: {"value": p1[k]["value"], "pass": p1[k]["pass"], "note": "%s; %d/%d surfaces over" % (p1[k]["worst_surface"], p1[k]["n_fail"], p1[k]["n_surfaces"])}
                          for k in ("v1", "159", "158", "constructed") if k in p1},
                "constructed": "v1 painting at half density over the same window (2688 × 1664)"})
    p2 = j("p2.json")
    out.append({"row": "P2", "kind": "quality", "neg": "R-C9-159",
                "metric": "lineage chain: share of static textures that resolve, link by link (sha record / bytes / pixels / plate-crop / cited producer), to the one painting's sha",
                "threshold": "100%", "threshold_source": "plan § 4 P2; Gate-1 W-7 (v1 painting sha eecb4266…)",
                "cells": {k: {"value": p2[k]["value"], "pass": p2[k]["pass"], "note": "%d/%d; unresolved: %s" % (p2[k]["resolved"], p2[k]["n"], ", ".join(p2[k]["unresolved"][:5]) or "none")}
                          for k in ("v1", "159", "158", "constructed", "constructed_foreign") if k in p2},
                "constructed": "v1 with bake ring_m95 swapped for a foreign texture (manifest sha breaks); v1 with one bake declared from a per-model sheet"})
    p3 = j("p3.json")
    c3 = {}
    for k, lab in (("v1", "v1"), ("159", "159"), ("constructed_reshade", "constructed")):
        v = p3.get(k, {})
        if "classes" in v:
            c3[lab] = {"value": v["value"], "pass": v["pass"], "note": "worst class: %s; %d class(es) over" % (v["worst_class"], v["n_over"])}
        elif v:
            c3[lab] = {"value": None, "pass": None, "note": v.get("pending", "")}
    out.append({"row": "P3", "kind": "quality", "neg": "R-C9-159",
                "metric": "rendered-vs-painting residual, per class: mean |render − painting| (sRGB 0–255) inside each class eroded 2 px, statics as played at the paint camera",
                "threshold": "≤ 15.5 for every class", "threshold_source": "take/build/mini_overlay.json summary.unlit_mean_abs 15.5 (lit 40.7)",
                "cells": c3, "constructed": "v1 render re-shaded by its own lit map × the painter's shadow (painted light lit twice)"})
    p4 = j("p4.json")
    c4 = {}
    for k, lab in (("v1", "v1"), ("159", "159"), ("constructed_relit_rock", "constructed"), ("constructed_patchwork_rock", "constructed (patchwork)")):
        v = p4.get(k)
        if v:
            fails = sum(1 for r in v["chunks"].values() for c in r["classes"].values() if c.get("pass") is False)
            c4[lab] = {"value": fails, "pass": v["pass"], "note": "class×chunk samples over their v1 bar: %d" % fails}
    out.append({"row": "P4", "kind": "quality", "neg": "R-C9-159",
                "metric": "per-class Lab-histogram (Hellinger) and spectrum-shape (RMS log-power, 4–32 px) distance to pooled v1, as displayed (100.6 px/m)",
                "threshold": "each ≤ v1's own leave-one-chunk-out maximum (snow hist 0.281 / spec 0.097; rock 0.481 / 0.190; ice 0.126 / 0.031)",
                "threshold_source": "v1's 16 paint chunks, leave-one-out", "cells": c4,
                "constructed": "v1 rock relit (×0.7 linear, cooled); patchwork rock (cellularity) — see discards"})
    p5 = j("p5.json")
    out.append({"row": "P5", "kind": "quality", "neg": "R-C9-158 (Gate-1 W-1)",
                "metric": "(a) overlap MAD between neighbouring raw canvases; (b) stitched seam visibility |log2(gradient on seam ÷ off-seam baseline)|",
                "threshold": "(a) ≤ %.2f; (b) ≤ %.3f" % (p5["bars_from_v1"]["mad_max"], p5["bars_from_v1"]["vis_max"]) if p5 else "",
                "threshold_source": "v1's own 24 overlaps / 6 seams (maxima)",
                "cells": {("constructed" if k == "constructed" else k): {"value": "%.2f / %.3f" % (p5[k]["value"]["mad_max"], p5[k]["value"]["vis_max"]), "pass": p5[k]["pass"],
                              "note": "pairs over %d, seams over %d" % (p5[k]["over_bar"]["mad_pairs"], p5[k]["over_bar"]["seams"])}
                          for k in ("v1", "159", "158", "constructed") if k in p5},
                "constructed": "(b) a 6 px misregistered blend in one band; (a) one canvas from a 6%-shifted hand"})
    p6 = j("p6.json")
    inv = p6.get("invention", {}).get("rows", {})
    iou = p6.get("iou", {}).get("rows", {})
    c6 = {}
    if "v1" in inv:
        c6["v1"] = {"value": "%d inv / IoU %.3f" % (inv["v1"]["inventions"], iou.get("v1", {}).get("median", float("nan"))),
                    "pass": inv["v1"]["inventions"] == 0 and iou.get("v1", {}).get("median", 0) >= p6["iou"]["bar_v1_median"], "note": ""}
    if "159" in iou:
        c6["159"] = {"value": "IoU %.3f" % iou["159"]["median"], "pass": iou["159"]["median"] >= p6["iou"]["bar_v1_median"], "note": "silhouette agreement (invention check: BVR)"}
    for k in [k for k in inv if k.startswith("BVR")]:
        c6[k] = {"value": "%d inventions" % inv[k]["inventions"], "pass": inv[k]["inventions"] == 0, "note": "%d dark openings found" % inv[k]["found"]}
    if "constructed" in inv:
        c6["constructed"] = {"value": "%d inv / IoU %.3f" % (inv["constructed"]["inventions"], iou.get("constructed", {}).get("median", float("nan"))),
                             "pass": inv["constructed"]["inventions"] == 0 and iou.get("constructed", {}).get("median", 0) >= p6["iou"]["bar_v1_median"], "note": "stamped doorway; ID shifted 1.5 m"}
    out.append({"row": "P6", "kind": "quality", "neg": "R-C9-155 BVR blocks (invention, Gate-1 W-1); R-C9-159 (silhouettes)",
                "metric": "(a) dark openings (L* < T after 0.1 m smoothing, ≥ 0.5 m²) not at a declared opening; (b) median per-piece IoU of model silhouette vs painted non-ground class",
                "threshold": "(a) inventions = 0, T = %s (v1's own ceiling); (b) ≥ %.3f (v1 median)" % (p6.get("invention", {}).get("T_v1_ceiling"), p6.get("iou", {}).get("bar_v1_median", float("nan"))),
                "threshold_source": "v1 painting: largest L* with no undeclared opening; v1's per-piece IoU median",
                "cells": c6, "constructed": "a 2.2 × 2.6 m doorway stamped on v1's open snow; v1's ID silhouettes shifted 1.5 m"})
    pp = j("p7_p8.json")
    p7, p8 = pp.get("p7", {}), pp.get("p8", {})
    out.append({"row": "P7", "kind": "constraint", "neg": "constructed (RED)",
                "metric": "painted tuft share and clutter share (L* < 55) on the walkable floor and every lane, measured on the painting",
                "threshold": "floor ≤ v1 quadrant max (tuft %.4f, clutter %.4f); lanes ≤ v1 segment max (tuft %.4f, clutter %.4f)" % tuple(p7["bars_from_v1"][k] for k in ("floor_tuft", "floor_clutter", "lane_tuft", "lane_clutter")) if p7 else "",
                "threshold_source": "v1 arena disc (4 quadrants), path + door corridor (2 m segments)",
                "cells": {k: {"value": "%.4f / %.4f" % (p7[k]["floor"]["tuft"], p7[k]["floor"]["clutter"]), "pass": p7[k]["pass"], "note": "lanes over: %s" % (p7[k]["lanes_over"] or "none")}
                          for k in ("v1", "159", "constructed") if k in p7},
                "constructed": "a 3 × 3 m patch of v1 heather ground pasted onto the arena centre"})
    pr = p8.get("precision", {})
    out.append({"row": "P8", "kind": "constraint", "neg": "constructed (RED)",
                "metric": "precision_drawn_on_painted (overlay_check.py's recorded quantity): drawn 3D-heather px on painted tuft px / drawn px, whole window. Reported beside it: instance share on tufts and tint r",
                "threshold": "≥ %s — v1's minimum chunk value (R-C9-169)" % pr.get("bar"),
                "threshold_source": "take/build/overlay_check.json per_chunk (16 chunks 0.4476–0.5783; whole window 0.5221), reproduced exactly by PT (fid/pc/results.json T3) and by PH",
                "cells": {k: {"value": "%.4f (share %.2f)" % (pr[k]["precision"], p8[k]["share"]), "pass": pr[k]["pass"], "note": ""}
                          for k in ("v1", "159", "constructed") if pr.get(k)},
                "constructed": "v1's drawn heather shifted 4 m"})
    p9 = j("p9_p10.json").get("p9", {})
    sw = p9.get("a_heather_sway", {}).get("rows", {})
    tr = p9.get("d_snow_trail_coverage", {})
    fd = p9.get("c_floe_drift", {})
    c9 = {}
    if "v1" in sw:
        c9["v1"] = {"value": "sway %.2f; trail %.2f" % (sw["v1"]["sway"], tr["v1"]["coverage"]), "pass": sw["v1"]["sway_pass"] and tr["v1"]["pass"], "note": "noise %.3f" % sw["v1"]["noise"]}
    else:
        c9["v1"] = {"value": "trail %.2f" % tr.get("v1", {}).get("coverage", float("nan")), "pass": None, "note": "sway pending in-engine capture"}
    if "v159" in sw:
        v = sw["v159"]
        c9["159"] = {"value": "sway %.2f; flow %.2f; drift %s px; trail %.2f" % (v["sway"], v.get("flow", float("nan")), fd.get("median_drift_px"), tr["159"]["coverage"]),
                     "pass": bool(v["sway_pass"] and v.get("flow_pass") and fd.get("pass") and tr["159"]["pass"]), "note": "informational (not a P9 negative)"}
    else:
        c9["159"] = {"value": "trail %.2f" % tr.get("159", {}).get("coverage", float("nan")), "pass": None, "note": "life capture pending"}
    c9["158"] = {"value": "trail %.2f; no SnowField, no wind, static sea" % tr.get("158", {}).get("coverage", 0), "pass": False, "note": "negative control (C-2)"}
    if "v1_nowind" in sw:
        ss = sw.get("v159", {}).get("flow_static_sea_RED")
        c9["constructed"] = {"value": "sway %.2f (v1, wind held); flow %s (159 sea, motion layers hidden)" % (sw["v1_nowind"]["sway"], ss),
                             "pass": bool(sw["v1_nowind"]["sway_pass"] or sw.get("v159", {}).get("flow_static_sea_pass")), "note": "each RED"}
    out.append({"row": "P9", "kind": "constraint", "neg": "R-C9-158; constructed (RED)",
                "metric": "(a) heather sway in a static in-engine pair; (b) water flow in-engine; (c) floe marker UV drift; (d) snow-trail coverage of the floor",
                "threshold": "(a),(b) ≥ 3× noise and ≥ 0.25× v1 heather sway (2.06); (c) ≤ 0.25 px; (d) ≥ 0.99",
                "threshold_source": "v1's own sway; v1 SnowField coverage 1.00; rest-pose UV = 0 drift (DEV-5)",
                "cells": c9, "constructed": "v1 with the wind held; the sea with its motion layers hidden"})
    p10 = j("p9_p10.json").get("p10", {})
    out.append({"row": "P10", "kind": "constraint", "neg": "constructed (RED)",
                "metric": "p99 frame time, desktop Forward+, 1920 × 1080, vsync off, him walking a loop, 900 frames",
                "threshold": "≤ 16.7 ms", "threshold_source": "plan § 4 P10 (10.9–12.4 ms target withdrawn, W-2)",
                "cells": {lab: ({"value": p10[k]["p99_ms"], "pass": p10[k]["pass"], "note": "p50 %.2f" % p10[k]["p50_ms"]} if p10.get(k) else {"value": None, "pass": None, "note": "capture pending"})
                          for k, lab in (("v1", "v1"), ("v159", "159"), ("v1_burn", "constructed"))},
                "constructed": "v1 with a 20 ms busy-wait per frame"})
    import p11_pairs as P11v1
    import p11_abx as ABX
    c11 = {}
    lab = {"cal_v1_vs_159": "159", "cal_v1_vs_158": "158", "cal_v1_vs_constructed_halfdensity": "constructed"}
    for st, nm in lab.items():
        ap = PH / "p11/answers" / (st + ".json")
        aa = PH / "p11/answers" / ("abx_" + st + ".json")
        if aa.exists():
            r = ABX.score(st, aa)
            c11[nm] = {"value": "ABX %.0f%% (inconsistency %.0f%%)" % (100 * r["abx_accuracy"], 100 * r["repeat_inconsistency"]),
                       "pass": r["pass"], "note": "judge VOID" if r["judge_void"] else ""}
        elif ap.exists():
            r = P11v1.score(st, ap)
            c11[nm] = {"value": "v0.1 directional %.1f%% (null FA %.0f%%)%s" % (100 * r["identification"], 100 * r["null_false_alarm"],
                       "" if r["judge_reliable"] else ", judge UNRELIABLE"), "pass": r["pass"] if r["judge_reliable"] else None,
                       "note": "v0.1 instrument, superseded by ABX (R-C9-168); ABX built, awaiting judges"}
    out.append({"row": "P11", "kind": "quality", "neg": "R-C9-159",
                "metric": "blind ABX (R-C9-168): 40 trials A | B | X, X from v1 or the candidate; accuracy of 'X is from A's / B's build'; 10 side-swapped repeats for reliability; fresh judge (C-3)",
                "threshold": "ABX accuracy ≤ 65% (≤ 26/40); judge void if repeat inconsistency > 25%", "threshold_source": "plan § 4 P11; R-C9-168; power table in calibration.md",
                "cells": c11, "constructed": "v1 stills at half texel density", "power": ABX.power_table()})
    return out


def table_md(R):
    cols = ["v1", "159", "158", "constructed"]
    lines = ["| Row | Kind | Negative control | Threshold | v1 | R-C9-159 | R-C9-158 | Constructed fail | Other |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in R:
        cells = []
        for c in cols:
            v = r["cells"].get(c)
            cells.append("—" if not v else "%s **%s**" % (v["value"], pf(v["pass"])))
        other = ["%s: %s **%s**" % (k, v["value"], pf(v["pass"])) for k, v in r["cells"].items() if k not in cols]
        lines.append("| %s | %s | %s | %s | %s | %s |" % (r["row"], r["kind"], r["neg"], r["threshold"], " | ".join(cells), "; ".join(other) or "—"))
    return "\n".join(lines)


if __name__ == "__main__":
    R = rows()
    out = {"_what": "BV2F lane PH -- the v1-parity harness P1-P11, calibrated (Phase 0 task 0.4)",
           "assembled_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "rows": R,
           "discarded": [
               {"row": "P4 (3) cellularity", "why": "cannot see a mechanism-faithful constructed failure (patchwork rock p95 0.417 vs v1 rock 0.402, bar 0.681; ±15% Voronoi tone stamp 0.391); kept as non-binding report"},
               {"row": "P9b film instrument", "why": "cannot separate R-C9-159's animated sea (median ratio 1.71-1.82) from R-C9-158's static one (1.38) on compressed panning films; replaced by the in-engine static pair"}],
           "re_instrumented": [
               {"row": "P6a", "from": "L* < 25, unsmoothed, 20 px opening (sees only BVR's declared door: 1 opening, 0 inventions)",
                "to": "L* < T on a 0.1 m Gaussian, T = v1's ceiling (32), 0.2 m opening, >= 0.5 m^2", "why": "a door interior is textured (planks, smoke, embers); T is computed from v1 alone"},
               {"row": "P5 constructed input", "from": "12 px whole-half shift (invisible to (b): 0.772 vs bar 0.799)", "to": "6 px misregistered blend (ghosting, (b) 1.250)",
                "why": "v1's partition-of-unity stitch cannot produce a hard seam; ghosting is its failure mode. Scope recorded in p5_seams.py"}]}
    dump(out, str(PH / "calibration.json"))
    md = PH / "calibration.md"
    t = table_md(R)
    if md.exists():
        s = md.read_text()
        a, b = s.find("<!-- CALIBRATION-TABLE -->"), s.find("<!-- /CALIBRATION-TABLE -->")
        if a >= 0 and b > a:
            s = s[:a] + "<!-- CALIBRATION-TABLE -->\n" + t + "\n" + s[b:]
            md.write_text(s)
    print(t)
