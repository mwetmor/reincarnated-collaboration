# Dispatch — 2026-06-02 — QDX-1 — WS1A.4-lite integration into Phase 5 skill naming

**From:** knight-rider (orchestrator)
**To:** rocket (PRIMARY — engine generation seam owner) + star-lord (LLM seam consultant)
**Authority:** Matt 2026-06-02 QDX chain Locks A-P preserved + LOCK Q (QD-engine workflow integration authority; ADDITIVE-ONLY)
**Wave:** cycle-17 QDX QD-Engine Re-Fire — Phase 1 (parallel with QDX-2 + QDX-3)
**State file:** `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`
**Tag intent:** `rocket/v1.5-qdx-1-ws1a-4-lite-phase-5-integration-<n>`
**Estimated horizon:** ~1-2 sessions

---

## 1. Authoritative reading (READ before any code work)

1. **`canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md`** § 1 Phase 5 (cohesion-coalescence; flavor + naming)
2. **`canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`** § 3.2 (per-skill LLM flavor-or-canonical naming; THE design pattern this integration implements)
3. **`canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`** § 2 (Q18 vocabulary pool per primary)
4. **`~/Games/reincarnated-engine/src/reincarnated/llm/ws1a4_lite_flavor_judgment.py`** (THE module to wire in)
5. **`~/Games/reincarnated-engine/src/reincarnated/generation/phase5_skill_naming.py`** (THE target module to amend)
6. **`~/Games/reincarnated-engine/src/reincarnated/generation/kit_space_skill_naming.py`** (EAA-1 wrapper; reference for how WS1A.4-lite composes with skill-naming output)
7. **`agentic_orchestration/dispatches/2026-06-02-eaa-1-ws1a-4-lite-implementation.md`** (EAA-1 original dispatch; reference for prompt design + per-skill judgment semantics)
8. **`agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`** (QDX wave-state; LOCK Q + escape clauses)

---

## 2. Target seam + scope

**Owner seam:** generation (rocket) with LLM consultation (star-lord)

**Target file:** `~/Games/reincarnated-engine/src/reincarnated/generation/phase5_skill_naming.py`

**Companion file:** `~/Games/reincarnated-engine/src/reincarnated/llm/ws1a4_lite_flavor_judgment.py` (already exists; no changes needed — it's the public API being consumed)

**Scope (ADDITIVE per LOCK Q):**

Phase 5 skill naming currently fires per-node LLM calls + cohesion-judge programmatic scoring (per `phase-5-cohesion-judge-calibration-spec-2026-05-25.md`). The integration adds an OPTIONAL pre-pass: when activated, WS1A.4-lite fires per-skill BEFORE the cohesion-judge naming call to decide flavor-or-canonical + (if flavor) pick the Q18 word; Phase 5 then uses that decision to constrain the cohesion-judge naming call.

**Activation parameter:** `ws1a4_active: bool = False` added to Phase 5 entry-point function signature. When False, existing Phase 5 behavior unchanged (backward-compatible per LOCK J/Q ADDITIVE-ONLY discipline). When True, fires WS1A.4-lite per-skill pre-pass and threads the decision into cohesion-judge prompt context.

**Out of scope (CRITICAL — do NOT touch):**
- Semantic behavior of existing Phase 5 cohesion-judge naming for `ws1a4_active=False` callers (any existing caller's behavior MUST be unchanged)
- The WS1A.4-lite module itself (`ws1a4_lite_flavor_judgment.py`) — public API is stable
- Q18 vocabulary lock contents (IMMUTABLE per canonical lock)
- Physical-primary opt-out semantics (WS1A.4-lite raises `PhysicalPrimaryOptOut`; Phase 5 catches and uses mechanical-schema templates per existing behavior)
- The kit_space_skill_naming.py wrapper from EAA-1 (it's not the integration target; QDX-1 wires INTO Phase 5 directly so the QD-engine workflow's Phase 5 invocation does the right thing without needing the wrapper)

---

## 3. Acceptance criteria

### 3.1 Functional

1. **Backward compatibility verified** — `phase5_skill_naming.py` callers that don't pass `ws1a4_active=True` (existing Phase 5 callers; smoke tests; etc.) get IDENTICAL output to current behavior. Add a regression smoke test that re-runs an existing Phase 5 smoke and asserts byte-identical (or modulo non-determinism, semantically-identical) output.

2. **WS1A.4-lite pre-pass activates when `ws1a4_active=True`** — for each non-physical-primary skill node, WS1A.4-lite fires; returns `{flavor: bool, flavor_word: str|null, skill_name: str}`. Decision is recorded on the node (e.g., `ws1a4_flavor_decision`, `ws1a4_flavor_word_used`, `ws1a4_attempt_number`).

3. **Phase 5 cohesion-judge naming consumes the WS1A.4-lite decision** — when `ws1a4_active=True` and the pre-pass returns `flavor=True` with a word, the cohesion-judge prompt is CONSTRAINED to use that flavor word in the skill name. When `flavor=False`, the cohesion-judge prompt is constrained to canonical naming (no flavor word; element-label + role/action noun pattern per Q18 lock § 3.2).

4. **Physical-primary opt-out preserved** — when WS1A.4-lite raises `PhysicalPrimaryOptOut`, Phase 5 falls back to existing mechanical-schema template behavior (no flavor decision recorded; skill receives canonical mechanical naming).

5. **Cost telemetry composes** — WS1A.4-lite cost (per `purpose = "ws1a4_lite_per_skill_flavor_judgment"`) and Phase 5 cost (per existing telemetry) are tracked separately and reportable. Per-fire totals available via existing stats dataclass extension or new return field.

### 3.2 Tests

6. **Unit tests** — at least 5 new tests covering: (a) `ws1a4_active=False` backward-compat; (b) `ws1a4_active=True` non-physical with flavor=True path; (c) `ws1a4_active=True` non-physical with flavor=False path; (d) physical opt-out path; (e) LLM client unavailable fallback (graceful degradation to canonical naming).

7. **Smoke test** — single-kit smoke that exercises a non-physical primary with `ws1a4_active=True`; asserts at least one skill has `ws1a4_flavor_decision=True` AND at least one has `ws1a4_flavor_decision=False` (variety required); asserts flavor words come from Q18 pool of the kit's primary.

### 3.3 Documentation

8. **MIGRATION.md entry** — `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` § new entry: "QDX-1 — WS1A.4-lite integration into Phase 5 skill naming; additive `ws1a4_active` parameter; backward-compatible; consumed by QDX-3 fire script".

9. **Docstring at function level** — Phase 5 entry-point function docstring extended to document `ws1a4_active` parameter semantics + opt-out behavior + composition with cohesion-judge.

### 3.4 Resource bounds (Discipline #1.1)

10. **Pre-fire resource-bounds projection** — at smoke gate, project memory + token budget for the integrated pipeline. WS1A.4-lite ~$0.0015-0.0025 per call (per its docstring); Phase 5 ~$1.17 per full run (per its docstring); composed ~$0.50 per kit-space-expansion-scale run; within Phase 5 spec § 2.4 target ($0.50-$2.00).

---

## 4. Smoke-test expectation

Before tagging, run the smoke test in § 3.2 item 7 with a non-physical primary (e.g., shadow). Expected output sample (illustrative):

```
Skill 1 (chain1_t1): ws1a4_flavor=True  word='wraith' → name='Wraith Touch'
Skill 2 (chain1_t2): ws1a4_flavor=False word=null    → name='Shadow Bolt'
Skill 3 (chain1_t3): ws1a4_flavor=True  word='void'  → name='Void Rending'
Skill 4 (chain1_t4): ws1a4_flavor=False word=null    → name='Shadow Crescent'
...
ws1a4_flavor_rate: 0.5
cohesion-judge attempts (all skills): 1
Phase 5 PASS rate: 100%
```

Variety check: ≥1 flavor=True AND ≥1 flavor=False in the kit (rejects all-True or all-False as a prompt-design failure signal).

Telemetry check: `ws1a4_total_cost_usd > 0` AND `phase5_total_cost_usd > 0`; both reportable separately.

---

## 5. Cross-seam impact + MIGRATION.md

- **Phase 5 consumers (downstream):** kit_space_skill_naming.py from EAA-1 currently calls Phase 5 indirectly — verify no break.
- **QDX-3 fire script (downstream):** will call Phase 5 with `ws1a4_active=True` for the QD-engine workflow re-fire.
- **MIGRATION.md** entry required per § 3.3 item 8.
- **ADR-004 compliance:** this is a generation-side change with NO new cross-seam contract — Phase 5 is internal to generation seam; ws1a4_lite_flavor_judgment is LLM seam (already in production; consumed via existing import). No new cross-seam contract to MIGRATE.

---

## 6. Tag intent

`rocket/v1.5-qdx-1-ws1a-4-lite-phase-5-integration-<n>`

(May increment if multiple commits are needed; first should land integration + smoke; subsequent for any iteration per Gate-2 INFO.)

---

## 7. Critique-pair coverage

- **Gate-1 (DESIGN-MODE):** jack-ryan reviews this dispatch BEFORE rocket fires the work. Common Gate-1 catches: missing backward-compat assertion, missing cost-telemetry path, missing physical-opt-out flow, missing variety smoke check.
- **Gate-2 (DEV-MODE):** jack-ryan reviews the tagged commit. Common Gate-2 catches: regression in `ws1a4_active=False` path, prompt-design issue (all-flavor or no-flavor), cost-telemetry not flowing, MIGRATION.md missing.
- **LOCK L iteration discipline:** if Gate-2 BLOCKs on prompt/integration design issue, seam re-fires within authority (1st BLOCK); 2+ BLOCKs → Matt escalation.

---

## 8. Quality criterion

**Game-quality goal this dispatch serves:** when the QD-engine workflow fires Phase 5, each non-physical-primary kit's skill set has both flavored skills (using Q18 pool words like "Wraith Touch", "Void Rending") and canonical skills (like "Shadow Bolt", "Shadow Crescent") on the same kit's skill bar — preserving the Necromancer-with-Bone-Spear-AND-Shadow-Bolt design pattern from canonical record § 3.2 example.

**Refutation conditions** (rocket surfaces if any apply):
- This dispatch contradicts canonical 39 Phase 5 architecture
- Alternative execution (e.g., a separate WS1A.4-pass module that runs BEFORE Phase 5 entirely) would serve the named quality goal better
- Acceptance criteria can pass without advancing the quality goal (e.g., flavor decisions fire but cohesion-judge naming ignores them; resulting names look canonical even when flavor=True)
- Dispatch framing pre-commits to a decision Matt has not ratified
- Dispatch introduces a pre-authored taxonomy without justification (#41 candidate)
- Dispatch introduces a scaffold value not flagged as pending-decision (#40)
- Backward-compatibility break detected (any existing Phase 5 caller's behavior changes; this would violate LOCK Q ADDITIVE-ONLY)

---

## 9. Required completion record

On work-completion, append a completion record block to this dispatch file with:

```markdown
## Completion record

**Completed by:** rocket (date)
**Tag:** `rocket/v1.5-qdx-1-...`
**Engine commit:** `<sha>`
**Tests:** <n>/<n> PASS (list of new tests)
**MIGRATION.md:** § new entry added
**Smoke output:** <paste illustrative smoke output with variety check>
**Cost telemetry:** ws1a4_total_cost_usd=$<x>, phase5_total_cost_usd=$<y>
**Gate-2 verdict:** PASS / PASS-with-INFO / BLOCK + jack-ryan finding file path
**Notes for downstream (QDX-3):** <any composition notes>
```

---

**End of QDX-1 dispatch.**

---

## Completion record

**Completed by:** rocket (2026-06-02)
**Tag:** `rocket/v1.5-qdx-1-ws1a-4-lite-phase-5-integration-1`
**Engine commit:** `76adb6e`

**Tests:** 10/10 PASS (new) + 34/34 PASS (existing WS1A.4-lite regression)

New tests in `tests/test_phase5_qdx1_ws1a4_integration.py`:
1. `test_backward_compat_false_path` — ws1a4_active=False: output identical to existing behavior; all ws1a4_* stats zero
2. `test_ws1a4_active_flavor_true_path` — flavor=True path: ws1a4_flavor_decision=True, word from Q18 pool, constraint injected
3. `test_ws1a4_active_flavor_false_path` — flavor=False path: ws1a4_flavor_decision=False, word=None, canonical constraint injected
4. `test_physical_opt_out_path` — physical primary: judge not called; ws1a4_physical_opt_out incremented; no ws1a4_* fields
5. `test_llm_unavailable_fallback` — llm_client=None + ws1a4_active=True: graceful degradation to placeholder naming
6. `test_stats_accumulation_flavor` — multi-skill kit: flavor/canonical/cost counters accumulate correctly
7. `test_variety_check` — ≥1 flavor=True AND ≥1 flavor=False in same kit (dispatch § 4 variety criterion)
8. `test_ws1a4_metadata_written_to_skill` — all 4 ws1a4_* fields written into skill dict
9. `test_phase5_stats_backward_compat` — Phase5RunStats new fields default 0/0.0; to_dict() includes ws1a4_* keys; existing fields preserved
10. `test_append_ws1a4_constraint_flavor_true_and_false` — constraint helper produces correct flavor/canonical blocks

**MIGRATION.md:** § QDX-1 entry added at `src/reincarnated/generation/MIGRATION.md` (top of entries; documents all new params, skill dict fields, Phase5RunStats additive fields, downstream consumer impact, cost telemetry composition)

**Smoke output (shadow kit, 6 skills, ws1a4_active=True):**
```
  chain1_t1: ws1a4_flavor=False  word=None       → name='Shadow Bolt'
  chain1_t2: ws1a4_flavor=True   word='wraith'   → name='Wraith Binding'
  chain1_t3: ws1a4_flavor=True   word='void'     → name='Void Wraith Strike'
  chain2_t1: ws1a4_flavor=True   word='shade'    → name='Shade Step'
  chain2_t2: ws1a4_flavor=True   word='soul'     → name='Soul Slip'
  chain2_t3: ws1a4_flavor=True   word='necrotic' → name='Necrotic Soul Slip'
ws1a4_flavor_rate: 5/6 = 0.83
Variety check: has_flavor_true=True, has_flavor_false=True — PASS
Q18 pool validation: PASS (all flavor words from shadow pool)
```

**Cost telemetry:** ws1a4_total_cost_usd=$0.0130, phase5_total_cost_usd=$0.0162 (both tracked separately; both > 0 per acceptance criterion § 3.1 item 5)

**Gate-2 verdict:** Awaiting jack-ryan Gate-2 post-output review.

**Notes for downstream (QDX-3):**

QDX-3 fire script invokes Phase 5 with `ws1a4_active=True` via:

```python
from reincarnated.generation.phase5_skill_naming import apply_phase5_skill_naming

result_dicts, stats, t4_stats = apply_phase5_skill_naming(
    llm_client=llm_client,
    export_dicts=export_dicts,
    archetype_tags=archetype_tags,        # parallel list per form
    form_summaries=form_summaries,        # parallel list per form
    verbose=True,
    run_t4_narration=True,
    ws1a4_active=True,                    # QDX-1 integration parameter
    kit_concepts=kit_concepts,            # parallel list of emergent kit concept strings per form
)
# stats.ws1a4_total_cost_usd = WS1A.4-lite cost
# stats.total_estimated_cost_usd = Phase 5 cohesion-judge cost
# stats.ws1a4_flavor_rate = fraction of skills that took flavor branch
```

`kit_concepts` is a parallel list of emergent kit concept strings (e.g., "Shadow Necromancer"),
one per form in `export_dicts`. If None is passed, `name_form_skills()` falls back to using
the form's `name` field — so it's optional but recommended for richer WS1A.4-lite context.

For physical-primary kits, ws1a4_active=True is safe: WS1A.4-lite opts out automatically;
no ws1a4_* fields are written; physical opt-out counter is incremented in stats.

The EAA-1 wrapper (`kit_space_skill_naming.py`) is unaffected — it calls `name_form_skills`
without the new params (backward-compat); QDX-3 should call `apply_phase5_skill_naming`
directly with `ws1a4_active=True`, not via the EAA-1 wrapper.
