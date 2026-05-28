# Dispatch — 2026-05-27 — Dispatch 3B: Phase 5 multimodal extension (gandalf + star-lord + rocket parallel)

**From:** knight-rider
**To:** gandalf (PM-2 LLM logic / cohesion-judge prompts) + star-lord (LLM call infrastructure + ExportFactionCluster schema + concurrency) + rocket (PM-1 multimodal clustering impl + generation pipeline integration)
**Approved by:** Matt 2026-05-27 (Matt-gate Path (1) ratification + "Fire the sequence: 3. Dispatch 3B → gandalf+star-lord+rocket Phase 5 impl (~2-3 weeks parallel; LOAD-BEARING two-wave sequencing + concurrency strategy + ExportFactionCluster schema + 5 star-lord PM-2 scope items)")
**Estimated effort:** ~2-3 weeks parallel across 3 seams
**Acceptance:** Phase 5 multimodal extension implemented per ratified specs (PM-1 GMM K∈{3,4} + PM-2 D-Hybrid + D-Separate + D-Sharpened); LOAD-BEARING two-wave sequencing (Wave A cluster faction calls → Wave B per-kit identity calls); ExportFactionCluster schema + MIGRATION.md; concurrency strategy for ~2,100 calls; local sentence-transformers for cross-faction diversity; THEMATIC_REGISTRY consumed at LLM prompts

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** lock the per-season faction-coalescent kit-naming/lore-flavor layer — Phase 5 transforms mechanical archive into player-facing identity. Without LOAD-BEARING two-wave sequencing, Phase 7 cohesion criterion is structurally weaker (kit identity choices wouldn't compose with faction-level coherence). Composes "Engine first. Game second. Phase third." orientation.

**Refutation conditions** (per agent surfaces if any apply):
- PM-1 GMM at K∈{3,4} BIC-selected fails empirically (n<20 fallback firing rate too high)
- Two-wave sequencing produces stale Wave-A clusters by Wave-B consumption (race condition)
- ExportFactionCluster schema conflicts with existing telemetry schema requiring breaking MIGRATION
- ~2,100 calls per season exceeds Anthropic API rate limits even with concurrency
- THEMATIC_REGISTRY not landed by Wave 3 (Phase 5 LLM impl) → block on gandalf cross-cutting

## Context

**Authority chain:**
- Matt-gate Path (1) RATIFIED 2026-05-27 (Package A 7 math-notes including PM-1 + PM-2)
- PM-1 math note transcribed at engine `307ed1e` (algorithm commit: A4 GMM primary K∈{3,4} BIC-selected; A1 k-means n<20 fallback; aesthetic-heavy sqrt-weights + PCA-whitening 95%; thresholds 24/20/12/8; PM-1↔MG-5 feedback § 5.4)
- PM-2 math note: D-Hybrid + D-Separate + D-Sharpened (§ 2.7 + § 3.7 at `7233e0f`; field rename clean at `27bfd0e`)
- Star-lord PM-2 cost consultation `708b575`: **LOAD-BEARING two-wave sequencing** finding; $0.015-$0.05/season cost confirmed within SC-3 envelope
- A2 superseded at PM-1 (K∈{3,4} not K∈{2,4}; k=2 NOT in selection space; Cycle 15+ revisit)
- THEMATIC_REGISTRY blocks Wave 3 (Phase 5 cohesion-judge LLM impl); gandalf cross-cutting dispatch firing in parallel

## Required reading

**Phase 5 math notes (canonical post-transcription):**
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-1-multimodal-clustering-math-2026-05-27.md`
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md` (D-Sharpened § 2.7 + § 3.7)

**Authority anchors:**
- `agentic_orchestration/star-lord/notes/2026-05-27-phase-5-pm-2-llm-cost-consultation.md` (PM-2 cost + 5 Dispatch 3B scope items + two-wave sequencing LOAD-BEARING)
- `agentic_orchestration/elrond/notes/2026-05-27-phase-4-5-methodology-consultation.md` § 5 PM-1 + § 6 cross-cutting (PM-1↔MG-5 feedback)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § Phase 5
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-register.md` § 5 "Risks + Watch Items"
- SC-3 (legolas Mode A) Pattern B Structured Output with Layer Tags — PRIMARY architecture

**Disciplines:**
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #1 / #11 / #18 / #19 (Agent-tool-not-for-waiting for LLM call backgrounding) / #41 / #42 / #44 / #46 § 7

## Discipline #46 compliance (DB-touching dispatch)

- [ ] ExportFactionCluster schema design follows per-cell bounding (Discipline #46 § 7); if archive-scope query needed, document pattern explicitly
- [ ] All DB queries stream / push-to-SQL / index / bound
- [ ] EXPLAIN QUERY PLAN captures
- [ ] MIGRATION.md per ADR-004 for new schema

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:** (1) PM-1 GMM K∈{3,4} BIC selection produces stable cluster counts at typical season scale (n=22-40 kits); (2) two-wave sequencing avoids stale-cluster-consumption race condition; (3) THEMATIC_REGISTRY will land by Wave 3 LLM impl phase
- **Q2 refutation evidence to seek:** PM-1 cluster-count distribution under empirical load; two-wave hand-off freshness check; THEMATIC_REGISTRY readiness signal from gandalf parallel dispatch
- **Q3 outcome trigger:** if any agent surfaces framing contradiction, invoke Discipline #44 framing-refusal + route back to KR

## Scope — multi-seam

### Seam 1 — rocket: PM-1 multimodal clustering impl (~3-5 days)

- [ ] Implement A4 GMM primary K∈{3,4} BIC-selected per PM-1 § 4.3
- [ ] Implement A1 k-means n<20 fallback
- [ ] Option β composition with Note 1 substrate-clustering (distinct algorithms per scale)
- [ ] Aesthetic-heavy sqrt-weights pre-PCA + PCA-whitening top-95% variance per § 3.3
- [ ] GMM-aware sparsity thresholds 24/20/12/8 per § 5.2
- [ ] Substrate-led discipline (Discipline #41) preserved
- [ ] Cluster output consumable by gandalf PM-2 algorithm (Seam 2)

### Seam 2 — gandalf: PM-2 faction-label assignment LLM logic (~5-7 days)

- [ ] Implement PM-2 D-Hybrid + D-Separate algorithm per math note § 3
- [ ] **D-Sharpened § 2.7 + § 3.7 encoding** — algorithm invariance regardless of substrate-anchored vs synthesized lineage
- [ ] SC-3 Pattern B Structured Output with Layer Tags as PRIMARY LLM architecture
- [ ] Cohesion-judge LLM prompts (Wave A faction-level + Wave B per-kit identity)
- [ ] Cross-Character Diversity Audit DETECTION integration
- [ ] **THEMATIC_REGISTRY consumed at LLM prompt construction** (gates Wave 3 impl; THEMATIC_REGISTRY landing parallel)

### Seam 3 — star-lord: LLM infra + ExportFactionCluster schema + concurrency (~5-7 days)

Per 5 star-lord PM-2 scope items (`708b575`):

- [ ] **Item 1 — LOAD-BEARING two-wave sequencing**: Wave A cluster faction calls MUST fire before Wave B per-kit identity calls (Phase 7 cohesion criterion structurally weaker without)
- [ ] **Item 2 — Concurrency strategy**: for ~2,100 Phase 5 calls per season; existing `_call_with_retry` is synchronous (sequential = 70-140 min unacceptable); design async/parallel pattern within Anthropic rate limits
- [ ] **Item 3 — ExportFactionCluster schema**: new schema entries; MIGRATION.md per ADR-004
- [ ] **Item 4 — Local sentence-transformers**: cross-faction diversity check (no Anthropic embedding API; local model)
- [ ] **Item 5 — Phase 7 joint-gate placeholder handling**: accepts placeholder when canonical null (gamora/gandalf flag)

### Cross-cutting (all 3 seams)

- [ ] PM-1↔MG-5 calibration feedback loop hookup (gamora Dispatch 3A side already; rocket+star-lord side here)
- [ ] 5-season window data structure compatible across telemetry schema
- [ ] Per-seed determinism preserved across all 3 seam contributions
- [ ] Cost monitoring: $0.015-$0.05/season expected (gandalf $0.15-$0.25 was conservative ceiling; star-lord empirical)
- [ ] No-classes vocabulary throughout (Discipline #41 LOAD-BEARING)

### Risks + Watch Items (per failure-modes register § 5)

- F-1 math methodology drift watch
- F-3 faction cardinality drift watch (A2 superseded by K∈{3,4}; revisit Cycle 15+ trigger if K=2 lockstep becomes essential)
- F-4 Phase 5 LLM volume drift watch (cost monitoring)
- F-5 joint-gate threshold drift watch
- D-2 faction pre-authored drift (LLM cohesion-judge must remain substrate-led; no taxonomy reimposition)
- D-4 Phase 5 LLM as oracle drift (LLM is naming/lore layer, not design authority)

### Closure (per seam)

- [ ] Update respective AGENT_STATE.md files (rocket generation; gandalf cross-cutting; star-lord export)
- [ ] All tests PASS (existing + new per-seam coverage)
- [ ] Tag at completion: `<seam>/v1.X-dispatch-3b-phase-5-multimodal-1` per seam
- [ ] MIGRATION.md for ExportFactionCluster schema (star-lord)
- [ ] Per-seam completion records appended; combined dispatch close at KR signaling Phase 5 close
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern

## Acceptance criteria (cross-seam)

- [ ] PM-1 GMM K∈{3,4} produces stable cluster output empirically
- [ ] PM-2 D-Hybrid + D-Separate + D-Sharpened logic implemented; algorithm invariance verified
- [ ] LOAD-BEARING two-wave sequencing implemented; Wave A→B hand-off freshness verified
- [ ] ExportFactionCluster schema landed + MIGRATION.md authored
- [ ] Concurrency strategy implemented; ~2,100 calls per season within rate limits
- [ ] Local sentence-transformers integration landed
- [ ] Phase 7 joint-gate placeholder handling implemented
- [ ] PM-1↔MG-5 feedback loop hookup (cross-seam coordination with gamora Dispatch 3A)
- [ ] All G-named smoke-test gates PASS (G-PM1-1 through G-PM1-4 plus PM-2 gates)
- [ ] Per-seam tags cut; consolidated Phase 5 close signal
- [ ] Commit + push per seam

## Out of scope

- Do NOT touch Phase 4 mechanical archive gates (gamora Dispatch 3A seam)
- Do NOT touch Wave 1.5 Stage 3 (rocket seam parallel firing on Option α impl)
- Do NOT touch THEMATIC_REGISTRY authoring (gandalf cross-cutting separate dispatch)
- Do NOT touch Phase 6 visual joint-gate (Cycle 15+)
- Do NOT touch Phase 7 2-layer joint-gate (separate dispatch post Phase 4+5 close)

## Open questions (per seam)

- **Q-3B-rocket-1:** PM-1 GMM stability at K=3 vs K=4 BIC selection — empirical clusters-count distribution; surface to elrond if drift to K=5 emerges
- **Q-3B-gandalf-1:** THEMATIC_REGISTRY readiness — coordinate with parallel gandalf cross-cutting dispatch; Wave 3 impl gated on registry landing
- **Q-3B-star-lord-1:** Concurrency strategy — async vs threadpool vs queue; your judgment under existing `_call_with_retry` extension authority
- **Q-3B-star-lord-2:** Local sentence-transformers model choice — your judgment (e.g., all-MiniLM-L6-v2 vs larger model); document at MIGRATION

## References

- Matt-gate ratification 2026-05-27 (verbatim above)
- Phase 5 math notes engine `307ed1e` + `27bfd0e` (canonical state)
- Star-lord PM-2 consultation `708b575` (5 scope items + two-wave LOAD-BEARING)
- Elrond consultation `f8eb1a4` § 5 + § 6 cross-cutting
- Path (1) failure-modes register § 5
- Engineering-disciplines.md § Discipline #1 / #11 / #18 / #19 / #41 / #42 / #44 / #46

---

## Completion record

(append per seam on completion; KR consolidates Phase 5 close)
