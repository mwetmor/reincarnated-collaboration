#!/usr/bin/env python3
"""
atlas_frozen_basis_reconstruct.py — Edition-IV support module (elrond, 2026-07-16).

FAITHFUL RECONSTRUCTION of the frozen Edition-I MCA basis from the durable snapshot
`atlas-frozen-fit-cellkeys-edition1.csv` (469 active cell_keys, byte-frozen). Reuses the
EXACT machinery of `atlas_derivation_2026_07_14.py` (build_indicator / mca_greenacre / the
Stage-0c fuse) — imported verbatim, never re-implemented — so the reconstructed basis is the
same one that seated E3's 469 active + 37 supplementary points.

WHY a reconstruction (Path A, spec §5 A2): supplementary projection needs the frozen fit's
column standard coordinates + MFA block weights + fuse map. Those live only inside the
derivation's runtime `st` object, not in any CSV. This module rebuilds them deterministically
from the 469 durable cell_keys, then EXPOSES:
  - project_one(cell_key_14)  -> 14-dim principal coord (CA supplementary transition formula)
  - cos2_one(cell_key_14)     -> per-point cos^2 (communality) in the frozen basis
  - level_flatten(cell_key_14)-> D1-derived levels ABSENT from the frozen indicator matrix
  - frozen_active_coords()    -> the 469 reconstructed active coords (for the sign-align + smoke test)

SMOKE TEST (self-check, run as __main__): reconstruct the 469 active (x,y) and verify they
reproduce E3's SERVED active coords to < 1e-6 after per-dim sign alignment. If the reconstruction
does not reproduce the served plane, the projection is NOT trustworthy -> the caller HALTS.

This is a TOOL script (curation/derivation), not engine code. Imported by
build_atlas_json_edition4.py. Parent lineage: atlas_derivation_2026_07_14.py (frozen basis).
"""

import csv
import os
import sys
from collections import Counter

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
# Import the derivation's EXACT machinery — never re-implement the math.
import atlas_derivation_2026_07_14 as deriv
from atlas_derivation_2026_07_14 import (
    NAMES, MASK, FUSE_MIN, OTHER_RARE, build_indicator, mca_greenacre,
)

ATLAS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "curated", "atlas"))
FROZEN_FIT_CSV = os.path.join(ATLAS_DIR, "atlas-frozen-fit-cellkeys-edition1.csv")
EDITION3_JSON = os.path.join(ATLAS_DIR, "atlas-edition3.json")
RETAINED_DIMS = 14   # frozen basis: parallel-analysis retained 14 dims (basis badge)


def _read_frozen_fit():
    ids, keys = [], []
    with open(FROZEN_FIT_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ids.append(row["kit_id"].strip())
            keys.append(row["cell_key"].strip())
    return ids, keys


def _build_fuse_map(kit_vals):
    """Stage-0c fuse (Greenacre n<FUSE_MIN -> other-rare), computed from the ACTIVE 469 level
    counts — byte-identical to the derivation because the 469 cell_keys are byte-identical."""
    fuse_map = {}
    for i in range(14):
        c = Counter(v[i] for v in kit_vals if v[i] not in MASK)
        for lv, n in c.items():
            if n < FUSE_MIN:
                fuse_map[(i, lv)] = OTHER_RARE
    return fuse_map


def _apply_fuse(vals, fuse_map):
    out = []
    for i in range(14):
        v = vals[i]
        out.append(v if v in MASK else fuse_map.get((i, v), v))
    return out


class FrozenBasis:
    """Reconstructed frozen Edition-I MCA basis + supplementary-projection surface."""

    def __init__(self):
        self.ids, keys = _read_frozen_fit()
        self.kit_vals = [k.split("|") for k in keys]
        for kid, parts in zip(self.ids, self.kit_vals):
            if len(parts) != 14:
                raise ValueError(f"frozen fit cell_key not 14-field: {kid}")
        self.N = len(self.ids)
        self.fuse_map = _build_fuse_map(self.kit_vals)
        self.kit_fused = [_apply_fuse(v, self.fuse_map) for v in self.kit_vals]

        # Frozen fit: indicator + Greenacre MCA (the exact derivation machinery).
        Z, col_meta, block_of_col, first_sv = build_indicator(self.kit_fused, block_weight=True)
        mca = mca_greenacre(Z, col_meta)
        self.Z = Z
        self.col_meta = col_meta                     # list of (coord_name, level)
        self.block_of_col = block_of_col
        self.first_sv = first_sv                     # MFA block weights (14,)
        self.sv = mca["sv"]
        self.nret = RETAINED_DIMS
        # column standard coordinates (CA transition): col_pc / sv, first nret dims
        self.col_std = mca["col_pc"][:, :self.nret] / self.sv[:self.nret][None, :]
        self.colidx = {lvl: i for i, lvl in enumerate(col_meta)}   # (coord,level) -> col index
        # frozen active principal coords (row_pc), first nret dims
        self.active_row_pc = mca["row_pc"][:, :self.nret]
        # the frozen indicator-matrix LEVEL VOCABULARY, per coordinate (post-fuse, present columns)
        self.basis_levels = {nm: set() for nm in NAMES}
        for (coord, lvl) in col_meta:
            self.basis_levels[coord].add(lvl)

        # sign alignment vs E3 served plane (SVD sign ambiguity) — computed lazily
        self._sign = None

    # --------- projection surface ---------
    def _row_profile(self, cell_key_14):
        """Build the supplementary weighted row profile in the frozen column space.
        Post-fuse; masks + absent-from-basis levels contribute nothing (passive)."""
        raw = cell_key_14.split("|")
        if len(raw) != 14:
            raise ValueError(f"supplementary cell_key not 14-field: {cell_key_14}")
        fused = _apply_fuse(raw, self.fuse_map)
        row = np.zeros(self.Z.shape[1])
        present = 0
        absent = []   # (coord, level) present in the row but NOT a frozen column
        for i in range(14):
            v = fused[i]
            if v in MASK:
                continue
            key = (NAMES[i], v)
            if key in self.colidx:
                j = self.colidx[key]
                row[j] = 1.0 / self.first_sv[self.block_of_col[j]]   # same MFA weight
                present += 1
            else:
                absent.append((NAMES[i], v))
        return row, present, absent

    def project_one(self, cell_key_14):
        """CA supplementary-row principal coordinate (weighted profile), first nret dims.
        Identical formula to atlas_derivation.project_supplementary."""
        row, present, _ = self._row_profile(cell_key_14)
        rt = row.sum()
        if rt <= 0:
            return None
        rowp = row / rt
        coord = np.zeros(self.nret)
        for j in range(len(row)):
            if rowp[j] != 0:
                coord += rowp[j] * self.col_std[j]
        return coord

    def cos2_one(self, cell_key_14, ndim=2):
        """cos^2 (squared cosine / communality) of the supplementary point in the retained space,
        computed on the first `ndim` principal axes (the PLANE the camera shows). cos^2 =
        sum_d F(d)^2 / (chi-square distance of the row profile to the centroid). For a supplementary
        row the total distance-to-centroid in the FULL retained space is ||F||^2 over all nret dims;
        we report communality on the plane = (F1^2 + F2^2) / sum_d F_d^2. Returns None if unprojectable."""
        coord = self.project_one(cell_key_14)
        if coord is None:
            return None
        denom = float(np.sum(coord ** 2))
        if denom <= 0:
            return None
        return float(np.sum(coord[:ndim] ** 2) / denom)

    def full_cos2_quality(self, cell_key_14):
        """Representation quality proxy for P-3 arm-1: the point's squared distance captured by the
        retained plane relative to the retained space (same as cos2_one(ndim=2)). Named separately
        for gate-report clarity."""
        return self.cos2_one(cell_key_14, ndim=2)

    def level_flatten(self, cell_key_14):
        """Return the list of (coordinate, level) pairs the row carries that are ABSENT from the
        frozen indicator matrix (no column) — the silently-flattened levels. § 9(b)."""
        _, _, absent = self._row_profile(cell_key_14)
        return absent

    # --------- sign alignment + smoke test ---------
    def _load_served_active(self):
        import json
        with open(EDITION3_JSON) as f:
            e3 = json.load(f)
        served = {}
        for p in e3["points"]:
            if not p.get("supplementary"):
                served[p["kit_id"]] = (float(p["x"]), float(p["y"]))
        return served

    def sign_alignment(self):
        """Per-dim sign (+1/-1) that aligns the reconstructed active dim1/dim2 to E3's served plane.
        SVD sign is arbitrary; the served plane fixes orientation."""
        if self._sign is not None:
            return self._sign
        served = self._load_served_active()
        idx = {kid: i for i, kid in enumerate(self.ids)}
        sign = [1.0, 1.0]
        for d in range(2):
            num = 0.0
            for kid, (sx, sy) in served.items():
                if kid in idx:
                    s = sx if d == 0 else sy
                    num += s * self.active_row_pc[idx[kid], d]
            sign[d] = 1.0 if num >= 0 else -1.0
        self._sign = sign
        return sign

    def frozen_active_coords(self):
        """469 reconstructed active (x, y) after sign alignment -> dict kit_id -> (x, y)."""
        sign = self.sign_alignment()
        out = {}
        for i, kid in enumerate(self.ids):
            out[kid] = (sign[0] * self.active_row_pc[i, 0], sign[1] * self.active_row_pc[i, 1])
        return out

    def project_point_xy(self, cell_key_14):
        """Sign-aligned supplementary (x, y) for a new point."""
        coord = self.project_one(cell_key_14)
        if coord is None:
            return None
        sign = self.sign_alignment()
        return (sign[0] * coord[0], sign[1] * coord[1])

    def smoke_test(self):
        """Reproduce the 469 served active (x,y); return (max_abs_err, n_checked). The caller HALTS
        if max_abs_err exceeds tolerance — the reconstruction must BE the frozen camera."""
        served = self._load_served_active()
        recon = self.frozen_active_coords()
        max_err = 0.0
        n = 0
        worst = None
        for kid, (sx, sy) in served.items():
            if kid in recon:
                rx, ry = recon[kid]
                e = max(abs(rx - sx), abs(ry - sy))
                if e > max_err:
                    max_err, worst = e, kid
                n += 1
        return max_err, n, worst


if __name__ == "__main__":
    fb = FrozenBasis()
    print(f"[reconstruct] frozen fit: N={fb.N} active rows; nret={fb.nret}")
    print(f"[reconstruct] fuse_map entries: {len(fb.fuse_map)}")
    print(f"[reconstruct] indicator: {fb.Z.shape[0]} x {fb.Z.shape[1]} columns")
    sign = fb.sign_alignment()
    print(f"[reconstruct] sign alignment vs E3 served plane: dim1={sign[0]:+.0f} dim2={sign[1]:+.0f}")
    max_err, n, worst = fb.smoke_test()
    print(f"[SMOKE] reproduced {n} served active (x,y); MAX abs err = {max_err:.3e} (worst: {worst})")
    TOL = 1e-6
    if max_err < TOL:
        print(f"[SMOKE] PASS — reconstruction reproduces the frozen camera to < {TOL:g}.")
    else:
        print(f"[SMOKE] FAIL — reconstruction drift {max_err:.3e} >= {TOL:g}. Projection NOT trustworthy.")
        sys.exit(2)
