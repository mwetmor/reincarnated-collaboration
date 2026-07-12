# Dossier — poe1 Ring of Shields (+ Replica)

**Mode:** A (analytical)
**Commissioner:** gandalf (via Matt's usage-offload directive, 2026-07-12)
**Roster targets:** H1 (orbital-guard "-lite guard"), B7
**Priority:** MED
**Corpus gap confirmed:** No ring-of-shields or orbital-guard record in `canon-corpus-poe1.jsonl`
**Crawl date:** 2026-07-12

---

## ⚠ KNOWLEDGE-GAP FLAG — PRIMARY FINDING

**"Ring of Shields" cannot be confirmed as a named PoE1 skill gem, unique item, or well-documented community build from training data or web searches (four targeted search passes conducted, including poe.ninja, poewiki.net, and pobarchives, all returning 403 or no matching result).**

This dossier documents:
1. What WAS found (closest candidates)
2. The engine-prefix claims those candidates would support
3. A recommended research pathway to resolve the gap

This dossier should NOT be treated as a confirmed record. Elrond should flag it for a direct PoE wiki verification pass before minting a corpus row.

---

## Best-candidate analysis

### Candidate A: Post-training-cutoff PoE1 skill gem (HIGH PROBABILITY)

PoE1 has continued receiving new skill gems through 2025–2026 (Settlers of Kalguur 3.25, Settlers Extended, Mercenaries 3.27, Keepers of the Flame 3.28, Affliction-era remixes). "Ring of Shields" may have been added in a 3.25–3.29 league that postdates training data. Supporting evidence:
- Svalinn (a unique tower shield with on-block elemental effects) is confirmed present in poe.ninja for Mercenaries and Keepers leagues (3.27–3.28), indicating shield-related mechanic expansion in recent leagues
- The "Replica" suffix in the commission name ("+ Replica") refers to Heist-league (3.13) Replica unique items OR could refer to a "Replica" unique version of a newer item — if "Ring of Shields" was added post-3.13, it could have a Replica counterpart from a later item expansion
- Commission's "orbital-guard ancestor" framing aligns with a new defensive skill creating orbiting shield constructs — a mechanic type PoE2 explored (Wall of Shields 0.5; Svalinn armor set) and PoE1 may have implemented as a skill gem in parallel development

### Candidate B: Spectral Shield Throw of Trarthus (LOW-MEDIUM PROBABILITY)

"Spectral Shield Throw of Trarthus" (transfigured gem from 3.24 Necropolis league, 2024) creates a shield that hovers at a target location and fires shard projectiles. The folk name for builds using this hovering-shield mechanic COULD be "Ring of Shields" in some community references. However: the description describes a shard-emitting fixed point, not an orbital ring — the "orbital-guard" framing doesn't fit cleanly.

### Candidate C: Bone Barrier builds (LOW PROBABILITY)

Necromancer ascendancy "Bone Barrier" (3.6 Synthesis, 2019) creates bone shields that orbit the character and absorb damage. These are guard-type effects. Community builds may use "Ring of Shields" as a folk name for Bone Barrier-heavy builds, but no evidence was found.

### Candidate D: Ancestral Bond + Totems-as-Guard builds (LOW PROBABILITY)

PoE1 builds using multiple stationary totems arranged in a ring formation for "orbital guard" effect — but this is a positioning meta-technique, not a named build.

---

## Conditional engine-prefix claims (SPECULATIVE — LOW CONFIDENCE)

Given the "orbital-guard" framing for H1 ("-lite guard") and B7, and assuming Candidate A or B is correct:

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | INT or DEX | LOW | If defensive guard skill: Necromancer (INT) or Gladiator (STR/DEX); "Spectral Shield Throw" arm = Gladiator (DEX). Cannot resolve without confirming the source build. |
| range | MID | LOW | Guard/orbital mechanics typically operate at mid-field; the player does not need to be adjacent or at max range |
| tempo | LOW | LOW | Guard-oriented builds typically have low action cadence; defensive posture |
| amp | VARIABLE | LOW | Orbital/guard constructs deal variable damage based on trigger frequency |
| proxy | HEAVY or MED | LOW | Orbital guard = proxy constructs doing defensive + offensive work; HEAVY if primary DPS, MED if supplemental |
| commitment | INSTANT | MED | Guard skill activation is typically instant in PoE (guard skills have no cast time) |

## Recommended resolution pathway

1. **Direct PoE wiki query:** Search https://www.poewiki.net/wiki/ for skills added in leagues 3.24–3.29 with "shield" in the name or the mechanic keyword "orbit"
2. **poe.ninja skill gem list:** Check https://poe.ninja/poe1/economy/keepers/skill-gems for any gem matching "Ring of Shields" or "Shield Ring"
3. **Reddit/forum search:** r/pathofexile search for "ring of shields build" or "orbital shield build" to identify if this is a folk name for a known build type
4. **PoE2 parallel check:** Confirm whether "Ring of Shields" exists as a PoE2 skill (it might be a PoE2 skill that Gandalf sourced from cross-game research rather than a PoE1 skill)

## Status

PENDING — do not mint corpus row until source build confirmed. Flag to Elrond for unresolved-gap routing.

## Sources

- poe.ninja (Mercenaries/Keepers economy pages — Svalinn confirmed, Ring of Shields not found)
- Multiple WebSearch passes (2026-07-12) — no results for "Ring of Shields" as named PoE1 entity
- V4-r2 §F4 mint-list (gandalf, 2026-07-12) — name sourced from Gandalf's cross-research
