#!/usr/bin/env python3
"""
axis_sign_alignment_refit_candidate_1_2026_07_16.py — WORK ITEM A of the R3-ADDENDUM completion charge.
======================================================================================================
Axis-sign alignment of the emitted Refit-Candidate-1 coordinates to Edition-I orientation, per the
addendum-completion brief item A:

  - On the 469 shared actives: corr(E1_dim1, refit_dim1) and corr(E1_dim2, refit_dim2) on RAW
    coordinates (atlas-coordinates-active.csv E1-frozen vs refit-candidate-1-coordinates-active.csv),
    NOT Procrustes-transformed.
  - Rule: reflection-only, max-|correlation| to Edition-I orientation. If a dim's corr < 0 -> flip
    that dim's sign EVERYWHERE. If |corr| < 0.10 for either dim -> HALT + surface (sign not
    determinable; don't guess).

OUTCOME (2026-07-16, recorded here + in MIGRATION.md): **HALT.** The RAW same-index correlations are
dim1 = 0.0446 (|.| < 0.10 -> tripwire) and dim2 = 0.4277. The full raw correlation matrix is
OFF-DIAGONAL dominant (|E1_d1 x refit_d2| = 0.6697 >> the diagonal), and the optimal orthogonal
transform mapping refit->E1 is a REFLECTION + ~117deg ROTATION (det = -1). The refit plane's axes are
ROTATED/SWAPPED relative to Edition-I (refit_dim2 tracks E1_dim1), not merely sign-flipped. A
reflection-only sign alignment (the brief's mandated + only-permitted operation) CANNOT anchor a
rotated plane; the sign of refit_dim1 is genuinely not determinable by the corr rule because its
Edition-I counterpart is refit_dim2, not refit_dim1.

The brief's stated expectation (dim1 ~ 0.64, dim2 ~ 0.27) is drawn from comparison-report §2, which
reports the POST-PROCRUSTES aligned correlations. Item A forbids that rotation and commands the RAW
frame; in the raw frame the axes have not survived in place. This script reproduces both frames so the
discrepancy is legible.

Per the brief HALT protocol ("HALT conditions: |corr| < 0.10 either dim") + elrond discipline (no
silent transformation; surface what the data says; escalate through knight-rider, never guess a
transform), item A HALTS. Items B/C/D key on the alignment ("EAST-half x>=0 = PERFORM side" is
meaningful only post-alignment) and are therefore BLOCKED pending a resolution ruling (gandalf's call:
whether to permit an orthogonal-Procrustes alignment for the region-pinned machinery, or to re-pin the
drill-in region on the refit's own axes). This script emits NOTHING to any artifact; it is a
read-only diagnostic. The served Edition-III / atlas.json frames are untouched.

Author: elrond (data steward). TOOL script (diagnostic/enumeration), not engine code.
Run:  python3 axis_sign_alignment_refit_candidate_1_2026_07_16.py
"""

import csv
import json
import os

import numpy as np
from scipy.spatial import procrustes

ATLAS = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/atlas"
E1_ACTIVE = os.path.join(ATLAS, "atlas-coordinates-active.csv")            # Edition-I frozen (469) — served frame
E1_JSON = os.path.join(ATLAS, "atlas.json")                               # served truth (identity check only)
RC_ACTIVE = os.path.join(ATLAS, "refit-candidate-1-coordinates-active.csv")  # refit (628)

HALT_THRESHOLD = 0.10   # brief item A: |corr| < 0.10 either dim -> HALT


def read_active(path):
    d = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            d[row["kit_id"].strip()] = (float(row["dim1"]), float(row["dim2"]))
    return d


def main():
    e1 = read_active(E1_ACTIVE)
    rc = read_active(RC_ACTIVE)
    shared = sorted(set(e1) & set(rc))

    # ---- integrity: confirm the E1 CSV IS the served frozen frame (never transformed) ----
    served = {p["kit_id"]: (p["x"], p["y"])
              for p in json.load(open(E1_JSON))["points"] if not p.get("supplementary")}
    common = sorted(set(served) & set(e1))
    max_l1 = max(abs(served[k][0] - e1[k][0]) + abs(served[k][1] - e1[k][1]) for k in common)

    E = np.array([e1[k] for k in shared])
    R = np.array([rc[k] for k in shared])

    def c(u, v):
        return float(np.corrcoef(u, v)[0, 1])

    # ---- item A: RAW same-index correlations (the alignment decision quantities) ----
    corr_d1 = c(E[:, 0], R[:, 0])
    corr_d2 = c(E[:, 1], R[:, 1])
    cross_12 = c(E[:, 0], R[:, 1])   # E1_dim1 vs refit_dim2
    cross_21 = c(E[:, 1], R[:, 0])   # E1_dim2 vs refit_dim1

    # ---- optimal orthogonal transform (refit-plane -> E1-plane): rotation vs reflection diagnosis ----
    Ec = E - E.mean(0); Rc = R - R.mean(0)
    Ec /= np.linalg.norm(Ec); Rc /= np.linalg.norm(Rc)
    U, S, Vt = np.linalg.svd(Rc.T @ Ec)
    Omega = U @ Vt
    det = float(np.linalg.det(Omega))
    angle = float(np.degrees(np.arctan2(Omega[1, 0], Omega[0, 0])))

    # ---- post-Procrustes (the frame report §2 used; item A FORBIDS it — shown for legibility) ----
    m1, m2, _ = procrustes(E, R)
    proc_d1 = c(m1[:, 0], m2[:, 0])
    proc_d2 = c(m1[:, 1], m2[:, 1])

    # ---- corr rule ----
    halt = (abs(corr_d1) < HALT_THRESHOLD) or (abs(corr_d2) < HALT_THRESHOLD)
    flip_d1 = corr_d1 < 0
    flip_d2 = corr_d2 < 0

    print("=" * 78)
    print("WORK ITEM A — axis-sign alignment, Refit-Candidate-1 -> Edition-I orientation")
    print("=" * 78)
    print("shared actives (469 expected):", len(shared))
    print("E1 CSV == served atlas.json frozen frame: max L1 diff = %.2e (0 => untransformed)" % max_l1)
    print()
    print("--- RAW same-index correlations (item A decision quantities; NOT Procrustes) ---")
    print("  corr(E1_dim1, refit_dim1) = %+.4f   |corr| = %.4f" % (corr_d1, abs(corr_d1)))
    print("  corr(E1_dim2, refit_dim2) = %+.4f   |corr| = %.4f" % (corr_d2, abs(corr_d2)))
    print()
    print("--- full RAW 2x2 corr matrix (E1 rows x refit cols) — off-diagonal reveals swap ---")
    print("             refit_d1   refit_d2")
    print("  E1_d1     %+8.4f   %+8.4f" % (corr_d1, cross_12))
    print("  E1_d2     %+8.4f   %+8.4f" % (cross_21, corr_d2))
    print()
    print("--- rotation/reflection diagnosis (optimal orthogonal refit->E1) ---")
    print("  Omega =", np.round(Omega, 4).tolist())
    print("  det(Omega) = %+.4f   (-1 => reflection component; +1 => pure rotation)" % det)
    print("  rotation angle ~ %.2f deg" % angle)
    print()
    print("--- post-Procrustes frame (report §2; item A FORBIDS this rotation) ---")
    print("  proc corr dim1 = %+.4f  dim2 = %+.4f   <- the ~0.64/~0.27 the brief 'expected'" % (proc_d1, proc_d2))
    print()
    print("--- corr rule outcome ---")
    print("  |corr(dim1)| < 0.10 :", abs(corr_d1) < HALT_THRESHOLD)
    print("  |corr(dim2)| < 0.10 :", abs(corr_d2) < HALT_THRESHOLD)
    print("  flip dim1 (corr<0)  :", flip_d1)
    print("  flip dim2 (corr<0)  :", flip_d2)
    print()
    if halt:
        print("VERDICT: **HALT** — sign not determinable by the reflection-only corr rule.")
        print("  refit_dim1 same-index corr = %.4f (|.|<0.10) AND its true E1 counterpart is refit_dim2" % corr_d1)
        print("  (|E1_d1 x refit_d2| = %.4f). The refit plane is ROTATED/SWAPPED vs Edition-I, not sign-flipped." % abs(cross_12))
        print("  Reflection-only alignment cannot anchor a rotated plane. Items B/C/D BLOCKED (region pin")
        print("  'EAST-half x>=0 = PERFORM side' would land on an un-anchored plane). Surface to gandalf.")
    else:
        print("VERDICT: alignment determinable — flips: dim1=%s dim2=%s" % (flip_d1, flip_d2))
    print("=" * 78)

    return {
        "shared_n": len(shared),
        "corr_dim1_raw": round(corr_d1, 6),
        "corr_dim2_raw": round(corr_d2, 6),
        "cross_E1d1_refit_d2": round(cross_12, 6),
        "cross_E1d2_refit_d1": round(cross_21, 6),
        "orthogonal_det": round(det, 4),
        "rotation_angle_deg": round(angle, 2),
        "proc_corr_dim1": round(proc_d1, 6),
        "proc_corr_dim2": round(proc_d2, 6),
        "halt": halt,
        "flip_dim1": flip_d1,
        "flip_dim2": flip_d2,
    }


if __name__ == "__main__":
    main()
