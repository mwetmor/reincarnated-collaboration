# Dispatch — 2026-05-25 — jack-ryan — Cycle 12 Gate-1 critique on interface contract (framing brief § 4)

**From:** knight-rider
**To:** jack-ryan (DESIGN-MODE — Gate-1 peer collaborator)
**Approved by:** Matt 2026-05-25 (Cycle 12 framing brief bulk-ratification — interface contract § 4 LOCKED as-drafted; KR autonomously orchestrates Gate-1 per scope-doc § 1)
**Estimated effort:** ~1 day jack-ryan
**Acceptance:** Gate-1 findings file at `agentic_orchestration/qa/findings/2026-05-25-gate1-cycle-12-interface-contract.md` reviewing framing brief § 4 contract for soundness + completeness; per principle severity classification (INFO / WARN / BLOCK) per REVIEW_PROCESS.md; rocket Layer 2 + Layer 3 dispatches CANNOT fire until Gate-1 clears

---

## Context

Cycle 12 (full new engine parallel-build per Option γ) opens with rocket parallel-firing Layer 2 (kit identity — BC-target subspace generator) and Layer 3 (skill content — trees + nodes + T4 slots + off-hand mechanical contract per SC-3) per framing brief § 8 sequencing. Per Q4 Option B ratification (contract-first then parallel), Layer 2 + Layer 3 share an INTERFACE CONTRACT — the framing brief § 4 PlayerClass + SkillTree + Skill + ConvergenceResult + Layer 6 wire-up contracts.

Matt RATIFIED the interface contract § 4 as-drafted per "Approve all gandalf recommendations + contract as-drafted." The contract is LOCKED for rocket consumption. BUT per Q2 Option B ratification, jack-ryan Gate-1 reviews the contract for soundness + completeness BEFORE rocket dispatches fire. This is the critique-pair gate per REVIEW_PROCESS.md — gandalf authored the contract; jack-ryan reviews for engineering rigor.

Cycle 12 fires in parallel with Cycle 11 close. Jack-ryan Gate-1 fires concurrently with legolas MC-1/MC-2 + elrond SC-1/SC-2 + Cycle 11 close drax Wave 3b. No specialist contention.

---

## Required reading before starting

- `canonical/00-ground-state.md` § 1
- **`agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md`** § 4 (interface contract — primary review target) + § 1 L1-L11 (canon basis for contract; especially L9 substrate split + L11 strict 4-tuple matching) + § 2 (scope context — what each layer produces) + § 3 Q-items (esp. Q2 contract authoring, Q3 AUGMENT pattern, Q4 parallel sequencing)
- **`agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`** (Cycle 12 scope statement + workstream roster + escape hatches)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` (Architecture B end-to-end workflow; PlayerClass shape in Phase 2 substrate-binding context)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (substrate composition policy; cell-match references)
- `canonical/story/skill-system-2026-05-24.md` (SkillTree + Skill + T4 references; § 8 Algorithm § 8 architecture for Layer 6 wire-up; § 9 spirit-guide explainer)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 (ConvergenceResult contract source)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` (T4-A architecture — T4Candidate + T4Slot + T4Alteration shape)
- `canonical/story/off-hand-items-2026-05-24.md` (Main/Secondary architecture — off_hand_item field on PlayerClass)
- `canonical/story/attribute-system-2026-05-24.md` (STR/INT/WIS/DEX — primary_stat + secondary_stat fields)
- `agentic_orchestration/REVIEW_PROCESS.md` (5 review principles + cross-seam round-trip + finding-file format + severity classification INFO/WARN/BLOCK)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (full 20-discipline canon — Gate-1 surfaces discipline citation triggers)
- Precedent Gate-1 finding files for shape reference: `agentic_orchestration/qa/findings/` recent entries (2026-05-25 Stage 3.5 gap-fill; 2026-05-23 phase-D dispatch)

---

## Math-before-code (per Discipline #1)

No code in this dispatch — Gate-1 critique-pair review only. But jack-ryan should specifically surface whether the contract honors Discipline #1 expectations for downstream Layer 2/3/4/6 implementation:

- Does the contract include enough type/shape information for math-note-bearing implementation? (e.g., is `bc_axis_contribution: list[float]` per-Skill specified clearly enough for rocket to math-note it before implementing?)
- Does the contract expose Discipline #1 substrate (math-before-code requirements explicit in the contract field semantics)?
- Does the contract surface Discipline #25 semantic-layer rep-audit hooks (mechanical vs semantic fields explicitly flagged per L9 substrate split)?

---

## Scope (jack-ryan DESIGN-MODE Gate-1 review)

Per REVIEW_PROCESS.md 5 principles + critique-pair Gate-1 protocol, jack-ryan reviews framing brief § 4 interface contract for:

### Principle 1 — Soundness against canonical authority

- Does PlayerClass field set match qd-engine-end-to-end-workflow § Phase 2 substrate-binding spec?
- Does PlayerClass `mechanical_substrate_triple` field correctly capture L9 mechanical-only substrate (no cultural_tradition / lineage / period leakage into mechanical-layer)?
- Does `cultural_tradition`, `lineage`, `period` placement on PlayerClass correctly flag them as semantic-overlay-only (NOT in BDI math model per L9)?
- Does SkillTree shape match skill-system-2026-05-24 + W1.13 dispatch § 3.1 invariants (chains with Tier 1 playability; topology validity)?
- Does ConvergenceResult shape match multi-dim-convergence-algorithm-2026-05-21 v1.1 (5-6 dimensions + tier-specific coefficients)?
- Does Layer 6 wire-up signature (`apply_t4_alteration_to_combat`) match skill-system § 8 Algorithm § 8 architecture + L9 opportunity-scan refactor requirement (mechanical signals, not cultural_tradition heuristics)?

### Principle 2 — Completeness for parallel L2 + L3 work

- Does the contract include all fields Layer 2 must EMIT for Layer 3 to consume? (e.g., does Layer 3 know how to walk the skill_tree fields if Layer 2 hasn't populated them yet)
- Does the contract include all fields Layer 3 must EMIT for Layer 4 to consume? (e.g., does Layer 4 know how to read skill_tree + t4_candidates for multi-dim convergence)
- Does the contract include all fields Layer 4 must EMIT for Layer 6 to consume? (e.g., does Layer 6 know how to read stat_allocation + attribute_coupling + converged_modifier)
- Are nullable fields explicitly flagged with `Optional[...]` shape vs not-nullable fields?
- Is `t4_alteration_output: Optional[T4Alteration]` correctly marked as nullable per Cycle 11 § 8 BC-shift FAIL convergence (some kits won't have alteration; ETA_FLOOR may not be cleared)?

### Principle 3 — Cross-seam round-trip readiness per Principle 6

- Does the contract permit round-trip smoke (PlayerClass serializes through star-lord JSON export, deserializes back to PlayerClass)?
- Does the contract avoid serialization-hostile shapes (e.g., circular references, non-serializable types like Optional[FunctionType])?
- Is the source_library field semantics clear (e.g., does it map to existing `source_library` from Cycle 11 star-lord schema extensions or a new value)?
- Does the contract include MIGRATION.md trigger conditions per ADR-004?

### Principle 4 — Engineering-disciplines compliance

- Does the contract support Discipline #1 math-before-code (math hotspots are math-note-able)?
- Does the contract support Discipline #18 + #18.2 methodology-before-execution (MC-1 + MC-2 + MC-3 outputs land naturally as contract-implementing functions)?
- Does the contract support Discipline #19 background-process patterns (rocket can fire L2/L3/L4 implementation in background per long-rocket-runs pattern)?
- Does the contract support Discipline #25 semantic-layer rep-audit (mechanical vs semantic boundary is auditable from field structure alone)?

### Principle 5 — Severity classification per REVIEW_PROCESS.md

For each finding, classify as:
- **INFO** — observation; no change required
- **WARN** — recommended change but not blocking
- **BLOCK** — change required before rocket L2/L3 dispatches can fire

Per scope-doc § 5 escape-hatch: if jack-ryan surfaces BLOCK on interface contract, KR routes to gandalf sub-agent for design-fit, then escalates Matt for ratification if amendment required.

### Cross-cutting

- **Q3 AUGMENT pattern compatibility** — does the contract support legacy ClassGenerator producing the SAME PlayerClass shape (so AUGMENT works; both generators emit identical shape)?
- **L11 strict 4-tuple matching** — does the contract correctly enforce strict matching (e.g., is bc_target_cell typed strictly enough that loose-matching cannot accidentally leak)?
- **§ 8 algorithm wire-up via Layer 6** — does the contract's `t4_alteration_output` field structure permit Layer 6 wire-up (`apply_t4_alteration_to_combat`) to consume it without schema amendment?
- **Off-hand mechanical contract (SC-3)** — does the `off_hand_item` field correctly accommodate SC-3 off-hand mechanical contract design (buff/aura/proxy effects for banner/focus/talisman/tome/horn)?

---

## Out of scope

- Direct rocket implementation work (Gate-1 is critique-only)
- Architectural amendment to contract (jack-ryan recommends; gandalf authors amendments; Matt ratifies per scope-doc § 5)
- Layer 4 / Layer 6 detailed math review (those fire after L2+L3 land; Gate-1 is contract-level, not algorithm-level)
- Methodology recommendation for MC-1/MC-2 (legolas Mode A consults are separate dispatches)
- Engine code changes
- Test infrastructure design (Layer 7 BDI test framework deferred to v1.1 per scope-doc § 0)

---

## Acceptance criteria

- [ ] Gate-1 findings file authored at `agentic_orchestration/qa/findings/2026-05-25-gate1-cycle-12-interface-contract.md`
- [ ] Per-principle review (5 principles + cross-cutting) covered
- [ ] Each finding classified INFO / WARN / BLOCK per REVIEW_PROCESS.md severity rubric
- [ ] Final verdict: CLEAR (rocket L2/L3 dispatches may fire) / CLEAR-WITH-AMENDMENTS (KR integrates non-blocking warnings before fire) / BLOCK (gandalf design-fit + Matt escalation required before fire)
- [ ] Cross-references to canonical sources (framing brief § 4 + supporting canonical docs)
- [ ] Discipline citations explicit for each finding (which discipline triggered the finding)
- [ ] Auto-commit + auto-push per jack-ryan seam authorization
- [ ] Tag: `jack-ryan/cycle-12-gate-1-interface-contract-2026-05-25`

---

## Open questions for the agent to resolve

- Whether contract should require Layer 6 wire-up signature to include `fight_engine_context: FightEngineContext` (as drafted) or a narrower type (jack-ryan judgment on sim-seam boundary; if narrower, flag for gandalf design-fit)
- Whether `generation_seed: int` + `generation_params: dict` should be required-not-nullable for reproducibility (jack-ryan judgment per Discipline #1 reproducibility expectations)
- Whether `t4_candidates: list[T4Candidate]` should be capped at a max length (jack-ryan judgment per per-chain coverage from skill-system + W1.13 dispatch § 3.1)
- Whether the contract should include an explicit `engine_version: str` field for downstream provenance + future schema migration (per Cycle 10 Sidecar A telemetry-gap finding — `engine_version unknown` was surfaced as gap)
- Whether `mechanical_substrate_triple: tuple[str, str, str]` shape is right (should it be a more structured type — e.g., MechanicalSubstrateTriple dataclass — for type safety + future extension)

---

## Cross-seam impact

Round-trip: not applicable — Gate-1 critique-pair review only; no production code; no schema changes; no cross-seam contract change. Findings inform downstream rocket L2/L3 dispatches which WILL have round-trip per Principle 6 (rocket L2 emits PlayerClass; star-lord serializes to JSON; loadout consumes — round-trip required at L2/L3 dispatch level).

If jack-ryan surfaces contract amendment, that's escape-hatch territory (per scope-doc § 5) — KR routes to gandalf + Matt before rocket fires.

---

## References

- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4 (primary review target)
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `agentic_orchestration/REVIEW_PROCESS.md` (5 review principles + severity rubric + finding-file format)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`
- `canonical/story/skill-system-2026-05-24.md` § 8 + § 9 + § 12 + § 13
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md`
- `canonical/story/off-hand-items-2026-05-24.md`
- `canonical/story/attribute-system-2026-05-24.md`
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q2 Option B pre-authored contract + Gate-1 critique-pair pattern + Q4 Option B parallel-after-Gate-1 sequencing); KR autonomously orchestrates Gate-1 per scope-doc § 1
**Status:** FIRE — Day-1 parallel-fire with legolas MC-1 + MC-2 + elrond SC-1/SC-2 + Cycle 11 close drax Wave 3b; gates rocket L2 + L3 dispatch authoring

**Matt-touch sequence:** Gate-1 findings → if CLEAR (or CLEAR-WITH-AMENDMENTS), KR integrates + authors rocket L2 + L3 dispatches when MC-1+MC-2 also land; if BLOCK surfaced, KR routes to gandalf sub-agent for design-fit + escalates Matt for contract amendment per scope-doc § 5
