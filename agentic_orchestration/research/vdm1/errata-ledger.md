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

---

## ERRATA-10 — poe1-venom-gyre era floor correction (3.7 -> 3.8 within bucket)

- **kit_id:** `poe1-venom-gyre`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.7-3.13;3.20+` -> `3.8-3.13;3.20+`
- **verdict:** CONTRADICTED (batch-08 verify, `era` claim family) on the 3.7-3.13
  band; paired with a CONFIRMED positive `era` row on the 3.20+ band.
- **batch:** 08
- **date applied:** 2026-07-18 (ingest wave 4)
- **verify_ledger:** `errata_applied=1` set on the ingested venom-gyre 3.7-3.13 `era`
  CONTRADICTED row (exactly one such row; the 3.20+ CONFIRMED row is NOT flagged).
- **provenance note:** EXCLUDED from promotion (carried a CONTRADICTED era). Venom
  Gyre has 0 probe facts in corpus.db regardless (zero-probe kit), so its promotion
  effect is moot; it is excluded on principle.
- **class:** debut-inside-bucket (same class as ERRATA-1/3/4/5/6/7). Venom Gyre
  debuted at patch **3.8.0**, inside the `3.7-3.13` bucket whose floor 3.7 predates
  it by one patch. Narrow the floor 3.7 -> 3.8, yielding `3.8-3.13;3.20+`; the
  `3.20+` band is untouched (it is independently attested — see anchor).
- **source anchors (verbatim):**
  - CONTRADICTED: "'[3.8] Venom Gyre Assassin done right' posted September 2019 —
    Venom Gyre introduced in patch 3.8.0; era floor 3.7 predates skill introduction"
    — pathofexile forum.
  - CONFIRMED (positive, 3.20+): "'[3.22] Vaal Venom Gyre - Pathfinder' forum
    thread; [3.23] league starter Venom Gyre Deadeye YouTube guide; Deadeye most
    prominent class 3.20-3.23."

---

## ERRATA-11 — poe1-viper-poison DROP unattested 3.0-3.6 bucket (RESTAMP under ERRATA-8 precedent)

- **kit_id:** `poe1-viper-poison`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.0-3.6;3.7-3.13` -> `3.7-3.13`
- **verdict:** CONTRADICTED (batch-08 verify, `era` claim family) on the 3.0-3.6
  band; **corroborated by a paired CONFIRMED positive `era` row on the 3.7-3.13
  band** (both rows landed via the granular one-row-per-band split).
- **batch:** 08
- **date applied:** 2026-07-18 (ingest wave 4)
- **verify_ledger:** `errata_applied=1` set on the ingested viper-poison 3.0-3.6
  `era` CONTRADICTED row (exactly one such row; the 3.7-3.13 CONFIRMED row is NOT
  flagged).
- **provenance note:** EXCLUDED from promotion (carried a CONTRADICTED era).
  viper-poison has 0 probe facts (zero-probe kit); promotion effect is moot; excluded
  on principle.
- **ADJUDICATION (drop-vs-restamp, per ERRATA-8 seismic-trap precedent):** The
  dispatch flagged this as a **combined-kit impossibility** — the ENTIRE 3.0-3.6
  bucket precedes co-skill **Pestilent Strike's 3.8.0 debut**. The stamped identity
  is the *dual-skill Poison Assassin* archetype (Viper Strike + Pestilent Strike);
  Viper-Strike-alone is a DIFFERENT claim and is not what is stamped. So the
  combined kit as stamped **cannot exist** before 3.8.0, which invalidates the
  entire 3.0-3.6 bucket (not just its floor). The ERRATA-8 rule is: *if no in-bucket
  attestation of the combined kit, DROP the bucket; RESTAMP only if the b08 anchors
  attest a specific later window.* Here the b08 anchors **DO attest a specific later
  window** — a CONFIRMED positive `era` row on **3.7-3.13**, anchored by the "[3.8]
  Pestilent Strike & Viper Strike Poison Assassin" thread by tylam6746 documenting
  the combined build from patch 3.8. Therefore this is a **RESTAMP, not a blanket
  DROP**: drop only the unattested 3.0-3.6 bucket and KEEP the attested 3.7-3.13
  window, yielding `3.7-3.13`. (Note: the surviving 3.7-3.13 band's floor 3.7 is one
  patch below the 3.8.0 co-skill debut; the band is retained as-is because the
  attestation is a *3.8-band* build inside that bucket and the bucket is the
  attested unit — no sub-band floor-narrowing is applied within an attested wide
  bucket, consistent with wave-3 register semantics.)
- **source anchors (verbatim):**
  - CONTRADICTED: "Pestilent Strike 'Added a new Dexterity/Intelligence Skill Gem -
    Pestilent Strike' in version 3.8.0; skill did not exist in 3.0-3.6. Viper Strike
    existed but the dual-skill Assassin archetype as stamped requires both." —
    poedb.tw.
  - CONFIRMED (positive, 3.7-3.13): "'[3.8] Pestilent Strike & Viper Strike Poison
    Assassin | Fast & Deadly | 6M Shaper DPS' thread by tylam6746 documents the build
    from patch 3.8." — pathofexile forum.
- **contrast with ERRATA-8 (seismic-trap DROP):** seismic-trap had NO attested band
  in the fetched sources except a *different* later floor (3.16 in the 3.14-3.19
  bucket), so its 3.7-3.13 bucket was dropped with no restamp needed (the 3.14-3.19
  band already stood on its own). viper-poison differs: the impossibility is at
  3.0-3.6 and a *specific* adjacent later band (3.7-3.13) IS positively attested, so
  the surviving stamp is that attested band. Both are the "band-unattested" class;
  the discriminator (DROP-only vs DROP-and-keep-attested) turns on whether a distinct
  later band carries positive evidence.

---

## ERRATA-12 — poe1-ward-loop era floor correction (3.14 -> 3.15 within bucket)

- **kit_id:** `poe1-ward-loop`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.14-3.19;3.20+` -> `3.15-3.19;3.20+`
- **verdict:** CONTRADICTED (batch-08 verify, `era` claim family) on the 3.14-3.19
  band; paired with a CONFIRMED positive `era` row on the 3.20+ band.
- **batch:** 08
- **date applied:** 2026-07-18 (ingest wave 4)
- **verify_ledger:** `errata_applied=1` set on the ingested ward-loop 3.14-3.19 `era`
  CONTRADICTED row (exactly one such row; the 3.20+ CONFIRMED row is NOT flagged).
- **provenance note:** EXCLUDED from promotion (carried a CONTRADICTED era).
- **class:** debut-inside-bucket. The **Ward mechanic** debuted at patch **3.15
  (Expedition)**, inside the `3.14-3.19` bucket whose floor 3.14 predates Ward's
  existence in the game (the build is literally impossible in 3.14). Narrow the floor
  3.14 -> 3.15, yielding `3.15-3.19;3.20+`; the `3.20+` band is untouched (attested).
- **source anchors (verbatim):**
  - CONTRADICTED: "Ward mechanic 'introduced in content patch 3.15 (Expedition)';
    era floor 3.14 predates Ward's existence in the game; build impossible in 3.14."
  - CONFIRMED (positive, 3.20+): "Multiple guides for 3.21, 3.22, 3.23, 3.26, 3.27,
    3.28 document Ward Loop as an active build with ongoing balance adjustments."

---

## ERRATA-13 — poe1-winter-orb era floor correction (3.0 -> 3.5 within bucket)

- **kit_id:** `poe1-winter-orb`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.0-3.6` -> `3.5-3.6`
- **verdict:** CONTRADICTED (batch-08 verify, `era` claim family) on the 3.0-3.6
  band.
- **batch:** 08
- **date applied:** 2026-07-18 (ingest wave 4)
- **verify_ledger:** `errata_applied=1` set on the ingested winter-orb 3.0-3.6 `era`
  CONTRADICTED row (exactly one such row).
- **provenance note:** EXCLUDED from promotion (carried a CONTRADICTED era).
  winter-orb has 0 probe facts (zero-probe kit); promotion effect is moot; excluded
  on principle.
- **class:** debut-inside-bucket. Winter Orb debuted at patch **3.5.0 (Betrayal)**,
  inside the `3.0-3.6` bucket whose floor 3.0 predates it by five patches. Narrow the
  floor 3.0 -> 3.5, yielding `3.5-3.6` (the sole band collapses to the two-patch
  window 3.5-3.6). poe.ninja records 9% representation at 3.5, corroborating Betrayal
  as the genuine debut/adoption league.
- **source anchor (verbatim):** "Winter Orb 'introduced in version 3.5.0' patch
  notes; era floor 3.0 predates skill introduction by five patches; Betrayal (3.5)
  is first era. '9% representation in Betrayal league' per poe.ninja."

---

## BACKFILL-1 — poe1-vaal-blade-vortex era fill (NULL -> attested crawl value; NOT errata)

- **kit_id:** `poe1-vaal-blade-vortex`
- **field:** `canon_corpus.eras`
- **old -> new:** `NULL` -> `3.0-3.6;3.7-3.13`
- **verdict:** the `era` verify row is **CONFIRMED** (batch-07). This is a **FILL of
  an EMPTY (NULL) column**, NOT a correction of a contradicted value — VBV is a
  DB-only census kit that carried NO era stamp. The b07 crawl established the window
  with citations.
- **batch:** 07
- **date applied:** 2026-07-18 (ingest wave 4)
- **verify_ledger:** **NO `errata_applied` flag set.** The flag is reserved for
  CONTRADICTED-era-row corrections; VBV's era row is CONFIRMED and there was no prior
  value to contradict. This ledger + the MIGRATION doc are the sole audit trail of the
  fill (no-silent-transformation). Verified: VBV has 0 `errata_applied=1` rows.
- **provenance note:** this is a **fill-from-verified-crawl**. VBV has 0 probe facts
  (zero-probe kit) so it is in the promote set but promotes 0 rows (nothing to
  promote); the era fill does not gate promotion.
- **source anchor (verbatim):** "Vaal Blade Vortex has been added to the game
  (3.3.0); '[3.8 Video Guide] Blade Vortex Inpulsa Clear Speed Build [Inquisitor]'
  confirms 3.7-3.13 era presence." — the 3.3.0 debut lands in the `3.0-3.6` bucket
  and the 3.8 guide confirms the `3.7-3.13` bucket, so the filled value is
  `3.0-3.6;3.7-3.13`. Guarded UPDATE `eras IS NULL` -> value, rowcount==1.

---

## REGISTER-ANNOT (wave 4) — Unattested Register + floor-based bucket-audit intro-patch notes

Not data changes; recorded for the stage-3 systematic bucket-audit sweep. The
floor-based bucket-audit register (wave-3 doc) **empties to 0** this wave: all 12
wave-3 register kits were individually crawled in batches 07-08, so none remains an
audit candidate. The three annotations below attach to now-verified rows as stage-3
sweep inputs.

- **UNATTESTED REGISTER — `poe1-totem-hierophant`:** era **UNSUPPORTED** (batch-07);
  eras unrecoverable from search. DB `eras` stays **NULL** (no data write — no
  attested window to fill; contrast BACKFILL-1 where VBV's window WAS attested). The
  landing-zone verify row ("Era stamps absent from DB — cannot verify era claims") is
  the record. Enters the **Unattested Register** per charter stream-1
  (UNSUPPORTED/SOURCE-NOT-FOUND on an unrecoverable axis). Note: totem-hierophant is a
  zero-probe kit; it is in the promote set but promotes 0 rows.
- **INTRO-PATCH ANNOT — `poe1-tectonic-slam` (intro 3.2.0):** b07 graded its
  `3.0-3.6` floor stamp **CONFIRMED** (genuine back-half presence: "Tectonic Slam
  introduced 3.2.0 … a very solid melee skill since its release"). NO errata basis
  (the floor is attested). The attested introduction patch **3.2.0** is attached to
  its floor-based bucket-audit register row for the stage-3 sweep — 3.2.0 sits inside
  the `3.0-3.6` bucket, so a future debut-vs-floor scrutiny would confirm the floor
  is correct (skill present AND meta-attested in the back half of the bucket).
- **INTRO-PATCH ANNOT — `poe1-toxic-rain` (intro 3.4.0):** b07 graded its `3.0-3.6`
  floor stamp **CONFIRMED** (genuine back-half presence: "Toxic Rain introduced 3.4.0
  Delve"). NO errata basis. The attested introduction patch **3.4.0** is attached to
  its register row for the stage-3 sweep — 3.4.0 sits inside `3.0-3.6`; back-half
  presence confirmed. (Note: toxic-rain's `3.7-3.13` mid-band was graded UNSUPPORTED
  in b07 — a partition-analysis input, not an errata; its floor and later bands are
  CONFIRMED, so the multi-band stamp `3.0-3.6;3.7-3.13;3.14-3.19;3.20+` is retained
  unchanged.)

---

## ERRATA-14 — poe1-tectonic-slam era floor correction (3.0 -> 3.2; D-2a uniform-law retro)

- **kit_id:** `poe1-tectonic-slam`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.0-3.6` -> `3.2-3.6`
- **verdict basis:** stage-3 **D-2a uniform law** — an era floor that predates the
  skill's introduction patch is **CONTRADICTED**, regardless of back-half meta
  presence. This RETIRES the earlier policy split under which b07 graded the floor
  CONFIRMED (see REGISTER-ANNOT wave 4 above, "genuine back-half presence").
- **batch:** b07 (attestation source); applied at ingest wave 6.
- **date applied:** 2026-07-18 (ingest wave 6)
- **verify_ledger:** **NO `errata_applied` flag set, and the b07 verdict rows are
  NOT retro-edited** — they KEEP their historical **CONFIRMED** grade (dispatch
  law). The `errata_applied=1` convention is reserved for CONTRADICTED-era verify
  rows; this kit has no such row. The data restamp + this ledger entry are the sole
  audit trail (same provenance shape as ERRATA-9 / BACKFILL-1: data change, no flag).
  Post-wave errata_applied total STAYS 12. (Verified: tectonic-slam has 0
  `errata_applied=1` rows post-ingest; its era verify row remains CONFIRMED,
  errata_applied=0.)
- **source anchor (verbatim, from the b07 era CONFIRMED verify row):** "Tectonic
  Slam was introduced in patch 3.2.0 as a new Strength Skill Gem" — the debut patch
  3.2.0 sits inside the `3.0-3.6` bucket; the bucket floor 3.0 predates it by two
  patches. Under D-2a the floor is narrowed 3.0 -> 3.2, yielding `3.2-3.6`.
- **class:** debut-inside-bucket (same shape as ERRATA-1/3/4/5/6/7/10) BUT reached
  under the NEW uniform law rather than a fresh CONTRADICTED crawl — the b07 floor
  grade was CONFIRMED under the retired split; D-2a re-classes the floor as
  contradicted-by-rule and applies the standard floor-narrowing.
- **supersedes:** the wave-4 REGISTER-ANNOT for tectonic-slam ("3.2.0 sits inside
  3.0-3.6, floor confirmed"). That annotation reflected the retired policy; the
  floor is now moved. The b07 CONFIRMED verdict row is nonetheless preserved
  unedited per dispatch law.
- **not-corrected fields:** `era_year` (=2013 bulk-fill artifact) untouched (out of
  this dispatch's scope; a systematic era_year backfill remains a stage-3 candidate).

---

## ERRATA-15 — poe1-toxic-rain era floor correction (3.0 -> 3.4; D-2a uniform-law retro)

- **kit_id:** `poe1-toxic-rain`
- **field:** `canon_corpus.eras`
- **old -> new:** `3.0-3.6;3.7-3.13;3.14-3.19;3.20+` -> `3.4-3.6;3.7-3.13;3.14-3.19;3.20+`
- **verdict basis:** stage-3 **D-2a uniform law** (as ERRATA-14). Floor predates the
  skill's debut -> CONTRADICTED-by-rule; the earlier CONFIRMED-with-note grade under
  the retired split is retired.
- **batch:** b07 (attestation source); applied at ingest wave 6.
- **date applied:** 2026-07-18 (ingest wave 6)
- **verify_ledger:** **NO `errata_applied` flag set; b07 verdict rows NOT retro-edited**
  (KEEP CONFIRMED, per dispatch law). Same provenance shape as ERRATA-14. Post-wave
  errata_applied total STAYS 12. (Verified: toxic-rain retains its CONFIRMED era
  verdict rows with errata_applied=0; the earlier `3.7-3.13` UNSUPPORTED partition
  row is likewise untouched.)
- **source anchor (verbatim, from the b07 era CONFIRMED verify row):** "Toxic Rain
  was introduced in version 3.4.0 (Delve league)" — the debut patch 3.4.0 sits
  inside the leftmost `3.0-3.6` bucket; the floor 3.0 predates it by four patches.
  Under D-2a the leftmost floor is narrowed 3.0 -> 3.4, yielding `3.4-3.6`.
- **scope of the correction (ONLY the leftmost bucket's floor moves):** the three
  later buckets are UNTOUCHED. `3.7-3.13` is retained as-is — its b07 UNSUPPORTED
  grade is a partition-analysis input, NOT an errata basis (per the wave-4
  REGISTER-ANNOT note); `3.14-3.19` and `3.20+` are CONFIRMED and untouched. So the
  corrected stamp is `3.4-3.6;3.7-3.13;3.14-3.19;3.20+`.
- **class:** debut-inside-bucket under the NEW uniform law (as ERRATA-14).
- **supersedes:** the wave-4 REGISTER-ANNOT for toxic-rain ("3.4.0 sits inside
  3.0-3.6; back-half presence confirmed; multi-band stamp retained unchanged"). The
  leftmost floor is now moved 3.0 -> 3.4; the three later bands remain unchanged as
  that annotation described. The b07 CONFIRMED verdict rows are preserved unedited.
- **not-corrected fields:** `era_year` (=2013 bulk-fill artifact) untouched.

---

# ============ BASIN-1 (PoE2) — ingest wave 8 ============

The entries below are the FIRST basin-1 (PoE2) adjudications (ingest wave 8, batches
01-02, kits 1-24). PoE2 uses the era-band vocabulary `0.1 | 0.2-dawn | 0.3-edict | 0.4
| 0.5-ancients` (Early-Access patch bands), NOT the PoE1 `3.x` bands. The same
adjudication classes carry over.

---

## ERRATA-16 — poe2-acolyte-darkness era restamp (drop pre-debut bands; D-2a-to-limit)

- **kit_id:** `poe2-acolyte-darkness`
- **field:** `canon_corpus.eras`
- **old -> new:** `0.1;0.2-dawn` -> `0.3-edict;0.4;0.5-ancients`
- **verdict:** CONTRADICTED (batch-01 verify, `era` claim family). The single era row
  covers both stamped bands (claim "Build present/meta in eras 0.1, 0.2-dawn").
- **batch:** 01 (basin-1)
- **date applied:** 2026-07-18 (ingest wave 8)
- **verify_ledger:** `errata_applied=1` set on the ingested acolyte-darkness `era`
  CONTRADICTED row (exactly 1 such row).
- **class:** **D-2a (floor-too-early) taken to its limit.** Into the Breach's poe2db
  version history STARTS at v0.3.0 and runs through v0.5.0. BOTH stamped bands (0.1,
  0.2-dawn) predate the 0.3.0 debut, so a naive D-2a floor-narrow would empty the
  stamp entirely. Under the ERRATA-11 rule (drop unattested bands AND restamp to the
  crawl-attested later window), the corrected value is the attested 0.3-0.5 window
  `0.3-edict;0.4;0.5-ancients`. The Acolyte of Chayula ascendancy existed from launch,
  but the specific Into the Breach skill gem — the kit's core skill — was added at 0.3.0.
- **source anchor (verbatim, from the b01 era CONTRADICTED verify row):** "version
  history starting from v0.3.0, with updates continuing through v0.5.0" —
  poe2db.tw/us/Into_the_Breach. Crawler's anchor verified in `batch-01-verify.jsonl`
  BEFORE restamping (dispatch requirement).
- **contrast with the PoE1 D-2a errata (14/15):** those narrowed only the leftmost
  floor and kept later attested bands in place. Here there are NO later bands in the
  DB stamp beyond the two pre-debut bands, so the restamp is a full drop-and-replace
  with the attested window (ERRATA-11 shape) rather than an in-place floor-narrow.
- **not-corrected fields:** identity + mechanics verify rows are UNSUPPORTED (folk name
  "Darkness Acolyte" and the chaos-conversion mechanic unattested; honest silence, no
  data change — the class is "Acolyte of Chayula" in all sources). `era_year` untouched.

---

## ERRATA-17 — poe2-concoction era floor EXTENSION (floor-too-LATE — NEW class)

- **kit_id:** `poe2-concoction`
- **field:** `canon_corpus.eras`
- **old -> new:** `0.2-dawn;0.3-edict;0.4;0.5-ancients` -> `0.1;0.2-dawn;0.3-edict;0.4;0.5-ancients`
- **verdict:** CONTRADICTED (batch-01 verify, `era` claim family). The era row claims
  "Build present/meta in eras 0.2-dawn, 0.3-edict, 0.4, 0.5-ancients"; the crawl found
  the build ALSO present one band earlier (0.1), making the stamped floor internally
  inconsistent with attested presence.
- **batch:** 01 (basin-1)
- **date applied:** 2026-07-18 (ingest wave 8)
- **verify_ledger:** `errata_applied=1` set on the ingested concoction `era` CONTRADICTED
  row (exactly 1 such row).
- **class:** **floor-too-LATE (NEW; the inverse of the D-2a floor-too-early class).** The
  stamped floor 0.2-dawn POSTDATES attested presence: a maxroll Poisonous Concoction guide
  carries "Adjusted build for patch 0.1.0e Hotfix 6" — the skill and build were active in
  0.1, one band below the stamped floor.
- **RULING (extend-floor vs leave+annotate):** **EXTEND the floor to 0.1**
  (fill-from-verified-crawl, BACKFILL-1 VBV precedent) rather than leave the stamp +
  annotate. The attestation is a specific, dated hotfix guide (0.1.0e Hotfix 6), so the
  floor fill is evidence-grounded, not speculative. Prepend the `0.1` band; the later four
  bands are untouched (all independently attested).
- **flag discriminator vs BACKFILL-1:** BACKFILL-1 (poe1-vaal-blade-vortex) FILLED an
  EMPTY (NULL) column from a CONFIRMED era row and set NO `errata_applied` flag. This case
  differs: the column was NON-empty and a CONTRADICTED era verify row DID land (the stamp
  is contradicted as internally inconsistent re: 0.1 presence). Per the flag convention
  ("errata_applied is set on CONTRADICTED-era verify rows"), the flag IS set here. So the
  RULING shares BACKFILL-1's *data shape* (fill a band from a verified crawl) but takes the
  ERRATA *flag treatment* (a CONTRADICTED row exists). This is the discriminator recorded
  for the floor-too-LATE class going forward: **extend + flag when the verify row is
  CONTRADICTED; extend + no-flag (BACKFILL) when the verify row is CONFIRMED/empty-fill.**
- **source anchor (verbatim, from the b01 era CONTRADICTED verify row):** "Adjusted build
  for patch 0.1.0e Hotfix 6. This patch fixes a bug where Chaos Inoculation was counted as
  being on Low Life." — maxroll.gg Poisonous Concoction Pathfinder build guide.
- **not-corrected fields:** the negative_canon UNSUPPORTED row (corpus-triage metadata,
  not a testable game-state claim) is landed but not acted on; identity + mechanics are
  CONFIRMED. `negative=1` on this kit is unchanged.

---

## ERRATA-18 — poe2-grim-feast era trim to 0.2-dawn (ES-overleech died at the 0.3.0 rework)

- **kit_id:** `poe2-grim-feast`
- **field:** `canon_corpus.eras`
- **old -> new:** `0.2-dawn;0.3-edict;0.4` -> `0.2-dawn`
- **verdict:** **2 CONTRADICTED** era rows (batch-02 verify: bands 0.3-edict AND 0.4),
  **corroborated by a paired CONFIRMED positive** era row on the 0.2-dawn band (all three
  landed via the batch-02 granular one-row-per-band split).
- **batch:** 02 (basin-1)
- **date applied:** 2026-07-18 (ingest wave 8)
- **verify_ledger:** `errata_applied=1` set on BOTH the 0.3-edict and 0.4 CONTRADICTED era
  rows (exactly 2 such rows; the 0.2-dawn CONFIRMED row is NOT flagged). **FIRST errata to
  flag 2 rows on one kit** — a paired-band drop. (Contrast ERRATA-8 seismic-trap, which
  flagged 1 because only 1 band was contradicted.)
- **class:** ERRATA-8/11 trim ("mechanic death — stamped bands postdate the mechanic's
  existence"). Grim Feast was **"completely reworked and re-enabled" at 0.3.0** (poe2db):
  the ES-overleech mechanic the kit describes (a Spirit-reserved buff that vacuums life
  remnants into energy-shield overleech) existed ONLY in 0.2-dawn; the reworked 0.3.0+
  skill is a DIFFERENT mechanic (collect remnants from dead Reviving Minions — a
  minion-revival layer). The 0.3-edict and 0.4 stamps therefore postdate the ES-overleech
  identity's death. TRIM to the attested ES window `0.2-dawn`.
- **RULING (trim vs split-kit):** **TRIM** the eras to `0.2-dawn` only. **Split-kit** (an
  ES-overleech variant 0.1-0.2 vs a post-rework "Grim Resurrection" minion variant 0.3+)
  was CONSIDERED and REJECTED as overkill for a single cross-build defensive-layer kit —
  the trim + a `mech_note` annotation (recording the 0.3.0 rework boundary) capture the
  transition losslessly without minting a second corpus row (which would also break the
  585-conservation invariant, cf. the di-druid ruling).
- **source anchor (verbatim, from both b02 CONTRADICTED era rows):** "Grim Feast has been
  completely reworked and re-enabled. Instead of granting energy shield, it now allows you
  to collect remnants from your dead Reviving Minions" — poe2db.tw/us/Grim_Feast.
- **not-corrected fields:** identity + mechanics CONFIRMED (the ES-overleech description is
  accurate for 0.2-dawn); untouched. A `mech_note` annotation records the rework boundary.

---

## REVIEW-2 (basin-1) — poe2-erasure-edc-lich "Erasure" phantom-mechanic (UNADJUDICATED; NO data change)

- **kit_id:** `poe2-erasure-edc-lich`
- **field:** `canon_corpus.core_skills` (carries `["Essence Drain lineage", "Contagion",
  "Erasure"]`) + `mech_note` (references "Erasure = PoE2-specific mechanic").
- **status:** REVIEW — **unadjudicated. NO data change / NO delete this wave.** Needs
  steward (gandalf) / Matt eyes. (The basin-1 parallel to REVIEW-1 earthshatter.)
- **batch:** 01 (basin-1)
- **date noted:** 2026-07-18 (ingest wave 8)
- **observation:** batch-01's crawl reports "Erasure" **404s on poe2db** and is **absent
  from all lich/witch sources fetched**. The Lich ascendancy overview lists 8 nodes — none
  named Erasure. Essence Drain + Contagion are CONFIRMED real. "Erasure" — the kit's
  distinguishing named mechanic — is either a wrong/mis-transcribed skill name (possible
  kb fabrication) or a very obscure node with no guide coverage. The era verify row is
  CONFIRMED (the ED/Contagion Lich build genuinely existed 0.2-0.5); identity + mechanics
  are UNSUPPORTED (blank-anchor honest silences).
- **investigation result:** "Erasure" IS present in the `core_skills` array of the
  canon_corpus row (confirmed by direct query). Per the dispatch, it is annotated as
  unverified-possible-phantom in `mech_note` (a prepended `[VDM-1 basin-1 2026-07-18]`
  clause) and **NOT deleted**.
- **why not deleted:** the no-silent-edits law forbids removing the skill on a mere
  not-found. A 404 / source-not-found is honest silence, not a contradiction — "Erasure"
  is NOT disproven, only un-located. Deleting it would destroy a datum a later/wider crawl
  might attest. Preserved verbatim in core_skills; flagged in mech_note + here for
  adjudication. **Mirrors exactly how earthshatter's phantom alias (REVIEW-1) and the
  di-spiritform-druid-pvp PHANTOM mis-naming were handled** (annotate-not-delete;
  `errata_applied` NOT set — the flag is for CONTRADICTED-era rows, and this is a
  mechanics/core_skills question with a CONFIRMED era row).
- **recommended action for steward/Matt:** either (a) a targeted re-crawl to attest or
  refute "Erasure" (checking whether it is a mis-transcription of a real Lich node), or
  (b) a ruling to demote/strike it if judged a kb fabrication. Until then it stays in the
  corpus unchanged. `eras` (`0.2-dawn;0.3-edict;0.4;0.5-ancients`) untouched.

---

## ANNOT-BASIN1 (wave 8) — mech_note annotations (NO data restamps)

Not data changes to `eras`/`core_skills`; recorded here for provenance. Each is a
guarded single-row `UPDATE canon_corpus SET mech_note=?` that PREPENDS a dated
`[VDM-1 basin-1 2026-07-18]`-tagged clause; the original harvest note is preserved
verbatim after it (no-silent-transformation). The annotation home is `mech_note`
(established for phantom/lineage notes — cf. the `di-spiritform-druid-pvp` PHANTOM note
and the PoE1 demon-form-class notes; the dispatch's named mechanism).

- **`poe2-demon-form` — element framing MISLEADING:** Demon Form is element-AGNOSTIC
  (Spark/lightning + cold + fire variants all attested per fetched sources); "fire spells
  in-form" is NOT the defining/exclusive mechanic (fire nodes exist in the Infernalist
  ascendancy but the form itself does not lock element). The mechanics verify row is
  UNSUPPORTED for the fire-exclusive claim. NO `element`/`eras` column restamp this wave —
  the element correction is a stage-later concern; the annotation records the finding.
- **`poe2-minion-infernalist` — (a) lineage shift + (b) alias correction:** (a) the
  Infernalist→Lich ascendancy lineage shift (Infernalist hosted 0.1/0.2; Lich dominant
  0.3+; the `class` field understates lineage complexity); (b) the **"Loyal Hellhound"**
  alias in `core_skills` is UNSUPPORTED — the actual skill name is **"Summon Infernal
  Hound"** (a.k.a. "Infernal Hound") across all guides. The alias is **NOT deleted** (same
  no-silent-edits discipline as the erasure phantom); its b02 mechanics verify row is
  UNSUPPORTED (landed in verify_ledger).
- **`poe2-infernal-legion` — lineage shift:** Infernalist→Lich from 0.3+ (Infernalist
  dominant 0.1/0.2 per Kripp Dec2024/Jan2025; current maxroll guide = Lich). Era stamps
  CONFIRMED (untouched); the `class` field understates lineage complexity. Annotation only.
- **`poe2-erasure-edc-lich`** — carries the REVIEW-2 phantom clause (see REVIEW-2 above).

Preservation verified post-write: "Erasure" and "Loyal Hellhound" both remain in their
kits' `core_skills`; all four notes start with the `[VDM-1 basin-1 2026-07-18]` tag.

---

## ROSTER-HYGIENE-1 (wave 8) — le-ring-of-shields corpus_bucket fix + basin-2 NULL-left notes

- **`le-ring-of-shields`:** `corpus_bucket` **`'poe1'` -> `'le'`** (provenance error; the
  kit is Last Epoch, id-prefix `le-`). Verified before fixing: the correct sibling bucket
  value is `'le'` (36 of 37 `le-` rows carry `'le'`; this kit was the SOLE outlier at
  `'poe1'`). Guarded single-row `UPDATE ... WHERE kit_id=? AND corpus_bucket='poe1'`
  (rowcount==1). Post-write: 0 `le-` rows remain non-`le`. This is a provenance-field
  correction, not an era/mechanic errata — no `errata_applied` flag (no verify row).
  eras + core_skills are NULL and the mobile-JSONL kb source has NO row for this kit
  (17 files searched; absent) -> **left NULL** per the dispatch honest-fill rule (basin-2
  crawl verifies what exists).
- **`le-shift-bladedancer`:** bucket already `'le'` (correct — no write). eras +
  core_skills NULL; kb source also absent -> **left NULL**. Documented as
  verified-correct-bucket + intentional-NULL-left; asserted unchanged in-script.
- **carry-forward anomaly (out of scope):** `corpus_bucket` carries both short + long
  Diablo tokens — `d3`/`diablo-3`, `d4`/`diablo-4`, `di`/`diablo-immortal` (one long-form
  singleton each). A normalization concern (gamecode-normalize territory), flagged for a
  future roster-hygiene pass; not touched this wave.
