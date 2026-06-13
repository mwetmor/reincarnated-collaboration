"""Build FACTION_LOOKUP_TABLE records[] — Q10 redraw (elrond, 2026-06-13).

Q10 ruling (Matt-ratified 2026-06-12): redraw the 8 faction boundaries so all 14
lineages land non-degenerately; add ONE composite ninth faction only if
mesoamerican / sub_saharan_african / south_southeast_asian genuinely cannot be
absorbed cleanly — never absorption-by-default, never token factions.

DESIGN DECISION: a composite ninth faction (Solar Pantheon) IS needed. The three
homeless lineages are cosmologically distinct from each other AND from the existing
eight; the ruling itself rejects absorbing them (e.g. obsidian-priest -> Sunfire
Dominion). They share one real, non-token thread: divine-kingship + ancestral
pantheons + sun/serpent cosmology rendered in stone and bronze, sitting outside the
Greco-Euro-Sinitic-MENA axes. Solar Pantheon homes all three as a real faction with
mythological / high_fantasy / primal_shamanic register coherence.

LOADER CONTRACT (confirmed against rocket's identity_sampling.py, NO shape change):
  - Each record = {"lineage", "period", "register", "faction"} (4 keys).
  - Exact index on (lineage, period, register) tuple.
  - Void override fires FIRST (before records): lineage in void_lineages OR register
    in void_registers -> "Void Covenant". So void_liminal lineage + cosmic_horror /
    void_arcane registers never reach the record lookup. We therefore do NOT emit
    records for void_liminal (override-homed) nor for the two void-intercepted
    register columns (dead cells). This is intentional, not a gap.
  - Nearest-match score = register*4 + lineage*2 + period*1; we emit an EXACT record
    for every non-void cell the sampler can produce, so nearest-match fallback is
    never reached BY CONSTRUCTION. rocket's nearest-match logging stays the empirical
    proof (it should log zero systematic fallbacks).

This is a tool script (data curation), not engine code. Reproducible: re-run to
regenerate the table verbatim from the lineage->faction map below.
"""
from __future__ import annotations

import json
from pathlib import Path

TABLE_PATH = (
    Path.home()
    / "Games" / "reincarnated-engine" / "data" / "identity" / "faction_lookup_table.json"
)

# Closed enums (locked; § 4.2-4.4, mirrored from identity_sampling.py).
CULTURAL_LINEAGES = (
    "western_european_germanic", "western_european_gothic", "norse_germanic_celtic",
    "greek_roman", "middle_eastern_persian", "north_african_egyptian",
    "east_asian_chinese", "east_asian_japanese", "east_asian_korean",
    "south_southeast_asian", "mesoamerican", "sub_saharan_african",
    "pan_industrial", "void_liminal",
)
HISTORICAL_PERIODS = (
    "ancient", "medieval", "early_modern", "industrial", "contemporary",
    "mythic", "void_atemporal",
)
REGISTERS = (
    "high_fantasy", "dark_fantasy", "mythological", "grimdark", "steampunk",
    "arcane_modern", "cosmic_horror", "primal_shamanic", "void_arcane",
)

# Void override consumes these BEFORE records are read (rocket loader, derive_faction
# step 1). Exclude them so we emit no dead records.
VOID_LINEAGE = "void_liminal"
VOID_REGISTERS = {"cosmic_horror", "void_arcane"}

# Q10 REDRAWN faction homes. 8 redrawn (Void Covenant handled by override) + 1 composite
# ninth (Solar Pantheon). Faction is lineage-anchored per § 7.2 (cultural lineage is the
# primary key; period/register are secondary descriptors). Every non-void lineage has a
# real, non-degenerate home; no lineage is absorbed-by-default into a thematically wrong
# faction.
#
#   Iron Covenant      <- western_european_germanic   (Germanic/Frankish/Arthurian high fantasy)
#   Shadow Courts      <- western_european_gothic      (Gothic/Slavic/dark-fae dark fantasy)
#   Rune-Clans         <- norse_germanic_celtic        (Norse/Celtic mythic-primal)
#   Bronze Sanctum     <- greek_roman                  (Greco-Roman mythological-martial)
#   Sunfire Dominion   <- middle_eastern_persian       (MENA / Persian / Islamic-golden)
#                       + north_african_egyptian       (Egyptian shares the sun-and-sand axis;
#                                                        same cosmological register, real home
#                                                        not tie-break absorption)
#   Eternal Dynasties  <- east_asian_chinese / _japanese / _korean  (Sinitic-sphere imperial)
#   Forge Republics    <- pan_industrial               (industrial / steampunk / arcane-modern)
#   Solar Pantheon     <- mesoamerican / sub_saharan_african / south_southeast_asian
#                         (COMPOSITE NINTH — divine-kingship + ancestral pantheons + sun/serpent
#                          cosmology outside the Euro-Sinitic-MENA axes; a real home)
LINEAGE_FACTION = {
    "western_european_germanic": "Iron Covenant",
    "western_european_gothic": "Shadow Courts",
    "norse_germanic_celtic": "Rune-Clans",
    "greek_roman": "Bronze Sanctum",
    "middle_eastern_persian": "Sunfire Dominion",
    "north_african_egyptian": "Sunfire Dominion",
    "east_asian_chinese": "Eternal Dynasties",
    "east_asian_japanese": "Eternal Dynasties",
    "east_asian_korean": "Eternal Dynasties",
    "pan_industrial": "Forge Republics",
    "mesoamerican": "Solar Pantheon",
    "sub_saharan_african": "Solar Pantheon",
    "south_southeast_asian": "Solar Pantheon",
    # void_liminal: intentionally absent — homed by Void Covenant override.
}


def build_records() -> list[dict]:
    records: list[dict] = []
    for lineage in CULTURAL_LINEAGES:
        if lineage == VOID_LINEAGE:
            continue  # override-homed; no records
        faction = LINEAGE_FACTION[lineage]
        for period in HISTORICAL_PERIODS:
            for register in REGISTERS:
                if register in VOID_REGISTERS:
                    continue  # void-register override intercepts before records
                records.append({
                    "lineage": lineage,
                    "period": period,
                    "register": register,
                    "faction": faction,
                })
    return records


def main() -> None:
    records = build_records()

    table = {
        "schema_version": "1.1",
        "_authoring_note": (
            "FACTION_LOOKUP_TABLE for Session 4 § 4.6 faction derivation. ELROND MAINTAINS "
            "records[]; rocket owns the loader + nearest-match + Void override "
            "(identity_sampling.py). Q10 redraw landed 2026-06-13 (elrond): 8 redrawn factions "
            "+ 1 composite ninth (Solar Pantheon homing mesoamerican / sub_saharan_african / "
            "south_southeast_asian). Faction is lineage-anchored (§ 7.2). One exact record per "
            "non-void (lineage, period, register) cell so nearest-match is never reached by "
            "construction; rocket's nearest-match logging is the empirical proof. void_liminal "
            "lineage + cosmic_horror/void_arcane registers are intentionally absent (consumed by "
            "the Void Covenant override before record lookup). Regenerate via "
            "agentic_orchestration/research/scripts/build_faction_lookup_table_q10_2026_06_13.py."
        ),
        "void_override_faction": "Void Covenant",
        "void_override_lineages": ["void_liminal"],
        "void_override_registers": ["cosmic_horror", "void_arcane"],
        "factions": [
            "Iron Covenant", "Shadow Courts", "Rune-Clans", "Bronze Sanctum",
            "Sunfire Dominion", "Eternal Dynasties", "Forge Republics",
            "Solar Pantheon", "Void Covenant",
        ],
        "records": records,
    }

    TABLE_PATH.write_text(json.dumps(table, indent=2) + "\n", encoding="utf-8")

    # Verification summary.
    factions = sorted({r["faction"] for r in records})
    non_void_lineages = [l for l in CULTURAL_LINEAGES if l != VOID_LINEAGE]
    homed = {r["lineage"] for r in records}
    missing = [l for l in non_void_lineages if l not in homed]
    expected = len(non_void_lineages) * len(HISTORICAL_PERIODS) * (len(REGISTERS) - len(VOID_REGISTERS))

    print(f"records written: {len(records)} (expected {expected})")
    print(f"distinct record-factions: {len(factions)} -> {factions}")
    print(f"+ Void Covenant via override = {len(factions) + 1} total factions")
    print(f"non-void lineages homed: {len(homed)}/{len(non_void_lineages)}; missing: {missing or 'none'}")
    print(f"void_liminal in records: {'void_liminal' in homed} (must be False)")
    print(f"path: {TABLE_PATH}")


if __name__ == "__main__":
    main()
