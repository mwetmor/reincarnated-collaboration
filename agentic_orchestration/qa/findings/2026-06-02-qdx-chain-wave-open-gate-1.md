# Finding — 2026-06-02 — QDX Chain Wave-Open + Phase 1 Dispatches — Gate-1

**Reviewer:** jack-ryan
**Severity:** PASS-with-INFO
**Target:** QDX wave-open + QDX-1 + QDX-2 + QDX-3 (pre-fire Gate-1; no commit yet)
**Developer:** knight-rider (authoring); rocket + star-lord (executing)
**Principles applied:** Review Principles 1, 2, 3, 4, 5 (all five; architecture-alignment, backward-compat, resource-bounds, cross-seam contracts, quality-criterion)

---

## Overall verdict: PASS-with-INFO

No BLOCKs. No WARNs. Seven INFOs captured across the four dispatch documents. Phase 1 is cleared to fire in parallel (rocket QDX-1 + QDX-3; star-lord QDX-2). INFOs are non-blocking for Phase 1 execution but are queued for Gate-2 review at workstream close.

---

## Per-dispatch verdicts

### Wave-open dispatch — INFO (2 items)

**INFO W-1 — Phase 3 sim (Phase 3 absent from QDX scope)**

The wave-open § 5 describes the QDX script orchestrating "Phase 1 → 2 → 4 → 5 → Wave A → Wave B → 7 → 8" in canonical 39 order. This explicitly skips Phase 3 (sim convergence). The omission is correctly noted in QDX-3 § 2 scope (gamora sim module, "if present"), and canonical 39 § 5.7 explicitly permits the 2-LAYER gate (mechanical + cohesion) for Cycle 14 v1 without Phase 6 (visual). However, Phase 3 is not Phase 6 — Phase 3 is the sim validation step that produces per-kit BC coordinates and playability gate disposition per canonical 39 Phase 3 box. The wave-open does not explicitly state that Phase 3 is deferred (vs skipped); the QDX-3 dispatch uses "Phase 1 → 2 → 4 → 5..." with Phase 3 entirely absent in the enumeration.

Likely justification: QDX-3 is composing against `season_generation_pipeline.py` (Cycle 13 wave-5 lineage) which presumably includes sim. But the dispatch narrative makes the pipeline look like it jumps from Phase 2 generation directly to Phase 4 Pareto. If sim is embedded inside the existing pipeline module and is not a separate QDX-3 step, this should be stated explicitly. Gate-2 should verify the smoke output shows Phase 3 sim executing and not silently skipped.

- Cite: Canonical 39 § 1 Phase 3; Discipline #18 (methodology-before-execution at sim validation hotspot)
- Action for QDX-3: confirm in docstring whether Phase 3 sim is (a) embedded in the composed module call, (b) lightweight-substitute, or (c) genuinely skipped under LOCK R parameters.

**INFO W-2 — n_candidates=200 vs. Cycle-14-equivalent~650: explicitly flagged as scaffold**

Wave-open and QDX-3 both state N_CANDIDATES=200 as KR-selected with "Cycle 14 wave-5 was ~650; QDX-3 starts lower for cost+wall-clock bound." The dispatch correctly flags this as a LOCK R parameter "rocket may amend within LOCK R." The scaffold-value-requires-canonical-decision discipline (#40) is satisfied because the wave-state LOCK R explicitly authorizes KR + rocket + star-lord to tune this parameter within bounds (no Matt-touch required within $60 / 20-kit floor). No WARN. Noting for Gate-2 that the completion record should document whether n_candidates=200 produced Pareto-surviving count in range; if outside range, the completion record must note the adjustment made.

- Cite: Discipline #40 (scaffold values); LOCK R escape clauses
- No action required for Phase 1.

---

### QDX-1 — INFO (2 items)

**INFO 1-1 — Backward-compat regression smoke: byte-identical vs. semantically-identical**

Acceptance criterion 3.1.1 specifies "IDENTICAL output... byte-identical (or modulo non-determinism, semantically-identical)." The LLM-backed Phase 5 is non-deterministic by nature (temperature > 0 on cohesion-judge calls). "Semantically-identical" is under-specified: does it mean same skill names? Same ws1a4 decisions? Same flavor words? Gate-2 will need to verify the regression smoke test has a concrete definition of "semantically-identical" — e.g., "same skill count, same canonical-vs-flavor split direction per skill, same PASS rate." Recommend rocket documents the specific assertion in the test, not just the word "semantically-identical."

- Cite: Discipline #8 (schema validation at export boundaries); Review Principle 2 (backward-compat)
- No blocking issue; flag for Gate-2 test inspection.

**INFO 1-2 — kit_space_skill_naming.py downstream impact verification**

QDX-1 § 5 correctly notes: "kit_space_skill_naming.py from EAA-1 currently calls Phase 5 indirectly — verify no break." This is identified as a downstream impact item but no explicit test is required in acceptance criteria § 3.2. The 5 unit tests in AC 3.2.6 cover the QDX-1 integration paths but do not include a test that exercises the EAA-1 wrapper path against the amended Phase 5. If the EAA-1 wrapper passes `ws1a4_active` implicitly or receives it as a default-False, it must not break. Recommend rocket adds this as a 6th unit test or smoke assertion.

- Cite: ADR-004 (cross-seam impact); Review Principle 2
- No blocking issue; flag for Gate-2 test inspection.

---

### QDX-2 — INFO (1 item)

**INFO 2-1 — MIGRATION.md dual-seam entry: generation-side MIGRATION.md not named**

QDX-2 § 5 states: "both export and generation side may need MIGRATION updates per ADR-004." AC 3.3.8 specifies the entry only in `export/MIGRATION.md`. If `season_generation_pipeline.py` (generation seam) is amended to add terminal-phase routing, that amendment is a generation-seam change and should have an entry in `generation/MIGRATION.md` per ADR-004 pattern established at EAA-1. The dispatch is aware of this (§ 5 parenthetical) but the acceptance criteria only requires the export MIGRATION entry, not the generation one. This gap between §5 awareness and §3.3 acceptance criteria should be resolved: either add the generation/MIGRATION.md entry to AC or confirm why it's not required.

- Cite: ADR-004 (cross-seam MIGRATION discipline); Review Principle 4
- Action: star-lord resolves at completion-record time (add generation/MIGRATION.md entry if generation-side code is touched; confirm if not).

---

### QDX-3 — INFO (2 items)

**INFO 3-1 — Wave A vs Wave B escalation path not mirrored for Wave A**

QDX-3 § 7 Critique-pair coverage states: "if Gate-2 BLOCKs on Wave B template-repeat → seam re-fires Wave B prompt within authority (1st BLOCK); 2+ BLOCKs → Matt escalation per LOCK R escape." Escape clause item 5 covers Wave B template-repeat escalation. However, Wave A (faction naming LLM) has no explicit 1st-BLOCK/2+-BLOCK escalation path named. Wave A failure would also be a prompt design failure requiring seam-authority re-fire. Recommend the completion record note confirm whether Wave A and Wave B share the same LOCK L iteration discipline, or if Wave A prompt design failure has a separate path.

- Cite: LOCK L iteration discipline (wave-state § 1 LOCK L); escape clause item 5
- No blocking issue; flag for Gate-2 and QDX-4 smoke review.

**INFO 3-2 — Pre-fire ABORT threshold documentation: $60 vs. computed projection path**

QDX-3 § 3.4.14 specifies: "If projection >$60 → ABORT + escalate (LOCK R escape)." The smoke output example (§ 4) correctly shows the ABORT threshold check in the startup log. The acceptance criteria are clear. One gap: the projected cost formula in § 2 ("Phase 5 skill naming: ~n_pareto_kits × 7 skills avg × 1 LLM call/skill = ~245 calls") uses n_pareto_kits as an input, but n_pareto_kits is only known AFTER Phase 4 Pareto reduction. This means the startup cost projection must use n_candidates × Pareto_yield_estimate as the upper bound, not the post-Pareto count. If the script projects cost using n_candidates (pre-Pareto) as the upper bound for the LLM call count estimate, this is conservative and correct. If it waits for Phase 4 output before projecting, the ABORT gate fires after potentially expensive Phase 2+3+4 work has already run. Recommend the docstring clarify this: pre-fire projection should use n_candidates × Pareto_yield × avg_skills_per_kit as the conservative upper bound, not post-Phase-4 actuals.

- Cite: Discipline #1.1 (resource-bounds projection); LOCK R escape
- No blocking issue; flag for Gate-2 script docstring review.

---

## Common Gate-1 catches — status

| Catch | Status |
|---|---|
| Missing backward-compat assertion | Present in QDX-1 AC 3.1.1 and QDX-2 AC 3.1.1. INFO 1-1 flags semantic-identity under-specification. |
| Missing cost-telemetry path | Present in QDX-1 AC 3.1.5 and QDX-3 § 2 cost projection + ABORT threshold. |
| Missing physical-opt-out flow | Present in QDX-1 AC 3.1.4 explicitly. |
| Missing variety smoke check | Present in QDX-1 AC 3.2.7 and QDX-3 AC 3.2.11. |
| Missing n_candidates → pareto_target sizing rationale | Present via LOCK R + QDX-3 § 2 LOCK R defaults block. |
| Missing Wave A vs Wave B distinction | Wave A/B both present in QDX-3 phase orchestration; escalation asymmetry flagged at INFO 3-1. |
| MIGRATION.md coverage | QDX-1 AC 3.3.8 and QDX-2 AC 3.3.8 both present; generation-side gap flagged at INFO 2-1. |
| Quality criterion + refutation conditions | All four dispatches carry both quality criterion AND refutation conditions sections. Strong. |
| ABORT threshold present | QDX-3 AC 3.4.14 explicit. |

---

## Architecture alignment assessment

**Canonical 39 phase semantics:** QDX-3 orchestrates Phase 1 → 2 → 4 → 5(a/b/c) → Wave A → Wave B → 7 → 8. This preserves canonical 39 phase ordering. Phase 6 is explicitly deferred per canonical 39 § 5.6. Phase 7 is 2-LAYER per canonical 39 § 5.7. No phase is semantically amended for existing callers (LOCK Q ADDITIVE-ONLY).

**Season-Archive Realm-Expansion pivot preserved:** QDX-2 routes via `should_use_kit_space_emit(True, True)` using EAA-2 skip flags as the routing signal. Output lands in `data/kit_space/` not `seasons/`. Chronicle event records the expansion event. FK linkage enforced. All architectural commitments from `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` preserved.

**LOCK Q ADDITIVE-ONLY:** All three dispatches explicitly prohibit semantic changes to existing callers. QDX-1 adds `ws1a4_active=False` default; QDX-2 uses `should_use_kit_space_emit()` as a routing switch preserving legacy path; QDX-3 is a new script, not an amendment to existing scripts. Clean.

**Discipline #54 (integration-smoke-gate):** LOCK S + QDX-4 explicitly operationalize this. Phase 1 PASS criterion gates QDX-4; QDX-4 PASS gates QDX-5. Correct sequencing.

**Discipline #46 (DB anti-materialization):** QDX-3 AC 3.4.15 references "Discipline #46 (Phase 4 protection); per-cell bounding for math gates." Present.

**Discipline #18 (methodology-before-execution):** QDX-3 references "Phase 4 Pareto reduction" and "Phase 5 cohesion clustering" as the hotspots; cost projection must precede execution. Pre-fire resource-bounds projection is a required acceptance criterion (AC 3.4.14). Satisfied.

**EAA chain infrastructure preservation:** WS1A.4-lite module (EAA-1) is consumed but not amended. skip_flag pattern (EAA-2) is consumed and composed at QDX-2 routing. kit_space_emitter (EAA-3+4) is consumed but not amended. EAA-5 v2 25-kit output preserved as historical artifact. Nothing thrown away. Clean.

---

## Composition notes for downstream Gate-2 reviews

**QDX-1 Gate-2 checklist additions:**
- Verify regression smoke test has concrete "semantically-identical" assertion definition, not just the word (INFO 1-1)
- Verify EAA-1 wrapper (kit_space_skill_naming.py) still passes when Phase 5 is called with default `ws1a4_active=False` (INFO 1-2)
- Verify `ws1a4_flavor_rate > 0` AND variety check (≥1 True, ≥1 False) in smoke output

**QDX-2 Gate-2 checklist additions:**
- Verify both export/MIGRATION.md AND generation/MIGRATION.md entries if generation-side code touched (INFO 2-1)
- Verify FK linkage in smoke output (kse_<YYYYMMDD>_<seq3> format per EAA-3 lock)
- Verify both skip_*=True and skip_*=False smoke paths in completion record

**QDX-3 Gate-2 checklist additions:**
- Verify Phase 3 sim presence or absence in smoke output with explicit narrative (INFO W-1 / INFO 3-1 composition)
- Verify startup cost projection uses pre-Pareto conservative upper bound, not post-Phase-4 actuals (INFO 3-2)
- Verify Wave A prompt design failure path exists if Wave A produces template-repeat faction names (INFO 3-1)
- Verify completion record includes QDX-4 parameter notes (seed, primary element suggestion)

**QDX-4 (smoke-gate) gate-2 checklist — pre-load:**
- 7-criteria smoke checklist from wave-open § 6 applies verbatim
- Phase 3 presence confirmed (or deferred path documented)
- Wave A + Wave B both produce non-template output in the single-kit smoke
- ws1a4_flavor_rate > 0 in smoke kit
- t4_selection non-null in smoke kit
- Chronicle event FK linkage verified
- Cost < $0.10 smoke bound

---

## Sign-off

**Reviewer:** jack-ryan
**Timestamp:** 2026-06-02
**Verdict:** PASS-with-INFO (7 INFOs; 0 WARNs; 0 BLOCKs)
**Phase 1 cleared to fire:** YES — QDX-1 + QDX-2 + QDX-3 parallel fire authorized
**LOCK L status:** No BLOCKs issued; LOCK L iteration discipline not triggered
**Escalation to Matt:** Not required

INFOs are queued for Gate-2 resolution at workstream close. Knight-rider routes QDX-4 smoke-gate only after QDX-1 + QDX-2 + QDX-3 all receive Gate-2 PASS per Phase 1 PASS criterion.
