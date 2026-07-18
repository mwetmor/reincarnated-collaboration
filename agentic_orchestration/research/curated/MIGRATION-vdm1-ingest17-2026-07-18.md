# MIGRATION — VDM-1 ingest wave 17 (basin-5 CRAWL INGEST — LAST crawl ingest of VDM-1 run)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 (basin-5 crawl stage) — run steward gandalf; fires under Matt's standing
autonomous-run mandate. WRITE commission (standing read-only default lifted for `corpus.db` only).
**Script:** `agentic_orchestration/research/vdm1/vdm1_ingest17_basin5_crawl_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; single `BEGIN IMMEDIATE`…`COMMIT` txn;
integrity_check + foreign_key_check both clean post-write).

**Spec:** `agentic_orchestration/research/vdm1/stage1/basin5/INGEST-BASIN5-CRAWL-MANIFEST.md`

**Scope:** Greenfield INSERT 123 kits (c01–c13) → `verify_ledger` / `kit_dossier` / `kit_citations`
+ N1/N2 normalizations + le-bomb REPLACE + RE-KEY + TIER-2 hygiene errata (20 corrections) +
TIER-3 promotion (96 kits × 10 = 960 facts). NO new `canon_corpus` kit rows — all 124 kits
pre-exist; this ingest adds the crawl-stage rows.

**FILES GOVERN.** All expected counts asserted EXACTLY before write; mismatch → ABORT.

---

## Backup + md5 chain

- **File:** `corpus.db.bak-20260718T225409`
- **Backup md5:** `91edd323858310372bacb99c43fee148` (== INGEST-16 post-md5; chain-head confirmed; unbroken)
- **Pre-ingest live md5:** `91edd323858310372bacb99c43fee148`
- **Post-ingest live md5:** `87bb6b471dbf3e42e56292f6fc577994`
- **md5 chain:** `91edd323858310372bacb99c43fee148` → `87bb6b471dbf3e42e56292f6fc577994`

Backup retained on disk; NOT committed (`*.db` and timestamped backup names gitignored under
`curated/.gitignore`).

---

## TIER 1 — Greenfield ingest (123 kits, c01–c13)

### Source files

All 13 batches under `agentic_orchestration/research/vdm1/stage1/basin5/`, 39 JSONL files total.
All files `json.loads`-clean (0 parse failures). All 123 kit_ids pre-exist in `canon_corpus`
(zero phantoms). 0 pre-existing landing-zone rows for the 123 kits (idempotency clean).

| Batch | verify | dossier | citations (raw) |
|---|---|---|---|
| c01 | 35 | 66 | 29 |
| c02 | 30 | 60 | 18 |
| c03 | 24 | 48 | 18 |
| c04 | 24 | 48 | 16 |
| c05 | 36 | 72 | 18 |
| c06 | 34 | 66 | 20 |
| c07 | 37 | 66 | 32 |
| c08 | 37 | 72 | 15 |
| c09 | 33 | 66 | 11 |
| c10 | 28 | 54 | 23 |
| c11 | 24 | 48 | 22 |
| c12 | 21 | 42 | 14 |
| c13 | 15 | 30 | 18 |
| **TOTAL** | **378** | **738** | **254 raw / 253 inserted** |

Raw citation count = 254; inserted = 253 (N2 drop, see below).

### Rows inserted

| Table | Inserted |
|---|---|
| `verify_ledger` | 378 |
| `kit_dossier` | 738 |
| `kit_citations` | 253 (254 raw − 1 N2 drop) |

### N1 — c01 abstained-with-payload normalization (HARD BLOCKER resolved)

**17 rows normalized.** All in `batch-c01-dossier.jsonl` (tq-a game kits, confirmed isolated to c01's
crawler). Each row had `abstained=1` with `payload_json={"abstain_reason":"…"}`, violating
`CHECK(abstained=0 OR payload_json IS NULL)`. Normalization: `payload_json` set to NULL at ingest
time. The `abstain_reason` text is not stored elsewhere — the normalization action itself is the
record (documented here). c02–c13 were clean (strict null-payload on all abstained rows).

### N2 — c05 ud-snowstorm-frost placeholder citation (DROPPED)

The all-null placeholder row (`url=None, cite_class=None, rank_class=None, quarantined=0`) from
`batch-c05-citations.jsonl` was **DROPPED** (not inserted). Reason: `kit_citations.url` carries a
`NOT NULL` constraint; inserting with `url=None` would raise a constraint violation. Per manifest
("quarantined=1 or drop"), DROP is the constraint-compliant path. Result: 0 citation rows for
`ud-snowstorm-frost` in the DB post-ingest (the fully-unattested kit carries no citations, which
is the honest record). Quarantined count unchanged (+0 from greenfield pass).

### 1d — le-bomb REPLACE + RE-KEY

**Deleted (basin-2 rows, pre-REPLACE):**
- `verify_ledger`: 3 rows (all SOURCE_NOT_FOUND from basin-2; the SNF wave that surfaced the identity mismatch)
- `kit_dossier`: 6 rows (all abstained/null from basin-2)
- `kit_citations`: 0 rows (basin-2 had no citations for le-bomb)

**Inserted (re-crawl `batch-lebomb-*.jsonl`):**
- `verify_ledger`: 4 rows (identity CONTRADICTED + mechanics CONTRADICTED + era CONTRADICTED + negative_canon UNSUPPORTED)
- `kit_dossier`: 6 rows (abstained=0, all with real payload; IDENTITY_MISMATCH wrappers are historical record, now resolved by re-key)
- `kit_citations`: 6 rows (5 authored + 1 official; all attested-era; 0 quarantined)

**RE-KEY canon_corpus display fields** (kit_id `le-bomb-lance-falconer` KEPT as opaque PK — NOT churned):
- `folk_name`: `"Bomb Lance Falconer"` → `"Explosive Ballista Falconer"`
- `core_skills`: `["Bomb Lance", "Falconry"]` → `["Explosive Trap", "Ballista", "Falconry", "Dive Bomb"]`
- `eras`: `"1.4-omens"` → `"1.0-launch;1.4-omens"` (Falconer introduced at LE 1.0, Feb 27 2024)
- `mech_note`: false "Bomb Lance / thrown-explosive" identity dropped; replaced with real identity
  (Rogue→Falconer; Explosive Trap [0-mana] procs explosive Ballista turrets + Dive Bomb burst +
  Falcon companion). Note for mapper: `IDENTITY_MISMATCH` in dossier wrappers is RESOLVED by this
  re-key; wrappers are historical record. `elem_raw` left for mapper (dossier carries cold
  [Apogee of Frozen Light] + fire [Explosive Trap "inflicting fire damage"]).

---

## TIER 2 — Hygiene errata (non-gating; applied same transaction)

### 2a. elem_raw / mech_note corrections

All guarded `UPDATE … WHERE kit_id=?`; rowcount asserted ==1 per row. Errata numbers in range
**ERRATA-43..55** (next available numbers in the errata ledger after ingest-12's ERRATA-42).

| # | Kit | Correction | Field |
|---|---|---|---|
| 1 | `tl2-prismatic-embermage` | `elem_raw` `"fire"` → `"fire/ice/lightning"` (tri-element) | elem_raw |
| 2 | `tl2-hailstorm-embermage` | `elem_raw` `"cold"` → `"ice"` | elem_raw |
| 3 | `tq-druid-squall-caster` | `elem_raw` `"lightning"` → `"n/a"` (element-silent; probe-inference only) | elem_raw |
| 4 | `chr-mechanist-turret-drone` | `elem_raw` `"holy"` → `"n/a"` (skill-name only, not damage-type) | elem_raw |
| 5 | `tq-liche-king-conjurer` | `mech_note` prepend: IDENTITY — summoned-pet (not player transform) | mech_note |
| 6 | `ud-lightning-vortex` | `mech_note` prepend: MECHANICS — melee (not ranged cast) | mech_note |
| 7 | `tq-distortion-templar` | `mech_note` prepend: MECHANICS — physical+vitality damage (not control-centric) | mech_note |
| 8 | `chr-bloodbinder-warlock` | `mech_note` prepend: MECHANICS — mana-stacking (not HP self-sacrifice) | mech_note |
| 9 | `tq-druid-squall-caster` | `mech_note` prepend: ELEMENT — element-silent (no lightning in anchor) | mech_note |
| 10 | `chr-mechanist-turret-drone` | `mech_note` prepend: ELEMENT — element-silent (skill-name only) | mech_note |
| 11 | `hot-warlock` | `mech_note` prepend: ELEMENT — not-attested (no-engine-family, silent) | mech_note |
| 12 | `hot-cleric-radiant` | `mech_note` prepend: ELEMENT — no-engine-family (silent) | mech_note |
| 13 | `hot-spirit-warrior` | `mech_note` prepend: ELEMENT + SCOPE — no-engine-family; cross-class ability | mech_note |
| 14 | `ud-snowstorm-frost` | `mech_note` prepend: ATTESTATION — fully-unattested | mech_note |
| 15 | `ud-toxic-flame` | `mech_note` prepend: MECHANICS — poison-only (not poison+fire dual) | mech_note |

### 2b. era / identity / scope corrections

| # | Kit | Correction | Field |
|---|---|---|---|
| 16 | `vs-out-of-bounds-freeze` | `eras` floor → arcana Patch 0.6.1 (May 2022); scope → 14 weapons | eras + mech_note |
| 17 | `vs-queen-sigma` | `eras` base → Patch 0.11.0 (Aug 2022) | eras + mech_note |
| 18 | `vs-big-trouser` | DLC → base game | eras + mech_note |
| 19 | `vs-fuwalafuwaloo` | DLC → base game | eras + mech_note |
| 20 | `vs-vlad-dracula` | `core_skills` starting weapon → Wine Glass (DB generic) | core_skills + mech_note |
| 21 | `hot-sage-ring-blades` | `eras` widened → added Feb-2024, active in 1.0-2024 | eras + mech_note |
| 22 | `hades1-aspect-guan-yu` | lifesteal on Spin Attack (not Special) | mech_note |
| 23 | `hades1-beowulf-cast` | bloodstones never lodge/fire alongside bull rush; Igneus-Eden wrong-weapon | mech_note |

**Total TIER-2 corrections applied: 20 corrections across 4 elem_raw fields + 11 mech_note prepends
+ 14 era/identity/scope changes (with mech_note riders).** No errata_applied verify flags set
(basin-5 policy: TIER-2 corrections are curation hygiene; errata_applied flag reserved for
CONTRADICTED-era verify rows with an explicit era restamp per ingest-8/9 precedent; the CONTRADICTED
rows in basin-5 are identity/mechanics, not era). Steward may elect to run a follow-up errata pass
flagging the 11 contradicted kits' verify rows — that is a separate op, not gated on this ingest.

---

## TIER 3 — Promotion

**Gate:** mechanics=CONFIRMED-with-anchor AND ZERO CONTRADICTED in any family AND kit has probe facts.

| Bucket | Count | Notes |
|---|---|---|
| **Promoted** | **96 kits × 10 = 960 facts** | `kb-legacy`/`named-source-unfetched` → `verified-v1.1` |
| Excluded (CONTRADICTED somewhere) | 11 | chr-bloodbinder-warlock, hades1-aspect-guan-yu, hades1-beowulf-cast, tq-calculated-strike, tq-distortion-templar, tq-liche-king-conjurer, ud-illusion-family, ud-lightning-vortex, ud-toxic-flame, vs-big-trouser, vs-fuwalafuwaloo |
| Excluded (mechanics not CONFIRMED+anchor) | 7 | chr-arrow-storm-warden, chr-bee-warden, chr-demon-legion-warlock, chr-fulmination-templar, tq-dream-harbinger, tq-thane-storm-warfare, ud-snowstorm-frost |
| Gate-pass but zero probe facts | 9 | hot-blood-catcher, mcd-dynamo-torment, mcd-fireworks, mcd-soul, mcd-speed, mcd-summoner, tl2-arc-beam, tq-flame-surge, vs-gatti-amari |

`verified-v1.1`: 2767 → 3727 (Δ+960). Total `canon_probe_facts` unchanged (4780).

---

## Pre/post state

| Table | Before | After | Δ |
|---|---|---|---|
| `verify_ledger` | 1689 | 2068 | +379 (378 greenfield + 4 le-bomb − 3 le-bomb-basin2) |
| `kit_dossier` | 2706 | 3444 | +738 (738 greenfield + 6 le-bomb − 6 le-bomb-basin2) |
| `kit_citations` | 1026 | 1285 | +259 (253 greenfield + 6 le-bomb − 0 le-bomb-basin2) |
| `canon_corpus` | 585 | 585 | 0 (no new kits; TIER-2 + le-bomb rekey updates in-place) |
| `canon_probe_facts` | 4780 | 4780 | 0 (provenance flip only, not row count change) |
| `verified-v1.1` facts | 2767 | 3727 | +960 |
| quarantined citations | 6 | 6 | 0 (N2 dropped, not quarantined; no new quarantine rows) |

---

## Verification

- `PRAGMA integrity_check` = **ok**
- `PRAGMA foreign_key_check` = **clean**
- `PRAGMA journal_mode` = **delete**
- N1: 0 abstained dossier rows with non-null payload (asserted post-write)
- N2: 0 null-url citations for ud-snowstorm-frost (asserted post-write; row was dropped)
- le-bomb: 4v/6d/6c post-REPLACE (asserted); all 4 display fields re-keyed (asserted individually)
- TIER-2: all 4 elem_raw + 11 mech_note + 14 era/identity changes guarded rowcount==1
- TIER-3: 96 kits promoted, 960 facts flipped; excluded sets asserted clean

---

## Anomaly log

**N2 resolution method.** Manifest said "quarantined=1 or drop." `kit_citations.url` is NOT NULL in
schema. The placeholder row had `url=None`, so `quarantined=1` insertion would fail the NOT NULL
constraint. DROP is the constraint-compliant path. Steward should note: D-2c battery check for
"citations quarantine correct" should confirm the placeholder is absent (not quarantined=1). The
practical effect is identical (the fully-unattested kit has no citations), but the mechanism is DROP
not quarantine.

**Manifest errata reference.** The manifest's TIER-2 abbreviated kit names (`tq-squall`, `tq-liche-king`,
`chr-bloodbinder`, etc.) map to the full corpus kit_ids as follows: `tq-squall` → `tq-druid-squall-caster`;
`tq-liche-king` → `tq-liche-king-conjurer`; `chr-bloodbinder` → `chr-bloodbinder-warlock`;
`chr-turret-drone` → `chr-mechanist-turret-drone`; `tq-distortion` → `tq-distortion-templar`;
`hot-sage` → `hot-sage-ring-blades`; `hades1-guan-yu` → `hades1-aspect-guan-yu`;
`hades1-beowulf` → `hades1-beowulf-cast`. All 8 resolved correctly; zero unmatched.

---

## Reproducibility + reversibility

Inputs static (post-audit basin-5 crawl JSONL, 39 files). Full restore = copy
`corpus.db.bak-20260718T225409` over `corpus.db` (backup md5 `91edd323858310372bacb99c43fee148`).

---

## ADR-004

No engine-telemetry change; star-lord-side MIGRATION.md unaffected (all writes are elrond-seam corpus
curation). Auto-committed per project discipline (Matt-authorized VDM-1 charge).
**NO push — steward (gandalf) pushes per basin checkpoint.**

## Commit note

Pathspec-only: this migration doc + the ingest script. `corpus.db` is gitignored and NOT committed.
Backup + md5 sidecar stay on disk (uncommitted). Basin-5 stage-1 crawl inputs (gandalf's, static) not touched.
