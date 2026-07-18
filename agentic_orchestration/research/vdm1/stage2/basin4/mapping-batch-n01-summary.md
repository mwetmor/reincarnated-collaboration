# VDM-1 basin-4 mapping batch n01 — summary

**Batch:** n01 · **Kits:** 11/11 (roster complete) · **Date:** 2026-07-18 · **Author:** gandalf (mapping-author role)

---

## Grade histogram (advisory — steward audits ≥25%)

| Grade | Count | Kits |
|---|---|---|
| EXACT | 1 | berserkers-technique |
| CLOSE | 8 | arthetinean-skill-machinist, asuras-path-breaker, barrage-enhancement-artillerist, brawl-king-storm-breaker, control-glaivier, death-strike-sharpshooter, deathblow-striker, demonic-impulse-shadowhunter |
| APPROX | 0 | — |
| GAPPED → MAPPED_DOCKET | 2 | blessed-aura-paladin, communication-overflow-summoner |

R-M7 biconditional check: both GAPPEDs are MAPPED_DOCKET; zero APPROX+MAPPED_DOCKET hybrids.

---

## Per-kit one-liners

- **la-arthetinean-skill-machinist** (CLOSE): B-tier DPS, negative-flag CONTRADICTED; Normal+Drone/Joint weave loop, Battery economy, no elemental damage-typing, Hypersync attested but suboptimal — omitting it IS the loop.
- **la-asuras-path-breaker** (CLOSE): Front Attack (DB erratum corrected); Stamina/Shock dual-sub-gauge → Asura Energy → timed Asura Destruction burst_window; Defensive Speculation shield = self_buff; no ailments.
- **la-barrage-enhancement-artillerist** (CLOSE): Generate Barrage Meter → Barrage Mode immobile turret (player-transform-as-turret, totem-approximated) → dump damage → exit no-Exhaustion → repeat; no element.
- **la-berserkers-technique** (EXACT): Fury Meter → timed Burst Mode Z → +30% crit/+20% ATK speed/+36% damage (stale values, shape only) → no Exhaustion on exit; canonical build-spend burst_window; maps cleanly.
- **la-blessed-aura-paladin** (GAPPED → MAPPED_DOCKET): Support-class deferral; Holy Aura party buff/heal has no solo engine loop analog; curse:amplify emitted for Sword of Justice enemy debuff but core party-utility identity is GAPPED.
- **la-brawl-king-storm-breaker** (CLOSE): Non-positional (attested explicit); dual Stamina/Shock perpetual alternation — both gauges always in motion (not standard accumulate-then-release); burst-blows on full Shock consume; novel dual-gauge rhythm.
- **la-communication-overflow-summoner** (GAPPED → MAPPED_DOCKET): Pet-core summoner deferral; Akir-as-buff mechanic UNSUPPORTED per verify_ledger; empty-projection applied; companions-as-damage has no solo engine analog.
- **la-control-glaivier** (CLOSE): Control locks Focus stance out entirely; flat +40% Flurry damage (stale — shape only); Dual Meter used only as buff on three specific skills (not identity release); back-attack positional.
- **la-death-strike-sharpshooter** (CLOSE): Rapid Hawk Meter via Death Strike passive; Silverhawk Assault (Z) deploys hawk debuff (curse:sap for 27% damage-to-boss); 12% damage while hawk absent = second timing state not fully captured.
- **la-deathblow-striker** (CLOSE): Strict 3-orb all-consume gate; Lightning NOT emitted (Lightning Tiger Strike = name only, hot-fact honored); back-attack positional; build-and-detonate identity maps cleanly but multiplicative per-orb scaling lost.
- **la-demonic-impulse-shadowhunter** (CLOSE): Near-permanent demon form (Eternal Blood) = PERMANENT burst per §LA row 2 → self_buff steady-state; Blood/shadow NOT emitted (name-only flavor); Shadowburst Meter accumulate-to-form loop.

---

## T4-door frequency

| T4 token | Count |
|---|---|
| TEMPORAL_CHARGE | 9 |
| MOMENTUM_CASCADE | 4 |
| CLOSE (door) | — |
| ZONE_CONTROL | 1 |
| DEFENSIVE_TRADEOFF | 1 |
| NETWORK_AMPLIFIER | 1 |
| RESONANCE_LOOP | 1 |
| PROXY_ASCENSION | 1 |
| RESOURCE_CONVERSION | 1 |
| PHASE_MOMENTUM | 1 |

TEMPORAL_CHARGE dominant (9/11 kits) — LA gauge-identity kits almost universally accumulate-then-release.

---

## Candidate files

- **mint-candidates-batch-n01.jsonl:** NOT CREATED (zero mint candidates this batch — no novel quantitative/qualitative mint forced; all kits mapped or docketed via existing classes).
- **docket-candidates-batch-n01.jsonl:** 2 entries: `support-class-identity` (blessed-aura-paladin) · `summoner-deferral-pet-core` (communication-overflow-summoner).


---

## §0 near-misses: elements/statuses wanted but not attested

**Elements I wanted to emit but could not (D4 NAME-ONLY LAW blocked all):**
- **lightning** (deathblow-striker): Lightning Tiger Strike is a skill name; hot-fact confirmed — highest-prob lightning at crawl but no in-store damage-typing descriptor. Blocked.
- **shadow / dark** (demonic-impulse-shadowhunter): Blood Demon, Blood Vortex, Shadowhunter class flavor — all name-only. No damage-typing descriptor. Blocked.
- **fire** (barrage-enhancement-artillerist): Flamethrower, Sea of Fire skill/node names — name-only, zero damage-typing. Blocked.
- **fire** (berserkers-technique): no element candidates even surfaced — correctly element-silent.
- **holy** (blessed-aura-paladin): Holy Aura, Heavenly Blessings — all class/skill name flavor. No damage-type descriptor. Blocked.

**Statuses I wanted to emit but could not (attestation law blocked):**
- **stun** (asuras-path-breaker, brawl-king-storm-breaker, deathblow-striker): Stagger/Shock language present throughout — all boss-break vocabulary per §LA row 4, never a 16-ailment emit.
- **sunder** (asuras-path-breaker): "Destruction" in gem names (Destruction Charger, Destruction damage on pet skills) — all name-only, no damage-taken-amplification descriptor on a generic effect noun.
- **freeze / chill** (control-glaivier): no cold language attested at all; null is correct.

---

## Anything forced / notable deviations

- **Barrage Mode as totem**: player-transforms-into-turret is approximated as `totem` — closest geometry but source player would note it is a self-transformation, not a placed proxy. Acceptable delivery texture approximation; CLOSE not APPROX because the burst cycle identity maps.
- **Dual-gauge economy (asuras + brawl-king)**: Stamina/Shock as two named sub-gauges feeding one pool (asuras) or alternating perpetually (brawl-king) is a novel economy shape; resource_economy carries it adequately as named keys but the perpetual-alternation rhythm (brawl-king) differs from accumulate-then-release.
- **Silverhawk "hawk absent" bonus** (death-strike-sharpshooter): the 12% damage while hawk NOT summoned creates a second timing loop the engine doesn't directly express — noted in fidelity_notes, not forced into a separate ailment or trigger.
- **Control Glaivier Dual Meter as buff-on-three-skills**: unlike other gauge kits, the Dual Meter here is a buff applicator on specific skills only, not a release button — expressed in resource_economy but acknowledged as a novel sub-use of the economy lane.
- **Communication Overflow mechanics UNSUPPORTED**: empty-projection applied per §E.2 — skills[], motion_frame, economy all empty/null. Docketed for summoner-deferral review-book.

---

**Signed:** gandalf (mapping-author) · 11/11 roster coverage confirmed · batch committed as `gandalf-seam: VDM-1 basin-4 mapping batch-n01 (11 kits)`
