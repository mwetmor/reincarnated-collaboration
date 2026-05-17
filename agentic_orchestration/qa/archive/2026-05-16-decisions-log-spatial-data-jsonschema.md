# Decisions-log entry draft — Spatial-data JSON-schema locked (hybrid architecture; meters; per-encounter dimension library; load-bearing 6-step cascade)

**Author:** knight-rider
**Date drafted:** 2026-05-16 (Day 4)
**Source:** Gandalf's `canonical/story/spatial-data-jsonschema.md` (gandalf authored 2026-05-16; Tier-1 ARPG-precedent-grounded; "exact" schema per Matt's directive). Plus Matt's load-bearing follow-on directive (carried from movement-speed work): "the movement speed must be added into the core of the engine once we come to a decision so that the gauntlet simulation will be balanced." Spatial-data is the SCHEMA SUPPLY that movement-speed integration consumes; the 6-step cascade is load-bearing-for-balance-correctness.
**Process:** Knight-rider drafts → jack-ryan Gate 1 → Matt approval → commit to `reincarnated-engine/design/decisions/decisions-log.md`. Same pattern as the form-bias 5-entry batch (committed `5d51b5a`) + ailment-deferral (committed `680a3f1`) + cipher-width (committed `1dff66d`).

**Target location:** before the "Recently considered, not yet decided" section, after the most-recent committed entry. Commit alongside the movement-speed-baseline entry (also drafted this turn) as a coordinated pair; the two entries cross-reference each other.

**Companion-to:** the in-pending movement-speed-baseline decisions-log entry (drafted parallel this turn). The two entries together define the spatial+movement architectural commitment for VS2a + gauntlet-balance-correctness.

---

## Entry — Spatial-data JSON-schema locked: hybrid architecture (continuous-coord + shape-descriptor + tile-grid forward-compat); meters unit; per-encounter dimension library; movement_profile enum; 6-step implementation cascade is load-bearing for gauntlet-balance correctness

### 2026-05-16: Spatial-data JSON-schema locked — hybrid architecture (continuous-coordinate at combatant + shape-descriptor at floor + tile-grid forward-compat); unit meters; PIXELS_PER_METER=48 preserved; per-encounter dimension library (32.7×14m trash / 28×28m elite / 40×24m boss / 50×30m act-boss); movement_profile enum (6 initial values); 6-step implementation cascade (load-bearing per Matt directive)

**Decision:** The engine's JSON-packet schema is extended with spatial-data fields per gandalf's 2026-05-16 design-recommendation work (`canonical/story/spatial-data-jsonschema.md`; Tier-1 ARPG-precedent-grounded; concrete per Matt's "exact" directive).

#### Schema architecture (locked)

**Hybrid:** continuous-coordinate at combatant level + shape-descriptor at floor level + tile-grid forward-compatible (for future modder-tooling support per Grim Dawn licensing-pitch-relevant reference).

**Unit:** meters / m/s — preserves the movement-speed-baseline lock (`canonical/story/movement-speed-baseline.md` Matt-approved 2026-05-16). PIXELS_PER_METER=48 (demo-render constant; matches current arena scale).

**Origin convention:** per-encounter floor-center.

**JSON shape (per gandalf's locked schema fragment):**

```json
{
  "encounter_id": "...",
  "spatial": {
    "floor": {
      "shape": "rectangle|rounded_rect|...",
      "width_m": 32.7,
      "height_m": 14.0,
      "origin_convention": "floor_center",
      "rotation_deg": 0
    },
    "walls": [...],
    "obstacles": [],
    "entry": {"x": ..., "y": ...},
    "exit": {"x": ..., "y": ...},
    "encounter_meta": {
      "encounter_kind": "trash|elite|boss|act_boss|...",
      "intended_combat_range_band": "close|mid|far|mixed",
      "spatial_complexity_tier": "open_arena"
    }
  },
  "combatants": [
    {
      "id": "...",
      "kind": "player|monster",
      "spawn": {"x": ..., "y": ...},
      "movement_speed_base": 5.75,
      "movement_speed_effective_at_stage": {"early": 6.0, "mid": 7.5, "late": 8.0},
      "movement_profile": "walking|running|crawling|floating|flying|teleporting",
      "terrain_interaction": "..."
    }
  ]
}
```

**Initial per-encounter-kind dimension library:**
- 32.7 × 14.0 m (trash) — matches current demo arena
- 28 × 28 m (elite)
- 40 × 24 m (boss)
- 50 × 30 m (act-boss)

**Initial movement_profile enum (6 values):** walking / running / crawling / floating / flying / teleporting. Final list per form-bias Stage 4 work (per-embodiment narrative-skin); this entry locks the initial 6 as the schema starting point.

#### Tier-1 ARPG precedent (6 vendors inventoried)

Per gandalf's Section 1 inventory:
- **Path of Exile:** hybrid (tile-prefab generation + continuous-coordinate runtime); reference for hybrid architecture
- **Diablo II:** tile-grid + sub-tile-fractional combatants; modder-gold-standard (.ds1/.dt1); reference for modder-tooling compatibility
- **Diablo III:** tile-grid + chunked composition; less modder-accessible
- **Diablo IV:** continuous-coordinate + chunk-streamed open world — **REJECTED as wrong reference** (open-world scope is wrong for Reincarnated's encounter-scale)
- **Last Epoch:** tile-grid (D3-family)
- **Grim Dawn:** tile-grid + hybrid; **modder-friendly Diablo-derivative — the licensing-pitch-relevant reference** for tile-grid forward-compatibility

**Six genre-convergent patterns** extracted from the inventory drive the hybrid-architecture decision.

#### 6-step implementation cascade (LOAD-BEARING per Matt's follow-on directive)

| # | Step | Owner | Effort | VS2a-gating? | Next-balanced-gauntlet-gating? |
|---|---|---|---|---|---|
| 1 | Decisions-log entry (THIS entry) | knight-rider | — | YES | YES |
| 2 | Rocket schema-additive emission | rocket | ~4-6h | YES | NO |
| 3 | 🔴 **Gamora Stage A2 sim consumption (per Lock 3b)** | gamora | ~1.5-2 weeks | NO (post-VS2a tight follow) | **🔴 YES — load-bearing for balance** |
| 4 | Star-lord telemetry persistence | star-lord | ~2-3h | parallel-compatible | parallel-compatible |
| 5 | Drax PixiJS demo consumption | drax | ~1-2 days | YES | NO |
| 6 | Knight-rider post-integration calibration-epoch decisions-log entry | knight-rider | — | NO | YES (follows Step 3) |

**VS2a-ship gating:** Steps 1+2+5 (knight-rider entry + rocket schema + drax demo).
**Next-balanced-gauntlet gating:** Step 3 (gamora Stage A2 — load-bearing per Matt directive).

**🔴 Matt's load-bearing follow-on directive (verbatim, carried from movement-speed entry context):**

> *"The movement speed must be added into the core of the engine once we come to a decision so that the gauntlet simulation will be balanced."*

This makes the gamora Stage A2 integration (Step 3 above) **load-bearing for gauntlet-balance correctness — NOT optional Stage A2 polish.** Per engine-balance-stewardship entry's Lock 3b + this entry's commitment, Step 3 is non-deferrable for balanced-gauntlet claims.

#### B12 + B13 roadmap implications

Per gandalf's recommendation:

- **B12 (movement speed / boots / gear slot audit):** Stage-A2-co-shipping recommended (tighter integration; boots' +%MS modifier extends core movement_speed handling natively). Knight-rider drafts roadmap amendment if Matt approves co-shipping; the amendment would move B12 from "deferred from VS2a" to "Stage-A2-co-shipping with gamora Step 3."
- **B13 (active mobility + telegraphs + i-frames):** stays deferred per current roadmap. Feel-enrichment layer; NOT load-bearing for balance correctness.

#### Calibration-epoch implication (LOAD-BEARING, gandalf Section 7 Q7)

Current calibration epoch (committed `c000d7d`; mean |mod-1.0| ≈ 0.82) + cipher-width resolution entry (committed `1dff66d`) + gamora V2 smoke compression (0.3175) + in-flight regen recovery are ALL grounded in a movement-speed-blind, spatial-data-blind sim. **Step 3 integration WILL likely re-shift modifier-range metrics.** New calibration-epoch decisions-log entry lands post-integration (Step 6 above; knight-rider drafts).

**Until Step 3 lands, ALL current gauntlet-balance claims are explicitly provisional.** Surfaced explicitly to prevent downstream agents (gamora B6 main; future balance-loop work; future regens) from over-anchoring on current calibration-epoch numerics.

**Reasoning:** Per gandalf's `canonical/story/spatial-data-jsonschema.md` design-recommendation. The decision rests on four load-bearing analyses:

1. **Hybrid-architecture selection.** Pure tile-grid (D2/D3/Last Epoch) loses combatant-position precision needed for movement-speed-aware sim; pure continuous-coordinate (D4 open-world) is wrong scope for encounter-scale ARPG. Hybrid (combatant-continuous + floor-shape-descriptor + tile-grid forward-compat) takes the best of all three references.
2. **Meters unit selection.** Preserves the movement-speed-baseline lock (m/s); enables future Unity-client to consume directly; enables drax PixiJS demo to back-derive arena scale at PIXELS_PER_METER=48; allows gear-affix mechanics (boots' +%MS) to operate against real-world-grounded base.
3. **Per-encounter dimension library.** 4 encounter-kinds (trash / elite / boss / act-boss) at 4 fixed dimensions; matches current demo arena scale (32.7×14m trash); enables drax-side spatial layout per encounter-kind without per-playthrough generation overhead. Procedural-room generation (Sub-option B from prior architectural conversation) deferred to VS2b OR future-roadmap.
4. **movement_profile initial enum (6 values).** Walking / running / crawling / floating / flying / teleporting — covers genre-canonical movement-types + future per-embodiment narrative-skin variance (form-bias Stage 4). Final list lands with Stage 4; initial 6 lock the schema starting point.

**Alternatives considered:**

- **Pure tile-grid architecture** (D2/D3/Last Epoch reference): rejected. Loses combatant-position precision needed for movement-speed-aware sim. Tile-grid forward-compat preserved for future modder-tooling per Grim Dawn reference.
- **Pure continuous-coordinate architecture** (D4 reference): rejected. Open-world scope is wrong for Reincarnated's encounter-scale ARPG; spatial complexity is overkill for room-scale combat.
- **Tiles-per-second / abstract-units unit convention:** rejected. Meters / m/s preserves movement-speed-baseline lock + enables future Unity-client + back-derives demo arena scale.
- **Procedural-room generation per playthrough** (Sub-option B from prior architectural conversation): rejected for VS2a. High drax bandwidth cost; doesn't add load-bearing value vs the per-encounter dimension library. Re-openable for VS2b OR future-roadmap if cross-playthrough room variance becomes a design pillar.
- **Defer spatial-data schema until post-VS2a** (Stage A2 only): rejected per Matt's load-bearing directive. Without spatial-data in the JSON packet, drax must invent spatial framing demo-side AND gamora's Stage A2 sim extension lacks the spatial-data supply it needs. Load-bearing path is to lock schema NOW; ship rocket emission + drax rendering for VS2a; ship gamora Stage A2 consumption for balanced-gauntlet post-VS2a.
- **B12 stay deferred** (per current roadmap): rejected per gandalf's Stage-A2-co-shipping recommendation. Boots' +%MS modifier extends core movement_speed handling natively; co-shipping is tighter integration. (Knight-rider drafts roadmap amendment pending Matt approval.)
- **More-than-6 initial movement_profile values:** deferred. Initial 6 cover genre-canonical movement-types + future per-embodiment narrative-skin variance; final list with form-bias Stage 4.
- **Wall-geometry beyond perimeter-only:** deferred (gandalf Section 7 Q2). Future scope.
- **Obstacle scope/timing:** deferred (gandalf Section 7 Q3). Initial `obstacles: []` empty array; future expansion.

**Cross-seam cascades:**

- **Knight-rider:** Step 1 (THIS entry) gates Steps 2-5. Step 6 (post-integration calibration-epoch entry) is also knight-rider's future task.
- **Rocket:** Step 2 (schema-additive emission) — ~4-6h; schema fields per the locked JSON shape; MIGRATION.md per ADR-004. Dispatch authoring follows this entry's commit.
- **Gamora:** Step 3 (Stage A2 sim consumption) — LOAD-BEARING per Matt directive; ~1.5-2 weeks; per Lock 3b of engine-balance-stewardship entry. Dispatch authoring post-this-entry-commit; intersects with the gamora B6 main work (form-bias Stage 1+2 work).
- **Star-lord:** Step 4 (telemetry persistence) — parallel-compatible with Step 2; ~2-3h.
- **Drax:** Step 5 (PixiJS demo consumption) — VS2a-ship-gating; ~1-2 days; per gandalf "single thing to watch" arena-scale back-derivation; HELD pending Steps 1+2 landing.
- **Legolas:** Mode A precursor research on Tier-1 ARPG spatial-data-format technical specifics — OPTIONAL per gandalf Section 9. Activation only if Reincarnated pursues modder-tooling support OR Matt wants implementation-detail validation pre-gamora-Stage-A2.
- **Elrond:** out of seam for this entry; spatial-data schema doesn't intersect catalogue-track work.
- **Gandalf:** future amendment if dimension-library refines post-playtest (gandalf Section 7 Q1); future amendment if movement_profile final list shifts at form-bias Stage 4 (Q4); future spatial-data-related strategy-doc amendments per the 8 open questions parked.
- **Jack-ryan:** Gate 1 reviewer on this entry; future Gate 1 reviewer of the post-Step-3 calibration-epoch entry.

**Status:** Active. Locks the spatial-data JSON-schema architecture + the 6-step implementation cascade. Step 1 complete on this entry's commit; Steps 2+5 unblock immediately for dispatch authoring; Step 3 dispatch authoring follows + is the load-bearing balance-correctness step.

**8 open questions parked for Matt-decision** (per gandalf Section 7):

1. Dimension-library refinement (playtest-dependent; future)
2. Wall-geometry beyond perimeter-only (future scope)
3. Obstacle scope/timing (future)
4. movement_profile final list (form-bias Stage 4)
5. Spatial-block DB-vs-file persistence (star-lord call)
6. Tile-grid forward-compat for modder tooling (Reincarnated-roadmap-dependent)
7. **Calibration-epoch implication (load-bearing; already baked into Step 3 + Step 6 of cascade)**
8. VS2b interaction (orthogonal — no blocking conflict)

These are gandalf-flags-for-Matt-decision items; this entry locks the schema architecture + cascade without pre-committing to the 8 open questions.

**Related:**

- **Source-of-truth doc:** `canonical/story/spatial-data-jsonschema.md` (gandalf authored; locked schema fragment; Tier-1 ARPG precedent inventory; 6-step cascade; 8 open questions parked)
- **Commission dispatch:** `agentic_orchestration/dispatches/2026-05-16-gandalf-spatial-data-jsonschema-recommendation.md` (knight-rider authored; gandalf executed; completion record filled)
- **Companion entry:** in-pending movement-speed-baseline entry at `agentic_orchestration/qa/pending/2026-05-16-decisions-log-movement-speed-baseline.md` — both entries reference each other; commit together
- **Engine-balance-stewardship entry** (committed `5d51b5a` family) — Lock 3 movement-modeling abstraction limitation; Lock 3b Stage A2 sim extension scheduling (this entry's Step 3)
- **2026-05-16 calibration-epoch entry** (committed `c000d7d`) — baseline; this entry's load-bearing-Step-3 implication: future calibration-epoch entry post-integration (Step 6 of cascade)
- **2026-05-16 form-bias 5-entry batch** (committed `5d51b5a`) — Entry 1 strategic-axis lock (sub-lock (a) ARPG-canon-primary at substrate-mechanical layer; spatial-data lives at this layer)
- **2026-05-16 cipher-width resolution entry** (committed `1dff66d`) — Outcome 2 + Foundation L2; this entry's per-embodiment movement_profile aligns with Stage 4 form-bias narrative-skin work
- **Roadmap:** `canonical/16-project-roadmap.md` §VS2a + §VS2b + §B12 (Stage-A2-co-shipping recommended) + §B13 (stays deferred)

---

## Knight-rider note (NOT for decisions-log; for jack-ryan Gate 1)

Cross-cutting questions for jack-ryan to test:

1. **Single-entry justification:** could split into "schema-architecture-locked" entry + "implementation-cascade" entry. Reasoning for single: gandalf's design-recommendation produced both as a coordinated bundle; splitting loses the architecture-cascade coupling. Push back if you'd prefer split.
2. **Load-bearing-Step-3 framing:** does the entry honor Matt's directive without over-claiming? Step 3 is explicitly load-bearing for balanced-gauntlet claims; NOT load-bearing for VS2a-ship (Steps 1+2+5 cover VS2a). Verify the bifurcation is clean.
3. **Discipline #11 attribution:** the entry cites gandalf's locked schema fragment + the 6 Tier-1 ARPG references verbatim. Verify all 4 dimension-library values + 6 movement_profile enum values + 4-vendor inventory match gandalf's source-of-truth.
4. **Discipline #12 (semantic-shifting):** spatial-data becomes a meaningful semantic axis after this entry lands. Verify the entry frames the calibration-epoch implication as semantic shift + flags downstream-agents not to over-anchor on current numerics.
5. **8 open questions parking:** does the entry park them cleanly without pre-committing? My read: 8 are explicit-parking; this entry resolves only the 4 load-bearing decisions (architecture / unit / dimension library / cascade) + leaves the 8 for future Matt-decision. Confirm.
6. **Companion-entry cross-references:** entry references movement-speed-baseline entry as companion. Verify bidirectional (movement-speed-baseline entry should reference back).
7. **B12 roadmap-amendment recommendation:** the entry says "Knight-rider drafts roadmap amendment if Matt approves co-shipping" — this routes the decision to Matt without pre-committing. Verify routing is clean.
8. **Alternatives section completeness:** eight alternatives covered. Any missing?

If all eight pass with no BLOCK, this entry is ready for Matt approval and commit. Recommended commit-sequence: commit alongside the movement-speed-baseline entry as a coordinated pair (cross-reference integrity).
