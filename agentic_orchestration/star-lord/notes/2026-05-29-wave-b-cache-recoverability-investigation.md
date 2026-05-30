# Wave B Cache Recoverability Investigation

**Date:** 2026-05-29
**Author:** star-lord
**Dispatch:** `agentic_orchestration/dispatches/2026-05-29-star-lord-cascade-r4-followon-llm-naming-gaps.md`
**Scope:** Determine whether Wave B per-kit character name LLM responses from the 3 cascade-r4 production seasons can be recovered from cache, logs, or telemetry — or whether re-fire is required.

---

## 1. Execution Timeline

Wave B implementation landed at commit `a553950` (2026-05-29 11:16).

Cascade-r4 production runs (seasons 001/002/003):
- Season 001: was re-fired as part of cascade-r3 RE-FIRE-3 (`85d8b41`, 2026-05-29 18:17)
- Seasons 002/003: fired via `dc3124d` (`run_season_production` multi-season runner, 2026-05-29 22:32)

**All 3 production seasons ran AFTER Wave B implementation.** Wave B did fire. The `wave_b_kit_count` and `wave_b_cost_usd` fields in `phase5_faction_clusters.json` are ACTUAL values from real LLM calls, not projections.

Evidence:
- Season 001: `wave_b_kit_count=34`, `wave_b_cost_usd=0.34`
- Season 002: `wave_b_kit_count=33`, `wave_b_cost_usd=0.33`
- Season 003: `wave_b_kit_count=33`, `wave_b_cost_usd=0.33`
- Total actual Wave B LLM spend: **~$1.00** (100 kits across 3 seasons)

---

## 2. Cache Investigation

### 2a. DiskCache (primary path for LLMClient.complete())

**Location:** `/Users/admin/Games/reincarnated-engine/cache/llm/`
**File count:** 12,533 SHA-256-keyed JSON files
**Cache mechanism:** `DiskCache` at `src/reincarnated/llm/cache.py` — SHA-256 of `{model, system, user, temperature}` → disk file
**Cache construction site:** `LLMClient.complete()` at `src/reincarnated/llm/client.py:60-74`

**Wave B calls bypass this cache entirely.**

`_call_wave_b_single` (phase5_orchestrator.py:1930) uses `await async_client.messages.create(...)` — direct `AsyncAnthropic` SDK call. It does NOT call `LLMClient.complete()`. The `DiskCache` is only populated when `LLMClient.complete()` is called. Therefore:
- None of the 12,533 cache files contain Wave B responses.
- Re-run of Wave B with identical prompts would make fresh API calls (no cache hit possible).

### 2b. LLM Logger (secondary audit trail)

**Location:** `/Users/admin/Games/reincarnated-engine/logs/llm/`
**Files:** `llm_20260507.jsonl` through `llm_20260526.jsonl` (10 files)
**Logger construction site:** `LLMLogger` used by `LLMClient.complete()` only.

Wave B calls bypass the LLMLogger for the same reason as DiskCache — `_call_wave_b_single` does not route through `LLMClient.complete()`. The most recent log file is dated 2026-05-26; the cascade-r4 production runs happened 2026-05-29. Even if the logger were wired, there are no log entries from 2026-05-29.

### 2c. Telemetry DB (llm_calls table)

**Relevant DBs checked:**
- `/Users/admin/Games/reincarnated-engine/data/telemetry.db` — 0 rows for purpose=`wave_b_kit_identity`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/telemetry/telemetry.db` — 0 rows (empty llm_calls table)
- Season-specific `telemetry.db` files (season-001 only present) — does not exist for seasons 002/003; season-001 telemetry.db has no tables matching llm_calls schema

**Why telemetry is empty for Wave B:** `wave5_season_orchestrator.py:run_phase5_cohesion_judge()` (line 1609) constructs `TrackedLLMClient` with `NullRecorder()`. Per the code comment at line 1603-1607: "NullRecorder: no DB write (no telemetry DB connection at this call site)." The `_call_wave_b_single` additionally uses a separate `tracker` reference for telemetry recording (lines 1901-1918), which also points to `NullRecorder`.

### 2d. Phase5_faction_clusters.json and other artifacts

The `phase5_faction_clusters.json` artifacts in each season directory record `wave_b_kit_count` and `wave_b_cost_usd` in metadata only. No `Phase5WaveBResult` fields (`kit_name_canonical`, `kit_identity_narrative`, `ai_tell_compliance_score`, `cohesion_judge_confidence`) are written to any disk artifact.

The write-path gap: `run_phase5_cohesion_judge()` returns `wave_b_results` dict; callers (`run_wave5_season_001` and `run_season_production`) use it only to populate `cohesion_data` for Phase 7 gate scores. No write to `wave_b_*.json` or any analogous artifact occurs anywhere in `wave5_season_orchestrator.py`.

---

## 3. Recoverability Disposition Per Season

| Season | Wave B Fired? | Kit Count | Actual Cost | Cache Recoverable? | Log Recoverable? | Telemetry Recoverable? |
|---|---|---|---|---|---|---|
| cycle-14-wave-5-season-001 | YES (cascade-r3 RE-FIRE-3) | 34 kits | $0.34 | NO | NO | NO |
| cycle-14-wave-5-season-002 | YES (cascade-r4 Track A) | 33 kits | $0.33 | NO | NO | NO |
| cycle-14-wave-5-season-003 | YES (cascade-r4 Track A) | 33 kits | $0.33 | NO | NO | NO |

**Disposition: NOT RECOVERABLE across all 3 seasons.**

All recovery paths are closed:
1. DiskCache — bypassed by async direct call; 0 Wave B files
2. LLMLogger — bypassed; no 2026-05-29 log files
3. Telemetry DB — NullRecorder; 0 rows written
4. JSON artifacts — write path does not exist

---

## 4. Root Cause of Missing Persistence

Two independent gaps compound:

**Gap 1 (architecture): Wave B bypasses LLMClient.**
`_call_wave_b_single` uses `AsyncAnthropic` directly, not `LLMClient.complete()`. This was a deliberate design choice for async performance (Phase 5 fan-out across 33-40 kits). Consequence: DiskCache and LLMLogger — both built into `LLMClient.complete()` — are not called.

**Gap 2 (orchestrator): no Wave B JSON write.**
`wave5_season_orchestrator.py` returns `wave_b_results` from `run_phase5_cohesion_judge()` and uses it to populate `cohesion_data` for Phase 7. It does not serialize `wave_b_results` to a `wave_b_identities.json` artifact or append it to `phase5_faction_clusters.json`. The write simply does not exist.

Gap 1 explains why cache/log recovery is impossible.
Gap 2 explains why the names are missing from output artifacts.
Gap 2 is what rocket's dispatch would fix (persistence write path). Gap 1 is a separate follow-on concern (add DiskCache support to async path) but is lower priority.

---

## 5. Retroactive Cost Projection

To retroactively generate Wave B names for all 3 seasons:

| Season | Kits | Expected Cost @ $0.01/kit |
|---|---|---|
| season-001 | 34 kits | ~$0.34 |
| season-002 | 33 kits | ~$0.33 |
| season-003 | 33 kits | ~$0.33 |
| **Total** | **100 kits** | **~$1.00** |

This is within standard per-season LLM budget. Cost is deterministic (same kit inputs → same prompt structure; temperature=0.7 so results will differ from original run, but cost will be identical).

Retroactive re-fire is the ONLY recovery path. There is no cheap replay option.

---

## 6. Impact on Current Season Artifacts

The following downstream consumers are currently blocked on per-kit character names:

| Consumer | Blocker | Impact |
|---|---|---|
| Drax loadout summary tab | `wave_b_name` absent from any JSON artifact | Faction tiles show member counts only; no per-kit names |
| Legolas image-gen prompts | `[wave_b_name]` blank in per-kit prompt templates (34 season-001 instances) | § 12.2 hero image gen blocked at wave_b_name layer |
| kit_archive.db `notes` field | cohesion_data populated from Wave B scores; but names never written to DB | Per-kit name absent in archive |

---

## 7. Recovery Requirements (for rocket dispatch)

To fix Gap 2 (persistence write path):

1. Add `wave_b_identities.json` write in `run_phase5_cohesion_judge()` (within `run_wave5_season_001` and `run_season_production`) — serialize `wave_b_results` dict as `{kit_id: {kit_name_canonical, kit_identity_narrative, ai_tell_compliance_score, cohesion_judge_confidence}}` to `{output_dir}/wave_b_identities.json`
2. Alternatively extend `phase5_faction_clusters.json` per-kit member entries with `wave_b_name_canonical` and `wave_b_identity_narrative` fields
3. Retroactive re-fire: re-run Phase 5 Wave B only for the 3 existing seasons using current kit populations from `phase4_archive_insertion.json` + `phase5_faction_clusters.json` faction context

Schema target per dispatch instruction: extend `season_summary.json` is an option but Wave B is per-kit (100 entries); a separate `wave_b_identities.json` file is cleaner than embedding 100-entry JSON in season_summary.

---

## 8. KR Routing Triggers

- **Wave B NOT recoverable across all 3 seasons** — re-fire authorization required (~$1.00 within cap; standard per-season budget already spent once)
- **rocket dispatch for Gap 2 fix** — persistence write path for future seasons (prevents recurrence)
- **Gap 1 note for rocket/star-lord follow-on** — async DiskCache support for Wave B calls (lower priority; prevents future silent loss but does not change current retroactive cost)

---

## 9. Wave-S Spec Status

Gandalf Wave-S design spec has NOT landed at time of this report (no file at `agentic_orchestration/gandalf/notes/2026-05-29-wave-s-season-naming-design-spec.md` or equivalent). Scope 2 (Wave-S LLM call infrastructure) is blocked pending spec. Placeholder authored in dispatch file; Scope 2 execution deferred until spec arrives.

---

**Signed:** star-lord (operational-pipeline seam owner)
**Status:** COMPLETE — Scope 1 investigation fully executed; recoverability disposition CLOSED; Gap 1+2 root cause documented; KR routing triggers surfaced
