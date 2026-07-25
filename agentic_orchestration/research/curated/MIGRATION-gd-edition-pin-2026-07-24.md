# MIGRATION — GD Edition-I `source_version` backfill (snapshot-with-editions pin)

**Author:** elrond (data steward) | **Date:** 2026-07-24 | **DB:** `agentic_orchestration/research/curated/corpus.db`
**Class:** DATA-ONLY. No DDL. One `UPDATE` on one banked row; ZERO schema change; ZERO other rows touched.
**Schema-meta version:** `gd-edition-pin-2026-07-24`
**Backup:** `corpus.db.pre-gd-edition-pin-20260725T002454Z-backup` (md5 `d0bf037c22555b3ce4352bc18d23e4f4`), pre-write, elrond backup discipline (Discipline #8/#11).
**Post-write corpus.db md5:** `113ebccbd06a9b62cdaa8a068a4b89e6`.

---

## Ruling lineage

Matt **RULING-A — snapshot with editions** (`agentic_orchestration/gandalf/notes/2026-07-24-corpus-edition-disposition-ruling.md` §2):
every banked row carries the manifest pin of the edition it was derived from; expansions produce NEW editions
alongside old ones. Immediate owed consequence (elrond): backfill Edition-I `source_version` **before** any Edition-II
row lands, because mixed populated/blank version columns are worse than uniformly blank. Owed follow-up recorded at
freeze §7 item 1 and cut §7 item 1. Freeze fingerprint: `2026-07-24-gd-edition-I-freeze-fingerprint.md` (§4 pin table).
Edition-II cut: `2026-07-24-gd-edition-II-cut-record.md` (§2 manifest diff, §3 byte-level 11/11 IDENTICAL).

---

## What changed (one line)

`exact_skill.source_version` on `gd-flames-of-ignaffar-purifier` set from `NULL` → the composite Edition-I pin.
No DDL, no other table, no other row. `integrity_check=ok`, `foreign_key_check` clean.

## The pin VALUE and why (elrond seam call)

```
gd-edition-I-20260723; depot=642280(gdx1/AshesOfMalmouth); manifest=2275863479823292335; arz_sha256=e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539
```

The pin is a **composite, self-describing string**, not a bare edition label and not a bare manifest ID. Steward test:
*"exactly which bytes produced this row, two years from now, even if the freeze note is lost?"*

- **Edition label** (`gd-edition-I-20260723`) — human-legible; resolves to the freeze §4 pin table.
- **Depot + friendly name** (`642280(gdx1/AshesOfMalmouth)`) — names which archive, not just which edition. A GD row
  derives from ONE archive; the edition owns twelve depots. The pin must resolve to the archive, and `source_file`
  (`GDX1.arz`) already names the file within it.
- **Manifest ID** (`2275863479823292335`) — the immutable, **empirically byte-validated** version key. Cut §3 proved
  identical manifest ⇒ identical bytes (11/11 IDENTICAL), so this ID means what we need it to mean. This is the depot
  642280 (gdx1) manifest, **unchanged** across Editions I and II (cut §2).
- **`arz_sha256`** (`e28ab2…ae3f`) — the SHA-256 of the exact `gdx1/database/GDX1.arz` bytes the adapter read (freeze §3
  line 46). This makes the pin **verifiable against the frozen bytes with ZERO dependency on the freeze note surviving.**
  A bare edition label fails the steward test (external lookup required); a bare manifest fails legibility. The composite
  passes both and is self-checking.

**Rejected alternatives:** (a) bare `gd-edition-I-20260723` — meaningless if the freeze note is lost; (b) bare manifest
ID — loses edition context and which-archive resolution; (c) all twelve depot manifests — the row derives from one
archive; pinning eleven irrelevant depots buries the load-bearing one.

## Schema delta

**None.** The existing `exact_skill.source_version TEXT` column fits; its schema comment already anticipated this
("GD build/patch if determinable"). No new column, no editions lookup table. Rationale for NOT building an editions
table now: exactly one edition-derived kit exists (width-one slice). A normalized `editions` lookup + FK is the right
shape once ≥2 editions have banked rows and the composite string starts repeating — flagged below as a future
normalization, not built speculatively (schema-for-the-data-that-exists, not the data I wish existed). Until then the
self-describing composite is the correct low-ceremony pin; the freeze §4 table is the authoritative expansion.

## Which rows I pinned vs did NOT — the `.arz`-datamine boundary

The edition pin answers "which frozen `.arz` bytes produced this row." It applies **only** to rows genuinely datamined
from the `.arz` primary source — NOT to GD rows sourced from community harvests (grimtools / wikis), which carry their
own citation provenance and no manifest.

| Table | GD rows | `.arz`-datamined? | Pinned? |
|---|---|---|---|
| `exact_skill` | 1 (`gd-flames-of-ignaffar-purifier`) | **YES** (`source_file=GDX1.arz`) | **YES — this migration** |
| `exact_skill_field` | 136 (same kit) | YES | version carried by header row; **no `source_version` column** (see below) |
| `kit_numeric` (FoI) | 26 scalars | NO — `source_anchor`=`lonewardengaming.com`/`grimdawn.com` (web) | no |
| `kit_dossier` (FoI) | prose | NO — `extraction_provenance=fetched-vdm1` (web crawl) | no |
| `skill_geometry_band` (FoI) | 2 | NO — `derivation=dossier-prose`, `exact_source_type=NULL` | no |
| other 40 GD `canon_corpus` kits | 40 | NO — community-harvest | no |

**Why `exact_skill_field` (136 rows) is not separately pinned:** it has no `source_version` column by design — one
version-per-skill lives on the `exact_skill` header, joined by `kit_id`. The field rows carry `source_file`/`record_path`
(same `GDX1.arz`) so provenance is intact; the version resolves through the header. This is a deliberate normalization
(no per-rank version duplication), not a gap.

## FINDING — the record lives in gdx1, not gdx2 (surfaced for a ruling)

Cut record §6 states "Flames of Ignaffar lives in gdx2; `GDX2.arz` is byte-identical across editions." **For this banked
record that is incorrect.** Verified empirically against the frozen Edition-I archives using the GD adapter's own
`ArzArchive` reader:

- `records/skills/playerclass07/purifyingflame1.dbr` is **present in `gdx1/GDX1.arz`** (18,447 records) and
  **absent from both `gdx2/GDX2.arz`** (16,451 records) **and `base/database.arz`** (34,114 records).
- The banked row's `source_file=GDX1.arz` and the adapter's hard-coded source
  (`~/Games/vendor/grim-dawn/gdx1/database/GDX1.arz`, adapter line 56) both agree: the byte-matched record was read
  from gdx1.
- Frozen `gdx1/database/GDX1.arz` SHA-256 = `e28ab2…ae3f` = freeze §3 line 46. Same bytes.

**Likely cause of the cut-record slip:** Flames of Ignaffar is thematically an Inquisitor skill and the Inquisitor
mastery shipped with Forgotten Gods (gdx2). But GD's archive layout does not map to expansion marketing — the base
skill record ships in the gdx1 archive; gdx2 carries only `itemskillsgdx2/.../purifyingflame.dbr` item-skill modifiers,
not the base skill.

**Materiality: LOW for correctness, worth a note for the record.** Both gdx1 (642280) and gdx2 (897670) manifests are
byte-identical across Editions I and II (cut §2), so the row is NOT version-skewed under either reading. But the pin
must name the archive that ACTUALLY produced the row, so I pinned **gdx1 / 642280**, not gdx2. The cut-record §6 line
should be read as "the FoI item-skill modifiers live in gdx2; the base skill record lives in gdx1" — flagged for gandalf
to annotate the cut record if desired. No corpus change hinges on it.

## Coverage-boundary declaration (Discipline D-a)

The task is complete for the population it was scoped to. Explicitly:

**INSPECTED (and this is the complete `.arz`-datamine population):**
- `exact_skill` — all rows (1). Pinned. Verified 1 total / 1 pinned / 0 blank post-write.
- `exact_skill_field` — all rows (136). Confirmed no `source_version` column exists; version resolves via header.
- Every other corpus table (42 total, incl. views) column-scanned for `manifest`/`depot`/`edition`/`arz`/`source_version`
  columns: **`exact_skill.source_version` is the only such column in the DB.**
- GD provenance of `kit_numeric`, `kit_dossier`, `skill_geometry_band` for the FoI kit spot-checked: all community-web /
  dossier-prose, none `.arz`-datamined — correctly NOT pinned.

**NOT INSPECTED / OUT OF SCOPE (declared so a clean result here does not imply completeness elsewhere):**
- The 40 non-FoI GD `canon_corpus` kits' community-source rows — no manifest pin applies to them by design; I did NOT
  audit each for citation-freshness (not this task).
- `monster_numeric` GD rows (if any) — the monster-side store carries `source_url`/`source_date` (web provenance), not
  an `.arz` manifest; not `.arz`-datamined, not in this pin's population. Not row-by-row audited.
- Non-GD lanes (D2 / PoE1 / PoE2 / LE) — no `.arz` datamine exists for any of them yet; their eventual primary-source
  pins are a future obligation under RULING-A's generalization clause (ruling §5), not this migration.
- I did NOT re-run the GD-SLICE G3 byte-match; the cut record's 11/11 IDENTICAL already proves the gdx1 bytes are
  unchanged, so re-verification would be redundant. The FoI certificate survives untouched (cut §6).

**A clean pin on the one row I looked at does NOT imply every GD row now carries correct provenance — it implies the one
`.arz`-datamined kit does, and that is the entire `.arz`-datamine population as of this migration.**

## Reversibility

1. **Restore from backup:** `corpus.db.pre-gd-edition-pin-20260725T002454Z-backup` (md5 `d0bf037c22555b3ce4352bc18d23e4f4`)
   restores exact pre-write state (`source_version=NULL`).
2. **In-place revert:** `UPDATE exact_skill SET source_version=NULL WHERE kit_id='gd-flames-of-ignaffar-purifier';` —
   single-row, exact inverse.
3. The write was transactional (`BEGIN/COMMIT`) and guarded (`WHERE source_version IS NULL`) so it is idempotent: a
   re-run touches 0 rows.

## Boundary note (ADR-004)

Change to elrond's own data layer (`corpus.db`) only. No engine-telemetry schema, no engine source, no cross-seam
ADR-004 request. The `.arz` is read-only vendor data; the frozen Edition-I tree is read-only. DB is gitignored — the
committed artifacts are this note, the MIGRATION.md top entry, and the `corpus_schema_meta` record inside the
regenerable DB. Auto-committed per project discipline (Matt-authorized). **NO push.**
