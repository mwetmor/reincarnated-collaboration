# VDM-1 Errata Ledger

**Append-only.** Charter law: no silent edits. Every correction to `canon_corpus`
(or any authored field) driven by a VDM-1 verification verdict is recorded here
with kit_id, field, old -> new, source anchor, and originating batch. Soft-flags
(plausible-but-skewed stamps, no data change) are recorded as `SOFT-FLAG` rows.

Steward: elrond (single writer, corpus.db). Run: vdm1.

---

## ERRATA-1 — poe1-crackling-lance era correction

- **kit_id:** `poe1-crackling-lance`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.7-3.13` -> `3.12-3.13`
- **verdict:** CONTRADICTED (batch-02 verify, `era` claim family)
- **batch:** 02
- **date applied:** 2026-07-18
- **verify_ledger:** `errata_applied=1` set on the ingested crackling-lance `era` row.
- **provenance note:** crackling-lance is EXCLUDED from this wave's
  `fact_provenance` promotion (it carried a CONTRADICTED era; only clean kits
  promote to `verified-v1.1`).
- **source anchor:** Crackling Lance was introduced in patch **3.12.0 (Heist
  league, September 2020)**. It cannot have been meta during 3.7-3.11. The
  correct attestable era is 3.12-3.13 at minimum (extends 3.20+ per guide
  titles). Introduction confirmed by mmogah.com and the pathofexile.com/forum
  patch announcement; multiple guide titles explicitly dated 3.12. The era
  coarse-prior flag (.85) set in the search spec — the contradiction is a
  prior-risk materializing, not a novel discovery.
- **not-corrected fields:** `era_year` (=2013) is a separate mint-era attribute
  unrelated to the PoE patch band; left untouched. Only the patch-band `eras`
  field was stamped "3.7-3.13" and is corrected.

---

## SOFT-FLAG-1 — poe1-aurastacker era (plausible, skewed later; NO data change)

- **kit_id:** `poe1-aurastacker`
- **field:** `canon_corpus.eras` (value `3.7-3.13`)
- **status:** SOFT-FLAG — plausible stamp, NOT contradicted. **No data change.**
- **batch:** 01
- **date noted:** 2026-07-18
- **verdict:** era CONFIRMED (the build existed in the stamped band).
- **observation:** Best recovered guide (Jix, forum thread 2913007) is labeled
  **3.18** (title "3.18 READY", references "3.17 READY"), which falls in
  `3.14-3.19`. The Aul's Uprising unique (core to the archetype) was added in
  patch **3.10 (Delirium)**, within the stamped `3.7-3.13` band — so the build
  genuinely existed from ~3.10. Assessment: the stamp `3.7-3.13` is plausible
  (build existed) but the peak/canonical guide era skews later (3.14-3.19). The
  stamp may be understated at the low end and short at the high end. Recorded as
  a soft-flag for future era-refinement work; no correction applied this wave.
