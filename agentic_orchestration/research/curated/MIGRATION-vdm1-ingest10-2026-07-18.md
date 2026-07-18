# MIGRATION — VDM-1 ingest wave 10 (basin-1 mapping 48 + REVIEW-3 un-quarantine + CONFIRMED-only promotions)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 (basin-1 close-out)
**Script:** `agentic_orchestration/research/scripts/vdm1_ingest10_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; never flipped to WAL; single short `BEGIN IMMEDIATE`
txn; basin-2 crawl agents ran concurrently READ-ONLY and were unaffected;
integrity_check + foreign_key_check both clean post-write)

**Scope — three dispatch items:** (1) ingest 48 basin-1 `kit_mapping` rows from the four
POST-AUDIT stage-2 files; (2) REVIEW-3 steward un-quarantine flip on the mobalytics/jungroan
temporalis-blink citation; (3) basin-1 probe-fact promotions, CONFIRMED-only per the steward
basin-close-out ruling. No stage-1 landing-zone rows this wave (verify/dossier/citations
counts unchanged).

---

## Backup

- **File:** `corpus.db.pre-vdm1-ingest10-20260718T045618`
- **pre-ingest live md5:** `c8dbd4898d0aa8878648c47ef95cc7dd` (== ingest-9 post-md5; unbroken
  chain, no interim writes between waves)
- **backup file md5:** `736993857cecc72a2ebc18cb3d61d036` (`.backup` re-pages the file so its
  md5 differs from live; content identical — integrity_check=ok, journal_mode=delete on backup)
- **post-ingest live md5:** `862229859306d5ccce487bee2a7c8e9b`
- md5 sidecar: `corpus.db.pre-vdm1-ingest10-20260718T045618.md5.txt`

Backup retained on disk for reversibility; deliberately NOT committed (a backup belongs on
disk). `corpus.db` is gitignored (`*.db`) and is not committed by any ingest (unbroken
precedent). A stale `corpus.db-shm` (from 01:44, pre-existing, no `-wal`) was left untouched
per the ingest-4 dispatch law — deleting -shm/-wal previously broke concurrent readonly crawlers;
harmless in DELETE mode.

---

## Item 1 — basin-1 `kit_mapping` ingest (48 rows; UPSERT idempotent)

Inputs (committed, static; HEAD carries the steward corrections applied in-place at
`bb5da3d7` / `38c4c5ab` / `0c7cc340` — the files on disk ARE the post-audit truth):

| File | Rows |
|---|---|
| `.../vdm1/stage2/basin1/mapping-batch-01.jsonl` | 12 |
| `.../vdm1/stage2/basin1/mapping-batch-02.jsonl` | 12 |
| `.../vdm1/stage2/basin1/mapping-batch-03.jsonl` | 12 |
| `.../vdm1/stage2/basin1/mapping-batch-04.jsonl` | 12 |

All 48 parsed clean (`json.loads` per line, 0 failures); `mapping_json` is a nested object
(serialized via `json.dumps(..., ensure_ascii=False)`); 48 distinct kit_ids (0 in-file dupes);
all 48 present in `canon_corpus` (FK guard passed).

**INSERT vs REPLACE:** **48 INSERTED / 0 REPLACED.** Zero of the 48 basin-1 kits carried a
pre-existing `kit_mapping` row (the PoE1 ingest at wave-4 populated only the 94 PoE1 kits; no
pre-audit basin-1 mapping ingest ever ran). The write uses `INSERT … ON CONFLICT(kit_id) DO
UPDATE` (post-audit state would win on conflict), but no conflict fired.

**Load-time asserts (all pass — dispatch file truths):**

| Assert | Result |
|---|---|
| row count == 48 | ✓ |
| grade histogram EXACT / CLOSE / APPROX / GAPPED | **0 / 34 / 14 / 0** ✓ (== dispatch expected) |
| terminal histogram | **MAPPED 48** ✓ (0 MAPPED_DOCKET) |
| 48 distinct kit_ids, all in canon_corpus | 48/48 ✓ |
| `mapping_provenance` | `authored-vdm1` on all 48 ✓ |

`kit_mapping` count: **94 → 142** (94 PoE1 + 48 basin-1).

---

## Item 2 — REVIEW-3 un-quarantine flip (steward ruling 2026-07-18)

The ingest-9 MIGRATION (§ REVIEW-3) flagged the conflict: `kit_citations` id=369
(`mobalytics.gg/.../blink-autobomber-jungroan`, kit `poe2-temporalis-blink`, `cite_class=authored`,
author `jungroan`) was `quarantined=1` yet was the crawler's anchor for temporalis-blink's
identity-CONFIRMED verify row. The steward ruled the flag **ERRONEOUS**: the crawler conflated
the DEAD-domain 403-probe with the junk-quarantine class; mobalytics/jungroan is
**authored-class evidence**, not junk-tail.

- **Write:** guarded `UPDATE kit_citations SET quarantined=0 WHERE id=369 AND quarantined=1`
  → rowcount==1. **id=369 quarantined 1 → 0.**
- **KEPT quarantined:** id=375 (`poe2-walking-calamity`, `mmoexp.com`) — genuine junk-tail,
  precondition-asserted still `quarantined=1` post-write. **Not touched.**
- **Total quarantined citations: 2 → 1** (only the mmoexp junk-tail remains).

**Provenance note (no annotation column):** `kit_citations` has no free-text annotation
column, so the steward ruling is recorded HERE (and in the errata ledger, ANNOT surface) rather
than on the row. The ruling: *"REVIEW-3 (2026-07-18, steward): id=369 mobalytics/jungroan
un-quarantined — crawler conflated DEAD-domain 403-probe with junk-quarantine class; the citation
is cite_class=authored (named author jungroan) and is the identity-CONFIRMED anchor for
poe2-temporalis-blink. Flag was the error, not the anchor usage."* This resolves the ingest-9
"quarantined row surfacing as a verify source" conflict in favor of the anchor (the flag was
wrong); the walking-calamity mmoexp contrast (correctly backs NO verify/dossier row) stands as
the clean junk case.

---

## Item 3 — basin-1 probe-fact promotions (CONFIRMED-only; whole-kit block)

**Steward ruling (basin close-out):** promote ONLY claim families whose verify verdict is
CONFIRMED-with-anchor; NO blanket promotion. Named exclusions: **era-family promotions excluded
for the era-contradicted kits** (their restamps carry errata); **identity/mechanics promotions
excluded for the ERRATA-19..23 carriers** (corrected via errata — errata state is authoritative).
Rationale on record: basin-1's 5-era / 4-mechanics / 2-identity contradiction split undermines
the kb-reliability presumption the PoE1 gate rested on, AND the m04 mapping audit found probe
facts being cited as if attestation — promotions must not launder kb rows into verified-looking
state.

### The NARROWER-THING resolution (dispatch: "if partial promotion cannot be expressed cleanly, do the narrower thing and report what you excluded")

`canon_probe_facts` carries **10 CONTENT families** (delivery, footprint, element, control,
defense, economy, movement, geo_text, rank1_upgrade, sources_used). `verify_ledger` carries
**4 VERIFICATION claim-families** (identity, mechanics, era, negative_canon). **The probe
families do NOT partition into era-vs-identity-vs-mechanics buckets** — there is no "era probe
family" to hold back while promoting the rest. A per-family partial promotion on a contradicted
kit therefore cannot be expressed cleanly WITHOUT flipping content facts that sit under a
contradicted verification axis into verified-looking state — exactly the m04 laundering the
ruling forbids.

So the machinery did the **narrower thing**: it applies the PoE1 ingest-4 gate at **whole-kit
granularity** —

> flip a kit's 10 probe facts → `verified-v1.1` **iff** the kit has **mechanics=CONFIRMED
> (with anchor)** AND **ZERO CONTRADICTED verdict in ANY family**.

Because the gate excludes *any* kit with *any* contradiction, **all 9 contradicted kits are
excluded whole** — which strictly and automatically honors BOTH named exclusion rules (the 4
era-contra kits AND the 4 ERRATA-19..23 carriers), and additionally excludes hades2-omega-magick
(mechanics-CONTRADICTED, ERRATA-adjacent movement correction). Nothing is excluded *beyond* what
the gate requires, and nothing under a contradicted axis is laundered.

### Result

- **Promoted: 32 kits × 10 facts = 320 facts** flipped `kb-legacy`/`named-source-unfetched` →
  `verified-v1.1`. (Of the 320: 280 were kb-legacy, 40 named-source-unfetched pre-flip; 0 were
  already verified-v1.1; 0 were fetched-vdm1 — no overwrite of fresher provenance.)
- **`verified-v1.1`: 720 → 1040** (Δ+320). `kb-legacy` 2030 → 1750 (−280);
  `named-source-unfetched` 2030 → 1990 (−40). −280 + −40 = −320 = exactly the 320 promoted. ✓

### Excluded — with reasons

**(a) CONTRADICTED somewhere — 9 kits (the ruling's core exclusion):**

| kit_id | contra family | errata |
|---|---|---|
| `poe2-acolyte-darkness` | era | ERRATA-16 (probe kit) |
| `poe2-concoction` | era | ERRATA-17 (zero-probe — moot) |
| `poe2-grim-feast` | era (×2 rows) | ERRATA-18 (probe kit) |
| `poe2-warbringer-totems` | era | ERRATA-20 (probe kit) |
| `poe2-walking-calamity` | identity + mechanics | ERRATA-19 (probe kit) |
| `tq2-whirlwind-rogue` | identity | ERRATA-21 (probe kit) |
| `tq2-elementalist` | mechanics | ERRATA-22 (probe kit) |
| `tq2-stormblade-ice-shards` | mechanics | ERRATA-23 (probe kit) |
| `hades2-omega-magick` | mechanics | (movement/mechanics correction, ingest-9 adj-4) |

The "5-era / 4-mechanics / 2-identity" split named in the ruling = **CONTRADICTED-row** counts:
5 era rows (grim-feast carries 2) + 4 mechanics rows + 2 identity rows, across these 9 kits
(walking-calamity is counted in both the identity and mechanics tallies).

**(b) CLEAN but mechanics NOT CONFIRMED — 4 kits** (excluded by the PoE1 gate, the wormblaster
precedent — mechanics verdict is UNSUPPORTED, honest silence ≠ attestation):
`poe2-archmage-totems`, `poe2-demon-form`, `poe2-erasure-edc-lich`, `poe2-titan-hotg`.

**(c) CLEAN + mechanics-CONFIRMED but ZERO probe facts — 3 kits** (0 rows to flip; correct,
not a miss): `poe2-chronomancer-01`, `poe2-perfect-strike-01`, `poe2-wall-of-shields`.

32 promoted + 9 (a) + 4 (b) + 3 (c) = **48** ✓.

**Note vs ingest-9's estimate:** ingest-9's MIGRATION flagged a rough "17 clean probe-fact-bearing
b03/b04 kits × 10 = 170" if a sweep were commissioned. This wave promotes the full basin (all
4 batches, not just b03/b04) under a stricter *per-family-verified* gate: 32 kits / 320 facts.
The ingest-9 figure was a b03/b04-only back-of-envelope; this is the audited whole-basin count.

---

## Verification (post-write, `sqlite3 -readonly` + independent Python)

- `PRAGMA integrity_check` = **ok**; `PRAGMA foreign_key_check` = **clean** (no rows);
  `PRAGMA journal_mode` = **delete**.
- `kit_mapping` basin-1 subset queried by exact 48-kit list: 48 rows, 34 CLOSE / 14 APPROX,
  all MAPPED, all `authored-vdm1`; 0 missing, 0 extra. `mapping_json` round-trips as valid JSON.
- id=369 quarantined=0; id=375 quarantined=1; total quarantined=1.
- verified-v1.1 = 1040; provenance arithmetic balances (−320). Spot-checks: promoted
  `poe2-bonestorm` → all verified-v1.1; excluded `poe2-grim-feast` (era-contra) + `tq2-whirlwind-rogue`
  (ERRATA-21) → still kb-legacy.

Table counts (this wave writes NO stage-1 rows):

| Table | Before | After | Δ |
|---|---|---|---|
| `verify_ledger` | 519 | 519 | 0 |
| `kit_dossier` | 852 | 852 | 0 |
| `kit_citations` | 411 | 411 | 0 (1 row's `quarantined` flipped) |
| `kit_mapping` | 94 | 142 | +48 |
| — quarantined citations | 2 | 1 | −1 |
| — `verified-v1.1` probe facts | 720 | 1040 | +320 |

---

## Reproducibility + reversibility

Inputs committed and static; the script is deterministic and re-runnable. The mapping write is
an idempotent UPSERT (re-run overwrites basin-1 rows with identical values); the REVIEW-3 flip
is `WHERE id=369 AND quarantined=1` (a re-run finds quarantined already 0 → rowcount 0, so the
in-script `rowcount==1` guard means a naked re-run would raise on item 2 — by design, signalling
"already applied"); the promotion is idempotent (`WHERE fact_provenance IN (kb-legacy,
named-source-unfetched)` skips already-verified rows). Full restore =
`corpus.db.pre-vdm1-ingest10-20260718T045618` over `corpus.db`
(md5 `736993857cecc72a2ebc18cb3d61d036`).

## ADR-004

No engine-telemetry change; star-lord-side MIGRATION.md unaffected (all writes are
elrond-seam corpus curation: `kit_mapping` + one `kit_citations.quarantined` flag +
`canon_probe_facts.fact_provenance`). Auto-committed per project discipline (Matt-authorized
VDM-1 charge). **NO push — steward (gandalf) pushes per basin checkpoint (R-9).**

## Commit note

Pathspec-only (matches ingest-1..9 precedent): this migration doc + the ingest script only.
`corpus.db` is gitignored/untracked (NOT committed); backups + md5 sidecar stay on disk
(uncommitted); basin-2 stage-2 crawl output (concurrent, not elrond's) is NOT touched.
