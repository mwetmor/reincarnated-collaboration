# Continuous-Observation Watchpoints — Phase-1 P1

**Author:** jack-ryan  
**Established:** 2026-05-17  
**Status:** ACTIVE — continuous-observation mode per hive-mind-protocol-2026-05-17.md § 7  
**Companion:** `baseline-test-snapshot-2026-05-17.md` (drift reference)  
**Hive log:** `phase-1-p1-log.md` (OBSERVATION entries filed here; findings link to this registry)

---

## WP-1 — Discipline #13 (implicit-pillar drift) across seams

**Risk level:** HIGH (per scope-of-work § 5, Risk #3)  
**Protocol ref:** hive-mind-protocol § 7.2

### WP-1a: Substrate identity field consistency

All four seams consume `SubstrateIdentity` after rocket D1 lands. Jack-ryan watches for divergent consumption:

| Field | Canonical name | Rocket source | Gamora consumption | Star-lord consumption | Drax consumption |
|---|---|---|---|---|---|
| Substrate name key | `identity.substrate` | `SubstrateIdentity.substrate` | resistance matrix row/col key | grouping label lookup | substrate browser display |
| Ailment name | `identity.ailment_signature.name` | loader | control-classification lookup | LLM prompt | N/A |
| Grouping label | `identity.grouping_label` | loader | N/A | `_CANONICAL_TO_GROUPING` replacement | substrate browser |
| Pair axis | `identity.pair_axis` | loader | resistance matrix valence | prompt pair-structure | N/A |
| Paired with | `identity.paired_with` | loader | resistance matrix 1.25×/0.75× lookup | pair-slot assignment | N/A |

**Trigger:** Any commit where a seam references substrate fields by a KEY that differs from `SubstrateIdentity` field names. E.g., if gamora indexes the resistance matrix as `"Lightning"` (capitalized) but rocket loads as `"lightning"` (lowercase) — silent mismatch that returns 1.0× for all lightning interactions. Case-sensitivity check at every D1 consumer review.

### WP-1b: Sub-system implementation vs canonical spec

After D3 (Path-a archetype refactor), per-substrate geometry biases must come from `SubstrateIdentity.geometry_affinities`, not default 1.0×. Watch for gamora composition function that falls back to 1.0× for new substrates (lightning, holy, shadow) due to missing entries. **This is Archetype-Coupling Archaeology Coupling #6.**

**Trigger:** gamora commits D3 composition function without explicit geometry_affinities × role composition for all 7 substrates.

### WP-1c: Vocabulary/naming inconsistencies

Canonical substrate name: `lightning` (lowercase, no alias). Watch for:
- star-lord LLM prompt using `"Lightning"` (capitalized)
- gamora resistance matrix using `"electric"` or `"lightning_bolt"`
- drax substrate browser using `"Thunder"` or `"Electric"`

**Source of truth:** `config/substrate_identities/lightning.yaml` field `substrate: lightning`

### WP-1d: Test coverage at cross-seam contract boundaries

Per coordination-matrix § 4, each producing seam's MIGRATION.md entry should have corresponding test coverage. Watch for MIGRATION.md entries WITHOUT a test exercising the cross-seam boundary (R11(b) vigilance).

Known gap: drax loadout has no MIGRATION.md and no cross-seam boundary tests. Will surface as OBSERVATION when drax begins D17/D21 work.

---

## WP-2 — Pattern P7 (silent-default convergence) watch

**Risk level:** HIGH (wide-net archaeology found 14+ instances; 3 HIGH-severity clusters unresolved)  
**Protocol ref:** hive-mind-protocol § 7.3; wide-net-coupling-archaeology § 2

### WP-2a: Coupling #8 — `llm/naming.py` `impact-mode-{element}` fallback

**File:** `src/reincarnated/llm/naming.py:32-42`  
**Current state:** `_CANONICAL_TO_GROUPING.get(element, f"impact-mode-{element}")` — silent fallback string for unknown substrate.  
**Required fix (D6):** Assert non-fallback. Any substrate not in `_CANONICAL_TO_GROUPING` must raise, not silently produce `"impact-mode-lightning"`.  
**Trigger:** star-lord ships D6 Phase A or Phase B without eliminating the `.get(element, default)` fallback pattern.

### WP-2b: Coupling #7 — constraint checker silent skip (gamora D3)

**File:** `src/reincarnated/generation/b6_kit_builder.py` constraint-checker registry  
**Current state:** **CLOSED 2026-05-18** — `_check_constraints()` raises `ValueError` on unknown tag. 9 new checkers registered. Verified at `gamora/v1.4-d3-path-a-impl-1`.  
**Required fix (D3):** Fail-loud on unknown constraint tags per scope-of-work § 1.1 D3 Coupling #7.  
**Trigger:** gamora ships D3 refactor without adding explicit `raise ValueError(f"Unknown constraint tag: {tag}")` or equivalent.

### WP-2c: Coupling #6 — geometry-bias silent-neutralization (gamora D3)

**File:** `src/reincarnated/generation/b6_archetype_templates.py` per-archetype geometry bias  
**Current state:** **CLOSED 2026-05-18** — `_compose_geometry_bias()` correctly multiplies `substrate.geometry_affinities` × `_ROLE_GEOMETRY_PREFS`. NEUTRAL-filter prevents 1.0× clutter. All 7 substrates produce non-neutral geometry biases. WP-9 smoke PASS post earth.yaml fix. Verified at `gamora/v1.4-d3-path-a-impl-1`.  
**Required fix (D3):** Composition function MUST multiply `SubstrateIdentity.geometry_affinities` × role's geometry preferences. No fallback to uniform 1.0×.  
**Trigger:** gamora D3 ships without confirming per-substrate geometry outputs for all 7 substrates (empirical check).

### WP-2d: Ailment registry gap — new substrates (gamora D5)

**Files:** `generation/element_biases.py`, `foundation/effect_categorization.py`, `generation/ability_grammar.py`  
**Current state:** `CONTROL_EFFECTS = frozenset({root, knockback, silence, chill})` — hardcoded. New ailments `shock` (lightning), `consecrate` (holy), `drain` (shadow) are NOT in this frozenset.  
**Effect:** New substrate ailments not recognized as control effects → AI strategy silently omits them from priority logic.  
**Required fix (D5):** `config/ailments.yaml` registry with `is_control` metadata; `CONTROL_EFFECTS` dynamically built from registry.  
**Trigger:** rocket ships any code that references `shock`, `consecrate`, or `drain` as ailments WITHOUT the D5 registry refactor in place.

### WP-2e: Role registry gap — AI strategy (gamora D4)

**File:** `simulation/ai_strategies.py:17-45` `ARCHETYPE_ROLE_PRIORITY` dict  
**Current state:** 20+ archetypes × role priority lists hardcoded. New archetypes for lightning/holy/shadow substrates will not appear in this dict.  
**Effect:** New archetypes default to whatever the AI strategy's unknown-archetype fallback is (likely baseline behavior, not substrate-coherent).  
**Required fix (D4):** gamora refactors `ai_strategies.py` to iterate the role registry and compute priorities per `SubstrateIdentity.role_affinities`, not hardcoded lists.  
**Trigger:** gamora ships D3 archetype composition without concurrent D4 AI strategy refactor.

---

## WP-3 — Discipline #1 (math-before-code) enforcement

**Protocol ref:** hive-mind-protocol § 7.4

### WP-3a: D7 math note review (PENDING — first active action)

Gamora's D7 math note is committed at `45a6014`. Gamora's AGENT_STATE explicitly marks "jack-ryan-ready for review." This is jack-ryan's first active obligation under continuous-observation.

**Review checklist (for hive log OBSERVATION entry):**
- [ ] Numeric 7×7 matrix present with all 49 cells documented
- [ ] DPS analysis at L1/L25/L50 — does any class become structurally over- or under-powered?
- [ ] Sensitivity analysis on ±25% valence magnitude — are there threshold effects?
- [ ] Implementation contract spec is unambiguous (call site, argument types, sparse vs dense representation)
- [ ] Extension path for P2 substrates (poison/acid) is spelled out per Discipline-candidate #14

**Target:** File OBSERVATION (INFO or WARN) in hive log after review. Approve with INFO or surface concerns with WARN/BLOCK.

### WP-3b: D10 (substrate-coherent generation rules) — frequency analysis required

Before gamora begins D10 code, per-substrate generation-frequency analysis must be authored. Specifically: at 7 substrates rotating through seasons, what is the expected per-substrate appearance frequency? Are any substrates over- or under-represented?  
**Status: CLOSED 2026-05-18** — D10 math note approved at `gamora/v1.4-d10-substrate-coherent-gen-math-1 @ abab9c4`. Frequency analysis complete in § 2.5/§ 6. D10 code phase READY.  
**Trigger:** gamora commits D10 code without a `simulation/math/substrate-generation-frequency-d10.md` (or equivalent) authored first.

### WP-3c: D14 (Layer-3 diversity gate) — similarity metric formula required

Before gamora begins D14 code, the Layer-3 similarity metric must be authored with explicit formula + threshold-T sensitivity analysis. This is BLOCKED on D27 perception test result.  
**Trigger:** gamora begins D14 code before perception test result + Layer-3 metric spec exist.

---

## WP-4 — Schema coherence vigilance (per protocol § 6.4)

### WP-4a: MIGRATION.md authoring concurrency

**Current gaps:**
- drax (loadout) has no MIGRATION.md — must be created before D17 browser surface ships
- drax (demo) has no MIGRATION.md — must be created before D19 VFX integration ships

**Watch pattern:** Any drax commit that introduces a cross-seam contract change (new schema field consumed from engine; new data format sent to loadout) WITHOUT a corresponding MIGRATION.md entry.

### WP-4b: Substrate field addition propagation

`PoolElement` (element/schema.py) received 5 new fields in Drift-14. One known gap: `telemetry/recorder.py` Coupling #9 has NOT been updated to iterate the new fields. When star-lord ships D2 Coupling #9 fix, watch that ALL 5 new PoolElement fields are correctly consumed, not just the ones star-lord was aware of.

**Trigger:** star-lord ships Coupling #9 telemetry update without addressing `substrate_native` field persistence.

### WP-4c: Resistance matrix consumer propagation

D7 adds a new damage-resolution path. Watch that ALL damage-resolution consumers are updated:
- `simulation/damage_resolver.py` (primary site, gamora)
- Any telemetry recorder field that captures "element vs element" or "substrate vs substrate" fight data (star-lord Coupling #9 may need new columns)
- Any export schema field that surfaces resistance interactions to drax

**Trigger:** gamora ships D7 code without star-lord acknowledging the new damage-resolution path in MIGRATION.md.

---

## WP-5 — Discipline-candidate #14 (layer-extensibility-judged-at-perimeter)

Per wide-net-coupling-archaeology § 2.1: "A layer's extensibility cannot be judged from one file's shape; the perimeter must be checked."

### WP-5a: Rocket D4 role registry — ALL 5+ consumer files

Rocket must refactor ALL 5 consumer files, not just `role_constraints.py`:
- `generation/role_constraints.py:27-114` (canonical authoring site)
- `generation/class_generator.py` (ROLE_SKILL_TEMPLATES, WEIRD_ROLE_POOLS, _EXPERIMENTAL_ROLE_POOL)
- `generation/monster_generator.py:59-66` (ARCHETYPE_ROLE_POOLS)
- `simulation/ai_strategies.py:17-45` (ARCHETYPE_ROLE_PRIORITY — gamora seam)
- `generation/ability_grammar.py` (role-keyed branching)

**Trigger:** rocket ships D4 role registry without MIGRATION.md listing all 5 consumer files. Or gamora ships D4 gamora-side without coordinating with rocket.

### WP-5b: Rocket D5 ailment registry — ALL 3+ consumer files

Per wide-net archaeology § 2.2, 3+ files consume hardcoded ailment names:
- `generation/element_biases.py:18-58` (ELEMENT_AILMENT, AILMENT_PARAM_RANGES, AILMENT_IS_CONTROL)
- `foundation/effect_categorization.py` (CONTROL_EFFECTS frozenset)
- `generation/ability_grammar.py` (fallback to `"silence"`)

**Trigger:** rocket ships D5 ailment registry without confirming all 3 consumer files iterate registry.

### WP-5c: Star-lord D6 — ALL LLM prompt sites adopt registry-driven generation

Per star-lord's own D6 plan § 1.2, 9 call sites are identified across categories A/B/C. Implementation must hit ALL of them, not just `cosmological_vocabulary.py`.

**Trigger:** star-lord ships D6 Phase A/B without confirming all 9 inventory sites are addressed (via test coverage or explicit scope-deferral note with justification).

---

## WP-6 — Race-condition discipline (per CHANGELOG 2026-05-16)

**Protocol ref:** scope-of-work § 5, Risk #8

**Watch pattern:** Any commit to the engine repo that:
- Uses `git add -A` or `git add .` (should always be explicit path)
- Has a commit message describing multiple seams' changes in one commit
- Touches files outside the committing seam's ownership boundaries

**Current state at baseline:** 4 post-activation commits are all single-seam, explicit-path commits. Good pattern established.

**Concurrent hot-spot alert:** `src/reincarnated/foundation/__init__.py` is touched by both rocket (D1 loader integration) and gamora (D2 Coupling #7 registry-passing). Coordination-matrix § 3 notes this. Watch for simultaneous edits when rocket commits D1 and gamora begins D2.

---

## WP-7 — Test-suite GREEN at every commit (per protocol § 8.5)

**Baseline:** 1988 PASSED, 3 FAILED (pre-existing, documented in baseline-test-snapshot § 1.2).  
**GREEN threshold:** ≤3 failing tests (the 3 pre-existing ones). Any 4th failure = regression.  
**Wall time reference:** Fast suite (no integration) ~60s; full suite ~26 min.

**Watch pattern:**
- Any commit that increases the failing-test count above 3
- Any commit that causes the substrate identity loader tests (107 tests) to fail
- Any commit that breaks test_no_canonical_four_in_llm_prompts.py (Discipline #14 guard)

**Broken state protocol:** Per § 8.5 — producing seam restores GREEN within 2 active hours; if not, surface to knight-rider.

---

## WP-8 — Drax D27 reference-monster representativeness (perception test prerequisite)

Per perception-test-experiment-scoping § 7.3: jack-ryan reviews drax's reference-monster spec for representativeness.

**What to check:**
- Does the reference monster require kiting (tests mobility archetypes)?
- Does the reference monster require some commitment/sustained fire (tests burst/control archetypes)?
- Does it have enough HP to exercise full rotations (>1-2 seconds)?
- Is it a meaningful threat (player must engage, not just stand and hit)?

**Trigger:** drax files HANDOFF for reference-monster spec in hive log → jack-ryan reviews within next active window.

---

## Active observation queue (updated 2026-05-18 post-D3 checkpoint review)

| Priority | Item | Status |
|---|---|---|
| ~~1~~ | D7 math note review | **CLOSED** (approved 2026-05-17) |
| ~~2~~ | D1 commit coherence check | **CLOSED** (rocket D1 @ `1e951be`) |
| ~~3~~ | D27 reference-monster spec review | **CLOSED** (drax D27 @ `drax/v0.23`) |
| ~~4~~ | D6 plan review | **CLOSED** (star-lord D6 @ `3d84a24`) |
| ~~5~~ | Loadout jest→vi fix | Low priority; non-blocking |
| ~~WP-2b~~ | Kit builder constraint silent-skip | **CLOSED** D3 @ `048611a` |
| ~~WP-2c~~ | Geometry bias silent-neutralization | **CLOSED** D3 @ `048611a` |
| ~~WP-9~~ | earth_caster smoke regression | **CLOSED** earth.yaml patched; smoke PASS |
| ~~WP-10~~ | New ARCHETYPE_ROLE_PRIORITY entries | **CLOSED** 11 new entries confirmed |
| ~~WP-11~~ | HYBRID_FORBIDDEN_PAIRS loader-derived | **CLOSED** substrate.forbidden_hybrid_with |
| ~~WP-3b~~ | D10 math note pre-code gate | **CLOSED** D10 approved; code phase READY |
| 1 | roles.yaml DPS-floor tag cleanup | INFO — route to rocket micro-task |
| 2 | New-substrate end-to-end integration smoke | INFO — gamora D10 code phase commitment |
| 3 | D3 → D14 downstream smoke (Layer-3 diversity gate) | Active — monitor as D8/D9 impl lands |

---

*Authored 2026-05-17 by jack-ryan. Active for Phase-1 P1 duration. Observations filed as hive log entries cross-referencing this registry (e.g., "see watchpoints WP-2a"). Updated when new watchpoints surface during continuous-observation.*
