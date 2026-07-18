# MIGRATION — VDM-1 ingest wave 11 (basin-2 full ingest 312/173/468 + errata queue + BACKFILL-1 + whole-kit promotion)

**Date:** 2026-07-18
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 (basin-2 crawl-stage close-in) — run steward gandalf; fires under Matt's standing
autonomous-run mandate. WRITE commission (standing read-only default lifted for `corpus.db` only).
**Script:** `agentic_orchestration/elrond/research/scripts/vdm1_ingest11_2026_07_18.py`
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged; never flipped to WAL; single `BEGIN`…`COMMIT` txn;
integrity_check + foreign_key_check both clean post-write).

**Scope — four parts (dispatch):** (1) ingest the 7 basin-2 batch file-triples (GD + LE, 78 kits)
into `verify_ledger` / `kit_citations` / `kit_dossier`; (2) the accumulated erratum queue
(ERRATA-24..40 + ANNOT-BASIN2 — 10 era restamps, blade-trap restamp, 3 mechanics fixes, the
WRONG-RESOURCE-GENERALLY sweep, 2 probe artifacts, 14 annotations); (3) BACKFILL-1 NULL-field era
backfills (2 kits); (4) whole-kit probe-fact promotion gate.

**FILES GOVERN.** All expected counts asserted EXACTLY on load; a mismatch RAISES (the dispatch's
"stop and report, do not reconcile silently" rule is enforced in-script, PRE-LOAD, before any write).

---

## Backup + md5 chain

- **File:** `corpus.db.pre-vdm1-ingest11-20260718T060151` (md5 `7866c90f9fef4d50557e0846cc2c3e78`;
  `.backup` re-pages so backup md5 ≠ live md5, content identical — integrity_check=ok,
  journal_mode=delete on the backup).
- **pre-ingest live md5:** `862229859306d5ccce487bee2a7c8e9b` (== ingest-10 post-md5; unbroken
  chain, no interim writes between waves).
- **post-ingest live md5:** `25a812c43243f94296af5405d90f7168`.
- md5 sidecar: `corpus.db.pre-vdm1-ingest11-20260718T060151.md5.txt`.

Backup retained on disk for reversibility; deliberately NOT committed (`*.db` and `*-backup`-adjacent
timestamped names are gitignored under `curated/.gitignore`; a backup belongs on disk). The stale
`corpus.db-shm` (from 01:44, pre-existing, no `-wal`) was left untouched per the ingest-4 dispatch
law (deleting -shm/-wal previously broke concurrent readonly crawlers; harmless in DELETE mode).

### Execution-integrity note (harness bug → restore → deliberate re-run)

An initial in-process **dry-run harness** intended to run the script against a scratch copy
mis-ordered `importlib` (set `mod.DB` BEFORE `exec_module`, which re-defined the module-level `DB`
constant back to the live path) — so the "dry-run" actually committed to LIVE `corpus.db`. The write
was correct, complete, and integral (the script's single-txn design held), BUT reaching the state via
an accidental path is not acceptable stewardship. **Remediation:** the clean backup was RESTORED over
`corpus.db` (restored md5 `7866c90f…` = backup re-paged, content-identical to the `862229…` baseline;
integrity_check=ok, all baseline counts confirmed: verify=519, verified-v1.1=1040, aar eras original,
quar=1), then the ingest was re-run **deliberately** via direct `python3 <script>` execution (the
correct path — the script's `DB` constant points at live `corpus.db`). The post-ingest md5
`25a812c43243f94296af5405d90f7168` is the deliberate-run result. Lesson banked: dry-run redirects must
override `DB` AFTER `exec_module`, or (better) parameterize the DB path as a CLI arg. Scratch DBs
removed.

---

## Inputs (post-audit truth — `.../vdm1/stage1/basin2/`, 21 jsonl files, 7 batches)

All 21 files `json.loads`-clean (0 parse failures). Batch summaries carry STEWARD AUDIT ADDENDUM
sections authoritative for errata targets. Recounts asserted EXACTLY (PRE-LOAD guard):

| Batch | verify (C/X/U/SNF) | citations (quar) | dossier (abstained) |
|---|---|---|---|
| 01 | 37 (32/2/3/0) | 25 (0) | 72 (26) |
| 02 | 36 (29/7/0/0) | 27 (0) | 72 (3) |
| 03 | 41 (37/2/2/0) | 22 (0) | 72 (10) |
| 04 | 52 (42/1/6/3) | 23 (0) | 72 (12) |
| 05 | 59 (44/1/14/0) | 31 (0) | 72 (15) |
| 06 | 54 (36/0/18/0) | 25 (1) | 72 (5) |
| 07 | 33 (30/0/3/0) | 20 (0) | 36 (2) |
| **TOTAL** | **312 (250/13/46/3)** | **173 (1)** | **468 (73)** |

- 78 distinct kit_ids (41 gd + 37 le); verify set == dossier set; all 78 pre-exist in `canon_corpus`
  (FK guard passed); 0 pre-existing landing-zone rows (idempotency clean).
- The 1 quarantined citation = `le-smite-paladin` / lastepochtools.com (b06, steward-quarantined;
  ingested AS-IS with `quarantined=1`, NO flip).
- Multi-row (kit, family) verify pairs are LEGAL (per-era-token + per-component verdicts,
  steward-accepted run-wide; DB precedent hades2-omega-magick, poe1-arc). No uniqueness constraint
  on `verify_ledger(kit_id, claim_family)`.

---

## Part 1 — landing-zone ingest (312 verify / 173 citations / 468 dossier)

Standard INSERTs, single transaction. Schema laws asserted in-script AND re-verified post-write:

- **verdict enum:** file `SOURCE-NOT-FOUND` -> schema `SOURCE_NOT_FOUND` (3 SNF rows this wave, all
  b04 le-bomb-lance-falconer). Anchor mandatory for CONFIRMED/CONTRADICTED (0 missing).
- **abstained dossier rows carry strictly-null payload** (schema CHECK + in-script assert; 0
  violations either direction). All non-null basin-2 payloads valid JSON (json_valid).
- **citations quarantine respected AS-IS:** the 1 quarantined row (b06 smite/lastepochtools)
  ingested with `quarantined=1`; no flip.
- **extraction_provenance** = `fetched-vdm1` on all 468 new dossier rows.

Table counts (before -> after):

| Table | Before | After | Δ |
|---|---|---|---|
| `verify_ledger` | 519 | 831 | +312 |
| `kit_citations` | 411 | 584 | +173 |
| `kit_dossier` | 852 | 1320 | +468 |
| — quarantined citations | 1 | 2 | +1 |
| — abstained dossier | 127 | 200 | +73 |
| `verify_ledger` errata_applied=1 | 22 | 35 | +13 |

Basin-2 verdict histogram (post-write, re-queried): **CONFIRMED 250 / CONTRADICTED 13 /
UNSUPPORTED 46 / SOURCE_NOT_FOUND 3** — exact.

---

## Part 2 — errata queue (ERRATA-24..40 + ANNOT-BASIN2; full detail in errata-ledger.md)

All guarded single-row/row-set UPDATEs; anchors read BEFORE writing; raw prior preserved (probe
`_prior_ingest11` key; mech_note PREPEND with original verbatim). The 13 CONTRADICTED verify rows
are flagged `errata_applied=1` (blade-trap is NOT flagged — its era row is UNSUPPORTED post steward
reclass, so the 13 flagged rows == the 13 CONTRADICTED verdicts exactly).

### (a) D-2a era-floor restamps ×10 — ERRATA-24..33

**Floor-too-early ×8 (drop the impossible pre-debut band):**

| kit | old eras | new eras | mastery blocker |
|---|---|---|---|
| gd-aar-spellbinder | `base-2016;aom-2017;fg-2019;patch-1.1-1.2` | `aom-2017;fg-2019;patch-1.1-1.2` | Necromancer=AoM |
| gd-callidors-tempest-templar | `base-2016;fg-2019;patch-1.1-1.2` | `fg-2019;patch-1.1-1.2` | Oathkeeper=FG |
| gd-fire-strike-purifier | `base-2016;aom-2017;patch-1.1-1.2` | `aom-2017;patch-1.1-1.2` | Inquisitor=AoM |
| gd-forcewave-warlord | `base-2016;fg-2019;patch-1.1-1.2` | `fg-2019;patch-1.1-1.2` | Oathkeeper=FG |
| gd-mortar-purifier | `base-2016;aom-2017;patch-1.1-1.2` | `aom-2017;patch-1.1-1.2` | Inquisitor=AoM |
| gd-panettis-mage-hunter | `base-2016;aom-2017;patch-1.1-1.2` | `aom-2017;patch-1.1-1.2` | Inquisitor=AoM |
| gd-primal-strike-vindicator | `base-2016;aom-2017;patch-1.1-1.2` | `aom-2017;patch-1.1-1.2` | Inquisitor=AoM |
| gd-shadow-strike-infiltrator | `base-2016;aom-2017;patch-1.1-1.2` | `aom-2017;patch-1.1-1.2` | Inquisitor=AoM |

**Floor-too-LATE ×2 (ADD the earlier attested floor band):**

| kit | old eras | new eras | reason |
|---|---|---|---|
| gd-vitality-conjurer | `aom-2017;fg-2019;patch-1.1-1.2` | `base-2016;aom-2017;fg-2019;patch-1.1-1.2` | Conjurer = Occ+Shaman, both base-game |
| le-healing-hands-paladin | `1.1-harbingers;1.4-omens` | `1.0-launch;1.1-harbingers;1.4-omens` | skill tree debuted at 1.0 launch |

Each restamp also flags its `era`-family CONTRADICTED verify row `errata_applied=1`.

### (b) gd-blade-trap era restamp — ERRATA-34

`base-2016;aom-2017;fg-2019;patch-1.1-1.2` -> `base-2016;aom-2017` (attested window). The crawl's
original CONTRADICTED was steward-RECLASSED CONTRADICTED->UNSUPPORTED in-place (claim-vs-claim
grounds + spec-text anchor, both illegal for CONTRADICTED — the basin-2 "claim-vs-claim is never
contradiction grounds" law). **NO `errata_applied` flag** (the row is UNSUPPORTED). The
negative_canon_target "mechanism later reworked" clause is UNVERIFIED from fetched text — recorded as
a `mech_note` ANNOTATION, NOT asserted.

### (c) mechanics content fixes ×3 — ERRATA-35/36/37

- **fire-strike (ERRATA-35):** probe economy `resource_verbatim` spirit/focus->energy (part of the
  (d) sweep) AND `model` meter->attack-replacer, `meter_type` focus->n/a (Fire Strike is a
  default-attack replacer, not a meter skill). mechanics row flagged.
- **panettis (ERRATA-36):** `elem_raw` lightning->`mixed(fire/cold/lightning)`; probe element label
  ->tri-elemental (shock-downstream-unreliable). mechanics row flagged.
- **pet-conjurer (ERRATA-37):** `core_skills` `Call of the Grave` (Necromancer) -> `Call of the
  Beast` (Shaman). mechanics row flagged.

### (d) WRONG-RESOURCE-GENERALLY sweep — ERRATA-38 [SYSTEMATIC CLASS]

GD's resource is **Energy** ("Spirit" is a GD STAT name — the confusion source). Swept ALL `gd-*`
resource fields reading spirit/focus/lowercase-mana in the **two dispatch-named stores**:

| store / field | gd hits | mapping |
|---|---|---|
| `canon_probe_facts` economy `facts_json.resource_verbatim` (+ leading `plain_text` token) | **16** | `mana`→`energy` (14); `mana (reserve)`→`energy (reserve)` (1); `spirit/focus`→`energy` (2) |
| `canon_corpus.econ_raw` | **13** | `mana`→`energy` substring (all `mana-…` compounds; 0 spirit/focus in econ_raw) |

- **NOT touched (safety-asserted post-write):** all `le-*` rows (LE Mana is CORRECT, capital-M; 0 LE
  resource fields relabelled; chthonic/erasing-strike/etc. economy still "Mana"). No LE `econ_raw`
  set to energy. d3/di Monk Spirit is GENUINE (basin-3 concern; not in scope).
- **NOT swept — FLAGGED for steward (scope discipline): `canon_engine_key.resource_verbatim`.**
  A THIRD store carries the SAME 16 gd artifacts (14 `mana` + 2 `spirit/focus` — belgothian +
  fire-strike; `economy_model`/`econ_meter_type` mirror the probe values). The dispatch named only
  `canon_corpus` + `canon_probe_facts`; per no-silent-scope-expansion, `canon_engine_key` was NOT
  swept this wave. **Recommendation:** a steward-directed follow-up erratum should sweep
  `canon_engine_key.resource_verbatim` (+ `economy_model` where 'generator-spender'/'spend' encodes
  the mana/focus assumption) for the same 16 gd kits, to keep the three stores consistent. Left
  un-swept, `canon_engine_key` and `canon_probe_facts` now DISAGREE on the resource label for these
  16 kits — an intentional, documented divergence pending steward ruling (I did not expand scope
  unilaterally).

### (e)-(m) probe artifacts + annotations

- **(e) ERRATA-39:** chthonic-fissure probe element `label_verbatim` "Void / Fire (FI suffix)" ->
  "fire / necrotic" (void unattested, generation artifact). LE kit — economy "Mana" NOT swept.
- **(i) ERRATA-40:** manifest-armor probe economy `resource_verbatim` "Forge Stacks" -> "Mana"
  (probe-fact fabrication; fetched Mana-based; model/builder_source preserved). LE Mana, NOT the
  gd->Energy sweep.
- **(f),(g),(h),(j),(k),(l),(m),(n) — ANNOT-BASIN2:** 14 `mech_note`-PREPEND annotations (no value
  change). Class/alias/framing (tempest-strike Acolyte-drop + negative era-scope · runic-invocation
  Primalist artifact · umbral-blades void-alias · fire-aura Flame-Ward framing · ghostflame
  beam→cone review); descriptive/negative/era WATCH (word-of-pain elem · harvest-lich CHIMERA ·
  stun-jacks negative-unverified · stormbox + detonating-arrow identity-intent · wraithlord era ·
  hammer-throw rename · storm-totem Spriggan Rage). All spec-field corrections land in `mech_note`
  because `canon_corpus` has no `class` column and none of these kits has a `roster_atlas` row
  (ERRATA-21/22/23 pattern).

**Errata write census:** 13 verify rows flagged; value changes on `canon_corpus.eras` (11:
10 restamps + blade-trap), `canon_corpus.elem_raw` (1: panettis), `canon_corpus.core_skills`
(1: pet-conjurer), `canon_corpus.econ_raw` (13: sweep), `canon_corpus.mech_note` (16 annotations +
2 backfill notes = 18 kits), `canon_probe_facts.facts_json` (16 economy sweep + fire-strike model +
panettis element + chthonic element + manifest resource = 19 probe rows).

---

## Part 3 — BACKFILL-1 (NULL-field era backfills; steward-ratified)

Guarded on `eras IS NULL OR eras=''`; raw prior (empty) recorded in the mech_note backfill note
under `_prior_ingest11`.

| kit | eras (NULL) -> | note |
|---|---|---|
| le-ring-of-shields | `1.0-launch;1.1-harbingers` | Forge Guard shield wall |
| le-shift-bladedancer | `beta-0.8-0.9;1.0-launch;1.1-harbingers;1.4-omens` | 1.2-woven unverifiable — OMITTED |

---

## Part 4 — whole-kit probe-fact promotion gate (ratified at ingest-10)

**Gate:** a kit's probe facts flip `kb-legacy`/`named-source-unfetched` -> `verified-v1.1` IFF
mechanics=CONFIRMED-with-anchor AND ZERO CONTRADICTED verdict in ANY family AND the kit HAS probe
facts. Computed from the just-ingested verify rows (files govern); cross-checked against DB post-write.

- **Promoted: 56 kits × 10 facts = 560 facts.** `verified-v1.1` **1040 -> 1600** (Δ+560).
  Provenance split of the 560: 50 were `kb-legacy`, 510 `named-source-unfetched` pre-flip →
  `kb-legacy` 1750→1700 (−50), `named-source-unfetched` 1990→1480 (−510). Total facts unchanged (4780).
- DB cross-check: exactly the 56 computed kits carry `verified-v1.1` facts; matches the computed set
  EXACTLY; **zero excluded kits leaked** into promotion.

### Exclusion census (22 kits)

| bucket | count | kits |
|---|---|---|
| CONTRADICTED-somewhere (ERRATA-24..37 carriers) | 11 | aar-spellbinder, callidors-tempest-templar, fire-strike-purifier, forcewave-warlord, mortar-purifier, panettis-mage-hunter, pet-conjurer, primal-strike-vindicator, shadow-strike-infiltrator, vitality-conjurer, healing-hands-paladin |
| clean but mechanics NOT CONFIRMED | 3 | gd-berserker-wereforms (mech-U; unshipped FoA) · **le-bomb-lance-falconer** (mech-SNF; full SNF → Unattested Register + re-crawl queue) · **le-harvest-lich** (mech-U; CHIMERA per (m)) |
| gate-pass but ZERO probe facts (nothing to flip) | 8 | gd-blade-trap, gd-reap-spirit, gd-stun-jacks, le-ring-of-shields, le-shield-bash-le, le-shift-bladedancer, le-soul-feast, le-tempest-strike |

**Census: 56 promoted + 11 contra + 3 mech-not-conf + 8 zero-fact = 78 ✓.**

- The mandatory exclusions (bomb-lance, harvest-lich) are captured by the gate itself (both are
  mechanics-not-CONFIRMED → not gate-pass); asserted in-script that neither is in the promote set.
  Both DO carry 10 probe facts each (all `named-source-unfetched` / `kb-legacy` respectively) — 0 of
  which were promoted. gd-berserker-wereforms likewise (10 facts, unpromoted).
- **NULL-field kits post-backfill:** ring-of-shields + shift-bladedancer are gate-PASS (id+mech
  CONFIRMED, zero-contra) but carry ZERO probe facts even after the era backfill (backfill adds era
  stamps, not probe rows) → zero-fact bucket; nothing to promote. Correct, not a miss.

---

## Verification (post-write, `sqlite3 -readonly` + independent Python)

- `PRAGMA integrity_check` = **ok**; `PRAGMA foreign_key_check` = **clean** (no rows);
  `PRAGMA journal_mode` = **delete**.
- Landing zone reconciles exactly: verify +312 (250C/13X/46U/3SNF), citations +173 (1 quar),
  dossier +468 (73 abstained, all strictly-null payload, all non-null valid JSON); 78 kits, no stray.
- 13 newly errata-flagged verify rows == the 13 CONTRADICTED verdicts, each on its correct claim
  family (fire-strike + panettis flag BOTH mechanics + era; pet-conjurer flags mechanics; the 8
  pure-era kits flag era). blade-trap NOT flagged (UNSUPPORTED). errata_applied total 22→35.
- All 10 era restamps + blade-trap verified to their exact target values. Resource sweep: 0 gd
  probe-economy resource labels and 0 gd `econ_raw` still reading mana/spirit/focus (16 + 13 swept);
  fire-strike model=attack-replacer/meter_type=n/a; LE resource fields untouched (0 LE energy).
  Content fixes (panettis elem, pet-conjurer Beast, chthonic "fire / necrotic", manifest "Mana")
  verified. Backfills verified. 14 annotations mech_note-prepended. Promotion 1040→1600; excluded
  kits (panettis, harvest-lich, vitality-conjurer, bomb-lance) confirmed unpromoted; promoted spot
  (aegis-paladin) all verified-v1.1.

---

## Reproducibility + reversibility

Inputs committed and static (post-audit basin-2 jsonl). The script is deterministic and idempotent:
landing-zone INSERTs are re-guarded (0 pre-existing rows for the 78 kits — a re-run aborts on the
idempotency guard); errata UPDATEs are guarded on exact prior value (a re-run finds the new value and
raises on the rowcount==1 guard, signalling "already applied"); the sweep skips already-`energy`
values; the promotion `WHERE fact_provenance IN (kb-legacy, named-source-unfetched)` skips
already-`verified-v1.1` rows. Full restore = `corpus.db.pre-vdm1-ingest11-20260718T060151` over
`corpus.db` (backup md5 `7866c90f9fef4d50557e0846cc2c3e78`; restores the `862229…`-equivalent
baseline).

## ADR-004

No engine-telemetry change; star-lord-side MIGRATION.md unaffected (all writes are elrond-seam corpus
curation: `verify_ledger` / `kit_citations` / `kit_dossier` inserts, `canon_corpus` +
`canon_probe_facts` errata, `canon_probe_facts.fact_provenance` promotions). The
`canon_engine_key.resource_verbatim` divergence flagged in ERRATA-38 (d) is an intra-corpus steward
follow-up, NOT an engine-telemetry request. Auto-committed per project discipline (Matt-authorized
VDM-1 charge). **NO push — steward (gandalf) pushes per basin checkpoint.**

## Commit note

Pathspec-only (matches ingest-1..10 precedent): this migration doc + the ingest script + the
appended errata-ledger only. `corpus.db` is gitignored (`*.db`) and is NOT committed by any ingest;
backups + md5 sidecar stay on disk (uncommitted); the basin-2 stage-1 crawl inputs (Legolas's, static)
are not touched.
