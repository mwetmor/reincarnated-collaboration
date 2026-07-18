# VDM-1 basin-3 mapping batch-01 summary

**Batch:** m01 · **Kits:** 12 · **Date:** 2026-07-18 · **Author:** gandalf (SPEC-AUTHOR)

## Grade histogram

| Grade | Count |
|---|---|
| EXACT | 1 |
| CLOSE | 9 |
| APPROX | 2 |
| GAPPED | 0 |

All 12 kits: `terminal_state: MAPPED`. No GAPPED/MAPPED_DOCKET this batch.

## Per-kit one-liners

| kit_id | grade | one-liner |
|---|---|---|
| d2-auradin | CLOSE | Item-defined aura-pulse (Dream/Dragon runewords); dual ring geometry + curse:sap Conviction; lightning+fire split |
| d2-avenger | CLOSE | Tri-element melee Vengeance; mapped fire+lightning (cold dropped per triple-element rule); curse:sap Conviction |
| d2-berserker | CLOSE | Magic-damage melee with zero-defense trade (DEFENSIVE_TRADEOFF); Howl fear attested; Hork to loot-economy docket |
| d2-blade-sin | APPROX | Fixed-IAS-immune Blade Fury projectile; IAS-hard-cap not native to engine cadence model |
| d2-blaze-sorc | APPROX | Movement-trail fire DoT (NOT channeled per ERRATA-46 RF-01); no 26-enum for movement-paints-ground-path |
| d2-blizzard-sorc | EXACT | Cursor-placed ice zone + Teleport repositioning; water element; freeze + chill attested |
| d2-bonemancer | CLOSE | Line-pierce Bone Spear + seeking Bone Spirit + root Prison; shadow element; PvM CE is variant-scope |
| d2-bowazon | CLOSE | Multi-projectile fan/sequential/seeking trio; physical element-neutral; Valkyrie pet-rider GAP noted |
| d2-bvc | CLOSE | Moving-channel WW (§CROSS row 5 MOVING) + Leap knockback; PvP context fidelity note |
| d2-charger | CLOSE | Traversal-strike composite Charge (§A row 3); MOMENTUM_CASCADE; Fanaticism IAS non-interaction fidelity |
| d2-conc-barb | CLOSE | Uninterruptible single-target physical swing; DEFENSIVE_TRADEOFF captures safety-trade identity |
| d2-daggermancer | CLOSE | Venom-melee earth element; poison DoT attested; Amp Damage → curse:amplify per §2 direct row |


## T4-door frequency

| T4 token | kits |
|---|---|
| PERSISTENCE_ENGINE_uptime | 4 (blaze-sorc, blizzard-sorc, bonemancer, conc-barb) |
| DEFENSIVE_TRADEOFF | 3 (berserker, bvc, conc-barb) |
| MOMENTUM_CASCADE | 2 (bvc, charger) |
| ZONE_CONTROL | 2 (blizzard-sorc, bonemancer) |
| NETWORK_AMPLIFIER | 2 (auradin, avenger) |
| GEOMETRY_COLLAPSE | 2 (berserker, charger) |
| ELEMENT_CONVERSION_HYBRID | 2 (auradin, avenger) |
| TEMPORAL_CHARGE | 2 (blade-sin, bowazon) |
| GEOMETRY_PROPAGATION_overkill | 1 (bowazon) |
| PERSISTENCE_ENGINE_saturation | 1 (daggermancer) |
| ELEMENT_CONVERSION_PHYSICAL | 1 (daggermancer) |
| GEOMETRY_PROPAGATION_cascade | 1 (bonemancer) |
| ELEMENT_CONVERSION_MONO | 1 (blizzard-sorc) |

## Candidate files

- `docket-candidates-batch-01.jsonl` — 2 entries
  - `loot-economy-identity`: d2-berserker Hork/Find-Item loop (§A row 4 standing docket)
  - `spatial-consumable-resource-node`: d2-berserker cold-avoidance-for-corpse-preservation (§CROSS row 1)
- `mint-candidates-batch-01.jsonl` — NOT created (no mint candidates surfaced this batch)

## §0 near-misses — statuses wanted but not attested

| Kit | Status wanted | Why not emitted |
|---|---|---|
| d2-berserker | stun (Howl) | Howl is 'panic tool to scatter' = fear (flee), not stun/interrupt |
| d2-charger | stun | Charge one-hit burst noted but no fetched stun language |
| d2-conc-barb | stun | Physical heavy hits implied but no fetched stun language |
| d2-bowazon | chill (Freezing Arrow variant) | Freezeazon is a VARIANT; core identity = physical Multishot/Strafe; variant-scope law governs |
| d2-berserker | curse:amplify | No Amp Damage in berserker skill set; Hork is loot-only |

## Forced decisions / notable rulings applied

- **ERRATA-46 RF-01 (blaze-sorc):** 'channeled' probe annotation overridden; fetched language 'player moves freely while trail persists' governs — movement-trail, not rooted channel.
- **Holy element not emitted (auradin):** §A row 6 hammerdin precedent: 'holy is a PROBE fabrication'; Holy Shock maps as lightning, Holy Fire as fire. No fetched auradin language names 'holy element' as engine family.
- **Berserker magic damage → element-neutral:** magic damage has no engine family (physical rule extension).
- **Bonemancer CE variant-scope:** Corpse Explosion (PvM variant) governed by variant-scope law; core loop = Bone Spear.
- **Daggermancer earth vs shadow:** Poison Dagger is venom-themed physical melee (not bone/necrotic lineage) → earth per §1 venom-themed branch.
- **Bowazon Valkyrie:** pet-rider noted in scaffold; does not elevate to GAPPED because bow-shot loop maps fully.
- **d2-berserker fear attestation:** Howl 'panic tool to scatter mobs' attests flee/fear behavior per §2 (fear = boss-immune).


## STEWARD AUDIT ADDENDUM (2026-07-18, MW1 close)
Recount CONFIRMED 1E/9C/2A/0G, roster 12/12, contiguity CLEAN. AUDIT-EDIT: blizzard-sorc Ice Blast chill→freeze (store attests 'freeze utility' — adjacent-status substitution, leak strike #1 basin-3; grade unchanged). Element rulings RATIFIED: berserker magic-tag = element-neutral; bonemancer bone→shadow = main-law table row (no new law). Docket filings (loot-economy-identity + spatial-consumable-resource-node) accepted → review-book consolidation.
