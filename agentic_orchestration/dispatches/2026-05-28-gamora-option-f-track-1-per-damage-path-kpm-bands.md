# Dispatch — 2026-05-28 — gamora — Option F Track 1: Per-damage-path KPM bands (4 archetypes × 4 cohorts = 16 calibrated values; ~0.5 day)

**From:** knight-rider
**To:** gamora (simulation seam owner; B14.5 V1 calibration loop infrastructure)
**Approved by:** Matt 2026-05-28 verbatim D1 RATIFIED Option F Track 1 + D2 REJECTED Option B scaffold-fallback ("scaffolds get RESOLVED, not deliberately introduced") + D3 DEFERRED to Cycle 15 entry per Discipline #18 refinement
**Estimated effort:** ~0.5 day gamora empirical sweep
**Acceptance:** 4-archetype × 4-cohort = 16 calibrated KPM band values landed; ≥12/18 Phase 2 kits emit under per-damage-path bands; smoke-test PASS; tag `gamora/v1.9-option-f-phase-1-stratified-floor-1` retires (superseded by Track 1)

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** close 7th Cycle 14 scaffold-drift case (cross-damage-path DPS variance) by calibrating KPM bands per damage-scaling PATH (mechanical partition per doc 47 § 3) — preserves substrate-led discipline (mechanical not class taxonomy) + resolves underlying scaffold per Matt D1 framework discipline ("scaffolds get RESOLVED, not deliberately introduced") + composes with Cycle 15 Track 2 architectural target per D3 deferral. Composes "Engine first. Game second. Phase third." — engine-layer per-path calibration protects Phase 7 quality-filter authority across damage-scaling variance.

**Refutation conditions:**
- Per-archetype calibration produces <12/18 emit (16 band values insufficient for substrate-emergent DPS variance within archetype)
- 4-archetype partition doesn't compose cleanly with existing cohort midpoint median estimator (jack-ryan canonical re-write firing in parallel may need bridge text)
- Empirical sweep surfaces 8th scaffold-drift case (would warrant D7 re-evaluation per Matt D2 hook)

## Context

**Authority chain:**
- Matt 2026-05-28 D1 verbatim: "Option F Track 1 — per-damage-path KPM bands (4 archetypes × cohorts = 16 calibrated values). Architectural anchor: 4 damage-scaling PATHS per doc 47 § 3 (STR-physical / DEX-physical / INT-magical / WIS-faith) are MECHANICAL partition, NOT class taxonomy. Discipline #45 compliant. Discipline #13a substrate-led partition permitted."
- Jack-ryan SC7-F1 Gate-3 disposition `044f4ea` + Gate-4 disposition `ce65b22` (BLOCK authority + Option F Track 1 recommendation)
- Your Option F Phase 1 completion at engine `80a4417` + `de86e9b` (stratified floor + KPM=600.0 bypass; Parts 1-3 STAND; Part 4 smoke surfaced 7th case)
- Your SC-7 calibration at engine `e7af7db` (single reference INT/WIS magical class calibrated; Track 1 supersedes for cross-path coverage)
- doc 47 § 3 damage-scaling path canonical (STR-physical / DEX-physical / INT-magical / WIS-faith)
- Discipline #13a-partition (mechanical partition permitted; substrate-led)
- Discipline #45 vocab lock (4 archetypes = damage-scaling PATHS, NOT class names — compliant)

**Tag retirement:** `gamora/v1.9-option-f-phase-1-stratified-floor-1` retires (Track 1 supersedes); new tag at Track 1 close.

**Framework discipline (Matt D2 rejection rationale):** "Scaffolds get RESOLVED, not deliberately introduced." Track 1 is canonical-decision resolution per Discipline #40 case (c) 6-step retraction; NOT a wider scaffold reintroduction.

**D3 deferral context (Discipline #18 refinement):** methodology consultation at extension hotspots fires AFTER baseline empirical signal lands. Track 1 IS that baseline. Track 2 (Option C damage/HP% vs Option A per-kit) design call deferred to Cycle 15 entry — consumes Track 1 telemetry for architectural commitment.

## Required reading

- `agentic_orchestration/qa/pending/2026-05-28-7th-scaffold-drift-cross-class-dps-gate-4-disposition.md` (jack-ryan Gate-4 disposition; primary authority source)
- `agentic_orchestration/cycle-14-wave-5-season-001/option-f-phase-1-smoke-telemetry.json` (Part 4 smoke evidence; 184/216 T1 REJECT; 3/18 emit; INT/WIS-only passing)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/sc7_calibration_loop.py` (your existing calibration infrastructure; extend for 4-archetype sweep)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (Option F Phase 1 stratified floor; line 85 area)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/sc-7-base-spell-damage-calibration-2026-05-28.md` (your SC-7 math note; § 3 Q-SC7-2 explicitly deferred per-class — Track 1 IS that closure)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 (doc 47 damage-scaling path canonical)
- `agentic_orchestration/cycle-14-wave-5-season-001/phase2_kit_candidates.json` (18 staged kits; archetype attribution)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #13a-partition + #18 + #39 + #40 + #45

## Discipline #46 compliance

- N/A — calibration loop iterations; no DB queries
- EXPLAIN QUERY PLAN at any new telemetry capture queries

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:** (1) 18 Phase 2 kits are correctly partitionable into 4 archetypes per doc 47 § 3 (STR-physical / DEX-physical / INT-magical / WIS-faith); (2) cohort midpoint median estimator composes per-archetype (jack-ryan canonical re-write firing parallel handles canonical authority); (3) per-archetype band ±0.25 absorbs intra-archetype substrate-DPS variance; (4) ≥12/18 emit achievable under 16-value band space
- **Q2 refutation evidence to seek:** verify 18-kit archetype distribution from Phase 2 staging (likely ~4-5 kits per archetype per substrate emergence); smoke against archetype subset before full sweep; verify per-archetype band width still discriminating
- **Q3 outcome trigger:** if <12/18 emit OR 8th scaffold-drift surfaces (intra-archetype variance exceeds band) → invoke #44 framing-refusal + Matt D2-hook re-evaluation

## Scope (4 parts)

### Part 1 — 18-kit archetype partition (~0.1 day)

- [ ] Load Phase 2 staged kits from `cycle-14-wave-5-season-001/phase2_kit_candidates.json`
- [ ] Per-kit archetype attribution per doc 47 § 3 damage-scaling path (STR/DEX/INT/WIS × physical/magical/faith)
- [ ] Verify archetype distribution (expect ~4-5 kits per archetype per substrate-emergence Phase 2 output)
- [ ] Surface unexpected distribution (e.g., 12 INT kits + 0 STR kits) as Discipline #42 framing-audit Q3 trigger

### Part 2 — Per-archetype calibration sweep (~0.25 day)

- [ ] Extend existing `sc7_calibration_loop.py` infrastructure for 4-archetype × 4-cohort sweep
- [ ] Per-archetype empirical KPM range at boss-encounter tier
- [ ] Median estimator per archetype-cohort cell (composes with jack-ryan canonical median estimator)
- [ ] Output: 16-value table `BAND[archetype][cohort] = (midpoint, ±0.25_band)`
- [ ] Telemetry capture at `cycle-14-wave-5-season-001/option-f-track-1-calibration-telemetry.json`

### Part 3 — Gauntlet sim integration (~0.1 day)

- [ ] Update `gauntlet_sim.py` stratified floor logic (Option F Phase 1 architecture STANDS): boss-encounter gate now looks up per-archetype band from 16-value table
- [ ] Per-kit archetype attribution at gate evaluation (read damage-scaling path from kit metadata)
- [ ] KPM=600.0 ceiling bypass UNCHANGED (Phase 1 architecture preserved)
- [ ] Inline comments cross-reference: Matt D1 ratification + jack-ryan Gate-4 disposition `ce65b22` + Track 2 Cycle 15 forward-link (D3 deferred)

### Part 4 — Smoke-test ≥12/18 emit acceptance (~0.05 day)

- [ ] Re-run Phase 3 via rocket's `run_phase3_from_staged_phase2()` with per-archetype bands
- [ ] Verify ≥12/18 Phase 2 kits achieve `season_emit=True` (D1 acceptance criterion)
- [ ] Per-archetype emit distribution capture (target ≥3 per archetype if substrate-emergence balanced)
- [ ] Principle 6 round-trip preserved
- [ ] Discipline #45 grep audit (verify 4-archetype attribution code uses "damage-scaling-path" vocabulary NOT "class")

### Closure

- [ ] Update `~/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
- [ ] **Retire tag** `gamora/v1.9-option-f-phase-1-stratified-floor-1` annotation (Track 1 supersedes; preserve in git history)
- [ ] **New tag** `gamora/v2.0-option-f-track-1-per-damage-path-bands-1`
- [ ] Append completion record to this dispatch + cross-seam co-record with jack-ryan Track 1 canonical re-write (firing parallel)
- [ ] Commit + push per Matt's per-cycle push pattern

## Acceptance criteria

- [ ] 18-kit archetype partition correctly attributed per doc 47 § 3
- [ ] 16-value band table calibrated empirically (4 archetypes × 4 cohorts)
- [ ] Per-archetype gate evaluation operational in gauntlet_sim.py
- [ ] **≥12/18 Phase 2 kits emit under per-damage-path bands** (D1 acceptance)
- [ ] Principle 6 round-trip preserved
- [ ] Discipline #45 vocab CLEAN (damage-scaling-path NOT class)
- [ ] Tag retired + new tag cut + AGENT_STATE.md updated
- [ ] Telemetry artifact filed
- [ ] Completion record + commit + push

## Out of scope

- Do NOT modify SC-7 calibrated BASE_SPELL_DAMAGE_L50 values (engine `e7af7db` STANDS — SC-7 was correct for INT/WIS magical; Track 1 extends, doesn't replace)
- Do NOT implement Track 2 per-kit calibration (D3 deferred Cycle 15 entry)
- Do NOT implement Option C damage/HP% metric (D3 Cycle 15 design call)
- Do NOT modify Phase 4 mechanical archive (engine `749d5aa` LOCKED)
- Do NOT touch Phase 7 IMPL bridge (engine `eca0aa5` LOCKED)
- Do NOT introduce wider band ±0.40 scaffold (Matt D2 REJECTED)

## Open questions for gamora

- **Q-T1-1:** Archetype attribution method — read kit metadata damage-scaling-path field directly OR derive from bc_attribute + weapon_type_family + range? Your judgment per Phase 2 staged kit format
- **Q-T1-2:** Per-archetype median estimator vs per-cohort-per-archetype — your judgment on aggregation level (16 cells = full granularity; 4 cells = archetype-only with cohort-aware band width)
- **Q-T1-3:** 18-kit archetype distribution — if surfaces unbalanced (e.g., 0 kits in DEX archetype), how to populate DEX band? Your judgment per #42 framing-audit Q3

## References

- Matt 2026-05-28 D1+D2+D3 verbatim ratifications
- Jack-ryan Gate-4 disposition `ce65b22` (Option F Track 1 recommended)
- Your SC-7 calibration `e7af7db` (single-class calibration stands; Track 1 extends)
- Your Option F Phase 1 `80a4417` + `de86e9b` (stratified floor STANDS; Track 1 enriches gate evaluation)
- doc 47 § 3 damage-scaling path canonical
- Discipline #13a-partition + #18 refinement + #39 + #40 case (c) + #45

---

## Completion record

### Jack-ryan Track 1 canonical re-write co-completion record

**Recorded:** 2026-05-28
**By:** jack-ryan (canonical re-write authority; firing parallel with this dispatch)

**Phase 7 canonical doc amended:** `reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md`

**Amendments landed:**
- § 3.8: Discipline #40 case (c) SECOND iteration retraction record — single-class-calibrated band RETIRED per Matt D1
- § 3.9: Per-damage-path KPM band canonical (4 archetypes × 4 cohorts; table structure; estimator; composition with stratified floor; Disciplines #13a-partition + #45 verified) — **16 band values PENDING gamora Track 1 telemetry**
- § 3.10: Track 2 D3 deferred Cycle 15 forward-link (Discipline #18 refinement § 18.2 compliance)
- § 3.7 AMENDED: Track 2 D3 deferral context (Option A + Option C as branches; consumes Track 1 baseline)
- STATUS header and §§ 0, 1 updated

**Critical pending action (gamora):** when Track 1 sweep completes and `option-f-track-1-calibration-telemetry.json` is filed, populate the 16 `BAND[archetype][cohort]` placeholder cells in § 3.9 with numeric `(midpoint, ±0.25)` values. The canonical architecture is locked; the numeric values are the only missing element. File a follow-on amendment to the canonical doc with the numeric values + a co-completion record pointer back to this dispatch.

**Jack-ryan dispatch completion record location:** `agentic_orchestration/dispatches/2026-05-28-jack-ryan-phase-7-track-1-canonical-re-write.md` § Completion record
