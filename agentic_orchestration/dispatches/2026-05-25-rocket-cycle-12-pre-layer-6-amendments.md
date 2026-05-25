# Dispatch — 2026-05-25 — rocket — Cycle 12 pre-Layer-6 amendments batch (L2 WARN-B/C + L4 INFO-A/B)

**From:** knight-rider
**To:** rocket (generation seam — engine content-generation owner)
**Approved by:** KR autonomous in-scope decision per Cycle 12 scope-doc § 1 (acceptance-criterion application — Gate-2 amendment integration before downstream layer fires) + skip-confirmation re-auth 2026-05-25
**Estimated effort:** ~15-30 min combined (4 small amendments across 3 files)
**Acceptance:** 4 amendments applied per Gate-2 verdicts: L2 WARN-B (MIGRATION.md § v1.4-layer-2 field-name reconciliation — PRE-LAYER-6 priority) + L2 WARN-C (dead option_c_cells cleanup in BcTargetCell.matching_policy — PRE-LAYER-6 priority) + L4 INFO-A (math note Math 5 § Param 1 naming reconciliation) + L4 INFO-B (math note VOTE_THRESHOLD sweep range expansion note); MIGRATION.md update if amendments materially affect cross-seam consumer awareness; rocket-internal-only otherwise

---

## Context

Two Gate-2 verdicts surfaced 4 amendment items rocket must address before Layer 6 dispatch fires:

**From Gate-2 on Layer 2 (PASS-WITH-AMENDMENTS; 3 WARN — WARN-B + WARN-C are PRE-LAYER-6 priority):**

- **WARN-B (PRE-LAYER-6 PRIORITY)**: `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.4-layer-2 PlayerClassV2 schema pseudocode field names don't match implementation:
  - `stat_distribution` should be `stat_allocation`
  - `substrate_triple` should be `mechanical_substrate_triple`
  - Plus phantom fields documented but not implemented (verify against actual PlayerClassV2 dataclass at `bc_target_player_class.py`)
  - **Downstream consumer hazard** for star-lord/gamora/drax cross-seam consumers reading MIGRATION.md to understand the new shape
  - Must amend before Layer 6 dispatch authoring fires (so Layer 6 dispatch can correctly reference cross-seam consumer obligations per accurate MIGRATION.md)

- **WARN-C (PRE-LAYER-6 PRIORITY)**: Dead `option_c_cells` set defined in `bc_target_cell_sampler.py` (or wherever BcTargetCell lives) but never used in `BcTargetCell.matching_policy` property — signals design intent (Option C routing per composition policy v1 § 3) but implements something different (attribute-only routing). Cleanup before Layer 6 wire-up to prevent consumption-site confusion when L6 reads matching_policy at runtime
  - Two acceptable resolutions: (a) remove dead `option_c_cells` set if Option C routing is genuinely not implemented at L2 + capture deferred-to-v1.1+ note; (b) wire `option_c_cells` into `matching_policy` if Option C should fire for v1 (verify against composition policy v1 § 3 + gandalf comp-policy § 4 verdict memo § 3 — Cell 20 Holy Knight is Option C candidate per gandalf)
  - Rocket judgment per implementation reality

**From Gate-2 on Layer 4 (PASS; 2 INFO — non-blocking; batch with above for efficiency):**

- **INFO-A** (Discipline #1 naming drift): Math note `cycle-12-layer-4-multi-dim-convergence-2026-05-25.md` Math 5 § Parameter 1 names `penalty_scale` and describes scaling the stagnation comparison. Code at `converge.py` has no `penalty_scale` constant. The code's `# param 1` comment annotates `MAX_SP_STEP_PER_ITERATION` (a different calibration constant). Stagnation function uses `STAGNATION_EPSILON = 0.001` directly. penalty_scale = 1.0 (no-op) means functional equivalence holds, but param-number-to-name mapping conflicts across note and code
  - Resolution: amend math note Math 5 § Parameter 1 to correctly name the implemented constant(s); OR keep penalty_scale name + add note clarifying functional-equivalence + no-op nature (rocket judgment)

- **INFO-B** (Discipline #17 sweep range): Dispatch specifies VOTE_THRESHOLD sweep range [0.1, 0.5]. Math note's actual sweep was [0.01, 0.05, 0.10, 0.20, 0.50] — widened downward. Chosen value 0.05 falls below the dispatch floor but passes the accept-pass criterion
  - Resolution: amend math note to note range expansion rationale + confirm chosen 0.05 was the empirically-best value per sweep results (rocket already presumably has this data)

After all 4 amendments land, KR authors Layer 6 dispatch immediately per scope-doc § 1 autonomous orchestration.

---

## Required reading before starting

- **`agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-1-rocket-layer-2.md`** — Gate-2 on L2 source (WARN-B + WARN-C primary load-bearing for this amendment batch)
- **`agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-3-rocket-layer-4.md`** — Gate-2 on L4 source (INFO-A + INFO-B primary load-bearing)
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-2-bc-target-subspace-generator.md` — Layer 2 dispatch (WARN-B + WARN-C context)
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-4-multi-dim-convergence.md` — Layer 4 dispatch (INFO-A + INFO-B context)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 3 (Option α/β/C matching strategies — relevant for WARN-C option_c_cells resolution decision)
- `agentic_orchestration/gandalf/notes/2026-05-25-comp-policy-section-4-coverage-gap-confirmation.md` (gandalf verdict memo § 3 references Cell 20 Holy Knight Option C candidate)
- Rocket source files (primary amendment targets):
  - `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.4-layer-2 (WARN-B)
  - `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_cell_sampler.py` (or wherever BcTargetCell.matching_policy lives — WARN-C)
  - `~/Games/reincarnated-engine/src/reincarnated/generation/notes/cycle-12-layer-4-multi-dim-convergence-2026-05-25.md` (INFO-A + INFO-B)
- `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_player_class.py` (reference for actual PlayerClassV2 field names; informs WARN-B reconciliation)
- `~/Games/reincarnated-engine/src/reincarnated/generation/converge.py` (or wherever L4 calibration constants live; informs INFO-A reconciliation)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #13a + #17 + #25)

---

## Math-before-code (per Discipline #1)

No new math. 4 documentation + cleanup amendments:
- 2 documentation fidelity amendments (WARN-B + INFO-A: ensure docs match implementation)
- 1 documentation expansion note (INFO-B: sweep range expansion rationale)
- 1 code cleanup OR wiring decision (WARN-C: dead code removal OR wire-up per Option C intent)

---

## Scope (rocket amendment execution)

### Amendment 1 — L2 WARN-B (MIGRATION.md § v1.4-layer-2 field-name reconciliation)

- [ ] Inspect actual PlayerClassV2 field names at `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_player_class.py`
- [ ] Update `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.4-layer-2 pseudocode to match actual implementation:
  - `stat_distribution` → `stat_allocation` (if that's actual field name)
  - `substrate_triple` → `mechanical_substrate_triple` (if that's actual field name)
  - Remove phantom fields documented but not implemented
- [ ] Verify cross-seam consumers (star-lord export schema; loadout types.ts; gamora sim consumer) can correctly read MIGRATION.md to understand shape
- [ ] Per Discipline #13a: ensure documentation reflects implementation; no drift

### Amendment 2 — L2 WARN-C (dead option_c_cells cleanup OR wire-up)

- [ ] Inspect `BcTargetCell.matching_policy` property + `option_c_cells` set definition
- [ ] DECIDE per rocket judgment + canonical authority:
  - **Option (a)**: Remove dead `option_c_cells` set + capture deferred-to-v1.1+ note in math note OR MIGRATION.md. Choose if Option C routing is genuinely not implemented at L2 + Cell 20 Holy Knight (per gandalf verdict memo § 3) is acceptable as default-heuristic-handled at v1
  - **Option (b)**: Wire `option_c_cells` into `matching_policy` per Option C routing intent. Choose if rocket determines Option C is implementable at L2 without breaking other tests + verdict memo § 3 routing pattern matches
- [ ] Apply chosen option + document rationale in math note OR commit message
- [ ] If Option (b) chosen, ensure 28/28 Layer 2 tests + 374/374 regression still PASS (re-run smoke)
- [ ] Cross-reference gandalf comp-policy verdict memo § 3 for Cell 20 Holy Knight handling

### Amendment 3 — L4 INFO-A (math note Math 5 § Parameter 1 naming reconciliation)

- [ ] Amend `~/Games/reincarnated-engine/src/reincarnated/generation/notes/cycle-12-layer-4-multi-dim-convergence-2026-05-25.md` Math 5 § Parameter 1:
  - **Option (a)**: Rename math note `penalty_scale` to match code's `MAX_SP_STEP_PER_ITERATION` + `STAGNATION_EPSILON` (per actual implementation)
  - **Option (b)**: Keep math note `penalty_scale` name + add explicit note that current implementation maps penalty_scale → no-op (1.0) with stagnation handled by `STAGNATION_EPSILON = 0.001` directly + `MAX_SP_STEP_PER_ITERATION` handles SP step bounds
- [ ] Rocket judgment per which reads more clearly for future-rocket archaeology
- [ ] Per Discipline #1.2: math note code-line citations remain accurate post-amendment

### Amendment 4 — L4 INFO-B (math note VOTE_THRESHOLD sweep range expansion note)

- [ ] Amend math note Math 5 § Parameter 3 (VOTE_THRESHOLD) to:
  - Note sweep range expansion from dispatch [0.1, 0.5] to actual [0.01, 0.05, 0.10, 0.20, 0.50]
  - Rationale for downward expansion (e.g., empirical observation suggested lower thresholds may converge better; explore widened range; rocket fills in actual reasoning)
  - Confirm chosen value 0.05 was empirically-best per sweep results
- [ ] Per Discipline #17: sweep documentation must show range + outcomes for archaeology

### Cross-cutting

- [ ] No regression on existing engine code (re-run 270/270 + 175/175 + 374/374 if any amendment touches code; Amendment 1 + 3 + 4 are doc-only; Amendment 2 may touch code)
- [ ] AGENT_STATE.md updated at session end with amendment-batch checkpoint
- [ ] Auto-commit + auto-push per rocket seam authorization per CLAUDE.md addendum
- [ ] Tag: `rocket/v0.0-cycle-12-pre-layer-6-amendments-2026-05-25` (single tag covering all 4 amendments)
- [ ] Per-amendment commit OK (rocket discretion) OR single combined commit

---

## Out of scope

- Layer 6 dispatch authoring (KR fires immediately after this amendment batch lands)
- Other Gate-2 findings outside this 4-item batch
- New Layer 2/3/4 functionality (this is amendment-only; no new behavior)
- Cross-seam consumer code changes (star-lord/gamora/drax consumer-side updates are L6-or-later; this dispatch only updates MIGRATION.md to enable correct cross-seam consumption)
- Architectural amendments
- Performance benchmarking
- v1.1+ queue items

---

## Acceptance criteria

- [ ] Amendment 1 (L2 WARN-B MIGRATION.md field-name reconciliation) applied
- [ ] Amendment 2 (L2 WARN-C dead option_c_cells cleanup OR wire-up) applied per rocket decision (a) or (b)
- [ ] Amendment 3 (L4 INFO-A math note Math 5 § Parameter 1 naming reconciliation) applied
- [ ] Amendment 4 (L4 INFO-B math note VOTE_THRESHOLD sweep range note) applied
- [ ] If Amendment 2 chose Option (b): 28/28 Layer 2 tests + 374/374 regression re-run PASS
- [ ] If Amendment 2 chose Option (a): deferred-to-v1.1+ note captured in math note OR MIGRATION.md
- [ ] No regression on existing 270/270 Layer 4 tests or 175/175 combined L3+L4 tests
- [ ] AGENT_STATE.md updated
- [ ] Tag: `rocket/v0.0-cycle-12-pre-layer-6-amendments-2026-05-25`
- [ ] Auto-commit + auto-push per rocket seam

---

## Open questions for the agent to resolve

- WARN-C Amendment 2 decision (Option a remove vs Option b wire-up) — rocket judgment per implementation reality + canonical authority alignment
- INFO-A Amendment 3 approach (Option a rename math note vs Option b add functional-equivalence note) — rocket judgment per future-archaeology clarity
- Whether amendments ship as single combined commit OR per-amendment commits (rocket discretion)

---

## Cross-seam impact

Round-trip: not applicable for Amendment 1, 3, 4 (documentation amendments; no schema change; no fixture-dict shape change). Amendment 2 may touch code; if Option (b) wires Option C routing, regression smoke verifies no Layer 2 / cross-seam consumer breakage.

MIGRATION.md update is the canonical cross-seam communication for Amendment 1; downstream consumers (star-lord, drax, gamora at L6 wire-up time) read updated MIGRATION.md for correct field names.

---

## References

- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-1-rocket-layer-2.md` (WARN-B + WARN-C source)
- `agentic_orchestration/qa/findings/2026-05-25-gate2-cycle-12-wave-3-rocket-layer-4.md` (INFO-A + INFO-B source)
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-2-bc-target-subspace-generator.md`
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-12-layer-4-multi-dim-convergence.md`
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 3
- `agentic_orchestration/gandalf/notes/2026-05-25-comp-policy-section-4-coverage-gap-confirmation.md` (Cell 20 Holy Knight Option C context for WARN-C)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #1 + #13a + #17 + #25

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** KR autonomous in-scope decision per Cycle 12 scope-doc § 1 (Gate-2 amendment integration before downstream layer fires) + skip-confirmation re-auth 2026-05-25
**Status:** FIRE — pre-Layer-6 priority amendment batch; gates Layer 6 dispatch authoring

**Matt-touch sequence:** rocket amendments land → KR captures completion in state file → KR authors Layer 6 dispatch (§ 8 algorithm wire-up + L9 opportunity-scan refactor + cross-seam SC-3 obligations per Gate-2 on L3 INFO-D — star-lord off_hand_contract export + gamora sim combatant consumption + drax Spirit Guide panel) → Layer 6 fires per scope-doc § 1 autonomous + skip-confirmation re-auth
