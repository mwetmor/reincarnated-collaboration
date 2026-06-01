# Dispatch — Rocket — Cycle 14 Wave 5 Swift Closure: Path X — Phase 4 Archive Feeds Phase 5 PM-1 Input

**Date:** 2026-06-01
**From:** knight-rider (orchestrator)
**To:** rocket (engine content-generation + orchestrator seam — generation/, element/, anchor/, foundation/, `wave5_season_orchestrator.py`)
**Authority:**
- gandalf 2026-06-01 Gate (c) recognition-record-intent verdict at `agentic_orchestration/gandalf/notes/2026-06-01-gate-c-recognition-record-intent-verdict.md` (commit `05c1300` verdict; `900c0bc` sign-off ref)
- gandalf 2026-05-29 surface note at `agentic_orchestration/gandalf/notes/2026-05-29-phase-4-phase-5-disjoint-population-bug-surface.md` (Path X spec § 2 + lean § 3 + empirical-criterion gate § 3)
- gandalf 2026-06-01 recognition record at `canonical/story/2026-06-01-gauntlet-metrics-as-provisional-hypotheses-recognition.md` (commit `daa1c98`) § 4.2 structural-integrity preservation language
- gamora 2026-06-01 archive-stable signal at `agentic_orchestration/gamora/notes/2026-06-01-wave-5-swift-closure-archive-snapshot-stable.md` (commit `16ce0bf`) — 34 kit IDs enumerated as Path X target population
- Hive-mind decision-routing § 3.9 (Matt 2026-05-23 directive) — rocket decides within generation/orchestrator seam authority; cross-seam collaboration with gamora (Phase 4 archive owner) + star-lord (Phase 5 consumer) per § 3.9; Matt last-resort escalation
- CLAUDE.md auto-commit addendum 2026-05-25 — routine in-scope work-products of authorized cycle work auto-commit; push gates explicit Matt go

**Pattern:** B sustained-execution (~1-2h estimate per gandalf 2026-05-29 surface § 3 + verdict § 2 Q3; bounded structural fix at one code location)
**Sequencing:** UNBLOCKS star-lord Phase 5 cohesion judge dispatch (`agentic_orchestration/dispatches/2026-06-01-star-lord-cycle-14-wave-5-swift-closure-cohesion-judge-snapshot.md` Gate (c) CONDITIONAL)
**Pre-flight:** no LLM compute load (code-only fix); resource-bounds projection N/A (Discipline #1.1 — no compute-heavy fire); rocket can fire immediately on receipt
**Gate-2 post-output:** jack-ryan Gate-2 critique-pair review on tagged commit BEFORE star-lord re-engages (queued; KR routes after rocket completion record)

---

## 0. TL;DR

**Path X structural fix: change Phase 5 PM-1 input source from `passing_kits + variant_passing_rows` to Phase 4 archive Pareto-2 winners (34 mixed-sample kits per gamora's archive-stable signal).**

**Rationale (per gandalf 2026-06-01 verdict § 0/§ 1/§ 2 Q1):** the recognition record's "fire AS-IS" intent carries **metric-axis provisionality**, NOT structural-axis tolerance. § 4.2 of the recognition record explicitly preserves "engine architecture (the gauntlet structural sieve remains valid; the Pareto-2 reduction methodology remains valid; only the metric-axis validity is in question)." A Phase 5 cohesion judge clustering a population disjoint from the Phase 4 Pareto-2 archive does NOT cluster the wave-5 archive — it clusters a different artifact. PROVISIONAL markers cannot retroactively cover input-population mismatch (category error per verdict § 2 Q1).

**The fix in one paragraph:** at `wave5_season_orchestrator.py:825-836`, replace the existing assignment

```python
base_kit_datas = [_build_pm1_kit_data(k, k.character_id) for k in passing_kits]
variant_kit_datas = [_build_pm1_kit_data(vr, vr.character_id) for vr in variant_passing_rows]
surviving_kit_datas = base_kit_datas + variant_kit_datas  # PM-1 input
```

with consumption of the Phase 4 archive Pareto-2 winners (34 kits, mixed s0/s1/s2 samples) as Phase 5 PM-1 input. Architecture: Phase 4 archive → Phase 5 PM-1 → Phase 7 cohesion gate (kit_id join coherent across phases).

**What this dispatch IS:**
- Code change at `wave5_season_orchestrator.py:825-836` per gandalf 2026-05-29 surface § 2 Path X spec
- PM-1 sparsity branch verification at n=34 (k may drop 4 → 2 or 3 — expected and informative per gandalf § 3 caveat 1 + verdict § 2 Q3)
- 8-element BC-axis coverage preservation smoke (verification gate; not expected to fail)
- 5-10 new tests covering the Path X code path + sparsity branch + coverage check
- MIGRATION.md entry documenting cross-seam Phase 5 input-source change

**What this dispatch IS NOT:**
- NOT Path Y (variant emission extends s0/s1/s2 — deferred to Cycle 15+ canonical-write candidate per gandalf 2026-05-29 § 3 caveat 2)
- NOT Path Z (variants enter Phase 4 archive via Pareto-2 — deferred to Cycle 15+ per gandalf 2026-05-29 § 3 caveat 2)
- NOT a recognition-record amendment (recognition record § 4.2 structural-integrity language preserved; this fix MAKES empirical state match design intent)
- NOT Phase 5 cohesion judge execution (star-lord seam; re-fires post-Path-X-land per Gate (c) PASS unblock)
- NOT wave-close canonical write (jack-ryan seam; gates on star-lord Phase 5 close + Path X jack-ryan Gate-2)

**Effort:** ~1-2h.

---

## 1. Required first reads (in order)

1. `agentic_orchestration/gandalf/notes/2026-06-01-gate-c-recognition-record-intent-verdict.md` (commit `05c1300`) — AUTHORITATIVE design-intent verdict:
   - § 0 TL;DR (the verdict in three paragraphs)
   - § 1 re-reading recognition record in light of Gate (c) (load-bearing § 4.2 framing)
   - § 2 the four questions answered (Q1 Option 1 rejected; Q2 N/A; Q3 three empirical-criterion checks; Q4 separability mis-application)
   - § 3 why Option 2 over Option 1 — design-intent grounding (snapshot semantic preservation)
2. `agentic_orchestration/gandalf/notes/2026-05-29-phase-4-phase-5-disjoint-population-bug-surface.md` — AUTHORITATIVE Path X spec:
   - § 0 TL;DR (the bug surface in numbers — 80% disjoint populations at kit_id join)
   - § 1 architectural status (Interpretation A vs B; resolved via gandalf 2026-06-01 verdict as Interpretation B canonical for Cycle 14 v1)
   - § 2 Path X spec (specifically — what code change; what downstream)
   - § 3 gandalf-lean recommendation with caveats (PM-1 sparsity at n=34; variant Pareto deferred; 8-element coverage resolved)
3. `canonical/story/2026-06-01-gauntlet-metrics-as-provisional-hypotheses-recognition.md` (commit `daa1c98`) § 4.2 structural-integrity preservation language (load-bearing for understanding why Path X is wave-close prerequisite, not deferral)
4. `agentic_orchestration/gamora/notes/2026-06-01-wave-5-swift-closure-archive-snapshot-stable.md` (commit `16ce0bf`) — 34 kit IDs enumerated as Path X target population + Phase 4 archive file path `agentic_orchestration/cycle-14-wave-5-season-001/phase4_archive_insertion.json`
5. `agentic_orchestration/star-lord/notes/2026-06-01-wave-5-swift-closure-cohesion-judge-surface.md` (commit `6593626`) — pre-fire surface that triggered Gate (c) resolution; gates that unblock post-Path-X
6. Existing `reincarnated-engine/src/reincarnated/llm/wave5_season_orchestrator.py:825-836` — current `surviving_kit_datas` assignment (Path X target code path)
7. Existing `reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` — PM-1 sparsity branch implementation (verify behavior at n=34)
8. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 11 (empirical inspection — MANDATORY; inspect actual Phase 4 archive + verify 34 kit_id set matches gamora's enumeration), § 18 (methodology-before-execution — Path X spec is the methodology; gandalf-locked), § 41 (substrate-led — orthogonal to this fix per verdict § 2 Q4; not in scope to extend here), § 42a (framing-audit — applied to your own framing of the Path X fix)
9. rocket reincarnated-rocket-operating-procedure skill (universal session-start protocol)

---

## 2. Scope

### 2.1 Code change at `wave5_season_orchestrator.py:825-836`

Replace the current Phase 5 PM-1 input assembly with Phase 4 archive output consumption:

**Current (per gandalf 2026-05-29 surface § 0 root cause):**
```python
base_kit_datas = [_build_pm1_kit_data(k, k.character_id) for k in passing_kits]
variant_kit_datas = [_build_pm1_kit_data(vr, vr.character_id) for vr in variant_passing_rows]
surviving_kit_datas = base_kit_datas + variant_kit_datas  # PM-1 input
```

**Target (Path X — fire against Phase 4 archive Pareto-2 winners):**
- Read Phase 4 archive output (the same 34 kit_ids gamora enumerated in archive-stable signal) — typically via `kit_archive.db` query OR via `phase4_archive_insertion.json` consumption, whichever matches existing orchestrator data-access patterns
- Build PM-1 kit data via `_build_pm1_kit_data()` for each of the 34 Phase 4 accepted kits
- Result: `surviving_kit_datas` contains 34 mixed-sample (s0/s1/s2) entries matching the Pareto-2 archive identity
- Phase 5 PM-1 → PM-1 GMM clustering → cohesion judge consumption — all downstream of this assignment honors the new input

### 2.2 PM-1 sparsity branch verification at n=34

Per gandalf 2026-05-29 surface § 3 caveat 1 + verdict § 2 Q3 check (ii):
- PM-1 GMM currently selects k=4 with ~208-member input
- At n=34, k may drop to 2 or 3 — **this is EXPECTED and acceptable**
- Verify PM-1 sparsity branch HANDLES n=34 gracefully (no division-by-zero, no clustering failure, no NaN propagation)
- Document the empirical k value observed at n=34 in the smoke-test output

### 2.3 8-element BC-axis coverage smoke

Per gandalf 2026-05-29 surface § 3 caveat 3 + verdict § 2 Q3 check (iii):
- Phase 4 archive's 34 kits span all 8 elements per Amendment 7 verification (rocket engine commit `8d5be1b`)
- Post-Path-X, verify that Phase 5 PM-1 input preserves 8-element coverage
- If 8-element coverage degrades to <6 elements: surface as Path X regression to KR; re-evaluate Path Y or Hybrid X+Y (NOT expected; verification gate)
- If 8-element coverage preserves at ≥6 elements with reasonable distribution: PASS

### 2.4 New tests (5-10 per gandalf 2026-05-29 surface § 3 implementation cost)

Required test coverage:
- Path X assignment correctness: `surviving_kit_datas` length == 34; kit_id set matches Phase 4 archive's 34 (use gamora's enumerated kit_ids as fixture if convenient)
- PM-1 sparsity branch behavior at n=34: clusters return without exception; k value observed (whatever it is — assertion that it's in {2,3,4})
- 8-element coverage check: post-Path-X PM-1 input preserves 8-element coverage from Phase 4 archive
- Backward-compat smoke: existing Phase 5 orchestrator entry points work with new input source (no regressions in `run_phase5_async`, `run_phase5_with_fc_and_wave_b_async`)
- Wave A / F-C / Wave B reachability smoke: Phase 5 LLM call paths fire correctly against new input source (no mock LLM calls needed; just verify input plumbing reaches the call sites)

### 2.5 MIGRATION.md entry

Document cross-seam impact:
- Phase 5 input source changed from `passing_kits + variant_passing_rows` (~208 `_s2`-variant heavy) to Phase 4 archive Pareto-2 winners (34 mixed-sample)
- Downstream consumers (star-lord Phase 5 cohesion judge; rocket Cycle 15+ pattern library Phase A): Phase 5 clusters now describe wave-5 Pareto-2 archive identity rather than variant population identity
- Composition: star-lord Phase 5 dispatch (Gate (c) CONDITIONAL) is UNBLOCKED post-Path-X; jack-ryan Gate-2 fires on Path X before star-lord re-engages
- Effective date: 2026-06-01 wave-5 swift-closure direction

---

## 3. Math-before-code

NONE NEW. Path X is structural fix, not new mathematical primitives. Discipline #1 math-before-code N/A. PM-1 GMM methodology already canonical; sparsity branch already implemented; this dispatch verifies behavior at smaller n, not re-derive math.

**Discipline #1.2 math-note code-citation:** if existing PM-1 sparsity branch has a math-note, verify the n=34 case is within documented operational envelope. If not, surface to gandalf for math-note amendment as Cycle 15+ candidate.

---

## 4. Cross-seam contract change? (Principle 6 gate)

**Cross-seam impact assessment:**

Does this dispatch add, modify, rename, or remove any field on telemetry/fight_log/loadout/export-packet/inter-seam fixture?

**Answer:** YES — modifies the Phase 5 PM-1 input SOURCE (semantic, not schema). Specifically:
- Phase 5 PM-1 input population changes from `passing_kits + variant_passing_rows` to Phase 4 archive Pareto-2 winners
- Phase 5 cluster output (downstream: gamora Phase 7 cohesion gate + star-lord Wave A/F-C/Wave B emissions + rocket Cycle 15+ pattern library inputs) now describes wave-5 Pareto-2 archive identity rather than variant population identity
- No field-level schema additions; the change is semantic at the input-population layer
- Schema-level: existing `cluster_id` / `cohesion_data` fields unchanged; only their semantic content changes

**Round-trip smoke required:**
- Fixture: Phase 4 archive snapshot (the actual `phase4_archive_insertion.json` produced by gamora's wave-5 swift-closure) → Path X consumption → PM-1 cluster output
- Consumer boundary exercised: star-lord Phase 5 cohesion judge consumption + gamora Phase 7 cohesion gate consumption (kit_id join now coherent)
- Field-presence check: `surviving_kit_datas` populated with 34 entries; kit_id set matches Phase 4 archive; PM-1 sparsity branch returns clusters; 8-element coverage preserved; downstream entry points fire without exception

**MIGRATION.md required:** YES — per § 2.5 above.

---

## 5. Acceptance criteria

- [ ] Code change at `wave5_season_orchestrator.py:825-836` per § 2.1; `surviving_kit_datas` consumes Phase 4 archive Pareto-2 winners
- [ ] Empirical-criterion gate (i) — Disc #11: `surviving_kit_datas` length == 34 and kit_id set matches Phase 4 archive (verified against gamora's enumerated 34 kit_ids in archive-stable signal note)
- [ ] Empirical-criterion gate (ii) — PM-1 sparsity branch: PM-1 returns clusters without exception at n=34; k value observed and documented (expected k ∈ {2, 3, 4})
- [ ] Empirical-criterion gate (iii) — 8-element BC-axis coverage: post-Path-X Phase 5 PM-1 input preserves 8-element coverage from Phase 4 archive
- [ ] 5-10 new tests covering Path X correctness + sparsity branch + coverage check + backward-compat
- [ ] MIGRATION.md entry filed per § 2.5
- [ ] Round-trip smoke per § 4: Phase 4 archive fixture → Path X → PM-1 cluster output → downstream consumers do not regress
- [ ] AGENT_STATE.md updated at session end with Path X complete signal + empirical-criterion gate verdicts
- [ ] Coordination signal to star-lord re-engagement path: drop note at `agentic_orchestration/rocket/notes/2026-06-01-wave-5-swift-closure-path-x-complete.md` confirming Gate (c) CONDITIONAL now PASS
- [ ] Tag: `rocket/v1.1-cycle-14-wave-5-swift-closure-path-x-phase4-feeds-phase5-1`

---

## 6. Quality criterion

**Game-quality goal this dispatch serves:** preserve internal coherence of the wave-5 closure artifact set. Per gandalf verdict § 3.1, the recognition record's load-bearing word is "snapshot" — for snapshot semantics to be valid, the artifact set must be internally coherent. A wave-5 closure shipping Phase 4 archive AND Phase 5 cohesion clusters that describe disjoint populations is not a snapshot of one thing; it is two artifacts laminated together claiming a shared identity they don't have. Path X makes the empirical state match the design intent: Phase 4 archive identity propagates to Phase 5 cohesion clusters; downstream consumers (rocket pattern library Phase A; Cycle 15+ workstreams) read a coherent snapshot.

**Refutation conditions** (sub-agent surfaces if any apply before executing):
- This dispatch contradicts canonical anchor X — IF rocket finds Path X contradicts an architectural commitment in `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` (Phase 5 LLM prompts AUTHORITATIVE spec) or orchestrator-math doc, surface immediately to KR (KR consults gandalf if needed)
- Alternative execution Y serves the named quality goal better — IF rocket identifies a code refactor that achieves Phase 4 → Phase 5 coherence more cleanly (e.g., consumer-side rather than producer-side; or via existing orchestrator helper rather than direct archive read), surface as Gate-1-style consultation; KR consults gandalf if needed
- Acceptance criteria can pass without advancing the quality goal — IF rocket notices acceptance criteria can be met (`surviving_kit_datas == 34`) without actually preserving snapshot coherence (e.g., kit_ids match but cluster identity inheritance is broken at downstream consumer), flag for refinement
- Dispatch framing pre-commits to a decision Matt has not ratified — N/A; this dispatch operationalizes gandalf design-intent verdict (seam-owner decision per § 3.9); Matt ratification not required
- Dispatch introduces a pre-authored taxonomy without justification (#41 candidate) — N/A; Path X is structural fix, not taxonomy
- Dispatch introduces a scaffold value not flagged as pending-decision (#40) — N/A; no new scaffold values

**Engine first; Game second; Phase third (per CLAUDE.md orientation):** engine architectural integrity (Phase 4 → Phase 5 consumption contract correctness) > game-side cluster taxonomy ambition > phase-level swift-closure timeline. The orientation resolves: Path X is engine architectural integrity; ~1-2 day timeline extension is acceptable phase-level cost.

**CRITICAL — gandalf verdict is canonical design intent:** § 2 Q1 explicitly rejected Option 1 (fire-AS-IS-against-disjoint). Do NOT re-litigate that decision at the rocket execution layer; the design call is locked. If a substantive blocker emerges during execution (not a refinement question), surface to KR per refutation conditions above.

---

## 7. Out of scope (explicit non-goals)

- Path Y (variant emission extends s0/s1/s2) — deferred to Cycle 15+ canonical-write candidate per gandalf 2026-05-29 surface § 3 caveat 2
- Path Z (variants enter Phase 4 archive via Pareto-2) — deferred to Cycle 15+ per same
- Hybrid X+Y — NOT this dispatch (highest implementation cost; deferred unless Path X 8-element coverage smoke fails and re-evaluation surfaces)
- Wave B implementation work (S5 cascade-r3 closed; star-lord pre-fire gate (b) verified no drift)
- Phase 5 cohesion judge execution (star-lord seam; re-fires post-Path-X-land + jack-ryan Gate-2)
- Phase 6/7 sign-off (gamora seam; already complete per `gamora/v2.18-...` tag)
- Wave-close canonical write (jack-ryan seam; queued after star-lord Phase 5 close)
- Recognition-record amendment (recognition record stands as-is; Path X makes empirical match intent)
- Disc #41 amendment authorship (jack-ryan seam; queued post-wave-close)
- Math note amendment for PM-1 sparsity at n=34 (gandalf seam; surface IF the n=34 case falls outside existing math-note operational envelope)

---

## 8. Open questions for rocket to resolve

- (Q1 — rocket seam decides per § 3.9): exact data-access pattern for reading Phase 4 archive output — direct `kit_archive.db` query vs `phase4_archive_insertion.json` parse vs existing orchestrator helper. rocket has authority to choose; favor consistency with existing wave5_season_orchestrator data access.
- (Q2 — empirical observation): PM-1 sparsity branch behavior at n=34 — record observed k value in completion record. If k=1 (degenerate cluster), surface as unexpected; if k ∈ {2, 3, 4}, document as observed and proceed.
- (Q3 — cross-seam coordination): if Q1 data-access pattern requires gamora coordination (e.g., kit_archive.db schema clarification), invoke gamora parallel sub-agent per § 3.9. Do NOT escalate to Matt unless cross-seam collaboration cannot resolve.
- (Q4 — Path X composition with future Amendment 7a-style work): if rocket finds Path X composes cleanly with deferred amendments still in flight, document the composition path in MIGRATION.md for downstream Cycle 15+ reference.

---

## 9. References

- `agentic_orchestration/gandalf/notes/2026-06-01-gate-c-recognition-record-intent-verdict.md` (AUTHORITATIVE design-intent; commits `05c1300` + `900c0bc`)
- `agentic_orchestration/gandalf/notes/2026-05-29-phase-4-phase-5-disjoint-population-bug-surface.md` (Path X spec source)
- `canonical/story/2026-06-01-gauntlet-metrics-as-provisional-hypotheses-recognition.md` (commit `daa1c98`) § 4.2 structural-integrity preservation
- `agentic_orchestration/gamora/notes/2026-06-01-wave-5-swift-closure-archive-snapshot-stable.md` (commit `16ce0bf`) — 34 kit IDs enumerated; Phase 4 archive `phase4_archive_insertion.json`
- `agentic_orchestration/star-lord/notes/2026-06-01-wave-5-swift-closure-cohesion-judge-surface.md` (commit `6593626`) — Gate (c) CONDITIONAL surface; unblocks post-Path-X
- `agentic_orchestration/cycle-14-hive-mind-state.md` § 1 Wave 5 row (KR will amend post-Path-X-completion-record)
- `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` (Phase 5 LLM prompts AUTHORITATIVE; downstream of Path X — Path X does not amend this canon)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 11 / § 18 / § 41 / § 42a / § 1.2
- rocket Amendment 7 commit `8d5be1b` (8-element coverage verification baseline)
- Companion dispatches (in flight): gamora `v2.18-...` (COMPLETE); star-lord `cohesion-judge-snapshot` (Gate (c) CONDITIONAL — UNBLOCKED on Path X completion)

---

**Authored by:** knight-rider (orchestrator) per gandalf 2026-06-01 Gate (c) verdict + 2026-05-29 Path X spec + hive-mind § 3.9 seam-owner decision routing
