# IA-1 Engine-Readiness Pre-Fire Response

**From:** star-lord (Phase 5+ pipeline owner; export/telemetry/LLM seam)
**Date:** 2026-06-01
**Dispatch:** `agentic_orchestration/dispatches/2026-06-01-star-lord-rocket-ia-1-engine-readiness-pre-fire-question.md`
**Authority:** Matt 2026-06-01 strategic reset + jack-ryan IA-1 Gate-1 PASS (commit `0eff666`)

---

## 1. Readiness verdict: MINIMAL-SETUP-REQUIRED

The pipeline is structurally sound end-to-end. However, the Drift-14 auto-demote behavior at load creates a material quality concern that requires one setup step before V1 fire produces a season worth shipping to drax. Details follow.

---

## 2. Pipeline end-to-end assessment

### 2.1 Which pipeline fires for IA-1 V1

IA-1 V1 "baseline season generation" uses the CLI-based `SeasonOrchestrator` (`src/reincarnated/generation/season_orchestrator.py`), invoked via:

```
python -m reincarnated.cli generate-season [--seed N] [--output DIR]
```

This is distinct from `wave5_season_orchestrator.py` (Cycle 14 Wave 5 cohesion-judge pipeline). The Wave 5 orchestrator does NOT reference pool.json or `select_seasonal_elements()`; it consumed a pre-built kit archive and fired Phase 5 cohesion-judge on top. IA-1 V1 is the SeasonOrchestrator path.

### 2.2 Substrate paths — what the pipeline reads

- `data/seasonal_elements/pool.json` (v1.1) — consumed via `element/selector.py:select_seasonal_elements()` → `element/pool.py:load_element_pool()`
- `data/seasonal_elements/vfx_coverage_manifest.json` — consumed at `load_element_pool()` time by `_validate_pool_invariants()` (Drift-14 gate)
- `config/elements.yaml` — canonical-7+1 element catalog (not changed; preserved)
- No reference to `data/seasonal_elements/physical_taxonomy.json` in the CLI pipeline (physical taxonomy is Architecture-A metadata; SeasonOrchestrator handles physical through its existing schema)

Pool.json v1.1 schema extension (4 additive fields: `substrate_validation_lineage`, `vocabulary_commonness`, `slot_unambiguous`, `ws1a_q18_lock_date`) — all have safe Pydantic defaults. The CLI pipeline reads `PoolElement` from `element/schema.py`. Reading the 4 new fields from pool.json via `PoolElement(**entry)` is backward-compat with all prior code. No code change needed to consume v1.1 pool.json. Confirmed from Gate-2 cross-seam ACK: "star-lord: no-action-required."

### 2.3 Skill-naming, class-naming, faction-naming sub-pipelines

`naming.py` (`name_skill`, `name_class`, `name_monster`, `name_gear_item`) references `elements.slots` (dict-keyed via Coupling #1; D6 Step 4). This is canonical-4 compatible today. SeasonorChestrator calls `select_seasonal_elements()` which populates `SeasonalElements.slots` dict. The naming layer reads `elements.slots.get(canonical_element)` — picks up the selected pool.json entry's `element_name`. No changes needed to naming prompts or path references.

The grouping-layer vocabulary loader (`grouping_vocabulary_loader.py`) loads at import time from `canonical/story/grouping-layer-vocabulary.md` v1.2. This provides canonical-4 + canonical-7 coverage. Pattern P7 CLOSED (KeyError on unknown substrate). No substrate expansion is needed for IA-1 V1 (canonical-4 fire).

Faction-naming: `phase5_orchestrator.py` (star-lord seam) handles Wave A faction-label + Wave B per-kit identity. For IA-1 V1 (SeasonOrchestrator path), this orchestrator is wired indirectly via Phase 5 sub-pipeline calls. The Phase 5 orchestrator is operational at commit `62f1429` (swift-closure COMPLETE; 250/250 tests PASS).

---

## 3. Drift-14 auto-demote assessment

### 3.1 Empirical scope (measured from engine)

- Pool.json v1.1: 100 allow-list entries (ws1a_q18_lock_date=2026-06-01 lock cohort = ALL 100)
- VFX manifest: 42 entries that cover allow-list entries
- Lock cohort entries covered by manifest: 42 of 100
- Lock cohort entries WITHOUT manifest coverage: **58 of 100** — these auto-demote to "eligible" at load

### 3.2 Per-primary effective allow-list post-Drift-14

After `_validate_pool_invariants()` applies at load:

| Primary | Effective allow-list | Demoted to eligible |
|---|---|---|
| fire | 10 (ember/cinder/blaze/scorch/lava/magma/charcoal/char/brand/flare) | 6 (inferno/ignite/fira/fusion/thermal/combustion) |
| water | 8 (tide/brine/frost/mist/ice/glacier/wave/marsh) | 6 (aqua/glacial/chill/torrent/hydro/hydraulic) |
| earth | 14 (stone/granite/marble/clay/sand/iron/gold/silver/lead/gem/crystal/obsidian/amber/thorn) | 4 (quake/tremor/seismic/tectonic) |
| wind | 5 (gale/gust/hail/sleet/cloud) | 8 (tempest/cyclone/whirlwind/hurricane/squall/zephyr/sonic/shockwave) |
| lightning | 1 (spark only) | 12 (arc/static/surge/volt/bolt/shock/thunder/plasma/flash/ion/voltage/tesla) |
| holy | 0 | 14 (all 14 holy entries) |
| shadow | 0 | 12 (all 12 shadow entries) |

### 3.3 Material quality impact

**Fire, water, earth:** acceptable. 8-14 effective allow-list entries per primary; LLM selection and deterministic fallback both have a viable pool. Weight is 2x for allow-list entries; "eligible" entries (post-demote) compete at 1x weight. Quality degraded vs. intended but functional.

**Wind: borderline.** 5 effective allow-list entries. The most evocative wind entries (tempest/cyclone/whirlwind/hurricane/squall/zephyr) are all demoted. The 5 that remain are the weaker half of the wind pool. This produces materially weaker wind-element season flavor.

**Lightning: critical.** 1 effective allow-list entry (spark). All 13 Q18-locked lightning entries except spark will demote to eligible. `spark` carries 2x weight; other 12 are 1x. The LLM prompt pool section shows lightning almost entirely as eligible. This is the worst-affected primary.

**Holy and shadow: critical.** Zero effective allow-list entries. No 2x-weight anchors exist for these primaries. All 14 holy and 12 shadow entries demote to eligible (1x weight uniform). For canonical-4 seasons (fire/wind/water/earth only), this is NOT a problem — holy and shadow slots do not fire in V1. BUT: if IA-1 V1 fires a canonical-4 season, this is irrelevant for holy/shadow. Confirmed: current SeasonOrchestrator generates canonical-4 seasons (VALID_SLOTS = fire/wind/water/earth). Lightning is not a canonical-4 primary. So the lightning demote is also irrelevant for canonical-4 V1 fire.

### 3.4 Drift-14 verdict for IA-1 V1 (canonical-4)

For a canonical-4 season (fire / wind / water / earth), the Drift-14 auto-demote affects only these four primaries. Fire and earth have adequate effective allow-lists (10 and 14 entries respectively). Water has 8 — acceptable. **Wind has 5 effective allow-list entries** — this is the one material concern.

The 5 remaining wind allow-list entries (gale / gust / hail / sleet / cloud) are Q18-locked pool members but are the flatter half of the wind vocabulary. The Q18-locked entries that demote (tempest/cyclone/whirlwind/hurricane/squall/zephyr/sonic/shockwave) are the higher-signal wind words. The LLM will still see ALL 13 wind entries in the prompt (eligible entries appear in the pool section at 1x weight), so it CAN select the demoted entries — it just won't receive the 2x weighting signal. The deterministic fallback would preferentially draw from the 5 allow-list entries.

**Assessment:** The Drift-14 demote degrades but does not break IA-1 V1 quality. The season is generatable; the element selection will draw from a degraded allow-list signal for wind specifically. This is acceptable V1 baseline behavior.

### 3.5 Setup step to address Drift-14

**Option A (recommended for V1):** Accept degraded allow-list signal as V1 baseline behavior. No setup required for element selection. The 58 Q18-lock entries demote to eligible; LLM still sees them; wind has 5 allow-list anchors. Season generates with adequate quality for drax integration testing. vfx_coverage_manifest extension is deferred (strategic reset disposition confirmed).

**Option B (if Matt wants better wind fidelity for V1):** Temporarily add the 8 most critical wind entries (tempest/cyclone/whirlwind/hurricane/squall/zephyr/sonic/shockwave) to vfx_coverage_manifest.json with tier B ratings. This is a star-lord-seam write to the manifest — not pool.json itself — and requires Matt authorization per ADR-006 (external data file write). This restores 2x weight for the wind pool's evocative core.

**Star-lord recommendation:** Option A. The V1 goal is baseline season generation + drax integration. Wind with 5 allow-list anchors is a known and traceable degradation, not a silent failure. The WARN logs at pool load will make it visible. Commit to Option B as a V2 pre-fire setup step if needed (IA-1 V2 post-IA-2).

---

## 4. LLM-call infrastructure readiness

### 4.1 Phase 5 cohesion-judge

The Phase 5 orchestrator (`llm/phase5_orchestrator.py`) is operational at engine commit `62f1429`. The swift-closure LLM fire confirmed: Wave A / Wave B / F-C / Wave-S all executed successfully; 250/250 tests PASS; cost ledger live via TrackedLLMClient.

For IA-1 V1 using the SeasonOrchestrator, the relevant LLM infrastructure is:
- `naming.py` — `name_skill`, `name_class`, `name_monster`, `name_gear_item` (via `LLMClient.complete_json`)
- `selector.py` — `select_seasonal_elements` (element selection LLM call + novel word scoring)
- `season_orchestrator.py` — wires TrackedLLMClient via `_make_recorder()` in cli.py

### 4.2 Cost tracking

`TrackedLLMClient` is operational. Per-call cost estimation: `_COST_PER_MILLION` pricing table includes `claude-sonnet-4-6` ($3.00 input / $15.00 output per million tokens). At $0.85–1.00 empirical per full season regen, the cost ledger is active. Anomaly detection via log WARNING at 2× expected (per AGENT_STATE.md).

### 4.3 API key

`ANTHROPIC_API_KEY` must be set in environment. CLI gracefully falls back to no-LLM mode if key missing (logs WARNING; degrades to deterministic fallback on element selection + no naming). For IA-1 V1 with full LLM naming, the key must be present.

### 4.4 LLM-side setup needed?

None. No prompt template changes are required. The Q18 vocabulary is available as substrate through pool.json v1.1 (the LLM sees the pool section in the element selection prompt). No prompt tweak references any external file path — the element pool section is dynamically built from `_format_pool(active_pool)` in `selector.py`, which reads the (post-Drift-14) active pool at runtime. The vocabulary is already in the substrate; the prompt picks it up automatically.

---

## 5. Rocket coordination surface

**None required for pre-fire assessment.**

One item to surface for rocket awareness (not blocking):

The `season_generation_pipeline.py` pipeline (Cycle 13 Wave 5) hardcodes `SEASON_ID = "cycle-13-mechanical-season-001"` and has hardcoded assertions (`assert final_result["cohort_count"] == 4`). If IA-1 V1 uses `run_season_generation()` from this module, those hardcoded values will either need updating or a new pipeline entry point is needed. However, based on the dispatch context ("Phase 5+ pipeline against current substrate; existing prompt design; no Q16/Q17/Q19 required"), IA-1 V1 most likely uses the CLI `generate-season` command (`SeasonOrchestrator`), not the Cycle 13 Wave 5 mechanical pipeline.

**Rocket coordination item:** Confirm which entry point fires for IA-1 V1:
- `python -m reincarnated.cli generate-season` (SeasonOrchestrator path) — correct for "fire a season with current substrate + existing Phase 5 naming pipeline"
- `run_season_generation()` from `season_generation_pipeline.py` — Cycle 13 Wave 5 mechanical pipeline (hardcoded season_id; may not be the intended IA-1 V1 entry point)

If rocket confirms the CLI path, no changes needed. If rocket intends `run_season_generation()`, SEASON_ID update is a one-line rocket-seam change. Routing this to rocket for confirmation is recommended.

---

## 6. Minimal setup steps (if MINIMAL-SETUP-REQUIRED path)

Three items, in priority order:

**Setup Step 1 (required — environment):** Confirm `ANTHROPIC_API_KEY` is set in execution environment before firing. Without it, season generates with deterministic fallback on element selection and no LLM naming (no-LLM mode). For a named V1 season: key required.

**Setup Step 2 (required — confirm entry point with rocket):** Confirm IA-1 V1 fires via `python -m reincarnated.cli generate-season` (SeasonOrchestrator; uses pool.json v1.1; READY). If instead `run_season_generation()` from `season_generation_pipeline.py` is intended, a SEASON_ID update is needed (rocket seam).

**Setup Step 3 (optional — Drift-14 wind fidelity):** If Matt wants better wind allow-list fidelity for V1, add 8 wind entries to `vfx_coverage_manifest.json` (tier B ratings). Requires Matt authorization per ADR-006. If not, accept Option A (5-entry wind allow-list) as V1 baseline.

---

## 7. Estimated V1 fire wall-clock

Based on empirical from AGENT_STATE.md and project memory:

- Full season regen (SeasonOrchestrator, inverted mode): ~$0.85–1.00 LLM cost
- At ~388 LLM calls/season (per CLI docstring), with 2-4 sec/call and DEFAULT_CONCURRENCY=10 (phase5_orchestrator): concurrent calling is in naming.py (sequential per class/skill), so wall-clock is roughly sequential
- Empirical from prior seasons: **~15–25 minutes wall-clock** for a full named season (varies by class count, fight count, LLM latency)
- Smoke mode (`--smoke`): 5 classes, 30 fights — **~3–5 minutes**

For IA-1 V1 baseline fire: budget 20 minutes wall-clock for a full named season, or 5 minutes for smoke validation first.

---

## 8. Routing back to KR

**MINIMAL-SETUP-REQUIRED.** Two steps before fire dispatch:

1. KR confirms / routes to rocket: "confirm IA-1 V1 entry point is CLI generate-season (not season_generation_pipeline.py)." Rocket should confirm or name the correction needed (1-line if correction needed).
2. Execution environment must have `ANTHROPIC_API_KEY` set — this is operational pre-check, not a code change.

Once rocket confirms entry point and API key is confirmed present: **fire IA-1 V1 immediately.**

Drift-14 wind degradation: acceptable V1 baseline behavior (Option A). WARN logs will appear at load for 58 demoted entries. This is expected behavior per strategic reset disposition (vfx_coverage_manifest extension DEFERRED).

---

## 9. Appendix — what star-lord seam specifically verified

- `element/pool.py` `_validate_pool_invariants()` behavior: confirmed auto-demote logic at lines 82–102
- `data/seasonal_elements/vfx_coverage_manifest.json`: 42 entries; 100 lock cohort entries; 58 uncovered → demote confirmed empirically
- `element/selector.py`: pool.json consumed via `load_element_pool()` → `_validate_pool_invariants()` at selection time; effective allow-list at runtime is post-demote state
- `element/schema.py` v1.1: 4 additive fields present; Pydantic safe defaults confirmed; backward-compat confirmed
- `llm/naming.py`: references `elements.slots` dict (D6 Step 4); no canonical-four labels in prompts; grouping-layer vocabulary loaded at import
- `llm/tracked_client.py`: cost tracking operational; pricing table includes claude-sonnet-4-6
- `llm/phase5_orchestrator.py`: operational at commit `62f1429`; Wave A/B/F-C/S all implemented; 250/250 tests PASS
- `export/AGENT_STATE.md`: last star-lord tag `star-lord/v1.5-cycle-14-wave-5-swift-closure-cohesion-judge-snapshot-1`; no star-lord-seam carry-forward items that block IA-1 V1 fire

---

**Signed:** star-lord (export/telemetry/LLM seam)
**For:** IA-1 engine-readiness pre-fire response; Routing: MINIMAL-SETUP-REQUIRED (2 setup steps; fire after confirmation)
