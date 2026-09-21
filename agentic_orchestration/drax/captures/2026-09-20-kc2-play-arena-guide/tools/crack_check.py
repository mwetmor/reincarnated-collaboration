#!/usr/bin/env python3
"""crack_check.py — THE SPIDERWEB GATE (crack law § 3 "the gate").

Run KC2-PLAY, Wave 2 scene instruments. Author: drax (presentation seam), 2026-09-20.
Deterministic. numpy + scipy + PIL only. NO model calls, NO network, NO writes under
astra_test_01/ (every input there is opened read-only).

WHAT IT MEASURES
----------------
The crack law (gandalf, `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-cathedral-
reframe-and-crack-law.md` § 3) says: cracks appear ONLY where the authored damage map draws
them; every other stone surface is smooth and whole. The gate operationalises the refusal:

    tile the painted FLOOR into cells of one flagstone; in each cell detect thin dark lines
    and count their JUNCTIONS; a cell with >= 3 junctions that carries NO authorised
    damage-mask pixel is a SPIDERWEB VIOLATION; pass = violations <= 2 % of cells.

FOUR THINGS THE GATE AS WRITTEN DOES NOT SUPPLY, AND WHAT THIS SCRIPT DOES INSTEAD
---------------------------------------------------------------------------------
(1) "from the id mask; skip wall/void/green" — the chunk's id mask has NO wall and NO void
    class. KP-19 deleted them (`b1a_manifest.json :: id_palette.reserved_not_present`
    marks wall band "REMOVED BY KP-19" and void "NOT present ... KP-19 makes the whole
    chunk paintable"). The id mask declares 1 532 064 px of floor = the ENTIRE chunk, plus
    one clipped pool disc. So it cannot say where the painter put floor.
    -> The floor region is a DECLARED geometric window in plate metres (--floor-window-m),
       identical for every painting compared, printed in the manifest; or an explicit
       binary mask (--floor-mask), e.g. the walkable mask mask_from_paint.py emits.

(2) "luminance below the cell's median - k*sigma" — MEASURED NOT TO WORK (see --threshold
    written). sigma is the cell's OWN contrast, so a cell full of cracks raises its own bar
    and a smooth cell's shading noise clears a bar that has collapsed to nothing. On the
    two proofs the written form separates B1a from B1d by a factor of ~1.5 and INVERTS at
    k >= 2.5 (it scores the spiderweb painting CLEANER than the crack-law painting).
    -> Default --threshold bth: threshold the BLACK-TOP-HAT response (the thin-line filter
       itself) at max(k*sigma, --abs-depth). Same k, same sigma, ~5x separation.
       The written form is kept runnable so the finding is reproducible.

(3) "carries no crack_line/impact_fracture/settlement_crack mask pixels" — `settlement_crack`
    IS NOT A CLASS the damage map can emit. damage_map.py's class table is
    crater/spall_ring/crack_line/impact_fracture/scorch/blast_scorch/soot_plume/debris/talus.
    The gate names a class its own generator does not have. Asked for, it is skipped and
    reported as missing rather than silently treated as empty.

(4) The three named classes are not the only authored reasons for dark line structure.
    A cell the map fills with `debris` or `talus` (painted rubble) has stone outlines, not
    cracks, and would score as a violation under the literal reading.
    -> Both readings are computed and BOTH are reported:
         A  as-written : authorised = {crack_line, impact_fracture, settlement_crack}
         B  intact-cell: authorised = ANY non-black damage class; the violation fraction is
                         taken over cells the map declares FULLY INTACT (the law's own
                         painter instruction: "every tile without a crack line in the mask
                         is smooth").

A painting with NO damage mask (B1a predates the crack law) authorises nothing, so its
violation fraction equals its raw junction-dense fraction. The raw fraction is therefore
also reported for every painting: it is mask-independent and is the fair head-to-head.

CELL SIZE
---------
0.6 m square = 60.37 px east x 48.18 px south at plate scale. Why 0.6 m:
  - it is the dressed-flagstone module, and it is what B1a MEASURES — the east-axis
    autocorrelation of B1a's nave floor puts its first strong pitch peak at 60 px = 0.596 m;
  - B1d's flagstones are larger (first peak 80 px = 0.795 m), so 0.6 m is <= one flagstone
    in BOTH paintings. That is the binding constraint: a cell larger than a flagstone
    straddles mortar joints, and a joint crossing is a junction. At <= one flagstone a plain
    joint grid contributes at most 1-2 junctions to a cell, which is why the law's
    >= 3 threshold is robust to joints at all.

USAGE
-----
  python3 crack_check.py --painting <p.png> --label B1d --out <dir> \
      [--mask <damage_mask.png> --events <events.json>] [flags]

OUTPUTS (under --out)
  <label>_crack_cells.json   per-cell table + parameters + both readings
  <label>_crack_heatmap.png  painting dimmed, cells tinted by junction count,
                             violations outlined red, authorised cells outlined green
"""

import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

# --- plate law (frozen; drax b1a_manifest.json :: chunk) ------------------------------
PX_E = 100.617553710938   # px per metre, EAST  (screen +x)
PX_S = 80.307624765       # px per metre, SOUTH (screen +y)
GATE_PX = (768.0, 798.72) # the north gate, native (0,0)

LUMA = np.array([0.2126, 0.7152, 0.0722])
N8 = np.ones((3, 3), bool)

# damage_map.py class table (read from --events when given; this is the fallback)
FALLBACK_CLASSES = {
    "crater": (120, 0, 120), "spall_ring": (200, 80, 200), "crack_line": (255, 255, 255),
    "impact_fracture": (255, 200, 0), "scorch": (60, 60, 60), "blast_scorch": (30, 30, 30),
    "soot_plume": (90, 90, 90), "debris": (0, 160, 255), "talus": (0, 90, 180),
}
AS_WRITTEN_CLASSES = ("crack_line", "impact_fracture", "settlement_crack")


# --- primitives -----------------------------------------------------------------------
def disk(r):
    r = max(1, int(round(r)))
    y, x = np.mgrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


def ellipse(rx, ry):
    rx = max(1, int(round(rx))); ry = max(1, int(round(ry)))
    y, x = np.mgrid[-ry:ry + 1, -rx:rx + 1]
    return (x * x) / float(rx * rx) + (y * y) / float(ry * ry) <= 1.0


def zhang_suen(b):
    """Zhang-Suen thinning. Deterministic, no library dependency."""
    b = b.astype(np.uint8).copy()
    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            P = np.pad(b, 1)
            p2 = P[:-2, 1:-1]; p3 = P[:-2, 2:]; p4 = P[1:-1, 2:]; p5 = P[2:, 2:]
            p6 = P[2:, 1:-1]; p7 = P[2:, :-2]; p8 = P[1:-1, :-2]; p9 = P[:-2, :-2]
            nb = [p2, p3, p4, p5, p6, p7, p8, p9]
            B = sum(nb)
            seq = nb + [p2]
            A = sum(((seq[i] == 0) & (seq[i + 1] == 1)).astype(np.uint8) for i in range(8))
            if step == 0:
                c1 = (p2 * p4 * p6 == 0); c2 = (p4 * p6 * p8 == 0)
            else:
                c1 = (p2 * p4 * p8 == 0); c2 = (p2 * p6 * p8 == 0)
            m = (b == 1) & (B >= 2) & (B <= 6) & (A == 1) & c1 & c2
            if m.any():
                b[m] = 0
                changed = True
    return b


def nbr_count(sk):
    P = np.pad(sk, 1)
    return (P[:-2, 1:-1] + P[:-2, 2:] + P[1:-1, 2:] + P[2:, 2:] +
            P[2:, 1:-1] + P[2:, :-2] + P[1:-1, :-2] + P[:-2, :-2])


def prune_spurs(sk, n):
    """Delete endpoint pixels n times: removes every branch of length <= n px.
    Junctions are interior, so they survive; a spur shorter than n px was never a crack."""
    for _ in range(int(n)):
        e = (sk == 1) & (nbr_count(sk) <= 1)
        if not e.any():
            break
        sk = sk.copy(); sk[e] = 0
    return sk


# --- the gate -------------------------------------------------------------------------
def cell_junctions(L_cell, bth_cell, k, abs_depth, min_line_px, spur_px, mode):
    sig = float(L_cell.std())
    med = float(np.median(L_cell))
    if mode == "written":
        # the gate VERBATIM: luminance below the cell's median - k*sigma.
        lm = (L_cell < med - k * sig) & (bth_cell >= abs_depth)
    else:
        # bth (default): threshold the thin-line filter's own response.
        lm = (bth_cell >= max(k * sig, abs_depth)) & (L_cell < med - 0.5 * sig)
    n_line = int(lm.sum())
    if n_line < min_line_px:
        return 0, n_line, sig
    lab, n = ndi.label(lm, structure=N8)
    if n:
        sz = ndi.sum(lm, lab, range(1, n + 1))
        keep = [i + 1 for i, s in enumerate(sz) if s >= min_line_px]
        lm = np.isin(lab, keep) if keep else np.zeros_like(lm)
    n_line = int(lm.sum())
    if n_line < min_line_px:
        return 0, n_line, sig
    sk = prune_spurs(zhang_suen(lm), spur_px)
    j = (sk == 1) & (nbr_count(sk) >= 3)
    _, nj = ndi.label(j, structure=N8)   # cluster adjacent junction px into ONE junction
    return int(nj), n_line, sig


def main():
    ap = argparse.ArgumentParser(description="crack law § 3 spiderweb gate")
    ap.add_argument("--painting", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--mask", default=None, help="damage mask PNG (class colours). Omit = nothing authorised.")
    ap.add_argument("--events", default=None, help="b1d_events.json (class->rgb table)")
    ap.add_argument("--floor-mask", default=None,
                    help="binary PNG, non-black = floor. Overrides --floor-window-m.")
    ap.add_argument("--floor-window-m", default="-4.0,4.0,-6.0,2.6",
                    help="x_min,x_max,y_min,y_max in plate metres from the gate")
    ap.add_argument("--cell-m", type=float, default=0.6)
    ap.add_argument("--k", type=float, default=2.0)
    ap.add_argument("--threshold", choices=("bth", "written"), default="bth")
    ap.add_argument("--line-se-m", type=float, default=0.03,
                    help="thin-line filter SE radius in metres (0.03 m = 3 px: a crack wider "
                         "than ~6 cm is a fissure, not a crack)")
    ap.add_argument("--abs-depth", type=float, default=10.0,
                    help="absolute line depth floor, luminance 0-255")
    ap.add_argument("--min-line-px", type=int, default=10)
    ap.add_argument("--spur-m", type=float, default=0.05)
    ap.add_argument("--dilate-m", type=float, default=0.08,
                    help="dilation applied to the damage mask before asking 'does this cell "
                         "carry an authorised pixel' — the painter is not pixel-exact")
    ap.add_argument("--junction-min", type=int, default=3)
    ap.add_argument("--pass-frac", type=float, default=0.02)
    ap.add_argument("--sweep", action="store_true",
                    help="re-run over k x {bth, written} and write <label>_calibration_sweep.json. "
                         "Honest calibration is part of the gate: the sweep is how you see "
                         "whether the instrument separates the paintings or was tuned to.")
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    img = Image.open(a.painting).convert("RGB")
    W, H = img.size
    rgb = np.array(img).astype(np.float64)
    L = rgb @ LUMA

    # --- floor region ------------------------------------------------------------------
    if a.floor_mask:
        fm = np.array(Image.open(a.floor_mask).convert("L")) > 0
        if fm.shape != (H, W):
            sys.exit("floor mask size mismatch")
        ys, xs = np.nonzero(fm)
        x0, x1, y0, y1 = int(xs.min()), int(xs.max()) + 1, int(ys.min()), int(ys.max()) + 1
        region_desc = {"kind": "floor_mask", "file": os.path.abspath(a.floor_mask)}
    else:
        xm0, xm1, ym0, ym1 = [float(v) for v in a.floor_window_m.split(",")]
        x0 = max(0, int(GATE_PX[0] + xm0 * PX_E)); x1 = min(W, int(GATE_PX[0] + xm1 * PX_E))
        y0 = max(0, int(GATE_PX[1] + ym0 * PX_S)); y1 = min(H, int(GATE_PX[1] + ym1 * PX_S))
        fm = np.zeros((H, W), bool); fm[y0:y1, x0:x1] = True
        region_desc = {"kind": "declared_window_m",
                       "x_min_m": xm0, "x_max_m": xm1, "y_min_m": ym0, "y_max_m": ym1,
                       "px_rect": [x0, y0, x1, y1]}
    # green is never floor, whatever the region says
    g_dom = rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2])
    fm = fm & (g_dom < 120)

    # --- damage mask -------------------------------------------------------------------
    classes = dict(FALLBACK_CLASSES)
    if a.events:
        ev = json.load(open(a.events))
        classes = {k: tuple(v) for k, v in ev.get("classes", classes).items()}
    missing_classes = [c for c in AS_WRITTEN_CLASSES if c not in classes]

    dil = ellipse(a.dilate_m * PX_E, a.dilate_m * PX_S)
    if a.mask:
        mk = np.array(Image.open(a.mask).convert("RGB"))
        if mk.shape[:2] != (H, W):
            sys.exit("damage mask size mismatch")

        def keyed(names):
            m = np.zeros((H, W), bool)
            for n in names:
                if n in classes:
                    m |= np.all(mk == np.array(classes[n], dtype=mk.dtype), axis=2)
            return m
        auth_A = ndi.binary_dilation(keyed(AS_WRITTEN_CLASSES), structure=dil)
        auth_B = ndi.binary_dilation(keyed(list(classes.keys())), structure=dil)
        mask_file = os.path.abspath(a.mask)
    else:
        auth_A = np.zeros((H, W), bool)
        auth_B = np.zeros((H, W), bool)
        mask_file = None

    # --- tile ---------------------------------------------------------------------------
    cw = a.cell_m * PX_E
    ch = a.cell_m * PX_S
    se = disk(a.line_se_m * PX_E)
    spur_px = int(round(a.spur_m * PX_E))
    bth = ndi.grey_closing(L, footprint=se) - L   # black top-hat = the thin-line filter

    nx = int((x1 - x0) // cw)
    ny = int((y1 - y0) // ch)

    def tile(k, mode):
        out = []
        for iy in range(ny):
            for ix in range(nx):
                ys_, ye_ = int(y0 + iy * ch), int(y0 + (iy + 1) * ch)
                xs_, xe_ = int(x0 + ix * cw), int(x0 + (ix + 1) * cw)
                if fm[ys_:ye_, xs_:xe_].mean() < 0.9:   # cell not fully inside the floor region
                    continue
                nj, nline, sig = cell_junctions(L[ys_:ye_, xs_:xe_], bth[ys_:ye_, xs_:xe_],
                                                k, a.abs_depth, a.min_line_px, spur_px, mode)
                hA = bool(auth_A[ys_:ye_, xs_:xe_].any())
                hB = bool(auth_B[ys_:ye_, xs_:xe_].any())
                dense = nj >= a.junction_min
                out.append({
                    "ix": ix, "iy": iy, "px": [xs_, ys_, xe_, ye_],
                    "x_m": round((0.5 * (xs_ + xe_) - GATE_PX[0]) / PX_E, 3),
                    "y_m": round((0.5 * (ys_ + ye_) - GATE_PX[1]) / PX_S, 3),
                    "junctions": nj, "line_px": nline, "sigma": round(sig, 2),
                    "dense": dense,
                    "authorised_A": hA, "authorised_B": hB,
                    "violation_A": bool(dense and not hA),
                    "intact_B": bool(not hB),
                    "violation_B": bool(dense and not hB),
                })
        return out

    cells = tile(a.k, a.threshold)
    n = len(cells)
    if n == 0:
        sys.exit("no cells — floor region empty")
    dense_n = sum(c["dense"] for c in cells)
    vA = sum(c["violation_A"] for c in cells)
    intactB = sum(c["intact_B"] for c in cells)
    vB = sum(c["violation_B"] for c in cells)

    res = {
        "label": a.label,
        "painting": os.path.abspath(a.painting),
        "damage_mask": mask_file,
        "generated": "2026-09-20",
        "author": "drax (presentation seam) — run KC2-PLAY W2 scene instruments",
        "gate": "crack law § 3 (gandalf 2026-09-20)",
        "plate": {"px_per_m_east": PX_E, "px_per_m_south": PX_S, "gate_px": list(GATE_PX)},
        "parameters": {
            "cell_m": a.cell_m, "cell_px": [round(cw, 2), round(ch, 2)],
            "k": a.k, "threshold_mode": a.threshold,
            "line_se_m": a.line_se_m, "line_se_px": int(round(a.line_se_m * PX_E)),
            "abs_depth_luma": a.abs_depth, "min_line_px": a.min_line_px,
            "spur_m": a.spur_m, "spur_px": spur_px,
            "dilate_m": a.dilate_m,
            "junction_min": a.junction_min, "pass_frac": a.pass_frac,
        },
        "floor_region": region_desc,
        "classes_used": {k: list(v) for k, v in classes.items()},
        "classes_named_by_the_gate_but_absent_from_the_map": missing_classes,
        "totals": {
            "cells": n,
            "junction_dense_cells": dense_n,
            "raw_dense_fraction": round(dense_n / n, 5),
            "reading_A_as_written": {
                "authorised_classes": list(AS_WRITTEN_CLASSES),
                "violations": vA, "fraction": round(vA / n, 5),
                "pass": bool(vA / n <= a.pass_frac),
            },
            "reading_B_intact_cells": {
                "authorised_classes": "any non-black damage class",
                "cells_declared_intact": intactB,
                "violations": vB,
                "fraction": round(vB / intactB, 5) if intactB else None,
                "pass": bool(intactB and vB / intactB <= a.pass_frac),
            },
        },
        "cells": cells,
    }
    jp = os.path.join(a.out, f"{a.label}_crack_cells.json")
    json.dump(res, open(jp, "w"), indent=1)

    # --- honest calibration: the same instrument across k and both threshold forms --------
    if a.sweep:
        sweep = {"label": a.label, "painting": os.path.abspath(a.painting),
                 "damage_mask": mask_file, "junction_min": a.junction_min,
                 "cells_in_region": n, "rows": []}
        for mode in ("bth", "written"):
            for kk in (1.0, 1.5, 2.0, 2.5, 3.0):
                cc = tile(kk, mode)
                m = len(cc)
                dn = sum(c["dense"] for c in cc)
                va = sum(c["violation_A"] for c in cc)
                ib = sum(c["intact_B"] for c in cc)
                vb = sum(c["violation_B"] for c in cc)
                sweep["rows"].append({
                    "threshold_mode": mode, "k": kk, "cells": m,
                    "raw_dense_fraction": round(dn / m, 5) if m else None,
                    "violation_fraction_A": round(va / m, 5) if m else None,
                    "cells_declared_intact_B": ib,
                    "violation_fraction_B": round(vb / ib, 5) if ib else None,
                })
                print(f"  sweep {mode:8s} k={kk}: dense {100*dn/m:5.2f} %   A {100*va/m:5.2f} %"
                      + (f"   B {100*vb/ib:5.2f} % of {ib}" if ib else ""))
        sp = os.path.join(a.out, f"{a.label}_calibration_sweep.json")
        json.dump(sweep, open(sp, "w"), indent=1)
        print(f"  -> {sp}")

    # --- heat map -----------------------------------------------------------------------
    hm = Image.fromarray((np.array(img).astype(np.float64) * 0.42).astype(np.uint8))
    d = ImageDraw.Draw(hm, "RGBA")
    jmax = max(1, max(c["junctions"] for c in cells))
    for c in cells:
        xs_, ys_, xe_, ye_ = c["px"]
        t = min(1.0, c["junctions"] / float(max(jmax, a.junction_min)))
        d.rectangle([xs_, ys_, xe_ - 1, ye_ - 1],
                    fill=(int(40 + 215 * t), int(200 * (1 - t)), int(60 * (1 - t)), 105))
        if c["violation_A"]:
            d.rectangle([xs_, ys_, xe_ - 1, ye_ - 1], outline=(255, 0, 0, 255), width=2)
        elif c["authorised_A"]:
            d.rectangle([xs_, ys_, xe_ - 1, ye_ - 1], outline=(0, 255, 90, 200), width=1)
    d.rectangle([6, 6, 1100, 118], fill=(0, 0, 0, 215))
    for i, line in enumerate([
        f"CRACK-LAW GATE  {a.label}   cell {a.cell_m} m   k={a.k} ({a.threshold})   "
        f"junctions>={a.junction_min}   pass<={a.pass_frac*100:.0f}%",
        f"cells {n}   junction-dense {dense_n} ({100*dense_n/n:.1f}%)   "
        f"A(as-written) violations {vA} = {100*vA/n:.1f}%  {'PASS' if vA/n<=a.pass_frac else 'FAIL'}",
        f"B(intact-cell) {vB}/{intactB} = {(100*vB/intactB):.1f}%" if intactB else "B(intact-cell) n/a",
        "red box = violation   green box = cell carries an authorised crack pixel   "
        "tint = junction count",
    ]):
        d.text((14, 14 + i * 26), line, fill=(255, 255, 255, 255))
    pp = os.path.join(a.out, f"{a.label}_crack_heatmap.png")
    hm.save(pp)

    print(f"[{a.label}] cells={n} dense={dense_n} ({100*dense_n/n:.2f}%)  "
          f"A={vA} ({100*vA/n:.2f}%, pass<={a.pass_frac*100:.0f}%: "
          f"{'PASS' if vA/n<=a.pass_frac else 'FAIL'})  "
          f"B={vB}/{intactB}" + (f" ({100*vB/intactB:.2f}%)" if intactB else ""))
    if missing_classes:
        print(f"[{a.label}] gate names classes the damage map cannot emit: {missing_classes}")
    print(f"  -> {jp}\n  -> {pp}")


if __name__ == "__main__":
    main()
