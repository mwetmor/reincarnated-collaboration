# VDM-2 Migration Package — Wave W3a — REVIEWABLE ARTIFACT for jack-ryan Gate-2

**Author:** elrond (data steward) · **Date:** 2026-07-22 · **Status:** ASSEMBLED (assemble ≠ apply; corpus.db UNTOUCHED, md5 verified)
**Run:** `2026-07-22-vdm2-edition-next-lap` (gandalf `RUN-CONDUCTOR`) · **Wave:** W3a (post-W2 all-gates-PASS `c4298612`)
**Gate:** this package is the pre-registered commitment-boundary safety BEFORE the first corpus.db mutation. **W3b apply runs ONLY after jack-ryan Gate-2 PASS.**
**corpus.db:** `agentic_orchestration/research/curated/corpus.db` @ `v1.1-verified` · **md5 `50df15b776ad5b0da93fe90cdee1163d`** at open AND close (assemble is note-space + throwaway-copy only; the live db was never touched).

---

## 0. PACKAGE MANIFEST (what to review)

| # | Artifact | Path (all in `elrond/notes/`) | Role |
|---|---|---|---|
| 1 | **DDL v1** | `2026-07-22-vdm2-ddl-v1.sql` | v0 + A-1..A-7 folded; 12 tables + 9 cols; the CHECK-safety header |
| 2 | **Data riders + seeds** | `2026-07-22-vdm2-riders.sql` | corpus_class/court/eras/original_element/atlas_coords riders + A-2/A-3 seeds + A-7 preserve-NULL |
| 3 | **Apply script** | `2026-07-22-vdm2-w3b-apply.sh` | runnable W3b sequence (backup-first → DDL → riders → asserts → v2.0 LAST); **DO NOT RUN this wave** |
| 4 | **MIGRATION.md draft** | `2026-07-22-vdm2-migration-draft.md` | ADR-004 entry; per-game era vocabs; additive/reversibility/downstream-deps |
| 5 | **This package report** | `2026-07-22-vdm2-w3a-migration-package.md` | the reviewable overview + census answers |

**Provenance chain:** W0 diff (`2026-07-22-vdm2-schema-diff-and-ddl-v0.md`) → DDL v0 → W2 pilot (`2026-07-22-vdm2-pilot-4kit.md`, all 5 gates PASS, A-1..A-7) → **this W3a package**. Rulings: charter + run-state ledger V-6/V-11..V-19.

---

## 1. WHAT THE PACKAGE DOES (one screen)

Lands the VDM-2 field-delta spec as an **additive** schema extension. The store is normalized-relational (not the spec's flat JSON), so six flat blocks re-home as `kit_id` side-cars. **Nothing existing is dropped/altered/re-keyed.** DDL v1 = DDL v0 + the 7 pilot amendments. The cheap census riders populate 5 columns; the side-car tables + `capstone`/`exact_json`/`normalization_rule` stay empty/NULL for named downstream waves.

**The apply is gated behind Gate-2, backup-first, and per-assert census checks that abort→rollback on any mismatch. The v2.0 stamp is the LAST statement and only lands if every assert passes.**

---

## 2. THE 7 AMENDMENTS (A-1..A-7) — how each folded, and its blast radius

| # | Amendment | Where in v1 | Kind | CHECK/rebuild? | VDM-1 touch? |
|---|---|---|---|---|---|
| A-1 | `self` → `range_band` enum | DDL P1-A `skill_geometry_band.range_band` | enum-value add | CHECK on **v1-NEW** table | **none** |
| A-2 | `parallel_triggers`/`trigger_condition`/`cadence_scale` trigger-door args | riders SEED A (`door_arg_schema` data rows) | DATA rows | no | none |
| A-3 | `fan_spread` → motion registry | riders SEED B (`motion_signature_registry` data row) | DATA row | no | none |
| A-4 | `real` → `arg_type` enum | DDL P0-A `door_arg_schema.arg_type` | enum-value add | CHECK on **v1-NEW** table | **none** |
| A-5 | origin vocab `at_target`/`self_and_proxies` | DDL P1-A `origin` column comment | doc-only (origin is free TEXT) | no | none |
| A-6 | corpus_class system tally = **19** (not 11) | riders RIDER 1 + this report §3 | doc/census | no | none |
| A-7 | preserve NULL `t4_doors` | riders A-7 block (NO strip UPDATE exists) | rider-behavior guarantee | no | none |

**The brief's pre-registered check — CONFIRMED:** the only two amendments touching a CHECK are **A-1** (`skill_geometry_band.range_band`) and **A-4** (`door_arg_schema.arg_type`). Both CHECKs live on tables **introduced by v0/v1 itself** — those tables do not exist in corpus.db yet. Therefore **A-1/A-4 incur no SQLite table-rebuild and touch zero VDM-1 data** (the tables are empty at CREATE). The two existing-table CHECKs a rebuild could have been forced on (`verify_ledger.claim_family`/`verdict`) are NOT touched — §7 needs no new family/verdict value. **Stated in the DDL v1 package header.**

---

## 3. THE A-6 CENSUS — record / annex / system over 585 (this closes the tally)

`corpus_class='system'` = **all 19 `is_system=1` rows** (V-14; NOT 11). The three historical figures reconcile as three definitions of "system":

| Figure | Definition | Verdict |
|---|---|---|
| **19** | all `is_system=1` | **the A-6 / V-14 figure — correct** |
| 11 | `is_system=1` AND no `kit_mapping` (W0 D-4 conflated "system-record" with "no mapping") | a subset |
| 22 | stale V9 `null_grain` snapshot (current `null_grain` = 11) | stale |

**Definitive partition over 585 (verified live, read-only):**

```
system = 19   (all is_system=1)  =  11 unmapped  +  8 mapped
record = 267  (is_system=0, corpus_bucket ∈ {poe1,d2,gd,poe2,le})
annex  = 299  (is_system=0, other 12 games)
--------------------------------------------------------------
total  = 585   ✓   [267 + 299 + 8-mapped-system = 574 kit_master ✓;
                     the 11 unmapped-system = the 585-574 gap]
```

- **11 unmapped system-records:** chr-crown-proc-engine, hades1-privileged-status, hot-artifact-stack, hot-gear-well-retrieval, la-monetization-confound, ud-chaos-dungeon-ladder, ud-classless-triad, ud-gear-enchant-economy, ud-link-rune-grammar, ud-zodiac-board, vs-golden-egg-scaling.
- **8 mapped system-records** (inside kit_master's 574): d3-lod-archetype, di-essence-transfer, di-inferno-ladder, di-resonance-awakening, hades2-omega-magick, **le-low-life-ward, poe2-grim-feast, poe2-temporalis-blink**.
- **The 3 record-game system-records** (le-low-life-ward + poe2-grim-feast + poe2-temporalis-blink) are all in the 8-mapped subset → record-CLASS = 267 even though record-BUCKET = 270.

**Rider-verified on throwaway:** corpus_class → record 267 | annex 299 | system 19 | NULL 0. Exact.

---

## 4. COURT COVERAGE + THE 13 NULL-ROW LIST (V-15)

**Coverage: 257/270 courted (95.2%), 13 honest-NULL** — lands in V-15's expected ≈257–260/270.
Distribution: **physical 90 · fire 54 · chaos-poison 44 · lightning 42 · cold 27 · NULL 13.**

**Mapping applied (within Q38 k=5; k NOT changed):** `fire`→fire · `cold`→cold · `lightning`,`aether`→lightning · `physical`,`physical?`,`pierce`,`bleed`→physical · `chaos`,`poison`,`acid`,`necrotic`,`vitality`,`void`,`void?`→chaos-poison · `?`-suffix uses base element's court.

**Reviewer flag (documented, not silent):** `pierce`(2)/`bleed`(2) → physical is a **rider extension** — V-15 named the decay set + the `?`-rule but did not enumerate `pierce`/`bleed`. Both are physical-family sub-tokens in every record-game taxonomy (bleed = physical DoT; pierce = physical weapon damage). Assigning them to the physical court is within k=5 and V-15's spirit. **If the reviewer prefers these NULL, delete the two tokens from the rider's physical WHEN-clause; coverage drops 257→253 and the 4 GD kits join the NULL list.**

**The complete 13 NULL-court rows** (V-15 honest-NULL for magic/n/a/mixed + the 3 genuinely-ambiguous multi/shadow tokens the ruling did not reach; all Leg-B per-kit-resolution candidates):

| elem_raw | count | kit_ids |
|---|---|---|
| `magic` | 4 | d2-berserker · d2-bonemancer · d2-hammerdin · d2-wl-abyss |
| `n/a` | 5 | d2-teleport-sorc · le-low-life-ward · poe1-aurabot · poe2-grim-feast · poe2-temporalis-blink |
| `mixed(fire/cold/lightning)` | 1 | gd-panettis-mage-hunter |
| `physical/chaos` | 1 | poe1-blood-magic-kit |
| `shadow?` | 1 | d2-wl-tainted-summoner |
| `shadow/blood?` | 1 | d2-wl-blood-boil |

`court` is **mutable** (V-18): runs on frozen-at-apply `elem_raw`; W5 elem_raw corrections re-derive affected rows later (W5 precedes Leg-B). W3 does NOT block on the ~6–8 W1-flagged anomalies.

---

## 5. PER-GAME ERA-TOKEN VOCABULARIES (V-16 option (c))

Fixed lowercase set PER GAME; NO cross-game ordinal in the column (shelves derive at Leg-B per Q38 eras=shelves). Raw `eras` preserved. Full lists also in the MIGRATION.md draft.

| game | tokens (count) |
|---|---|
| **poe1** (15) | `1.x` · `2.x` · `3.0-3.6` · `3.2-3.6` · `3.4-3.6` · `3.5-3.6` · `3.7-3.13` · `3.8-3.13` · `3.11-3.13` · `3.12-3.13` · `3.14-3.19` · `3.15-3.19` · `3.16-3.19` · `3.19` · `3.20+` |
| **d2** (16) | `classic` · `lod` · `lod-1.09` · `lod-1.09+` · `lod-1.10+` · `lod-1.11+` · `lod-infinity+` · `lod-pvp` · `d2r` · `d2r-2.4+` · `d2r-2.6+` · `d2r-pvp` · `rotw` · `rotw-s13` · `rotw-s13+` · `rotw-s14` |
| **gd** (5) | `base-2016` · `aom-2017` · `fg-2019` · `patch-1.1-1.2` · `foa-pending` |
| **poe2** (5) | `0.1` · `0.2-dawn` · `0.3-edict` · `0.4` · `0.5-ancients` |
| **le** (5) | `beta-0.8-0.9` · `1.0-launch` · `1.1-harbingers` · `1.2-woven` · `1.4-omens` |

**Note (report-what-exists):** poe1's overlapping bands (`3.7-3.13`/`3.8-3.13`; `3.14-3.19`/`3.15-3.19`/`3.16-3.19`) are legitimate distinct per-kit first-viable-window markers, NOT ingest errors. The vocabulary is a validation contract: a token outside its game's set is a W4/W5 lint, not a silent normalization. `eras_normalized` non-NULL on record = 268/270 (2 poe1 rows have NULL eras — honest).

---

## 6. THE OTHER RIDERS (cheap census) + WHAT STAYS EMPTY

**Populated at W3b (rider-verified on throwaway, exact):**
- `original_element` ← `elem_raw` promotion: **270/270** on record (total; elem_raw never dropped).
- `atlas_coords` ← `cell_key` promotion: **268/270** (2 honest-NULL: poe1-blood-magic-kit, d2-teleport-sorc lack cell_key).
- `eras_normalized`: **268/270** (V-16, above).
- **GX-02 census-tail 3 kits (V-6):** gd-berserker-wereforms (record) + la-ferality-wildsoul & la-phantom-beast-awakening-wildsoul (annex) get the SAME cheap census columns as their class via the riders. **Discipline (steward call):** the "V13 99.47%→100%" completion is a census-EXPRESSIBILITY metric (does the GX-02 shapeshift LAYER express these) — that is ENGINE-side (GX-02 docket-to-spec = separate gandalf lane; ESC-1 / `kit_architecture` enum is NOT conductor-ruled, NOT this lap, per V-17-c). So this rider writes NO shapeshift `architecture` value. The 3 kits are folded by being PRESENT + CLASSIFIED in the re-emission — exactly the "fold into the data pass" V-6 asks for. Rider 6 is documentation of the correct null-op (no SQL beyond Riders 1–5).

**Ships empty/NULL at apply (named downstream deps):**
- `normalization_rule` — EMPTY (V-13); rule population = battle-sim gamora/star-lord (ADR-004 when populated); `rdr_value` honest-NULL.
- `exact_json`/`exact_source_type` — NULL (G-FIND-1 / V-19); population = legolas Mode-B `.txt`/DBR datamine.
- `capstone_source_acquisition` — column lands, NULL at apply (per-kit prose read = W4 re-emission, not census-cheap).
- All 12 side-car tables except the 2 registry seeds (6 pilot doors + A-2 args; motion registry + A-3 fan_spread) — populated at W4 per-game tranches.

---

## 7. A-7 PRESERVE-NULL + A COUNT CORRECTION I FOUND IN VALIDATION

A-7 guarantees the door-strip rider does NOT coerce NULL `t4_doors` → `[]`/`""`. **There is NO door-strip UPDATE in the rider file** — the guarantee is that the NULLs stay NULL.

**Count correction (report-what-EXISTS law):** the pilot §7 listed "8 NULL-t4_doors" — those 8 are the **record-game subset** (all D2), which was the pilot's scope. The FULL live population of `t4_doors == JSON-null` (via `json_type='null'`) is **29**: 8 record-game + 21 annex-game (d3 9 · di 9 · d4 3). Separately, **16** rows carry an empty array `[]`. The pilot's characterization of the 8 record-game D2 kits (7 meaningful + 1 phantom `d2-wl-void-rift`) is UNCHANGED and correct; only the corpus-wide tally was under-counted in the pilot's §7 framing. **The A-7 apply assert is corrected to 29** (`json_type(mapping_json,'$.t4_doors')='null'` MUST equal 29, unchanged pre/post riders). This is exactly why the throwaway-validation step exists — it caught a count that would otherwise have shipped as an assert set to the wrong number.

---

## 8. THE APPLY SCRIPT (W3b) — sequence + safety (DO NOT RUN this wave)

`2026-07-22-vdm2-w3b-apply.sh` — bash-syntax-validated (`bash -n` clean), mode 644 (not executable; cannot run by accident). Sequence:

0. **preflight:** assert stamp == v1.1-verified AND md5 == `50df15b…`; abort if either drifted.
1. **BACKUP FIRST:** `corpus.db.pre-vdm2-schema-<date>-backup` + record md5 (the reversibility anchor).
2. `PRAGMA foreign_keys=ON` (loud FK failure on any typo'd kit_id).
3. additive DDL v1.
4. data riders + registry seeds.
5. **per-assert census checks** (RAISE→ABORT→ROLLBACK on any mismatch): corpus_class 267/299/19/0 · court 90/54/44/42/27/13 · original_element 270 · atlas_coords 268 · eras_normalized 268 · A-7 t4_doors-null 29 · iron-law 585/574/19.
6. **v2.0 stamp LAST** (only reached if every assert passed).
7. MIGRATION.md entry per ADR-004 (append the draft).
8. compendium regen from kit_master (smoke: kit_master assembles post-DDL).

Steps 3–6 run in **one transaction** — an assert failure rolls the whole thing back; nothing persists but the backup. New dockets take `status='open'` (distinct from the 19 matt-ratified).

---

## 9. VALIDATION EVIDENCE (throwaway copy only; live db untouched)

- DDL v1 applied clean on a throwaway copy of corpus.db: all **12 tables** created, all **9 columns** present, `DDL_EXIT=0`.
- Riders ran clean (`RIDERS_EXIT=0`): every census count EXACT (corpus_class 267/299/19/0 · court 90/54/44/42/27/13 · original_element 270 · atlas_coords 268 · eras_normalized 268).
- A-1 CHECK: `self`-range insert OK; `BOGUS` correctly rejected. A-4: `real` arg_type accepted. A-2: 6 doors + 3 trigger args seeded. A-3: `fan_spread` in motion registry.
- `PRAGMA foreign_key_check` empty (clean); `PRAGMA integrity_check` = ok.
- **Throwaway deleted; live corpus.db md5 = `50df15b776ad5b0da93fe90cdee1163d` (unchanged).** No stray copies.

---

## 10. WHAT I NEED FROM GATE-2 (and the two open routing items, non-blocking)

**For Gate-2 to rule on:** (a) the A-1/A-4 CHECK-safety claim (v1-NEW tables only, no rebuild, no VDM-1 touch); (b) the additive-only guarantee; (c) the census riders' correctness (throwaway-verified); (d) the backup-first + assert-then-stamp apply sequence; (e) the `pierce`/`bleed`→physical rider extension (accept, or send NULL).

**Two open routing items carried forward (neither blocks the apply):**
- **`accepted_downgrade` sign-off owner-identity** — pilot used `elrond (pilot)`; whether a design owner (Gandalf/Matt) co-signs is a W4 process question. The CHECK fires correctly regardless.
- **`normalization_rule` rule SEMANTICS** — ADR-004 cross-seam (battle-sim gamora/star-lord). The empty container ships now (elrond seam); rule population is the downstream dependency.

**Package ready for Gate-2.**

---

**Signed:** elrond (data steward) · Wave W3a assemble · corpus.db UNTOUCHED (md5 verified open+close) · DDL v1 + riders throwaway-validated (copy deleted) · local auto-commit, **NO push** (conductor centralizes).
