#!/usr/bin/env python3
"""
magic-anchor caster sim_props authoring pass — elrond curation, 2026-06-14
===========================================================================

Lifts the 102 `gandalf-authored-magic-anchor-*` caster-weapon rows in
reincarnated-loadout/data/telemetry.db from knowledge-only reserve
(v1_scope=0, ZERO weapon_sim_props, ZERO weapon_type_family, quality_tier null)
to selectable weapon-as-identity roots.

Authority : Matt-authorized 2026-06-14 (via gandalf) — Pattern-B.
Spec      : agentic_orchestration/gandalf/notes/2026-06-14-magic-anchor-simprops-design-spec.md
Precedent : agentic_orchestration/elrond/research/substrate-enrichment-2026-05-27/ (same mechanics).

This script is IDEMPOTENT-SAFE in intent: it INSERT-OR-REPLACEs the
weapon_sim_props row for each of the 102 weapon_ids, and UPDATEs quality on the
knowledge rows. A pre-run backup is the rollback path (see MIGRATION.md).

Per-row family/template/element resolution is encoded EXPLICITLY below
(ROW_PLAN), grounded in:
  - proxy_attribute_class (the family-resolution INPUT)
  - the existing v1_scope_composition_trace.matching_policy already on each row
    (option_beta_caster_attribute_level => pure caster; option_c_cross_attribute
     + option_alpha_martial_5tuple => hybrid) — independently corroborates the
    8-row hybrid set.
  - canonical_name + description register (the arcane-vs-faith discriminator for
    the 81 INT_or_WIS rows).

All template VALUES are the proven sibling-row conventions pulled live from the
pool 2026-06-14 (Flutterby Rod / Mace of Nova Scotia / vajra / Censer of
Righteousness exemplars), NOT invented.
"""

import sqlite3
import json
import sys
import datetime

DB = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
VERIFIED_DATE = "2026-06-14"
SIMPROPS_TAG = "gandalf_magic_anchor_simprops_v1_2026_06_14"

# Pool-modal base_physical_damage_l50 conventions (live-verified 2026-06-14):
BASE_PHYS_CASTER = 50.22   # caster-arcane (235/235) + caster-faith (modal 161/228)
BASE_PHYS_HYBRID_STR = 75.0  # hybrid/STR (all 41 rows)

# ---------------------------------------------------------------------------
# The six archetype sim-profile templates (spec § 3), grounded in real pool
# exemplars verified live 2026-06-14. Each returns the column tuple.
# Fields: range_min, range_max, atk_speed, charge_s, hits, aoe,
#         amp_min, amp_max, default_spellmod, family, primary_stat
# ---------------------------------------------------------------------------
TEMPLATES = {
    # A — Arcane single-target (staff/rod/wand/focus/sceptre). Exemplar: Flutterby Rod.
    "A": dict(rmin=5.0,  rmax=18.0, spd=1.5, charge=0.0, aoe=0.0, amin=0.84, amax=2.4, spellmod=82, fam="caster-arcane", stat="INT"),
    # A-short — spell-glove / gauntlet (close-mid hand-caster). Template A at short end.
    "A_short": dict(rmin=2.5, rmax=10.0, spd=1.5, charge=0.0, aoe=0.0, amin=0.84, amax=2.4, spellmod=82, fam="caster-arcane", stat="INT"),
    # A-ext — gun-caster identity-forced, extended range (spec § 5). range_max up to 22.
    "A_ext": dict(rmin=8.0, rmax=22.0, spd=1.5, charge=0.0, aoe=0.0, amin=0.84, amax=2.4, spellmod=82, fam="caster-arcane", stat="INT"),
    # B — Arcane area (projector/diffuser/emitter/orb). Censer-pattern, arcane-coded.
    "B": dict(rmin=5.0, rmax=18.0, spd=0.7, charge=1.2, aoe=3.5, amin=0.48, amax=3.0, spellmod=68, fam="caster-arcane", stat="INT"),
    # C — Faith melee channel (reliquary-sword/brand/faith-mace). Exemplar: Mace of Nova Scotia.
    "C": dict(rmin=0.5, rmax=2.5, spd=1.5, charge=0.0, aoe=0.0, amin=0.84, amax=2.4, spellmod=62, fam="caster-faith", stat="WIS"),
    # D — Faith ritual implement (censer/distaff/pestle/sigil/broom/vajra/sceptre-regalia). Exemplar: vajra.
    "D": dict(rmin=2.5, rmax=7.0, spd=0.7, charge=1.2, aoe=3.5, amin=0.48, amax=3.0, spellmod=85, fam="caster-faith", stat="WIS"),
    # E — Faith long-range area (high censer / banner / oriflamme / tug). Exemplar: Censer of Righteousness.
    "E": dict(rmin=5.0, rmax=18.0, spd=0.7, charge=1.2, aoe=3.5, amin=0.48, amax=3.0, spellmod=50, fam="caster-faith", stat="WIS"),
    # F — Martial-faith hybrid (STR-coded named sword + faith/element overlay). hybrid/STR.
    #     atk_speed 1.5 to match live pool hybrid/STR convention (Eldritch Knight's Longsword,
    #     Gram, etc.) — DEVIATION from spec § 3's listed 1.2, taken for pool coherence (noted in MIGRATION).
    "F": dict(rmin=0.5, rmax=2.5, spd=1.5, charge=0.0, aoe=0.0, amin=0.84, amax=2.4, spellmod=45, fam="hybrid", stat="STR"),
}

# ---------------------------------------------------------------------------
# PER-ROW PLAN — the authoritative resolution. id -> (template, element, flag)
#   element : weapon element for element_affinity_modifiers_json {"<el>":15};
#             None -> {} (non-elemental / abstract / register-only).
#   flag    : optional note appended to sim_viability_notes (gun-caster, faith-register-tension, etc.)
# Hybrid rows (template F) carry secondary_stat='WIS' (the faith/divine overlay), matching the
# pool's STR+WIS paladin/holy-sword convention.
# ---------------------------------------------------------------------------
ROW_PLAN = {
    # ===================== ANCIENT (24) — deity-elemental foci =====================
    # All deity-anchored ELEMENTAL/COSMIC foci => caster-arcane/INT (template A), per spec § 2
    # default lean ("they wield element/cosmos, not devotion"), EXCEPT the 2 explicit WIS rows
    # (Gaia, Ra) => caster-faith, and Brand of Surt (STR_or_WIS sword) => hybrid/F.
    226088: ("A", "fire",      None),   # Agni-Astra Staff (Vedic fire-deity missile-staff)
    226089: ("F", "fire",      "named_legendary_sword_faith_overlay"),  # Brand of Surt (Norse fire-jötunn SWORD; Mjolnir/Gungnir STR parallel) -> hybrid/STR
    226090: ("A", "fire",      None),   # Xiuhcoatl Fire-Serpent Wand (Aztec fire-serpent)
    226091: ("A", "fire",      None),   # Hephaestus' Forge-Spark Staff (Greek forge-fire)
    226092: ("A", "water",     None),   # Varuna's Pasha-Rod (Vedic water-deity)
    226093: ("A", "water",     None),   # Tlaloc Rain-Conch Staff (Aztec rain-deity)
    226094: ("A", "water",     None),   # Manannán's Tide-Wand (Irish sea-deity)
    226095: ("A", "water",     None),   # Poseidon Aquamancer's Trident-Focus (explicit caster-class variant)
    226096: ("A", "earth",     None),   # Prithvi-Bhumi Staff (Vedic earth-mother)
    226097: ("D", "earth",     None),   # Gaia's Loam-Sceptre (WIS; Greek earth-mother sceptre/regalia) -> caster-faith
    226098: ("A", "earth",     None),   # Geb Earthmother Wand (Egyptian earth-deity)
    226099: ("A", "wind",      None),   # Stribog's Gale-Stave (Slavic wind-deity)
    226100: ("A", "wind",      None),   # Aeolus' Tempest-Pipes (Greek wind-keeper)
    226101: ("A", "wind",      None),   # Shu Skyholder Staff (Egyptian air/sky-deity)
    226102: ("A", "lightning", None),   # Perun's Stormaxe Focus (Slavic thunder-deity)
    226103: ("A", "lightning", None),   # Raijin Drum-Mallet Rod (Shinto thunder-deity)
    226104: ("A", "lightning", None),   # Tlaloc Bolt-Conch Staff (lightning-primary variant)
    226105: ("D", "holy",      None),   # Ra Solar-Disc Sceptre (WIS; Egyptian sun-deity divine-regalia sceptre) -> caster-faith
    226106: ("A", "holy",      None),   # Quetzalcoatl Plumed-Serpent Staff (dawn-deity holy-radiance; elemental-cosmic -> arcane)
    226107: ("A", "holy",      None),   # Khakkhara Pilgrim-Staff (Buddhist ringed-staff; Bodhisattva radiance — arcane-cosmic lean)
    226108: ("A", "shadow",    None),   # Hades' Bident Focus (Greek underworld-deity)
    226109: ("A", "shadow",    None),   # Anubis Embalmer's Wand (Egyptian mortuary-deity)
    226110: ("A", "shadow",    None),   # Yama's Danda-Rod (Vedic death-deity)
    226111: ("A", "shadow",    None),   # Kali Skull-Garland Staff (Hindu death-mother)

    # ===================== MEDIEVAL (29) =====================
    # Arcane (alchemist/witch/grimoire) -> A/B; faith (crusader-censer/reliquary/saint/banner-of-faith)
    # -> D/E/C; named-legendary STR/STR_or_WIS swords -> hybrid/F.
    226112: ("F", "fire",      "named_legendary_sword_faith_overlay"),  # Brand of Roland (Carolingian paladin's fire-SWORD) -> hybrid/STR
    226113: ("D", "fire",      None),   # Witch's Brimstone Censer (witch-fire ritual censer) -> faith-ritual
    226114: ("A", "fire",      None),   # Alchemist's Athanor-Rod (alchemical furnace-rod; arcane)
    226115: ("F", "fire",      "reliquary_sword_faith_overlay"),  # Crusader Reliquary Brand of San Pietro (STR; reliquary-SWORD, Pentecostal-fire) -> hybrid/STR
    226116: ("F", "water",     "named_legendary_sword_faith_overlay"),  # Joyeuse Aqua-Veil (Charlemagne's STR-tier-S SWORD, water-caster rebalance) -> hybrid/STR
    226117: ("D", "water",     None),   # Bran's Cauldron Ladle (Welsh cauldron-of-rebirth ritual implement) -> faith-ritual
    226118: ("D", "water",     None),   # Hag's Tide-Distaff (folk-magic distaff ritual) -> faith-ritual
    226119: ("A", "water",     None),   # Alchemist's Mercurial Flask-Focus (alchemical water-coded; arcane)
    226120: ("F", "earth",     "named_legendary_sword_faith_overlay"),  # Durendal Stone-Cleaver (Roland's SWORD, earth-caster rebalance) -> hybrid/STR
    226121: ("A", "earth",     None),   # Witch-Sabbath Stone-Circle Wand (witch wand; arcane-elemental)
    226122: ("D", "earth",     None),   # Geomancer's Sigil-Pestle (geomantic sigil/pestle ritual) -> faith-ritual
    226123: ("A", "wind",      None),   # Aeolian Harp of the Troubadour (wind-played harp-focus; arcane-elemental)
    226124: ("D", "wind",      None),   # Witch-Storm Broom-Stave (witch broom ritual wind-implement) -> faith-ritual
    226125: ("E", None,        None),   # Banner of the Steppe-Khan (Sülde Tug — spirit-banner standard, long projection) -> faith-area
    226126: ("A", "wind",      None),   # Alchemist's Bellows-Focus (alchemical wind/bellows; arcane)
    226127: ("F", "lightning", "named_legendary_sword_faith_overlay"),  # Hauteclère Stormbrand (Olivier's SWORD, lightning-caster rebalance) -> hybrid/STR
    226128: ("E", "lightning", None),   # Crusader Storm-Ward Censer (apotropaic storm-ward censer, long projection) -> faith-area
    226129: ("A", "lightning", None),   # Witch-Storm Lodestone Rod (lodestone storm-rod; arcane-elemental)
    226130: ("F", "lightning", "named_legendary_sword_faith_overlay"),  # Skofnung Spark-Sword (Norse saga-SWORD; Mjolnir/Gungnir STR parallel) -> hybrid/STR
    226131: ("F", "holy",      "reliquary_sword_faith_overlay"),  # Curtana Reliquary-Sword of Mercy (STR; English coronation regalia SWORD) -> hybrid/STR
    226132: ("D", "holy",      None),   # Khakkhara of St. Christopher (Christian pilgrim-staff; devotional saint-attribution) -> faith-ritual
    226133: ("D", "holy",      None),   # Sceptre of the Three Kings (Magi reliquary-sceptre; WIS) -> faith-ritual/regalia
    226134: ("E", "holy",      None),   # Oriflamme of Saint-Denis (Capetian royal war-banner; long projection) -> faith-area
    226135: ("D", "shadow",    None),   # Grimoire Athame of Solomon (Solomonic ritual-dagger/athame) -> faith-ritual (grimoire-conjuration register)
    226136: ("B", "shadow",    None),   # Picatrix Mirror-Focus (astral-magical mirror-focus, area-divination) -> arcane-area
    226137: ("A", "shadow",    None),   # Sefer HaRazim Necromancer's Quill-Rod (Hebrew grimoire necromancy quill-rod; arcane)
    226138: ("D", "shadow",    None),   # Seiðstafr of the Völva (Norse seeress seidr-staff ritual implement) -> faith-ritual
    226139: ("A", "shadow",    None),   # Plague-Doctor's Bone-Staff (plague-doctor staff; arcane-shadow)
    226140: ("D", "shadow",    None),   # Inquisitor's Iron Maiden Reliquary (Inquisition reliquary ritual-implement) -> faith-ritual

    # ===================== MODERN (49) — sci-fi tech-casters =====================
    # Almost all -> caster-arcane/INT. Gloves/gauntlets -> A_short. Projector/diffuser/emitter
    # area-vessels -> B. The 5 gun-casters -> A_ext + gun_caster_identity_forced. The 3 WIS
    # sceptres -> caster-faith/D (regalia register; flagged register-tension).
    226141: ("A", "lightning", None),   # Plasma Lance Focus (plasma; lightning-primary w/ fire flex)
    226142: ("A_ext", "fire",  "gun_caster_identity_forced"),  # Thermal Channeler Carbine-PISTOL (gun-caster) -> arcane/INT ext-range
    226143: ("A", "fire",      None),   # Fusion Cell Staff
    226144: ("A_short", "fire", None),  # Combustion Coil GLOVE -> A-short
    226145: ("B", "fire",      None),   # Pyroclastic PROJECTOR (area-vessel) -> arcane-area
    226146: ("A", "fire",      None),   # Magnesium Flare Caster
    226147: ("A", "fire",      None),   # Tactical Incendiary Channeler
    226148: ("A", "water",     None),   # Cryogenic Projector Lance (lance form -> single-target despite 'projector')
    226149: ("A", "water",     None),   # Hydraulic Pressure Caster
    226150: ("A", "water",     None),   # Hydro Cavitation Rod
    226151: ("A", "water",     None),   # Aquajet Focus Pistol (focus-pistol; arcane focus)
    226152: ("B", "water",     None),   # Cryo Mist DIFFUSER (area-vessel) -> arcane-area
    226153: ("A", "water",     None),   # Hydrostatic Channeler Staff
    226154: ("A", "earth",     None),   # Seismic Hammer Channeler
    226155: ("A", "earth",     None),   # Tectonic Resonance Rod
    226156: ("A", "earth",     None),   # Mass Driver Focus
    226157: ("A_short", "earth", None), # Geodynamic Pulse GLOVE -> A-short
    226158: ("A", "earth",     None),   # Concussion Lattice Staff
    226159: ("B", "earth",     None),   # Tremor Wave PROJECTOR (area-vessel) -> arcane-area
    226160: ("A", "wind",      None),   # Sonic Emitter Lance (lance form -> single-target)
    226161: ("B", "wind",      None),   # Shockwave PROJECTOR Rod (area-vessel) -> arcane-area
    226162: ("A", "wind",      None),   # Acoustic Pressure Caster
    226163: ("A_short", "wind", None),  # Subsonic Diffuser GLOVE -> A-short (glove form wins over diffuser)
    226164: ("A", "wind",      None),   # Ultrasonic Resonance Staff
    226165: ("A", "wind",      None),   # Concussive Air Channeler
    226166: ("A", "wind",      None),   # Doppler Disruption Focus
    226167: ("A", "lightning", None),   # Tesla Coil Staff
    226168: ("A_ext", "lightning", "gun_caster_identity_forced"),  # Coilgun Caster PISTOL (gun-caster) -> arcane ext-range
    226169: ("A_short", "lightning", None),  # Voltage Surge GLOVE -> A-short
    226170: ("A", "lightning", None),   # Flash-Discharge Focus
    226171: ("A_ext", "lightning", "gun_caster_identity_forced"),  # Ion Pulse CARBINE-Caster (gun-caster) -> arcane ext-range
    226172: ("A", "lightning", None),   # Plasma-Arc Lance
    226173: ("A_ext", "lightning", "gun_caster_identity_forced"),  # Railgun Caster ROD (railgun gun-caster) -> arcane ext-range
    226174: ("D", "lightning", "wis_caster_register_tension_scifi"),  # EMP Channeler SCEPTRE (WIS; sci-fi regalia-sceptre) -> caster-faith/D, register-tension flagged
    226175: ("A_short", "lightning", None),  # Static-Discharge GAUNTLET -> A-short
    226176: ("A", "holy",      None),   # Photon Projector Staff (staff form -> single-target despite 'projector')
    226177: ("A", "holy",      None),   # Laser Focus Lance
    226178: ("D", "holy",      "wis_caster_register_tension_scifi"),  # Prism Array SCEPTRE (WIS; sci-fi regalia-sceptre) -> caster-faith/D, register-tension flagged
    226179: ("A_short", "holy", None),  # Light-Amplification GAUNTLET -> A-short
    226180: ("A", "holy",      None),   # Stellar Concentrator Rod
    226181: ("B", "holy",      None),   # Solar Coronal Beam-EMITTER (area-vessel) -> arcane-area
    226182: ("B", "holy",      None),   # Radiant Emitter Channeler (emitter area-vessel) -> arcane-area
    226183: ("A_ext", "shadow", "gun_caster_identity_forced"),  # Antimatter Channeler RIFLE-Caster (gun-caster) -> arcane ext-range
    226184: ("A", "shadow",    None),   # Singularity Generator Focus
    226185: ("A", "shadow",    None),   # Dark-Energy Emitter Rod (rod form -> single-target)
    226186: ("A", "shadow",    None),   # Void Projector Lance (lance form -> single-target)
    226187: ("A_short", "shadow", None),  # Null-Field GAUNTLET -> A-short
    226188: ("D", "shadow",    "wis_caster_register_tension_scifi"),  # Blackhole Containment SCEPTRE (WIS; sci-fi regalia-sceptre) -> caster-faith/D, register-tension flagged
    226189: ("B", "shadow",    None),   # Dark-Matter DIFFUSER Staff (diffuser area-vessel) -> arcane-area
}

# ---------------------------------------------------------------------------
# Quality scoring (spec § 6 acceptance #3: quality_tier non-null on all 102).
# Pool tier thresholds on quality_composite_score (live-verified 2026-06-14):
#   C: 0.10-0.330 | B: 0.330-0.479 | A: 0.479-0.62 | S: special (named-myth-correlated)
# Discipline call (elrond): these are gandalf-authored high-coherence rows but the
# pool's Pattern-6 named-bearer pipeline has NOT run on them. Rather than mass-promote
# the 59 named_mythological_match rows to S (which would distort the rare S tier; S is
# only 1214/whole pool), cap at A for the named-anchor rows and B for the rest. Gun-caster
# soft-spot rows held at B (still selectable, honest mid-tier). This sits them as
# strong-but-not-legendary content, matching gandalf's "excellent/coherent/mostly strong"
# review without inflating the apex tier.
# ---------------------------------------------------------------------------
SCORE_A = 0.52   # lands in A band (0.479-0.62)
SCORE_B = 0.43   # lands in B band (0.330-0.479)


def tier_for_score(s: float) -> str:
    if s >= 0.479:
        return "A"
    if s >= 0.330:
        return "B"
    if s >= 0.10:
        return "C"
    return "C"


def main(commit: bool):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Pull the 102 rows: id, name, proxy_attribute_class, named_myth_match, existing trace
    cur.execute("""
        SELECT id, canonical_name, proxy_attribute_class, named_mythological_match,
               v1_scope_composition_trace
        FROM weapon_knowledge_entries
        WHERE source_library LIKE 'gandalf-authored-magic-anchor%'
        ORDER BY id
    """)
    rows = cur.fetchall()
    assert len(rows) == 102, f"expected 102 rows, got {len(rows)}"

    plan_ids = set(ROW_PLAN.keys())
    db_ids = {r[0] for r in rows}
    missing = db_ids - plan_ids
    extra = plan_ids - db_ids
    assert not missing, f"DB rows with no plan entry: {sorted(missing)}"
    assert not extra, f"plan entries with no DB row: {sorted(extra)}"

    fam_counts = {"caster-arcane": 0, "caster-faith": 0, "hybrid": 0}
    flag_counts = {}
    gun_casters = []
    template_counts = {}

    for (wid, name, pac, myth_match, trace_json) in rows:
        template_key, element, flag = ROW_PLAN[wid]
        t = TEMPLATES[template_key]
        fam = t["fam"]
        stat = t["stat"]
        fam_counts[fam] += 1
        template_counts[template_key] = template_counts.get(template_key, 0) + 1

        # secondary_stat: 'none' for pure casters; 'WIS' faith-overlay for hybrid/STR (template F).
        secondary = "WIS" if fam == "hybrid" else "none"

        # base_physical_damage_l50 per family-modal pool convention
        base_phys = BASE_PHYS_HYBRID_STR if fam == "hybrid" else BASE_PHYS_CASTER

        # element_affinity_modifiers_json: {"<el>":15} if elemental, else {}
        elem_json = json.dumps({element: 15}) if element else "{}"

        # sim_viability_notes: template letter + tag + any flag
        note_parts = [f"template={template_key}", f"family={fam}", SIMPROPS_TAG]
        if flag:
            note_parts.append(flag)
            flag_counts[flag] = flag_counts.get(flag, 0) + 1
            if flag == "gun_caster_identity_forced":
                gun_casters.append((wid, name))
        notes = "; ".join(note_parts)

        # INSERT OR REPLACE the weapon_sim_props row
        cur.execute("""
            INSERT OR REPLACE INTO weapon_sim_props
                (weapon_id, range_min_units, range_max_units, base_attack_speed,
                 charge_time_s, hits_per_attack, aoe_radius_units,
                 primary_stat, secondary_stat, damage_amplitude_min, damage_amplitude_max,
                 sim_viable, sim_viability_notes, sim_verified_date,
                 base_physical_damage_l50, spell_damage_modifier_pct,
                 element_affinity_modifiers_json, weapon_type_family)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            wid, t["rmin"], t["rmax"], t["spd"],
            t["charge"], 1, t["aoe"],
            stat, secondary, t["amin"], t["amax"],
            1, notes, VERIFIED_DATE,
            base_phys, float(t["spellmod"]),
            elem_json, fam,
        ))

        # Quality: A for named_mythological_match anchors, B otherwise.
        has_myth = myth_match is not None and str(myth_match).strip() != ""
        score = SCORE_A if has_myth else SCORE_B
        tier = tier_for_score(score)

        # Preserve existing composition_trace; append simprops authoring marker.
        try:
            trace = json.loads(trace_json) if trace_json else {}
        except (json.JSONDecodeError, TypeError):
            trace = {}
        trace["magic_anchor_simprops_v1_2026_06_14"] = True
        trace["simprops_template"] = template_key
        trace["simprops_family"] = fam

        cur.execute("""
            UPDATE weapon_knowledge_entries
            SET quality_composite_score = ?, quality_tier = ?,
                v1_scope_composition_trace = ?
            WHERE id = ?
        """, (score, tier, json.dumps(trace), wid))

    print("=== Resolution summary (dry-run pre-commit) ===")
    print(f"Total rows planned: {sum(fam_counts.values())}")
    print(f"Family split: {fam_counts}")
    print(f"Template distribution: {dict(sorted(template_counts.items()))}")
    print(f"Flags: {flag_counts}")
    print(f"Gun-casters ({len(gun_casters)}): {[g[1] for g in gun_casters]}")

    if commit:
        conn.commit()
        print("\n=== COMMITTED ===")
    else:
        conn.rollback()
        print("\n=== DRY RUN — rolled back (pass --commit to apply) ===")
    conn.close()


if __name__ == "__main__":
    main(commit="--commit" in sys.argv)
