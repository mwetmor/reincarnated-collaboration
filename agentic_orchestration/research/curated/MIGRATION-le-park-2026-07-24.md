# MIGRATION — Last Epoch PARK-not-DELETE (active-roster flag, additive)

**Author:** elrond (data steward) | **Date:** 2026-07-24 | **DB:** `agentic_orchestration/research/curated/corpus.db`
**Class:** ADDITIVE + non-destructive UPDATE. Three new columns on `canon_corpus`; 37 rows re-flagged; ZERO deletions.
**Backup taken:** `corpus.db.pre-le-park-20260724T041034-backup` (+ `.md5.txt` = `4c96057bafb2eb99196b01b68b34d6bf`), pre-DDL, elrond backup discipline (Discipline #8/#11).
**Migration script (durable, committed, rebuild-guaranteeing):** `agentic_orchestration/research/scripts/corpus_le_park_2026_07_24.py`
**Schema-meta version:** `le-park-2026-07-24`

---

## Ruling lineage

**Matt 2026-07-24 — TSR-7 fork (ii).** Source of record: gandalf true-sources grill brief
`agentic_orchestration/gandalf/notes/2026-07-23-true-sources-grill-brief.md` §4 (rulings ledger, **TSR-7** row).

TSR-7 was HELD-FOR-VERIFICATION: an earlier park commission was TaskStopped CLEAN before execution (Matt wanted
"one last research… personally, before removing"). That research returned; Matt then ruled fork (ii). This note
records the **ruling-confirmed execution** of the park.

## The tightened roster rule (verbatim, final text)

> **"active-roster membership requires banked anchors OR a LANDED/agent-executable raw lane."**

This is a **disjunction**: one satisfied branch is sufficient for active-roster membership. That property is
load-bearing — it is exactly why the LE park does **not** cascade to PoE2 (see below).

---

## Why LE fails — both disjuncts

**Disjunct (1): banked anchors — FAIL.** LE holds **0** `kit_numeric` rows and **0** `kit_composition` rows.
No deep anchor kit exists for LE. (Re-verified as a pre-write sanity gate; see below.)

**Disjunct (2): a LANDED / agent-executable raw lane — FAIL.** Nothing landed. The lane exists *in-class* but is
stale or inaccessible:

| Candidate lane | Status | Verdict |
|---|---|---|
| `prowner/last-epoch-data` (`skillTrees.ts`, 5,102,196 B) | Pushed **2024-03-19**, LE-1.0 era — STALE | Proves data class is extractable; not current, not landed |
| `aianlinb/LELocalePatch` | FRESH (pushed **2026-03-27**) | Tooling ecosystem alive; a locale patcher, not a data drop |
| lastepochtools.com (Dammitt, 2019–2026) | Live + maintained but **bot-gated (403** to WebFetch and browser-UA curl) | Not agent-fetchable |
| Official EHG Game Data API | **"not yet available"** | No lane |
| Unity il2cpp extraction | Highest-cost fallback; not executed | Not landed |

LE is the roster's **verification orphan** (TSF-4 language): no deep-anchor kit AND no raw lane. It fails both
branches of the disjunction, so it fails the tightened rule.

## Why PoE2 passes — the precedent does NOT cascade

PoE2 satisfies **disjunct (1) on banked anchors alone: 105 `kit_numeric` rows.** Because the rule is a
disjunction, a single satisfied branch is sufficient — PoE2 needs no raw-lane assessment to stay active. PoE2
remains **ACTIVE** and untouched (verified: PoE2 `kit_numeric` still 105 post-migration). The LE park is
LE-specific; no other roster game is affected.

## Reactivation trigger (stays live)

**A fresh LE datamine drop LANDING** (agent-executable, current-patch) = LE re-passes disjunct (2) and returns
to the active roster. Because this is a **PARK-not-DELETE** (all 37 rows retained), reactivation is a flag flip,
not a re-ingest:

```
UPDATE canon_corpus
   SET roster_status='active',
       roster_status_note='REACTIVATED <date>: <landed lane cite>',
       roster_status_date='<date>'
 WHERE game='le';
-- then restore the active record-bucket denominator 233 -> 270 in the coverage matrix.
```

---

## Mechanism — why PARK not DELETE, and the schema choice

**Curated rows are capital, and the transformation is reversible.** Deletion would discard 37 curated kits'
prose, lattice coordinates, tier assignments, citations, and provenance — all of which cost real curation
effort and remain valid the moment a raw lane lands. Park keeps that capital intact behind a flag.

**Flag mechanism chosen: an explicit `roster_status` column (tagged, not encoded).** Per elrond
tagged-not-encoded law (Discipline #14 spirit): park state is a first-class status column, **not** packed into
`kit_id`, the `game` code, or a compound flag. Every parked row still traces to its origin (`source`,
`source_date`, `provenance_tag` all preserved and untouched). This makes the park self-documenting, queryable,
and trivially reversible.

### Additive DDL on `canon_corpus`

| Column | Type / constraint | Meaning |
|---|---|---|
| `roster_status` | `TEXT CHECK IN ('active','parked') NOT NULL DEFAULT 'active'` | Active-roster membership flag |
| `roster_status_note` | `TEXT` | Park lineage + reactivation note (NULL for active rows) |
| `roster_status_date` | `TEXT` | Date the status was last set |

The `DEFAULT 'active'` means all pre-existing 553 non-LE rows became `active` automatically; only the 37 LE
rows were then flipped to `parked`. No existing column's shape changed.

### The UPDATE

`UPDATE canon_corpus SET roster_status='parked', roster_status_note=<lineage>, roster_status_date='2026-07-24'
WHERE game='le'` → **37 rows** flagged. Zero deletions. `kit_numeric` / `kit_composition` untouched (LE has none
anyway — the sanity gate below is a hard assertion in the script, not a comment).

---

## Denominator sync: active record-bucket 270 → 233

The **270** is the **record-BUCKET** = the five active-roster games (poe1 94 · d2 60 · gd 41 · poe2 38 · le 37).
This is the denominator the coverage matrix in the master `MIGRATION.md` uses (its court / element / atlas-coord
rows: "257/270", "270/270", "268/270", etc.). It is distinct from `corpus_class='record'` CLASS = 267 (three
system-records — `le-low-life-ward`, `poe2-grim-feast`, `poe2-temporalis-blink` — sit in the record games but
carry `corpus_class='system'`).

Parking all 37 LE bucket-members (33 record + 3 negative-record + 1 system: `le-low-life-ward`) removes the LE
contribution wholesale: **270 − 37 = 233.** The new active record-bucket is **poe1 94 · d2 60 · gd 41 · poe2 38
= 233**, verified post-migration via
`SELECT COUNT(*) FROM canon_corpus WHERE game IN ('poe1','d2','gd','le','poe2') AND roster_status='active'`.

Where the denominator lives in curation surfaces: it is prose in the master `MIGRATION.md` coverage-matrix
section, not a stored count. `roster_atlas` holds **0** LE rows (checked), so no stored roster-count surface
needed syncing there. The VDM-2 export `vdm2-exports/vdm2-w4-le-2026-07-22.json` is a reversible provenance
artifact and is **left intact** per park-not-delete (it records what was curated; it is not an active-roster
count). Going forward, coverage-matrix statements should read against `roster_status='active'` (denominator
**233**) unless explicitly reporting the full historical bucket (270, LE-inclusive).

---

## Sanity gate (pre-write, hard assertions in the script)

```
LE kits            = 37    (expected 37)   PASS
LE kit_numeric     = 0     (expected 0)    PASS   -> park touches no exact-number data
LE kit_composition = 0     (expected 0)    PASS   -> park touches no composition data
PoE2 kit_numeric   = 105   (expected 105)  PASS   -> PoE2 anchors intact; no cascade
record-bucket before = 270 / after = 233                PASS
```

## Post-apply verification (on the live DB)

```
canon_corpus total rows      : 590   (unchanged — zero deletions)
roster_status='parked'       : 37    (all LE; 0 non-LE parked)
roster_status='active'       : 553   (0 LE active)
LE rows still present         : 37    (retained, reversible)
active record-bucket (denom)  : 233
PoE2 kit_numeric              : 105   (untouched)
foreign_key_check             : clean
integrity_check               : ok
```

---

## Reversibility

Three routes, in ascending cost:
1. **Reactivate (intended path):** flag flip per the SQL above — all data is present.
2. **Restore from backup:** `corpus.db.pre-le-park-20260724T041034-backup` (md5 `4c96057bafb2eb99196b01b68b34d6bf`).
3. **Rebuild:** re-run `scripts/corpus_le_park_2026_07_24.py` (idempotent) against a pre-park DB.

## Boundary note

This is a change to elrond's own data layer (`corpus.db`) only. No engine telemetry schema, no engine source,
no ADR-004 cross-seam request. KR verifies and pushes; elrond commits (DB file is gitignored — the committed
artifacts are this note, the migration script, and the schema_meta record inside the regenerable DB).
