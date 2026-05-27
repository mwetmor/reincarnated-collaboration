# Dispatch — star-lord — Cycle 13 Track C (REVISED) Step 1 — Normal-Season Export Transform Pipeline

**Date authored:** 2026-05-27
**Authored by:** knight-rider (per Matt directive 2026-05-27 — Cycle 13 Track C REVISED)
**Status:** PENDING
**Cycle:** 13 (post-close additive scope per Matt directive)
**Track:** C REVISED Step 1 (drax Step 2 fires after this completes)
**Authorization:** Matt 2026-05-27 verbatim "continue per-cycle pushes per Matt 2026-05-27 verbatim authorization" + Track C REVISED authorization

---

## 0. Context

**Why this dispatch exists:** The earlier Track B Step 2 (drax commit `4cf8312`) added a "Cycle 13 Characters" gap-fill tab to the Sample page that bypasses the loadout app's normal season-data flow. Matt directs the corrective architectural move: integrate the 16-character `cycle-13-mechanical-season-001` content as a **NORMAL SEASON** in the loadout app's existing `useSeasonData` hook infrastructure, so it flows through to ALL pages naturally (Loadout / Sample / Analytics / Encounters). Then drax retires the gap-fill tab in Step 2.

Star-lord owns Step 1 (the export transform pipeline that produces the loadout-app-consumable season files). Drax Step 2 fires after this completes.

**Matt's framing this as a corrective architectural pass, not a remediation WARN** — earlier Track B Step 2 made an assumption-architectural-choice (gap-fill tab) that turned out to be the wrong direction. Per Discipline #11 + the iterative engineering disciplines, the fix is to land the correct architecture + retire the gap-fill cleanly.

---

## 1. Required reading

1. **`reincarnated-loadout/public/seasons/v2_narrow_phase_5/`** — canonical reference for the target schema (`metadata.json` + `classes.json`). Examine top-level structure + per-class structure + per-skill structure (especially the 21-field skill schema with `bc_axis_contribution`, `canonical_element`, `chain_id`, `cooldown_seconds`, `damage_multiplier`, `effects`, `energy_cost`, `flavor_text`, `geometry_type`, `id`, `name`, `phase5_*` fields, `role`, `seasonal_element`, `spatial_geometry_type`, `tier`).
2. **`reincarnated-loadout/data/sample-season/` + `data/season_002015/`** — the older `data/*/manifest.json + classes/*.json` convention. **CONVENTION CLARIFICATION REQUIRED:** Matt's directive named target as `reincarnated-loadout/public/seasons/cycle-13-mechanical-season-001/` (matching the `public/seasons/v2_narrow_phase_5/` precedent — single `classes.json` flat-list + `metadata.json`). However, `src/hooks/useSeasonData.ts` reads from `../../data/*/manifest.json` (the OLDER convention with per-class JSON files). **You may need to write to BOTH paths** OR write to the `public/seasons/` path per Matt's spec + flag for drax to update the hook in Step 2.
3. **`reincarnated-loadout/src/hooks/useSeasonData.ts`** — read in full to understand selectableSeasons discovery logic + class data loading
4. **`reincarnated-loadout/src/data/types.ts`** — TypeScript types for `ClassData`, `GearPoolEntry`, `SeasonData`, `SeasonManifest`
5. **`reincarnated-engine/output/cycle-13-mechanical-season-001/season_metadata.json`** — top-level season manifest (source)
6. **`reincarnated-engine/output/cycle-13-mechanical-season-001/characters/`** — 16 character JSONs (source)
7. **`reincarnated-engine/output/cycle-13-mechanical-season-001/gear_sets/`** — 16 gear set JSONs (source for gear_pool.json)
8. **`reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json`** — empirical gauntlet sim results (27,360 fights / 16 kits / 912 encounters; canonical path post W2 fix). Optional source for Analytics page consumption.
9. **`reincarnated-loadout/MIGRATION.md`** — current sections (especially § v2.0 + § v2.1 for the cycle13_characters.db + Cycle 13 Sample page consumer)
10. **`reincarnated-engine/src/reincarnated/export/MIGRATION.md`** — engine-side star-lord MIGRATION; add new § for this Step 1
11. **`canonical/46-concentration-architecture-2026-05-27.md`** § 6 (if it discusses cohesion-judge layered architecture) — for the placeholder-per-skill-content rationale
12. **`canonical/story/phase-5-cohesion-judge-calibration-spec-2026-05-25.md`** — context on what Phase 5 cohesion coalescence will populate in Cycle 14 (so your placeholders are well-formed in anticipation)

---

## 2. Scope — sequential steps

### Step 1 — Inventory + schema reconciliation

Read 2-3 v2_narrow_phase_5 class entries + 2-3 cycle-13 char JSONs side by side. Map:
- v2_narrow_phase_5 fields → cycle-13 char source field
- Where source data is missing (the placeholder skills), what synthetic value to emit
- Per-skill schema (21 fields) → which come from cycle-13 substrate (chain composition, T4 metadata, BC cell) vs which are synthesized placeholders

### Step 2 — Write the transform pipeline

Author at `reincarnated-engine/src/reincarnated/export/cycle13_normal_season_export.py` (or appropriate location per existing export patterns):

```python
def transform_cycle13_to_normal_season(
    engine_season_dir: Path,     # reincarnated-engine/output/cycle-13-mechanical-season-001/
    gauntlet_results_path: Path, # reincarnated-engine/src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-2026-05-27.json
    output_dir: Path,            # reincarnated-loadout/public/seasons/cycle-13-mechanical-season-001/
) -> ExportResult:
    """
    Transform cycle-13-mechanical-season-001 → loadout-app normal-season schema.
    Emit: metadata.json + classes.json + gear_pool.json
    Placeholder per-skill content marked with cycle_14_refresh_pending flag.
    """
```

### Step 3 — Emit `metadata.json`

Match the v2_narrow_phase_5 metadata structure. Add discipline note flag:

```json
{
  "season_id": "cycle-13-mechanical-season-001",
  "engine_version": "v1.30+cycle13",  // or whatever the current engine version reports
  "generation_seed": <from source>,
  "n_kits": 16,
  "generation_mode": "cycle13_mechanical_substrate_validated",
  "placeholder_skill_content": true,
  "cycle_14_refresh_pending": true,
  "cycle_14_refresh_rationale": "Per-skill content (names, damage_multiplier, cooldown_seconds, energy_cost, bc_axis_contribution, geometry_type, flavor_text, effects) comes from Phase 5 cohesion coalescence in Cycle 14 per doc 40 § 5 + closeout Block A.5. Current values are synthesized placeholders matching _SyntheticPlayerClass parameters used in the gauntlet sim that empirically validated this season (27,360 fights GAUNTLET_SIM_PASS=True).",
  "phase5_stats": null,  // or {}, indicating phase5 has not yet run for this season
  ...other fields from cycle-13 season_metadata.json + computed totals
}
```

### Step 4 — Emit `classes.json`

For each of the 16 characters, emit a class entry matching v2_narrow_phase_5 schema:

- `archetype_tag`: derive from cycle-13 char filename (e.g., `S1_endgame_str_01_heavy_barbarian` → `endgame_str_01_heavy_barbarian` or similar; or pull from char JSON if present)
- `balance_metadata`: synthesize from `wr_bracket_details` + gauntlet sim per_cohort breakdown (if available)
- `carried_gear`: pull from gear_set JSON
- `color_palette`: synthesize from element / dominant_element (or empty placeholder)
- `dominant_element`: from char JSON
- `energy_type`: synthesize (most likely "mana" or "stamina" per attribute family — str/dex = stamina, int/wis = mana)
- `engine_version`: same as metadata
- `flavor_text`: placeholder "Cycle 14 Phase 5 will populate."
- `id`: derive (e.g., `cycle13_class_001`)
- `is_act_boss`: false (likely; or derive from char metadata if present)
- `main_weapon`: from `gear_set.main_weapon` or char `weapon` field
- `mechanical_substrate_triple`: synthesize from char `bc_tuple` (e.g., bc_tempo / bc_amplitude / bc_proxy_density)
- `movement_speed`: synthesize default
- `name`: human-friendly from filename (e.g., "Heavy Barbarian")
- `range_profile`: synthesize from main_weapon type
- `role_orientation`: derive from char attribute family (str/dex = damage; wis = support; int = damage/control mix)
- `seasonal_dominant_element`: same as `dominant_element` for cycle 13
- `secondary_item`: from `gear_set.secondary_item` if present
- **`skills`** (the placeholder synthesis):
  - For each `chain_composition` chain (typically t4_chain_1, t4_chain_2, supporting_chain_1):
    - For each node in the chain (passive 1-5 + active 1-15 + T4 binary 1):
      - Synthesize a skill entry with 21-field schema:
        - `id`: `cycle13_skill_<char_id>_<chain_id>_<node_index>`
        - `name`: `"<Element-name-cased> Chain <chain_id> - <Active/Passive/T4> <node_index>"`
        - `chain_id`: from chain_composition
        - `tier`: derive from chain depth position (1-3 typical)
        - `canonical_element`: char's `dominant_element`
        - `seasonal_element`: same
        - `damage_multiplier`: synthetic-mode value matching `_SyntheticPlayerClass` (magnitude=3000)
        - `cooldown_seconds`: 0.7 (matching `_SyntheticPlayerClass`)
        - `energy_cost`: 0 (matching `_SyntheticPlayerClass`)
        - `bc_axis_contribution`: synthesize from char's BC cell aggregate (e.g., 30%-split across the 3 BC axes that compose the kit's bc_tuple)
        - `geometry_type`: derive from substrate (default `radius` or `cone`)
        - `spatial_geometry_type`: same as `geometry_type` or null
        - `role`: synthesize (damage / support / control / utility per chain function)
        - `effects`: `[{"placeholder": true, "cycle_14_refresh_pending": true}]`
        - `flavor_text`: "Cycle 14 Phase 5 will populate."
        - `phase5_attempt_number`: 0
        - `phase5_cache_hit`: false
        - `phase5_cohesion_breakdown`: null
        - `phase5_cohesion_score`: null
        - `phase5_is_placeholder`: true ← **THE KEY FIELD** drax can use to detect + show "Cycle 14 refresh pending" indicator
        - `phase5_thematic_tags`: []
- `source_library`: `"cycle-13-mechanical-substrate"`
- `stat_distribution`: synthesize from char attribute family + level (L50 per doc 41)
- `t4_alteration_output`: synthesize from char `t4_candidates` (the JSON metadata for the kit's T4 selections)
- `title_completion`: placeholder

### Step 5 — Emit `gear_pool.json` (if loadout consumer expects it)

Source: 16 gear_set JSONs + per-slot per-rarity gear instances. Emit `GearPoolEntry[]` matching the existing type schema (look at any Yomi pool file in `data/` directories for shape).

If the loadout app does NOT require gear_pool.json for non-Yomi seasons (per the `useSeasonData.ts` TODO comment about Yomi-fallback), emit a minimal entry or omit. Document choice in MIGRATION.

### Step 6 — Convention check / dual-write decision

Critical decision per § 1 reading item 2:

- **Matt's spec** target: `reincarnated-loadout/public/seasons/cycle-13-mechanical-season-001/` (single classes.json + metadata.json)
- **`useSeasonData.ts` hook** reads from `../../data/*/manifest.json + ../../data/*/classes/*.json` (the OLDER convention)

Likely the loadout app has TWO consumers: the hook reads from `data/`, and the `public/seasons/` directory feeds some other consumer (possibly a static-fetch pattern OR a future migration target).

**Recommended approach:**
1. Write to `public/seasons/cycle-13-mechanical-season-001/` per Matt's spec (matches v2_narrow_phase_5 precedent)
2. ALSO write to `data/cycle-13-mechanical-season-001/manifest.json + classes/*.json` (the old convention the hook reads) so cycle13 appears in `selectableSeasons` automatically
3. Document the dual-write in MIGRATION + flag for drax to consolidate as part of Step 2

OR

**Alternative:** write only to `public/seasons/` per Matt's spec + flag drax for Step 2 hook update.

**Your call** based on what the hook empirically discovers; pick the path that makes drax's Step 2 work cleanly.

### Step 7 — Sentinel + MIGRATION + tests

- Sentinel file: `reincarnated-engine/src/reincarnated/export/cycle13_normal_season_export_landed.sentinel`
- `reincarnated-engine/src/reincarnated/export/MIGRATION.md` new § (next version after current; document the transform pipeline + the dual-path or single-path emission choice)
- `reincarnated-loadout/MIGRATION.md` new § (cross-reference; document what drax should consume)
- Tests: round-trip test (load source cycle-13 char → transform → assert output matches loadout-schema-validator); count-assertion (16 classes); per-class-skill-count assertion; placeholder-flag assertion

---

## 3. Acceptance criteria

- [x] `reincarnated-loadout/public/seasons/cycle-13-mechanical-season-001/metadata.json` exists + matches `v2_narrow_phase_5/metadata.json` structure + has `placeholder_skill_content: true` + `cycle_14_refresh_pending: true` flags
- [x] `reincarnated-loadout/public/seasons/cycle-13-mechanical-season-001/classes.json` exists + contains 16 classes matching v2_narrow_phase_5 per-class schema
- [x] Per-class `skills` array populated with synthesized placeholder entries; each skill has `phase5_is_placeholder: true`
- [x] `gear_pool.json` emitted OR documented-as-omitted with rationale
- [x] (If recommended path) `data/cycle-13-mechanical-season-001/manifest.json + classes/*.json` also emitted so `useSeasonData.ts` discovers cycle13 in `selectableSeasons`
- [x] Sentinel at `reincarnated-engine/src/reincarnated/export/cycle13_normal_season_export_landed.sentinel`
- [x] `reincarnated-engine/src/reincarnated/export/MIGRATION.md` + `reincarnated-loadout/MIGRATION.md` cross-referenced entries
- [x] Round-trip + count + placeholder-flag tests PASS
- [x] No regressions in 488+ engine tests
- [x] WARN-pattern preservation chain maintained

---

## 4. Out-of-scope (explicit)

- **Do NOT** modify the 16 source JSONs in `reincarnated-engine/output/cycle-13-mechanical-season-001/` (immutable substrate)
- **Do NOT** modify drax's loadout UI — that's Step 2's scope
- **Do NOT** retire the gap-fill tab — that's Step 2 (drax)
- **Do NOT** modify `useSeasonData.ts` hook — that's drax's seam (if hook update needed, flag for Step 2)
- **Do NOT** populate per-skill content with real cohesion-judge output — that's Cycle 14 Phase 5
- **Do NOT** modify cycle13_characters.db — the DB is parallel infrastructure for the gap-fill tab; leave intact for now (drax may decide to retire it in Step 2 cleanup)
- **Do NOT** invent new per-skill schemas — match v2_narrow_phase_5 exactly

---

## 5. Cross-seam impact

- **Drax-side:** consumer interface; Step 2 fires after this completes; sentinel signals readiness
- **Engine-side:** none beyond export pipeline addition
- **Discipline #1.2 code-citation:** transform pipeline cites source field → target field mapping in code-comments + MIGRATION
- **Discipline #12 semantic shifting:** `_SyntheticPlayerClass` placeholder synthesis is a documented semantic-shift instance (skill values that LOOK real but flag as placeholder via `phase5_is_placeholder: true`)

---

## 6. Discipline citations

- **#1.2 math-note code-citation** — schema-mapping documented in code-comments + MIGRATION
- **#11 empirical inspection over assumption** — inspect v2_narrow_phase_5 source first, then design transform
- **#12 semantic shifting** — placeholder vs real per-skill content disambiguated via `phase5_is_placeholder` flag
- **#19 Agent-tool-not-for-waiting** — single serial pytest invocation for verification (do not fire concurrent test suites per W3 OP amendment)
- **#21 / #22** — completion record uses workstream-relative framing

---

## 7. Completion record protocol

Append a completion record with:

- **Status:** COMPLETE
- **Convention chosen:** public/seasons/ only OR dual-write OR data/ only (with rationale)
- **`metadata.json` path + brief summary** (n_kits, key fields)
- **`classes.json` path + count** (16)
- **`gear_pool.json` decision** (emitted or omitted with rationale)
- **Sentinel path**
- **MIGRATION § paths + versions** (engine + loadout)
- **Test result**
- **Drax-Step-2 readiness signal** (yes; KR routes drax)
- **Commit SHA(s)**

KR will pick up + fire drax Step 2 dispatch.

---

**Authority:** knight-rider per Matt 2026-05-27 Track C REVISED directive + per-cycle-push authorization.

**Push pattern:** per Matt authorization, commit + push as work-products land.
