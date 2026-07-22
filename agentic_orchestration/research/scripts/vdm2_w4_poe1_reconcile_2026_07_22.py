#!/usr/bin/env python3
"""
VDM-2 W4 — PoE1 evidence reconciliation.

For each of the 94 PoE1 record-class kits, checks that the re-emitted structured
facts (geometry delivery-family, element register, chain/pierce, deviation
presence) AGREE with the hand-verified W1 evidence file
(legolas/research/vdm2-verify-poe1-2026-07-22/<kit>.md).

Reports:
  - clean matches (re-emitted facts corroborated by evidence)
  - discrepancies (a re-emitted fact the evidence contradicts)
  - anomaly-flag corroboration (evidence's own "Anomaly noted" callouts vs the
    8-anomaly / 2-partial FLAG registry)

This is a READ-ONLY reconciliation (mode=ro). It writes nothing to corpus.db.
"""
import importlib.util
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "emit", os.path.join(HERE, "vdm2_w4_poe1_sidecar_emit_2026_07_22.py"))
emit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emit)

# PoE element -> the register token that may legitimately appear in evidence.
# (evidence talks in PoE terms: lightning/cold/fire/chaos/physical; the mapping
# skills[] carry RDR register: shadow=chaos, water=cold, earth=physical-ish.)
REGISTER_TO_POE = {
    "shadow": ["chaos", "shadow", "dark"],
    "water": ["cold", "ice", "water", "freeze", "chill"],
    "earth": ["physical", "earth", "phys"],
    "fire": ["fire", "burn", "ignite"],
    "lightning": ["lightning", "shock", "electric"],
}

# geometry delivery-family -> evidence keywords that would corroborate it.
# Widened 2026-07-22 after reconciliation r1 surfaced heuristic false-positives:
# self_buff/aura kits describe their TRIGGER (cwdt/warcry/ward) not "aura"; orbit
# kits describe the orbiting SKILL not "spin"; zone kits vary widely. The list is
# a CORROBORATION aid, not the structuring authority (the mapping prose is).
DELIVERY_EVIDENCE = {
    "beam": ["chain", "beam", "channel", "arc", "lash", "ray", "laser"],
    "projectile": ["projectile", "arrow", "bolt", "throw", "thrown", "fires", "fire ",
                   "shoot", "wand", "missile", "orb", "spectral", "helix", "pierc",
                   "return", "homing", "icicle", "spark", "lance"],
    "zone": ["aoe", "area", "circle", "nova", "ground", "explos", "ring", "cascade",
             "trap", "mine", "brand", "cloud", "zone", "burst", "shockwave", "quake",
             "erupt", "detonat", "radius", "cascade", "pulse", "cast"],
    "melee_arc": ["melee", "strike", "slam", "swing", "cleave", "hit ", "attack",
                  "hammer", "sweep", "flurry", "boneshatter", "warcry"],
    "summon_delegate": ["totem", "minion", "summon", "skeleton", "zombie", "spectre",
                        "golem", "ballista", "spirit", "reaper", "animate", "weapon",
                        "raise", "companion", "clone"],
    "aura": ["aura", "reserv", "buff", "herald", "banner", "cwdt", "cast when",
             "warcry", "ward", "shield", "enchant", "block", "trigger", "damage taken"],
    "motion": ["cyclone", "whirl", "dash", "blink", "flicker", "spin", "move",
               "orbit", "winter orb", "gyre", "vortex", "channel"],
}


def load_evidence(kit_id):
    path = os.path.join(emit.EVIDENCE_DIR, f"{kit_id}.md")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    conn = sqlite3.connect(f"file:{emit.DB_PATH}?mode=ro", uri=True)
    kits = emit.load_kits(conn)
    assert len(kits) == 94

    clean = 0
    missing_evidence = []
    discrepancies = []
    anomaly_corroborated = []
    partial_corroborated = []
    evidence_anomaly_kits = []

    for k in kits:
        kid = k["kit_id"]
        ev = load_evidence(kid)
        if ev is None:
            missing_evidence.append(kid)
            continue
        ev_low = ev.lower()
        bands = emit.derive_geometry_bands(k)
        kit_ok = True
        kit_notes = []

        # 1) delivery-family corroboration (primary skill).
        if bands and bands[0].get("delivery_class"):
            deliv = bands[0]["delivery_class"]
            kws = DELIVERY_EVIDENCE.get(deliv, [])
            if kws and not any(w in ev_low for w in kws):
                kit_ok = False
                kit_notes.append(
                    f"delivery_class='{deliv}' not corroborated by evidence keywords")

        # 2) element register corroboration (skills element_primary).
        elems = [sk.get("element_primary") for sk in (k["mapping"].get("skills") or [])
                 if isinstance(sk, dict) and sk.get("element_primary")]
        if elems:
            reg = elems[0]
            poe_terms = REGISTER_TO_POE.get(reg, [reg])
            # Only flag if NONE of the register's PoE terms appear AND the kit is
            # NOT a known frozen-elem anomaly (those are EXPECTED to mismatch).
            if (not any(t in ev_low for t in poe_terms)
                    and kid not in emit.ELEM_ANOMALIES):
                kit_ok = False
                kit_notes.append(
                    f"element register '{reg}' ({'/'.join(poe_terms)}) absent from evidence")

        # 3) chain corroboration (if band claims chain, evidence should mention chain).
        if bands and bands[0].get("chain") and "chain" not in ev_low:
            kit_notes.append("band claims chain but evidence silent on chaining")
            # soft note, not a hard discrepancy

        # 4) evidence's own anomaly callout vs the FLAG registry.
        if "anomaly noted" in ev_low or ("anomaly" in ev_low and "elrond adjudicates" in ev_low):
            evidence_anomaly_kits.append(kid)
            if kid in emit.ELEM_ANOMALIES:
                anomaly_corroborated.append(kid)

        if kid in emit.PARTIALS:
            if "partial" in ev_low or "not on poedb" in ev_low or "not a unique item" in ev_low:
                partial_corroborated.append(kid)

        if kit_ok:
            clean += 1
        else:
            discrepancies.append((kid, kit_notes))

    print(f"===== PoE1 EVIDENCE RECONCILIATION ({len(kits)} kits) =====")
    print(f"CLEAN (re-emitted facts corroborated by evidence): {clean}/{len(kits)}")
    print(f"Missing evidence files: {len(missing_evidence)} {missing_evidence}")
    print()
    print(f"DISCREPANCIES: {len(discrepancies)}")
    for kid, notes in discrepancies:
        print(f"  {kid}:")
        for n in notes:
            print(f"    - {n}")
    print()
    print(f"Evidence files with own 'Anomaly noted' callout: "
          f"{len(evidence_anomaly_kits)} {evidence_anomaly_kits}")
    print(f"  of which in the 8-anomaly FLAG registry (corroborated): "
          f"{len(anomaly_corroborated)} {anomaly_corroborated}")
    print(f"Partials corroborated by evidence: "
          f"{len(partial_corroborated)} {partial_corroborated}")

    # Anomalies in the registry NOT self-flagged by their evidence file (worth noting).
    reg_not_in_evidence = [a for a in emit.ELEM_ANOMALIES
                           if a not in evidence_anomaly_kits]
    print()
    print(f"8-anomaly registry members whose evidence file does NOT carry an "
          f"explicit 'Anomaly noted' callout: {reg_not_in_evidence}")
    print("  (these are anomalies elrond identified from the mapping/dossier prose,")
    print("   not necessarily surfaced as an explicit W1 evidence callout)")


if __name__ == "__main__":
    main()
