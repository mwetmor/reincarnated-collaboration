# VDM-1 Stage-2 PoE1 mapping batch-08 — summary (FINAL PoE1 batch)

**Author:** gandalf-seam mapping author · **Date:** 2026-07-18 · **Kits:** 10 (venom-gyre, viper-poison, wander, warchief, ward-loop, whispering-ice, wild-strike, winter-orb, woc-ignite, wormblaster)

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 0 | — |
| CLOSE | 4 | viper-poison, warchief, winter-orb, woc-ignite |
| APPROX | 3 | venom-gyre, wander, whispering-ice |
| GAPPED | 3 | ward-loop, wild-strike, wormblaster |

Terminal states: 7 MAPPED, 3 MAPPED_DOCKET (R-M7 1:1 pairing verified programmatically).

## Per-kit one-liners

- **venom-gyre** (APPROX): throw-catch-dash poison magazine — accumulator + dash_attack carry the fill/spend rhythm; stack-count→burst-size binding has no lane (mint accrual filed). Earth family per venom register. Eras post-errata.
- **viper-poison** (CLOSE): melee poison stacker whose kills pop contagion — lands on GEOMETRY_PROPAGATION_cascade natively. Eras post-errata (3.8 debut).
- **wander** (APPROX): Kinetic Blast impact-cluster approximated as multi_projectile; blast-overlap wall-shotgun tech lost; physical rule → element-neutral + ELEMENT_CONVERSION_PHYSICAL door; Power Siphon cull = execute.
- **warchief** (CLOSE): totem geometry + PROXY_ASCENSION are native; only the player-proximity-coaches-totem buff becomes flavor.
- **ward-loop** (GAPPED): the engine can express the reactive CWDT hop but not the CLOSED loop (self-generated damage-taken re-entering its own trigger; no minion-death→self-damage lane; MAX_CHAIN_DEPTH=1 LOCKED). Perpetual-motion-in-an-empty-room is the identity → docket. Eras post-errata (Ward debuts 3.15).
- **whispering-ice** (APPROX): item-keystone kit ruled MAPPED — stat-stacking HAS lanes (native caster-stat scaling + attribute-stack gear affixes + RESOURCE_CONVERSION); lost the stat→DURATION binding; staff dissolves per crosswalk §4.
- **wild-strike** (GAPPED, negative=1): per-hit random element AND random secondary geometry; second accrual of the elemental-hit RNG-pool docket, gapped worse (no pruning endpoint exists). Trap-canon mapped honestly, not laundered.
- **winter-orb** (CLOSE): charge-then-cruise personal turret — orbit + accumulator + PERSISTENCE_ENGINE_uptime; explicitly NOT the R-M6 drift-tick class (self-anchored, not travelling). Era post-errata (3.5-3.6 single-era peak).
- **woc-ignite** (CLOSE): cone + burn + sunder (exposure via application-shape rule) all native; PERSISTENCE_ENGINE base token per R-M1 (variant unclear).
- **wormblaster** (GAPPED, weakest facts): mechanics claim UNSUPPORTED (403'd; 3.3 variant contradicts) — mapped on the attested flask-worm invariant only; self-supplied victim-fodder has no lane; conf-caveated docket per heavy-strike-stun precedent.

## T4-door frequency

TEMPORAL_CHARGE 3 · PERSISTENCE_ENGINE_saturation 3 · ELEMENT_CONVERSION_PHYSICAL 2 · PERSISTENCE_ENGINE_uptime 1 · PERSISTENCE_ENGINE (base) 1 · GEOMETRY_PROPAGATION_cascade 1 · PROXY_ASCENSION 1 · RETRIBUTION_ENGINE 1 · SACRIFICE_ASCENDANCY 1 · RESOURCE_CONVERSION 1 · PHASE_MOMENTUM 1 · ELEMENT_CONVERSION_MONO 1 · PROXY_INVERSION 1

## Candidates

- **Docket (3):** ward-loop closed-loop self-damage trigger economy · wild-strike RNG-element+geometry roll (ACCRUAL → consolidate with elemental-hit family) · wormblaster synthetic-victim fodder supply (5th member of the entity-as-consumable-resource-pool family; conf-caveated).
- **Mint (1, qualitative):** venom-gyre stack→release-projectile-count binding — 2nd accrual instance of the batch-02 crackling-lance stack-parameterizes-geometry candidate (graduation threshold evidence, not a duplicate mint).

## What felt forced

- **self_buff as geometry for trigger-chassis meta-gems** (CWDT in ward-loop, CoC in wormblaster): the 26-enum has no "no-geometry meta-carrier" member; self_buff + a "carried in trigger_grammar" note is the least-bad slot. If more trigger-chassis kits accrue in D2-D4/LE batches, a steward convention note would help.
- **Winter Orb's auto-targeting turret** into `orbit`: nearest player-anchored persistent entity, but orbit is contact-damage semantics; behavioral note carries the projectile emission. Held CLOSE under R-M6 spirit (nearest geometry + note).
- **Wander's impact-cluster** into multi_projectile: honored multi-point footprint, but impact-anchored blast clusters are a recurring PoE shape (KB here; GD/D3 siblings likely) — if a 2nd/3rd impact-cluster kit accrues, consider whether `circle`-at-impact + count param wants a quantitative widen.
- **3 GAPPED in one batch** (vs b04's 2): not grade drift — two were spawner-flagged as structurally weak/loop-locked (ward-loop, wormblaster) and wild-strike is a pre-registered accrual to an existing docket family. All three fail the R-M7 player test cleanly.

**PoE1 mapping now complete through batch-08 (final PoE1 batch).**

---

## STEWARD AUDIT (DRIFT-CRITIC, 2026-07-18) — ACCEPTED as-is

Enum/law sweep CLEAN (geometry / element / ailment-16 / curse-variant / t4 ∪ Layer-2 / chain_count / R-M7 pairing 1:1). Deep-sample 5/10 (the three GAPPED + whispering-ice + venom-gyre). Self-report histogram = file truth. Zero re-grades.

**Three-GAPPED scrutiny — all UPHELD, not grade drift:**
- **ward-loop:** exemplary R-M7 articulation ("full cast throughput in an EMPTY ROOM — perpetual motion is the identity"). MAX_CHAIN_DEPTH=1 template law respected — no depth mint attempted; the reactive half honestly credited as expressible. Also accrues **hp_cost_scale 0.3 at-ceiling instance** to the review-book accumulator.
- **wild-strike:** trap-canon mapped without laundering (negative flag stays on the corpus row); fixed-element approximation would fail "not that build" — correct.
- **wormblaster:** graded on the attested worm-fodder invariant only, UNSUPPORTED mechanics not smuggled into the mapping, conf-caveat per heavy-strike-stun precedent. Model weakest-facts honesty.

**Steward corrections — cross-batch family arithmetic** (root cause: mappers can't see sibling batches; definitive counts live here):
1. **R-M5 TIMED-WHILE-ACTIVE:** whispering-ice's token appears in a NEGATION ("does not apply — storm duration is skill-native"). True accrual count = **2** (seismic-trap b06, storm-brand b07); graduation threshold ≥3 NOT reached. **Brief-amendment candidate (D-3):** greppable tokens must never be emitted in negated form — write "R-M5 considered, not applicable" without the literal token.
2. **stack-parameterizes-geometry family:** venom-gyre = forcing kit **#3** (crackling-lance b02 founding · pizza-sticks b06 · venom-gyre b08), not #2 → graduation case STRENGTHENED at D-4.
3. **entity-as-consumable-resource-pool family:** wormblaster = member **#7** (animate-weapon, bladefall, dark-pact, detonate-dead, minion-pact-bv, reaper, + wormblaster conf-caveated), not 5th.
4. **RNG-element-pool family:** wild-strike = accrual **#3** (elemental-hit founding · skeleton-mages b06 · wild-strike b08).

**Law-reading vindications:** winter-orb's explicit NOT-R-M6 distinction (self-anchored turret vs travelling drift-orb) is a correct reading — CLOSE upheld. woc-ignite base-token PERSISTENCE_ENGINE per R-M1 (variant unclear) correct. `self_buff`-as-trigger-chassis-carrier (CWDT/CoC) accepted as least-bad convention → **R-M8+ wording candidate at D-3** for D2-D4/LE basins. Wander impact-cluster logged as watch-item (2nd/3rd accrual → quantitative widen question).

**Candidates:** docket 3 + mint 1 ACCEPTED as filings (ratification at stage-3 D-4).
