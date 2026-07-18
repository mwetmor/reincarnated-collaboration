# MIGRATION — VDM-1 ingest wave 12 (basin-2 mapping +76 → 218 + 3 riders)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 basin-2 (VDM-1 verify+dossier+map autonomous run) — run steward gandalf; fires under
Matt's standing autonomous-run mandate. WRITE commission (standing read-only default lifted for
`corpus.db` only).
**Script:** `agentic_orchestration/elrond/research/scripts/vdm1_ingest12_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; never flipped to WAL; single `BEGIN`…`COMMIT` txn;
integrity_check + foreign_key_check both clean post-write).

**Scope — four payloads, one ingest (dispatch INGEST-12):** (1) `kit_mapping` +76 basin-2 rows
(142 → 218); (2) b05 author_credit backfill — 10 abstained rows populated in-place (kit_dossier
stays 1320); (3) `canon_engine_key` WRONG-RESOURCE third-store sweep — 16 gd `resource_verbatim`
rows → energy (ERRATA-41, extends ERRATA-38, steward Ruling 1); (4) le-umbral-blades mech_note
circular-clause reword (ERRATA-42, annotation class).

**FILES GOVERN.** All expected counts asserted PRE-LOAD; a mismatch RAISES before any write
(stop-and-report, no silent reconcile).

---

## Backup + md5 chain

- **Backup:** `corpus.db.pre-vdm1-ingest12-20260718T083334` (md5 `396681ce55f23fde4acc1329b77c8b9f`;
  `.backup` re-pages so backup md5 ≠ live md5, content-identical — integrity_check=ok,
  journal_mode=delete on the backup; baseline counts confirmed on it: kit_mapping=142,
  kit_dossier=1320, gd `resource_verbatim` residue=16).
- **pre-ingest live md5:** `25a812c43243f94296af5405d90f7168` (== ingest-11 post-md5; unbroken chain,
  no interim writes between waves — verified twice pre-write).
- **post-ingest live md5:** `8c5e816e1d66d69b2c08d25528ffcf86`.
- md5 sidecar: `corpus.db.pre-vdm1-ingest12-20260718T083334.md5.txt`.

Backup retained on disk for reversibility; deliberately NOT committed (`*.db` + timestamped-backup
names gitignored under `curated/.gitignore`).

### Execution-integrity note (ingest-11 lesson applied)

The ingest-11 dry-run-wrote-live-db incident (an `importlib` mis-order redirected a "dry-run" onto
the live DB) is banked. This wave took the correct path from the start: **NO dry-run harness pointed
at the live path.** The script's `DB` constant points at live `corpus.db` and it was invoked
directly (`python3 <script>`). All four payloads run inside ONE `BEGIN…COMMIT` txn; every UPDATE
guards `rowcount == expected` and RAISES → ROLLBACK on any mismatch; integrity_check +
foreign_key_check gate the COMMIT. Clean backup + md5 recorded BEFORE the write; live md5 verified ==
baseline (twice) pre-run. Verified via independent `sqlite3 -readonly` after (not the write process).

---

## Payload 1 — kit_mapping ingest (142 → 218; +76 basin-2)

Standard INSERTs (INSERT-only law: any kit_id collision with the existing 142 STOPS the run — 0
collisions; no upsert). Source: `stage2/basin2/mapping-batch-01..07.jsonl` (post-audit truth,
steward-corrected in-place with audit stamps). Per-file 12/12/12/11/11/12/6 = **76** asserted.
`mapping_json` stored as JSON text; `mapping_provenance` default `authored-vdm1`, `authored_date`
default `date('now')` (2026-07-18) stand on all 76.

- **FK:** all 76 kit_ids resolve against `canon_corpus` (0 FK-fail).
- **New-76 grade histogram:** **9 EXACT / 43 CLOSE / 13 APPROX / 11 GAPPED**.
- **New-76 terminal:** **65 MAPPED / 11 MAPPED_DOCKET**.
- Full-table after: kit_mapping = **218** (11E / 139C / 49A / 19G · 199 MAPPED / 19 DOCKET).

### FILE-vs-TARGET histogram divergence (documented; FILES governed)

The dispatch's D-2c verification target stated **9E/44C/12A/11G**. The 76 files carry
**9E/43C/13A/11G** — a 1-row CLOSE↔APPROX difference isolated to **W1** (W2 and W3 match the plan
exactly). The files ARE internally consistent with their own **post-audit per-batch** addenda:
- b01 post-audit `1E/8C/1A/2G` (blade-trap APPROX ratified, audit ruling (c)).
- b02 post-audit `2E/8C/1A/1G` (**forcewave regraded APPROX→CLOSE in-place**; eor-warlord stays
  APPROX — b02 summary line 75/80).
- b03 recount `5E/3C/1A/3G` (stormbox APPROX — b03 summary line 74).
- Sum W1 = **8E/19C/3A/6G** → full-corpus **9E/43C/13A/11G** = the files.

The WAVE-PLAN "W1 CLOSED … 8E/20C/2A/6G" rollup line (and the brief's derived target) undercount
APPROX by 1 / overcount CLOSE by 1 — an **arithmetic slip in the rollup**, not a data error (the b02
running tally at summary line 92, "m02+m03 = 7E/11C/2A/4G", already shows 2 APPROX for m02+m03 alone,
which with b01's blade-trap = 3 W1 APPROX, contradicting the "2 APPROX" rollup). Per FILES-GOVERN
the ingest truth is the files (43C/13A); NO grade was edited to conform to the stale rollup. **The
steward's D-2c battery should expect 9E/43C/13A/11G, not 44C/12A.** Recommend correcting the
WAVE-PLAN W1-CLOSED line + the INGEST-12 SPEC full-corpus figure to 9E/43C/13A/11G.

---

## Payload 2 — b05 author_credit backfill (10 rows abstained → populated; kit_dossier stays 1320)

UPDATE-in-place on the 10 existing abstained author_credit rows (matched on `kit_id` +
`family='author_credit'` + `abstained=1`; the backfill source_urls match the existing rows' URLs, so
the `(kit_id, family, source_url)` UNIQUE constraint is respected — no duplicate family rows
inserted). Source: `stage1/basin2/batch-05-dossier-authorcredit-backfill.jsonl` (legolas `6c14ed8f`,
steward-recounted). Each: `abstained 1→0`, `payload_json` / `source_url` / `anchor_quote` / `conf`
filled. Guarded rowcount==1 per row; total affected == 10; kit_dossier total unchanged at **1320**
(asserted — the UPDATE must not INSERT).

- ⚠ **Zaodon caveat rides IN-ROW as disclosed** (le-low-life-ward: conf 0.75, `note: "thread OP"` —
  QUESTION-thread OP, NOT a build author; the review-book author-lineage discount handles it; no
  annotation strip). **Aayron** is genuine (le-healing-hands-paladin: conf 0.80, 1.0-era build-guide
  thread OP). Both verified in-row post-write.
- Post-write: 10/10 author_credit rows for these kits `abstained=0`.

---

## Payload 3 — canon_engine_key WRONG-RESOURCE third-store sweep (ERRATA-41; 16 gd rows)

Extends ERRATA-38 to the third store flagged (but not swept) at ingest-11; authorized by steward
Ruling 1. Measure-first readonly SELECT == **16** gd `resource_verbatim` rows reading
spirit/focus/lowercase-mana (== expected; STOP-if-≠16 guard did not trip). Guarded exact-prior
UPDATEs, rowcount==1 each:

- `mana` → `energy` (14) · `mana (reserve)` → `energy (reserve)` (1: skeleton-ritualist, qualifier
  preserved per ERRATA-38 precedent) · `spirit/focus` → `energy` (2: belgothian, fire-strike).
- Post-write: gd `resource_verbatim='energy'` = 15 (+ 1 `energy (reserve)` = 16 swept); **0 gd
  residue remaining**; **0 LE contamination** (asserted); `econ_meter_type` (belgothian/fire-strike
  `focus`), `economy_model`, `econ_status` NOT touched (scope = `resource_verbatim` only, mirroring
  ERRATA-38 + the probe store's own post-38 state). The three stores now AGREE on the resource label
  for these 16 gd kits — ERRATA-38's documented divergence resolved.

Errata-ledger: **ERRATA-41** appended (next free number per the ledger index; highest prior = 40).
No `errata_applied` verify flag (policy sweep, per ERRATA-38 precedent — DB errata_applied counter
policy unchanged; the flag is reserved for CONTRADICTED-era verify rows).

---

## Payload 4 — le-umbral-blades mech_note circular-clause reword (ERRATA-42; annotation)

The ingest-11 ANNOT-BASIN2 (h) annotation claimed fetched text "attests… physical/cold (probe
element already reads 'Physical / Cold')" — CIRCULAR to probe (m07 store-grep: 0 cold tokens in
`kit_dossier`/`verify_ledger`; re-confirmed at ingest-12 measure-time, dossier-cold=0/verify-cold=0).
Reworded the circular clause ONLY:

- **before:** `…fetched text attests Umbral Blades as physical/cold (probe element already reads
  'Physical / Cold'), NOT void…`
- **after:** `…probe element reads Physical/Cold; fetched text is element-silent, NOT void…`

Rest of the mech_note preserved verbatim (identity-CONFIRMED note + original two-phase mechanic note).
Guarded rowcount==1, exact-prior match. **ERRATA-42** appended (annotation class; no `errata_applied`
flag; mapping already ships null/null element correctly).

---

## Verification (post-write, `sqlite3 -readonly` + in-script re-query)

- `PRAGMA integrity_check` = **ok**; `PRAGMA foreign_key_check` = **clean**; `PRAGMA journal_mode` =
  **delete**.
- P1: kit_mapping 142 → **218**; new-76 hist 9E/43C/13A/11G · 65 MAPPED / 11 DOCKET; all 76 FK-resolve;
  0 overlap; all `authored-vdm1`/2026-07-18. Spot-join 5 kits (blade-arc EXACT, stormbox APPROX,
  low-life-ward GAPPED/DOCKET, swarmblade CLOSE, wraithlord GAPPED/DOCKET) all resolve to canon_corpus.
- P2: 10/10 author_credit `abstained=0`; kit_dossier == 1320 unchanged; Zaodon 0.75 / Aayron 0.80
  caveats in-row.
- P3: 16 swept (15 energy + 1 energy-reserve); 0 gd residue; 0 LE energy contamination.
- P4: new clause present, old clause gone.

---

## Reproducibility + reversibility

Inputs committed and static (post-audit basin-2 mapping jsonl + b05 backfill jsonl). The script is
deterministic and idempotent: P1 INSERTs re-guard on the overlap check (a re-run aborts on the
collision guard); P2/P3/P4 UPDATEs are guarded on exact prior value + rowcount==1 (a re-run finds the
new value and raises "already applied"); the P3 sweep skips already-`energy` values. Full restore =
`corpus.db.pre-vdm1-ingest12-20260718T083334` over `corpus.db` (backup md5
`396681ce55f23fde4acc1329b77c8b9f`; restores the `25a812c4…`-equivalent baseline).

## ADR-004

No engine-telemetry change; star-lord-side MIGRATION.md unaffected (all writes are elrond-seam corpus
curation: `kit_mapping` inserts, `kit_dossier` author_credit backfill, `canon_engine_key`
resource-label sweep, `canon_corpus.mech_note` annotation). ERRATA-41 resolves the intra-corpus
three-store divergence that ERRATA-38 flagged — an elrond-seam follow-up, NOT an engine request.
Auto-committed per project discipline (Matt-authorized VDM-1 charge). **NO push — steward (gandalf)
pushes per basin checkpoint.**

## Commit note

Pathspec-only (matches ingest-1..11 precedent): this migration doc + the ingest script + the appended
errata-ledger only. `corpus.db` is gitignored and NOT committed by any ingest; backups + md5 sidecar
stay on disk (uncommitted); the basin-2 stage inputs (legolas's, static) are not touched.
