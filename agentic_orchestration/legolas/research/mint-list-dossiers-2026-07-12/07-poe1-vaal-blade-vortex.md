# Dossier — poe1 Vaal Blade Vortex

**Mode:** A (analytical)
**Commissioner:** gandalf (via Matt's usage-offload directive, 2026-07-12)
**Roster target:** B10 (operator-tier variant of base Poison BV, already attested in corpus)
**Priority:** LOW-MED
**Corpus gap confirmed:** `poe1-poison-bv` exists; `poe1-minion-pact-bv` exists. No Vaal BV record.
**Crawl date:** 2026-07-12

---

## Identity

**Game:** poe1 (Path of Exile 1)
**Patch/era span:** 3.0 (Fall of Oriath, August 2017) through 3.29 (ongoing). Base BV existed earlier (pre-3.0 as a simpler skill); Vaal BV gem added with the Vaal gem expansion. Peak Vaal BV meta presence: 3.0–3.7 era; Poison BV Occultist (which incorporates Vaal BV) peaked 3.0–3.15.
**Canon tier:** moderate (the Vaal VARIANT specifically; the base Poison BV is deep canon; Vaal BV is the burst-operator layer on top of that sustained base)
**Folk names:** "Vaal BV," "VBV Occultist," "Vaal Blade Vortex Occultist," "VBV Trickster," "Vaal BV Poison"
**Shipped / negative-canon status:** SHIPPED — used as the boss-kill burst layer in Poison BV builds; community-named as a distinct sub-build in forums and PoB archives (216 VBV builds on pobarchives.com).

## Build identity (2–4 sentences)

Vaal Blade Vortex is the Vaal-gem version of Blade Vortex: it consumes stored souls (the Vaal resource, charged by killing enemies) to create a powerful orbiting blade storm that homes in on enemies — dealing higher base damage than standard BV and adding a burst-layer on top of the sustained Poison DoT stack. In the canonical Poison BV kit, standard BV runs continuously to stack Poison on enemies (each hit = a new Poison application), while Vaal BV is held for boss encounters to apply an immediate burst of additional stacks. This creates an OPERATOR mechanic: you farm Vaal souls on trash packs, then "spend" them for a single burst on a boss — a resource-detonation layer distinct from the base sustained loop. The community-named this split explicitly as "VBV for bosses, BV for mapping," making them lattice-grain distinct (G1 check: the boss-loop involves soul-farming + single detonation; the trash-loop is pure orbital sustained — different engagement models).

## Lineage

**Parent record:** `poe1-poison-bv` (already in corpus) — the base kit; Vaal BV is an operator-tier addition
**Sibling record:** `poe1-minion-pact-bv` (already in corpus) — different sub-variant of the BV family

**Cross-game family:**
- GX-09: Body-orbit / autonomous orbiters (BV is specifically a SELF-orbit, not body-orbit of constructs; GX-09 names it as "Poison BV anchor" — this record reinforces that anchor)
- GX-03: Mark-and-consume / apply-then-detonate (Vaal BV adds a stored-resource detonation layer ON TOP of the sustained orbital — GX-03 secondary evidence)
- Vaal mechanics family across PoE1: Vaal Cyclone, Vaal Ice Nova, Vaal Arc — all share the soul-farming operator model

**Descendants:**
- PoE2 "Vaal" skill variants (GGG continues the Vaal soul-system in PoE2)
- RDR B10 (bench kit; Vaal BV as the design ancestor for a "resource-accumulate → burst-discharge" orbital identity)

## Engine-prefix claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | INT | MED | Most Vaal BV builds run Occultist (Witch = INT class) or Assassin (INT/DEX); spell scaling via INT; Occultist's chaos damage nodes are canonical. |
| range | MID | MED | Blades orbit the player at arm-length radius (~10–15 units); player must position within hit-range of enemy; not adjacent (melee) but not safe-range (ranged). MID is accurate. |
| tempo | HIGH | HIGH | Standard BV runs at maximum stacks (10 blades, 7 hits/second) continuously; the tempo of Poison stack application is very high. The VBV burst is LOW-tempo in isolation (soul-farm, then single cast) but the continuous BV baseline is HIGH. Recording the COMBINED kit tempo: HIGH for the standard BV component. |
| amp | VARIABLE | MED | Standard BV produces consistent orbital hits (FLAT-ish); Vaal BV burst produces an extreme damage spike (SPIKY). The combined kit has a VARIABLE pattern: sustained flat baseline + periodic extreme spike. |
| proxy | SOLO | HIGH | Blades orbit the player — they are the player's attack, not a separate proxy entity. Solo. |
| commitment | WIND-UP | MED | Standard BV requires pre-stacking 10 blades before engagement (brief wind-up); Vaal BV adds a soul-farming accumulation before detonation. The full kit has a WIND-UP character: prepare → engage → burst. |

## Raw descriptors (not engine keys)

**geo:** Short-radius ring AoE around player (blade orbit ~10–15 unit radius); enemies must be adjacent to the player's orbit to be hit; tight engagement zone. Vaal BV may home in on nearest enemy cluster, extending the effective engagement range temporarily.

**ctrl:** No CC from BV itself; the orbit's hit rate can interrupt enemy attacks de facto but no explicit stun/slow/freeze mechanic.

**mob:** Player must stay near enemies for orbital damage to connect; slower repositioning during active BV stacking (moving away from enemies reduces damage). Moderate mobility penalty during combat.

**def:** Primarily CI (Chaos Inoculation) or high evasion; Occultist's Profane Bloom and Void Beacon provide defensive passive benefits. The kit's defense comes from CI (immune to chaos damage) combined with the fact that enemies near the player are dying fast from Poison stacks.

**econ:** Mana cost per BV cast (moderate); Vaal souls from killing enemies (passive accumulation during trash clear; free resource). Flask-based sustain common. Poison charges/stacks managed via hit count (each BV hit = Poison application; no active econ management).

**elem:** Chaos primary (Poison DoT converts to Chaos damage in PoE); physical base (BV is physical hit that applies Poison); some builds run full conversion to chaos hits.

## Sources

- PoB Archives (pobarchives.com): 216 Vaal BV builds confirmed
- PoE Forum thread "[3.16] Vaal Blade Vortex + Poison Trickster" — mechanic confirmation
- Maxroll "Poison BV Occultist" guide (3.21 Crucible): https://maxroll.gg/poe/build-guides/poison-blade-vortex-occultist-league-starter-guide
- PoE Wiki "Vaal Blade Vortex": https://www.poewiki.net/wiki/Vaal_Blade_Vortex
- Knowledge base (kb) — BV mechanics from training data
- V4-r2 §F4 mint-list + GX-09 ledger entry

## Knowledge gaps

- Exact Vaal BV soul cost and soul generation rates not verified
- Whether the community explicitly names "VBV" as a distinct build from "Poison BV" (vs treating it as a sub-option within the same build) affects G1 grain ruling — PoB archives data shows 216 distinct builds listed as "Vaal BV" suggesting community DOES name it as a separate build entity
- Post-3.20 era viability of Vaal BV vs base Poison BV not verified (skill balance changes in 3.20–3.29 range)
