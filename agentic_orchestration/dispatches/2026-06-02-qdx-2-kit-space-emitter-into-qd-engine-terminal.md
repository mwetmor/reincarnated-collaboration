# Dispatch — 2026-06-02 — QDX-2 — kit_space_emitter wired into QD-engine workflow terminal

**From:** knight-rider (orchestrator)
**To:** star-lord (PRIMARY — export/output/telemetry seam owner) + rocket (generation seam consultant)
**Authority:** Matt 2026-06-02 QDX chain Locks A-P preserved + LOCK Q (QD-engine workflow integration authority; ADDITIVE-ONLY)
**Wave:** cycle-17 QDX QD-Engine Re-Fire — Phase 1 (parallel with QDX-1 + QDX-3)
**State file:** `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`
**Tag intent:** `star-lord/v1.5-qdx-2-kit-space-emit-into-qd-engine-terminal-<n>`
**Estimated horizon:** ~1 session

---

## 1. Authoritative reading (READ before any code work)

1. **`canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md`** § 1 Phase 8 (export; multi-profile export deferred Cycle 15+; Reincarnated v1 via existing star-lord Track C; for QDX-2 we add kit_space emit path as alternative terminal)
2. **`canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`** § 3.3-3.4 (continuous kit space; per-kit JSON entries; chronicle expansion events)
3. **`~/Games/reincarnated-engine/src/reincarnated/export/kit_space_emitter.py`** (THE module to wire in; public API `emit_kit_space_expansion_event()` + `should_use_kit_space_emit()`)
4. **`~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py`** (the QD-engine workflow Cycle 13 wave 5 lineage — verify whether this is the canonical entry point or there's a successor for QDX; either way, identify the terminal emit phase)
5. **`~/Games/reincarnated-engine/src/reincarnated/generation/season_orchestrator.py`** (EAA-2 added `skip_theme_coalescence` + `skip_cosmological_vocabulary` defaults True; QDX-2 verifies these flags compose correctly with the kit_space emit path)
6. **`~/Games/reincarnated-engine/scripts/eaa5_kit_space_first_fire_20260602.py`** (reference — EAA-5 v2 used ClassGenerator + direct call to `emit_kit_space_expansion_event()`; QDX-2 wires this composition INTO the QD-engine workflow itself so QDX-3's fire script doesn't need to bypass the workflow)
7. **`~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md`** (existing emit-pipeline MIGRATION entries; v1.72 reference for EAA-3+4 emit integration)

---

## 2. Target seam + scope

**Owner seam:** export (star-lord) with generation seam consultation (rocket)

**Target files:**
- `~/Games/reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py` (the QD-engine workflow; needs terminal-phase routing to kit_space emit when skip_* flags True) — **OR** equivalent QD-engine-workflow entry point that QDX-3 will compose against
- `~/Games/reincarnated-engine/src/reincarnated/export/kit_space_emitter.py` (NO CHANGES expected; public API already stable from EAA-3+4)
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` (new entry for terminal-phase kit_space routing)

**Scope (ADDITIVE per LOCK Q):**

The QD-engine workflow currently has a terminal phase that writes to `seasons/season_NNNNNN/` (per-season manifest path). QDX-2 adds an ALTERNATIVE terminal phase that routes the workflow's output through `emit_kit_space_expansion_event()` when `skip_theme_coalescence=True AND skip_cosmological_vocabulary=True` (Realm Expansion default; consistent with EAA-2 skip-flag pattern + EAA-3+4 emit-order discipline).

The decision is made via `should_use_kit_space_emit(skip_theme_coalescence, skip_cosmological_vocabulary)` from `kit_space_emitter.py`.

**Out of scope (CRITICAL — do NOT touch):**
- Semantic behavior of existing season-manifest emit path (any caller with `skip_*=False` MUST behave identically to current state)
- `kit_space_emitter.py` public API (already stable from EAA-3+4; QDX-2 is a CONSUMER not an author of changes)
- CHRONICLE_SCHEMA.md (already stable; QDX-2 uses the existing chronicle schema)
- Atomic-write convention (already enforced by emitter; QDX-2 doesn't need to re-implement)
- EAA-2 skip-flag default values (LOCK M Stage 1 deferred to later cleanup)

---

## 3. Acceptance criteria

### 3.1 Functional

1. **Backward compatibility verified** — when `skip_theme_coalescence=False` OR `skip_cosmological_vocabulary=False`, the QD-engine workflow terminal writes to `seasons/season_NNNNNN/` per existing season-manifest path. Add a regression smoke test that re-runs an existing season-manifest fire and asserts identical output structure (allowing for any non-determinism in the engine).

2. **Kit_space emit activates when both skip_* True** — when `skip_theme_coalescence=True AND skip_cosmological_vocabulary=True` (Realm Expansion defaults per EAA-2), the QD-engine workflow's terminal phase routes the workflow's output through `emit_kit_space_expansion_event()`. Output lands at `data/kit_space/`:
   - `kit_space_chronicle.json` appended with new event entry
   - `data/kit_space/kits/kit_<primary>_<seq6>.json` × n_kits

3. **Composition with EAA-2 skip-flags verified** — `should_use_kit_space_emit(True, True) == True` AND existing `season_orchestrator.SeasonOutput.skip_*` defaults True (per EAA-2) → kit_space emit fires automatically. No explicit emit-path argument required by callers using the Realm Expansion defaults.

4. **Emit-order discipline preserved** — per `CHRONICLE_SCHEMA.md` § 5.1: chronicle entry written FIRST; per-kit JSONs SECOND; atomic `.tmp` → `os.replace`. QDX-2 doesn't re-implement this — it routes through the emitter which already enforces.

5. **Generation parameters propagate to chronicle** — the QD-engine workflow's parameters (n_candidates, Pareto reduction target, cohesion clustering params, Wave A/B LLM call params, T4 selection params, ws1a4_active state, skip flags state) are captured in `generation_parameters` dict and passed through to `emit_kit_space_expansion_event()`. This is essential for chronicle event provenance.

### 3.2 Tests

6. **Unit tests** — at least 4 new tests covering: (a) skip_*=False path writes to seasons/season_NNNNNN/; (b) skip_*=True path writes to data/kit_space/; (c) mixed skip-flags (one True, one False) routes to legacy path (per `should_use_kit_space_emit` semantics); (d) generation_parameters dict properly composed and passed through.

7. **Smoke test** — single-kit smoke with skip_*=True; asserts kit JSON lands at `data/kit_space/kits/kit_<primary>_<seq6>.json`; asserts chronicle event appended; asserts FK linkage (kit's `kit_space_expansion_event_id` == chronicle event_id).

### 3.3 Documentation

8. **MIGRATION.md entry** — `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § new entry: "QDX-2 — kit_space_emitter wired into QD-engine workflow terminal; activates when both EAA-2 skip flags True (Realm Expansion defaults); backward-compatible with season-manifest path".

9. **Docstring at terminal-phase function level** — terminal-phase docstring documents the emit-path routing logic + composition with skip flags + emit-order discipline reference.

### 3.4 Resource bounds (Discipline #1.1)

10. **Pre-fire resource-bounds projection** — emit overhead is bounded (n_kits × per-kit JSON size; chronicle entry growth bounded by event count). Verify smoke shows wall-clock emit time < 5s for single-kit smoke.

---

## 4. Smoke-test expectation

Before tagging, run the smoke test in § 3.2 item 7. Expected smoke output (illustrative):

```
QD-engine workflow terminal phase entered.
skip_theme_coalescence=True  skip_cosmological_vocabulary=True
should_use_kit_space_emit(True, True) = True [ROUTING TO KIT_SPACE]
emit_kit_space_expansion_event() called with n_kits=1
chronicle entry written: event_id='kse_20260602_002' (atomic .tmp -> os.replace)
per-kit JSON written: data/kit_space/kits/kit_shadow_000026.json
FK linkage verified: kit.kit_space_expansion_event_id == 'kse_20260602_002'
emit_stats: kits_emitted=1, kits_validation_errors=0
```

Smoke also verifies `skip_*=False` path:

```
QD-engine workflow terminal phase entered.
skip_theme_coalescence=False  skip_cosmological_vocabulary=True
should_use_kit_space_emit(False, True) = False [ROUTING TO SEASON-MANIFEST]
season manifest written: seasons/season_NNNNNN/
```

---

## 5. Cross-seam impact + MIGRATION.md

- **generation seam (rocket):** QDX-2 amends the QD-engine workflow's terminal phase in season_generation_pipeline.py (or equivalent). Coordination with rocket required if generation-side imports change.
- **export seam (star-lord):** kit_space_emitter.py is consumed; no changes to its public API.
- **telemetry seam (star-lord):** chronicle entry includes engine_version_sha from telemetry; consumed via existing emitter; no telemetry-seam changes.
- **MIGRATION.md** entries required (both export and generation side may need MIGRATION updates per ADR-004).
- **ADR-004 compliance:** if any new cross-seam IMPORT is introduced (e.g., new function call from generation to export), document via MIGRATION.md per ADR-004; if no new imports (just routing logic uses existing imports), MIGRATION.md entry still recommended for documentation.

---

## 6. Tag intent

`star-lord/v1.5-qdx-2-kit-space-emit-into-qd-engine-terminal-<n>`

---

## 7. Critique-pair coverage

- **Gate-1 (DESIGN-MODE):** jack-ryan reviews this dispatch BEFORE star-lord fires. Common Gate-1 catches: backward-compat assertion missing; emit-order discipline reference missing; generation_parameters composition under-specified.
- **Gate-2 (DEV-MODE):** jack-ryan reviews the tagged commit. Common Gate-2 catches: regression in skip_*=False path; emit-order violation; missing FK linkage; missing MIGRATION.md entry.

---

## 8. Quality criterion

**Game-quality goal this dispatch serves:** when QDX-3's fire script runs the QD-engine workflow with Realm Expansion defaults, the output lands NATIVELY in `data/kit_space/` with proper chronicle event recording — without QDX-3 needing to bypass the workflow and call the emitter directly (as EAA-5 v2 did). This preserves the QD-engine workflow as canonical content pipeline AND the kit-space output schema as architectural commitment, composed cleanly.

**Refutation conditions** (star-lord surfaces if any apply):
- This dispatch contradicts canonical 39 Phase 8 architecture (semantically alters export pipeline)
- Alternative execution (e.g., QDX-3 calls emitter directly post-workflow, bypassing workflow's terminal phase) would serve the named quality goal better
- Acceptance criteria can pass without advancing the quality goal (e.g., emit fires but generation_parameters is empty / chronicle event is uninformative)
- Dispatch framing pre-commits to a decision Matt has not ratified
- Dispatch introduces a pre-authored taxonomy without justification (#41 candidate)
- Dispatch introduces a scaffold value not flagged as pending-decision (#40)
- Backward-compatibility break detected (any existing season-manifest caller's behavior changes; this would violate LOCK Q ADDITIVE-ONLY)

---

## 9. Required completion record

On work-completion, append a completion record block to this dispatch file with:

```markdown
## Completion record

**Completed by:** star-lord (date)
**Tag:** `star-lord/v1.5-qdx-2-...`
**Engine commit:** `<sha>`
**Tests:** <n>/<n> PASS (list of new tests)
**MIGRATION.md:** § new entry added (export + generation if applicable)
**Smoke output:** <paste both skip_*=True (kit_space) and skip_*=False (season-manifest) smoke runs>
**FK linkage:** verified == PASS
**Gate-2 verdict:** PASS / PASS-with-INFO / BLOCK + jack-ryan finding file path
**Notes for downstream (QDX-3):** <any composition notes; e.g., how QDX-3's fire script should invoke the workflow's terminal phase with skip_*=True>
```

---

**End of QDX-2 dispatch.**

---

## Completion record

**Completed by:** star-lord (2026-06-02)
**Tag:** `star-lord/v1.5-qdx-2-kit-space-emit-into-qd-engine-terminal-1`
**Engine commit:** `9fba775`
**Tests:** 14/14 PASS
  - TestLegacyPath::test_skip_false_routes_to_legacy
  - TestLegacyPath::test_both_false_routes_to_legacy
  - TestLegacyPath::test_legacy_path_writes_manifest_file
  - TestKitSpacePath::test_both_true_routes_to_kit_space
  - TestKitSpacePath::test_kit_space_path_writes_chronicle_and_kit_json
  - TestMixedSkipFlags::test_skip_theme_false_skip_vocab_true
  - TestMixedSkipFlags::test_skip_theme_true_skip_vocab_false
  - TestGenerationParametersPropagation::test_generation_parameters_in_chronicle
  - TestGenerationParametersPropagation::test_generation_parameters_none_is_ok
  - TestEmitOrderAndFKLinkage::test_chronicle_written_before_kit_json
  - TestGuardConditions::test_none_export_dicts_raises
  - TestGuardConditions::test_empty_list_kit_space_path
  - TestGuardConditions::test_empty_list_legacy_path
  - TestResourceBounds::test_single_kit_wall_clock_under_5s
**MIGRATION.md:** 2 entries added:
  - `src/reincarnated/export/MIGRATION.md` § v1.73-qdx-2-kit-space-emitter-wired-into-qd-engine-terminal
  - `src/reincarnated/generation/MIGRATION.md` § [2026-06-02] QDX-2
**Smoke output:**
```
should_use_kit_space_emit truth table: PASS

SMOKE PATH 1 (skip_*=True kit_space):
  QD-engine workflow terminal phase entered.
  skip_theme_coalescence=True  skip_cosmological_vocabulary=True
  should_use_kit_space_emit(True, True) = True [ROUTING TO KIT_SPACE]
  emit_kit_space_expansion_event() called with n_kits=1
  chronicle entry written: event_id='kse_20260602_001' (atomic .tmp -> os.replace)
  per-kit JSON written: data/kit_space/kits/kit_shadow_000001.json
  FK linkage verified: kit.kit_space_expansion_event_id == 'kse_20260602_001'
  emit_stats: kits_emitted=1, kits_validation_errors=0
  wall_clock: 0.02s (< 5s: True)
  PASS

SMOKE PATH 2 (skip_*=False season-manifest):
  QD-engine workflow terminal phase entered.
  skip_theme_coalescence=False  skip_cosmological_vocabulary=True
  should_use_kit_space_emit(False, True) = False [ROUTING TO SEASON-MANIFEST]
  season manifest written: terminal_phase_manifest.json
  PASS
```
**FK linkage:** verified == PASS (kit.kit_space_expansion_event_id == chronicle event_id)
**Emit-order discipline:** PRESERVED — chronicle FIRST delegated to emitter (CHRONICLE_SCHEMA.md § 5.1). run_qd_engine_terminal_phase() routes through emit_kit_space_expansion_event() which enforces the order; terminal function does NOT re-implement it.
**Backward compat:** LOCK Q ADDITIVE-ONLY preserved. w5r3_author_season_content() + run_season_generation() UNCHANGED. skip_*=False callers route to legacy path, no behavior change.
**Existing test suite:** 113/113 pre-existing kit_space emitter + schema + skill_naming tests PASS (no regressions).
**Gate-2 verdict:** Pending jack-ryan Gate-2 review of tagged commit.
**Implementation note:** The QD-engine workflow terminal function is located at:
  `src/reincarnated/generation/season_generation_pipeline.py` § 6.5 — `run_qd_engine_terminal_phase()`
  Target file verified as canonical Cycle 13 Wave 5 lineage entry point (wave-state + dispatch both point here).

**Notes for downstream (QDX-3):**
QDX-3's fire script should call `run_qd_engine_terminal_phase()` as the final step after
Phase 5 output (WS1A.4-lite + cohesion naming) is ready. Minimal call pattern:

```python
from reincarnated.generation.season_generation_pipeline import run_qd_engine_terminal_phase

terminal_result = run_qd_engine_terminal_phase(
    export_dicts_with_metadata=named_export_dicts,  # list[dict] from Phase 5 output
    skip_theme_coalescence=True,                    # Realm Expansion default (EAA-2)
    skip_cosmological_vocabulary=True,              # Realm Expansion default (EAA-2)
    event_scope="QDX-5 full fire: N kits from QD-engine workflow + WS1A.4-lite",
    substrate_inputs_changed=["Q18 vocabulary lock", "WS2.P2 magic weapons"],
    generation_parameters={
        "n_candidates": n_candidates,
        "pareto_target": pareto_target,
        "ws1a4_lite_active": True,
        "skip_theme_coalescence": True,
        "skip_cosmological_vocabulary": True,
        # ... any other fire-run parameters for chronicle provenance
    },
    # kit_space_data_dir defaults to data/kit_space/ (engine repo root relative)
    # Override for tests: kit_space_data_dir=Path("...") 
)

assert terminal_result["emit_path"] == "kit_space"
assert terminal_result["kits_validation_errors"] == 0
print(f"event_id: {terminal_result['event_id']}")
print(f"kits_emitted: {terminal_result['kits_emitted']}")
```

No bypass of the workflow needed (contrast with EAA-5 v2 which bypassed and called the emitter
directly). QDX-3's fire script invokes the workflow and calls `run_qd_engine_terminal_phase()`
at the end — that IS the correct composition. The emitter is wired INTO the terminal; QDX-3
does not call `emit_kit_space_expansion_event()` directly.

**export_dicts_with_metadata schema:** each dict must have:
  - `dominant_element`: str (lowercase canonical-7+1)
  - `skills`: list of skill dicts (with ws1a4_* fields populated by WS1A.4-lite per EAA-1)
  - `name`: str | None (kit name from Wave B identity LLM)
  - `balance_metadata`: dict | None (cultural_tradition, period)
  - `archetype_tag`: str | None
  - Optional: `emergent_kit_concept`, `chain_composition`, `t4_selection`, `supporting_chain`, `substrate_trace`

This matches the output format of `apply_kit_space_skill_naming_batch()` + any Phase 5 enrichment.
