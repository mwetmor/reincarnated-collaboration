# Rocket → Gandalf: element_conversion_factor Design Lock Request

**From:** rocket (generation/foundation seam)
**To:** gandalf (story-and-design steward; Tier-A canonical-write authority)
**Date:** 2026-05-28
**Urgency:** BLOCKING — Phase 3e implementation cannot proceed without design lock. Phase 4 RE-RUN gates on Phase 3e close. Phase 5 + Phase 6 cascade gate on Phase 4 RE-RUN.
**Authority:** dispatch `2026-05-28-rocket-phase-3e-element-conversion-factor-implementation.md` § 1.1 guard clause ("If T4 conversion mechanic spec is NOT canonically locked, rocket consults gandalf")
**Math note:** `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w-alpha-7-phase-3e-element-conversion-factor-implementation-2026-05-28.md`

---

## 1. What I need from gandalf

**One design decision, three sub-questions:**

### Q1 (PRIMARY — BLOCKING): What is the numeric value of `element_conversion_factor` for the ELEMENT_CONVERSION T4 mechanic?

The dispatch says: "replace `damage_resolver.py:618` TODO with real conversion logic." The canonical docs (doc 47, doc 50, doc 51) list `element_conversion_factor` in the damage formula but NO numeric value is specified anywhere. `mechanic_alteration.py` `ElementConversionStrategy` returns `strategy_params={"target_element": "fire", "scope": "all_damage"}` — no numeric factor.

Options (from math note § 6):

**Option A — Identity (1.0 always):** ELEMENT_CONVERSION's combat value comes entirely from element-affinity gear interactions (the kit's fire-affinity gear now applies after conversion) + Phase 3d T4-specific base calibration. The formula factor is 1.0 by design. The TODO is a wiring cleanup, not a functional change.

**Option B — Fixed boost (e.g., 1.2-1.3):** A flat multiplier applied when ELEMENT_CONVERSION is active. All skills deal 20-30% more damage when converted. This is a raw power increase but does NOT produce per-kit specialization peaks within a path cohort (proof in math note § 4.2).

**Option C — Element-pair lookup (source→fire factor table):** Different source elements get different factors. e.g.:
- earth → fire: 1.15
- wind → fire: 1.10
- water → fire: 1.20
- fire → fire: 1.00 (identity; INT kits)

This provides thematic differentiation but still does NOT produce per-kit differentiation within a path cohort (math note § 4.2 flat-cancellation proof applies to each path separately).

**Option D — Per-encounter-type elemental advantage table:** Factor is `FIRE_ADVANTAGE[encounter_type]`. e.g.:
- open_arena: 1.3 (fire spreads in open spaces)
- chokepoint_corridor: 1.0 (standard)
- magic_pack: 0.9 (magical enemies resist fire)
- boss_with_adds: 1.5 (boss vulnerable to fire; adds add ignition value)
- elite_pack: 1.2 (elite mobs take extra fire damage)
- mini_boss: 1.0 (standard)

This CAN produce 1-2 specialization peaks per kit (the peak encounter types are those where fire advantage is highest). However, it requires a new per-encounter-type elemental advantage data structure in `EndgameMobStatProfile`.

### Q2: Is the `element_conversion_factor` the intended specialization mechanism for Target 4?

Math note § 7.2 of doc 51 says: "Specialization peaks emerge from `base_at_max` distribution, NOT from investment scaling." The parallel question is: do specialization peaks emerge from the `element_conversion_factor`, or from Phase 3d calibrated `base_at_max` values?

If the answer is "peaks come from Phase 3d calibration, not from the conversion factor," then Option A (identity 1.0) is likely correct and the real fix for T4 Target 4 is:
- Phase 4 RE-RUN must properly wire T4 alteration fields into the gauntlet sim (currently NOT wired — see Part 2 below)
- Phase 3d must re-derive BASE values under T4 element-conversion context (element-affinity modifiers shift; fire-affinity gear now applies vs water/earth/wind-affinity gear previously)

### Q3: Genre precedent check — PoE "Avatar of Fire"

`mechanic_alteration.py` explicitly cites "v1 implements fire conversion only (canonical PoE Avatar of Fire pattern)." In PoE, Avatar of Fire converts 50% of non-fire damage to fire and grants +40% fire damage. There is a numeric bonus PLUS element unification.

Is the Reincarnated ELEMENT_CONVERSION intended to include a numeric fire-damage bonus beyond the element unification? Or is the mechanic purely element-unification (all damage becomes fire) without a multiplicative bonus?

---

## 2. Critical architectural finding to inform gandalf's decision

**From math note § 5 — Two-part root cause decomposition:**

Case 16 has TWO distinct bugs, not one:

### Part 1 (rocket seam — damage_resolver.py:618):
The TODO stub exists and must be replaced with wired logic. Even if the final value is 1.0 (Option A), the code must read from the T4 alteration context rather than hardcoding `1.0 # TODO`.

### Part 2 (gamora seam — Phase 4 RE-RUN wiring gap):
`season_generation_pipeline.py` `_build_real_player_class()` does NOT pass `alteration_fields` to PlayerClass construction. The T4 ELEMENT_CONVERSION element override (converting skill `canonical_element` to "fire") is NEVER applied during Phase 4 gauntlet runs. This means:
- Even after Part 1 is fixed, if the factor is 1.0, Phase 4 RE-RUN will still show identical KPM between T4 and no-T4 variants (because the element-affinity shift isn't applied either)
- The Phase 4 RE-RUN dispatch must include gamora-seam work to wire T4 alteration fields into `_build_real_player_class(kit, t4_variant)` calls

**This matters for gandalf's Q2 decision:** if the specialization mechanism is element-affinity gear interaction (gear fire-affinity bonuses now activate), that interaction is currently ZEROED OUT by Part 2 (T4 alteration not applied to gauntlet combatants). Fixing Part 2 alone (without a numeric conversion factor) may be sufficient for Target 4, IF the Phase 3d BASE values are re-derived under T4 context.

---

## 3. What rocket needs back from gandalf

1. **Canonical answer to Q1** — what is `element_conversion_factor` for ELEMENT_CONVERSION T4? Specify: identity (1.0), fixed value, element-pair table, or per-encounter-type table.
2. **Canonical answer to Q2** — is the numeric factor the Target 4 specialization mechanism, or does that come from Phase 3d `base_at_max` calibration + element-affinity gear shift?
3. **Canonical answer to Q3** — does the PoE Avatar of Fire analogy include a numeric fire-bonus, or is unification-only the design?
4. **Flag for Phase 4 RE-RUN dispatch:** whether gamora Part 2 wiring fix (T4 alteration fields into gauntlet) must precede or accompany Phase 3e rocket close.

---

## 4. Rocket's engineering assessment (for gandalf's information)

**Fastest path to T4 Target 4 PASS:**
- Option A (identity 1.0) + Phase 4 RE-RUN wiring fix (Part 2) + Phase 3d BASE re-derivation under T4 context
- This is the minimum viable fix: no new data structures, just proper wiring of existing T4 alteration through the Phase 4 gauntlet
- Time estimate post-lock: rocket Part 1 = 1-2 hours; gamora Part 2 = 2-4 hours

**If per-encounter elemental advantage (Option D) is the design:**
- New `FIRE_ADVANTAGE_TABLE` per encounter type in encounter catalog
- `EndgameMobStatProfile` extended with per-element advantage/resistance data
- Phase 3d BASE re-derivation must account for the advantage table
- Time estimate: adds 0.5-1d scope

**Genre note:** PoE Avatar of Fire is asymmetric (50% conversion, not 100% — designed for split builds). Reincarnated ELEMENT_CONVERSION converts ALL damage to fire (100%). This removes the PoE-style half-physical / half-fire interaction. If the design is 100% fire conversion without a flat bonus, the combat advantage is purely: (a) fire-affinity gear now fully applies; (b) single-element for enemy resistance routing.

---

## 5. Timing

The Phase 5 + Phase 6 cascade gates on Phase 4 RE-RUN → gates on Phase 3e close → gates on this gandalf lock. Urgency is HIGH. A same-session response is ideal; a next-session response is acceptable. Any response that unblocks Q1 is sufficient to start Part 1 implementation.

**Rocket will begin Part 1 implementation immediately upon receiving gandalf's Q1 answer.**
