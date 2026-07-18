# VDM-1 Stage-2 — PoE1 mapping batch-01 summary

**Date:** 2026-07-18 · **Author:** gandalf-seam mapping author (SPEC-AUTHOR; delegated hand under gandalf-prime) · **Batch:** 01 (12 kits) · **Provenance:** `authored-vdm1` · **Crosswalk law:** `2026-07-18-vdm1-crosswalks.md`

## Grade histogram

| Grade | Count | Kits |
|---|---|---|
| EXACT | 1 | arc |
| CLOSE | 8 | aegis-max-block, archmage, armageddon-brand, aurastacker, ball-lightning, bane, baron-zombies, blade-flurry |
| APPROX | 2 | animate-weapon, autobomber |
| GAPPED | 1 | aurabot |

Terminal states: 11 `MAPPED`, 1 `MAPPED_DOCKET` (aurabot).

## Per-kit one-liners

1. **aegis-max-block** — CLOSE. Block-triggers-ES-recovery defensive loop → on-block-successful trigger + resource-fill + TH `damage_taken_converts_shape`; DEFENSIVE_TRADEOFF / RETRIBUTION_ENGINE. Delivery-agnostic offense = single_target placeholder. Block-cap is a numeric def-bin rider.
2. **animate-weapon** — APPROX. Transient poison-proxy swarm (shadow, PROXY_FISSION) lands, but the signature "ground-lying weapons ARE the summon ammunition; loot-drop-stream = resource pool" has no engine lane → docketed. Bladefall = multi_projectile feeder; animated weapons = totem-proxies w/ poison.
3. **arc** — EXACT. Textbook chain geometry + lightning + per-chain damage growth (native chain-scaling). Shock→**sunder** (false-friend handled). ELEMENTAL_ECHO.
4. **archmage** — CLOSE. Mana-as-weapon → RESOURCE_CONVERSION (exact); MoM/Indigon economy warps land in resource_economy (cost_slope escalating). Ball Lightning drift-tick orb = geometry friction (approx `circle`).
5. **armageddon-brand** — CLOSE. Attach-emitter-mark + periodic meteor → trigger_grammar (mark_identity + burst-damage) + ground_targeted_circle. Timed-proc-while-marked approximated to on-mark-apply. Brand Recall = mark-relocation (blink handle).
6. **aurabot** — GAPPED / MAPPED_DOCKET. Ally-buff-projection (party-support) has no solo-scope lane; "useless solo" per source. Aura shell + clamped reserve mapped; identity docketed as scope-boundary.
7. **aurastacker** — CLOSE. Self-stacking aura-network → NETWORK_AMPLIFIER (solo-viable, unlike aurabot). ~100% reserve clamped to 0.75 LOCKED cap. water/cold (Call of the Brotherhood).
8. **autobomber** — APPROX. On-kill propagation → GEOMETRY_PROPAGATION_cascade; dual-element (cold shatter + lightning explosion); freeze + shock→sunder. UNBOUNDED cascade truncated to MAX_CHAIN_DEPTH=1 (never minted). §7.2 dominant loop = movement (dash_attack).
9. **ball-lightning** — CLOSE. Same drift-tick orb geometry friction as archmage (approx `circle`); here the orb IS the identity. Mine throw/detonate chassis via trigger_grammar + activation-toggle. shock→sunder + blind (Saboteur).
10. **bane** — CLOSE. Chaos DoT (→**drain** ailment, not poison) + curse-bundle (Despair→curse:sap, Enfeeble→curse:weaken, Temporal Chains→curse:decrepify) + per-curse multiplier → NETWORK_AMPLIFIER. ground_targeted_circle.
11. **baron-zombies** — CLOSE. Str-stacked zombie army → PROXY_ASCENSION + attribute-affix (STR→minion count/power) + TH leech (1000-STR). Physical-melee proxies = element-neutral (physical rule). ground_slam per-zombie.
12. **blade-flurry** — CLOSE. Channel-stack-release → PC tick-cost + charge-stack accumulator + TEMPORAL_CHARGE. Physical → element-neutral; Voidheart poison+bleed. Frontal-close-AoE approx `melee_arc`.

## T4-door frequency

| Door | Count | Kits |
|---|---|---|
| ELEMENTAL_ECHO | 4 | arc, archmage, armageddon-brand, ball-lightning |
| GEOMETRY_PROPAGATION_cascade | 4 | arc (alt), armageddon-brand, autobomber, ball-lightning |
| NETWORK_AMPLIFIER | 3 | aurabot, aurastacker, bane |
| RESONANCE_LOOP | 2 | aurabot, aurastacker |
| PROXY_ASCENSION | 2 | animate-weapon (via FISSION pair), baron-zombies |
| RESOURCE_CONVERSION | 1 | archmage |
| DEFENSIVE_TRADEOFF | 1 | aegis-max-block |
| RETRIBUTION_ENGINE | 1 | aegis-max-block |
| PROXY_FISSION | 1 | animate-weapon |
| PROXY_SOVEREIGNTY | 1 | baron-zombies |
| TEMPORAL_CHARGE | 1 | blade-flurry |
| MOMENTUM_CASCADE | 1 | blade-flurry |
| PERSISTENCE_ENGINE_saturation | 1 | bane |

Observation: this batch is PoE-alphabetical (aegis→blade), which front-loads **caster/aura/summoner** archetypes. ELEMENT (echo/conversion) and GEOMETRY_PROPAGATION dominate; near-total absence of the pure-melee-strike and single-target-nuke doors is a sampling artifact of the alphabetical slice, not a corpus signal. The steward should expect the door-distribution to rebalance across later batches.

## Mint / docket candidates

- **Docket candidates: 2** (`docket-candidates-batch-01.jsonl`)
  - `animate-weapon`: ground-dropped-item-consumption-as-summon-fuel resource-substrate — no engine lane.
  - `aurabot`: ally-buff-projection (party-support) in a solo-only engine — scope boundary, not a mintable mechanism.
- **Mint candidates: 0** (file not written). Two over-ceiling cases arose and were BOTH resolved by approximation against LOCKED ceilings, which is correct parsimony-ladder behavior — NOT a mint:
  - autobomber's unbounded kill-cascade vs `MAX_CHAIN_DEPTH=1 LOCKED` → APPROX + note (charter: deeper-chain source → APPROX, never a depth mint).
  - aurabot + aurastacker ~100% reservation vs `reservation_percent 0.75 LOCKED cap` → clamped in-map. Minting against a LOCKED cap is a Matt-ruling boundary, not an author mint.

## Anything that felt forced (geometry / ailment / precedence stretches)

1. **The Ball-Lightning orb has no clean 26-geometry.** A slow-drifting projectile that ticks a small AoE every 150ms with *inverse-velocity* damage (slower = more hits) appears in TWO kits this batch (archmage, ball-lightning) and both were approximated to `circle` (tick-AoE around the dwell point). The drift + inverse-velocity is a *behavioral* property the geometry enum simply doesn't carry. If PoE1 later batches keep surfacing drift-tick orbs (Orbiting variants, Storm-family), the steward may want a phrase-book ruling: "drift-tick orb → `circle` (canonical) + behavioral note" so authors stop re-deciding it.
2. **PoE shock → sunder (false-friend) fired 4×** (arc, archmage, autobomber, ball-lightning). Handled per §2 every time. Worth a steward spot-check since it is the single most seductive mis-map in the PoE corpus and I want the 25% audit to confirm I never let `shock` (paralysis) leak in.
3. **Reservation cap tension (0.75 LOCKED vs ~100% source).** Both aura-reservation kits push past the cap. Clamping is correct, but the *feel* delta (a full-reserve build clamped to 75%) is real and I flagged it in each fidelity_note. Steward call whether the 0.75 cap should ever flex for the reservation-identity archetype (I did NOT assume so).
4. **Bane's chaos DoT → `drain`, not `poison`.** Tempting to reach for `poison` (chaos, stacking-feel), but Bane is a hex-DoT not a venom-stacker; §1/§2 route chaos-DoT/decay → drain. Called out because it's a plausible audit flag.

## Template friction (first-batch calibration duty)

Honest report on brief/crosswalk/schema ambiguities the steward should resolve before scaling to the remaining 7 batches:

1. **`t4_doors` token spelling — base vs Layer-2-suffixed.** Crosswalk §5 writes `GEOMETRY_PROPAGATION_cascade` / `_overkill` and `PERSISTENCE_ENGINE_uptime` / `_saturation`, but the engine `t4_catalog_v2.py` enum has only the BASE tokens (`GEOMETRY_PROPAGATION`, `PERSISTENCE_ENGINE`) — the suffixes are Layer-2 *variants* (CAPSTONE_LAYER2), and the brief says "mapping only picks the STRATEGY; never re-pins Layer-2." **I used the crosswalk's suffixed spelling** (since the crosswalk is THE LAW and authored them that way), treating the suffix as the door-token the crosswalk intends. But this arguably *is* naming a Layer-2 variant, which the brief says not to do. **Steward ruling needed:** should `t4_doors` carry the base strategy token only (`GEOMETRY_PROPAGATION`) or the crosswalk's variant-suffixed form (`GEOMETRY_PROPAGATION_cascade`)? My validator accepted both; pick one for cross-batch consistency. This is the single most likely source of cross-author drift.

2. **`scaffold.chain_count` — no guidance; I defaulted every kit to 2.** The canonical shape shows `"chain_count": 2` and the chain-link law says engine chains are length {2,3}, but the brief gives no rule for WHEN a kit is 3 vs 2. I set all 12 to 2 (safe floor; none of these kits obviously demanded a 3-length chain). If chain_count is meant to reflect the kit's identity-skill count or its support-lane density, that rule isn't stated. **Steward ruling needed:** what determines chain_count, or is 2 the universal default and 3 reserved for a named condition?

3. **Curse-subtype notation in the `ailments` array.** The registry writes curse as `curse{amplify, weaken, decrepify, sap}`. I emitted subtypes as `"curse:weaken"` etc. (colon-delimited) in the ailments array. The crosswalk and ailments.yaml treat the variant as a separate emission-time enum, not necessarily a colon-suffixed ailment string. **This notation was my choice** — if the schema expects bare `"curse"` in ailments + the variant recorded elsewhere, my rows need a reshape. Flagging because bane carries three curse subtypes and it's the most consequential place this notation lands.

4. **`resource_economy` "only deviating keys" — deviation FROM WHAT baseline?** The brief says include "ONLY keys deviating from identity defaults (the default corner is a no-op)." The *identity defaults* (per-chassis default corner) aren't enumerated in the brief or crosswalk — resource_economy.py has 40 keys with enums but I don't have the per-identity DEFAULT values to diff against. I included keys I judged clearly load-bearing (e.g. `reservation_percent: 0.75`, `cost_slope: escalating`) and left the object empty where the chassis default suffices. **Steward ruling needed:** is there a per-identity default table authors should diff against, or is "clearly load-bearing deviation, author judgment" the intended bar? I operated on the latter.

5. **`trigger_grammar` enum for TIMED procs.** `proc_trigger_condition` has on-hit-threshold / on-crit / on-cast-linked / on-kill / on-damage-taken / on-mark-apply / on-mark-consume / on-block-successful / on-ailment-application / on-defender-death — but NO member for "timed proc while a mark/condition is active" (armageddon-brand's periodic meteor, aegis's continuous block-loop). I approximated to `on-mark-apply` (brand) and `on-block-successful` (aegis). Brand's meteor genuinely fires on a TIMER while attached, not on the apply event. **Steward note:** if timed-while-marked procs are common in later batches (brands, totems, ground-DoT emitters), the enum may want a `timed-while-active` member, or a documented ruling to fold them to on-mark-apply. Not a mint request — an enum-coverage observation for the steward's audit.

6. **`mark_identity` / `consequence_type` free-text vs enum.** `mark_identity` is clearly free-text (I wrote descriptive strings). `consequence_type` has an enum (apply-mark/consume-mark/linked-cast/resource-fill/ailment-overwrite/burst-damage) which I respected. `trigger_chain_shape` (apply-only/consume-only/apply-consume-pair) also respected. No friction here — noting it worked as specified so the steward knows these three sub-keys behaved.

7. **Minor:** the brief's canonical `mapping_json` shows `resource_economy: {"<key>": "<value>"}` with string values, but several resource_economy values are naturally numeric (`reservation_percent: 0.75`). I emitted numeric where numeric (0.75 as a float, not "0.75"). If the schema wants all-string values, that's a reshape. Assumed native types are fine.

---

**Signed:** gandalf-seam mapping author (SPEC-AUTHOR discipline; delegated authoring hand). **For:** gandalf-prime steward audit before Stage-2 scale-out.
