# Dispatch — 2026-05-25 — Post-Cycle 10 #5 (Optional Parallel) — Star-Lord G12 LLM-Call Cache-Hit-Rate Measurement

**Cycle:** Post-Cycle-10 continuation (fires immediately after Cycle 10 wind-down filing, in parallel with G1)
**Owner:** star-lord (LLM-call seam owns LLM-call infrastructure + repeat-rate visibility)
**From:** knight-rider (orchestrator)
**Date:** 2026-05-25
**Authority:** Cycle 10 fresh-session kicker § "Post-cycle continuation Optional #5" + Matt 2026-05-25 skip-confirmation fire-forward authorization + Pi recognition record § 8 G12 gate
**Status:** FIRE (parallel with G1) — pure measurement; informs D9 LLM response cache decision

---

## 0. TL;DR

Measure LLM-call repeat-rate over last 2 weeks. If ≥20% of calls have cacheable identical inputs → cache build candidate triggered per Pi recognition record § 8 G12.

**Pure measurement.** Fires in parallel with G1 (same star-lord seam; same measurement window). NOT cache implementation.

---

## 1. Required reading

1. `canonical/00-ground-state.md` § 1
2. **`canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md` § 5 + § 7 D9 + § 8 G12** (recognition record; G12 criterion)
3. LLM-call infrastructure (star-lord seam; `~/Games/reincarnated-engine/src/reincarnated/llm/` and adjacent)
4. Telemetry DB schema where LLM calls are logged (`weapon_knowledge_entries` content authoring + `cohesion_judge` calls + spirit-guide explainer calls + any other LLM-traced surfaces)
5. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#11 empirical inspection; #19 background processes)

---

## 2. Scope (star-lord measurement work)

### 2.1 LLM-call repeat-rate measurement

- Definition: LLM call repeat = same prompt (or normalized-prompt-signature) submitted to same model within measurement window
- Measurement window: last 2 weeks (rolling; same window as G1 for consistency)
- Per-call surface enumeration:
  - cohesion-judge calls (Phase 5 cohesion-coalescence)
  - description_text authoring (Phase 2 generation)
  - spirit-guide explainer (per skill-system § 9; if instrumented)
  - LLM-judge for ambiguous mechanical-tagging (per Stage 4)
  - Any other LLM-instrumented surfaces in star-lord seam
- Normalization: trim whitespace + lowercase + canonical key ordering; document normalization protocol
- Metric: repeat rate = (calls with prompt-signature seen prior in window) / (total calls)
- Per-surface breakdown: which surfaces have high repeat-rate (cohesion-judge likely candidate; description-text authoring may also)

### 2.2 G12 criterion evaluation

- If repeat rate ≥ 20% → cache build candidate TRIGGERED per § 8 G12
- If < 20% → cache build NOT TRIGGERED; defer D9 to subsequent re-measurement
- Cost estimate: $$ saved if cache deployed (LLM-call $ × repeat rate)

### 2.3 Output

- Report at `agentic_orchestration/star-lord/research/g12-llm-cache-hit-rate-measurement-2026-05-25/report.md`
- Companion data files (CSV / JSON for per-call signatures + repeat counts)
- G12 verdict per § 8 criterion (TRIGGERED / NOT TRIGGERED / INCONCLUSIVE)
- Cost savings estimate if cache deployed

---

## 3. Out of scope

- LLM response cache IMPLEMENTATION (gated on D9 ratification per Pi recognition record § 7)
- G1 infrastructure measurement (separate dispatch; can fire in parallel — see `2026-05-25-star-lord-g1-infrastructure-measurement.md`)
- Cache architecture design (Postgres-backed cache vs in-memory vs other — gated on D9 commitment AND D1 Postgres decision)
- Schema changes
- Engine code changes

---

## 4. Acceptance criteria

- [ ] LLM-call repeat rate measured over last 2 weeks; metric documented with normalization protocol
- [ ] Per-surface breakdown (cohesion-judge + description-text + spirit-guide + LLM-judge + other)
- [ ] G12 verdict (TRIGGERED / NOT TRIGGERED / INCONCLUSIVE) per § 8 G12 criterion
- [ ] Cost savings estimate if cache deployed
- [ ] Report + companion data files at named star-lord research path
- [ ] Auto-commit + auto-push per star-lord seam authorization
- [ ] Tag intent: `star-lord/g12-llm-cache-hit-rate-measurement-2026-05-25`

---

## 5. Open questions for the agent to resolve

- Per-surface enumeration completeness (have all LLM-instrumented surfaces been included) — star-lord audits
- Normalization protocol choice (strict signature vs fuzzy match vs LLM-judged similarity) — strict signature preferred for cache safety
- Inconclusive verdict criteria (insufficient call volume; missing surface instrumentation) — documented if surfaces

---

## 6. Cross-seam impact

Round-trip: not applicable — pure measurement; no production code changes; no schema changes; no cross-seam contract change.

---

## 7. References

- Pi recognition record: `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md` § 5 + § 7 D9 + § 8 G12
- `agentic_orchestration/operating-procedures/star-lord.md` (LLM-mode)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` #11 + #19
- Telemetry DB: `~/Games/reincarnated-loadout/data/telemetry.db`

---

## 8. Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Cycle 10 fresh-session kicker post-cycle continuation Optional #5 + Pi recognition record § 8 G12 gate + Matt 2026-05-25 skip-confirmation fire-forward authorization
**Status:** FIRE (parallel with G1) — pure measurement; informs D9 LLM response cache decision but does not commit cache architecture

---

## Completion record

**Completed:** 2026-05-25
**Executor:** star-lord

### G12 Verdict: NOT TRIGGERED

Measured repeat rate: **0.13%** (4 repeats / 3,001 calls in 2-week window). Full corpus: **0.14%** (7 / 4,992). Threshold: 20%. Delta: -19.87pp.

**D9 (LLM response cache) remains DEFERRED.** Empirical gate G12 did not trigger.

### Key findings

1. **Zero cross-season prompt-signature collisions** across all 4,992 calls and 16 seasons. The prompt architecture (season-specific + entity-specific content embedded in every prompt) makes cross-session cache hits structurally impossible. This is by design.

2. **All 7 repeats in full corpus are within-session same-season reruns** — already handled by the existing DiskCache at $0.00 cost. season_100002 was generated twice within 2 minutes; season_001005 had 27 generation_runs.

3. **Active surfaces enumerated (8):** skill_naming (57% of calls), gear_unique_naming (28%), monster_naming (10%), class_naming, element_selection, theme_coalescence, cosmological_vocabulary, trial_naming.

4. **3 expected surfaces absent from telemetry:** cohesion_judge (Phase 5, not yet implemented), spirit_guide_voice (instrumented but gated on earth_self_name — not passed in standard runs), llm_judge for mechanical tagging (not an LLM call site; rule-based).

5. **Cost savings if cache deployed: <$0.01/season.** DiskCache already captures all actual repeats. DB-level cache adds operational complexity for negligible gain.

### Data artifacts

Companion CSV files at `agentic_orchestration/star-lord/research/g12-llm-cache-hit-rate-measurement-2026-05-25/`:
- `llm_calls_window_2wk.csv` — full 3,001-row extract with key columns
- `per_surface_breakdown.csv` — per-purpose aggregated stats
- `repeated_prompt_signatures.csv` — all 7 repeated cache_key entries

### Acceptance criteria

- [x] LLM-call repeat rate measured over last 2 weeks; normalization protocol documented
- [x] Per-surface breakdown (all 8 active surfaces; 3 absent surfaces explained)
- [x] G12 verdict: NOT TRIGGERED
- [x] Cost savings estimate: <$0.01/season; negligible
- [x] Companion data CSV files at named research path
- [x] Auto-commit fires post-completion-record write
- [ ] Tag: `star-lord/g12-llm-cache-hit-rate-measurement-2026-05-25` (post-commit)
