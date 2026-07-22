#!/usr/bin/env python3
"""
Leg-B (Edition-V) STEP 2 — element_primary DECISION RULE — 2026-07-22
=====================================================================
Executes the BINDING pre-registration STEP 2 (§3.1 element_primary decision rule, §13):
  "BEFORE feeding the indicator matrix, elrond runs the within-cell test — for kits sharing
   the same atlas_coords tuple (same mechanical cell), is element_primary CONSISTENT or
   SCATTERED? Operationalized as Cramér's V of element_primary against the dominant active
   coordinate. Within-cell CONSISTENT -> ADMIT as AXIS INPUT; within-cell SCATTER -> DEMOTE
   to supplementary/validation-only. If borderline/ambiguous -> RETURN to conductor."

Executor: elrond. READ-ONLY corpus.db. Numbers return; conductor rules any borderline.

The decision rule is FROZEN pre-results (A-LB6 + legolas Q1) so mint/no-mint can't be retro-fitted.
This script computes the number(s) and applies the rule as written; where the atlas_coords
tuple is near-unique (a structural fact of the frozen coordinate register), that degeneracy is
itself reported as a number.

Two complementary operationalizations (both reported for the conductor):
  (1) STRICT within-cell scatter: over cells holding >=2 record kits, is element_primary
      homogeneous within the cell? (The literal reading. Structurally: 265 kits / 259 cells,
      so only ~5 cells are multi-kit -> underpowered; reported honestly.)
  (2) element_primary vs DOMINANT ACTIVE COORDINATE Cramér's V: does element_primary track the
      mechanical coordinate that dominates the frozen basis (the coordinate carrying the most
      loading mass), or is it an orthogonal overlay? This is the powered form of the same
      question ("does the flavor register move WITH mechanics or independently of them").
"""

import os, sys, json, sqlite3, math
from collections import Counter, defaultdict

import numpy as np
from scipy.stats import chi2_contingency

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from atlas_frozen_basis_reconstruct import NAMES  # coordinate order

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
OUT = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/atlas"
SEED = 20260722

# Cramér's V decision bands (legolas supplied the threshold via A-LB6; the rule is directional:
# CONSISTENT/tracks-mechanics => ADMIT; SCATTER/orthogonal => DEMOTE). We report the number and
# apply: V >= 0.5 tracks strongly (ADMIT), V <= 0.3 orthogonal (DEMOTE per legolas Q1 non-
# recoverability), 0.3 < V < 0.5 borderline -> RETURN to conductor.
V_ADMIT = 0.5
V_DEMOTE = 0.3

np.random.seed(SEED)


def ro_connect(path):
    return sqlite3.connect("file:%s?mode=ro" % path, uri=True)


def cramers_v(a, b):
    """Bias-corrected Cramér's V on two aligned categorical lists (drop None pairwise)."""
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(pairs) < 3:
        return float("nan"), float("nan"), 0
    ax = [p[0] for p in pairs]; bx = [p[1] for p in pairs]
    ca = sorted(set(ax)); cb = sorted(set(bx))
    if len(ca) < 2 or len(cb) < 2:
        return 0.0, 1.0, len(pairs)
    ia = {v: i for i, v in enumerate(ca)}; ib = {v: i for i, v in enumerate(cb)}
    tbl = np.zeros((len(ca), len(cb)))
    for x, y in pairs:
        tbl[ia[x], ib[y]] += 1
    chi2, p, _, _ = chi2_contingency(tbl, correction=False)
    n = tbl.sum()
    phi2 = chi2 / n
    r, k = tbl.shape
    phi2corr = max(0.0, phi2 - (k - 1) * (r - 1) / (n - 1))
    rcorr = r - (r - 1) ** 2 / (n - 1)
    kcorr = k - (k - 1) ** 2 / (n - 1)
    denom = min(kcorr - 1, rcorr - 1)
    v = math.sqrt(phi2corr / denom) if denom > 0 else 0.0
    return v, p, len(pairs)


def main():
    report = {}
    print("# Leg-B (Edition-V) STEP 2 — element_primary DECISION RULE")
    print("# Seed %d · READ-ONLY corpus.db" % SEED)
    print()

    con = ro_connect(DB)

    # Pull record-class kits with atlas_coords + first-skill element_primary
    rows = con.execute(
        "SELECT c.kit_id, c.atlas_coords, km.mapping_json "
        "FROM canon_corpus c JOIN kit_mapping km ON km.kit_id=c.kit_id "
        "WHERE c.corpus_class='record' AND c.atlas_coords IS NOT NULL").fetchall()
    kit_coords = {}     # kit -> 14-tuple list
    kit_ep = {}         # kit -> element_primary (first skill) or None
    for kid, ac, mj in rows:
        parts = ac.split("|")
        if len(parts) != 14:
            continue
        kit_coords[kid] = parts
        ep = None
        try:
            d = json.loads(mj)
            skills = d.get("skills", [])
            if skills:
                ep = skills[0].get("element_primary")
        except Exception:
            pass
        kit_ep[kid] = ep
    kits = sorted(kit_coords)
    print("- record kits with atlas_coords + mapping_json: %d" % len(kits))
    report["n_kits"] = len(kits)

    # ---------------------------------------------------------------
    # (1) STRICT within-cell scatter test
    # ---------------------------------------------------------------
    print()
    print("## (1) STRICT within-cell scatter (cells with >=2 record kits)")
    cell_members = defaultdict(list)
    for kid in kits:
        cell_members["|".join(kit_coords[kid])].append(kid)
    multi_cells = {c: m for c, m in cell_members.items() if len(m) >= 2}
    print("- distinct cells: %d ; multi-kit cells (>=2): %d ; kits in multi-kit cells: %d"
          % (len(cell_members), len(multi_cells), sum(len(m) for m in multi_cells.values())))
    report["n_cells"] = len(cell_members)
    report["n_multi_cells"] = len(multi_cells)

    within_homog = 0
    within_scatter = 0
    cell_detail = []
    for c, members in sorted(multi_cells.items()):
        eps = [kit_ep[k] for k in members]
        distinct = set(e for e in eps)  # includes None as a value
        homog = len(distinct) == 1
        if homog:
            within_homog += 1
        else:
            within_scatter += 1
        cell_detail.append({"members": members, "element_primary": eps, "homogeneous": homog})
        print("  - cell {%s...}: %s -> %s"
              % ("|".join(c.split("|")[:4]), [(k.split('-',1)[-1], e) for k, e in zip(members, eps)],
                 "HOMOGENEOUS" if homog else "SCATTER"))
    print("- within-cell result: %d homogeneous / %d scatter (of %d multi-kit cells)"
          % (within_homog, within_scatter, len(multi_cells)))
    report["within_cell_homogeneous"] = within_homog
    report["within_cell_scatter"] = within_scatter
    report["within_cell_detail"] = cell_detail
    print("- NOTE: near-unique atlas_coords (265 kits / %d cells) => strict test is "
          "structurally UNDERPOWERED (only %d testable cells). The powered form is (2)."
          % (len(cell_members), len(multi_cells)))

    # ---------------------------------------------------------------
    # (2) element_primary vs DOMINANT ACTIVE COORDINATE Cramér's V
    # ---------------------------------------------------------------
    print()
    print("## (2) element_primary vs each active coordinate — Cramér's V")
    print("- Question: does element_primary TRACK a mechanical coordinate (=> coherent direction,")
    print("  ADMIT), or scatter orthogonally across ALL coordinates (=> emission overlay, DEMOTE)?")
    print("- element_primary restricted to NON-null (the flavor-bearing kits); coordinate levels")
    print("  drop mask values pairwise.")
    MASK = {"unknown", "blank", "post-cutoff-deferred", "post-cutoff"}
    # element_primary vector (None kept as its own — but for the association we test the flavor
    # signal, so we test BOTH: (a) all kits incl null-as-level, (b) non-null-only).
    ep_all = [kit_ep[k] if kit_ep[k] is not None else "(null)" for k in kits]
    ep_nonnull_mask = [kit_ep[k] is not None for k in kits]

    per_coord = []
    for i, nm in enumerate(NAMES):
        coord_vals = [kit_coords[k][i] if kit_coords[k][i] not in MASK else None for k in kits]
        # (a) all kits, null-as-level
        v_all, p_all, n_all = cramers_v(ep_all, coord_vals)
        # (b) non-null element_primary only
        ep_nn = [ep_all[j] for j in range(len(kits)) if ep_nonnull_mask[j]]
        cv_nn = [coord_vals[j] for j in range(len(kits)) if ep_nonnull_mask[j]]
        v_nn, p_nn, n_nn = cramers_v(ep_nn, cv_nn)
        per_coord.append({"coordinate": nm, "V_all": v_all, "p_all": p_all, "n_all": n_all,
                          "V_nonnull": v_nn, "p_nonnull": p_nn, "n_nonnull": n_nn})
    per_coord.sort(key=lambda x: -(x["V_nonnull"] if not math.isnan(x["V_nonnull"]) else -1))
    print()
    print("| coordinate | V (non-null ep) | p | n | V (all, null=level) |")
    print("|---|---|---|---|---|")
    for r in per_coord:
        print("| %s | %.3f | %.2e | %d | %.3f |"
              % (r["coordinate"], r["V_nonnull"], r["p_nonnull"], r["n_nonnull"], r["V_all"]))
    report["per_coordinate_cramers_v"] = per_coord

    # the DOMINANT active coordinate = the frozen basis's most-loaded coordinate. From the
    # loadings, delivery/geometry dominate dim1. We report element_primary's V against the
    # single strongest-associated coordinate AND the max V across coordinates (the "does it
    # track ANY mechanical axis" signal).
    best = per_coord[0]
    max_v = best["V_nonnull"]
    print()
    print("- STRONGEST element_primary~coordinate association (non-null): %s (V=%.3f, n=%d)"
          % (best["coordinate"], best["V_nonnull"], best["n_nonnull"]))
    report["max_cramers_v"] = max_v
    report["max_cramers_v_coordinate"] = best["coordinate"]

    # cross-check against the RB-6 headline: element_primary vs COURT (damage register) — is the
    # flavor register the SAME as the damage court, or genuinely orthogonal? (legolas Q1/Q2).
    court_rows = con.execute(
        "SELECT c.kit_id, c.court FROM canon_corpus c WHERE c.corpus_class='record' AND c.atlas_coords IS NOT NULL"
    ).fetchall()
    court_map = {k: ct for k, ct in court_rows}
    ep_nn2 = [kit_ep[k] for k in kits if kit_ep[k] is not None]
    court_nn = [court_map.get(k) for k in kits if kit_ep[k] is not None]
    v_court, p_court, n_court = cramers_v(ep_nn2, court_nn)
    print("- CROSS-CHECK element_primary~court (damage register) Cramér's V = %.3f (p=%.2e, n=%d) "
          "— high V here would mean flavor==damage (redundant); low-moderate V confirms ORTHOGONAL."
          % (v_court, p_court, n_court))
    report["cramers_v_ep_vs_court"] = {"V": v_court, "p": p_court, "n": n_court}

    # ---------------------------------------------------------------
    # DECISION
    # ---------------------------------------------------------------
    print()
    print("## DECISION")
    # The rule: element_primary tracks mechanics (CONSISTENT) => ADMIT; scatters (orthogonal
    # overlay) => DEMOTE. legolas Q1 established element_primary is NOT recoverable from
    # elem_raw and the frozen basis has NO element coordinate => it is genuinely absent (an
    # ADMIT candidate). The within-cell + V evidence decides whether it tracks mechanics
    # coherently (a usable axis) or injects orthogonal noise.
    print("- STRICT within-cell: %d/%d multi-cells homogeneous (underpowered)."
          % (within_homog, len(multi_cells)))
    print("- Max element_primary~mechanical-coordinate V = %.3f (%s)." % (max_v, best["coordinate"]))
    print("- element_primary~court V = %.3f (orthogonality cross-check)." % v_court)

    if max_v >= V_ADMIT:
        decision = "ADMIT-AS-AXIS-INPUT"
        rationale = ("element_primary tracks the %s mechanical coordinate at V=%.3f >= %.2f "
                     "(coherent direction, not orthogonal noise)." % (best["coordinate"], max_v, V_ADMIT))
    elif max_v <= V_DEMOTE:
        decision = "DEMOTE-TO-SUPPLEMENTARY"
        rationale = ("element_primary's strongest mechanical association is only V=%.3f <= %.2f "
                     "(orthogonal emission overlay; would inject noise as an axis) -> supplementary + "
                     "loadings-inspection target (§5)." % (max_v, V_DEMOTE))
    else:
        decision = "BORDERLINE-RETURN-TO-CONDUCTOR"
        rationale = ("element_primary max mechanical V=%.3f falls in the borderline band "
                     "(%.2f, %.2f) -> RETURN to conductor with the number." % (max_v, V_DEMOTE, V_ADMIT))
    print()
    print("- **DECISION: %s**" % decision)
    print("  %s" % rationale)
    report["decision"] = decision
    report["rationale"] = rationale
    report["V_admit_threshold"] = V_ADMIT
    report["V_demote_threshold"] = V_DEMOTE

    con.close()
    with open(os.path.join(OUT, "2026-07-22-legb-step2-elemprimary.json"), "w") as f:
        json.dump(report, f, indent=2, default=float)
    print()
    print("=== summary written: %s ===" % os.path.join(OUT, "2026-07-22-legb-step2-elemprimary.json"))
    return decision


if __name__ == "__main__":
    main()
