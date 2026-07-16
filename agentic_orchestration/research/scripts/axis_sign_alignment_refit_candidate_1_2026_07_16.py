#!/usr/bin/env python3
"""
axis_sign_alignment_refit_candidate_1_2026_07_16.py — WORK ITEM A / A' of the R3-ADDENDUM charge.
=================================================================================================
HISTORY (two states, both preserved as lineage):

  ITEM A (original brief, 2026-07-16, commit 90f839de) — HALTED. The brief mandated a
  REFLECTION-ONLY sign alignment (max-|correlation|, "Pure reflection, never rotation"). On the 469
  shared actives the RAW same-index correlations are dim1 = +0.0446 (|.| < 0.10 tripwire) and
  dim2 = +0.4277; the raw 2x2 corr matrix is OFF-DIAGONAL (anti-diagonal) dominant
  (|E1_d1 x refit_d2| = 0.6697 is the largest entry). The optimal orthogonal refit->E1 map is a
  REFLECTION + ~117deg ROTATION (det = -1): the refit plane rotated and its axes ~swapped. A
  reflection-only alignment CANNOT anchor a rotated plane, so item A HALTED and surfaced to gandalf.

  RULING (gandalf, verify gate, 2026-07-16 — brief "RULING" section, commit 0bc3b9da): item A is
  AMENDED to A'. Compute the optimal orthogonal 2x2 map Q (det +-1, NO scaling, NO translation --
  both fits barycenter-origin) minimizing ||E1 - refit.Q||^2 over the 469 shared; apply Q to EVERY
  plane coordinate in the emitted refit artifacts atomically; stamp `plane_alignment`; assert the
  post-alignment same-index corr matrix becomes diagonal-dominant. This is an IN-PLANE ORTHOGONAL
  PROCRUSTES alignment (rotation+reflection), disclosed on-plate and headlined -- distances,
  spreads, congruence, gates, inertia-of-plane are ALL invariant under Q; only the (already
  arbitrary MCA/SVD) orientation convention changes. Raw-axes plates would HIDE the geography
  comparison Matt ordered; alignment EXPOSES the rotation, it does not bury it.

THIS SCRIPT (A') is the reproducible Q-derivation diagnostic + single source of the Q the emitter
and comparison script both consume. It computes Q the SAME way they do (deterministic from the two
RAW plane CSVs), reports the RAW and POST-alignment corr matrices, rotation_deg, det, and the
diagonal-dominance flip, and exposes `compute_Q()` for import. It emits NOTHING to any artifact
(read-only diagnostic + importable helper). Served Edition-III / atlas.json frames are untouched.

DIAGONAL-DOMINANCE TEST (the ruling's assert; also the HALT gate "post-alignment corr NOT
diagonal-dominant"): a 2x2 orientation-agreement matrix is DIAGONAL-DOMINANT iff
  (i)  sum|diag| > sum|anti|   (the magnitude mass sits on the diagonal), AND
  (ii) the single largest-magnitude entry lies ON the diagonal.
RAW is anti-diagonal dominant (fails both); POST-Q is diagonal-dominant (passes both). Note the
row-2 diagonal (E1_dim2 vs aligned dim2) is weak (~0.27) and below its off-diagonal (~0.40): this
is the GENUINE structural finding that the refit's second axis does not survive the ~117deg rotation
cleanly -- disclosed, not smoothed. It does NOT fail the whole-matrix diagonal-dominance test.

Q is computed from the CENTERED clouds (Rc.T @ Ec via SVD) -> orientation-only, translation-free
(the emitted coordinates are NOT translated; corr is translation-invariant so centering only
isolates the orientation Q). Both are barycenter-origin fits per the ruling; the tiny residual
subset-mean is centered out so Q is the pure orientation map.

Author: elrond (data steward). TOOL script (diagnostic/enumeration + importable helper), not engine
code. Run:  python3 axis_sign_alignment_refit_candidate_1_2026_07_16.py
"""

import csv
import json
import os

import numpy as np

ATLAS = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/atlas"
E1_ACTIVE = os.path.join(ATLAS, "atlas-coordinates-active.csv")               # Edition-I frozen (469) — served frame
E1_JSON = os.path.join(ATLAS, "atlas.json")                                  # served truth (identity check only)
RC_ACTIVE = os.path.join(ATLAS, "refit-candidate-1-coordinates-active.csv")  # refit (628) — RAW derivation output

HALT_THRESHOLD = 0.10   # (item-A lineage) |corr| < 0.10 either dim -> reflection-only not determinable


def read_active(path):
    d = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            d[row["kit_id"].strip()] = (float(row["dim1"]), float(row["dim2"]))
    return d


def _corr(u, v):
    return float(np.corrcoef(u, v)[0, 1])


def corr_matrix(A, B):
    """2x2 corr matrix, E1 rows (A) x refit/aligned cols (B)."""
    return np.array([[_corr(A[:, 0], B[:, 0]), _corr(A[:, 0], B[:, 1])],
                     [_corr(A[:, 1], B[:, 0]), _corr(A[:, 1], B[:, 1])]])


def is_diagonal_dominant(C):
    """The ruling's diagonal-dominance test: sum|diag| > sum|anti| AND max-|entry| on the diagonal."""
    absC = np.abs(C)
    sum_diag = float(absC[0, 0] + absC[1, 1])
    sum_anti = float(absC[0, 1] + absC[1, 0])
    max_on_diag = int(absC.argmax()) in (0, 3)   # flat idx 0=(0,0), 3=(1,1)
    return (sum_diag > sum_anti) and max_on_diag, sum_diag, sum_anti, max_on_diag


def compute_Q(e1_active=E1_ACTIVE, rc_active=RC_ACTIVE):
    """THE single source of Q (the emitter + comparison script import this).

    Optimal orthogonal 2x2 map minimizing ||E1 - refit.Q||^2 over the shared actives, both
    barycenter-origin (centered -> orientation-only, translation-free). Returns Q (2x2, det +-1) and
    a full diagnostic dict. Deterministic from the two RAW plane CSVs.
    """
    e1 = read_active(e1_active)
    rc = read_active(rc_active)
    shared = sorted(set(e1) & set(rc))
    E = np.array([e1[k] for k in shared])
    R = np.array([rc[k] for k in shared])

    Ec = E - E.mean(0)
    Rc = R - R.mean(0)
    U, S, Vt = np.linalg.svd(Rc.T @ Ec)   # minimizes ||Ec - Rc.Q||_F over orthogonal Q; maps refit->E1
    Q = U @ Vt
    det = float(np.linalg.det(Q))
    rotation_deg = float(np.degrees(np.arctan2(Q[1, 0], Q[0, 0])))

    C_raw = corr_matrix(E, R)
    C_post = corr_matrix(E, R @ Q)
    raw_dom, raw_sd, raw_sa, raw_maxdiag = is_diagonal_dominant(C_raw)
    post_dom, post_sd, post_sa, post_maxdiag = is_diagonal_dominant(C_post)

    return Q, {
        "shared_n": len(shared),
        "Q": Q.tolist(),
        "det": round(det, 6),
        "rotation_deg": round(rotation_deg, 4),
        "raw_corr": np.round(C_raw, 6).tolist(),
        "post_corr": np.round(C_post, 6).tolist(),
        "raw_diagonal_dominant": raw_dom,
        "post_diagonal_dominant": post_dom,
        "raw_sum_diag": round(raw_sd, 6), "raw_sum_anti": round(raw_sa, 6),
        "post_sum_diag": round(post_sd, 6), "post_sum_anti": round(post_sa, 6),
        "post_max_entry_on_diagonal": post_maxdiag,
        # item-A lineage quantities (the reflection-only decision numbers that HALTED)
        "raw_same_index_dim1": round(float(C_raw[0, 0]), 6),
        "raw_same_index_dim2": round(float(C_raw[1, 1]), 6),
        "raw_cross_E1d1_refit_d2": round(float(C_raw[0, 1]), 6),
    }


def main():
    # integrity: confirm the E1 CSV IS the served frozen frame (never transformed)
    e1 = read_active(E1_ACTIVE)
    served = {p["kit_id"]: (p["x"], p["y"])
              for p in json.load(open(E1_JSON))["points"] if not p.get("supplementary")}
    common = sorted(set(served) & set(e1))
    max_l1 = max(abs(served[k][0] - e1[k][0]) + abs(served[k][1] - e1[k][1]) for k in common)

    Q, d = compute_Q()

    print("=" * 82)
    print("WORK ITEM A' — in-plane orthogonal Procrustes alignment, Refit-Candidate-1 -> Edition-I")
    print("=" * 82)
    print("shared actives (469 expected):", d["shared_n"])
    print("E1 CSV == served atlas.json frozen frame: max L1 diff = %.2e (0 => untransformed)" % max_l1)
    print()
    print("--- item-A lineage (reflection-only decision quantities that HALTED) ---")
    print("  RAW same-index corr(E1_dim1, refit_dim1) = %+.4f  (|.| < 0.10 tripwire)"
          % d["raw_same_index_dim1"])
    print("  RAW same-index corr(E1_dim2, refit_dim2) = %+.4f" % d["raw_same_index_dim2"])
    print("  RAW cross |E1_dim1 x refit_dim2|         = %+.4f  (off-diagonal, the largest entry)"
          % d["raw_cross_E1d1_refit_d2"])
    print()
    print("--- RAW 2x2 corr matrix (E1 rows x refit cols) ---")
    _print_matrix(np.array(d["raw_corr"]))
    print("  sum|diag| = %.4f  sum|anti| = %.4f  -> diagonal-dominant: %s (ANTI-diagonal dominant)"
          % (d["raw_sum_diag"], d["raw_sum_anti"], d["raw_diagonal_dominant"]))
    print()
    print("--- optimal orthogonal Q (refit -> E1; rotation+reflection, NO scaling, NO translation) ---")
    print("  Q =", np.round(Q, 6).tolist())
    print("  det(Q) = %+.4f   (-1 => reflection component present)" % d["det"])
    print("  rotation angle = %.4f deg" % d["rotation_deg"])
    print()
    print("--- POST-alignment 2x2 corr matrix (E1 rows x aligned-refit cols) ---")
    _print_matrix(np.array(d["post_corr"]))
    print("  sum|diag| = %.4f  sum|anti| = %.4f  max-entry-on-diagonal: %s"
          % (d["post_sum_diag"], d["post_sum_anti"], d["post_max_entry_on_diagonal"]))
    print("  -> POST diagonal-dominant: %s" % d["post_diagonal_dominant"])
    print()
    if d["post_diagonal_dominant"]:
        print("VERDICT: **PROCEED (A')** — Q maps the corr mass onto the diagonal (anti-dominant -> "
              "dominant). Alignment anchors the plane; items B/C/D run in the aligned frame.")
        print("  NOTE (disclosed structure): row-2 diagonal (E1_dim2 vs aligned dim2 = %+.4f) is weak "
              "and below its" % np.array(d["post_corr"])[1, 1])
        print("  off-diagonal (%+.4f) -- the refit's 2nd axis does not survive the ~117deg rotation "
              "cleanly. Honest finding, not a defect." % np.array(d["post_corr"])[1, 0])
    else:
        print("VERDICT: **HALT** — post-alignment corr matrix is NOT diagonal-dominant (Q failed to "
              "move the mass onto the diagonal). Surface to gandalf.")
    print("=" * 82)
    return d


def _print_matrix(C):
    print("             refit_d1   refit_d2")
    print("  E1_d1     %+8.4f   %+8.4f" % (C[0, 0], C[0, 1]))
    print("  E1_d2     %+8.4f   %+8.4f" % (C[1, 0], C[1, 1]))


if __name__ == "__main__":
    main()
