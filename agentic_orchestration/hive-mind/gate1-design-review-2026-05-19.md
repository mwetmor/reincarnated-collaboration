# Gate 1 Design Review — 2026-05-19 (Next-Pass Batch)

**Reviewer:** jack-ryan
**Date:** 2026-05-19
**Session context:** Engine-rebuild hive — second jack-ryan invocation. First-pass Gate 1 PASS on R1 math note (bf47591) cleared gamora for baseline measurement. This pass reviews five targets dispatched by knight-rider HANDOFF (hive log 0b51312).
**Principles applied:** Review Principles 1-5; Engineering Disciplines #1, #8, #11, #13a, P7; ADR-004
**BLOCK authority:** retained per protocol § 4.5. No specialist has ignored a surfaced concern; first response is WARN.

---

## Target 1 — R3 Schema Design Coherence

**File reviewed:** `reincarnated-engine/design/working-agreement/R3-schema-design-2026-05-19.md`
**Authors:** rocket (§§ R-0–R-8), star-lord (§§ SL-1–SL-8), elrond (§§ E-0–E-10)
**Companion MIGRATION.md reviewed:** `src/reincarnated/generation/MIGRATION.md` [2026-05-19 R3+R7 section]
**Companion MIGRATION.md reviewed:** `src/reincarnated/export/MIGRATION.md` [schema 2.6/2.7/2.8 skeleton]

### Verdict: WARN

Two items require attention before implementation begins. Neither is a BLOCK because both are reconcilable within the existing document structure without design revision; they are internal consistency gaps, not principle violations.

---

#### WARN-R3-1: Archetype vocabulary mismatch between rocket section and elrond section

**What was found:**

Rocket's `preferred_behavior` derivation table (§ R-2.1) lists archetype_tag values from current production bestiary: `brute`, `tank`, `caster`, `ranger`, `bruiser`, `skirmisher`. Elrond's empirical cross-table (§ E-3.2) lists DIFFERENT archetype_tag values observed in the 5 shipped seasons: `brute`, `caster`, `swarmer`, `controller`, `tank`, `sniper`.

The shipped catalogue uses `swarmer` / `controller` / `sniper` — not `ranger` / `bruiser` / `skirmisher`. These are NOT the same archetypes with different names; the role distributions differ.

**Concrete drift instances (Discipline #13a):**

| Shipped archetype (elrond empirical) | Rocket's derivation table | Elrond's 4-value enum (pre-update) |
|---|---|---|
| `swarmer` | NOT in rocket § R-2.1 table | mapped to `melee_aggressive` |
| `controller` | NOT in rocket § R-2.1 table | mapped to `cast_at_range` |
| `sniper` | NOT in rocket § R-2.1 table | mapped to `ranged_kite` |
| `ranger` | In rocket § R-2.1 — maps to `ranged_kite` | NOT in shipped catalogue |
| `bruiser` | In rocket § R-2.1 — maps to `charge_then_melee` | NOT in shipped catalogue |
| `skirmisher` | In rocket § R-2.1 — maps to `hit_and_run` | NOT in shipped catalogue |

Rocket's `skill_rotation_priority` defaults table (§ R-2.5) also uses `ranger`, `bruiser`, `skirmisher` — none of which appear in the shipped catalogue per elrond's empirical audit.

**Impact:** elrond's backfill script, written against the shipped archetype vocabulary (`swarmer`, `controller`, `sniper`), will successfully derive `preferred_behavior` using elrond's derivation table. But rocket's generator, once implemented, will use `ranger`, `bruiser`, `skirmisher` vocabulary for new content. Post-R3 new content will have a different archetype vocabulary than backfilled content. This is a latent Discipline #13a drift instance — implementation will follow the design doc; the design doc has an internal inconsistency about which vocabulary is canonical.

**Cite:** Discipline #13a (implementation-vs-intent); WP-R3-A-1 (schema field naming drift across seams); WP-XSEAM-2 (three-seam concurrent ownership of monster JSON schema)

**Required action (elrond + rocket, before implementation):** Elrond and rocket must reconcile the archetype vocabulary. One of two resolutions:

1. **Rocket adopts shipped vocabulary** (`brute`, `tank`, `caster`, `swarmer`, `controller`, `sniper`) as the canonical archetype_tag set for all new content generation. Rocket updates §§ R-2.1, R-2.5 derivation tables to use the shipped names. The 6-value `preferred_behavior` enum is unchanged; only the archetype→behavior mapping table column headings change.

2. **New content uses new vocabulary** (`ranger`, `bruiser`, `skirmisher`) while backfill uses old vocabulary. Elrond's backfill then maps old→new archetype during backfill (a translation layer). This is more complex and requires explicit documentation.

L1 schema authority: rocket. Elrond coordinates per WP-XSEAM-2. Knight-rider to route if the decision creates schedule pressure.

---

#### WARN-R3-2: `range_m` minimum stated inconsistently across documents

**What was found:**

The schema design doc (§ R-1.2) states the minimum for `range_m` is `0.0` (self-cast sentinel). The generation MIGRATION.md (line 2102) states: `float (meters; 0.0 = self-cast sentinel; minimum 0.5 for non-self-cast)`.

The phrase "minimum 0.5 for non-self-cast" is NOT in the schema design doc. This creates an ambiguity at validator implementation: does the validator enforce `range_m >= 0.5` for non-self-cast skills, or does it enforce `range_m >= 0.0` with a separate self-cast role check?

The schema design doc's self-cast cross-check (§ R-1.2 final bullet) is the correct mechanism: if `range_m == 0.0` AND `role` is not `defensive/sustain/mobility`, the validator raises. This implicitly establishes 0.0 as valid ONLY for those roles, which means the effective minimum for other roles is the smallest positive value derivable from the effect_category table — which happens to be 1.5m for `melee_strike`. But that is not the same as a 0.5m floor.

**Impact:** validator implementers (rocket at generation seam, gamora at fight_engine.py) may implement different floors depending on which doc they read first. Minor but catches exactly the kind of implementation drift Discipline #13a is designed to prevent.

**Required action (rocket):** add one sentence to MIGRATION.md [2026-05-19 R3+R7 section] clarifying: "minimum range_m for non-self-cast is 0.0 effectively (via the role cross-check, not a numeric floor); no separate 0.5 minimum enforced; the role cross-check IS the non-self-cast gate." If a 0.5 floor is intended, add it to the schema design doc § R-1.2 explicitly.

---

#### Non-blocking observations (PASS-level):

**Pattern P7 commitment (§ R-6.3):** Strong. The schema design doc explicitly bans `dict.get("preferred_behavior", default)`. The MIGRATION.md consumer obligations table is comprehensive (generation, sim, export, parity-test seams all named). The validation timing decision (boot-time fail-loud) is clear and correctly positioned.

**`range_m = 0.0` self-cast sentinel:** design intent is unambiguous (§ R-1.2). The role cross-check (`if role not in {defensive, sustain, mobility}: raise`) is a sound validator design. No runtime ambiguity for consumers that implement the validator before use.

**`leash_distance_m >= aggro_radius_m + 2.0` validation:** rationale is sound (prevents aggro-and-instant-leash loop). Edge case: the boss/miniboss override pass (§ R-5.2) sets `aggro_radius_m = 12.0`; the leash default for `stationary_caster` is `18.0`. 18.0 >= 12.0 + 2.0 = 14.0 — constraint satisfied. No degenerate case from the override pass.

**Disengage algorithm (§ R-4):** producer-consumer surface is clean. Disengage is described as a sim-side behavioral rule reading from JSON fields (`leash_distance_m`, `aggro_radius_m`); it is NOT a new JSON field. Gamora seam owns implementation; rocket seam owns the JSON fields that disengage reads. Clean separation.

**Three-author coherence (star-lord + elrond + rocket):** star-lord's `range_band` as derived telemetry field (not source schema) resolves correctly. Elrond's coordination notes (§ E-9) are thorough. The remaining archetype vocabulary gap (WARN-R3-1 above) was flagged by rocket in the HANDOFF but not yet resolved in the document.

**MIGRATION.md concurrency (WP-R3-A-2):** SATISFIED. Both generation/MIGRATION.md and export/MIGRATION.md carry R3 entries. ADR-004 gate honored explicitly in generation MIGRATION.md header. All 7 new fields named in the MIGRATION.md table.

**Cross-seam consumer obligations:** generation MIGRATION.md enumerates all consumer seams (gamora, drax/R4+R5, star-lord, elrond) with their field obligations. Demo-side obligations correctly deferred to R4+R5 dispatches.

---

## Target 2 — R7 Parity Test Specification

**File reviewed:** `reincarnated-engine/design/working-agreement/R7-parity-test-spec-2026-05-19.md`
**Author:** star-lord
**Companion reviewed:** `R7-consumer-audit-2026-05-19.md`

### Verdict: WARN

One item — the DemoAgentMock `.get()` usage — is a direct Pattern P7 conflict that must be addressed before harness implementation.

---

#### WARN-R7-1: DemoAgentMock uses `.get()` for required fields — Pattern P7 violation in the test harness itself

**What was found:**

The DemoAgentMock in § 5 reads required R3 fields with `monster_json.get("aggro_radius_m")` etc.:

```python
self.aggro_radius_m = monster_json.get("aggro_radius_m")      # REQUIRED: fail-loud if absent
self.leash_distance_m = monster_json.get("leash_distance_m")  # REQUIRED
self.preferred_behavior = monster_json.get("preferred_behavior")  # REQUIRED
self.range_profile = monster_json.get("range_profile")         # REQUIRED
```

The `.get()` method returns `None` silently when the field is absent. The subsequent `assert self.aggro_radius_m is not None` DOES raise on None, but only for `aggro_radius_m` — the other three (`leash_distance_m`, `preferred_behavior`, `range_profile`) have no corresponding assert. They can silently be `None` and the mock proceeds to use them in `simulate_aggro_trigger()` and `simulate_preferred_behavior()`.

This is the precise Pattern P7 shape: `.get()` produces `None`; downstream logic fails or silently defaults. The parity test harness, designed to CATCH Pattern P7 in production consumers, contains Pattern P7 in its mock.

The correct pattern for required fields is `monster_json["aggro_radius_m"]` — raises `KeyError` immediately if absent, consistent with the schema design doc § R-6.3 commitment. The assert is then a redundant guard, not the primary gate.

**Required action (star-lord):** replace all four `.get()` calls in `DemoAgentMock.__init__()` with direct key access (`monster_json["aggro_radius_m"]` etc.) per § R-6.3. If the comment rationale is "we want to produce a friendlier error message than KeyError," add the try/except with explicit error message — but do NOT use `.get()`. The pattern P7 ban applies to the test harness as much as to production code.

**Cite:** Pattern P7; § R-6.3 Pattern P7 commitment; WP-R7-A-4 (missing JSON field triggers fail-loud); WP-R3-A-3 (schema validators fail-loud on missing fields)

---

#### Non-blocking observations (PASS-level):

**Harness architecture (instantiate-both-engines):** rationale is sound and well-documented (§ 3). The telemetry-comparison rejection reasons (no controlled mutation; wrong observability grain) are correct.

**Test 2 (intentional-break / WP-R7-A-3):** explicitly specified (`test_intentional_break_fails_loud()` in § 7). The test injects a hardcoded-constant mock consumer and asserts file:line failure reporting. This is the self-validation test the watchpoint requires. WP-R7-A-3 is satisfied in spec.

**Failure reporting mechanism (§ 4):** the file:line reporting plan is credible. The "static analysis grep" fallback for TS constants is honest about its limits. The Pattern P7 failure message is explicit ("Override detected: consumer did NOT read monster JSON field. This is a Pattern P7 violation.").

**±10% default tolerance / ±15% leash pre-R4 (§ 2):** the leash tolerance rationale is correct — room-edge halt is a proxy, not the actual `leash_distance_m` field, so higher tolerance is warranted. The tighten-to-±10%-after-R4 note is forward-appropriate.

**`preferred_behavior` exact-match (zero tolerance):** correct. A categorical observable has no partial-credit semantics.

**Demo-side mock fidelity contract (§ 5):** the mock replacement post-R5 is explicit — same interface, different implementation. The "mock itself is tested" note is good discipline.

**Discipline #11 (live-state verification) load-bearing check:** the parity test IS the gold standard for the parity claim. The spec is the gate for R7. Satisfied.

**Consumer audit (§ 5 in R7-consumer-audit-2026-05-19.md):** engine-side 4 call sites enumerated correctly. WP-R7-A-2 known sites (`world/movement.ts:74-78 PREFERRED_RANGE` and `:81 KITE_TRIGGER`) are named in the audit summary. WP-R7-A-2 is satisfied.

---

## Target 3 — R7 Consumer Audit

**File reviewed:** `reincarnated-engine/design/working-agreement/R7-consumer-audit-2026-05-19.md`
**Author:** star-lord (engine-side); rocket section placeholder

### Verdict: PASS (with OBSERVATION on rocket section placeholder)

The engine-side audit is comprehensive and correct. The rocket section placeholder is expected at this stage and is non-blocking.

---

#### OBSERVATION-R7-audit-1: Rocket section placeholder — not blocking, gated on schema design

The rocket section (§ 4) is a placeholder — "Rocket appends this section when R3 schema lands." This is by design per the dispatch sequencing: rocket's consumer section requires the schema design to be final first. Now that rocket's schema design section is complete, rocket should append the `CombatantState` construction section in the next implementation session.

**Non-blocking** because this section is a design-doc addendum, not a code change. The consumer audit is sufficiently covered by star-lord's engine-side enumeration for the Gate 1 review. Implementation cannot proceed for the `CombatantState` construction call site until rocket appends it, which is the correct ordering.

---

#### Non-blocking OBSERVATION (demo-side, read-only):

The two demo-side TS constants (`world/movement.ts:74-78 PREFERRED_RANGE` and `:81 KITE_TRIGGER`) are named correctly. This is a read-only audit finding — star-lord correctly defers these to drax/R5. No anomalies in the demo-side enumeration.

---

## Target 4 — R8 LLM Orchestration Design

**Files reviewed:** `R8-pipeline-design-2026-05-19.md` (star-lord section §§ SL-1–SL-6); `src/reincarnated/llm/MIGRATION.md` (R8 skeleton)
**Authors:** rocket (pipeline section — placeholder), star-lord (LLM orchestration section)

### Verdict: WARN

One mode-naming inconsistency between documents requires resolution before implementation. The rocket section placeholder is a sequencing gap (not a WARN on its own given the two-mode design is unresolved), but combined with the naming issue it creates a concrete pre-implementation ambiguity.

---

#### WARN-R8-1: Mode name inconsistency — `"inverted_naming"` vs `"inverted"` across documents

**What was found:**

Star-lord's R8 pipeline design doc (§ SL-2) defines two sub-modes:
- `"inverted_naming"` — Phase B naming retained, coalesced vocabulary as context
- `"inverted_no_naming"` — Phase B naming replaced by template-from-vocabulary

But the `generation_mode` column values defined in § SL-4 (and echoed in the LLM MIGRATION.md) use `"inverted"` (not `"inverted_naming"`) for the first sub-mode:
- `"inverted"` — `_coalesce_seasonal_theme()` ran; Phase B naming uses coalesced vocabulary
- `"inverted_no_naming"` — same as inverted but Phase B naming template-derived

The LLM MIGRATION.md also uses `generation_mode="inverted"` in the example code and `set_context(generation_mode="inverted")` in the `TrackedLLMClient` change. The R8 smoke Smoke 1 checks `llm_calls.generation_mode = "inverted"`.

So: design concept is called `"inverted_naming"` in the sub-mode description, but the telemetry column value is `"inverted"`. This is a Discipline #13a drift instance — the design label and the implementation constant differ, and implementers reading both sections will author inconsistent code.

Additionally, the knight-rider coordination decision (hive log, 0b51312) routes the two-mode finding and refers to the modes as `inverted` and `inverted_no_naming` — matching the telemetry values, not the design-concept names.

**Required action (star-lord):** in the R8 pipeline design doc § SL-2, rename the sub-mode from `"inverted_naming"` to `"inverted"` to match the telemetry column value and the knight-rider routing decision. This is a documentation consistency fix; no implementation change needed since the telemetry column value is already `"inverted"`.

**Cite:** Discipline #13a (implementation-vs-intent naming drift); WP-MIGRATION-4 (R8 LLM MIGRATION.md cadence)

---

#### Non-blocking observations (PASS-level):

**Two-mode design support:** the star-lord section cleanly documents both modes. The cost analysis (§ SL-2) is the correct diagnosis: `inverted` alone saves ~0% on cost; `inverted_no_naming` delivers ~98% reduction. The star-lord OBSERVATION routing was correct.

**Rocket section placeholder:** rocket's pipeline section is still a placeholder. This is expected — per the hive log routing decision, rocket's pipeline implementation must accommodate both modes. The WARN-R8-1 naming fix should be incorporated when rocket authors the implementation section. Not an independent WARN because the design concept is clear from star-lord's section; the gap is in naming consistency only.

**Cost telemetry structure (§ SL-4 / SL-6):** the `generation_mode` column and pre-authored queries are correct. The `season_id`-grouped mode query and the cost-reduction percentage query are both well-formed.

**Retry / fallback for coalescence call (§ SL-3):** 3-attempt exponential backoff with null_theme fallback is sound. The null_theme fallback path is exercised by `--no-coalesce` smoke already — good design reuse.

**Pattern P7 for `--no-coalesce` (§ SL-6 Smoke 3):** the smoke explicitly checks that theme fields are NULL/absent under `--no-coalesce`, not silently filled. WP-R8-A-4 is satisfied in spec. No silent default.

**Discipline #14 (canonical-four leakage in orchestration code):** the `set_context(generation_mode=...)` path and the LLM MIGRATION.md changes contain no canonical-four element labels as structural keys. No Discipline #14 violation in the orchestration design.

---

## Target 5 — R8 Cohesion-Judging Protocol (WP-R8-A-2 deferred Gate)

**File reviewed:** `agentic_orchestration/hive-mind/R8-cohesion-judging-protocol-2026-05-19.md`
**Author:** gandalf
**Companion reviewed (sanity skim):** `R8-theme-coalescence-prompt-2026-05-19.md`

### Verdict: PASS

Scale anchoring is durable, LLM-judge prompt is blind to pipeline identity, disposition decision-tree is deterministic, 6-facet structure is independent and equally weighted. WP-R8-A-2 is satisfied.

---

#### PASS rationale:

**Anchor durability (§ 1.1):**

- Cohesion-5 anchor: `season_002017` (necropolis). Specific enough; the slot-fill examples are named and quoted; the "read-aloud test" is a clean operational criterion.
- Cohesion-4 anchors: `season_002013` (dwarves' empty halls) and `season_002015` (mad king). Two anchors for cohesion-4 is stronger than one — inter-season variation at the same cohesion level is documented (002015's "Gauntlet Strike" drift is named). This helps judges recognize that cohesion-4 is not a single template.
- The cohesion-3, -2, -1 are hypothetical examples, not anchored to real seasons. This is appropriate — the protocol explicitly notes anchors to real seasons are for calibration at the high end, not across every scale point. The hypothetical examples are well-constructed (the "Mountain Pass" example correctly articulates the templated-but-not-authored failure mode).
- Anchors reference files in `output/` (cosmological_vocabulary.json) — these are stable artifacts from the engine, not in-flight content. Durability holds.

**Blindness (§ 3.1 + § 4):**

The judging protocol explicitly requires shuffle before gandalf scores (§ 3.1 step 1). Gandalf sees season IDs only after scoring is complete. The LLM-judge prompt (§ 4) contains no mention of "inverted" or "baseline" in the system or user prompt. The LLM sees anchor, slot fills, pair rationales, and sampled content — no pipeline-identity information. Blindness requirement met.

**Disposition decision-tree (§ 5.4):**

The decision tree is deterministic and complete. Every path terminates at A, B, or C. No ambiguous mid-range state exists without an explicit outcome (the Test 5 borderline at 0.55-0.70 maps to DISPOSITION C explicitly). The "Matt-deferred secondary trigger" (§ 3.2) is well-bounded: invoked ONLY if inverted mean is within 0.4-0.6 of baseline AND wind-down not called AND gandalf judges it material. This is appropriately constrained.

**6-facet structure (§ 2):**

Each facet is independently scorable:
- F1 (Anchor coherence) — assessed from anchor name alone
- F2 (Slot-fill register unity) — assessed from the 8 slot fills without reference to downstream content
- F3 (Anchor-to-slot-fill extension) — requires anchor + slot fills together, but is distinct from F2 (unity vs extension are different questions)
- F4 (Element-anchor-mechanic fit) — assessed from dominant_element + anchor + season_theme_element
- F5 (Pair rationale articulation) — assessed from pair_rationales alone
- F6 (Cross-content consistency) — assessed from the 22-name sample

Equal weighting (1/6 each) is appropriate. None of the six facets subsumes another. The F6 sampling discipline (§ 2.1) is specific enough to be reproducible.

**Dry-run validation (§ 7):**

The pre-A/B-run dry-run on season_002017 is an excellent calibration gate. If human + LLM judge diverge on the cohesion-5 anchor reference (scoring it < 4.0), the protocol self-revises before the A/B run contaminates the data. This is Discipline #1 (methodology-before-execution) applied correctly.

**`inverted_no_naming` arm (knight-rider coordination, hive log 0b51312):**

The protocol was authored before knight-rider's two-mode routing decision. It currently covers `inverted` and `baseline`. The knight-rider decision routes gandalf to author an addendum for the `inverted_no_naming` arm. This addendum is not yet present — which is expected (it was not yet dispatched at authoring time). This is a known open item per the knight-rider HANDOFF, not a review finding. Gandalf should append § 10 or similar when the addendum dispatch fires.

**Discipline #14 check on coalescence prompt (WP-R8-A-1 + WP-D14-1):**

The theme-coalescence prompt (R8-theme-coalescence-prompt-2026-05-19.md) was first-pass cleared. Sanity skim confirms: the system prompt instructs the LLM to read `dominant_element` from the data (input-driven discovery), not to use canonical-four labels as structural keys. The LLM-judge prompt (§ 4.1) likewise uses no canonical-four structural labels. WP-D14-1 remains satisfied.

---

## Summary gate table

| Target | Verdict | WARNs | BLOCKs | Gate fires? |
|---|---|---|---|---|
| R3 Schema Design Coherence | WARN | 2 | 0 | Conditional — after WARN-R3-1 and WARN-R3-2 addressed |
| R7 Parity Test Spec | WARN | 1 | 0 | Conditional — after WARN-R7-1 addressed |
| R7 Consumer Audit | PASS | 0 | 0 | YES |
| R8 LLM Orchestration Design | WARN | 1 | 0 | Conditional — after WARN-R8-1 addressed |
| R8 Cohesion-Judging Protocol | PASS | 0 | 0 | YES |

---

## Tag implications

**`hive-rebuild/v0.4-r3-schema-draft-committed`:** CONDITIONAL HOLD. This tag fires after R3 schema design review PASS. Current verdict is WARN (not BLOCK). The WARNs are documentation-consistency fixes (archetype vocabulary reconciliation + range_m minimum clarification). Tag should fire once rocket + elrond reconcile WARN-R3-1 and rocket clarifies WARN-R3-2 in MIGRATION.md. Estimated effort: one focused authoring session.

**R7 implementation phase:** CONDITIONAL HOLD. Waits on WARN-R7-1 (DemoAgentMock `.get()` fix in R7 spec). The fix is a single-pass edit to the spec before harness implementation begins. Non-blocking to R3 work continuing in parallel.

**R8 implementation phase:** CONDITIONAL HOLD. Waits on WARN-R8-1 (mode name consistency fix in R8 pipeline doc). Single-pass edit. Non-blocking to R3 and R7 work.

All three WARNs are addressable in pre-implementation authoring sessions without architectural revision.

---

## Watchpoints updated

**WP-R3-A-1 (schema field naming drift):** PARTIALLY SATISFIED. Field names are consistent for the 7 new fields. But archetype vocabulary used in derivation tables is inconsistent between rocket and elrond sections — new WARN-R3-1. Status: OPEN (upgraded to WARN-R3-1).

**WP-R3-A-2 (MIGRATION.md concurrent authoring):** CLOSED. Both generation and export MIGRATION.md carry concurrent R3 entries. ADR-004 gate honored.

**WP-R7-A-1 (parity-test spec before harness):** CLOSED in spec. Harness implementation is gated; spec exists and is reviewed. WARN-R7-1 is a spec fix, not a missing spec.

**WP-R7-A-2 (consumer audit enumeration):** CLOSED. Both known sites (movement.ts:74-78, movement.ts:81) are named.

**WP-R7-A-3 (Test 2 intentional-break required):** CLOSED in spec. `test_intentional_break_fails_loud()` is explicitly included.

**WP-R8-A-2 (cohesion scale anchoring):** CLOSED. Gate 1 PASS on cohesion-judging protocol.

**WP-R8-A-3 (Discipline #14 for coalescence prompt):** CLOSED (sanity skim confirms; first-pass clear stands).

**WP-MIGRATION-1 (R3 generation MIGRATION.md):** CLOSED. All 7 fields present.

**WP-MIGRATION-2 (R3 export MIGRATION.md):** CLOSED. Additive-only decision documented; consumer obligations stated.

**WP-MIGRATION-4 (R8 LLM MIGRATION.md):** WARN — mode naming inconsistency surfaces here (WARN-R8-1).

---

## Action table

| Action | Owner | Priority | Non-blocking to whom |
|---|---|---|---|
| WARN-R3-1: Reconcile archetype vocabulary (swarmer/controller/sniper vs ranger/bruiser/skirmisher) in §§ R-2.1, R-2.5 derivation tables | rocket (L1) + elrond (coordination) | Before `v0.4` tag | Elrond backfill can begin with elrond's vocabulary; blocks rocket implementation alignment |
| WARN-R3-2: Clarify `range_m` minimum in generation MIGRATION.md (0.5 floor vs role-cross-check) | rocket | Before `v0.4` tag | Low effort — MIGRATION.md edit only |
| WARN-R7-1: Replace `.get()` with direct key access in DemoAgentMock `__init__()` | star-lord | Before R7 harness implementation | Non-blocking to R3 |
| WARN-R8-1: Rename `"inverted_naming"` to `"inverted"` in R8 pipeline design doc § SL-2 | star-lord | Before R8 implementation | Non-blocking to R3, R7 |
| OBS-R7-audit-1: Rocket appends CombatantState construction section to R7 consumer audit | rocket | Next implementation session | Non-blocking to all others |
| Gandalf: Append `inverted_no_naming` arm addendum to R8 cohesion-judging protocol | gandalf | Before A/B run | Non-blocking until A/B run fires |

---

*Authored 2026-05-19 by jack-ryan under autonomous-operation authority. Five Gate 1 targets reviewed: 2 PASS, 3 WARN. Zero BLOCKs. All WARNs are pre-implementation documentation consistency fixes; no architectural revision required. The design is sound — these are seam-naming and internal-consistency catches. The disciplines are holding.*
