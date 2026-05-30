# Dispatch: star-lord — Cascade-R4 Follow-On LLM Naming Gaps

**Date:** 2026-05-29
**Author:** knight-rider
**Agent:** star-lord
**Priority:** ROUTINE (post-cascade-r4 follow-on; no blocking gates)
**Authorization:** Matt 2026-05-29 directive verbatim: "Can we implement retroactive LLM naming across these gaps? Afterwards, let's plug the gaps for future generation." + hive-mind decision-routing

---

## § 1. Context

Cascade-r4 production output surfaces two LLM naming gaps:

1. **Wave B per-kit character names** — FIRE + COSTED (~$1.00 across 3 seasons; 100 kits) but NOT PERSISTED to JSON artifacts. `wave_b_results` dict lives only in-memory during season orchestration; no write path to `wave_b_*.json` exists.

2. **Season-itself names (Wave-S)** — NEVER IMPLEMENTED. No `season_name` generation code exists anywhere in engine src.

Matt directive asks: retroactive naming across these gaps + plug gaps for future generation.

---

## § 2. Scope 1 — Wave B Cache Recoverability Investigation

**STATUS: COMPLETE (star-lord 2026-05-29)**

Finding report: `agentic_orchestration/star-lord/notes/2026-05-29-wave-b-cache-recoverability-investigation.md`

### Key findings:

**All 3 seasons ran Wave B after implementation landed (commit `a553950` 11:16).** Wave B did fire. Costs are actual, not projected:
- Season 001: 34 kits, $0.34
- Season 002: 33 kits, $0.33
- Season 003: 33 kits, $0.33
- Total: ~$1.00

**Recoverability disposition: NOT RECOVERABLE across all 3 seasons.**

Three cache paths investigated:
1. **DiskCache** (`/Users/admin/Games/reincarnated-engine/cache/llm/`, 12,533 files) — Wave B calls use `AsyncAnthropic` directly, bypassing `LLMClient.complete()` and the DiskCache entirely. Zero Wave B files present.
2. **LLM Logger** (`/Users/admin/Games/reincarnated-engine/logs/llm/`) — Same bypass; last log file dated 2026-05-26; no 2026-05-29 entries exist.
3. **Telemetry DB** (engine `data/telemetry.db` + season `telemetry.db`) — `NullRecorder()` used in `run_phase5_cohesion_judge()`; 0 rows written for `purpose=wave_b_kit_identity`.

**Root cause — Gap 1:** `_call_wave_b_single` uses direct `async_client.messages.create()`, bypassing `LLMClient.complete()`, DiskCache, and LLMLogger.

**Root cause — Gap 2:** `wave5_season_orchestrator.py` extracts `cohesion_data` from `wave_b_results` for Phase 7 gate but never serializes the full `Phase5WaveBResult` objects (`kit_name_canonical`, `kit_identity_narrative`) to disk.

### KR routing from Scope 1:
- Wave B NOT recoverable → **re-fire required** (~$1.00; within standard cap; same budget already spent once)
- Gap 2 fix → rocket dispatch (persistence write path; prevents recurrence for future seasons)
- Gap 1 follow-on → async DiskCache support for Wave B (lower priority; prevents future silent loss)

---

## § 3. Scope 2 — Wave-S LLM Call Infrastructure

**STATUS: BLOCKED — gandalf Wave-S design spec not yet landed**

Gandalf Wave-S spec has NOT arrived at `agentic_orchestration/gandalf/notes/2026-05-29-wave-s-season-naming-design-spec.md` or equivalent location as of this report.

Per dispatch instructions: "If gandalf Wave-S spec NOT yet landed: complete Scope 1 fully; Scope 2 placeholder authored with iteration plan post-gandalf; surface to KR for sequencing."

### Scope 2 iteration plan (pending gandalf spec):

When gandalf Wave-S spec lands, star-lord implements in `phase5_orchestrator.py`:

1. `_build_wave_s_system_prompt()` / `_build_wave_s_user_prompt()` per gandalf spec
2. `_call_wave_s_single()` — single LLM call; no fan-out; semaphore + 3-retry exponential backoff
3. `_parse_wave_s_response()` — JSON parse + field validation
4. `_validate_wave_s_acceptance()` — D7 AI-tell compliance + gandalf acceptance gates
5. `run_wave_s_async()` — 1 call per season; parallel-OK with Wave B (no dependency)
6. Integration into `run_phase5_with_fc_and_wave_b_async/sync()` entry points

**Wave-S sequencing:** fires post-Wave-A (season-name informed by faction context); parallel-OK with F-C and Wave B.

**Cost model:** 1 LLM call per season ≈ $0.01-0.02; trivially bounded.

**Persistence target:** extend `season_summary.json` with Wave-S fields (additive; backward-compatible):
```
"wave_s_season_name_canonical": "...",
"wave_s_season_name_narrative_short": "...",
"wave_s_season_name_thematic_tags": [...],
"wave_s_llm_call_id": null,
"wave_s_cost_usd": 0.01
```

**Tests:** ~3-5 new (Wave-S call fires; parse/validate; acceptance gates; cost projection; integration with wave_b sequence).

### KR action required: sequence gandalf Wave-S spec dispatch → star-lord Scope 2 execution

---

## § 4. Deliverables Summary

| Item | Status |
|---|---|
| Wave B cache recoverability disposition per season | COMPLETE |
| Retroactive cost projection | COMPLETE (~$1.00 re-fire) |
| Gap 1 root cause (async bypass) | COMPLETE |
| Gap 2 root cause (no write path) | COMPLETE |
| Finding report committed | COMPLETE |
| Wave-S infrastructure implementation | BLOCKED (awaiting gandalf spec) |
| Wave-S persistence schema draft | COMPLETE (season_summary.json extension above) |
| Cross-seam impact (rocket + drax) | DOCUMENTED below |

---

## § 5. Cross-Seam Impact

### Rocket dispatch required (Gap 2 fix + retroactive re-fire):
1. Add `wave_b_identities.json` write path in `run_phase5_cohesion_judge()` — serialize full `Phase5WaveBResult` per kit to `{output_dir}/wave_b_identities.json`
2. Retroactively re-run Phase 5 Wave B for seasons 001/002/003 using existing kit population from phase4_archive + faction context from phase5_faction_clusters. Expected cost: ~$1.00 (same as first run).
3. On re-fire: seasons are deterministic for Phase 2-4 (DB already populated); Wave B is not cached (temperature=0.7, direct async call) so results will differ slightly from original run but acceptance criteria apply.

### Drax data contract:
- New `wave_b_identities.json` artifact added to season output directory
- `season_summary.json` Wave-S extension (additive; no breaking change)
- MIGRATION.md update required when rocket implements Gap 2 fix (per ADR-004)

---

## § 6. Tag

To be committed: `star-lord/v1.0-cascade-r4-followon-llm-naming-gaps-1`

---

## Completion Record

**Scope 1 COMPLETE 2026-05-29 (star-lord):**
- Wave B cache investigation executed across all 4 cache/log/telemetry locations
- Recoverability disposition: NOT RECOVERABLE across all 3 seasons
- Root cause 1 (async bypass) + Root cause 2 (no write path) documented
- Finding report at `agentic_orchestration/star-lord/notes/2026-05-29-wave-b-cache-recoverability-investigation.md`
- KR routing triggers surfaced: re-fire authorization (~$1.00) + rocket Gap 2 dispatch + gandalf Wave-S spec needed

**Scope 2 BLOCKED (star-lord):**
- Gandalf Wave-S spec not yet landed
- Iteration plan documented in § 3 above
- Awaiting KR sequencing of gandalf spec dispatch → star-lord Scope 2 execution
