# MIGRATION — VDM-1 ingest wave 9 (basin-1 b03+b04 + six-item adjudication docket)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 (basin-1)
**Script:** `agentic_orchestration/research/scripts/vdm1_ingest9_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; never flipped to WAL; single short write txn;
integrity_check + foreign_key_check both clean post-write)

**Scope — two parts (dispatch):** (1) standard stage-1 ingest of basin-1 batches 03+04
(kits 25-48 across poe2/hades2/tq2) into `verify_ledger` / `kit_citations` /
`kit_dossier`, mirroring ingest-1..8 practice; (2) a six-item adjudication docket, of
which items 1 and 3 are the **run's FIRST CONTENT-field errata** (identity/mechanics/class
corrections) — all prior errata (ERRATA-1..18) were era-family band corrections.

---

## Backup

- **File:** `corpus.db.pre-vdm1-ingest9-20260718T041317`
- **md5:** `3f176914508dae2708b15799872bed5e` (matched live DB at backup time via
  `.backup`; integrity_check=ok, journal_mode=delete on the backup)
- **post-ingest live md5:** `c8dbd4898d0aa8878648c47ef95cc7dd`

The backup is retained on disk for reversibility. NOTE the dispatch-specified name uses a
timestamp suffix (`pre-vdm1-ingest9-<ts>`), which matches NEITHER the `*.db` nor the
`*-backup` gitignore rule — so it is trackable. Per the pathspec-only commit discipline it
is deliberately NOT committed (a backup belongs on disk, not in git); `corpus.db` itself is
gitignored (`*.db`) and was not committed by any of ingests 1-8 (verified) — this ingest
follows that unbroken precedent.

---

## Inputs (committed, static — under `.../vdm1/stage1/basin1/`, HEAD 362f342b)

Row counts RECOUNTED from files (file-truth governs; agent summaries drifted — D-2c):

| File | Rows | Destination |
|---|---|---|
| `batch-03-verify.jsonl` | 37 (31 CONFIRMED / 3 CONTRADICTED / 3 UNSUPPORTED / 0 SNF) | `verify_ledger` |
| `batch-03-citations.jsonl` | 25 (2 quarantined — the run's FIRST quarantined rows) | `kit_citations` |
| `batch-03-dossier.jsonl` | 72 (21 abstained) | `kit_dossier` |
| `batch-04-verify.jsonl` | 39 (35 CONFIRMED / 4 CONTRADICTED / 0 U / 0 SNF) | `verify_ledger` |
| `batch-04-citations.jsonl` | 31 (0 quarantined) | `kit_citations` |
| `batch-04-dossier.jsonl` | 72 (14 abstained) | `kit_dossier` |

- b04-dossier line 11 (poe2-witchhunter-grenades author_credit) was steward-repaired
  upstream (duplicate closing brace removed); full file parses clean — ingested as-is
  (validated in Python: json.loads over all 6 files, 0 parse failures).
- 24 distinct kit_ids; verify set == dossier set; all 24 pre-exist in `canon_corpus`
  (FK guard passed).

---

## Part 1 — landing-zone ingest (76 verify / 56 citations / 144 dossier)

Standard INSERTs, single transaction, idempotency re-guarded inside the txn (0 pre-existing
landing-zone rows for these 24 kits). Schema laws asserted in-script AND re-verified post-write:

- **verdict enum:** file `SOURCE-NOT-FOUND` -> schema `SOURCE_NOT_FOUND` mapping ready (0 fired
  — no SNF rows this batch). Anchor mandatory for CONFIRMED/CONTRADICTED (0 missing).
- **abstained dossier rows carry strictly-null payload** (schema CHECK + in-script assert;
  0 violations either direction). All 852 non-null dossier payloads valid JSON (json_valid).
- **citations quarantine respected:** the 2 quarantined rows (b03) ingested with
  `quarantined=1` — `poe2-temporalis-blink` (mobalytics jungroan, `authored`) and
  `poe2-walking-calamity` (mmoexp). See REVIEW-3 below re: temporalis-blink.
- **negative_canon filler guard:** exactly 1 negative_canon verify row ingested this wave
  (`poe2-wall-of-shields|CONFIRMED`, id>443) — the sole negative kit in b03/b04 carrying such
  a row. `poe2-perfect-strike-01` (negative=1, referenced in dispatch) is NOT in these
  batches; its negative_canon row is from a prior ingest. No filler leaked.
- **extraction_provenance** = `fetched-vdm1` on all 144 new dossier rows.

Table counts (before -> after):

| Table | Before | After | Δ |
|---|---|---|---|
| `verify_ledger` | 443 | 519 | +76 |
| `kit_citations` | 355 | 411 | +56 |
| `kit_dossier` | 708 | 852 | +144 |
| — quarantined citations | 0 | 2 | +2 |
| — abstained dossier | 92 | 127 | +35 |
| `verify_ledger` errata_applied=1 | 16 | 22 | +6 |

---

## Part 2 — adjudication docket (six items; anchors read BEFORE writing)

All are guarded single-row UPDATEs asserting the exact prior value + rowcount==1. Full
anchor quotes + rationale are in the errata ledger (`.../vdm1/errata-ledger.md`) as
ERRATA-19..23 + ANNOT-BASIN1 (wave 9). One-line dispositions:

1. **poe2-walking-calamity — ERRATA-19, CONTENT correction (identity + mechanics).** kb
   MISDESCRIBED the kit (b03 contradicted BOTH identity + mechanics). `folk_name`
   "Walking Calamity Autobomber" -> "Walking Calamity Shaman"; `core_skills`
   `["herald/retaliation procs","Molten Crash(weapon)"]` ->
   `["Walking Calamity","Herald of Ice","Polcirkeln"]`. 2 CONTRADICTED verify rows flagged
   `errata_applied=1`. **Run's FIRST identity-family contradiction + first CONTENT erratum.**
2. **poe2-warbringer-totems — ERRATA-20, era restamp.** Drop pre-debut 0.1 band (Ancestral
   Warrior Totem version history begins v0.2.0). `0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients`
   -> `0.2-dawn;0.3-edict;0.4;0.5-ancients`. 1 CONTRADICTED era row flagged. D-2a class.
3. **tq2 class-field ×3 — ERRATA-21/22/23, CONTENT corrections via `mech_note`.**
   whirlwind-rogue -> Warfare (identity-family contradiction); elementalist -> Storm+Earth
   PAIRING (mechanics); stormblade-ice-shards -> Rogue+Storm dual (mechanics). **STRUCTURAL:**
   `canon_corpus` has no `class` column; none of the 3 kits has a `roster_atlas` row (the
   only class store) — mirrors REVIEW-2 poets-pen-vd. Correction recorded as a dated
   `mech_note` PREPEND (established class/lineage annotation home) with the original harvest
   note preserved verbatim. 3 CONTRADICTED rows flagged on their CORRECT claim families
   (whirlwind=identity; other two=mechanics — a per-kit distinction the guard caught).
4. **hades2-omega-magick — movement probe-fact correction.** kb `canon_probe_facts` movement
   family claimed sprint-while-charging/full-move; b04 attests STATIONARY. `facts_json`
   `verbs`->`["stationary-while-charging"]`, `policy_while_casting`->`"stationary"`; raw prior
   preserved under a `_prior_ingest9` key (no-silent-transformation). NO errata flag
   (convention reserves it for CONTRADICTED-era rows; this is a movement/mechanics contradiction).
5. **Alias spelling — tq2-elementalist.** "Rolling Magma" -> "Roiling Magma" in `core_skills`
   (sole basin-1 row carrying the misspelling; correct spelling coexisted nowhere). Guarded.
6. **Erasure annotation (poe2-erasure-edc-lich) — RE-VERIFIED intact, NO action.** ingest-8
   REVIEW-2 annotation stands untouched (core_skills keeps "Erasure"; mech_note leads with the
   PHANTOM-CANDIDATE clause). Asserted in-script; a missing/altered annotation would have HALTED.

---

## REVIEW-3 (basin-1) — temporalis-blink quarantine/anchor conflict (steward eyes)

The `mobalytics.gg/.../blink-autobomber-jungroan` citation is `quarantined=1` YET the SAME URL
is the crawler's `source_url` anchor for temporalis-blink's identity CONFIRMED verify row AND
its variants dossier row (both faithfully ingested from file-truth). This violates the
"quarantined rows never surface as verify/dossier sources" rule — but the conflict is IN the
source JSONL (Legolas both quarantined the domain and used it as an anchor), not in the ingest.
Per no-silent-transformation, elrond did NOT rewrite the crawler's attribution nor invent a
substitute (no alternate in-file source backs the identity claim). Notable: the citation is
`cite_class='authored'` (named author jungroan), NOT junk-tail — so the quarantine FLAG may be
the error, not the anchor usage. Recommended steward (gandalf) action: (a) un-quarantine the
mobalytics citation if judged a legitimately-authored mis-flag (zero re-crawl), OR (b) targeted
re-crawl to re-anchor. Faithful file-truth ingest stands until ruled. Recorded in the errata
ledger. (Contrast walking-calamity's quarantined mmoexp citation — correctly backs NO
verify/dossier row, the clean case.)

---

## Promotion policy (basin-1 non-promotion — matches ingest-8)

The dispatch's "standard promotions for clean kits per the established gate (mechanics-CONFIRMED
& zero-CONTRADICTED; identity-UNSUPPORTED does not block — minion-pact-bv precedent)" was applied
at the VERDICT level: 18 of 24 kits are verdict-clean; 6 carry a CONTRADICTED verdict
(walking-calamity, warbringer-totems, hades2-omega-magick, tq2-elementalist,
tq2-stormblade-ice-shards, tq2-whirlwind-rogue) and are EXCLUDED.

**No `fact_provenance` probe-fact promotion to `verified-v1.1` was written this ingest**, matching
the immediate and ONLY prior basin-1 precedent: ingest-8's clean PoE2 probe-fact-bearing kits
(demon-form, minion-infernalist, infernal-legion) were likewise left `kb-legacy` (verified). The
720 verified-v1.1 facts remain exactly the 72 clean PoE1 kits promoted at ingest-4 (the last
promoting ingest; ingest-5 MIGRATION: "NO promotions this wave, those all landed at ingest-4").
The `minion-pact-bv` precedent named in the dispatch is a PoE1 promotion (mechanics-CONFIRMED +
identity-UNSUPPORTED -> verified-v1.1) done at ingest-4; it governs the GATE LOGIC (identity-
UNSUPPORTED is honest silence), but the basin-1 execution precedent does NOT write PoE2/hades2/tq2
probe-fact promotions. **If a basin-1 probe-fact promotion sweep was intended it is a distinct
steward-directed action** (would promote the 17 clean probe-fact-bearing b03/b04 kits ×10 = 170
facts) — flagged for the steward, not written speculatively.

---

## Verification (post-write, `sqlite3 -readonly`)

- `PRAGMA integrity_check` = **ok**; `PRAGMA foreign_key_check` = **clean** (no rows);
  `PRAGMA journal_mode` = **delete**.
- Inserts reconcile exactly: verify +76 (37+39), citations +56 (25+31), dossier +144 (72+72);
  all 24 kits represented, no stray kit_ids.
- 6 newly errata-flagged rows == the 6 CONTRADICTED verdicts, each on its correct claim family.
- Quarantined=2 (expected pair); abstained=127 (92+35); every non-null payload valid JSON.
- All six adjudications re-queried and confirmed post-write.

## Reversibility

Restore = copy `corpus.db.pre-vdm1-ingest9-20260718T041317` over `corpus.db` (md5
`3f176914508dae2708b15799872bed5e`). The ingest is deterministic and re-runnable from the
committed static inputs via the committed script; the idempotency guard prevents double-ingest.
