# MIGRATION — VDM-1 POST-REVIEW RATIFICATION (the run's final write)

**Date:** 2026-07-19
**Steward:** elrond (single writer, `corpus.db`)
**Run:** vdm1 (post-review ratification pass) — run steward gandalf (SPEC-AUTHOR).
Fires under Matt's standing autonomous-run mandate. WRITE commission (standing read-only
default lifted for `corpus.db` only).
**Brief (single source of truth):** `agentic_orchestration/research/vdm1/MIGRATION-BRIEF-post-review.md`
**Authorities:** `REVIEW-BOOK.md` §§ 2/4/5/10 · `errata-ledger.md` · `stage5/BLIND-RIDER-DIVERGENCE-REPORT.md` ·
`agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-crosswalks.md` (§ 8 element/ailment law).
**Ruling status:** ALL eleven rulings D-1…D-11 are **Matt-ratified** (REVIEW-BOOK.md § 2 + Matt margins
2026-07-19). Nothing here re-opens a ruling; every operation traces to a Matt-ratified ruling.
**Scripts:**
- `agentic_orchestration/research/scripts/vdm1_migration_post_review_2026_07_19.py` (the migration; single transaction)
- `agentic_orchestration/research/scripts/vdm1_compendium_gen_2026_07_19.py` (D-11a compendium regen; read-only)
**DB:** `agentic_orchestration/research/curated/corpus.db`
**journal_mode:** DELETE (unchanged). Migration ran in a single `BEGIN…COMMIT`; `integrity_check`=ok and
`foreign_key_check`=clean asserted pre-commit AND on final state. sqlite 3.42.0 (≥3.35 for `DROP COLUMN`).

**Do NOT git-commit** — the steward (gandalf) does the single pathspec commit after an independent
read-only verify battery. `corpus.db` is gitignored-local. Git-tracked outputs of this migration:
the 4 `errata-ledger.md` entries (ERRATA-56…59), the regenerated compendium
(`research/vdm1/compendium/`), the two scripts, and this doc.

---

## Backup + md5 chain (HARD RULE 1)

- **Backup file:** `corpus.db.pre-review-ratification-20260719T200446Z` (retained on disk; gitignored).
- **Backup md5 sidecar:** `corpus.db.pre-review-ratification-20260719T200446Z.md5.txt`
- **Pre-migration md5 (chain-head, == INGEST-18 post-md5):** `4a1ae47c7ded48f6443780602eb7e8ea`
- **Content-md5-before-final-stamp:** `cb51101d61db53f93967db5e39b3b5c7` (the DB state at COMMIT, before the
  post-commit md5-stamp note-write; recorded inside `corpus_schema_meta.v1.1-verified`)
- **Post-migration file md5 (pre citation-fold):** `6a9a6e5dfa188f8b8c3a3ada99c2f084`
- **TRUE FINAL file md5 (authoritative, post D-11e citation-fold):** `50df15b776ad5b0da93fe90cdee1163d`
- **md5 chain:** `4a1ae47c…` → `6a9a6e5d…` (migration) → `50df15b776ad5b0da93fe90cdee1163d` (D-11e citation fold)
- **Second backup (pre citation-fold):** `corpus.db.pre-ud-snowstorm-citation-20260719T201600Z`
  (md5 `6a9a6e5dfa188f8b8c3a3ada99c2f084`) + sidecar.

> **md5 fixpoint note (D-10 honesty):** stamping the post-md5 INTO the DB (per the brief's "record post-md5
> in the meta table") inherently changes the file's md5 — an in-DB checksum can never equal its own file
> md5. So `corpus_schema_meta` carries the pre-stamp content checksum (`cb51101d…`) plus a self-documenting
> note pointing here; **this doc's `50df15b776ad5b0da93fe90cdee1163d` is the authoritative final file md5**
> (after the D-11e citation fold + compendium re-stamp — see D-11e). Matches the prior content-md5 convention
> (schema/stale-reclass migrations recorded content-md5, not file-md5, for the same reason). Restore = copy
> the backup over `corpus.db` (backup md5 `4a1ae47c…`).

---

## Execution order (per brief § "Execution order") — all applied in ONE transaction

1. Backup + pre-md5 guard (script asserts pre-md5 == `4a1ae47c…` or ABORT).
2. D-1 errata → D-7 annotations → D-3 mint stamps + accrual rows → D-4 docket ratify + § 5 consolidation
   → D-5 summoner flip → D-8 normalizations + D-11d.
3. D-11b drop cols → D-11c deprecate source_urls → D-11e citation fold (legolas absent → residue recorded).
4. D-11a create `kit_master` view → regenerate compendium from it → stamp md5.
5. D-10 v1.1 stamp + post-md5.

---

## D-1 — Blind-rider errata (4 kits) → ERRATA-56…59

Attestation-set corrections in `kit_mapping.mapping_json`. Elements/ailments live inside
`mapping_json.skills[]` (`element_primary` / `element_secondary` / `ailments[]`); there is no flat set
column, so the "attested set" is the union across skills (the D-11a `kit_master` view computes it live).
Additions are recorded WITHOUT overwriting mapper provenance: a `+element` uses a new
`attested_elements_errata` array on the skill (primary/secondary preserved); a `−element` nulls the
over-attested `element_primary`; a `+ailment` appends to the skill's `ailments[]`. **Grades unchanged**
(attestation completions, no grade-boundary crossings — confirmed per kit).

| ERRATA | kit_id | axis | before → after (attested set) | mechanism |
|---|---|---|---|---|
| **56** | `d2-avenger` | element | `{fire,lightning}` → `{fire,lightning,water}` | Vengeance `attested_elements_errata += water` (cold→water) |
| **57** | `le-runic-invocation` | element | `{lightning}` → `{fire,lightning,water}` | Runic Invocation `attested_elements_errata += fire,water` |
| **58** | `d2-ghost-pvp` | element | `{lightning,shadow}` → `{lightning}` | Mind Blast `element_primary shadow→null` (name-only over-attest struck) |
| **59** | `gd-bwc-demolitionist` | ailment | `{blind,curse:sap}` → `{blind,curse:sap,burn}` | Blackwater Cocktail `ailments += burn` (union) |

- **errata_applied counter:** 0 verify rows flipped for all 4 kits — none had a driving CONTRADICTED
  verify row on the corrected axis (these are blind-rider attestation completions / name-only strikes, the
  same no-flip annotation-class convention as ERRATA-53/55). `errata-ledger.md` is authoritative (D-8.3).
- **Verified in `kit_master` view (post-migration):** d2-avenger `fire,lightning,water`; d2-ghost-pvp
  `lightning`; gd-bwc-demolitionist ailments `blind,burn`; le-runic-invocation `fire,lightning,water`.
- Ledger entries appended: `errata-ledger.md` ERRATA-56…59 (git-tracked).

---

## D-7 — Kit-level annotations (`kit_mapping.deviation_notes`) — 7 items

All annotations on already-committed evidence; NO re-crawl, NO legolas. **Brief-shorthand kit_ids resolved
to actual corpus kit_ids** (see "Anchor-resolution ledger" below).

1. **`d2-wl-void-rift`** — keep-as-ghost annotation appended (kb-hallucination-class ghost; harvest FAILED
   all four families; retained as a documented negative; deletion is Matt-tier).
2. **`di-bombardment-wizard-pvp`** *(brief "di-bombardment")* — d3→di misapplication flag appended; kept
   (mapped identity is the attested DI one).
3. **`d4-spiritborn-vortex`** — component-class annotation appended; kept mapped (skill, not archetype).
4. **`di-spiritform-druid-pvp`** *(brief wrote "d2-spiritform-druid-pvp"; the DI-prefixed kit is the one
   carrying the negative flag + mis-specified-mechanic record — anchor resolved to `di-`)* — the
   mis-specified-mechanic negative claim RELABELED to its correct target (sustain-denial / CC-stack); kept.
5. **`le-harvest-lich`** — chimera SPLIT into **two** `deviation_notes` sub-entries (Harvest Flay → water +
   melee_arc; Death Seal Lich → DEFENSIVE_TRADEOFF), each citing the basin-2 dossier anchor. **Kit row stays
   one row** (Matt: "split at migration time, no legolas re-fire"; any true two-kit split defers to VDM-2 LE
   re-crawl). Verified: exactly 2 SUB-KIT entries present.
6. **`poe1-earthshatter`** — phantom alias `"Foulborn Ghostwrithe zerker(3.28)"` STRUCK (poe1-REVIEW-1
   resolved). The prior "correctly ignored" sentence was replaced with an explicit STRUCK record. Verified:
   old sentence gone (0), STRUCK present (1).
7. **`poe2-erasure-edc-lich`** *(brief "poe2-erasure")* — possible-phantom annotation KEPT; NO deletion
   (deletion is Matt-only). Also basin-qualified the sole DB-resident REVIEW token (D-8.2): the `mech_note`
   `"REVIEW-2, basin-1"` → `"b1-REVIEW-2 (basin-1)"`, and the referenced `"REVIEW-1 earthshatter"` →
   `"poe1-REVIEW-1 earthshatter"`.

All 7 kits carry a `D-7.*` tag in `deviation_notes` (verified).

---

## D-3 — Mint-all + three-tier evidence stamp (`mint_ledger`)

**(1) Columns added:** `evidence_tier TEXT CHECK(evidence_tier IN ('A-attested','B-quantitative',
'C-provisional'))` + `build_authorized INTEGER CHECK(build_authorized IN (0,1))`. Every mint row
`status='matt-ratified'`.

**(2a) 6 existing candidates stamped:**

| mint_id | mechanism | tier | build_authorized |
|---|---|---|---|
| 1 | chain fan-out >1.0 (quant) | B-quantitative | 1 |
| 2 | stack-parameterizes-geometry (GRADUATED-3) | A-attested | 1 |
| 3 | out-and-return path (6-kit family) | A-attested | 1 |
| 4 | temp-minion swarm ~20 (quant) | B-quantitative | 1 |
| 5 | placed-proxy (totem) count (quant) | B-quantitative | 1 |
| 6 | enemy-seeking mobile AoE (1 kit) | C-provisional | 0 |

**(2b) 6 NEW accrual-family rows promoted (mint_ids 7–12)**, each with mechanism text + forcing-kit list +
`ladder_step_audit='book§4-accrual …'`:

| mint_id | family | tier | build_auth | forcing kits (resolved) |
|---|---|---|---|---|
| 7 | two-tier-accumulator | **A-attested** | 1 | poe2-shaman-bear, poe2-walking-calamity, gd-cadence-witchblade, le-tempest-strike, le-runic-invocation, d3-raekor-boulder, d3-raiment-shenlong, d3-vyr-archon (≥3 independent kits → A) |
| 8 | roaming-persistent-AoE / twister | C-provisional | 0 | poe2-twister (~1) |
| 9 | HoWA attribute-total-as-flat-damage | C-provisional | 0 | poe2-howa-invoker, poe2-gemling-stacker (~1–2) |
| 10 | GD wandering-emitter | C-provisional | 0 | **none — descriptive anchor only** (see FLAG below) |
| 11 | GD enemy-attached-emitter | C-provisional | 0 | gd-stormbox-elementalist (~1) |
| 12 | GD proximity-armed-trigger | C-provisional | 0 | gd-roh-infiltrator (~1) |

- **Tier law honored:** A = qualitative primitive forced by ≥3 independent kits → build_authorized=1;
  B = numeric range-extension → build_authorized=1; C = qualitative primitive forced by 1–2 kits →
  build_authorized=0 (VDM-2 corroborate-or-drop watch-list). Final tier distribution: **A×3 · B×3 · C×6**.
- **R-M5 trigger-enum gaps** (`AUTOCAST_ON_MOVE`, `COMBO_BEAT_NTH`, `MINION_CONSUME`) left as recorded — NOT
  minted (enum gaps, not mints), per brief.
- **`mint_ledger` count: 6 → 12.**

> **⚑ FLAG (D-3 mint #10 anchor gap — reported, not guessed):** the review-book § 4 / brief accrual table
> names "GD wandering-emitter (**wind-devil**)" with forcing kit `wind-devil (~1)`. **No discrete corpus
> `kit_id` carries this pattern as its primary identity at map-time** — the GD Wind Devil (Druid/Elementalist
> wandering-emitter) was never decomposed into its own corpus row. Per HARD RULE 5 (report ambiguity, don't
> fabricate), I minted the row as ruled (C-provisional, build_authorized=0) but recorded `forced_by_kits=[]`
> with the descriptive anchor in `ladder_step_audit` rather than invent a kit_id. **The RULING (mint the GD
> wandering-emitter accrual at tier C) is preserved; only the forcing-kit anchor is honestly empty.** VDM-2
> should decompose the anchor kit if/when it materializes, then fold the kit_id in.

---

## D-4 — Docket ratifications + § 5 consolidation (`mechanic_gap_docket`)

**Columns added:** `disposition TEXT` + `docket_family TEXT`.

**(1+2+3) 8 original rows → `status='matt-ratified'` + disposition:**

| docket_id | mechanism | disposition | ruling |
|---|---|---|---|
| 1 | entity-as-consumable-resource-pool | engine-design-intake | D-4.2 mint-or-declare fork |
| 2 | ally-buff-projection (party-support) | permanent-gap-record | D-4.1 permanent gap (NOT a mint) |
| 3 | RNG-element-pool identity | permanent-gap-record | D-4.1 permanent gap |
| 4 | stun-magnitude-as-damage + perma-stunlock | engine-design-intake | D-4.2 declare-half; **collision-half → working-as-intended** (recorded in provenance_json — compound row, both halves ruled) |
| 5 | self-damage cost → proxy life-pool | permanent-gap-record | D-4.1 permanent gap |
| 6 | closed-loop self-damage vs MAX_CHAIN_DEPTH=1 | working-as-intended | D-4.3 intentional-guard collision (the guard IS the design) |
| 7 | world-entity-capture (spectres) | engine-design-intake | D-4.2 mint-or-declare fork |
| 8 | attribute→proxy-count (siege-ballista) | engine-design-intake | D-4.2 mint-or-declare fork |

> **Schema call (row 4 compound):** a single row holds one `disposition` column. Row 4 carries BOTH a
> declare-half (stun-magnitude-as-damage → engine-design-intake) and a collision-half (perma-stunlock floor
> / heavy-strike-stun → working-as-intended). I set `disposition='engine-design-intake'` (the mint-or-declare
> primary) and recorded the working-as-intended collision-half in `provenance_json.disposition_note`. **Both
> halves are ruled as Matt stated; only the single-column representation is my mechanism call** (brief
> authorizes schema judgment for the *mechanism*, never the *ruling*).

**(4) § 5.2 held-row consolidation → 11 canonical FAMILY rows (docket_ids 9–19)**, each
`status='matt-ratified'`, `mechanism_class='[§5.2 FAMILY] <name>'`, `destination='book-consolidation'`,
member-list in `spec_text_or_path` + `provenance_json.member_list`, `provenance='book§5.2-consolidation'`:

| docket_id | family | disposition |
|---|---|---|
| 9 | summoner-deferral (incl. army-GAP CotA/garg, ~23) | engine-design-intake *(flipped by D-5)* |
| 10 | stat-as-damage-substrate (6 DO-NOT-MERGE + accruals) | engine-design-intake |
| 11 | spatial-consumable-resource-node (7) | engine-design-intake |
| 12 | support-party-scope (LA cluster, 5) | permanent-gap-record |
| 13 | loot-economy-identity (4) | permanent-out-of-scope |
| 14 | mode-swap-identity (3) | hold |
| 15 | roguelite-idiom (hades1, 6) | permanent-genre-law-record |
| 16 | minion-consumption-harvest (2) | standing-family-record |
| 17 | recipe-combination-determines-output (2) | standing-family-record |
| 18 | gear-stat-as-minion-scaling (2) | standing-family-record |
| 19 | held-singletons (~17, 1-each) | hold |

- **stat-as-damage-substrate 6-way split kept INTACT** (DO-NOT-MERGE: armour-value · armor-conversion ·
  stun-substrate · block-chance · max-Mana→minion · missing-Mana→spell) — recorded verbatim in the row-10
  member list.
- **Side-files freeze as lineage** after ingest (D-11f inversion; the static
  `docket-candidates-batch-*.jsonl` remain in git as pipeline lineage).
- **`mechanic_gap_docket` count: 8 → 19.**

> **Schema call (§5.2 mechanism):** the 87 held rows were never ingested to `mechanic_gap_docket` (they lived
> as static side-files, TIER-2 HOLD). Per the brief's authorized latitude ("roll to family rows with member
> lists — your schema call"), I ingested the § 5.2 **family structure** as 11 canonical family rows carrying
> the member lists, rather than importing 87 individual rows. This makes the taxonomy the canonical docket
> surface (queryable, dispositioned) while preserving the member enumerations. The RULING (consolidate to the
> § 5.2 taxonomy, keep the stat-as-damage split) is preserved exactly.

---

## D-5 — Summoner un-deferral (disposition flip; NO kit re-mapping)

The **summoner-deferral family row** (docket_id 9) flipped **`deferred/Phase-5/evidence-bank` →
`matt-ratified` / `disposition='engine-design-intake'`** (Matt overturned the book's reaffirm-lean:
"amend deferral; based on the count of kits this can no longer be deferred"). Cross-linked in
`provenance_json` to `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md`
[RESOLVED 2026-07-06, Matt ruled Option 1 — build the summon-skill GENERATION path]; D-5 is the mapping-side
twin of that emission-side commit (mapped corpus summoners become validation targets for the built gen-path).

- **NO kit re-mapping.** The ~21 summoner GAPPED kits stay mapped-to-deferral in the VDM-1 snapshot (correct
  — the primitive did not exist at map-time). **0 `kit_mapping` rows touched by D-5.** Only the docket
  *disposition* changed.
- Verified: summoner-deferral row `disposition='engine-design-intake'`, `provenance_json.D5_crosslink` present,
  `D5_undeferral='deferred/Phase-5/evidence-bank -> matt-ratified / engine-design-intake'`.

---

## D-6 — No ailment-registry expansion (NO DB write)

No DB change (correct per brief). The 16-closed registry stands; the six no-home statuses are permanent
crosswalk footnotes in `2026-07-18-vdm1-crosswalks.md` § 8 (**gandalf-authored, already present — verified;
not my write**). Recorded here for the ledger: Shadow Daggers ≈ stack-payoff → D-3 two-tier mint territory
(routed to mint_id 7, not an ailment); Time Rot ≈ drain+chill compound.

---

## D-8 — Normalizations (+ D-11d)

1. **corpus_bucket duplicate Diablo tokens** → canonical short form: `diablo-3→d3` (1 row), `diablo-4→d4`
   (1 row), `diablo-immortal→di` (1 row). Post: no long-form tokens remain; d3=49, d4=46, di=24 (matches the
   per-game matrix exactly).
2. **REVIEW-numbering collision** → the **sole DB-resident** REVIEW token (`poe2-erasure-edc-lich.mech_note`)
   basin-qualified to `b1-REVIEW-2` (applied under D-7.7). The poe1-REVIEW-2 (poets-pen-vd) collision partner
   is **doc-only** (review rosters / errata-ledger), NOT in the DB — no bare ambiguous DB token existed.
3. **Errata bookkeeping law** (standing): `errata-ledger.md` authoritative; DB `errata_applied` counter
   subordinate, excludes policy-restamps. No numeric restamp needed this pass (D-1 errata flipped 0 verify
   rows — see D-1).
4. **D-11d `suffix_rekey_status`** → 107 `'awaiting-rekey'` rows normalized to `'complete-kit-mapping'` (the
   awaited re-key IS `kit_mapping`, now complete). `mob/elem` raws stay `'descriptor-final'` (were never
   'awaiting-rekey'). Post: 107 `complete-kit-mapping`, 478 `keyed-v1`.

---

## D-11 — One-representation consolidation

- **D-11a — `kit_master` VIEW + compendium regen.** Created the assembled VIEW: `canon_corpus` ⋈
  `kit_mapping` (grade, terminal, deviations) with **live-aggregated** `elements_attested` /
  `ailments_attested` (distinct union over `mapping_json.skills[]` incl. the D-1 `attested_elements_errata`),
  ⋈ citation aggregate (`citation_count` + `citations_json` = `{url,archive_url,site,author_handle,cite_class}`,
  **non-quarantined only**), ⋈ verify C/X/U tallies, ⋈ dossier row-count. **Row count = 574** (asserted).
  **Provenance-clean:** exposes NO mobile-era raw descriptors (`elem_raw`, suffix raws) — verified absent
  from view columns (D-11a + D-11f). Sanity-asserted the D-1 errata are reflected (avenger +water, ghost
  −shadow, bwc +burn). **Compendium regenerated FROM the view** (post-errata): 21 per-game `.md`
  (`kits-<game>.md`) + one `vdm1-compendium.jsonl` (574 kit lines + 1 meta line) + `README.md`, all stamped
  `v1.1-verified` + db md5 `6a9a6e5d…`, in `research/vdm1/compendium/`. Supersedes the 4 review rosters
  (which carry no citations).
- **D-11b — DROP dead columns.** Precondition re-asserted 0-populated (`motion_frame`=0, `t4_doors`=0,
  `option_c_substrate_flags`=0 across 585 rows), then `ALTER TABLE canon_corpus DROP COLUMN` each. Post:
  all 3 columns absent (verified via `pragma_table_info` + "no such column" on query). Zero data lost.
- **D-11c — deprecate `canon_corpus.source_urls`.** **Frozen, NOT dropped** (60 rows preserved). Deprecation
  recorded in `corpus_schema_meta` (`v1.1-deprecation-source_urls` row); `kit_citations` is the sole citation
  authority (0 kit-level orphan). Post: source_urls still present, 60 rows.
- **D-11d** — folded into D-8.4 above.
- **D-11e — citation orphan → CLOSED 574/574.** The legolas micro-fetch was ABSENT at migration-COMMIT time
  (573/574 residue recorded), but `agentic_orchestration/legolas/findings/vdm1-micro-ud-snowstorm-frost-2026-07-19.md`
  **LANDED during execution** and returned an **admissible** citation. Per HARD RULE 4, folded it into
  `kit_citations`: **2 authored citations** for `ud-snowstorm-frost` — (1) `pockettactics.com` (author
  @Connor Christie; verbatim anchor explicitly naming the "snowstorm" skill-rune as cold-element) as the
  primary admissible cite; (2) `youtube.com/watch?v=RZsbOkPf_Fg` (dedicated "Frost Storm" S11 build-guide
  video; author_handle not extractable). Both `cite_class='authored'`, `rank_class='recovered'`,
  non-quarantined. **Coverage 573 → 574/574; 0 orphan.** Fold ran in its own transaction (integrity ok, FK
  clean, coverage asserted 574) against a second backup (`corpus.db.pre-ud-snowstorm-citation-…`, md5
  `6a9a6e5d…`); the compendium was **regenerated** from the view (now rendering the 2 cites) and re-stamped
  (final md5 `50df15b776ad5b0da93fe90cdee1163d`). The `v1.1-verified` schema_meta note records the fold.
- **D-11f — inversion.** `kit_master` reads truth from the normalized tables (mapping + citations + verify +
  dossier), NEVER from frozen raws (verified: no raw descriptor columns in the view). The declaring README at
  `research/vdm1/` is gandalf-authored (this batch — not my write); I authored only the compendium's own
  `README.md` (provenance stamp + index).

---

## D-10 — Corpus v1.1 stamp

`corpus_schema_meta` stamped **`v1.1-verified`** (applied_utc `2026-07-19T20:04:46Z`) + a
`v1.1-deprecation-source_urls` row. Post-migration md5 recorded in the meta table (as the pre-final-stamp
content checksum `cb51101d…` with a self-documenting fixpoint note + the D-11e fold note) AND here (TRUE
final file md5 `50df15b776ad5b0da93fe90cdee1163d`, post citation-fold). Tracker writes are gandalf-side,
post-verify.

---

## Pre/post state

| Table / object | Before | After | Delta |
|---|---|---|---|
| `kit_mapping` rows | 574 | 574 | 0 (errata are in-row edits) |
| `kit_mapping` grade histogram | E53/C347/A88/G86 | E53/C347/A88/G86 | unchanged (no grade re-derivation) |
| `mint_ledger` rows | 6 | 12 | +6 (accrual families) |
| `mint_ledger` new columns | — | evidence_tier, build_authorized | +2 |
| `mechanic_gap_docket` rows | 8 | 19 | +11 (§5.2 family rows) |
| `mechanic_gap_docket` new columns | — | disposition, docket_family | +2 |
| `canon_corpus` rows | 585 | 585 | 0 |
| `canon_corpus` columns | (incl. 3 dead) | (3 dropped) | −3 (motion_frame, t4_doors, option_c_substrate_flags) |
| `corpus_schema_meta` rows | n | n+2 | +2 (v1.1-verified + source_urls-deprecation) |
| `kit_master` VIEW | absent | present, 574 rows | NEW |
| `kit_citations` rows | 1285 | 1287 | +2 (D-11e ud-snowstorm-frost fold) |
| `verify_ledger` rows | 2068 | 2068 | 0 |
| `kit_dossier` rows | 3444 | 3444 | 0 |
| citation coverage (mapped kits, non-quar) | 573/574 | **574/574** | +1 (D-11e orphan CLOSED) |

---

## Anchor-resolution ledger (brief shorthand → actual corpus kit_id)

Recorded for the verify battery. These are anchor RESOLUTIONS (finding the real kit_id), NOT ruling changes.

| brief shorthand | resolved kit_id | note |
|---|---|---|
| D-7.2 `di-bombardment` | `di-bombardment-wizard-pvp` | the DI kit (not `d3-lon-bombardment`); matches the d3→di flag |
| D-7.4 `d2-spiritform-druid-pvp` | `di-spiritform-druid-pvp` | **brief prefix typo `d2-`→`di-`**; the DI kit carries the negative flag + mis-specified-mechanic record (ERRATA-53 lineage); ruling unambiguous, applied to the DI kit |
| D-7.7 `poe2-erasure` | `poe2-erasure-edc-lich` | poe2 EDC Lich |
| D-3#7 accrual (two-tier) | 8 kit_ids | poe2-shaman-bear, poe2-walking-calamity, gd-cadence-witchblade, le-tempest-strike, le-runic-invocation, d3-raekor-boulder, d3-raiment-shenlong, d3-vyr-archon |
| D-3#8 accrual (twister) | `poe2-twister` | (also `d3-dmo-twister` exists; § 5.2 singleton = poe2) |
| D-3#9 accrual (HoWA) | `poe2-howa-invoker`, `poe2-gemling-stacker` | |
| D-3#10 accrual (wind-devil) | **NONE** | no discrete corpus kit_id — descriptive anchor only (see D-3 FLAG) |
| D-3#11 accrual (stormbox) | `gd-stormbox-elementalist` | |
| D-3#12 accrual (rune-of-hagarrad) | `gd-roh-infiltrator` | folk_name "Rune of Hagarrad Infiltrator" |

---

## Verification (final state)

- `PRAGMA integrity_check` = **ok** (pre-commit AND final)
- `PRAGMA foreign_key_check` = **clean** (0 rows, pre-commit AND final)
- `PRAGMA journal_mode` = **delete**
- Pre-md5 guard: `4a1ae47c…` == chain-head — **PASS** (else ABORT)
- R-M7 biconditional: GAPPED (86) == MAPPED_DOCKET (86) — **PASS** (invariant; unchanged)
- `kit_mapping` rows == 574 — **PASS**
- D-1: 4 errata reflected in `kit_master` view — **VERIFIED** (avenger +water, ghost −shadow, bwc +burn, runic +fire+water)
- D-7: all 7 kits carry D-7 tag; earthshatter alias struck (old gone, STRUCK present); harvest-lich = 2 sub-kit entries — **VERIFIED**
- D-3: mint_ledger 6→12; tiers A×3/B×3/C×6; all status='matt-ratified' — **VERIFIED**
- D-4: docket 8→19; 8 original matt-ratified + dispositioned; 11 family rows; stat-as-damage 6-way intact — **VERIFIED**
- D-5: summoner-deferral flipped to engine-design-intake + crosslink; 0 kit re-maps — **VERIFIED**
- D-8.1: no long-form Diablo buckets; d3=49/d4=46/di=24 — **VERIFIED**
- D-11b: 3 dead columns dropped (0-populated precondition asserted) — **VERIFIED**
- D-11c: source_urls frozen (60 rows), not dropped — **VERIFIED**
- D-11d: 107 awaiting-rekey → complete-kit-mapping — **VERIFIED**
- D-11a: kit_master view = 574 rows, provenance-clean (no raw descriptors) — **VERIFIED**
- D-11e: citation coverage **574/574** — ud-snowstorm-frost orphan CLOSED (legolas micro-fetch landed during
  execution; 2 authored cites folded, 0 orphan) — **VERIFIED**
- Grade histogram unchanged E53/C347/A88/G86 — **VERIFIED**
- Compendium: 21 per-game .md + 1 jsonl (575 lines = 574+meta) + README, md5-stamped `50df15b7…` — **GENERATED (re-stamped post-fold)**

---

## Anomaly log

1. **md5 fixpoint (D-10):** stamping post-md5 into the DB changes the file md5 (self-reference). Resolved by
   recording the pre-stamp content checksum in-DB with a self-documenting note; the TRUE final file md5
   `6a9a6e5d…` is authoritative here. Not an error — inherent + honestly documented (matches prior
   content-md5 convention).
2. **D-3 mint #10 (GD wandering-emitter) has no forcing kit_id** — the corpus never decomposed the GD Wind
   Devil into its own row. Minted as ruled (C-provisional) with an empty `forced_by_kits` + descriptive
   anchor. Reported (not guessed); ruling preserved. **Flagged to steward.**
3. **D-7.4 brief prefix typo** (`d2-spiritform-druid-pvp` → actual `di-spiritform-druid-pvp`). Anchor
   resolved to the DI kit that carries the negative; ruling unambiguous. **Flagged to steward.**
4. **D-11e citation landed mid-execution.** The legolas micro-fetch was absent at COMMIT (573/574 recorded)
   but landed before finalization; folded in a follow-on transaction per HARD RULE 4 (573→574/574). This is
   the expected "trailing one-row fold" the brief anticipated — not an anomaly, but noted for the md5 chain
   (final md5 moved `6a9a6e5d…` → `50df15b7…`).

No other anomalies. All assertions passed on first execution; both transactions committed clean.

---

## Reproducibility + reversibility

- **Inputs static** (committed): the migration script, the compendium-gen script, and all brief/authority
  docs. Both scripts are deterministic against the chain-head DB.
- **Full restore** = copy `corpus.db.pre-review-ratification-20260719T200446Z` over `corpus.db` (backup md5
  `4a1ae47c7ded48f6443780602eb7e8ea`).
- **Reversibility of errata:** D-1 additions are recorded via new fields (`attested_elements_errata`) /
  additive appends without overwriting mapper provenance; the raw mapper `element_primary`/`secondary` and
  original deviation text are preserved (per elrond reversibility principle — no silent destructive
  transformation).
- **Compendium re-gen** is a one-command read-only regenerate; trivially re-runs if the D-11e citation lands.

---

## ADR-004

No engine-telemetry change; star-lord-side `MIGRATION.md` unaffected (all writes are elrond-seam corpus
curation on `corpus.db`). No cross-seam migration request. Auto-committed per project discipline (Matt-
authorized VDM-1 charge) — but per the brief, **elrond does NOT git-commit**; the steward (gandalf) does the
single pathspec commit after an independent read-only verify battery. **NO push.**

## Commit note (for the steward)

Pathspec-only (steward commits): this MIGRATION doc · `errata-ledger.md` (ERRATA-56…59) ·
`research/vdm1/compendium/` (21 .md + 1 .jsonl + README) · the two scripts
(`vdm1_migration_post_review_2026_07_19.py`, `vdm1_compendium_gen_2026_07_19.py`). `corpus.db` is gitignored
and NOT committed; the backup + md5 sidecar stay on disk (uncommitted). The 4 review rosters are superseded
by the compendium but retire to git as review artifacts (steward's call on their disposition at review close).
