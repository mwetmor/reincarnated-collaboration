# Wave-S LLM Call Infrastructure — Implementation Notes

**Date:** 2026-05-29
**Author:** star-lord
**Dispatch:** `agentic_orchestration/dispatches/2026-05-29-star-lord-cascade-r4-followon-llm-naming-gaps.md` Scope 2
**Spec authority:** `agentic_orchestration/gandalf/notes/2026-05-29-wave-s-season-naming-design-spec.md` (commit `a8d5a28`; tag `gandalf/v1.0-wave-s-season-naming-spec-1`)
**Engine commit:** Cascade-R4 Follow-On Scope 2 (star-lord 2026-05-29)
**Tag:** `star-lord/v1.0-wave-s-implementation-1`

---

## 1. Implementation Summary

Wave-S is implemented as a fourth Phase 5 LLM call surface in
`reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py`.

**Sequencing per gandalf spec § 6:**
```
Wave A → {Wave-S, F-C} (parallel) → Wave B
```

Wave-S fires AFTER Wave A (consumes faction-name + thematic-tag substrate),
PARALLEL with F-C (no inter-dependency), BEFORE Wave B (Wave B's SEASON_CONTEXT
block consumes {season_name} — wired by rocket in orchestrator integration).

**Volume:** k=1 per season (one season name; season-stable forever).
**Cost:** ~$0.015/season (250-350 tokens per call).

---

## 2. Functions Implemented

| Function | Location | Purpose |
|---|---|---|
| `_build_wave_s_system_prompt()` | phase5_orchestrator.py | SYSTEM prompt per spec § 4.1 |
| `_build_wave_s_user_prompt(...)` | phase5_orchestrator.py | USER prompt per spec § 4.2; W-S8 purity at assembly |
| `_parse_wave_s_response(response_text)` | phase5_orchestrator.py | JSON parse; required-key validation; float coerce |
| `_validate_wave_s_acceptance(parsed, wanderer_count, prior_season_names)` | phase5_orchestrator.py | All 10 gates W-S1..W-S10 |
| `_call_wave_s_single(...)` | phase5_orchestrator.py | Async call; 3-attempt backoff; max 1 regen on W-S6/W-S7 |
| `run_wave_s_async(faction_clusters_input, config, prior_season_names, tracker)` | phase5_orchestrator.py | Orchestration entry; substrate aggregation; k=1 |
| `build_export_season_name(wave_s_result, season_id)` | phase5_orchestrator.py | Boundary-validated export dict for season_summary.json |

**New constants:**
- `AI_TELL_PHRASES_WAVE_S` — 18 phrases (11 season-specific per spec + 7 shared base)
- `WAVE_S_COST_ANOMALY_THRESHOLD_USD = 0.03` — 2× upper bound
- `WAVE_S_PATTERN_REGEX` — Pattern A / B regex per spec § 5 W-S2

**New dataclasses / extensions:**
- `Phase5WaveSResult` — 16-field result dataclass
- `Phase5OrchestratorConfig.wave_s_max_tokens: int = 256`
- `Phase5Result.wave_s_result / wave_s_cost_usd / wave_s_cost_anomaly_flagged` — 3 new fields

---

## 3. Acceptance Gates W-S1..W-S10

All 10 gates from gandalf spec § 5 implemented in `_validate_wave_s_acceptance()`.

| Gate | Failure → status | Implementation |
|---|---|---|
| W-S1 | FAIL_RECORD | word_count in [3,7] for A; [3,5] for B |
| W-S2 | FAIL_RECORD | WAVE_S_PATTERN_REGEX.match() |
| W-S3 | ACCEPT_WARN | len(substrate_signals_referenced) >= 2 |
| W-S4 | FAIL_RECORD | ai_tell_grep_check(season_name, AI_TELL_PHRASES_WAVE_S) |
| W-S5 | FAIL_RECORD | SUBSTRATE_PURITY_VOCAB_REGEX.search(season_name) |
| W-S6 | FAIL_RECORD (→ regen) | ai_tell_compliance_score >= 0.7 |
| W-S7 | FAIL_RECORD (→ regen) | Jaccard distance >= 0.5 vs each prior season name |
| W-S8 | CascadeBlockError (halt) | SUBSTRATE_PURITY_VOCAB_REGEX at _build_wave_s_user_prompt() |
| W-S9 | ACCEPT_WARN (soft) | null iff wanderer_count==0; <=1 sentence if wanderer_count>=1 |
| W-S10 | via W-S6 | register coherence; backstopped by self-assessment score |

**Regeneration discipline (spec § 5):**
- Max 1 regeneration per call on W-S6 OR W-S7 fail
- W-S7 regen: diversity-penalty preamble appended to SYSTEM; prior season names enumerated
- temperature=0.85 on regen (higher than 0.7 primary; promotes diversity)
- Second fail → FAIL_RECORD + KR surface (no silent fallback; high-trust real-estate)

---

## 4. AsyncAnthropic vs LLMClient.complete() Routing Decision

**Decision:** AsyncAnthropic direct call (same pattern as Wave A/B/F-C).

**Trade-off analysis:**

| Factor | AsyncAnthropic | LLMClient.complete() |
|---|---|---|
| Cache recoverability | No (Scope 1 root cause) | Yes (DiskCache + LLMLogger) |
| Non-recoverability cost at k=1 | ~$0.015/season | N/A |
| Async consistency | Native (same pattern as all waves) | Requires sync wrapping for async context |
| Implementation complexity | Minimal (pattern copy) | Moderate (async wrapper needed) |
| Pattern consistency | Matches Wave A/B/F-C | Breaks pattern for this seam only |

**Rationale:** Wave-S is k=1/season at ~$0.015/call. The non-recoverability exposure is
trivially small compared to Wave B's $1.00 non-recoverability. The benefit of
LLMClient.complete() routing (cache hit on identical re-fire) is also trivially small
at k=1 (season names don't repeat). Async consistency with Wave A/B/F-C outweighs
the small cache benefit.

**If this should change:** if Wave-S ever runs in multi-season parallel batches (e.g.,
batch retroactive execution of 100 past seasons), the cost asymmetry changes and
LLMClient.complete() routing becomes more compelling. At that point, wrap
LLMClient.complete() in `asyncio.get_event_loop().run_in_executor()` and add to semaphore pattern.

**Root cause connection:** Scope 1 showed the AsyncAnthropic bypass WAS the root cause
of Wave B non-recoverability at $1.00 scale. This is documented at
`agentic_orchestration/star-lord/notes/2026-05-29-wave-b-cache-recoverability-investigation.md`.
The decision to use AsyncAnthropic for Wave-S is made WITH that context; the scale
difference (k=1 vs k=100) justifies different conclusions for the same architectural pattern.

---

## 5. Substrate Aggregation in run_wave_s_async

`run_wave_s_async` aggregates substrate from `faction_clusters_input` (post-Wave-A list)
before calling `_call_wave_s_single`. Aggregation:

- **faction_name_set:** prefer `faction_name` (Wave A output); fallback to `faction_label_placeholder`
- **faction_thematic_tags_aggregate:** flatten + deduplicate (preserve order; exact duplicates removed)
- **element_weighted:** weighted by `member_count` per cluster; dominant_element = max(weighted)
- **lineage_weighted:** weighted vote by `member_count`; modal_cultural_lineage = max(weighted)
- **wanderer_count:** sum `member_count` where `cluster_id == "SINGLETON"` (Amendment 1)

This matches gandalf spec § 2 substrate-inputs table exactly.

---

## 6. season_summary.json Extension (rocket integration target)

`build_export_season_name()` produces a dict with 14 fields (7 primary + 7 quality).

All fields start with `wave_s_` prefix. All are additive to `season_summary.json`.
Pre-Wave-S seasons will have these fields absent (defaulting to null on read).
No breaking change.

**Rocket integration steps (NOT star-lord scope):**
1. Call `run_wave_s_async` after Wave A completes, parallel with `run_fc_per_pair_async`
2. After both Wave-S and F-C complete, call `run_wave_b_async` passing `season_name` as `{season_name}` in SEASON_CONTEXT block per spec § 6
3. Call `build_export_season_name(result.wave_s_result, season_id)` and merge into `season_summary.json`
4. Retroactive backfill for season_001/002/003 (chronological; prior_season_names accumulates)

---

## 7. Test Coverage

66 tests PASS in `tests/test_wave_s_season_naming_impl.py`:
- Group 1: Phase5WaveSResult dataclass (4 tests)
- Group 2: _build_wave_s_system_prompt (6 tests)
- Group 3: _build_wave_s_user_prompt (8 tests)
- Group 4: _parse_wave_s_response (5 tests)
- Group 5: _validate_wave_s_acceptance — W-S1..W-S10 individually tested + Pattern A/B election + full ACCEPT path (28 tests)
- Group 6: TestWaveSConstants + TestBuildExportSeasonName (15 tests)

Prior baseline: 253/253 PASS (all LLM wave tests: wave_b_impl + wave3_fc_infra + wave_composition_rules)
Combined: 319/319 PASS, 0 regressions.

---

## 8. Cross-Seam Data Contract

**For rocket (primary consumer):**
- Entry point: `run_wave_s_async(faction_clusters_input, config, prior_season_names=None, tracker=None)`
- Returns: `Phase5WaveSResult` (access via `result.season_name`, `result.season_sub_narrative`, etc.)
- Export builder: `build_export_season_name(wave_s_result, season_id)` → dict for season_summary.json
- Public exports: `Phase5WaveSResult`, `run_wave_s_async`, `build_export_season_name` all in `llm/__init__.py`

**Retroactive backfill ordering (spec § 8):**
```python
# season_001: no prior names
result_001 = await run_wave_s_async(clusters_001, config_001, prior_season_names=[])
# season_002: prior = [season_001 name]
result_002 = await run_wave_s_async(clusters_002, config_002, prior_season_names=[result_001.season_name])
# season_003: prior = [season_001, season_002 names]
result_003 = await run_wave_s_async(clusters_003, config_003, prior_season_names=[result_001.season_name, result_002.season_name])
```

**For drax (downstream consumer):**
- Fields to consume: `wave_s_season_name_canonical`, `wave_s_season_name_narrative_short`, `wave_s_pattern_used`
- `wave_s_season_name_canonical` unblocks summary-tab header line
- All fields nullable; guard with null-check

---

## 9. MIGRATION.md

Filed at `reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.63-wave-s-season-naming.

---

**Signed:** star-lord (operational-pipeline seam owner)
**Status:** COMPLETE — Wave-S infrastructure fully implemented; 66 new tests PASS; 0 regressions; MIGRATION.md § v1.63 authored; notes doc filed
