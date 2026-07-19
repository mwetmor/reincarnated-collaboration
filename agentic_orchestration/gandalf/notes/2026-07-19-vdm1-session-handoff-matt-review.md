# VDM-1 SESSION HANDOFF — run CLOSED, awaiting Matt's margins (2026-07-19)

**Author:** gandalf (steward) · **For:** the next gandalf session (any model seat). Read this first; act only on Matt's margins.

---

## 1. State in one paragraph

VDM-1 is **complete**: 574/574 kits crawled + verified + dossiered + mapped + ingested across 5 basins / 21 games; Stage-5 blind rider PASSED (no systematic bias; ~95% element / ~97% ailment right-or-defensible); **THE REVIEW BOOK authored + presented** (`research/vdm1/REVIEW-BOOK.md`, commit `f3541ba7`) then **amended with D-11** (`d2912005`). Red-flag ledger **EMPTY** — zero pings across the autonomous span. `corpus.db` post-INGEST-18 (md5 `4a1ae47c…`), kit_mapping = 574. Tasks #6–15 all completed. **The run waits on exactly ONE thing: Matt's margins on the eleven rulings (book § 2, D-1…D-11). NOTHING is applied until they land.**

## 2. Delta since the book was presented (this is the part not yet in the run ledger)

Matt asked mid-review for **one representation per kit — the most complete version, with URL + authorship citations**. Steward ran a readonly consolidation audit of every representation layer vs `corpus.db` and appended **D-11** to the book's decision surface (six sub-rulings, each with a lean). The memo in five lines:

1. **Horizontal duplication does NOT exist** — 0 same-game folk-name collisions; `kit_id` is PK; 585 distinct rows. The felt problem is **vertical** (kit truth spans `canon_corpus` ⊕ `kit_dossier` ⊕ `verify_ledger` ⊕ `kit_citations` ⊕ `kit_mapping`; no existing view joins mapping + citations), **temporal** (D-1 errata pending), and **mobile-harvest schema residue**.
2. Citations are near-total: **573/574** kits ≥1 live citation (avg 2.2; 385 with `author_handle`); sole orphan = `ud-snowstorm-frost`.
3. Dead parallel columns confirmed: `canon_corpus.motion_frame`/`t4_doors`/`option_c_substrate_flags` = **0 populated** (pre-VDM-1 Layer-3 plan superseded by `kit_mapping`); `canon_corpus.source_urls` (60 rows) **fully redundant** with `kit_citations`.
4. The fix: **one truth STORE (normalized DB) + one assembled REPRESENTATION (`kit_master` view → regenerated citation-bearing compendium) + demotions** (drop dead columns, deprecate `source_urls`, rosters retire post-review).
5. **The inversion rule (D-11f):** files governed during the run; at the v1.1 stamp authority inverts — **DB + compendium govern; every `stage*/` jsonl freezes as immutable lineage**, declared in a `research/vdm1/` README.

**Model-seat note:** the book was authored on fable-5 per the discharged model-gate. Matt's later `/model claude-fable-4-8` switch FAILED ("not found"). **No model requirement remains** — post-ratification execution is mechanical and runs on any seat.

## 3. EXECUTION RECIPE when margins land (ONE elrond migration + ONE steward commit)

Per-ruling mechanics (fire only the ratified ones; a contested lean → re-adjudicate from committed dossier/verify anchors, then fold):

| Ruling | If ratified → do |
|---|---|
| **D-1** | 4 `kit_mapping.mapping_json` errata (d2-avenger +water · le-runic-invocation +fire+water · d2-ghost-pvp −shadow · gd-bwc-demolitionist +burn) → log as **ERRATA-56…59** in `errata-ledger.md` with the book's anchor citations |
| **D-2** | crosswalk-law footnotes (Paralysis→`shock` rule · cold≠chill/freeze stays strict · summoner-kits element-silent) → amend `design-inputs/2026-07-18-vdm1-crosswalks.md`; **no DB write** |
| **D-3/D-4** | `mint_ledger` (6) + `mechanic_gap_docket` (8) status → `matt-ratified`; consolidate the 87 held side-file candidates per book § 5 family taxonomy (elrond ingests the ratified consolidation; side-files then freeze as lineage) |
| **D-5/D-6** | no-op records (summoner-deferral reaffirmed; no ailment-registry expansion) — note in ledger close-out only |
| **D-7** | seven kit-level `deviation_notes` annotations (void-rift · bombardment · spiritborn-vortex · spiritform · harvest-lich · earthshatter · Erasure) per book § 2 D-7 text |
| **D-8** | three DB normalizations (per book D-8) **+ D-11d** `suffix_rekey_status` normalization (107 'awaiting-rekey' → moot) |
| **D-9** | citation export **ONLY IF** `canonical/matt_decision_needed/2026-07-13-ip-clearance-devlog-and-hook-surface.md` is also ruled; else stays gated |
| **D-10** | `v1.1-verified` stamp in `corpus_schema_meta` + tracker writes from the pre-drafted lines in book § 10 (serial-content + engine trackers) |
| **D-11** | `kit_master` VIEW (identity ⋈ mapping ⋈ citation-aggregate ⋈ verify tallies ⋈ dossier count) · compendium generator + regen (per-game `.md` + one `.jsonl`, stamped md5+v1.1) · DROP 3 dead columns · deprecate `source_urls` · legolas micro-fetch for `ud-snowstorm-frost` (→574/574 cited) · inversion README at `research/vdm1/` · 4 review rosters retire to git |

**Order:** elrond migration (all DB items, one MIGRATION doc) → steward D-2c-style verify battery (readonly recount; advisory never trusted) → compendium regeneration → steward commit (pathspec-only) + push → tracker writes (D-10) → run-state ledger close-out bullet → prune pass (rosters + accumulators to git per doc-lifecycle § 6.3).

## 4. Reading order for the fresh session

1. **This file.** 2. **`REVIEW-BOOK.md` § 2** + wherever Matt's margins are (inline edits, a reply doc, or verbal — take them in any form). 3. Run-state ledger `notes/2026-07-18-vdm1-run-state.md` for deep history *only as needed*. Do NOT re-derive anything; book + errata-ledger + DB are the state.

## 5. What is lost / not lost at session boundary

**Not lost:** every ruling, lean, count, and anchor — all committed. **Lost:** warm in-context familiarity with individual kits — irrelevant for mechanical execution, and if a margin contests a lean, the committed dossier + verify anchors exist precisely so any session can re-adjudicate from evidence.

---

**Signed:** gandalf (steward) · session handoff at the Matt-review boundary · the run's paper trail was built so this handoff costs nothing.
