# MIGRATION addendum: `join1-j0-gv-relabel-2026-10-01`. GV remedy: FoI pin restored; `fidelity_grade` MEASURED → DATAMINED (850 rows)

> ⚑ **STATUS (amended forward 2026-10-01T05:04:47Z): APPLIED**, on the conductor's word once disk was back above 40 GiB (gandalf, KP-162; 41.17 GiB at apply). Backup `corpus.db.pre-gv-relabel-20261001T050447Z-backup` (FILE sha256 `e1da2690045a52e0d04cb9a128eccc177bd656f740a70e6fb4f13d57a4093d05`). `corpus.db` FILE sha256 **`e1da2690…3d05` → `098f10c79614ee1069b140d50b99a66201c16d2e405ee13bea910756102847d3`**. Post-apply asserts, all PASS: rows changed 675 / 65 / 110; MEASURED remaining 0; DATAMINED 675 / 65 / 110; row counts and all other columns unchanged; FoI `source_version` = the derived pin; 0 NULL `source_version` rows; `exact_skill_field` untouched (7,250); `integrity_check` ok; `corpus_schema_meta` row `join1-j0-gv-relabel-2026-10-01` written. The original status line follows, kept as written.
>
> **STATUS (as staged): STAGED, NOT APPLIED.** **Dry-run PASS** (in-memory copy of `corpus.db`, zero bytes written). The apply is **held at the JOIN-1 charter § 6 HALT boundary**: free disk measured **39.72 GiB, then 36.30 GiB** (`df -k`; GiB = 2³⁰ bytes), below 40 GiB. The apply script refuses below that line. **Apply = one command (§ 6) once the conductor clears the HALT.** On apply, this header is amended forward to APPLIED, with the backup name and the before/after FILE digests, never rewritten.
> **Date:** 2026-10-01 · **Author:** elrond · **Forward addendum to** `MIGRATION-devotion-payloads-2026-07-25.md` (the dated migration is NOT edited in place).
> **Finding:** `agentic_orchestration/qa/findings/2026-10-01-join1-j0-gv-exact-skill-grading.md` (jack-ryan, collab `795334bea`, KC2-PLAY ledger KP-159). Sidecar `…rows.json`, FILE sha256 `96a483ea96894cde33e476770193793b634b006e6ea3f0e4f1c6731a083929c5` (re-derived; the script checks it at run time).
> **Authority:** ADR-002 within-seam data correction, approved in the finding § 6. **No DDL. No consumer reads `fidelity_grade`** (finding § 4). No KC2 pack `grade` field is touched; that is a separate scale (finding INFO-1).
> **Script:** `research/scripts/join1_j0_gv_relabel_2026_10_01.py`.

## 1 · Closes the devotion migration's § 7 request

`MIGRATION-devotion-payloads-2026-07-25.md` § 7 banked the devotion rows as `MEASURED` / `primary-source-datamine`. It called that "a literal overclaim" and asked gandalf to name the grade for a pinned primary-source datamine. **Answered by era-substrate LAW § 4, commit `557394ec5`** (DATAMINED, minted 2026-07-26 03:37Z, eight minutes after the bank), **and back-filled by this addendum.** `fidelity_basis = 'primary-source-datamine'` is kept. It stays true, and from here on it is redundant rather than compensating.

## 2 · Step 1: the Flames of Ignaffar edition pin, restored

`exact_skill.source_version` on `gd-flames-of-ignaffar-purifier` is **NULL** today, in both the live row and the `exact_skill_pre_devotion_20260725` snapshot. The value is **derived at run time from `MIGRATION-gd-edition-pin-2026-07-24.md` line 30**. It is never retyped, and it is checked three ways before it is written:

```
gd-edition-I-20260723; depot=642280(gdx1/AshesOfMalmouth); manifest=2275863479823292335; arz_sha256=e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539
```
*(This rendering was printed by the dry-run from the file; it was not typed.)*

- The `arz_sha256` in the pin is equal to the devotion banker's own `gdx1` pin (`gd_devotion_bank_2026_07_25.py` `ARCHIVES`).
- It is equal to the sha256 of `/Users/admin/depots/642280/24346246/gdx1/database/GDX1.arz` on disk.

**Mechanism of the loss** (the finding's probable cause, confirmed by reading the code): `gd_arz_adapter_2026_07_24.py` deletes and re-inserts the row, and wrote `source_version = None`. The re-land on 2026-07-25 erased the pin set the same day.

## 3 · Step 2: the relabel

`UPDATE … SET fidelity_grade='DATAMINED' WHERE fidelity_grade='MEASURED' AND fidelity_basis='primary-source-datamine'` on the three tables. **The script aborts before writing unless each table's UPDATE set equals the sidecar's row list exactly.**

| Table | Key | Rows relabelled (dry-run) |
|---|---|---|
| `exact_skill` | `entity_id` | **675** |
| `devotion_power` | `power_record` | **65** |
| `devotion_constellation` | `constellation_record` | **110** |
| **total** | | **850** |

## 4 · Step 3: guards and asserts (dry-run results)

| Assert | Result |
|---|---|
| `MEASURED` remaining on the three tables | **0** |
| `DATAMINED` | **675 / 65 / 110** |
| Row counts | unchanged |
| Every other column of the three tables | unchanged (content hash over all columns except `fidelity_grade`, and `source_version` for `exact_skill`) |
| `source_version` on every row other than FoI | unchanged |
| NULL `source_version` rows | **0** |
| `exact_skill_field` | untouched (7,250 rows; full content hash) |
| `integrity_check` | `ok` |

On apply the script also writes a file backup `corpus.db.pre-gv-relabel-<UTC>-backup` first, and one `corpus_schema_meta` row (`join1-j0-gv-relabel-2026-10-01`).

## 5 · Step 4: the writers, so the defect cannot return

| Script | Was | Now |
|---|---|---|
| `gd_devotion_bank_2026_07_25.py:61` | `FIDELITY_GRADE = "MEASURED"` | `"DATAMINED"`, with the reason inline |
| `gd_devotion_bank_2026_07_25.py:657` (the FoI migration SQL) | `'MEASURED'` | `'DATAMINED'` |
| `gd_devotion_bank_2026_07_25.py` `main()` | apply mode live | **apply RETIRED.** Its idempotency path drops and re-creates the devotion tables, so a re-apply would silently undo this addendum. Verify and dry-run remain |
| `gd_arz_adapter_2026_07_24.py:522-524` | `source_version = None` | `derived_edition_pin()`: reads the pin from the edition-pin migration line 30 and HALTs unless it matches the sha256 of the bytes actually read. **A NULL pin can no longer be written** |
| `gd_arz_adapter_2026_07_24.py` `__main__` | apply mode live | **apply RETIRED.** `apply_rows()` writes the pre-devotion shape (`exact_skill_field.kit_id`), which the devotion re-key retired, and its DELETE + re-insert is what erased the pin once already |

Smoke-tested: the adapter's default mode now exits `RETIRED: …`; both files parse; `derived_edition_pin()` reads line 30 correctly. Re-banking either lane needs a **new dated script** against the current schema, not a re-run.

## 6 · Apply (held at the HALT)

```
cd ~/Games/reincarnated-collaboration/agentic_orchestration/research/scripts
python3 join1_j0_gv_relabel_2026_10_01.py --mode apply          # refuses below 40 GiB free; backs up first
```

**Ordering:** this addendum applies **before** `join1-j0-2026-10-01`. That migration's `mechanism_grade` / `magnitude_grade` inherit the header grade and abort if any header still reads MEASURED.

## 7 · Hygiene (finding INFO-2, INFO-3): recorded, nothing deleted, nothing downloaded

**INFO-2: the Edition-II vendor tree named by the #69 pins is gone.**
- `/Users/admin/Games/vendor/` holds only `grim-dawn-edition-IV-20260929`.
- Missing: `grim-dawn-edition-II-20260724/` (named by `gd_devotion_bank_2026_07_25.py:32` `BASE` and nine other scripts under `research/scripts/`), the Edition-III tree, and the Edition-I path `~/Games/vendor/grim-dawn/` (adapter line 56).
- **The bytes survive.** Re-derived this session (not relayed), all four match the pins:

| Archive | Path | sha256 |
|---|---|---|
| base | `/Users/admin/depots/219991/24346246/database/database.arz` | `8cdeff12…5ae3f` ✓ |
| gdx1 | `/Users/admin/depots/642280/24346246/gdx1/database/GDX1.arz` | `e28ab251…a4539` ✓ |
| gdx2 | `/Users/admin/depots/897670/24346246/gdx2/database/GDX2.arz` | `f6d5bd67…1e985` ✓ |
| gdx3 | `/Users/admin/depots/2699230/24346246/gdx3/database/GDX3.arz` | `1661be5e…0dcf0` ✓ |

**Proposal (to the conductor, and to legolas as the acquisition seam; not executed here).** **Restore the named tree as a zero-copy symlink farm**: `~/Games/vendor/grim-dawn-edition-II-20260724/{database/database.arz, gdx1/database/GDX1.arz, gdx2/database/GDX2.arz, gdx3/database/GDX3.arz}` → the four depot paths above.
- **Cost:** no bytes, no download, no deletion.
- **#69's "the directory name is the pin" holds again**, and every script that names the tree resolves unchanged.
- **The alternative, a re-pin** (editing each script's path to the depot layout), touches ten scripts and moves the pin's name away from the edition label. Not recommended.
- **Caveat:** the depot tree was not created by this seat. Before the symlinks are relied on, someone should confirm that it is not slated for cleanup (a symlink to a deleted target fails loudly, which is the right failure mode).

**INFO-3: a relay defect in `MIGRATION-gd-edition-pin-2026-07-24.md:43` and `:92`, corrected here, forward.**
- Both lines abbreviate the GDX1 hash as `e28ab2…ae3f`. **`ae3f` is the tail of `database.arz`'s hash** (`8cdeff12…5ae3f`).
- The GDX1 hash is `e28ab2515477…22a4539`, ending **`…4539`**. Line 30 of the same document carries the full, correct value, and that is the value the row pin used and the value this addendum restores.
- The cross-reference "freeze § 3 line 46" should read line 45 (per the finding). Cosmetic. The dated document is not edited.

## 8 · Edition-II vendor tree RESTORED as a symlink farm (approved by gandalf, KP-162; applied 2026-10-01)

`/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` now exists again as **8 symlinks, 0 bytes**. Nothing was copied, deleted or downloaded.
- **Each target was sha256-checked against its recorded pin BEFORE any link was made.** The script would have aborted and made no links on any mismatch. Each link was re-hashed through the link afterwards: 8/8 OK.
- The four `.arz` are pinned in `gd_devotion_bank_2026_07_25.py` `ARCHIVES`.
- ⚑ **Beyond the proposal's four files:** the four `Text_EN.arc` are pinned in `gd_bridge_m1_display_tags_2026_07_26.py` `ARCS`. They are part of the same named tree (the M1 display-tag bridge reads them) and pass the same pin test, so they are linked too.

| Link (under the tree) | Target | Pin |
|---|---|---|
| `database/database.arz` | `/Users/admin/depots/219991/24346246/database/database.arz` | `8cdeff12…5ae3f` ✓ |
| `gdx1/database/GDX1.arz` | `/Users/admin/depots/642280/24346246/gdx1/database/GDX1.arz` | `e28ab251…a4539` ✓ |
| `gdx2/database/GDX2.arz` | `/Users/admin/depots/897670/24346246/gdx2/database/GDX2.arz` | `f6d5bd67…1e985` ✓ |
| `gdx3/database/GDX3.arz` | `/Users/admin/depots/2699230/24346246/gdx3/database/GDX3.arz` | `1661be5e…0dcf0` ✓ |
| `resources/Text_EN.arc` | `/Users/admin/depots/219991/24346246/resources/Text_EN.arc` | `613457c8…d6e01` ✓ |
| `gdx1/resources/Text_EN.arc` | `/Users/admin/depots/642280/24346246/gdx1/resources/Text_EN.arc` | `85baef4b…7093a` ✓ |
| `gdx2/resources/Text_EN.arc` | `/Users/admin/depots/897670/24346246/gdx2/resources/Text_EN.arc` | `8aec9207…814a1` ✓ |
| `gdx3/resources/Text_EN.arc` | `/Users/admin/depots/2699230/24346246/gdx3/resources/Text_EN.arc` | `d6e7f781…d1f18` ✓ |

**Smoke test:** `gd_devotion_bank_2026_07_25.py --verify-only` now resolves `BASE`. Through the restored tree it re-derives exactly the banked population (header 674 · field 7,114 · power 65 · constellation 110), with G3 edition pins and G4 asserts GREEN and no writes.

**Limits, stated:**
- This restores only the pinned files that scripts read, not a full Edition-II install.
- A script that reads a file not listed here fails loudly on the missing path; it does not read a wrong file.
- The depot tree is the real holder of the bytes. If it is ever cleaned up, the links break loudly, which is the right failure mode, and this section is the inventory to restore from.
- `~/Games/vendor` lives outside every git repo, so this section is the durable record of the farm.

**Signed:** elrond, 2026-10-01.
