# Finding — 2026-07-16 — ailment-layer (Gate-2, both slices)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-AMENDMENTS (no BLOCK; one spec-amendment CANDIDATE recorded; no owing seam)
**Target:** rocket `6cf00ad·4f40a02·744aeee·488f19d·9a572fa·d0935f2` (tags `rocket/v2.9-ailment-1..4`) + gamora `e2dd87f·0463892·c136f55·579e87a·14fbeec` — engine `main` HEAD `14fbeec`, NOT pushed.
**Developer:** rocket (config/emission slice) + gamora (sim-resolution slice)
**Commissioner:** gandalf (autonomous atlas-parity run, Matt authorization 2026-07-16)
**Principles applied:** #1 (math-before-code), #3 (cross-seam impact / MIGRATION), #4 (decisions-log as truth), #5 (severity), + Disciplines #1, #8, #11, #12; DL-03 stream law; ADR-004 (MIGRATION), ADR-002 (jack-ryan-tier writes).
**Governing law:** `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` — Gate-1 PASS-WITH-AMENDMENTS (c8fcf5b2), 8 inline amendments = the law audited against. Companion Gate-1 finding: `2026-07-16-ailment-layer-spec-gate1.md`.

## Verdict

**PASS-WITH-AMENDMENTS.** Both slices implement the amended spec faithfully. All eight Gate-1 amendments are honored in code. All five §10 escalation rulings landed as ruled. Byte-neutrality holds under inspection AND under a 685-test sim/damage/effect/combatant/proxy regression battery (0 failures). No trivial-and-safe inline fix was owed; nothing named to an owing seam. One spec-amendment CANDIDATE recorded (§5.5 per-defender vs per-attacker) — a documentation reconciliation, not a code defect.

## What I found (descriptive)

**Target 1 — Sunder.** `_compute_sunder_amp` (`damage_resolver.py:85-114`) is single-instance max-magnitude (:104-106), `effective_amp = min(SUNDER_MAX_AMP_CAP=0.50, current_amp)` (:111), GX-15 synergy bonus added THEN cap re-applied (:112-113) — cap-after-add exactly as amendment #1 + sim math §1.2 specify. Composition site is `resolve_skill:496-498`, placed AFTER dmgvar (:488) and BEFORE the physical/elemental mitigation branch (:501) — pre-mitigation lineage confirmed. Byte-neutral: :497 mutates magnitude only when amp > 0. Single-instance refresh has its own dedicated `_add_or_refresh` branch (:1188-1197) taking `max(existing, incoming) damage_taken_percent` — mirrors the F3 DoT law. §7 consecrate×sunder DOUBLE-multiplicative holds: consecrate is `category: amplification`, so `get_dot_ailments` (:387-391) excludes it from `_DOT_AILMENT_NAMES`; consecrate never routes through the DoT-tick amp path in this slice (its zone-DoT mechanism is a separate seam, untouched).

**Target 2 — Freeze.** Shatter placement (`effect_resolver.py:136-151`) fires when `duration_remaining <= 0` (:136), AFTER the tick-loop decrement (:92), BEFORE the expiry cull (:161) — reads the still-live effect object, precisely amendment #2. Threshold 0.25 / shatter 0.20 defaults present in yaml (:254-261). Chill+freeze coexist: `slow_factor` (`combatant.py:399-405`) reads chill entries only; freeze does not contribute and does not clear chill. `can_use_skill` (:433-452) rejects on `is_frozen` (:440). Note: on the terminal tick the DoT-tick block (:95-119) precedes the shatter check (:136) in the same iteration, so a DoT can push the target under threshold and trigger shatter same-tick — genre-consistent, not a defect.

**Target 3 — Stun.** Hybrid DR present in three parts as §10-c requires: universal `stun_immune_remaining` decrement in `tick_effects:79-81`; max-preserving expiry stamp at `:152-158` (`max(current, immunity_after_seconds)`); hard-drop at `_try_apply_ailment:1070-1071`. **RNG-stream discipline VERIFIED:** the hard-drop `return` (:1071) executes BEFORE the RNG gate `did_apply_ailment(... rng.random())` (:1073) — the drop path consumes NO RNG draw, so it cannot silently shift the stream and perturb unrelated seasons. Boss multiplier at :1113-1115 reads `getattr(defender, "is_boss", False)` (safe default; branch dark until spatial-engine wires it). `is_stunned` (:388-396) correctly distinct from `stun_immune_remaining` (docstring :392-394).

**Target 4 — Poison.** Independent-stack via `_add_poison_stack` (`damage_resolver.py:1136-1153`), routed at :1130-1131 — NOT `_add_or_refresh`. FIFO cap eviction: `pop(stacks[0])` drops the oldest (insertion-order == age-order for append) at :1152. Poison is a `category: dot` ailment; it enters `_DOT_AILMENT_NAMES` and DOT/CONTROL categorization sets registry-driven — it is NOT added to `_control_effects` (amendment #3 honored; the sim slice explicitly does not touch `geometry_derivation.py:238`, math §4.5).

**Target 5 — Taunt.** `PROXY_TAUNT_PRIORITY` (`proxy_vocabulary_bridge.py:70-74`) is a NEW parallel dict at top-of-module (moved up to break a circular import with the sim-side consumer, :42-48). `PROXY_TYPE_TIER` and `PROXY_TYPE_TARGETING` (:120-135) are UNCHANGED and still string-valued — non-mutation confirmed. `_taunt_weighted_distance` (`spatial_engine.py:1168-1184`) = `distance * (1.0 - taunt_priority)` with two byte-neutral guards (None proxy_type → nominal :1179; priority ≤ 0.0 → nominal :1182). Nav-selection at :2731-2737 swaps `min(_foes, key=mob.distance_to)` for the taunt-weighted variant (byte-identical at all-zero priorities). `proxy_type` stamped at `_spawn_one_ally:2140`. `bodyguard=0.7` audited against yaml/spec: it is a rocket INFERENCE (no spec enumeration) grounded in `PROXY_TYPE_TARGETING["bodyguard"]="intercept"` (:122) = functional partial-taunt, set below golem's 1.0 to preserve golem tank-primary. Defensible; gandalf concurred. `fragile_escort=0.0` explicit exclusion.

**Target 6 — Byte-neutrality (highest-stakes).** Verified by inspection: every sim-side addition is guarded to no-op when no ailment-layer effect is present — sunder amp (:497), DoT-tick amp (`effect_resolver.py:89,104`), immunity decrement (:80), taunt weight (:1179/1182), stun drop (:1070 condition), boss branch (:1113 default False). Both new `CombatantState` fields default to byte-neutral sentinels (`stun_immune_remaining=0.0`, `is_boss=False`; `combatant.py:352,359`); `ActiveEffect.source_element` defaults None (:113). Verified empirically: targeted regression battery `-k "spatial|simulation|damage|effect|combatant|resolver|fight|byte|dot|ailment|proxy|summon"` (4 pre-existing grouping-vocab-path collectors excluded) = **685 passed, 0 failed** with the ailment code live.

## Test batteries (jack-ryan re-run on HEAD 14fbeec)

- Both slice suites (`test_ailment_layer_rocket_slice.py` + `test_ailment_layer_gamora_slice.py`): **103 passed** (66 + 37).
- Ailment registry + w02 (`test_ailment_registry.py` + `test_w02_archetype_label_round_trip.py` + `test_w02_bc_target_composer.py`): **139 passed**.
- Byte-neutrality regression battery (targeted `-k`, 4 pre-existing grouping-vocab collectors excluded): **685 passed, 0 failed** (98.99s).
- Expected reds confirmed and ISOLATED: `test_substrate_identity_loader.py::TestFoundationIntegration` = **2 failed** (`test_rotating_elements_count_is_four`, `test_load_foundation_still_passes_element_count`) — both assert stale 5-element/4-rotating counts; 8 elements exist post water→ice (lineage 2ae665b). Out of scope; nothing else red in that class (12/14 pass).
- **Environmental (NOT ailment-caused):** 4 collection ERRORS on the LLM-naming suites (`test_cosmological_vocabulary`, `test_cp8_gear_naming`, `test_naming`, `test_no_canonical_four_in_llm_prompts`) — all raise `Cannot locate grouping-layer-vocabulary.md` (story-canon doc relocated in the 2026-06-30 historical/-subfolder-retirement reorg; doc genuinely absent from the collab repo). Last touched by pre-ailment commits (8f53ff2 rocket legacy-test sweep; LLM D15/D6). Zero ailment commits touch them. Same out-of-scope class as the 2 substrate reds. (These 4 are why a full-tree `pytest tests/` interrupts at collection; the "928/928 across 19 files" smoke claim is a subset that excludes them.)

## Amendments named

1. **SPEC-AMENDMENT CANDIDATE — §5.5 poison stack cap: "per-attacker" → "per-defender" (documentation reconciliation).** Spec §5.5/§5.6 say `stack_cap_per_attacker`; `ActiveEffect` carries no attacker id, so gamora enforced the cap per-defender across all poison stacks (`_add_poison_stack:1149`, math §4.2/§8 flag). gandalf CONCURRED (veto-open). This is a spec-text-vs-implementation gap, not a code defect — the lenient per-defender reading is safe for the current corpus (mob-vs-player poison is not emitted yet). Recorded in decisions-log this date (ruling batch #8). Follow-on: if multi-attacker poison abuse surfaces, add `attacker_id` on `ActiveEffect` and tighten. No owing seam now.

## MIGRATION.md accuracy vs diffs

Both entries accurate and thorough. `generation/MIGRATION.md` [2026-07-16] documents the 8→12 canonical growth, parallel-map non-mutation (Principle-6 additive-only gate), and the star-lord cross-seam consumers (LLM prompt vocabulary + telemetry bin cardinality). `simulation/MIGRATION.md` [2026-07-16] documents both new `CombatantState` fields with byte-neutral defaults + consumers, `_compute_sunder_amp` + `_add_poison_stack` signatures, the `_add_or_refresh` sunder special-case (framed, not buried), the `can_use_skill` freeze/stun change, HARD guards, and the consecrate×sunder double-multiplicative note (Gate-1 amendment #7). ADR-004 satisfied.

## Action

- [x] Developer (rocket/gamora): none owed — implementation PASSES; no trivial fix and no named breach.
- [x] jack-ryan: decisions-log Gate-2 verdict + delegated-ruling batch appended (engine repo, this date).
- [ ] Matt (veto-open review, non-blocking): confirm/overturn gandalf-prime rulings #5 (name `sunder`), #6 (five escalation resolutions), #7 (state-noun `shape`), #8 batch (melee_tank_pet/thorns_barrier_summon abstention CONCUR; bodyguard=0.7 CONCUR; §5.5 per-defender CONCUR + amendment candidate). All Matt-veto-open.
- [ ] Follow-on (flagged, not blocking): wire `SpawnSpec.is_boss → CombatantState.is_boss` at spatial-engine construction to light the stun boss-DR branch; S6 gauntlet calibration pass for all four ailments; per-attacker poison attribution IF abuse surfaces.
- gandalf pushes both repos after this verdict (no push by jack-ryan per dispatch).

## References

- Spec (law): `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` (§2.6, §3.6, §5.5, §5.7, §6.5.1, §7, §10, §11).
- Math notes (both pre-code, Discipline #1): `src/reincarnated/generation/math/ailment-layer-rocket-slice-math-2026-07-16.md`; `src/reincarnated/simulation/math/ailment-layer-sim-resolution-2026-07-16.md`.
- Sim: `damage_resolver.py:85-114,496-498,1070-1071,1113-1115,1130-1153,1188-1197`; `effect_resolver.py:79-81,88-105,136-158`; `combatant.py:113,352,359,384-396,433-452`; `spatial_gauntlet/spatial_engine.py:1165-1184,2140,2731-2737`.
- Gen/config: `config/ailments.yaml:203-316`; `foundation/ailment_loader.py:44-92,387-391`; `generation/element_biases.py:107-116`; `generation/proxy_vocabulary_bridge.py:70-74,120-135`; `generation/substrate_templates.py:667-669`.
- MIGRATION: `src/reincarnated/generation/MIGRATION.md` [2026-07-16]; `src/reincarnated/simulation/MIGRATION.md` [2026-07-16].
- Decisions-log Gate-2 entry (this date): `~/Games/reincarnated-engine/design/decisions/decisions-log.md`.
- Companion Gate-1 finding: `agentic_orchestration/jack-ryan/reviews/2026-07-16-ailment-layer-spec-gate1.md`.
