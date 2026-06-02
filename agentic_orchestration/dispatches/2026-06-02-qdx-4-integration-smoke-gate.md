# Dispatch — 2026-06-02 — QDX-4 — Integration-smoke-gate (LOCK S; Discipline #54)

**From:** knight-rider (orchestrator)
**To:** rocket (PRIMARY — fire the non-physical-primary smoke through the composed Phase 1 pipeline) + jack-ryan (PRIMARY — Gate-2 verification per 7-criteria checklist on QDX-1+QDX-2+QDX-3 outputs + the QDX-4 smoke output)
**Authority:** Matt 2026-06-02 QDX chain Locks A-P preserved + LOCK Q (ADDITIVE-ONLY integration) + LOCK R (fire parameters bounded) + LOCK S (integration-smoke-gate per Discipline #54)
**Wave:** cycle-17 QDX QD-Engine Re-Fire — Phase 2 (gates on Phase 1 PASS achieved)
**State file:** `agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`
**Estimated horizon:** ~0.5-1 session

---

## 1. Why this dispatch exists

QDX-3's self-smoke (commit `cf6e9ae`) fired the composed pipeline end-to-end but its substrate happened to be physical-only — which opts out of WS1A.4-lite per Architecture A. The smoke verified phase composition + FK linkage + Wave B non-template emergent identity + T4 narration, but did NOT empirically verify WS1A.4-lite per-skill metadata flowing through the composed pipeline (variety check MARGINAL).

QDX-4 fires a fresh smoke with a NON-PHYSICAL primary to satisfy:
- 7-criteria checklist item 5 (`ws1a4_flavor_rate > 0`; per-skill `ws1a4_*` metadata present)
- 7-criteria checklist item 7 (Per-skill flavor decisions thematically coherent; sample inspection)

QDX-4 also COMPOSES with jack-ryan's formal Gate-2 review of QDX-1+QDX-2+QDX-3 outputs (commits `76adb6e`, `9fba775`, `cf6e9ae`) — one unified Gate-2 finding covering Phase 1 outputs + QDX-4 smoke output verifies LOCK S smoke-gate per Discipline #54.

On QDX-4 PASS → Phase 2 closes → KR routes Phase 3 (QDX-5 full fire + QDX-6 Gate-2 acceptance verification).

---

## 2. Authoritative reading

1. **`agentic_orchestration/cycle-17-qdx-qd-engine-re-fire/wave-state.md`** § 2 Phase 1 status (all PASS; QDX-3 INFO disposition)
2. **`canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md`** § 1 (phase composition)
3. **`canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md`** § 3.2 (per-skill flavor-or-canonical naming)
4. **`canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`** § 2 (Q18 vocabulary per primary)
5. **`~/Games/reincarnated-engine/scripts/qdx_qd_engine_re_fire_20260602.py`** (the fire script tagged at `cf6e9ae`)
6. **Phase 1 engine commits:** `76adb6e` (QDX-1 ws1a4 Phase 5 wiring) + `9fba775` (QDX-2 terminal-phase routing) + `cf6e9ae` (QDX-3 fire script + 7 smoke bug fixes)
7. **Phase 1 dispatch completion records** (appended at `dispatches/2026-06-02-qdx-{1,2,3}-*.md` § completion record block)
8. **`~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`** Discipline #54 (Integration-smoke-gate)

---

## 3. Workstream A — rocket fires the QDX-4 LOCK S smoke

### 3.1 Scope

Re-fire the QDX-3 fire script (`scripts/qdx_qd_engine_re_fire_20260602.py`) in `--smoke` mode (or equivalent single-kit mode) — FORCING a non-physical primary element (e.g., shadow). The goal: satisfy WS1A.4-lite variety check empirically through the composed pipeline.

### 3.2 Fire parameters (LOCK R-bounded; for QDX-4 smoke specifically)

```python
# QDX-4 smoke parameters (per LOCK S formal smoke-gate)
SMOKE_MODE = True
SMOKE_FORCE_NON_PHYSICAL = True       # NEW for QDX-4 — force shadow / fire / water / earth / etc.
SMOKE_PRIMARY = "shadow"              # KR-suggested; rocket may use any non-physical primary
SEED = 20260602                       # match QDX-3 self-smoke for reproducibility
N_CANDIDATES_SMOKE = 2-5              # single-kit smoke equivalent
COST_BOUND = 0.10                     # ≤ $0.10 per LOCK S smoke
WALL_CLOCK_BOUND_MIN = 5              # ≤ 5 min per LOCK S smoke
```

If the fire script's existing `--smoke` flow doesn't naturally produce non-physical (because of substrate cell selection logic), rocket has authority per LOCK Q ADDITIVE-ONLY to:
- Add a `--force-primary <elem>` flag to the script (additive parameter; doesn't change default behavior), OR
- Run a one-off Python invocation with the smoke parameters constructed inline, OR
- Adjust the substrate cell selection in --smoke mode to bias toward non-physical for QDX-4 verification

Whichever path is simplest. Document the approach in completion record.

### 3.3 Smoke acceptance criteria

The QDX-4 smoke MUST verify:

1. **Pipeline composition end-to-end** — Phase 1 → 2 → 4 → 5(a/b/c) → Wave A → Wave B → 7 → 8 in canonical 39 order. Per-phase logs as in QDX-3 smoke output.

2. **WS1A.4-lite variety on non-physical primary** — `ws1a4_flavor_rate > 0` AND `ws1a4_flavor_rate < 1.0` (at least one flavor=True AND at least one flavor=False in the smoke kit's skills). Per-skill `ws1a4_*` metadata populated on the emitted kit JSON.

3. **Q18 pool validation** — when `ws1a4_flavor=True`, the flavor word selected belongs to the kit's primary element's Q18 pool per `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` § 2.

4. **Non-template Wave B emergent identity** — emergent kit name is NOT "{Element} {Archetype}" generic (e.g., NOT "Shadow Necromancer", NOT "Shadow Caster"). Some emergent richness expected (e.g., "Necromancer of the Pale Court", "Wraith-Binder of [tradition]"). If template-repeat detected on the smoke kit, this is BLOCK-class signal (Wave B prompt design failure) → LOCK L 1st BLOCK iteration.

5. **Multi-T4 selection populated** — `t4_selection` field not null; T4 narration ran.

6. **kit_space emit verified** — kit JSON lands at `data/kit_space/kits/kit_<primary>_<seq6>.json`; chronicle event appended; FK linkage `kit.kit_space_expansion_event_id == chronicle event_id`.

7. **Cost + wall-clock bounds** — `total_llm_cost ≤ $0.10` (LOCK S smoke bound); `wall_clock ≤ 5 min`. ABORT if cost projection exceeds $0.10 at startup.

### 3.4 Smoke output structure (expected illustrative)

```
=== QDX-4 LOCK S Integration-Smoke-Gate (non-physical primary forced) ===
Pre-fire resource-bounds projection:
  primary forced: shadow
  projected LLM cost: $0.05 (≤$0.10 bound)
  projected wall-clock: ~2 min
[PASS: pre-fire bounds]

=== Phase 1 — Archive state inspection ===
BC-target queue: 1 cell (shadow primary)
[OK]

=== Phase 2 — Candidate generation ===
n_candidates=2 generated
[OK]

=== Phase 4 — Pareto reduction ===
1 kit surviving
[OK]

=== Phase 5a — Cohesion clustering ===
1 cluster (smoke)
[OK]

=== Phase 5b — Skill naming (ws1a4_active=True) ===
skills_named: 6
ws1a4_flavor_decisions: True=3, False=3 [variety check PASS]
Q18 pool validation: all flavor_words from shadow allow-list [PASS]
[OK]

=== Phase 5c — T4 narration ===
t4_selection populated [PASS]
[OK]

=== Wave A — Faction naming ===
1 faction: "Pale Court Ascendants"
[OK]

=== Wave B — Per-kit emergent identity ===
"Necromancer of the Pale Court" [non-template PASS]
[OK]

=== Phase 7 — Gate (2-LAYER) ===
mechanical PASS; cohesion PASS
[OK]

=== Phase 8 — Emit ===
event_id: kse_20260602_006
kit JSON: data/kit_space/kits/kit_shadow_000027.json
chronicle entry written; FK linkage verified
[OK]

=== QDX-4 LOCK S Smoke COMPLETE ===
wall_clock: 1.8 min (≤5 min PASS)
llm_cost: $0.048 (≤$0.10 PASS)
```

### 3.5 Tag intent

`rocket/v1.5-qdx-4-lock-s-smoke-1` (if any script amendment); OR no new tag if just a re-run of existing fire script with environment override.

### 3.6 Auto-commit + push

Per CLAUDE.md team commit + push discipline (rocket auto-commit pattern: cycle work-products of authorized authorized cycle). Push per cycle-push pattern.

---

## 4. Workstream B — jack-ryan Gate-2 unified review

### 4.1 Scope

Single unified Gate-2 finding at `agentic_orchestration/qa/findings/2026-06-02-qdx-phase-1-phase-2-gate-2.md` covering:

- **QDX-1 output** (engine commit `76adb6e`) — backward-compat verified; ws1a4 active path; physical opt-out; cost telemetry composes
- **QDX-2 output** (engine commit `9fba775`) — new function additive; both paths verified; emit-order preserved; MIGRATION.md both seams
- **QDX-3 output** (engine commit `cf6e9ae`) — fire script composition + 7 smoke bug fixes + dependencies verified
- **QDX-4 LOCK S smoke output** (when fired by rocket; engine artifact at `data/kit_space/kits/kit_<primary>_<seq6>.json` + chronicle event entry) — variety check satisfied empirically

### 4.2 7-criteria smoke checklist (LOCK S verification)

Per wave-state file § 6 acceptance verification + LOCK S:

1. Kit count in 30-40 range (relaxed to ≥1 for smoke)
2. Distinct emergent kit identities (no template-repeat across kits sharing primary)
3. Faction emergence ≥3 named clusters (≥1 for smoke)
4. Multi-T4 selection populated on all kits (`t4_selection` not null)
5. `ws1a4_flavor_rate > 0`; per-skill `ws1a4_*` metadata present on non-physical kits
6. Substrate-led element distribution (not round-robin; reflects substrate composition)
7. Per-skill flavor decisions thematically coherent (sample inspection: flavor words match expected pool; canonical naming reads as canonical)

### 4.3 Gate-2 findings format

For each of QDX-1, QDX-2, QDX-3, QDX-4 emit one verdict block:
- Verdict: PASS / PASS-with-INFO / BLOCK
- INFO/WARN/BLOCK list with line citations to engine commits
- Remediation suggestion if INFO/WARN

### 4.4 Disposition of Gate-1 INFOs

Verify Gate-1 INFOs from finding `9f5c01d` have been addressed (or carry-forward to next-touch):
- QDX-1 INFO 1-1: backward-compat regression test "semantically-identical" definition — verify test concreteness
- QDX-2 INFO 2-1: generation/MIGRATION.md entry if generation-side code touched — verify (star-lord added)
- QDX-3 INFO 3-2: pre-fire cost projection methodology (pre-Pareto upper bound vs post-Phase-4 actuals) — verify
- Gate-1 W-1 (QDX-3): docstring clarity on Phase 3 sim embedding/skip — verify

### 4.5 LOCK L iteration if BLOCK

If Gate-2 BLOCKs on any of QDX-1/2/3/4, LOCK L iteration discipline applies:
- 1st BLOCK on any single workstream → seam re-fires within authority (no Matt-touch)
- 2+ BLOCKs accumulate → Matt escalation per LOCK L escape clause
- Currently 0 BLOCKs across QDX chain (Gate-1 PASS-with-INFO, QDX-1/2/3 PASS or PASS-with-INFO)

### 4.6 Tag intent + commit

`jack-ryan/v1.5-qdx-phase-1-phase-2-gate-2-1` (or no tag; auto-commit finding file per critique-pair pattern). Auto-commit + push per CLAUDE.md jack-ryan auto-commit pattern.

---

## 5. Quality criterion

**Game-quality goal this dispatch serves:** verify (empirically) that the QDX-1+QDX-2+QDX-3 composition produces the architectural richness Matt's chain-close goal requires — specifically that WS1A.4-lite per-skill flavor naming flows through the composed pipeline when the substrate happens to include non-physical primaries. The QDX-3 self-smoke gave us phase composition + Wave B + T4 confidence; QDX-4 closes the WS1A.4-lite empirical loop.

**Refutation conditions** (sub-agents surface if any apply):
- QDX-4 smoke contradicts a Gate-2 finding on QDX-1/2/3 (signals integration regression)
- QDX-4 smoke produces ws1a4_flavor_rate=0 OR ws1a4_flavor_rate=1.0 on non-physical primary (signals WS1A.4-lite prompt design issue → LOCK L iteration on prompt)
- QDX-4 smoke Wave B produces template-repeat ("Shadow Necromancer" etc.) (signals Wave B prompt design issue → LOCK L iteration)
- QDX-4 smoke FK linkage broken (signals emit pipeline regression)
- Acceptance criteria can pass without advancing the quality goal (e.g., variety check PASSes but flavor words are obviously non-thematic / off-genre)

---

## 6. Required completion record

On work-completion, BOTH workstreams append a completion record to this dispatch file:

```markdown
## Completion record — Workstream A (rocket QDX-4 smoke)

**Fired by:** rocket (date)
**Engine commit / re-run:** <SHA or "re-run of cf6e9ae"> with smoke parameters
**Smoke output:** <paste full smoke output>
**Variety check:** PASS / FAIL (ws1a4_flavor_rate value)
**Q18 pool validation:** PASS / FAIL
**Wave B non-template check:** PASS / FAIL (emergent identity name)
**FK linkage:** PASS / FAIL
**Cost + wall-clock vs bounds:** $<x> / <y> min (vs $0.10 / 5 min)
**Smoke kit JSON path:** <data/kit_space/kits/kit_<primary>_<seq6>.json>
**Chronicle event_id:** <kse_20260602_NNN>
**Path used:** --smoke + force-primary / --smoke + bias / inline / other

## Completion record — Workstream B (jack-ryan Gate-2 unified)

**Completed by:** jack-ryan (date)
**Finding file:** `qa/findings/2026-06-02-qdx-phase-1-phase-2-gate-2.md`
**Commit:** <SHA>
**Per-workstream verdicts:** QDX-1 / QDX-2 / QDX-3 / QDX-4 each (PASS / PASS-with-INFO / BLOCK)
**LOCK S 7-criteria checklist:** <each item PASS/FAIL/MARGINAL with note>
**Gate-1 INFO disposition:** <addressed / carry-forward / new INFO>
**BLOCKs accumulated:** <count; 2+ = Matt escalation>
**Phase 3 routing clearance:** YES / NO
```

---

**End of QDX-4 dispatch.**

---

## Completion record — Workstream B (jack-ryan Gate-2 unified)

**Completed by:** jack-ryan (2026-06-02)
**Finding file:** `qa/findings/2026-06-02-qdx-phase-1-phase-2-gate-2.md`
**Commit:** (see git log)
**Per-workstream verdicts:**
- QDX-1: PASS-with-INFO (INFO 1-2 carry-forward: EAA-1 wrapper test gap; no BLOCKs)
- QDX-2: PASS (all criteria met; Gate-1 INFO 2-1 dual-MIGRATION.md closed)
- QDX-3: PASS-with-INFO (INFO 3-A Wave A escalation path carry-forward; Gate-1 INFOs W-1 + 3-2 closed)
- QDX-4: PENDING (rocket Workstream A not landed; criteria 5-7 unverified; chronicle at kse_20260602_005; no non-physical smoke kit on disk)

**LOCK S 7-criteria checklist (partial — QDX-4 pending):**
1. Kit count ≥1: PASS (QDX-3 smoke: 2 kits)
2. Distinct emergent kit identities: PASS (Wave B non-template confirmed in QDX-3 smoke)
3. Faction emergence ≥1: PASS (QDX-3 smoke: "Null Convergence Drift")
4. t4_selection not null: PASS (QDX-3 smoke: 2/2 kits narrated)
5. ws1a4_flavor_rate > 0; per-skill ws1a4_* metadata: PENDING (QDX-4 required)
6. Substrate-led element non-physical: PENDING (QDX-4 required)
7. Per-skill flavor coherence (sample inspection): PENDING (QDX-4 required)

**Gate-1 INFO disposition:**
- INFO W-1: CLOSED (Phase 3 docstring present in QDX-3 script)
- INFO W-2: CLOSED (n_candidates scaffold documented; LOCK R operative)
- INFO 1-1: CLOSED (test uses concrete structural assertions, not vague "semantically-identical")
- INFO 1-2: CARRY-FORWARD (MIGRATION.md consumer table documents; no explicit test added)
- INFO 2-1: CLOSED (both export/MIGRATION.md + generation/MIGRATION.md present)
- INFO 3-1: CARRY-FORWARD (Wave A escalation path implicit under LOCK L; no separate escape clause written)
- INFO 3-2: CLOSED (pre-fire projection uses PARETO_TARGET at startup; conservative and correct)

**BLOCKs accumulated:** 0
**Phase 3 routing clearance:** CONDITIONAL YES (clears on QDX-4 LOCK S smoke PASS + criteria 5-7 verification)
