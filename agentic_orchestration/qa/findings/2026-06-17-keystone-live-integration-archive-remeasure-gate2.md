# Finding — 2026-06-17 — keystone-live-integration-archive-remeasure (Wave A1)

**Reviewer:** jack-ryan
**Severity:** WARN (PARK the §2.1 ENDORSE — evidence gap, not a confirmed balance defect)
**Target:** `gamora/v-keystone-live-integration-1` (commits `90ffa03` math, `7f40674` build, `d7097e0` state) — NOT pushed
**Developer:** gamora
**Principles applied:** #1 (math-before-code), #2/#2.1 (smoke/resource), #11 (empirical inspection), Review Principle 2 (smoke-gate), Principle 4 (decisions/charter as truth); ADR-006 (read-only). Charter `2026-06-17-autonomous-run-plan-v2.md` §2.1 gate.

## What I found

The discipline floor is solid: math note `90ffa03` precedes build `7f40674`; the 6b instrument constants in `combatant.py` (2pc +10%, 4pc +35%, armor +18%, hp +12%, named `KEYSTONE_6B_REFERENCE_SET_*`) match the note's derivation exactly and the +35% is a sound chain-T4-band-midpoint anchor against the v1.2-LOCKED conversion magnitudes [0.25, 0.50]; it is a single neutral 6b magnitude, not profile-keyed 6a; production `apply_max_profile_investment=False` default is intact; the build commit touches no `kit_archive.db` (read-only preserved); a smoke artifact precedes the full run. The kit-power lift is real and the 0.35× floor is gone (wr 0.182→1.000, 34/34).

**I CONCUR that the −0.38 open_arena Spearman is a measurement-ceiling artifact, not a balance defect.** The proof is stronger than gamora stated: AFTER `mobs_killed` is **34/34 tied at exactly 8.0** (every kit clears the 8-mob open_arena, wr=1.0, 15–26s). The reported Spearman and `max_rank_shift:21`/13 `implausible_inversions` are computed by `_spearman` on `before_mk` vs `after_mk` — i.e. a correlation against a **constant column**, which is mathematically degenerate (the "after rank" is pure sort-index tie-break noise). So the negative number carries no balance signal. open_arena cannot rank-order anything post-keystone; it is saturated.

**The PARK reason is NOT the Spearman — it is the missing corroborating evidence.** gamora's INFO classification rests on the claim that "ordering re-emerges cleanly on harder scenarios (elite_pack KPM 17–44, boss_with_adds KPM 18–100, both distinctly ordered)." **That data does not exist in the deliverable and is not producible by this harness.** `keystone-archive-remeasure-full.json` contains `open_arena` only (`grep` count: elite_pack=0, boss_with_adds=0); the script hardcodes `REF_SCENARIO = SCENARIO_OPEN_ARENA` for both arms and the mob_hp baseline and never runs a headroom scenario. The charter §2.1 ENDORSE condition (4) requires rank ordering "preserved or improves in coherence" — that is an affirmative requirement, and the artifact contains **zero non-saturated evidence** to satisfy it. The one measure that would demonstrate coherence is the one that was claimed-but-not-run.

**Secondary, and the reason the gap matters concretely:** `_weapon_offense_from_kit` reads `substrate_weapon_binding["spell_damage_modifier"]` straight into `bonus_damage_percent` (a +% multiplier into `buff_dmg_mult`). The resulting per-kit `gear_dmg_pct` ranges 3.45→**149.45** → weapon `bonus_damage_percent` of +300% to **+14,900%**. The script already guards the `base_physical_damage_l50` double-count path but leaves the `spell_damage_modifier` path unguarded; +149.0 as a fractional percent is almost certainly a unit/semantics mismatch (an absolute or differently-scaled field, not a fraction). open_arena saturation **masks** this entirely (everyone clears regardless), but it would **dominate and distort** exactly the headroom scenario gamora invokes. The unverifiable claim and the unguarded weapon magnitude are the same blind spot.

## Rationale

- Charter §2.1 ENDORSE(4) is an affirmative "preserved or improves in coherence" requirement; the deliverable supplies no measure capable of evaluating it (Principle 4 — charter as truth; Principle 2 — the right instrument for the question, an unmeasured claim is not a passed gate).
- Discipline #11 (empirical inspection over assumption): "ordering re-emerges on harder scenarios" is asserted, not measured in this artifact. gamora's own §1 substrate divergence was exemplary #11 work — the same standard applies to the corroboration.
- Weapon-percent inflation (#11 + boundary-validation #8): `spell_damage_modifier`→`bonus_damage_percent` is an un-validated unit cross of magnitude ~149; it is invisible under saturation, load-bearing under headroom.
- This is WARN/PARK, not BLOCK: nothing is wrong with the math, the instrument, the read-only discipline, or the lift. The gate simply cannot be ENDORSED on saturated-only evidence. Per §2.1 this is "PARK for Matt" territory on the ordering-coherence predicate.

## Action
- [ ] Developer (gamora): add a headroom scenario (elite_pack and/or boss_with_adds) as a third+ arm so AFTER `mobs_killed`/clear-time is NON-saturated, and report Spearman/Kendall on that arm. The open_arena Spearman should be dropped or explicitly stamped "degenerate (constant after-column) — not a coherence measure."
- [ ] Developer (gamora): validate/clamp the `spell_damage_modifier`→`bonus_damage_percent` mapping in `_weapon_offense_from_kit`; confirm +149.0 is a faithful fractional percent and not a scale/unit cross. Re-run only after this is resolved (it would otherwise corrupt the very headroom arm above).
- [ ] Matt (PARK): the §2.1 ENDORSE cannot fire on open_arena-only evidence. Decide: (a) accept the ceiling-artifact concurrence + require the headroom re-run before ENDORSE, or (b) ENDORSE the keystone lift now and track ordering-coherence as a follow-on. Recommendation: (a) — the re-run is cheap and the weapon-magnitude question rides on it.

## References
- `~/Games/reincarnated-engine/output/keystone-archive-remeasure-full.json` (open_arena only; 34/34 AFTER tied at mobs_killed=8.0)
- `~/Games/reincarnated-engine/scripts/gamora_keystone_archive_remeasure_2026_06_17.py` (`REF_SCENARIO=SCENARIO_OPEN_ARENA` hardcoded; `_weapon_offense_from_kit` L116–130; `_spearman` on constant column L301)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/combatant.py` (`KEYSTONE_6B_REFERENCE_SET_*` L400–403; `apply_max_profile_investment=False` default)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/keystone-live-integration-archive-remeasure-2026-06-17.md`
- charter `~/Games/reincarnated-collaboration/canonical/story/2026-06-17-autonomous-run-plan-v2.md` §2.1 (L66, L68)
