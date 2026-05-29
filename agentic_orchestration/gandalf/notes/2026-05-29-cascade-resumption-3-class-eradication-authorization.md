# Cascade-Resumption-3 — Class-Eradication + Full Cascade-Architecture Completion Authorization

> **STATUS:** CURRENT (operational dispatch authorization as of 2026-05-29; AMENDED with S7 addition 2026-05-29 evening) — Matt 2026-05-29 invoked CLAUDE.md Engine > Game > Phase orientation directive. Substantial scope amendment to Cycle 14 v1 close trajectory: ~7-12d engine + LLM + Gate-2 work before A2-1 RE-FIRE-3 (was ~6-10d pre-S7-amendment). Engine-architectural-integrity takes precedence over Phase-operational-timing per CLAUDE.md.
>
> **Amendment 1 (S7 addition):** S0 empirical verification (gandalf in-thread) surfaced that substrate weapon library IS wired at Phase 2 BC discovery (per `substrate_weapon_binding.py:716` call from `season_generation_pipeline.py`) but: (1) only 1 substrate weapon per BC cell (1:1 binding; 18 cells → 18 substrate weapons); (2) `cultural_lineage_canonical` + `historical_period_canonical` + `register_canonical` fields exist on `weapon_knowledge_entries` schema BUT are NOT in the SELECT query at `substrate_weapon_binding.py:316`. S7 (NEW) wires the missing lineage/period/register fields AND adds multi-sample substrate selection (N samples per BC cell). Substrate schema exists; this is a "wire it up + multi-sample" refactor, not schema extension. ~1-2d engineering. Inserted BEFORE S2 so gauntlet mechanical cycling operates on substrate-diverse base (not substrate-monoculture).
>
> **Amendment 2 (parallel sub-agent fan-out enabled):** Matt 2026-05-29 evening direction: "please allow multiple agents to be fired in parallel as sub agents. We have been doing this for months without issue. I think the RAM issue was around my opening of other apps like installers." **R48.4 single-seam constraint RELAXED for cascade-resumption-3** where dependency graph permits parallel work. Pre-flight `vm_stat` check still load-bearing per Disc #48 R48.1/R48.2/R48.3/R48.5 (oversized-file + grep-bounds + find-exec + RAM pre-flight); R48.4 specifically (single-seam constraint) is relaxed for this cascade-resumption-3 work program based on Matt's empirical history claim (months of parallel sub-agent fan-out without freeze). **Discipline #48 R48.4 itself flagged as Pattern B revisit candidate** for Matt re-engage (the Mac mini freeze 2026-05-28 attribution may need empirical re-validation — was the cause sub-agent fan-out, OR Matt's parallel installer workload, OR confluence?). Not blocking; cascade-resumption-3 proceeds with parallel fan-out where graph allows. **SUPERSEDED by Amendment 3** (full retirement of R48.4 + R48.5; see below).
>
> **Amendment 3 (Discipline #48 RAM-awareness RETIRED):** Matt 2026-05-29 evening verbatim: "Let's retire the RAM awareness." **R48.4 + R48.5 retired entirely** per gandalf recommendation at `agentic_orchestration/gandalf/notes/2026-05-29-discipline-48-ram-awareness-retirement.md`. Founding-incident attribution (Mac mini freeze 2026-05-28) empirically refuted: months of parallel sub-agent fan-out without incident; likely confounded with Matt's parallel UE installer workload (RAM-intensive; crashed twice at 75% FC02 FileConstructionFail on this host). **Pre-flight vm_stat checks REMOVED from required-action sequences** for cascade-resumption-3 and forward workstreams. R48.1/R48.2/R48.3 (oversized-file operational safety) reclassified under new Discipline #49 per jack-ryan canonical-write target (separable; non-blocking). **Discipline #42a Instance 7 case-type captured** — founding-incident-confounding-attribution; pushback memo amendment at next batch.
>
> **Updated trajectory: ~5-8d wall-clock to A2-1 RE-FIRE-3** (was ~7-12d sequential pre-Amendment-2; Amendment 3 removes pre-flight handoff overhead but doesn't change wall-clock estimate materially; minor reduction ~0.5d possible).

**Date:** 2026-05-29
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-29 in-session direction:
- "Per claude.md, there is only one choice here: erase class concept at all levels, then construct the Wave 2 [Wave B] LLM naming, then fire the full engine gen again with Wave 2 [Wave B] LLM entity naming"
- "Confirm scope, commit the authorization" (in response to gandalf scope: strip class taxonomy from `endgame_encounter_catalog.py` + downstream surfaces; preserve cohort_archetype as load-bearing for BVV; Cycle 15+ flag for community vocabulary research convergence)

**Companion docs (required KR first reads at consumption):**
1. `agentic_orchestration/gandalf/notes/2026-05-29-concern-1-and-2-resolution-plan.md` — original Phase A2 resolution plan + § 1.5 D13 parallel-fire
2. `agentic_orchestration/gandalf/notes/2026-05-29-concern-3-resolution-authorization-and-pre-ratification.md` — Concern #3 P3c routing (LANDED in cascade-resumption-2)
3. THIS authorization — cascade-resumption-3 work program
4. `agentic_orchestration/gandalf/notes/2026-05-29-no-classes-architectural-recommitment.md` (via `2026-05-27-no-classes-architectural-recommitment.md`) — Path (ii) verbatim recommitment Matt 2026-05-27
5. `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` — recognition record + § 0.1 amendment-pass-record (will receive root-cause amendment in same commit batch)
6. `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` — Instance 6 pushback memo (will receive root-cause amendment in same commit batch)
7. `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 — Primary T4 DDA universal slot architecture (PRESERVED; T4 Capstone Skill design intact)
8. `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — Path α RATIFIED architecture; cohort_archetype is LOAD-BEARING for BVV (preserved per Matt scope confirmation)
9. `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` — § 4 Wave A + § 5 Wave B + § 6 F-C prompt templates (gandalf S4 audit target)

---

## 0. TL;DR

**Matt election (per CLAUDE.md Engine > Game > Phase orientation):** Cycle 14 v1 close DOES NOT ship against pre-imposed-class-taxonomy substrate. Engine refactor is mandatory; Phase-timing cedes to architectural integrity.

**Work program (7 streams — AMENDED with S7 NEW + PARALLEL FAN-OUT enabled per Amendment 2):**

| Stream | Owner | Effort | Dependency | Parallel-eligible? |
|---|---|---|---|---|
| **S1 — Class-concept eradication at substrate-input layer** ✅ CLOSED 2026-05-29 evening | rocket primary | ~1-2d (landed in ~6-8min wall-clock per engine `99d67aa` + tag `rocket/v1.0-cascade-r3-s1-class-eradication-1`) | first; root-cause fix | n/a (closed) |
| **S4 — Phase 5 LLM prompt audit for class-free substrate** ✅ CLOSED 2026-05-29 (commit `13822ba`) | gandalf (in conversation thread) | ~1-2h | parallel-safe (already done ahead of cascade) | n/a (closed) |
| **S7 (NEW) — Phase 2 multi-sample substrate consumption + lineage/period propagation** | rocket + elrond consultation | ~1-2d | S1 ✅ | **YES — parallel with S5 prep** |
| **S5 — Wave B FULL implementation per canonical § 5** (star-lord side; rocket integration deferred to S5b) | star-lord (primary) | ~4-6h | S4 ✅ (canonical § 5 spec consumption) | **YES — fires in parallel with S7** |
| **S2 — Gauntlet variant enumeration expansion** | rocket + gamora | ~1-2d | S7 (substrate-diverse base required) | **PARTIAL — gamora T4 strategy applicability research can fire parallel with S7** |
| **S3 — Phase 4 archive variant preservation** | rocket | ~0.5-1d | S2 | sequential |
| **S5b — Wave B rocket integration** (Wave B invocation in orchestrator + kit_archive.cohesion_data wiring) | rocket | ~2-4h | S3 + S5 | sequential |
| **S6 — Integration + jack-ryan Gate-2 + A2-1 RE-FIRE-3** | rocket + gamora + star-lord + jack-ryan | ~1-1.5d | S1-S7-S2-S3-S5-S5b | sequential |

**Parallel-enabled trajectory:**

```
S1 ✅ CLOSED + S4 ✅ CLOSED (already done; gate cleared for parallel fan-out below)
  ↓
  ┌──────────────────────────────┐
  ↓                              ↓
S7 (rocket; ~1-2d)            S5 (star-lord Wave B impl; ~4-6h)
  ↓                              │
  ↓ + gamora T4 strategy research in parallel
  ↓                              │
S2 (rocket+gamora; ~1-2d) ←─────┘ (S5 may complete before S2; S5b integration awaits S3)
  ↓
S3 (rocket; ~0.5-1d)
  ↓
S5b (rocket integration; ~2-4h)
  ↓
S6 (integration + Gate-2 + A2-1 RE-FIRE-3; ~1-1.5d)
```

**Realistic total to A2-1 RE-FIRE-3 PASS: ~5-8 days** (was ~7-12d sequential pre-Amendment-2; parallel fan-out enabled cuts ~2-4d). Cascade through A2-2 → A2-7 + D13 parallel-fire per existing Phase A2 sequence after.

**Parallel sub-agent fan-out protocol (per Amendment 2; UPDATED per Amendment 3 retirement):**

- ~~**Pre-flight per dispatch:** vm_stat shows free + reclaimable > 1 GB combined; if free drops below 200 MB and reclaimable < 1 GB combined, halt + serialize next dispatch~~ **RETIRED per Amendment 3** (R48.5 retirement). macOS inactive-page reclamation handles RAM pressure naturally; no per-dispatch pre-flight required.
- ~~**Concurrent sub-agent count limit:** 2-3 concurrent sub-agents at ~600 MB RSS empirical~~ **RETIRED per Amendment 3** (R48.4 retirement). KR coordinates fan-out per dependency graph without count constraint.
- ~~**R48.4 violations that still hold:** if specialist dispatch is a substrate-crawl OR analytical sweep~~ **RETIRED per Amendment 3.** Sweep-resident workstreams self-throttle internally (existing background-process discipline); no external sweep-residency-vs-other-dispatch constraint.
- **R48.1/R48.2/R48.3 PRESERVED (reclassification candidate under new Discipline #49):** oversized-file find pre-flight + grep-bounds + find-exec safety remain load-bearing per gandalf retirement recommendation Option B; jack-ryan canonical-write target for engineering-disciplines.md § 49 NEW (separable from cascade-resumption-3; non-blocking).
- **Dependency graph determines parallelism eligibility:** S7 + S5 parallel (different seams, no shared dependencies); S2 sequential after S7 (substrate-diverse base required); S6 sequential after all (integration step). KR coordinates per graph; no RAM-pre-flight gate.

## S7 (NEW) — Phase 2 multi-sample substrate consumption + lineage/period propagation

**Empirical basis (S0 verification 2026-05-29 evening):** substrate IS wired at Phase 2 but partially. `gear_representative.main_weapon.substrate_binding` carries 8 fields (substrate_weapon_id, substrate_canonical_name, base_physical_damage, spell_damage_modifier, element_affinity_modifiers, to_skill_level_modifiers, attribute_requirement, weapon_type_family). All 18 kits empirically have populated bindings (Lance head / Sword / Mjölnir / Whip / Wurrog Staff / Khakkhara / etc.) — substrate IS consulted. BUT:

1. **1:1 binding pattern** — `substrate_weapon_binding.select_and_bind_substrate_weapon()` selects ONE substrate weapon per call via `rng.choice(row_dicts)`. Phase 2 calls it once per kit; 18 kits → 18 substrate weapons.
2. **cultural_lineage / historical_period / register NOT in SELECT query** — `weapon_knowledge_entries` schema HAS `cultural_lineage_canonical` (14-enum) + `historical_period_canonical` (9-enum) + `register_canonical` (6-enum) + `cultural_lineage_confidence` REAL + `named_mythological_match` TEXT, but the SELECT at `substrate_weapon_binding.py:316` doesn't pull them. Substrate_binding dict therefore lacks lineage/period/register fields → downstream Wave A LLM `modal_cultural_lineage` defaults to placeholder.
3. **weapon_type_family collapses to 4 attribute-keyed buckets** (martial-heavy / ranged / caster-arcane / caster-faith) — empirical spread across 18 kits.

**S7 work scope:**

| Sub-work | Owner | Effort |
|---|---|---|
| Extend SQL query at `substrate_weapon_binding.py:316` to also SELECT `cultural_lineage_canonical`, `historical_period_canonical`, `register_canonical`, `cultural_lineage_confidence`, `named_mythological_match` | rocket | ~30min |
| Extend `_build_weapon_binding()` to include new fields in substrate_binding dict (11+ fields) | rocket | ~30min |
| Refactor `select_and_bind_substrate_weapon()` to support multi-sample selection (`select_n_substrate_weapons_per_bc_cell(n=3-5)`) | rocket | ~2-4h |
| Refactor `season_generation_pipeline.py:w5r1_generate_kit_candidates()` to generate N kits per BC cell from N substrate samples (was: 1 kit per BC cell) | rocket | ~1-2h |
| Propagate lineage/period/register to kit top-level for downstream Phase 3 PM-1 + Phase 5 Wave A consumption | rocket | ~1h |
| Update Phase 3 PM-1 multimodal clustering input to consume new lineage/period/register fields as multimodal vector axes (composes with existing BC tuple + element axes) | gamora consultation; rocket implements | ~1-2h |
| Phase 5 Wave A `modal_cultural_lineage` aggregation now sources from kit lineage (not placeholder) | rocket | ~30min |
| Smoke test + Disc #11 audit | rocket+gamora | ~1h |
| jack-ryan Gate-2 (Pattern E pre-auth) | jack-ryan | ~half-day |

**Acceptance criteria (S7 close):**

- substrate_binding dict carries 11+ fields including cultural_lineage_canonical + historical_period_canonical + register_canonical + cultural_lineage_confidence + named_mythological_match (NEW; in addition to existing 8 mechanical fields)
- Phase 2 generates N kits per BC cell (N=3-5 per Matt election; default N=3) → 18 cells × 3 samples = 54+ kits (was: 18)
- Per-season cultural_lineage_canonical distribution shows ≥5 distinct values across all kits (empirical spread target)
- Per-season weapon_type_family distribution shows ≥5 distinct values (NOT collapse to 4 attribute-keyed buckets if lineage-diversity is real)
- Phase 5 Wave A `modal_cultural_lineage` field sources from kit aggregates (not placeholder default)
- jack-ryan Gate-2 PASS-with-WARN/INFO (Pattern E)

**Pre-ratified contingent decisions for S7 (KR routes per § 3 of this authorization):**
- N=3 default substrate samples per BC cell (KR can elect N=5 if substrate density supports per elrond consultation; surface to Matt only if N=10+ or substrate density issues surface)
- Substrate library SELECT query extension scope: 5 new fields per S7 sub-work table; surface if schema gaps surface beyond these 5
- Multi-sample selection method: seeded rng without replacement (simple); surface if methodology has multiple options requiring legolas Mode A consultation
- Lineage/period field placement on kit top-level (NOT just substrate_binding): rocket implements per simpler-flow principle; surface if schema impact ripples beyond Phase 2

**S7 surface-to-Matt edge cases (additions to § 4):**
- Substrate library schema gap surfaces (cultural_lineage missing OR sparse across attribute buckets) → halt + surface (substrate library quality issue beyond cascade-resumption-3 scope)
- Multi-sample selection produces NO additional cluster spread post-PM-1 (variant count up; cluster count still ~3-4 fallback) → surface (deeper algorithmic issue with PM-1 multimodal clustering methodology; Pattern B design call territory)
- S7 effort exceeds ~3d (substantial implementation complexity surfaced) → surface (scope-amendment reconsideration; might affect cascade-resumption-3 trajectory)

**Strip:** class taxonomy from `endgame_encounter_catalog.py` (archetype_name field; encounter_id class-name suffix; intent "the class" references; cohort_notes class-bound assignments) + audit other engine files for surviving class taxonomy.

**Preserve:** cohort_archetype (DPS-min-maxer / Balanced / Defensive / Hybrid) as LOAD-BEARING for bounded-viability-with-specialization framework (doc 50 Path α RATIFIED 2026-05-28). T4 Capstone Skill architecture (doc 47 § 4.6) also PRESERVED.

**Cycle 15+ flag:** cohort_archetype IS pre-authored taxonomy per strict Discipline #41 reading; may converge with experiential archetype dimension (Magic Find / Boss Speed Run / Swarm Clear / End Game Generalist / Build Crafter) per gate (ii) legolas Mode A community vocabulary research. Cycle 15+ revisit candidate.

---

## 1. What Matt elected — CLAUDE.md orientation invocation

Matt 2026-05-29 verbatim:

> "Per claude.md, there is only one choice here:
> - erase class concept at all levels, then
> - construct the Wave 2 [Wave B] LLM naming, then
> - fire the full engine gen again with Wave 2 [Wave B] LLM entity naming"

**CLAUDE.md orientation directive (load-bearing):**

> Engine first. Game second. Phase third.
> Engine = architectural integrity (substrate-led discipline; canonical docs).
> Game = player-facing quality. Phase = operational unit (waves, dispatches).
> Conflict resolution: engine > game > phase.

**Architectural truth surfaced 2026-05-29:** ENDGAME_ENCOUNTER_CATALOG (`reincarnated-engine/src/reincarnated/generation/endgame_encounter_catalog.py`) is Cycle 13 SC-6 hand-crafted artifact embedding class taxonomy at substrate-input layer. The no-classes architectural recommitment (Matt 2026-05-27 verbatim) landed at player-architecture but NOT at substrate-input layer. Cascade architecture's substrate-led emergence promise empirically refuted at root.

**Engineering-priority resolution:** Engine architectural integrity > Phase A2 cascade timing. Class eradication + cascade-architecture completion before A2-1 RE-FIRE-3.

---

## 2. Work streams — detailed sequencing

### Stream S1 — Class-concept eradication at substrate-input layer

**Owner:** rocket (primary engine refactor)
**Effort:** ~1-2d
**Dispatch:** KR-authored under hive-mind decision-routing

**Work:**
- **Refactor `endgame_encounter_catalog.py`:**
  - Strip `archetype_name` field — replace with substrate-derived neutral identifier (e.g., BC-tuple-derived: `bc_str_melee_low_spiky_str_none` or similar; NOT class names)
  - Refactor `encounter_id` naming — remove class-name suffix; use BC-tuple-derived ID (e.g., `endgame_bc_melee_low_spiky_str_none` rather than `endgame_str_01_heavy_barbarian`)
  - Rewrite `intent` descriptions — remove "the class" framing; describe encounter in terms of BC-tuple capabilities + mob composition + scenario shell
  - Refactor `cohort_notes` — preserve cohort viability assessment but remove class-name references
- **Audit other engine files for surviving class taxonomy:**
  - Phase 2 BC discovery code (`reincarnated-engine/src/reincarnated/generation/`)
  - Phase 3 gauntlet sim consumers
  - Phase 4 archive insertion (kit_id derivation)
  - Any `*archetype*` files for class-as-identity vocabulary surfaces
  - Any test files referencing class names
- **Kit_id derivation pipeline** — change from class-keyed to substrate-keyed (BC tuple + cultural tradition + element + emergence properties)

**Preserve:**
- cohort_archetype constants (`COHORT_DPS_MIN_MAXER`, `COHORT_BALANCED`, `COHORT_DEFENSIVE`, `COHORT_HYBRID`) — load-bearing for BVV framework
- BC tuple fields (range, tempo, amplitude, attribute, proxy_density) — substrate-led 5-tuple
- T4 Capstone Skill architecture per doc 47 § 4.6 — unchanged
- Scenario shell IDs (boss_with_adds, open_arena, etc.) — encounter-structure-keyed, not class-keyed

**Acceptance criterion:** zero class-name strings ("barbarian", "wizard", "cleric", "monk", "knight", "fighter", "assassin", "archer", "sniper", "fencer", "spellsword", "mage", "caller") remaining in `endgame_encounter_catalog.py` after refactor (`grep -rE 'barbarian\|wizard\|cleric\|monk\|knight\|fighter\|assassin\|archer\|sniper\|fencer\|spellsword\|mage\|caller'` should return 0 matches in the file).

**Discipline composition:**
- Disc #41 substrate-led vocabulary lock (LOAD-BEARING; this work IS the application)
- Disc #45 vocabulary lock — no class/role/archetype non-exempt vocabulary
- Disc #42a framing-audit Q1-Q6 at every refactor step

### Stream S2 — Gauntlet variant enumeration expansion

**Owner:** rocket + gamora
**Effort:** ~1-2d
**Dependency:** S1 (needs class-free kit identifiers)
**Dispatch:** KR-authored under hive-mind decision-routing

**Work:**
- Extend Phase 3 gauntlet to cycle through MORE variant dimensions beyond chain-placement:
  - **T4 strategy variants** — cycle through 6 Layer 2 strategies per doc 47 § 4.6 (Element Conversion A/B/C + Trade-off Reversed + Geometry Collapse + Resource Conversion)
  - **Investment scaling profiles** — cycle through low / mid / max-investment profiles per doc 51 Patterns 1+2 (gauntlet runs each kit at multiple investment profiles)
  - **Optional: skill tree variants** — within-chain skill composition cycling (if architecturally tractable)
- **Goal:** produce 22-40+ variant kits from 18 BC base × variant cycling (matching A/B comparison protocol § 2 spec line 72)
- **Output:** gauntlet emits ≥22 unique kit-variant rows (not just 18 base or 22 limited T4-chain-placement)

**Acceptance criterion:** gauntlet output `kit_results` has ≥22 unique (BC × T4_strategy × investment_profile × ...) tuples; PM-1 input variant population matches A/B protocol spec.

**Discipline composition:**
- Disc #18 math hotspot consultation if variant-cycling methodology has multiple options (gandalf design-spec-as-math handoff for variant cycling axes)
- Disc #11 empirical inspection — verify gauntlet emit count matches expected variant cardinality
- Disc #42a framing-audit at dispatch consumption

### Stream S3 — Phase 4 archive variant preservation

**Owner:** rocket
**Effort:** ~0.5-1d
**Dependency:** S2 (needs variants to preserve)
**Dispatch:** KR-authored

**Work:**
- Change `kit_archive` insertion logic at `wave5_season_orchestrator.py` Phase 4 hook
- Preserve (kit_base × T4_variant × ...) tuples as DISTINCT ROWS in kit_archive (not deduped by base character_id)
- PM-1 clustering at Phase 3 → Phase 4 → PM-1 input consumes variant population
- Update PM-1 clustering input filter to consume all archive ACTIVE rows (no class-keyed filter)

**Acceptance criterion:** kit_archive count ≥ gauntlet variant count (22-40+); PM-1 input cardinality matches archive variant cardinality.

**Discipline composition:**
- Disc #11 empirical inspection — verify archive variant cardinality
- Disc #1 math-before-code (variant-preservation insertion math)

### Stream S4 — Phase 5 LLM prompt audit for class-free substrate

**Owner:** gandalf (in current conversation thread; no sub-agent dispatch)
**Effort:** ~1-2h
**Dependency:** parallel-safe with S1-S3
**Authority:** Matt 2026-05-29 confirmation ("I'll audit all three Phase 5 prompts (§ 4 Wave A / § 5 Wave B / § 6 F-C) for class-name surfaces in S4; refactor whatever needs it. Confirm." — confirmed)

**Work:**
- Audit `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md`:
  - § 4 Wave A SYSTEM/USER prompts for class-name field consumption
  - § 5 Wave B SYSTEM/USER prompts for class-name field consumption
  - § 6 F-C SYSTEM/USER prompts for class-name field consumption
- Identify any class-name field references (archetype_name, class_name, character archetype labels)
- Refactor identified prompts to consume class-free substrate fields (BC tuple, cultural lineage, element, faction emergence, etc.)
- Authored amendment-pass-record at canonical Phase 5 prompts doc § 0.1 (if not present, add)

**Acceptance criterion:** all three Phase 5 LLM prompts consume class-free substrate fields; no `archetype_name` or class-keyed field references.

**Discipline composition:**
- Disc #41 substrate-led vocabulary lock
- Disc #45 vocabulary lock
- Disc #11 empirical inspection of canonical prompt content

### Stream S5 — Wave B FULL implementation per canonical § 5

**Owner:** star-lord (primary) + rocket (integration)
**Effort:** ~1-1.5d
**Dependency:** S3 (needs variant-preserved archive for input) + S4 (needs class-free prompts)
**Dispatch:** KR-authored

**Work:**
- **star-lord:**
  - Implement `run_wave_b_async()` per canonical § 5 spec (mirrors Wave A pattern)
  - Implement `Phase5WaveBResult` dataclass with `kit_name_canonical` + `kit_identity_narrative` + `ai_tell_compliance_score` + `cohesion_judge_confidence` fields
  - Per-kit prompt execution infrastructure with functional cost-tracker (already wired post Concern #3 resolution)
- **rocket:**
  - Integrate Wave B invocation in `wave5_season_orchestrator.py` Phase 5 hook (sequence: Wave A → F-C → Wave B per orchestrator docstring line 12)
  - Persist per-kit Wave B outputs to `kit_archive.cohesion_data` (unhardcode `cohesion_data={}` at `wave5_season_orchestrator.py:1169`)
  - Wire `cohesion_data` flow to Phase 7 cohesion-judge gate consumption
  - Validate Phase 7 `cohesion_judge_confidence >= 0.75` gate becomes binding (not pass-through)

**Acceptance criterion:** Wave B fires for all kits in cascade; per-kit identity LLM outputs populated; Phase 7 cohesion-judge gate is BINDING with real cohesion_judge_confidence scores from Wave B.

**Discipline composition:**
- Disc #11 empirical inspection — verify Wave B fires + outputs persist + Phase 7 consumes
- Disc #18 math hotspot consultation if Wave B cohesion-confidence scoring math has methodology choice
- Disc #42a framing-audit Q1-Q6 at dispatch consumption (no phantom-component propagation)

### Stream S6 — Integration + jack-ryan Gate-2 + A2-1 RE-FIRE-3

**Owner:** rocket + gamora + star-lord + jack-ryan
**Effort:** ~1-1.5d
**Dependency:** S1-S5 all closed
**Dispatch:** KR-authored

**Work:**
- **Smoke test** — fire full Phase 2-7 pipeline on small sample (3-5 kits) to verify integration
- **Disc #11 audit** — verify all streams operational: class-free substrate + 22+ variants + Phase 4 preservation + Wave B firing + Phase 7 binding
- **jack-ryan Gate-2** — Pattern E pre-auth; PASS/WARN/INFO fire-and-continue; BLOCK halts
- **A2-1 RE-FIRE-3** — full season_001 production fire with all fixes operational

**Acceptance criterion:** A2-1 RE-FIRE-3 produces ≥12/18 shipped_worthy at Phase 7 + Wave A + F-C + Wave B all fire with functional cost guard + PM-1 produces real emergent clusters (not k=3 fallback degenerate) + per-kit identities populated.

**Discipline composition:**
- Disc #43 design-quality wave-close audit (A1-A5) by jack-ryan
- Disc #42a framing-audit Q1-Q6 at Gate-2 review
- Pattern E autonomous-pair ratification per Phase A1 closure record § 7

### Stream S7 (post-A2-1-RE-FIRE-3) — cascade through A2-7

Per existing Phase A2 sequence in Phase A1 closure record § 7 and resolution plan § 1.5 D13 parallel-fire authorization. Unchanged from prior authorization.

---

## 3. Pre-ratified contingent decisions (KR routes without Matt re-surface)

| Decision point | KR action |
|---|---|
| S1 class-name token list to strip — KR identifies via grep; gandalf has named primary candidates (barbarian, wizard, cleric, monk, knight, fighter, assassin, archer, sniper, fencer, spellsword, mage, caller) | KR + rocket extend list per grep audit; auto-strip per Disc #45 vocabulary lock |
| S1 substrate-derived encounter_id naming scheme | KR + rocket implement BC-tuple-derived naming (e.g., `endgame_bc_melee_low_spiky_str_none`) per gandalf scheme; surface if architectural alternatives surface |
| S2 variant cycling axes priority — T4 strategy first; investment profile second; skill tree variant if architecturally tractable | KR routes per ordering; surface if architecturally complications surface |
| S3 archive insertion math change — variant-preserving (BC × T4 × invest) tuples as distinct rows | KR routes per Disc #1 math-before-code; rocket implements |
| S4 gandalf Phase 5 prompt audit findings — gandalf authors refactor in conversation thread | gandalf authors + commits in same batch as this authorization |
| S5 Wave B implementation per § 5 spec (no scope expansion) | star-lord implements canonical spec verbatim; gandalf reviews via Gate-2 |
| S6 jack-ryan Gate-2 Pattern E disposition (PASS-with-WARN/INFO fire-and-continue) | KR routes per Pattern E pre-auth; BLOCK halts + surfaces |

---

## 4. Surface-to-Matt conditions (additions to existing $50 / R48.4 / Gate-2 BLOCK)

| Condition | Trigger | KR action |
|---|---|---|
| **S1 audit surfaces class taxonomy in unexpected engine surfaces** (e.g., decisions-log entries; canonical doc references; engine canonical library; LLM prompts already canonical) | KR + rocket surface findings | Halt + surface to Matt — scope-amendment decision required |
| **S2 variant cycling requires methodology choice** | gandalf design-spec-as-math handoff insufficient; multiple methodology options surface | Halt; legolas Mode A methodology consultation per Disc #18 OR gandalf Pattern B design dialogue |
| **S3 PM-1 still produces degenerate fallback at 22+ variants** | Empirical PM-1 input cardinality ≥22; primary algorithm still falls back to kmeans_k3 | Surface to Matt — gandalf Pattern B design call on PM-1 methodology refinement (separable from substrate refactor) |
| **S5 Wave B implementation surfaces canonical § 5 spec gaps** | star-lord encounters spec ambiguity OR canonical prompt requires refinement | Halt; gandalf S4 amendment to canonical prompt OR surface to Matt if architectural |
| **A2-1 RE-FIRE-3 returns another material fail** | RE-FIRE-3 has ≥1 material-fail finding distinct from already-resolved concerns | Halt cascade; surface to Matt queue (no re-fire loop) |
| **All other resolution plan § 3 + Concern #3 authorization § 4 conditions** | Per existing surface conditions | Unchanged |

---

## 5. What KR will NOT do without Matt evidence

- Touch cohort_archetype taxonomy (DPS-min-maxer / Balanced / Defensive / Hybrid) — load-bearing for BVV; PRESERVED per Matt scope confirmation
- Touch T4 Capstone Skill architecture (doc 47 § 4.6) — PRESERVED; Path α RATIFIED 2026-05-28
- Touch bounded-viability-with-specialization framework (doc 50) — PRESERVED; Path α RATIFIED
- Touch the A/B comparison protocol itself — independent of substrate refactor; runs at Wave 5 close
- Recalibrate Phase 7 `cohesion_judge_confidence >= 0.75` threshold — scaffold-flag; Pattern B design call for Matt re-engage if systematic under-0.75 in A2-1 RE-FIRE-3 telemetry
- Player-facing faction-architecture commitments — deferred-commitments recognition record stands
- Decisions-log canonical writes beyond completion records — jack-ryan owns; deferred to Matt re-engage
- Scope-amendment expansion to investment scaling Patterns 3-6 work — Cycle 15+ candidate
- Antagonist/contrast-faction generation — Cycle 15+ per recognition record gate (iii)

---

## 6. Composition with existing canon

| Existing artifact | Composition with this authorization |
|---|---|
| `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` | S1 IS the operational application of this recommitment at substrate-input layer — completes the recommitment that landed at player-architecture only |
| `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 | T4 Capstone architecture PRESERVED; not touched by class eradication |
| `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` | BVV framework PRESERVED; cohort_archetype preserved as load-bearing |
| `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` Patterns 1+2 | Investment scaling preserved; Patterns 1+2 may be exercised by S2 variant cycling |
| `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` | Phase 2-7 architecture preserved; substrate-input layer (catalog) refactored within Phase 2 |
| `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` | S4 audits + refactors as needed for class-free substrate consumption |
| `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` | § 0.1 amendment-pass-record receives "catalog class-taxonomy root-cause finding" entry in same commit batch |
| `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` | Instance 6 receives root-cause sub-case (catalog level) in same commit batch |
| `agentic_orchestration/gandalf/notes/2026-05-29-concern-1-and-2-resolution-plan.md` + `2026-05-29-concern-3-resolution-authorization-and-pre-ratification.md` | Prior resolution plans + Concern #3 authorization COMPOSE with this; carry-forward gates ($50 + Pattern E + R48.4 + push pattern + D13) PRESERVED |
| `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` | Disc #11 + #18 + #41 + #42a + #43 + #45 + #48 all carry forward per resolution plan + this authorization |

---

## 7. Discipline composition

| Discipline | Application in this authorization |
|---|---|
| **Disc #41 substrate-led vocabulary lock** | S1 IS the operational application — completes Cycle 14 no-classes recommitment at substrate-input layer |
| **Disc #42a framing-audit (Q1-Q6)** | Applied at every dispatch consumption gate; Instance 6 case-type empirically validated at S1 dispatch consumption |
| **Disc #42a Instance-6 (component-existence + canonical-vs-implementation match)** | Cumulative Instance 6 record: Wave B phantom + Wave B canonical-vs-implementation gap + kit-count canonical-vs-empirical gap + gauntlet variant enumeration shallow + Phase 4 archive collapse + **CATALOG class-taxonomy ROOT-CAUSE (this finding)** |
| **Disc #45 vocabulary lock** | S1 + S4 enforce; no class/role/archetype non-exempt vocabulary surviving |
| **Disc #11 empirical inspection** | S1 grep verification; S2/S3 variant cardinality verification; S5 Wave B fires verification; S6 cascade output verification |
| **Disc #18 math hotspot consultation** | S2 variant cycling methodology if multiple options surface |
| **Disc #40 scaffold-flagging** | Catalog itself is Cycle 13 SC-6 scaffold that survived to production via cycle-boundary; data point captured; cohort_archetype flagged as Cycle 15+ scaffold candidate |
| **Disc #43 design-quality wave-close audit** | S6 jack-ryan Gate-2 applies A1-A5 |
| **Disc #48 R48.4 single-seam** | Strict sequential throughout S1 → S6 |
| **Pattern E autonomous-pair pre-authorization** | Carries forward for S6 jack-ryan Gate-2 |
| **Recognition → empirical validation → commit** | Recognition: catalog class-taxonomy finding 2026-05-29; validation: S1 grep zero-match + S6 cascade output emergence; commit: A2-1 RE-FIRE-3 PASS |
| **CLAUDE.md Engine > Game > Phase** | Engine architectural integrity > Phase A2 cascade-timing per Matt 2026-05-29 invocation |

---

## 8. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-29 CLAUDE.md orientation invocation + scope confirmation

**Authority chain:**
- Matt 2026-05-29 verbatim: "Per claude.md, there is only one choice here: erase class concept at all levels, then construct the Wave 2 [Wave B] LLM naming, then fire the full engine gen again with Wave 2 [Wave B] LLM entity naming"
- Matt 2026-05-29 verbatim: "Confirm scope, commit the authorization"
- Composes with hive-mind decision-routing directive Matt 2026-05-23 (seam-owner decides per audit evidence; Matt is last-resort escalation)
- Composes with Phase A1 closure record Matt 3-gate authorization (RATIFIED) + resolution plan § 1.5 D13 parallel-fire RATIFIED at Gate (c) + Concern #3 § 3.2 pre-ratified routing

**For:** the operational dispatch authorization + work-program scope-amendment for Cycle 14 v1 close trajectory; engine refactor completes no-classes recommitment at substrate-input layer; Phase A2 cascade-resumption-3 trajectory delivers substrate-led emergence promise the recognition record + cycle artifacts have been claiming

**Cycle 14 v1 trajectory update:**
- Prior estimate: ~1-1.5d Wave B + cascade through A2-7 (under cascade-resumption-2 path)
- Current estimate (this authorization): ~6-10d engine refactor + LLM + Gate-2 BEFORE A2-1 RE-FIRE-3 → cascade through A2-7 + D13 parallel-fire AFTER
- Total Cycle 14 v1 close shift: ~5-9d additional wall-clock vs prior trajectory
- Engine > Phase per CLAUDE.md; trajectory cost ACCEPTED per Matt 2026-05-29 election

**Next steps:**
1. Matt pastes cascade-resumption-3 fire prompt to new KR session (companion artifact same commit batch)
2. KR onboards via required first reads
3. KR fires Step S1 (rocket class-eradication dispatch) under R48.4 single-seam
4. Gandalf S4 fires in parallel in conversation thread (no sub-agent dispatch; no R48.4 conflict)
5. Cascade-resumption-3 sequence Step S1 → S6 → A2-1 RE-FIRE-3 → cascade through A2-7 + D13 parallel
