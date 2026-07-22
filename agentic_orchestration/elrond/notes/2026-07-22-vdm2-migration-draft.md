# MIGRATION.md ENTRY DRAFT — VDM-2 schema landing (v1.1-verified → v2.0)

**STATUS: DRAFT for jack-ryan Gate-2. Appends to `agentic_orchestration/research/curated/MIGRATION.md` at W3b (after Gate-2 PASS + backup). NOT yet applied.**

**Author:** elrond (data steward) · **Wave:** W3a assemble → W3b apply · **Run:** `2026-07-22-vdm2-edition-next-lap` (gandalf RUN-CONDUCTOR)
**ADR:** ADR-004 (cross-seam handoff via MIGRATION.md) · **From:** corpus.db @ `v1.1-verified` (md5 `50df15b776ad5b0da93fe90cdee1163d`) · **To:** `v2.0`
**Companion artifacts (co-located `elrond/notes/`):** `2026-07-22-vdm2-ddl-v1.sql` · `2026-07-22-vdm2-riders.sql` · `2026-07-22-vdm2-w3b-apply.sh` · `2026-07-22-vdm2-w3a-migration-package.md` · pilot `2026-07-22-vdm2-pilot-4kit.md` · diff `2026-07-22-vdm2-schema-diff-and-ddl-v0.md`

---

## What changes

VDM-2 lands the field-delta spec (`matt_notes_handoff_docs/rdr-vdm2-field-delta-spec.md`) as an **additive** schema extension. The spec modeled a kit as a flat JSON record; the store is normalized-relational, so the six flat VDM-2 blocks re-home as `kit_id`-keyed side-car tables (W0's largest correction). NOTHING existing is dropped, altered, or re-keyed.

### 12 new side-car tables
| Table | Grain | Purpose (spec §) |
|---|---|---|
| `door_registry` | door_name | door catalogue (§2) |
| `door_arg_schema` | (door, arg) | typed per-door arg schema incl. A-2 trigger-door args (§2) |
| `kit_door_arg` | (kit, door, arg) | per-kit arg bindings + `mutation_surface` locked\|mutable (§2, §8) |
| `kit_deviation` | deviation_id | structured deviations {engine_inexpressible, param_gap, accepted_downgrade} + auto-docket wiring (§3) |
| `skill_geometry_band` | (kit, skill_ordinal) | per-skill geometry bands incl. A-1 `self` range, A-3 `fan_spread` motion (§4) |
| `motion_signature_registry` | signature_name | growable named-path registry incl. A-3 `fan_spread` (§4) |
| `normalization_rule` | rule_id | **ships EMPTY** — versioned rule registry (§5) |
| `kit_numeric` | (kit, numeric_key) | dual-column numerics; `rdr_value` honest-NULL (§5) |
| `recognition_hook` | (kit, hook_id) | ranked recognition hooks + machine-checkable coverage (§6) |
| `kit_acceptance_assert` | assert_id | sim acceptance asserts + red-test docket routing (§6) |
| `kit_delta_t4` | kit_id | delta_t4 {step, ramp} + human-validated shape sign-off (§6) |
| `expected_section_checklist` | (game, section) | per-game required-section config (§8) |

### 9 additive columns on 3 existing tables
- **`canon_corpus` +6:** `corpus_class`, `eras_normalized`, `original_element`, `court`, `atlas_coords`, `capstone_source_acquisition`.
- **`mechanic_gap_docket` +3:** `source_deviation_id`, `source_kit_id`, `intake_lane` (the second, deviation-side intake distinct from the existing mint lane).
- **`verify_ledger` +3:** `claim_subject`, `anchor_lint`, `source_lane` (mechanics-verdict granularity + anchor lint + player-attested lane; §7 is a granularity extension — mechanics verdicts ALREADY EXIST, 597 rows).

### 2 CHECK-enum additions (both on v1-NEW tables — no rebuild, no VDM-1 touch)
- **A-1:** `skill_geometry_band.range_band` gains `self`.
- **A-4:** `door_arg_schema.arg_type` gains `real`.

The two existing-table CHECKs a rebuild could have been forced on (`verify_ledger.claim_family`/`verdict`) are deliberately NOT touched — §7 needs no new family/verdict value.

### Data riders (the cheap census derivations only)
| Rider | Column | Result | Ruling |
|---|---|---|---|
| corpus_class | `corpus_class` | record **267** / annex **299** / system **19** (NULL 0) | V-14 + A-6 |
| court | `court` | **257/270** courted; **13** honest-NULL | V-15 (Q38 k=5) + V-18 |
| original_element | `original_element` | **270/270** on record (total promotion) | H3 |
| atlas_coords | `atlas_coords` | **268/270** (2 honest-NULL) | H5 |
| eras_normalized | `eras_normalized` | **268/270** (2 poe1 NULL-eras) | V-16 |

`capstone_source_acquisition` column lands but stays NULL at apply (per-kit prose derivation = W4 re-emission, not a census-cheap map). `exact_json`/`exact_source_type` stay NULL (G-FIND-1 / V-19). `normalization_rule` ships empty (V-13). Registry seeds: 6 pilot-attested doors + A-2 trigger-door args + A-3 motion registry incl. `fan_spread`.

---

## The A-6 census (record / annex / system over 585) — the tally that closes the count

`corpus_class='system'` = **all 19 `is_system=1` rows** (V-14). The historical figures (11, 19, 22) reconcile as three different definitions of "system":

| Figure | Definition | Correct? |
|---|---|---|
| **19** | all `is_system=1` (the A-6 / V-14 figure) | **YES — this is the ruling** |
| 11 | `is_system=1` AND no `kit_mapping` (W0 D-4 conflated "system-record" with "no mapping") | subset only |
| 22 | a stale V9 `null_grain` snapshot (current `null_grain` = 11) | stale |

**The definitive partition over 585:**
- **system = 19** (all `is_system=1`): **11 unmapped** (`chr-crown-proc-engine`, `hades1-privileged-status`, `hot-artifact-stack`, `hot-gear-well-retrieval`, `la-monetization-confound`, `ud-chaos-dungeon-ladder`, `ud-classless-triad`, `ud-gear-enchant-economy`, `ud-link-rune-grammar`, `ud-zodiac-board`, `vs-golden-egg-scaling`) + **8 mapped** (`d3-lod-archetype`, `di-essence-transfer`, `di-inferno-ladder`, `di-resonance-awakening`, `hades2-omega-magick`, `le-low-life-ward`, `poe2-grim-feast`, `poe2-temporalis-blink`).
- **record = 267** (`is_system=0`, corpus_bucket ∈ {poe1, d2, gd, poe2, le}).
- **annex = 299** (`is_system=0`, other 12 games).
- **267 + 299 + 19 = 585** ✓ · cross-check: 267 record + 299 annex + 8 mapped-system = **574 kit_master** ✓; the 11 unmapped-system = the 585−574 gap.

The 3 system-records inside the record games (`le-low-life-ward` + `poe2-grim-feast` + `poe2-temporalis-blink`) are all in the 8-mapped subset — they carry `corpus_class='system'`, so record-CLASS = 267, even though the record-BUCKET = 270.

---

## Per-game canonical era-token vocabularies (V-16 option (c))

`eras_normalized` carries a fixed **lowercase era-token vocabulary PER GAME**. NO cross-game ordinal is baked into the column — shelf assignment derives AT the Leg-B beat per Q38 eras=shelves. The value is the raw semicolon-shorthand VALIDATED against its game's vocabulary; any token outside its game's set is an ingest error to catch at W4/W5, never silently normalized. Raw `eras` is preserved (reversible).

**poe1 (15 tokens):** `1.x` · `2.x` · `3.0-3.6` · `3.2-3.6` · `3.4-3.6` · `3.5-3.6` · `3.7-3.13` · `3.8-3.13` · `3.11-3.13` · `3.12-3.13` · `3.14-3.19` · `3.15-3.19` · `3.16-3.19` · `3.19` · `3.20+`
*(Note: overlapping bands like `3.7-3.13`/`3.8-3.13` and `3.14-3.19`/`3.15-3.19` are legitimate distinct per-kit debut/span markers, NOT errors — they encode different kits' first-viable windows.)*

**d2 (16 tokens):** `classic` · `lod` · `lod-1.09` · `lod-1.09+` · `lod-1.10+` · `lod-1.11+` · `lod-infinity+` · `lod-pvp` · `d2r` · `d2r-2.4+` · `d2r-2.6+` · `d2r-pvp` · `rotw` · `rotw-s13` · `rotw-s13+` · `rotw-s14`

**gd (5 tokens):** `base-2016` · `aom-2017` · `fg-2019` · `patch-1.1-1.2` · `foa-pending`

**poe2 (5 tokens):** `0.1` · `0.2-dawn` · `0.3-edict` · `0.4` · `0.5-ancients`

**le (5 tokens):** `beta-0.8-0.9` · `1.0-launch` · `1.1-harbingers` · `1.2-woven` · `1.4-omens`

---

## Court coverage + the 13 honest-NULL rows (V-15)

**Coverage: 257/270 courted (95.2%), 13 NULL.** Distribution: physical 90 · fire 54 · chaos-poison 44 · lightning 42 · cold 27 · NULL 13. Lands in V-15's expected ≈257–260/270.

**Mapping applied (within Q38 k=5; k UNCHANGED):**
- `fire`→fire · `cold`→cold · `lightning`,`aether`→lightning · `physical`,`physical?`,`pierce`,`bleed`→physical · `chaos`,`poison`,`acid`,`necrotic`,`vitality`,`void`,`void?`→chaos-poison.
- `?`-suffix uses the base element's court (`physical?`→physical; `void?`→chaos-poison).
- **`pierce`/`bleed`→physical is a documented rider extension** (V-15 named the decay set + the `?`-rule but did not enumerate `pierce`/`bleed`; both are physical-family sub-tokens in every record-game taxonomy). Flagged for the reviewer, not silent. If the reviewer prefers these NULL, coverage drops 257→253.

**The 13 NULL-court record rows** (V-15 honest-NULL: `magic`/`n/a`/`mixed` + the 3 genuinely-ambiguous multi/shadow tokens the ruling did not reach; all Leg-B per-kit-resolution candidates):
| elem_raw | kit_ids |
|---|---|
| `magic` (4) | d2-berserker, d2-bonemancer, d2-hammerdin, d2-wl-abyss |
| `n/a` (5) | d2-teleport-sorc, le-low-life-ward, poe1-aurabot, poe2-grim-feast, poe2-temporalis-blink |
| `mixed(fire/cold/lightning)` (1) | gd-panettis-mage-hunter |
| `physical/chaos` (1) | poe1-blood-magic-kit |
| `shadow?` (1) | d2-wl-tainted-summoner |
| `shadow/blood?` (1) | d2-wl-blood-boil |

`court` is **mutable data** (V-18): W5 `elem_raw` corrections (the ~6–8 flagged PoE1 anomalies) trigger a bounded court re-derivation on affected rows. W3 does NOT block on the anomalies; W5 verify precedes the Leg-B derivation that consumes court, so any error is caught within Leg A.

---

## Additive-only guarantee

- Every new structure is `CREATE TABLE IF NOT EXISTS` (side-car) or `ALTER TABLE … ADD COLUMN` (nullable). SQLite `ADD COLUMN` is O(1) metadata-only; it cannot invalidate an existing row.
- **Zero** `DROP`, **zero** `ALTER … DROP/RENAME COLUMN`, **zero** CHECK-modification on an existing table.
- `kit_master` (574) recomputes identically (it selects named columns; new columns are invisible until the view is intentionally extended later). The frozen `cell_key`s stay byte-identical.
- The two A-1/A-4 CHECK additions land on v1-NEW tables (empty at CREATE) → no rebuild, no VDM-1 touch.
- `PRAGMA foreign_keys=ON` is set before side-car inserts so a typo'd `kit_id` fails loud.
- Validated: DDL v1 + riders ran clean on a THROWAWAY COPY (all 12 tables + 9 columns present; census counts exact; `PRAGMA foreign_key_check` empty; `integrity_check` ok). The copy was deleted; the live db md5 is unchanged.

## Reversibility

- Full rollback = restore `corpus.db.pre-vdm2-schema-<date>-backup` (recorded md5 = `50df15b776ad5b0da93fe90cdee1163d`), the W3b apply's step-1 anchor.
- Every housekeeping derivation preserves its raw source: `elem_raw`→`original_element`+`court`, `eras`→`eras_normalized`, `cell_key`→`atlas_coords`. Raws are NEVER dropped.
- Side-car tables are independently droppable without touching VDM-1 data. `corpus_class` is re-derivable from `is_system`+`corpus_bucket`; `court` from `elem_raw`.
- New auto-opened dockets take `status='open'` (distinct from the 19 `matt-ratified` VDM-1 rows) — reversible by deleting `intake_lane='deviation'` rows.

## Named downstream dependencies (ADR-004 cross-seam)

1. **`normalization_rule` population — battle-sim (gamora / star-lord).** The table ships EMPTY (V-13). Rule SEMANTICS (e.g. "D3 set multipliers map into the RDR T4 multiplier band") are engine-balance decisions; per ADR-004 they need a battle-sim co-authored migration (knight-rider routing + Matt approval) when populated. `rdr_value` stays honest-NULL until rules exist; the sim reads `rdr_value` only. **elrond authors ZERO balance transforms.**
2. **`exact_json` datamine population — legolas Mode-B.** The `.txt`/DBR/RePoE datamine lane is NOT on record (G-FIND-1 / V-19). `exact_json`/`exact_source_type` stay NULL at apply; genuine population is a downstream legolas Mode-B datamine acquisition. The bands land on prose alone; exact never blocks a kit.
3. **W5 `elem_raw` → `court` re-derivation.** The ~6–8 W1-flagged PoE1 `elem_raw` anomalies (aegis, discharge, spectral-throw, wild-strike, etc.) route to W5 adjudication. When corrected, a named, bounded, cheap court re-derivation runs on affected rows (court is mutable; V-18). W5 precedes Leg-B.
4. **`capstone_source_acquisition` population — W4 re-emission.** Per-kit prose derivation of capstone provenance; lands at W4 per-game tranches, not this census.
5. **`accepted_downgrade` sign-off owner-identity — W4 routing.** The pilot used `elrond (pilot)` to satisfy the CHECK; whether a design owner (Gandalf/Matt) co-signs an `accepted_downgrade` is a W4 process question (the CHECK fires correctly regardless).

---

**Signed (draft):** elrond (data steward) · W3a assemble · appends at W3b after Gate-2 PASS + backup · corpus.db UNTOUCHED at assemble.
