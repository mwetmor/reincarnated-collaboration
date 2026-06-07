# Criterion 3.5 — PCG Framework Consumes Engine Geo-Spatial Output

**Verdict:** DEFERRED (not RED)
**Date:** 2026-06-06 Session 1
**Authority:** dispatch § 6 explicit rule — "if engine doesn't yet emit room-layout JSON at all, mark this criterion as DEFERRED (not RED) with cross-reference to engine workstream that produces it. Does NOT block port workstreams 1-3."

---

## Finding

The engine's cycle-14 wave-5 JSON output (available in meta-repo at `agentic_orchestration/cycle-14-wave-5-season-001/`) does NOT include room-layout or geo-spatial encounter data. Files present:

- `phase2_kit_candidates.json` — kit BC-axis metadata
- `phase3_gauntlet_results.json` — simulation gauntlet results
- `phase3_quality_vectors.json` — per-kit quality/substrate vectors
- `phase4_archive_insertion.json` — archive selection records
- `phase5_faction_clusters.json` — faction cluster membership
- `phase7_season_summary.json` — season-level summary
- `wave_b_identities.json` — kit identity + narrative

None of these files contain room-layout geometry, spawn-point arrays, or navigation hint data.

**Verified empirically:** searched meta-repo JSON files for `room`, `encounter_geometry`, `spawn_point`, `dimensions`. Not found.

---

## Why this is DEFERRED not RED

Per dispatch § 6: "PCG framework consumes engine geo-spatial output... if engine doesn't yet emit room-layout JSON, mark as DEFERRED."

The PCG framework in UE 5.7 is fully capable of consuming such data — the question is whether the engine emits it. This is an engine workstream gap, not a UE capability gap. The UE 5.7 PCG framework is a mature system (shipped with UE 5.2, substantially improved in 5.3-5.7) that natively accepts data-driven inputs for room generation.

PCG graph nodes that would consume room-layout JSON include:
- `PCGGetDataFromTag` node → reads spatial data from world actors
- `PCGCreateSpatialSamplerNode` → can seed from JSON-provided positions
- Blueprint-to-PCG data injection via `PCGData` context API

The integration is architecturally sound; the schema simply doesn't exist yet.

---

## Cross-seam request: engine room-layout JSON schema

For WS4 (continuity workstream) to eventually engage PCG, mantis needs star-lord to emit a room-layout JSON schema minimum:

```json
{
  "room_id": "enc_001",
  "room_type": "arena | corridor | boss_chamber | etc",
  "dimensions": {"x_m": 20.0, "y_m": 15.0, "ceiling_m": 5.0},
  "spawn_points": [
    {"pos": [5.0, 5.0, 0.0], "type": "player_entry"},
    {"pos": [10.0, 12.0, 0.0], "type": "enemy_wave_1"}
  ],
  "obstacle_positions": [
    {"pos": [8.0, 7.0, 0.0], "radius": 1.5, "type": "cover"}
  ],
  "navmesh_hint": "open_arena"
}
```

This is a suggested schema only — final schema owned by star-lord/gamora engine seam.

---

## Does NOT block

- WS1 (data layer) — entirely kit/substrate JSON focused
- WS2 (rendering layer) — cosmograph + character rendering
- WS3 (materialization payoff) — character confirmation cinematic

**Does block** WS4 (continuity — combat encounter generation) if engine never emits room-layout JSON. Not a current concern; WS4 is ~6-12 months out.

---

*Criterion 3.5 status: DEFERRED — engine geo-spatial JSON emission is the prerequisite. Route to star-lord + gamora for WS4 scheduling.*
