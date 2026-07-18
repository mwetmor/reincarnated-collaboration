# VDM-1 Stage-2 PoE1 mapping — batch-02 summary

**Author:** gandalf (SPEC-AUTHOR; DRIFT-CRITIC self-audit pass) · **Date:** 2026-07-18 · **Batch:** 02 (12 kits) · **Provenance:** authored-vdm1

## Grade histogram
| Grade | Count | Kits |
|---|---|---|
| EXACT | 2 | cleave, cyclone |
| CLOSE | 5 | blood-magic-kit, boneshatter, caustic-arrow, coc-ice-nova, cold-dot-occ |
| APPROX | 5 | bladefall-bladeblast, charged-dash, crackling-lance, cwdt-loop, dark-pact |
| GAPPED | 0 | — |

All 12 terminal_state = **MAPPED** (0 MAPPED_DOCKET — every kit lands via a lane or an honest approximation; the docket candidates are steward-queue substrate-gaps that ride alongside APPROX grades per batch-01 animate-weapon precedent, not kit-terminal gaps).

Candidate counts: **docket = 2**, **mint = 1** (qualitative, un-ratified).

## Per-kit one-liners
- **bladefall-bladeblast** — APPROX. multi_projectile seed -> ring detonation-cascade; physical/no-family. MISS: lingering-blade field as a consumable detonation-queue (field-resource-consume; blade-count = Blade Blast's damage budget). Docketed.
- **blood-magic-kit** — CLOSE. Keystone, not a skill; reservation_resource=hp + hp_cost_scale (engine's LITERALLY-named 'PoE1 Blood Magic guard'). Drift: PoE is total+uncapped, engine clamps 0.30 max-HP/cast.
- **boneshatter** — CLOSE. Trauma = charge-stack accumulator (on-hit-dealt, cap 9) + hp_cost_scale self-damage; ground_slam + stun. Drift: the reset-cliff risk-dance (ride to 9, dread the 10th) + quadratic self-hit approximated.
- **caustic-arrow** — CLOSE. ground_targeted_circle + poison, chaos->shadow; hit-independent DoT-cloud native. Drift: PoE fixed-tick chaos-DoT vs engine stack-additive poison.
- **charged-dash** — APPROX (NEGATIVE kit). dash_attack reposition-strike. MISS: the steerable illusion-phantom + non-overlapping lane-pulses (the single-target flaw) + uncancellable teleport (the danger flaw) — the two mechanics that MAKE it negative. Deliberately not minted.
- **cleave** — EXACT. melee_arc IS the frontal-180-swing; physical/no-family + bleed. Nothing identity-bearing lost. (negative_canon UNSUPPORTED + inference-not-attested per batch note — excluded from grade; a meta-economy 'no lever' claim maps to no mechanism regardless.)
- **coc-ice-nova** — CLOSE (trigger kit). on-crit -> linked-cast (whirlwind host -> ring Ice Nova); cadence_scale carries 'attack-rate becomes cast-rate'. Two smoothings: Cospri parallel 2nd-trigger; CDR server-tick cadence.
- **cold-dot-occ** — CLOSE. Twin of caustic-arrow: two ground_targeted_circle cold pools + chill, water; self-anchored Vortex-at-feet. Drift: fixed-tick cold-DoT vs stacking-ailment; CI/ES facetank is a def-bin rider.
- **crackling-lance** — APPROX. beam_channel + lightning + sunder. MISS: Intensity morphs the GEOMETRY (stacks widen beam + narrow branching, fan->lance) as it ramps damage — no lane binds stack-count -> live geometry. Qualitative mint-candidate filed. Era 3.12-3.13 per verify_ledger errata, respected.
- **cwdt-loop** — APPROX (trigger kit; the MAX_CHAIN_DEPTH=1 collision). on-damage-taken -> linked-cast native at depth 1; the CLOSED self-feeding circuit (consequence re-triggers its cause, depth >1) is LOCKED-out and cannot be minted. Canonical MAX_CHAIN_DEPTH exemplar.
- **cyclone** — EXACT. whirlwind IS spin-to-win; channel-move + radius-hits + leech-sustain native, physical/no-family. Fire/CoC are separate variants, not core. Nothing lost.
- **dark-pact** — APPROX. chain + shadow(chaos) + drain. MISS: proxy-pattern INVERSION — skeletons are consumable BATTERIES whose max-life is the ammo (Minion Life gear scales YOUR damage). hp_cost_scale carries the no-skeleton self-cost fallback (native). Docketed.

## T4-door frequency
SACRIFICE_ASCENDANCY ×4 · ZONE_CONTROL ×4 · GEOMETRY_COLLAPSE ×3 · TEMPORAL_CHARGE ×3 · PERSISTENCE_ENGINE_uptime ×2 · ELEMENTAL_ECHO ×2 · GEOMETRY_PROPAGATION_cascade ×1 · DEFENSIVE_TRADEOFF ×1 · PHASE_MOMENTUM ×1 · RETRIBUTION_ENGINE ×1 · MOMENTUM_CASCADE ×1 · PROXY_FISSION ×1.

Note the SACRIFICE_ASCENDANCY cluster (blood-magic, boneshatter, cwdt-loop, dark-pact) — this batch is heavy on self-cost / life-as-fuel identities, which is a coherent signal, not door-spam: four distinct source mechanics (life-as-resource keystone; trauma self-damage; self-hit trigger loop; minion-life sacrifice) all route to the same capstone family.

## Candidates (steward ratifies before any elrond ingest)
**Docket (2):**
1. `placed-entity-field-as-consumable-detonation-queue` — bladefall-bladeblast. Blade-field is a shared resource Bladefall plants + Blade Blast spends.
2. `proxy-max-life-as-consumable-per-cast-ammo (proxy inversion)` — dark-pact. Skeleton max-life is spent ammo; Minion Life gear inflates the battery.

**Mint (1, qualitative, un-ratified):**
1. `stack-driven geometry morph` — crackling-lance. Intensity stack-count continuously reshapes beam width + branching angle. New mechanism (geometry-parameterized-by-stack), evidence-gated; graduate only on 2nd/3rd forcing kit (R-M5-style accrual).

**STEWARD CONSOLIDATION FLAG:** docket #1 (bladefall) + docket #2 (dark-pact) + batch-01's animate-weapon (ground-item-as-summon-fuel) form ONE recurring family — **'entity-on-the-field as a consumable resource pool spent by a skill.'** Three kits across two batches. The steward may wish to collapse them into a single `entity-as-consumable-resource-pool` docket with a design ruling: either mint one shared resource primitive (entity-count/entity-life -> consuming-skill budget), or rule the substrate flavor-only (approximations canonical). This is the batch's most important design signal — a genuine engine-lane gap, recurring, not a one-off.

## What felt forced
- **cwdt-loop** was the sharpest constraint-collision: the kit's ENTIRE identity (a build that plays itself via a closed self-feeding trigger circuit) is precisely what MAX_CHAIN_DEPTH=1 LOCKS out. This is not a modelling failure — it is the lock doing its job — but grading it APPROX undersells how much of the kit evaporates. The engine gives one triggered cast per external hit; the source gives infinite self-perpetuation. Recorded as the canonical exemplar so future depth-lock discussions have a concrete reference.
- **crackling-lance** forced the only mint because the geometry-morph is genuinely un-approximable in either direction — carry the damage-ramp and you lose the beam-tightening; carry the beam and you lose the ramp. The AoE-vs-damage geometry trade IS the skill.
- **The three self-cost/life-as-fuel kits + the two field-consume kits** made batch-02 feel like a stress test of the engine's resource-substrate expressiveness specifically. The hp_cost_scale 0.30 LOCK appeared as a real magnitude clamp on THREE kits (blood-magic, boneshatter, dark-pact) — worth the steward noting whether 0.30 is the right ceiling given how many canonical PoE identities are uncapped-self-cost.
- **charged-dash** (negative kit): I deliberately declined a mint. Reproducing a known-bad skill's bespoke awkwardness (non-overlapping pulses, uncancellable teleport) violates parsimony — the negative-canon value is the RECORD of why it failed, not a build target. Flagging this as a general principle for negative-kit mapping: approximate the shape, catalogue the flaw in fidelity_notes, do not mint mechanisms to reproduce failure.

## Steward audit addendum (DRIFT-CRITIC, 2026-07-18)
- **ACCEPTED as-is.** Both EXACTs legitimate under the engine-owns-archetype pattern (cleave→melee_arc, cyclone→whirlwind; arc-precedent nativeness test applied — no false engine-behavior claims).
- crackling-lance channel-intensify qualitative mint correctly DEFERRED at 1 forcing kit (steward graduates at a 2nd accrual).
- Enum sweep 12/12 CLEAN (geometry/element/ailment/t4_doors/chain_count; curse notation R-M3-conformant).
- Post-audit histogram: EXACT 2 / CLOSE 5 / APPROX 5 / GAPPED 0. R-M7 conformant (bladefall/dark-pact APPROX/MAPPED is the correct side of the line — identity intact, corpse/blade economy approximated).
