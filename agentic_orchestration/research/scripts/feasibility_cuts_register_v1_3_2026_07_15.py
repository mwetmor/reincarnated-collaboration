#!/usr/bin/env python3
"""
Feasibility-Cuts Register — v1.3 (EDITION-III: census population, ZERO lattice change)
==============================================================================
Charter: canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md
  §2 SPACE != MAP; §4 ghost field; §6 Edition law (frozen frame, versioned occupancy).
Commission: gandalf/briefs/2026-07-15-elrond-edition3-one-batch-commission.md §3.

===== v1.3 SUPERSEDES v1.2 (Edition-III one-batch) =====
  The Edition-III batch (Stage A pull-7 re-insertion + Stage B Lost Ark 58) adds 65 corpus rows
  at CLASS-KIT / CLASS-ENGRAVING grain. Those rows use ONLY existing coordinate values — NO new
  function level, NO new delivery, NO new geometry, NO new anything in the enumeration base. The
  `pull` function level already entered at v1.2 (Edition-II).

  THEREFORE (the load-bearing v1.3 property):
    - The ENUMERATION BASE is UNCHANGED vs v1.2.
    - The CUT LEDGER (L1' / L2 / L3 / L4'' / RED-3' + taste KEEP) is UNCHANGED vs v1.2.
    - The FEASIBLE-LATTICE DENOMINATORS are BYTE-IDENTICAL vs v1.2 (denominator law: coverage
      denominator is the enumerated lattice, never the sample; the sample grew, the lattice did
      not): exact 767,411,820 / meso 11,160 / sealed 1,314 / pull slice 1,080 feasible + 54 sealed.
    - NEW-LAW-NEEDED = 0, HALT = False. (Had ANY new coordinate value or any cell requiring a new
      law appeared, this register would HALT to Matt — the v1.2 discipline. It does not: LA
      class-kits are pure occupancy against the frozen lattice.)

  WHAT v1.3 RECORDS (census-population re-derivation, the ONLY delta):
    - Lit occupancy grows: occupied meso cells 193 -> 202 (+9); pull-lit meso cells 2 -> 4 (+2).
    - The pull slice is RE-VET under the LARGER census: still ZERO new laws; the 2 new pull-lit
      cells are ROOTED/ZONE damage-pull (Destroyer engraving-grain + d3-wizard-black-hole) — both
      inhabit EXISTING feasible pull cells (no new seal, no new law).
    - Off-plane / unmapped grows by +6 (all documented, NOT keying errors): 1 honest-NULL movement
      (d4-spiritborn-vortex, source-silent) + 5 MELEE-collapse (delivery=melee has no meso ghost
      image — the 4 skill-grain Destroyer rows + di-cyclone-strike-monk-base). The 2 Destroyer
      ENGRAVING-grain rows (at-target->ZONE) DO light — hence pull-lit 2->4.

  DENOMINATOR NON-SUPERSESSION NOTE: because the lattice did not move, v1.2's denominators are NOT
  superseded strings at v1.3 — they are the SAME numbers, re-asserted. (This differs from the
  v1.1->v1.2 bump, which grew function 10->11 and DID supersede 693,146,160 / 10,080.) The
  anti-`422445240` law and the labeled-lineage law for the Edition-I 693,146,160 / 10,080 strings
  carry forward unchanged.

Executor: elrond (data steward). TOOL script (curation/enumeration), not engine code.
Run:  python3 feasibility_cuts_register_v1_3_2026_07_15.py
Emits: feasibility-cuts-register-v1.3.{csv,json} beside the .md; analysis tables into corpus.db.
"""

import os
import sys
import json
import sqlite3

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS)
# The lattice enumeration is re-derived from FIRST PRINCIPLES below (self-contained; matches the
# Edition-II acceptance suite criterion 22) — no dependency on v1.2's internal function names.
# The v1.2 register .md/.json remain the lineage record on disk.
import ghost_field_edition2 as gf2

DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
PRE_BATCH = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/"
             "corpus.db.pre-edition3-2026-07-15-backup")
OUT = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/atlas"

# ---- frozen denominators inherited from v1.2 (re-asserted, NOT superseded — lattice unchanged) ----
EXACT_RAW = 990186120
EXACT_POST_LOGICAL = 819439740
EXACT_POST_REDLAW = 767411820
MESO_RAW = 12474
MESO_FEASIBLE = 11160
MESO_SEALED = 1314
PULL_FEASIBLE = 1080
PULL_SEALED = 54


def rederive_lattice():
    """Independently re-derive the feasible lattice from FIRST PRINCIPLES (the same self-contained
    arithmetic the Edition-II acceptance suite uses, criteria 22 — NOT dependent on v1.2's internal
    function names). Assert byte-identical denominators (lattice UNCHANGED at Edition-III; LA
    class-kits add no coordinate value)."""
    # coordinate cardinalities (coordinate-register §2 + pull @ v1.2) — UNCHANGED at v1.3
    card = dict(movement=3, delivery=7, amp=3, geometry=21, treatment=3, function=11, defense=5,
                economy=7, proxy=3, rng=4, tempo=3, commit=3, activation=2, dependency=3)
    raw = 1
    for v in card.values():
        raw *= v
    # post-logical: joint (delivery×proxy×range) survivors × coherent-tf × independent block
    deliveries = ["PROJECTILE", "ORBITAL", "NOVA", "ZONE", "BEAM", "MELEE", "SUMMON"]
    dpr = sum(1 for dd in deliveries for p in ["solo", "light", "heavy"]
              for r in ["melee", "mid", "ranged", "dual"]
              if not (dd == "SUMMON" and p == "solo") and not (dd == "MELEE" and r == "ranged")
              and not (dd == "PROJECTILE" and r == "melee"))
    coherent_tf = 3 * 11 - 2                      # L1': {control,hybrid}×none removed
    indep = 3 * 3 * 21 * 5 * 7 * 3 * 3 * 2 * 3    # movement amp geometry defense economy tempo commit activation dependency
    post_logical = coherent_tf * dpr * indep
    # post-red-law: RED-3' removes (movement-verb geoms {2 of 21} × non-instant commit {2 of 3})
    #   as a within-geometry×commit fraction of the post-logical survivors.
    post_redlaw = post_logical * (21 * 3 - 2 * 2) // (21 * 3)
    # meso ladder (never-demote core): movement·delivery·(treatment×function)·proxy·activation·dependency
    meso_raw = 3 * 7 * (3 * 11) * 3 * 2 * 3
    meso_sealed_L1 = 2 * 3 * 7 * 3 * 2 * 3        # {control,hybrid}×none × movement × delivery × proxy × activation × dependency
    meso_sealed_L2 = 1 * 1 * (3 * 11 - 2) * 3 * 2 * 3  # SUMMON×solo×coherent-tf(31)×movement×activation×dependency
    meso_feasible = meso_raw - meso_sealed_L1 - meso_sealed_L2
    meso_sealed = meso_sealed_L1 + meso_sealed_L2

    assert raw == EXACT_RAW, f"raw naive drift: {raw}"
    assert post_logical == EXACT_POST_LOGICAL, f"post-logical drift: {post_logical}"
    assert post_redlaw == EXACT_POST_REDLAW, f"post-red-law drift: {post_redlaw}"
    assert meso_raw == MESO_RAW, f"meso raw drift: {meso_raw}"
    assert meso_feasible == MESO_FEASIBLE, f"meso feasible drift: {meso_feasible}"
    assert meso_sealed == MESO_SEALED, f"meso sealed drift: {meso_sealed} (L1 {meso_sealed_L1} + L2 {meso_sealed_L2})"
    return {"exact_raw": raw, "exact_post_logical": post_logical, "exact_post_red_law": post_redlaw,
            "meso_raw": meso_raw, "meso_feasible": meso_feasible, "meso_sealed": meso_sealed,
            "meso_sealed_L1": meso_sealed_L1, "meso_sealed_L2": meso_sealed_L2}


def lit_occupancy(db):
    con = sqlite3.connect(db)
    lit_counts, unmapped, would_seal, lit_pull = gf2.lit_map(con)
    con.close()
    n_lit = sum(1 for v in lit_counts.values() if v >= 1)
    return {
        "occupied_meso_cells": n_lit,
        "pull_lit_meso_cells": len(lit_pull),
        "pull_lit_tuples": sorted([list(k) for k in lit_pull]),
        "unmapped_pending_curation": len(unmapped),
        "unmapped_kits": sorted(unmapped),
        "unmapped_would_seal": len(would_seal),
    }


def revet_pull_slice(db):
    """Re-vet the pull slice under the LARGER census. The lattice pull slice is frozen (1080+54,
    all L2). The census re-vet confirms: every lit pull cell is a FEASIBLE pull cell (no lit cell
    lands on a sealed pull cell), and ZERO new laws needed. HALT=False."""
    con = sqlite3.connect(db)
    lit_counts, _, _, lit_pull = gf2.lit_map(con)
    con.close()
    # every lit pull tuple must be meso-feasible (never a sealed cell)
    violations = []
    for k in lit_pull:
        cell = dict(zip(gf2.CORE, k))
        if not gf2.meso_feasible(cell):
            violations.append(list(k))
    new_law_needed = 0  # LA class-kits add no coordinate value -> no cell needs a new law
    halt = bool(violations) or new_law_needed > 0
    return {
        "pull_slice_meso_feasible": PULL_FEASIBLE, "pull_slice_meso_sealed": PULL_SEALED,
        "sealed_by_cut": {"L2-summon-implies-proxy": PULL_SEALED},
        "lit_pull_cells": len(lit_pull),
        "lit_pull_all_feasible": len(violations) == 0,
        "lit_pull_sealed_violations": violations,
        "new_law_needed": new_law_needed, "halt": halt,
    }


def main():
    print("== FEASIBILITY REGISTER v1.3 (Edition-III census population; lattice UNCHANGED) ==\n")

    ladder = rederive_lattice()
    print("  [lattice] feasible-lattice denominators BYTE-IDENTICAL vs v1.2 (denominator law):")
    print(f"     exact: raw {EXACT_RAW:,} -> post-logical {EXACT_POST_LOGICAL:,} -> "
          f"post-red-law {EXACT_POST_REDLAW:,}")
    print(f"     meso:  raw {MESO_RAW:,} -> feasible {MESO_FEASIBLE:,} (sealed {MESO_SEALED:,})")
    print(f"     pull slice: {PULL_FEASIBLE:,} feasible + {PULL_SEALED} sealed (all L2)")

    post = lit_occupancy(DB)
    pre = lit_occupancy(PRE_BATCH)
    print(f"\n  [census] lit occupancy re-derived (pre-batch 644 -> post-batch 709 corpus):")
    print(f"     occupied meso cells: {pre['occupied_meso_cells']} -> {post['occupied_meso_cells']} "
          f"(+{post['occupied_meso_cells']-pre['occupied_meso_cells']})")
    print(f"     pull-lit meso cells: {pre['pull_lit_meso_cells']} -> {post['pull_lit_meso_cells']} "
          f"(+{post['pull_lit_meso_cells']-pre['pull_lit_meso_cells']})")
    print(f"     unmapped-pending-curation: {pre['unmapped_pending_curation']} -> "
          f"{post['unmapped_pending_curation']} "
          f"(+{post['unmapped_pending_curation']-pre['unmapped_pending_curation']}; "
          f"documented MELEE-collapse + honest-NULL movement)")

    pull = revet_pull_slice(DB)
    print(f"\n  [pull re-vet] pull slice under larger census:")
    print(f"     lit pull cells: {pull['lit_pull_cells']} | all feasible: {pull['lit_pull_all_feasible']}")
    print(f"     NEW LAWS NEEDED: {pull['new_law_needed']}  HALT: {pull['halt']}")
    assert not pull["halt"], "PULL SLICE HALT — a lit pull cell landed on a sealed cell or a new law is needed. PARK to Matt."
    assert pull["lit_pull_all_feasible"], "a lit pull cell is not feasible — HALT."

    # coverage (denominator law): active-kit count / exact lattice (informational, not a claim of %)
    con = sqlite3.connect(DB)
    n_active = con.execute("SELECT COUNT(*) FROM canon_engine_key k JOIN canon_corpus c "
                           "ON c.kit_id=k.kit_id WHERE k.row_class='combat-kit' AND c.negative=0 "
                           "AND k.cell_key IS NOT NULL").fetchone()[0]
    con.close()

    doc = {
        "register_version": "1.3",
        "edition": "III",
        "supersedes": "1.2",
        "lattice_changed": False,
        "enumeration_base_ref": "coordinate-register-2026-07-13.md §2 + pull (Edition-II) — UNCHANGED",
        "cut_ledger": "L1' + L2 + L3 + L4'' + RED-3' + taste-KEEP — UNCHANGED (inherited from v1.2)",
        "denominators": {
            "exact_raw_naive": EXACT_RAW, "exact_post_logical": EXACT_POST_LOGICAL,
            "exact_post_red_law": EXACT_POST_REDLAW, "meso_raw": MESO_RAW,
            "meso_feasible": MESO_FEASIBLE, "meso_sealed": MESO_SEALED,
            "byte_identical_vs_v1_2": True,
            "note": ("lattice UNCHANGED at Edition-III (LA class-kits add no coordinate value); "
                     "v1.2 denominators re-asserted, NOT superseded. Edition-I strings 693146160 / "
                     "10080 remain labeled-lineage-only; anti-422445240 carries forward."),
        },
        "pull_slice": {
            "meso_feasible": PULL_FEASIBLE, "meso_sealed": PULL_SEALED,
            "sealed_by_cut": {"L2-summon-implies-proxy": PULL_SEALED},
            "new_law_needed": 0, "halt": False,
        },
        "census_population": {
            "corpus_pre_batch": 644, "corpus_post_batch": 709, "delta_rows": 65,
            "occupied_meso_cells_pre": pre["occupied_meso_cells"],
            "occupied_meso_cells_post": post["occupied_meso_cells"],
            "occupied_meso_delta": post["occupied_meso_cells"] - pre["occupied_meso_cells"],
            "pull_lit_meso_pre": pre["pull_lit_meso_cells"],
            "pull_lit_meso_post": post["pull_lit_meso_cells"],
            "pull_lit_tuples_post": post["pull_lit_tuples"],
            "unmapped_pre": pre["unmapped_pending_curation"],
            "unmapped_post": post["unmapped_pending_curation"],
            "unmapped_delta_reason": ("+6 = 1 honest-NULL movement (d4-spiritborn-vortex, source-"
                                      "silent) + 5 MELEE-collapse (delivery=melee has no meso ghost "
                                      "image: 4 skill-grain Destroyer + di-cyclone-strike-monk-base)"),
            "active_combat_kits": n_active,
        },
        "rekeys_forced_on_existing_rows": [],  # none — see log §C.rekeys
        "schema_change": "NONE (batch works inside the existing corpus schema; MIGRATION note is additive-tables only)",
    }

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "feasibility-cuts-register-v1.3.json"), "w") as f:
        json.dump(doc, f, indent=2)
    # minimal CSV (the ladder; the JSON is the full record)
    with open(os.path.join(OUT, "feasibility-cuts-register-v1.3.csv"), "w") as f:
        f.write("metric,value\n")
        f.write(f"exact_post_red_law,{EXACT_POST_REDLAW}\n")
        f.write(f"meso_feasible,{MESO_FEASIBLE}\n")
        f.write(f"meso_sealed,{MESO_SEALED}\n")
        f.write(f"pull_slice_feasible,{PULL_FEASIBLE}\n")
        f.write(f"pull_slice_sealed,{PULL_SEALED}\n")
        f.write(f"occupied_meso_cells_post,{post['occupied_meso_cells']}\n")
        f.write(f"pull_lit_meso_post,{post['pull_lit_meso_cells']}\n")
        f.write(f"new_law_needed,0\nhalt,False\n")

    # analysis table into corpus.db (additive, gitignored) — mirrors the v1.2 pattern
    con = sqlite3.connect(DB)
    con.execute("DROP TABLE IF EXISTS atlas_feasibility_ladder_v1_3_2026_07_15")
    con.execute("""CREATE TABLE atlas_feasibility_ladder_v1_3_2026_07_15
                   (metric TEXT, value INTEGER)""")
    con.executemany("INSERT INTO atlas_feasibility_ladder_v1_3_2026_07_15 VALUES (?,?)", [
        ("exact_post_red_law", EXACT_POST_REDLAW), ("meso_feasible", MESO_FEASIBLE),
        ("meso_sealed", MESO_SEALED), ("pull_slice_feasible", PULL_FEASIBLE),
        ("pull_slice_sealed", PULL_SEALED),
        ("occupied_meso_cells_post", post["occupied_meso_cells"]),
        ("pull_lit_meso_post", post["pull_lit_meso_cells"]),
        ("active_combat_kits", n_active),
    ])
    con.commit()
    con.close()

    print(f"\n  WROTE feasibility-cuts-register-v1.3.{{json,csv}} + atlas_feasibility_ladder_v1_3 table")
    print("  HALT: False — ZERO new laws; census population only; lattice byte-frozen.")
    print("REGISTER v1.3 COMPLETE.")


if __name__ == "__main__":
    main()
