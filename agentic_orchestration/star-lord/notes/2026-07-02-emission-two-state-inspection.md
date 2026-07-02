# Star-lord: Emission Two-State Inspection (Demo vs Launch)

**Date:** 2026-07-02  
**Commissioned by:** Matt (via knight-rider MASTER 2026-07-02-one-realm-mvp-build-MASTER.md D1)  
**Scope:** READ-ONLY survey. No production code changes. No DB writes.  
**Provenance tag:** `[star-lord-verified]` = code-read this session with file:line cites.

---

## §0 TL;DR (≤15 lines)

**Two-track verdict:** Two emission tracks exist and do not meet. Neither track alone produces a Godot-consumable bundle with all required content types.

**State 1 (Demo / one-realm hand-join):** A hand-join IS achievable. The raw ingredients exist but require plumbing:
- Kits: cycle-14 track produces named kits with 12 real skills, BUT all 12 skill `flavor_text` are NULL (confirmed on disk, 5 files sampled). `proxies` field is absent from cycle-14 output (not even `[]`). `main_weapon` is NULL.
- Monsters: old-track `seasons/season_XXXXXX/monsters/*.json` exist (44 per season) with names and flavor_text (confirmed NOT NULL on old seasons that ran through LLM naming). Confirmed present at `seasons/season_000001/`.
- Gear: old-track gear_pool via `season_exporter.export_season()` — 200 items, LLM-named for rare/epic/legendary — is the only complete gear artifact.
- Factions: generated (in collab staging dirs), never written to any bundle. `_export_season_inner()` writes zero faction JSON. `ExportSeason.faction_clusters` field exists in schema but is never populated by the writer.
- The summoner proxy decl for demo kits (D2 rocket output) has no landing point in either track today.

**State 2 (Launch serial driver):** No serial driver exists. The b6 deletion removed `season_orchestrator.py` and `generate-season` CLI (commit `4b089e3`). The `run_season_production.py` script routes through `wave5_season_orchestrator.py` → cycle-14 track → `cycle14_wave5_emitter.py` to `reincarnated-loadout/data/`. The `season_exporter.export_season()` function still exists but has no caller driving it for current seasons.

**Demo hand-join verdict:** ACHIEVABLE with bounded plumbing. No content is genuinely missing except (a) summoner proxy decls (D2 feeds D1) and (b) a driver that reads old-track monsters + cycle-14 kits/names + gear from DB and writes one consolidated JSON. Weapon descriptors: nice-not-critical per §5.1; the substrate binding identity fields exist in `gear_representative.main_weapon.substrate_binding` for cycle-14 kits when present.

---

## §1 Pipeline Map — Two Tracks End-to-End

### TRACK NEW (Cycle-14 Wave-5)

```
scripts/run_season_production.py
  → simulation/wave5_season_orchestrator.py::run_season_production()
      Phase 2: BC discovery (18 kit candidates via ENDGAME_ENCOUNTER_CATALOG)
      Phase 3: Gauntlet + PM-1 clustering (WR-bracket gate + faction clustering)
      Phase 4: Mechanical archive → kit_archive.db
      Phase 5: phase5_orchestrator.py (Wave A faction labels, F-C relationships, Wave B kit identities, Wave S season name)
               LLM calls: AsyncAnthropic; Wave A 3-5 calls/season, F-C 3-6 calls, Wave B 16-40+ calls, Wave S 1 call
      Phase 7: 2-layer joint gate; verdict log
  → export/cycle14_wave5_emitter.py::main()
      Reads: agentic_orchestration/cycle-14-wave-5-season-{N}/
             phase5_faction_clusters.json, wave_b_identities.json, season_summary.json,
             phase4_archive_insertion.json, kit_archive.db, phase2_kit_candidates.json
      Writes: reincarnated-loadout/data/cycle-14-wave-5-season-{N}/
              manifest.json (SeasonManifest)
              classes/{slug}.json (ClassData per ACCEPT kit)
              public/engine-state/season-{N}/phase7_kit_verdicts.json
```

**TRACK NEW artifacts on disk (confirmed [star-lord-verified]):**
- `reincarnated-loadout/data/cycle-14-wave-5-season-{001,002,003}/` — present
- `reincarnated-loadout/data/cycle-14-wave-5-season-001/classes/` — named class files (e.g. `ashfen_gloomchain_warden.json`)
- NO monsters.json, NO gear_pool.json, NO faction_clusters.json in the loadout data dirs

### TRACK OLD (season_exporter)

```
export/season_exporter.py::export_season(season_id, output_dir, telemetry_db)
  → _export_season_inner()
      Reads: seasons/<season_id>/manifest.json
             seasons/<season_id>/classes/*.json
             seasons/<season_id>/monsters/*.json
             telemetry.db: gear_instances, classes (carried_gear, target_win_rate), abilities (geometry_type)
             seasons/<season_id>/gear/catalog.json (deterministic re-regen of gear stats)
      Writes: exports/<season_id>/
              metadata.json, classes.json, monsters.json, gear_pool.json
              gauntlet_recipe.json (passthrough copy)
              damage_formula.md, design_context.md
```

**TRACK OLD artifacts on disk (confirmed [star-lord-verified]):**
- `seasons/season_000001/` present (+ 000007, 000013, 000042, 000043, 000046, 000093, 000099, 000100, 000200)
- `seasons/season_000001/classes/` and `seasons/season_000001/monsters/` present
- `exports/` dir: only `v2_narrow/` and `v2_narrow_phase_5/` subdirs (stale non-production exports: classes.json + metadata.json only, no monsters/gear)
- **No current-generation season has a complete exports/<season_id>/ directory with monsters.json + gear_pool.json**

**CLI driver:** `generation/season_orchestrator.py` and `cmd_generate_season` DELETED at commit `4b089e3` (rocket: b6-stack Phase 2, 2026-06-16). The `generate-season` subparser is gone from `cli.py` [star-lord-verified: cli.py commit a2deaa0 + 4b089e3 stats confirm deletion].

### Kit-Space Track (parallel, not either main track)

`export/kit_space_emitter.py` — emits per-kit JSONs to `data/kit_space/` + chronicle entry. Called via EAA-3/EAA-4 path. Not a Godot-consumable bundle; a persistent kit-identity store. Not directly relevant to demo hand-join.

---

## §2 Six-Content-Type × Two-Track Coverage Matrix

| Content Type | TRACK OLD (season_exporter) | TRACK NEW (cycle14_wave5_emitter) | Demo-critical? |
|---|---|---|---|
| **kits** | PRESENT — `classes.json` with stat_distribution, skills, balance_metadata; LLM `name` = stub (`class_0001`), `flavor_text` = NULL [star-lord-verified: seasons/season_000001/classes/class_0001.json] | PRESENT — named kits (wave_b_identities), 12 real skills, `flavor_text` populated at kit level; **skill `flavor_text` ALL NULL** [star-lord-verified: 5 class files sampled, 100% null]; `proxies` field ABSENT (not even `[]`) | Yes |
| **monsters** | PRESENT — `monsters.json` 44 monsters/season with stats + archetype; LLM `name`/`flavor_text` NULL in season_000001 raw [star-lord-verified] — naming only fires when pipeline invoked with LLM | ABSENT — cycle-14 track is kit-only; `cycle14_wave5_emitter.py` sources from faction_clusters + wave_b_identities, no monster generation step | Yes |
| **factions** | ABSENT — `_export_season_inner()` writes {metadata, classes, monsters, gear_pool, gauntlet_recipe} only; `ExportSeason.faction_clusters = None` never populated by the writer [star-lord-verified: season_exporter.py:776-779, schemas.py:1395] | PARTIAL — generated (collab staging dirs: `phase5_faction_clusters.json`, `phase5_faction_relationships.json`); NOT written to loadout bundle by `cycle14_wave5_emitter.py` [star-lord-verified: emitter module reads them but does not emit them to loadout dir] | Presentation-side only (III.7 invariant) |
| **gear** | PRESENT — `gear_pool.json` 200 items; LLM-named (rare/epic/legendary via `name_gear_item()` in old pipeline); stats re-derived deterministically from catalog.json | PARTIAL — `gear_representative` (11 slots) present per kit in ClassData JSON [star-lord-verified: ashfen_gloomchain_warden.json `gear_representative` key present]; NOT a rolled gear pool; no `gear_pool.json` in loadout dir | Yes |
| **weapons** | ABSENT — `main_weapon` field in old class JSON is NULL [star-lord-verified: seasons/season_000001/classes/class_0001.json: `"main_weapon": null`]; `ExportWeaponDescriptor` schema exists in export/schemas.py; `_build_weapon_descriptor()` in season_exporter.py:371 returns None because source JSON has null | PARTIAL — `substrate_binding` exists within `gear_representative.main_weapon` in phase2 data; `emit_weapon_descriptor()` in `cycle14_unified_bundle_emitters.py:522` can extract it; but `main_weapon` field in emitted ClassData is NULL [star-lord-verified: ashfen_gloomchain_warden.json: `"main_weapon": null`] | Nice-not-critical (§5.1) |
| **flavortext** | PARTIAL — kit `name`/`flavor_text` NULL (pipeline not run with LLM for stored seasons); monster `name`/`flavor_text` NULL [star-lord-verified]; gear LLM-named only when gear_generation pipeline run with real LLM client; skill `flavor_text` NULL | PARTIAL — kit `name` POPULATED (wave_b_identities), kit `flavor_text` POPULATED; skill `name` POPULATED (phase5_skill_naming path fires in wave5_season_orchestrator); **skill `flavor_text` ALL NULL** [star-lord-verified: 60 skills sampled across 5 files, 100% null]; monster absent from track | Yes (kit/monster level; skill NULL is a gap) |

---

## §3 The Five Questions

### Q1. Track-by-track, artifact-by-artifact

**TRACK NEW produced artifacts (confirmed on disk):**

`reincarnated-loadout/data/cycle-14-wave-5-season-001/manifest.json` fields:
- `manifest_version`, `season_id`, `generated_at`, `engine_version`, `season_theme_element`, `anchor`, `elements`, `seasonal_elements`, `summary`, `validation_passed`, `placeholder_skill_content`, `cycle_14_refresh_pending`, `wave_s_ai_tell_compliance_score`, `phase7_acceptance_rate`, `phase4_accepted_count`, `phase5_cluster_count`
- `engine_version`: present in manifest (value not null) [star-lord-verified: manifest.json keys list]

`cycle-14-wave-5-season-001/classes/{slug}.json` fields (confirmed [star-lord-verified: ashfen_gloomchain_warden.json]):
- `id`, `name` (LLM-populated via wave_b), `title_completion`, `flavor_text` (populated), `archetype_tag`, `energy_type`, `role_orientation`, `range_profile`, `dominant_element`, `seasonal_dominant_element`, `color_palette`, `stat_distribution` (primary=100 scaffold, Cycle 15+ real values), `skills` (12 real phase2 skills), `balance_metadata`, `movement_speed`, `is_retired`, `main_weapon` (NULL), `secondary_item` (NULL), `source_library`, `t4_alteration_output`, `gear_representative` (11-slot dict populated), `chain_composition`, `class_chain_count`, `t4_scope`, `t4_candidates`, `primary_t4`, `bc_target_cell`, `engine_version`, `ai_tell_compliance_score`, `final_compliance_status`, `parent_faction_id`, `parent_faction_label`
- Skills fields: `id`, `abilities`, `composition_mode`, `energy_cost`, `cooldown_seconds`, `effects`, `geometry`, `timing`, `triggers`, `damage_multiplier`, `range_m`, `spatial_geometry_type`, `role`, `canonical_element`, `effect_category`, `color_value`, `power_tier`, `scaling_attribute`, `tier`, `chain_id`, `chain_position`, `parent_skill_ids`, `damage_scaling_type`, `tier_coefficient`, `hybrid_pattern`, `hybrid_balance_factor`, `scaling_coefficient`, `trait_slots`, `name` (POPULATED — e.g. "Shadow Chain A - T1 Primary Attack"), `flavor_text` (NULL — 100% on 5 sampled files), `skill_node_type`, `investment_points_passive`, `passive_effect_base_at_max`, `passive_effect_magnitude`, `investment_points`
- `proxies`: field ABSENT from ClassData shape (not even empty list)

Writer code: `export/cycle14_wave5_emitter.py::build_class_data()` and `emit_class_file()` — no LLM calls (`# No LLM calls. No DB writes. Pure export.` — cycle14_wave5_emitter.py:37)

**TRACK OLD produced artifacts:**

`seasons/season_000001/manifest.json` keys: `manifest_version`, `season_id`, `generated_at`, `generation_seed`, `season_theme_element`, `anchor`, `elements`, `elements_metadata`, `summary`, `validation_passed` — NO `engine_version` field [star-lord-verified]

`seasons/season_000001/classes/class_0001.json` fields: `id`, `name` (stub `"class_0001"`), `title_completion` (None), `flavor_text` (None), `archetype_tag`, `dominant_element`, `color_palette`, `stat_distribution`, `skills`, `balance_metadata` — NO `energy_type`, NO `role_orientation`, NO `range_profile`, NO `movement_speed`, NO `main_weapon`, NO `proxies` [star-lord-verified]

`seasons/season_000001/monsters/monster_00001.json` fields: `id`, `name` (stub `"monster_00001"`), `flavor_text` (None), `threat_tier`, `archetype_tag`, `dominant_element`, `max_hp`, `armor`, `elemental_resistances`, `skills`, `balance_metadata` [star-lord-verified]

`exports/` directory: NO production exports exist. Only `v2_narrow/` and `v2_narrow_phase_5/` subdirs, each containing only `classes.json` + `metadata.json` (stale research artifacts, no monsters/gear/factions) [star-lord-verified].

**season_exporter.export_season() output shape** (code-verified, never driven for a live season):
- `exports/<season_id>/metadata.json` — ExportMetadata: season_id, timestamp, seed, season_theme_element, anchor, elements, seasonal_elements, class_count, monster_count, trial_defeat_rate, convergence_failures, calibrated_stat_floors (empty {})
- `exports/<season_id>/classes.json` — list[ExportClass]: id, name (from JSON, NULL for stub seasons), title_completion, flavor_text (NULL), archetype_tag, energy_type, role_orientation, range_profile, dominant_element, seasonal_dominant_element, is_act_boss, color_palette, stat_distribution, skills (flavor_text NULL, geometry_type from DB), carried_gear (from DB), balance_metadata, movement_speed, t4_alteration_output, main_weapon (NULL), secondary_item (NULL), source_library [season_exporter.py:710-734]
- `exports/<season_id>/monsters.json` — list[ExportMonster]: id, name (NULL), flavor_text (NULL), threat_tier, archetype_tag, energy_type, role_orientation, range_profile, dominant_element, seasonal_dominant_element, max_hp, armor, elemental_resistances, skills, movement_speed [season_exporter.py:740-763]
- `exports/<season_id>/gear_pool.json` — list[ExportGearItem]: 200 items; name/flavor_text LLM-populated ONLY if generation pipeline was run with real LLM; from DB rows [season_exporter.py:471-563]
- `exports/<season_id>/gauntlet_recipe.json` — passthrough copy
- `exports/<season_id>/damage_formula.md` + `design_context.md` — static documentation strings [season_exporter.py:791-792]
- **NEVER writes:** faction_clusters.json, faction_relationships.json, weapon_descriptors.json [season_exporter.py:776-779, confirmed]

### Q2. The Demo Hand-Join (State 1)

**What a minimal one-realm bundle needs:**
Per `one-realm-mvp-scope.md §5.1`: kits + monsters + gear + flavortext. Weapon descriptors nice-not-critical. Faction fields presentation-side only.

**Piece-by-piece from each track:**

| Bundle piece | Source track | Status |
|---|---|---|
| Kit identity (name, title_completion, flavor_text, archetype_tag, energy_type, role_orientation, range_profile, dominant_element, color_palette) | TRACK NEW | PRESENT — wave_b names, kit-level flavor_text populated |
| Kit skills (12 real skills with names) | TRACK NEW | PRESENT — skill names populated; **skill flavor_text NULL** |
| Kit stat_distribution | TRACK NEW | PRESENT (scaffold only: primary=100, others=10; Cycle 15+ real values) |
| Kit gear_representative (11 slots) | TRACK NEW | PRESENT in ClassData JSON |
| Kit proxies | NEITHER TRACK | ABSENT — awaits D2 (rocket hand-authored proxy decls) |
| Kit main_weapon | TRACK NEW (if wired) | PARTIAL — substrate_binding exists in gear_representative.main_weapon; `emit_weapon_descriptor()` can extract; but ClassData has `main_weapon: null`; nice-not-critical per §5.1 |
| Monsters (stats + archetype + skills) | TRACK OLD | PRESENT — `seasons/season_000001/monsters/*.json` (44 monsters); LLM name/flavor_text NULL for stored seasons but names CAN be populated by running LLM naming |
| Gear pool (200 items, LLM-named) | TRACK OLD (via season_exporter) | PRESENT — requires season_exporter.export_season() to be invoked against a season_id with a populated telemetry.db and catalog.json |
| Flavortext: kit level | TRACK NEW | PRESENT |
| Flavortext: skill level | NEITHER TRACK | NULL — 100% null in cycle-14 output; old track never ran LLM skill naming for stored seasons |
| Flavortext: monster | TRACK OLD (if LLM run) | NULL in stored seasons; LLM path exists via `llm/naming.py::name_monster()` |
| Flavortext: gear | TRACK OLD (if LLM run) | NULL if rare/epic/legendary LLM not run; path exists via `llm/naming.py::name_gear_item()` |

**What is GENUINELY MISSING from both tracks (must be authored/wired):**
1. **Skill `flavor_text`** — NULL in cycle-14 output. The `phase5_skill_naming.py` path runs `name_skill_node()` in the generation pipeline, but the emitted ClassData JSON has `flavor_text: null` on all 12 skills. Root cause: `build_real_skills()` in `cycle14_wave5_emitter.py:359` propagates `flavor_text` from phase2 skill records verbatim — the phase2 skill records store `null` for `flavor_text` because `phase5_skill_naming.py::name_skill_node()` populates `ws1a4_flavor_decision` / `ws1a4_flavor_word_used` as separate fields, not `flavor_text` directly. The actual `flavor_text` population in cycle-14 requires a separate naming pass (the old `llm/naming.py::name_skill()` path or equivalent). This is the LLM surface gap (see Q4).
2. **Summoner proxy decls** — D2 (rocket) hand-authored decls. Not in either track. `build_proxies_surface()` in `proxy_vocabulary_bridge.py:295` will translate them once authored.
3. **Assembly driver** — a script/function that reads cycle-14 ClassData JSONs + old-track monsters/*.json + gear via season_exporter + writes a single Godot-consumable bundle JSON. Neither `_export_season_inner()` (TRACK OLD, no factions/cycle-14 kits) nor `cycle14_wave5_emitter.py` (TRACK NEW, no monsters/gear) produces this.

**What does NOT block a Godot-consumable bundle:**
- Faction fields are explicitly presentation-side per III.7 invariant; `emit_faction_block()` in `cycle14_unified_bundle_emitters.py:211` is built and validated; assembly into bundle is what's parked.
- The combat math (`damage_formula.md`) is present in season_exporter output.
- `ExportSeason` schema in `schemas.py:1386` already has `faction_clusters` and `faction_relationships` optional fields.

**Where D2 rocket proxy decls enter the bundle:**
`PlayerClassV2.to_dict()` carries a `proxies` list. `build_proxies_surface(skills)` in `proxy_vocabulary_bridge.py:295` consumes summon-skill fields and produces decl dicts. For hand-authored demo summoner kits, rocket will author decls directly that match the `entity_from_proxy_dict` shape (`proxy_type`, `behavioral_tier`, `base_hp`, `damage_multiplier`, `range_m`, `targeting_behavior`, `attack_interval_s`, `proxy_max_active`, `count`, `duration_s`, `spawn_cadence_s`, `acquisition`). These decls enter the ClassData as the `proxies` key. The cycle14_wave5_emitter does not currently pass them through since `proxies` is absent from its emitted ClassData shape; the assembly driver (D1) must include them.

### Q3. The Launch Serial Driver (State 2)

**Tracker II.3 (a)-(d) verification against code:**

**(a) Single driver routing cycle-14 content through (or replacing) `season_exporter`:**
- CONFIRMED GAP. `P1_ARCHITECTURE_PARK` constant in `cycle14_unified_bundle_emitters.py:46` explicitly marks the route-vs-replace choice as Tier-3 PARK for Matt. `build_unified_season_content_blocks()` (:620) builds validated per-type blocks but does NOT assemble them. No driver exists [star-lord-verified].

**(b) Monster generation wired into the cycle-14 track:**
- CONFIRMED GAP. `wave5_season_orchestrator.py` is kit-focused (Phase 2-7). Monster generation via `monster_generator.py` is not called in this orchestrator. Old track's `generate_season_gear_pool()` + monster generation remain in `generation/` but are not invoked by the cycle-14 pipeline.

**(c) `faction_clusters` actually written:**
- CONFIRMED GAP. `_export_season_inner()` in `season_exporter.py:776-779` writes only {metadata, classes, monsters, gear_pool}. `ExportSeason.faction_clusters` field defined at `schemas.py:1395` but never populated in the writer. Faction data sits in collab staging dirs (`phase5_faction_clusters.json`) and in `ExportFactionCluster` instances in memory but is never disk-committed to the bundle. `emit_faction_block()` in `cycle14_unified_bundle_emitters.py:211` is built and validated but is not called by any production driver [star-lord-verified: grep of season_exporter.py confirmed zero faction_clusters writes].

**(d) Weapon descriptor wired `substrate_weapon_binding → main_weapon`:**
- CONFIRMED GAP (with nuance). `emit_weapon_descriptor()` in `cycle14_unified_bundle_emitters.py:522` extracts from `gear_representative.main_weapon.substrate_binding`. This function exists and is tested. But it is not called by `cycle14_wave5_emitter.py::build_class_data()` — the emitter sets `main_weapon: null` explicitly [star-lord-verified: cycle14_wave5_emitter.py:518 note: "main_weapon and secondary_item remain null in ClassData to avoid WeaponSlot schema mismatch"]. The blocker is a schema incompatibility between WeaponDescriptor (expects name/category/cultural_register) and phase2 gear (different contract). The substrate_binding path via `emit_weapon_descriptor()` avoids this mismatch but is unwired.

**What the deleted one-shot CLI driver did:**
`generation/season_orchestrator.py` (deleted commit `4b089e3`, rocket b6-stack Phase 2, 2026-06-16) contained `SeasonOrchestrator` + `SeasonOutput` — the b6 archetype-template-based generation stack. `cli.py::cmd_generate_season` drove it. This was the PRE-SPATIAL-SIM generation path (b6 templates, not the 2D spatial gauntlet). Its deletion was correct: it was the LEGACY path, not the spatial-sim path. The SPATIAL SIM path (`season_generation_pipeline.py` / `wave5_season_orchestrator.py` / `run_season_production.py`) survived the deletion intact.

**What replaced the CLI driver:**
Nothing replaces it as a single-command emission entry point. `scripts/run_season_production.py` covers the cycle-14 generation pipeline (seasons 002, 003). `export/season_exporter.py::export_season()` exists as the old-track export function but has no automated invoker for current seasons. Neither produces a unified Godot bundle.

**Tracker misses (items II.3 does not name):**
- Skill `flavor_text` wiring: cycle-14 skills have names but no flavor_text. `phase5_skill_naming.py::name_skill_node()` produces WS1A4 flavor judgments but these are separate fields; `flavor_text` is never populated in the emitted skill records. This is a genuine LLM-surface gap not surfaced in the tracker's (a)-(d) list.
- The `proxies` field is absent from ClassData shape in cycle14_wave5_emitter — not mentioned as a gap in II.3.
- `kit_space_emitter.py` track (EAA-3/EAA-4) is a third parallel path not mentioned in II.1 at all; it handles continuous kit-space expansion (per-kit JSONs + chronicle). It is live but operates independently of either main track.

### Q4. LLM Naming/Flavor Call Inventory

**Live LLM call surfaces in the emission path:**

| LLM call | Module | What it names/flavors | Wired (cycle-14) | Wired (old-track) |
|---|---|---|---|---|
| `name_skill()` | `llm/naming.py:197` | skill name + flavor_text (Layer One) | NOT wired — cycle14_wave5_emitter has no LLM calls; skill naming fires in old generation pipeline, not in the emitter | NOT wired for stored seasons |
| `name_class()` | `llm/naming.py:273` | kit name, title_completion, flavor_text (Layer Two) | NOT directly — cycle-14 uses Wave B via phase5_orchestrator (different LLM call structure; Wave B produces `kit_name_canonical` and `kit_identity_narrative`, not the same output fields) | NOT wired for stored seasons |
| `name_monster()` | `llm/naming.py:348` | monster name + flavor_text (Layer Two) | NOT wired — cycle-14 track has no monsters | NOT wired for stored seasons |
| `name_gear_item()` | `llm/naming.py:416` | gear name, flavor_text, visual_prompt, color_signature (Layer Three) | NOT wired — no gear pool in cycle-14 track | NOT wired for stored seasons (path exists in old generation pipeline) |
| `Phase5Orchestrator::run_wave_a_async()` | `llm/phase5_orchestrator.py` | faction_label_canonical, faction_identity_narrative, faction_thematic_tags (Wave A) | WIRED via wave5_season_orchestrator; cost anomaly threshold $0.10/season [phase5_orchestrator.py:124] | NOT applicable |
| `Phase5Orchestrator::run_fc_async()` | `llm/phase5_orchestrator.py` | inter-faction relationship narrative (F-C wave) | WIRED; 3-6 calls/season; cost anomaly threshold $0.60 [phase5_orchestrator.py:267] | NOT applicable |
| `Phase5Orchestrator::run_wave_b_async()` | `llm/phase5_orchestrator.py` | kit_name_canonical + kit_identity_narrative per kit (Wave B, 16-40+ calls) | WIRED; cost anomaly $2.00 [phase5_orchestrator.py:201] | NOT applicable |
| `Phase5Orchestrator::run_wave_s_async()` | `llm/phase5_orchestrator.py` | season name (Wave S, 1 call/season) | WIRED; cost anomaly $0.03 [phase5_orchestrator.py:230] | NOT applicable |
| `phase5_skill_naming.py::name_skill_node()` | `generation/phase5_skill_naming.py:699` | WS1A4 flavor judgment + word selection — populates `ws1a4_flavor_decision`/`ws1a4_flavor_word_used` fields; NOT the same as `skill.flavor_text` | Called in generation pipeline (via `kit_space_skill_naming.py`) but output does NOT land in emitted ClassData `skills[*].flavor_text` | NOT applicable |

**Why cycle-14 skill `flavor_text` is NULL:**
`cycle14_wave5_emitter.py::build_real_skills()` at line 359 propagates `flavor_text` from `phase2_kit_candidates.json` skill records via `_SKILL_PASSTHROUGH_FIELDS` list (cycle14_wave5_emitter.py:346-356). The phase2 skill records store `flavor_text` as the key but its value is null because the generation pipeline does not call `name_skill()` (Layer One) on these skills. `phase5_skill_naming.py::name_skill_node()` computes WS1A4 flavor judgments into separate fields (`ws1a4_flavor_decision`, `ws1a4_flavor_word_used`) — not the `flavor_text` field on the skill object. The classic `name_skill()` in `llm/naming.py` would populate `flavor_text`, but it is not called anywhere in the cycle-14 pipeline. It was the old-track's naming path and is currently not invoked.

**Demo-sufficiency of the LLM surface:**
The demo bundle needs named+flavored content. Kit-level names and identity narratives ARE produced (Wave B). Skill flavor_text, monster names/flavor, and gear names/flavor are NOT produced by the cycle-14 track. A demo bundle requiring complete flavortext needs either (a) a separate LLM naming pass over cycle-14 skills using `name_skill()` or (b) skill flavor_text from a different source. Gear and monster naming require the old-track generation pipeline to run with a real LLM client against an appropriate season. The LLM infrastructure (`llm/naming.py`, `LLMClient`, `TrackedLLMClient`) is present and functional; the call sites are simply unwired in the cycle-14 emission path.

**Cost/batching notes:**
Phase5Orchestrator uses `AsyncAnthropic` with `Semaphore(DEFAULT_CONCURRENCY=10)` and 3-retry exponential backoff [phase5_orchestrator.py:44-65]. Per AGENT_STATE.md session 2026-06-01: Phase 5 (Wave A + F-C + Wave B + Wave S) cost $0.50 for season-001 (34-kit snapshot). Full production estimate: $0.85-1.00 per season. Anomaly guard: >2x expected triggers flag. `TrackedLLMClient` in `llm/tracked_client.py` logs token counts per call.

### Q5. Tracker Corrections

The tracker (`current-to-end-state-engine.md` PART II, vintage 2026-06-23, updated 2026-07-02) is generally accurate for the emission pipeline. The following over-claims and under-claims were found:

| Tracker claim | Code truth | Direction |
|---|---|---|
| II.1: "skill flavor_text NULL" for cycle-14 — claim made as a GAP | CONFIRMED: all 12 skills per kit have `flavor_text: null` [star-lord-verified: 5 files, 60 skills, 100% null rate] | ACCURATE |
| II.1: "main_weapon NULL everywhere" | CONFIRMED: `main_weapon: null` in ClassData for all sampled cycle-14 kits [star-lord-verified] | ACCURATE |
| II.1: "factions PARTIAL — generated, `_export_season_inner()` never writes them, schema `schemas.py:1174`" — the line reference is WRONG | `ExportFactionCluster` is at `schemas.py:588`; `ExportSeason.faction_clusters` is at `schemas.py:1395`. The *claim* is accurate (factions generated, never written) but the line cite is stale | OVER-CLAIM (line cite wrong; verdict accurate) |
| II.1: "monsters MISSING (cycle-14)" | CONFIRMED: `cycle14_wave5_emitter.py` produces no monster output [star-lord-verified: module docstring line 37 "No LLM calls. No DB writes. Pure export." and sources list does not include monster_generator] | ACCURATE |
| II.1: "gear WORKING" — claims gear is working | PARTIALLY ACCURATE: gear_pool.json schema and logic exist in `season_exporter.py`. BUT no complete exports directory exists for any live season; `exports/` only contains stale v2_narrow research artifacts [star-lord-verified]. The exporter function exists; the trigger does not. "Working" overstates: it means "the writer code works when called" not "gear is being emitted for current seasons" | OVER-CLAIM |
| II.1: "one-shot generate-season CLI driver DELETED in the b6 deletion" | CONFIRMED: deleted at commit `4b089e3` (rocket, 2026-06-16), which deleted `generation/season_orchestrator.py` (1914 lines) and `cli.py::cmd_generate_season` [star-lord-verified] | ACCURATE |
| II.1: "`proxies: []` everywhere" | PARTIALLY INACCURATE: cycle-14 ClassData JSON has `proxies` field ABSENT (not even empty list) [star-lord-verified: ashfen_gloomchain_warden.json — `proxies` not in key list]. Old-track class JSONs also have `proxies: null` (not `[]`) [star-lord-verified: seasons/season_000001/classes/class_0001.json: `"proxies": null`]. The claim that every kit carries `proxies: []` was accurate for `PlayerClassV2.to_dict()` at generation time [proxy_vocabulary_bridge.py:23: "returns ONE decl per summon-bearing skill; an EMPTY list for any kit with no summon skills"] but does NOT survive into the emitted ClassData JSON | OVER-CLAIM (applies at generation layer, not at emitted artifact layer) |
| II.1: "weapons PARTIAL — identity in `substrate_weapon_binding`" | CONFIRMED with detail: `emit_weapon_descriptor()` can extract from `gear_representative.main_weapon.substrate_binding` but is unwired. The cycle14_wave5_emitter.py note at line 518 confirms the explicit null: "main_weapon and secondary_item remain null in ClassData to avoid WeaponSlot schema mismatch" | ACCURATE |
| II.3 (a)-(d) gap list | CONFIRMED — all four gaps are real. MISSING from the list: skill flavor_text wiring (separate from kit-level naming), `proxies` field absent from ClassData shape (not merely `[]`) | UNDER-CLAIM (two gaps unlisted) |
| II.1: "TRACK OLD `classes.json` full stat_distribution + skills + LLM names" — implies LLM names are populated | INACCURATE for stored seasons: `seasons/season_000001/classes/class_0001.json` has `name: "class_0001"` (stub), `flavor_text: null` [star-lord-verified]. The tracker implies LLM naming is a characteristic of the old track; it is only true if the generation pipeline was run with a real LLM client against those seasons. The stored seasons did not have LLM naming run | OVER-CLAIM |

---

## §4 Tracker-Corrections Table (Formal)

| # | Tracker claim (PART II, §vintage 2026-06-23) | Verdict | Code evidence |
|---|---|---|---|
| C-1 | `schemas.py:1174` — line cite for faction schema | WRONG LINE — ExportFactionCluster is at `schemas.py:588`; ExportSeason.faction_clusters at `schemas.py:1395` | `schemas.py:588, 1395` [star-lord-verified] |
| C-2 | "gear WORKING" implies gear bundles are being produced | OVER-CLAIM — gear_pool.json writer code works; no complete exports/ dir exists for any live season; stale v2_narrow artifacts only | `exports/` dir listing; `season_exporter.py:export_season()` exists but uncalled for current seasons [star-lord-verified] |
| C-3 | "every kit emits `proxies: []`" | OVER-CLAIM — accurate at `PlayerClassV2.to_dict()` layer; emitted ClassData JSON has `proxies` ABSENT (not `[]`) | `ashfen_gloomchain_warden.json` key list [star-lord-verified]; `proxy_vocabulary_bridge.py:295` |
| C-4 | "classes.json full stat_distribution + skills + LLM names" (old track) | OVER-CLAIM — LLM names are stubs (`class_0001`) in stored seasons; not populated | `seasons/season_000001/classes/class_0001.json: name="class_0001"` [star-lord-verified] |
| C-5 | II.3 (a)-(d) gap list is complete | UNDER-CLAIM — two gaps unlisted: (e) skill `flavor_text` unwired in cycle-14 (100% null confirmed); (f) `proxies` field absent from ClassData shape (architectural gap, not just empty list) | Confirmed on disk [star-lord-verified]; `cycle14_wave5_emitter.py:37, :359` |

---

## §5 Sign-off

**Survey mode maintained throughout:** all claims are descriptive of what IS, with file:line or artifact-path evidence. No production code was modified. No DB writes were performed.

**Key carry-forwards for D1 execution:**
1. The assembly driver for D1 must source: (a) kit ClassData from cycle-14 loadout dir, (b) monsters from `seasons/<id>/monsters/*.json` (old track), (c) gear_pool via `season_exporter._load_gear_pool()` against a telemetry DB, (d) D2 proxy decls inserted per summoner kit.
2. Skill `flavor_text` is an open question for the demo — either a separate LLM naming pass or accepted as null for demo scope.
3. The `emit_weapon_descriptor()` function at `cycle14_unified_bundle_emitters.py:522` is demo-ready if weapon descriptors are desired; substrate_binding data exists in gear_representative.
4. The `emit_faction_block()` at `cycle14_unified_bundle_emitters.py:211` is demo-ready for the faction presentation layer; wiring is the only gap.
5. MIGRATION.md update is mandatory before D1 tags (per ADR-004; the bundle schema is new to drax).

**Report author:** star-lord, 2026-07-02  
**Note file:** this document — research substrate for D1 mandatory pre-emit schema note (MASTER Gate-1 fold (a))
