# Cycle 14 — Phase 5 Cohesion Coalescence + Track D Content Gap Closure + Concentration Architecture (9 layers) Framing Brief

> **STATUS:** **RATIFIED 2026-05-27** — Matt ratified Q1-Q11 in full. Canonical authority basis for Cycle 14 hive-mind scope-doc + KR kicker.
>
> **Q4 + Q9 + Q10 carry Matt sharpening clarifications worth highlighting** (see § 12 ratification record):
> - **Q4 "extremely confirm.. retire it"** — discipline #39 (no-synthetic-stub-as-permanent-fallback) is load-bearing; emphatic lock
> - **Q9 disposition shift** — Cycle 13 season cycle-13-mechanical-season-001 DISREGARDED ("not relevant; made to fit synthetic gauntlet"); Cycle 14 generates fresh roster end-to-end (not regenerate-Cycle-13)
> - **Q10 quality > timeline** — Matt verbatim "extend timeline as needed for Wave 0.5 and all waves. The goal is not to ship something but to ship a game (playable characters that run the gauntlet in band)" — Cycle 14 NOT timeline-gated; "in band" means actual cohort-band KPM, not synthetic_mode override

**Author:** gandalf (story-and-design steward)
**Authority basis:** Matt 2026-05-27 directives:
- Doc 46 (concentration architecture; 9 layers) ratified + § 6.5 gauntlet representative loadout discipline amendment
- Doc 47 (damage scaling architecture; physical / magical / hybrid routing) ratified
- Cycle 14 framing brief authorization to draft (this doc)
- Synthetic-sim regression risk surfaced (Matt 2026-05-27 verbatim "will we run any risk of knight-rider and team deciding to run a synthetic or partial gauntlet vs the prepared version within cycle 14") — load-bearing discipline lock embedded per § 6

**Companion docs (anchor + context):**
- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/02-roadmap.md` — engine build visual-flow progress tracker
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` — engine workflow + content lifecycle dependency chain
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation (D1-D86)
- `canonical/41-progression-framework-2026-05-27.md` — L50 hybrid progression framework
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` — partition design intent
- `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` — T4 algorithm Phases 1-2
- `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` — T4 Phase 3 scope-dimension
- `canonical/45-spec-driven-gear-gen-wave-4-rocket-track-intent-2026-05-27.md` — Wave 4 spec-driven gear gen
- `canonical/46-concentration-architecture-2026-05-27.md` — concentration architecture 9 layers (Cycle 14 sidecar foundation)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — damage scaling architecture (Wave 0.5 prerequisite)
- `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` — Cycle 13 framing brief precedent (RATIFIED)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — Cycle 13 design session closeout
- `agentic_orchestration/skill_handoff_2026-05-27-cycle-13-close.md` — Cycle 13 close wind-down summary
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-legendary-t4-reference-table.md` — empirical reference table that surfaced capability-soup pattern
- `agentic_orchestration/operating-procedures/hive-mind-scope-discipline.md` — per-cycle scope-of-autonomy enumeration discipline
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — engineering disciplines (including queued candidates #33-#39)

---

## 0. TL;DR — what this brief asks Matt to ratify

**Cycle 14 scope = three concurrent threads converging on Phase 5 cohesion coalescence:**

1. **Track D content gap closure** (Wave 0.5; NEW): Cycle 13 scope that wasn't delivered — elements expansion (Foundation passed through → 7 elements unlock) + per-skill mechanical content emission with `damage_scaling_type` per doc 47 + substrate weapon binding output to character JSON + fight engine damage scaling routing
2. **Doc 46 concentration architecture amendments** (Waves 1-2): stat-range bounds + affix migration + capability scope reduction + trigger vocabulary + concentration probability + synergy scan refined + set keying to T4 strategy clusters + class-agnostic drops
3. **Phase 5 cohesion coalescence** (Waves 3-5; Q9 Pattern A original scope): cohesion-judge LLM with layered architecture + spirit-guide data-oracle integration + T4-attuned gear cohesion + D21 acquisition curve calibration + gauntlet sim re-calibration with REAL content (synthetic_mode RETIRED)

**Cycle 14 close = the SUBSTANTIVE delivery point** that Cycle 13 close was originally framed as. Engine generates 16+ characters with real skills + real weapons + real combat validation + Phase 5 cohesion thematic identities.

**LOAD-BEARING discipline lock**: `synthetic_mode` is STRUCTURALLY RETIRED at Wave 0.5 close. Discipline candidate #39 (no-synthetic-stub-as-permanent-fallback) queued. See § 6.

**11 open design questions** for Matt ratification covering scope-of-autonomy, wave sequencing, synthetic-sim retirement discipline, prerequisite gating, sidecars, post-cycle planning.

---

## 1. Locked canon — what's already canonical (cycle inheritance)

These items are canonical from prior canonical-doc work. Matt's ratification on these is implicit unless he amends.

### L1. Architectural foundation (docs 38 + 39 + 40 + 41 + 46 + 47)

- Doc 38 (D1-D10 delivery strategy) — Variant C engine + game; isekai provisional; ~200-220 day timeline
- Doc 39 (Architecture B engine workflow) — substrate-bound at Phase 2; one-way dependency chain
- Doc 40 (Cycle 13 architectural foundation; D1-D86) — Cycle 14 amendments queued per doc 46 § 13
- Doc 41 (L50 hybrid progression framework; ~30-day seasonal duration) — Cycle 14 implements against this
- Doc 46 (concentration architecture; 9 layers) — Cycle 14 sidecar foundation
- Doc 47 (damage scaling architecture; physical / magical / hybrid routing) — Wave 0.5 prerequisite

### L2. Cycle 13 close as-is (PASS-with-WARN ratified)

Per jack-ryan close Gate-2 PASS-with-WARN (commit `482801c`) + KR wind-down summary (commit `249fc92`):
- FRAMEWORK + ARCHITECTURE COMPLETE: T4 algorithm 4 phases / gear gen / compositional synergy scan / scope-dimension selection / multi-T4 architecture / sim infrastructure
- CONTENT LAYER thin (acknowledged WARNs):
  - Per-skill mechanical content NOT generated (Phase 2a gap)
  - Substrate weapon binding output NOT persisted to character JSON (Phase 2c gap)
  - Only 4 of 7 canonical elements emitted (legacy fallback hardcoded VALID_SLOTS)
  - Synthetic-mode stub used in gauntlet sim (Track A remediation; KPM-band-bypass)
  - Defensive cohort 0/16 (synthetic stub limitation)

Cycle 13 close DOES NOT REOPEN. Cycle 14 Wave 0.5 absorbs the content gap.

### L3. Engineering disciplines + 7 queued candidates from doc 46 + 47 sessions

Existing 32 disciplines + amendments apply throughout Cycle 14. 7 candidates queued for jack-ryan SC-2 expansion ratification:
- #33 Stat-range bounds discipline (doc 46 Layer 1)
- #34 Concentration discipline (doc 46 Layer 5)
- #35 Layered cohesion discipline (doc 46 Layer 6)
- #36 Substrate-as-keying-source discipline (doc 46 Layer 8)
- #37 Class-agnostic drop discipline (doc 46 Layer 9)
- #38 Damage-scaling-path discipline (doc 47 § 6)
- **#39 No-synthetic-stub-as-permanent-fallback discipline** (NEW; this brief § 6)

### L4. Wave 0.5 prerequisite (Track D content gap closure) gates Phase 5 cohesion

Wave 3 Phase 5 cohesion-judge LLM consumes the per-skill content + substrate weapon binding + damage scaling routing from Wave 0.5. Wave 0.5 MUST land before Wave 3 fires.

### L5. Synthetic_mode RETIREMENT discipline (LOAD-BEARING — see § 6)

`synthetic_mode=True` in `t4_sim_cycling.py` + `gauntlet_sim.py` is structurally retired at Wave 0.5 close. Production sim paths use real per-skill content + real substrate weapon stats + damage_scaling_type routing per doc 47.

### L6. Cycle 14 close criterion (per § 7 acceptance)

By Cycle 14 close:
- All 7 elements emitted across season generation
- Per-skill mechanical content for chain T1-T3 + T4 capstones with proper damage_scaling_type routing
- Substrate weapon binding output reflected in character JSON
- Fight engine executes real combat (NO synthetic stub) with proper physical vs magical vs hybrid damage routing
- Concentration architecture (doc 46) implemented (all 9 layers)
- Phase 5 cohesion coalescence (cohesion-judge LLM + spirit-guide data-oracle + T4-attuned gear cohesion + acquisition curve)
- Defensive cohort empirical validation IMPROVES with real content
- Loadout app + HTML doc render the "character that was and is" with real content

---

## 2. Cycle 14 wave structure (proposed)

Cycle 14 fires as a multi-wave hive-mind cycle. Proposed wave structure:

### Wave 0 — Scope-doc + canonical authoring + sidecar dispatches

**Duration:** 1 week
**Owners:** gandalf (canonical) + KR (orchestration) + jack-ryan (Gate-1 critique-pair)
**Outputs:**
- Cycle 14 scope-doc at `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md`
- Doc 40 amendments per doc 46 § 13 + doc 47 § 5
- Doc 47 ratification (canonical doc already authored 2026-05-27; jack-ryan Gate-2 verification)
- Sidecar dispatches authored (SC-1 through SC-7; see § 8)

### Wave 0.5 — Track D content gap closure (NEW; LOAD-BEARING)

**Duration:** 1-2 weeks wall-clock
**Owners:** rocket (per-skill emission + substrate binding output) + gamora (damage scaling routing + synthetic_mode retirement) + elrond (substrate weapon stat audit) + jack-ryan (Gate-2 critique)
**Scope:**

| Item | Owner | Acceptance criterion |
|---|---|---|
| **Elements expansion** | rocket | `season_generation_pipeline.py` instantiates Foundation with 7 rotating substrates + passes to element selector; element_biases verified for lightning/holy/shadow; subsequent test season exercises all 7 elements (substrate-led; may not all emit in v1 endgame scope but unlock for v1.1+) |
| **Per-skill mechanical content emission** | rocket | Phase 2a per-skill emission for chain T1-T3 nodes; each skill has: name (placeholder pre-Phase-5) + damage_multiplier + cooldown_seconds + energy_cost + geometry_type + bc_axis_contribution + `damage_scaling_type` (per doc 47) + `scaling_attribute` + tier + chain_id; schema match v2_narrow_phase_5 lineage where applicable; loadout-app season schema compatible |
| **Substrate weapon binding output** | rocket + elrond | Phase 2c substrate-bound weapon reference persists to character JSON; `gear_representative.main_weapon` includes substrate_weapon_id + substrate_canonical_name + base_physical_damage + spell_damage_modifier + element_affinity_modifiers + weapon_type_family; per-attribute weapon profile per doc 47 § 3 |
| **Damage scaling routing** | gamora | Fight engine `damage_resolver` routes per skill's `damage_scaling_type`; calculate_physical / calculate_magical / calculate_hybrid functions per doc 47 § 4 |
| **Synthetic_mode RETIREMENT** | gamora | `grep "synthetic_mode" src/reincarnated/` in production paths returns ZERO matches; test fixtures may retain for backwards-compat verification only; production gauntlet sim uses real per-skill content + real weapons; Discipline candidate #39 ratified |

**Gate:** jack-ryan Gate-2 PASS on Wave 0.5 close; synthetic_mode retirement verified empirically via grep + test suite

**Note**: this wave is LOAD-BEARING for Wave 3. Phase 5 cohesion-judge LLM consumes per-skill content + weapon binding. Without Wave 0.5, Phase 5 has nothing to cohere.

### Wave 1 — Concentration architecture Layers 1-4 + 7

**Duration:** 1 week
**Owners:** rocket + gandalf design-spec + jack-ryan Gate-2
**Scope:**
- **Layer 1**: Stat-range bounds canonical authoring + algorithm enforcement (rocket `gear_instance_generator.py` amendment)
- **Layer 2**: Affix migration (`general_passive_*` → partition affixes per Magic/Rare/Epic rarity)
- **Layer 3**: Capability scope reduction (drop character_wide + chain_wide from legendary capability scope; new local scopes per doc 46 § 5)
- **Layer 4**: Trigger condition vocabulary expansion (~50+ conditions across 11 families; capability template library expansion)
- **Layer 7**: Compositional synergy scan refined extension to legendary capability + triggered_passive generation (thematic seeds encouraged + redundancy filtered)

**Gate:** jack-ryan Gate-2 PASS on Wave 1; Discipline candidates #33 + #34 ratified

### Wave 2 — Concentration architecture Layers 5 + 8 + 9

**Duration:** 3-5 days
**Owners:** rocket + gandalf design-spec + jack-ryan Gate-2
**Scope:**
- **Layer 5**: Concentration probability table by tier (Common-Rare 0% cap; Epic 25% trig-passive only; T0/T0.5 30-50% cap XOR trig; T1 75% both; T2 100% both with T4-attune; sets replace individual cap)
- **Layer 8**: Set keying to T4 strategy × element clusters (NEW `set_generator.py` module; ~12-20 named sets per season; cross-character shareable)
- **Layer 9**: Class-agnostic spec-driven per-drop generation (drop pipeline amendment)
- **§ 6.5 amendment**: Gauntlet sim representative loadout discipline (full T1 + set replacement where matching set exists per Layer 8)

**Gate:** jack-ryan Gate-2 PASS on Wave 2; Discipline candidates #36 + #37 ratified

### Wave 3 — Phase 5 cohesion-judge LLM architecture (layered cohesion per doc 46 Layer 6)

**Duration:** 1 week
**Owners:** gandalf (design-spec for LLM prompt structure) + star-lord (LLM integration) + rocket (call architecture)
**Scope:**
- Cohesion-judge LLM call structure with layered cohesion prompt (CORE identity from chain composition weighted toward lower tiers + ENDGAME nod additive)
- Templated input/output structure per AI-tell discipline D7
- Three core disciplines tested (identity-without-gear / T4-choice-independence / endgame-nod-additivity per doc 46 § 7.3)
- Spirit-guide data-oracle integration (D28-D32)
- Phase 5 cohesion-judge calibration spec produces real skill names + flavor + descriptions (replacing Wave 0.5 placeholders)
- Heroic Spirit narrative cohesion (D36) — T4 paths as Spirit aspects
- Replay value within Servant (D37) via multi-T4 + attunement + set completions

**Gate:** jack-ryan Gate-2 PASS on Wave 3; Discipline candidate #35 ratified

### Wave 4 — T4-attuned gear cohesion + D21 acquisition curve calibration

**Duration:** 3-5 days
**Owners:** gandalf design-spec + rocket implementation + gamora acquisition math
**Scope:**
- Tier 1+2 legendary/set T4-attunement alignment confirmation per content-compositional pattern (Block B1)
- Set bonus content composition with T4 strategy clusters
- Acquisition curve calibration — D21 Option A specifics under L50 hybrid engagement window
- Pure RNG with calibrated rate (no smart-loot pity)
- Gap-filling discipline (D80) — drop calibration accounts for stat-sheet gaps
- Spirit-guide projection language honesty (D31)

**Gate:** jack-ryan Gate-2 PASS on Wave 4

### Wave 5 — Gauntlet sim re-calibration with REAL content + cohesion validation

**Duration:** 3-5 days
**Owners:** gamora (gauntlet sim re-run) + gandalf (cohesion validation) + jack-ryan (Cycle 14 close Gate-2)
**Scope:**
- Gauntlet sim runs against REAL per-skill content + REAL substrate weapon stats + REAL damage_scaling_type routing
- Synthetic_mode VERIFIED RETIRED (grep + test suite)
- 18 endgame reference encounters × real cohort behavior (Defensive expected to validate empirically with real defensive kits, not 0/16)
- WR-bracket pass calc derives from real per-skill + real weapon math
- Real KPM bands measured (cohort bands viable; not 0% pass rate)
- Cohesion validation against doc 46 Layer 6 disciplines (identity-without-gear / T4-choice-independence / endgame-nod-additivity)
- Initial mechanical+cohesion season generation: one season's worth of kits + gear + cohesion-coalesced identities

**Gate:** Cycle 14 close Gate-2 PASS → milestone marker → post-cycle sequencing decision

---

## 3. Wave 0.5 — Track D content gap closure (LOAD-BEARING DETAIL)

This wave is the prerequisite linchpin. Detail per doc 47 § 7 + doc 46 Layer 1.

### 3.1 Elements expansion (rocket; ~2-4 hrs)

Current state per `element/selector.py:49`: `VALID_SLOTS = ("fire", "wind", "water", "earth")` legacy fallback fires when no Foundation passed. Cycle 13 emitted 4 of 7 elements as result.

Fix:
1. Amend `season_generation_pipeline.py:w5r1_generate_kit_candidates` (or equivalent) to instantiate Foundation with all 7 rotating substrates
2. Pass Foundation through to element selector via `select_seasonal_elements(...)` call
3. Verify `element_biases.py` defines couplings for lightning / holy / shadow elements per BC attribute
4. Test: generate a test season with all 7 elements available; verify subsequent generations exercise lightning / holy / shadow at substrate-led rates

Acceptance: substrate generates against full 7-element catalog; v1 endgame scope may not emit all 7 immediately (substrate-led per Q10) but unlock the design space for v1.1+ generation cycles.

### 3.2 Per-skill mechanical content emission (rocket; ~2-5 days)

Current state: Phase 2a kit composition produces `chain_composition` COUNTS only. Per-skill content (names + damage_multiplier + cooldown_seconds + energy_cost + geometry_type + bc_axis_contribution) does NOT emit.

Fix:
1. Implement Phase 2a per-chain per-node skill emission per `skill-system-2026-05-24.md` § 1 (10-15 nodes per kit; mechanic-altering passives; per-tier organization)
2. Each skill emits with schema:

```python
class GeneratedSkill:
    skill_id: str               # e.g., "S1_endgame_str_01_chain_1_t1_active_1"
    chain_id: str               # e.g., "t4_chain_1"
    tier: int                   # 1, 2, 3, 4
    name: str                   # placeholder pre-Phase-5; "Earth Chain 1 - T1 Active 1"
    role: str                   # "primary_attack", "utility", "build_defining", etc.
    canonical_element: str      # from kit element or T4 conversion
    geometry_type: str          # single_target / cone / circle / chain / beam / etc.
    timing: AbilityTiming       # cast_time + cooldown structure
    damage_multiplier: float    # scales with skill_level
    energy_cost: float
    cooldown_seconds: float
    damage_scaling_type: str    # physical / magical / hybrid per doc 47
    scaling_attribute: str      # STR / DEX / INT / WIS per doc 47
    tier_coefficient: float     # per skill-system § 8
    bc_axis_contribution: dict  # 8-axis numerical contributions
    effects: list[AbilityEffect] # placeholder pre-Phase-5
    hybrid_pattern: str | None  # physical_with_element_flavor / magical_with_martial_weapon / sum_paths
    hybrid_balance_factor: float | None  # 0.0-1.0 split for hybrid sum_paths
```

3. Schema match v2_narrow_phase_5 `classes.json` `skills[]` lineage where applicable
4. Loadout-app season schema compatible per star-lord Track C transform
5. T4 capstones emit per chain with the existing T4 algorithm output structure

Acceptance: each kit's 10-15 chain nodes emit as skill instances with full schema; placeholder names retained for Phase 5 LLM coalescence in Wave 3.

### 3.3 Substrate weapon binding output (rocket + elrond; ~1-2 days)

Current state: `gear_representative.main_weapon` is a generic legendary T1 instance with partition affixes. Substrate-bound real weapon reference does NOT persist to character JSON.

Fix:
1. Phase 2c substrate weapon selection result persists to character JSON
2. `gear_representative.main_weapon` includes additional fields:

```python
{
  "substrate_weapon_id": "<substrate library row id>",
  "substrate_canonical_name": "<weapon name from substrate>",
  "base_physical_damage": <number>,
  "spell_damage_modifier": <pct>,
  "element_affinity_modifiers": {"fire": pct, "water": pct, ...},
  "to_skill_level_modifiers": <count>,
  "attribute_requirement": "STR" | "DEX" | "INT" | "WIS",
  "weapon_type_family": "martial-heavy" | "martial-light" | "ranged" | "caster-arcane" | "caster-faith" | "hybrid",
  # ... existing fields preserved: partition_modifiers, capability_modifiers, etc.
}
```

3. Similar for `secondary_item` for off-hand category items per `off-hand-items-2026-05-24.md`
4. Elrond audits substrate library for the new stat exposure (base_physical_damage / spell_damage_modifier / element_affinity / to_skill_level / weapon_type_family); enriches substrate data if not already present

Acceptance: each character's gear_representative reflects substrate-bound real weapon with full stat profile; loadout-app + HTML doc consume real weapon names + stats.

### 3.4 Damage scaling routing implementation (gamora; ~1-2 days)

Current state: fight engine uses `_SyntheticPlayerClass` with single synthetic primary_attack (magnitude=3000). All damage flat.

Fix:
1. `fight_engine.simulate_fight` damage_resolver routes per skill's `damage_scaling_type` per doc 47 § 4 logic
2. `calculate_physical_damage()` / `calculate_magical_damage()` / `calculate_hybrid_damage()` functions per doc 47 § 4
3. Respect stat-range bounds per doc 46 Layer 1 (caps on crit / DR / etc.)
4. Apply T4 effects per skill_id of active T4 (Category A character-wide; B/C chain-specific)

Acceptance: damage calculation routes per skill type; no flat-weapon-scaling for magical skills; per-attribute weapon profile produces expected damage shapes (wooden staff does NOT scale Ice Spike's damage; mage's spell scales from base_spell_damage + INT + element affinity per doc 47 § 2.2).

### 3.5 Synthetic_mode RETIREMENT (gamora; ~half-day)

Current state: `synthetic_mode=True` flag in `t4_sim_cycling.py:w4g1_tier_1_sweep` + `w4g2_tier_2_full_sim` + `gauntlet_sim.py:run_gauntlet_sim` overrides KPM-band gates with "encounter completable" semantic.

Fix:
1. Remove `synthetic_mode` parameter from production sim paths
2. Restore Discipline #12 semantic: `in_band` means "KPM within cohort band" (original definition, not synthetic-mode override)
3. Test fixtures may retain `synthetic_mode` for backwards-compat verification; production code paths use real-content fight execution
4. Verify with grep: `grep "synthetic_mode" src/reincarnated/simulation/` returns ZERO matches in production paths (test files OK)

Acceptance: production gauntlet sim runs against real per-skill content + real weapons + real damage routing; cohort KPM bands enforced; Defensive cohort empirically validates per real defensive kit content (not 0/16 synthetic-stub limitation)

---

## 4. Scope-of-autonomy enumeration (per hive-mind-scope-discipline)

Per `agentic_orchestration/operating-procedures/hive-mind-scope-discipline.md`.

### 4.1 Knight-rider AUTONOMOUS scope (no Matt re-engagement)

- Wave sequencing within locked structure (Wave 0 → 0.5 → 1 → 2 → 3 → 4 → 5)
- Dispatch authoring within wave per established patterns
- Gate-1 critique-pair coordination (gandalf + jack-ryan)
- Sidecar dispatching for parallel work
- Skip-confirmation fire-forward authorization (carried from Cycle 13 precedent)
- Mid-wave routing per established disciplines
- Roadmap updates per § 6 protocol
- Wind-down summary authoring + ratification request to Matt

### 4.2 Matt RE-ENGAGEMENT required

- Cycle 14 scope changes beyond this framing brief
- Tier 2/3 ratification per ADR-002
- Engineering-discipline candidates moving to canonical adoption (jack-ryan canonical write)
- Scope-expansion requests from specialist seams
- Cycle close authorization (KR drafts wind-down; Matt ratifies)
- Push to remote (per ADR-006 read-only-by-default)
- **CRITICAL**: any proposal to retain `synthetic_mode` past Wave 0.5 close — REQUIRES MATT EXPLICIT (this is the load-bearing discipline lock; see § 6)

### 4.3 Per-seam scope

- **rocket**: per-skill emission + substrate binding output + concentration architecture amendments in `gear_instance_generator.py`
- **gamora**: damage scaling routing + synthetic_mode retirement + Phase 5 cohesion-judge LLM math methodology
- **gandalf**: design-spec authoring + canonical doc amendments + cohesion-judge LLM prompt structure
- **jack-ryan**: Gate-1 critique + Gate-2 verification + discipline candidate ratification
- **elrond**: substrate weapon stat audit + substrate library enrichment if needed
- **star-lord**: Phase 5 LLM integration + cohesion-judge call architecture + Track C transform refresh post Wave 0.5
- **legolas**: Mode A research on cohesion-judge LLM call best practices + trigger condition vocabulary research
- **drax**: post Wave 0.5 + Track C: refresh loadout app season display with real content; no major UI changes
- **galadriel**: no active work in Cycle 14 (Phase 6 visual coalescence is Cycle 15)

---

## 5. Sidecar work

| Sidecar | Owner | Description | Gate |
|---|---|---|---|
| **SC-1: Discipline candidate ratification** | jack-ryan | Ratify 7 candidates (#33-#39) from doc 46 + doc 47 + this brief | Async; non-blocking |
| **SC-2: Doc 40 amendments** | gandalf | Author doc 40 amendments per doc 46 § 13 + doc 47 § 5 | Wave 0 |
| **SC-3: Legolas Mode A — cohesion-judge LLM call architecture research** | legolas | Research best practices for layered narrative LLM generation under AI-tell discipline (D7) | Wave 3 gate |
| **SC-4: Legolas Mode A — trigger condition vocabulary research** | legolas | ARPG community catalog of trigger conditions (PoE / D2-D4 / LE / GD / Lost Ark) | Wave 1 gate |
| **SC-5: Legolas Mode A — damage scaling pattern research** | legolas | ARPG community catalog of physical vs magical vs hybrid scaling formulas | Wave 0.5 gate |
| **SC-6: Elrond substrate weapon stat audit** | elrond | Audit substrate library for base_physical_damage / spell_damage_modifier / element_affinity / weapon_type_family stat exposure; enrich if needed | Wave 0.5 gate |
| **SC-7: Drax Track C transform refresh** | drax | Post Wave 0.5: refresh loadout-app season transform to consume real per-skill content + real weapon stats | Async post Wave 0.5 |

---

## 6. CRITICAL — Synthetic-sim regression risk lock

**Matt 2026-05-27 verbatim**: "will we run any risk of knight-rider and team deciding to run a synthetic or partial gauntlet vs the prepared version within cycle 14?"

**Answer**: Yes, the risk exists. Cycle 13 demonstrated the failure mode: `synthetic_mode=True` introduced as Track A stopgap became effective permanence when the gauntlet "PASS" got ratified at Cycle 13 close. The actual content gap got buried under the synthetic-mode KPM-band-bypass.

**Discipline locks in this framing brief**:

### 6.1 Synthetic_mode is RETIRED at Wave 0.5 close

`synthetic_mode=True` in production sim paths is structurally REMOVED at Wave 0.5 acceptance. Test fixtures may retain for backwards-compat verification; production paths do not.

### 6.2 Wave 5 acceptance criterion EXPLICITLY requires real-content gauntlet

Cycle 14 close Gate-2 verifies:
1. `grep "synthetic_mode" src/reincarnated/simulation/` returns ZERO matches in production code paths
2. Gauntlet sim execution uses `damage_scaling_type` routing per doc 47 § 4
3. Defensive cohort empirically validates with real defensive kits (no longer 0/16 synthetic-stub limitation)
4. KPM-band gates ENFORCED (Discipline #12 original semantic restored)

### 6.3 Discipline candidate #39 — no-synthetic-stub-as-permanent-fallback discipline

**Candidate**: stopgaps that bypass empirical-validation gates must be RETIRED at the cycle-close gate that introduced them, OR explicitly carry forward as documented WARN with a retirement-trigger empirical criterion.

**Failure mode this guards against**: Cycle 13 pattern where `synthetic_mode` was introduced as Track A stopgap, made gauntlet "PASS" via KPM-band-bypass, got ratified at PASS-with-WARN close, became effective permanence of the bypass mechanism.

**This discipline ALSO applies to future cycles** — any "stopgap" introduced during cycle execution must be explicitly tagged as stopgap with retirement-trigger; cannot be silently carried forward as production behavior.

**Queued for jack-ryan SC-1 ratification.**

### 6.4 If Wave 0.5 takes longer than estimated

If real content emission requires more wall-clock than Wave 0.5 budget (~1-2 weeks), **DO NOT regress to synthetic_mode**. Options:
1. Extend Wave 0.5 timeline (preferred)
2. Ship partial real content (e.g., physical-only first; magical second) with explicit deferred-commitment for the remainder
3. Matt re-engagement to amend cycle scope

`synthetic_mode` retention past Wave 0.5 close = Matt explicit authorization required.

### 6.5 KR autonomous-scope clarification

Per § 4.1 KR autonomous scope: wave sequencing within locked structure. **KR is NOT autonomous on `synthetic_mode` retention** — that's an architectural commitment that requires Matt explicit per § 4.2.

---

## 7. Per-wave acceptance criteria (concise)

| Wave | Acceptance criterion |
|---|---|
| **Wave 0** | Scope-doc authored + ratified; doc 40 amendments landed; doc 47 ratification complete; SC-1 through SC-7 sidecar dispatches authored; jack-ryan Gate-1 PASS |
| **Wave 0.5** | All 5 Track D items per § 3 complete; synthetic_mode RETIRED (grep verified); per-skill content emission tested; substrate weapon binding output verified; damage scaling routing tested; jack-ryan Gate-2 PASS-with-WARN or PASS |
| **Wave 1** | Concentration architecture Layers 1-4 + 7 implemented; stat-range bounds enforced at generation + runtime; affix migration complete; capability scope reduction live; trigger vocabulary expanded; synergy scan refined for capability+triggered_passive; jack-ryan Gate-2 PASS; Discipline candidates #33 + #34 ratified |
| **Wave 2** | Concentration architecture Layers 5 + 8 + 9 implemented; concentration probability gate per tier; set_generator emits sets keyed to T4-strategy × element clusters; class-agnostic drops fire; jack-ryan Gate-2 PASS; Discipline candidates #36 + #37 ratified |
| **Wave 3** | Phase 5 cohesion-judge LLM operational with layered cohesion prompt structure; identity-without-gear test PASS; T4-choice-independence test PASS; endgame-nod-additivity test PASS; spirit-guide data-oracle integration live; jack-ryan Gate-2 PASS; Discipline candidate #35 ratified |
| **Wave 4** | T4-attuned gear cohesion alignment confirmed; D21 acquisition curve calibrated; gap-filling discipline operational; spirit-guide projection language honesty enforced; jack-ryan Gate-2 PASS |
| **Wave 5** | Gauntlet sim runs against REAL content (synthetic_mode RETIRED per § 6); populated strata reflect real cohort behavior; Defensive empirically validates per real kits; cohesion validation PASS per doc 46 Layer 6; initial mechanical+cohesion season generation complete; Cycle 14 close Gate-2 PASS-with-WARN or PASS |

---

## 8. Critique-pair cadence + Gate-1 throughput planning

Cycle 14 has ~8 critique-pair cycles needed:

| Critique-pair cycle | Wave |
|---|---|
| Wave 0 scope-doc Gate-1 | Wave 0 |
| Wave 0.5 Track D Gate-1 (multi-item) | Wave 0.5 |
| Wave 1 Layers 1-4+7 Gate-1 | Wave 1 |
| Wave 2 Layers 5+8+9 Gate-1 | Wave 2 |
| Wave 3 Phase 5 cohesion-judge Gate-1 | Wave 3 |
| Wave 4 T4-attuned + acquisition curve Gate-1 | Wave 4 |
| Wave 5 gauntlet + cohesion validation Gate-1 | Wave 5 |
| Cycle 14 close Gate-2 | Wave 5 |

KR manages critique-pair scheduling autonomously per § 4.1; pre-allocates availability; parallelizes where possible.

---

## 9. Compute budget for Wave 5 sim + LLM calls

### 9.1 Wave 5 gauntlet sim with real content

Combinatorial scale: N kits × M T4 configurations × K cohort archetypes × L encounters × R real-content damage calc per fight.

Real content fights more complex than synthetic stub (multiple skills per kit; per-skill geometry; per-skill cooldown rotation; per-skill damage routing). Estimated 2-5× compute vs synthetic-mode Cycle 13 sim (which ran 27,360 fights in 12.5s).

Anticipated Wave 5 wall-clock: ~30-60s for full sim run. Multi-run validation acceptable.

### 9.2 Phase 5 cohesion-judge LLM calls

Per character × per skill × per gear instance = N × M × K LLM calls for cohesion narration. At 16 characters × ~12 chain skills × ~11 gear slots = ~2,100 LLM calls per season at Phase 5.

Per session 2026-05-25 P5 cohesion-judge calibration spec: cost per LLM call ~$0.0003-0.003 depending on model + prompt size. Estimated Phase 5 LLM cost per season: ~$0.50-$5. Tractable.

Math note required (Discipline #1) per Wave 3 implementation.

---

## 10. Composition with Cycle 13 outputs

Cycle 13 produces (already landed):
- 16 characters with chain composition counts + T4 candidates + gear with partition modifiers + capability_modifiers + triggered_passive (per `output/cycle-13-mechanical-season-001/`)
- Gauntlet sim infrastructure (488 tests pass)
- Canonical gauntlet sim results JSON (Track A remediation; synthetic-mode-bypassed)
- Loadout app gap-fill Cycle 13 Characters tab (to be retired post Track C star-lord transform)

Cycle 14 inherits all of this and extends:
- **Wave 0.5** ADDS per-skill content + substrate weapon binding output + damage scaling routing — fills the Cycle 13 content gap
- **Waves 1-2** implement concentration architecture amendments to existing gear gen pipeline
- **Wave 3** adds cohesion narrative layer on top of mechanical content
- **Wave 4** calibrates acquisition curve
- **Wave 5** re-validates with real content (synthetic_mode RETIRED)

Cycle 13 character JSONs may be REGENERATED at Wave 5 with real content (preserving character_id continuity but refreshing skill content + weapon bindings). Or a NEW season (`cycle-14-cohesion-season-001`) emits as a fresh artifact and the Cycle 13 season is preserved as historical reference.

**Recommendation (deferred to Matt): regenerate Cycle 13 season with real content** since the Cycle 13 season is the substrate for loadout app display. Drax Track C transform refreshes when real content lands.

---

## 11. Open design questions for Matt ratification

Numbered Q1-Q11. Matt ratifies each (or amends).

### Q1. Cycle 14 scope confirmation

Cycle 14 = Phase 5 cohesion coalescence + doc 46 concentration architecture 9 layers + Track D content gap closure (Wave 0.5). All three threads converge in Cycle 14.

**Confirm or amend.**

### Q2. Wave structure (§ 2 — 7 waves including Wave 0.5)

Wave 0 (scope-doc + amendments + sidecars) → Wave 0.5 (Track D content gap) → Wave 1 (Layers 1-4+7) → Wave 2 (Layers 5+8+9) → Wave 3 (Phase 5 cohesion-judge) → Wave 4 (T4-attuned + acquisition curve) → Wave 5 (gauntlet sim re-calibration + cohesion validation).

**Confirm or amend wave structure / sequencing.**

### Q3. Scope-of-autonomy boundaries (§ 4)

KR autonomous per § 4.1; Matt re-engagement per § 4.2.

**Confirm or amend autonomy boundaries.**

### Q4. Synthetic_mode RETIREMENT discipline lock (§ 6)

**Load-bearing**. `synthetic_mode` retired at Wave 0.5 close. Discipline candidate #39 queued. KR NOT autonomous on `synthetic_mode` retention past Wave 0.5.

**Confirm or amend the synthetic-mode retirement discipline.**

### Q5. Sidecar work (§ 5)

SC-1 (disciplines) / SC-2 (doc 40 amendments) / SC-3 (cohesion-judge research) / SC-4 (trigger vocab research) / SC-5 (damage scaling research) / SC-6 (substrate weapon audit) / SC-7 (Track C refresh).

**Confirm sidecar list + ownership + gating.**

### Q6. Critique-pair throughput planning (§ 8)

8 critique-pair cycles in Cycle 14. KR manages scheduling autonomously OR Matt wants per-cycle re-engagement.

**Confirm KR autonomous OR per-cycle re-engagement.**

### Q7. Compute budget for Wave 5 + Phase 5 LLM calls (§ 9)

Wave 5 real-content gauntlet sim ~2-5× compute vs synthetic-mode Cycle 13. Phase 5 LLM calls ~$0.50-$5 per season.

**Confirm compute budget tolerated; gamora methodology consultation per Discipline #18 if compute optimization needed.**

### Q8. Cycle 14 close criterion (§ 7 Wave 5)

Gauntlet sim PASS with REAL content + cohesion validation PASS + jack-ryan Gate-2 PASS = Cycle 14 close.

**Confirm close criterion.**

### Q9. Cycle 13 season regeneration vs new Cycle 14 season

Per § 10: Option A regenerate Cycle 13 season with real content (preserves character_id) OR Option B emit new cycle-14-cohesion-season-001 (preserves Cycle 13 as historical).

**Confirm A or B.**

### Q10. Wave 0.5 timeline tolerance

If Wave 0.5 takes longer than 1-2 weeks budget, per § 6.4: extend timeline (preferred) / ship partial real content with deferred-commitment / Matt re-engagement to amend scope.

**Confirm preferred path; KR escalates if exceeded.**

### Q11. Skip-confirmation fire-forward authorization

Carried from Cycle 13 precedent: KR can auto-close Cycle 14 wind-down per skip-confirmation discipline (Matt pre-authorization).

**Confirm or amend.**

---

## 12. Sign-off + ratification

**Author:** gandalf (story-and-design steward)
**Status:** **RATIFIED 2026-05-27 — Matt ratified Q1-Q11 in full**

**Ratification record per Matt 2026-05-27:**

| Q | Topic | Ratification + notes |
|---|---|---|
| **Q1** | Cycle 14 scope confirmation | ✅ RATIFIED |
| **Q2** | Wave structure (Wave 0 → 0.5 → 1 → 2 → 3 → 4 → 5) | ✅ RATIFIED |
| **Q3** | Scope-of-autonomy boundaries (§ 4) | ✅ RATIFIED |
| **Q4** | Synthetic_mode RETIREMENT discipline lock (§ 6) | ✅ **"extremely confirm.. retire it"** — discipline #39 load-bearing; emphatic lock |
| **Q5** | Sidecar work (SC-1 through SC-7) | ✅ RATIFIED |
| **Q6** | Critique-pair throughput planning | ✅ RATIFIED — KR manages scheduling autonomously |
| **Q7** | Compute budget tolerance | ✅ RATIFIED — "we need converged characters to pass the gauntlet" — converged ≠ synthetic; real-content convergence required |
| **Q8** | Cycle 14 close criterion | ✅ RATIFIED — gauntlet sim PASS with REAL content + cohesion validation + jack-ryan Gate-2 PASS |
| **Q9** | Cycle 13 season regeneration vs new Cycle 14 season | ✅ **DISREGARD Cycle 13 season** — verbatim "It is not relevant. These characters were made to fit the synthetic gauntlet. Generate and converge a new cycle 14 roster of characters." |
| **Q10** | Wave 0.5 timeline tolerance | ✅ **EXTEND TIMELINE AS NEEDED** — verbatim "extend timeline as needed for Wave 0.5 and all waves. The goal is not to ship something but to ship a game (playable characters that run the gauntlet in band)" |
| **Q11** | Skip-confirmation fire-forward authorization | ✅ RATIFIED — KR can auto-close per Cycle 13 precedent |

**Locked outcomes from Matt 2026-05-27 ratification (incl. Q4 + Q9 + Q10 clarifications):**

- **Cycle 14 quality > timeline lock** (Q10): the cycle ships when characters genuinely pass the gauntlet in-band per real-content combat. NOT timeline-gated. Wave extension is the expected path if quality isn't met.
- **Cycle 13 season disregarded** (Q9): cycle-13-mechanical-season-001 is treated as a synthetic-stub artifact, not a baseline for Cycle 14 work. Cycle 14 Wave 5 generates a FRESH Cycle 14 roster (`cycle-14-cohesion-season-001` or equivalent) using real per-skill content + real substrate weapon binding + real damage scaling routing + real cohesion-judge LLM thematic identities. Drax Track C transform integration awaits the new roster; Track C dispatch from prior conversation becomes obsolete (pending fresh dispatch when Cycle 14 roster materializes).
- **Synthetic_mode retired ABSOLUTELY** (Q4): discipline #39 load-bearing; emphatic; not even partial retention.
- **"In band" means real cohort-band KPM** (Q7 + Q10 composition): not synthetic_mode override. Defensive cohort must validate empirically per real defensive kits at real cohort-band KPM ranges.
**Ratification effect**: once ratified, brief becomes canonical authority basis for Cycle 14 scope-doc authoring + KR kicker. KR has full autonomous scope per § 4.1 to orchestrate Cycle 14 through 7 waves. Matt re-engagement limited to items per § 4.2.

**Locked outcomes after ratification (anticipated)**:
- Q1-Q11 all ratified (or amended) by Matt
- KR fires Wave 0 dispatch
- Cycle 13 close framed honestly as PASS-with-WARN with content gap absorbed by Cycle 14 Wave 0.5
- Synthetic-mode retirement discipline #39 queued for SC-1 ratification
- 7-week wall-clock estimate (4-6 + buffer; could vary per Wave 0.5 actual duration)

**Composition**: with doc 46 + doc 47 + doc 41 + doc 40 + skill-system + weapon-substrate composition policy + Cycle 13 framing brief precedent

**Downstream**: Cycle 14 scope-doc authoring (gandalf or KR per Q9 of original Cycle 13 framing brief framing) → KR Wave 0 dispatch → Cycle 14 fires per ratified wave structure

---

**Signed:** gandalf (story-and-design steward)
**For:** Cycle 14 framing brief covering Phase 5 cohesion coalescence (Q9 Pattern A original scope) + doc 46 concentration architecture 9-layer amendments + Track D content gap closure (Wave 0.5 — Cycle 13 scope that wasn't fully delivered). Once ratified, becomes canonical authority basis for Cycle 14 scope-doc + KR kicker. Cycle 14 close = the SUBSTANTIVE delivery point that Cycle 13 close was originally framed as.
