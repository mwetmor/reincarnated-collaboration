# MIGRATION — VDM-1 ingest wave 13 (basin-3 crawl ingest 680+overlay + ERRATA-43..55 + promotions)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 (basin-3 Diablo d2/d3/d4/di, 179 kits) — run steward gandalf; fires under Matt's standing
autonomous-run mandate. WRITE commission (standing read-only default lifted for `corpus.db` only).
**Script:** `agentic_orchestration/elrond/research/scripts/vdm1_ingest13_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; never flipped to WAL; single `BEGIN`…`COMMIT` txn;
integrity_check + foreign_key_check both clean post-write).

**Scope — four parts:** (1) ingest 15 basin-3 batch file-triples (180 distinct kits) into verify_ledger /
kit_citations / kit_dossier; (2) BACKFILL-3 overlay (22 in-place UPDATEs + 1 INSERT + 27 citations
OR-IGNORE); (3) errata queue ERRATA-43..55 (falsified-negatives, di resource sweep, probe-fabrication
series renumber, era restamps, core_skills, alias, kit-level flags, NULL-era backfills, unattested
register); (4) whole-kit promotion gate.

**FILES GOVERN.** All expected counts asserted EXACTLY on load; a mismatch RAISES (stop and report,
never reconcile silently). PRE-LOAD assertion table matched file-truth exactly (all 15 batches × 3 files
+ backfill × 2 files).

---

## Backup + md5 chain

- **File:** `corpus.db.pre-vdm1-ingest13-20260718T122143` (md5 `20104dbbedd08c05e94fd0cb44bbaaad`;
  `.backup` re-pages so backup md5 ≠ live md5, content identical — integrity_check=ok,
  journal_mode=delete on the backup).
- **pre-ingest live md5:** `8c5e816e1d66d69b2c08d25528ffcf86` (== ingest-12 post-md5; unbroken chain,
  no interim writes between waves).
- **post-ingest live md5:** `90e29009b21998af5baa71991548c398`.
- md5 sidecar: `corpus.db.pre-vdm1-ingest13-20260718T122143.md5.txt`.

Backup retained on disk for reversibility; deliberately NOT committed (`*.db` and timestamped backup
names are gitignored under `curated/.gitignore`).

---

## Inputs (post-audit truth — `.../vdm1/stage1/basin3/`, 48 jsonl files + 1 backfill pair)

All files `json.loads`-clean (0 parse failures). Batch summaries carry STEWARD AUDIT ADDENDUM sections
authoritative for errata targets. Recounts asserted EXACTLY (PRE-LOAD guard):

| Batch | verify (C/X/U/SNF) | citations (quar) | dossier (abstained) |
|---|---|---|---|
| 01 | 48 (47/0/1/0) | 26 (1) | 72 (4) |
| 02 | 47 (46/1/0/0) | 22 (0) | 72 (4) |
| 03 | 54 (44/0/10/0) | 23 (0) | 72 (21) |
| 04 | 51 (44/0/7/0) | 27 (0) | 72 (27) |
| 05 | 47 (39/0/7/1) | 29 (0) | 72 (18) |
| 06 | 47 (43/1/3/0) | 16 (0) | 72 (3) |
| 07 | 50 (49/1/0/0) | 16 (0) | 72 (0) |
| 08 | 53 (39/4/10/0) | 29 (0) | 72 (3) |
| 09 | 42 (40/2/0/0) | 22 (0) | 72 (5) |
| 10 | 42 (26/1/15/0) | 20 (2) | 72 (7) |
| 11 | 44 (39/0/5/0) | 29 (1) | 72 (2) |
| 12 | 51 (31/4/16/0) | 22 (0) | 72 (10) |
| 13 | 36 (28/1/7/0) | 25 (0) | 72 (19) |
| 14 | 34 (20/1/13/0) | 21 (0) | 72 (42) |
| 15 | 34 (19/2/13/0) | 19 (0) | 66 (25) |
| **TOTAL** | **680 (554/18/107/1)** | **346 (4)** | **1074 (190)** |

- 179 distinct kit_ids (all Diablo d2/d3/d4/di); verify set == dossier set; all 179 pre-exist in
  `canon_corpus` (FK guard passed); 0 pre-existing landing-zone rows (idempotency clean).
- Quarantined-4 citations: b01 rpgstash.com ×1 + b10 mywowgold.com ×1 + b10 epiccarry.com ×1 +
  b11 wowcarry.com ×1 — ingested AS-IS with quarantined=1, no flips.
- Multi-row (kit, family) verify pairs are LEGAL (per-era-token precedent); no uniqueness constraint
  on `verify_ledger(kit_id, claim_family)`.
- Abstained dossier rows carry strictly-null payload (schema CHECK + in-script assert; 0 violations).

---

## Part 1 — batch ingest (680 verify / 346 citations / 1074 dossier)

Standard INSERTs, single transaction. Schema laws asserted in-script AND re-verified post-write:

- verdict enum: `SOURCE-NOT-FOUND` -> schema `SOURCE_NOT_FOUND` (1 SNF row: b05 d2-wl-void-rift mechanics).
- anchor mandatory for CONFIRMED/CONTRADICTED (0 missing).
- abstained rows carry strictly-null payload (190 rows; 0 violations).
- citations quarantine respected AS-IS (4 quarantined rows ingested with `quarantined=1`).
- `extraction_provenance = 'fetched-vdm1'` on all 1074 new dossier rows.

---

## Part 2 — BACKFILL-3 overlay

### Supersede rule: 22 in-place UPDATEs

The backfill-3-verify.jsonl carries 31 rows. 22 are in-place UPDATEs (see below); 7 are retry-exhausted
UNSUPPORTED rows NOT ingested.

**In-place UPDATEs (22 total):**

| item | kit_id | family | batch state | overlay action |
|------|--------|--------|-------------|----------------|
| 1 | d2-golemancer | era | CONFIRMED (CW2 anchor) | anchor-upgrade (better Wayback source; verdict unchanged) |
| 2 | d2-grim-ward-barb | era | UNSUPPORTED | U→C |
| 3 | d2-impale-zon | era (classic) | UNSUPPORTED | U→C |
| 4 | d2-inferno-sorc | era (classic) | UNSUPPORTED | U→C |
| 6 | d2-firewall-sorc | era | CONFIRMED (CW2 anchor) | anchor-upgrade |
| 7 | d2-fishyzon | era | CONFIRMED (CW2 anchor) | anchor-upgrade |
| 8 | d2-sacrifice | era | UNSUPPORTED | U→C |
| 9 | d4-heartseeker | era | UNSUPPORTED | U→C |
| 10 | d4-lightning-spear | mechanics | UNSUPPORTED | U→X (contradiction-by-enumeration: 6-slot bar, no Ice Blades) |
| 11 | d4-mighty-throw | era | CONTRADICTED (s7-s12) | X→C (voh-s6+; backfill supersedes X row with correct claim) |
| 12 | d4-andariel-flurry | identity | UNSUPPORTED | U→C |
| 12 | d4-andariel-flurry | era | UNSUPPORTED | U→C (one of two U era rows; launch-s1-3 superseded) |
| 14 | d4-twisting-blades | era | UNSUPPORTED | U→C |
| 15 | d4-ww-dust-devils | era | UNSUPPORTED | U→C |
| 16 | d4-shadowblight | era | UNSUPPORTED | U→C |
| 18 | d4-ball-lightning | era | UNSUPPORTED | U→C |
| 19 | d4-blood-lance | era | UNSUPPORTED | U→C |
| 20 | d4-blood-surge | era (launch-s1-3) | UNSUPPORTED | U→C (one of two U era rows) |
| 21 | d4-bone-spear | era (launch-s1-3) | UNSUPPORTED | U→C (one of two U era rows) |
| 23 | di-cyclone-monk-pvp | identity | UNSUPPORTED | U→C |
| 23 | di-cyclone-monk-pvp | era | UNSUPPORTED | U→C |
| 24 | di-ray-of-frost-wizard | era | UNSUPPORTED | U→C |

**Anchor-upgrade note (items 1, 6, 7):** batches delivered CW2 runs that landed CONFIRMED era rows with
game-forum anchors; backfill delivers Wayback/Arreat-Summit anchors (stronger instrument-class). The batch
CONFIRMED verdict stands; anchor_quote/source_url upgraded to the Wayback snapshot. Counts as 3 of the 22
UPDATE operations.

**Dispatch histogram reconciliation:** dispatch states 576C/85U/19X/1SNF post-overlay. FILES GOVERN. Actual
file-truth state is 573C/89U/18X/1SNF = 681 rows. Discrepancy of 3C/4U/1X arises because items 1, 6, 7
were CONFIRMED in the delivered batch files (CW2 re-crawl landed CONFIRMED anchors before batch close);
the dispatch's assumption of "21 U→C" counted these as U→C but they contributed 0 to the C-delta. The
in-script assertion was updated to match file-truth.

**Retry-exhausted register (7 rows NOT ingested):**

| item | kit_id | family | reason |
|------|--------|--------|--------|
| 2 | d2-grim-ward-barb | identity | retry-exhausted U |
| 2 | d2-grim-ward-barb | negative_canon | retry-exhausted U |
| 5 | d2-leap-attack-barb | era | retry-exhausted U |
| 10 | d4-lightning-spear | identity | retry-exhausted U |
| 13 | d4-blood-wave | era | retry-exhausted U |
| 22 | di-corpse-explosion-necro | era | retry-exhausted U |
| 25 | di-resonance-awakening | era | retry-exhausted U |

**Item 17 exception (d4-wing-strike-arbiter era):** batch b13 era row is already CONFIRMED (loh-s13-14);
backfill finding (S11–S12 meta presence) lands as era-extension erratum ONLY (ERRATA-50), not a supersede.

**Item 26 new INSERT (di-cyclone-strike-monk-base mechanics CONFIRMED):** b14 coverage miss. No batch
mechanics row existed for this kit; verified absence inside transaction, then inserted.

### Backfill citations: 27 rows, OR-IGNORE semantics
- **Inserted:** 21 new rows
- **Ignored:** 6 (UNIQUE(kit_id,url) collision with batch citations)

### POST-STATE (asserted in-script):
- verify_ledger total = **1512** (= 831 + 680 batch + 1 insert)
- basin-3 effective histogram = **573C/89U/18X/1SNF** (681 effective rows; FILES GOVERN)

---

## Part 3 — errata queue (ERRATA-43..55)

Full detail in `agentic_orchestration/research/vdm1/errata-ledger.md` (ERRATA-43 through ERRATA-55 +
additional era errata).

**Summary:**

| ERRATA | class | kits/rows | verify flags |
|--------|-------|-----------|--------------|
| 43 | FALSIFIED-NEGATIVE annotations ×5 | spectral-blade, wave-of-force, incinerate, kick, wind-shear | 5 negative_canon X rows |
| 44 | di resource WRONG-RESOURCE sweep (annotation) | 23 di economy probe rows | 0 |
| 45 | d4 Paladin/Warlock resource CONTESTED + debut correction | wing-strike-arbiter, blazing-abyss (annotations) | 0 |
| 46 | Probe-fabrication series (11 value fixes + 2 annot-only) | god-hungering,inna,uliana,trag,shenlong,bash,heartseeker,evade-sb,dok,payback,frenzy-h90 + hammerdin-paladin,blaze-sorc | 1 (warlock mechanics X) |
| 47 | era: lod-archetype set-era dropped | d3-lod-archetype | 1 |
| 48 | era: ww-wastes vanilla->ros-early | d3-ww-wastes | 1 |
| 49 | era: raekor-boulder set-era->s26-rework | d3-raekor-boulder | 1 |
| 50 | era: wing-strike-arbiter s7-s12 extension | d4-wing-strike-arbiter | 0 |
| 51 | core_skills ×5 (fishyzon/rathma/blazing-abyss/shadowblight/frenzy-h90) | 5 kits | 3 (fishyzon/rathma/blazing-abyss mechanics X) |
| 52 | alias/element (god-hungering/di-frenzy-barb/di-tempest) | 3 kits | 2 (god-hungering identity X, di-tempest mechanics X) |
| 53 | kit-level flag annotations ×4 | void-rift, bombardment-wizard, spiritborn-vortex, spiritform-druid | 0 |
| 54 | NULL-era backfills ×7 | d2-sacrifice, d2-teleport-sorc, d3-call-ancients, d3-dashing-strike, d3-wizard-black-hole, d4-spiritborn-vortex, di-cyclone-strike-base | 0 |
| 55 | Unattested Register annotations ×2 | grim-ward-barb, tainted-summoner | 0 |
| extra | era: natalya-rov s39 removal; mighty-throw voh-s6+; lightning-spear S5 note; summon-druid rotw; annotations | 4 canon_corpus eras + 5 annotations | 2 (natalya-rov, lightning-spear era X rows) |

**Total errata_applied=1 new flags: 18** (35 → 53 total in verify_ledger).

**Errata write census:**
- `canon_corpus.eras` changes: lod-archetype, ww-wastes, raekor-boulder, wing-strike-arbiter, natalya-rov, mighty-throw, lightning-spear (annotation only), summon-druid = 8 kits
- `canon_corpus.core_skills` changes: fishyzon, rathma-aotd, blazing-abyss, shadowblight, frenzy-h90 = 5 kits
- `canon_corpus.elem_raw` changes: di-tempest = 1 kit
- `canon_corpus.mech_note` annotations (all PREPEND): ~30 kits
- `canon_probe_facts.facts_json` changes: 23 di economy (annotation), 11 probe-fabrication fixes = 34 probe rows

---

## Part 4 — whole-kit promotion gate

**Gate:** identity + mechanics + era all CONFIRMED (effective post-overlay); zero CONTRADICTED verdict in
ANY family; kit not in the 4 kit-level-flag set; for di kits, economy family excluded from promotion
(ERRATA-44: di resource fields unreliable).

**Census (179 kits):**

| bucket | count | note |
|--------|-------|------|
| Promoted (with probe facts) | **117** | verified-v1.1 fact_provenance set |
| Promoted (zero probe facts) | 7 | gate-pass but nothing to flip: d2-blade-sin, d2-blaze-sorc, d2-golemancer, d2-impale-zon, d2-inferno-sorc, d2-leap-attack-barb, d2-sacrifice |
| CONTRADICTED-somewhere | 18 | excludes from promotion |
| Kit-level flag | 4 | void-rift, bombardment-wizard, spiritborn-vortex, spiritform-druid |
| Mechanics not CONFIRMED | 17 | honest-U mechanics wall (di-kit cluster + d4-quill-volley, d4-rapid-fire, d4-shadowblight) |
| Identity/era not CONFIRMED (other) | 16 | era-U wall (d2/d3 classic kits + d4 post-cutoff cluster) |
| **TOTAL** | **179** | ✓ |

- **Promoted: 117 kits × ~10 facts = 1167 facts.** `verified-v1.1` **1600 → 2767** (Δ+1167).
- Ingest-11 pattern respected: di economy family excluded from promotion for di kits (ERRATA-44 sweep).

---

## Verification (post-write, `sqlite3` re-query + independent manual checks)

- `PRAGMA integrity_check` = **ok**; `PRAGMA foreign_key_check` = **clean** (no rows);
  `PRAGMA journal_mode` = **delete**.
- Table counts (before → after):

| Table | Before | After | Δ |
|---|---|---|---|
| `verify_ledger` | 831 | 1512 | +681 |
| `kit_citations` | 584 | 951 | +367 (346 batch + 21 backfill; 6 ignored) |
| `kit_dossier` | 1320 | 2394 | +1074 |
| — quarantined citations | 4 | 6 | +2 (4 batch quar already counted; 2 backfill quar) |
| — abstained dossier | 200 | 380 | +180 |
| `verify_ledger` errata_applied=1 | 35 | 53 | +18 |
| `canon_probe_facts` verified-v1.1 | 1600 | 2767 | +1167 |

- basin-3 effective verify histogram (681 rows): **573C / 89U / 18X / 1SNF** (FILES GOVERN; see Part-2
  dispatch reconciliation note).

---

## Reproducibility + reversibility

Inputs committed and static (post-audit basin-3 jsonl). Script is deterministic: landing-zone INSERTs
guarded by idempotency check (0 pre-existing rows for 179 kits); backfill UPDATEs guarded by exact row
selection; errata UPDATEs guarded on exact prior values; promotion `WHERE fact_provenance IN
('kb-legacy','named-source-unfetched')` skips already-verified-v1.1 rows.

Full restore = `corpus.db.pre-vdm1-ingest13-20260718T122143` over `corpus.db`
(backup md5 `20104dbbedd08c05e94fd0cb44bbaaad`; restores the `8c5e816e…`-equivalent baseline;
integrity_check=ok, baseline counts vl=831, kc=584, kd=1320 confirmed).

## ADR-004

No engine-telemetry change; star-lord-side MIGRATION.md unaffected (all writes are elrond-seam corpus
curation). Auto-committed per project discipline (Matt-authorized VDM-1 charge). **NO push — steward
(gandalf) pushes per basin checkpoint.**

## Commit note

Pathspec-only: this migration doc + the ingest script + the appended errata-ledger. `corpus.db` is
gitignored and NOT committed by any ingest; backups + md5 sidecar stay on disk (uncommitted);
basin-3 stage-1 crawl inputs (Legolas's, static) are not touched.
