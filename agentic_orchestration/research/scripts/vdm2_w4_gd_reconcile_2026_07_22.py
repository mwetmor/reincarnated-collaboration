#!/usr/bin/env python3
"""
VDM-2 W4 — GD INTERNAL-CONSISTENCY reconciliation (RB-5, LOAD-BEARING).

GD has NO W1 hand-verified evidence substrate (only PoE1 got a legolas W1
evidence tranche; W5 will be GD's systematic external check). So this reconcile
checks the emitted VDM-2 side-cars against the EXISTING VDM-1 corpus fields for
these 41 kits — an internal cross-consistency test, not an external one. It
still catches emitter bugs (the PoE1 reconcile caught 2; the D2 reconcile caught
0 but surfaced the poison-register split; GD's value = confirmation + the
acid-register-split catch — the GD substrate was surveyed BEFORE the emitter, so
the crosswalk tables are one-pass by construction).

Three independent VDM-1 fields are cross-checked against the emitted structure:

  1) geo_raw (canon_corpus) — the VDM-1 BC-axis geometry code, an INDEPENDENT
     kit-LEVEL geometry derivation. The emitted skill_geometry_band.delivery_class
     (a PER-SKILL delivery family from geometry_value) should be consistent with
     the delivery-family implied by geo_raw. A COARSE kit code legitimately spans
     MANY per-skill delivery families (a 'small-AOE' kit can have a melee primary,
     a totem primary, a bolt primary, a zone primary) — so the crosswalk flags
     ONLY a HARD contradiction (self/aura-only code emitting a payload-projectile,
     or a pure-projectile code emitting a self-aura). Everything else is grain-gap-
     consistent (the emitter maps skill0.geometry_value faithfully — the
     structuring authority — not the coarse BC code). Same rule as D2 (60/60).

  2) elem_raw (canon_corpus) — the FROZEN element field. The emitted H2 element-
     register recognition_hook (from skills[].element_primary) should be
     reconcilable to elem_raw via the RDR register crosswalk, which derives from
     the FROZEN court column (the W3b court authority: aether->lightning;
     physical/pierce/bleed->physical(earth); acid/vitality/chaos->chaos-poison
     (shadow); mixed->NULL). A register that contradicts the court-licensed set
     with NO documented crosswalk = a flag. The GD anomaly kits + the acid-split
     kits are EXPECTED to mismatch (excluded / W5-routed).

  3) verify_ledger mechanics/identity verdict (per kit) — if the kit's mechanics
     verdict is CONTRADICTED/UNSUPPORTED, an emitted CLOSE/EXACT-grade clean band
     with no EI deviation is worth noting (structure asserts more than VERIFY).

Also: for the 6 EI-deviation (GAPPED-terminal) kits, confirms each opened exactly
one docket (structural closure), and confirms kit_door_arg stayed empty (V-21).

READ-ONLY (mode=ro). Writes nothing to corpus.db.

USAGE
  python3 vdm2_w4_gd_reconcile_2026_07_22.py
"""
import importlib.util
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "emit", os.path.join(HERE, "vdm2_w4_gd_sidecar_emit_2026_07_22.py"))
emit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emit)

# geo_raw (VDM-1 BC-axis kit code) -> the per-skill delivery_class families it is
# consistent with. Same permissive-families rule that reached 60/60 on D2: a
# coarse kit-level code spans every payload-delivery family; flag ONLY the hard
# self/aura-vs-projectile contradiction. GD's observed pairs (surveyed) all fall
# inside these sets.
GEO_RAW_TO_DELIVERY = {
    "large-AOE": {"zone", "aura", "beam", "projectile", "summon_delegate",
                  "motion", "melee_arc"},
    "small-AOE": {"zone", "aura", "beam", "projectile", "summon_delegate",
                  "motion", "melee_arc"},
    "multi-spawn": {"projectile", "summon_delegate", "motion", "zone", "melee_arc"},
    # 'single' (single-target) spans direct-hit families: bolt, melee, beam,
    # motion, single-summon primaries (one Reap-spirit / one Skeleton as skill0),
    # AND the pet-core aura primary (pet-conjurer's mappable player-layer skill0
    # is a self-buff = aura; the pet delivery is deferred).
    "single": {"projectile", "melee_arc", "beam", "motion", "summon_delegate",
               "zone", "aura"},
    "single-target": {"projectile", "melee_arc", "beam", "motion",
                      "summon_delegate", "zone", "aura"},
    "chain": {"beam", "projectile", "summon_delegate", "zone", "aura", "motion"},
    "melee": {"melee_arc", "motion"},
    "cone": {"zone", "projectile"},
    "self": {"aura", "zone", "motion"},
    "line": {"projectile", "beam", "zone"},
    "point-blank": {"zone", "melee_arc", "aura", "motion"},
    "orbit": {"motion", "zone"},
    "beam": {"beam", "projectile"},
    "aura": {"aura", "zone"},
    "ground": {"zone"},
}

# elem_raw -> the RDR element register(s) that reconcile cleanly, DERIVED from the
# frozen court crosswalk (W3b MIGRATION §court). Multi-element GD kits legitimately
# carry a skill0 register that differs from the headline elem_raw (a grain gap,
# handled by the footprint allowance in the check logic, not by widening this).
ELEM_RAW_TO_REGISTER = {
    "fire": {"fire"},
    "cold": {"water"},
    "lightning": {"lightning"},
    "aether": {"lightning"},            # court=lightning (aether->lightning)
    # court=chaos-poison -> shadow. BUT the frozen mapping sets element_primary=
    # 'earth' for GD 'acid' on dee/righteous-fervor — a acid->earth register
    # choice that DISAGREES with the chaos-poison court. Recognized here as the
    # known-anomaly crosswalk (earth allowed alongside shadow), ROUTED TO W5.
    "acid": {"shadow", "earth"},
    "vitality": {"shadow"},             # court=chaos-poison
    "chaos": {"shadow"},                # court=chaos-poison
    "physical": {"earth"},              # court=physical
    "pierce": {"earth"},                # court=physical (pierce->physical rider)
    "bleed": {"earth"},                 # court=physical (bleed->physical rider)
    "mixed(fire/cold/lightning)": set(),  # court=NULL; no single register (anomaly)
}

# GD acid kits whose skill.element_primary='earth' disagrees with court=
# chaos-poison — a frozen-mapping register inconsistency to surface for W5
# (parallels the D2 poison->earth split).
ACID_EARTH_W5 = {"gd-dee-witch-hunter", "gd-righteous-fervor-dervish"}


def norm_geo_raw(g):
    if not g:
        return None
    g = g.strip().lower()
    if "small" in g and "aoe" in g:
        return "small-AOE"
    if "large" in g and "aoe" in g:
        return "large-AOE"
    if "aoe" in g:
        return "large-AOE"
    if g.startswith("multi"):
        return "multi-spawn"
    if g == "single" or "single" in g:
        return "single"
    if "point" in g and "blank" in g:
        return "point-blank"
    return g


def main():
    conn = sqlite3.connect(f"file:{emit.DB_PATH}?mode=ro", uri=True)
    kits = emit.load_kits(conn)
    assert len(kits) == 41

    corpus = {}
    for kid, geo_raw, elem_raw, atlas in conn.execute(
            "SELECT kit_id, geo_raw, elem_raw, atlas_coords FROM canon_corpus "
            "WHERE game='gd' AND corpus_class='record'"):
        corpus[kid] = dict(geo_raw=geo_raw, elem_raw=elem_raw, atlas=atlas)

    verdict = {}
    for kid, fam, v in conn.execute(
            "SELECT kit_id, claim_family, verdict FROM verify_ledger "
            "WHERE kit_id LIKE 'gd-%' AND claim_family IN ('mechanics','identity')"):
        rank = {"CONTRADICTED": 3, "SOURCE_NOT_FOUND": 2, "UNSUPPORTED": 1,
                "CONFIRMED": 0}.get(v, 0)
        cur = verdict.get(kid)
        if cur is None or rank > cur[1]:
            verdict[kid] = (v, rank)

    clean = 0
    flagged = []
    adjudicated = []
    anomaly_expected = []
    acid_earth_w5 = []

    for k in kits:
        kid = k["kit_id"]
        c = corpus.get(kid, {})
        bands = emit.derive_geometry_bands(k)
        hooks = emit.derive_hooks(k, bands)
        notes = []
        kit_ok = True

        # --- CHECK 1: emitted delivery_class vs independent geo_raw code ---
        # use the FIRST delivery-bearing band (GD pet-core kits' skill0 has no
        # geometry; the mappable delivery is on a later ordinal — the emitter's
        # H1/acceptance already use the first delivery-bearing band).
        b0 = None
        for b in bands:
            if b.get("delivery_class"):
                b0 = b
                break
        if b0 is not None:
            deliv = b0["delivery_class"]
            gr = norm_geo_raw(c.get("geo_raw"))
            allowed = GEO_RAW_TO_DELIVERY.get(gr) if gr else None
            if allowed is not None and deliv not in allowed:
                kit_ok = False
                notes.append(
                    f"delivery_class='{deliv}' (from geometry_value) NOT consistent "
                    f"with geo_raw='{c.get('geo_raw')}' (allows {sorted(allowed)})")

        # --- CHECK 2: emitted element register (H2) vs frozen elem_raw ---
        reg = None
        for h in hooks:
            if h["hook_type"] == "register":
                reg = h["expressed_by"].split(":", 1)[-1]
                break
        if reg:
            er = (c.get("elem_raw") or "").strip().lower()
            allowed_reg = ELEM_RAW_TO_REGISTER.get(er)
            if kid in emit.ELEM_ANOMALIES:
                if allowed_reg is not None and reg not in allowed_reg:
                    anomaly_expected.append(
                        f"{kid}: register '{reg}' vs elem_raw '{er}' (W5-flagged anomaly; expected)")
            elif allowed_reg is not None and reg not in allowed_reg:
                # register the frozen elem_raw does not license, on a NON-anomaly
                # kit — classify: documented crosswalk, multi-element grain-gap, or
                # a genuine flag.
                kit_elems = set()
                for sk in (k["mapping"].get("skills") or []):
                    if isinstance(sk, dict):
                        if sk.get("element_primary"):
                            kit_elems.add(sk["element_primary"])
                        if sk.get("element_secondary"):
                            kit_elems.add(sk["element_secondary"])
                if reg in kit_elems:
                    # multi-element kit: H2 reports skill0's element — a REAL
                    # element the kit carries (verified in its footprint) that
                    # differs from the headline elem_raw. Faithful to mapping_json
                    # — a grain gap, not a bug (aether-headline/fire-or-shadow-
                    # skill: callidors/krieg; chaos-headline/fire-skill: doom-bolt;
                    # bleed-headline/shadow-vitality-skill: wendigo).
                    adjudicated.append(
                        f"{kid}: H2 register '{reg}' is a real kit element (skill0's "
                        f"primary); elem_raw '{er}' is the headline "
                        f"(multi-element grain gap, faithful; kit elements={sorted(kit_elems)})")
                else:
                    kit_ok = False
                    notes.append(
                        f"element register '{reg}' not licensed by elem_raw '{er}' "
                        f"(allows {sorted(allowed_reg) if allowed_reg else 'none'})")

        # W5 route: acid->earth frozen-mapping register inconsistency (court=
        # chaos-poison vs skill.element=earth). Surfaced regardless of the CLEAN
        # verdict, so W5 sees it. Not an emitter bug — a frozen-data flag.
        if kid in ACID_EARTH_W5:
            regs = {sk.get("element_primary")
                    for sk in (k["mapping"].get("skills") or [])
                    if isinstance(sk, dict) and sk.get("element_primary")}
            if "earth" in regs:
                acid_earth_w5.append(
                    f"{kid}: skill.element_primary='earth' but elem_raw='acid' / "
                    f"court='chaos-poison' — frozen-mapping register inconsistency (W5)")

        # --- CHECK 3: mechanics verdict vs emitted grade/deviation ---
        v = verdict.get(kid)
        if v and v[0] in ("CONTRADICTED", "SOURCE_NOT_FOUND"):
            dev = emit.derive_deviations(k)
            has_ei = any(d["deviation_class"] == "engine_inexpressible" for d in dev)
            if k["grade"] in ("CLOSE", "EXACT") and not has_ei:
                notes.append(
                    f"verify mechanics verdict={v[0]} but emitted grade={k['grade']} "
                    f"with no EI deviation (structure asserts more than VERIFY)")
                # soft note — does not flip kit_ok (grade is frozen VDM-1, not ours)

        if kit_ok:
            clean += 1
        else:
            flagged.append((kid, notes))

    print(f"===== GD INTERNAL-CONSISTENCY RECONCILIATION ({len(kits)} kits) =====")
    print("(no W1 external evidence for GD — cross-checks emitted side-cars against")
    print(" the independent VDM-1 fields geo_raw / elem_raw / verify_ledger verdict)")
    print()
    print(f"CLEAN (emitted structure consistent with VDM-1 fields): {clean}/{len(kits)}")
    print()
    print(f"FLAGGED (real internal inconsistency — candidate emitter/data bug): {len(flagged)}")
    for kid, notes in flagged:
        print(f"  {kid}:")
        for n in notes:
            print(f"    - {n}")
    print()
    print(f"ADJUDICATED (mismatch explained by a documented crosswalk, NOT a bug): {len(adjudicated)}")
    for a in adjudicated:
        print(f"  - {a}")
    print()
    print(f"ANOMALY-EXPECTED (elem mismatch on the W5-flagged elem anomalies, expected): {len(anomaly_expected)}")
    for a in anomaly_expected:
        print(f"  - {a}")
    print()
    print(f"W5-ROUTED (acid->earth frozen-mapping register inconsistency, NOT a bug): {len(acid_earth_w5)}")
    for a in acid_earth_w5:
        print(f"  - {a}")
    print()

    # --- structural closure checks ---
    ei_kits = [k["kit_id"] for k in kits
               if any(d["deviation_class"] == "engine_inexpressible"
                      for d in emit.derive_deviations(k))]
    dockets = conn.execute(
        "SELECT source_kit_id, COUNT(*) FROM mechanic_gap_docket "
        "WHERE docket_family='vdm2-w4-gd' GROUP BY source_kit_id").fetchall()
    docket_by_kit = {kid: n for kid, n in dockets}
    print("STRUCTURAL CLOSURE:")
    print(f"  EI-deviation kits: {len(ei_kits)}")
    print(f"  deviation-lane dockets opened (family=vdm2-w4-gd): {sum(docket_by_kit.values())} "
          f"across {len(docket_by_kit)} kits")
    orphan_ei = [kid for kid in ei_kits if kid not in docket_by_kit]
    orphan_docket = [kid for kid in docket_by_kit if kid not in ei_kits]
    print(f"  EI kits with NO docket (orphans, must be []): {orphan_ei}")
    print(f"  dockets with NO EI kit (orphans, must be []): {orphan_docket}")
    kda = conn.execute("SELECT COUNT(*) FROM kit_door_arg WHERE kit_id LIKE 'gd-%'").fetchone()[0]
    print(f"  kit_door_arg rows for GD (V-21 carve-out, must be 0): {kda}")

    # --- red-assert routing closure ---
    red = conn.execute(
        "SELECT COUNT(*), SUM(CASE WHEN routed_docket_id IS NOT NULL THEN 1 ELSE 0 END) "
        "FROM kit_acceptance_assert WHERE kit_id LIKE 'gd-%' AND last_result='red'").fetchone()
    print(f"  red acceptance asserts: {red[0]}, routed to docket: {red[1] if red[1] else 0} "
          f"(every red must route)")


if __name__ == "__main__":
    main()
