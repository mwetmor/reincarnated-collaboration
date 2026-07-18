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

---

## ERRATA-2 — poe1-deaths-oath era floor correction (2.x -> 1.x)

- **kit_id:** `poe1-deaths-oath`
- **field:** `canon_corpus.eras`
- **old -> new:** `2.x;3.0-3.6;3.7-3.13` -> `1.x;3.0-3.6;3.7-3.13`
- **verdict:** CONTRADICTED (batch-03 verify, `era` claim family)
- **batch:** 03
- **date applied:** 2026-07-18 (ingest wave 2)
- **verify_ledger:** `errata_applied=1` set on the ingested deaths-oath `era` row.
- **provenance note:** deaths-oath is EXCLUDED from this wave's `fact_provenance`
  promotion (it carried a CONTRADICTED era; only clean kits promote to
  `verified-v1.1`). Its 10 probe facts remain `kb-legacy`.
- **source anchor (verbatim):** "Death's Oath question … DoT mechanics? [thread
  dated November 26, 2013, version 1.0.2]" — pathofexile.com/forum/view-thread/651516.
- **adjudication:** The stamped floor bucket was `2.x`. The anchor is a
  **November 26, 2013** forum thread discussing the Death's Oath item under
  **version 1.0.2** — v1.0.2 falls in the **1.x** patch band. The item (and thus
  the build) was attested and in play at 1.0.2, one band earlier than the stamped
  2.x floor. The anchor supports extending the floor DOWN to `1.x`. Corrected the
  first bucket `2.x` -> `1.x`; the remaining buckets (`3.0-3.6`, `3.7-3.13`) are
  untouched. Corroborated by the citation stream (batch-03-citations line 3: forum
  thread "Death's Oath + 1.0.2 DoT mechanics? (Forum thread, Nov 2013)").
- **not-corrected fields:** none. Only the patch-band `eras` floor bucket changed.
  The `3.7-3.13` bucket token remains intact, so this kit STAYS in the stage-3
  bucket-audit register (see MIGRATION-vdm1-ingest2 § bucket-audit).

---

## ERRATA-3 — poe1-generals-cry era floor correction (3.7 -> 3.11 within bucket)

- **kit_id:** `poe1-generals-cry`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.7-3.13;3.20+` -> `3.11-3.13;3.20+`
- **verdict:** CONTRADICTED (batch-04 verify, `era` claim family)
- **batch:** 04
- **date applied:** 2026-07-18 (ingest wave 2)
- **verify_ledger:** `errata_applied=1` set on the ingested generals-cry `era` row.
- **provenance note:** generals-cry is EXCLUDED from this wave's promotion (carried
  a CONTRADICTED era). Its 10 probe facts remain `named-source-unfetched`.
- **source anchor (verbatim):** "General's Cry was added in patch 3.11.0. Era
  bucket 3.7-3.13 has floor 3.7 but skill did not exist until 3.11 within that
  bucket." — poedb.tw/us/Generals_Cry.
- **adjudication:** Same shape as ERRATA-1 (crackling-lance): the skill debuted at
  patch **3.11.0**, inside the `3.7-3.13` bucket. The build cannot have been meta
  during 3.7-3.10. The bucket floor is narrowed from `3.7` to the debut patch
  `3.11`, yielding `3.11-3.13`. The later `3.20+` bucket is untouched. This narrows
  generals-cry OUT of the literal `3.7-3.13` bucket token, so it LEAVES the
  stage-3 bucket-audit register (register 52 -> 50 for the corrected state).

---

## ERRATA-4 — poe1-hexblast-mines era floor correction (3.7 -> 3.12 within bucket)

- **kit_id:** `poe1-hexblast-mines`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.7-3.13;3.20+` -> `3.12-3.13;3.20+`
- **verdict:** CONTRADICTED (batch-04 verify, `era` claim family)
- **batch:** 04
- **date applied:** 2026-07-18 (ingest wave 2)
- **verify_ledger:** `errata_applied=1` set on the ingested hexblast-mines `era` row.
- **provenance note:** hexblast-mines is EXCLUDED from this wave's promotion (carried
  a CONTRADICTED era). Its 10 probe facts remain `kb-legacy`.
- **source anchor (verbatim):** "Added a new Intelligence Skill Gem - Hex Blast:
  Deals chaos damage to a targeted enemy... [introduced in 3.12.0 Heist patch
  notes]. Era bucket floor 3.7 predates skill introduction by 5 patches." —
  pathofexile.com/forum/view-thread/2935777 (GGG 3.12.0 Heist patch notes).
- **adjudication:** Hexblast was introduced in patch **3.12.0 (Heist)** — the same
  league as crackling-lance (ERRATA-1). The `3.7-3.13` bucket floor of 3.7 predates
  the skill by 5 patches. Narrow the bucket floor from `3.7` to the debut `3.12`,
  yielding `3.12-3.13`. The `3.20+` bucket is untouched. Narrows hexblast-mines OUT
  of the literal `3.7-3.13` bucket token, so it LEAVES the stage-3 bucket-audit
  register.

---

## REVIEW-1 — poe1-earthshatter phantom alias "Foulborn Ghostwrithe zerker(3.28)" (UNADJUDICATED)

- **kit_id:** `poe1-earthshatter`
- **field:** `canon_corpus` alias text carried in the identity claim (via the folk
  alias listed in the earthshatter `identity` verify row + the mobile-harvest alias
  surface). Present in verify_ledger as: identity claim_text "…alias 'Foulborn
  Ghostwrithe zerker(3.28)' for Berserker class".
- **status:** REVIEW — **unadjudicated. NO data change this wave.** Needs steward
  (gandalf) / Matt eyes.
- **batch:** 03
- **date noted:** 2026-07-18 (ingest wave 2)
- **observation:** batch-03's crawl COULD NOT locate the alias string "Foulborn
  Ghostwrithe zerker(3.28)" in ANY fetched source. The earthshatter identity verdict
  is CONFIRMED overall — the anchor ("[3.27] Earthshatter Berserker Build … [3.11]
  Earthshatter - Berserker, Max Rage", poedb.tw/us/Earthshatter) confirms the
  Earthshatter/Berserker build identity, but does NOT attest this specific alias.
  "Ghostwrithe" is a real PoE unique (chest armour, 3.16 Scourge) and "3.28" would
  be a post-cutoff patch band; the compound "Foulborn Ghostwrithe zerker" reads like
  a build-specific coinage that no located guide carries. It may be a hallucinated
  or mis-transcribed alias from the original mobile-harvest, or a genuine niche
  community label that the crawl's source set simply did not reach.
- **why not deleted:** the no-silent-edits law forbids removing the alias on a mere
  not-found. SOURCE-NOT-FOUND is honest silence, not a contradiction — the alias is
  NOT disproven, only un-located. Deleting it would destroy a datum that a later,
  wider crawl might attest. Preserved verbatim; flagged here for adjudication.
- **recommended action for steward/Matt:** either (a) a targeted re-crawl to attest
  or refute the alias, or (b) a ruling to demote/strike it if judged a harvest
  artifact. Until then it stays in the corpus unchanged. Note: earthshatter's `era`
  row is CONFIRMED and its eras (`3.7-3.13;3.20+`) are NOT touched this wave, so
  earthshatter REMAINS in the stage-3 bucket-audit register (its stamp still floors
  the 3.7-3.13 bucket though the skill debuted 3.11 — a soft register-candidate the
  dispatch explicitly excluded from correction this wave).
