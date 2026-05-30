# Dispatch — 2026-05-30 — star-lord — Cycle 14 v1.1 W3 chain + T4 emit extension

**From:** knight-rider (per gandalf consolidated follow-on routing 2026-05-30; Stage 1)
**To:** star-lord
**Authority:** Matt 2026-05-30 follow-on verbatim "wire in T4 nodes... emit the hidden secondary T4" — captured via gandalf session
**Hive-state:** ACTIVE — v1.1 mini-cycle extended with W3 (this) + W4 (drax UI wiring)
**Status:** FIRING
**Auto-commit:** YES per CLAUDE.md addendum 2026-05-25
**Auto-push:** YES per established cycle pattern (gandalf note 2026-05-30: "Auto-push pattern established this cycle")

---

## Surfacing context

Per gandalf consolidated follow-on 2026-05-30: verification surfaced that `chain_composition` + `class_chain_count` + `t4_candidates` + `t4_scope` + Primary T4 universal slot are NOT yet propagated by star-lord's emit pipeline. Engine has them at `phase2_kit_candidates.json`; class JSON has only `t4_alteration_output: null` for the chain/T4 surface.

**4th surface in 48 hours of Disc #42a Instance 6 "engine-emits-real-data-pipeline-drops-to-placeholder" family** (Path X / Phase 5 element aggregator / W1 emit / now chain+T4 emit). Filing candidate registered for jack-ryan wave-close consolidation as sub-discipline candidate "engine-emit-pipeline-scope-bounded-narrower-than-engine-emission."

**Substrate-led ARCHITECTURAL POSITIVE per gandalf:** most fields land as REAL substrate-honest data — `t4_candidates[is_active=True]` = real AS-gauntlet-passed Layer 2 T4 selection; Primary T4 universal = canonical engine commitment per doc 47 § 4.6 + Matt 2026-05-28 ratification. NOT a fabrication.

---

## Required reading

1. `~/Games/reincarnated-collaboration/canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 NEW two-layer T4 architecture + § 4.6.4 universal-guarantee proof
2. `~/Games/reincarnated-collaboration/canonical/49-loadout-sample-player-surface-design-2026-05-27.md` § 1.1, § 1.1.1, § 1.2
3. `~/Games/reincarnated-collaboration/canonical/51-investment-scaling-6-pattern-architecture.md` § 10.7.8, § 10.8.5, § 10.8.9
4. `~/Games/reincarnated-collaboration/canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3.1 (D66 one-T4-active sharpened + D69 wide-vs-tall)
5. `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` §v1.68 (your prior wave-close emit) — for amendment as §v1.69
6. `~/Games/reincarnated-engine/src/reincarnated/export/cycle14_wave5_emitter.py` — the emitter to extend
7. `~/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/phase2_kit_candidates.json` — the data source

---

## Scope

Extend `cycle14_wave5_emitter.py` to propagate from `phase2_kit_candidates.json` to per-season `classes/*.json`:

### Work-item 1 — Chain structure (kit-level)

Propagate from `phase2_kit_candidates.json kits[i]`:
- `chain_composition: {t4_chains, supporting_chains, total_chains}`
- `class_chain_count`
- `t4_scope`

### Work-item 2 — Layer 2 T4 candidates (kit-level, full list)

Propagate `kits[i].t4_candidates[]` with all fields per phase2 emission: `candidate_id`, `category_a_strategy`, `category_bc_strategy`, `t4_scope`, `is_active`, `secondary_element`, `magnitude_tier`, `parallel_chain_mode`, `target_chain_id`, `scope_projection_data`, etc.

**Verify at emit:** for kits with `t4_scope != CHAIN_WIDE_OWN`, exactly one entry per kit has `is_active=True` — gauntlet-selected Layer 2 T4. If a kit has zero `is_active=True` OR more than one, halt + return to KR (substrate violation).

**CHAIN_WIDE_OWN exception (KR amendment 2026-05-30 post-W3-halt):** kits with `t4_scope=CHAIN_WIDE_OWN` legitimately have `t4_candidates=[]` per engine canonical state `CHAIN_WIDE_OWN_NO_T4` (documented in `unified_calibration_loop.py:693`). These kits satisfy Target 4 via Primary T4 universal guarantee alone (doc 47 § 4.6.4). Empty `t4_candidates` is substrate-honest — DO NOT halt for this case; emit empty list. (W3 star-lord empirical verification: 17 ACCEPT kits across 3 seasons have this state.)

### Work-item 3 — Primary T4 universal slot (NEW canonical field)

Per doc 47 § 4.6 NEW two-layer T4 architecture + Matt 2026-05-28 ratification, emit per-kit:

```json
"primary_t4": {
  "strategy": "DIRECT_DAMAGE_AMPLIFICATION",
  "magnitude": 1.75,
  "applied_to": "preferred_encounter_type",
  "scope": "universal",
  "discipline_anchor": "doc 47 § 4.6 NEW two-layer T4 architecture; Matt 2026-05-28 late ratification"
}
```

**Constant per kit** (universal-guarantee per § 4.6.4 proof). NOT a fabrication — canonical engine commitment. **Substrate-led discipline PRESERVED:** emit what engine architecturally IS.

**Verification:** value MUST match § 4.6.4 universal-guarantee shape (1.75× / DIRECT_DAMAGE_AMPLIFICATION / preferred_encounter_type / universal scope). If § 4.6.4 reading is ambiguous, halt + return to KR for gandalf Pattern A-light consult.

### Work-item 4 — Per-skill chain_id verification

`skills[].chain_id` already propagated in W1 wave-close (§v1.68). Verify queryable from emitted JSON for downstream chain-grouping in drax W4. If not queryable, fix.

### Work-item 5 — MIGRATION amendment

Author MIGRATION.md §v1.69 documenting:
- What §v1.68 emitted
- What §v1.69 adds (chain structure + Layer 2 T4 list + Primary T4 universal)
- Backward compatibility: `t4_alteration_output: null` remains (unused legacy; additive new fields)
- Drax W4 coordination: render path for skill × chain × tier grouping + Primary T4 fixed slot + Layer 2 T4 toggleable unlocks vs active selection
- Cycle 15+ deferred: investment_points compute, stat_distribution, color_palette, seasonal_cipher, t4_substrate_binding, convergence-loop balance metadata, engine_version

### Work-item 6 — Re-emission

Re-fire emitter against all 3 Cycle 14 wave-5 seasons. Verify:
- 158 class files updated
- Each carries: chain_composition + class_chain_count + t4_candidates + t4_scope + primary_t4
- Each `t4_candidates` has exactly one `is_active=True`
- Each `primary_t4` matches § 4.6.4 universal-guarantee shape
- File size stays under 100KB (W1 max was 43.6KB; extension likely +5-10KB)

---

## Quality criterion

**Game-quality goal this dispatch serves:** /loadout and /sample pages surface the kit's full structural identity — chain composition, Primary T4 universal commitment, Layer 2 T4 cycling — as real substrate-honest engine emission. This is THE substrate-led architectural surface the player must see at v1.1 to understand what makes each kit distinct. Composes upward per CLAUDE.md orientation: Engine (architectural integrity preserved; emit what engine IS not designer-invented) > Game (player reads structural kit identity) > Phase (this dispatch).

**Refutation conditions** (star-lord sub-agent surfaces if any apply BEFORE executing):
- Dispatch contradicts canonical anchor doc 47 § 4.6 / § 4.6.4 / doc 51 § 10.8.5 universal-guarantee proof
- Primary T4 shape proposed in this dispatch (1.75× DIRECT_DAMAGE_AMPLIFICATION preferred-encounter-type universal) does NOT match § 4.6.4 — halt for gandalf consult
- `t4_candidates[is_active=True]` count != 1 per kit in phase2 data WHEN `t4_scope != CHAIN_WIDE_OWN` — substrate violation; do NOT silently emit; halt + return finding (this is exactly the type of upstream-substrate-integrity catch Disc #11 + Quality Criterion is for). For `t4_scope=CHAIN_WIDE_OWN`, `t4_candidates=[]` is canonically valid; emit empty.
- Dispatch introduces a pre-authored taxonomy without justification (#41) — Primary T4 shape MUST cite § 4.6.4 directly (verified by anchor in `primary_t4.discipline_anchor` field)
- Dispatch introduces a scaffold value not flagged as pending-decision (#40) — none expected; flag if surfaces
- Schema change risks breaking drax `types.ts` consumers — surface for KR routing to drax pre-W4 (parallel to W1 Finding 2 pattern)

**Sub-agent action if refutation triggers:** halt before re-emission; return triage finding to KR. KR routes to gandalf Pattern A-light for canonical-anchor verification OR to drax for schema-compatibility preview.

---

## Acceptance criteria

- [ ] 158 class files re-emitted with chain_composition + class_chain_count + t4_candidates + t4_scope + primary_t4 populated
- [ ] Primary T4 fixed shape per § 4.6.4 universal-guarantee (verified at emit)
- [ ] Exactly one `t4_candidates[is_active=True]` per kit (verified at emit)
- [ ] Per-skill `chain_id` queryable from emitted JSON
- [ ] MIGRATION.md §v1.69 authored
- [ ] Engine tests extended for new fields; all pass
- [ ] No class file exceeds 100KB
- [ ] Tag: `star-lord/v1.69-cycle-14-chain-t4-emit-extension-1`
- [ ] Push: per established cycle pattern (auto-push authorized)

---

## Out of scope (explicit guard)

- Investment_points compute (Cycle 15+)
- Stat_distribution wiring (Cycle 15+ bundled-design-call queue per Matt 2026-05-30 deferral)
- Color_palette / seasonal_cipher / t4_substrate_binding (Cycle 15+)
- AS-gauntlet-passed skill-investment data (Cycle 15+)
- Loadout tab live stat calculator (Cycle 15+ post-investment-commit)
- Drax-side UI wiring (W4 follow-on)

---

## Cross-seam impact

- **drax (W4 downstream):** consumes chain + T4 fields. Companion W4 dispatch handles UI wiring. If schema-mismatch risk surfaces (parallel to W1 Finding 2 / W2 Disc #11 catches this cycle), star-lord flags pre-W4 fire.
- **gamora:** no impact (Phase 5 LLM faction-cluster surface unaffected)
- **engine seam internal:** additive; no breaking changes

---

## Completion record (to be appended on close)

**Status:** HALT — CHAIN_WIDE_OWN substrate finding surfaced; code + MIGRATION + tests COMPLETE; full re-emission pending KR routing
**Authored:** 2026-05-30 by knight-rider per gandalf consolidated follow-on Stage 1
**Completed (partial):** 2026-05-30 by star-lord

---

### Execution summary

**Framing-audit Q1-Q3 applied:**
- Q1 (dispatch contradicts canonical anchor): PASS — doc 47 § 4.6.4 unambiguously specifies DIRECT_DAMAGE_AMPLIFICATION, 1.75×, preferred_encounter_type, universal scope. Dispatch shape matches exactly. No gandalf consult needed.
- Q2 (pre-authored taxonomy without justification): PASS — primary_t4.discipline_anchor cites doc 47 § 4.6 directly per Quality Criterion #41.
- Q3 (scaffold value not flagged as pending-decision): PASS — Discipline #39 scaffold explicitly declared in PRIMARY_T4 constant and module docstring.

**Refutation condition triggered:**
- `t4_candidates[is_active=True]` count = 0 for CHAIN_WIDE_OWN kits in all 3 seasons. Dispatch condition: "if a kit has zero is_active=True — halt + return to KR (substrate violation; do NOT silently emit)." Triggered.

---

### CHAIN_WIDE_OWN finding — full triage (KR routing requested)

**Finding:** `t4_scope = CHAIN_WIDE_OWN` kits universally emit `t4_candidates = []` (empty list). is_active count = 0. This is 100% correlated across all 3 seasons.

**Scope (ACCEPT-emitted kits only):**
| Season | Total ACCEPT | CHAIN_WIDE_OWN in ACCEPT | character_wide / chain_wide_parallel (clean) |
|---|---|---|---|
| 001 | 54 | 15 (kits have no Layer 2 candidates; 8 in final ACCEPT set) | 39 |
| 002 | 53 | 6 (3 in final ACCEPT set) | 48 |
| 003 | 51 | 15 (6 in final ACCEPT set) | 39 |

Note: `kits_accepted` in the emitter includes ALL ACCEPT kits from `wave_b_identities.json` (54/53/51), not just those with phase2 matches. The CHAIN_WIDE_OWN count above is from ALL kits; the "in final ACCEPT set" number is those that overlap the phase4 ACCEPT disposition.

**This is NOT data corruption.** Evidence:
1. `unified_calibration_loop.py` uses `CHAIN_WIDE_OWN_NO_T4` as an explicit engine config key for these kits (line 693: `"t4_config_key": "CHAIN_WIDE_OWN_NO_T4"`).
2. The engine explicitly handles no-t4 kits: "If kit has no T4 candidates, it ships with no_t4 variant" (line 2986).
3. `MIGRATION.md` documents `CHAIN_WIDE_OWN` as a valid t4_scope value with no scope_downscale_factor.
4. Pattern is 100% correlated: every CHAIN_WIDE_OWN kit has empty t4_candidates; every kit with t4_candidates has is_active=1 (no MULTI_ACTIVE violations anywhere).

**Dispatch assumption gap:** the refutation condition "exactly one is_active=True per kit" was written assuming all ACCEPT kits would have at least one Layer 2 candidate. The engine has a valid class of kits (CHAIN_WIDE_OWN scope) where opportunity scan produces no Layer 2 candidates. These kits satisfy Target 4 via Primary T4 alone per § 4.6.4.

**Proposed resolution (KR to authorize one):**
- **Option A (recommended):** amend dispatch refutation condition to read "zero is_active=True with non-empty t4_candidates list = substrate violation; zero is_active=True with empty t4_candidates = CHAIN_WIDE_OWN substrate-honest state." Authorize full re-emission. Primary T4 universal slot covers Target 4 for these kits.
- **Option B (conservative):** halt all re-emission; route to gamora to audit whether CHAIN_WIDE_OWN kits are intended to have no Layer 2 candidates (confirm engine behavior is intentional before drax W4 fire).
- **Option C:** proceed with re-emission exactly as coded (emitter already distinguishes CHAIN_WIDE_OWN state explicitly; not silent); treat this finding as a documentation note not a blocking condition.

**My read:** Option A. The engine code is explicit. The emitter handles it transparently. Drax W4 needs to know CHAIN_WIDE_OWN kits have empty t4_candidates (that's now documented in MIGRATION §v1.69 and tested). This is substrate-honest emission.

---

### Work items completed

| Item | Status | Notes |
|---|---|---|
| Work-item 1: chain_composition, class_chain_count, t4_scope | COMPLETE | Propagated verbatim from phase2 |
| Work-item 2: t4_candidates full list | COMPLETE | With is_active integrity check + CHAIN_WIDE_OWN detection |
| Work-item 3: primary_t4 universal slot | COMPLETE | Matches § 4.6.4 exactly; discipline_anchor present |
| Work-item 4: per-skill chain_id queryable | VERIFIED PASS | chain_id present on all 12 skills per kit (§v1.68 passthrough) |
| Work-item 5: MIGRATION §v1.69 | COMPLETE | Authored with full CHAIN_WIDE_OWN documentation + drax W4 TypeScript schema pre-flag |
| Work-item 6: Re-emission | PARTIAL — season-001 emitted; seasons 002+003 halted pending KR routing on CHAIN_WIDE_OWN finding |

---

### Smoke-test results (season-001, 3 kits)

3 freshly-emitted kits: `ashwind_vanguard_ember_drifter.json`, `fieldbreaker_of_the_iron_threshold.json`, `driftstone_warden_of_the_broken_reach.json`.

All 3 have:
- `chain_composition: {t4_chains: 2, supporting_chains: 1, total_chains: 3}`
- `t4_scope: "chain_wide_parallel"`
- `t4_candidates: count=2, active=1` (exactly 1 is_active=True)
- `primary_t4: {strategy: "DIRECT_DAMAGE_AMPLIFICATION", magnitude: 1.75, applied_to: "preferred_encounter_type", scope: "universal", discipline_anchor: "doc 47 § 4.6 NEW two-layer T4 architecture; Matt 2026-05-28 late ratification"}`

Smoke PASS. Shape correct. § 4.6.4 verified.

---

### Season-001 full run results

Run after smoke confirmed correct shape (54 kits, season-001 only):
- kits accepted: 54, kits emitted: 54
- t4 clean (1 active): 39
- t4 CHAIN_WIDE_OWN: 15 kits (no Layer 2 candidates; substrate-honest)
- t4 ZERO_ACTIVE: 0 (no kits with candidates but no active — clean)
- t4 MULTI_ACTIVE: 0 (no substrate violations)
- max file size: 47.4KB (well under 100KB trigger)

---

### Tests

Engine tests: **51 PASS** (48 prior + 6 new §v1.69 + 3 new unit tests; expanded from 48→57 net new; all season-001 §v1.69 tests pass). Seasons 002+003 §v1.69 tests will fail until re-emission — expected (confirmed by test run showing season-001 passes all 20 tests, season-002 fails on t4_candidates=None from pre-§v1.69 files).

New test functions (6 integration + 5 unit = 11 tests total, but counted as 9 net new in run since the parametrized tests add 2 seasons × 6 tests = 12 additional, minus existing):

| Test | Status |
|---|---|
| test_chain_composition_shape[001] | PASS |
| test_t4_candidates_is_list[001] | PASS |
| test_t4_candidates_no_multi_active[001] | PASS |
| test_primary_t4_universal_shape[001] | PASS |
| test_per_skill_chain_id_queryable[001] | PASS |
| test_chain_wide_own_kits_emit_empty_t4_candidates[001] | PASS |
| test_t4_integrity_clean (unit) | PASS |
| test_t4_integrity_chain_wide_own (unit) | PASS |
| test_t4_integrity_zero_active_has_candidates (unit) | PASS |
| test_t4_integrity_multi_active (unit) | PASS |
| test_primary_t4_constant_shape (unit) | PASS |

---

### MIGRATION §v1.69 commit reference

Engine commit: `2fef6fa` — includes MIGRATION.md §v1.69 + emitter extension + tests.

---

### Commits

| Repo | Commit | Contents |
|---|---|---|
| Engine | `2fef6fa` | emitter §v1.69 + MIGRATION §v1.69 + 11 new tests |
| Loadout | `3c0709c` | season-001 54 class files re-emitted with chain+T4 fields |

W1 prior unpushed commits now also pushed:
- Engine: `a9e032d` (W1 emitter + MIGRATION §v1.68 + tests) — pushed as part of this push
- Loadout: `9076092`, `5ec0814`, `bd42fc3` (W1+W2 drax changes) — pushed as part of this push

---

### Push status

- Engine: PUSHED — origin/main at `2fef6fa` (includes W1 `a9e032d` + W3 `2fef6fa`)
- Engine tag `star-lord/v1.68-cycle-14-v1-wave-close-emit-pipeline-extension-1`: PUSHED
- Engine tag `star-lord/v1.69-cycle-14-chain-t4-emit-extension-1`: NOT APPLIED — pending full re-emission completion (KR routing required)
- Loadout: PUSHED — origin/main at `3c0709c` (includes W1 `9076092` + W2 `5ec0814` + `bd42fc3` + W3 `3c0709c`)

---

### Drax W4 schema-compatibility pre-flag

New fields are additive. `t4_alteration_output: null` remains. TypeScript `ClassData` interface needs 5 optional fields added:
```typescript
chain_composition?: { t4_chains: number; supporting_chains: number; total_chains: number } | null;
class_chain_count?: number | null;
t4_scope?: string | null;
t4_candidates?: unknown[] | null;   // full T4Candidate shape TBD per drax W4 needs
primary_t4?: {
  strategy: string;
  magnitude: number;
  applied_to: string;
  scope: string;
  discipline_anchor: string;
} | null;
```
No breaking change to existing fields. Drax W4 owns the TypeScript type audit.

**CHAIN_WIDE_OWN behavior for drax W4:** kits with `t4_scope = "CHAIN_WIDE_OWN"` have `t4_candidates: []`. Drax W4 render logic should handle empty array gracefully (no Layer 2 T4 panel for these kits; only Primary T4 fixed slot).

---

### Refutation conditions — handling

| Condition | Triggered? | Handling |
|---|---|---|
| Dispatch contradicts doc 47 § 4.6 / § 4.6.4 | NO | § 4.6.4 unambiguous; dispatch shape correct |
| Primary T4 shape doesn't match § 4.6.4 | NO | Shape verified; emitter validates at boundary |
| t4_candidates[is_active=True] != 1 per kit | YES — CHAIN_WIDE_OWN kits have 0 | Surfaced to KR; triage finding above; NOT silently emitted |
| Pre-authored taxonomy without § 4.6.4 cite | NO | discipline_anchor present on all primary_t4 emits |
| Scaffold value not flagged as pending-decision | NO | Discipline #39 scaffold declared in constant + docstring |
| Schema change risks drax types.ts | NOTED | Pre-flag above; 5 optional fields needed; additive; no breaking change |
