# Dispatch — 2026-05-25 — legolas — Cycle 12 MC-2 substrate-binding heuristics consult

**From:** knight-rider
**To:** legolas (Mode A — analytical research; read-only)
**Approved by:** Matt 2026-05-25 (Cycle 12 framing brief bulk-ratification — "Let's move ahead with it"; Q6 Option B substrate-led methodology consultation timing — MC-2 fires at Cycle 12 open in parallel with MC-1)
**Estimated effort:** ~1-2 days legolas Mode A (parallel with MC-1)
**Acceptance:** Methodology recommendation memo authored at `agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md` covering kit's mechanical_substrate_triple choice from v1_scope per cell-match + thin-cell-fallback heuristics; cheapest-refuting-test design; resource-bounds projection; sources cited

---

## Context

Cycle 12 Layer 2 (kit identity — BC-target subspace generator per framing brief § 2 + § 4 PlayerClass contract) is a load-bearing math hotspot per Discipline #18 (methodology-before-execution). MC-1 (separate dispatch) covers BC-target cell sampling methodology. MC-2 (this dispatch) covers **substrate-binding heuristics** — given a sampled BC-target cell, how does the generator select the kit's `mechanical_substrate_triple` (per framing brief § 4 PlayerClass contract; the constituents of the BDI math model per L9 substrate split — mechanical only) from v1_scope substrate?

Key questions per framing brief § 2 MC-2:

1. **Cell-match outcome**: given a sampled cell, how does the kit choose its specific substrate (element + weapon_kind + energy_type + weapon_mechanical_profile) from substrate rows matching that cell?
   - Single-row selection (deterministic — first match in v1_scope) vs probabilistic (sample from matches with weights) vs hybrid (filter → sample)
   - Per matching strategy: Option α (full-strict cell-tuple) vs Option β (relaxed within thin-cell-fallback) vs Option C (cross-axis-substitution per composition policy § 3)
2. **Thin-cell-fallback**: per composition policy v1 § 4 (per-cell routing decisions locked at Stage 3 design call; cell-pair sharing per D3 Option A; 5-tuple cell-pair routing), what's the algorithmic shape of the fallback when the cell has insufficient substrate?
   - Trigger condition (substrate count threshold)
   - Fallback target (cell-pair sharing target OR composition policy § 4 floor-fill target)
   - Substitution policy (which substrate-axis can shift to satisfy cell-match — element-substitution? weapon_mechanical_profile-substitution? etc.)
3. **Substrate-triple coherence**: per L9 substrate split, the `mechanical_substrate_triple` is the BDI math model substrate. How does the heuristic ensure coherence across the triple (element + weapon_kind + energy_type cohesively combine into a playable kit)?
4. **Interaction with MC-1 cell sampling**: dependencies / coupling — does MC-1 sampling methodology constrain MC-2 substrate-binding heuristic? (legolas judgment; coordinate with MC-1 if needed)

Cycle 12 fires in parallel with Cycle 11 close (Tier 2 ratified drax Wave 3b). MC-1 + MC-2 fire concurrently at Cycle 12 open per Q6 substrate-led pattern; MC-3 fires later at Layer 4 start. This is MC-2.

---

## Required reading before starting

- `canonical/00-ground-state.md` § 1
- **`agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md`** § 2 (MC-2 scope statement) + § 4 (PlayerClass contract — `mechanical_substrate_triple: tuple[str, str, str]` shape) + § L9 (mechanical vs semantic substrate split) + § L11 (strict 4-tuple matching context)
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md` § 0-1
- **`canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`** § 3 (Option α/β/C matching strategies — primary load-bearing reference) + § 4 (thin-cell resolution policy — primary load-bearing reference) + § 5 (per-cell coverage)
- **`canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`** (Architecture B Phase 2 substrate-binding spec — primary load-bearing reference)
- **`canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`** (8 BC axes; bin definitions; weapon_mechanical_profile components: range, tempo, amplitude, AoE, primary_stat, hits_per_attack)
- v1_scope substrate (per Cycle 10 wind-down): `elrond/v0.0-cycle-10-stage-3-phase-2-v1-scope-2026-05-25` tag → 3,042 rows; per-axis distribution within ±5pp; per-cell coverage report at elrond Phase 3 artifact
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` (precedent: legolas methodology consult pattern — Scored-Candidate Strategy Registry + η-coefficient + cheapest-refuting-test)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 math-before-code; #18 + #18.2 methodology-before-execution at hotspots; #19.1 cheapest-refuting-test; #23 framing-audit checklist; #25 semantic-layer rep-audit; #20 density-based row-duplication prohibition)
- Cycle 10 Stage 3 Phase 1 legolas methodology consult (precedent for constrained-knapsack methodology under thin-cell pressure): `agentic_orchestration/legolas/research/...stage-3-phase-1-constrained-knapsack-methodology-2026-05-25/...`

---

## Math-before-code (per Discipline #1)

No code in this consult — Mode A research only. But methodology recommendation MUST surface:

- Mathematical objective of substrate-binding: what does "good" substrate-binding look like quantitatively? (cell-match fidelity + composition-policy alignment + kit-coherence + substrate-availability respect)
- Selection function shape: deterministic (rank substrate by score, take top) vs probabilistic (sample with weights) vs hybrid (filter → score → sample)
- Coherence constraints across substrate-triple components (element + weapon_kind + energy_type interactions)
- Interaction with composition policy § 4 thin-cell fallback (when substrate is insufficient, what does the heuristic do — fall back to cell-pair sharing? composition policy floor-fill? graceful-fail-with-fallback-substrate?)
- L11 strict 4-tuple matching consequence: if cell match is STRICT 4-tuple, what happens when v1_scope has zero substrate satisfying all 4 dimensions?

---

## Scope (legolas Mode A consult)

Mode A analytical research (read-only; ~1-2 day budget; parallel with MC-1):

- **Literature scan** on substrate-binding patterns in archive-driven procedural generation (MAP-Elites archive query + tag-matching; semantic substrate-based generation; thematic-coherence checks in template selection)
- **Per-methodology analysis** for substrate-binding heuristics:
  - **Deterministic top-rank** — rank substrate by cell-match score, take top-1
  - **Probabilistic weighted-sample** — sample substrate with weights proportional to cell-match score
  - **Hybrid filter-then-sample** — filter to candidate substrate set (e.g., top-k by cell-match), then sample uniformly within candidates
  - **Coherence-constrained** — additional constraint that substrate-triple coherence score above threshold
  - Per-method: pros / cons / compute envelope / kit-diversity-implications
- **Thin-cell-fallback algorithmic shape** — primary load-bearing analysis per composition policy v1 § 4
  - Trigger condition (substrate count threshold; per-cell-pair coverage threshold)
  - Fallback target (cell-pair sharing target per § 4; composition policy floor-fill target per § 1)
  - Substitution policy — which substrate-axis can shift to satisfy cell-match (recommend per-axis priority: e.g., element_substitution last; weapon_mechanical_profile_substitution first within thin-cell-fallback acceptable set)
  - Graceful-fail behavior — when fallback exhausted, what happens (NULL substrate-triple — kit ungenerable? floor-fill with composition policy default-tier substrate?)
- **L11 strict 4-tuple matching interaction** — primary load-bearing analysis per framing brief § L11
  - When v1_scope has zero substrate for a 4-tuple, what's the recommended algorithmic behavior (skip cell? widen to nearest cell? force fallback per § 4?)
  - Distinction between gauntlet sim strict-match requirement and player-game equip-flexibility (deferred to v1.1+)
- **Cohesion constraint** — substrate-triple component interactions:
  - Element + weapon_kind cohesion (which combinations are thematically incoherent — e.g., fire + ranged-bow OK; water + heavy-melee-mace ambiguous; per existing cultural-tradition data substrate)
  - Energy_type + element cohesion (mana / rage / charge / focus — per existing cultural-tradition data; recommend whether to enforce as a coherence check OR allow generator to express incoherence as feature)
  - Per L9: this coherence is mechanical_substrate-level; semantic overlay (cultural_tradition / lineage / period) is NOT in scope for this MC-2 consult (separate concerns)
- **Composition policy v1 alignment** — how does the heuristic achieve composition policy v1 § 1 register-share targets at the kit-generation scale (rather than substrate-curation scale)
- **Cheapest-refuting-test design** per Discipline #19.1: what's the minimal experiment that would refute a proposed substrate-binding heuristic (e.g., 100 kits from method X produce coherent substrate-triple per spot-check rate ≥ 90% — PASS; outside → FAIL)
- **Resource-bounds projection** — per-method runtime compute + memory envelope; per-100-kits and per-1000-kits scaling
- **Methodology recommendation memo** — proposed heuristic + rationale + cheapest-refuting-test + implementation-shape sketch (just enough for rocket Layer 2 dispatch to consume)
- **Framing-audit checklist application per Discipline #23** — three-question protocol against the recommended methodology
- **Discipline #25 semantic-layer rep-audit** — explicit check that substrate-triple components stay in mechanical-layer per L9; cultural_tradition / lineage / period are NOT substrate-binding targets at this layer

---

## Out of scope

- Algorithm Layer 2 implementation in rocket (gated on this consult + MC-1 landing)
- Engine code changes (Mode A is read-only)
- Architectural amendments to composition policy / BC-axes-lock / framing brief (escalate to gandalf if surfaced)
- Direct testing against substrate / no DB writes
- Cross-seam consultation beyond legolas Mode A (jack-ryan Gate-2 happens AFTER rocket Layer 2 lands)
- MC-1 BC-target cell sampling methodology (separate dispatch — fires in parallel with this MC-2)
- MC-3 multi-dim convergence libraries (separate dispatch — fires at Layer 4 start)
- Semantic-overlay substrate-binding (cultural_tradition / lineage / period) — per L9, NOT in this MC-2 scope; deferred to spirit-guide explainer integration and naming layers

---

## Acceptance criteria

- [ ] Mode A literature scan completed; sources cited
- [ ] Per-methodology analysis for the four heuristic baselines (deterministic top-rank / probabilistic weighted-sample / hybrid filter-then-sample / coherence-constrained)
- [ ] Thin-cell-fallback algorithmic shape analysis (trigger + target + substitution policy + graceful-fail)
- [ ] L11 strict 4-tuple matching interaction analysis
- [ ] Cohesion constraint analysis (element + weapon_kind; energy_type + element)
- [ ] Composition policy v1 alignment analysis
- [ ] Cheapest-refuting-test design with concrete pass/fail threshold
- [ ] Resource-bounds projection
- [ ] Methodology recommendation with rationale + implementation-shape sketch
- [ ] Framing-audit checklist application per Discipline #23
- [ ] Discipline #25 semantic-layer rep-audit application
- [ ] Output artifact at `agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md`
- [ ] Auto-commit + auto-push per legolas seam authorization
- [ ] Tag: `legolas/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25`

---

## Open questions for the agent to resolve

- Whether substrate-binding should be deterministic or probabilistic — surface tradeoff explicitly
- Whether coherence-constraints should be enforced at substrate-binding step OR deferred to a downstream cohesion-judge (per § 9 spirit-guide explainer + § 12 cohesion-judge naming)
- Whether thin-cell-fallback substitution priority should be: element first, weapon_kind second, energy_type third (or other ordering) — surface tradeoffs
- Whether MC-1 cell sampling methodology decision should inform MC-2 substrate-binding (legolas judgment; if dependency surfaces, flag to KR for coordination)
- Whether substrate-triple coherence check should be a hard constraint (reject incoherent kits) or soft constraint (score them lower in selection but allow)
- Whether to recommend a single unified heuristic OR per-matching-strategy heuristics (Option α vs β vs C — per composition policy § 3)

---

## Cross-seam impact

Round-trip: not applicable — Mode A research only; no DB writes; no cross-seam contract change. Methodology recommendation informs rocket Layer 2 dispatch authoring; round-trip happens at rocket Layer 2 generator output + cross-seam contract per framing brief § 4 PlayerClass.

---

## References

- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 2 MC-2 + § 4 PlayerClass contract + § L9 + § L11
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 3 + § 4 (primary load-bearing)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` (Architecture B Phase 2)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` (precedent)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #1 + #18 + #18.2 + #19.1 + #23 + #25 + #20

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification + Discipline #18 LOAD-BEARING gate on rocket Layer 2 implementation
**Status:** FIRE — Day-1 parallel-fire with MC-1 + jack-ryan Gate-1 + elrond SC-1/SC-2 + Cycle 11 close drax Wave 3b

**Matt-touch sequence:** consult returns → KR integrates into rocket Layer 2 dispatch authoring (parallel with MC-1 + Gate-1 clearance); if methodology surfaces surprises beyond framing brief assumptions OR if MC-1/MC-2 dependency emerges, KR routes to gandalf + jack-ryan critique-pair before forward-fire (per Cycle 12 scope-doc § 6)

---

## Completion record

**Status:** COMPLETE — 2026-05-25
**Output artifact:** `agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md`
**Acceptance criteria met:**
- [x] Mode A literature scan completed; sources cited (§ 2 — QD/MAP-Elites archive-seeded generation; ARPG item binding; constraint-relaxation PCG literature)
- [x] Per-methodology analysis for four heuristic baselines (§ 3.1-3.4: deterministic top-rank / probabilistic weighted-sample / hybrid filter-then-sample / coherence-constrained)
- [x] Thin-cell-fallback algorithmic shape analysis (§ 4: trigger THIN_CELL_THRESHOLD=5; substitution cascade weapon_mechanical_profile → tempo → range → energy_type → element; graceful-fail as UNGENERABLE)
- [x] L11 strict 4-tuple matching interaction analysis (§ 5: zero-match → thin-cell-fallback, not cell-skip; gauntlet-sim vs player-game distinction; no architectural conflict)
- [x] Cohesion constraint analysis (§ 6: element × weapon_kind soft coherence table; energy_type × element soft matrix; coherence-as-feature recommendation)
- [x] Composition policy v1 alignment analysis (§ 7: v1_scope materialization handles register-share targets; Option α/β/C routing at Layer 2)
- [x] Cheapest-refuting-test design: 50-kit spot-check; ≥90% coherence gate; ≥25% diversity gate; ≤10% deep-relaxation gate (§ 8)
- [x] Resource-bounds projection: all methods < 1 sec per 1,000 kits substrate-binding; Phase 3 dominates; no resource bottleneck (§ 9)
- [x] Methodology recommendation: hybrid filter-then-sample with soft coherence weighting; single unified heuristic; implementation-shape sketch (§ 10)
- [x] Framing-audit checklist per Discipline #23 (§ 11: four load-bearing assumptions; Phase 5 gap noted and mitigated via cheapest-refuting-test proxy)
- [x] Discipline #25 semantic-layer rep-audit: CLEAN — cultural_tradition / lineage / period NOT in Phase 2 binding criteria (§ 12)

**Flags for KR routing:**
1. **MC-1/MC-2 coupling (minor):** if MC-1 recommends substrate-coverage-aware cell sampling, shared data dependency at per-cell candidate count level. Coupling is data-input level, not algorithm level. Does NOT require sequencing; can inform same Layer 2 dispatch independently. (§ 13)
2. **Composition policy v1 § 4 potential gap:** policy locks routing for 12 CRITICAL thin cells; may not cover all 22 cells for runtime thin-cell-fallback graceful-fail scenarios. Route to gandalf for coverage review before Layer 2 dispatch authoring. (§ 14)
3. **element_weapon_kind_coherence_matrix data dependency:** rocket Layer 2 needs this table as an input artifact. Route to elrond for Tier S/A element × weapon_kind frequency query against v1_scope. (§ 15, gap 1)
