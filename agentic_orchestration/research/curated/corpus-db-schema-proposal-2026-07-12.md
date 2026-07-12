# Canon-Corpus DB — schema proposal + staged-ingest plan (v1.0 PROPOSED)

**Author:** elrond · **Date:** 2026-07-12 · **Status:** PROPOSED / paper-work.
**Authority:** `agentic_orchestration/gandalf/views/corpus-rekey-spec-v1.md` §1–§3 — the §2 slot-by-slot fate table IS the schema authority.
**Gate:** schema + MIGRATION proposal are ungated (this doc). **DB ingest fires only after Matt's corpus-housing D-ruling + ADR-006 authorization.**

---

## 0. One-line intent

Represent the 563-row mobile ARPG canon corpus **under the engine coordinate frame as schema of record**: keep the 6-slot prefix as typed engine-lattice coordinates (1:1 with the engine lattice), demote the mobile-invented suffix to raw descriptors *awaiting-rekey*, and harden the measured-vs-projected law into the schema — corpus rows can **never** carry measured values.

Deliverables of this proposal:
- `scripts/catalogue_migrations/corpus_v1_0_canon_corpus.sql` — the DDL (not executed).
- `scripts/corpus_ingest_dryrun_2026_07_12.py` — READ-ONLY dry-run + row-level validator (writes nothing; run below).
- MIGRATION.md v1.13 entry (PROPOSED, ingest-gated).
- §4 open-questions for Matt / KR.

---

## 1. Source & the lossy-projection reality (curation-critical)

**Substrate of record:** `claude-mobile-session-docs/ARPG-canonical-kit-research/final-docs-v3/rdr-kit-atlas-v3.csv` (563 rows).

The v3 CSV is a **lossy projection** of the harvest's source `.jsonl`. Two facts drive the whole schema design and one open question:

1. **Prefix values live only inside `atlas_key`.** The CSV carries raw columns for `proxy`, `commit`, `mob`, `geo`, `econ`, `elem_p` — but **not** for `attr`/`range`/`tempo`/`amp`, and **not** the raw source strings for `ctrl`/`def`. Those survive only as single-character *codes* positional inside `atlas_key` (e.g. `DRHFSI-HMDD-SP-PH-~~`). The ingest therefore **decodes the prefix from `atlas_key`** (positions 0–5 → attr/range/tempo/amp/proxy/commit; the generator's `code_*` maps invert cleanly). `ctrl_raw`/`def_raw` are recoverable only as coarse code-tokens → flagged `ctrl_def_from_code=1` so re-key never mistakes them for source truth.

2. **Per-slot confidence is collapsed.** The CSV has a single `avg_conf` = mean of *proxy/geo/commit* confidence only. True per-axis `{v, c}` survives **only** in `rdr-roster-kits.jsonl** (the 48 roster/bench rows). For the 515 canon rows the source `canon-corpus-*.jsonl` files (were at `/mnt/user-data/outputs/`) are **not present in this tree.** → **Open Q1.** The schema holds `{value, confidence}` per prefix slot regardless; canon rows ingest with `prefix_conf_provenance='avg-collapsed'` until/unless the jsonl are recovered.

3. **`game` ≠ `corpus`.** Game-of-record is the CSV `game` column. `corpus` is the harvest *bucket* — bucket `hades` splits to games `hades1`/`hades2`; bucket `tl` splits to `tl1`/`tl2`/`tli`. The dry-run flagged 13 rows where using `corpus` as game would corrupt identity; the schema stores `game` as identity and keeps `corpus_bucket` as harvest provenance.

**Nothing real is lost** (spec §1): the prefix is the engine lattice 1:1 — that is exactly why V4/V4-r2 joins worked. The suffix was mobile-invented vocabulary that never passed a design gate; demoting it to raw *awaiting-rekey* is the whole point of the re-key.

---

## 2. Schema shape (per the §2 fate table)

Full DDL: `scripts/catalogue_migrations/corpus_v1_0_canon_corpus.sql`. Summary:

| Fate-table slot(s) | Schema realization |
|---|---|
| **PREFIX** attr·range·tempo·amp·proxy·commit (KEEP — typed lattice) | six `<slot>_val` enum columns + six `<slot>_conf` reals + `lattice_coord` (6-char prefix = engine coord 1:1) + `prefix_conf_provenance` flag. Commit enum **of record `instant`/`wind-up`/`channel`**. |
| **SUFFIX** mob·geo·ctrl·def·econ·elem (RETIRE→raw) | six `*_raw` columns + `suffix_rekey_status='awaiting-rekey'`. **No mappings invented.** |
| **ADD** engine-native | `motion_frame`, `t4_doors`, `option_c_substrate_flags`, `commit_provenance` — NULL at ingest, authored at re-key time. |
| **measured semantics** RETIRED | **No measured column exists on `canon_corpus`.** Schema law: measured = gauntlet fingerprints only, separate engine-side store. |
| Identity | `kit_id` (PK), `folk_name`, `game`, `tier`+`tier_confirm_pending`, `canon_tier`, `eras`, `negative`, `lineage`, `gx`, `source`, `roster_provenance_only`, `is_system`, `unresolved`, `atlas_key_orig` (verbatim), `key_completeness`, `corpus_bucket`, `provenance_tag='mobile-harvest-v3'`, `source_date`. |

**The join-without-rewrite discipline (spec §2 requirement).** The six re-key mapping tables (`rekey_geo/ctrl/mob/def/econ/elem`) are created **empty** at v1.0, keyed on the raw descriptor. When a design session supplies a mapping table, it populates `rekey_<slot>(raw, engine_value, confidence, session_ref, note)` — and every corpus row carrying that raw value lights up **through the `v_canon_corpus_rekeyed` LEFT-JOIN view**, with **zero UPDATEs to `canon_corpus`**. Rows are never rewritten; the engine value is derived at read time. Raw is always preserved (reversibility discipline).

**HoT ruling (spec §2):** Halls of Torment is its own game — `game='hot'` (19 rows). Tier lean **T3** (gandalf lean) written with `tier_confirm_pending=1` → flag for Matt confirm at ingest.

---

## 3. Staged ingest plan (dry-run counts · validation · rollback)

### 3a. Dry-run counts (from `corpus_ingest_dryrun_2026_07_12.py`, READ-ONLY — verified)

```
TOTAL ROWS: 563   |   unique kit_id: 563/563   |   0 ERROR  0 WARN
source class:   515 canon · 35 roster · 13 bench
staged routing buckets:
   496  canon substrate      (source='canon', is_system=0, unresolved=0)  → v_corpus_substrate
    48  roster/bench         (roster_provenance_only=1)   — Matt throw-out: lineage-only
    18  SYS-annex            (is_system=1)                — evidence records, not kits
     1  canon UNRESOLVED     (unresolved=1, key_completeness<4)
games-of-record: 20 distinct (poe1 91 · d2 58 · d3 46 · d4 45 · gd 41 · poe2 38 · le 35 …
                 hot 19 · hades1 8 · hades2 5 · tl1 2 · tl2 11 · tli 9 · tq2 5 …)
HoT: 19 rows (tier lean T3, tier_confirm_pending=1)
```

### 3b. Row-level validation (enforced by the dry-run; all currently PASS)

1. `kit_id` uniqueness — PK integrity. **563/563 unique, 0 collisions.**
2. Prefix decode vs raw-column cross-check — `proxy`/`commit` decoded from `atlas_key` must agree with the CSV raw columns. **0 mismatches.**
3. `game` ∈ known-games whitelist (20 games). **0 unknown** (after `game`-not-`corpus` correction).
4. `avg_conf` numeric ∈ [0,1]. **0 violations.**
5. `negative` ∈ {True,False}. **0 violations.**
6. Enum-domain CHECKs on the six prefix `_val` columns are enforced at DDL layer (SQLite CHECK constraints).

### 3c. Staged execution order (when authorized)

1. Create `corpus.db` (or Matt-chosen housing) from `corpus_v1_0_canon_corpus.sql` — tables + empty rekey_* + views + `corpus_schema_meta` 1.0 row.
2. Ingest **canon** rows (515) first → the substrate. Confirm `v_corpus_substrate` = 496.
3. Ingest **roster/bench** (48) with `roster_provenance_only=1` (**pending Open Q3** — in-or-out).
4. Set `is_system=1` on the 18 SYS-annex rows; `unresolved=1` on the 1 sub-threshold row.
5. Post-ingest asserts: row count = 563 (or 515 if Q3=skip); `v_corpus_substrate`=496; HoT tier_confirm_pending count = 19; every `suffix_rekey_status='awaiting-rekey'`.

### 3d. Reversibility / rollback (source-anchored discipline)

- `corpus.db` will be **gitignored** (`curated/.gitignore` already ignores `*.db`); the committed source-of-truth is the **DDL + ingest script + this doc**. A clean rebuild from the v3 CSV lands at the identical curated state — the curation is reproducible, not a one-off mutation.
- Before any post-v1.0 mutation: `cp corpus.db corpus.db.pre-<change>-backup` per the established catalogue convention.
- Rollback of a bad ingest = `DROP` + re-run the deterministic script. No data is authored in-DB at v1.0 that isn't reproducible from the CSV (the ADD columns are NULL until re-key sessions, which will themselves be script-anchored).

---

## 4. Open questions (Matt / KR)

| # | Question | elrond recommendation | Blocks |
|---|---|---|---|
| **Q1** | **Confidence provenance.** Canon rows lack per-slot `{v,c}` and raw attr/range/tempo/amp — the v3 CSV gives only `atlas_key` codes + collapsed `avg_conf`. Are the `canon-corpus-*.jsonl` harvest sources retained anywhere (they were under `/mnt/user-data/outputs/`)? | Recover the jsonl → ingest true per-slot confidence + raw prefix values (`prefix_conf_provenance='per-slot'`). If unrecoverable, ingest with `avg-collapsed` and accept the degraded confidence honestly. | full-fidelity prefix confidence (not ingest itself) |
| **Q2** | **Housing D-ruling.** Where does the corpus live? | NEW store `curated/corpus.db` (distinct domain from art-asset `catalogue.db`). Alternative: namespaced table-set in an existing curated DB. DDL is housing-agnostic. | ingest start |
| **Q3** | **Roster-provenance rows in-or-out.** 35 roster + 13 bench (mobile encoding retired to provenance per Matt throw-out). | **Ingest flagged `roster_provenance_only=1`** (lineage preserved, filtered out of `v_corpus_substrate`) rather than skip — cheap, reversible, keeps the V4-r2 lineage trail queryable. | roster/bench ingest only |
| **Q4** | **HoT tier confirm.** gandalf lean T3 for all 19 HoT rows. | Ingest `tier='T3', tier_confirm_pending=1`; Matt confirms/adjusts, then clear the flag. | tier finalization |
| **Q5** | **SYS-annex (18) + UNRESOLVED (1).** System/mechanic evidence records and one sub-threshold-key row. | Ingest flagged (`is_system=1` / `unresolved=1`), excluded from substrate view; keeps the evidence trail without polluting the kit substrate. | none (recommendation stands) |

---

## 5. What this proposal does NOT do

- Does not invent any suffix→engine mapping (that is the six design sessions' job; spec §2/§5).
- Does not author any ADD-column values (motion_frame etc. come at re-key time).
- Does not write any DB (ingest is gated). The dry-run script is strictly read-only.
- Does not touch engine telemetry / measured axes (boundary with star-lord; measured law hardened by *omission*).

**Signed:** elrond, 2026-07-12.
