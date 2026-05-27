# Dispatch — 2026-05-27 — legolas — Cycle 14 SC-4 Mode A trigger condition vocabulary research

**From:** knight-rider
**To:** legolas (research + catalogue-crawl seam)
**Approved by:** Matt 2026-05-27 (framing brief Q5 ratified — sidecar list confirmed including SC-4)
**Estimated effort:** ~8-12 hours Mode A analytical research
**Acceptance:** research artifact filed at `agentic_orchestration/research/2026-05-27-cycle-14-sc-4-trigger-vocabulary.md` cataloguing ~50+ trigger conditions across 11 families with cross-game prevalence + composition properties

## Context

Cycle 14 Wave 1 implements doc 46 Layer 4 — trigger condition vocabulary expansion (~50+ conditions across 11 families: action / defense / resource / state / enemy-state / environmental / skill-conditioned / combo / positional / element / timer). The current Cycle 13 trigger vocabulary is too narrow — empirical inspection of the legendary T4 reference table surfaced 2x speed_boost_on_dodge + 2x defense_aura patterns (wis_04 / dex_04) which is duplicate-template stacking from vocabulary poverty.

This sidecar gates Wave 1 (per framing brief § 5 SC-4 entry: "Wave 1 gate"). Legolas Mode A research from ARPG community-canonical trigger condition catalogues (PoE / D2 LoD / D3 / D4 / Last Epoch / Grim Dawn / Lost Ark) informs gandalf's design-spec authoring for the expanded vocabulary + rocket's capability template library expansion at Wave 1.

The vocabulary must support doc 46 Layer 7 (compositional synergy scan refined extension to legendary capability + triggered_passive generation) — i.e., the trigger conditions enable thematic seed combinations (Pass 1 thematic seeds encouraged) while remaining filterable for redundancy (Pass 2 same-pattern_id dedup + same-trigger-window cap).

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/46-concentration-architecture-2026-05-27.md` § 4 (Layer 4 trigger vocabulary expansion target) + § 5 (Layer 5 concentration probability) + § 7 (Layer 7 compositional synergy scan)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — particularly capability scope + triggered_passive entries
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-legendary-t4-reference-table.md` — empirical reference table that surfaced the capability-soup pattern; this artifact diagnoses vocabulary poverty
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 2 Wave 1 + § 5 SC-4
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- `.claude/skills/reincarnated-legolas-operating-procedure` — Mode A protocol
- Prior legolas Cycle 13 SC-4 9-category-synergy research at `agentic_orchestration/research/` for format reference

## Math-before-code

Vocabulary expansion is design-spec input, not math hotspot per se. The composition properties (synergy / dedup / trigger-window-cap properties of trigger conditions) inform compositional algorithm design at Wave 1 — gandalf consumes legolas' vocabulary catalog + composition properties when authoring the Wave 1 design-spec.

## Cross-seam contract change?

**NO** — research output, no code emission. Round-trip not applicable.

## Scope

- [ ] Survey 7+ ARPGs (PoE / D2 LoD / D3 / D4 / Last Epoch / Grim Dawn / Lost Ark; add Path of Exile 2 / Wolcen / Diablo Immortal if community catalogues are accessible) for trigger condition catalogues
- [ ] Organize into the 11 trigger families per doc 46 Layer 4 anchor
- [ ] For each family, target ~5-10 trigger conditions = ~50-110 total vocabulary entries
- [ ] Composition properties per condition (per § 7.2 below)
- [ ] AI-tell + redundancy patterns to avoid (per § 7.3 below)
- [ ] File research artifact at `agentic_orchestration/research/2026-05-27-cycle-14-sc-4-trigger-vocabulary.md`
- [ ] Append completion record to this dispatch file
- [ ] Round-trip: not applicable

## Acceptance criteria

- [ ] Research artifact filed with ~50+ trigger conditions catalogued across 11 families
- [ ] Per-condition composition-property fields (per § 7.2 below)
- [ ] Cross-game prevalence noted per condition (which games use this; how prevalent)
- [ ] Concentration-architecture-fit assessment (does the condition support Layer 5 concentration without triggering Layer 7 redundancy filter?)
- [ ] AI-tell + redundancy mitigation patterns surveyed (per § 7.3 below)
- [ ] Completion record appended; commit + push per Matt 2026-05-27 per-cycle push pattern

## Out of scope (explicit non-goals)

- Do NOT implement code — Wave 1 implementation work owned by rocket informed by this research + gandalf design-spec
- Do NOT author capability template library entries — that's rocket's seam at Wave 1
- Do NOT make probability-table calls — Layer 5 concentration probability is gandalf's design-spec call at Wave 1 design session
- Do NOT enter Mode B catalogue crawl — Mode A analytical research only
- Do NOT touch substrate library / DB / external systems — read-only research

## Research questions (legolas resolves)

### 7.1 The 11 trigger families (per doc 46 Layer 4)

Per family, catalog ~5-10 trigger conditions from community sources:

| Family | Examples (seed; legolas expands) |
|---|---|
| **action** | on-attack / on-skill-use / on-cast / on-channel-tick / on-melee-hit |
| **defense** | on-block / on-dodge / on-parry / on-take-damage / on-near-death |
| **resource** | on-energy-spend / on-mana-low / on-resource-full / on-energy-tick |
| **state** | while-stationary / while-moving / while-low-hp / while-channeling |
| **enemy-state** | on-enemy-killed / on-enemy-stunned / on-enemy-low-hp / on-enemy-bleeding |
| **environmental** | in-cold-region / in-stormy-weather / on-ground-effect / in-shadow |
| **skill-conditioned** | on-T4-active / on-chain-finisher / on-spell-cast / on-physical-skill |
| **combo** | on-N-hits-in-Xs / on-skill-rotation-complete / on-buff-stack-cap |
| **positional** | on-flank-attack / on-backstab / on-close-range / on-melee-range |
| **element** | on-fire-skill / on-element-react / on-cold-immunity-breach |
| **timer** | every-N-seconds / once-per-encounter / for-N-seconds-after-X |

### 7.2 Per-condition composition properties

For each catalogued condition:

- `trigger_id` — unique identifier (e.g., `on_block_counter`)
- `family` — one of the 11 families
- `cross_game_prevalence` — count of games using this (1-7+)
- `frequency_class` — `common` / `uncommon` / `rare` (genre-canonical perception)
- `pattern_id` — for dedup grouping (e.g., counter_on_block / counter_on_dodge / counter_on_parry → pattern_id="counter_on_defensive")
- `trigger_window` — instant / brief (≤1s) / brief-buff (1-5s) / sustained-buff (5-30s) / encounter / persistent — for Layer 7 trigger-window-cap discipline
- `concentration_fit` — `legendary_capability` / `legendary_triggered_passive` / `epic_triggered_passive` / `set_bonus` / `multi-tier` — where this condition fits in doc 46 Layer 5 concentration probability table
- `thematic_seed` — element + archetype affinity (e.g., "fire + heavy_melee + offensive_aggressive") for Layer 7 Pass 1 thematic seeding
- `synergy_pattern` — what other conditions this composes with (Layer 7 Pass 1 synergy scan candidates)
- `ai_tell_risk` — risk that this condition produces formulaic-sounding-content when LLM-narrated; mitigations per § 7.3

### 7.3 AI-tell + redundancy patterns

- **Q-SC4-1**: Across the 11 families, which conditions produce highest AI-tell risk when LLM-narrated (e.g., "on-attack" is generic and produces "and behold, your attack..." flavor pattern)? Survey community-flavor-text examples + recommend mitigations.
- **Q-SC4-2**: Which conditions in the vocabulary cluster as same-pattern_id risks per Layer 7 Pass 2 dedup discipline? Recommend pattern_id assignments + the cluster size for each pattern (e.g., counter_on_defensive cluster = 3 conditions; cap firing to 1 per character).
- **Q-SC4-3**: Which conditions have same-trigger-window risks per Layer 7 Pass 2 cap discipline? Map trigger-window collisions across the vocabulary (e.g., 4 different counter conditions all firing in 1s window = collision).
- **Q-SC4-4**: Which conditions break the concentration discipline by reading as "skills disguised as triggered passives" (per the empirical str_01 / wis_04 / dex_04 pattern)? Recommend redirection to chain composition or T4 layer.

## References

- `canonical/46-concentration-architecture-2026-05-27.md` § 4 (Layer 4) + § 5 (Layer 5) + § 7 (Layer 7)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (capability + triggered_passive entries)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-legendary-t4-reference-table.md` (empirical motivation)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 2 Wave 1 + § 5 SC-4
- Prior legolas Mode A research artifacts at `agentic_orchestration/research/`
- Path of Exile wiki / D2 LoD community catalogs / Last Epoch wiki / Grim Dawn community catalogs / Lost Ark engraving + tripod community catalogs

---

## Completion Record

**Status:** COMPLETE
**Completed:** 2026-05-27
**Executor:** legolas (Mode A analytical research)
**Artifact:** `agentic_orchestration/research/2026-05-27-cycle-14-sc-4-trigger-vocabulary.md`

**Acceptance criteria check:**
- [x] Research artifact filed at named path
- [x] 63 trigger conditions catalogued across all 11 families (exceeds 50+ target)
- [x] Per-condition composition-property fields: trigger_id / family / cross_game_prevalence / frequency_class / pattern_id / trigger_window / concentration_fit / thematic_seed / synergy_pattern / ai_tell_risk — all populated
- [x] Cross-game prevalence noted per condition (1-7+ scale; sources cited)
- [x] Concentration-architecture-fit assessment per condition (Layer 5 tier mapping)
- [x] AI-tell + redundancy mitigation patterns surveyed (Q-SC4-1 through Q-SC4-4 answered)
- [x] Completion record appended

**Family counts:**
- action: 6 conditions
- defense: 6 conditions
- resource: 5 conditions
- state: 6 conditions
- enemy-state: 6 conditions
- environmental: 6 conditions (note: 3 of 6 are low-priority for solo-only game; see knowledge gaps)
- skill-conditioned: 6 conditions
- combo: 5 conditions
- positional: 5 conditions
- element: 5 conditions
- timer: 5 conditions
- TOTAL: 63 conditions

**Pattern_id dedup clusters identified:**
- `counter_on_defensive` — 3 members (on_block / on_dodge / on_parry if added) — CRITICAL dedup risk
- `attack_on_hit` — 2 members (on_hit / on_melee_hit) — HIGH dedup risk
- `resource_threshold_high` — 2 members (on_resource_full / on_resource_pop) — HIGH dedup risk
- `buff_stack_accumulation` — 2 members (on_n_hits_in_window / on_buff_stack_cap) — HIGH dedup risk
- `periodic_repeating` — 2 members (every_n_seconds / on_resource_tick) — MEDIUM dedup risk

**Key open questions for Wave 1 design call:**
1. Environmental family — near_ally / isolated / in_shadow are not design-fit for a solo-only game; recommend dropping these 3 from the v1 vocabulary. Reduces environmental to 3 conditions (on_ground_effect / while_in_element_zone / in_objective_area).
2. Positional family — on_flank_attack / while_kiting have weak cross-game vocabulary backing (1-2/7). Recommend keeping on_back_attack / on_front_attack / on_melee_range as the core 3; flag the others as low-confidence extensions.
3. on_combo_break — only 1/7 cross-game; not recommended for v1 vocabulary. Drop from combo family.
4. Counter_on_defensive cluster cap — is 1-per-loadout the right hard cap, or should gandalf's design-spec consider allowing 1 per family TYPE (1 block trigger + 1 dodge trigger) as long as effect-categories differ? Dispatch flags the collision but the design call is gandalf's.
5. AI-tell line (doc 46 Layer 6 D7 reference): on_hit / on_enemy_killed / every_n_seconds are the three highest-risk conditions. Gandalf's Phase 5 cohesion-judge LLM architecture should include specific prompt guardrails for these three when they appear on Legendary T1/T2 items.
