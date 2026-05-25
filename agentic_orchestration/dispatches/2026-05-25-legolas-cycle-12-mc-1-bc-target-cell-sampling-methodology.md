# Dispatch — 2026-05-25 — legolas — Cycle 12 MC-1 BC-target cell sampling methodology consult

**From:** knight-rider
**To:** legolas (Mode A — analytical research; read-only)
**Approved by:** Matt 2026-05-25 (Cycle 12 framing brief bulk-ratification — "Let's move ahead with it"; Q6 Option B substrate-led methodology consultation timing — MC-1 fires at Cycle 12 open)
**Estimated effort:** ~1-2 days legolas Mode A
**Acceptance:** Methodology recommendation memo authored at `agentic_orchestration/legolas/research/cycle-12-mc-1-bc-target-cell-sampling-methodology-2026-05-25/methodology-recommendation.md` covering uniform vs composition-policy-weighted vs substrate-coverage-aware sampling approaches; cheapest-refuting-test design with concrete pass/fail threshold; resource-bounds projection; sources cited

---

## Context

Cycle 12 Layer 2 (kit identity — BC-target subspace generator per framing brief § 2 + § 4 PlayerClass contract) is a load-bearing math hotspot per Discipline #18 (methodology-before-execution). Before rocket implements the generator, legolas Mode A consultation is REQUIRED to recommend the BC-target cell sampling methodology — i.e., how the generator chooses which BC-target cells (5-tuple: range × tempo × amplitude × attribute × proxy-density per qd-engine-bc-axes-lock-2026-05-20 + composition policy v1) to instantiate kits for.

Three baseline options on the table (per framing brief § 2 MC-1):

1. **Uniform sampling** — equal probability across all cells in the BC-target space
2. **Composition-policy-weighted** — weight per composition policy v1 § 1 register-share targets + register-share-cap to honor the curation policy at generation time
3. **Substrate-coverage-aware** — weight by substrate availability per v1_scope cell-coverage (avoid kits in cells where substrate is thin)

Each has tradeoffs in BC-space coverage, generation efficiency, and composition-policy alignment. Legolas's methodology recommendation gates rocket's Layer 2 generator implementation per Discipline #18.

Cycle 12 fires in parallel with Cycle 11 close (Tier 2 ratified drax Wave 3b). MC-1 + MC-2 fire concurrently at Cycle 12 open per Q6 substrate-led pattern; MC-3 fires later at Layer 4 start. This is MC-1.

---

## Required reading before starting

- `canonical/00-ground-state.md` § 1
- **`agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md`** § 2 (MC-1 scope statement) + § 4 (PlayerClass contract — what cell-match outputs) + § L1-L11 (L9 substrate split + L11 strict 4-tuple matching context)
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md` § 0-1 (Cycle 12 scope + workstream roster)
- **`canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`** § 1 (register-share targets + cap) + § 3 (Option α/β/C matching strategies) + § 4 (thin-cell resolution policy) + § 5 (per-cell coverage)
- **`canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`** (8 BC axes; 5-tuple cell coordinate system; bin definitions)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` (Architecture B Phase 2 substrate-binding spec — how cell-match flows into kit identity)
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` (precedent: legolas methodology consult pattern — Scored-Candidate Strategy Registry + η-coefficient + cheapest-refuting-test)
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-re-review-post-bc-shift-fail-2026-05-25.md` (precedent: Pattern A-deep methodology re-review after BC-shift FAIL — sweep-design rigor pattern)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 math-before-code; #18 + #18.2 methodology-before-execution at hotspots; #19 background processes; #19.1 cheapest-refuting-test; #23 framing-audit checklist; #24 single-parameter-sweep isolation; #25 semantic-layer rep-audit)
- v1_scope substrate (per Cycle 10 wind-down): `elrond/v0.0-cycle-10-stage-3-phase-2-v1-scope-2026-05-25` tag → 3,042 rows curated; per-axis distribution within ±5pp; per-cell coverage report at elrond Phase 3 artifact

---

## Math-before-code (per Discipline #1)

No code in this consult — Mode A research only. But methodology recommendation MUST surface:

- Mathematical objective of sampling: what does "good" cell sampling look like quantitatively? (BC-space coverage uniformity vs composition-policy fidelity vs substrate-availability respect)
- Selection function shape: deterministic (enumerate all cells) vs probabilistic (sample with weights); per-cell-fired-once vs multi-fires; with-replacement vs without
- Interaction with L11 strict 4-tuple matching (per framing brief § L11; gauntlet sim strict-match requirement)
- Interaction with composition policy v1 § 4 thin-cell fallback (Option β / undifferentiated floor-fill behavior at thin cells)

---

## Scope (legolas Mode A consult)

Mode A analytical research (read-only; ~1-2 day budget):

- **Literature scan** on sampling methodologies in procedural-generation contexts (Quality-Diversity / MAP-Elites; archive-driven generation; rejection sampling; stratified sampling; importance sampling) — focus on what's used in ARPG generation, roguelike generators, MAP-Elites archive seeding
- **Per-methodology analysis** — uniform / composition-policy-weighted / substrate-coverage-aware:
  - What does the method DO mathematically (sampling distribution shape)
  - Pros / cons for BC-space coverage uniformity
  - Pros / cons for composition-policy alignment (per § 1 register-share targets + register-share-cap)
  - Pros / cons for substrate-availability respect (avoid thin cells per § 4 thin-cell fallback)
  - Compute envelope (deterministic enumeration vs sampling overhead)
- **Hybrid options analysis** — are there hybrid methods that combine the three baselines (e.g., uniform-with-composition-policy-bias; substrate-coverage-aware-with-policy-renormalization)
- **Interaction with L11 strict 4-tuple matching** — does the chosen sampling method gate on cell-substrate availability (sample → match → fallback) OR pre-filter cells by substrate availability (filter → sample) — implications for thin-cell handling
- **Composition policy alignment** — how does the method achieve composition policy v1 § 1 register-share targets at the kit-generation scale vs the substrate-curation scale (different optimization objects)
- **Cheapest-refuting-test design** per Discipline #19.1: what's the minimal experiment that would refute a proposed sampling methodology (e.g., 100 kits from method X produce per-register-share distribution within ±10pp of target — PASS; outside → FAIL)
- **Resource-bounds projection** — per-method runtime compute + memory envelope; per-100-kits and per-1000-kits scaling
- **Methodology recommendation memo** — proposed method + rationale + cheapest-refuting-test + implementation-shape sketch (just enough for rocket Layer 2 dispatch to consume)
- **Framing-audit checklist application per Discipline #23** — three-question protocol against the recommended methodology

---

## Out of scope

- Algorithm Layer 2 implementation in rocket (gated on this consult + MC-2 landing; Matt does not need to re-lock since framing brief Q-ratification covers; rocket dispatch fires after both MC-1 + MC-2 + jack-ryan Gate-1 clear)
- Engine code changes (Mode A is read-only)
- Architectural amendments to composition policy / BC-axes-lock / framing brief (escalate to gandalf if surfaced)
- Direct testing against substrate / no DB writes
- Cross-seam consultation beyond legolas Mode A (jack-ryan Gate-2 happens AFTER rocket Layer 2 lands, not at consult)
- MC-2 substrate-binding heuristics (separate dispatch — fires in parallel with this MC-1)
- MC-3 multi-dim convergence libraries (separate dispatch — fires at Layer 4 start)

---

## Acceptance criteria

- [ ] Mode A literature scan completed; sources cited
- [ ] Per-methodology analysis for the three baselines (uniform / composition-policy-weighted / substrate-coverage-aware)
- [ ] Hybrid options analysis
- [ ] L11 strict 4-tuple matching interaction analysis
- [ ] Composition policy v1 alignment analysis
- [ ] Cheapest-refuting-test design with concrete pass/fail threshold
- [ ] Resource-bounds projection
- [ ] Methodology recommendation with rationale + implementation-shape sketch
- [ ] Framing-audit checklist application per Discipline #23
- [ ] Output artifact at `agentic_orchestration/legolas/research/cycle-12-mc-1-bc-target-cell-sampling-methodology-2026-05-25/methodology-recommendation.md`
- [ ] Auto-commit + auto-push per legolas seam authorization
- [ ] Tag: `legolas/cycle-12-mc-1-bc-target-cell-sampling-methodology-2026-05-25`

---

## Open questions for the agent to resolve

- Whether the recommended method should be deterministic or probabilistic — surface tradeoff explicitly
- Whether sampling should be per-cell-fired-once or multi-fires per cell — implications for kit diversity
- Whether the method needs separate behavior for Tier-S / A / B / C cells (per Cycle 10 wind-down per-tier counts: S=532, A=1431, B=1056, C=23) — substrate density varies by tier
- Whether MC-2 substrate-binding heuristics decision should inform MC-1 OR fire independently (legolas judgment; if dependency surfaces, flag to KR for coordination)

---

## Cross-seam impact

Round-trip: not applicable — Mode A research only; no DB writes; no cross-seam contract change. Methodology recommendation informs rocket Layer 2 dispatch authoring; round-trip happens at rocket Layer 2 generator output + cross-seam contract per framing brief § 4 PlayerClass.

---

## References

- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 2 MC-1
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`
- `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md` (precedent)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #1 + #18 + #18.2 + #19.1 + #23

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q6 Option B substrate-led methodology consultation timing — MC-1 + MC-2 fire at Cycle 12 open) + Discipline #18 LOAD-BEARING gate on rocket Layer 2 implementation
**Status:** FIRE — Day-1 parallel-fire with MC-2 + jack-ryan Gate-1 + elrond SC-1/SC-2 + Cycle 11 close drax Wave 3b

**Matt-touch sequence:** consult returns → KR integrates into rocket Layer 2 dispatch authoring (parallel with MC-2 + Gate-1 clearance); if methodology surfaces surprises beyond framing brief assumptions, KR routes to gandalf + jack-ryan critique-pair before forward-fire (per Cycle 12 scope-doc § 6 pre-resolved known-unknowns)
