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

---

## ERRATA-5 — poe1-icicle-mines era floor correction (3.7 -> 3.8 within bucket)

- **kit_id:** `poe1-icicle-mines`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.7-3.13` -> `3.8-3.13`
- **verdict:** CONTRADICTED (batch-05 verify, `era` claim family)
- **batch:** 05
- **date applied:** 2026-07-18 (ingest wave 3)
- **verify_ledger:** `errata_applied=1` set on the ingested icicle-mines `era` row.
- **provenance note:** icicle-mines is EXCLUDED from this wave's `fact_provenance`
  promotion (it carried a CONTRADICTED era). Its 10 probe facts remain legacy
  (verified 0 `verified-v1.1`).
- **source anchor (verbatim):** "Icicle Mine was introduced in patch 3.8.0
  (originally as 'Freeze Mine,' which was completely reworked and renamed)" —
  poedb.tw/us/Icicle_Mine.
- **adjudication:** Same shape as ERRATA-1/3/4 (debut-inside-bucket). The skill
  debuted at patch **3.8.0**, inside the `3.7-3.13` bucket. The build cannot have
  been meta during 3.7 (the sole patch below the debut in-bucket). Narrow the
  bucket floor from `3.7` to the debut `3.8`, yielding `3.8-3.13`. The identity
  (Saboteur Icicle Mine build) and mechanics (throw-and-detonate mine, converging
  icicle volleys) are both CONFIRMED and untouched.
- **not-corrected fields:** none. Only the patch-band `eras` floor bucket changed.
  Note the DB `era_year` (=2013) is a separate mint-era artifact, left untouched
  on this kit (only kinetic-fusillade's era_year was rekeyed this wave — ERRATA-9).

---

## ERRATA-6 — poe1-lightning-conduit era floor correction (3.14 -> 3.19 within bucket)

- **kit_id:** `poe1-lightning-conduit`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.14-3.19;3.20+` -> `3.19;3.20+`
- **verdict:** CONTRADICTED (batch-05 verify, `era` claim family)
- **batch:** 05
- **date applied:** 2026-07-18 (ingest wave 3)
- **verify_ledger:** `errata_applied=1` set on the ingested lightning-conduit `era` row.
- **provenance note:** EXCLUDED from promotion (carried a CONTRADICTED era). 10
  probe facts remain legacy.
- **source anchor (verbatim):** "Lightning Conduit was introduced in patch 3.19.0
  (Lake of Kalandra). Three new skill gems themed around lightning damage and
  shock" — poe-vault.com/guides/lake-of-kalandra-league-new-skill-gems.
- **adjudication:** The skill debuted at patch **3.19.0 (Lake of Kalandra)**, at
  the very top of the `3.14-3.19` bucket. The bucket floor 3.14 predates the skill
  by five patches; the only attestable in-bucket patch is 3.19 itself. Narrow the
  `3.14-3.19` bucket to the single debut patch `3.19`, yielding `3.19;3.20+`
  (the collapsed single-patch token `3.19` denotes the debut patch alone; the
  `3.20+` bucket is untouched). Convention note: where a debut lands on the
  top-most patch of a wide bucket, the bucket collapses to that single patch token
  rather than a `X-Y` range (contrast ERRATA-5/7 where the debut is mid-bucket and
  a residual range remains).

---

## ERRATA-7 — poe1-pconc era floor correction (3.14 -> 3.16 within bucket)

- **kit_id:** `poe1-pconc`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.14-3.19;3.20+` -> `3.16-3.19;3.20+`
- **verdict:** CONTRADICTED (batch-05 verify, `era` claim family)
- **batch:** 05
- **date applied:** 2026-07-18 (ingest wave 3)
- **verify_ledger:** `errata_applied=1` set on the ingested pconc `era` row.
- **provenance note:** EXCLUDED from promotion (carried a CONTRADICTED era). 10
  probe facts remain legacy.
- **source anchor (verbatim):** "Poisonous Concoction was introduced in patch
  3.16.0 Scourge League, described as a new Dexterity Skill Gem" —
  poedb.tw/us/Poisonous_Concoction.
- **adjudication:** The skill debuted at patch **3.16.0 (Scourge)**, inside the
  `3.14-3.19` bucket. The bucket floor 3.14 predates the skill by two patches.
  Narrow the bucket floor from `3.14` to the debut `3.16`, yielding
  `3.16-3.19;3.20+`. The `3.20+` bucket is untouched. Same league as ERRATA-8's
  positive-evidence window (Scourge 3.16), an independent corroboration that 3.16
  is the correct floor for skills of that cohort.

---

## ERRATA-8 — poe1-seismic-trap DROP unattested 3.7-3.13 bucket (distinct root-cause class)

- **kit_id:** `poe1-seismic-trap`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.7-3.13;3.14-3.19` -> `3.14-3.19`
- **verdict:** CONTRADICTED (batch-06 verify, `era` claim family) on the 3.7-3.13
  bucket; corroborated by a paired CONFIRMED positive-evidence `era` row on the
  3.14-3.19 bucket (both rows landed in verify_ledger via the batch-06 granular
  one-row-per-band split).
- **batch:** 06
- **date applied:** 2026-07-18 (ingest wave 3)
- **verify_ledger:** `errata_applied=1` set on the ingested seismic-trap 3.7-3.13
  `era` CONTRADICTED row (exactly one such row; the 3.14-3.19 CONFIRMED row is NOT
  flagged).
- **provenance note:** EXCLUDED from promotion (carried a CONTRADICTED era). 10
  probe facts remain legacy.
- **DISTINCT ROOT-CAUSE CLASS:** **"patch-buff-seeded stamp, no adoption evidence."**
  This is NOT the debut-inside-bucket class of ERRATA-1/3/4/5/6/7. Seismic Trap
  **existed since patch 3.3.0** — so the skill predates the entire `3.7-3.13`
  bucket and a naive debut-floor correction would WRONGLY keep the bucket (the
  skill was present). But *presence of the skill* is not *presence of the build in
  meta*. The crawl found **no guide, thread, or attestation** of a Seismic Trap
  meta build during 3.7-3.13; the earliest confirmed meta is **3.16 (Scourge)**,
  with 3.16 and 3.18 forum guides anchoring the 3.14-3.19 window. A 3.13-era
  patch-buff to the skill most plausibly **seeded the era stamp** in the original
  mobile-harvest (a data-entry inference from "buffed in 3.13" to "meta in
  3.7-3.13") **without any adoption evidence**. The correction therefore DROPS the
  entire unattested `3.7-3.13` bucket rather than narrowing its floor, leaving only
  the attested meta window `3.14-3.19`.
- **source anchors (verbatim):**
  - CONTRADICTED: "Seismic Trap introduced 3.3.0; all found meta guides begin at
    3.16 (Scourge). No guide or attestation found for 3.7-3.13 meta. Earliest
    confirmed meta is 3.16+." — poedb.tw/us/Seismic_Trap.
  - CONFIRMED (positive, 3.14-3.19): "'[3.16] Seismic/Exsanguinate Trap Build |
    Saboteur | Scourge' forum post; '[3.18] Seismic Trap / Exsanguinate Saboteur'
    guide confirm 3.16-3.18 active" — pathofexile.com/forum/view-thread/3179858.
- **register effect:** dropping the `3.7-3.13` bucket removes the literal token,
  and the corrected floor becomes `3.14-3.19` — seismic-trap is now floored in the
  `3.14-3.19` bucket. It is individually verified this wave regardless, so it is
  NOT a stage-3 register member.
- **methodology note for stage-3:** this class ("skill present but build unattested
  in a stamped band") is distinct from debut-floor errata and is likely to recur.
  The discriminator is: *does the skill's debut predate the bucket?* If YES and the
  bucket is still unattested, suspect a patch-buff-seeded stamp and require positive
  meta evidence for EACH stamped band, not just skill existence. Recommend stage-3
  apply this test to every multi-band PoE1 stamp.

---

## ERRATA-9 — poe1-kinetic-fusillade era_year rekey (2013 -> 2024; NON-eras column)

- **kit_id:** `poe1-kinetic-fusillade`
- **field:** `canon_corpus.era_year` (NOT `eras` — a distinct mint/introduction-year
  column)
- **old -> new:** `2013` -> `2024`
- **verdict:** the `era` verify row is **CONFIRMED** (stamped `3.20+` is correct;
  Kinetic Fusillade was added in version 3.27.0, which is in the 3.20+ band). The
  era_year=2013 is a **bulk-fill artifact** (every kit in batches 05/06 carries the
  identical placeholder 2013 in `era_year`), not a verified value. This errata
  corrects the artifact; it does NOT touch `eras`.
- **batch:** 05
- **date applied:** 2026-07-18 (ingest wave 3)
- **verify_ledger:** **NO `errata_applied` flag set.** The `errata_applied=1`
  convention is reserved for CONTRADICTED-era-row corrections. kinetic-fusillade's
  era row is CONFIRMED; flagging it would falsely imply the era stamp was wrong.
  The era_year correction is recorded here (ledger) as the sole audit trail, per
  no-silent-transformation. (Verified: kinetic-fusillade has 0 `errata_applied=1`
  rows post-ingest.)
- **provenance note:** kinetic-fusillade **IS PROMOTED** to `verified-v1.1` (10
  facts) — its era verdict is CONFIRMED and it carries no CONTRADICTED verdict; only
  the non-eras era_year artifact was rekeyed, which does not gate promotion.
- **source anchors (verbatim):**
  - verify era row: "Kinetic Fusillade was Added a new Intelligence Skill Gem in
    version 3.27.0" — poedb.tw/us/Kinetic_Fusillade.
  - citation titles anchoring the year: "[3.27] Kinetic Fusillade, the build of the
    league (Elementalist/Olroth)" (pathofexile.com forum) and "Kinetic Fusillade
    Ballista Hierophant League Starter (3.28)" (maxroll.gg). PoE 3.27/3.28 shipped
    in **2024**, establishing the introduction year as 2024, not 2013.
- **not-corrected fields:** `eras` (=`3.20+`, CONFIRMED) untouched. Only `era_year`.
- **red-flag origin:** batch-05 flagged era_year=2013 as a bulk-fill artifact. The
  batch-05 citations anchor the true introduction (3.27/3.28 = 2024), so this is
  applied as an errata (not deferred to a REVIEW row). NOTE: the identical 2013
  bulk-fill placeholder persists on the OTHER 23 batch-05/06 kits and on prior-wave
  kits; those were NOT individually rekeyed this wave (only kinetic-fusillade was
  in-scope per the dispatch red flag). A systematic era_year backfill is a stage-3
  candidate — see MIGRATION-vdm1-ingest3 § era_year-artifact.

---

## REVIEW-2 — poe1-poets-pen-vd class field (Berserker/Inquisitor vs stamped Elementalist/Necromancer) — NO in-scope column to correct

- **kit_id:** `poe1-poets-pen-vd`
- **field:** ascendancy/class — **NOT a `canon_corpus` column.** The class value
  lives in `roster_atlas.class_v4r2` (mirrored in `roster_lineage_enrichment`),
  which is OUTSIDE elrond's landing-zone write scope AND — critically —
  **`poe1-poets-pen-vd` has NO row in `roster_atlas` at all** (verified: 0 rows in
  both roster_atlas and roster_lineage_enrichment for this kit_id). There is no
  writable class column in `corpus.db` for this kit. The "DB class field says
  Elementalist/Necromancer" premise in the dispatch refers to a value in the
  upstream mobile-harvest source / a stage-3 mapping not present in corpus.db.
- **status:** REVIEW — **NO data change this wave.** The class evidence IS captured
  and anchored in the landing zone (verify identity rows CONFIRMED + the batch-06
  `variants` dossier row, both ingested), but there is no in-scope column to
  correct. Routed to the `roster_atlas` owner via knight-rider for adjudication.
- **batch:** 06
- **date noted:** 2026-07-18 (ingest wave 3)
- **positive evidence (anchored, ingested into kit_dossier / verify_ledger):** the
  batch-06 `variants` dossier row for poets-pen-vd carries payload
  `["Berserker/Marauder (3.1 original)", "Inquisitor Templar (3.2+ after Berserker
  nerf)", "Occultist", "Scion Ascendant (3.10)"]` with verbatim anchor "as of Patch
  3.2, this build is no longer supported. Berserker class is no longer viable
  choice... leading to the Templar[/Inquisitor]" (pathofexile.com forum). The
  identity CONFIRMED rows cite the odealo guide title "Poet's Pen Volatile Dead
  **Berserker/Marauder** Patch 3.1 Build". So the primary sources attest the class
  lineage **Berserker (3.1) -> Inquisitor Templar (3.2+)** — NOT Elementalist or
  Necromancer.
- **why not corrected here:** (1) no-silent-transformation forbids inventing a
  class column; (2) the authoritative class store (`roster_atlas`) is not elrond's
  seam and, in any case, lacks a row for this kit. Correcting the upstream value
  requires the roster_atlas owner (per ADR-004 cross-seam coordination) — elrond
  authors the request; another agent applies the roster-side change.
- **recommended action for steward/Matt/roster owner:** rekey the poets-pen-vd
  class from Elementalist/Necromancer to the attested `Inquisitor` (3.2+ canonical
  peak) with the Berserker (3.1 original) lineage noted, WHEREVER that value is
  authoritatively stored (roster_atlas.class_v4r2 and/or the mobile-harvest source
  that seeds it). The batch-06 dossier `variants` row is the citation. Until the
  roster owner acts, the corpus.db landing zone correctly records the anchored
  evidence and this REVIEW note; no corpus.db field is silently changed.
