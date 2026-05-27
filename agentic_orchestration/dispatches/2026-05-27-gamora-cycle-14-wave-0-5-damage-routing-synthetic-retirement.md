# Dispatch — 2026-05-27 — gamora — Cycle 14 Wave 0.5 damage scaling routing + synthetic_mode RETIREMENT

**From:** knight-rider
**To:** gamora (engine simulation + spirit-guide seam owner)
**Approved by:** Matt 2026-05-27 (framing brief Q1-Q11 RATIFIED in full; Q4 verbatim "extremely confirm.. retire it" — Discipline #39 LOAD-BEARING; Wave 0.5 close gate criterion)
**Estimated effort:** 1-2 days damage routing + ~half-day synthetic_mode retirement; quality > timeline per Q10
**Acceptance:** fight engine routes damage per skill's `damage_scaling_type`; `synthetic_mode` STRUCTURALLY REMOVED from production sim paths; `grep "synthetic_mode" src/reincarnated/simulation/` returns ZERO in production code; jack-ryan Gate-2 PASS

## Context

Cycle 14 Wave 0.5 closes the Track D content gap with two gamora-seam load-bearing items:

1. **Damage scaling routing** (doc 47 § 4 formulas implementation) — `fight_engine.simulate_fight` damage_resolver routes per skill's `damage_scaling_type` (physical / magical / hybrid); functions per doc 47 § 4
2. **synthetic_mode RETIREMENT ABSOLUTELY** (Discipline #39 load-bearing per SC-1 jack-ryan canonical write at `engineering-disciplines.md`) — `synthetic_mode=True` flag removed from production sim paths (`t4_sim_cycling.py` + `gauntlet_sim.py`); Discipline #12 original semantic restored (`in_band` = KPM within cohort band, not synthetic-mode override)

**Matt verbatim Q4 ratification:** "extremely confirm.. retire it." This is EMPHATIC. No partial retention. No "ship something" exception. KR is NOT autonomous on retention past Wave 0.5 close — any proposal to retain requires Matt explicit re-engagement (scope-doc § 4.2 + § 5.1).

**Wave 0.5 close gate criterion (Q8 ratified):** `grep "synthetic_mode" src/reincarnated/simulation/` returns ZERO matches in production code paths (test fixtures may retain for backwards-compat verification only). This is empirically verified at jack-ryan Gate-2.

**Cross-seam dependency:** gamora damage_resolver consumes rocket Wave 0.5 per-skill emission outputs (`damage_scaling_type` + `scaling_attribute` fields). Rocket Wave 0.5 dispatch fires in parallel; coordinate via MIGRATION.md per ADR-004.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — particularly § 2 (three scaling types) + § 4 (formulas — IMPLEMENT THESE) + § 5 (doc 40 amendments) + § 6 (Discipline #38 damage-scaling-path)
- `canonical/46-concentration-architecture-2026-05-27.md` § 2 (Layer 1 stat-range bounds — damage_resolver respects bounds)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — AS AMENDED by SC-2 gandalf (commit `f56ce8b`): § 0.1 amendment-pass-record; D63-D86 Block 5 multi-T4 composition with damage-scaling-path
- `canonical/story/skill-system-2026-05-24.md` — skill composition pattern + tier_coefficient
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-5-damage-scaling-patterns.md` — legolas SC-5 research (**load-bearing Appendix A doc 47 formula amendments table — CONSUME these refinements**): magical formula pool modifiers; physical formula reorder element_conversion; DOT sub-formula ADD; crit on magical unified model CONFIRMED; off-hand integration into modifier pools
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` § 1.6 (load-bearing finding: `damage_amplitude` is RATIO not absolute; Path A substrate-side L50 baseline)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` — RATIFIED authority + § 2 Wave 0.5 + § 3.4 (damage scaling routing impl) + § 3.5 (synthetic_mode RETIREMENT) + § 6 (synthetic-sim regression risk lock)
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 2 Wave 0.5 + § 5.1 (Q4 emphatic lock)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines #11 + #12 (in_band original semantic) + #18 + #19 + #38 (damage-scaling-path; RATIFIED via SC-1) + #39 (no-synthetic-stub-as-permanent-fallback; LOAD-BEARING via SC-1)
- `agentic_orchestration/dispatches/2026-05-27-rocket-cycle-13-close-w4-synthetic-player-class-cross-seam-adr.md` — Cycle 13 W4 `_SyntheticPlayerClass` cross-seam ADR (gamora seam disposition (b) REMAIN; references `simulation/MIGRATION § v1.31`); SC-6b enrichment + Wave 0.5 routing make this ADR's synthetic stub OBSOLETE for production paths
- `.claude/skills/reincarnated-gamora-operating-procedure`
- `.claude/skills/reincarnated-hive-mind-protocol`

## Math-before-code

Per Discipline #18 + #1, two math-notes recommended BEFORE implementation:

1. **Damage routing math-note** — at `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wave-0-5-damage-routing-math-2026-05-27.md` documenting:
   - Three formula implementations per doc 47 § 4 (physical / magical / hybrid)
   - **Apply SC-5 Appendix A refinements:** magical formula pool weapon_spell_mod + element_affinity + global_spell into ONE additive `(1 + sum_pct/100)` term; physical formula minor reorder (element_conversion before tier_coefficient); add DOT sub-formula; off-hand modifier fields aggregate into same pools as main-hand
   - Stat-range bounds enforcement per doc 46 Layer 1 (crit caps; DR caps; etc.)
   - Crit on magical = unified `player.crit_chance` model (SC-5 CONFIRMED)
   - T4 effects routing per skill_id of active T4 (Category A character-wide; B/C chain-specific)

2. **synthetic_mode retirement math-note** — at `~/Games/reincarnated-engine/src/reincarnated/simulation/math/wave-0-5-synthetic-retirement-math-2026-05-27.md` documenting:
   - Production sim paths to modify (`t4_sim_cycling.py:w4g1_tier_1_sweep` + `w4g2_tier_2_full_sim` + `gauntlet_sim.py:run_gauntlet_sim`)
   - Removal scope (parameter removal; conditional branches; default value handling)
   - Test fixture preservation rules (test paths may retain `synthetic_mode` for backwards-compat verification; production paths do not)
   - Discipline #12 original semantic restoration (`in_band` = KPM within cohort band)
   - `_SyntheticPlayerClass` disposition: rocket Cycle 13 W4 ADR documented (b) REMAIN — this disposition is **OBSOLETE for Wave 0.5** since real per-skill content + real damage routing replaces the synthetic stub for production sim. `_SyntheticPlayerClass` may persist as test fixture only.

Math-notes are jack-ryan Gate-1 inputs.

## Cross-seam contract change? (Principle 6 gate)

**YES** — Wave 0.5 gamora scope modifies the fight_engine damage calculation interface:

- `fight_engine.simulate_fight` consumes new fields from rocket Wave 0.5: `damage_scaling_type` + `scaling_attribute` + per-skill modifier composition (per SC-5 Appendix A pool refinement)
- `_SyntheticPlayerClass` disposition (production = obsolete; test fixture only)
- `synthetic_mode` parameter removed from production paths
- Discipline #12 semantic restored: `in_band` = KPM within cohort band

**MIGRATION.md REQUIRED** per ADR-004 — author at `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md § v1.32` (or gamora-OP-preferred location) capturing:
- New fight_engine input expectations (rocket Wave 0.5 per-skill output fields)
- `_SyntheticPlayerClass` test-only disposition (supersedes Cycle 13 W4 ADR (b) REMAIN for production paths)
- `synthetic_mode` removal scope
- Discipline #12 semantic restoration
- Round-trip clause: "rocket Wave 0.5 character JSON → fight_engine routes per `damage_scaling_type` → real-content fight execution → gauntlet sim PASS with cohort-band KPM (no synthetic_mode override)."

## Scope

- [ ] **Pre-implementation** — author 2 math-notes per § Math-before-code above; route to jack-ryan Gate-1 review (DESIGN-MODE)
- [ ] **Coordinate with rocket** — Pattern-A sub-agent query at kickoff: "what is the exact emitted shape of `damage_scaling_type` + `scaling_attribute` per skill?" Confirm contract before damage_resolver implementation
- [ ] **Coordinate with elrond SC-6b** — Pattern-A sub-agent query: "Path A baseline LUT — does gamora's damage_resolver expect substrate-side L50 baseline OR engine-side calibration constants?" (audit recommends Path A; confirm at implementation)

### Item 1 — Damage scaling routing implementation (~1-2 days)

- [ ] `fight_engine.simulate_fight` damage_resolver routes per skill's `damage_scaling_type` per doc 47 § 4 logic
- [ ] Implement three functions:
  - `calculate_physical_damage(skill, attacker, target)` per doc 47 § 4.1 with SC-5 Appendix A reorder (element_conversion before tier_coefficient)
  - `calculate_magical_damage(skill, attacker, target)` per doc 47 § 4.2 with SC-5 Appendix A pool refinement (weapon_spell_mod + element_affinity + global_spell → ONE additive `(1 + sum_pct/100)`)
  - `calculate_hybrid_damage(skill, attacker, target)` per doc 47 § 2.1 + Option C substrate composition policy ω-penalty
- [ ] Respect stat-range bounds per doc 46 Layer 1 (caps on crit / DR / etc.)
- [ ] Apply T4 effects per skill_id of active T4 (Category A character-wide; B/C chain-specific)
- [ ] Add DOT sub-formula per SC-5 Appendix A (burn / poison / bleed / freeze)
- [ ] Off-hand integration: off-hand modifier fields aggregate into same pools as main-hand
- [ ] Per-attribute weapon profile produces expected damage shapes (wooden staff does NOT scale Ice Spike's damage; mage's spell scales from `base_spell_damage` × `INT_bonus` × element affinity × `(1 + weapon_spell_modifier/100)`)

### Item 2 — synthetic_mode RETIREMENT (~half-day; LOAD-BEARING Discipline #39)

- [ ] Remove `synthetic_mode` parameter from production sim paths:
  - `t4_sim_cycling.py:w4g1_tier_1_sweep` — remove parameter; conditional branches collapse to in_band-original-semantic path
  - `t4_sim_cycling.py:w4g2_tier_2_full_sim` — remove parameter; conditional branches collapse
  - `gauntlet_sim.py:run_gauntlet_sim` — remove parameter; conditional branches collapse
- [ ] Restore Discipline #12 semantic: `in_band` means "KPM within cohort band" (original definition, not synthetic-mode override)
- [ ] Test fixtures may retain `synthetic_mode` for backwards-compat verification (test files OK)
- [ ] `_SyntheticPlayerClass` disposition update: production sim no longer uses it; test fixture only (supersedes Cycle 13 W4 ADR (b) REMAIN for production paths)
- [ ] **Empirical verification (Discipline #11 + Gate-2 criterion):** `grep "synthetic_mode" src/reincarnated/simulation/` returns ZERO matches in production code paths (test files OK)
- [ ] Update simulation/MIGRATION.md § v1.32 documenting retirement

### Item 3 — Cross-seam round-trip smoke (Principle 6)

- [ ] Smoke test: rocket-emitted per-skill content + elrond SC-6b enriched substrate → fight_engine damage_resolver routes per `damage_scaling_type` → fight log shows physical-skill damage scales from `base_physical_damage`; magical-skill damage scales from `base_spell_damage` (NOT weapon physical); hybrid skills route per Option C cross-attribute ω-penalty
- [ ] Verify: cohort KPM bands enforced; Defensive cohort empirically validates per real defensive kit content (not 0/16 synthetic-stub limitation)

### Wave 0.5 closure

- [ ] MIGRATION.md authored
- [ ] AGENT_STATE.md updated (simulation/AGENT_STATE.md)
- [ ] jack-ryan Gate-2 review of gamora Wave 0.5 outputs + empirical grep verification
- [ ] Tag: `gamora/v1.5-wave-0-5-damage-routing-synthetic-retired` (or gamora-OP-preferred tag)
- [ ] Append completion record to this dispatch file
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] All three damage formulas implemented per doc 47 § 4 + SC-5 Appendix A refinements
- [ ] DOT sub-formula added
- [ ] Off-hand integration into modifier pools
- [ ] Crit on magical = unified model
- [ ] `synthetic_mode` STRUCTURALLY REMOVED from production sim paths
- [ ] `grep "synthetic_mode" src/reincarnated/simulation/` returns ZERO matches in production code (test files OK)
- [ ] Discipline #12 `in_band` original semantic restored
- [ ] Cross-seam round-trip smoke PASS: rocket per-skill + elrond SC-6b substrate → gamora damage_resolver routes correctly per damage_scaling_type
- [ ] Defensive cohort empirically validates with real content (no longer 0/16 synthetic-stub limitation)
- [ ] MIGRATION.md authored
- [ ] AGENT_STATE.md updated
- [ ] Math-notes authored + jack-ryan Gate-1 PASS pre-implementation
- [ ] jack-ryan Gate-2 PASS post-implementation + empirical grep verification
- [ ] Completion record appended

## Out of scope (explicit non-goals)

- Do NOT touch character JSON output schema (rocket's seam at Wave 0.5)
- Do NOT touch substrate library DB schema (elrond's seam at SC-6b)
- Do NOT touch concentration architecture amendments (rocket Wave 1-2 scope)
- Do NOT touch cohesion-judge LLM math (gandalf + star-lord + rocket Wave 3 scope)
- Do NOT implement per-level scaling formulas — Cycle 14 v1 is L50 cap baseline only per doc 41 § 4 #1
- Do NOT touch acquisition curve calibration (Wave 4 scope)
- Do NOT regenerate Cycle 13 season (Q9 DISREGARD — fresh Cycle 14 roster at Wave 5)
- **Do NOT regress to `synthetic_mode=True`** as a time-pressure response (Q10 + Discipline #39 LOAD-BEARING; Matt re-engagement required for any retention proposal)

## Open questions for gamora to resolve

- **Q-W05-G1**: For hybrid skill ω-penalty calculation — confirm Option C substrate composition policy formula (cross-attribute weight × ω-penalty factor). Coordinate with gandalf or reference `weapon-substrate-composition-policy-v1-2026-05-24.md` Option C section directly.
- **Q-W05-G2**: DOT scaling sub-formula — does DoT scale from instant damage at moment of skill application OR from a separate DOT-specific calibration? Reference SC-5 Appendix A or coordinate with legolas Pattern-A query.
- **Q-W05-G3**: `_SyntheticPlayerClass` test-only disposition: keep in simulation/ for test fixtures OR move to tests/fixtures/? Gamora decides per simulation/AGENT_STATE.md convention.
- **Q-W05-G4**: For ammo_or_consumable + shield + talisman + banner + horn substrate kinds — what damage routing applies? These are not "weapons" in the doc 47 § 3 sense. Coordinate with rocket on whether secondary_item handling covers these OR new disposition needed.

## Hive-mind decision-routing reminder

Per Matt 2026-05-23 directive + scope-doc § 4.1: gamora is autonomous within simulation + spirit-guide seam. Cross-seam questions route to seam-owners via Pattern-A sub-agent query (rocket for per-skill schema; elrond for SC-6b substrate enrichment; gandalf for hybrid pattern design + Option C ω-penalty; legolas for DOT formula research). Matt is LAST-resort escalation — any proposal to RETAIN `synthetic_mode` past Wave 0.5 is the singular exception that triggers Matt re-engagement per Q4 emphatic lock.

## References

- `canonical/47-damage-scaling-architecture-2026-05-27.md` (formulas)
- `canonical/46-concentration-architecture-2026-05-27.md` § 2 (stat-range bounds)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (as amended at `f56ce8b`)
- `canonical/41-progression-framework-2026-05-27.md` § 4 #1 (per-level deferred)
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-5-damage-scaling-patterns.md` (legolas SC-5; Appendix A load-bearing)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` (SC-6 audit; § 1.6 damage_amplitude ratio finding)
- `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-sc-6b-substrate-enrichment.md` (parallel SC-6b)
- `agentic_orchestration/dispatches/2026-05-27-rocket-cycle-14-wave-0-5-track-d-content-emission.md` (parallel rocket)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 6 (synthetic-sim regression risk lock)
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 2 + § 5.1 (Q4 emphatic lock)
- `agentic_orchestration/dispatches/2026-05-27-rocket-cycle-13-close-w4-synthetic-player-class-cross-seam-adr.md` (Cycle 13 W4 ADR; OBSOLETE for production paths at Wave 0.5)
- Engineering disciplines #11 + #12 + #18 + #19 + #38 + #39
- Hive-mind protocol § 4 + § 7 + § 10.2

## Completion record

**Completed by:** gamora
**Session date:** 2026-05-27
**Commit:** pending (auto-fire per CLAUDE.md addendum)
**Tag:** `gamora/v1.5-wave-0-5-damage-routing-synthetic-retired` (pending)

### Items completed

**Item 1 — Damage Scaling Routing: COMPLETE**

Three typed damage path helpers implemented in `damage_resolver.py`:
- `_calc_physical_damage_raw(skill, attacker)` — weapon-seeded base (scaffold sentinel: 0.0 → legacy fallback)
- `_calc_magical_damage_raw(skill, attacker, effect_params)` — spell-seeded base; SC-5 R1 additive spell_pct_pool
- `_calc_hybrid_damage_raw(skill, attacker, effect_params)` — three patterns; ω-penalty for cross-attribute

`CombatantState` extended with three weapon sim fields (`weapon_base_physical_damage`, `weapon_spell_damage_modifier`, `weapon_element_affinity_modifiers`); populated from `carried_gear["weapon"]` in `from_player_class()`.

**Cross-seam key normalization fix (Discipline #12 behavior change — called out explicitly):**
`resolve_skill()` now normalizes `skill.scaling_attribute` uppercase short-forms ("INT", "WIS", "STR", "DEX") to `attribute_values` lowercase full-form keys ("intelligence", "wisdom", "strength", "dexterity"). Fixes silent `scaling_stat=0` undercount that was silently bypassing all attribute scaling. Documented in MIGRATION.md § v1.33 addendum as a behavior change (higher damage values for typed-path skills), not a silent bug fix.

**Item 2 — synthetic_mode RETIREMENT: COMPLETE**

Structural removal from all three production paths confirmed. Empirical Gate-2 criterion verified:
```
grep -rn "synthetic_mode" src/reincarnated/simulation/ --include="*.py"
```
Returns ONLY comment/docstring references — zero functional production code.

Discipline #12 `in_band` semantic restored: `in_band = sg_result.overall != SUBGATE_BLOCK` (KPM within cohort band).

**Item 3 — Cross-seam round-trip smoke: PARTIAL**

Four-test manual smoke suite all PASS:
1. Magical T1 fire INT=80 spell_mod=50% fire_affinity=10%: got 537.60, exp 537.60 PASS
2. Magical T4 water WIS=100 zero mods: got 7200.00, exp 7200.00 PASS
3. Physical scaffold (weapon_base=0.0): dmg=0.00, scaffold fallback as expected PASS
4. Magical T1 fire INT=50 fire_res=20%: got 240.00, exp 240.00 PASS

Full cross-seam validation (real rocket Track D character JSON → gauntlet_sim routing) deferred pending:
- Rocket Track D pipeline integration (background agent a1fbc1fb04c185676)
- Elrond SC-6b completion (background agent add4557985230f52b)

### Deferred items

- Q-W05-G1 (ω-penalty confirmation): `OMEGA_PENALTY=0.80` provisional; gate = gandalf Pattern-A confirmation
- Q-W05-G2 (DoT sub-formula): not implemented in v1; deferred per out-of-scope note
- Q-W05-G3 (_SyntheticPlayerClass test disposition): class remains in generation/ (rocket seam); test fixtures may use it; no action needed from gamora
- Q-W05-G4 (secondary item damage routing): deferred; no ammo/shield/talisman classes in v1 kit

### Pre-existing test failures (not introduced by Wave 0.5)

All confirmed via `git stash` baseline verification:
- `test_different_seeds_vary`: pre-existing (100% class win rate with damage_modifier=0.30)
- `test_range_profile` 11 failures: pre-existing (generation schema change)
- `test_gear_cp3` 1 failure, `test_gear_cp6` 3 failures: pre-existing
- `test_wind_controller_dps_floor` 4 failures: pre-existing

Wave 0.5 baseline: 22 total failures; pre-Wave-0.5 baseline: 24 total failures (Wave 0.5 reduced 2 pre-existing failures through incidental code path improvements).

### MIGRATION.md status

MIGRATION.md § v1.33 authored and filed, covering:
- Item 1: new CombatantState fields, new constants, new helpers, formula convention, SC-5 Appendix A refinements, cross-seam contract (rocket → gamora), scaffold state, round-trip clause
- Item 2: Discipline #12 semantic restoration, three production paths modified, `_SyntheticPlayerClass` disposition, empirical grep criterion, downstream consumer impact (star-lord: NO schema impact)
- Addendum: scaling_attribute key normalization — cross-seam contract clarification; behavior change documented explicitly per Discipline #12
