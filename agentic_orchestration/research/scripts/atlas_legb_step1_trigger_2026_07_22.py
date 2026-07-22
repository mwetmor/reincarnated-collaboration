#!/usr/bin/env python3
"""
Leg-B (Edition-V) STEP 1 — refit-TRIGGER diagnostic — 2026-07-22
================================================================
Executes the BINDING pre-registration STEP 1 (two-arm refit trigger):
  agentic_orchestration/gandalf/design-inputs/2026-07-22-leg-b-edition-next-preregistration.md (§2, §13)

Executor: elrond (data steward). EXECUTE WITH NO INTERPRETATION.
Numbers return; gandalf (RUN-CONDUCTOR) reads them.

STEP 1 (pre-registration discipline: PUBLISH the census even though the vocabulary
arm is forecast to fire — never skip the measurement because the outcome is predicted):

  (a) cos^2 communality of each record-267 kit in the FROZEN E4 basis (== the frozen
      Edition-I 14-dim MCA; E2/E3/E4 all kept it, basis block edition:1/frozen:true).
      Report cohort median vs E1-active median. Same-machinery projection (the E4 P-3
      arm-1 convention: full_cos2_quality, plane communality dim1-2 over the retained space).
        - 265 record kits carry atlas_coords (14-position, == cell_key format) -> projectable.
        - 2 record kits (d2-teleport-sorc, poe1-blood-magic-kit) carry NULL atlas_coords
          AND are canon_engine_key.row_class='system-record' with NULL cell_key: they are
          degenerate/non-combat identities (pure-movement / keystone-passive) with NO
          derivable 13/14-tuple -> UNPROJECTABLE (reported, not forced; cf. E1's
          vs-golden-egg-scaling handling). The prereg's "trivial fresh projection" assumed
          an atlas_coords tuple that does not exist in v2.0 -> documented curation finding.

  (b) NEW-LEVEL CENSUS: v2.0 geometry-band vocabulary + element_primary levels absent from
      the frozen fit-cellkeys vocabulary. Uses atlas-frozen-fit-cellkeys-edition1.csv as the
      AUTHORITATIVE frozen level column list (NOT atlas-loadings.csv alone, which omits
      reference categories). Level -> exhibit count. Geometry-bands are per-skill grain
      (skill_geometry_band rows); element_primary is per-kit (mapping_json first-skill).

TRIGGER (pinned, pre-results):
  1. Expression arm: record-267 cohort median cos^2 < 0.5 x E1-active median -> refit warranted.
  2. Vocabulary arm: any single absent v2.0 level accumulates >= 20 admitted exhibits -> refit warranted.
  EITHER fires -> STEP 2/3 (Path-B refit). NEITHER -> HALT + RETURN to conductor (§8-A is the
  conductor's ruling, not elrond's).

READ-ONLY on corpus.db (md5 bebc933b... must not move). Emits a diagnostic report to stdout
+ a machine-readable JSON summary for the conductor's independent re-computation.

Run:  python3 atlas_legb_step1_trigger_2026_07_22.py
"""

import os, sys, json, sqlite3
from collections import Counter, defaultdict

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from atlas_frozen_basis_reconstruct import FrozenBasis, NAMES  # exact frozen-basis machinery

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
OUT = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/atlas"
SEED = 20260722  # pinned (no stochastic step here, but pinned per prereg §7)

COS2_ARM_FACTOR = 0.5     # expression arm: cohort median < 0.5 x E1-active median
VOCAB_ARM_MIN = 20        # vocabulary arm: any absent level >= 20 exhibits

np.random.seed(SEED)


def ro_connect(path):
    """Read-only connection — corpus.db must not be mutated by this derivation."""
    return sqlite3.connect("file:%s?mode=ro" % path, uri=True)


def main():
    report = {}
    print("# Leg-B (Edition-V) STEP 1 — refit-TRIGGER diagnostic")
    print("# Seed %d · READ-ONLY corpus.db · frozen E4==E1 basis" % SEED)
    print()

    fb = FrozenBasis()
    # Confirm the frozen camera reproduces (guard: the projection must BE the frozen basis).
    max_err, n_smoke, worst = fb.smoke_test()
    print("[frozen-basis] reconstruct N=%d nret=%d; smoke max_abs_err=%.3e (worst %s) -> %s"
          % (fb.N, fb.nret, max_err, worst, "OK" if max_err < 1e-6 else "FAIL"))
    if max_err >= 1e-6:
        print("!!! HALT: frozen-basis reconstruction drift — projection not trustworthy.")
        sys.exit(2)
    report["frozen_basis_smoke_max_err"] = max_err

    con = ro_connect(DB)

    # ---------------------------------------------------------------
    # (a) cos^2 — record-267 cohort vs E1-active baseline
    # ---------------------------------------------------------------
    print()
    print("## STEP 1(a) — cos^2 communality (frozen E4 basis)")

    # E1-active baseline: cos^2 via the SAME supplementary-projection formula on the 469
    # frozen cell_keys (the E4 P-3 arm-1 convention — full_cos2_quality). Identical machinery
    # for both cohorts => apples-to-apples comparison.
    e1_cos2 = []
    for kid, parts in zip(fb.ids, fb.kit_vals):
        ck = "|".join(parts)
        q = fb.full_cos2_quality(ck)
        if q is not None:
            e1_cos2.append(q)
    e1_median = float(np.median(e1_cos2))
    print("- E1-active baseline: n=%d projectable; median cos^2 = %.5f (mean %.5f)"
          % (len(e1_cos2), e1_median, float(np.mean(e1_cos2))))
    report["e1_active_cos2_n"] = len(e1_cos2)
    report["e1_active_cos2_median"] = e1_median

    # record-267 cohort
    rec = con.execute(
        "SELECT kit_id, atlas_coords FROM canon_corpus WHERE corpus_class='record' ORDER BY kit_id"
    ).fetchall()
    rec_cos2 = []
    unprojectable = []
    field_bad = []
    for kid, ac in rec:
        if ac is None or ac.strip() == "":
            unprojectable.append(kid)
            continue
        if len(ac.split("|")) != 14:
            field_bad.append((kid, len(ac.split("|"))))
            continue
        q = fb.full_cos2_quality(ac)
        if q is None:
            unprojectable.append(kid)
        else:
            rec_cos2.append(q)
    rec_median = float(np.median(rec_cos2))
    print("- record-267 cohort: %d record kits; %d projectable (atlas_coords 14-field); "
          "%d UNPROJECTABLE (NULL/degenerate atlas_coords)."
          % (len(rec), len(rec_cos2), len(unprojectable)))
    print("  - UNPROJECTABLE kits: %s" % (", ".join(sorted(unprojectable)) if unprojectable else "NONE"))
    if field_bad:
        print("  - FIELD-COUNT anomalies (not 14): %s" % field_bad)
    print("  - record-267 median cos^2 = %.5f (mean %.5f)"
          % (rec_median, float(np.mean(rec_cos2))))
    report["record_total"] = len(rec)
    report["record_projectable_n"] = len(rec_cos2)
    report["record_unprojectable"] = sorted(unprojectable)
    report["record_cos2_median"] = rec_median

    # Expression-arm decision
    arm1_threshold = COS2_ARM_FACTOR * e1_median
    arm1_fires = rec_median < arm1_threshold
    print("- **Expression arm:** record median %.5f %s 0.5 x E1-active median (%.5f) -> **%s**."
          % (rec_median, "<" if arm1_fires else ">=", arm1_threshold,
             "FIRES" if arm1_fires else "does NOT fire"))
    report["expression_arm_threshold"] = arm1_threshold
    report["expression_arm_fires"] = bool(arm1_fires)

    # ---------------------------------------------------------------
    # (b) NEW-LEVEL CENSUS — geometry-bands + element_primary absent from frozen vocab
    # ---------------------------------------------------------------
    print()
    print("## STEP 1(b) — new-level census (absent from frozen E4 fit-cellkeys vocabulary)")

    # The frozen vocabulary: the set of levels present in the frozen fit indicator matrix,
    # per coordinate (fb.basis_levels). The geometry-band + element_primary registers use
    # DIFFERENT field names than the 14 frozen coordinates, so their levels are absent-by-
    # construction unless a level name coincides with a frozen coordinate level. We census
    # the v2.0-added registers as their own named fields and mark each level absent iff it
    # appears in NO frozen coordinate's level vocabulary (the honest structural test: "a word
    # the camera has no column for").
    all_frozen_levels = set()
    for nm, lvls in fb.basis_levels.items():
        all_frozen_levels |= lvls
    report["frozen_level_vocab_size"] = len(all_frozen_levels)
    print("- Frozen fit level vocabulary: %d distinct (coord,level) columns across 12 populated "
          "coordinates (range/tempo have all-reference levels; using cellkeys as the authoritative list)."
          % fb.Z.shape[1])
    print("- Frozen distinct level-strings (union across coords): %d" % len(all_frozen_levels))

    # geometry-bands: per-skill grain, record-class only (the derivation population)
    gb_fields = ["delivery_class", "range_band", "motion_signature", "width_band",
                 "speed_band", "cadence_class", "origin"]
    census = {}   # field -> {level -> exhibit_count, absent: bool}
    print()
    print("### geometry-band registers (per-skill grain, record-class exhibits)")
    for fld in gb_fields:
        rows = con.execute(
            "SELECT sgb.%s, COUNT(*) FROM skill_geometry_band sgb "
            "JOIN canon_corpus c ON c.kit_id=sgb.kit_id "
            "WHERE c.corpus_class='record' AND sgb.%s IS NOT NULL AND sgb.%s <> '' "
            "GROUP BY sgb.%s ORDER BY COUNT(*) DESC" % (fld, fld, fld, fld)).fetchall()
        census[fld] = {}
        print("- **%s:**" % fld)
        for lvl, cnt in rows:
            absent = lvl not in all_frozen_levels
            census[fld][lvl] = {"count": cnt, "absent": absent}
            flag = " [ABSENT>=20]" if (absent and cnt >= VOCAB_ARM_MIN) else (" [absent]" if absent else " [in-vocab]")
            print("    - %s = %d%s" % (lvl, cnt, flag))

    # element_primary: per-kit (first-skill), record-class
    print()
    print("### element_primary delivery-register (per-kit first-skill, record-class exhibits)")
    ep_rows = con.execute(
        "SELECT km.mapping_json FROM kit_mapping km JOIN canon_corpus c ON c.kit_id=km.kit_id "
        "WHERE c.corpus_class='record' AND km.mapping_json IS NOT NULL").fetchall()
    ep_counter = Counter()
    for (mj,) in ep_rows:
        try:
            d = json.loads(mj)
        except Exception:
            continue
        skills = d.get("skills", [])
        if skills:
            ep = skills[0].get("element_primary")
            ep_counter[ep if ep is not None else "(null)"] += 1
    census["element_primary"] = {}
    for lvl, cnt in ep_counter.most_common():
        # element_primary vocabulary: fire/lightning/shadow/water/earth/(null). The frozen
        # basis has NO element coordinate at all (Class-B exclusion, legolas Q1) -> every
        # non-null element_primary level is absent from the frozen vocabulary by construction.
        absent = lvl not in all_frozen_levels
        census["element_primary"][lvl] = {"count": cnt, "absent": absent}
        flag = " [ABSENT>=20]" if (absent and cnt >= VOCAB_ARM_MIN) else (" [absent]" if absent else " [in-vocab]")
        print("    - %s = %d%s" % (lvl, cnt, flag))

    # Vocabulary-arm decision: any absent level with >= 20 exhibits
    absent_ge20 = []
    for fld, levels in census.items():
        for lvl, meta in levels.items():
            if meta["absent"] and meta["count"] >= VOCAB_ARM_MIN and lvl not in ("(null)",):
                absent_ge20.append((fld, lvl, meta["count"]))
    absent_ge20.sort(key=lambda x: -x[2])
    arm2_fires = len(absent_ge20) > 0
    print()
    print("- **Vocabulary arm:** %d absent levels >= %d exhibits -> **%s**."
          % (len(absent_ge20), VOCAB_ARM_MIN, "FIRES" if arm2_fires else "does NOT fire"))
    for fld, lvl, cnt in absent_ge20:
        print("    - %s=%s : %d exhibits" % (fld, lvl, cnt))
    report["vocabulary_arm_absent_ge20"] = [{"field": f, "level": l, "count": c} for f, l, c in absent_ge20]
    report["vocabulary_arm_fires"] = bool(arm2_fires)
    report["census"] = census

    # ---------------------------------------------------------------
    # TRIGGER DECISION
    # ---------------------------------------------------------------
    print()
    print("## TRIGGER DECISION")
    fired = arm1_fires or arm2_fires
    report["trigger_fired"] = bool(fired)
    print("- Expression arm (cos^2): %s" % ("FIRES" if arm1_fires else "no"))
    print("- Vocabulary arm (census): %s" % ("FIRES" if arm2_fires else "no"))
    if fired:
        print("- **REFIT WARRANTED (STEP 2/3 proceeds).** At least one arm fired.")
    else:
        print("- **NEITHER ARM FIRES -> HALT + RETURN to conductor (§8-A is the conductor's ruling).**")

    con.close()

    # machine-readable summary for conductor independent re-computation
    with open(os.path.join(OUT, "2026-07-22-legb-step1-trigger.json"), "w") as f:
        json.dump(report, f, indent=2, default=float)
    print()
    print("=== summary written: %s ===" % os.path.join(OUT, "2026-07-22-legb-step1-trigger.json"))
    return fired


if __name__ == "__main__":
    main()
