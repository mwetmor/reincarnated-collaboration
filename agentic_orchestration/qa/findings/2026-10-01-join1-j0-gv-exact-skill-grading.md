# Finding — 2026-10-01 — JOIN-1 J0 GV: grading of the 675 `exact_skill` rows

**Reviewer:** jack-ryan
**Severity:** WARN (a canon-law labelling defect with zero behavioural consumers; it blocks no JOIN-1 gate)
**Target:** `corpus.db :: exact_skill` (all rows), read-only, 2026-10-01. Charter `agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md` v0.5: § 5 J0 jack-ryan row, § 8 GV row
**Developer:** elrond (curation seam; writer of the rows, migration `gd-devotion-payloads-2026-07-25`)
**Principles applied:** REVIEW_PROCESS #3 (cross-seam impact), #4 (decisions-log and canon as truth), #5 (severity matters). Disciplines #19.1(b), #69, #82
**Sidecar (machine-readable, one record per row):** `agentic_orchestration/qa/findings/2026-10-01-join1-j0-gv-exact-skill-grading.rows.json` (FILE sha256 `96a483ea…`, derived at write time)

---

## Verdict, in one table

| Class | Rows | Owner of the remedy |
|---|---|---|
| **MIS-GRADED, source on disk** | **675** (674 devotion + 1 corpus kit; the corpus kit needs its pin restored first, § 3.2) | **elrond** |
| MIS-GRADED, source missing | **0** | (legolas: nothing owed) |
| Correctly MEASURED | **0** | n/a |
| Ambiguous | **0** | n/a |
| *Outside the 675, the same defect:* `devotion_power` + `devotion_constellation` | *175* | *elrond, in the same pass* |

**Impact on JOIN-1:** none on the three kits, the REFERENT-v1 pack or the KC2 oracle. **No HALT to Matt.** (§ 4)

---

## 1 · The population: where the 675 comes from

- **Source.** `agentic_orchestration/research/curated/corpus.db`, table `exact_skill`, **every row** (no filter). I opened it with `mode=ro`.
- **Count: 675, confirmed.** It matches elrond's P0 census § 8.1 (`elrond/notes/2026-09-28-join1-p0-internal-boundary-census.md:226-227`, `78797db4b`), which is the count the charter carries:

| `entity_kind` | `rank_axis` | `lane` | `fidelity_grade` | `fidelity_basis` | rows |
|---|---|---|---|---|---|
| `corpus_kit` | `bought_rank` | `gd-class-skill` | MEASURED | `primary-source-datamine` | 1 (`gd-flames-of-ignaffar-purifier`) |
| `game_skill` | `none` | `gd-devotion` | MEASURED | `primary-source-datamine` | 605 |
| `game_skill` | `skill_xp_level` | `gd-devotion` | MEASURED | `primary-source-datamine` | 69 |

- All 675 are `game = gd`. Source archives: `database.arz` 446 · `GDX1.arz` 92 (91 devotion + FoI) · `GDX2.arz` 59 · `GDX3.arz` 78. Their dependents in `exact_skill_field` number **7,250**, with 0 orphans and 0 header/field disagreements on `source_file` or `record_path`.

## 2 · What the LAW requires, and why: DATAMINED for every row

The LAW (`canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md` § 4):
- **MEASURED** means *"verified against a live game oracle (fixtures, L0–L5 ladder): attests runtime BEHAVIOR."*
- **DATAMINED** means *"verified against the source game's own shipped data files, edition-pinned + checksum-verified: attests AUTHORED DATA, not runtime behavior."* The LAW applies DATAMINED, **by name**, to the *"GD devotion payload lane (`gd-edition-II-20260724`, 4/4 `.arz` sha256)."*

Each row meets DATAMINED's predicate and fails MEASURED's:
1. **The basis is a pinned extraction.** The rows' own `fidelity_basis = primary-source-datamine`, and 674 of them carry a composite `source_version` (edition · depot · manifest · `arz_sha256`).
2. **No live oracle attests any of the 675 entities.** In `fixtures.db`, `measured_fixture` holds 3 rows, all on `gd-werewolf-kitcal-1`. The only `evidence_claim` rows that mention devotion are `EC-DEVOTION-NO-PROC` and `EC-DEVOTION-ZERO-ASSIGNED`, and both are **absence controls**: they say no devotion was assigned or fired. They do not verify any devotion payload's behaviour.
3. **The same lane's later tables already use the correct word.** `gd_display_tag` (20,490), `gd_monster_record` (4,066) and `gd_monster_bio` (6,627) all carry `DATAMINED`. They were banked hours later on 2026-07-26 by the same seat.

**How the rows came to be labelled MEASURED (this is the record, not a fault-finding exercise).** The devotion migration banked the rows at **2026-07-26T03:29:13Z** (`corpus_schema_meta`). Its § 7 called MEASURED *"a literal overclaim"* and asked gandalf to mint a term (`MIGRATION-devotion-payloads-2026-07-25.md:217-235`). gandalf minted DATAMINED in commit **`557394ec5`** at 2026-07-26T03:37Z, **eight minutes later**. That commit amends the LAW and a charter draft only. It schedules no back-fill, and none ever ran. Elrond's question was answered, but the 675 rows that prompted it were never updated to match the answer.

## 3 · Classification, row by row (the sidecar carries all 675 records)

### 3.1 · The source is on disk and re-derives exactly: verified, not inferred

The pinned Edition-II bytes **are on disk**, though not where the banking scripts look for them (§ 5, INFO-2): `~/depots/<depot>/24346246/…`.

| Archive | On-disk path | sha256 on disk == pin |
|---|---|---|
| `database.arz` | `/Users/admin/depots/219991/24346246/database/database.arz` | `8cdeff12…` ✓ |
| `GDX1.arz` | `/Users/admin/depots/642280/24346246/gdx1/database/GDX1.arz` | `e28ab251…` ✓ |
| `GDX2.arz` | `/Users/admin/depots/897670/24346246/gdx2/database/GDX2.arz` | `f6d5bd67…` ✓ |
| `GDX3.arz` | `/Users/admin/depots/2699230/24346246/gdx3/database/GDX3.arz` | `1661be5e…` ✓ |

**Instrument.** A scratch read-only script imported the adapter's own `ArzArchive` reader, unmodified, from `research/scripts/gd_arz_adapter_2026_07_24.py`. For every row it checked three things:
- (a) the archive's sha256 equals the row's pin;
- (b) the row's `record_path` is present in that archive's record table;
- (c) **every one of the 7,250 `exact_skill_field.raw_value`s** equals the decoded field at its rank (float equality, no tolerance).

**Result:** sha 675/675 · present 675/675 · **field byte-match 7,250/7,250**. In #19.1(b) terms, I read the instrument and did not inherit the claim. The rows are faithful extractions of the pinned bytes. Only their label is wrong.

### 3.2 · Row flags (all inside MIS-GRADED, none of which changes the class)

- **`PIN-RESTORE-REQUIRED`: 1 row, `gd-flames-of-ignaffar-purifier`.** Its `source_version` is **NULL**. Migration `gd-edition-pin-2026-07-24` set it at 2026-07-25T00:25:17Z (`corpus_schema_meta` row 25; `MIGRATION-gd-edition-pin-2026-07-24.md:30` carries the full value: `gd-edition-I-20260723; depot=642280(gdx1/AshesOfMalmouth); manifest=2275863479823292335; arz_sha256=e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539`). The pin is **gone from the live row and from the `exact_skill_pre_devotion_20260725` snapshot alike**, so it was lost before the devotion re-key.
  - **Probable mechanism** (supported by evidence, not proven): the FoI adapter re-landed the row. `gd_arz_adapter_2026_07_24.py:428-429` deletes and re-inserts the row, and `:522-524` hard-codes `source_version = None`. The row's `created_date` reads 2026-07-25, the same day the pin was applied.
  - **Why the class stays MIS-GRADED, not AMBIGUOUS:** the LAW gives an unambiguous answer for this row, and the GDX1 bytes on disk match the recorded pin, which is byte-identical across Editions I and II. The gap is in the row's provenance field. It does not affect the grade question. **But relabelling this row DATAMINED without restoring the pin would put an unsupported claim on the row's face**, because DATAMINED means *edition-pinned*. Restore the pin first.
- **`HEADER-ONLY`: 9 rows** with no field rows. They are 3 `tier{1,2,3}__petbonus` records plus Assassin's Mark, Mark of the Wendigo, Rend, Eldritch Fire, Rumor and Mark of Rattosh. Their headers (`record_type`, `rank_count`, axis) are still `.arz` extractions, the records are present in the pinned archives, and DATAMINED applies.
- **`RECORD-NAMED-BY-KC2-ORACLE-SOURCE`: 3 rows**: Turtle Shell `tier1_29e`, Tip the Scales `tier2_02f`, Arcane Barrier `tier2_17c`. These are cited by `simulation/kc2/counterplay.py:62-83`. See § 4: the oracle names the record paths and reads its own substrate. It never reads these rows or their label.

### 3.3 · The empty classes, stated so the zeros read as findings

- **Source missing: 0.** Every row's archive is on disk with a matching hash, and every record is present.
- **Correctly MEASURED: 0.** No row is backed by a live-oracle fixture (§ 2.2).
- **Ambiguous: 0.** The only candidate was FoI, and § 3.2 explains why it is not ambiguous.

## 4 · Impact: kits, REFERENT-v1, the KC2 oracle

**Zero consumers read the label.** A search for `fidelity_grade` across `reincarnated-collaboration/agentic_orchestration`, `reincarnated-engine/src` + `scripts` and `reincarnated-godot` returns **only its three writers**: `gd_devotion_bank_2026_07_25.py`, `gd_bridge_m1_display_tags_2026_07_26.py` and `gd_bridge_m2_monster_records_2026_07_26.py`.

| Surface | Reads `exact_skill`? | Effect of the mis-grade / of a relabel |
|---|---|---|
| **`d2-ww-barb`** (J-S3) | No. `exact_skill` holds **no D2 rows** (675/675 `gd`) | **None.** J-S3 already grades D2 `Skills.txt` DATAMINED, which is correct under the LAW |
| **`d2-fire-sorc`** (J-S3b) | No (same reason) | **None** |
| **`gd-eor-warlord`** (J-S4) | No. The kit compiler's `kit_reader.py` reads `canon_corpus`, `kit_mapping`, `skill_geometry_band`, `kit_numeric` and `kit_composition` only. The kit JSON's devotion payloads are EMPTY by its own `deviation_notes` | **None.** Its `grade: APPROX` belongs to a different vocabulary (the kit-mapping grade) |
| **REFERENT-v1 pack** (v3.4.2, J-S1) | No. The emitters (`export/kc2_baton*.py`) contain no `exact_skill`, `fidelity_*` or `corpus.db` reference, and neither do the pack files | **None** |
| **KC2 oracle** (`simulation/kc2/`, J-S6) | No. "corpus" in `kc2/*.py` means the pinned `.arz` substrate, not `corpus.db`. The 3 devotion records it names are read from its own substrate | **None. A relabel cannot change ORACLE behaviour; no § 4.7 / § 6 HALT** |

⚑ **A homonym, recorded but not classified (INFO-1).** The KC2 packs carry their own `grade` ladder: `MEASURED / DECODED / INFERRED-WITH-EVIDENCE / DECLARED-FREE-PARAMETER / UNDERIVABLE-WITH-PATH-NAMED`. The v3.4.2 model pack has **17,647** `grade: "MEASURED"` rows, many of them `.arz`- or CSV-derived. That is a **different field with a different vocabulary**, defined in the KC2 lift preregs. **It is not in the GV population, and I make no grading claim about it here.** Whether the LAW § 4 vocabulary governs that ladder is a canon question for gandalf, who owns the LAW. **Any relabel of a sealed REFERENT-v1 pack is a J-S1 change and therefore a HALT to Matt by § 6.** I recommend no such change.

## 5 · Further observations (INFO)

- **INFO-2: the Edition-II tree named in the pins is not on disk under its name.** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` is cited by `gd_devotion_bank_2026_07_25.py:32` and by about ten legolas notes, and it is absent. `~/Games/vendor/` holds only `grim-dawn-edition-IV-20260929`, whose four `.arz` hashes **all differ** from Edition-II. The Edition-III tree (`…edition-III-20260808`) is absent too. The bytes survive under `~/depots/<depot>/24346246/`, which is how C-11b refers to them. #69 says *"the directory name is the pin"*, so this is a #69 hygiene gap. **Re-running the bankers would fail on path, not on bytes.** The relabel in § 6 needs no re-run.
- **INFO-3: relay defect in `MIGRATION-gd-edition-pin-2026-07-24.md:43` and `:92`.** The prose abbreviates the GDX1 hash as `e28ab2…ae3f`, but `ae3f` is the tail of **`database.arz`**'s hash (freeze record line 44). GDX1's hash ends `…4539` (line 45, not the "line 46" the doc cites). Line 30 of the same doc carries the **correct full value**. This is a #79 / derive-don't-relay instance. It is cosmetic, because the row pin used the full value.
- **INFO-4: Edition-IV does not affect GV.** DATAMINED states what the rows attest **about Edition-II**. Whether they carry forward to Edition-IV is a #69 descent question for whoever next consumes them against Edition-IV. A relabel neither licenses nor requires that descent.
- **INFO-5: the population is broader than the figure (#82).** "675" is the `exact_skill` header count. **The defect also sits on `devotion_power` (65) and `devotion_constellation` (110)**: the same migration, the same `MEASURED / primary-source-datamine`. Their sources are on disk: present 175/175, sha 175/175. I did **not** run field-level re-derivation on them. Their records are in the sidecar's `adjacent_population`. **GV's true population is 850 rows in three tables.** The charter's "675" stays correct as a description of `exact_skill`.

## 6 · Remedy

**One data-only correction, owned by elrond. I approve it under ADR-002** as a within-seam data correction: no DDL, no consumer reads the column (§ 4), and nothing touches a sealed artifact. **It is not a cross-seam schema change and needs no Matt surface.** I am not performing it, because `corpus.db` is elrond's layer and my canonical-doc authority does not reach it.

- [ ] **elrond, step 1: restore the FoI pin.** Set `exact_skill.source_version` on `gd-flames-of-ignaffar-purifier` to the full composite at `MIGRATION-gd-edition-pin-2026-07-24.md:30`. Derive it from that line and do not retype it from this finding.
- [ ] **elrond, step 2: relabel.** In **all three tables** (`exact_skill`, `devotion_power`, `devotion_constellation`), change `fidelity_grade` from `MEASURED` to `DATAMINED` wherever `fidelity_basis = 'primary-source-datamine'`. That is **850 rows** (675 + 65 + 110). Keep `fidelity_basis`: it remains true and becomes redundant rather than wrong.
- [ ] **elrond, step 3: guard and assert.**
  - Take a backup first.
  - Post-assert: `MEASURED` = 0 and `DATAMINED` = 675 / 65 / 110 on those tables; row counts unchanged; `exact_skill_field` untouched (7,250); integrity_check ok.
  - Add a `corpus_schema_meta` row.
  - Write a **forward MIGRATION addendum** (ADR-004) that closes `MIGRATION-devotion-payloads-2026-07-25.md` § 7's request as *"answered by LAW § 4, `557394ec5`; back-filled here."* Do not edit the dated migration in place.
- [ ] **elrond, step 4: stop the defect from coming back.** `gd_devotion_bank_2026_07_25.py:61` and `:657` hard-code `'MEASURED'`, and `gd_arz_adapter_2026_07_24.py:522-524` hard-codes a NULL pin. A re-run of either script would re-introduce what steps 1 and 2 fix. Elrond chooses the form: retire the scripts, add a guard, or note it in the addendum.
- [ ] **elrond, optional: correct the hash abbreviation (INFO-3) in the same addendum.**
- [ ] **legolas:** nothing owed for GV (source-missing class = 0). **INFO-2 is routed to legolas** as the acquisition seam: record where the Edition-II bytes now live, or restore the named tree, so that #69's name-as-pin holds. This does not gate GV.
- [ ] **gandalf (INFO-1, non-blocking):** decide whether LAW § 4 governs the KC2 pack `grade` ladder. Any action touching a sealed pack HALTs to Matt.
- [ ] **Matt:** **nothing.** No BLOCK, no ESCALATE, no ORACLE-behaviour change.

**Re-check:** once elrond lands steps 1–3, I re-run the three-table grade census, which takes one query. GV closes on that count, not on the addendum's prose.

## References

- `agentic_orchestration/gandalf/notes/2026-09-29-join-1-run-charter.md` (v0.5; § 5 J0, § 8 GV, § 6 HALTs)
- `canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md` § 4 (and commit `557394ec5`)
- `agentic_orchestration/elrond/notes/2026-09-28-join1-p0-internal-boundary-census.md` § 8.1
- `agentic_orchestration/research/curated/corpus.db` (`exact_skill`, `exact_skill_field`, `exact_skill_pre_devotion_20260725`, `devotion_power`, `devotion_constellation`, `corpus_schema_meta`), plus `fixtures.db`
- `agentic_orchestration/research/curated/MIGRATION-devotion-payloads-2026-07-25.md` § 7 · `MIGRATION-gd-edition-pin-2026-07-24.md` · `MIGRATION.md:136,170,194`
- `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` · `gd_devotion_bank_2026_07_25.py`
- `reincarnated-engine/src/reincarnated/simulation/kit_compiler/kit_reader.py` · `simulation/kc2/counterplay.py` · `export/kc2_baton*.py` · `output/kc2-model-pack-v3-E-s09-cp150-mech-v3p4p2-20260929_063506/`
- `agentic_orchestration/research/curated/kits-export/{d2-ww-barb,d2-fire-sorc,gd-eor-warlord}.json`
- `/Users/admin/depots/{219991,642280,897670,2699230}/24346246/…/*.arz` (Edition-II bytes) · `/Users/admin/Games/vendor/grim-dawn-edition-IV-20260929/`

---

## 7 · RE-CHECK, 2026-10-01: **GV CLOSED**

**Trigger:** elrond applied the § 6 remedy. Records are in collab `a97445c28` (staged at `fcb4f0ebd`); the GV migration-meta row is `join1-j0-gv-relabel-2026-10-01`, dated 2026-10-01T05:04:47Z. I re-ran every check by query, read-only, and derived the digests from disk rather than relaying them.

**The three files compared:**

| File | FILE sha256 (derived) | State |
|---|---|---|
| `corpus.db.pre-gv-relabel-20261001T050447Z-backup` | `e1da2690…3d05` | before GV |
| `corpus.db.pre-join1-j0-20261001T050456Z-backup` | `098f10c7…47d3` | **after GV, before the J0 migration**: this file isolates GV |
| `corpus.db` (live) | `dffad643…d473` | after GV and J0 |

| # | Check | Result |
|---|---|---|
| R1 | `MEASURED` = 0 on `exact_skill` / `devotion_power` / `devotion_constellation` | ✅ 0 / 0 / 0 (live and post-GV) |
| R2 | DATAMINED = 675 / 65 / 110 | ✅ exactly, with no other grade value present |
| R3 | FoI pin restored and equal to the derived pin | ✅ **string-equal** to `MIGRATION-gd-edition-pin-2026-07-24.md` line 30 (compared by shell `=`, not by eye); NULL/empty pins on the three tables = **0** (was 1) |
| R4 | No row changed except the label | ✅ **before-GV → after-GV, cell by cell over every column:** `exact_skill` 675 rows, changed = `fidelity_grade` ×675 + `source_version` ×1 (FoI only) · `devotion_power` 65 rows, changed = `fidelity_grade` ×65 only · `devotion_constellation` 110 rows, changed = `fidelity_grade` ×110 only · no row added or removed. **Whole DB, before-GV → after-GV:** schema byte-identical; tables whose content hash moved = exactly those three + `corpus_schema_meta` (the new row) + `v_exact_skill_by_kit`. That view is a projection of `exact_skill` that includes `source_version`, so it moves with the FoI pin and nothing else. `exact_skill_field`'s original columns are identical before-GV → live (7,250 rows); in live it carries 5 added J0 columns, which are J-L4's change, not GV's. `integrity_check` = ok |
| R5 | Both writers fixed | ✅ `gd_devotion_bank_2026_07_25.py`: `FIDELITY_GRADE = "DATAMINED"` (`:65`), the FoI back-fill literal is amended (`:661`), and **apply mode is retired** (`:866-873`, `sys.exit("RETIRED…")`), because its idempotency path would drop and re-create the corrected tables. `gd_arz_adapter_2026_07_24.py`: the NULL pin is replaced by `derived_edition_pin()` (`:404-414`; it reads line 30 and HALTs unless the bytes' sha matches), and **apply mode is retired** (`:576-580`). Verify and dry-run remain available. Retiring apply mode is stronger than the guard I asked for, and it is the right call: re-banking now needs a new dated script |

**GV is CLOSED: 850 rows relabelled, 1 pin restored, 0 collateral changes.** The § 6 action boxes for elrond, steps 1 through 4, are discharged. INFO-3 (the hash abbreviation) is acknowledged in elrond's migration as a forward note, with the dated document left unedited, which is correct.

### 7.1 · elrond's step beyond the brief: the four `Text_EN.arc` links. **RATIFIED, with one INFO**

**Verified independently.** The tree `~/Games/vendor/grim-dawn-edition-II-20260724/` holds **8 symlinks and 0 regular files** (`du` 0 B). I re-hashed every link through the link:
- The 4 `.arz` match the § 3.1 pins.
- The 4 `Text_EN.arc` (`613457c8…`, `85baef4b…`, `8aec9207…`, `d6e7f781…`) match their recorded pins in `MIGRATION-gd-displayname-bridge-2026-07-26.md:38-41`, and match the Edition-II rows that the Edition-III intake re-verified (`legolas/notes/2026-08-08-kc2-edition-III-intake-and-diff.md:184-196`).

The step is sound, and arguably owed. The M1 display-tag bridge pins and reads those four files, so restoring the named tree without them would have left a second banker unable to re-run. Linking adds no bytes and creates no fork from the pin, and every target was checked before linking. I see no problem with ratifying it.

**INFO-6, non-blocking: the farm is partial, and one of its stated limits is not true for every consumer.** The Edition-II cut held **16** data files: 8 `.arz` and 8 `Text_EN.arc`. The farm links **8**. The other 8 (`mods/survivalmode`, `survivalmode1/2/3`, each `.arz` + `Text_EN.arc`) are **also on disk** under `~/depots/{483840,642281,897671,2699231}/24346246/`, and **all 8 hash to their recorded Edition-II pins** (cut record / Edition-III intake).
- Elrond's limit says *"a script that reads a file not listed here fails loudly on the missing path."* That holds for a **named-path** reader like the bankers. It does **not** hold for a **glob** reader: four legolas scratch scripts (`legolas/scratch/2026-07-28-eor/probe15|16|17*.py`, `2026-08-08-kc2-ed3-diff/d2_tags.py`) `rglob("Text_EN.arc")` over a GD root, and several notes describe *"the eight-archive overlay stack"* at this path. Run against the farm, such a reader would silently get 4 of 8 archives. A record or tag that exists only in a survival-mode archive would then read as **ABSENT**, with no error.
- That matters most for **Crucible** (`survivalmode2`, FG Crucible), which is KC2's own arena precedence. It is the #70 shape: a check that passes over a population it never saw.
- **Recommended remedy (elrond or legolas, their choice; neither gates anything):** either (a) link the other 8 files, so the named tree is complete at 16/16, zero bytes, every target pin-verified (the evidence above shows they all pass); or (b) amend § 8's limit forward to say "named-path readers fail loudly; **glob/overlay readers silently see 8 of 16**." I prefer (a), because it removes the hazard instead of documenting it.

**Re-check signed:** jack-ryan, 2026-10-01. **GV: CLOSED.** No BLOCK, no ESCALATE, nothing to Matt.
