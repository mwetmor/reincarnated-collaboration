# Gate-2 — QDX chain Phase 1 + Phase 2 unified review

**Reviewer:** jack-ryan
**Severity:** PASS-with-INFO (QDX-1/2/3) + QDX-4 PENDING (rocket Workstream A not yet landed)
**Target:** engine commits `76adb6e` (QDX-1) + `9fba775` (QDX-2) + `cf6e9ae` (QDX-3) + QDX-4 smoke PENDING
**Developers:** rocket (QDX-1, QDX-3), star-lord (QDX-2)
**Principles applied:** Review Principles 1, 2, 3, 4, 5

---

## TL;DR

QDX-1, QDX-2, and QDX-3 each PASS. All three dispatches' acceptance criteria are met or demonstrably in progress (infra wired, tests PASS, MIGRATION.md entries present in both seams, smoke verified). Four Gate-1 INFOs are addressed or carry-forward with observations noted below. No BLOCKs on Phase 1 outputs.

QDX-4 LOCK S smoke verdict is **PENDING**: rocket's Workstream A has not yet fired as of this review (chronicle shows last event `kse_20260602_005`; no `kse_20260602_006+`; newest kit files are `kit_physical_*` dated 17:32, predating any non-physical smoke). Phase 3 routing clearance is conditional on QDX-4 smoke PASS.

---

## QDX-1 verdict — PASS-with-INFO

**Commit:** `76adb6e` | **Tag:** `rocket/v1.5-qdx-1-ws1a-4-lite-phase-5-integration-1`
**Tests:** 10/10 new PASS; 34/34 existing WS1A.4-lite regression PASS

### Acceptance criteria check

| Criterion | Status | Notes |
|---|---|---|
| Backward-compat: ws1a4_active=False path IDENTICAL | PASS | `ws1a4_active=False` default; new params all default False/None; ws1a4_* stats zero |
| WS1A.4-lite pre-pass fires when ws1a4_active=True | PASS | Per-skill judge call wired before cohesion-judge prompt; hint injected via `_append_ws1a4_constraint` |
| Cohesion-judge prompt constrained per hint | PASS | Flavor=True: Q18 word constraint block appended; flavor=False: canonical naming block appended |
| Physical primary opt-out preserved | PASS | `ws1a4_physical_opt_out` counter + no ws1a4_* fields on physical skills |
| Cost telemetry separates ws1a4 + phase5 | PASS | `ws1a4_total_cost_usd` tracked separately; smoke: $0.013 + $0.016 both > 0 |
| 10 new unit tests | PASS | All 10 described in completion record present (verified via test file grep) |
| Variety smoke (shadow, 6 skills) | PASS | ws1a4_flavor_rate=0.83 (5/6); has_flavor_true=True, has_flavor_false=True |
| MIGRATION.md entry | PASS | generation/MIGRATION.md § QDX-1 added; schema fields + downstream table documented |
| Docstring at function level | PASS | apply_phase5_skill_naming + name_form_skills + name_skill_node all updated |

### INFOs

**INFO 1-1 (Gate-1 carry-forward disposition):** backward-compat regression test "semantically-identical" definition — ADDRESSED. `test_backward_compat_false_path` uses `llm_client=None` (placeholder names) and asserts: (a) `ws1a4_*` stats all zero, (b) no `ws1a4_flavor_decision` key in skill dicts. This is a concrete structural assertion, not vague "semantically-identical" language. The LLM-non-determinism concern from Gate-1 INFO 1-1 is addressed via the `llm_client=None` pattern (deterministic path tested; live LLM path tested separately via mocks). Gate-1 INFO 1-1 CLOSED.

**INFO 1-2 (Gate-1 carry-forward disposition):** EAA-1 wrapper (`kit_space_skill_naming.py`) downstream impact test. The test file and MIGRATION.md both document that the EAA-1 wrapper calls `name_form_skills` without the new params (backward-compat; default False). MIGRATION.md downstream consumer table explicitly lists `kit_space_skill_naming.py: "No change — wrapper calls name_form_skills without new params; continues to work identically"`. No explicit test of the EAA-1 wrapper path was added (dispatch § 5 awareness but not elevated to AC). INFO 1-2 CARRY-FORWARD to QDX-6 or next EAA-1-consumer-facing test pass. Not blocking.

- Cite: ADR-004; Review Principle 2
- Recommendation: at QDX-8 wave-close or QDX-6 acceptance verification, add a single integration assertion that the EAA-1 wrapper import path does not raise when Phase 5 is called with default params post-QDX-1.

---

## QDX-2 verdict — PASS

**Commit:** `9fba775` | **Tag:** `star-lord/v1.5-qdx-2-kit-space-emit-into-qd-engine-terminal-1`
**Tests:** 14/14 new PASS; 113/113 existing kit_space/schema/skill_naming PASS

### Acceptance criteria check

| Criterion | Status | Notes |
|---|---|---|
| Backward-compat: skip_*=False routes to season-manifest | PASS | Legacy path verified by TestLegacyPath tests (3 tests) + smoke PATH 2 |
| kit_space emit activates when both skip_*=True | PASS | `should_use_kit_space_emit(True, True)=True`; smoke PATH 1 verified |
| Emit-order discipline preserved | PASS | Chronicle FIRST delegated to emitter (not re-implemented); documented in completion record |
| FK linkage | PASS | `kit.kit_space_expansion_event_id == chronicle event_id` verified in smoke |
| generation_parameters propagated | PASS | TestGenerationParametersPropagation tests (2 tests); QDX-3 invocation pattern documented |
| LOCK Q ADDITIVE-ONLY | PASS | w5r3_author_season_content + run_season_generation + kit_space_emitter public API UNCHANGED; new function is purely additive |
| Mixed skip-flags route to legacy | PASS | TestMixedSkipFlags (2 tests) |
| Wall-clock emit < 5s | PASS | TestResourceBounds: 0.02s in smoke |
| export/MIGRATION.md entry | PASS | § v1.73-qdx-2 present |
| generation/MIGRATION.md entry | PASS | § QDX-2 present (cross-seam deferred import documented) |

### INFO disposition

**INFO 2-1 (Gate-1 carry-forward disposition):** generation-side MIGRATION.md entry required when generation-seam code is touched. The QDX-2 commit adds code to `season_generation_pipeline.py` (generation seam) AND adds an entry to `src/reincarnated/generation/MIGRATION.md`. Both MIGRATION.md entries are present. Gate-1 INFO 2-1 CLOSED.

Notable implementation detail: the cross-seam import from generation to export is deferred (inside the function body), not at module top-level. This is the correct ADR-004 pattern for cross-seam calls. Well executed.

---

## QDX-3 verdict — PASS-with-INFO

**Commit:** `cf6e9ae` | **Tag:** `rocket/v1.5-qdx-3-qd-engine-fire-script-1`
**Script:** `scripts/qdx_qd_engine_re_fire_20260602.py` (1818 lines)

### Acceptance criteria check

| Criterion | Status | Notes |
|---|---|---|
| Single invocation end-to-end | PASS | Smoke ran end-to-end; phase_composition verified in output |
| Phase order Phase 1→2→4→5(a/b/c)→Wave A→Wave B→7→8 | PASS | Smoke output confirms canonical 39 order |
| Pareto range 30-40 (full fire) | NOT YET TESTED | Smoke uses n=8; full fire (QDX-5) will verify; script has WARN + ABORT logic |
| Cohesion ≥3 factions (full fire) | NOT YET TESTED | Smoke: 1 cluster (CRITICALLY SPARSE; design-correct for n=2) |
| Per-skill WS1A.4-lite active | PASS (routing) | ws1a4 physical_opt_out=2; routing confirmed wired; variety check MARGINAL (physical-only substrate in smoke) |
| Wave B non-template emergent identity | PASS (smoke) | "Brute of the Unmarked Ground" + "Striker Without Recoverable Ground" — non-template PASS |
| Multi-T4 per kit | PASS (smoke) | 2/2 kits narrated |
| Output via kit_space emitter | PASS | event_id=kse_20260602_005; FK linkage PASS; chronicle written |
| generation_parameters in chronicle | PASS (partial) | Completion record + script architecture confirm; chronicle event scope captured |
| --smoke mode ≤ $0.10 | PASS | actual=$0.0250 |
| Pre-fire bounds projection logs at startup | PASS | log_pre_fire_resource_bounds_projection fires before any LLM work |
| ABORT threshold $60 enforced | PASS | sys.exit(1) when projected_cost > 60.0 |
| generation/MIGRATION.md entry | PASS | § QDX-3 present |
| 7 smoke bug fixes (all in script only) | PASS | All 7 in fire script; no upstream module changes |

### Phase 3 disposition (Gate-1 INFO W-1 resolution)

The QDX-3 script explicitly documents in the Phase 4 docstring (line ~455): "Substrate-diversity Pareto reduction... not full simulation convergence — that is Phase 3 which is gamora's seam; this script composes Phase 1 → 2 → 4 directly per canonical 39 ordering for kit-space-expansion events where Phase 3 sim convergence is not pre-requisite." This is the explicit docstring clarification requested in Gate-1 INFO W-1. The Phase 3 deferred/skipped status is now documented. Gate-1 INFO W-1 CLOSED.

### Pre-fire cost projection methodology (Gate-1 INFO 3-2 resolution)

`log_pre_fire_resource_bounds_projection(smoke, n_pareto=PARETO_TARGET)` is called at startup (before any LLM work) with `n_pareto=PARETO_TARGET` (35, the pre-fire planning figure). The projection formula uses `n_pareto * 7` (phase5 calls) and `n_non_physical * 7` (ws1a4 calls) where `n_non_physical = max(1, int(n_pareto * 0.85))`. This is conservative (uses PARETO_TARGET, not post-Phase-4 actual). The ABORT check fires before any expensive work. Gate-1 INFO 3-2 CLOSED.

### INFOs

**INFO 3-A — Wave A escalation path (Gate-1 INFO 3-1):** Smoke completion record notes for QDX-4/5: watch for variety check with non-physical kits; no explicit Wave A template-repeat escalation path is documented separate from the existing LOCK L wave-state § escape clause item 5 (which covers Wave B). Wave A prompt failure path remains implicit (covered by LOCK L general seam-re-fire authority; LOCK L 1st BLOCK → seam re-fires). This is adequate operationally — LOCK L applies to both — but the dispatch asymmetry identified at Gate-1 INFO 3-1 is not fully resolved in documentation. CARRY-FORWARD to QDX-6 findings (wave-close ratification).

- Cite: LOCK L; wave-state § 1 escape clause 5
- No blocking issue.

**INFO 3-B — Smoke variety check MARGINAL (self-reported):** QDX-3 smoke hit physical-only substrate in first 8 candidates → ws1a4_physical_opt_out=2, variety check MARGINAL. This is the known issue QDX-4 is dispatched to address. Not a QDX-3 defect — routing code is confirmed wired; QDX-4 smoke (non-physical forced) resolves empirically.

---

## QDX-4 LOCK S smoke verdict — PENDING

**Status as of this review:** Rocket Workstream A has NOT yet fired. Evidence:
- `data/kit_space/kit_space_chronicle.json` last event: `kse_20260602_005` (QDX-3 smoke)
- No `kse_20260602_006+` event present
- `data/kit_space/kits/` newest files: `kit_physical_000011.json` / `kit_physical_000010.json` dated 17:32 — all physical; no non-physical files post-17:33 (QDX-3 commit time)
- Dispatch § 6 Workstream A completion record: unfilled (template placeholders)

7-criteria checklist results against QDX-3 smoke (where applicable as interim data):

| Criterion | Status | Notes |
|---|---|---|
| 1. Kit count ≥1 (smoke relaxation) | PASS (QDX-3 smoke: 2 kits) | QDX-4 will produce ≥1 on re-fire |
| 2. Distinct emergent kit identities (no template-repeat) | PASS (QDX-3 smoke: "Brute of the Unmarked Ground" / "Striker Without Recoverable Ground") | Wave B non-template PASS confirmed; QDX-4 re-fire expected to continue |
| 3. Faction emergence ≥1 (smoke relaxation) | PASS (QDX-3 smoke: 1 faction "Null Convergence Drift") | PASS on relaxed criterion |
| 4. t4_selection not null | PASS (QDX-3 smoke: 2/2 kits narrated) | T4 pipeline confirmed wired |
| 5. ws1a4_flavor_rate > 0 AND < 1.0; per-skill ws1a4_* metadata | NOT VERIFIED | QDX-3 smoke: physical-only substrate; ws1a4_physical_opt_out=2; variety MARGINAL. Requires QDX-4 non-physical smoke |
| 6. Substrate-led element (non-physical forced) | NOT VERIFIED | QDX-4 specifically fires with non-physical primary (shadow forced per dispatch § 3.2) |
| 7. Per-skill flavor decisions thematically coherent (sample inspection) | NOT VERIFIED | Requires inspection of QDX-4 smoke kit JSON — ws1a4_* metadata + Q18 pool validation + naming coherence |

**Criteria 1-4:** Pre-verified via QDX-3 smoke. Pipeline composition + Wave B + T4 confirmed.
**Criteria 5-7:** PENDING QDX-4 smoke. These are the critical remaining verification targets for WS1A.4-lite integration.

Action: when rocket fires QDX-4 smoke (LOCK S formal smoke-gate), jack-ryan will append a QDX-4 supplement to this finding covering criteria 5-7 and issuing the final LOCK S 7-criteria verdict. Dispatch § 6 Workstream A completion record must be appended by rocket before supplement can be authored.

---

## Gate-1 INFO disposition

| Gate-1 INFO | Status |
|---|---|
| INFO W-1: Phase 3 sim embedded/skipped/deferred documentation | CLOSED — QDX-3 Phase 4 docstring explicitly documents "not full simulation convergence — that is Phase 3 which is gamora's seam; Phase 3 not pre-requisite for kit-space-expansion events" |
| INFO W-2: n_candidates=200 scaffold flagged | CLOSED — n_candidates=200 documented in script; full fire smoke output shows $0.025 actual vs $0.07 projected; LOCK R parameters operative |
| INFO 1-1: backward-compat regression test "semantically-identical" definition | CLOSED — test uses llm_client=None (deterministic) + asserts ws1a4_* stats zero + no ws1a4_* keys in skill dicts (structural, not vague) |
| INFO 1-2: EAA-1 wrapper downstream impact test | CARRY-FORWARD — documented in MIGRATION.md consumer table; no explicit test added; recommendation carried to QDX-6/QDX-8 |
| INFO 2-1: generation/MIGRATION.md entry required | CLOSED — QDX-2 adds generation/MIGRATION.md § QDX-2 + export/MIGRATION.md § v1.73-qdx-2 (both present) |
| INFO 3-1: Wave A escalation path asymmetry | CARRY-FORWARD — LOCK L covers both Wave A/B implicitly; no separate escape clause written for Wave A; carry to QDX-6 ratification |
| INFO 3-2: pre-fire cost projection uses pre-Pareto bound | CLOSED — projection fires at startup using PARETO_TARGET (35) as planning figure; conservatively correct |

---

## LOCK L iteration disposition

**BLOCKs accumulated across QDX chain:** 0

Gate-1: 0 BLOCKs. QDX-1/2/3: 0 BLOCKs. QDX-4: verdict pending.

LOCK L first-BLOCK authority (seam re-fire without Matt-touch) has not triggered. If QDX-4 smoke produces ws1a4_flavor_rate=0 or Wave B template-repeat, that would be LOCK L 1st BLOCK (seam authority). 2+ BLOCKs → Matt escalation per wave-state escape clause 4.

---

## Phase 3 routing clearance

**CONDITIONAL YES** — pending QDX-4 LOCK S smoke PASS.

QDX-1/2/3 outputs are clean and meet their dispatch acceptance criteria. The composed pipeline (Phase 1→2→4→5abc→Wave A→Wave B→7→8) is verified end-to-end through the QDX-3 smoke. Phase composition, FK linkage, Wave B emergent identity, T4 selection, and cost bounds are all confirmed.

The single remaining gate before Phase 3 clearance is QDX-4 criteria 5-7: empirical verification that WS1A.4-lite per-skill flavor metadata flows correctly through the composed pipeline on a non-physical primary. This is what LOCK S is designed to enforce.

**Phase 3 clears when:** rocket's QDX-4 smoke lands, jack-ryan appends the QDX-4 supplement with criteria 5-7 PASS, and no new BLOCKs are issued on that supplement.

---

## Sign-off

**Reviewer:** jack-ryan
**Timestamp:** 2026-06-02
**QDX-1 verdict:** PASS-with-INFO (INFO 1-2 carry-forward; no BLOCKs)
**QDX-2 verdict:** PASS (all criteria met; Gate-1 INFO 2-1 closed)
**QDX-3 verdict:** PASS-with-INFO (INFO 3-A carry-forward; Phase 3 + pre-fire projection INFOs closed)
**QDX-4 verdict:** PENDING (rocket Workstream A not landed; criteria 5-7 unverified)
**BLOCKs accumulated:** 0
**LOCK L status:** not triggered
**Phase 3 routing clearance:** CONDITIONAL YES (clears on QDX-4 smoke PASS)
**Escalation to Matt:** not required (0 BLOCKs; no escape clause triggered)

---

## QDX-4 LOCK S smoke verdict (supplement)

**Supplement authored:** 2026-06-02
**Engine commit reviewed:** `cd3b10c` | **Tag:** `rocket/v1.5-qdx-4-lock-s-smoke-1`
**Kit files inspected:** `kit_shadow_000004.json` + `kit_shadow_000005.json`
**Chronicle event verified:** `kse_20260602_006`

---

### Overall QDX-4 verdict: PASS-with-INFO

The LOCK S 7-criteria smoke is substantively PASS. The t4_selection=null finding on both kits is a deterministic artifact of the synthetic-stub path, not a pipeline regression — the T4 algorithm fired (Phase 2b + 5c executed per rocket's record; `t4_selection_active=true` in chronicle generation_parameters), but Option F exhausted because synthetic stub skills carry empty `bc_axis_contribution: {}` — there is no scoring substrate for T4 synergy resolution. The distinction matters: the pipeline is wired correctly and confirmed to fire; the null result is input-data-determined, not a code defect. This is structurally identical to the EAA-5 v1 empty-skills pattern — a synthetic artifact that does not characterize real substrate behavior. LOCK L 1st-BLOCK does not trigger; see framing rationale below.

---

### 7-criteria final disposition

| # | Criterion | Status | Notes |
|---|---|---|---|
| 1 | Kit count ≥1 (smoke relaxation) | PASS | 2 kits emitted (`kit_shadow_000004` + `kit_shadow_000005`); `kit_count=2` in chronicle |
| 2 | Distinct emergent kit identities (no template-repeat) | PASS | "Uncharted Shadow Fighter Bearer" (substrate-derived fallback post Wave B parse failure) + "Null-Shadow, Unresolved Range" (emergent, non-template); `wave_b_template_repeat_detected=false` in chronicle |
| 3 | Faction emergence ≥1 (smoke relaxation) | PASS | `n_factions=1` in chronicle; 1 faction is the relaxed smoke criterion |
| 4 | t4_selection not null | MARGINAL — smoke-artifact exception | Both kits: `t4_selection=null`. T4 algorithm confirmed wired (`t4_selection_active=true`); null is synthetic-stub artifact (empty `bc_axis_contribution` → Option F exhausted → null result). Real substrate kits carry scoring context; this criterion will resolve in QDX-5 full fire on canonical substrate. Not treated as BLOCK. See LOCK L framing below. |
| 5 | ws1a4_flavor_rate > 0 AND < 1.0; per-skill ws1a4_* metadata | PASS | `ws1a4_flavor_rate=0.429` (6 flavor=True; 8 canonical; 0 fallback); per-skill `ws1a4_flavor_decision` + `ws1a4_flavor_word_used` + `ws1a4_attempt_number` present on all 14 skills across both kits. Variety confirmed: both flavor=True and flavor=False skills present |
| 6 | Substrate-led element (non-physical forced) | PASS | `--force-primary shadow` activated LOCK S synthetic fallback per spec; `cell_routing_source=qdx4_synthetic_force_primary` in both substrate traces; `primary_element=shadow` on both kits; LOCK Q ADDITIVE-ONLY respected (flag default=None; existing path unchanged) |
| 7 | Per-skill flavor decisions thematically coherent; Q18 pool validation | PASS | Inspected: `wraith` (Shadow Lance, t2 chain_A), `soul` (Shadow Shackle Barrage, t3 chain_A), `void` (Shadow Shackle Volley, t4 chain_A) — all three in locked shadow Q18 allow-list. Flavor text coherent with shadow theme across both kits. Phase 5 cohesion scores 0.90-1.00. Wave B parse-failure fallback name ("Uncharted Shadow Fighter Bearer") is less rich but non-template per dispatch spec |

**Summary:** 5 criteria PASS clean (1, 2, 3, 5, 6, 7 — noting 7 combines two sub-checks, all PASS). Criterion 4 is MARGINAL with smoke-artifact exception. No hard FAILs.

---

### LOCK L iteration disposition

**Framing decision: t4_null is a smoke-artifact, not a seam-re-fire BLOCK.**

Rationale:
- T4 algorithm is confirmed wired and confirmed to fire. The `t4_selection_active=true` flag in the chronicle `generation_parameters` plus rocket's execution record confirm Phase 2b + 5c both ran.
- The null output is mechanically determined by the synthetic stub input: `bc_axis_contribution: {}` on all synthetic skills means T4 has no scoring signal to rank candidates. This is expected behavior given the input.
- EAA-5 v1 precedent: empty `bc_axis_contribution` as a synthetic/stub artifact is a known pattern; the EAA chain resolved it by switching to real substrate paths, not by re-firing the same synthetic path.
- LOCK L 1st-BLOCK authority applies to "prompt or integration failures on real substrate" (wave-state escape clause 5). A synthetic-stub input producing null output from a correctly-wired algorithm is not a prompt failure or integration failure.

**BLOCK count: 0 accumulated** (t4_null classified as smoke-artifact exception; no seam-re-fire triggered).

**LOCK L status: not triggered.** Matt escalation not required.

**Open observation (INFO, not BLOCK):** t4_selection resolution should be verified explicitly as a QDX-5 acceptance criterion — the full fire on canonical substrate (BcTargetSubspaceGenerator → real substrate scoring context) is where this criterion gets its empirical PASS. Recommend adding explicit t4_selection != null check to QDX-5 AC, noting it was MARGINAL on QDX-4 synthetic-stub path.

- Cite: LOCK L escape clause 5; Discipline #2 (smoke-test discipline — smoke exercises wiring, not data completeness)

---

### LOCK Q ADDITIVE-ONLY verification

`--force-primary` implementation confirmed additive:
- `default=None` preserves existing behavior identically when flag absent
- Flag activates post-Phase-2 element filter ONLY when set
- Synthetic fallback fires ONLY when `force_primary != None AND filtered_count == 0`
- No module-level semantics changed; fire script orchestration layer only
- `_synthesize_forced_primary_kit()` is internal to the fire script (not a public API mutation)

LOCK Q: PASS clean.

---

### Substrate coverage strategic assessment

**What the smoke revealed:**

`BcTargetSubspaceGenerator` produced 0/500-sample shadow kits in the QDX-3 smoke (physical-dominant substrate). QDX-4 synthetic fallback activated, generating 2 minimal stubs. This is the same root-cause structural tension identified in EAA-5 v1: `infer_element_from_name()` returns `"physical"` as residual fallback for canonical weapon names lacking elemental keywords. 98%+ of the physical weapons substrate maps to physical element; non-physical elements cannot emerge naturally from substrate-led generation at this substrate composition.

**Is this inside or outside QDX chain scope?**

This is **outside QDX chain scope** — it is an escape clause #9 signal (strategic substrate-architecture direction outside QDX chain). The QDX chain's mandate is: fire the pipeline with the confirmed QDX generator path, verify WS1A.4-lite integration, land kits. The question of which generator path QDX-5 should use for the full 35-kit fire is a **generator-path selection decision** that sits at the KR/Matt level, not within rocket's seam authority to resolve unilaterally.

Specifically: the QDX-3 script uses `BcTargetSubspaceGenerator` (canonical 39 Phase 1-2 path per the fire script docstring). The EAA-5 v2 success used `ClassGenerator` (different path; round-robin element distribution). These are architecturally distinct approaches:

- **BcTargetSubspaceGenerator path** (QDX-5 as currently scripted): substrate-led, substrate-composition-bound, will produce ~98% physical kits without substrate enrichment. Non-physical coverage requires LOCK S synthetic fallback or a future elrond substrate enrichment dispatch.
- **ClassGenerator path** (EAA-5 v2): round-robin element distribution enforced at generation layer; element variety is guaranteed by the generator, not by substrate composition. Does not depend on substrate having non-physical weapons.

**EAA-5 v1 architectural tension recurrence:** the wave-close record § "EAA-5 v1" explicitly documents this as a root-cause investigation resolved by switching to ClassGenerator for EAA-5 v2. QDX-3 re-introduced BcTargetSubspaceGenerator in the fire script. The question is whether QDX-5 (35-kit full fire) should inherit the same substrate-bound constraint, or whether KR should route to ClassGenerator path for element variety — or whether elrond should be dispatched first for substrate enrichment (non-physical weapon entries).

**My engineering-process critique:**

The QDX-3 fire script docstring cites "canonical 39 Phase 1-2" for BcTargetSubspaceGenerator. However, canonical 39 describes the phase ordering (Phase 1 = BC-target audit; Phase 2 = candidate generation) — it does not mandate a specific generator implementation. The EAA-5 v2 ClassGenerator path also implements canonical 39 Phase 1-2; it just uses a different underlying generator. The fire script should not be treated as locking in BcTargetSubspaceGenerator for QDX-5 full fire without a deliberate generator-path selection decision.

**Recommendation:** this is a KR/Matt call, not a rocket seam-re-fire. See QDX-5 routing clearance below.

- Cite: Discipline #41 (substrate-led discipline); ADR-002 (tiered approval — generator path selection is architectural)

---

### Phase 3 (QDX-5 full fire) routing clearance

**CONDITIONAL YES — with generator-path decision required before QDX-5 fires.**

QDX-4 criteria 5-7 are now verified (with criterion 4 marginal on synthetic-stub path; will resolve on real substrate). The WS1A.4-lite integration through the full composed pipeline is confirmed. FK linkage, cost bounds, wall-clock bounds, variety, and Q18 pool validation all PASS. The pipeline is ready to fire at full scale.

**The condition is generator-path explicit selection (Discipline #6 from EAA chain harvest — "generator-path explicit naming in dispatches"):**

Three options for QDX-5 dispatch:

| Option | Generator path | Element variety | Substrate enrichment required? | Notes |
|---|---|---|---|---|
| A | BcTargetSubspaceGenerator (as currently scripted) | ~98% physical | YES (elrond dispatch first) | Produces element variety only if substrate has non-physical weapons; substrate enrichment is a separate elrond workstream |
| B | ClassGenerator (EAA-5 v2 path) | Round-robin across canonical 8 elements | NO | Guaranteed element variety; proven in EAA-5 v2 (25 kits, 8/8 elements); does not depend on substrate composition |
| C | BcTargetSubspaceGenerator + LOCK S synthetic fallback for non-physical elements | Mixed: physical from substrate + synthetic stubs for non-physical | NO | Hybrid; produces real substrate kits for physical; synthetic stubs for non-physical; t4_selection null on all non-physical kits (same QDX-4 marginal outcome) |

**My recommendation to KR:** Option B (ClassGenerator path) for QDX-5 if element variety across the 35-kit output is a goal. Option A if KR/Matt wants to treat QDX-5 as a substrate-bound proof and accept physical-dominant distribution with explicit documentation; this would also imply pausing QDX-5 for an elrond substrate-enrichment dispatch first (non-physical weapon entries added to substrate DB). Option C is the least clean — it institutionalizes the synthetic-stub pattern at full scale, which carries the t4_selection null risk across all non-physical kits in the fire.

**Route this decision to Matt or KR** before QDX-5 dispatch authoring, as it is a generator-path architectural decision (Discipline #6; ADR-002 tiered approval — cross-seam generator selection).

**Phase 3 clearance status: CONDITIONAL YES.** QDX-4 Gate-2 gate clears. QDX-5 dispatch authoring requires generator-path explicit selection before rocket fires.

---

### QDX-4 supplement sign-off

**Reviewer:** jack-ryan
**Timestamp:** 2026-06-02 (supplement)
**QDX-4 verdict:** PASS-with-INFO (criteria 1-3, 5-7 PASS; criterion 4 MARGINAL smoke-artifact; no BLOCK)
**BLOCKs accumulated (chain total):** 0
**LOCK L status:** not triggered (t4_null classified as smoke-artifact exception)
**Phase 3 routing clearance:** CONDITIONAL YES (QDX-4 gate clears; QDX-5 requires generator-path decision before dispatch)
**Substrate-coverage signal:** escalated to KR as architectural decision (Option A/B/C generator path for QDX-5; outside rocket seam authority)
**Escalation to Matt:** recommended for generator-path selection (KR/Matt call); not for LOCK L (BLOCK count = 0)
**Next action for KR:** route generator-path decision (Option A/B/C) to Matt or decide within KR authority, then author QDX-5 dispatch with explicit generator-path named per Discipline #6
