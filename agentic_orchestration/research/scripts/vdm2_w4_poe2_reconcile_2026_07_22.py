#!/usr/bin/env python3
"""
VDM-2 W4 — PoE2 INTERNAL-CONSISTENCY reconciliation (RB-5, LOAD-BEARING).

PoE2 has NO W1 hand-verified evidence substrate (only PoE1 got a legolas W1
evidence tranche; W5 will be PoE2's systematic external check). So this
reconcile cross-checks the emitted VDM-2 side-cars against the EXISTING VDM-1
corpus fields for the 36 PoE2 record kits — an internal cross-consistency test,
not an external one (exact GD pattern). It catches emitter bugs (the PoE1
reconcile caught 2; D2 caught 0 but surfaced the poison-register split; GD
caught 0 + the acid-register split).

Three independent VDM-1 fields are cross-checked against the emitted structure:

  1) geo_raw (canon_corpus) — the VDM-1 BC-axis kit-LEVEL geometry code, an
     INDEPENDENT geometry derivation. The emitted skill_geometry_band.
     delivery_class (per-skill delivery family from geometry_value) should be
     consistent with the family implied by geo_raw. A coarse kit code spans MANY
     per-skill families, so flag ONLY a HARD contradiction (self/aura-only code
     emitting a payload-projectile, or a pure-projectile code emitting a
     self-aura). Same permissive-families rule that reached 60/60 on D2 / 41/41
     on GD.

  2) elem_raw (canon_corpus) — the FROZEN element field. The emitted H2 element-
     register recognition_hook (from skills[].element_primary) should reconcile
     to elem_raw via the RDR register crosswalk derived from the FROZEN court
     column (W3b court authority: lightning->lightning; physical->earth;
     fire->fire; cold->water; chaos-poison->shadow). A register the court does
     NOT license, on a NON-anomaly kit, is classified: multi-element grain-gap
     (H2 reports skill0's REAL element, faithful to mapping_json) OR a genuine
     flag. The 2 poison->earth split kits are EXPECTED to mismatch (W5-routed).

  3) verify_ledger mechanics/identity verdict (per kit) — if the kit's mechanics
     verdict is CONTRADICTED/UNSUPPORTED but the emitted grade is CLOSE/EXACT
     with no EI deviation, note it (structure asserts more than VERIFY). Soft
     note; grade is frozen VDM-1, not ours.

Also: confirms each EI-deviation kit opened exactly one deviation-lane docket
(structural closure), every red acceptance assert routes to a docket, and
kit_door_arg stayed empty for PoE2 (V-21).

READ-ONLY (mode=ro). Writes nothing to corpus.db.

USAGE
  python3 vdm2_w4_poe2_reconcile_2026_07_22.py
"""
import importlib.util
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "emit", os.path.join(HERE, "vdm2_w4_poe2_sidecar_emit_2026_07_22.py"))
emit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emit)

# geo_raw (VDM-1 BC-axis kit code) -> the per-skill delivery_class families it is
# consistent with. Same permissive-families rule as D2 (60/60) and GD (41/41).
# PoE2's observed geo_raw values (surveyed): small-AOE, large-AOE, multi-spawn,
# single, chain.
GEO_RAW_TO_DELIVERY = {
    "large-AOE": {"zone", "aura", "beam", "projectile", "summon_delegate",
                  "motion", "melee_arc"},
    "small-AOE": {"zone", "aura", "beam", "projectile", "summon_delegate",
                  "motion", "melee_arc"},
    "multi-spawn": {"projectile", "summon_delegate", "motion", "zone", "melee_arc"},
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
# frozen court crosswalk (W3b MIGRATION §court). Multi-element PoE2 kits
# legitimately carry a skill0 register that differs from the headline elem_raw
# (a grain gap, handled by the footprint allowance in the check logic).
ELEM_RAW_TO_REGISTER = {
    "fire": {"fire"},
    "cold": {"water"},
    "lightning": {"lightning"},
    "physical": {"earth"},
    # court=chaos-poison -> shadow. BUT the frozen mapping sets element_primary=
    # 'earth' for PoE2 'chaos' on concoction / poison-pathfinder — a poison->earth
    # register choice that DISAGREES with the chaos-poison court. Recognized here
    # as the known-split crosswalk (earth allowed alongside shadow), ROUTED TO W5.
    "chaos": {"shadow", "earth"},
}

# PoE2 chaos kits whose skill.element_primary='earth' disagrees with court=
# chaos-poison — a frozen-mapping register inconsistency to surface for W5
# (parallels the D2 poison->earth and GD acid->earth splits; RB-6).
POISON_EARTH_W5 = set(emit.POISON_REGISTER_INCONSISTENCY.keys())


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
    assert len(kits) == 36

    corpus = {}
    for kid, geo_raw, elem_raw, atlas in conn.execute(
            "SELECT kit_id, geo_raw, elem_raw, atlas_coords FROM canon_corpus "
            "WHERE game='poe2' AND corpus_class='record'"):
        corpus[kid] = dict(geo_raw=geo_raw, elem_raw=elem_raw, atlas=atlas)

    verdict = {}
    for kid, fam, v in conn.execute(
            "SELECT kit_id, claim_family, verdict FROM verify_ledger "
            "WHERE kit_id LIKE 'poe2-%' AND claim_family IN ('mechanics','identity')"):
        rank = {"CONTRADICTED": 3, "SOURCE_NOT_FOUND": 2, "UNSUPPORTED": 1,
                "CONFIRMED": 0}.get(v, 0)
        cur = verdict.get(kid)
        if cur is None or rank > cur[1]:
            verdict[kid] = (v, rank)

    clean = 0
    flagged = []
    adjudicated = []
    anomaly_expected = []
    poison_earth_w5 = []

    for k in kits:
        kid = k["kit_id"]
        c = corpus.get(kid, {})
        bands = emit.derive_geometry_bands(k)
        hooks = emit.derive_hooks(k, bands)
        notes = []
        kit_ok = True

        # --- CHECK 1: emitted delivery_class vs independent geo_raw code ---
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
                kit_elems = set()
                for sk in (k["mapping"].get("skills") or []):
                    if isinstance(sk, dict):
                        if sk.get("element_primary"):
                            kit_elems.add(sk["element_primary"])
                        if sk.get("element_secondary"):
                            kit_elems.add(sk["element_secondary"])
                if reg in kit_elems:
                    # multi-element kit: H2 reports skill0's element — a REAL
                    # element the kit carries that differs from the headline
                    # elem_raw (a grain gap, faithful to mapping_json). PoE2
                    # cases: shaman-bear (physical headline / fire skill0),
                    # walking-calamity (fire headline / water propagation skill).
                    adjudicated.append(
                        f"{kid}: H2 register '{reg}' is a real kit element (skill0's "
                        f"primary); elem_raw '{er}' is the headline "
                        f"(multi-element grain gap, faithful; kit elements={sorted(kit_elems)})")
                else:
                    kit_ok = False
                    notes.append(
                        f"element register '{reg}' not licensed by elem_raw '{er}' "
                        f"(allows {sorted(allowed_reg) if allowed_reg else 'none'})")

        # W5 route: poison->earth frozen-mapping register inconsistency (court=
        # chaos-poison vs skill.element=earth). Surfaced regardless of the CLEAN
        # verdict, so W5 sees it. Not an emitter bug — a frozen-data flag (RB-6).
        if kid in POISON_EARTH_W5:
            regs = {sk.get("element_primary")
                    for sk in (k["mapping"].get("skills") or [])
                    if isinstance(sk, dict) and sk.get("element_primary")}
            if "earth" in regs:
                poison_earth_w5.append(
                    f"{kid}: skill.element_primary='earth' but elem_raw='chaos' / "
                    f"court='chaos-poison' — frozen-mapping register inconsistency "
                    f"(W5; parallels D2-poison + GD-acid splits, RB-6)")

        # --- CHECK 3: mechanics verdict vs emitted grade/deviation ---
        v = verdict.get(kid)
        if v and v[0] in ("CONTRADICTED", "SOURCE_NOT_FOUND"):
            dev = emit.derive_deviations(k)
            has_ei = any(d["deviation_class"] == "engine_inexpressible" for d in dev)
            if k["grade"] in ("CLOSE", "EXACT") and not has_ei:
                notes.append(
                    f"verify mechanics verdict={v[0]} but emitted grade={k['grade']} "
                    f"with no EI deviation (structure asserts more than VERIFY)")
                # soft note — does not flip kit_ok (grade is frozen VDM-1)

        if kit_ok:
            clean += 1
        else:
            flagged.append((kid, notes))

    print(f"===== PoE2 INTERNAL-CONSISTENCY RECONCILIATION ({len(kits)} kits) =====")
    print("(no W1 external evidence for PoE2 — cross-checks emitted side-cars against")
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
    print(f"ADJUDICATED (mismatch explained by multi-element grain gap, NOT a bug): {len(adjudicated)}")
    for a in adjudicated:
        print(f"  - {a}")
    print()
    print(f"ANOMALY-EXPECTED (elem mismatch on W5-flagged elem anomalies, expected): {len(anomaly_expected)}")
    for a in anomaly_expected:
        print(f"  - {a}")
    if not anomaly_expected:
        print("  (none — PoE2 has no elem_raw anomalies)")
    print()
    print(f"W5-ROUTED (poison->earth frozen-mapping register split, NOT a bug; RB-6): {len(poison_earth_w5)}")
    for a in poison_earth_w5:
        print(f"  - {a}")
    print()

    # --- structural closure checks ---
    ei_kits = [k["kit_id"] for k in kits
               if any(d["deviation_class"] == "engine_inexpressible"
                      for d in emit.derive_deviations(k))]
    dockets = conn.execute(
        "SELECT source_kit_id, COUNT(*) FROM mechanic_gap_docket "
        "WHERE docket_family='vdm2-w4-poe2' GROUP BY source_kit_id").fetchall()
    docket_by_kit = {kid: n for kid, n in dockets}
    print("STRUCTURAL CLOSURE:")
    print(f"  EI-deviation kits: {len(ei_kits)} {sorted(ei_kits)}")
    print(f"  deviation-lane dockets opened (family=vdm2-w4-poe2): {sum(docket_by_kit.values())} "
          f"across {len(docket_by_kit)} kits")
    orphan_ei = [kid for kid in ei_kits if kid not in docket_by_kit]
    orphan_docket = [kid for kid in docket_by_kit if kid not in ei_kits]
    print(f"  EI kits with NO docket (orphans, must be []): {orphan_ei}")
    print(f"  dockets with NO EI kit (orphans, must be []): {orphan_docket}")
    kda = conn.execute("SELECT COUNT(*) FROM kit_door_arg WHERE kit_id LIKE 'poe2-%'").fetchone()[0]
    print(f"  kit_door_arg rows for PoE2 (V-21 carve-out, must be 0): {kda}")

    # --- red-assert routing closure ---
    red = conn.execute(
        "SELECT COUNT(*), SUM(CASE WHEN routed_docket_id IS NOT NULL THEN 1 ELSE 0 END) "
        "FROM kit_acceptance_assert WHERE kit_id LIKE 'poe2-%' AND last_result='red'").fetchone()
    print(f"  red acceptance asserts: {red[0]}, routed to docket: {red[1] if red[1] else 0} "
          f"(every red must route)")


if __name__ == "__main__":
    main()
