# State of Hive — QD-Engine Rebuild

**Hive:** QD-Engine Rebuild (continuous single-hive operating mode)
**Activation:** 2026-05-21 by gandalf activation dispatch
**Owner:** knight-rider (autonomous orchestration)
**Expected duration:** 24-37 weeks
**Update cadence:** Every phase boundary + major workstream completion; ad-hoc on structural surfaces.

---

## 1. Current phase: P0 — Constraint Removal + Drift Cleanup

**Phase state:** P0 OPEN — 7 of 9 dispatches authored + active. gandalf attestation 2026-05-21 cleared all framing-approval blockers; Matt's prior approvals (Confirm § 2.9 / Confirm § 2.8 / substrate-as-cohesion ratification) are attested on record. Track C synthesis absorbed; uniform-depth enrichment confirmed for P1 W1.11.
**Phase duration estimate:** 3-4 weeks (with W0.9 added per § 2.9 of activation dispatch)
**Phase tag namespace:** `qd-rebuild/v0.X-<descriptor>`
**Milestone tag at phase close:** `v0.0-constraint-removal-shipped`

### P0 workstream roster (9 workstreams)

| ID | Description | Owner | Status | Dispatch | Tag |
|---|---|---|---|---|---|
| W0.1 | **B14.5 V2 energy-type lever in primary recompose loop** (LC-004 calibration-side fix; complements B6 pre-work already shipped 2026-05-16 at `rocket/v1.3-b6-energy-type-tiers`); gandalf endorsed B14.5 V2 follow-on interpretation per matt-briefing § 4 | gamora | DISPATCH ACTIVE | `2026-05-21-gamora-w0-1-b14-5-v2-energy-type-lever.md` | `qd-rebuild/v0.1-b14-5-v2-energy-type-lever` |
| W0.2 | Archetype template Path-a refactor (LC-001; REMOVE templates entirely under substrate-as-cohesion-only) | rocket | DISPATCH ACTIVE | `2026-05-21-rocket-w0-2-archetype-template-path-a-refactor.md` | `qd-rebuild/v0.2-archetype-refactor-complete` |
| W0.3 | Foundation validator update (LC-012 fix; D5 = 7-substrate) | rocket | **🔄 IN-FLIGHT (background worktree; agentId a6f39f540799283a6)** | `2026-05-21-rocket-w0-3-foundation-validator-d5.md` | `qd-rebuild/v0.3-foundation-validator-7-substrate` |
| W0.4 | Specialist code audit (12 HIGH-risk LCs verify; 18 MEDIUM-risk follow-up; INCLUDES § 2.8 W1.13 current-state verification + OQ-2 + OQ-3 per Alt A) | rocket + gamora + star-lord; jack-ryan reviews | **🔄 PARTIAL: star-lord portion ✅ COMPLETE 2026-05-21** (engine tag `star-lord/v1.15-w0-4-code-side-audit-1`); rocket + gamora portions queued. Critical findings surfaced — see § 2.2.2 below. | `2026-05-21-rocket-plus-gamora-plus-star-lord-w0-4-specialist-code-audit.md` | `qd-rebuild/v0.4-code-side-audit-complete` (hive tag fires when all 3 seams + jack-ryan reviews) |
| W0.5 | Mana-bug verify (LC-026 quick verify; ~2 hours) | gamora | **✅ COMPLETE 2026-05-21 — RESOLVED** — engine commit `4bce461`; tag `qd-rebuild/v0.5-mana-bug-verify-resolved` pushed. Phase 1 dimensional refactor (2026-05-08 commit `4c28ed6`) structurally resolved at pool-assignment + skill-costing layers. 152 tests PASS. Substrate-as-cohesion compatibility CONFIRMED. **Residual:** `base_stamina` column never written by `recorder.py` — flagged for star-lord W0.4 in-flight. | `2026-05-21-gamora-w0-5-mana-bug-verify.md` | `qd-rebuild/v0.5-mana-bug-verify-resolved` (FIRED) |
| W0.6 | Drift candidate closures (LC-006, LC-007, LC-014, LC-028) | jack-ryan DESIGN-MODE primary + gandalf architectural disposition | **✅ FULL CLOSURE 2026-05-21** — engine commit `2b1b9a6`; tag `qd-rebuild/v0.6-drift-closures-complete` fired (supersedes -partial). LC-006 graduated to full closure per gandalf disposition (D3 cohesion-judge architecturally clean; Option B + Option-C label-emission sliver). | `2026-05-21-multi-seam-w0-6-drift-candidate-closures.md` | `qd-rebuild/v0.6-drift-closures-complete` (FIRED) |
| W0.7 | LC-002 + LC-009 + LC-011 ablation experiments | gamora | DISPATCH ACTIVE (queued; jack-ryan Gate-1 per ablation) | `2026-05-21-gamora-w0-7-ablation-experiments.md` | `qd-rebuild/v0.7-ablation-complete` |
| W0.8 | Axis 2 substrate completeness check (~2-3 hours; map 16-type palette to 5-bin Axis 2; identify per-bin gap to 5× rule) | rocket | **✅ COMPLETE 2026-05-21** — collab commit `d7544bf`; tag `qd-rebuild/v0.8-axis-2-substrate-check` pushed | `2026-05-21-rocket-w0-8-axis-2-substrate-check.md` | `qd-rebuild/v0.8-axis-2-substrate-check` (FIRED) |
| **W0.9** | **Gauntlet architecture migration** (NEW per § 2.9; retire PackProxy ×8; true multi-monster positional gauntlet as default; ~1-2 weeks) — **gandalf-attested Matt-approval "Confirm § 2.9 edit"** | gamora | **🔄 Phase 1 + Phase 1.5 COMPLETE**; tag `qd-rebuild/v0.9-math-note-phase-1-complete` fired (engine commit `edcac29`). 7 amendments folded. Phase 2 kickoff pending: (a) gandalf magic/elite/mini-boss scenario definitions (A8); (b) star-lord schema v2.14 migration spec (A5 + LC-003). | `2026-05-21-gamora-w0-9-gauntlet-architecture-migration.md` | `qd-rebuild/v0.9-gauntlet-migration-complete` (final) |

### P0 sequencing plan

**Front-loaders (cheap; can fire in parallel):** W0.1, W0.5, W0.8.
**Substantial work (takes most of phase duration):** W0.2 (archetype refactor — simpler now under substrate-as-cohesion) + W0.4 (specialist code audit, broadest scope).
**Trivially actionable:** W0.3 (single validator function update).
**Closure phase:** W0.6 (drift candidates) + W0.7 (ablations).
**New scope (blocked-on-Matt):** W0.9 (gauntlet architecture; framing approval required before fire).

### P0 critique-pair structure

- W0.1 + W0.2: jack-ryan reviews before rocket fires (design intent verification)
- W0.4: gandalf reviews seam-by-seam findings (cross-seam coherence)
- W0.5 + W0.7: jack-ryan reviews ablation experiment design before fires
- W0.6: critique-pair sequence per drift item (gandalf design-side, jack-ryan dev-side)
- W0.9: gandalf reviews architectural alignment ("fix the arena" principle); jack-ryan reviews migration correctness (PackProxy retirement complete; Discipline #13a drift check); **Matt approves framing before fire**

---

## 2. Hive-wide operational state

### 2.1 Tag namespace established

- `qd-rebuild/v<X.Y>-<descriptor>` — intermediate tags (knight-rider autonomous)
- `v<X.0>-<phase-name>-shipped` — Matt-approved milestone tags (one per phase boundary)
- `v8.0-qd-engine-final` — production cutover tag (W7.5)

### 2.2 Phase progression overview

| Phase | Name | Duration | Status |
|---|---|---|---|
| **P0** | Constraint Removal + Drift Cleanup | 3-4 wk | OPENING (current) |
| P1 | Substrate Enrichment (incl. NEW W1.13 skill tree node population) | 5-8 wk | PENDING |
| P2 | BC Measurement Infrastructure | 3-4 wk | PENDING |
| P3 | MAP-Elites Archive Implementation | 2-3 wk | PENDING |
| P4 | Sim Extensions for Deferred Bins | 4-6 wk | PENDING |
| P5 | Theme Coalescence + Cohesion-BC + Visual-BC | 3-5 wk | PENDING |
| P6 | Profile Assembly Layer | 2-3 wk | PENDING |
| P7 | Validation Gauntlet + Production Cutover | 2-3 wk | PENDING |

### 2.2.2 W0.4 star-lord portion findings (folded into downstream consumers)

Per W0.4 star-lord portion completion 2026-05-21 (engine tag `star-lord/v1.15-w0-4-code-side-audit-1`; collab commit pending this push):

**Per-LC verdicts (star-lord seam):**
- **LC-006 (canonical-four LLM exposure)** — **RESOLVED**. Cipher migration is fully live in `llm/naming.py`. All 4 naming functions route through `_grouping_label()` + `_seasonal_element_line()` — no canonical-four label reaches any LLM prompt. Test guard at `tests/test_no_canonical_four_in_llm_prompts.py`. `canonical_element` fields in export schemas marked DEPRECATED (intentional backward-compat). Rocket's `element/selector.py` + `canonical/library_generator.py` sites pending rocket W0.4 portion verification.
- **LC-007 (humanoid gear schema in export)** — **VERIFIED (not yet fixed)**. `export/schemas.py:88-89` carries `slot/handedness` humanoid values; `telemetry/migrations.py:_V1_6` persists same. Position C migration not shipped. Cross-seam fix requires coordinated rocket → star-lord → drax MIGRATION.md.
- **🚨 LC-003 (modifier floor-lock) — DRIFT-FROM-AUDIT — CRITICAL CROSS-SEAM GAP.** `floor_lock_recompose`, `working_modifier`, `floor_lock_detected` are specced in gamora's `simulation/MIGRATION.md` (Option B floor-lock recovery fields) but **ABSENT from star-lord's `migrations.py` + `recorder.py`**. If gamora re-enables Option B (currently soft-disabled), these fields will be silently dropped at the telemetry boundary. **Disposition:** fold into W0.9 schema v2.14 migration scope (W0.9 already plans v2.13 → v2.14 bump for true-multi-monster sim telemetry; LC-003 fields ride along). Cross-reference noted for gamora W0.9 math note + jack-ryan Gate-1 review.
- **LC-008 (STR/DEX/INT LLM visibility)** — **NEEDS-DOWNSTREAM-FIX**. `naming.py:323` passes `stats.as_dict()` directly into `name_class` user prompt; raw stat labels reach LLM. Separate fix dispatch required for per-embodiment narrative reframing.

**§ 2.8 W1.13 ArchiveEntry schema extension scope (for P1):**
- None of 7 ArchiveEntry fields (`node_subset`, `per_node_coefficients`, `scalar_modifier`, `bc_coordinate`, `per_tier_WR`, `cohesion_theme`, `visual_identity`) exist in star-lord tables
- **NEW `archive_entries` table required** — NOT an ALTER of existing tables
- Export schema change not needed until P3
- Folded into P1 W1.X telemetry-extension scope; star-lord owns the migration

**W0.8 `bounce_count` + `spawn_count` for P1 W1.1:**
- `abilities` table has no `bounce_count` or `spawn_count` columns
- Clean additive ALTER TABLE migration; 4 files (`migrations.py`, `recorder.py:_insert_skill()`, `schemas.py:ExportSkill`, `season_exporter.py:_build_skill()`); ~20 LOC
- No round-trip breakage risk (Pattern P7 defensive getattr at recorder boundary)
- Folded into P1 W1.1 scope; star-lord coordinates with rocket at boundary

**Schema state confirmed:**
- v2.12 + v2.13 LIVE in production DB as of 2026-05-19; no drift from AGENT_STATE records

**No new HIGH-risk LCs surfaced — no § 7.4 phase-halt trigger.**

### 2.2.1 W0.8 findings (folded into downstream consumers)

Per W0.8 completion 2026-05-21 (collab commit `d7544bf`):

- **Aggregate per-bin gap:** ~58-64 distinguishable templates vs ~125 target (49-52%). Chain ~21-22 gap (HIGH); multi-spawn ~19-20 gap (HIGH); single-target ~13 gap (MEDIUM); large-AOE ~5-7 gap (MEDIUM); small-AOE ~3-5 gap (LOW).
- **24 enrichment seed candidates authored** (12 chain C-1..C-12 + 12 multi-spawn M-1..M-12). All substrate-AGNOSTIC. Folds into P1 W1.5 (movement-skill expansion) + P1 W1.7 (legolas Phase 2 depth pass) + P1 W1.11 (substrate-themed cohesion access).
- **OQ-7 water DPS density disposition:** M-3 (N=8 radial burst), M-8 (meteor shower), C-4 (control chain with CC rider) recommended for water cohesion access. Substrate-AGNOSTIC at generation; cohesion-judge assigns water label post-generation per substrate-as-cohesion architecture. P1 W1.11 must ensure these templates exist in the pool.
- **NEW schema fields recommended for P1 W1.1 (Ability schema extensions):** `bounce_count` (int; chain_lightning + ricochet_bounce) and `spawn_count` (int; multi_projectile + totem). Without these, bounce-count distinguishability cannot be measured at BC-assignment time — all chain_lightning kits would classify identically regardless of bounce depth.
- **Total geometry inventory:** 28 VALID_GEOMETRIES entries (canonical-09 final table says 26 due to counting methodology; code is authoritative at 28). 23 damage-bearing; 5 non-damage (blink, roll, defensive_dash, teleport, self_buff).
- **Multi-bin edge cases resolved:** leap_strike → small-AOE (landing impact); cone → small-AOE (2-3 tile depth); aura → large-AOE (4-8 tile radius); totem → multi-spawn (placed independent damage entity, not Axis 2A proxy AI). summon_combatant out of scope (Axis 2A territory; deferred per axis-lock § 5).

### 2.3 Background dispatches in flight

- **Track C resumption** — **SYNTHESIS LANDED 2026-05-21 ~10:03 EDT** at `canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md` (gandalf commit `623f8a3`). Key findings:
  - OQ-1 resolved: COLLAPSE — substrate severity gradient is CALIBRATION ARTIFACT, not substrate-intrinsic
  - **P1 W1.11 scope: UNIFORM comprehensive enrichment depth** confirmed (saves ~1-2 weeks vs differentiated approach)
  - § 2.8 + § 2.9 empirically validated as necessary, not optional
  - New OQ-6 (physical hunter modifier ceiling) + OQ-7 (water DPS density) for downstream attention (P7 W7.2 + P1 W1.11 scoping respectively)
  - Knight-rider absorbed; folded into P1 W1.11 scope-finalization (no new dispatch needed)
- **Monster thematic depth assessment** (Legolas + Galadriel + gandalf synthesis dispatch at `agentic_orchestration/dispatches/2026-05-21-monster-thematic-depth-assessment.md`) — QUEUED to fire post-P0 open.

### 2.4 Matt-blocking items

| Item | Surfaced | Status |
|---|---|---|
| W0.9 gauntlet architecture migration framing approval | 2026-05-21 hive activation | **CLEARED** — gandalf attestation 2026-05-21 § 3.1 (Matt 2026-05-21 "Confirm § 2.9 edit"); W0.9 dispatch ACTIVE |
| W1.13 skill tree node population framing approval | 2026-05-21 hive activation | **CLEARED** — gandalf attestation 2026-05-21 § 3.2 (Matt 2026-05-21 "Confirm § 2.8 edit"); fires at P1 boundary |
| W0.2 archetype template Path-a refactor (structural per protocol § 6.1.5) | 2026-05-21 activation | **CLEARED** — gandalf attestation 2026-05-21 § 3.3 (implicit approval via substrate-as-cohesion ratification "1 = yes / 2 = yes / 3 = yes / all 3 confirmed. Free to write."); W0.2 dispatch ACTIVE |
| W0.1 scope interpretation | 2026-05-21 activation | **CLEARED** — gandalf attestation 2026-05-21 § 4 (endorses B14.5 V2 follow-on; operationally correct empirical inspection finding); W0.1 dispatch ACTIVE |
| Per activation dispatch § 5: structural architecture changes / procurement >$100 / production cutover (W7.5) / Discipline #18 ratification / Profile A ship-blocker / axis-lock v1.1+ revision | — | none currently pending |

### 2.5 Engine state (carry-forward from recompose-hive close)

- Option A floor widening: ACTIVE (`MODIFIER_SEARCH_FLOOR = 0.01`)
- Option B recompose-trigger: INSTALLED + SOFT-DISABLED (`LEVER_FLOOR_LOCK_WORKING_MODIFIER = MODIFIER_SEARCH_FLOOR`)
- 179/179 tests PASS
- Schema v2.13 telemetry active
- No rollback executed
- Tag `recompose-hive/v1.1-canonical-record-complete` fires on this session's commit (engine + collab parity)

### 2.6 Discipline state

- Disciplines #1-#17 LIVE
- **Discipline #11.1 — State-space conditioning of empirical signals** (NEW; ratified 2026-05-21 per gandalf P3 § 9.6 recommendation; folded into engineering-disciplines.md)
- **Discipline #18 — Joint-gate ship criterion** — CANDIDATE (registered 2026-05-21; ratification deferred to P5 W5.6 pending empirical evidence from cohesion-BC + visual-BC archives)
- R11(b), Pattern P7, Pattern P6.a continue LIVE
- Sibling-cluster-sweep lesson continues LIVE
- Terminology Lock continues LIVE

---

## 3. Cross-references

- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` — the activation dispatch
- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — vision
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — operational 8-axis spec
- `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate-as-cohesion architecture
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` — 8-phase workflow
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — phased rebuild plan
- `reincarnated-engine/design/decisions/decisions-log.md` — 2026-05-21 activation + #11.1 + #18 entries
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — § 11.1 ratified
- `agentic_orchestration/hive-mind/retrospective-recompose-validation.md` — recompose-hive canonical close
- `agentic_orchestration/CHANGELOG.md` — 2026-05-21 hive activation + recompose-hive closure entries
- `agentic_orchestration/knight-rider/daily/2026-05-21.md` — phase-progress log for this session

---

*State-of-hive doc maintained continuously by knight-rider. Updated on every phase boundary + major workstream completion + Matt-surface event.*

**Last updated:** 2026-05-21 (hive activation; P0 opening)
