# Decisions-log entry draft — Movement-speed baseline locked (D3/D4/Last-Epoch design family; gauntlet-balance-load-bearing per Matt directive)

**Author:** knight-rider
**Date drafted:** 2026-05-16 (Day 4)
**Source:** Gandalf's `canonical/story/movement-speed-baseline.md` (Matt-approved 2026-05-16) + gandalf's commission `agentic_orchestration/gandalf/requests/2026-05-16-movement-speed-baseline-vs2a-gating.md` (handoff items #1-5). Plus Matt's load-bearing follow-on directive: "the movement speed must be added into the core of the engine once we come to a decision so that the gauntlet simulation will be balanced." Per gandalf handoff #4: decisions-log entry lands BEFORE drax begins implementation.
**Process:** Knight-rider drafts → jack-ryan Gate 1 → Matt approval → commit to `reincarnated-engine/design/decisions/decisions-log.md`. Same pattern as the form-bias 5-entry batch (committed `5d51b5a`) + ailment-deferral (committed `680a3f1`) + cipher-width (committed `1dff66d`).

**Target location:** before the "Recently considered, not yet decided" section, after the most-recent committed entry (cipher-width `1dff66d` OR D1 scope entry if it commits first).

**Companion-to:** the in-pending spatial-data-schema decisions-log entry (drafted parallel this turn) — both entries are part of the spatial+movement architectural commitment for VS2a + gauntlet-balance-correctness.

---

## Entry — Movement-speed baseline locked (player + monster archetypes at meters/s; PIXELS_PER_METER=48; AI_SPEED_MULTIPLIER=0.767 for VS2a; D3/D4/Last-Epoch design family); gauntlet-balance load-bearing per Matt directive

### 2026-05-16: Movement-speed baseline locked — player base 5.75 m/s + mid-VS2a 7.5 m/s + late 8.0 m/s; monster trash 5.75 m/s + fast archetypes 6.6-7.5 m/s; PIXELS_PER_METER=48; AI_SPEED_MULTIPLIER=0.767 (VS2a); range-profile MS variance dropped; design family D3/D4/Last-Epoch; movement-speed integration into engine core is load-bearing for gauntlet-balance correctness

**Decision:** The movement-speed baseline for player + monster combatants is locked per gandalf's 2026-05-16 design-recommendation work (`canonical/story/movement-speed-baseline.md`; Matt-approved 2026-05-16). The locked values:

| Parameter | Value | Demo px/s at 48 px/m |
|---|---|---|
| Player base MS | 5.75 m/s | 276 px/s |
| Early game | 6.0 m/s | 288 px/s |
| **Mid game (VS2a)** | **7.5 m/s** | **360 px/s** |
| Late game | 8.0 m/s | 384 px/s |
| Monster trash | 5.75 m/s | 276 px/s |
| Monster fast archetypes | 6.6–7.5 m/s | 317–360 px/s |
| PIXELS_PER_METER | 48 (constant) | — |
| AI_SPEED_MULTIPLIER (VS2a) | 0.767 | yields trash 276 px/s vs player mid 360 px/s; 84 px/s chase margin |
| Range-profile MS variance | DROPPED | All classes uniform |

**Design-family anchor:** **D3 / D4 / Last Epoch.** Conservative late-game delta (+39% over trash baseline); positional gameplay preserved through progression; fast monster archetypes practically threatening at endgame. **Deliberately NOT the PoE-1 zoom-zoom track.**

**🔴 Matt's load-bearing follow-on directive (2026-05-16 Day 4):**

> *"The movement speed must be added into the core of the engine once we come to a decision so that the gauntlet simulation will be balanced."*

This makes the gamora Stage A2 movement-speed-aware sim extension (per engine-balance-stewardship Lock 3b) **load-bearing for gauntlet-balance correctness — NOT optional Stage A2 polish.** Any new balance work between this entry's commit and the Stage A2 integration is provisional; new calibration-epoch entry will follow post-Stage-A2.

**Reasoning:** Per gandalf's `canonical/story/movement-speed-baseline.md` design-instinct + the gandalf commission's analytical work (`gandalf/requests/2026-05-16-movement-speed-baseline-vs2a-gating.md`). The decision rests on three load-bearing analyses:

1. **Genre-canon anchor selection.** Gandalf's analysis surfaced three design-family options: (i) D3/D4/Last Epoch (conservative late-game delta; positional gameplay preserved); (ii) PoE-1 zoom-zoom (aggressive late-game delta; positional gameplay erodes); (iii) D2-classic (very conservative baseline; rigid walk-vs-run distinction). Option (i) selected for Reincarnated. Rationale: aligns with solo-focused gameplay (per `project_design_intent.md`); preserves the "fast monster archetypes practically threatening at endgame" gameplay surface; matches Western ARPG-audience legibility expectations.
2. **Unit-convention selection.** Meters / m/s selected over abstract-units / tiles-per-second. Rationale: physics-grounded; enables drax PixiJS demo to back-derive arena scale (48 px/m); enables future Unity-client work to consume meters directly; allows gear-affix mechanics (boots' +%MS) to operate against a real-world-grounded base value.
3. **PIXELS_PER_METER=48 anchor.** Selected as the demo-render unit-conversion constant. Rationale: aligns with current demo arena dimensions (32.7×14m at 48 px/m matches the existing arena.ts spatial framing per gandalf's "single thing to watch" arena-scale-back-derivation note); enables drax to verify the arena hasn't drifted from the locked scale.

**The range-profile MS variance DROPPED decision:** prior simulator-internal positional state included range_profile (close / mid-close / mid-far / far) which implicitly varied movement_speed per class via range-profile assignment. Per gandalf's analysis, this variance was a movement-speed-blind-sim artifact — under the locked baseline, ALL CLASSES are uniform at 5.75 m/s base; per-archetype variance lives at monster-fast-archetype level (6.6-7.5 m/s) only. Player-class movement_speed scales by stage (5.75 → 6.0 → 7.5 → 8.0 m/s); per-class variance is zero at the base.

**Implementation cascade (LOAD-BEARING per Matt's follow-on directive):**

Per gandalf's commission handoff items #1-5:

| # | Step | Owner | Effort | VS2a-gating? |
|---|---|---|---|---|
| 1 | **movement_speed schema field** (m/s, 2-decimal; class default 5.75; monster trash default 5.75; monster fast 6.6-7.5 range) | rocket | ~1-2h | YES — gates demo + sim consumption |
| 2 | **Drax PixiJS implementation** (replace world/movement.ts per locked values; verify arena scale; re-tune AI multiplier to 0.767; re-run playtest calibration equivalent to phase 6.1/6.2) | drax | ~1-2 days | YES — VS2a-ship-gating |
| 3 | **Gamora Stage A2 sim consumption** (Gate 3b: 4-band distance state (melee / near / mid / far); movement-speed-aware kiting modeling; per-class movement_speed consumption in balance_loop) | gamora | ~1.5-2 weeks | **POST-VS2a tight follow; gauntlet-balance load-bearing per Matt directive** |
| 4 | **Decisions-log entry** (THIS entry) | knight-rider | — | Gates step 2 per gandalf #4 |
| 5 | **Star-lord per-fight observed-MS telemetry** (v2.2 schema column `observed_movement_speed`; cross-validates rocket schema + future gamora Stage A2 consumption) | star-lord | ~1h | NOT VS2a-gating; shipped 2026-05-16 (commit `db4aa09`) ✓ |

**Step status as of this entry's drafting:**
- Step 1: in flight (rocket movement_speed schema dispatch fired 2026-05-16; working tree shows modifications)
- Step 2: HELD pending this entry committing
- Step 3: NOT yet authored (gamora dispatch authoring post-spatial-data-schema-entry commit; per spatial-data-schema entry's 6-step cascade Step 3 is the load-bearing balance integration)
- Step 4: THIS entry (in qa/pending)
- Step 5: ✅ COMPLETE (star-lord/v1.3-telemetry-schema-v2.2-observed-ms @ `db4aa09`)

**Single thing to watch (per gandalf commission):** the arena-scale back-derivation in drax's Step 2 implementation pass. When drax verifies current arena dimensions in arena.ts against 48 px/m:
- If current arena is already designed for ~48 px/m: player perceives near-2× speed-up (current 180 px/s medium represents ~3.75 m/s; new mid is 360 px/s = 7.5 m/s). Will feel substantially faster. May want a brief tuning pass on arena dimensions to prevent the new speed from making the arena feel cramped.
- If current arena is implicitly ~24 px/m: the rebase is a no-op in feel — same perceived speed, just a unit clarification.

Drax should report which case applies as part of the implementation pass. Case (a) may surface a follow-on arena-tuning decision (not a blocker for VS2a ship).

**Calibration-epoch implication:** the current calibration epoch (committed `c000d7d`; mean |mod-1.0| ≈ 0.82) + the cipher-width resolution entry (committed `1dff66d`) + the gamora V2 smoke compression (0.3175) + the in-flight regen recovery are ALL grounded in a movement-speed-blind sim. Per Matt's load-bearing directive + per the engine-balance-stewardship entry's Lock 3b, the Stage A2 integration (Step 3 above) will RE-SHIFT modifier-range metrics. A new calibration-epoch decisions-log entry lands post-Stage-A2 integration (knight-rider drafts; same flow). **Until Stage A2 lands, all gauntlet-balance claims are provisional.**

**Alternatives considered:**

- **PoE-1 zoom-zoom design family** (Option ii from gandalf's analysis): rejected. Aggressive late-game delta erodes positional gameplay; monsters become non-threatening; player perception shifts to "movement-puzzle" rather than "tactical-combat." Wrong fit for Reincarnated's solo-focused gameplay.
- **D2-classic design family** (Option iii): rejected. Very conservative baseline + rigid walk-vs-run distinction. Misses the genre-canonical "fast monster archetypes practically threatening at endgame" surface; less rewarding for endgame-build investment.
- **Abstract-units or tiles-per-second unit convention** (rejected per gandalf's unit-selection analysis): meters / m/s is physics-grounded + enables future Unity-client + back-derives demo arena scale; abstract-units lose those benefits without compensating gains.
- **Defer movement-speed integration to post-VS2a entirely** (Stage A2 only): rejected per Matt's load-bearing directive. Without movement_speed in the core sim, the gauntlet-balance work IS gauntlet-balance-blind to a load-bearing axis; future balance claims would be permanently provisional. Stage A2 timing-as-tight-follow-VS2a is the right cadence; deferring further compromises balance correctness.
- **Per-class movement_speed variance at the base** (preserve range-profile MS variance): rejected per gandalf's analysis. Movement-speed-blind sim artifact; ALL CLASSES uniform at 5.75 m/s base is the cleaner architectural commitment; monster-side variance carries the per-archetype-threat differentiation.
- **PIXELS_PER_METER alternative values** (24, 32, 64): rejected per gandalf's anchor selection. 48 aligns with current demo arena dimensions; alternatives would force arena-scale rework.

**Cross-seam cascades:**

- **Rocket:** Step 1 (movement_speed schema field) — in flight per `dispatches/2026-05-16-rocket-movement-speed-schema-field.md`; schema-additive; MIGRATION.md per ADR-004
- **Star-lord:** Step 5 telemetry shipped ✓ (`star-lord/v1.3-telemetry-schema-v2.2-observed-ms` @ `db4aa09`); v2.2 DB migration to live data/telemetry.db requires separate Matt ADR-006 authorization
- **Drax:** Step 2 (PixiJS implementation) HELD pending this entry committing per gandalf handoff #4. Dispatch authoring follows this entry's commit; arena-scale back-derivation report is a known "single thing to watch"
- **Gamora:** Step 3 (Stage A2 sim consumption) — LOAD-BEARING per Matt directive; dispatch authoring post-spatial-data-schema entry commit (the two entries' cascades converge at Step 3 which is the spatial-data + movement-speed integrated sim extension)
- **Knight-rider:** post-Stage-A2 integration, draft new calibration-epoch decisions-log entry (separate; future)
- **Jack-ryan:** Gate 1 reviewer on this entry; future Gate 1 reviewer of the post-Stage-A2 calibration-epoch entry

**Status:** Active.

**Related:**

- **Source-of-truth doc:** `canonical/story/movement-speed-baseline.md` (gandalf authored; Matt-approved 2026-05-16)
- **Commission:** `agentic_orchestration/gandalf/requests/2026-05-16-movement-speed-baseline-vs2a-gating.md` (gandalf-authored; full design-analysis + 5 handoff items + decisions-log entry template)
- **Step 1 dispatch:** `agentic_orchestration/dispatches/2026-05-16-rocket-movement-speed-schema-field.md`
- **Step 5 dispatch (complete):** `agentic_orchestration/dispatches/2026-05-16-star-lord-telemetry-observed-ms-emission.md`
- **Related: spatial-data-schema entry (companion; drafted parallel this turn)** at `agentic_orchestration/qa/pending/2026-05-16-decisions-log-spatial-data-jsonschema.md` — Step 3 of the spatial-data cascade IS the gauntlet-balance-integration step that also satisfies this entry's Step 3
- **Engine-balance-stewardship entry** (committed `5d51b5a` family) — Lock 3 movement-modeling abstraction limitation; Lock 3b Stage A2 sim extension scheduling
- **2026-05-16 calibration-epoch entry** (committed `c000d7d`) — baseline + projected B6+V2 target (~0.50); this entry's load-bearing-Stage-A2 implication: future calibration-epoch entry post-integration
- **Roadmap (gandalf-updated 2026-05-16):** `canonical/16-project-roadmap.md` §VS2a (locked values + B12 split entry + seam allocations + ship trigger amended); §Stage-A2 summary updated
- **Engine-balance-stewardship.md § Gate 3:** supersession note added per gandalf 2026-05-16
- **Memory note:** `project_design_intent.md` (solo-focused gameplay framing this design-family selection)

---

## Knight-rider note (NOT for decisions-log; for jack-ryan Gate 1)

Cross-cutting questions for jack-ryan to test:

1. **Load-bearing-Stage-A2 framing:** Matt's "movement speed must be added into the core of the engine" directive makes Stage A2 load-bearing-not-deferrable. The entry frames Step 3 as POST-VS2a tight follow. Verify this framing honors Matt's directive: NOT "ship VS2a then defer indefinitely" — rather "Stage A2 is the next gauntlet-balance-critical-path item after VS2a ships."
2. **Discipline #11 attribution:** the entry cites gandalf's locked values + commission verbatim. Verify all 8 parameter values match gandalf's `canonical/story/movement-speed-baseline.md` source-of-truth.
3. **Discipline #12 (semantic-shifting):** movement_speed becomes a meaningful semantic axis after this entry lands. Verify the entry frames the calibration-epoch implication as semantic shift (gauntlet-balance claims pre-Stage-A2 are semantically different from post-Stage-A2).
4. **Alternatives completeness:** six alternatives. Any missing?
5. **Single-entry vs split-entry:** I drafted as one entry covering all 5 handoff items + cascade. Could split into "movement-speed-values locked" entry + "implementation-cascade-load-bearing" entry. Reasoning for single: gandalf's commission produced both as a coordinated bundle; splitting loses coupling. Push back if you'd prefer split.
6. **Companion-to spatial-data-schema entry:** the entry references the spatial-data-schema entry as companion. Verify cross-reference is bidirectional (spatial-data-schema entry should reference back).
7. **Arena-scale-back-derivation note:** "single thing to watch" framing. Verify it's framed as drax-implementation-observation rather than blocker.

If all seven pass with no BLOCK, this entry is ready for Matt approval and commit. Recommended commit-sequence: D1 scope first (already in jack-ryan Gate 1 this turn), THEN this entry + spatial-data-schema entry as a coordinated pair (both reference each other; commit together to preserve cross-reference integrity).
