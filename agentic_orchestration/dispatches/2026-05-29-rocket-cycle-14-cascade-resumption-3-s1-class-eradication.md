# Dispatch — Rocket — Cycle 14 Cascade-Resumption-3 Stream S1: Class-Concept Eradication at Substrate-Input Layer

**Date:** 2026-05-29
**From:** knight-rider (orchestrator)
**To:** rocket (content generation seam — generation/, element/, anchor/, foundation/, engine-internal canonical library)
**Authority:**
- Matt 2026-05-29 CLAUDE.md Engine > Game > Phase orientation invocation
- gandalf cascade-resumption-3 authorization at `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` § 2 Stream S1
- Matt verbatim 2026-05-27 "There are no classes... This must be deleted, and immediately" at `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md`
- Hive-mind decision-routing (seam-owner decides per audit evidence; Matt last-resort escalation)

**Pattern:** B sustained-execution (~1-2 days)
**R48.4:** SINGLE-SEAM — rocket dispatched alone; gandalf S4 fires in parallel conversation thread (no sub-agent dispatch from S4); no other sub-agent active

---

## 0. TL;DR

**Erase class taxonomy from substrate-input layer at `endgame_encounter_catalog.py` and downstream surfaces that consume class-suffixed encounter_ids.** This completes the Matt 2026-05-27 no-classes architectural recommitment at the substrate-input layer (it previously landed only at player-architecture layer per doc 48 VESTIGIAL + engine commit `c9fcb1d`).

**Substrate-derived encounter_id naming scheme** (pre-ratified per authorization § 3 line 226 gandalf scheme):
`endgame_bc_{range}_{tempo}_{amplitude}_{attribute}_{proxy_density}`
e.g., `endgame_str_01_heavy_barbarian` → `endgame_bc_melee_low_spiky_str_none`

**Preserve:** cohort_archetype constants (DPS-min-maxer / Balanced / Defensive / Hybrid — load-bearing for BVV per doc 50 Path α RATIFIED); BC tuple fields (range/tempo/amplitude/attribute/proxy_density); T4 Capstone architecture (doc 47 § 4.6); scenario shell IDs (boss_with_adds/open_arena/elite_pack/chokepoint_corridor/magic_pack/mini_boss); MobSpec.archetype_tag (mob-side taxonomy: swarmer/caster/brute/sniper/controller/tank).

**Acceptance gate:** ZERO class-name strings (barbarian / wizard / cleric / monk / knight / fighter / assassin / archer / sniper / fencer / spellsword / mage / caller) in `endgame_encounter_catalog.py` AND in downstream surfaces that consume catalog encounter_ids. Verified via grep (Disc #11 empirical inspection).

**Effort:** ~1-2 days. Engine architectural-integrity work; Phase A2 cascade-timing cedes per CLAUDE.md.

---

## 1. Required first reads (in order)

1. `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` — AUTHORITATIVE work-program; § 2 Stream S1 + § 3 pre-ratified decisions + § 5 preservation constraints
2. `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` — Matt 2026-05-27 verbatim; vocabulary lock; what survives untouched (§ 1.4); retired vocabulary table (§ 2); 5 weapon_type_family substrate tuples (§ 6)
3. `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` § 4-quater Instance 6 ROOT-CAUSE sub-case — propagation cascade table; substrate-input layer empirical refutation
4. `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 — T4 Capstone architecture PRESERVED
5. `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — cohort_archetype LOAD-BEARING for BVV; PRESERVED
6. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #11 + #41 + #42a + #45 + #48 LOAD-BEARING for this work

---

## 2. Scope

### 2.1 Primary refactor target — `endgame_encounter_catalog.py`

File location: `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_encounter_catalog.py` (1002 lines, 18 entries)

**Refactor every encounter entry (all 18):**

| Field | Action | Notes |
|---|---|---|
| `encounter_id` | RENAME to substrate-derived scheme | `endgame_bc_{range}_{tempo}_{amplitude}_{attribute}_{proxy_density}` (gandalf scheme) |
| `archetype_name` | RETIRE / REPLACE with substrate-derived neutral identifier | Substrate-anchored descriptor (e.g., "melee / low-tempo / spiky-amplitude / STR / no-proxy" or analogous neutral form). Field MAY be removed entirely if no downstream consumer requires it; if removed, document removal in dataclass `EndgameReferenceEncounter` (line 99) + update load order |
| `intent` | REWRITE — remove "the class" framing | Describe encounter in terms of BC-tuple capabilities + mob composition + scenario shell. E.g., instead of "tests the Heavy Barbarian's burst-window timing," write "tests low-tempo spiky-amplitude STR rotation against high-HP boss + sustained-pressure adds" |
| `cohort_notes` | REWRITE — remove class-name references | Preserve cohort viability assessment in BC-tuple + cohort_archetype terms. E.g., "Defensive cohort may fall below KPM floor due to low-tempo class" → "Defensive cohort may fall below KPM floor at low-tempo / spiky-amplitude rotation depth" |

**Preserve unchanged in this file:**
- `EndgameReferenceEncounter` dataclass structure (line 99) except `archetype_name` field (per above)
- BC 5-tuple fields (`bc_range`, `bc_tempo`, `bc_amplitude`, `bc_attribute`, `bc_proxy_density`)
- `scenario_shell_id` values (boss_with_adds / open_arena / elite_pack / chokepoint_corridor / magic_pack / mini_boss) — encounter-structure-keyed, not class-keyed
- `mob_composition` lists + MobSpec dataclass — mob-side archetype_tag taxonomy (swarmer/caster/brute/sniper/controller/tank) is DIFFERENT concept from player-class and PRESERVED
- `wr_expectation`, `endgame_node`, `difficulty_calibration`, `sequence_intent`, `termination_conditions`, `arena_interaction`, `playability_gate`, `viable_cohorts` — all preserved unless they contain class-name references (audit + rewrite if so)
- `COHORT_DPS_MIN_MAXER`, `COHORT_BALANCED`, `COHORT_DEFENSIVE`, `COHORT_HYBRID` constants (lines 56-59) + `ALL_COHORTS` tuple — LOAD-BEARING for BVV per doc 50; PRESERVED
- `_validate_catalog()` empirical count assertion (18 encounters); the renaming preserves count

### 2.2 Cross-seam downstream surfaces requiring parallel update (atomic semantic coherence)

These files consume catalog `encounter_id` as string keys; encounter_id renaming requires parallel update to preserve runtime correctness. Per ADR-004 this is cross-seam work; rocket executes the parallel updates atomically; **MIGRATION.md entry REQUIRED** for cross-seam impact awareness (gamora-owned simulation seam consumed).

| File | Surface | Action |
|---|---|---|
| `src/reincarnated/simulation/phase7_bridge.py` lines 134-151 | `PHASE7_SYNTHETIC_KIT_MAGNITUDE_BY_BC_CELL` dict keyed on class-suffix encounter_ids | UPDATE all 18 keys to new substrate-derived encounter_ids; preserve magnitude values; preserve trailing comment metadata (encounter type / damage→DPS routing) |
| `src/reincarnated/simulation/phase7_bridge.py` line 202 | Docstring "Satisfies the player_class interface" framing | REWRITE to "Satisfies the kit-substrate-input interface" or analogous class-free phrasing |
| `src/reincarnated/simulation/phase7_bridge.py` line 222 | Docstring "bc_cell_id (= encounter_id from ENDGAME_ENCOUNTER_CATALOG)" | UPDATE if class-keyed example strings appear; verify class-free |
| `src/reincarnated/simulation/phase7_cohort.py` line 9 + 286-310 | Module docstring + `classify_kit_cohort_from_encounter_id()` function | AUDIT for class-suffix expectations in encounter_id parsing; if classify logic depends on suffix-string-pattern parsing (e.g., regex on `_heavy_barbarian` suffix), refactor to substrate-tuple-keyed classification |
| `src/reincarnated/simulation/gauntlet_sim.py` lines 113, 372, 396, 408, 443, 628, 721, 735-759, 807, 859, 940, 954, 1015 | Multiple references to `ENDGAME_ENCOUNTER_CATALOG` + `encounter_id` field consumption | AUDIT each reference; code references to `encounter.encounter_id` (the dataclass field) survive renaming without change; HARDCODED string-key references require update; verify Disc #11 grep |
| `src/reincarnated/simulation/bounded_viability_validation.py` lines 968-991 | Imports catalog for scenario_shell_id check | AUDIT only — scenario_shell_id field unchanged; no action expected unless class-suffix encounter_id parsing exists |
| `src/reincarnated/llm/spirit_guide_voice.py` line 289 | `form.archetype_name` reference | INVESTIGATE — this is form-level (post-Phase-5 cohesion judge output), NOT catalog archetype_name; if form.archetype_name is a substrate-anchored form descriptor produced by Phase 5 (Sketch F), preserve; if it consumes catalog archetype_name as input, refactor. Likely PRESERVE but verify |

### 2.3 Test alignment

| File | Action |
|---|---|
| `tests/test_cycle14_wave1_concentration.py` lines 394, 427 | UPDATE comment references "Cycle 13 regression: str_01 heavy_barbarian 4x damage-reflection" + "wis_04 storm_caller duplicate counter_on_block" — encounter_id strings need rewrite to new substrate-derived names |
| Test files referencing class-suffix encounter_ids | AUDIT grep across `tests/` for `endgame_str_`, `endgame_dex_`, `endgame_int_`, `endgame_wis_` patterns; update each to new naming |
| Tests asserting `archetype_name` field value | AUDIT; if `archetype_name` field is removed from dataclass per § 2.1, test assertions need parallel update |

### 2.4 Audit other engine surfaces for surviving class taxonomy

Beyond the enumerated above, rocket must grep + audit (Disc #11 empirical inspection per acceptance gate § 3):

```bash
grep -rnE 'barbarian|wizard|cleric|monk|knight|fighter|assassin|archer|sniper|fencer|spellsword|mage|caller' \
  ~/Games/reincarnated-engine/src/reincarnated/ --include='*.py'
```

**Pre-known surviving SAFE surfaces (PRESERVE — not in scope):**
- `llm/phase5_orchestrator.py` lines 37, 783, 885 — comments enforcing Disc #45 vocabulary lock ("no class/warrior/mage/rogue/hunter/paladin in prompts"); these are POLICY enforcement strings, not taxonomy use; PRESERVE
- `llm/spirit_guide_voice.py` lines 92, 230-234, 330 — Tidecaller/Stormcaller (form-level naming) + "Do NOT use class-archetype labels" policy + "fire-mage tropes" LLM-bias commentary; these are substrate-anchored form names + policy enforcement; PRESERVE
- `element/selector.py` lines 113, 119, 128 — uses "mage", "haze", "smoke" as LINGUISTIC EXAMPLES for vowel-ending word phonetic detection; PRESERVE (not taxonomy)
- `llm/naming.py` line 39, 210 — "fire-mage tropes" LLM-bias commentary; PRESERVE (not taxonomy use)

**If grep surfaces unanticipated class-taxonomy surfaces beyond the enumerated above + the pre-known SAFE list:** SURFACE TO KNIGHT-RIDER per § 4 (scope-amendment decision required; authorization § 4 line 239 condition).

---

## 3. Acceptance criteria (Disc #11 empirical inspection)

Run all of the following at S1 close; ALL must PASS:

### 3.1 Catalog file grep (PRIMARY)

```bash
grep -nE 'barbarian|wizard|cleric|monk|knight|fighter|assassin|archer|sniper|fencer|spellsword|mage|caller' \
  ~/Games/reincarnated-engine/src/reincarnated/generation/endgame_encounter_catalog.py
```

**Expected:** ZERO matches (PASS condition for Disc #45 vocabulary lock at primary substrate-input layer).

### 3.2 Engine-wide downstream grep (CROSS-SEAM coherence)

```bash
grep -rnE 'barbarian|wizard|cleric|monk|knight|fighter|assassin|archer|sniper|fencer|spellsword|caller' \
  ~/Games/reincarnated-engine/src/reincarnated/ --include='*.py' --exclude='naming.py'
```
(naming.py excluded for "fire-mage tropes" LLM-bias commentary which is PRESERVE)

**Expected:** ZERO matches in encounter-id / archetype-name / class-taxonomy use; the pre-known SAFE surfaces (phase5_orchestrator policy strings, spirit_guide_voice form names + policy) may be ALLOWED if explicitly audited as policy-enforcement OR substrate-anchored form-level vocabulary, NOT pre-imposed class taxonomy.

NOTE on "mage": this token survives in:
- LLM policy enforcement strings (Disc #45 enforcement — PRESERVE)
- element/selector.py phonetic linguistic data (PRESERVE)
- llm/naming.py "fire-mage tropes" bias commentary (PRESERVE)

These surfaces are PRESERVE and documented as such; if rocket grep surfaces a NEW "mage" use outside these surfaces, that requires audit.

### 3.3 Catalog dataclass integrity

- `_validate_catalog()` empirical count assertion (18 encounters) MUST still PASS at module load
- All 18 encounter_ids MUST be unique (substrate-derived naming preserves uniqueness IF BC 5-tuples are unique, which they are by catalog construction)

### 3.4 Phase7 bridge magnitude dict integrity

- 18 keys in `PHASE7_SYNTHETIC_KIT_MAGNITUDE_BY_BC_CELL` MUST match 18 catalog encounter_ids exactly (string equality; runtime correctness gate)
- Magnitude values MUST be preserved unchanged (gamora Concern #1 Step 1 calibration preserved)

### 3.5 Test suite

- All engine-wide tests PASS post-refactor (smoke gate per Disc #2)
- Specific watch: `test_phase7_bridge.py`, `test_phase7_cohort.py`, `test_gauntlet_sim.py`, `test_cycle14_wave1_concentration.py`, `test_endgame_encounter_catalog.py` (if exists)

### 3.6 Smoke test (Disc #2)

- Module import smoke: `from reincarnated.generation.endgame_encounter_catalog import ENDGAME_ENCOUNTER_CATALOG` succeeds; `len(ENDGAME_ENCOUNTER_CATALOG) == 18`
- Phase 7 bridge construction smoke: `Phase7SyntheticKit` constructor succeeds for each new substrate-derived bc_cell_id (verifies magnitude dict + cohort classification both resolve)
- Gauntlet sim catalog load smoke: `build_reference_gauntlet()` returns 18 configs without error

---

## 4. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **Unexpected propagation surface** | Grep surfaces class-taxonomy outside enumerated targets + pre-known SAFE surfaces (e.g., canonical doc references; decisions-log entries; engine canonical library file content; additional LLM prompt surfaces beyond audited) | HALT refactor + commit current state to branch + surface findings to knight-rider with grep output; per authorization § 4 line 239 scope-amendment decision required |
| **MobSpec.archetype_tag semantic ambiguity** | Mob-side archetype_tag values (swarmer/caster/brute/sniper/controller/tank) raise vocabulary-lock semantic concerns (e.g., "sniper" overlaps player-class taxonomy at glance) | DEFER — rocket attestation flags as captured finding for cumulative gandalf review; NOT a S1 BLOCKING decision (these are mob-archetype, not player-class; semantic-mode-separation argument lands) |
| **archetype_name field removal vs preserve decision** | rocket audit surfaces downstream consumer of catalog `archetype_name` field that prevents clean removal | DEFAULT: preserve field with substrate-anchored neutral identifier (NOT class name); document the constraint at completion record; surface to knight-rider for awareness |
| **Phase7 bridge bc_cell_id format incompatibility** | If phase7_cohort.py `classify_kit_cohort_from_encounter_id()` parses encounter_id via class-suffix regex pattern, refactor requires non-trivial logic change | HALT mid-refactor + surface findings to knight-rider; may require gamora seam consultation |
| **Test failures post-refactor** | Any test in engine-wide suite fails after refactor due to expected class-name string assertion | PASS-1 attempt: align test expectations to new substrate-derived strings; PASS-2: if test failure indicates DEEPER class-taxonomy dependency (not just string update), HALT + surface |
| **R48.4 pre-flight** | `vm_stat` shows < 1 GB free + reclaimable RAM at mid-execution checkpoints | PAUSE + report; resume when RAM available |
| **Disc #42a framing-audit catch** | Q1-Q6 surfaces pre-imposed assumption mid-execution (e.g., refactor assumes catalog-encounter-id matches kit-id-derivation pattern but empirical evidence shows divergence) | HALT + surface findings to knight-rider |

---

## 5. Out-of-scope for S1

The following are explicitly OUT OF SCOPE for S1 (per authorization § 5):

- cohort_archetype taxonomy (preserved as load-bearing for BVV per doc 50)
- T4 Capstone Skill architecture (preserved per doc 47 § 4.6)
- BVV framework (preserved per doc 50)
- A/B comparison protocol (runs at Wave 5 close; independent)
- Phase 7 cohesion_judge_confidence ≥ 0.75 threshold (scaffold-flag for separate Pattern B if needed)
- Player-facing faction-architecture commitments (deferred-commitments recognition record stands)
- Decisions-log canonical writes (jack-ryan owns; not rocket scope)
- Investment scaling Patterns 3-6 (Cycle 15+ candidate)
- Antagonist/contrast-faction generation (Cycle 15+ per recognition record gate (iii))

S2 (gauntlet variant enumeration expansion) and S3 (Phase 4 archive variant preservation) are SEPARATE dispatches that fire AFTER S1 acceptance gate; rocket does NOT pre-execute S2/S3 work in this dispatch.

S5 (Wave B full implementation) is star-lord-primary + rocket-integration AFTER S3+S4; rocket does NOT pre-execute S5 in this dispatch.

---

## 6. Engineering disciplines composition

| Discipline | Application in S1 |
|---|---|
| **Disc #1 math-before-code** | N/A — refactor is renaming + substrate-vocabulary replacement, not algorithmic change (no math hotspot in S1) |
| **Disc #2 smoke-test before full fire** | § 3.6 smoke test gate before tag |
| **Disc #11 empirical inspection** | § 3.1 + § 3.2 grep verification = the primary acceptance gate |
| **Disc #18 math hotspot consultation** | N/A in S1 (relevant for S2 variant-cycling methodology if multiple options surface) |
| **Disc #41 substrate-led vocabulary lock** | LOAD-BEARING — S1 IS the operational application at substrate-input layer |
| **Disc #42a framing-audit Q1-Q6** | Applied at every refactor step + at any mid-execution surprise (cross-reference Instance 6 ROOT-CAUSE sub-case at pushback memo § 4-quater) |
| **Disc #43 design-quality wave-close audit** | jack-ryan applies at S6 Gate-2; NOT rocket scope at S1 |
| **Disc #45 vocabulary lock** | LOAD-BEARING — § 3.1 + § 3.2 grep is the enforcement instrument |
| **Disc #48 R48.4 single-seam** | rocket dispatched alone; gandalf S4 parallel conversation thread is NOT a sub-agent (no R48.4 conflict) |
| **Pattern E autonomous-pair pre-authorization** | Applies at S6 Gate-2 (post-S5); NOT at S1 fire |
| **Recognition → empirical validation → commit** | Recognition: Matt 2026-05-29 catalog class-taxonomy finding + CLAUDE.md orientation election; Validation: § 3 grep + smoke + tests; Commit: rocket auto-commits per CLAUDE.md addendum 2026-05-25 |

---

## 7. Deliverables

1. **Engine commit(s)** — refactored `endgame_encounter_catalog.py` + parallel-updated `simulation/phase7_bridge.py` magnitude dict + audited downstream consumers + tag (rocket prefix per CLAUDE.md conventions: e.g., `rocket/v1.0-cascade-r3-s1-class-eradication-1`)
2. **MIGRATION.md entry** per ADR-004 — captures cross-seam impact (catalog encounter_id renames; phase7_bridge dict key updates; downstream consumer audit findings); gamora-readable cross-seam handoff
3. **Completion record appended to this dispatch file** — captures: (a) all 18 encounter_id renames mapped (old → new); (b) all 18 archetype_name field changes (preserved-with-substrate-vocab or removed); (c) audit findings on downstream consumers + pre-known SAFE surfaces verified; (d) acceptance criteria § 3.1-3.6 results; (e) any surface-to-knight-rider findings; (f) Disc #11 + Disc #45 grep output ZERO PASS
4. **AGENT_STATE.md checkpoint** at `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — captures S1 close + cascade-resumption-3 trajectory + next-cascade-step expectation (S2 gauntlet variant enumeration expansion, separate dispatch)
5. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade-resumption-3 work; commit fires without re-asking; push REQUIRES Matt-explicit-authorization (per addendum default; cascade-resumption-3 push-pattern NOT yet established by Matt; rocket does NOT push)

---

## 8. Sign-off

**Authored:** knight-rider per Matt 2026-05-29 cascade-resumption-3 entry + gandalf authorization § 2 Stream S1 + hive-mind decision-routing in-scope orchestration

**Rocket session-start protocol:**
1. Onboard via § 1 required first reads
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption (verify load-bearing assumptions; surface if any refute)
3. Execute § 2 refactor scope
4. Apply § 3 acceptance gate
5. Surface conditions per § 4 if triggered
6. Author § 7 deliverables
7. Auto-commit per CLAUDE.md addendum

**KR next-step on S1 close:** verify § 3 acceptance criteria + § 7 deliverables; route S2 dispatch (gauntlet variant enumeration expansion; rocket + gamora; depends on S1) per cascade-resumption-3 authorization § 2.

**Cascade-resumption-3 trajectory:** S1 → S2 → S3 → (S4 parallel by gandalf in conversation thread) → S5 → S6 → A2-1 RE-FIRE-3 → A2-2 → A2-3 → A2-4 → A2-5 → A2-6 → A2-7 v1 tag ratification.

**Signed:** knight-rider (orchestrator)
