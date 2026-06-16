# Keystone Implementation — Design-Conformance Review (gandalf)

**Date:** 2026-06-16
**Author:** gandalf (story-and-design steward)
**Mode:** Pattern A-deep — design-conformance review of MY OWN keystone contract's implementation. Authorized autonomous run; KR coordinating; Matt not in loop.
**Independence:** Rendered conclusion-free relative to jack-ryan, who is gating the same two commits TECHNICALLY in parallel. I did NOT coordinate with him. This is the DESIGN verdict — does the implementation faithfully realize the *meaning* of the measurement, especially the parked and spec'd items.

**Reviewed:**
- **Half A — rocket gear materialization (contract §3 + §7.1):** code `c4f20f6` (`generation/keystone_loadout_materializer.py`); math-note `54e6304` (`generation/math/keystone-gear-materialization-2026-06-16.md`).
- **Half B — gamora node-wire (contract §2 + §7.2):** code `85f5c97` (`simulation/combatant.py` flag-gated `from_player_class(apply_max_profile_investment=False)`); math-note `76a74a0` (`simulation/math/keystone-max-profile-node-wire-2026-06-16.md`).

**Governing spec:** `canonical/story/representative-loadout-measurement-contract-2026-06-16.md` (the keystone I authored).

---

## VERDICTS (one line each)

| Half | Verdict |
|---|---|
| **Half A — rocket gear materialization** | **ENDORSE** |
| **Half B — gamora node-wire** | **ENDORSE** |
| **Set-bonus park (§6) — Matt's call preserved?** | **YES — untouched; nothing pre-empted** |
| **Sequencing (§7.3) — both stopped at ~90% boundary?** | **YES — neither performed the parked live integration** |
| **Must anything surface to Matt on DESIGN grounds NOW?** | **NO new park.** The pre-existing §6 set-bonus-content park (6a vs 6b + magnitude) remains the ONLY open design decision, exactly as the contract framed it. Confirmed below. |

Both halves conform. No meaning-drift. The things I PARKED were respected; the things I SPEC'd were honored faithfully, not approximated.

---

## 1. §2 node-profile fidelity (Half B) — ENDORSE

**Question:** does max-profile (15 active / 5 passive → 1.0× multipliers) + the T4-as-tier-4-cap reduction faithfully realize "the kit measured at its true investment"? Any meaning-drift in gamora's reduction?

**Finding: faithful. No drift.** Verified by code-read + empirical check:

- **The 15/5 caps are CANONICAL, not invented.** `per_skill_emitter.NODE_MAX_ACTIVE = 15`, `NODE_MAX_PASSIVE = 5`, `PATTERN_1_FLOOR = 1.0 - 0.65 = 0.35`. The wire imports these constants; it introduces no new balance numbers. This is exactly contract §2.2 ("15 is the per-node cap, not a budget") realized as code.
- **The construction property holds exactly.** Empirically: `compute_investment_multiplier_p1(15, 1.0) == 1.0` and `(0, 1.0) == 0.35`. The wire closes precisely the 0.35×→1.0× gap the contract identifies (§2.1; math-note §2). Passive magnitude is re-baked to `base_at_max × 1.0` — the Pattern-2 1.0× construction property (contract §2.1 line 74), matching `_patch_kits_option_a`/`_patch_kits_profile("max")` semantics exactly.
- **The T4-as-tier-4-cap reduction is the CORRECT reduction — and it strengthens, not weakens, the contract.** gamora's empirical finding (math-note §3) is that there is NO boolean `t4_unlocked` gate inside the fight seam; T4 is realized through (a) presence/availability of the tier-4 skill and (b) the orthogonal `t4_alteration_output` channel, neither of which is an investment input. So "T4 unlocked at the measured point" reduces to "the tier-4 node carries max investment, like every other node." **This is a faithful — indeed more honest — realization of contract §2.3.** My contract said "the kit's single algorithm-chosen T4 is unlocked (Mode A)." The reduction confirms that, at the measurement layer, "unlocked" was never a *separate mechanism* to build — it is subsumed by cap-everything. The `t4_unlocked = True` boolean in `construct_profile_distribution(kit,"max")` is a *gauntlet-config* concern (consumed by `_build_t4_context_configs`), not a fight-multiplier input. gamora correctly declined to invent a parallel T4 gate. **No drift; the reduction realizes my intent without adding mechanism — which is exactly Discipline #11/#12 done right.**
- **D66 one-T4-at-a-time is preserved.** The wire caps "whatever T4 node is in `player_class.skills`" — it does not unlock multiple variants. Matches contract §2.3 (primary variant only; per-variant measurement is a separate downstream concern).
- **No in-place mutation.** `_apply_max_profile_investment` uses `model_copy` — the original skill list is untouched (empirically confirmed: orig active ip stays 0). This is what makes flag-OFF byte-identical and the measured point deterministic + reproducible (contract §4). Good.

**One design-grade observation (not a non-conformance, registered for the integration):** the alteration channel (`t4_alteration_output`) is left UNTOUCHED by the node-wire (math-note §3 park P1). At the staged node layer this is correct — the contract's §2 is purely the *investment* half. But the contract's §3.2 ("the measured kit's gear *reinforces its own build*, aligned to the kit's chain + algorithm-chosen T4") means the FULL measured point must, at integration, ensure the primary T4's alteration arithmetic is in fact populated and flowing. gamora's P1 park names exactly this. It is correctly deferred to the §7.2-step-3+ integration, not a node-wire concern. I flag it only so the integration dispatch does not lose it: **the T4 the gear is attuned to (rocket Half A) and the T4 whose alteration channel fires (gamora) must be the SAME variant at the live measurement, or the kit is measured with gear reinforcing one T4 and arithmetic from another.** Park P1 is the right home for this; no action now.

---

## 2. §3 gear fidelity (Half A) — ENDORSE

**Question:** does "kit's own selected_weapon as Legendary-T1 identity surface" + 11-slot Legendary-T1 on the affinity matrix honor the gear intent? Is the identity-surface semantics (weapon-as-envelope) preserved, or flattened into a generic stat block?

**Finding: faithful. The identity surface is PRESERVED, not flattened.** This was my single sharpest worry going in — a measurement that strips the weapon to a stat-stick measures the kit *without its identity* (contract §3.3, recognition §3). rocket honored it:

- **The weapon IS the kit's own `selected_weapon`, not a generic best-weapon.** `materialize_legendary_t1_weapon` takes the kit's `selected_weapon` dict and extracts `_WEAPON_IDENTITY_KEYS` — `weapon_type_family`, `primary_stat`, `proxy_geometry_class`, `proxy_range_class`, `proxy_tempo_class`, `element_affinity_modifiers_json`, `base_type_id`, `name`. The smoke output confirms this rides through intact (e.g. the mana caster's "Emberreach Staff" carries `caster-arcane / INT / projectile / long / moderate / {fire:0.8, wind:0.2}`). **This is the weapon-as-ENVELOPE preserved** — the geometry/range/tempo proxy classes that gate the kit's geometry sub-palette travel WITH the materialized instance. A consumer reading this loadout reads THIS kit's identity, not a flattened stat block. Contract §3.3 honored exactly.
- **The modifier surface rolls on the doc-42 affinity matrix, NOT flat scalars.** The weapon rolls as a `GearSlot.MAIN_WEAPON` Legendary-T1 instance through the existing `roll_partition_gear_instance`. The smoke shows the main-hand's dominant categories skew Damage/Crit/On-trigger/build_identity/speed/resource — the matrix's main_weapon triple-primary (doc 42 §2.1). The loadout exposes 8 of 9 categories on the mana sample (only `on_trigger`=0, a stochastic seed outcome, not a structural gap). **This is modifier-surface EXPANSION over the stopgap's 4 flat scalars** (contract §3.2; doc 40 §3.4/D56). The whole point of retiring `compute_balance_gear_stats` is realized.
- **The modifier-surface is summed, not scalar'd.** `MaterializedLoadout` carries the full 11× `PartitionGearInstance` list with their rich modifier surfaces. The `project_loadout_to_gearstats` helper is explicitly marked DIAGNOSTIC-only (for the smoke's comparable summary) and is NOT plumbed into the sim — the rich surface is what survives. Contract §0 ("modifier-surface SUM not scalar") honored.
- **Resource-gating + no-skill-modifier rule inherited correctly.** The smoke confirms cross-resource absence (mana kit shows no rage/stamina filters; rage kit shows `["rage"]` only, no mana leakage). The no-skill-modifier rule holds by inheritance (the partition pool carries no +levels-to-skill modifiers; capability toolkit adds triggered-passives/true-actives only). Contract §3.2 honored.
- **T4-attunement as metadata-content, not scalar.** Every slot carries a T4 annotation (smoke: 11/11 t4_annotation_slots) aligned to the kit's chain + `t4_target_intent`. This is the content-compositional model (D33) — attunement is metadata; the rolled content IS the attunement. Contract §3.2 honored.
- **No new balance constants.** rocket's math-note §1.3 is explicit and verified: the keystone is an ASSEMBLY layer over the existing calibrated pool + tier grid. The only new constant is `_SEED_SPLAY` (a deterministic seed-derivation mixing constant, NOT a balance number — `slot_seed(main_weapon)==base_seed` so the weapon roll is reproducible). This is correct discipline.

**Design verdict:** the gear half is the truest realization of the contract I could have asked for. The identity surface is not merely "kept around" — it is carried as the read-surface (`weapon_identity`) the consumer uses to recover the kit's geometry sub-palette. The kit wears ITS weapon. Endorsed without reservation.

---

## 3. §6 set-bonus park — RESPECTED (zero set pieces; Matt's call intact)

**Question:** confirm rocket built ZERO set pieces and correctly deferred the 4 set slots to the magnitude ruling (6a generated-aligned vs 6b fixed-reference). This park must remain Matt's call.

**Finding: respected structurally and explicitly. Nothing pre-empted.**

- **Zero set pieces built.** Every one of the 11 slots is rolled with `set_id=None`. I verified the roller's signature: the set-assembly path only fires when `set_id is not None` (`partition_roller.py:289` "if not None, this is a set piece; assembles set bonus definition"). With `set_id=None` uniformly, NO set bonus is assembled on any slot. All 11 are NON-SET Legendary T1 — the "non-set ceiling" (contract §7.3).
- **The deferral is explicit and correct.** The module docstring, math-note §0/§5 (JC-1), and the code comments all state: the 4 set-piece slots are PARKED on Matt's §6 ruling; at integration, 4 of these non-set slots SWAP to set pieces. rocket did NOT pick 6a or 6b; did NOT invent a reference-set magnitude; did NOT pre-empt the band-ceiling decision.
- **My lean (6b-for-keystone / 6a-as-shipped) was NOT auto-adopted.** Good — it was a recommendation, not a ruling (contract §6.3). rocket correctly treated it as un-decided. The magnitude of any reference set sets the band ceiling, so it is genuinely Matt's call, and it stays Matt's call.

**This park remains the ONLY open design decision in the keystone, exactly as the contract framed it.** Nothing in either half narrowed Matt's option space.

---

## 4. §7.3 sequencing — RESPECTED (both halves stopped at ~90%)

**Question:** confirm both halves stopped at the "determined ~90%" boundary and did NOT perform the parked live integration (consume real gear + re-measure the archive).

**Finding: both halves are production-inert. Neither crossed the boundary.**

- **Half A (rocket) did NOT:** modify/retire `compute_balance_gear_stats` (the stopgap — §7.1 step 4 is gamora's, parked); wire into `balance_loop` or any sim path; build set content. It is a CLEAN SIBLING of the stopgap. The materializer is a standalone additive module. Confirmed by docstring + code (no imports of balance_loop; no edits to gear_catalog).
- **Half B (gamora) did NOT:** consume rocket's real gear; retire the stopgap; re-measure the rogue/gauntlet; re-run the archive. The flag `apply_max_profile_investment` defaults **False**, and when False the branch is not taken (`_measured_skills = player_class.skills` unchanged → `skill_states` byte-identical). I verified empirically: flag-OFF leaves the original skill list unmutated. Production path is byte-identical; no semantic shift.
- **The live integration is correctly named as the LATER coordinated step** in both math-notes (rocket §0/§5; gamora §5.3/§7 P3). Flipping the flag to production is gated on rocket's gear path + the §6 set park + a deliberate decisions-log semantic-shift declaration. None of that was done. **The boundary held.**

This is recognition→validate→commit done correctly: commit the determined additive halves now; the empirical gate (re-measure the rogue at full power) fires at the LATER integration, NOT now. No deletion (1D/b6) can have fired on these — they are inert.

---

## 5. The six surfaced parks (rocket JC-1/2/3; gamora P1/2/3) — disposition

**Question:** are any of these actually DESIGN questions that belong in MY seam to rule on NOW, or do they all correctly defer to Matt / the later integration?

I can resolve TWO as steward right now (they are not Matt-grade design calls — they are measurement-semantics rulings in my lane), and the rest correctly stay parked.

| Park | What it is | Disposition |
|---|---|---|
| **rocket JC-1** (set-piece slots) | The 4 set slots deferred to §6. | **STAYS PARKED — Matt's call.** This IS the §6 Tier-3 park (band-ceiling magnitude). Not mine to resolve. Correct. |
| **rocket JC-2** (loadout total power vs doc-50 band) | If summed 11-slot power lands the kit outside the band at the measured point. | **STAYS PARKED — gamora's acceptance (contract §7.1 step 5), resolved EMPIRICALLY at the re-measure.** Not a rocket re-calibration; not a design ruling I make in advance. The contract §8 prediction 2 registers exactly this (band shifts upward but cross-path variance holds). It resolves the moment gamora re-runs — empirical gate, not a steward decision. Correct to park. |
| **rocket JC-3** (off-hand for 2H weapons) | Should a 2H main-hand null the secondary_item slot AT MEASUREMENT? | **I CAN RULE THIS NOW — and I do (measurement-semantics, my lane). RULING: at the measurement point, a 2H main-hand does NOT null the secondary_item slot — the measured loadout counts all 11 slots regardless of 1H/2H.** Reasoning: the measured loadout is the *calibration ceiling*, the "ideal build the player aspires toward" (contract §1.2 rationale 5; doc 51 §10.1). The band is defined against the structural ceiling, not the realistic in-hand constraint. A 2H wielder at endgame still fills the off-hand-equivalent power budget through the slot taxonomy (the partition 11-slot model treats secondary_item as a distinct slot precisely so the *power surface* is uniform across weapon profiles). Nulling it at measurement would make 2H kits measure ~9% below 1H kits at the ceiling purely from a UI/equip-convention artifact — a measurement bias fighting the "measure the ceiling" principle. This mirrors how PoE balances 2H builds against the full passive+gear ceiling, not a reduced slot count; and how D2 LoD's 2H builds aren't penalized in the synergy-max reference. **So: count all 11 slots; the secondary_item materializes for every kit. rocket already does this (it rolls the slot regardless); my ruling CONFIRMS the materialization is correct and instructs the LATER consumer (gamora's wire) to count it.** Player-consequence: a 2H endgame build and a 1H+offhand endgame build are judged at parity ceilings, so neither weapon profile is structurally penalized by the band. *This ruling is in-lane (measurement-semantics, not a balance-constant) and I record it here as steward; it does not need Matt.* |
| **gamora P1** (alteration-channel completeness under flag) | Should the measurement assert `t4_alteration_output` is populated for the primary T4 when the flag is ON? | **STAYS PARKED — LATER integration (§7.2 step 3+).** But I name the design requirement it must satisfy (see §1 above): at the live measurement, the gear's attuned-T4 and the firing alteration-channel T4 must be the SAME variant. That is the integration dispatch's acceptance criterion, not a node-wire concern. Correctly parked; I've recorded the criterion so it isn't lost. |
| **gamora P2** (which T4 is "primary" for multi-variant kits) | Tie-break when a kit ships multiple in-band T4 variants. | **ALREADY RULED in the contract (§2.3) — the measured loadout uses the PRIMARY (algorithm-default, highest-scored) variant; per-variant measurement is a separate downstream concern.** gamora's wire correctly caps "whatever T4 node is in `player_class.skills`," which IS the primary at the measurement point. So this is not actually open — it's resolved by §2.3, and the wire conforms. I confirm: no new ruling needed; the existing contract ruling stands and the implementation honors it. |
| **gamora P3** (live production adoption / flip flag to ON) | Flip default to ON as the production measurement. | **STAYS PARKED — the coordinated integration itself.** This is a semantic shift (changes the power level every kit is judged at) requiring rocket's gear path + the §6 park + a decisions-log semantic-shift declaration. Exactly the §7.3 boundary. Not now; not without Matt's §6 ruling first. Correct. |

**Summary of park dispositions:** ONE I resolve as steward NOW (JC-3 — 2H counts all 11 slots; recorded above, in-lane, no Matt needed). ONE was already resolved by the contract (P2 — primary variant; implementation conforms). FOUR correctly stay parked (JC-1→Matt §6; JC-2→empirical re-measure; P1→integration with the criterion I named; P3→the integration itself). **No park that belongs to Matt was pre-empted, and no park that I could resolve in-lane was left dangling.**

---

## 6. Does anything surface to Matt on DESIGN grounds now?

**NO new design decision is created by either half.** The pre-existing §6 set-bonus-content park (6a generated vs 6b fixed-reference, + the reference-set magnitude that sets the band ceiling) remains the SINGLE open design call — unchanged, un-narrowed, exactly as the contract framed it. That is Matt's, and it was correctly left untouched.

Everything else is either (a) determined-from-canon and faithfully implemented, (b) an empirical gate that resolves at the re-measure (not a decision), or (c) an integration-step park with its acceptance criterion now recorded. **My JC-3 ruling (2H counts all 11 slots) is in-lane measurement-semantics and does not require Matt — it confirms rocket's materialization and instructs the later consumer.**

When the integration dispatch is authored (the §7.2-step-3+ coordinated step), it should carry forward: (1) Matt's §6 ruling first; (2) the T4-variant-coherence criterion (gear-attuned T4 == alteration-firing T4); (3) my JC-3 ruling (count the secondary_item for 2H kits); (4) the empirical re-measure as the gate that validates JC-2 (band placement) and the §8 predictions.

---

## 7. Sign-off

**Half A — rocket gear materialization: ENDORSE.** The weapon-as-envelope identity surface is preserved (not flattened); the 11-slot loadout rolls on the doc-42 matrix as modifier-surface expansion over scalar; zero set pieces (§6 park respected); no new balance constants; production-inert. Faithful to contract §3 + §7.1 steps 1-2.

**Half B — gamora node-wire: ENDORSE.** The 15/5 caps are canonical; the 0.35×→1.0× construction property holds exactly; the T4-as-tier-4-cap reduction faithfully (and more honestly) realizes §2.3 without inventing a parallel mechanism; flag OFF by default → byte-identical production; no in-place mutation → deterministic. Faithful to contract §2 + §7.2 steps 1-2.

**Sequencing: RESPECTED.** Both halves stopped at the ~90% determined boundary. Neither performed the parked live integration. The boundary held; no deletion fired on stopgap evidence.

**Set-bonus park: RESPECTED.** Matt's §6 call is intact; the only open design decision in the keystone is exactly the one the contract parked.

**Steward ruling recorded (in-lane):** JC-3 — at the measurement point, a 2H main-hand does NOT null the secondary_item; the measured loadout counts all 11 slots for every weapon profile (parity ceilings; no weapon-profile structural penalty).

The implementation is the truest realization of the contract I authored. Both halves conform. No meaning-drift.

**Signed:** gandalf (story-and-design steward), 2026-06-16.
