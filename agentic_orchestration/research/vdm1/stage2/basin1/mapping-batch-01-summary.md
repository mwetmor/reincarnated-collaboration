# VDM-1 basin-1 mapping — batch-01 (m01) summary

**Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-18 · 12 kits, all poe2 (basin-1 spec lines 1-12), dossiers ingest-8 ✓
**Provenance:** `authored-vdm1` — OUR judgment against source-verified dossier facts. Post-cutoff basin: dossier verbatim is sole source-truth; training priors treated as stale.
**Histogram is ADVISORY — steward recounts from `mapping-batch-01.jsonl`.**

## Grade histogram
| Grade | n | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 7 | blood-mage, bonestorm, cof-comet, concoction, erasure-edc-lich, galvanic-shards, gas-arrow-ignite |
| APPROX | 5 | acolyte-darkness, archmage-totems, chronomancer-01, demon-form, gemling-stacker |
| GAPPED | 0 | — |

All 12 `terminal_state: MAPPED` (no GAPPED → no MAPPED_DOCKET row; kits graded un-docketed per parsimony ladder even where they FILE docket-candidates).

## Per-kit one-liners
- **acolyte-darkness** APPROX — chaos→shadow melee striker; Waking Dream Darkness = Spirit-reservation swap (FALSE-FRIEND) + on-kill Remnant fill; novel pickup-resource lost. Era ERRATA-16 respected.
- **archmage-totems** APPROX — totem-Spark proxy maps clean, but mana-as-weapon coupling degrades to cost_scale note; 3-way combo joint-attestation WEAK (conf 0.45) flagged.
- **blood-mage** CLOSE — physical (element-neutral) multi_projectile + Impale→sunder + on-kill Life-Remnant vacuum; hp_cost_scale clamped 0.30; overheal-150% → docket.
- **bonestorm** CLOSE — physical channel-release multi_projectile; Impale→**sunder** (not bleed); channel = wind-up accumulator; Bone Cage placed_lane (thin).
- **chronomancer-01** (neg) APPROX — Time Freeze→**stun** (mass, dur-capped, not freeze); Time Snap cooldown-reset → docket; trap-canon UNLAUNDERED (wild-strike precedent).
- **cof-comet** CLOSE — R-M9 chassis: Cast-on-Freeze = self_buff + trigger_grammar; Frostbolt→freeze→Comet (ground_targeted_circle), depth-1 LOCKED; cold→water.
- **concoction** (neg) APPROX-adjacent→CLOSE — poison-flask ground_targeted_circle, chaos-poison→earth; flask-charge-ammo→cycle; era ERRATA-17 floor-extended; honest map.
- **demon-form** APPROX — **GX-02 fired**; form=self_buff, fire primary (element ambiguous — attested builds use Spark/lightning); Demonflame ramp EXCEEDS hp_cost_scale 0.30 → clamped.
- **erasure-edc-lich** CLOSE — **Erasure PHANTOM** removed per C.6 binding; maps as clean ED/Contagion chaos-DoT + on-kill GEOMETRY_PROPAGATION; chaos→shadow, ED→drain, exposure→curse:amplify.
- **galvanic-shards** CLOSE — armour-break→**sunder** (hit-proc); two-stage fragments→beams, dominant=fork fan-out + PROPAGATION door for beam stage; shock rider kept distinct.
- **gas-arrow-ignite** CLOSE — two-stage cloud→detonate, dominant=detonation ground_targeted_circle; fire+earth hybrid, burn+poison; phys-to-fire conversion door.
- **gemling-stacker** APPROX — attribute-stack→flat-damage is the whole engine; NOT docket #8 (stat→count) → own docket-candidate; lightning+water, shock+freeze; melee_arc shell survives, stacker fantasy hollowed.

## T4-door frequency
`4 GEOMETRY_COLLAPSE · 4 GEOMETRY_PROPAGATION · 3 SACRIFICE_ASCENDANCY · 2 RESOURCE_CONVERSION · 2 PERSISTENCE_ENGINE · 1 each: PROXY_ASCENSION, NETWORK_AMPLIFIER, RETRIBUTION_ENGINE, TEMPORAL_CHARGE, ZONE_CONTROL, ELEMENTAL_ECHO, PHASE_MOMENTUM, ELEMENT_CONVERSION_PHYSICAL.` All base ENGINE tokens (R-M1); crosswalk _cascade/_uptime suffixes folded to base per R-M1.

## Geometry values
`4 ground_targeted_circle · 3 multi_projectile · 3 self_buff · 2 melee_arc · 2 single_target · 1 each: totem, placed_lane, ring, fork.` All 26-enum members (verified vs geometry_constants.py + crosswalk §6).

## Candidates
**mint-candidates:** NONE. Every two-stage geometry resolved to an existing 26-token via §7.2 dominant-loop; no accumulator reshaped geometry (no crackling-lance-class mint forced).
**docket-candidates (3)** — `docket-candidates-batch-01.jsonl`:
1. **overheal-above-max-life buffer** (blood-mage; steward consolidates w/ grim-feast b02 per §B watch-item).
2. **cooldown-reset burst** (chronomancer Time Snap; no native key zeroes cooldowns).
3. **attribute-total→flat-damage coupling** (gemling; DISTINCT from docket #8 stat-as-army-size — stat-as-DAMAGE).

## GX-02 / watch-item flags FIRED
- **GX-02 form-swap:** poe2-demon-form (Demon Form entry) — flagged in fidelity_notes, no numbering; accrues to standing form-swap register. (acolyte GX-05, archmage/gemling GX-07, cof GX-17, concoction GX-14, blood-mage GX-06, gas-arrow GX-03 are corpus gx tags, not form-swap gates — only demon-form's GX-02 is the form-swap class.)
- **hp_cost_scale 0.30 clamp fired:** blood-mage (Sanguimancy, source rate unquantified) · demon-form (Demonflame EXCEEDS 0.30, ramps unbounded w/ Mastered Darkness). Both accrue to review-book clamp list.
- **overheal-above-cap watch-item fired:** blood-mage (150% max life) → docket-candidate (§B).
- **cooldown-reset watch-item fired:** chronomancer (Time Snap) → docket-candidate (§B).
- **HoWA stat→damage watch-item fired:** gemling → own docket-candidate, NOT docket #8 (§B / C).
- **Two-tier accumulator watch-item:** NOT fired this batch (no Rage→Glory-class second tier attested in these 12; nearest are single-tier accumulators: Demonflame, Bonestorm channel, crossbow ammo cycles).
- **Erasure phantom handled** per C.6 binding (mapped from ED+Contagion only, graded as if Erasure nonexistent).

## What felt forced (honest flags for steward audit)
- **gemling-stacker** — the closest to GAPPED. The entire identity (attribute-stack-AS-damage) has no engine lane; kept APPROX because the melee shell maps + the gap is a docket-able quantitative coupling, not an unmodelable mechanism. Steward should sanity-check APPROX-vs-GAPPED here.
- **chronomancer** — also APPROX-bordering-GAPPED: BOTH signature mechanics (literal time-STOP, and the cooldown-reset engine) degrade — stun≠time-stop, and cadence_scale≠cooldown-zero. Two identity-level losses on one kit.
- **archmage-totems** — the joint attestation is genuinely weak (conf 0.45, "not confirmed in a single source"); if the Oracle+Archmage+Totem synergy is a phantom-combo the kit is really just totem-Spark. Mapped components honestly, flagged.
- **demon-form element** — corpus says fire; dossier says attested fetched builds run Spark (lightning) in-form and "element is not locked to fire." Honored corpus fire per the row but a lightning override would be equally legal — steward may prefer the attested-build element.
