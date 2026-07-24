# GD-SLICE run report — TRUE-SOURCES pipe proven at width one (Flames of Ignaffar)

**Executor:** elrond (schema + adapter + curation) | **Conductor:** gandalf (`RUN-CONDUCTOR`) | **Date:** 2026-07-24
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-24-gd-slice-run-charter.md` (gates G1–G5 govern)
**Result:** **ALL GATES GREEN.** G3 = **22/22 byte-match PASS.** VERIFIED CLAIM CEILING met: *the GD adapter path is proven at width one.*

---

## Per-gate results

### G1 — schema: PASS
Normalized exact-fields surface created in `corpus.db`, additive, backed up first (`corpus.db.pre-gd-slice-20260724T002255-backup`, md5 `61457147aa0175fe872d8caec9399356`). Two tables:
- **`exact_skill`** (header, PK `kit_id`): player-facing `display_name` + raw provenance (`record_type`, `rank_count`, `source_file`, `source_version`, `record_path`) + per-game `ext_json` + `name_provenance` flag.
- **`exact_skill_field`** (per-field/per-rank, PK `kit_id,canon_key,rank`): player-facing `canon_value`/`canon_unit` + raw provenance (`raw_field`, `raw_value`, `field_kind`, `source_file`, `record_path`) + `is_core` (TSR-2 core/extension) + `monotonic_class` (drives tier-2).

TSR-2 core/extension is a **per-row `is_core` tag**, not separate tables — one queryable surface. TSR-1 is served by the explicit `canon_key`↔`raw_field` two-column mapping (canonical vocab + exact source field name both first-class; reversible from the raw column alone; tagged-not-encoded per Discipline #14). Schema-meta version `gd-slice-exact-fields-2026-07-24`. Documented in `MIGRATION-gd-slice-exact-fields-2026-07-24.md`.

### G2 — adapter: PASS
`scripts/gd_arz_adapter_2026_07_24.py` productionizes the probe's TQIT `.arz` format into a reusable `ArzArchive` reader (24-byte header · u32-prefixed string table · variable-length record table · per-record LZ4-block decompress · DBR field decode type IDs 0/1/2/3) + the GD `build_rows` adapter. Idempotent, `--verify-only`, `--dry-run`. Parsed `GDX1.arz` (18,447 records / 57,204 strings) → `purifyingflame1.dbr` → **1 header + 136 field rows** (5 rank-arrays × 26 + 6 statics). **Tier-2 in-pipe asserts (non-null · monotonic rank arrays where field-class implies · range bounds): 136/136 GREEN.**

**Parser bug, found + fixed:** first bring-up `IndexError` on the string table. Root cause = the `.arz` string table carries a **`u32 COUNT` prefix** (57,204) misread as string[0]'s length. Fix = consume the prefix; confirmation = the record-table walk then lands exactly on its end boundary (0 bad name_ids, 18,447 records). Documented inline for the next GD source.

### G3 — anchor verify (tier-1): PASS — 22/22 byte-match
Landed values byte-match the probe §2 `.arz` oracle across all five R-K5 rank-array families + geometry + cadence + rank count (table below). Re-verified post-apply against rows **read back from SQLite**: CLEAN. `foreign_key_check` clean, `integrity_check` ok.

### G4 — provenance + name bridge: PASS
Raw columns populated (`raw_field`, `raw_value`, `record_path`, `source_file=GDX1.arz`). `source_version` NULL + flagged (no in-record build tag parsed; not a blocker). Display name "Flames of Ignaffar" via `skillBitmapName='skillicon_flamesofignaffar1up.tex'` workaround; `name_provenance` flags the authoritative `.arc` tag-bridge (`tagGDX1Class07SkillName04A`) PENDING (`.arc` not in scope). Raw tag preserved in `ext_json.skill_display_tag` for later bridging.

### G5 — contradiction hygiene: PASS (curation-note flag; ZERO overwrites)
Swept corpus.db for the grimtools 60-rank shape: **not banked anywhere.** The FoI `kit_numeric` 26 rows are formula-constant **scalars** (crit mults, attr-per-point, PtH constants, `foi_tick_interval_sec`), NOT damage rank-arrays; `kit_dossier` GD rows are prose (0 arrays ≥30 elements); `skill_geometry_band` FoI rows are `dossier-prose`, `exact_json` NULL. The 60-vs-26 contradiction lives only in the legolas join-surface probe note §2c (an observation of the grimtools source). So G5 is a note-level flag (recorded in the MIGRATION §G5), not a row-flag — **zero rows overwritten**; FoI `kit_numeric` intact post-apply (`foi_tick_interval_sec=0.3`, `crit_mult_pth070=1.0`).

---

## G3 byte-match table (probe §2 oracle vs landed)

| Anchor | Expected | Landed | Verdict |
|---|---|---|---|
| `rank_count` | 26 | 26 | PASS |
| `offensiveFireMin` [r1/r16/r26] | 8.0 / 129.0 / 262.0 | 8.0 / 129.0 / 262.0 | PASS |
| `offensiveFireMax` [r1/r16/r26] | 18.0 / 157.0 / 306.0 | 18.0 / 157.0 / 306.0 | PASS |
| `offensiveSlowFireMin` (burn DoT) [r1/r16/r26] | 8.0 / 211.0 / 382.0 | 8.0 / 211.0 / 382.0 | PASS |
| `skillManaCost` [r1/r16/r26] | 7.0 / 39.0 / 69.0 | 7.0 / 39.0 / 69.0 | PASS |
| `weaponDamagePct` [r1/r16/r26] | 9.0 / 42.0 / 58.0 | 9.0 / 42.0 / 58.0 | PASS |
| `maxRange` | 9.1 | 9.1 (f32) | PASS |
| `endWidth` | 4.5 | 4.5 | PASS |
| `startWidth` | 2.2 | 2.2 (f32) | PASS |
| `timeBetweenAttacks` | 300 | 300 | PASS |
| `skillCooldownTime` | 0.3 | 0.3 (f32) | PASS |
| `offensiveSlowFireDurationMin` | 3.0 | 3.0 | PASS |

**The one diagnosis (float32, not tolerance).** First G3 run FAILED 3/22 — `maxRange` `9.100000381469727` vs oracle `9.1` (and `startWidth`, `skillCooldownTime`). Per charter law, HALT-diagnosed not fudged. **Layer = the COMPARISON, not the parse:** these are `float32` in the `.arz` (type ID 1); `9.1` is not binary-exact in single precision, so its byte-true float64 value IS `9.100000381469727`; the probe listed the readable literal. Proof exact-not-approx: `struct.pack('<f',9.1)` round-trips to the landed value (`EXACT_MATCH=True`) for all three. Fix (non-fudging): G3 canonicalizes both sides through float32 and asserts identical single-precision bit patterns — byte-matching at the source's native precision, not an epsilon. Parser was byte-true from run one.

---

## Schema shape chosen (for the report-back)

- Tables: **`exact_skill`** (header) + **`exact_skill_field`** (per-field/per-rank).
- Core/extension split: **per-row `is_core` tag** — 107 core (fire min/max, mana, weapon-%, range, cadence, cooldown) + 29 GD-extension (`offensiveSlowFireMin` burn-DoT array 26 + `startWidth`/`endWidth` cone geometry + burn duration). The next adapter adds its own extension rows with no schema change (TSR-2 property demonstrated).

## Harvest-lap hand-offs (flagged, not done this run — out of width-one scope)
1. `skill_geometry_band` FoI bands are still `dossier-prose`/NULL; `exact_skill_field` now holds exact cone geometry to populate `exact_json`/`exact_source_type` and upgrade `derivation` to `datamine`.
2. `source_version` determination (depot manifest / file-hash → GD patch map).
3. `.arc` tag-bridge completion for authoritative display names.
4. Any future grimtools-derived GD damage rows must be re-verified against 26-rank `.arz` primary truth before banking.

## Files + backup
- Adapter: `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py`
- MIGRATION: `agentic_orchestration/research/curated/MIGRATION-gd-slice-exact-fields-2026-07-24.md`
- Report: `agentic_orchestration/elrond/notes/2026-07-24-gd-slice-run.md` (this file)
- Backup: `corpus.db.pre-gd-slice-20260724T002255-backup` (md5 `61457147aa0175fe872d8caec9399356`)
- DB is gitignored; committed artifacts = adapter + MIGRATION + report + `corpus_schema_meta` record inside the regenerable DB.
