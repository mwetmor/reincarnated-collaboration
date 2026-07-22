#!/usr/bin/env python3
"""
VDM-2 W4 — D2 INTERNAL-CONSISTENCY reconciliation (RB-5, LOAD-BEARING).

D2 has NO W1 hand-verified evidence substrate (only PoE1 got a legolas W1
evidence tranche; W5 will be D2's systematic external check). So this reconcile
checks the emitted VDM-2 side-cars against the EXISTING VDM-1 corpus fields for
these 60 kits — an internal cross-consistency test, not an external one. It still
catches emitter bugs (the PoE1 reconcile caught 2 real ones on PoE1).

Three independent VDM-1 fields are cross-checked against the emitted structure:

  1) geo_raw (canon_corpus) — the VDM-1 BC-axis geometry code, an INDEPENDENT
     geometry derivation from mapping_json.skills[].geometry_value. The emitted
     skill_geometry_band.delivery_class (derived from geometry_value) should be
     consistent with the delivery-family implied by geo_raw. Two independent
     geometry encodings disagreeing = a candidate emitter/data bug.

  2) elem_raw (canon_corpus) — the FROZEN element field. The emitted H2
     element-register recognition_hook (derived from skills[].element_primary)
     should be reconcilable to elem_raw via the RDR register crosswalk. A
     register that contradicts elem_raw with NO documented crosswalk = a flag.
     (The 6 W5-flagged elem anomalies are EXPECTED to mismatch — excluded.)

  3) verify_ledger mechanics/identity verdict (per kit) — if the kit's mechanics
     verdict is CONTRADICTED/UNSUPPORTED, an emitted CLOSE/EXACT-grade clean band
     with no deviation is worth noting (structure asserts more than VERIFY did).

Also: for the 13 EI-deviation kits, confirms each opened exactly one docket
(structural closure), and confirms kit_door_arg stayed empty (V-21 carve-out).

READ-ONLY (mode=ro). Writes nothing to corpus.db.

USAGE
  python3 vdm2_w4_d2_reconcile_2026_07_22.py
"""
import importlib.util
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "emit", os.path.join(HERE, "vdm2_w4_d2_sidecar_emit_2026_07_22.py"))
emit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emit)

# geo_raw (VDM-1 BC-axis code) -> the delivery_class families it is consistent
# with. geo_raw is a COARSE, kit-LEVEL BC-axis geometry code (the whole kit's
# damage-geometry archetype); delivery_class is a PER-SKILL delivery family. A
# single coarse code legitimately spans MANY per-skill delivery families — a
# 'small-AOE' kit can have a melee primary (Zeal), a whirlwind primary (WW), a
# bolt primary (Fire Bolt), or a trap primary (Sentry). Reconcile-r1 confirmed
# (2026-07-22) that the kit-level vs skill-level grain gap makes a tight
# per-code allow-set produce false positives. The crosswalk therefore flags ONLY
# a HARD contradiction: a self/aura-only code emitting a payload-projectile, or
# a pure-projectile code emitting a self-aura. Everything else is grain-gap-
# consistent (the emitter maps skill0.geometry_value faithfully; that is the
# structuring authority, not the coarse BC code).
GEO_RAW_TO_DELIVERY = {
    # coarse-AOE codes span every delivery family (melee/motion/projectile/
    # summon/zone/aura all legitimately produce a small-or-large AoE footprint)
    "large-AOE": {"zone", "aura", "beam", "projectile", "summon_delegate",
                  "motion", "melee_arc"},
    "small-AOE": {"zone", "aura", "beam", "projectile", "summon_delegate",
                  "motion", "melee_arc"},
    "multi-spawn": {"projectile", "summon_delegate", "motion", "zone", "melee_arc"},
    # 'single' (single-target) spans direct-hit families: bolt, melee, beam,
    # motion, AND single-summon primaries (one Golem / one Hydra as skill0)
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

# elem_raw -> the RDR element register(s) that reconcile cleanly. NOTE this is a
# HEADLINE-element check; multi-element D2 kits legitimately carry a skill0
# register that differs from elem_raw (e.g. a physical-headline Fishyzon whose
# skill0 Lightning Fury is 'lightning'). Those are handled by the multi-element
# allowance in the check logic, not by widening this table.
ELEM_RAW_TO_REGISTER = {
    "fire": {"fire"},
    "cold": {"water"},
    "lightning": {"lightning"},
    # D2 poison -> court=chaos-poison (shadow family) per court column. BUT the
    # frozen mapping_json sets skill.element_primary='earth' for D2 poison skills
    # (Poison Dagger/Plague Javelin/Rabies) — a poison->earth-register choice that
    # DISAGREES with the chaos-poison court. This is a genuine frozen-mapping
    # register inconsistency ROUTED TO W5 (do not fix, V-18); the check below
    # recognizes poison->earth as the known-anomaly crosswalk, not a bug.
    "poison": {"shadow", "earth"},
    "physical": {"earth", "shadow"},  # physical -> earth-nature; necro-physical -> shadow
    "magic": set(),                # element-neutral; no register expected (anomaly-flagged)
    "holy": {"lightning", "fire"},  # holy is probe fabrication; either or neutral
    "n/a": set(),                  # no-element utility kit (anomaly-flagged)
}

# D2 poison kits whose skill.element_primary='earth' disagrees with court=
# chaos-poison — a frozen-mapping register inconsistency to surface for W5.
POISON_EARTH_W5 = {"d2-daggermancer", "d2-poison-javazon", "d2-rabies-wolf",
                   "d2-poison-nova-necro"}


def norm_geo_raw(g):
    if not g:
        return None
    g = g.strip().lower()
    # collapse common variants to the coarse code keys above
    if "small" in g and "aoe" in g:
        return "small-AOE"
    if "large" in g and "aoe" in g:
        return "large-AOE"
    if "aoe" in g:
        return "large-AOE"
    if g.startswith("multi"):
        return "multi-spawn"
    if g == "single" or "single" in g:
        return "single-target"
    if "point" in g and "blank" in g:
        return "point-blank"
    return g


def main():
    conn = sqlite3.connect(f"file:{emit.DB_PATH}?mode=ro", uri=True)
    kits = emit.load_kits(conn)
    assert len(kits) == 60

    # pull the independent VDM-1 fields
    corpus = {}
    for kid, geo_raw, elem_raw, atlas in conn.execute(
            "SELECT kit_id, geo_raw, elem_raw, atlas_coords FROM canon_corpus "
            "WHERE game='d2' AND corpus_class='record'"):
        corpus[kid] = dict(geo_raw=geo_raw, elem_raw=elem_raw, atlas=atlas)

    # per-kit mechanics/identity verdict (worst verdict wins)
    verdict = {}
    for kid, fam, v in conn.execute(
            "SELECT kit_id, claim_family, verdict FROM verify_ledger "
            "WHERE kit_id LIKE 'd2-%' AND claim_family IN ('mechanics','identity')"):
        rank = {"CONTRADICTED": 3, "SOURCE_NOT_FOUND": 2, "UNSUPPORTED": 1,
                "CONFIRMED": 0}.get(v, 0)
        cur = verdict.get(kid)
        if cur is None or rank > cur[1]:
            verdict[kid] = (v, rank)

    clean = 0
    flagged = []          # (kit, [notes]) — a real internal inconsistency
    adjudicated = []      # (kit, note) — mismatch explained by documented crosswalk
    anomaly_expected = [] # elem mismatches on the 6 W5-flagged anomalies (expected)
    poison_earth_w5 = []  # poison->earth frozen-mapping register inconsistency (W5)

    for k in kits:
        kid = k["kit_id"]
        c = corpus.get(kid, {})
        bands = emit.derive_geometry_bands(k)
        hooks = emit.derive_hooks(k, bands)
        notes = []
        kit_ok = True

        # --- CHECK 1: emitted delivery_class vs independent geo_raw code ---
        if bands and bands[0].get("delivery_class"):
            deliv = bands[0]["delivery_class"]
            gr = norm_geo_raw(c.get("geo_raw"))
            allowed = GEO_RAW_TO_DELIVERY.get(gr) if gr else None
            if allowed is not None and deliv not in allowed:
                # a hard cross-geometry contradiction — candidate bug
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
                # anomaly kits are EXPECTED to mismatch — record, don't flag
                if allowed_reg is not None and reg not in allowed_reg:
                    anomaly_expected.append(
                        f"{kid}: register '{reg}' vs elem_raw '{er}' (W5-flagged anomaly; expected)")
            elif allowed_reg is not None and reg not in allowed_reg:
                # a register the frozen elem_raw does not license, on a NON-anomaly
                # kit — classify: documented crosswalk, multi-element grain-gap, or
                # a genuine flag.
                # all elements the kit actually carries (primary AND secondary,
                # across every skill) — the full element footprint of the kit
                kit_elems = set()
                for sk in (k["mapping"].get("skills") or []):
                    if isinstance(sk, dict):
                        if sk.get("element_primary"):
                            kit_elems.add(sk["element_primary"])
                        if sk.get("element_secondary"):
                            kit_elems.add(sk["element_secondary"])
                if er == "physical" and reg == "shadow":
                    adjudicated.append(
                        f"{kid}: physical->shadow register (documented necro/dark crosswalk)")
                elif reg in kit_elems:
                    # multi-element kit: H2 reports skill0's element, which is a
                    # REAL element the kit carries (verified in its skill element
                    # footprint) but differs from the headline elem_raw. Faithful
                    # to mapping_json — a grain gap, not a bug. (H2's "first non-
                    # null skill element" rule may pick a secondary-headline
                    # element on tri-element charge kits, e.g. Mosaic Sin.)
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
        # verdict, so W5 sees it. Not an emitter bug — a frozen-data flag.
        if kid in POISON_EARTH_W5:
            regs = {sk.get("element_primary")
                    for sk in (k["mapping"].get("skills") or [])
                    if isinstance(sk, dict) and sk.get("element_primary")}
            if "earth" in regs:
                poison_earth_w5.append(
                    f"{kid}: skill.element_primary='earth' but elem_raw='poison' / "
                    f"court='chaos-poison' — frozen-mapping register inconsistency (W5)")

        # --- CHECK 3: mechanics verdict vs emitted grade/deviation ---
        v = verdict.get(kid)
        if v and v[0] in ("CONTRADICTED", "SOURCE_NOT_FOUND"):
            dev = emit.derive_deviations(k)
            has_ei = any(d["deviation_class"] == "engine_inexpressible" for d in dev)
            if k["grade"] in ("CLOSE", "EXACT") and not has_ei:
                # structure asserts a clean map but VERIFY says contradicted — note
                notes.append(
                    f"verify mechanics verdict={v[0]} but emitted grade={k['grade']} "
                    f"with no EI deviation (structure asserts more than VERIFY)")
                # soft note — does not flip kit_ok (grade is frozen VDM-1, not ours)

        if kit_ok:
            clean += 1
        else:
            flagged.append((kid, notes))

    print(f"===== D2 INTERNAL-CONSISTENCY RECONCILIATION ({len(kits)} kits) =====")
    print("(no W1 external evidence for D2 — cross-checks emitted side-cars against")
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
    print(f"ANOMALY-EXPECTED (elem mismatch on the 6 W5-flagged anomalies, expected): {len(anomaly_expected)}")
    for a in anomaly_expected:
        print(f"  - {a}")
    print()
    print(f"W5-ROUTED (poison->earth frozen-mapping register inconsistency, NOT a bug): {len(poison_earth_w5)}")
    for a in poison_earth_w5:
        print(f"  - {a}")
    print()

    # --- structural closure checks ---
    ei_kits = [k["kit_id"] for k in kits
               if any(d["deviation_class"] == "engine_inexpressible"
                      for d in emit.derive_deviations(k))]
    dockets = conn.execute(
        "SELECT source_kit_id, COUNT(*) FROM mechanic_gap_docket "
        "WHERE docket_family='vdm2-w4-d2' GROUP BY source_kit_id").fetchall()
    docket_by_kit = {kid: n for kid, n in dockets}
    print("STRUCTURAL CLOSURE:")
    print(f"  EI-deviation kits: {len(ei_kits)}")
    print(f"  deviation-lane dockets opened (family=vdm2-w4-d2): {sum(docket_by_kit.values())} "
          f"across {len(docket_by_kit)} kits")
    orphan_ei = [kid for kid in ei_kits if kid not in docket_by_kit]
    orphan_docket = [kid for kid in docket_by_kit if kid not in ei_kits]
    print(f"  EI kits with NO docket (orphans, must be []): {orphan_ei}")
    print(f"  dockets with NO EI kit (orphans, must be []): {orphan_docket}")
    kda = conn.execute("SELECT COUNT(*) FROM kit_door_arg WHERE kit_id LIKE 'd2-%'").fetchone()[0]
    print(f"  kit_door_arg rows for D2 (V-21 carve-out, must be 0): {kda}")

    # --- red-assert routing closure ---
    red = conn.execute(
        "SELECT COUNT(*), SUM(CASE WHEN routed_docket_id IS NOT NULL THEN 1 ELSE 0 END) "
        "FROM kit_acceptance_assert WHERE kit_id LIKE 'd2-%' AND last_result='red'").fetchone()
    print(f"  red acceptance asserts: {red[0]}, routed to docket: {red[1]} "
          f"(every red must route)")


if __name__ == "__main__":
    main()
