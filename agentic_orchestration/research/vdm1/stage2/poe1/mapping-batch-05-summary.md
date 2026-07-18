# VDM-1 Stage-2 PoE1 mapping batch-05 — summary

**Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-18 · **Kits:** 12 · **Provenance:** authored-vdm1 (OUR judgment against source-verified stage-1 facts)

Batch character: a **lightning-heavy striker/trigger cohort** (5 of 12 lightning) plus two channel/volley ramp kits, two item-keystone kits (Shavs, Mjölner — both dissolve cleanly into named crosswalk lanes), one mines kit, one bleed melee, one flask-ammo poison lobber, and one post-cutoff sacrifice kit. Three kits carry ingest-3 errata'd eras (icicle-mines 3.8-3.13, lightning-conduit 3.19;3.20+, pconc 3.16-3.19;3.20+ — corpus rows are post-errata truth, mapped as such) and kinetic-fusillade's era_year was rekeyed 2013→2024 (3.27-era kit).

## Grade histogram
| Grade | Count |
|---|---|
| EXACT | 0 |
| CLOSE | 11 |
| APPROX | 1 |
| GAPPED | 0 |

**Terminal state:** MAPPED 12 · MAPPED_DOCKET 0 (R-M7 1:1 holds: the sole APPROX files a candidate but keeps identity → MAPPED).
**Candidate counts:** docket-candidates **1**, mint-candidates **0** (no mint file emitted; no quantitative range/count extension forced).

No EXACT per grade-honesty: every kit carries at least one un-enumerated behavioral/numeric property (sequential-vs-simultaneous chain semantics, trigger ICDs, stage/release magnitudes, overlap-shotgun emergence, snapshot couplings).

## Per-kit one-liners
- **poe1-icicle-mines** (CLOSE): mine-field cold volleys — `multi_projectile` converging from placements; mine chassis via b04 GC-mines trigger-grammar + activation-toggle; detonation-sequence projectile growth → GEOMETRY_PROPAGATION_cascade. Eras post-errata 3.8-3.13.
- **poe1-incinerate** (CLOSE): founding-era rooted channel — `beam_channel` (cone footprint noted per §7.2), tick-cost PC; stage-ramp→release-wave = MOMENTUM_CASCADE (Layer-2 stacking→THRESHOLD_BURST, verified). 1.x 3-stage vs modern 8-stage era-drift noted.
- **poe1-kinetic-fusillade** (CLOSE): post-cutoff 3.27 wand volley — physical rule (element-neutral, no ailments); hover-bank → `multi_projectile` + accumulator(12) + MOMENTUM_CASCADE crescendo. Single door; thin-source noted.
- **poe1-lacerate-glad** (CLOSE): element-neutral `melee_arc` + bleed + stance `self_buff`/activation-toggle; PERSISTENCE_ENGINE_uptime + GEOMETRY_PROPAGATION_cascade (Gratuitous Violence bleed-pop). PHASE_MOMENTUM considered/rejected (parks, doesn't cycle). Era claim UNSUPPORTED — mapped on CONFIRMED mechanics.
- **poe1-lightning-arrow** (CLOSE): bow `chain` with **shock→sunder** false-friend applied; simultaneous-splash-to-3 vs engine sequential 0.7×-decay hops is the honest drift; ELEMENT_CONVERSION_PHYSICAL + ELEMENTAL_ECHO.
- **poe1-lightning-conduit** (CLOSE): in-kit apply-consume-pair — Orb of Storms (`totem`) applies sunder, Conduit (`circle` 6m) consumes it; on-mark-consume/consume-mark; RESONANCE_LOOP (Layer-2 SEQUENCE→THRESHOLD_BURST is literally this kit). Eras post-errata 3.19;3.20+.
- **poe1-lightning-strike** (CLOSE): frost-blades-precedent composite `melee_strike`→`multi_projectile` forward 85° fan; ELEMENT_CONVERSION_PHYSICAL + GEOMETRY_PROPAGATION_cascade; shock→sunder.
- **poe1-low-life-shavs** (CLOSE): item-keystone economy archetype — §4 names Shavronne's low-life BY NAME → item dissolves into `reservation_percent=0.65` + `reservation_resource=hp` (b02 blood-magic precedent); DEFENSIVE_TRADEOFF + SACRIFICE_ASCENDANCY + NETWORK_AMPLIFIER (aura payload); below-35% conditional flattens faithfully to the permanently-pinned static trade. No docket (lane expresses the warp).
- **poe1-minion-pact-bv** (APPROX): 3.28 sacrifice-snapshot — native `orbit` BV + spectre feedstock (`totem`); consume-only/on-cast-linked/resource-fill grammar + cycle econ + SACRIFICE_ASCENDANCY/RESOURCE_CONVERSION; entity-as-consumable-resource gap DOCKETED (4th evidence for the b02 consolidation family; dark-pact R-M7 precedent keeps it APPROX/MAPPED). Folk name honestly UNATTESTED (identity UNSUPPORTED, promoted on mechanics) — caveat carried in fidelity_notes.
- **poe1-mjolner** (CLOSE): item-keystone trigger — §4 mechanic-granting unique dissolves into on-hit-threshold/linked-cast + proc-loop PC at DEPTH-1; payload Arc `chain` (inherits arc-b01 decay drift; Ball Lightning alt per R-M6, not re-decided); RESONANCE_LOOP + ELEMENTAL_ECHO. 0.25s ICD + free-payload-cost have no carriers (cadence_scale and cost_scale=0.0 both rejected as misuse; noted instead).
- **poe1-molten-strike** (CLOSE): composite `melee_strike`→`multi_projectile` magma rain; the overlap boss-shotgun is emergent, not enumerated; ELEMENT_CONVERSION_PHYSICAL (60% verbatim) + GEOMETRY_PROPAGATION_cascade.
- **poe1-pconc** (CLOSE): chaos-POISON → **earth** (venom/Pathfinder register; shadow alternative noted; contrast b03 deaths-oath/edc shadow+drain) + `ground_targeted_circle` lob; flask-charge ammo lands on real keys (charge_stack=cycle, charge_max=10, recharge=time) + RESOURCE_CONVERSION (recovery-stat→damage) + PERSISTENCE_ENGINE_saturation; probe 'wither' held out as build-external. Eras post-errata 3.16-3.19;3.20+.

## T4-door frequency
| n | door |
|---|---|
| 5 | ELEMENTAL_ECHO |
| 4 | GEOMETRY_PROPAGATION_cascade |
| 3 | ELEMENT_CONVERSION_PHYSICAL |
| 2 | MOMENTUM_CASCADE · RESONANCE_LOOP · SACRIFICE_ASCENDANCY · RESOURCE_CONVERSION |
| 1 | PERSISTENCE_ENGINE_uptime · PERSISTENCE_ENGINE_saturation · DEFENSIVE_TRADEOFF · NETWORK_AMPLIFIER |

All 11 distinct door tokens verified against `t4_catalog_v2.py` / `layer2_dimensions.py` (R-M1). ELEMENTAL_ECHO + conversion dominance is the mono-lightning/fire signature; the RESONANCE_LOOP pair (conduit, mjolner) is a genuine match — its verified Layer-2 (SEQUENCE trigger → THRESHOLD_BURST) is exactly the apply-then-cash-in / swing-until-proc shape, not door-spam.

## Docket candidates (1) — steward ratification required before any elrond ingest
1. **Entity-as-consumable-resource (proxy-sacrifice snapshot)** (minion-pact-bv): minion life pool read into spell damage on cast-sacrifice, snapshotted. Filed as the **4th evidence kit** for the b02 STEWARD CONSOLIDATION FLAG family (animate-weapon b01, bladefall + dark-pact b02) — now spanning three batches. Ruling requested on the consolidated family: mint one shared primitive, or declare the approximations canonical.

## What felt forced / judgment calls worth the steward's eye
- **Lightning-arrow `chain`:** the source splash is SIMULTANEOUS to up-to-3 at full splash damage; engine chain is sequential with 0.7×/hop decay (arc-b01 verified). Chain is still the honest 26-type — the drift is cadence-visible, damage-minor. multi_projectile rejected (one arrow).
- **Incinerate `beam_channel` over `cone`:** channel-dominance per §7.2 (the held channel is the identity; commit=channel corroborates); the stage-expanding cone footprint is the recorded alternative. A reader preferring footprint-over-delivery would flip this; I ruled delivery.
- **Mjolner's two rejected econ keys:** cadence_scale (scales the kit's own cooldown table, not a trigger ICD) and cost_scale=0.0 (would claim the whole chassis free, but only the triggered payload is free). Both would have been token-shaped lies; noted in prose instead. If trigger-ICD accrues more instances, it may deserve R-M5-style graduation.
- **PConc earth-vs-shadow:** first chaos-poison kit routed to EARTH this run (b03's chaos kits went shadow+drain). The §1 poison row splits on register; Pathfinder alchemical-venom reads earth. Steward may want a standing sub-rule (alchemical/venom→earth, corruption→shadow) to keep future batches deterministic.
- **Low-life-shavs threshold flattening:** the below-35% conditional payoff is mapped as a permanent static trade because reservation PINS the state — faithful to lived play, but a design-purist could call the conditional structure itself identity-bearing. Graded CLOSE on the named-§4-row + b02 blood-magic precedent; flag if the steward reads it APPROX.
