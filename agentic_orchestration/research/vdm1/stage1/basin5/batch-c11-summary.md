# Batch c11 summary — Halls of Torment (hot-b) — 2026-07-18

## Per-kit one-liners

- **hot-norseman-frost-avalanche**: Norseman class confirmed; Frost Avalanche is a frost-damage AoE nova; offer-pool hygiene strategy confirmed; ERA confirmed (added Aug 2023 EA, active 1.0-2024 + 1.1-2026).
- **hot-phantom-needles**: Phantom Needles confirmed as Archer's pierce-line filler ability; projectile pierce confirmed; era confirmed (1.0-2024 guide attested).
- **hot-sage-ring-blades**: Sage + Ring Blades identity confirmed; orbit/travel-out geometry confirmed; era claim partially clarified — Sage added Feb 2024 (pre-1.0), so hot-1.1-2026-only era claim is CONSERVATIVE (Sage exists in the pre-1.0 gap too); conf capped at 0.45 per post-cutoff rule.
- **hot-shieldmaiden-block**: Block-Stack build confirmed with direct "take x2 hammer splash at level 60" quote from forum; Shield Bash scales 2x Block Strength confirmed; level-60 capstone attested.
- **hot-sorceress-splinters**: Sorceress + Arcane Splinters confirmed; 8-projectile mechanic (4 above/4 below) confirmed; screen-coverage scaling confirmed; element status see below.
- **hot-spirit-warrior**: Spirit Warrior ability confirmed as magic-melee summon/proxy; damage type = "Melee + Magic" per community source; era claim (1.0-2024 only) UNSUPPORTED — no source explicitly limits to that era; guides are era-generic.
- **hot-swordsman**: Swordsman as default starter class confirmed from multiple sources; frontal slash arc confirmed; early access 2023 floor confirmed; physical damage confirmed.
- **hot-warlock**: Warlock as summoner class confirmed; Ravaging Specters mechanics confirmed (chain-to-nearest, 2s/20-hit cap); "dark/arcane" label in DB is NOT confirmed by fetched text — sources say "summon damage" and "magic damage" only; see element notes below.

## Verdict histogram (ADVISORY — steward recounts from file)

- CONFIRMED: 21
- UNSUPPORTED: 1 (hot-spirit-warrior era — no source explicitly floors or caps the era)
- CONTRADICTED: 0
- SOURCE_NOT_FOUND: 0

## Contradictions

NONE. 0 contradictions this batch.

## SNF kits

NONE. 0 SOURCE_NOT_FOUND kits. All 8 kits have live attested sources via Steam community + gaming sites. fandom.com was 402-blocked as predicted; self-recovered to Steam forums and community guides throughout.

## Dossier coverage

All 8 kits: 5/6 families populated (skill_loop, skill_geometry, item_alterations, capstone_alterations, variants = 5; author_credit = abstained on all 8 — no named guide authors extractable from communal Steam/gaming-site sources). 40 non-abstained rows / 48 total rows = 83% populated. Author_credit abstention documented — communal Steam sources do not expose individual author handles for most guides.

## Element-attestation summary (per-kit)

- **hot-norseman-frost-avalanche**: ATTESTED. Source text says "Applies a frost status effect to enemies" and "releases a big circular Frost Nova wave" — frost as a DAMAGE TYPE/STATUS confirmed in fetched text. Element = frost/cold. Anchor: "Applies a frost status effect to enemies; enemies with frost explode when they exceed 20 stacks or upon death."
- **hot-phantom-needles**: NOT attested. Fetched text describes "Physical/Projectile" but no element word applied as damage-type descriptor to generic effect noun. DB label "physical/phantom" stands as unconfirmed element label; element-silent in dossier.
- **hot-sage-ring-blades**: NOT attested for the primary damage type. "Piercing Blades upgrade adds 2 projectiles that deal magic damage" — this is an upgrade add-on, not the base Ring Blades damage. Base damage type not explicitly stated in fetched text. Element-silent on base; upgrade adds magic.
- **hot-shieldmaiden-block**: NOT attested. Physical melee damage throughout sources; no element word applied as damage-type descriptor. Element-silent.
- **hot-sorceress-splinters**: PARTIALLY attested. DB label "arcane" — fetched text says "Arcane Splinters" (name only, not a damage-type descriptor). "Arcane Elements upgrade adds elemental damage" — this is upgrade-gated, not base. Base damage type not stated as "arcane" in fetched text. ELEMENT LAW: name-only, not attested. Element-silent on base per law.
- **hot-spirit-warrior**: ATTESTED. Source text: "Spirit Warrior (main attack) - Melee + Magic" — magic applied as damage-type descriptor. Element = magic. Anchor: "Spirit Warrior (main attack) - Melee + Magic."
- **hot-swordsman**: NOT attested for element. Sources confirm physical AOE sword attack; no element word as damage-type descriptor. Element-silent.
- **hot-warlock**: NOT attested for dark/arcane. DB label "dark/arcane" — fetched text says "summon damage" and "magic damage" (for specters from community). No source uses "dark damage" as a damage-type descriptor in fetched text. Element-silent per ELEMENT LAW; "dark" rejected as name-only inferred label.

## Rotation-shaped UNSUPPORTED note

All 8 hot-b kits are auto-attack roguelite. No rotation-shaped claims were made or needed. The DB probe facts correctly model HoT as auto-fire (offer-pool drafting, not manual rotation). UNSUPPORTED for rotation framing is not applicable here — probe facts were drafted without rotation framing throughout.

## Red flags / source access

- **fandom.com 402**: Confirmed. hot.fandom.com returned 402 on all direct fetch attempts. Self-recovered to Steam community + fantasywarden.com + gaming guides throughout. No information was blocked — adequate live alternatives existed.
- **hot-sage-ring-blades era note**: DB era = hot-1.1-2026 only. Fetched sources confirm Sage was added Feb 19 2024 (pre-1.0, so it existed during hot-1.0-2024 as well). The era stamp in DB may be over-narrow. Flagged for steward; not a contradiction (era stamp could mean "1.1-2026 is the era we analyzed" not "absent in 1.0").
- **hot-warlock dark label**: DB elem_raw = "dark/arcane"; no fetched source confirms "dark" as a damage type. Community says "summon damage" + "magic"; dark is a label inferred from aesthetics/naming. Element law rejects it. Steward should correct elem_raw if downstream mapping applies element filter.
- **hot-spirit-warrior identity clarification**: Spirit Warrior is an ABILITY (not a class). The kit_id "hot-spirit-warrior" represents a build archetype built around this ability — likely on Warlock or another class. Sources confirm the ability is cross-class usable (Warlock synergy is the dominant community framing). Kit identity as "ghost-proxy" ability build is sound; class attribution = multi-class.
- **primagames.com 403**: One fetch blocked; recovered to alternative Steam sources without loss.
- **steamcommunity.com 429**: One throttle hit; route diversity avoided blocking the crawl.
