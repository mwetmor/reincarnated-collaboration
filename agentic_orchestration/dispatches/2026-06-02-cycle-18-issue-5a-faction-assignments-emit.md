# Dispatch — 2026-06-02 — cycle-18 — Issue 5A — faction_assignments.json emit

**From:** knight-rider (orchestrator)
**To:** star-lord (PRIMARY — engine operational-pipeline seam owner) + rocket (generation seam consultant for Phase 5a clustering data source)
**Authority:** Matt 2026-06-02 verbatim "yes, let's do it all" → gandalf transmission with Issue 5A schema spec + LOCK Q ADDITIVE-ONLY discipline + ADR-004 cross-seam MIGRATION
**Wave:** cycle-18 Drax QDX-7-AMEND-FULL — Phase 1 (parallel with Issue 4 + Gate-1)
**State file:** `agentic_orchestration/cycle-18-drax-amend-full/wave-state.md`
**Tag intent:** `star-lord/v1.6-cycle-18-issue-5a-faction-assignments-emit-1`
**Estimated horizon:** ~1 session

---

## 1. Authoritative reading

1. **`agentic_orchestration/cycle-18-drax-amend-full/wave-state.md`** § 2 Issue 5A
2. **gandalf transmission 2026-06-02** — Issue 5A schema spec
3. **`canonical/story/2026-06-02-qdx-chain-wave-close-record.md`** § Phase 3 QDX-5 (event_008 metrics including 3 Wave A factions: Iron Ground Crushers / Scattered Meridian Cannons / Earthen Siege Wardens)
4. **`agentic_orchestration/qa/findings/2026-06-02-qdx-phase-3-qdx-5-gate-2.md`** (jack-ryan QDX-6 noted faction data lives in Phase 5a clustering output, not per-kit JSON)
5. **`~/Games/reincarnated-engine/data/kit_space/kit_space_chronicle.json`** — event_008 entry; `generation_parameters` includes `n_factions=3` and `pm1_algorithm=GMM_K3`; Wave A faction names in event notes
6. **`~/Games/reincarnated-engine/src/reincarnated/generation/phase5_pm1_multimodal_clustering.py`** (Phase 5a cohesion clustering source; verify cluster output structure)
7. **`~/Games/reincarnated-engine/src/reincarnated/export/kit_space_emitter.py`** (existing emit module; pattern reference)
8. **`~/Games/reincarnated-engine/data/kit_space/`** — current directory state; new artifact lands here as sibling to chronicle + kits/

---

## 2. Target seam + scope

**Owner seam:** export (star-lord; primary) with generation seam consultation (rocket; provides Phase 5a clustering data source)

**Target files:**
- NEW: `~/Games/reincarnated-engine/data/kit_space/faction_assignments.json` (the artifact this dispatch produces)
- AMEND: `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` (cross-seam MIGRATION per ADR-004)
- AMEND: `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (if generation-side touched per ADR-004)
- AMEND: `~/Games/reincarnated-engine/src/reincarnated/export/kit_space_emitter.py` (if extending emitter; ADDITIVE only per LOCK Q)
- OPTIONAL NEW: `~/Games/reincarnated-engine/scripts/export_faction_assignments_event008.py` (one-off export script if simplest path)

**Scope (ADDITIVE per LOCK Q):**

Export Phase 5a clustering data for event `kse_20260602_008` to a new artifact `data/kit_space/faction_assignments.json` with the schema specified in § 3 below. The artifact maps each of the 37 kit_ids to a faction_id + faction_name.

**Out of scope (CRITICAL):**
- Any semantic amendment to `phase5_pm1_multimodal_clustering.py` or `kit_space_emitter.py` public API (LOCK Q ADDITIVE-ONLY)
- Re-running Phase 5a clustering (use the existing event_008 cluster output already in chronicle / generation logs / temp state if accessible)
- Modifying chronicle event_008 entry (preserve as-is per Path α; the new artifact lives alongside, not in chronicle)
- Modifying per-kit JSONs (faction membership lives in the new sibling file; per-kit JSON unchanged)
- Re-firing QDX-5 (using existing emit data only)

---

## 3. Schema specification (per gandalf transmission)

```json
{
  "event_id": "kse_20260602_008",
  "schema_version": "1.0",
  "factions": [
    {
      "faction_id": "f001",
      "faction_name": "Iron Ground Crushers",
      "kit_ids": ["kit_<primary>_<seq6>", "..."]
    },
    {
      "faction_id": "f002",
      "faction_name": "Scattered Meridian Cannons",
      "kit_ids": ["...", "..."]
    },
    {
      "faction_id": "f003",
      "faction_name": "Earthen Siege Wardens",
      "kit_ids": ["...", "..."]
    }
  ]
}
```

**Schema requirements:**
- `event_id` matches an existing chronicle event
- `schema_version` for future evolution
- `factions` array; each entry has `faction_id` (e.g., `f001`/`f002`/`f003` for v1) + `faction_name` (matching Wave A LLM output) + `kit_ids` (array of kit_id strings)
- **All 37 kit_ids from event_008 MUST be accounted for** across the 3 factions (no kit unassigned)
- Sum of kit_ids across all factions equals total kits in event_008

---

## 4. Implementation guidance

**Data source decision (rocket consultation):**

The Phase 5a clustering output for event_008 was computed during QDX-5 fire (`scripts/qdx_qd_engine_re_fire_20260602.py`; commit `00cfbd0`). Possible sources for the cluster assignments:
- (a) Re-run Phase 5a clustering deterministically against the 37 emitted kits (using `phase5_pm1_multimodal_clustering` against the kit JSONs + same seed/params); produces deterministic re-derivation if pm1_algorithm + seed are stable
- (b) Inspect QDX-5 fire log at `/tmp/qdx5_full_fire.log` or AGENT_STATE checkpoint (if cluster assignments were logged)
- (c) Reconstruct from chronicle event_008's `generation_parameters` + Wave A faction-naming output if the per-kit mapping was preserved

Star-lord + rocket select the most reliable + simplest path. Option (a) deterministic re-derivation is most robust if the pm1_algorithm is stable. Document the chosen path in the completion record.

**Sample distribution (gandalf-informed approximation; not authoritative — verify via clustering):**
- "Iron Ground Crushers" — likely physical-heavy kits + earth/lightning grounded archetypes
- "Scattered Meridian Cannons" — likely caster/projectile kits (fire/wind/holy/shadow with ranged orientation)
- "Earthen Siege Wardens" — likely defensive/structural physical + earth + holy fortress archetypes

Star-lord+rocket should NOT guess the distribution — use the Phase 5a clustering output (deterministic or logged).

---

## 5. Acceptance criteria

### 5.1 Functional

1. **`data/kit_space/faction_assignments.json` exists** with schema per § 3
2. **`event_id == "kse_20260602_008"`**
3. **3 factions present** with names matching QDX-5 Wave A output (Iron Ground Crushers / Scattered Meridian Cannons / Earthen Siege Wardens)
4. **All 37 kit_ids accounted for** — sum of kit_ids across factions equals 37; no duplicates; no unassigned kits
5. **Each kit_id matches the format** `kit_<primary>_<seq6>` and exists in `data/kit_space/kits/`

### 5.2 LOCK Q ADDITIVE-ONLY

6. **No semantic amendment** to `phase5_pm1_multimodal_clustering.py` or `kit_space_emitter.py` public API
7. **No amendment to existing kit JSONs**
8. **No amendment to chronicle event_008 entry**

### 5.3 Cross-seam MIGRATION

9. **MIGRATION.md entry** at `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § cycle-18 Issue 5A — documents new artifact + schema + cross-seam consumer (drax loadout)
10. **If generation-side touched** (e.g., for clustering re-derivation), MIGRATION.md entry at `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` per ADR-004

### 5.4 Tests

11. **Smoke test** — load `faction_assignments.json` + verify schema + verify all 37 kit_ids present
12. **No regressions** — existing tests PASS (per LOCK Q ADDITIVE-ONLY)

---

## 6. Tag intent + commit + push

Tag: `star-lord/v1.6-cycle-18-issue-5a-faction-assignments-emit-1`

Auto-commit + auto-push per CLAUDE.md star-lord auto-commit pattern + cycle-push.

---

## 7. Critique-pair coverage

- **Gate-1 (jack-ryan DESIGN-MODE pre-fire):** unified Gate-1 finding covering cycle-18 dispatches including this one
- **Gate-2 (jack-ryan DEV-MODE post-output):** verifies schema + all 37 kits accounted + LOCK Q ADDITIVE-ONLY held

---

## 8. Quality criterion

**Game-quality goal this dispatch serves:** drax can render faction badges + filter UI properly (Issue 5B Phase 2 consumer) without needing to ask the engine for additional data shape — the artifact provides exactly what the consumer needs: kit_id → faction_name mapping that's deterministic, schema-versioned, and event-tied.

**Refutation conditions** (star-lord/rocket surface if any apply):
- Phase 5a clustering output cannot be reliably reconstructed for event_008 (signals data-provenance gap; surface to KR)
- Sum of kit_ids != 37 OR kits unassigned (clustering implementation gap)
- Schema cannot represent the actual cluster structure (e.g., clusters overlap; one kit in multiple factions) — surface for schema amendment if so
- LOCK Q ADDITIVE-ONLY would be violated to do the export cleanly — surface for escape clause invocation

---

## 9. Required completion record

```markdown
## Completion record

**Completed by:** star-lord (date)
**Tag:** `star-lord/v1.6-cycle-18-issue-5a-faction-assignments-emit-1`
**Engine commit:** `<sha>`
**New artifact:** `data/kit_space/faction_assignments.json`
**Schema version:** 1.0
**Event_id:** `kse_20260602_008`
**Faction count:** 3 (Iron Ground Crushers / Scattered Meridian Cannons / Earthen Siege Wardens)
**Kit assignments:** 37/37 accounted for
**Per-faction kit counts:** {<faction_id>: <count>, ...}
**Data source path used:** (a) deterministic re-derivation / (b) log inspection / (c) chronicle reconstruction
**MIGRATION.md updates:** `export/MIGRATION.md` § cycle-18 + (if applicable) `generation/MIGRATION.md`
**LOCK Q ADDITIVE-ONLY:** RESPECTED (no semantic API amendments)
**Tests:** smoke PASS + existing suite PASS (no regressions)
**Gate-2 readiness:** READY
**Notes for drax Phase 2 (Issue 5B):** <consumption notes; e.g., expected file path; recommended caching strategy>
**Notes for jack-ryan Gate-2:** <any verification specifics>
```

---

**End of Issue 5A dispatch.**

---

## Completion record

**Completed by:** star-lord (2026-06-02)
**Tag:** `star-lord/v1.6-cycle-18-issue-5a-faction-assignments-emit-1`
**Engine commit:** `50c5e71`
**New artifact:** `data/kit_space/faction_assignments.json`
**Schema version:** 1.0
**Event_id:** `kse_20260602_008`
**Faction count:** 3 (Iron Ground Crushers / Scattered Meridian Cannons / Earthen Siege Wardens)
**Kit assignments:** 37/37 accounted for
**Per-faction kit counts:** {f001: 16, f002: 18, f003: 3}
**Data source path used:** (b) log inspection — `/tmp/qdx5_full_fire.log` (QDX-5 Phase 5a cluster output). Option (a) deterministic re-run ATTEMPTED and FAILED: emitted kit JSONs store simplified BC axis representation vs. in-memory export_dicts used during original QDX-5 fire; all 16 physical kits are near-identical in the simplified feature space (B6 substrate-coverage gap), causing GMM to collapse to k=2 instead of k=3. Log reconstruction confirmed cluster structure: 16 physical → Cluster 1 → Iron Ground Crushers; 18 caster-non-earth (fire/water/wind/lightning/holy/shadow) → Cluster 2 → Scattered Meridian Cannons; 3 earth → Cluster 3 → Earthen Siege Wardens. Distribution {1:16, 2:18, 3:3} verified matches chronicle n_factions=3 and QDX-5 log cluster sizes exactly.
**MIGRATION.md updates:** `src/reincarnated/export/MIGRATION.md` § v1.74-cycle-18-issue-5a-faction-assignments-emit (new artifact + schema + cross-seam consumer drax loadout). Generation MIGRATION.md NOT touched (no generation-side code amended per LOCK Q ADDITIVE-ONLY).
**LOCK Q ADDITIVE-ONLY:** RESPECTED — no semantic API amendments to `phase5_pm1_multimodal_clustering.py` or `kit_space_emitter.py`. New artifact + one-off export script + smoke tests only.
**Tests:** 12/12 new smoke tests PASS (`tests/test_faction_assignments_event008.py`); 113/113 existing kit_space tests PASS (zero regressions).
**Gate-2 readiness:** READY

**Notes for drax Phase 2 (Issue 5B):**
- File path: `data/kit_space/faction_assignments.json` in reincarnated-engine; sync to `public/kit-space/faction_assignments.json` in loadout (same pattern as kit_space_chronicle.json + kits/ sync)
- Recommended pattern: load file at module init; `factions` array is small (3 entries); full in-memory use acceptable; no caching strategy needed
- Faction lookup: iterate `factions` array to build `kit_id → {faction_id, faction_name}` reverse map for badge rendering
- `event_id` field matches `kse_20260602_008` — can use as guard if multi-event support added later
- Faction membership is mutually exclusive (no kit in multiple factions); no deduplication required
- Kit order within each faction's `kit_ids` array follows kit_ids_generated order from chronicle (generation order, not alphabetical)

**Notes for jack-ryan Gate-2:**
- 12 acceptance criteria implemented as unit tests in `tests/test_faction_assignments_event008.py` (AC-1 through AC-12); all 12 PASS
- Key verification targets: AC-6 (37/37 total), AC-9 (no cross-faction duplicates), AC-10 (per-faction counts {f001:16, f002:18, f003:3}), AC-5 (faction names match QDX-5 Wave A)
- Data provenance carry-forward (surfaced for rocket via KR per dispatch-discipline): `pm1_result.kit_cluster_assignments` computed during Phase 5a but not persisted to chronicle. This caused Option (a) failure. Future events should persist cluster assignments to `generation_parameters.cluster_assignments` or a sibling `phase5a_cluster_map.json` artifact. This is a rocket seam concern; not star-lord to initiate.
- LOCK Q ADDITIVE-ONLY compliance: confirmed — zero amendments to `phase5_pm1_multimodal_clustering.py`, `kit_space_emitter.py`, per-kit JSONs, or chronicle entry
