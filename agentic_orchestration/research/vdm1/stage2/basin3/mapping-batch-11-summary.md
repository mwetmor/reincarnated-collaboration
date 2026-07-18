# VDM-1 basin-3 mapping batch-11 — summary

**Batch:** m11 · **Game:** d4 · **Kits:** 12 · **Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-18

---

## Grade histogram

| Grade | Count | Kit IDs |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 10 | d4-cataclysm, d4-chain-lightning, d4-dance-of-knives, d4-death-trap, d4-earthquake-barb, d4-evade-sb, d4-flame-shield-immortal, d4-hammerdin-paladin, d4-heartseeker, d4-hota |
| APPROX | 2 | d4-dread-claws-warlock, d4-frozen-orb |
| GAPPED | 0 | — |

---

## Per-kit one-liners

| Kit ID | Grade | One-liner |
|---|---|---|
| d4-cataclysm | CLOSE | Lightning-storm ultimate; CDR-collapse permanent AoE zone; Spirit economy; ZONE_CONTROL + PERSISTENCE_ENGINE_uptime |
| d4-chain-lightning | CLOSE | Bidirectional chain hop (caster as return node); Mana economy; Crackling Energy as self_buff not R-M6; TEMPORAL_CHARGE + ZONE_CONTROL |
| d4-dance-of-knives | CLOSE | Moving-channel spin-to-win; Poison Imbuement skill-name blocked (§0 collision); physical null; ZONE_CONTROL + PERSISTENCE_ENGINE_uptime |
| d4-death-trap | CLOSE | Ultimate placed-trap with CDR collapse; vacuum pull in delivery_notes; Energy breakpoint identity-load-bearing; ZONE_CONTROL + TEMPORAL_CHARGE |
| d4-dread-claws-warlock | APPROX | Post-cutoff Warlock; element null (no damage-type language); Greater Demon = summoner-GAP rider; §C.5 cooldown framing; ZONE_CONTROL + TEMPORAL_CHARGE |
| d4-earthquake-barb | CLOSE | Leap/Stomp zone-stack with HotA detonation; Fury economy; earthquake_zone_active trigger mark; ZONE_CONTROL + GEOMETRY_PROPAGATION_overkill |
| d4-evade-sb | CLOSE | Evade-as-damage-verb triggering Storm Feathers barrage; Vigor + Ferocity cycle economy; MOMENTUM_CASCADE + TEMPORAL_CHARGE |
| d4-flame-shield-immortal | CLOSE | Permanent immunity via CDR collapse; fire element attested ('Burning damage'); burn ailment blocked (DoT delivery ≠ status); SACRIFICE_ASCENDANCY + PERSISTENCE_ENGINE_uptime |
| d4-frozen-orb | APPROX | MW3 BINDING: 'Frozen Orb' name alone does not attest water/freeze; zero element/ailment in any anchor; projectile-shatter delivery shape preserved; ZONE_CONTROL + TEMPORAL_CHARGE |
| d4-hammerdin-paladin | CLOSE | D4 Paladin; ERRATA-46: element null (holy = d2 import, struck); orbit spiral follows character (R-M8 pursuit); §C.5 cooldown framing; PERSISTENCE_ENGINE_uptime + ZONE_CONTROL |
| d4-heartseeker | CLOSE | §C.1/.2 hot-facts: seeking arrow + Paingorger echo rider; physical null; TEMPORAL_CHARGE + GEOMETRY_PROPAGATION_overkill |
| d4-hota | CLOSE | §C.3 hot-fact: Overpower = burst_window not ailment; fire element attested ('Fire-based melee'); Ancients as cast-proxy totem; TEMPORAL_CHARGE + ZONE_CONTROL |

---

## T4-door frequency

| T4 Token | Occurrences | Kits |
|---|---|---|
| ZONE_CONTROL | 10 | cataclysm, chain-lightning, dance-of-knives, death-trap, dread-claws-warlock, earthquake-barb, frozen-orb, hammerdin-paladin, hota, heartseeker (via GEOMETRY_PROPAGATION_overkill companion) |
| TEMPORAL_CHARGE | 8 | chain-lightning, death-trap, dread-claws-warlock, evade-sb, frozen-orb, heartseeker, hota, dance-of-knives (proxy) |
| PERSISTENCE_ENGINE_uptime | 4 | cataclysm, dance-of-knives, flame-shield-immortal, hammerdin-paladin |
| GEOMETRY_PROPAGATION_overkill | 2 | earthquake-barb, heartseeker |
| MOMENTUM_CASCADE | 1 | evade-sb |
| SACRIFICE_ASCENDANCY | 1 | flame-shield-immortal |

---

## §0 near-misses — statuses wanted but could not attest

| Kit | Wanted token | Why blocked |
|---|---|---|
| d4-cataclysm | shock | 'lightning strikes' attests element; no shock/stun/paralysis status word in anchor |
| d4-chain-lightning | shock | 'shock' appears only as skill-category name ('Shock builds', 'shock skill damage bonus') — §0.3 skill-name collision |
| d4-dance-of-knives | poison | 'Poison Imbuement' is a skill NAME — §0.3 collision; no verbatim 'poison damage' or 'poisoned' status language |
| d4-earthquake-barb | stun | 'Ground Stomp' name implies stun; no 'stun' or 'interrupt' status word in any anchor |
| d4-flame-shield-immortal | burn | 'Burning damage over 4 seconds' = DoT delivery language per basin-2 DoT-timing rule; the enemy STATUS not named as ailment in anchor |
| d4-frozen-orb | freeze / chill / water | MW3 BINDING: all element/ailment language comes from skill names only ('Frozen Orb', 'Ice Spikes', 'Azurewrath') — zero verbatim cold-damage or status language |
| d4-dread-claws-warlock | shadow | 'abyssal claw theme' + 'shadow' in item names only (Aspect of Deeper Shadows, Shadow of Harash) — §0.3 collision + mech_note probe |
| d4-hammerdin-paladin | holy | ERRATA-46: d4 Paladin 'holy' is a d2-lineage probe fabrication; struck from record |

---

## Candidates

### Docket candidates
None. Summoner-GAP riders in dread-claws-warlock and hota ride as fidelity notes; the summoner-deferral docket class already exists (no new docket entry required — existing family absorbs).

### Mint candidates
None. No new quantitative or qualitative mint required.

---

## Forced decisions

- **d4-frozen-orb element null:** MW3 binding is the hardest forced decision in this batch. A kit canonically associated with cold/ice in every player's mind maps element null and ailment null because the dossier contains zero verbatim cold-damage or status language beyond skill names. This is the single most jarring gap in the batch.
- **d4-hammerdin-paladin element null:** ERRATA-46 applies; 'holy' element is confirmed d2/d3 Paladin lineage import; struck at ingest.
- **d4-dread-claws-warlock §C.5:** Wrath resource attested in variants row but addendum §C.5 governs — cooldown framing applied; Wrath attestation noted in fidelity_notes without populating the contested key.

---

## Batch notes

- All 12 kits d4 (positive=1). No SYSTEM kits.
- Both APPROX kits (frozen-orb, dread-claws-warlock) reach MAPPED terminal state — no GAPPED row in this batch.
- MW3 attestation law did the heaviest work: 6 ailment/element slots blocked across multiple kits for name-only grounds.
- Post-cutoff Paladin and Warlock both handled cleanly under §C.5.


## STEWARD AUDIT ADDENDUM — MW4-close 2026-07-18 (gandalf run steward)
Recount m11: 12 kits, grades {CLOSE:10, APPROX:2}, terminal {MAPPED:12}; biconditional CLEAN (0 GAPPED). Battery 92S/4E/15M contiguous.
**0 strikes.** 6 element-name flags investigated via full-store context dump; ALL resolve to KEEP:
- cataclysm lightning — "lightning strikes and twisters" (behavior, not name).
- chain-lightning — 3 skills lightning w/ "bolt bounces between enemies"; lone "frost" = Frost Nova / Azurewrath season-variant NAMES, no water skill.
- dread-claws shadow — 8 hits all shadowform-buff / shadow-of-harash-set / aspect-of-deeper-shadows (name/mechanic-only); null correct.
- earthquake-barb — all null; earthquake / ground-stomp / fissure = effect-names, "physical" mech_note inadmissible; mapper resisted earthquake->earth name trap. [flavor specimen "incendiary fissures" -> review book]
- flame-shield fire — "Burning damage over 4 seconds to surrounding enemies" (behavior); Teleport correctly null.
- hota fire — "Fire-based melee" descriptor; shouts correctly null.
Mapper self-blocked 6 name-only slots proactively (per its own summary) — MW3-close element-name amendments PROPAGATED cleanly into the mapper. m11 = the clean-propagation datapoint.
