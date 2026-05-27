# Dispatch — 2026-05-27 — rocket — Cycle 14 Wave 1 concentration architecture (Layers 1-4 + 7)

**From:** knight-rider
**To:** rocket (engine content-generation seam owner; primary implementer)
**Approved by:** Matt 2026-05-27 (framing brief Q1-Q11 RATIFIED; Wave 0.5 ✅ CLOSED 2026-05-27; KR autonomous on Wave 1 dispatch authoring per scope-doc § 4.1)
**Estimated effort:** ~1 week anchor (per framing brief Q10 quality > timeline; extends as needed)
**Acceptance:** doc 46 concentration architecture Layers 1-4 + 7 implemented; algorithm enforces stat-range bounds + affix migration + capability scope reduction + trigger vocabulary + synergy scan refined; jack-ryan Gate-2 PASS; Disciplines #33 + #34 canonically backed (RATIFIED via SC-1)

## Context

Cycle 14 Wave 1 implements doc 46 concentration architecture **Layers 1-4 + Layer 7** (Wave 2 handles Layers 5 + 8 + 9 in a follow-on dispatch). Per framing brief § 2 Wave 1, this wave addresses the **capability-soup pattern** that Cycle 13 produced empirically — 22 mechanic-alterations per endgame character driven by vocabulary poverty + scope unboundedness + missing concentration discipline.

**The architectural through-line** (doc 46 § 1): **identity emerges from chain composition + T4 selection + 4-6 build-defining items**. Other equipment is stat-affix support. Wave 1 implements the algorithm-side enforcement of this principle through 5 layers:

- **Layer 1 (Discipline #33 RATIFIED)** — stat-range bounds: bounded vs unbounded stat dimensions; algorithm enforces caps at gen-time + runtime (two-layer enforcement)
- **Layer 2** — affix migration: `general_passive_*` entries move OUT of legendary capability pool, INTO Magic/Rare/Epic partition affixes (these were stat boosts disguised as mechanic-altering capabilities — gamora SC-4 research confirmed via empirical str_01 / wis_04 / dex_04 inspection)
- **Layer 3** — capability scope reduction: drop `character_wide` + `chain_wide` from legendary capability scope vocabulary (those are T4 territory); new local scopes per doc 46 § 5 (slot-bound / trigger-bound / skill-specific / item-family / state-conditioned)
- **Layer 4** — trigger condition vocabulary expansion: ~50+ conditions across 11 families per SC-4 legolas research (63 conditions catalogued + 5 critical pattern_id dedup clusters; AI-tell mitigations)
- **Layer 7 (Discipline #34 RATIFIED via SC-1 — composition extension)** — compositional synergy scan refined: Pass 1 thematic seeds ENCOURAGED (cross-element / cross-mechanic combinations); Pass 2 redundancy FILTERED via same-pattern_id dedup + same-trigger-window cap

Wave 2 (subsequent dispatch) handles Layer 5 concentration probability + Layer 8 set keying + Layer 9 class-agnostic drops.

**Cross-seam dependency:** rocket's `gear_instance_generator.py` is the primary touch surface. Pattern-A queries to gandalf for design-spec on probability tables, capability scope semantics, synergy scan thresholds. Pattern-A queries to legolas for SC-4 vocabulary detail.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/46-concentration-architecture-2026-05-27.md` — particularly:
  - § 1 architectural through-line (concentration over distribution)
  - § 2 Layer 1 stat-range bounds + caps table
  - § 3 Layer 2 affix migration (general_passive_* → partition affixes)
  - § 5 Layer 3 capability scope reduction (new local scopes)
  - § 4 Layer 4 trigger condition vocabulary (11 families)
  - § 7 Layer 7 compositional synergy scan refined (Pass 1 thematic seeds; Pass 2 redundancy filter)
  - § 13 amendment list to doc 40 (already landed via SC-2 at `f56ce8b`)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — AS AMENDED at `f56ce8b`: § 0.1 amendment-pass-record; D9/D33/D38/D51/D54/D55/D56 + others marked AMENDED
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-4-trigger-vocabulary.md` — legolas SC-4 research (**LOAD-BEARING for Layer 4**): 63 trigger conditions across 11 families; 5 critical pattern_id dedup clusters (counter_on_defensive direct Cycle 13 failure-mode match; attack_on_hit; resource_threshold_high; buff_stack_accumulation; periodic_repeating); 3 highest AI-tell risk conditions flagged (on_hit / on_enemy_killed / every_n_seconds); 5 open questions for Wave 1 design call
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-legendary-t4-reference-table.md` — empirical reference table that surfaced capability-soup pattern (the failure mode Wave 1 architecturally remediates)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 2 Wave 1 + § 1 L3 (#33 + #34 candidates RATIFIED via SC-1)
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 2 Wave 1 + § 5 disciplines
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines #33 stat-range bounds + #34 concentration (both RATIFIED via SC-1 commit `d148808`)
- `~/Games/reincarnated-engine/src/reincarnated/generation/gear_instance_generator.py` — primary touch surface
- `.claude/skills/reincarnated-rocket-operating-procedure`
- `.claude/skills/reincarnated-hive-mind-protocol`
- `.claude/skills/reincarnated-engineering-disciplines`

## Math-before-code

Per Discipline #18 + #1, **four math-notes** recommended BEFORE implementation:

1. **Layer 1 stat-range bounds math-note** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-layer-1-stat-range-bounds-math-2026-05-27.md` documenting:
   - Per-stat cap table per doc 46 § 2 (crit chance / DR / movement speed / etc. — bounded list with explicit upper bounds)
   - Two-layer enforcement strategy: gen-time clamp + runtime assertion
   - Discipline #33 compliance pattern (RATIFIED via SC-1)

2. **Layer 2 affix migration math-note** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-layer-2-affix-migration-math-2026-05-27.md` documenting:
   - Inventory of `general_passive_*` entries currently in legendary capability pool (rocket inspects existing data)
   - Migration mapping: each entry → Magic/Rare/Epic partition affix slot
   - Backwards-compat: do migrated entries lose their old capability_modifier provenance? Document.

3. **Layer 3+4 capability scope + trigger vocabulary math-note** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-layer-3-4-capability-scope-trigger-vocab-math-2026-05-27.md` documenting:
   - New local scope enum (slot-bound / trigger-bound / skill-specific / item-family / state-conditioned per doc 46 § 5)
   - Drop list: character_wide + chain_wide (move to T4 territory)
   - Trigger vocabulary mapping from SC-4 research (63 conditions across 11 families)
   - Per-condition composition properties consumed from SC-4 (`trigger_id` / `family` / `pattern_id` / `trigger_window` / `concentration_fit` / `thematic_seed` / `synergy_pattern` / `ai_tell_risk`)
   - AI-tell guardrails for on_hit / on_enemy_killed / every_n_seconds (3 highest-risk conditions per SC-4 § 7.3)

4. **Layer 7 synergy scan refined math-note** at `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-layer-7-synergy-scan-refined-math-2026-05-27.md` documenting:
   - Pass 1: thematic seed encouragement algorithm (cross-element / cross-mechanic combinations promoted)
   - Pass 2: redundancy filter algorithm:
     - same-pattern_id dedup (cap at 1 per loadout per pattern; e.g., counter_on_defensive cluster cap=1)
     - same-trigger-window cap (max 2 ACTION-family + max 2 DEFENSE-family instant-window per loadout per SC-4 § 7.3)
   - Layer 7 composition with Layer 5 (Wave 2): probability gate at tier-level
   - Discipline #34 compliance pattern (concentration; RATIFIED via SC-1)

Math-notes are jack-ryan Gate-1 inputs.

## Cross-seam contract change? (Principle 6 gate)

**PARTIAL** — Wave 1 modifies generation-side algorithms but doesn't change inter-seam JSON shape directly. The character JSON `gear_representative` capability/triggered_passive fields shift in *content* (fewer stat-disguised entries; tighter scope; new trigger vocabulary; deduplicated patterns) but not in *shape*. Cross-seam consumers (gamora damage_resolver; star-lord Track C transform) read the same field names.

**Round-trip: not applicable for cross-seam contract**. Intra-seam smoke test required:
- Generate test season post-Wave-1; verify per-character endgame loadout has ≤6 mechanic-altering items (down from Cycle 13's ~22)
- Verify no `general_passive_*` entries remain in legendary capability pool (Layer 2 migration verified empirically)
- Verify no `character_wide` or `chain_wide` capabilities emit at legendary tier (Layer 3 scope reduction verified)
- Verify trigger vocabulary uses ~63 SC-4 catalogued conditions (Layer 4 expansion verified)
- Verify synergy scan filter prevents 2x counter_on_defensive / 2x speed_boost_on_dodge patterns (Cycle 13 failure-mode regression test)

**MIGRATION.md** at `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md § Wave 1` capturing:
- Layer-by-layer algorithm change summary
- Discipline #33 + #34 enforcement points (cross-reference SC-1 canonical writes)
- Empirical regression checks (Cycle 13 capability-soup patterns no longer reproducible)

## Scope

### Pre-implementation

- [ ] Author 4 math-notes per § Math-before-code above
- [ ] Pattern-A query to gandalf: confirm design-spec for Layer 5 probability gate (Wave 2 spec; may inform Layer 7 Pass 2 cap thresholds in Wave 1)
- [ ] Pattern-A query to gandalf (optional): hybrid pattern + thematic seed semantics for Layer 7 Pass 1
- [ ] Route math-notes to jack-ryan Gate-1 DESIGN-MODE review WITHIN your session (per OP convention)

### Item 1 — Layer 1 stat-range bounds (~1-2 days)

- [ ] Author canonical cap table per doc 46 § 2 (stat-range bounds list)
- [ ] Amend `gear_instance_generator.py` to enforce caps at gen-time (clamp values to range)
- [ ] Add runtime assertion layer (Discipline #33 two-layer enforcement)
- [ ] Smoke: generate test season; verify no stat exceeds cap; verify runtime assertion catches engineered violations

### Item 2 — Layer 2 affix migration (~1-2 days)

- [ ] Inventory existing `general_passive_*` entries in legendary capability pool (audit via DB query OR data inspection)
- [ ] Map each entry to Magic/Rare/Epic partition affix slot per doc 46 § 3
- [ ] Update `gear_instance_generator.py` to migrate these at gen-time (or at data-layer pre-gen)
- [ ] Smoke: generate test season; verify no `general_passive_*` entries in legendary capability pool; verify equivalent entries appear in Magic/Rare/Epic affix slots

### Item 3 — Layer 3 capability scope reduction (~1 day)

- [ ] Update capability scope enum to new local scopes per doc 46 § 5 (slot-bound / trigger-bound / skill-specific / item-family / state-conditioned)
- [ ] Drop `character_wide` + `chain_wide` from legendary capability scope vocabulary
- [ ] Migrate any existing entries with those scopes — recommend: surface as Wave 1 candidates for T4 promotion (route to gandalf for design call) OR retire if not load-bearing
- [ ] Smoke: generate test season; verify no `character_wide` or `chain_wide` capabilities at legendary tier

### Item 4 — Layer 4 trigger vocabulary expansion (~1-2 days)

- [ ] Consume SC-4 legolas research catalog (63 conditions across 11 families) — `agentic_orchestration/research/2026-05-27-cycle-14-sc-4-trigger-vocabulary.md`
- [ ] Update trigger condition vocabulary in capability template library
- [ ] Implement per-condition composition properties (`pattern_id`, `trigger_window`, `concentration_fit`, etc.) so Layer 7 synergy scan can consume them
- [ ] Implement AI-tell guardrails for 3 highest-risk conditions (on_hit / on_enemy_killed / every_n_seconds) per SC-4 § 7.3 mitigations
- [ ] Smoke: generate test season; verify trigger conditions sampled from expanded ~63-condition vocabulary; verify dedup pattern_id clusters dedupe correctly

### Item 5 — Layer 7 synergy scan refined (~1-2 days)

- [ ] Implement Pass 1: thematic seed encouragement algorithm (cross-element / cross-mechanic combinations promoted)
- [ ] Implement Pass 2: redundancy filter:
  - same-pattern_id dedup (cap 1 per loadout; counter_on_defensive cluster cap=1)
  - same-trigger-window cap (max 2 ACTION-family + max 2 DEFENSE-family instant-window)
- [ ] Cycle 13 regression test: verify str_01 4x damage-reflection pattern no longer emerges; wis_04 + dex_04 duplicate template patterns prevented
- [ ] Smoke: 16-character test season; verify endgame loadout has ≤6 mechanic-altering items per character (down from Cycle 13's ~22); verify capability-soup pattern empirically prevented

### Closure

- [ ] Author generation/MIGRATION.md § Wave 1 per § Cross-seam contract above
- [ ] Update generation/AGENT_STATE.md
- [ ] Cross-seam round-trip smoke: gamora damage_resolver consumes Wave 1 character JSON cleanly (no shape change; content change only); star-lord Track C transform (future Wave 5+) consumes cleanly
- [ ] jack-ryan Gate-2 review of Wave 1 outputs (includes Disciplines #33 + #34 empirical verification)
- [ ] Tag: `rocket/v1.5-wave-1-concentration-architecture-layers-1-4-7` (or rocket-OP-preferred)
- [ ] Append completion record to dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] Layer 1 stat-range bounds enforced two-layer (gen-time + runtime); Discipline #33 compliance verified empirically
- [ ] Layer 2 affix migration complete; no `general_passive_*` in legendary capability pool
- [ ] Layer 3 capability scope reduction live; no `character_wide` / `chain_wide` at legendary tier
- [ ] Layer 4 trigger vocabulary expanded to SC-4 63-condition catalog; AI-tell guardrails active for 3 highest-risk conditions
- [ ] Layer 7 synergy scan refined; Cycle 13 capability-soup regression prevented (≤6 mechanic-altering items per endgame loadout)
- [ ] All 5 dedup pattern_id clusters honored (counter_on_defensive / attack_on_hit / resource_threshold_high / buff_stack_accumulation / periodic_repeating)
- [ ] MIGRATION.md authored
- [ ] AGENT_STATE.md updated
- [ ] Math-notes (4) authored + Gate-1 PASS
- [ ] jack-ryan Gate-2 PASS post-implementation; Disciplines #33 + #34 empirical verification
- [ ] Completion record appended; commit + push + tag

## Out of scope (explicit non-goals)

- Do NOT implement Layer 5 concentration probability table (Wave 2 scope)
- Do NOT implement Layer 6 layered cohesion (Wave 3 scope — Phase 5 cohesion-judge LLM)
- Do NOT implement Layer 8 set keying or Layer 9 class-agnostic drops (Wave 2 scope)
- Do NOT touch damage_resolver / fight engine (gamora's seam; Wave 0.5 closed)
- Do NOT touch substrate library DB (elrond's seam; SC-6b enrichment is canonical)
- Do NOT amend doc 46 or doc 47 (those are canonical; Wave 1 implements against them)
- Do NOT implement per-level scaling formulas (deferred per doc 41 § 4 #1)
- Do NOT regenerate Cycle 13 season (Q9 DISREGARD)
- Do NOT regress synthetic_mode (Discipline #39 LOAD-BEARING; verified RETIRED at Gate-2)

## Open questions for rocket

- **Q-W1-R1**: Layer 7 Pass 2 cap thresholds — are SC-4 recommended caps (1 per pattern_id; 2 ACTION-family + 2 DEFENSE-family instant-window) the right starting point? Pattern-A query to gandalf if uncertain.
- **Q-W1-R2**: Layer 3 capability scope migration — any existing `character_wide` / `chain_wide` entries that warrant T4 promotion (route to gandalf design call) vs retirement? Inspect via DB + decide.
- **Q-W1-R3**: Layer 4 AI-tell guardrails — what's the exact mitigation pattern for on_hit / on_enemy_killed / every_n_seconds? Cohesion-judge LLM (Wave 3) is the primary AI-tell mitigation surface; Layer 4 may flag these conditions for Wave 3 LLM-prompt guardrails OR limit their gen-time emit-rate. Decide + record.
- **Q-W1-R4**: Layer 2 affix migration backwards-compat — do migrated entries lose their old capability_modifier provenance, or carry forward as a hybrid? Rocket decides per Discipline #10 attribution clarity + Discipline #11 empirical inspection of existing data.

## References

- `canonical/46-concentration-architecture-2026-05-27.md` (all 9 layers; Wave 1 implements Layers 1-4 + 7)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (as amended at `f56ce8b`)
- `agentic_orchestration/research/2026-05-27-cycle-14-sc-4-trigger-vocabulary.md` (Layer 4 substantive input)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-legendary-t4-reference-table.md` (empirical motivation)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 2 Wave 1
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 2 + § 5
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #33 + #34 (RATIFIED via SC-1 commit `d148808`)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` (Path A architectural commitment at `f053281`)
- Engineering disciplines #1 + #10 + #11 + #18 + #33 + #34
- Hive-mind protocol § 4 (decision-routing) + § 7 (math hotspots)
