# Dispatch — 2026-05-30 — star-lord — Cycle 14 v1 wave-close emit-pipeline extension

**From:** knight-rider (per gandalf surface 2026-05-30; routing recommendation Item 1)
**To:** star-lord
**Authority:** Matt (PENDING fire-signal — scope-amendment post-v1-close per CLAUDE.md addendum "scope-amendment commits require fresh Matt-authorization")
**Hive-state:** ACTIVE candidate — wave-close scope-extension (Cycle 14 v1 SHIPPED 2026-05-29 commit `2d20b2c`)
**Status:** PENDING
**Auto-commit:** YES upon fire (per CLAUDE.md addendum 2026-05-25)
**Auto-push:** PENDING per-workstream-pattern re-establishment (last cycle's push pattern closed at v1 ship)

---

## Surfacing context

Gandalf surface 2026-05-30 (this session): Loadout app /loadout + /sample pages render blank skills + blank gear + 100/10/10/10 stat fabrication for Cycle 14 wave-5 seasons. **Not a drax bug.** Drax adapter cleanup dispatch (commit `d97462f`) closed correctly per its §v1.67 scope. The gap is: engine emits real data at phase2_kit_candidates layer; the emit pipeline drops it to placeholder per a narrower-than-engine emission scope.

Empirical confirmation (knight-rider 2026-05-30):
- `phase2_kit_candidates.json` carries 54 kits
- Each kit has **12 full-schema skills** (id, abilities, composition_mode, energy_cost, cooldown_seconds, effects, geometry, timing, triggers, damage_multiplier, range_m, spatial_geometry_type, role, canonical_element, effect_category, color_value, power_tier, scaling_attribute, tier, chain_id)
- Each kit has **11 gear_representative slots** (main_weapon, secondary_item, head, chest, hands, feet, legs, amulet, ring_1, ring_2, belt)
- Only `investment_points` are uncomputed (0 across all 648 records — correct deferred to Cycle 15+ per gandalf)

**Cumulative Disc #42a Instance 6 pattern surface #8 candidate:** "engine emits real data that downstream pipeline drops to placeholder because emit-pipeline scope was bounded narrower than engine emission scope." Same family as Phase 4 → Phase 5 disjoint (Path X fix) and Phase 5 element_distribution aggregator (rocket fix landed 04:49 UTC).

---

## Required reading (before authoring code)

1. `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` §v1.67 — current emission scope (what to extend)
2. `~/Games/reincarnated-engine/src/reincarnated/export/cycle14_wave5_emitter.py` — the emitter to extend
3. `~/Games/reincarnated-collaboration/canonical/49-loadout-sample-player-surface-design-2026-05-27.md` § 1.1.1 (Rank-0 amendment), § 1.2 (Sample tab Cycle 15+ scope)
4. `~/Games/reincarnated-collaboration/canonical/47-damage-scaling-architecture-2026-05-27.md` § 4 — stat distribution architecture (primary attribute + scaling ratios vs 100/10/10/10 fabrication)
5. `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-30-cycle-14-wave-5-loadout-blank-surfaces-routing.md` (companion gandalf note if filed; otherwise use this dispatch's surfacing context section as authoritative)
6. `~/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-wave-5-season-001/phase2_kit_candidates.json` — the data source to propagate
7. `~/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-30-drax-cascade-r4-v1-session-end-adapter-cleanup.md` — drax-side context (what's already in place)

---

## Scope

Extend `cycle14_wave5_emitter.py` to propagate from `phase2_kit_candidates.json` into per-season `classes/*.json` output for all 3 Cycle 14 wave-5 seasons (season-001, season-002, season-003).

### Work-item 1 — Skills propagation (12 per kit)

Replace single-placeholder-skill emission with all 12 real skills per kit from phase2_kit_candidates.json `kits[i].skills[0..11]`.

**Required fields per skill:** id, abilities, composition_mode, energy_cost, cooldown_seconds, effects, geometry, timing, triggers, damage_multiplier, range_m, spatial_geometry_type, role, canonical_element, effect_category, color_value, power_tier, scaling_attribute, tier, chain_id.

**investment_points:** stays `0` per Wave 1/2/3 deferred to Cycle 15+ (gandalf confirmation in surface). Schema field exists; emit as 0. Drax will render per doc 49 § 1.1.1 Rank-0 amendment (rank-0 uninvested presentation).

**phase5_is_placeholder:** retire from emitted skill records (this was the single-placeholder flag; with 12 real skills, the flag is misleading). Replace with `investment_state: "rank_0_uninvested"` per doc 49 § 1.1.1 nomenclature.

### Work-item 2 — Gear propagation (11 slots per kit)

Replace `main_weapon: null` + `secondary_item: null` + (likely other null slots) with full propagation of `kits[i].gear_representative.{main_weapon, secondary_item, head, chest, hands, feet, legs, amulet, ring_1, ring_2, belt}`.

**Required fields per gear instance:** rarity, partition_modifiers, capability_modifiers, substrate_binding (and any other fields present in phase2 emission; copy the full structure).

### Work-item 3 — Stat distribution (replace 100/10/10/10 fabrication)

Per doc 47 § 4, replace `stat_distribution` fabrication with one of two approaches (star-lord chooses; jack-ryan Gate-1 validates choice):

**Option A — Primary attribute name + scaling ratios:**
```json
"stat_distribution": {
  "primary_attribute": "dex",
  "scaling_ratios": {"dex": 1.0, "str": 0.1, "int": 0.1, "vit": 0.1},
  "computation_mode": "scaling_ratios"
}
```

**Option B — Null + live-calc flag:**
```json
"stat_distribution": null,
"stat_computation_flag": "live_calc_pending"
```

**Recommendation:** Option A is preferred — drax can render meaningful primary-attribute callout without engine-side investment computation. Option B punts the render decision downstream. Per doc 47 § 4 authoritative reading (star-lord verifies before choosing).

### Work-item 4 — Update `placeholder_skill_content` manifest flag

With 12 real skills emitted per kit, `placeholder_skill_content: true` is no longer accurate. Change to `placeholder_skill_content: false` at manifest level. Drax amber banner will need text update OR removal — drax dispatch (companion) handles drax-side change.

**Note on banner:** the v1-close banner stays accurate at v1 ship moment ("skills are substrate-derived placeholders"); this dispatch closes the v1-close architectural gap by making the skills real (so banner text becomes inaccurate post this dispatch's fire).

### Work-item 5 — MIGRATION.md amendment

Author MIGRATION.md §v1.68 (or appropriate next section number) documenting the scope-extension. Required content:
- What §v1.67 emitted (placeholder)
- What §v1.68 emits (12 real skills + 11 real gear slots + scaling-ratio stat distribution)
- Drax-side coordination: `placeholder_skill_content` flag flips; banner text changes (companion drax dispatch)
- Cycle 15+ deferred items: `investment_points` computation, full convergence-loop balance metadata, color_palette, seasonal_dominant_element, t4_alteration_output, engine_version

### Work-item 6 — Re-emission

Re-fire `cycle14_wave5_emitter.py` against all 3 Cycle 14 wave-5 seasons. Write directly to `~/Games/reincarnated-loadout/data/` per §v1.67 (a) cross-seam write path. Verify:
- 158 class files updated (54 + 53 + 51)
- Each class file's skills array has 12 entries (not 1)
- Each class file's gear slots populated (main_weapon, secondary_item, head, chest, hands, feet, legs, amulet, ring_1, ring_2, belt all non-null with full structure)
- Stat distribution reflects Option A (or chosen approach) — not 100/10/10/10
- Manifest `placeholder_skill_content: false`

---

## Cross-seam impact

- **drax (downstream):** Loadout tab + Sample tab render real 12-skill structure (rank-0 uninvested) + gear catalog. Companion drax dispatch at `2026-05-30-drax-cycle-14-v1-wave-close-render-verification.md` handles render verification + banner text update.
- **Sample tab scope (gandalf reminder):** Sample tab stays placeholder for Cycle 14 v1 per doc 49 § 1.2 — Sample requires AS-gauntlet-passed investment commit which is Cycle 15+ scope. Real 12-skill emission is for Loadout tab (rank-0 uninvested rendering). Drax dispatch enforces this scope boundary.
- **Analytics tab:** Already consuming `balance_metadata.actual_winrate` + `quality_vector` + `cohort` from §v1.67 — this dispatch does not affect analytics.
- **Encounters tab:** Out of scope (gamora Cycle 15+ work).

---

## Math-before-code requirements (Discipline #1)

This dispatch is mostly data-plumbing (propagation from phase2 → classes/*.json). No new computation. Discipline #1 not triggered at the propagation layer.

**Exception — stat_distribution scaling ratios:** if Option A is chosen, the scaling ratio values (1.0 / 0.1 / 0.1 / 0.1) need a one-paragraph justification citing doc 47 § 4. Either:
(a) These ratios come from doc 47 § 4 as canonical — cite the section
(b) These ratios are a fresh decision — flag to gandalf + jack-ryan Gate-1 before fire
Star-lord must verify (a) before authoring. If (b), escalate to Gate-1.

---

## Smoke-test expectation (Discipline #2)

Before full re-emission:
1. Run emitter against season-001 ONLY (smallest scope; 54 kits)
2. Spot-check 3 class files: 12 skills present + 11 gear slots populated + stat_distribution non-fabricated
3. Verify total file size stays well under 100KB per file (current max ~2.5KB; extension may bring max to ~15KB — verify against KR oversized-file trigger)
4. Re-run if smoke-test fails; do NOT proceed to seasons 002 + 003 until 001 smoke passes

---

## Acceptance criteria

- [ ] 158 class files re-emitted with 12 skills + 11 gear slots each
- [ ] stat_distribution per Option A (or chosen approach) — not 100/10/10/10 fabrication
- [ ] Manifest `placeholder_skill_content` flipped to `false` for all 3 seasons
- [ ] MIGRATION.md §v1.68 authored documenting scope extension + Cycle 15+ deferred items
- [ ] Smoke-test PASS on season-001 before seasons 002 + 003 fire
- [ ] No class file exceeds 100KB
- [ ] Tag: `star-lord/v1.X-cycle-14-v1-wave-close-emit-pipeline-extension-1` (version number per star-lord seam state)
- [ ] Engine tests still PASS (45 tests in test_cycle14_wave5_loadout_emission.py; some may need amendment for new skill/gear schema — author or amend tests as part of this dispatch)

---

## Out of scope (explicit guard against scope creep)

- `investment_points` computation (Cycle 15+ scope per gandalf)
- Phase 5 LLM re-fire for canonical_skill_names (not the gap being closed here)
- Color palette generation (Cycle 15+ scope)
- Seasonal cipher (`seasonal_dominant_element`) (Cycle 15+ scope)
- Substrate-binding run for `t4_alteration_output` (Cycle 15+ scope)
- Sample tab AS-gauntlet-passed investment commit (Cycle 15+ scope per doc 49 § 1.2)
- Encounter sim emission (gamora Cycle 15+ scope)
- Drax-side render verification (companion drax dispatch)

---

## Pattern A-deep verdict request (gate before fire)

**Gate 1 routing:** This dispatch SHOULD route through jack-ryan DESIGN-MODE Gate-1 before fire because:
- Scope-amendment post-v1-close (per CLAUDE.md addendum, fresh Matt-authorization required)
- Stat-distribution Option A vs Option B choice — needs doc 47 § 4 alignment verification
- `phase5_is_placeholder` retirement vs amendment — Discipline #12 semantic-shifting risk (semantic shift in emitted skill records)
- Cumulative Disc #42a Instance 6 pattern surface #8 candidate registration

**Gandalf Pattern A-deep verdict request:** confirm Sample tab scope-boundary (stays placeholder for Cycle 14 v1) + confirm doc 49 § 1.1.1 Rank-0 amendment is operational for drax-side render.

---

## Completion record (to be appended on close)

**Status:** PENDING fire-signal
**Authored:** 2026-05-30 by knight-rider
