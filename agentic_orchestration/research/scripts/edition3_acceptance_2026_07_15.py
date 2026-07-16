#!/usr/bin/env python3
"""
edition3_acceptance_2026_07_15.py — Edition-III acceptance suite (audit-grade self-verification).

Run AFTER build_atlas_json_edition3.py. Reads atlas-edition3.json + atlas-edition2.json +
atlas.json (Edition-I) + corpus.db. Fail-loud on any criterion. This is elrond's audit-grade
self-verification before gandalf's audit + Matt's Edition-III freeze ratification.

Criteria (Edition-III commission §4 + §5):
  E3-1  register v1.3: denominators BYTE-IDENTICAL to v1.2 (lattice unchanged), independently re-derived.
  E3-2  FIT-layer frozen: basis + 506 point coords + tombstones byte-identical to Edition-I.
  E3-3  Edition-II PRESERVED (never overwritten): atlas-edition2.json is still an Edition-II artifact.
  E3-4  lattice-integrity: depth_sum == 767,411,820 (unchanged); lit census reproduces from corpus keys.
  E3-5  pull-slice-lit-integrity: every pull kit intrinsic-evidence; ZERO mcd-lit.
  E3-6  census population: corpus 709; active 628; occupied meso 202 (>193); pull-lit 4 (>2).
  E3-7  edition stamp + register v1.3 ref + anti-stale greps (anti-422445240 carries forward).
  E3-8  frozen-basis gate: the +65 census rows are NOT active fit points (still 469); they light ghosts only.
"""

import json
import os
import sys
import sqlite3
import itertools

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import ghost_field_edition3 as gf3

ATLAS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "curated", "atlas"))
E3_JSON = os.path.join(ATLAS_DIR, "atlas-edition3.json")
E2_JSON = os.path.join(ATLAS_DIR, "atlas-edition2.json")
E1_JSON = os.path.join(ATLAS_DIR, "atlas.json")
DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append((name, detail))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def main():
    with open(E3_JSON) as f:
        a = json.load(f)
    with open(E2_JSON) as f:
        e2 = json.load(f)
    with open(E1_JSON) as f:
        e1 = json.load(f)
    g = a["ghost_field"]
    d = g["denominators"]
    con = sqlite3.connect(DB)

    print("== EDITION-III ACCEPTANCE SUITE ==\n")

    # ---- E3-1: register v1.3 denominators byte-identical to v1.2 (independently re-derived) ----
    card = dict(movement=3, delivery=7, amp=3, geometry=21, treatment=3, function=11, defense=5,
                economy=7, proxy=3, rng=4, tempo=3, commit=3, activation=2, dependency=3)
    raw = 1
    for v in card.values():
        raw *= v
    deliveries = ['PROJECTILE', 'ORBITAL', 'NOVA', 'ZONE', 'BEAM', 'MELEE', 'SUMMON']
    dpr = sum(1 for dd in deliveries for p in ['solo', 'light', 'heavy'] for r in ['melee', 'mid', 'ranged', 'dual']
              if not (dd == 'SUMMON' and p == 'solo') and not (dd == 'MELEE' and r == 'ranged')
              and not (dd == 'PROJECTILE' and r == 'melee'))
    coherent_tf = 3 * 11 - 2
    indep = 3 * 3 * 21 * 5 * 7 * 3 * 3 * 2 * 3
    post_logical = coherent_tf * dpr * indep
    post_redlaw = post_logical * (21 * 3 - 2 * 2) // (21 * 3)
    check("E3-1 exact raw naive == 990186120", raw == 990186120, str(raw))
    check("E3-1 exact post-logical == 819439740", post_logical == 819439740, str(post_logical))
    check("E3-1 exact post-red-law == 767411820 (== emitted)",
          post_redlaw == 767411820 == d["exact_post_red_law"], f"{post_redlaw} vs {d['exact_post_red_law']}")
    check("E3-1 meso feasible == 11160 (unchanged)", d["meso_feasible"] == 11160, str(d["meso_feasible"]))
    check("E3-1 meso sealed == 1314 (L1 756 + L2 558)",
          d["meso_sealed"] == 1314 and d["meso_sealed_L1"] == 756 and d["meso_sealed_L2"] == 558,
          f"{d['meso_sealed']} = {d['meso_sealed_L1']}+{d['meso_sealed_L2']}")
    check("E3-1 pull slice 1080+54 (all L2), 0 new laws, HALT=False",
          g["pull_slice"]["meso_feasible"] == 1080 and g["pull_slice"]["meso_sealed"] == 54
          and g["pull_slice"]["new_law_needed"] == 0 and g["pull_slice"]["halt"] is False)

    # ---- E3-2: fit-layer frozen (basis + 506 point coords + tombstones byte-identical to E1) ----
    check("E3-2 basis byte-identical to Edition-I", a["basis"] == e1["basis"])
    e1p = {p["kit_id"]: p for p in e1["points"]}
    e3p = {p["kit_id"]: p for p in a["points"]}
    same_points = (set(e1p) == set(e3p) and all(
        e1p[k]["x"] == e3p[k]["x"] and e1p[k]["y"] == e3p[k]["y"] for k in e1p))
    check("E3-2 all 506 point coords byte-identical", same_points, f"{len(e3p)} points")
    same_tomb = all(e1p[k].get("death_class") == e3p[k].get("death_class")
                    for k in e1p if e1p[k].get("supplementary"))
    check("E3-2 tombstone death_class strings byte-identical", same_tomb)

    # ---- E3-3: Edition-II PRESERVED (never overwritten) ----
    check("E3-3 atlas-edition2.json still an Edition-II artifact",
          e2.get("edition") == 2 and e2.get("atlas_version") == "Edition-II")
    check("E3-3 Edition-III is a SEPARATE artifact (edition==3, own file)",
          a.get("edition") == 3 and a.get("emitted_alongside", "").startswith("atlas-edition2"))

    # ---- E3-4: lattice-integrity (depth Σ unchanged; lit reproduces) ----
    check("E3-4 depth_sum == exact denominator 767411820 (unchanged vs E2)",
          g["depth_sum_check"] == 767411820, str(g["depth_sum_check"]))
    lit_counts, unmapped, would_seal, lit_pull = gf3.lit_map(con)
    n_lit_recompute = sum(1 for combo in itertools.product(*[gf3.REG[c] for c in gf3.CORE])
                          if gf3.meso_feasible(dict(zip(gf3.CORE, combo)))
                          and lit_counts.get(tuple(combo), 0) >= 1)
    check("E3-4 lit census reproduces from corpus keys", n_lit_recompute == g["lit_cells"],
          f"recompute {n_lit_recompute} == emitted {g['lit_cells']}")

    # ---- E3-5: pull-slice-lit-integrity (every pull kit intrinsic; ZERO mcd-lit) ----
    rows = con.execute("SELECT k.kit_id, k.cell_key FROM canon_engine_key k JOIN canon_corpus c "
                       "ON c.kit_id=k.kit_id WHERE k.row_class='combat-kit' AND c.negative=0 "
                       "AND k.cell_key IS NOT NULL").fetchall()
    pull_kits = [kid for kid, ck in rows if ck.split("|")[gf3.CK_IDX["function"]] == "pull"]
    mcd_pull = [k for k in pull_kits if k.startswith("mcd-")]
    intrinsic = {
        "d3-zbarb", "di-cyclone-monk-pvp", "la-destroyer-vortex-gravity", "la-destroyer-gravity-impact",
        "la-destroyer-gravity-force", "d4-spiritborn-vortex", "d3-wizard-black-hole",
        "di-cyclone-strike-monk-base", "la-destroyer-rage-hammer", "la-destroyer-gravity-training",
    }
    check("E3-5 all pull kits intrinsic-evidence (10)", set(pull_kits) == intrinsic,
          f"{len(pull_kits)} pull kits: {sorted(pull_kits)}")
    check("E3-5 ZERO mcd-lit pull cells", len(mcd_pull) == 0, str(mcd_pull))

    # ---- E3-6: census population ----
    n_corpus = con.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    n_active = con.execute("SELECT COUNT(*) FROM canon_engine_key k JOIN canon_corpus c "
                           "ON c.kit_id=k.kit_id WHERE k.row_class='combat-kit' AND c.negative=0 "
                           "AND k.cell_key IS NOT NULL").fetchone()[0]
    check("E3-6 corpus == 709", n_corpus == 709, str(n_corpus))
    check("E3-6 active combat-kit == 628", n_active == 628, str(n_active))
    check("E3-6 occupied meso cells == 202 (> Edition-II 193)", g["lit_cells"] == 202, str(g["lit_cells"]))
    check("E3-6 pull-lit meso cells == 4 (> Edition-II 2)", g["pull_slice"]["lit_cells"] == 4,
          str(g["pull_slice"]["lit_cells"]))

    # ---- E3-7: edition stamp + register ref + anti-stale ----
    check("E3-7 Edition-III stamp present", a["atlas_version"] == "Edition-III" and a["edition"] == 3)
    check("E3-7 register v1.3 ref present", a["register_ref"] == "feasibility-cuts-register-v1.3"
          and g["register_ref"] == "feasibility-cuts-register-v1.3")
    s = json.dumps(a)
    check("E3-7 anti-422445240 (never appears)", "422445240" not in s)

    # ---- E3-8: frozen-basis gate (65 census rows are NOT active fit points) ----
    check("E3-8 active fit points still 469 (census rows light ghosts only, not fit)",
          a["counts"]["active"] == 469, str(a["counts"]["active"]))
    check("E3-8 total fit points still 506", a["counts"]["total"] == 506, str(a["counts"]["total"]))

    con.close()

    print(f"\n== RESULT: {len(PASS)} PASS / {len(FAIL)} FAIL ==")
    if FAIL:
        print("FAILURES:")
        for n, det in FAIL:
            print(f"  - {n}: {det}")
        sys.exit(1)
    print("ALL EDITION-III ACCEPTANCE CRITERIA PASS.")


if __name__ == "__main__":
    main()
