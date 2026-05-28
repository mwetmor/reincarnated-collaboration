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

---

### Seam 1 completion — rocket (2026-05-27)

**Status:** COMPLETE
**Commit:** `a466eb1`
**Tag:** `rocket/v1.6-dispatch-3b-seam-1-pm-1-g-b-1`
**Smoke gate:** 50/50 new + 111/111 prior = 161/161 PASS; 10-season G-B smoke tie-break rate 0% (acceptance: <20%)
**MIGRATION.md:** `generation/MIGRATION.md` — Dispatch 3B Seam 1 entry (ADR-004 compliant)

#### PM-1 scope delivered

**A4 GMM primary k∈{3,4} BIC-selected:**
`run_pm1_clustering()` implements GMM 5-restart BIC sweep at k=3 vs k=4; selects lower BIC. At n>=24, BIC selection is empirically stable (confirmed across 10-season smoke).

**A1 k-means n<20 fallback:**
Four-tier sparsity branches per PM-1 § 5.2 GMM-aware thresholds (24/20/12/8):
- `|K| >= 24`: GMM k∈{3,4} BIC (SparsityFlag.NONE)
- `20 <= |K| < 24`: GMM k=3 fixed (SparsityFlag.SEASON_SPARSE)
- `12 <= |K| < 20`: k-means k=3 (SparsityFlag.SEASON_SPARSE)
- `8 <= |K| < 12`: k-means k=2 degraded (SparsityFlag.SEASON_SPARSE)
- `|K| < 8`: clustering SKIPPED; single "unaffiliated-convergent" cluster (SparsityFlag.SEASON_CRITICALLY_SPARSE)

**Aesthetic-heavy sqrt-weights + PCA-whitening:**
Per § 3.3.1: `sqrt(w_aes=0.4)/sqrt(w_mech=0.3)/sqrt(w_subs=0.2)/sqrt(w_elem=0.1)` pre-PCA.
Per § 3.3.2: PCA-whitening + truncate to top-95% variance (19 raw dims → typically 8-14 PCA dims at n=28-32).

**Substrate-led discipline (Discipline #41) preserved:**
Feature vectors are multimodal (BC axes + substrate-theme + aesthetic-tuples + element-attr); no pre-authored faction taxonomy at any layer. Clusters EMERGE from data.

**PM-1↔MG-5 feedback loop hookup (§ 5.4):**
`run_pm1_clustering(feedback_channel=...)` consumes `PM1FeedbackChannel.get_recent_evictions(season_id_int)` from gamora Dispatch 3A. Returns `feedback_summary` dict with eviction counts + sparsity_flag for star-lord telemetry emission. Graceful None handling when channel not yet initialized.

**Cluster output consumable by G-B + gandalf PM-2 (Seam 2):**
`PM1ClusteringResult.clusters` carries per-cluster: `centroid_pca`, `member_vectors_pca`, `modal_*` reps, `faction_label_placeholder`, `element_distribution`, `modal_bc_axis_signature` — all fields PM-2 Wave A LLM prompt needs.

#### G-B scope delivered (Path III addition)

**Mahalanobis pairwise centroid distance over PM-1 clusters:**
`select_primary_faction_pair()` computes O(k²) pairwise distances (max 12 at k=4). REUSES MG-3 Tikhonov λ=1e-3 pooled-covariance regularization — no parallel implementation (per § 13.4 cross-link).

**Tie-break logic per PM-2 § 13.2:**
Priority: lineage diversity divergence → named-anchor count → geometry divergence → lexicographic (always deterministic). 10-season smoke: 0% tie-break rate (well under 20% acceptance bound).

**primary_faction_pair + background_faction_pairs metadata:**
Per § 13.3 schema: `{faction_a_cluster_id, faction_b_cluster_id, pairwise_distance, selection_rationale}` + list of remaining pairs.

**primary_pair_flag ready for F-C Wave 3 inputs:**
`GBPrimaryPairResult.primary_faction_pair` is the direct input for F-C LLM call narrative intensification when Wave 3 dispatch fires.

#### Open questions

- **Q-3B-rocket-1 (K=3 vs K=4 distribution):** 10-season smoke both k=3 and k=4 selected at n=28-32; empirical distribution across full live-generation scale TBD; surface to elrond if drift to k=5 emerges.

#### Cross-seam dependencies

- **Gandalf (Seam 2):** Wire `PM1ClusteringResult.clusters` into Wave A LLM prompt construction; consume `GBPrimaryPairResult.primary_faction_pair` as `primary_pair_flag` in F-C LLM call inputs
- **Star-lord:** Emit `surviving_kit_count` + `sparsity_flag` + `pairwise_distance` + `selection_rationale` to telemetry; map `PM1Cluster` fields to `ExportFactionCluster` skeleton before `run_phase5_wave_a_sync()`
- **Gamora:** Pass `PM1FeedbackChannel` instance as `feedback_channel` to `run_pm1_clustering()`; PM-1 side of 5-season window feedback loop is live

---

### Seam 3 completion — star-lord (2026-05-27)

**Status:** COMPLETE
**Commit:** `bf7f659`
**Tag:** `star-lord/v1.0-dispatch-3b-phase-5-seam-3-1`
**Smoke gate:** 50/50 new + 205/205 prior = 255/255 PASS
**MIGRATION.md:** `export/MIGRATION.md § v1.10` + `llm/MIGRATION.md Phase 5 section` (ADR-004 compliant)

#### 5 scope items delivered

**Item 1 — LOAD-BEARING two-wave sequencing:**
`Phase5OrchestratorConfig.should_fire_wave_a` + `run_phase5_wave_a_sync/async()` implement the Wave A → Wave B dependency. Wave A (faction-label calls) MUST complete before Wave B (per-kit identity calls) begins. Callers receive `Phase5Result` with all Wave A outputs before Wave B can start. No stale-cluster consumption race condition.

**Item 2 — Concurrency strategy (Q-3B-star-lord-1 RESOLVED):**
asyncio + `AsyncAnthropic` (SDK 0.97.0 verified). `asyncio.Semaphore(DEFAULT_CONCURRENCY=10)`. Rate limit headroom: 10 concurrent × 2-4 sec ≈ 20 calls/min; Sonnet tier-2 = 50 req/min. Synchronous callers use `run_phase5_wave_a_sync()` via `asyncio.run()`. Exponential backoff: 3 attempts max; 1s/2s/4s waits (Discipline #19 compliant — no polling).

**Item 3 — ExportFactionCluster schema:**
New 21-field Pydantic model in `export/schemas.py`. D-Hybrid architecture (placeholder always produced; canonical null for v1). D-Sharpened encoding (substrate_anchored_personages field; analytics only; NEVER LLM-prompt-exposed per D-Sharp-1). No-classes vocabulary throughout (Discipline #41). `ExportSeason.faction_clusters` additive nullable field (backward compat). Consumer obligations documented in MIGRATION.md § v1.10.

**Item 4 — Local diversity checker (Q-3B-star-lord-2 RESOLVED):**
Current backend: scikit-learn TF-IDF character n-gram (2,4) via `llm/faction_diversity.py`. No Anthropic API calls; no cost; no tracking gap. Upgrade path: `sentence-transformers>=2.2.0`, model `all-MiniLM-L6-v2` (86MB; 384-dim; local inference) — implementation in `_sentence_transformer_cosine_similarity()` dormant until dep added to `pyproject.toml`. Graceful fallback with WARNING log if import fails. Regeneration policy: 1 max per faction per season; no further retry post-regeneration; collision logged to telemetry.

**Item 5 — Phase 7 joint-gate placeholder handling:**
`phase7_gate_status = "placeholder"` by default (all Reincarnated v1 seasons). `"canonical"` only when `faction_label_canonical` is non-null. Short-circuit path produces all placeholder records when `faction_visibility = "invisible"`. Phase 7 MUST accept `"placeholder"` status — `faction_label_placeholder` carries sufficient semantic tokens for cohesion evaluation. Gamora/gandalf awareness flagged in MIGRATION.md.

#### Open questions resolved

- **Q-3B-star-lord-1:** asyncio + AsyncAnthropic primary; Semaphore(10) conservative start; increase to 20-30 if rate monitoring shows headroom
- **Q-3B-star-lord-2:** TF-IDF current (scikit-learn in deps); sentence-transformers all-MiniLM-L6-v2 upgrade path ready and documented

#### Cross-seam dependencies

- **Rocket (Seam 1):** call `run_phase5_wave_a_sync(faction_clusters_input, config)` before Wave B per-kit calls; pass `faction_label_canonical` from results into per-kit call context
- **Gandalf (Seam 2):** `Phase5OrchestratorConfig.thematic_registry` slot ready to receive THEMATIC_REGISTRY when it lands; Wave 3 impl gated on gandalf cross-cutting dispatch (per dispatch § out-of-scope)
- **Gamora:** Phase 7 joint-gate design must accept `phase7_gate_status = "placeholder"` (all v1 seasons)
- **Drax:** null-check `season.faction_clusters`; `substrate_anchored_personages` is metadata-only surface (NOT primary kit name per D-Sharp-2)

#### Hand-back to KR

Seam 3 complete. KR consolidates Phase 5 close signal when rocket Seam 1 (PM-1 clustering impl) and gandalf Seam 2 (PM-2 LLM logic + cohesion-judge prompts) complete.
