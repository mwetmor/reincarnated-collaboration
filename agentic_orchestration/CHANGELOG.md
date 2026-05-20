# CHANGELOG — Reincarnated synthetic engineering team

This log records **team-level events** — agent additions, ADR additions/amendments, process changes, scope re-allocations. It does NOT log routine developer commits (those live in their respective git repos).

---

## 2026-05-21 — QD-rebuild P0 W0.10 Phase 2 IN-FLIGHT: boss AI leash-reset fix implementation + W0.10.5 re-sweep verification

**Event:** W0.10 Phase 2 implementation dispatched to gamora (agentId `a49ef8e61d492ab72`). FINAL substantial implementation of P0 per gandalf Option A disposition.

**Phase 1 + Phase 1.5 LOCKED + both critique-pair reviews APPROVED prior to Phase 2 fire:**
- Math note at `reincarnated-engine/src/reincarnated/simulation/math/w0-10-boss-ai-leash-reset-fix.md` (1027 lines)
- jack-ryan Gate-1 — APPROVE-WITH-AMEND (AMEND-1: §3.2 entity ID lookup `entity_id == f"mob_{focus_index}"` was incorrect; folded via Phase 1.5 reference-storage pattern `_boss_focus_entity` as primary)
- gandalf Gate-1 — ARCHITECTURALLY ALIGNED ("textbook continuation of W0.9 architectural commitments"); 3 sharpening amendments folded (A1, A2, A3)

**Phase 2 implementation scope:**
1. Player AI boss-focus targeting in `spatial_engine.py` (with `_boss_focus_entity` reference-storage)
2. Add leash semantics in `arena.py` + NEW `SpawnSpec.suppress_leash_hp_reset` flag
3. D2/PoE preserved-HP semantics on leash for boss/mini-boss scenarios; D3 HP-reset retained for swarm/magic/elite (degenerate-edge no-op)
4. New tests at `tests/test_w010_boss_ai_focus.py`
5. MIGRATION.md v1.29 with explicit D3 → D2/PoE genre repositioning cite
6. Caller-side wiring fold-in (jack-ryan W0.9 cumulative Amendment 1)
7. W0.10.5 re-sweep verification + W0.10.5 vs W0.9.6 archaeology artifact

**Predicted re-sweep outcomes (from locked math note §5):**
- physical_grappler boss WR: 0.80-0.90
- shadow/wind boss WR: 0.55-0.75
- water/earth boss WR: 0.30-0.50
- fire_mage residual: 0.05-0.15 (multi-dim convergence territory; expected)
- Discipline #17 anomaly count target: 2-8 (vs current 50/50)

**On Phase 2 return:** knight-rider fires W0.10 cumulative Gate-2 critique-pair (jack-ryan + gandalf parallel) → on Gate-2 APPROVAL → final tag `qd-rebuild/v0.10-boss-ai-leash-reset-fixed` fires → W0.7 ablation experiments dispatch fires → on W0.7 close → P0 milestone tag `v0.0-constraint-removal-shipped`.

State-of-hive § 1 W0.10 row added; P0 roster expanded 9 → 10.

---

## 2026-05-21 — QD-rebuild P0 W0.9 FULLY CLOSED: cumulative Gate-2 APPROVED; joint-resolution triad structurally sufficient (§ 2.3.1 caveat folded)

**Event:** W0.9 cumulative Gate-2 critique-pair returned. Both reviews APPROVED w/ amendments. Final tag `qd-rebuild/v0.9-gauntlet-migration-complete` FIRED.

**gandalf cumulative Gate-2 — ARCHITECTURALLY ALIGNED:**
*"Joint-resolution triad structurally sufficient — W0.9 PackProxy retirement + spatial gauntlet promotion completes the W0.9 leg. The triad's structural sufficiency claim survives."*

Triad close-out summary:
- ✅ W0.2 source diversity — substrate-AGNOSTIC composition LIVE
- ✅ W0.1 calibration fairness — #13a-partition canonical exemplar LIVE
- ✅ W0.9 arena fidelity — PackProxy retired; spatial gauntlet promoted; 6× faster than baseline

**§ 2.3.1 BEHAVIORAL-CORRECTNESS CAVEAT AMENDMENT** (folded into `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` by gandalf):

The triad addresses *structural* sufficiency. Behavioral correctness of arena occupants (player AI, monster AI, leash semantics, targeting logic) is a separate, lower-tier concern that the triad implicitly assumed. **Triad presumes arena-occupant behavioral correctness; defects in occupant AI are out-of-band and resolved per-bug.**

The W0.10 boss AI fix workstream is the per-bug resolution for the leash-reset behavior surfaced by Phase 2.5. Future occupant-behavior bugs follow the same per-bug pattern (Discipline #11.1 cold-start empirical surfaces them; the triad does not pre-suppose them).

**The triad's structural sufficiency claim survives. The behavioral-correctness caveat is an addition, not a refutation.**

**jack-ryan cumulative Gate-2 DEV-MODE — APPROVE-WITH-AMEND** (1 amendment, non-blocking):

All 5 W0.9 sub-phase commits verified clean:
- Phase 2.1 PackProxy retirement + R2 promotion ✅
- Phase 2.2 ConvergenceUsageMode / ValidationUsageMode (P7 W7.2 barred from `run_spatial_fight`) ✅
- Phase 2.3 4 perf mitigations + A3 stability ✅
- Phase 2.4 SqliteSpatialTelemetryWriter + 8-axis BC fight_events ✅
- Phase 2.5 calibration sweep + critical finding ✅

R11(b) round-trip smoke confirms 975,450 fight_events rows landed cleanly. Discipline #12 semantic shifts documented across MIGRATION.md v1.24-v1.28.

**Amendment 1 (caller-side wiring fold-in) — folded into W0.10 Phase 2 scope:** the `_run_spatial_slot` caller-side wiring of `spatial_telemetry_writer` parameter requires production-caller readiness verification. Folded into W0.10 Phase 2 to ride along with that workstream's caller-side wiring touches.

State-of-hive § 1 W0.9 row updated to FULLY CLOSED.

---

## 2026-05-21 — QD-rebuild P0 W0.10 Phase 1 + 1.5 COMPLETE: boss AI leash-reset fix math-before-code locked

**Event:** W0.10 math-before-code Phase 1 + amendment fold-in Phase 1.5 returned. Tag `qd-rebuild/v0.10-math-note-phase-1-complete` FIRED. Math note at `reincarnated-engine/src/reincarnated/simulation/math/w0-10-boss-ai-leash-reset-fix.md` (1027 lines).

**Scope per gandalf Option A disposition:** structural arena-AI bug surfaced by W0.9 Phase 2.5 calibration sweep. Player AI targets nearest mob → elite add chases beyond `leash_distance_m=12.0` → leashes back with `entity.hp = entity.max_hp` full reset cycle → boss never engaged in 240s.

**Math validates boss IS killable if reached:** at modifier=0.742, `spatial_DM=2.97`, `base_damage=1485`, `boss_HP=53,216`, DPS=990 HP/s, TTK=~54s well within 240s timeout. NOT a scaling issue — structural arena-AI bug.

**Fix design (per locked math note):**
1. Player AI boss-focus when `win_condition == "boss_killed"` (reference-storage pattern `_boss_focus_entity`; per Phase 1.5 fold-in)
2. Leash semantics rework: D2/PoE preserved-HP on leash for boss/mini-boss scenarios (NO HP reset cycle); D3 HP-reset retained for swarm/magic/elite (where it's degenerate-edge no-op)
3. NEW `SpawnSpec.suppress_leash_hp_reset` flag (per-encounter configurable; gandalf A3 architectural amendment)
4. MIGRATION.md v1.29 documents Discipline #12 semantic shift + D3→D2/PoE genre repositioning cite

**Phase 1.5 amendment fold-in:**
- jack-ryan AMEND-1: §3.2 entity ID lookup `entity_id == f"mob_{focus_index}"` was incorrect — folded via reference-storage `_boss_focus_entity` adopted as primary mechanism
- gandalf A1: smoke-test prediction band sharpening (per-archetype WR predictions explicit)
- gandalf A2: Discipline #17 anomaly count target (2-8 vs current 50/50)
- gandalf A3: leash semantics as ARPG-canon repositioning (D2/PoE behavior; not just bug fix)

**Both Gate-1 reviews APPROVED:**
- jack-ryan: APPROVE-WITH-AMEND (Amendment 1 folded into Phase 1.5)
- gandalf: ARCHITECTURALLY ALIGNED ("textbook continuation of W0.9 architectural commitments")

**Phase 2 fires next** (gamora launched agentId `a49ef8e61d492ab72`). Final substantial implementation of P0.

---

## 2026-05-21 — QD-rebuild P0 W0.9 Phase 2.5 COMPLETE: CRITICAL FINDING — boss AI leash-reset bug; W0.9 ready for cumulative Gate-2

**Event:** W0.9 Phase 2.5 (W0.9.6 calibration sweep co-run with W0.1) returned. Tag `qd-rebuild/v0.9-phase-2-5-calibration-sweep-complete` fired (engine commit `0837c7b`). **All 5 W0.9 sub-phases now COMPLETE.**

**Calibration sweep telemetry verified:** 10 kits × 5 tiers × 30 fights = 1,500 `spatial_fight_results` rows + **975,450 fight_events rows** emitted cleanly with zero failures. SqliteSpatialTelemetryWriter operational in production-mirror environment.

**PERFORMANCE PASS — 6× FASTER THAN PACKPROXY:** measured 0.17× ratio vs PackProxy baseline (math note §3.4 target ≤5×; prediction <2×; actual achievement: 6× IMPROVEMENT). Per-kit avg 4.9s vs PackProxy baseline 28.3s per class.

**🚨 CRITICAL FINDING — DISCIPLINE #17 STRUCTURAL ANOMALY (50/50 tier-class combos flagged):**

**Root cause empirically diagnosed per Discipline #11 inspection (NOT a scaling/calibration issue):**

**Boss AI leash-reset bug** prevents player engagement of boss:
1. Player AI targets nearest alive mob — elite add at ~12m, NOT boss at ~17m
2. Player damages add → add chases player beyond `leash_distance_m=12.0` from spawn → add leashes back → `entity.hp = entity.max_hp` (FULL HP RESET)
3. Repeat for 240s timeout. Boss (stationary_caster) NEVER ENGAGED.
4. Empirical evidence: physical_grappler dealt 215,238 damage total (145 casts × 1,485 base damage = 215k); elite add HP dropped only 4,453 (consistent with ~3 hits landing between leash cycles).

**Math shows boss IS killable if reached:** at modifier=0.742, `spatial_DM = 0.742 × 4.0 = 2.97`; `base_damage = 1.0 × 500 × 2.97 = 1485`; `boss_HP after 0.40× = 53,216`; DPS at 1.5s CD = 990 HP/s; **TTK = ~54s well within 240s timeout**. Boss tier is reachable; the structural block is that player AI never focuses the boss.

**This is the recompose-hive "fix the arena, not the synergy" principle catching the NEXT arena bug.** PackProxy ×8 was the wrong arena (Phase 2.1 retired it); the new spatial arena reveals its own player-AI bug (boss never engaged due to add-leash-reset cycle). The principle catches both issues exactly as designed.

**Required remediation (Discipline #1 math-note required before code):**
- Player AI boss-focus mode when `win_condition == "boss_killed"`
- Add spawn position calibration (move adds near boss, not at arena edge)
- Scope: `spatial_engine.py` player action phase + `arena.py` spawn positions

**Boss AI fix is a NEW open item — scoped for follow-on workstream.** Discipline #11/Discipline #17 escalation filed to knight-rider + gandalf per W0.9.5 standards. **Does NOT block W0.9 cumulative Gate-2 architectural review** (architectural components — PackProxy retirement, usage modes, performance, telemetry — are solid; the structural bug is in player AI behavior).

**Joint-resolution empirical verdict: DEFERRED pending boss AI fix.** Once fix ships, math note §5.3 prediction should hold (high-modifier kits exit boss-zero floor at spatial_DM=2.97; low-modifier mage kits need multi-dim convergence per P2/P3).

**OQ-6 (physical hunter modifier=1.0 ceiling): CLOSED.** Hunter at modifier=0.6355 (not at ceiling). Boss WR=0 reflects add-leash bug, not modifier saturation.

**OQ-7 (stamina-as-resource 1.25× probe overcorrection): CLOSED.** physical_warrior modifier=0.1094 (well below 1.0; no overcorrection). Pool-design escalation not needed.

**Multi-tier archive gap:** routed to P1/P2 follow-on workstream per gamora disposition.

**Discipline #1 (W0.1 + W0.9 math-note predict-vs-measure):** pre-B6 kits used in this sweep (modifiers below prediction band). Full Discipline #1 verification of W0.1 lever predictions requires B6+W0.1 kits — deferred to post-B6 verification sweep (W0.1 Concern 1 not yet fully resolved).

**W0.9 CUMULATIVE GATE-2 READY.** All 5 sub-phases complete; architectural components verified; boss AI fix is new open item for follow-on. Knight-rider fires Gate-2 critique-pair next.

State-of-hive § 1 W0.9 row updated.

---

## 2026-05-21 — QD-rebuild P0 W0.9 Phase 2.4 COMPLETE: telemetry instrumentation LIVE; PARALLEL MODE PRODUCTION READY

**Event:** W0.9 Phase 2.4 (W0.9.5 telemetry instrumentation) returned. Tag `qd-rebuild/v0.9-phase-2-4-telemetry-instrumented` fired (engine commit `8b1703f`). 154/154 tests PASS (36 new W0.9.5 + 118 prior W0.9).

**6 implementation tasks COMPLETE:**

1. **SqliteSpatialTelemetryWriter LIVE** at `telemetry/spatial_recorder.py` — implements `write_fight_event()` + `write_fight_events_batch()`. `_run_spatial_slot()` accepts `spatial_telemetry_writer` parameter (NullWriter default; SqliteWriter for production seasons via caller-side wiring).

2. **8-axis BC fight_events emission per math note §6.7 + star-lord §B amendments:**
   - `FightEvent` dataclass with 14 fields (final spec)
   - 4 event types emitted from `SpatialFightEngine.run()`:
     - `damage_dealt` (Axis 2 / 3B / 2A / 2B) — at player skill fires
     - `damage_received` (Axis 4) — at mob hits landing; mitigation_source="armor"
     - `resource_spent` (Axis 5) — at player skill energy consumption
     - `resource_recovered` (Axis 5) — at tick-level passive energy regen; recovery_source="passive_regen"
   - All 4 star-lord §B amendments honored

3. **Archive insertion from convergence wired:** `BatchGauntletRunner.run_batch()` accepts `archive + archive_entry_builder` callable; insertion under `archive_lock` after each future completes; non-fatal failure handling (WARNING + result returned)

4. **R11(b) round-trip smoke 36/36 PASS** at `tests/test_w095_telemetry.py`: 5-fight convergence at sample_rate=1.0 → fight_events rows populated → SELECT → column presence + value round-trip confirmed

5. **PARALLEL MODE PRODUCTION READY:** `TestParallelIntegration::test_parallel_batch_with_archive_no_corruption` PASS — 2-kit batch via ProcessPoolExecutor with archive insertion; both entries land independently; no shared-state corruption

6. **Storage flag:** `fight_events_sample_rate=0.0` is production default (off; ~430 MB/season at 1.0 prohibitive for routine convergence). Enable 1.0 for targeted BC measurement / calibration sweep passes. 4 dedicated test coverage cases.

**Discipline #12 semantic shift:** the gauntlet now emits per-fight events (8-axis BC fan-out); prior was per-class aggregates only. Documented MIGRATION.md v1.27.

**Phase 2.5 (W0.9.6) fires next** — gamora launched (agentId `ad3feeef4d192f508`). FINAL W0.9 sub-phase + deferred Discipline #17 verification for both W0.1 and W0.9. Calibration sweep design + execution (10-kit roster; production-mirror env; fight_events_sample_rate=1.0) + joint W0.9+W0.1 empirical verification + perf wall-clock benchmark + OQ-6/OQ-7 dispositions + multi-tier archive gap disposition.

---

## 2026-05-21 — QD-rebuild P0 W0.9 Phase 2.3 COMPLETE: 4 performance mitigations LIVE + A3 stability verified

**Event:** W0.9 Phase 2.3 (W0.9.4 performance optimization) returned. Tag `qd-rebuild/v0.9-phase-2-3-performance-optimized` fired (engine commit `09cb812`). 161 tests PASS (37 W0.9.4 + 41 W0.9.3 + 27 W0.9.2 + 56 balance_loop).

**4 Mitigations LIVE:**

1. **Smoke-test mode:** `SmokeTierConfig` (n_fights=30, tick_size=REDUCED_TICK_SIZE, wr_floor=0.05, wr_ceiling=0.95) + `SmokeResult` + `ConvergenceUsageMode.run_slot_smoke()` + tick_size parameter on `run_slot()`. Quick-reject/accept signals enable convergence binary-search early-exit.

2. **Parallel batches (ProcessPoolExecutor):** `KitSlotSpec` picklable + `_run_kit_slot_worker()` top-level + `BatchGauntletRunner.run_batch(use_parallel=True)` + `BatchGauntletRunner.archive_lock` pre-wired for Phase 2.4. Parallelism boundary: ACROSS kits, SEQUENTIAL within a kit.

3. **Cell-targeted convergence:** `CellPriorityResult(NamedTuple)` + `GauntletArchive.cell_priorities()` returns priorities 1=sparse / 2=failing-certification / 3=satisfied. Callers filter `priority < 3` to skip satisfied cells. Estimated ~50% avg convergence iteration reduction.

4. **Reduced-tick-rate (REQUIRED per math note §3.4):** `REDUCED_TICK_SIZE = 0.5` in `spatial_engine.py`. `SpatialFightEngine.tick_size` propagates through all 5 tick operations (mob navigation, player step, cooldown, energy, elapsed).

**A3 stability verification PASS** (math note §3.4 criterion: per-class WR delta ≤ ±0.05 for any tier between 0.1s and 0.5s tick rates):

| Tier | WR(0.1s) | WR(0.5s) | Delta | Status |
|------|----------|----------|-------|--------|
| swarm (open_arena) | 1.0000 | 1.0000 | 0.0000 | PASS |
| boss (boss_with_adds) | 1.0000 | 1.0000 | 0.0000 | PASS |

**REDUCED_TICK_SIZE is QUALIFIED for both swarm and boss tier smoke passes.** No tier disqualification.

**Performance wall-clock benchmark deferred to Phase 2.5 (W0.9.6 calibration sweep with full class cohort).**

**Discipline #12 semantic shift documented (MIGRATION.md v1.26):** smoke-tier convergence iterations at REDUCED_TICK_SIZE=0.5s produce coarser WR time-resolution than full-fidelity iterations. Deliberate: smoke WR is quick binary-search signal, not archive-insertion quality.

**Phase 2.4 (W0.9.5) fires next** — gamora launched (agentId `a7a3920cf469454a1`). Wires real spatial telemetry writer to LIVE v2.15 schema + 8-axis BC fight_events emission + archive insertion via BatchGauntletRunner.archive_lock + round-trip smoke + parallel integration test + fight_events_sample_rate storage flag.

---

## 2026-05-21 — QD-rebuild P0 W0.9 Phase 2.2 COMPLETE: convergence vs validation usage modes implemented

**Event:** W0.9 Phase 2.2 (W0.9.3) returned. Tag `qd-rebuild/v0.9-phase-2-2-usage-modes-implemented` fired (engine commit `c7ede22`). 124 tests PASS (41 W0.9.3 + 27 W0.9.2 + 56 balance_loop).

**P7 W7.2 architectural commitment LIVE.** Two new modules + balance_loop.py delegation:

**`gauntlet_archive.py`** — archive data layer + P7 W7.2 query surface:
- `PerTierWinRate` (per-tier spatial WR record; Optional[float])
- `GauntletArchiveEntry` (one converged kit at BC-cell coord; validate() per Pattern P7)
- `ArchiveQueryResult` (found / entry / certification_pass / failing_tiers)
- `TIER_WR_CONTRACT` (5-tier dict mirroring balance_loop TIER_FLOORS/CEILINGS)
- `GauntletArchive` class: `insert()` (convergence path) + `query()` (validation path) + `query_all()` + `certification_summary()`

**`gauntlet_modes.py`** — explicit caller-level routing:
- `ConvergenceUsageMode` — convergence caller; `run_slot()` calls `run_spatial_fight()`
- `ValidationUsageMode` — P7 W7.2 caller; `certify()` / `certify_batch()` call `archive.query()` ONLY; **architecturally barred from calling `run_spatial_fight()` — verified by test**
- `CertificationRequest` / `CertificationResult` (P7 W7.2 I/O records)

**Architectural violation clause (math note §6.4 A4):** future code calling `run_spatial_fight()` inside P7 W7.2 certification path requires explicit ADR-level approval. The structural barrier is in code, not just in commentary.

**balance_loop.py delegation:** `_run_spatial_slot()` now delegates to `ConvergenceUsageMode(session_id_prefix=SWARM_SPATIAL_SESSION_PREFIX).run_slot(...)`. Functional behavior unchanged. Discipline #12 semantic shift documented MIGRATION.md v1.25.

**Phase 2.3 (W0.9.4) fires next** — gamora launched (agentId `a325dc8096ab5d272`). 4 performance mitigations: smoke-test mode + parallel batches + cell-targeted convergence + reduced-tick-rate (REQUIRED per math note §3.4 + A3 stability criterion).

---

## 2026-05-21 — QD-rebuild P0 W0.1 FULLY CLOSED: B14.5 V2 energy-type lever shipped + Gate-2 critique-pair complete

**Event:** W0.1 Phase 2 Gate-2 critique-pair returned with both reviews. Tag `qd-rebuild/v0.1-b14-5-v2-energy-type-lever` stands (engine commit `a0889d2`). Documentation amendment folded by knight-rider per jack-ryan ADR-002 APPROVE authority (engine commit `9254980`).

**gandalf architectural close-out — ARCHITECTURALLY ALIGNED:**
*"The implementation IS the canonical exemplar of Calibration Lever Partition Principle (#13a-partition). Future calibration levers will reference W0.1 as the partition-on-mechanical-population pattern."*

8 architectural-compliance findings verified:
- #13a-partition: zero substrate-keying anywhere; lever inputs are mechanical (`energy_type`, working_modifier, floor_lock_detected, WR)
- G3 architectural invariant: assertion + defense-in-depth (outer guard + inner assertion); lever-ownership message present in code
- Joint-resolution triad orthogonality preserved (W0.1 calibration / W0.2 source / W0.9 arena)
- Substrate-as-cohesion preservation: telemetry field keyed off mechanical population
- OQ-6 handoff to W0.2 + W0.9 joint resolution honored
- Reversibility 3-tier (sub-lever A independent flag + sub-lever B soft-disable + full removal) — architecturally SUPERIOR to monolithic Option B
- ARPG-canon thematic: rage startup-gap closure + physical/rage calibration headroom both genre-canonical
- gandalf A6 naming preference (`recompose_energy_calibration_applied`) adopted in implementation

2 gandalf RECOMMENDED non-blocking amendments (carry forward):
- Math note §3.2 anti-pattern foreclosure: per-energy-type magnitude scaling rejected as lever-tuning anti-pattern
- Future engineering-disciplines.md codification of #13a-partition with W0.1 as canonical exemplar

**jack-ryan Gate-2 DEV-MODE — APPROVE-WITH-AMEND** (1 documentation amendment, non-blocking):

9 review focus areas all PASS/PARTIAL-PASS:
- Sub-lever A correctness vs A1 fold-in spec: PASS (activation `energy_type==rage AND not reduce_dps AND not increase_dps AND WR<0.50` confirmed at balance_loop.py:2151-2161)
- Sub-lever B correctness: PASS (G3 assertion fires at top; A5 probe scope isolation comment present)
- Telemetry field always-present (key always emitted with False for non-rage): PASS
- R11(b) round-trip smoke E.2: PASS (Q3 probe arithmetic 0.55 × 1.25 = 0.6875)
- Test surface 56/56: CONFIRMED
- Discipline #11.1: PARTIAL PASS — amendment for math note status block
- Discipline #12 semantic shift: PASS
- Discipline #1 math-before-code: PASS
- #13a-partition compliance: PASS

**Amendment 1 (folded by knight-rider per jack-ryan ADR-002 APPROVE authority):** math note status block updated to reflect Phase 2 COMPLETE + pre-B6 fallback smoke caveat (rage=0.155, stamina-as-resource=0.037 well outside 0.60-0.70 prediction band; smoke confirms MECHANISM not predictions) + full Discipline #17 verification deferred to W0.9.6 co-run.

**Concern dispositions:**
- Concern 1 (calibration co-run with W0.9.6): APPROVED scheduling
- Concern 2 (sub-lever A dormancy pre-B6): acceptable transitional state
- Concern 3 (stamina-as-resource 1.25× overcorrection): monitor post-B6 per Track C OQ-7
- Concern 4 (v2.15 migration deferral): RESOLVED — star-lord shipped v2.15 migration this session (engine `0e15f61`)

**W0.1 FULLY CLOSED.** Joint-resolution triad status:
- ✅ **W0.2 source diversity** — substrate-AGNOSTIC composition LIVE
- ✅ **W0.1 calibration fairness** — energy-type lever LIVE; canonical exemplar of #13a-partition
- 🔄 **W0.9 arena fidelity** — Phase 2.1 done; Phase 2.2 in-flight; 2.3-2.5 queued

State-of-hive § 1 W0.1 row updated to FULLY CLOSED.

---

## 2026-05-21 — QD-rebuild Cross-seam: v2.15 MIGRATION SHIPPED to production DB

**Event:** Star-lord shipped the v2.15 ALTER TABLE migration to production telemetry.db. Engine commits `0e15f61` (feat) + `5f1e3e4` (AGENT_STATE) + `9d41e8d` (telemetry/MIGRATION.md). Tag `star-lord/v1.18-v2-15-migration-shipped` fired.

**E.1 fixture (recorder-side round-trip smoke for archetype_label):** 8/8 PASS at `tests/test_w02_archetype_label_round_trip.py`. All 9 spec assertions from v2.15 §E.1 covered. Confirms: TEXT column type; NULL backward-compat; exact key contract (`archetype_label` only — `archetype` / `archetype_tag` do NOT pollute); no WARN on null; mixed-vintage row coexistence; zero silent_drop_counters after both paths.

**recorder.py integration (same commit):**
- `archetype_label` read on `record_class_fight_loadouts`
- `floor_lock_recompose` read on `record_class_balance_results` (v2.14 catch-up)
- NEW `record_recompose_attempts` method (v2.14 + v2.15 P7 WARN for post-W0.9.5 missing key)
- NEW `record_fight_events` method (v2.14)
- NullRecorder stubs for both new methods
- SCHEMA_VERSION bump: "2.13" → "2.15"

**PRODUCTION DB MIGRATION EXECUTED** in sequence 2.12 → 2.13 → 2.14 → 2.15. Star-lord caught up v2.13 + v2.14 catch-up migrations (DB was at 2.12 pre-session; v2.13 had not been applied to production despite being in MIGRATIONS list).

**Post-migration verification (all new fields/tables present):**
- `archetype_label` in `class_fight_loadouts` ✅
- `recompose_energy_calibration_applied` in `recompose_attempts` ✅
- `fight_events` table (18 columns) ✅
- `floor_lock_recompose` in `class_balance_results` ✅
- `geometry_type_source` in `spatial_fight_results` (v2.13 catch-up) ✅

**80/80 round-trip regression suite PASS** (round_trip_r3 + round_trip_r1 + round_trip_r1_kill_rate + round_trip_spatial). Stale schema assertion `SCHEMA_VERSION == "2.13"` fixed to forward-compat `>= (2, 13)`.

**Cross-seam delivery contract complete:**
- W0.2 round-trip smoke E.1 (rocket write-side stub + star-lord recorder-side) ✅ PASS
- W0.1 round-trip smoke E.2 (gamora write-side + star-lord recorder-side) ✅ PASS (per W0.1 Phase 2 completion)
- v2.15 ALTER TABLE migration ✅ EXECUTED against production DB per knight-rider authorization (per Matt autonomous-operation directive)
- Both new columns + recompose_attempts table + fight_events table LIVE

**No drax impact** per v2.15 §E.3 (archetype_label is telemetry-only; not exported in season JSON packet).

**Major architectural milestone:** The v2.15 schema infrastructure is now production-ready. W0.1 + W0.2 cross-seam contracts fulfilled. Future workstreams (W0.9 Phase 2.4 telemetry instrumentation; W1.13 archive_entries table; P3 archive maintenance) build on this LIVE schema foundation.

---

## 2026-05-21 — QD-rebuild P0 W0.2 FULLY CLOSED: Phase 2.5 cleanup amendments folded

**Event:** W0.2 Phase 2.5 (rocket cleanup fold-in) completed. All 3 jack-ryan Gate-2 amendments folded. Engine commit `6d4743d`; collab commit `5387256`. Tag `qd-rebuild/v0.2-phase-2-5-cleanup` fired.

**Amendments folded:**
- **A1 (WARN — b6_archetype_templates.py deprecation banner):** explicit deprecation block added matching `archetype_composer.py` pattern (DEPRECATED date + tag + removal gate P5 W5.X + replacement module + math note §9.3 + recompose-hive Option B precedent cites)
- **A2 (WARN — test file paths):** test artifact table appended to AGENT_STATE.md: `tests/test_w02_bc_target_composer.py: 57/57` + `tests/test_d3_archetype_composer.py: 67/67` (2 pre-existing skips, not failures). 124 pass / 2 skipped / 0 failures verified.
- **A3 (INFO — unified_mechanic_pool.yaml footer):** corrected stale count from "70 / 4 / 74" → accurate "67 / 4 / 71" matching the W0.2.1 deliverable.

**W0.2 FULLY CLOSED.** All W0.2 tags:
- `qd-rebuild/v0.2-math-note-phase-1-complete` (Phase 1+1.5 math-before-code)
- `qd-rebuild/v0.2-archetype-refactor-complete` (Phase 2 implementation)
- `qd-rebuild/v0.2-phase-2-5-cleanup` (Phase 2.5 cleanup)

**Carry-forward advisories** (documented in AGENT_STATE open items):
- gandalf A3 (P5 W5.X): scrub substrate-origin section-header comments from `unified_mechanic_pool.yaml` at cohesion-judge ship-gate cleanup
- gandalf A4 (Phase 3 handoff): treat `pool_depletion_events` counter as pool-expansion diagnostic, not algorithm-tuning input
- v2.15 migration execution: star-lord seam; gated on W0.1 round-trip smoke E.2 PASS

**Substrate-AGNOSTIC GENERATION ARCHITECTURALLY COMPLETE.** The substrate-as-cohesion-only commitment ratified 2026-05-21 is now fully implemented at the generation layer of the engine. Phase 5 cohesion-judge will supersede `archetype_label` with thematic substrate identity at P5 W5.X.

State-of-hive § 1 W0.2 row updated to FULLY CLOSED. Joint-resolution triad status:
- ✅ W0.2 source diversity (archetype-lock removed; substrate-AGNOSTIC composition LIVE)
- 🔄 W0.9 arena fidelity (Phase 2.1 done; 2.2-2.4 queued)
- 🔄 W0.1 calibration fairness (Phase 2 implementation in-flight)

---

## 2026-05-21 — QD-rebuild P0 W0.2 Phase 2 Gate-2 critique-pair returns: BOTH APPROVE-WITH-AMEND (no BLOCK)

**Event:** Both Gate-2 reviews of W0.2 Phase 2 implementation returned per protocol § 4.2 critique-pair pattern.

**gandalf architectural close-out — ARCHITECTURALLY ALIGNED:**
*"This implementation is the cleanest engine-layer expression of substrate-as-cohesion-only that has appeared in the codebase. The W0.2 math note's commitment that 'substrate is NOT an input to mechanical generation' is honored end-to-end."*

8 strong-alignment findings verified:
- Substrate-AGNOSTIC pool VERIFIED CLEAN (substrate tags appear ONLY in section-header provenance comments, not data)
- Composer substrate-AGNOSTIC VERIFIED (`(bc_target, role, rng, profile)` only signature)
- archetype_label format VERIFIED (no substrate string anywhere)
- #13a-partition compliance VERIFIED (partitions only on mechanical properties)
- Orchestrator severance audit ACCEPT-THE-FINDING (parallel architecture transitional state correctly scoped)
- Cohesion-judge handoff CLEAN (three-label coexistence model enabled by ComposedKit + nullable archetype_label)
- Cross-substrate hybrid composition ENABLED (cost-filtered pool draws across previously substrate-locked mechanic pools — the load-bearing architectural unlock)
- Joint-resolution triad decoupling CLEAN (W0.2 source diversity independent of W0.9 arena fidelity + W0.1 calibration fairness)

2 advisory amendments (non-blocking):
- gandalf A3 (P5 W5.X advisory): scrub substrate-origin section-header comments from unified_mechanic_pool.yaml at cohesion-judge ship-gate cleanup
- gandalf A4 (Phase 3 handoff advisory): treat `pool_depletion_events` counter as pool-expansion diagnostic, NOT algorithm-tuning input

**jack-ryan Gate-2 DEV-MODE — APPROVE-WITH-AMEND:**

17 check areas verified; 3 amendments (all WARN/INFO; no BLOCK):
- A1 WARN: b6_archetype_templates.py needs explicit W0.2 deprecation banner block (similar to archetype_composer.py lines 1-33); module docstring lacks the "DEPRECATED as of W0.2 / removal gate P5 W5.X" treatment
- A2 WARN: test file paths in qa/pending submission missing (57 new W0.2 tests + 67 D3 backward-compat tests claimed passing but paths not provided; process gap not correctness gap)
- A3 INFO: unified_mechanic_pool.yaml footer count stale (70/4/74 → should be 67/4/71)

All other check areas PASS: 8-step algorithm fidelity, resolve_cost_type lockdown, role-cost_type correlation table match, Gumbel-max weighted draw, role-shape POST-assembly, PoolDepletionError→DeferredEvaluation, HP-economy/proxy/charge-stack infeasibility mapping, orchestrator severance audit empirically correct, ARCHETYPE_TEMPLATES deprecation banners, R11(b) open item correctly documented, v2.15 co-migration mandate, Discipline #11.1 BC distribution, Discipline #12 semantic shift framing, Discipline #1 math-before-code predictions verified, #13a-partition compliance.

**Outcome:** W0.2 Phase 2 architecturally + correctness verified. Knight-rider fires quick Phase 2.5 cleanup dispatch to rocket for the 3 jack-ryan amendments (banner + test paths + count correction). gandalf A3 + A4 advisories carry forward to P5 / Phase 3 obligations (no immediate action).

---

## 2026-05-21 — QD-rebuild P0 W0.2 Phase 2 COMPLETE: archetype removal implementation shipped; substrate-AGNOSTIC composition LIVE

**Event:** W0.2 Phase 2 substantial implementation returned (rocket; ~54min execution). All 6 sub-tasks complete. Tag `qd-rebuild/v0.2-archetype-refactor-complete` fired (engine commits `e696b9f` + `321afa5`).

**Sub-task deliverables:**

- **W0.2.1 — Unified mechanic pool** (`generation/unified_mechanic_pool.yaml`): 71 entries (67 active + 4 deferred); 5 cost types; 15 CC + 5 movement + 8 gear affixes. Deferred bins (HP-economy, charge-stack, damage-taken-converts, proxy-creation) marked with reasons per LC-030. **Substrate tags stripped throughout** — pure mechanical-property pool per substrate-as-cohesion-only.

- **W0.2.2 — bc_target_composer.py** + **HARD GATE: Orchestrator severance audit CONFIRMED COMPLIANT.** Full 8-step algorithm per math note §4. `resolve_cost_type(econ_bin, role, rng) ONLY` lockdown enforced (gandalf A2). Weighted-random Gumbel-max draw without replacement. Role-shape POST-assembly. PoolDepletionError → DeferredEvaluation (jack-ryan A1). HP-economy → None (hard-infeasible). Proxy bins → DeferredEvaluation. `pool_depletion_events` telemetry counter logged. **Audit finding:** `season_orchestrator._generate_classes()` does NOT emit archetype tags; archetype_tag derived inside ClassGenerator via `classify_archetype()`; seasonal elements feed coalescence/naming only. Contract 1 satisfied.

- **W0.2.3 — ARCHETYPE_TEMPLATES deprecation:** banners added; dict preserved + populated for backward-compat. P5 W5.X removal gate documented.

- **W0.2.4 — legacy_archetype_shim.py:** 24-row translation table (all archetype tags from math note §5.1). `compose_for_archetype_tag()` + `bc_target_for_archetype()`. ArchetypeTagNotFound raises on unknown.

- **W0.2.5 — Tests:** 57 new W0.2 tests **57/57 PASS**; 204 existing generation tests **204/204 PASS**; 67 D3 archetype composer **67/67 PASS**. Pre-existing failures unchanged (bruiser gap, gear cp3 balance). BC distribution verified: physical_warrior → rage → tier 65; hunter → focus → tier 58; elemental → mana → tier 50. Pool depletion for thin CC pools (control + stamina) correctly routes to DeferredEvaluation.

- **W0.2.6 — MIGRATION.md** (`generation/MIGRATION.md`): cross-seam consumer obligations + v2.15 co-migration mandate + orchestrator severance finding + shim calibration obligation. PlayerClass.archetype_label field added (nullable backward-compat). **R11(b) PARTIAL** — schema field added; recorder.py integration is star-lord seam (open Gate-2 item; v2.15 migration execution gate).

**Architectural concern (Gate-2 awareness):** `resolve_cost_type()` 10% stochastic noise (90% top-pick + 10% non-top). For thin-pool cost types (stamina-as-resource: 2 mechanics, no CC), control-role compositions hitting the 10% non-top path produce DeferredEvaluation. Correct per math note spec (PoolDepletionError → DeferredEvaluation). gandalf A2 lockdown spirit satisfied (rng is explicit input). Awareness-only flag.

**Cross-seam coordination tasks:**
- Star-lord: recorder.py writes `player_class.archetype_label` → `class_fight_loadouts.archetype_label` (v2.15 co-migration execution)
- Gamora: `CombatantState.archetype` prefers `archetype_label` when non-null; falls back to `archetype_tag`
- Drax: `archetype_label` is BC-coordinate format (not human-friendly); placeholder or `archetype_tag` during migration

**SUBSTRATE-AGNOSTIC GENERATION NOW LIVE.** Phase 5 cohesion-judge will supersede `archetype_label` with proper substrate-themed identity at P5 W5.X. Substrate-as-cohesion architectural commitment is now empirically implemented in the engine.

State-of-hive § 1 W0.2 row updated. Gate-2 critique-pair review fires next (jack-ryan + gandalf parallel).

---

## 2026-05-21 — QD-rebuild P0 W0.9 Phase 2.1 COMPLETE: PackProxy retired; 5-tier spatial gauntlet promoted

**Event:** W0.9 Phase 2.1 (PackProxy ×8 retirement from swarm-tier convergence + R2 spatial sub-gauntlet promotion to default for all 5 tiers + 3 new arena scenarios per A8 § 9) returned successfully after ~46 minutes of substantial implementation work. Engine tag `qd-rebuild/v0.9-phase-2-1-packproxy-retired-r2-promoted` fired (commit `0041a12`).

**PackProxy disposition: DEPRECATED in-tree (not removed).** Rationale: 3 test files contain PackProxy-specific assertions documenting pre-W0.9.1 behavior; `damage_resolver.py` `pack_proxy_size` AOE multiplier preserved for backward-compat; backward-compat with telemetry reads of pre-W0.9.1 season data. "Fix the arena, not the synergy" principle calls for removal from the *convergence path* — in-tree retention is correct for the DEPRECATED class itself until a deliberate cleanup dispatch.

**3 new ArenaScenario constants** authored in `simulation/spatial_gauntlet/arena.py` per gandalf A8 § 9 handoff:
- `SCENARIO_MAGIC_PACK` (32.7×14m; 1 magic + 3 swarm; 120s kills-only; WR 0.55-0.70)
- `SCENARIO_ELITE_PACK` (28×28m; 1 elite + 2 magic; 180s kills-only; WR 0.45-0.60)
- `SCENARIO_MINI_BOSS` (30×30m; 1 mini-boss + 2 elite; mini_boss_killed; 150s soft / 240s hard)
- Boss tier uses existing `SCENARIO_BOSS_WITH_ADDS` (per A8 § 6 — no new scenario)

`ArenaScenario` dataclass extended with `mini_boss_index`, `soft_timeout_s`, `has_mini_boss` property. `SpatialFightEngine.run()` handles `mini_boss_killed` with two-phase timeout.

**Encounter_kind `"magic"` enum value DEFERRED to W0.9.5** (Phase 2.3 star-lord territory). Phase 2.1 uses `NullSpatialTelemetryWriter` — no telemetry emitted from convergence-path spatial fights. `"elite"` + `"mini-boss"` already exist in schema. Cross-seam request documented in `simulation/MIGRATION.md v1.23`.

**Test results:** 311 targeted smoke tests PASS; 27 new `test_spatial_gauntlet_scenarios.py` tests PASS. 2 previously failing `TestModifierClampGate` tests fixed by extending mock coverage to `_run_spatial_slot`.

**Discipline #12 semantic shifts documented** in commit message + MIGRATION.md v1.23:
1. Swarm-tier opponent type: `PackProxy` → raw `Monster` (spatial sim) — architectural arena change
2. `TIER_CONVERGENCE_WEIGHTS["swarm"]`: 0.0 → 1.0 — under PackProxy, swarm WR was 1.000 trivially (no info content; weight 0.0 correct). Under true multi-monster, swarm WR carries information about positional AOE effectiveness; weight 1.0 reflects ARENA change, not tuning preference.

**Phase 2.2 next-fire context (W0.9.3):** `_run_spatial_slot()` provides convergence-mode entry point. P7 W7.2 archive-query validation path (per math note §6.4) is load-bearing architectural commitment.

**W0.1 Phase 2 UNBLOCKED** (balance_loop.py changes now safely sequential; W0.1 fires per its own dispatch).

State-of-hive § 1 W0.9 row updated to Phase 2.1 COMPLETE.

---

## 2026-05-21 — QD-rebuild Cross-seam: v2.15 co-migration spec authored (W0.2 + W0.1 jointly)

**Event:** Per jack-ryan W0.2 Gate-1 Amendment A4 mandate (single ALTER TABLE for co-migration), star-lord authored the v2.15 schema co-migration spec. Engine tag `star-lord/v1.17-w0-2-w0-1-schema-v2-15-co-migration-spec` fired (commit `c4a409c`).

**v2.15 transition (telemetry/MIGRATION.md Sections A-F; ~460 lines):**
- **Section A** versioning rationale: v2.14 amendment path closed (W0.9 Phase 2.1 in-flight race risk); v2.15 clean non-racing bump; co-migration batches both columns into single `_V2_15` SQL block
- **Section B** W0.2 `archetype_label TEXT NULL` on `class_fight_loadouts`. **Critical clarification:** `class_fight_loadouts` does NOT carry `archetype_tag` column in existing schema — that field lives on rocket's in-memory `ArchetypeTemplate` kit object. The "deprecated-in-place" obligation therefore applies to rocket's kit object, not telemetry schema column. Drax NOT affected (telemetry-only field).
- **Section C** W0.1 `recompose_energy_calibration_applied INTEGER NULL` on `recompose_attempts`. NULL/0/1 semantics; NULL semantically distinct from 0. Pattern P7 WARN-level trigger when `floor_lock_detected` is present (post-W0.9.5 gamora) but the new key is absent.
- **Section D** single `_V2_15` SQL block (no window where one column exists without the other); SCHEMA_VERSION bump `"2.14" → "2.15"` sequenced AFTER both round-trip fixtures PASS
- **Section E** two round-trip smoke fixtures per R11(b):
  - E.1 W0.2 archetype_label: rocket stub dict (write) + star-lord recorder (9-step assertions)
  - E.2 W0.1 recompose_energy_calibration_applied: gamora write (physical_warrior rage =True + fire_mage mana =False) + star-lord recorder (16-step including P7 WARN trigger test)
- **Section F** ownership + migration execution gate: both fixtures pass + knight-rider authorization (per Matt autonomous-operation directive 2026-05-21)

**Cross-seam coordination questions surfaced:**

For rocket (W0.2 Phase 2 in-flight, agentId `a6b155079a5eff915`):
1. fight_log dict key must be exactly `archetype_label`
2. Smoke fixture E.1 can be minimal stub dict — no full season regen required
3. archetype_label is telemetry-only (NOT export schema)

For gamora (W0.1 Phase 2 future):
1. Every attempt dict post-W0.1 must include `recompose_energy_calibration_applied` as explicit key (False for non-rage classes; not absent — triggers P7 WARN otherwise)
2. `floor_lock_detected` must also be always-present in post-W0.9.5 dicts (False not absent)
3. Smoke fixture E.2 modifier value 0.55 needs to fall within sub-lever B trigger range — gamora confirms

For knight-rider:
- Migration execution gate: both fixtures PASS → knight-rider authorizes ALTER TABLE migration execution against production telemetry.db (under Matt autonomous-operation directive 2026-05-21)

---

## 2026-05-21 — QD-rebuild P0 W0.2 Phase 1 + Phase 1.5 COMPLETE: archetype removal math-before-code locked + substantial-workstream-triad math-before-code FULLY LOCKED

**Event:** W0.2 (rocket; archetype template Path-a refactor under substrate-as-cohesion-only) Phase 1 + Phase 1.5 (amendment fold-in) complete. Tag `qd-rebuild/v0.2-math-note-phase-1-complete` fired (engine commit `ad22883`; collab commit `784750e`).

**Math note canonical version** at `reincarnated-engine/src/reincarnated/generation/math/w0-2-archetype-removal-bc-target-composition.md`. 6 amendments handled from jack-ryan Gate-1 (4) + gandalf architectural review (2):

**Folded into math note pre-Phase-2:**
1. **gandalf A2 — resolve_cost_type input lockdown (§4.1):** function signature changed to `(econ_bin, role, rng) ONLY`. Role-cost_type correlation table PUBLISHED in math note (damage prefers rage>combo>focus>mana>stamina; control prefers mana>focus>stamina>combo>rage; support mana-dominant; hybrid spans all). Econ_bin-to-cost_type structural mapping published.
2. **jack-ryan A1 — Pool depletion fallback (§4.3):** `PoolDepletionError → DeferredEvaluation` route chosen. No silent truncation. Telemetry obligation: log `pool_depletion_events` counter per (cost_type, role) pair; >10% rate triggers pool extension.
3. **jack-ryan A2 — v2.15 column bump LOCKED (§8.2):** "DECISION" framing replaces "recommendation." Column-repurpose path explicitly closed per Discipline #12. NEW `archetype_label TEXT` alongside existing `archetype_tag` is ONLY acceptable path.
4. **gandalf A1 — season_orchestrator.py Phase 1 architectural contract (§11.5):** expanded with 3 locked commitments (seasonal elements feed P5 cohesion-judge ONLY; orchestrator emits BC-targets not archetype tags; W0.2.2 orchestrator-severance-audit hard gate before any smoke run).

**Deferred to W0.2.6 MIGRATION.md authoring:**
- jack-ryan A3 (§5.1 tail): shim pass/fail criterion — >20% drift on any axis triggers recalibration before P5
- jack-ryan A4 (§8.4): v2.15 co-migration mandatory — SINGLE ALTER TABLE script covering W0.2 (`archetype_label`) + W0.1 (`recompose_energy_calibration_applied`); star-lord joint authorship

**Gandalf closing assessment of W0.2 Phase 1:** *"Cleanest expression of substrate-as-cohesion-only that has yet appeared in the engine."* All five safeguard principles of the substrate supplement honored at algorithm level.

**SUBSTANTIAL-WORKSTREAM TRIAD MATH-BEFORE-CODE FULLY LOCKED:**
- ✅ W0.9 Phase 1 + 1.5 + A8 + A5 (gauntlet architecture migration; Phase 2.1 implementation in-flight)
- ✅ W0.1 Phase 1 + 1.5 (B14.5 V2 energy-type lever; Phase 2 pending W0.9 Phase 2.1)
- ✅ W0.2 Phase 1 + 1.5 (archetype removal; Phase 2 pending co-migration spec)

Joint-resolution triad architecturally locked: W0.2 source diversity + W0.9 arena fidelity + W0.1 calibration fairness. Three orthogonal layers; all three needed to resolve Pattern-A boss-floor.

**Phase 2 implementation routing (next):**
- W0.9 Phase 2.1 in-flight (must complete before W0.1 Phase 2 because both touch `balance_loop.py`)
- W0.1 Phase 2 fires after W0.9 Phase 2.1 returns
- W0.2 Phase 2 can fire independently (different seam: `generation/` vs `simulation/`)
- Star-lord v2.15 co-migration spec coordinates W0.2 + W0.1 columns jointly

State-of-hive § 1 W0.2 row updated. **8 P0 workstreams milestone-complete** (W0.3 + W0.4 star-lord + W0.4 rocket + W0.5 + W0.6 + W0.8 + W0.1 phase-1.5 + W0.9 phase-1.5 + W0.2 phase-1.5; W0.9 Phase 2.1 implementation in-flight; W0.1 + W0.2 Phase 2 implementations queued; W0.7 + W0.4 gamora portion remaining).

---

## 2026-05-21 — engineering-disciplines.md § 13a-partition ratified: Calibration Lever Partition Principle

**Event:** Per gandalf W0.1 architectural review amendment A8, ratified by jack-ryan DESIGN-MODE as new sub-prescription **Discipline #13a-partition** (Option A — elaboration under existing #13a drift-discipline; route-of-authority for substrate-keying-at-calibration anti-pattern detection). Engine commit `18f47a8`.

**The principle (load-bearing one-sentence statement):**
*"Calibration levers in the balance loop and convergence pipeline must partition their adjustments by mechanical population properties (energy_type, geometry-range, arena scenario, etc.) — never by substrate identity (physical / shadow / holy / lightning / etc.)."*

**Empirical anchors:**
- W0.1 sub-lever B (energy_type partition; first statement of principle in gamora math note § 5)
- W0.9 spatial migration (arena/geometry partition in gamora math note)
- substrate-as-cohesion-only architectural recommitment (substrate supplement 2026-05-21 § 1 + § 3)

**Rationale for Option A:** substrate-keyed calibration branching is observable from code-reading alone (detectable at Gate-1 without telemetry) — exact structural signature of a Discipline #13a drift violation against the substrate-as-cohesion-only commitment. Routing through #13a consolidates drift-discipline authority.

**Detection mechanism:** any `if substrate == "X"` branching in `balance_loop.py` or `convergence_pipeline.py` flagged at Gate-1 as a #13a-partition violation. Reviewers cross-check substrate-keyed branches against this discipline.

**Cross-references:**
- `canonical/story/substrate-design-supplement-2026-05-21.md` § 1 + § 3 (architectural recommitment + five safeguard principles)
- `reincarnated-engine/src/reincarnated/simulation/math/w0-1-b14-5-v2-energy-type-lever.md` § 5 A8 (first statement of principle)
- `reincarnated-engine/src/reincarnated/simulation/math/gauntlet-migration-arena-equivalence.md` (W0.9 math note; arena/geometry partition)
- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 2.0 (architectural intent enforced)

**Authority:** jack-ryan DESIGN-MODE per ADR-002 + Matt's autonomous-operation directive 2026-05-21; knight-rider authorized the codification per the protocol § 7.1 routine governance flow.

---

## 2026-05-21 — QD-rebuild P0 W0.2 Phase 1 COMPLETE: archetype removal math-before-code

**Event:** W0.2 (rocket; archetype template Path-a refactor under substrate-as-cohesion-only — REMOVE archetype layer entirely) Phase 1 math-before-code complete. Engine commit `e306c0b`. Math note at `reincarnated-engine/src/reincarnated/generation/math/w0-2-archetype-removal-bc-target-composition.md` (865 lines, 11 sections).

**Scope sharpened by W0.4 LC-001 finding** (D3 Path-a composition already live): W0.2 is NOT "refactor frozen dict to compose at boot" (done) but "REMOVE the archetype layer entirely; pure BC-target-driven composition from unified substrate-AGNOSTIC mechanic pool."

**Key design decisions:**
- **Composition algorithm:** 8-step pseudocode; weighted-random draw without replacement; per-axis alignment score product as weight; role-shape constraints POST-assembly; infeasible → None or DeferredEvaluation
- **Unified pool:** ~150-250 mechanics; substrate tags stripped from 23 current templates
- **ARCHETYPE_TEMPLATES disposition:** DEPRECATE-IN-PLACE (mirrors recompose-hive precedent)
- **`archetype_label` format:** BC-coordinate-derived `"{eng_bin}/{geo_bin}/{ctrl_bin}/{def_bin}/{econ_bin}_{role}_{cost_type}"`
- **Energy-type tier carry-forward:** B6 tier amounts preserved (rage=65, combo/focus=58, mana=50); keying migrates to cost_type (mechanical pillar; satisfies #13a-partition)
- **Cross-seam:** v2.15 schema bump on class_fight_loadouts (archetype_label TEXT nullable) — **aligns with W0.1's v2.15** for co-migration opportunity

**Four architectural concerns for Gate-1:** season_orchestrator coupling (deferred to W0.2.2); shim translation table is prediction-only; physical template special constraints map to mechanic geometry; support role deferred Profile A.

**Joint-resolution triad confirmed:** W0.2 (source diversity) + W0.9 (arena fidelity) + W0.1 (calibration fairness) — all three needed; orthogonal architectural layers.

**Phase 2 routing:** jack-ryan Gate-1 + gandalf architectural review fired in parallel. Phase 2 implementation pending consolidation.

---

## 2026-05-21 — QD-rebuild P0 W0.1 Phase 1 + Phase 1.5 COMPLETE: B14.5 V2 energy-type lever math-before-code locked

**Event:** W0.1 (gamora; B14.5 V2 energy-type lever in primary recompose loop) Phase 1 (math-before-code) + Phase 1.5 (amendment fold-in) workstreams complete. Tag `qd-rebuild/v0.1-math-note-phase-1-complete` fired (engine commit `5bbc2f4`; collab commit `351252a`).

**Math note canonical version** at `reincarnated-engine/src/reincarnated/simulation/math/w0-1-b14-5-v2-energy-type-lever.md`. 8 amendments folded from jack-ryan Gate-1 (5; including 2 BLOCK) + gandalf architectural review (3):

**jack-ryan amendments:**
- A1 BLOCK: sub-lever A activation condition — GAP CONFIRMED via empirical inspection. Phase 2 spec: fire when `energy_type=="rage" AND not reduce_dps AND not increase_dps AND WR<0.50`. Stays within-lever.
- A2 BLOCK: R11(b) schema coordination — path (b) v2.15 bump chosen (avoids W0.9 Phase 2.3 execution race risk); ALTER TABLE recompose_attempts ADD COLUMN `recompose_energy_calibration_applied INTEGER`
- A3 WARN: epoch arithmetic reconciliation (9-class/11-term count + post-W0.1 0.78 vs 0.65-0.72 target)
- A4 WARN: Discipline #17 smoke environment parity (gear_catalog + monster_pool production-mirror)
- A5 INFO: probe scope isolation comment for Phase 2 implementation

**gandalf amendments:**
- A6 architectural: field naming — `recompose_energy_calibration_applied:bool` adopted (gandalf preference; describes what lever DID, not what it's named after)
- A7 architectural: G3 floor-lock guard reframed as ARCHITECTURAL INVARIANT (assertion-at-top-of-sub-lever-B); lever-ownership principle
- A8 architectural: **NEW NAMED PRINCIPLE** — "Calibration levers are partitioned by mechanical population (energy_type, geometry-range, etc.), never by substrate identity." Engineering-disciplines.md candidate.

**Lever design (post-fold-in canonical):**
- Sub-lever A: within-lever modification to `_lever_cooldown_energy` — fires for rage classes when WR<0.50 in fine-tune zone; targets highest-energy-cost skill for cost reduction
- Sub-lever B: new `_lever_energy_type_calibration` (4th lever in `_primary_recompose_loop`); applies `ENERGY_TYPE_LEVER_PROBE_ADJUSTMENT = 1.25` to working_modifier for `ENERGY_TYPE_LEVER_PHYSICAL_TYPES = frozenset({"rage", "combo", "stamina-as-resource"})`
- F3 armor mitigation excluded (B6 pre-work addresses)
- Focus/hunter excluded provisionally (re-inclusion gate at post-B6 hunter modifier < 0.75)
- G3 floor-lock short-circuit assertion (architectural invariant)
- Reversibility: `ENERGY_TYPE_LEVER_PROBE_ADJUSTMENT = 1.0` soft-disable (Option B precedent)

**Predicted compression (corrected post-fold-in):**
- physical_warrior 0.38 → 0.60-0.70 (B6+W0.1 combined)
- mean |mod-1.0| epoch 0.82 → 0.65-0.72
- 0.50 target requires W0.9 + P1/P2 multi-dim convergence

**Phase 2 implementation gates:**
- W0.9 Phase 2.1 completion (both W0.9 + W0.1 touch balance_loop.py; sequential to avoid conflict)
- Star-lord v2.15 schema migration (recompose_energy_calibration_applied field) — coordinate at Phase 2 fire

**Gandalf closing on W0.1 math note:** substrate-as-cohesion preservation CLEAN; W0.1/W0.9 joint-resolution architecturally orthogonal; Track C calibration-uniform aligned; ARPG canon preserved.

State-of-hive § 1 W0.1 row updated to Phase 1+1.5 complete.

---

## 2026-05-21 — QD-rebuild P0 W0.4 rocket portion COMPLETE: LC-001 DRIFT-FROM-AUDIT (positive); W0.2 scope reframed

**Event:** W0.4 rocket portion completed and merged. Engine tag `rocket/v1.23-w0-4-code-side-audit-1` fired (commit `f4554f7`).

**MAJOR FINDING — LC-001 DRIFT-FROM-AUDIT (positive):** D3 Path-a composition is ALREADY LIVE via `archetype_composer.py`. `ARCHETYPE_TEMPLATES` is built at boot from SubstrateIdentity × Role (NOT the "frozen 14-entry dict" jack-ryan's Phase 1 audit described). 23 templates total: 18 composed elemental (7 substrates × 3 composition roles with fire/water alias collapse + earth_burst + wind_burst) + 5 physical hardcoded (hunter / physical_warrior / physical_grappler / physical_skirmisher / rogue).

**Implication for W0.2:** under substrate-as-cohesion-only, W0.2 scope is NOT "refactor frozen dict to compose at boot" (already done) but "**REMOVE the entire archetype layer; pure BC-target-driven composition from unified substrate-AGNOSTIC mechanic pool**." Sharper starting point for W0.2 math-before-code.

**Other findings:**
- LC-002 VERIFIED — 2× fire sampling weight + ELEMENT_AFFINITY cascade; ablation per Discipline #13b still needed (W0.7 territory)
- LC-006 SUBSTANTIALLY-RESOLVED — rocket-owned outstanding action: add `_build_prompt()` test coverage to `tests/test_no_canonical_four_in_llm_prompts.py`
- LC-007 VERIFIED (deferred P4)
- LC-008 NEEDS-DOWNSTREAM-FIX — star-lord seam (`naming.py:323`)
- LC-012 RESOLVED (W0.3)

**W1.13 current-state:** infrastructure FULLY ABSENT from `b6_kit_builder.py`, `class_generator.py`, `b6_archetype_templates.py`. W1.13 requires building new infrastructure on both seams (rocket generation + star-lord archive_entries table). Purely additive.

**Alt A OQ verification:**
- **OQ-2 (chain_lightning boss multi-hop):** sim gives FULL geometric-series credit (~2.76× multiplier all hitting boss in solo-sim). Over-estimates relative to multi-target environment under W0.9 spatial migration. Flag for W0.9.6 calibration sweep.
- **OQ-3 (5-skill kit anomaly):** NOT REPRODUCIBLE from current code. Kit_min=10/12 hardcoded. Alt A observation likely from legacy state or test fixture.

**Cross-seam drift surfaced:** D3 added 11 new archetype tags (lightning/holy/shadow variants); no MIGRATION.md was filed. Knight-rider awareness item.

State-of-hive § 2.2.3 captures the canonical record of W0.4 rocket portion findings for downstream consumption. W0.4 PARTIAL: star-lord ✅ + rocket ✅ complete; gamora portion deferred (likely folded into W0.7 ablations since most gamora LCs are empirical/ablation-bound: LC-003 already verified by star-lord; LC-005 PackProxy being retired in W0.9 Phase 2.1; LC-009/010/011 ablation territory).

---

## 2026-05-21 — QD-rebuild P0 W0.9 Phase 2 kickoff dependencies COMPLETE; Phase 2.1 implementation IN-FLIGHT

**Event:** Both W0.9 Phase 2 kickoff dependencies returned successfully + Phase 2.1 implementation fired.

**A8 (gandalf) — Magic/elite/mini-boss arena scenario definitions** complete (collab commit `6b1134e`). Deliverable at `canonical/story/gauntlet-arena-scenarios-magic-elite-miniboss-2026-05-21.md`. 3 new arena scenarios:
- SCENARIO_MAGIC_PACK (32.7×14m; 1 magic + 3 swarm; 120s kills-only; WR 0.55-0.70)
- SCENARIO_ELITE_PACK (28×28m; 1 elite + 2 magic; 180s kills-only; WR 0.45-0.60)
- SCENARIO_MINI_BOSS (30×30m; 1 mini-boss + 2 elite; 150s soft/240s hard; WR 0.35-0.55)
- Boss tier: existing SCENARIO_BOSS_WITH_ADDS — no new scenario needed.
- Substrate-AGNOSTIC § 7 commitment explicit.
- § 9 gamora implementation handoff: 7 concrete arena.py changes.

**A5 (star-lord) — Schema v2.14 migration spec** complete (engine tag `star-lord/v1.16-w0-9-schema-v2-14-spec`; commits `dd5fa42` + `8a41a57`). MIGRATION.md authored (570 lines). 4 amendments to gamora §6.7 first draft:
- NEW `fight_events` table (not ALTER on existing); per-event fan-out linked via `class_fight_loadout_id`
- `mitigation_source TEXT` (mechanism label) vs gamora's `mitigation_applied` (which implied float magnitude)
- `event_type TEXT` collapsed (was event_direction split)
- Resource events unified under same `event_type` column
- LC-003 fields placement: `floor_lock_recompose` on `class_balance_results`; `working_modifier` + `floor_lock_detected` on NEW `recompose_attempts` table
- Storage flag: ~430 MB/season at full emission; `fight_events_sample_rate` parameter (default 0.0 = off) recommended
- 2 round-trip smoke fixtures specified per R11(b) discipline

**W0.9 Phase 2.1 implementation IN-FLIGHT** (gamora; agentId `a246a66bda7e52889`). Scope: W0.9.1 (PackProxy ×8 retirement from swarm-tier convergence) + W0.9.2 (R2 spatial sub-gauntlet promotion to default for all 5 tiers; 3 new arena scenarios per A8 § 9 handoff). W0.9.3/4/5/6 fire in subsequent Phase 2 sub-sessions.

Cross-seam dependency from A8: encounter_kind enum needs "magic" value added (`spatial-data-jsonschema.md:275`). Folded into Phase 2.1 dispatch instructions for gamora-star-lord coordination.

---

## 2026-05-21 — QD-rebuild P0 W0.3 COMPLETE: Foundation validator update (D5 = 7-substrate; LC-012 drift closed)

**Event:** W0.3 (rocket; trivial-actionable workstream) completed and merged. Engine commit `3e428ae`; tag `qd-rebuild/v0.3-foundation-validator-7-substrate` pushed.

**Change:** `foundation/foundation.py:39-65` updated from 4-rotating+1-physical hardcoded check to `CANONICAL_SUBSTRATES = frozenset({fire, water, earth, wind, lightning, holy, shadow})` membership check. Rotating elements must be in canonical-7 set; at most 1 non-rotating element; if non-rotating present must be named `physical`. Count of rotating elements no longer enforced (1-7 valid).

**Test results:**
- Foundation suite: 70/70 PASS (incl. 2 new validator acceptance tests: `test_validator_accepts_7_substrate_elements` + `test_validator_rejects_non_canonical_substrate`)
- Core generation: 382/382 PASS
- Full suite: 3092 collected; 2 pre-existing failures unchanged before/after (`test_all_elements_monsters` bruiser archetype gap; `test_geared_player_deals_more_damage` gear cp3 balance assertion)

**Cross-seam impact:** None. Validator is generation-internal gating; no MIGRATION.md required.

**Architectural note:** Per substrate-as-cohesion-only § 5.2, full substrate-AGNOSTIC validator refactor is deferred to P5 W5.X cohesion-BC work. This W0.3 closes LC-012 drift at the count-level; preserves physical-as-non-rotating pattern for backward compatibility.

State-of-hive § 1 W0.3 row updated to COMPLETE. **Fifth P0 workstream milestone complete** (W0.3 + W0.5 + W0.6 + W0.8 + W0.4 star-lord portion). W0.9 at Phase 1+1.5 milestone (Phase 2 implementation pending A8 + A5 kickoff dependencies). 4 P0 workstreams remaining (W0.1 + W0.2 + W0.4 rocket/gamora portions + W0.7).

---

## 2026-05-21 — QD-rebuild P0 W0.9 Phase 1 + Phase 1.5 COMPLETE: math-before-code locked

**Event:** W0.9 (gauntlet architecture migration) Phase 1 (math-before-code) + Phase 1.5 (amendment fold-in) workstreams complete. Tag `qd-rebuild/v0.9-math-note-phase-1-complete` fired (engine commit `edcac29`); collab commit `1a1b3d7` (dispatch completion record).

**Math note canonical version** at `reincarnated-engine/src/reincarnated/simulation/math/gauntlet-migration-arena-equivalence.md`. 7 unique amendments folded from jack-ryan Gate-1 (3) + gandalf architectural review (5; with 1 overlap):

1. §6.6 NEW — LC-003 cross-seam schema gap acknowledgment + round-trip smoke fixture spec (jack-ryan A1; REQUIRED)
2. §6.1 — SPATIAL_DAMAGE_SCALE Discipline #17 calibration parameter anchoring + re-calibration trigger condition (jack-ryan A2 + gandalf A6 combined)
3. §3.4 — tick-rate stability verification criterion (±0.05 WR delta threshold per tier; jack-ryan A3)
4. §6.4 — P7 W7.2 archive-query clarification (gandalf A4)
5. §6.7 NEW — W0.9.5 telemetry coverage for all 8 BC axes (gandalf A5; most consequential)
6. §5.4 — swarm convergence weight 0.0→1.0 Discipline #12 semantic-shift annotation (gandalf A7)
7. §6.3 — magic/elite/mini-boss scenario gate phrasing (gandalf A8)

**Phase 2 kickoff dependencies surfaced by Phase 1.5 completion:**
- **Gandalf A8 follow-on:** magic/elite/mini-boss arena dimensions + composition + win conditions are gandalf-territory design decisions. Phase 2 W0.9.2 (all-5-tier promotion) cannot complete without these. Knight-rider routes gandalf dispatch.
- **Star-lord A5 follow-on:** §6.7 8-axis BC event spec needs star-lord review before W0.9.5 instrumentation begins. Schema v2.14 migration includes LC-003 fields + 8-axis BC fields. Knight-rider routes star-lord dispatch (pre-Phase 2 schema agreement).
- **LC-003 round-trip smoke fixture (gamora-owned):** gamora authors + runs smoke; star-lord confirms recorder mapping once schema proposal surfaces.

**Gandalf closing assessment of Phase 1 work:** *"Cleanest piece of math-before-code work I've seen out of this seam."* Architectural commitment holds; recommend Gate-1 pass on architectural-alignment lane pending amendments (now folded).

State-of-hive § 1 W0.9 row updated. Phase 2 implementation fires when A8 + A5 dispatches return.

---

## 2026-05-21 — QD-rebuild P0 W0.6 FULL CLOSURE: drift candidate dispositions complete (LC-006 + LC-007 + LC-014 + LC-028)

**Event:** W0.6 drift candidate closures workstream completes with full closure (supersedes earlier `qd-rebuild/v0.6-drift-closures-partial`). Tag `qd-rebuild/v0.6-drift-closures-complete` fired (engine commit `2b1b9a6`). Per-LC final dispositions:

- **LC-006 canonical-four LLM exposure — FULL CLOSURE.** RESOLVED at LLM-prompt-construction layer (W0.4 star-lord verified: cipher migration live in `llm/naming.py`; test guard at `tests/test_no_canonical_four_in_llm_prompts.py`). D3 cohesion-judge layer architecturally clean by design (gandalf disposition 2026-05-21 — Option B with Option-C label-emission sliver). **No second cipher migration required at cohesion-judge layer.** Implementation contract for P5 cohesion-judge prompt design: mechanical signature + thematic-grammar reference + canonical-7 label-set as emission vocabulary (NOT candidate labels). Critical test guard: prompt must NOT inject canonical-seven as "candidate labels to choose from."
- **LC-007 humanoid gear schema — FORMAL-DEFER** to P4 W4.1 (sim extensions enable non-humanoid) + Stage 1 form-bias migration (separately scoped per cadence strategy).
- **LC-014 D1 element-name pool humanoid-fantasy selection bias — FORMAL-DEFER** to catalogue-track sub-locks per decisions-log 2026-05-16. Q4 syllable-cap gate amendment is partial implicit mitigation; BC measurement risk LOW; deferral does not block QD archive filling.
- **LC-028 single-word rule — REVISE-CANONICAL-DOC (knight-rider action item COMPLETE).** Decisions-log entry 2026-05-21 scopes rule to D1 + L2 layers only; L3 cipher-generated per-season vocabulary explicitly NOT constrained. Pre-cipher-migration-dispatch requirement satisfied.

**Architectural insight (gandalf disposition for LC-006):** the cohesion-judge runs BACKWARD (kit-already-exists → name-it). The bias-removal job is structurally satisfied because the mechanical kit is locked before the judge looks. The judge IS allowed to know the canonical-7 label-set exists — that's its output vocabulary, not an inference-shaping input. The grouping-layer cipher (canonical-7 v1.2) exists for FORWARD generation to hide substrate during inference. For BACKWARD judgment, the architecture dissolves the concern.

**Engineering disciplines anchored:** Discipline #13 (implicit-pillar drift) — the alternative framing "find the kit's archetype slot from a known set" would have recreated archetype-lock-in pathology one phase later; the architectural test guard prevents this.

State-of-hive § 1 W0.6 row updated to FULL CLOSURE. **Fourth P0 workstone milestone complete** (W0.5 + W0.6 + W0.8 + W0.4 star-lord portion). 5 remaining.

---

## 2026-05-21 — QD-rebuild P0 W0.4 star-lord portion COMPLETE: telemetry/export-side LC verification + critical cross-seam gap surfaced

**Event:** Per multi-seam W0.4 dispatch, star-lord completed the telemetry/export seam portion. Engine tag `star-lord/v1.15-w0-4-code-side-audit-1` fired (pushed). Deliverables: `agentic_orchestration/star-lord/research/qd-rebuild-w0-4-star-lord-code-side-audit.md` + shared `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/phase-2-code-side-verification.md` (star-lord section).

**Critical finding — LC-003 DRIFT-FROM-AUDIT (cross-seam gap):** `floor_lock_recompose`, `working_modifier`, `floor_lock_detected` fields specced in gamora's `simulation/MIGRATION.md` (Option B floor-lock recovery) but **ABSENT from star-lord's `migrations.py` + `recorder.py`**. Currently dormant because Option B is soft-disabled — but if Option B is re-enabled, telemetry will silently drop these fields. **Disposition:** fold into W0.9 schema v2.14 migration scope (W0.9 already plans v2.13 → v2.14 bump for true-multi-monster sim telemetry). Cross-referenced for gamora W0.9 math-before-code + jack-ryan Gate-1 review.

**Per-LC verdicts (star-lord seam):**
- LC-006 (canonical-four LLM exposure): **RESOLVED**. Cipher migration live in `llm/naming.py`; test guard at `tests/test_no_canonical_four_in_llm_prompts.py`. (Rocket sites pending rocket W0.4 portion verification.)
- LC-007 (humanoid gear schema in export): **VERIFIED (not yet fixed)**. `export/schemas.py:88-89` carries `slot/handedness`. Position C migration not shipped.
- LC-003 (modifier floor-lock): **DRIFT-FROM-AUDIT** (see above; critical cross-seam gap)
- LC-008 (STR/DEX/INT LLM visibility): **NEEDS-DOWNSTREAM-FIX**. `naming.py:323` passes raw stats to LLM prompt.

**W1.13 ArchiveEntry schema (for P1):** all 7 fields require NEW `archive_entries` table (not ALTER). Export schema change not needed until P3. Star-lord owns the migration.

**W0.8 schema fields (for P1 W1.1):** `bounce_count` + `spawn_count` is clean additive ALTER. ~20 LOC across 4 files; no round-trip breakage risk (Pattern P7 defensive getattr).

**Schema v2.12 + v2.13:** LIVE; no drift. **No new HIGH-risk LCs** (no § 7.4 phase-halt trigger).

State-of-hive § 2.2.2 added — canonical record of star-lord findings for downstream consumption. W0.4 partial complete (star-lord done; rocket + gamora portions pending).

---

## 2026-05-21 — QD-rebuild P0 W0.5 COMPLETE: Mana-bug verify LC-026 — RESOLVED

**Event:** Per W0.5 dispatch `agentic_orchestration/dispatches/2026-05-21-gamora-w0-5-mana-bug-verify.md`, gamora completed empirical inspection of LC-026 mana-bug. **Verdict: RESOLVED.** No follow-on fix workstream required. Engine commit `4bce461`; LC-026 addendum at `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/lc-026-mana-bug-verify-addendum-2026-05-21.md`.

**Tag fired:** `qd-rebuild/v0.5-mana-bug-verify-resolved` (engine + pushed to origin).

**Key findings:**

- **Phase 1 dimensional refactor (engine commit `4c28ed6`, 2026-05-08) structurally resolved at both layers:**
  - Pool assignment (`combatant.py:362-366`): `_ENERGY_CONFIGS` branches before stat computation — rage gets pool=100/start=0/regen=0; combo gets pool=5/start=0; focus gets pool=100/start=full/regen=-5/s; stamina-as-resource gets pool=150/start=full/regen=+20/s. The int/wis values no longer influence pool size for non-mana classes.
  - Skill costing (`ability_grammar.py:341-364`): `_get_energy_cost()` routes by energy_type — rage skills cost 25-50, combo primaries cost 0/spenders cost 3, all within respective pool maximums.
- **Test surface validates:** 54/54 test_energy_types.py PASS + 75 passed test_balance_loop.py + test_class_generation.py + 23 passed test_combat_simulator.py = 152 tests PASS. No regressions.
- **Architectural compatibility confirmed:** substrate and energy_type are orthogonal axes — no coupling. Axis 5 (resource economy) BC profiling can read `energy_type` from class schema as the correct structural signal — fully compatible with substrate-as-cohesion-only architecture.

**Residual finding (documentation gap, NOT a fight-engine defect):**
- `base_stamina` column in telemetry `classes` table is never written by `recorder.py`. Flagged for star-lord (whose W0.4 portion is currently in-flight; will fold this into the cross-seam audit).

**Downstream implication:** QD-rebuild P1 substrate work can proceed with mana pipeline structurally sound. No P1 W1.X resource-economy substrate creation work is blocked.

State-of-hive § 1 W0.5 row updated to COMPLETE. Second P0 workstream complete; 7 remaining (W0.3 + W0.4 star-lord portion in-flight; W0.1 + W0.2 + W0.4 rocket/gamora portions + W0.6 + W0.7 + W0.9 queued).

---

## 2026-05-21 — QD-rebuild P0 W0.8 COMPLETE: Axis 2 (damage geometry) substrate completeness check

**Event:** Per W0.8 dispatch `agentic_orchestration/dispatches/2026-05-21-rocket-w0-8-axis-2-substrate-check.md`, rocket completed the Axis 2 substrate completeness analytical workstream. Deliverable filed at `agentic_orchestration/rocket/research/qd-rebuild-w0-8-axis-2-substrate-check.md` (44KB; collab commit `d7544bf`).

**Tag fired:** `qd-rebuild/v0.8-axis-2-substrate-check` (pushed to origin).

**Key findings:**
- **Aggregate gap quantified:** ~58-64 distinguishable templates across all 5 Axis 2 bins vs ~125 target (49-52% coverage at the 5× rule).
- **Per-bin priorities:** chain HIGH (~21-22 gap); multi-spawn HIGH (~19-20 gap); single-target MEDIUM (~13 gap); large-AOE MEDIUM (~5-7 gap); small-AOE LOW (~3-5 gap).
- **24 enrichment seed candidates authored** for HIGH-priority bins (12 chain C-1..C-12 + 12 multi-spawn M-1..M-12). All substrate-AGNOSTIC.
- **OQ-7 water DPS density (Track C surface)** dispositioned: M-3 + M-8 + C-4 recommended for water cohesion access.
- **NEW schema-field recommendations for P1 W1.1:** `bounce_count` + `spawn_count` (without these, bounce-count and spawn-count distinguishability cannot be measured at BC-assignment time).
- **Total geometry inventory:** 28 VALID_GEOMETRIES (engine code authoritative); 23 damage-bearing.

**Downstream consumers folded:**
- P1 W1.1 (Ability schema extensions): NEW `bounce_count` + `spawn_count` fields
- P1 W1.5 (movement-skill expansion): chain + multi-spawn seed candidates
- P1 W1.7 (legolas Phase 2 depth pass): full enrichment-seed-list as scope input
- P1 W1.11 (substrate-themed cohesion access): OQ-7 water DPS density resolution + M-3/M-8/C-4 in pool

State-of-hive § 2.2.1 captures the canonical record of W0.8 findings for downstream consumption. First P0 workstream completion; 8 remaining (W0.3 + W0.5 in-flight; W0.1 + W0.2 + W0.4 + W0.6 + W0.7 + W0.9 queued).

---

## 2026-05-21 — QD-ENGINE REBUILD HIVE ACTIVATED: continuous single-hive multi-phase rebuild (P0-P7; 24-37 weeks)

**Event:** Per gandalf activation dispatch `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md`, the QD-engine rebuild hive activates under knight-rider's autonomous orchestration. This is the longest road the project has walked — multi-month continuous single-hive operating mode through phases P0 (constraint removal) → P7 (validation + production cutover for Profile A).

**Architectural foundation (canonical stack now etched + committed):**
- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — vision (QD-engine + 4 profiles + IDC meta-principle)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — operational spec (8 BC axes × 68,040 cells)
- `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate-as-cohesion-only architectural recommitment (substrate identity coalesces post-generation; mechanical generation is substrate-agnostic and BC-target-driven)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` — 8-phase workflow with Profile A/B/C/D touchpoints
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — phased rebuild plan

**Audit deliverables synthesized into rebuild plan:**
- `agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-20/phase-1-reconnaissance/` (substrate gaps; Mixamo TOS; procurement shortlist; vision-layer geometry gaps)
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` (62 constraints; 12 HIGH-risk)
- `agentic_orchestration/rocket/research/substrate-generalization-study-2026-05-21/` (Alt A; Pattern-A generalizes universally)

**Matt-resolved decisions (delegated to gandalf 2026-05-21):**
- **D1** Unity render pipeline: URP
- **D2** Phase 0 element scope: 7 elements (fire / water / earth / wind / lightning / holy / shadow)
- **D3** Cohesion-BC sequenced post-cipher migration
- **D4** BC Axis 2 measurement: all fights, fight-context-tagged
- **D5** Foundation validator: 7-substrate
- **D6** Vision-layer geometry gaps documented for v1.1; do not block P0

**Post-protocol architectural refinements (substrate-as-cohesion-only recommitment 2026-05-21):**
- Substrate identity is a pure cohesion-layer concern; mechanical generation is substrate-agnostic and BC-target-driven
- Shadow = trade-off thematic identity (cohesion theme; ARPG + cultural + isekai canon grounding)
- Physical = warcry/shout exception (cohesion theme; D2/D3/D4 Barbarian canonical)
- Holy = aura self-amplification primary (cohesion theme; D2 Paladin / D3 Crusader / PoE Guardian canonical)
- Kit-redesign queue CANCELED (philosophical contradiction with QD-engine paradigm); 12-archetype list preserved as P7 W7.2 archive-query reference roster
- **NEW separate repo `~/Games/reincarnated-game/`** — Unity production (drax-owned PARALLEL initiative; multi-month scope; Meshy 6 pipeline; URP); ships independently of QD-rebuild
- Dual-render Profile A: Pixi.js 2D (existing demo) + Unity 3D (reincarnated-game); missing sprites acceptable
- VFX procurement deferred to P6-equivalent in reincarnated-game initiative (NOT QD-rebuild scope)
- W1.8/W1.9/W1.10 REMOVED from QD-rebuild P1 (moved to reincarnated-game initiative)
- **NEW P1 W1.13** — skill tree node population (procedural per-class-per-season ~120-node trees; multi-dim convergence over node-subset × per-node-coefficients × scalar modifier; resolves Pattern-A compression mathematically per § 2.8 of activation dispatch)
- **NEW P0 W0.9** — gauntlet architecture migration (retire PackProxy ×8; true multi-monster positional gauntlet as default convergence path; P7 W7.2 certification is archive QUERY not re-execution; per § 2.9 of activation dispatch)

**Decision authority during hive (per activation dispatch § 5):** knight-rider operates autonomously, surfacing to Matt only for: structural architecture changes / procurement >$100 cumulative / production cutover (W7.5) / Discipline #18 ratification (P5 W5.6) / Profile A ship-blocker / axis-lock v1.1+ revision / W0.9 + W1.13 framing approval (new scope from protocol v1.1).

**Knight-rider opening sequence (per activation dispatch § 4):**
1. Close recompose-hive trigger #3 (P5 canonical record commit; engineering-disciplines.md #11 elaboration; star-lord "33" → "35" corrective; final tag `recompose-hive/v1.1-canonical-record-complete`; retrospective doc) — **EXECUTED THIS SESSION**
2. Draft decisions-log entries for D1-D6 + QD-rebuild hive activation + Discipline #11 elaboration ratification + Discipline #18 candidate registration + § 2.8 W1.13 commitment + § 2.9 W0.9 commitment — **EXECUTED THIS SESSION**
3. Acknowledge Track C in-flight (gandalf synthesizes verdict when it returns; fold synthesis into P1 W1.11 scope-finalization) — **ACKNOWLEDGED**
4. Open QD-rebuild P0 with workstream sequence W0.1 + W0.5 + W0.8 front-loaders; W0.2 + W0.4 substantial; W0.3 + W0.6 + W0.7 + W0.9 in parallel
5. Tag `v0.0-constraint-removal-shipped` at P0 completion
6. Open P1 with W1.13 (new scope; Matt approval required for framing before fires)
7. Continuous execution through P7

**Background dispatches in flight:**
- Track C resumption (TC-1 water resume + TC-2 earth; SKIP TC-3 shadow per shadow trade-off framing) — running when activation dispatched; verdict feeds P1 W1.11 substrate enrichment scope; does NOT block P0 fire
- Monster thematic depth assessment (Legolas + Galadriel + gandalf synthesis) — QUEUED to fire post-P0 open

**Tag namespace:** `qd-rebuild/v<X.Y>-<descriptor>` (intermediate); `v<X.0>-<phase-name>-shipped` (Matt-approved milestone); `v8.0-qd-engine-final` (production cutover).

**Hive-state hygiene:** state-of-hive doc at `agentic_orchestration/knight-rider/state-of-hive-qd-rebuild.md`; phase-progress logs at `agentic_orchestration/knight-rider/daily/<YYYY-MM-DD>.md`; skill_handoff docs per Matt session-open.

---

## 2026-05-21 — RECOMPOSE-VALIDATION HIVE CANONICAL RECORD CLOSED: trigger #3 P5 completion at full scope

**Event:** Per gandalf QD-rebuild activation dispatch § 4 Step 1 and Matt's blended-path-A acceptance, the recompose-validation hive's canonical record is committed at FULL P5 scope (Matt response category A from Matt briefing § 7). This supersedes the 2026-05-20 lightweight close.

**Full P5 deliverables completed at this entry:**
- ✅ Single Discipline #11 elaboration applied to `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (§ 11.1 state-space conditioning of empirical signals — ratified per gandalf P3 § 9.6 P5-ready language)
- ✅ Retrospective doc filed at `agentic_orchestration/hive-mind/retrospective-recompose-validation.md`
- ✅ Engine-side star-lord analysis count corrective applied (33 → 35; `output/p2-fresh-diagnostic-regen-2026-05-19/p2-classification-and-floor-lock-analysis.md`; per jack-ryan Gate-2 Amendment 1 out-of-collab-scope)
- ✅ Final tag `recompose-hive/v1.1-canonical-record-complete` fires on this commit (engine + collab parity)

**Continuity to QD-rebuild:** the recompose-hive's findings (empirical kit-composition pathology + Discipline #11.1 elaboration + "fix the arena, not the synergy" governance principle) anchor multiple downstream QD-rebuild workstreams. Specifically: substrate-as-cohesion-only architecture (resolves kit-composition pathology architecturally); Discipline #17 calibration sweeps (carry equilibrium-state conditioning forward); P0 W0.9 gauntlet architecture migration (retire PackProxy ×8 per the "fix the arena" principle). See retrospective § 6 for full continuity map.

**Hive state at full close:**
- Engine code state: Option A active (`MODIFIER_SEARCH_FLOOR = 0.01`); Option B installed + soft-disabled (`LEVER_FLOOR_LOCK_WORKING_MODIFIER = MODIFIER_SEARCH_FLOOR`); 179/179 tests PASS; schema v2.13 telemetry live; no rollback executed
- Documentation state: canonical findings v0.4.1 amended (collab) + retrospective (collab) + Discipline #11.1 (engine) + decisions-log entries (engine; new entry filed at this Step 2) + engine-side analysis count corrective applied
- All hive milestone tags resolved: v0.0 + v0.1 + v0.3 + v0.4 FIRED; v1.1 FIRES at this commit; v0.2 HELD PERMANENTLY

**Hive close is final. Future references to recompose-hive findings cite the canonical artifact inventory in the retrospective doc § 5.**

---

## 2026-05-20 — RECOMPOSE-VALIDATION HIVE DEACTIVATED: Matt explicit wind-down (Trigger 1) signaled post-Trigger 3

**Event:** Matt explicit wind-down signal received (verbatim: *"please commit/push and wind down"*). Trigger 1 per protocol § 7 signaled at this entry, completing the recompose-validation hive's deactivation cycle (Trigger 3 fired at verdict-handoff; Trigger 1 fires at Matt's explicit wind-down acceptance).

**Hive deactivation deliverables verified at this CHANGELOG entry:**
- All canonical findings + amendments committed + pushed (collab `9b425db` v0.4.1 amended state)
- Matt briefing finalized + pushed (collab `e7b4a65` with gandalf Amendment 2 disaggregation language folded)
- Engine decisions-log entries P0 + P1 + P3 all filed (engine `a58b60f` + `22b1c3c` + `c5332cd`)
- Hive log final knight-rider STATE + this CHANGELOG closing entry committed (collab; this commit)
- All hive milestone tags fired at this close: v0.0-pre-activation + v0.1-option-a-floor-widened + v0.3-diagnostic-regen-complete + v0.4-validation-verdict
- v0.2-option-b-recompose-conditioned HELD PERMANENTLY per current evidence

**P5 disposition under Matt's wind-down framing (lightweight; NOT full § 7 (A)):**

Matt's directive was minimal ("commit/push and wind down") — not directing full P5 (engineering-disciplines.md amendment + retrospective doc + hive-runs review v5 update + tag `recompose-hive/v1.1-canonical-record-complete`). The verdict-handoff cycle's substantive deliverables (canonical findings doc + Matt briefing + decisions-log entries + CHANGELOG entries + hive log + state-of-hive docs) already constitute the de-facto P5 canonical record at lightweight close.

**Deferred to future Matt-direction:**
- Single Discipline #11 elaboration applied to `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (proposed language in canonical findings doc § 9.6 P5-ready)
- Retrospective doc at `agentic_orchestration/hive-mind/retrospective-recompose-validation.md`
- Hive-runs review v5 update (gandalf research; fold this hive's findings)
- Engine-side star-lord analysis count corrective (33 → 35; per jack-ryan Gate-2 Amendment 1 out-of-collab-scope)
- Tag `recompose-hive/v1.1-canonical-record-complete` (would fire on full P5 completion)

**Knight-rider next-session continuity:** `agentic_orchestration/skill_handoff_2026-05-20.md` filed at this commit. If Matt later directs full P5 closure OR an alternative architectural direction (kit-redesign queue / substrate-generalization study / etc.), knight-rider's next session picks up from the skill_handoff context.

**Engine state preserved at deactivation:**
- Option A active; Option B installed + soft-disabled (one-line re-enable cost if future verification directs)
- 179/179 tests PASS at engine HEAD
- Schema v2.13 telemetry active
- No rollback executed; ready for next-step architectural direction

**Hive cumulative metrics:**
- ~4h 45min wall-clock total (activation 2026-05-19 22:28 EDT → final wind-down 2026-05-20)
- ~2x faster than 4-7d parallelized estimate
- 11+ subagent invocations; 12+ knight-rider orchestration cycles
- 2 FRICTION events dispositioned cleanly within hive scope
- 4 hive milestone tags fired + 1 held permanently
- 3 canonical findings produced (empirical + methodological + per-failure-mode)
- 3 governance principles surfaced + codified
- 0 Matt-trigger escalations during autonomous-operation phase (clean autonomous run)

**Recommended next-step architectural decisions REMAIN ON RECORD for future Matt direction** (per Matt briefing § 5):
- Primary: kit-redesign queue execution (R1 + per-failure-mode disaggregation)
- Alt A: substrate-generalization study (~hours; cheapest epistemic insurance)
- Alt B: disposition-3 sensitivity check (~hours)
- Alt C: targeted single-class kit-redesign pilot (~2-3 weeks)

**Hive DEACTIVATED.** No further knight-rider orchestration cycles for this hive's scope. The road forward awaits Matt's next direction at whatever cadence.

---

## 2026-05-20 — RECOMPOSE-VALIDATION HIVE WIND-DOWN TRIGGER #3 SIGNALED: P3 verdict CANNOT REJECT NULL; hive autonomous-operation phase ENDS

**Event:** The recompose-validation hive (third hive activation; six-phase mission) reached its P3 validation synthesis verdict: **CANNOT REJECT NULL**. Hypothesis H_RC ("per-tier convergence is satisfiable for existing generation rules if recompose can fire") is **not supported** by season_100005 evidence (observed 0% kit-acceptable at worst-case bound; 100% Pattern-A boss-DPS-floor structural; 0/10 floor-lock-recovery candidates). H_RC_0 (null: generation rules require revision) is **reinforced**. Wind-down trigger #3 signals per protocol § 7; **P4 (ship true season) does NOT fire autonomously**. Hive autonomous-operation phase ENDS pending Matt direction. Matt briefing filed at `agentic_orchestration/matt-briefing-recompose-validation-2026-05-20.md`.

**Hive cycle pace:** ~4 hours wall-clock total from activation (2026-05-19 22:28 EDT) through verdict-handoff (2026-05-20). ~2x faster than the 4-7 day parallelized estimate. 11 subagent invocations + orchestration cycles. Two FRICTION events surfaced + dispositioned within hive scope (P1 smoke-B1 test-class-selection + P2 Phase 1-vs-Phase-2 signal reversal); both resolved cleanly under autonomous-operation framework as designed.

**Six-phase outcome summary:**
- **P0** Option A floor widening: SHIPPED 2026-05-19 (engine `a58b60f`; tag `recompose-hive/v0.1-option-a-floor-widened`). Mechanism verified; prior floor-lock failure mode eliminated.
- **P1** Option B recompose-trigger conditioning: MECHANICALLY COMPLETE / BEHAVIORALLY SOFT-DISABLED 2026-05-19 (engine `554e310`; tag `gamora/v1.14-balance-loop-option-b-recompose-conditioned-soft-disable` with load-bearing qualifier; hive milestone `recompose-hive/v0.2-option-b-recompose-conditioned` HELD permanently per current evidence). Mechanism verified mechanically; preserved as sleeping safety net.
- **P2** Fresh diagnostic regen: ACCEPTED 2026-05-20 (tag `recompose-hive/v0.3-diagnostic-regen-complete`). Rocket Phase 1 (engine `07d13f8`) + gamora Phase 2 (engine `6cb7fa4`) + star-lord Phase 3 (engine `46d850c`).
- **P3** Validation synthesis: VERDICT CANNOT REJECT NULL 2026-05-20 (gandalf canonical findings collab `3205d0e` + amendments; jack-ryan Gate-2 collab `fe3a2c1`; tag `recompose-hive/v0.4-validation-verdict`).
- **P4** Ship true season: **HELD** — does not fire on CANNOT REJECT NULL per protocol § 7.
- **P5** Canonical record: subsumed into this CHANGELOG entry + Matt briefing + decisions-log entry + canonical findings doc; if Matt directs hive closure at P5, deliverables get folded (engineering-disciplines.md amendment for single Discipline #11 elaboration; hive-runs review update; retrospective doc).

**Three canonical findings produced:**

1. **Empirical (cleanest possible diagnosis per protocol § 11):** 100% Pattern-A at full-season scope on shadow substrate. Catalogue kit-composition pathology IS the load-bearing problem. Triangulation: R1 (38/51 broken kits) + R2+ST counterfactual joint synthesis Row 5 ("catalogue has deeper pathology") + this hive's P2 evidence all converge.

2. **Methodological (single Discipline #11 elaboration candidate; queued for P5):** *Pipeline-state-conditioned signals are NOT equivalent to equilibrium-state-conditioned canonical convergence signals.* Two independent hive events surfaced this pattern within ~24 hours (P1 smoke-design warm-start-signature error + P2 generation-time-vs-cold-start signal reversal); shared root cause is state-space conflation. Gandalf's proposed elaboration language drafted in canonical findings § 9.6 for P5 co-authoring.

3. **Per-failure-mode disaggregation (kit-redesign queue handoff input; from jack-ryan Gate-2 Amendment 2):** sub-pattern 2 boss-DPS-floor = 10/10 universal; sub-pattern 5 recompose-couldn't-recover = 9/9 canonical (disaggregated into 8 compression-only [classes 0002-0009] + 1 lever-signal-gap [class_0001 modifier_fallback path; deeper kit-architecture revision need]); sub-pattern 6 generation-rule-pathology = 10/10 universal; sub-pattern 4 floor-lock-still-active = 0/10 explicitly NOT implicated. class_0009 shadow_controller carries additional controller-mechanic mismatch sub-pattern (elite over-shoot + boss=0). Prevents one-size-fits-all kit-redesign assumptions.

**Three governance principles surfaced + codified during the hive:**

1. **A BLOCKING smoke gate exists to falsify the design diagnosis, not the mechanism.** These are different failure modes that demand different dispositions. Authored at P1 re-disposition (gandalf brief v1.1 § 4.4 amendment); applied to disposition the smoke-B1-test-class-selection failure as soft-disable rather than full revert.
2. **Hive milestone tags do not fire on un-empirically-tested behavioral changes.** Tag-firing discipline as governance precedent. Applied to HOLD `recompose-hive/v0.2-option-b-recompose-conditioned` pending empirical verification on a real subject (which P2 + this hive's evidence empirically refuted at season scope).
3. **"When your test arena lacks the monster you designed your synergy against, you fix the arena, not the synergy."** Diablo II Iron Maiden / Returned-Damage lesson restated. Authored as load-bearing principle for soft-disable disposition; preserved 165 LOC of Gate-1-approved infrastructure rather than throwing away on a test-design miss.

**Recommended next-step architectural decision (FOR MATT'S CONSIDERATION; not committed):**
- **Primary:** kit-redesign queue execution (R1 38/51 queue + per-failure-mode disaggregation; ~4-6 weeks)
- **Alternative A (knight-rider's framing favorite for epistemic insurance):** substrate-generalization study (regen on different substrate; ~hours) before committing to kit-redesign weeks
- **Alternative B:** disposition-3 sensitivity check (~hours)
- **Alternative C:** targeted single-class kit-redesign pilot (~2-3 weeks) before queue execution

**Hive state at deactivation:**
- Code: Option A active; Option B installed + soft-disabled; 179/179 tests PASS at engine HEAD
- Telemetry: schema v2.13 in force; diagnostic fields automatically record on future regens
- Documentation: canonical findings doc + Gate-1 + Gate-2 critiques + briefs + analyses + hive log + state-of-hive docs (Day 0 + Day 1) + MIGRATION.md v1.21 + v1.22 + Matt briefing + this CHANGELOG entry + engine decisions-log entry
- Tags: 4 hive milestones fired (v0.0, v0.1, v0.3, v0.4); 1 held (v0.2 — fires retrospectively only if future evidence + re-enable + smoke PASS); seam tags fired through full disposition arc
- Engine-side P5 corrective deferred (star-lord analysis "33" carry-over of pre-amendment count; per jack-ryan Gate-2 § 5 Amendment 1 out-of-collab-scope note; included in Matt briefing § 7 (A) execution items if Matt directs P5 closure)

**Adjacent canonical work running in parallel (informational; not in hive scope):** Matt's QD-engine + profile architecture vision; gandalf's QD-engine BC axes work; legolas dispatch v3; jack-ryan QD-rebuild legacy constraint audit. These continue independently of trigger #3.

**Hive trigger watch at CHANGELOG entry close:** ⏰ Trigger 3 (CANNOT REJECT NULL verdict) SIGNALED. ⏸ Triggers 1, 2, 4 await Matt's response category per Matt briefing § 7 (accept wind-down + P5 / direct further investigation / direct alternative architectural path).

**The hive walked the road it was authored to walk.** The cleanest possible diagnosis has been delivered; the road forward is named; Matt's direction sets the next step.

---

## 2026-05-20 (early morning) — RECOMPOSE-VALIDATION HIVE P2 Phase 1: empirical signal REINFORCES hive central premise (6/10 floor_lock_recompose=True at generation-time)

**Event:** Rocket completed P2 Phase 1 (full-season fresh diagnostic regen; season_100005, substrate=shadow-first rotation, R8 inverted pipeline; engine `07d13f8`; tag `rocket/v1.22-p2-fresh-regen-shadow-100005`). The generation-time embedded balance-loop convergence run surfaced **a substantively positive empirical signal for the recompose-validation hive's central premise**: 6/10 classes (60%) show `floor_lock_recompose=True` — FAR ABOVE gandalf brief § 2.5's 3-8/season conservative estimate (3-8 classes per ~49-class season = 6-16% expected rate). Pre-Phase 2 canonical convergence, the structure of the masked-Pattern-B-extreme population is visible at full-season scope.

**Three-tier modifier structure at generation-time** (rocket diagnostic):
- **Tier 1 (normal, m\* ≥ 0.05; 3 classes / 30%):** class_0001 (shadow_mage 0.0719), class_0008 (physical_warrior 0.1956), class_0009 (shadow_controller 0.1338) — these are Pattern-B classes served by Option A alone
- **Tier 2 (EXTREME_LOW converged; 5 classes / 50%):** class_0003 (water_mage 0.0332), class_0005 (wind_caster 0.0255), class_0006 (lightning_mage 0.0139), class_0007 (holy_caster 0.0139), class_0010 (experimental 0.0255)
- **Tier 3 (EXTREME_LOW FAILED at floor; 2 classes / 20%):** class_0002 (fire_mage 0.0110), class_0004 (earth_caster 0.0110) — **these are the canonical floor-lock-recovery subjects** that Option B was designed to serve (true `m* < MODIFIER_SEARCH_FLOOR=0.01`; binary search bottomed out at floor)

**Implication for the three-way P2 disposition gate** (per dispatch § 5):
- ❌ **"Zero floor-lock candidates" path (wind-down trigger #3 at P3; premise refuted)** — RULED OUT. Clear evidence at 6/10 + 2 at-floor failures.
- ✅ **"Multiple floor-lock candidates" path (re-enable Option B + smoke B1 against confirmed subject + retroactive milestone tag fire)** — FIRING. On gamora Phase 2 canonical confirmation, knight-rider will route gamora for **Option B re-enable** (`LEVER_FLOOR_LOCK_WORKING_MODIFIER = 0.005` literal value, removing named-constant reference per docstring re-enable path); smoke B1 re-runs against class_0002 and/or class_0004 (the canonical at-floor candidates); on BLOCKING all-PASS, fire `recompose-hive/v0.2-option-b-recompose-conditioned` hive milestone tag retrospectively.

**Pattern A/B/B-extreme distribution observed in season_100005** (10 classes total):
- 3 Pattern-B classes converge above floor (Option A alone served)
- 5 EXTREME_LOW classes converge with floor_lock_recompose=True (Option B's served population under cold-start; would benefit from re-enable)
- 2 Pattern-B-extreme classes failed at floor (canonical Option B re-enable verification subjects)

This is consistent with gandalf's brief § 2.5 prediction structure, just at a different scale than the Phase B.2 conservative estimate suggested. The implication: **the masked-Pattern-B-extreme population is larger and more general than initially predicted**, which means Option B's mechanism is even more architecturally load-bearing than the brief framed it.

**P2 status:** Phase 1 ACCEPTED by knight-rider (Gate-2-read pass on rocket's HANDOFF). Phase 2 (gamora cold-start canonical convergence with full v2.12 + v2.13 telemetry) IN FLIGHT. On gamora Phase 2 completion, star-lord Phase 3 (classification + Pattern-A/B + canonical floor-lock candidate analysis) fires; on star-lord completion, knight-rider applies the three-way disposition gate + fires P2 acceptance tag `recompose-hive/v0.3-diagnostic-regen-complete`.

**Pre-existing anomalies surfaced during Phase 1 (non-blocking; pre-existing not generation defects):**
- [R3] skill_000246 + skill_000355 range_m=None — canonical library backfill pending (elrond seam; not this hive's scope)
- [D4] unknown archetype 'trial' in ai_strategies — known gap
- No canonical entry for (lightning/holy/shadow, role) — correct fallback behavior under R8 inversion
- Export pipeline: ExportMetadata.elements=null in inverted-mode manifest — engine-side artifacts intact; not a blocker for gamora Phase 2

**Hive trigger watch:** ⏸ all four still unsignaled. Trigger #3 (premise refuted) is now empirically RULED OUT at Phase 1 (would require zero floor-lock candidates; observed 6/10).

**Adjacent canonical work (informational; not in hive scope):** gandalf authored a follow-on commit on the QD-engine BC axes + Unity VFX directive amendment (collab `afeaa4c`). This is Matt's QD-engine vision (engine-architecture-vision-qd-profile doc) work; runs in parallel with the hive but doesn't affect routing.

---

## 2026-05-19 (night) — RECOMPOSE-VALIDATION HIVE P0 ACCEPTED: Option A floor widened; P1 (Option B design brief) routed to gandalf

**Event:** Gamora completed P0 in ~26 minutes (significantly faster than 4-hour estimate; pre-authored dispatch with all critique-pair amendments folded enabled verbatim execution). Knight-rider Gate-2-read disposition: ACCEPT with spirit-of-acceptance framing on the cold-start sub-0.05 demonstration (deferred to P2 fresh diagnostic regen per gamora's documented warm-start vs cold-start framing).

**P0 deliverables landed (engine commits `d5a20e0` + `75cfdc4` + `a58b60f`):**
- 4 floor sites in `balance_loop.py` updated to use `MODIFIER_SEARCH_FLOOR=0.01` + `MODIFIER_SEARCH_CEILING=4.0` named constants with full module-level docstring (Discipline #18 implicit-pillar resolved)
- `modifier_extreme_low` bool flag added to `ClassBalanceResult` + `balance_metadata` + `convergence_report` (designer-attention surface)
- Smoke A1 (floor-lock regression, BLOCKING): `FAILED → CONVERGED` for class_0001 season_100002. PASS.
- Smoke A2 (test-assertion audit, BLOCKING): 44/44 `test_balance_loop.py` PASS; literal-floor assert in `tests/test_range_profile.py:1033` updated to derive from named constant in same commit. PASS.
- Smoke A3 (telemetry-recorder range check): no modifier guard found in `recorder.py`/`spatial_recorder.py`. PASS. Star-lord no-action.
- Stop-gap regen of 3 diagnostic seasons (099002 brine / 100001 char / 100002 ember): convergence rate 100%/100%/100% (prior failure rates 60%/73%/80%, all resolved at warm-start).
- MIGRATION.md v1.21 entry filed with star-lord schema v2.12 obligations queued.
- Decisions-log entry filed (engine `a58b60f`) per dispatch § 7 + Gate-2-read amendments.

**Tags fired (knight-rider under standing ADR-006 amendment authority):**
- `gamora/v1.13-balance-loop-floor-widened-option-a` (engine seam tag)
- `recompose-hive/v0.1-option-a-floor-widened` (engine + collab hive milestone tag)

**Warm-start diagnostic note:** the stop-gap regen warm-starts classes from prior `final_modifier=0.0509`; at that modifier, aggregate WR ≈ 0.49 satisfies `TOLERANCE=0.03` immediately, so the binary search does not descend below 0.05 in the stop-gap output (`modifier_extreme_low=0` across all 31 converged classes). This is expected behavior, not a defect. The mechanism is unambiguously unblocked at the code level; empirical sub-0.05 convergence demonstration is the right scope for P2 (cold-start fresh diagnostic regen), not P0's stop-gap.

**Disciplines confirmed by P0 work:** #1 math-before-code (gamora investigation pre-authored); #2 smoke-test (single-class A1; test-suite A2; 3-season stop-gap only); #11 empirical inspection (warm-start finding documented, not hand-waved); #12 semantic shift (named explicitly in commit message + MIGRATION.md v1.21 header + docstring + `ClassBalanceResult` annotation); #18 implicit-pillar named constant (resolved with full docstring).

**P1 (Option B) routing:** knight-rider routed Option B recompose-trigger re-conditioning design brief authoring to gandalf as background subagent. Gandalf's deliverable: design brief covering (a) trigger re-condition location in `balance_loop.py`, (b) signal-range math + epsilon choice, (c) working-modifier disposition for lever evaluation, (d) smoke gate B1 design (the falsifying experiment), (e) cross-seam impact (star-lord telemetry + MIGRATION.md v1.22), (f) Discipline #12 semantic-shift framing. Sequence after gandalf: jack-ryan Gate-1 critique → gamora implementation → smoke B1 → P1 acceptance tag → P2 phase begins. Expected ~6-10h total for P1.

**Hive trigger watch:** no signals; P0 clean. ⏸ Triggers 1-4 (explicit wind-down / P5 completion / P3 CANNOT REJECT NULL / hard architectural blocker) all unsignaled.

---

## 2026-05-19 (night) — THIRD HIVE ACTIVATED: recompose-validation hive (P0 Option A floor widening fired to gamora)

**Event:** Fresh knight-rider session activated the **third hive-mind** per `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md`. Engine-rebuild knight-rider stood down by Matt; this is a clean activation, not a continuation.

**Mission:** validate per-tier convergence + recompose mechanism via fresh diagnostic regen; ship a true season under the new tuning mechanism if it validates. Six phases (P0 Option A → P1 Option B → P2 fresh diagnostic regen → P3 validation synthesis → P4 ship true season → P5 canonical record).

**Operating mode:** AUTONOMOUS continuation per engine-rebuild protocol § 4.0. No L3-to-Matt during operation. SME agents decide within seams; gandalf decides cross-cutting design; knight-rider orchestrates; jack-ryan continuous-observation with BLOCK retained. Matt re-enters only at one of four wind-down/completion triggers (explicit wind-down / P5 completion / P3 CANNOT REJECT NULL verdict / hard architectural blocker).

**Activation sequence completed (this entry):**
1. ~45-min required reading absorbed (launch dispatch + protocol + HELD P0 dispatch + R2+ST findings amended + 2026-05-17 archived mechanics + engine-rebuild § 4.0 amendment + balance-loop investigation + Pattern-B PARKED thread)
2. Pre-hive baseline tagged + pushed across all 4 repos: `recompose-hive/v0.0-pre-activation`
3. Hive operational artifacts authored: `scope-of-work-recompose-validation.md`, `coordination-matrix-recompose-validation.md`, `recompose-validation-log.md`, `state-of-hive-2026-05-19-recompose-validation.md`
4. P0 dispatch renamed (HELD- prefix dropped) and fired to gamora as background subagent
5. Activation artifacts committed (`ae5191f`) + pushed

**P0 in flight:** gamora executes Option A floor widening (4-line change at `balance_loop.py` lines 767/891/1247/1941 → `MODIFIER_SEARCH_FLOOR=0.01` named constant + module-level docstring per Discipline #18) + smoke gates A1/A2/A3 + MIGRATION.md entry + `modifier_extreme_low` telemetry flag + stop-gap regen of 3 diagnostic seasons. Expected wall-time ~4 hours.

**Standing authority:** ADR-006 amendment grants commit+push on milestone tags + push-readiness summaries without per-tag re-ask. Tag namespace: `recompose-hive/v<X.Y>-<milestone>` (distinct from `hive-rebuild/`, `vs2a/`, `vs2b/`).

**Adjacent state held:** Pattern-B PARKED (commercial-direction thread parked at `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`); R6 host-calibration not in scope; engine-rebuild closure already done; VS2a continuation is a different track.

**Phase B.2's Pattern-A/Pattern-B finding is the empirical foundation for the new hive:** 22 classes (44.9%) are Pattern-B (latent boss-kill capability gated by floor + binary WR) — exactly the slice Option A unblocks; 27 classes (55.1%) are Pattern-A (kit-composition pathology) — the open empirical question that the fresh diagnostic regen at P2 will answer (does recompose-validation produce categorically different kits, or does kit-redesign queue work remain required?).

---

## 2026-05-19 (late evening) — INVESTIGATION CLOSURE: R2+ST counterfactual chain complete; Pattern-B finding aligns with new hive's central premise

**Event:** Matt confirms Phase B.2 verdict aligns with the next hive's framing. Investigation chain (R2+ST counterfactual; Phases A through B.2) is now CLOSED. This session's role ends at Phase B.2 closure + clean handoff. Hive holds position pending Matt's explicit wind-down + launch of fresh knight-rider window for the recompose-validation hive (third hive activation).

**Phase B.2 verdict alignment with new framing (per Matt):**

- **22 Pattern-B classes (44.9% of catalogue)** — boss WR becomes nonzero at modifier ∈ [0.50, 2.0] but swarm WR ceiling-violates first at those modifiers. **These 22 classes empirically validate the recompose-hive's central premise.** The latent boss-kill capability exists; the 1D-floor blocks it; recompose-trigger refinement (or per-tier-recompose validation) is the right surgical lever for this slice.

- **27 Pattern-A classes (55.1% of catalogue)** — boss WR = 0.000 at all modifiers ≤ 2.0; pure kit-composition pathology. **These 27 classes are the open empirical question** that the new hive's fresh regen will answer: does the recompose-validation mechanism produce kits that escape this pattern, or do they require kit-redesign queue work?

The 49-class catalogue splits cleanly between the two paths the new hive will exercise: ~half empirically reachable via the recompose mechanism (Pattern B); the other half is the test of whether the new hive's regen mechanism produces categorically different kits (Pattern A's open question).

**Investigation chain artifacts (all committed + pushed; engine `c2eb1a6` + collab `b3738fa`):**

- Phase A: methodology + sigmoid blockers
- Phase B+C+D: original-framing math notes (Exp 1 / Exp 2 / joint synthesis)
- Phase B.2: actual H1 test with proper modifier-sweep data
- Canonical findings memo with § 8 methodological amendment
- Sweep script (new; no engine code modifications)

**Continuation path (NOT this session):** the recompose-validation hive (third hive activation) fires from a fresh knight-rider window per Matt. Launch artifacts (Matt-authored; uncommitted in this session's working tree intentionally; Matt commits + activates from the fresh window):

- Protocol: `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md`
- Launch dispatch: `agentic_orchestration/dispatches/2026-05-19-knight-rider-recompose-validation-hive-launch.md`

**Discipline pattern for the project record (running total today):** four same-day self-corrections — (1) substrate hypothesis weakened; (2) floor-mechanism diagnosis; (3) 1D-vs-2D measurement-architecture critique surfaced and then refuted-in-its-own-data; (4) refutation-framing correction (Matt-surfaced; canonical record amended in place per § 8 + Phase B.2 commissioned as the actual H1 test). The cadence — disposition language updated when evidence does not actually support it — is the project's immune system working.

---

## 2026-05-19 (night) — Phase B.2 R2 modifier sweep COMPLETE — row 5 confirmed with key refinement

**Event:** Gamora executed Phase B.2 — the proper H1 test of the R2-as-canonical counterfactual. Multi-modifier R2 sweep run for 49 classes at {0.05, 0.10, 0.20, 0.50, 1.0, 2.0} × 3 scenarios × 30 fights = 26,460 fights.

**Verdicts:**
- H1 (R2-as-canonical architectural critique): **CANNOT_REJECT_NULL** — 0/49 classes (0.0%) achieve joint M* satisfiability (threshold: 60%)
- H2 (catalogue-quality counter-hypothesis): **CONFIRMED** — 49/49 classes unsatisfiable (threshold: 40%)
- Joint matrix: **Row 5 confirmed** — catalogue has deeper pathology

**Critical NEW finding (not visible from Phase A):** 22/49 classes (44.9%) CAN achieve boss kills at modifier ≥ 0.50–2.0. Phase A observed boss WR = 0 at the single 1D-converged modifier and concluded boss-kill inability was universal. The sweep shows boss-kill capability is modifier-dependent for nearly half the catalogue.

**Why H1 still cannot reject null:** The WR surfaces are binary step functions (WR ∈ {0.000, 1.000} only). No intermediate values across 30 fights per modifier point. The narrow target bands [0.65, 0.80] (swarm) and [0.30, 0.45] (boss) are architecturally unreachable under the current R2 calibration (decisive fight outcomes). Joint satisfiability requires the swarm and boss targets to overlap — impossible when both WR transitions happen at the same modifier (ceiling violation on swarm at the modifier where boss becomes killable).

**Two distinct unsatisfiability patterns:**
- Pattern A (boss_nz_never, 27/49 = 55.1%): Kit-composition pathology. Cannot kill boss at any modifier ≤ 2.0. Kit-redesign queue.
- Pattern B (swarm_ceiling_at_boss_nz, 22/49 = 44.9%): Latent boss-kill capability gated by modifier floor + binary WR structure. These classes benefit from Option A.

**Artifacts filed:**
- Math note: `reincarnated-engine/design/working-agreement/r2-modifier-sweep-phase-b2-2026-05-19.md`
- Sweep script: `reincarnated-engine/scripts/r2_modifier_sweep_phase_b2.py`
- Sim output: `reincarnated-engine/output/R2-modifier-sweep-2026-05-19/per_class_modifier_results.json`
- AGENT_STATE.md updated

**Routing:** gamora → knight-rider → gandalf for Phase B.2 verdict review + Phase E gate disposition (Phase E does not trigger under CANNOT_REJECT_NULL).

**Wind-down trigger:** Phase B.2 verdict ready. Row 5 stands. Option A + kit-redesign queue remain the actionable path.

---

## 2026-05-19 (later evening) — AMENDMENT: R2+ST counterfactual refutation framing was overreach

**Event:** Matt push-back on the entry below ("Investigation COMPLETE") surfaced that the disposition language overstated what existing telemetry could support. The "both levers empirically eliminated" framing closed two architectural-direction doors that the data did not actually close.

**What was overstated:**

- **Experiment 1 (R2-as-canonical) was NOT TESTED.** The existing R2 telemetry carries a single converged modifier per class — the one each class reached under 1D PackProxy convergence. It does NOT carry per-class WR observations across the modifier landscape. The investigation observed *"at the 1D-converged modifier, what does R2 show?"* — NOT *"if R2 had been the convergence target, where would each class converge to?"* The latter requires multi-modifier R2 data per class to fit a sigmoid and solve for hypothetical M\*. Phase A correctly identified the sigmoid as uncalibratable; the disposition then mistakenly treated absence-of-multi-modifier-signal as refutation rather than "the experiment cannot be run with this data."

- **Experiment 2 (ST K-sweep) refutation is correct AT the floor-locked modifier, but UNPROVEN above.** When WR_boss_baseline = 0, the linearization WR(K) = WR_base × DPS_ratio(K) = 0 for any K (mathematically exact). But the very classes where WR_base > 0 at their current modifier — including any class converging above the floor — are exactly where K would have its strongest potential effect, and K's effect at those modifiers was not tested. K-as-lever is not eliminated; it is bounded-below by whatever moves boss WR off zero.

**What stays correct in the original entry:** the mathematical observation about WR_base = 0; the Phase A finding that R2 boss_with_adds_wr = 0.000 for all 51 classes at their 1D-converged modifiers; the `get_1d_wr_for_class()` bug finding; the actionable-lever sharpening (Option A + kit-redesign queue remain the right immediate paths under either reading); the joint matrix row 5 interpretation insofar as it captures "at the 1D operating point" observations.

**What was commissioned to correct the gap:** **Phase B.2 — R2 modifier sweep.** Re-run R2 spatial sub-gauntlet for each class at a sweep of modifier values (rather than only the 1D-converged value), producing the per-class per-modifier WR observations needed to fit the sigmoid and solve for hypothetical M\* under R2-as-canonical convergence. Until Phase B.2 lands, H1 remains untested.

**Artifacts amended in place (audit trail preserved):**

- `canonical/story/r2-st-counterfactual-findings-2026-05-19.md` — top banner + new § 8 ("Methodological gap correction") binding the disposition language in § 0-§ 7
- `agentic_orchestration/gandalf/research/hive-runs-review-2026-05-19/review.html` — top banner + new Part 2.B.5.amend section + Decision #1 inline correction; document status bumped to v1.3
- This CHANGELOG entry

**Discipline pattern (fourth same-day self-correction):** the previous three same-day self-corrections were substantive empirical updates. This fourth is a *framing correction* — a disposition that was empirically grounded but rhetorically over-extended. The team lesson: *empirical evidence that bounds-the-question is not the same as empirical evidence that closes-the-question.* The disposition language must distinguish them, especially when existing data was collected for a different purpose than the question being asked.

**Trigger A queue impact:** unchanged. Option A modifier-floor widening remains the actionable next step under either reading of the counterfactual evidence. Matt's approval gate stands. The corrected disposition does not change Decision #1's recommendation; it sharpens the rationale for *why* Option A leads (it's the prerequisite that moves boss WR off zero, making K-as-lever testable for the subset of classes that would benefit).

---

## 2026-05-19 — R2+ST Counterfactual Math Investigation COMPLETE (gamora Phases B+C+D)

> **⚠️ AMENDED — see entry above ("AMENDMENT: refutation framing was overreach").** The "Investigation COMPLETE" language and the "both levers empirically eliminated" framing in this entry overstate what the data supported. Read this entry through the amendment lens. Specifically: "R2-as-canonical convergence would not have moved boss-tier collapse" is true *at the 1D operating point* but does not bind the counterfactual; the counterfactual is the question Phase B.2 actually tests.

**Event:** Gamora completed Phases B, C, and D of the R2+ST counterfactual math investigation commissioned by gandalf this morning and authorized in § 13.1 of the S1-firstbatch-fail disposition. Three math notes filed. Trigger A does not fire. Joint matrix row 5.

**Experiment 1 (R2 convergence counterfactual):** PRIMARY FINDING: R2 spatial boss WR = 0.000 identically to R1 1D boss WR = 0.000 for all 51 classes. R2-as-canonical convergence would not have moved boss-tier collapse for this catalogue. Matt's architectural critique ("tuning against 1D while gating on R2 is counterproductive") is not empirically supported; the spatial measurement replicates the same zero-kill-rate pathology as the 1D measurement. The kit-composition diagnosis is corroborated, not undermined. SECONDARY FINDING: R2 swarm WR is bimodal (38/51 WR=1.0, 13/51 WR=0.0); threshold between pass/fail is kit-composition-driven, not modifier-driven.

**Experiment 2 (ST damage multiplier K sweep):** K* = None. K** = None. K*** = None. All-tier-pass rate = 0.0% at every K in [1.0, 2.5] (31 values). Structural blocker: boss WR = 0.000 for 49/49 eligible classes. The linearization model WR(K) = WR_base * DPS_ratio(K) returns 0 for all K when WR_base = 0. Per-cast DPS scaling cannot rescue a zero-kill-rate tier at the current modifier floor.

**Sensitivity subsection (R2-modifier baseline for 17 mismatched classes):** K* = None under R2 baseline for all computable cases (same structural blocker). Robustness flag: N/A — no K* exists to characterize robustness of.

**Joint synthesis matrix:** Row 5 — "cannot reject H1 + no K works + catalogue has deeper pathology." Both hypothesized levers (R2-as-canonical + ST scaling) insufficient for current catalogue at current modifier levels.

**Trigger A:** DOES NOT FIRE. Phase E (ST multiplier implementation) does not proceed.

**Recommended next dispatches:** (1) Option A HELD dispatch for Matt approval (modifier floor adjustment); (2) Kit-redesign queue continuation (jack-ryan / star-lord); (3) P3 R2 bug fix `get_1d_wr_for_class()` (rocket + star-lord); (4) D11 design review for zero-damage classes (class_0043, class_0060).

**Math notes filed:**
- `design/working-agreement/r2-counterfactual-convergence-math-2026-05-19.md` (Experiment 1)
- `design/working-agreement/st-damage-multiplier-counterfactual-math-2026-05-19.md` (Experiment 2 + sensitivity)
- `design/working-agreement/r2-st-counterfactual-joint-synthesis-2026-05-19.md` (Phase D joint synthesis)

**Routing:** gamora → knight-rider → gandalf for Phase D final summary + Trigger A gate disposition.

---

## 2026-05-19 — VS2a S1 arc CLOSED at Trigger A — Option A balance-loop floor widening queued for Matt approval

**Event:** End-of-day wind-down by knight-rider at Matt "please wind down" re-entry. The autonomous VS2a S1 arc converged onto one queued decision after ~8 hours of work:

**Arc summary:** S1 first-batch (rocket; season_100001 char) PASSed cohesion (gandalf 4.83) but FAILed mechanics (gamora canonical R1 0/11 boss). Methodology-conflation audit (jack-ryan) refuted transposition hypothesis + named knight-rider's dispatch authoring as failure point of origin. Substrate-prior retry path tested with seed 100002 (ember PREFER-list) — also 80% floor-lock, weakening gandalf's substrate hypothesis. Knight-rider routed gandalf for re-disposition; gandalf took ownership of category error ("a cohesion-layer truth applied as a mechanics-layer prediction"), withdrew retries 2+3, pivoted to balance-loop floor-mechanism investigation. Gamora investigation diagnosed root cause: B14.5 V1 recompose trigger fires correctly but at modifier=0.0509 all kits win 98-100% → levers produce delta=0 → loop exits as `failed_regenerate`. Architectural failure mode: recompose's signal range [0.30, 0.70] is unreachable when floor=0.05 blocks the search. Recommended Option D (widen floor 0.05→0.01 now + re-condition recompose-trigger this week).

**Critique-pair concurrence #2:** gandalf CONCUR + structural amendment (stage A and B as separate Matt approvals); jack-ryan Gate 1 APPROVE WITH AMEND + 4 process amendments (diagnostic-only temporal gate, blocking test-assertion audit, MIGRATION.md required, smoke gate A4 prerequisite for B).

**Trigger A activation:** Matt briefing § 8 assembled with one-sentence framing + decisions-log text + 6 decision items + HELD implementation dispatch (all critique-pair amendments folded in; fire-on-approval). Path-a hand-redesign held in reserve. Retry-3 withdrawn.

**Bonus empirical:** retry-2 (re-fired under nohup polling) produced 11/11 (100%) convergence failures across 4 distinct failure signatures (floor-lock dominant ~60%; mid-stuck, ceiling-lock, severe-floor-lock minority). Third data point at >70% floor-lock across three substrates (char 72.7%, ember 80%, ember 100%). Substrate hypothesis empirically refuted.

**Team rhythm:** three critique-pair invocations in one day, all productive. Gandalf took explicit ownership of a category error (Mithrandir's "I did this to myself" in disposition § 9.8). Jack-ryan's audit traced back to knight-rider's dispatch authoring discipline (Fix 4 acknowledged). Autonomous mode handled hard failure cleanly; Matt re-enters to a fully-prepared decision packet.

**Tags fired today:** rocket/v1.22-s1-first-batch-regen, gamora/v1.12-r1-sprint-s1-firstbatch, vs2a/v0.1-geometry-type-schema-shipped, vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue (engine); vs2a/v0.6-b6-skilltree-ui-decomposition (demo).

**Skill handoff updated:** `agentic_orchestration/skill_handoff_2026-05-19.md` — wind-down section appended with full arc summary + queued decisions + next-session focus.

**Matt opens first:** `agentic_orchestration/matt-briefing-2026-05-19-s1-firstbatch-fail-disposition.md` § 8.

---

## 2026-05-19 — VS2a S1 first-batch FAIL + critique-pair dispositions (gandalf design + jack-ryan process)

**Event:** S1 first-batch validation gate on season_100001 returned a split verdict:

- **Cohesion (criterion 3) PASS** at 4.83/5.0 (gandalf judgment; exceeds R8 inverted A/B benchmark of 4.77). Season_100001 surfaced as candidate cohesion-5 anchor referent.
- **Mechanics (criteria 1+2) FAIL** under canonical R1 sprint by gamora — 0/11 boss kills (0.000 WR); only 1/11 at mini_boss kill-rate threshold. Statistically indistinguishable from shipped catalogue kit-broken subset.

Critique-pair fired in parallel:

**Gandalf disposition** (`canonical/story/s1-firstbatch-fail-disposition-2026-05-19.md`): Option 1 + Option 4 SELECTED. 5-season regen authorization WITHDRAWN. season_100001 prose retained as cohesion-5 anchor referent; mechanical substrate discarded. Retry path: 3-seed serial budget (100002, 100003, 100004) under substrate-archetypal-stance prior — prefer wind/ember/grit/brine-action; reject char/pall/miasma/rime + aftermath/mourning anchor framing + >50% convergence_failures. Path-a fallback (hand-redesign) activates automatically if all 3 retries fail. Major design insight surfaced: substrate-archetypal-stance is a real design lever; battlefield-clerical canonical rosters (char) have low damage-throughput convention; force/strike/ignite substrates (wind/ember/grit) have higher native throughput.

**Jack-ryan DEV-MODE Gate 2 audit** (`agentic_orchestration/qa/pending/2026-05-19-s1-measurement-discrepancy-audit.md`): transposition hypothesis REFUTED. Root cause is **methodology conflation**, not cross-season copy-paste. Rocket used convergence-time kill-rate estimates (floor modifier, N=30, NO disposition-3 calibration) as proxy for canonical R1 sprint measurements. Disciplines violated: #11 (empirical inspection over assumption), #10 (attribution clarity), #2 (smoke vs full milestone). **Failure point of origin: knight-rider's dispatch authoring** — § 2.4 underspecified the measurement instrument. Four process fixes recommended:

1. Gate criterion must specify instrument, not just threshold
2. Convergence-time estimates must be labeled provisional, not gate-eligible
3. Gate 2 audit before knight-rider fires any first-batch PASS tag
4. Dispatch author (knight-rider) responsible for instrument specification

BLOCK on the PASS claim, not on the work quality. First-batch FAIL is the correct starting state for an iterative sprint. Matt review warranted for the BLOCK severity + future-dispatch standard adoption.

**Knight-rider operational consolidation:**

- Retry dispatch authored: `agentic_orchestration/dispatches/2026-05-19-rocket-plus-gandalf-vs2a-S1-retry-with-seed-constraint.md` — incorporates gandalf § 2.3 substrate prior + jack-ryan § 2.4-bis instrument specification + § 7 process-fix enforcement
- Retry 1 fired to rocket (seed 100002; agentId on file). Serial execution per Discipline #3.
- Matt briefing on deck for natural wind-down re-entry; autonomous execution continues per "do not stop unless I intervene" directive.

**Outstanding tag amendment:** `rocket/v1.22-s1-first-batch-regen` (already pushed) does not claim PASS semantics — it marks the intermediate seam state. The PASS claim lives in the dispatch completion record + AGENT_STATE; both are to be amended by rocket per Fix 2 (convergence-summary heading) during the retry.

---

## 2026-05-19 — VS2a tag-fire batch (intermediate milestones; autonomous-op tag-fire authority per ADR-006 amendment)

**Event:** Knight-rider fired four intermediate milestone tags during autonomous-operation execution:

- `vs2a/v0.1-geometry-type-schema-shipped` @ `cd6e5dd` (engine) — F1 close; star-lord schema 2.13 + geometry_type_source round-trip; 79/79 tests PASS
- `vs2a/v0.3-r2-h1-revalidated-on-existing-catalogue` @ `155e1f2` (engine) — Stage 1 R2-RT v3 PARTIAL-CLOSE per gandalf § 5.3 routing-to-S1 OR-clause; CD-variance domination finding (Drift-17 Layer 4); Stage 2 on S1 regenerated catalogue queued
- `vs2a/v0.6-b6-skilltree-ui-decomposition` @ `08a9f325e` (demo) — F4 close; drax B6 skill-tree UI surface decomposition (design dispatch + prototype shipped; § 7 data contract surfaced to S2)
- `rocket/v1.22-s1-first-batch-regen` @ `f609928` (engine) — S1 first-batch regen; season_100001 generated under R8 `inverted` pipeline; 4/5 first-batch validation criteria PASS (cohesion pending gandalf judgment)

**Rationale (per ADR-006 amendment under autonomous-operation authority):** Developers surface tag-fire requests via AGENT_STATE; knight-rider fires + pushes under pre-approval-batch authority. Matt re-enters only at wind-down.

**In-flight at this moment:**
- Background agent `a263f7a885ae19bfb` — gamora R1 sprint re-run on regenerated catalogue (validation gate criteria 1+2 confirmation at bigger N + includes SMOKE_CLASS_IDS metadata-sampling fix per rocket B6 pre-work audit flag)
- Background agent `a5683abd1cbb8dc88` — gandalf cohesion judging on season_100001 (criterion 3; R8 6-facet rubric; ≥ 4.0 threshold)

**Next gated work (held pending notifications):**
- Full 5-season regen (rocket; gated on validation gate PASS)
- Stage 2 R2-RT v4 on S1 catalogue (gamora; gated on full regen)
- S3 sim MS extension (gamora; independent of S1; C1 cascade ready; held to avoid sim-code collision with in-flight R1 sprint re-run)
- S2 B6 main work (rocket + gamora; gated on S1 full regen)
- L1 demo regen / VS2a SHIP GATE (star-lord + gamora; gated on all VS2a upstream)

---

## 2026-05-19 — Stage A2 PRE-APPROVAL BATCH authored (full 7-dispatch set; VS2A → VS2B → Stage A2 continuation per Matt directive)

**Event:** Per Matt directive 2026-05-19 ("approved, proceed all the way through Stage A2"), knight-rider authored the complete Stage A2 closeout dispatch set alongside VS2a + VS2b pre-approval batches. Combined 25-dispatch production sprint under one Matt approval.

**Seven Stage A2 dispatches authored:**

1. **A1 — gamora — B7 gear-percentile variance gate** — engine-only sim; gates catalogue stability across gear rolls; tag `stage-a2/v0.1`
2. **A2 — rocket + gamora + drax — B12 full audit** — boots/gloves/belt slot expansion + +% MS affixes + hard-cap + UI; cross-seam contract change; tag `stage-a2/v0.2`
3. **A3 — rocket + gamora — B13 post-narrow-slice** — 5 defensive mobility geometries (`roll`/`defensive_dash`/`strafe_mode`/`blink`/`dodge_stance`) + mini-boss/boss strategic escape AI + archetype-emergence observability + trait-pool extension; tag `stage-a2/v0.3`
4. **A4 — gamora — B14 multi-band convergence sim** — extends B14.5 V1 canonical balance-loop pattern; riskiest piece; rollback to `v1.3-b14-5-primary-loop` available; tag `stage-a2/v0.4`
5. **A5 — rocket + drax — B16 loot drop architecture** — drop rules + auto-pickup + visual layer per A6 framework; **Drift-12 candidate filing**; tag `stage-a2/v0.5`
6. **A6 — gandalf — Stage A2 design watch-items framework** — single framework covering B12 visual/UX + B13 telegraph-art convention + B16 loot visual layer; Drift-12 filing; tag `stage-a2/v0.6`
7. **A7 — gandalf + knight-rider + Matt — Playtest Cycle 1** — three phases: autonomous prep + Matt-gated execution + autonomous disposition; substrate = VS2a regen season_001003 + VS2b regen season_001005; tag `stage-a2/v1.0-stage-a2-ship` (Stage A2 CLOSED)

**Combined sprint inventory (consolidated):**
- VS2a: 12 production dispatches (F1-F4 + F5 + F6 + F6-D + R2-RT + S1 + S2 + S3 + L1)
- VS2b: 6 production dispatches (V1-V6)
- Stage A2: 7 production dispatches (A1-A7)
- TOTAL production: **25 dispatches**
- In-flight VS2a continuations: C1-C4 (4 items)
- Matt-gated wind-down items: M1 (Drift-15 selection) + M2 (engine-rebuild playtest tags) + A7-exec (Playtest Cycle 1 execution) = 3 items
- GRAND TOTAL: **32 roadmap items** locked under pre-approval-batch

**Estimated duration:** ~10-16 weeks wall from VS2a L1 ship through Stage A2 v1.0 ship, depending on parallel execution + Matt wind-down session cadence.

**Operating mode:** AUTONOMOUS per protocol § 4.0 + § 4.9 through Stage A2 closeout. Matt re-enters at wind-down (his discretion) for M1 + M2 + A7-exec triple-gated step (Drift-15 pack + engine-rebuild playtest tags + Stage A2 Playtest Cycle 1 — all addressable in single Matt session).

**Forward routing post-Stage-A2:**
- Stage A3 (B9 series; ~4-6 weeks; design fully resolved 2026-05-12 in file 32) — pre-approval-batch decision DEFERRED to Matt at next wind-down session
- Stage A4 (B5 + B15) / A5 / A6 / A7 (progression system) — further deferred
- Playtest Cycles 2-4 — gandalf authors rubrics per A7 template; Matt-gated execution

**Pre-approval surface (Matt's three-doc review):**
- `agentic_orchestration/hive-mind/vs2a-pre-approval-batch-2026-05-19.md` (12 dispatches)
- `agentic_orchestration/hive-mind/vs2b-pre-approval-batch-2026-05-19.md` (6 dispatches)
- `agentic_orchestration/hive-mind/stage-a2-pre-approval-batch-2026-05-19.md` (7 dispatches; consolidated combined view in § 6)

**Authority:** Matt directive 2026-05-19 (VS2A → VS2B → Stage A2 pre-approval continuation); knight-rider operationalization + dispatch authoring under autonomous-mode authority.

---

## 2026-05-19 — VS2b PRE-APPROVAL BATCH authored (full 6-dispatch set; VS2A → VS2B continuation per Matt directive)

**Event:** Per Matt directive 2026-05-19 ("approved, proceed with VS2A → VS2B"), knight-rider authored the complete VS2b dispatch set alongside the VS2a pre-approval batch. Pre-approval-batch mode extended through VS2b. Combined VS2a + VS2b = 18 dispatches; Matt approves one batched sprint plan; no Matt-engagement between batches.

**Six VS2b dispatches authored:**

1. **V1 — rocket — `embodiment_narrative_beat` schema field** — per `canonical/story/embodiment-display-loadout.md` § 15; Discipline #14 generative-side schema; two-stage migration; tag `vs2b/v0.1`
2. **V2 — star-lord — LLM beat-generation call orchestration** — folds into Stage 2 cosmological-vocabulary pipeline as follow-on; anti-bias scaffolding per Discipline #14 candidate; tag `vs2b/v0.2`
3. **V3 — drax — loadout embodiment-narrative-display surface** — per spec § 15 + § 13 implementation cascade; loadout-first; Diablo III class-select reference; tag `vs2b/v0.3`
4. **V4 — gandalf — chierit element-reconciliation (small ~30 min)** — closes VS2a + VS2b chierit watch-items; element-only mapping decision + physical/hybrid fallback; tag `vs2b/v0.4`
5. **V5 — drax + elrond — full Pimen catalogue integration** — extends VS2a C2 (11/13 GREEN-list) to full coverage; tag `vs2b/v0.5`
6. **V6 — star-lord + gamora — VS2b ship gate (regen season_001005)** — fresh regen demonstrates cipher migration + embodiment-axis + embodiment-narrative display + Pimen full integration; tag `vs2b/v1.0-vs2b-ship` (VS2b CLOSED)

**Roadmap-drift surfaced + flagged:** `canonical/16-project-roadmap.md` § VS2b lists some items as "in-flight" or "dispatch not yet authored" that have shipped per dispatch completion records. Stage 1 (rocket) + Stage 2 vocab + Stage 3 engine + Stage 3 drax all shipped 2026-05-16. Roadmap doc amendment forward-flagged to gandalf at next pass. Scope-of-work-vs2b § 1 captures ground truth.

**Combined VS2a + VS2b inventory:**
- VS2a: 12 dispatches (F1-F4 + F5 + F6 + F6-D + R2-RT + S1 + S2 + S3 + L1)
- VS2b: 6 dispatches (V1-V6)
- In-flight: C1-C4 (continue per AGENT_STATE)
- Matt-gated: M1 (Drift-15 selection) + M2 (engine-rebuild playtest tags)
- TOTAL: 24 roadmap items locked under pre-approval-batch

**Operating mode:** AUTONOMOUS per protocol § 4.0 + § 4.9. Matt re-enters only at wind-down (his discretion). Post-VS2b: Stage A2 closeout pre-approval-batch decision DEFERRED to Matt at next wind-down session.

**Pre-approval surface (Matt's one-doc review):**
- `agentic_orchestration/hive-mind/vs2a-pre-approval-batch-2026-05-19.md` (12 dispatches)
- `agentic_orchestration/hive-mind/vs2b-pre-approval-batch-2026-05-19.md` (6 dispatches)
- `agentic_orchestration/hive-mind/scope-of-work-vs2b.md` + `coordination-matrix-vs2b.md` (companion plans)

**Authority:** Matt directive 2026-05-19 (VS2A → VS2B pre-approval continuation); knight-rider operationalization + dispatch authoring under autonomous-mode authority.

---

## 2026-05-19 — VS2a PRE-APPROVAL BATCH authored (full 12-dispatch set; per Matt directive)

**Event:** Per Matt directive 2026-05-19 ("Batch all of VS2a now so I can approve everything in advance"), knight-rider authored the full VS2a dispatch set (12 dispatches total) for Matt's pre-approval review before autonomous execution proceeds. After Matt's review + approval, no further Matt-engagement is required until wind-down (M1 + M2 + retrospective).

**Eight additional dispatches authored (sibling to F1+F2+F3+F4 from earlier today):**

5. **F5 — legolas + gandalf — VS2a Drift-14 pool × VFX-catalogue mapping audit** — Mode A audit + gandalf re-scoring + culled-pool summary; gates: F3 framework lands; tag: `vs2a/v0.10-drift14-audit-complete`
6. **F6 — legolas — VS2a Drift-15 environment-tileset Track A sweep** — Mode B catalogue crawl across Tier-1 pixel-art vendors; gates: F3 framework lands; tag: `vs2a/v0.11-drift15-track-a-complete`
7. **F6-D — drax — VS2a Drift-15 Track D environment-tileset integration** — renderer extension + pack manifest consumption; gates: M1 Matt-selection at wind-down; tag: `vs2a/v0.16-drift15-drax-integration-complete`
8. **R2-RT — gamora — VS2a R2 H1 re-validation under explicit geometry_type** — R2 disposition § 3.2 forward-routed re-test under ORIGINAL variance ≥ 0.10 threshold; gates: F1 acceptance complete; tag: `vs2a/v0.2-r2-h1-revalidated`
9. **S1 — rocket + gandalf consult — VS2a kit-redesign sprint (3-branch per F2 path)** — three-branch pre-authored dispatch (hand-redesign / R8-inversion / hybrid); gates: F2 + F1 land; tag: `vs2a/v0.7-kit-redesign-sprint-complete`
10. **S2 — rocket + gamora — VS2a B6 main work (tree structure + tree-aware convergence)** — per `canonical/28` B6 extension; gates: F2 + rocket pre-work + S1 partial; tag: `vs2a/v0.8-b6-main-work-complete`
11. **S3 — gamora — VS2a Gate-3b sim MS extension** — sim consumer of engine-emitted JSON MS values; gates: rocket schema-default + star-lord export-DTO (C1 in-flight cascade); tag: `vs2a/v0.9-sim-ms-gate3b-complete`
12. **L1 — star-lord + gamora — VS2a demo regen on single season (SHIP GATE)** — full integrated stack demonstration; gates: F1 + F4 + S1 + S2 + S3 + C1 + C2 + C3 + F5; tag: `vs2a/v1.0-vs2a-ship`

**Pre-approval surface for Matt review:** `agentic_orchestration/hive-mind/vs2a-pre-approval-batch-2026-05-19.md` — full inventory + DAG + activation-gate map + Matt-approval pattern (what Matt approves; what Matt may amend; what Matt does NOT need to approve under autonomous-mode).

**Operating mode:** AUTONOMOUS per protocol § 4.0 + § 4.9 (Matt re-enters only at wind-down). Pre-approval-batch mode is the Matt-side preference shift: Matt reviews the whole sprint plan up front, then walks away knowing every dispatch is locked.

**M1 + M2 Matt-gated items unchanged:** Drift-15 Matt-selection at wind-down; engine-rebuild playtest tag firings v0.12 + v0.16. F6-D drax integration is pre-authored but HELD post-M1.

**Authority:** Matt directive 2026-05-19 (pre-approval-batch mode); knight-rider operationalization + dispatch authoring under autonomous-mode authority.

---

## 2026-05-19 — VS2a first-fire batch DISPATCHED (F1 + F2 + F3 + F4 authored)

**Event:** Knight-rider authored four VS2a first-fire dispatches under AUTONOMOUS-OPERATION (continuation of engine-rebuild close → VS2a sequencing per dispatch § 6.5 explicit ordering). All four fire immediately; no upstream gating on each other beyond F3 → F5/F6 (second-fire batch). C1–C4 in-flight continuations independent. M1 + M2 Matt-gated items HELD for wind-down.

**Dispatches authored (`agentic_orchestration/dispatches/`):**

1. **F2 — gandalf — VS2a kit-redesign approach Gate-1 decision** (`2026-05-19-gandalf-vs2a-kit-redesign-approach-decision.md`) — HIGHEST leverage; gates S1 + S2. Decision: hand-redesign (a) vs R8-inversion (b) vs hybrid (c). Acceptance: `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md` + tag `vs2a/v0.5-kit-redesign-approach-decided`.
2. **F1 — rocket + star-lord — VS2a `geometry_type` per-skill schema field** (`2026-05-19-rocket-plus-star-lord-vs2a-geometry-type-schema.md`) — engine-rebuild R2 H1 fall-out per gandalf R2 disposition § 3.1 + jack-ryan Q1 disposition. Schema additive-nullable → non-null post-backfill. MIGRATION.md required at both seams. Round-trip smoke per Principle 6. Acceptance: tag `vs2a/v0.1-geometry-type-schema-shipped`.
3. **F3 — gandalf — Drift-14 + Drift-15 design framework** (`2026-05-19-gandalf-vs2a-drift14-15-framework.md`) — gates F5 + F6 legolas commissions. Drift-15 framework includes EXPLICIT autonomous-vs-Matt-gated step separation (Tracks A+B autonomous; Track C HELD for wind-down per M2 pattern; Track D post-Matt). Acceptance: framework docs + drift-audit.md updates + tags `vs2a/v0.3` + `vs2a/v0.4`.
4. **F4 — drax — VS2a B6 skill-tree UI surface decomposition** (`2026-05-19-drax-vs2a-b6-skilltree-ui-decomposition.md`) — closes fifth P6 instance (engine emits tree data; demo has no rendering surface). Drax authors design dispatch + ships prototype. Acceptance: design doc + prototype + tag `vs2a/v0.6-b6-skilltree-ui-decomposition`.

**Second-fire (gated on F3):** F5 (legolas Mode A Drift-14 pool × VFX-catalogue mapping audit) + F6 (legolas Mode B Drift-15 environment-tileset sweep Track A).

**In-flight continuations (specialist independent; no knight-rider dispatch):** C1 movement-speed baseline + C2 B11 GREEN-list VFX + C3 chierit character rendering + C4 Pimen curation pipeline.

**Matt-gated (HELD for wind-down):** M1 (Drift-15 Matt-selection per Track C) + M2 (engine-rebuild playtest tags `v0.12-r5-hypothesis-test-passed` + `v0.16-r4-hypothesis-test-passed`).

**Operating mode:** AUTONOMOUS per protocol § 4.0 + § 4.9 (inherited from engine-rebuild protocol into VS2a per scope-of-work § 6). No L3-to-Matt during operation. Matt re-enters only at wind-down.

**Authority:** Matt directive 2026-05-19 (autonomous-operation continuation); knight-rider operationalization + dispatch authoring under launch-dispatch § 6.5 routing.

---

## 2026-05-19 — Engine-rebuild batch CLOSED (`hive-rebuild/v1.0-engine-rebuild-complete` fired across all 4 repos)

**Event:** Engine-rebuild hive-mind session completed under AUTONOMOUS-OPERATION mode. Knight-rider proceeds immediately to VS2a per dispatch § 6.5 explicit ordering; Matt does NOT return to loop (wind-down trigger remains exclusively Matt's explicit declaration per protocol § 4.9).

**Tag fired:** `hive-rebuild/v1.0-engine-rebuild-complete` across all 4 repos under "operational-completion category-of-completion" framing per gandalf disposition `canonical/story/v1.0-engine-rebuild-complete-disposition-2026-05-19.md` (Option γ).
- Engine: at `bb013b7` (gamora R2 production graduation; substrate-completion commit)
- Collab: at `9391b22` (gandalf disposition commit)
- Demo: at `542f1115b` (latest HEAD; R4 v0.15 operational already tagged)
- Loadout: at `ec73ea7` (latest HEAD)

**Workstream completion table:**
| WS | Status | Hyp tag |
|---|---|---|
| R1 — Per-tier balance | CLOSED | `v0.3` (4-sub-claim category-of-completion) |
| R2 — Spatial sub-gauntlet | CLOSED | `v0.14` (Option D instrument-limited PASS) |
| R3 — Per-skill range + AI schema | CLOSED | `v0.6` |
| R4 — Demo collision + leash + range | OP-COMPLETE; PLAYTEST-PENDING | `v0.16` HELD (Matt-gated) |
| R5 — Demo AI parity | OP-COMPLETE; PLAYTEST-PENDING | `v0.12` HELD (Matt-gated) |
| R7 — AI catalogue source-of-truth | CLOSED | `v0.7` |
| R8 — Season-as-emergent-output | CLOSED | `v0.10` + `v0.11` (Sub-case 3 disposition) |

5 of 7 CLOSED; 2 of 7 OP-COMPLETE with playtest-pending tags HELD for Matt wind-down session. Notional `hive-rebuild/v1.1-engine-rebuild-final` fires when v0.12 + v0.16 resolve.

**R-series disposition arc (4 dispositions; category-of-completion pattern established):**
- R1 Blocker 3 — gandalf — "70% pass-rate" retired; 4 sub-claims (GATE WORKS + REACHABLE + KIT-BROKEN SURFACE + QUEUE EXISTS); kit-redesign queue authored as VS2a handoff (`canonical/story/r1-kit-redesign-queue-2026-05-19.md`)
- R8 Sub-case 3 — gandalf — `inverted` as default; `inverted_no_naming` deferred behind template-distribution repair; `canonical/19-llm-call-map.md` Phase A swap
- R2 H1 Option D — gandalf — variance ≥ 0.10 threshold preserved as VS2a re-test target once `geometry_type` per-skill schema field lands (instrument-limited by name-heuristic 43/3/4 sample imbalance)
- v1.0 Option γ — gandalf — operational-completion framing; playtest-pending tags HELD; roadmap continuation unblocked

**Engine-rebuild fall-out items routed to VS2a:**
1. `geometry_type` per-skill schema field (rocket + star-lord) — re-enables R2 H1 under original threshold
2. Kit-redesign queue execution (~20-30 mediocre + ~10-15 broken classes) (rocket + gandalf consult) — intersects with B6 main work
3. Spatial boss recalibration if needed (gamora; may be VS2b)
4. Template-distribution repair (rocket; LOW; capacity-when-available)
5. `--anchor-id` CLI flag (rocket; deferred)
6. R1 second-pass calibration knobs (gamora; deferred — boss reachability stable per N=60 Test 3)

**Items completed this session that were on the R-disposition forward-routing list (removed from VS2a queue):**
- `seasonal_dominant_element` write-back gap fix (rocket commit `9f6e4e6`)
- R8 Test 5 multi-shot stability execution (Jaccard 1.00 on `inverted/season_099002`)

**Operating-mode metrics:**
- Matt escalations: 0
- Hard BLOCKs by jack-ryan: 0
- WARN findings resolved in-session: 4
- Structural blockers surfaced + dispositioned: 3
- Gandalf disposition decisions: 4
- Canonical-doc amendments authored: 8+
- Transient infrastructure failures recovered: 1 (rocket API overloaded_error → re-fire)
- Specialist sessions: ~33
- Tags shipped + pushed: 15
- Push hard-constraint violations: 0
- Elapsed wall time: activation 04:26Z → batch close ~07:05Z (~2h 40min; ~7h cumulative specialist time)

**Closeout state-of-hive:** `agentic_orchestration/hive-mind/state-of-hive-2026-05-19-engine-rebuild-v1.0.md` (knight-rider authored at batch close per dispatch § 6.5 step 3). Mid-day snapshot at `state-of-hive-2026-05-19-engine-rebuild-mid-day.md` for full chronological detail.

**Authority:** Matt directive 2026-05-19 (autonomous-operation launch); gandalf v1.0 disposition; knight-rider operationalization + state-of-hive closeout authorship.

---

## 2026-05-19 — Engine-rebuild hive ACTIVATED (second hive-mind invocation; AUTONOMOUS-OPERATION mode)

**Event:** Knight-rider activated the **engine-rebuild hive-mind session** per Matt directive 2026-05-19 + gandalf-authored launch dispatch (`agentic_orchestration/dispatches/2026-05-19-knight-rider-engine-rebuild-launch.md`, commit `d49c587`). This is the **second hive-mind activation** (first was 2026-05-17 Phase-1 P1; mission completed + archived).

**Mission scope:** Seven workstreams closing the gauntlet-simulator gaps diagnosed 2026-05-18 + running the season-as-emergent-output A/B test:
- **R1** Per-tier balance targets (gamora; 1–2 wk)
- **R3** Per-skill range + AI behavior schema migration (rocket + star-lord + elrond; 2–4 wk)
- **R7** AI catalogue source of truth (rocket + star-lord; 2–3 wk parallel with R3)
- **R8** Season-as-emergent-output A/B (rocket + star-lord + gandalf; 1–2 wk)
- **R5** Demo AI parity audit (drax; 1 wk, queued behind R3)
- **R2** 2D spatial sub-gauntlet (gamora + star-lord; 3–5 wk, queued behind R3)
- **R4** Demo collision + leash + range (drax; 2–3 wk, queued behind R3)

**Out of scope:** R6 Host-Calibration (Pattern-B parked per `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`); Pattern-B commercial-direction work; Phase-1 P1 re-work.

**First-fire batch (parallel, dispatches authored):** R1 + R3 + R7 + R8. R5 + R2 + R4 queued behind R3.

**Critical operational change vs 2026-05-17 protocol:** **AUTONOMOUS OPERATION** per protocol § 4.0. No L3-to-Matt escalation during operation. SME agents decide within their seams; gandalf decides cross-cutting design/canonical/architectural; knight-rider decides orchestration/sequencing. Matt re-enters **only** at wind-down — engine-rebuild completion does NOT trigger wind-down; flow continues onto VS2a → VS2b → Stage A2 per Matt roadmap-continuation directive (launch dispatch § 6.5).

**Commit + push authority extended** per launch dispatch § 6.6 (ADR-006 amendment extension): knight-rider may commit + push on major milestone achievement and hypothesis-test passage without per-action authorization. Hard constraints retained (no force-push, no hook bypass, explicit refspec, summary from live git state).

**Mechanics inheritance:** All operating mechanics from `canonical/story/archived/hive-mind-protocol-2026-05-17.md` §§ 3–11 inherit by reference; engine-rebuild protocol specifies what's distinct (mission scope, coordination matrix, autonomous-operation amendment, galadriel sub-agent restriction).

**Galadriel sub-agent restriction in effect** per protocol § 7 + amendment to `.claude/agents/galadriel.md` (already authored 2026-05-19 per Matt directive). Galadriel does NOT invoke sub-agents during the hive; surfaces requests via hive log REQUEST entry.

**Pre-rebuild safety baseline tagged + pushed across all 4 repos:**
- `hive-rebuild/v0.0-pre-engine-rebuild`
- collaboration `d49c587`, engine `89f83c2`, demo `59b933031`, loadout `ec73ea7`

**Operational artifacts committed:** activation commit `edeeea8` (collaboration repo, main, pushed):
- `agentic_orchestration/hive-mind/engine-rebuild-log.md` (append-only hive log with activation STATE + 4 HANDOFF entries)
- `agentic_orchestration/hive-mind/scope-of-work-engine-rebuild.md`
- `agentic_orchestration/hive-mind/coordination-matrix-engine-rebuild.md`
- `agentic_orchestration/hive-mind/state-of-hive-2026-05-19-engine-rebuild.md`
- 4 first-fire dispatches at `agentic_orchestration/dispatches/`:
  - `2026-05-19-gamora-R1-per-tier-balance-targets.md`
  - `2026-05-19-rocket-plus-star-lord-plus-elrond-R3-schema-migration.md`
  - `2026-05-19-rocket-plus-star-lord-R7-ai-catalogue-source-of-truth.md`
  - `2026-05-19-rocket-plus-star-lord-plus-gandalf-R8-season-as-emergent-output.md`

**Authority:** Matt directive 2026-05-19 (autonomous-operation launch); gandalf protocol + solutions doc + Pattern-B PARKED thread (commit `d49c587`); knight-rider operationalization.

**Tag namespace:** `hive-rebuild/v0.<N>-<milestone>` (distinct from `hive/v0.<N>` used for Phase-1 P1).

---

## 2026-05-18 — hive-log STATE: star-lord multi-season encounter analytics complete — telemetry.db backfilled for 6 seasons + MS/AOE schema extended

**Event:** star-lord completed dispatch `2026-05-18-star-lord-fights-jsonl-ingest-plus-multi-season-encounter-analytics`. Matt L3 authorized "fire star-lord on Path A."

**Block 1 — fights.jsonl ingest:** New script `scripts/ingest_fights_jsonl_to_telemetry.py` (engine). Backfilled `class_fight_loadouts`, `abilities`, and `monsters` in `telemetry.db` for 6 seasons: 002011, 002012, 002013, 002014, 002015, and 002328. Total: 609,800 fight rows. Row counts match class-phase JSONL counts exactly. Idempotency smoke-tested (drop-and-replace pattern for fight rows; INSERT OR IGNORE for abilities/monsters). Geometry_type derived via `derive_geometry_type()` 3-layer cascade (same as D10 generation). All V2.x spatial columns NULL for backfilled rows — fights.jsonl has no positional data.

**Block 2 — multi-season encounter analytics:** 6 per-season `encounter_analytics_NNNNNN.json` files landed in `reincarnated-loadout/data/`. Existing `encounter_analytics.json` (season_001005) renamed to `encounter_analytics_001005.json` for naming consistency (original retained).

**Block 3 — MS/AOE radius bands:** Extended `gen_encounter_analytics.py` with two new per-class fields. `movement_speed_band` (slow/medium/fast, per-season 33rd/67th percentile). `aoe_radius_band` (tight/medium/wide, same). AOE radius sourced from canonical geometry-type default table (B11 math note) — per-skill spatial radius params do not exist in class JSON. Documented in output JSON and MIGRATION.md v1.15.

**Findings:** All D10 seasons have uniform movement_speed=8.0 m/s — MS bands degenerate (all "slow"). season_002328 predates movement_speed field (NULL). AOE-vs-monster-position correlation not possible from existing data — no spatial data in fights.jsonl. Flagged to knight-rider for future instrumentation dispatch.

**Engine commit:** `d85fb45`, `89f83c2` — pushed to main. **Loadout commit:** `9b23382` — pushed to main.
**Tag:** `star-lord/v1.8-fights-jsonl-ingest-plus-multi-season-encounter-analytics-plus-ms-aoe-bands-1`
**MIGRATION.md:** v1.15 appended.

**drax v1.18 Block 2 status:** UNBLOCKED. Per-season encounter_analytics files ready for consumption.

---

## 2026-05-18 — hive-log STATE: star-lord bulk re-roll resume complete — 12 missing portraits generated; total 24/24 in `_reroll_all/`

**Event:** Resumed `bulk_reroll_anatomy.py` after prior run died silently at 12/24. Patched script with skip-if-exists idempotency guard, then ran to completion synchronously.

**Root cause (prior silent death):** Script had no skip-if-exists check — re-running from scratch would have re-generated already-complete images. The silent kill was most likely a process-level timeout or OOM from the agent harness after the 12th sequential gpt-image-1 API call (~10 min elapsed). No retry or resume path existed in the original script. Idempotency patch closes the gap.

**12 images generated this session:**
- `season_002011/pitch-smuggler.png` (fire mage)
- `season_002013/shaft-diver.png` (physical hunter — canary slug skipped per brief)
- `season_002014/` — all 5: plague-wind-censer, plague-lantern-bearer, chalk-handed-quarantine-warden, quarantine-lector, plague-diver
- `season_002015/` — all 5: marble-tongued-royal-scribe, banished-royal-herald, windborne-herald-of-the-fractured-court, mad-kings-lector, exiles-gauntlet

**Cost this session:** 12 × $0.04 = $0.48. Ledger total: $2.16. Sprint ceiling remaining: $12.84.

**Script patched + committed:** `fix(star-lord): bulk_reroll_anatomy.py idempotency — skip existing files` — commit `55fa186` on `reincarnated-engine/main`.

**Constraints honored:** pitchData.ts NOT touched. Images NOT pushed. Originals at `season_<id>/<slug>.png` NOT disturbed.

**Status: READY FOR GANDALF CURATION.** All 24/24 portraits now present in `_reroll_all/`. Gandalf curates winners, wires pitchData.ts, and pushes.

Output dir: `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_reroll_all/`
Cost ledger: `/Users/admin/Games/reincarnated-loadout/public/pitch/cost-ledger.json`

---

## 2026-05-18 — hive-log STATE: Canary reroll complete — ready for gandalf curation

**Event:** Star-lord completed anatomy-correction re-roll for Canary of the Drowned Seam (Hero of the Engine). All 3 existing Canary images had hand-anatomy failures (canonical + preflight: 3 fingers; attempt-1: 4 distorted fingers). 4 new attempts generated with progressively stronger anatomy interventions.

**Files generated (all OK, $0.04 each):**
- `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_reroll_canary/canary-attempt-1.png` — original composition + aggressive anatomy negatives embedded in prompt
- `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_reroll_canary/canary-attempt-2.png` — pose change: flame hovering above open palm (summoned, not grasped — eliminates grip failure mode)
- `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_reroll_canary/canary-attempt-3.png` — pose change: hand at side, flame floats behind shoulder near canary (hand minimized in focal area)
- `/Users/admin/Games/reincarnated-loadout/public/pitch/heroes/_reroll_canary/canary-attempt-4.png` — tight chest-up portrait: hand and flame both below bottom frame edge (hand problem eliminated entirely)

**Cost:** $0.16 total (4 × $0.04). Ledger total now $1.20. Sprint ceiling remaining: $13.80.

**Constraints honored:** pitchData.ts NOT touched. Images NOT pushed. Existing _preflight/ and season_002013/ files NOT disturbed.

**Status: READY FOR GANDALF CURATION.** Gandalf reviews all 4, picks winner, wires into pitchData.ts and triggers push as part of swap commit.

Script preserved at: `/Users/admin/Games/reincarnated-engine/scripts/pitch/canary_reroll.py`

---

## 2026-05-18 evening — Overnight autonomous sprint ACTIVATED (mobile-playable + loadout analytics + visual benchmark)

**Event:** Matt-authorized single-night autonomous sprint launched within Phase-1 P1 hive-mind operating mode. Invocation authored by gandalf 2026-05-18 evening per Matt directive; knight-rider engaged at session-open and activated per § 11 checklist.

**Three tracks active:**
- **Track A — Mobile-playable demo (local-dev path).** v1.20 + v1.21 already shipped; D11.5 debug-state URL hook + mobile-render validation queued.
- **Track B — Loadout analytics suite iteration-1.** Gandalf IA → star-lord + elrond data manifests (parallel) → drax implementation → Vercel preview auto-deploy.
- **Track C — Visual benchmark pilot (galadriel commission).** State-matched captures vs Matt's 7-image DoE reference set; rubric authoring; first-pass benchmark report.

**Galadriel — new agent commission.** Sixteenth agent role: visual perception and UX-similarity steward (Tier C+; mirrors elrond/legolas conventions). Persona: Galadriel, keeper of the Mirror. Owns `agentic_orchestration/galadriel/`. **Status: deferred to morning Matt approval** — `.claude/agents/galadriel.md` write was denied by harness at activation; full agent-file draft preserved at `agentic_orchestration/galadriel/AGENT-DRAFT.md` for clean drop-in (see morning-briefing L3-1). Track C work proceeds under deferred-agent-creation workaround (gandalf + drax co-author).

**Protocol amendments for single-night cadence (per invocation § 5):**
- Hive log entries every 30 minutes minimum per active seam
- Two state-of-hive snapshots (midpoint + end-of-sprint) vs daily
- DECISION entries can be 1-sentence rationale during sprint
- Per-seam intermediate tags optional; only morning-checkpoint tag required (`sprint/v0.1-mobile-analytics-benchmark-2026-05-18`)
- Knight-rider expanded L2.5 authority within § 6 pre-authorization matrix; L3 items queue to `morning-briefing-2026-05-19.md`
- Halt-condition discipline preserved (queue-for-morning is not failure)

**Dispatches authored at activation (8 total):**
- `2026-05-18-gandalf-loadout-analytics-suite-information-architecture.md` (Track B.5; critical-path BLOCKER)
- `2026-05-18-drax-debug-state-url-hook-D11-5-plus-mobile-render-validation.md` (Track A.2 + D11.5)
- `2026-05-18-star-lord-loadout-analytics-data-manifest-engine-side.md` (Track B.6 engine-side)
- `2026-05-18-elrond-loadout-analytics-data-manifest-catalogue-side.md` (Track B.6 catalogue-side)
- `2026-05-18-drax-plus-star-lord-vercel-deployment-asset-pipeline-options-paper.md` (§ 2.4 scoping)
- `2026-05-18-drax-galadriel-workaround-capture-pipeline-and-state-matched-captures.md` (Track C pipeline)
- `2026-05-18-drax-loadout-analytics-suite-iteration-1.md` (Track B.7 implementation)
- `2026-05-18-gandalf-plus-drax-visual-benchmark-report-vs2a.md` (Track C.13 report)
- `2026-05-18-jack-ryan-overnight-sprint-watchpoints.md` (continuous-observation)

**Pre-authorization matrix § 6 verified.** HARD NOs honored: no vendor acquisitions, no `git push --force`, no Vercel demo deployment (scope-only paper), no CLAUDE.md / AGENTS.md modifications, no Phase-1 P1 scope changes, no load-bearing canonical-doc amendments.

**Sprint activation commit:** `72495b8` (hive-log STATE + 8 dispatches + morning-briefing + galadriel working tree).

---

## 2026-05-17 — drax v1.16.1 HOTFIX: wave-progression hang + audio/VFX gap

**Event:** Matt L3 playtest on drax v1.16 revealed two critical blockers in VS2a demo.

**Bug 2 (wave-hang) root cause:** v1.16 `gauntletFromRecipe()` paired 2 pack-proxies per wave (3 × 16-mob rooms). The `allPackDead` condition (`pack.every(m => !m.combatant.isAlive)`) stalls when any mob survives outside its anchor room — mobs halt pursuit at room edge per `shouldHaltPursuit()`, leaving the player in `fighting` state indefinitely. Additionally: 8 total waves vs. 7-room dungeon caused `roomForWave(dungeon, 8) = undefined` — act-boss wave 2 had no room anchor. **Fix: Reshape A** — 1 pack-proxy per wave (6 × 8 mobs), extending to 11 total waves + 11-room dungeon plan.

**Bug 1 (audio gap) root cause:** AudioContext suspended before user gesture. Howler v2.2 auto-resumes its own context, but our Web Audio API Tier-1 procedural context (`getAudioCtx()`) is a separate `AudioContext` that does not. **Fix:** `_hookAudioContextResume()` explicitly resumes both contexts on first `mousedown`/`keydown`/`touchstart`.

**Diagnostic logging added** throughout both subsystems (grep `[diag]` tag) for Matt's re-playtest DevTools session.

**Commit:** `430a9f4` (reincarnated-demo); **tag:** `drax/v1.16.1-hotfix-wave-hang-plus-audio-vfx-gap-1`
**Dispatch:** `2026-05-17-drax-v1-16-1-hotfix-wave-hang-plus-audio-vfx-gap.md` — completion record appended.

Format: reverse chronological, dated entries with brief rationale.

---

## 2026-05-17 — Phase-1 P1 hive-mind mode ACTIVATED

**Event:** Matt directive 2026-05-17 ("100% heads down development work across the entire team and rebuild the engine from the ground up to achieve full Phase-1 P1 before demo VS2a. ... All in perfect harmony. Let's take this on as a hive mind.") triggered Phase-1 P1 hive-mind operating mode per gandalf invocation request `agentic_orchestration/gandalf/requests/2026-05-17-knight-rider-phase-1-p1-full-overhaul-coordination.md` + operating protocol `canonical/story/hive-mind-protocol-2026-05-17.md`.

**Standard mode SUSPENDED for duration of Phase-1 P1.** Specialists operate under distributed authority (L1 in-seam; L2 cross-seam via knight-rider; L3 architectural to Matt). Jack-ryan continuous-observation replaces Gate-1/Gate-2 retrospective review. Per-dispatch authorization gating removed; specialists execute against the scope-of-work continuously. Gandalf continuously available for design-direction.

**Pre-Phase-1 P1 baselines tagged** (local; not pushed per ADR-006 pending Matt authorization):
- engine: `hive/v0.0-pre-phase-1-p1 @ f9c363e`
- demo: `hive/v0.0-pre-phase-1-p1 @ 692c555`
- loadout: `hive/v0.0-pre-phase-1-p1 @ 90db544`

**Hive operational artifacts authored at activation** (knight-rider; per invocation § 4):
- `agentic_orchestration/hive-mind/scope-of-work-phase-1-p1.md` — 27-deliverable executable plan with per-seam tasking + critical-path identification + in-flight work disposition (fold/pause/standalone) + risk register + ship-gate criteria
- `agentic_orchestration/hive-mind/coordination-matrix.md` — seam × deliverable matrix; cross-seam dependency DAG; concurrent-edit hot-spots; MIGRATION.md cadence
- `agentic_orchestration/hive-mind/phase-1-p1-log.md` — append-only hive log; activation entry + per-seam initial tasking distribution
- `agentic_orchestration/hive-mind/state-of-hive-2026-05-17.md` — activation-day digest

**Per-seam initial tasking distributed** (per scope-of-work § 2):
- Rocket: Deliverable 1 (substrate identity loader + 7-YAML extraction) — Layer-1 foundation
- Gamora: Deliverable 7 math note (resistance matrix 7×7; Discipline #1 load-bearing) + cut pending Gate 3b tag
- Star-lord: Deliverable 6 PLAN + scoping doc (LLM prompt structure refactor — highest unknown)
- Drax: Deliverable 27 session-runner readiness + Deliverable 19 planning
- Jack-ryan: continuous-observation rhythm setup + baseline test-suite snapshot
- Gandalf: continuous design-direction availability + Deliverable 20 (grouping-vocab extension; 1 day; gates D6 implementation)

**Standing Matt-disposition queue (surfaced in activation broadcast):**
1. Vendor acquisitions (CraftPix premium + Fellor Crystal + Frostwindz Deathbringer) — blocks D19 implementation
2. VFX scene-needs spec micro-decisions (gandalf open thread) — fold into activation discussion
3. Hive activation timing (knight-rider recommendation: STAGED)
4. Push authorization for 3 baseline tags to origin

**Ship gate (per scope-of-work § 6):** `v1.0-phase-1-p1` tag cut Matt-approved when all 27 deliverables ship + diversity-architecture dominant-cluster success criterion validates + cross-doc updates land + test suite GREEN + retrospective authored.

**Estimated duration:** 8-12 weeks per gandalf invocation; knight-rider re-scopes after Week-1 seam assessments.

**Files updated:** This CHANGELOG entry; hive-mind/ directory created with 4 artifacts; 3 baseline tags created locally (not yet pushed). No agent-definition or governance-doc changes; hive-mode operates over baseline topology per protocol § 2.2.

---

## 2026-05-17 — Substrate-expansion Branch A confirmed: canonical-four → 6 (Phase-1 P1); vocab freeze standing constraint

**Event:** Gandalf 2026-05-17 escalation on substrate-level genre-positioning surfaced the canonical-four (fire/water/earth/wind) substrate as below-ARPG-genre-floor. Compounding evidence: Case D Fire_Lord thunder math-impossibility resolved Day-4 via mini-boss tier-bump was a symptom of missing substrate, not an isolated case; legolas Track A REVERSE TIER 1 expansion candidates concentrate in beyond-canonical-four substrates (5 of 5: holy/electric/poison/void/shadow); spirit-swap differentiation as load-bearing per 2026-05-08 design intent argues for >4 archetype identities; earth-meta-layer / ascended-spirit / Earth-self thematic framing aligns naturally with luminance axis (Solo Leveling, Bleach, Mushoku Tensei healing-light reference cluster); ARPG-vs-JRPG Day-4 commitment direction.

**Decision (Matt-confirmed Branch A 2026-05-17; gandalf design doc landed `1df535b`):** Expand canonical-four → 6 substrates in Phase-1 P1. Substrate naming + light/dark treatment LOCKED per gandalf design doc:
- + **`lightning`** as own substrate (not wind-flex). Genre-canon across D2-D4/PoE/Last Epoch/Grim Dawn. Closes Case-D pattern at substrate level.
- + **`holy`** and **`shadow`** as TWO distinct substrates (PAIRED-LUMINANCE-AXIS, not collapsed single-luminance). Rationale: paired-opposition mirrors Mirror/Body-swap/Passage triadic cosmology; ARPG-genre archetype fidelity (D2 Paladin vs Necromancer; D4 Necromancer-vs-Holy); legolas reverse-audit shows distinct VFX coverage for holy-radiance vs shadow-tendril.
- Defer poison/acid (earth-flex adequate; Phase-2 candidate).
- Decline void (anti-substrate; boss-exclusive only via trial-room gallery permit).
- VS2a/VS2b ship on canonical-four explicitly. NO scope creep into in-flight visual surfaces.
- Final substrate set (6): **fire / water / earth / wind / lightning / holy / shadow** (Phase-1 P1 target state).

**Standing constraints in effect:**

1. **Vocab freeze (operational ask #1, Matt-authorized 2026-05-17):** seven substrate-distinct entries MUST NOT be promoted to allow-list under wind/earth flex pending Phase-1 P1 substrate landing:
   - **thunder, lightning, bolt** (electric substrate; will land at expansion)
   - **holy, divine** (light substrate)
   - **shadow, umbra** (dark substrate)
   - Any future pool-promotion dispatch (rocket, knight-rider-authored, or otherwise) MUST check against this freeze list before recommending allow-list promotion under canonical-four flex
   - Freeze duration: until Phase-1 P1 substrate-expansion dispatch chain ships

2. **Rocket Drift-14 pool-cull dispatch — HOLD LIFTED 2026-05-17 (post-design-doc-landing); awaits Matt fire-approval:**
   - At `agentic_orchestration/dispatches/2026-05-17-rocket-drift-14-pool-cull-and-selector-hardfloor-amendment.md`
   - Substrate-expansion design doc landed (commit `1df535b`); HOLD condition satisfied
   - Amendment scope: D1 rubric extension ships `substrate_native` as third dimension alongside `canonical_pair_leak` + `vfx_catalogue_mapping_clean`
   - **Pool D1 re-score scopes 156 entries across full 6-substrate target state** (fire/water/earth/wind/lightning/holy/shadow), per gandalf substrate-expansion doc § 5.2
   - **CRITICAL: vocab freeze REMAINS ACTIVE during re-score.** Re-score scopes the TARGET STATE the freeze will lift to (when Phase-1 P1 substrate-expansion ships). The 7 frozen entries (thunder/lightning/bolt/holy/divine/shadow/umbra) re-score to substrate-native primary slots BUT do not lift to allow-list until Phase-1 P1 activates the 6-substrate runtime.
   - VS2a/VS2b runtime selection stays canonical-four-bounded (selector allow-list filter unchanged)

**Phase-1 P1 dispatch chain (queued per gandalf cascade order; knight-rider sequences after decisions-log entry lands per gandalf recommendation to draft post-rocket-Drift-14-fire):**

Cascade order per gandalf substrate-expansion doc § 6:
1. ✅ Design doc COMMITTED (`1df535b` 2026-05-17)
2. **Decisions-log entry** (knight-rider drafts AFTER rocket Drift-14 fires so log references unified state; gandalf reviews)
3. **Rocket Drift-14 amendment fires** (awaits Matt approval)
4. **Pool D1 re-score** (within Drift-14 dispatch; scopes 6-substrate target state)
5. **VS2a + VS2b ship on canonical-four** (unchanged; substrate-orthogonal)
6. **Phase-1 P1 dispatch chain:**
   - Rocket: resistance-matrix extension 4×4 → 6×6 (engine-side; symmetry + paired-luminance valence handling per design doc)
   - Rocket: substrate-coherent generation rules
   - Jack-ryan: resist-matrix-extension review (Discipline #1 math-before-code; stress-test on architectural assertion)
   - Gamora: balance-loop modifier table extension + spirit-swap differentiation math validation for **3 new substrate-archetypes (lightning + holy + shadow)** — paired-luminance means holy + shadow are distinct classes, not merged (per gandalf doc § 5.2 correction)
   - Drax: loadout + demo surface updates for 6-substrate selection (deferred to Phase-1 P1, NOT VS2a/VS2b)
   - Star-lord: LLM prompt-template extension for 6-substrate vocabulary
   - Elrond: D1 pool schema extension for `substrate_native` flag + trait-architecture extension (3 new class trait pools per dual-source design 2026-05-12)
   - Gear-affix gating extension (rocket; D1 affix pool expansion across 6 substrates)
7. **Revisit poison/acid as P2 candidate** post-Phase-1 P1

**Freeze enforcement infrastructure (advisory; gandalf surface 2026-05-17):**
- Consider adding `freeze_list` check to dispatch-authoring Gate 1 checklist (knight-rider territory)
- Consider adding `freeze_list` check to pool-curation Gate 2 review (jack-ryan territory)
- Optional: rocket Drift-14 amendment could include `freeze_list_member` boolean as fourth D1 dimension (surface to rocket scoping as side-note, not blocking)
- Gandalf will audit pool weekly during Phase-1 P1 as backstop

**Vendor acquisitions (Matt-authorized 2026-05-17 — VFX track per gandalf Track B Section 3 + Matt override on Frostwindz; ENVIRONMENT track per legolas Mode B sweep):**

**VFX track:**
- **CraftPix premium (wood-nature substrate)** — ACQUIRE HIGH PRIORITY. Gates earth-slot rebuild after biological-organic cluster cull (+5-8 allow-list entries projected: root/bark/leaf/petal/vine/moss/lichen/wood).
- **Fellor Crystal pack (gem cluster)** — ACQUIRE MED PRIORITY. Reinforces 13-entry crystal/gem/precious-metal cluster the cull KEEPS.
- **Frostwindz Deathbringer (bone)** — ACQUIRE per Matt override 2026-05-17. Gandalf Track B initially DEFER'd citing canonical-four-bounded biological-organic drift concern. Matt reframe: under expanded 6-substrate cosmology (Branch A above), bone/death/skeleton VFX has natural home in **shadow substrate** (necromancy / lich / shadow-monarch / earth-meta-layer ascended-spirit register) — not forced into earth-flex where the drift concern lives. Sequencing: acquire alongside Phase-1 P1 substrate-expansion dispatch chain so VFX assets land on disk before shadow-substrate selector/render wiring needs them.

**Environment tileset track (Matt-authorized 2026-05-17 post-legolas Mode B sweep):**
- **Foozle Lucifer Dungeon** — ACQUIRE IMMEDIATELY (FREE CC0). Drax pipeline-testing baseline; cost-free option-value; 32×32 retro register acceptable as pipeline baseline pending HD-2D-quality VS2a pack acquisition.
- **Kokoro Reflections Reaper Tileset** — ACQUIRE ($9.99). Death/undead palace/fog theme; 48×48 exact-meter-fit; HD-2D-ADJACENT (gandalf visual inspection needed before VS2a commit).
- **Kokoro Reflections Phoenix Tileset** — ACQUIRE ($9.99). Fire/volcanic palace/lava theme; 48×48 exact-meter-fit; HD-2D-ADJACENT.
- **Kokoro Reflections Naga Tileset** — ACQUIRE ($8.99; richest content 13 MB). Serpentine/water palace/marble theme; 48×48 exact-meter-fit; HD-2D-ADJACENT.

Total environment track cost: ~$29 ($28.97 + free baseline). Kokoro Reflections vendor has 2 additional themed palace packs not surfaced by name in legolas Mode B Top-5 (legolas surfaced 3 of 5; remaining 2 can surface in next legolas session if Matt wants full 5-pack acquisition).

**Downstream cascade for environment tileset acquisitions:**
1. Matt action: license/cost payment for the 3 Kokoro packs
2. Asset download + on-disk placement at `~/Games/reincarnated-demo/public/assets/<vendor>/<pack>/`
3. Drax ingest-pipeline extension for environment tilesets (separate knight-rider-authored dispatch; analogous to monster-ingest pipeline)
4. Gandalf Track B environment-tileset framework authoring (next session per per-seam discipline; gandalf visual-inspect Kokoro samples; Matt VS2a selection)
5. Drax integration: room/hallway renderer extension consuming environment-pack manifest at season-load time (Phase-1 P1 timeline per gandalf commission Track D)

**Files updated:** This CHANGELOG entry; rocket Drift-14 dispatch HOLD note. Gandalf design doc + decisions-log entry pending. Gandalf substrate-expansion design doc should cross-reference Frostwindz acquisition as already-in-hand dark-substrate VFX precedent.

**Cross-references:** Drift-14 cascade (Track A original + Track B + Track A REVERSE); Case D math-impossibility (Fire_Lord V1 mini-boss tier-bump per gandalf 8a89d1b § Case 4); Drift-15 commission (8a89d1b); Engine Option C 4-phase plan (substrate expansion sits Phase-1 P1, not VS2a/VS2b in-scope); Trait architecture 2026-05-12 (dual-source design extends naturally to 6 with per-class intrinsic pool authoring cost noted).

---

## 2026-05-16 — Dispatch Gate-1 rubric codified for knight-rider self-discipline

**Event:** Matt and knight-rider reconciled Gate-1 application during Day-4 close. Strict reading of `knight-rider.md` (Dispatch authoring requirements) says every Pattern B dispatch routes through jack-ryan DESIGN-MODE before publishing. In practice during fast-moving sessions, knight-rider had been bypassing this when Matt's directive was explicit.

**Decision:** Accept the practical cadence; codify the rubric for when Gate-1 IS required so the bypass isn't ad-hoc.

**INVOKE jack-ryan Gate 1 when ANY of:**
- Cross-seam empirical/code investigation (math-before-code per Discipline #1)
- Strategy doc that will produce decisions-log entries
- Conflict-risk with locked decisions or canonical docs
- Specialist work >2-3 hours of complex scope (cost of misdirection is high)
- Schema migrations affecting multiple consumers
- Matt's directive is loose (knight-rider inferring scope, not executing instruction)

**BYPASS when ALL of:**
- Matt's directive is explicit and well-scoped
- Single-seam ownership, clear authority
- Reversible / low blast radius
- No new design positions encoded
- Specialist has straightforward execution path

**Retrospective application** (Day-4 session): 7 of 9 bypasses were principled; 2 of 9 (gandalf form-bias-cadence strategy + star-lord tier-1 coverage investigation) should have invoked Gate 1. The two misses were in the highest-stakes categories — strategy doc + cross-seam empirical — which is exactly where the rubric now triggers INVOKE.

**Operational cost of Gate 1:** ~15-30 min for a Pattern A subagent of jack-ryan with the draft dispatch as the prompt. Cheap insurance against multi-hour specialist misdirection.

**Files updated:** No agent-definition files touched (the rubric is in this CHANGELOG; knight-rider applies via self-discipline). If the rubric proves stable through subsequent sessions, fold into `knight-rider.md` Dispatch authoring requirements as a formal section.

---

## 2026-05-16 — Dispatch-flow discipline reinforced: flagged-but-not-dispatched items route through knight-rider

**Event:** During Day 4, star-lord performed an opportunistic session-scan pass and autonomously executed the `summary_formatter.py` `actual_winrate` → `convergence_winrate` fix that gamora had flagged as a cross-seam item. The fix was technically correct — in-seam (star-lord owns `output/`), mathematically grounded by B10.4 Option 2 semantics, Discipline #12 honored via explicit comment — but bypassed the dispatch flow.

**Why this matters:** The team's review process depends on every substantive change being attributed to a knight-rider-authored dispatch with explicit acceptance criteria, required-reading, and (where applicable) Gate 1 review. Specialists picking up flagged-but-not-dispatched items breaks the audit trail:
- Lost attribution — work appears in commits but doesn't trace to a dispatch
- Missed Gate 1 — Matt's pre-execution awareness is bypassed
- Audit gap — the retrospective can't reconstruct "what was approved when"

**Rule, normative across all specialist agents:** if a specialist notices an open item in a handoff, an AGENT_STATE cross-seam flag, or any carry-forward queue that is in their seam but has no knight-rider-authored dispatch, **they do NOT pick it up autonomously**. They surface it to knight-rider and request a dispatch. The cost of asking is tiny.

**Knight-rider's role:** when a specialist surfaces a flagged item, knight-rider's response is usually inline-rapid — a small dispatch authored in the same conversation turn. The bottleneck is not authoring time; it's attribution discipline.

**Files updated:** `.claude/agents/star-lord.md` (added the rule under Agent-specific rules). The rule should propagate to other specialist agents (rocket, gamora, drax, elrond, legolas) the next time their definitions are touched — non-blocking sweep.

---

## 2026-05-16 — Parallel-session `git add -A` race condition (new failure mode)

**Event:** During Day 4, knight-rider staged a decisions-log.md edit + L157 cosmetic fix on the engine repo, then ran `git commit` with a substantive multi-line message documenting the 7-entry batch landing. The commit failed with `nothing added to commit but untracked files present`. Investigation showed that star-lord's parallel session — running in another terminal at the exact moment — had executed its own commit (`9e3a458 chore: update AGENT_STATE — c1f02ca hardening + research-db cleanup complete`) which **swept knight-rider's staged decisions-log changes into star-lord's commit**.

**Functional outcome:** All decisions-log content landed correctly on main (the diff in `9e3a458` matches what knight-rider staged exactly). But attribution is ambiguous: the commit message describes star-lord's AGENT_STATE work, while the diff contains the gate-cleared decisions-log batch. Knight-rider's intended commit message — which would have made the landing visibly attributable in git log — was lost. No corrective action taken because `9e3a458` is already pushed to `origin/main` and amending would require force-push.

**Root cause:** Star-lord (or its commit helper) used a wide staging pattern (`git add -A` or `git add .`) that picked up any staged changes in the working tree rather than naming specific files. Combined with two terminals committing to the same repo in the same minute, this guaranteed cross-session contamination.

**Mitigation going forward:**
1. **Specialists must stage by explicit file path** — `git add path/to/file` not `git add -A` / `git add .` / `git commit -am`. Already mentioned in knight-rider's commit protocol but never required of specialists. This makes it normative for all agents.
2. **Knight-rider should not commit engine files while another agent session is committing in the same repo.** When both are running concurrently, knight-rider waits for the other session to settle (or dispatches the commit to the specialist instead of doing it directly).
3. **Specialist commit messages should describe ONLY their own staged changes** — if the message says "chore: update AGENT_STATE" but the diff also touches `decisions-log.md`, that's a smoke signal worth checking pre-commit.
4. **Consider a pre-commit hook** that lists changed files vs the commit message to catch attribution mismatches. Out of scope for today; flagged for future tooling work.

**Files updated:** No new files. Lesson captured here + in `skill_handoff_2026-05-16.md`.

---

## 2026-05-16 — Catalogue work patterns codified: authority tiers, viability gate, score-don't-filter

**Event:** Three structural patterns governing the new agents' catalogue work were locked. These extend the team's operating discipline and address concrete failure modes surfaced during the demo1 phase.

**Pattern 1 — Authority tiers explicit.** The team now has four authority tiers codified in AGENTS.md:
- Tier A: senior critics/stewards (gandalf, jack-ryan) with escalation privileges
- Tier B: orchestrator (knight-rider)
- Tier C+: implementers with steward authority within their domain (elrond — data architecture)
- Tier C: implementers/specialists (Guardians + legolas)

Elrond explicitly sits at C+, not A. He owns data architecture within his seam authoritatively but does not critique outside it. Escalation through knight-rider only; no parallel-to-Matt privilege.

**Pattern 2 — Viability gate for catalogue work.** Before any full Legolas catalogue crawl, a three-track sample review:
- Structural (elrond) — metadata, schema-fit, license, decomposition signal
- Wiring (drax) — pixi.js consumption viability
- Design (gandalf) — thematic and style-register coherence

All three must pass. Addresses the demo1 failure mode where agents brought back sprites that couldn't be wired due to missing body/head/weapon decomposition.

**Pattern 3 — Score-don't-filter for catalogue data.** Legolas crawls widely; assets are scored by style register as curated metadata; the locked style register becomes a **consumption-time filter**, not a crawl-scope constraint. Preserves pivot flexibility — if engine/story/design/experience needs shift the style register, the catalogue already contains the data.

**Elrond's first major task locked:** comprehensive data-architecture audit before any new schema work. Audit covers all data stores across all four repos; produces baseline at `research/curated/data-architecture-audit-<date>.md`; grounds all subsequent Elrond work.

**Files updated:** `gandalf.md` (style-register scope addition); `legolas.md` (viability-gate protocol + score-don't-filter + expanded metadata schema); `elrond.md` (authority tier C+ codified; data-architecture audit as first task; viability-gate structural-track role); `AGENTS.md` (authority tiers + viability-gate + score-don't-filter as team-level patterns).

**Files created:** `research/knowledge/asset-catalogues/2026-05-16-pixijs-compatible-2d-vfx-libraries.md` (external research contribution captured as durable knowledge — Tier 1/2/3 element vocabulary, source list, style-register observations).

---

## 2026-05-16 — Three agents added: gandalf, legolas, elrond (6 → 9 entities)

**Event:** The synthetic engineering team expanded from 6 entities to 9, adding generative-side design critique, research, and data stewardship capabilities.

**Agents added:**

- **`gandalf`** (Opus) — Story and Design Steward. Generative-side peer to jack-ryan. Pushes back hard on design drift; recommends thematic and player-experience improvements proactively. Layered persona: White Wizard, cross-development-house veteran (anime/isekai houses, founding Diablo team across all four PC titles + Immortal). Has parallel-escalation privilege — can recommend rescoping to knight-rider AND Matt simultaneously. Two-phase onboarding (read project + immediate preliminary deliverable, then post-Legolas-research updated deliverable).

- **`legolas`** (Sonnet) — Researcher and Scout. Two modes: Mode A analytical research (web, genre knowledge, design retrospectives); Mode B systematic catalogue crawl (2D sprite libraries, Unity Asset Store, etc.). Read-only across all sources; outputs structured findings to `agentic_orchestration/research/`.

- **`elrond`** (Opus) — Data Steward. Owns external/cross-cutting data layers (research DB, catalogue DB, abstraction-analysis tables). Schema design, curation, emergent-grouping analysis. Boundary with star-lord at engine-side telemetry — coordination via ADR-004 (MIGRATION.md).

**Rationale:**

- The form-bias deep dive (2026-05-14) surfaced a real gap on the generative-side of design critique. Jack-ryan stress-tests technical/process; nothing in the prior team stress-tested thematic/experiential dimensions. Gandalf fills this gap.
- The catalogue-based form-bias resolution path (Matt's 2026-05-16 design decision, captured in doc 37 update) requires systematic asset-library crawling at scale plus emergent-grouping abstraction analysis. Legolas + Elrond are the right shape for this work.
- Knight-rider's research-pass improvisations (dispatching star-lord for the fight-log granularity research; ad-hoc Explore agents) were filling a Legolas-shaped gap. Now those passes route through the correct owner.

**Structural patterns established:**

- **Critique-pair pattern:** jack-ryan + gandalf form the two-sided critique pair (technical/process + thematic/experiential). Knight-rider invokes both during decision loops when appropriate.
- **Research + data pattern:** legolas + elrond form the knowledge-acquisition pair. Commissions flow from knight-rider or gandalf; raw output → curated structure → abstraction analysis.
- **Gandalf's parallel-escalation asymmetry** with jack-ryan is intentional and codified. Design issues escalate to Matt directly; technical issues route through knight-rider. Revisit if asymmetry causes friction.

**Files created:**
- `.claude/agents/gandalf.md`
- `.claude/agents/legolas.md`
- `.claude/agents/elrond.md`
- `agentic_orchestration/research/` directory tree (subdirs: knowledge/, catalogue/, commissions/, curated/, scripts/) with README

**Files updated:**
- `agentic_orchestration/AGENTS.md` — topology 6 → 9 entities; new seam descriptions
- `canonical/37-form-bias-diagnosis-and-recovery.md` — catalogue design decision incorporated (Matt's 2026-05-16 update)

**Immediate next step:** gandalf first-invocation Phase 1 (read project + produce preliminary bullet-point deliverable across Overall Game Design, Player Journey, Storytelling/Dramatic Themes). Phase 2 follows after Legolas Mode-A research returns.

---

## 2026-05-16 — Catalogue-based form-bias resolution path (doc 37 update)

**Event:** Matt locked a design decision that reshapes the form-bias work's empirical resolution path.

**Decision:** The 3-consumer CV-3D-generation approach (file 29's highest-risk item) is replaced as the primary path by a **catalogue-based mapping** approach for both 2D and 3D content. Crawl all major 2D sprite libraries + Unity Asset Store; build catalogue database with per-asset metadata (cost, license, dimensions, style); analyze for emergent groupings; use groupings as the engine's embodiment vocabulary.

**Rationale:**
- Validates against demo1's already-working JSON-to-sprite mapping pattern
- Retires the highest-risk CV-3D-generation item
- Makes form-bias resolution **empirical** rather than aspirational — abstractions are derived from what catalogues actually contain, not from what designers wish existed
- Quality gate: ~25% seasonal failure rate acceptable; non-conforming seasons discarded; one-week cohesion floor sufficient (not perfect form match)

**Implications:**
- Closes doc 37 § 10.2 open #4 ("Unit of embodiment variation") empirically
- Provides empirical grounding mechanism for doc 37 § 6 cipher architecture
- Structurally enforces Discipline #13 — catalogue IS the structural constraint, not a conversational pillar that can drift
- Spins up the legolas + elrond agent pair to execute the research and analysis

**Status:** Active; doc 37 updated; legolas + elrond agents created to execute.

---

## 2026-05-16 — Permission allowlist switched to bypassPermissions mode

**Event:** `~/.claude/settings.json` `defaultMode` switched from `"acceptEdits"` to `"bypassPermissions"`.

**Change:** All permission prompts now skipped globally. Deny list (18 destructive operation patterns) still enforced. Allow list retained as documentation of expected normal operations.

**Rationale:** Routine permission prompts were creating significant workflow friction without commensurate safety benefit. The deny list is the actual safety floor — it catches the operations that matter (force-push, hard-reset, rm-rf, sudo, dd, mkfs, chown/chgrp, force-clean, force-delete-branch). Everything else is friction.

**One-time activation:** First session after the change requires user acceptance of the bypass-mode confirmation dialog. Subsequent sessions don't re-prompt.

**Reversibility:** Trivial — revert to `"acceptEdits"` or `"default"` if the bypass mode produces unexpected behavior.

---

## 2026-05-15 — Form-bias structural diagnosis captured (doc 37 draft 2)

**Event:** Major design conversation between Matt and knight-rider produced a structural diagnosis of humanoid-form bias in the engine, with five positions locked in conversation and six open questions identified.

**Artifact:** `canonical/37-form-bias-diagnosis-and-recovery.md` (draft 2) — incorporates jack-ryan Gate 1 PASS WITH FLAGS findings and Matt's position-locks.

**Locked positions (in doc 37 draft 2):**
- Position C — slot-as-functional-mechanic + embodiment-as-narrative-skin
- Position (ii) — abstracted mechanical signatures; cipher = resistance-translation only
- Smart-loot in-season + spirit-conversion post-Phase-0
- Three body-swap gear rules (Trial / doppelganger / death)
- Ailment-damage-signatures re-activated as load-bearing dependency under Position (ii)

**Diagnosis framing:** This is **structural realignment to realize latent design intent**, not a pivot — the project name "Reincarnated," the Spirit Guide module name, and the originating isekai premise all carried non-humanoid intent that drifted humanoid via implementation defaults. Per jack-ryan WARN 1: scope is multi-seam schema migration (ADR-004 territory), not documentation cleanup.

**Rationale:** Catching structural drift before it ossifies into more seasons of generation. The diagnosis surfaced two engineering-discipline candidates (#13 implicit-pillar drift, #14 internal-vs-generative schema separation) — both have multiple empirical instances in the project, strengthening the case for codification.

**Status:** Working positions captured; **next steps gated on Matt's cadence choice (Option I/II/III)**. Decisions-log entries + Discipline #13/#14 drafts queued.

---

## 2026-05-15 — Discipline #13 + #14 candidates surfaced

**Event:** Two engineering-discipline candidates emerged from the form-bias diagnosis with multiple independent empirical instances.

**#13 — Implicit-pillar drift.** Design intent that isn't structurally enforced drifts during implementation. Counter: pillars must be structurally enforced (schema, tests, dispatch acceptance criteria, or decisions-log entries). *"We agreed in conversation"* is not enforcement.

**#14 — Internal-vs-generative schema separation (reviewable check).** When introducing or modifying any LLM-visible category, the prompt-construction code must not expose canonical mechanical labels — per-instance vocabulary only.

**Empirical instances backing the candidates:**
- Spirit-swap as non-humanoid pillar → drifted humanoid via gear/class axes
- Form-agnosticism implicit in project name → drifted humanoid via implementation defaults
- Canonical four = "Earth-realm cipher only" → leaked into seasonal flavor surfaces
- D1 rubric = "Earth-realm humanoid-fantasy element naming" → never named, drifted unexamined

**Status:** Drafted in doc 37; pending Matt approval for `engineering-disciplines.md` addition.

---

## 2026-05-15 — Permission allowlist consolidated to user-level

**Event:** `~/.claude/settings.json` updated with comprehensive permission rules covering all four repos in the Reincarnated ecosystem.

**Change:** 98 allow rules + 18 deny rules + `defaultMode: "acceptEdits"` + `additionalDirectories` covering reincarnated-collaboration, reincarnated-engine, reincarnated-demo, reincarnated-loadout.

**Rationale:** Per-repo `settings.local.json` files had accreted ad-hoc allows over many sessions, with inconsistent coverage. User-level consolidation applies uniformly across all agents and all repos. Destructive operations (force-push, hard-reset, rm-rf, etc.) remain denied — safety preserved.

**Impact:** Reduces routine prompts for all future agent sessions. Sessions running at the time of the change did NOT pick up the new rules; only new sessions get the benefit. Per-repo `settings.local.json` files retained (additive to user-level).

---

## 2026-05-15 — Dispatch protocol gaps surfaced (two process flags)

**Event:** Two distinct dispatch-pickup failure modes were exposed during Day 2 execution. Both warrant template fixes in `agentic_orchestration/dispatches/README.md`.

**Failure 1 — Grep-heuristic false positive (drax).** Drax used `grep -l "## Completion record"` to detect completed dispatches at session start. The dispatch template contains `## Completion record` as a section header for instructions to be filled in — the grep matched the literal header regardless of whether anyone had filled it in. Drax silently skipped the v0.5.1 dispatch and started Tier 3 housekeeping; self-corrected after Matt prompted.

**Failure 2 — HELD-status language ambiguity (drax v0.6).** The v0.6-encounter-viz dispatch was marked **HELD** in the prior session's handoff. Drax read "HELD" as *"wait for the metric data that may inform the mechanism viz"* and executed anyway (interpretation: the dispatch's actual scope didn't depend on the metric data, so HELD didn't apply to it specifically). Work was sound; process miss only.

**Fix to land in dispatches/README.md:**
1. Add explicit `**Status:** PENDING` header to dispatch template — flips to `COMPLETE` only when completion record is filled in. Agents check `Status:` field, not section-header presence.
2. HELD-dispatch language must explicitly state: *"Do not execute. Knight-rider will confirm when this dispatch is active."* No ambiguity.

**Status:** Captured but not yet implemented across template + existing dispatches. ~30 min of work for the next session.

---

## 2026-05-14 — Tag protocol clarified: milestone tags require knight-rider confirmation at closure

**Event:** ADR-003 tag protocol tightened based on Day 1 operating experience.

**Ruling (Matt, 2026-05-14):** Milestone tags (no seam prefix, e.g., `v1.3-b10-2-pack-proxy`) require developer to **pause and confirm with knight-rider before cutting the tag**. Knight-rider escalates to Matt if the scope warrants it. Upfront dispatch approval is NOT sufficient on its own — confirmation is required at closure time.

**What triggered this:** gamora tagged `v1.3-b10-2-pack-proxy` on dispatch-approval authority without a closure check-in. Tag was retrospectively valid (dispatch named it as acceptance criterion and Matt approved the dispatch), but the process gap was identified.

**Going forward:** All dispatch scope checklists will include an explicit "Confirm with knight-rider before cutting milestone tag" item. Seam-prefix intermediate tags (e.g., `gamora/v1.3-b10-2-pre-impl`) remain developer-autonomous.

---

## 2026-05-14 — Working branch convention updated: stage-a2 → main (engine)

**Event:** Matt directed that all engine development continue on `main` going forward. `stage-a2` branch is retired as the active working branch.

**Change:** `CLAUDE.md` §Key conventions updated — "Working branch (engine): `stage-a2`" → "Working branch (engine): `main`".

**Rationale:** Engine was already on `main` at Day 1 startup (post-B10.1 merge). Aligning the documented convention to reality avoids ambiguity for all agents reading CLAUDE.md. Existing tags (e.g., `v1.3-b10-1-structure`, `v1.3-b14-5-secondary-loop`) remain valid; new tags will be cut from `main`.

**Impact:** All specialist agents (gamora, rocket, star-lord) should treat `main` as the base branch. Tag protocol (seam-prefix intermediates, Matt-approved milestones) unchanged.

---

## 2026-05-13 — Team established (Day 0)

**Event:** Founding of the 6-entity synthetic engineering team.

**Entities:**
- Matt (Senior Architect, human)
- knight-rider (Opus, orchestrator)
- jack-ryan (Sonnet, analyst/QA)
- rocket (Sonnet, content generation)
- gamora (Sonnet, simulation + spirit_guide)
- star-lord (Sonnet, output/telemetry/llm)
- drax (Sonnet, presentation: demo + loadout)

**Founding documents:**
- `AGENTS.md` — topology, scope map, 7 cycle-trimming tactics
- `GOVERNANCE.md` — 8 founding ADRs
- `REVIEW_PROCESS.md` — 5 principles + change lifecycle + file-type rules
- `skill_handoff_2026-05-13.md` — Day 0 project state snapshot
- `.claude/agents/<name>.md` — 6 agent definition files

**Rationale:** Solo development hit four recurring bottlenecks (context-load tax, cross-seam misalignment, Matt as review bottleneck, late-caught design-principle violations). The team is structured to attack all four via specialization + durable handoffs + tiered review. Primary goal: trim dev cycles. Secondary goal: enable parallelism across genuinely independent seams.

**Pre-history:**
- 2026-05-12 — first BOOTSTRAP_AGENTIC_TEAM.md drafted in `~/Games/reincarnated-collaboration/`. Initial bootstrap session run, partially completed (6 agent files drafted), then terminated. Partial state cleaned and backed up to `.bootstrap-backup-2026-05-13/agents-partial/`.
- 2026-05-13 — strategic review identified that the bootstrap's seam-split had three issues (no loadout owner, star-lord seam too wide, no cycle-trimming tactics). Path B (direct artifact drafting with Matt review) chosen to address.

**Initial state of project:**
- Engine on `stage-a2` branch, tag `v1.3-b14-5-secondary-loop` + `v1.3-b10-1-structure`
- Loadout production URL live at `https://reincarnated-loadout.vercel.app`, tag `v0.3.3-sample-gear`
- Demo (demo1) shipped 2026-05-08
- Most recent season: Yomi (`season_002328`), validation passed
- 12 engineering disciplines codified
- Decisions-log captures all locked design decisions

**Next milestone:** First operational session (planned for 2026-05-14). Two candidate first tasks: gamora B10.2 + drax loadout gear effects. Both have clear scope and contained risk.

---

## How to extend

Append entries above this section. Date format: `YYYY-MM-DD`. Title format: brief noun phrase describing the event. Body: what changed, why, references.

Examples of events that warrant an entry:
- New ADR adopted or existing ADR amended
- Agent added, removed, or scope re-allocated
- Tactic adoption confirmed or revised (e.g., "MIGRATION.md pattern proved valuable in 5 of 5 cross-seam changes — keep")
- Authority delegation expanded or restricted
- New repo added to team scope

Examples of events that do NOT warrant an entry (these belong in their respective git repos):
- Individual feature commits
- Bug fixes
- Routine deploys
- Per-seam tag events (unless milestone level)
