# MIGRATION — GD-SLICE normalized exact-fields schema (first adapter proves the schema)

**Author:** elrond (data steward) | **Date:** 2026-07-24 | **DB:** `agentic_orchestration/research/curated/corpus.db`
**Class:** ADDITIVE. Two new tables (`exact_skill`, `exact_skill_field`); one kit's rows landed; ZERO overwrites of banked rows.
**Backup taken:** `corpus.db.pre-gd-slice-20260724T002255-backup` (+ `.md5.txt` = `61457147aa0175fe872d8caec9399356`), pre-DDL, elrond backup discipline (Discipline #8/#11).
**Adapter (durable, committed, rebuild-guaranteeing):** `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` (idempotent + `--verify-only` + `--dry-run`).
**Schema-meta version:** `gd-slice-exact-fields-2026-07-24`

---

## Ruling lineage

**gandalf GD-SLICE run charter** `agentic_orchestration/gandalf/notes/2026-07-24-gd-slice-run-charter.md`, ratified by
standing rulings **TSR-1** (player-facing canonical values + raw provenance columns), **TSR-2** (per-game adapters →
ONE normalized exact-fields schema; game-agnostic core + per-game extension; the FIRST adapter proves the schema),
**TSR-3** (GD first adapter — Matt 2026-07-24), **TSR-4** (three-tier verification: family anchors / in-pipe asserts /
spot-checks). Source of the .arz format + oracle: legolas probe `2026-07-23-gd-arz-extraction-probe.md`.

**Intent (charter §0):** prove the TRUE-SOURCES pipe end-to-end **at width one** — GD `.arz` → GD adapter → normalized
exact-fields schema → corpus rows for Flames of Ignaffar, byte-verified against `.arz` ground truth. VERIFIED CLAIM
CEILING: *"the GD adapter path is proven at width one."* This is **not coverage** (harvest lap is next).

---

## The schema (G1) — two additive tables

The normalized exact-fields surface separates the **skill header** (one row per skill) from **per-field/per-rank
values** (the exact-number payload). The TSR-2 game-agnostic-core / per-game-extension split is carried by a per-row
`is_core` flag rather than by separate tables — one queryable surface, the extension fields tagged, not walled off.

### `exact_skill` — header (PK `kit_id`)

| Column | Meaning | TSR |
|---|---|---|
| `kit_id` | FK → `canon_corpus(kit_id)` — the join to the existing corpus | join key |
| `game`, `display_name` | player-facing canonical name (via G4 `skillBitmapName` workaround) | TSR-1(a) |
| `record_type` | LP_string record class (`Skill_AttackSpellCone`) | provenance |
| `rank_count` | authoritative rank cardinality (**26** for FoI) | anchor |
| `source_file`, `source_version`, `record_path` | raw provenance: file, GD build, `.dbr` path | TSR-1 raw |
| `ext_json` | per-game extension meta (`skillMaxLevel`, `skillUltimateLevel`, `templateName`, `skillBitmapName`, `skillDisplayName` tag) | TSR-2 ext |
| `name_provenance` | flag: `.arc` tag-bridge PENDING (see G4) | TSR-1 |
| `adapter`, `schema_version`, `created_date` | reproducibility | reversible-law |

### `exact_skill_field` — per-field/per-rank (PK `kit_id, canon_key, rank`)

| Column | Meaning | TSR |
|---|---|---|
| `canon_key` | player-facing **canonical key** (game-agnostic vocab, e.g. `damage_fire_min`) | TSR-1(a) |
| `rank` | 1-based rank (1..26); `NULL` for static scalars | — |
| `canon_value`, `canon_unit` | player-facing canonical value + normalized unit tag | TSR-1(a) |
| `raw_field` | **exact `.arz` field name** (`offensiveFireMin`) — tagged, not encoded | TSR-1 raw |
| `raw_value` | byte-faithful value from the record | TSR-1 raw |
| `field_kind` | `rank_array` \| `static` | schema |
| `is_core` | 1 = game-agnostic core; 0 = per-game extension | TSR-2 |
| `monotonic_class` | 1 = field-class implies non-decreasing across ranks (drives tier-2 assert) | TSR-4(2) |
| `source_file`, `record_path`, `schema_version`, `created_date` | raw provenance | TSR-1 |

**Why this shape (elrond seam call).** `canon_key`↔`raw_field` is an explicit two-column mapping — the canonical
player-facing vocabulary and the raw source field name are BOTH first-class, so provenance is never lost and the
transform is reversible from the raw column alone (Discipline #14 spirit: tagged, not encoded — no meaning packed
into compound IDs). The core/extension split is a per-row tag: GD's cone geometry (`startWidth`/`endWidth`), burn-DoT
array (`offensiveSlowFireMin`), and burn duration are `is_core=0` (no D2/PoE analog per probe §5); fire min/max, mana
cost, weapon-damage-%, range, cadence, cooldown are **`is_core=1`** (cross-game concepts). The landed split is
107 core + 29 GD-extension rows.
The next adapter (D2/PoE1) adds its own `is_core=0` extension rows without a schema change — that is the TSR-2
"first adapter proves the schema" property, now demonstrated.

---

## The adapter (G2) — `gd_arz_adapter_2026_07_24.py`

Productionizes the legolas probe's `.arz` format knowledge (probe §0) into elrond curation tooling. The probe script
was an instrument; this is the product. Three concerns, cleanly separated:

1. **`ArzArchive`** — a reusable TQIT `.arz` reader. Header (24-byte), string table, record table, per-record LZ4-block
   decompress + DBR field decode (type IDs 0/1/2/3). Indexes 18,447 records + 57,204 strings from `GDX1.arz`.
2. **`build_rows`** — the GD adapter: raw `purifyingflame1` record → normalized `exact_skill` header + `exact_skill_field`
   rows (one per field×rank for arrays, one per field for statics), each carrying canonical value + raw provenance.
3. **`tier2_asserts` / `g3_byte_match`** — verification (below).

**Parser bring-up — the one bug, named.** First bring-up walked off the string table (`IndexError`). Root cause: the
`.arz` string table carries a **`u32 COUNT` prefix** (57,204) before the LP_string entries; without skipping it, the
count is misread as the first string's length. Fix: consume the 4-byte prefix. Confirmation the fix is correct — after
it, the record-table walk consumes exactly to its end boundary (`final pos == rt_offset + rt_size`, 0 bad name_ids,
18,447 records). This is documented inline in `_parse_string_table` so future adapters (D2/PoE use different formats,
but a second GD source — `database.arz`, `GDX2.arz` — reuses this reader) inherit the correction.

**Tier-2 in-pipe asserts (G2, oracle-free, on EVERY row):** non-null on `canon_value`/`raw_value`; range bounds
(no negative damage/cost/pct/geometry); **monotonic non-decreasing** across ranks for the five rank-array field
families (field-class implies growth — flagged per-field via `monotonic_class`). **136/136 rows GREEN.**

---

## Verification (G3) — byte-match against the `.arz` ground-truth oracle

Tier-1 family anchor (TSR-4): FoI is GD's first formula-family anchor. Landed values **BYTE-MATCH** the probe §2
oracle across all five R-K5 rank-array families + geometry + cadence + rank count. **22/22 anchors PASS.**

| Anchor | Expected (probe §2) | Landed | Verdict |
|---|---|---|---|
| `rank_count` | 26 | 26 | PASS |
| `offensiveFireMin` [r1 / r16 / r26] | 8.0 / 129.0 / 262.0 | 8.0 / 129.0 / 262.0 | PASS |
| `offensiveFireMax` [r1 / r16 / r26] | 18.0 / 157.0 / 306.0 | 18.0 / 157.0 / 306.0 | PASS |
| `offensiveSlowFireMin` (burn DoT) [r1 / r16 / r26] | 8.0 / 211.0 / 382.0 | 8.0 / 211.0 / 382.0 | PASS |
| `skillManaCost` [r1 / r16 / r26] | 7.0 / 39.0 / 69.0 | 7.0 / 39.0 / 69.0 | PASS |
| `weaponDamagePct` [r1 / r16 / r26] | 9.0 / 42.0 / 58.0 | 9.0 / 42.0 / 58.0 | PASS |
| `maxRange` | 9.1 | 9.1 (f32) | PASS |
| `endWidth` | 4.5 | 4.5 | PASS |
| `startWidth` | 2.2 | 2.2 (f32) | PASS |
| `timeBetweenAttacks` | 300 | 300 | PASS |
| `skillCooldownTime` | 0.3 | 0.3 (f32) | PASS |
| `offensiveSlowFireDurationMin` | 3.0 | 3.0 | PASS |

### The one diagnosis — float32, not tolerance

First G3 run FAILED 3/22: `maxRange` landed `9.100000381469727` vs oracle `9.1`; same for `startWidth` (2.2) and
`skillCooldownTime` (0.3). Per charter law ("name which layer; never tolerance-fudge") this was **HALT-diagnosed**, not
fudged. **Layer named: the COMPARISON, not the parse.** These fields are `float32` in the `.arz` (type ID 1); `9.1` is
not binary-exact in single precision, so its byte-true value promoted to float64 IS `9.100000381469727`. The probe §2
oracle listed the human-readable single-precision literal. Proof it is exact, not approximate: `struct.pack('<f', 9.1)`
round-tripped equals the landed value with `EXACT_MATCH=True` for all three. Fix (non-fudging): G3 canonicalizes **both
sides through float32** and asserts identical single-precision bit patterns — that is byte-matching at the source's
native precision, not an epsilon tolerance. (4.5 / 3.0 / all integral rank values are binary-exact and pass raw.) The
parser was byte-true from the first run; only the compare needed to respect the source's storage precision.

Post-apply, G3 is re-run against the rows **read back from SQLite** (float64 storage → re-canonicalized to float32):
**CLEAN.** `foreign_key_check` clean, `integrity_check` ok.

---

## G4 — provenance + name bridge

- **Raw provenance populated:** `raw_field` (exact `.arz` name), `raw_value` (byte-true), `record_path`
  (`records/skills/playerclass07/purifyingflame1.dbr`), `source_file` (`GDX1.arz`).
- **`source_version`:** left `NULL` and flagged — `GDX1.arz` carries no in-record build tag this adapter parses. Not a
  blocker; a downstream determination (depot manifest / file-hash → patch map).
- **Display name:** "Flames of Ignaffar" via the `skillBitmapName` workaround
  (`skillicon_flamesofignaffar1up.tex` → readable stem), stored in `exact_skill.display_name`. `name_provenance` column
  flags that the authoritative `.arc` tag-bridge (`skillDisplayName = tagGDX1Class07SkillName04A`) is **PENDING** —
  `.arc` parsing is NOT in scope (charter G4). The raw tag is preserved in `ext_json.skill_display_tag` so the bridge
  can be completed later without re-parsing the `.arz`.

---

## G5 — contradiction hygiene (NO overwrites)

The probe §2 material finding: grimtools `all_skills.js` reports **60-rank** arrays for FoI; the `.arz` ground truth is
**26 ranks** (`skillMaxLevel` 16 + `skillUltimateLevel` 26). This validates the TRUE-SOURCES premise (community harvest
disagrees with primary source).

**Sweep result — the 60-rank shape is NOT banked anywhere in corpus.db.** Verified:

| Store | Content | 60-rank arrays? |
|---|---|---|
| `kit_numeric` (FoI) | **26 rows — formula-constant SCALARS** (crit multipliers, attr-per-point coefficients, PtH constants, `foi_tick_interval_sec`). NOT damage rank-arrays. | none |
| `kit_dossier` (all GD) | prose skill_loop / geometry / item / capstone / author / variants | 0 (swept for ≥30-element arrays) |
| `skill_geometry_band` (FoI) | 2 rows, `derivation='dossier-prose'`, `exact_json`/`exact_source_type` NULL | none |

So the 60-vs-26 contradiction lives **only in the legolas join-surface probe note §2c** (an observation of the grimtools
source), never in banked rows. **G5 is therefore a curation-note flag** (this section), not a row-flag: there are no
banked 60-rank rows to flag and **zero rows were overwritten** — the FoI `kit_numeric` scalars are intact (re-verified
post-apply: `foi_tick_interval_sec=0.3`, `crit_mult_pth070=1.0`). This matches the charter exactly ("No silent
overwrite of banked rows this run — reconciliation is the harvest lap's charter"). The reconciliation obligation for the
harvest lap: if any grimtools-derived GD rows are ingested later, they must be re-verified against the 26-rank `.arz`
primary truth before banking, and any prior grimtools-derived GD damage numbers (none currently) flagged for
re-verification.

**`exact_skill` vs `skill_geometry_band` (a note for the harvest lap, not a change now):** `skill_geometry_band` carries
FoI as `delivery_class='zone'` with `range_band`/`width_band` still NULL and `derivation='dossier-prose'`. The new
`exact_skill_field` now holds the exact `maxRange=9.1` / `startWidth=2.2` / `endWidth=4.5` cone geometry that would let
those bands be derived from primary source. **Not reconciled this run** (out of the width-one slice scope); flagged so
the harvest lap can populate `skill_geometry_band.exact_json` / `exact_source_type` from `exact_skill_field` and
upgrade the FoI bands' `derivation` to `datamine`.

---

## Reversibility

1. **Re-run (intended):** `python3 scripts/gd_arz_adapter_2026_07_24.py` is idempotent — it `DELETE`s prior slice rows
   for the kit then re-lands, so re-running against the current-patch `.arz` reproduces the exact rows.
2. **Restore from backup:** `corpus.db.pre-gd-slice-20260724T002255-backup` (md5 `61457147aa0175fe872d8caec9399356`).
3. **Drop:** the two tables are additive and isolated (`exact_skill`, `exact_skill_field`); dropping them removes the
   slice with no effect on any existing table.

## Boundary note

Change to elrond's own data layer (`corpus.db`) only. No engine telemetry schema, no engine source, no ADR-004
cross-seam request. The `.arz` is read-only vendor data. KR verifies and pushes; elrond commits (DB file is gitignored —
the committed artifacts are this note, the adapter script, the run report, and the `corpus_schema_meta` record inside
the regenerable DB).
