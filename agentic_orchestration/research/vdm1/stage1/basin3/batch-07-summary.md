# VDM-1 basin-3 batch-07 summary — d3 kits L73–84

**Batch:** b07 | **Date:** 2026-07-18 | **Mode:** B (systematic crawl) | **Game:** d3 (all 12 kits)

---

## Per-kit one-liners

| kit_id | verdict summary |
|---|---|
| d3-inarius-bonestorm | identity C · mechanics C · era(late-sets) C — Note: no bone-storm-dedicated maxroll guide; Inarius Death Nova guide carries the bonestorm set mechanics |
| d3-inna-allies | identity C · mechanics C · era(late-sets) C · era(s39) C — probe resource "mana (reserve)" contradicts fetched "Spirit"; red-flagged below |
| d3-invoker-thorns | identity C · mechanics C · era(set-era) C · era(late-sets) C · era(s39) C |
| d3-jade-harvester | identity C · mechanics C · era(set-era) C · era(late-sets) C |
| d3-leapquake | identity C · mechanics C · era(set-era) C · era(late-sets) C · era(s39) C |
| d3-lod-archetype | identity C · mechanics C · era(set-era) CONTRADICTED · era(late-sets) C · era(s39) C |
| d3-lod-bazooka | identity C · mechanics C · era(late-sets) C · era(s39) C |
| d3-lon-bombardment | identity C · mechanics C · era(set-era) C · era(late-sets) C |
| d3-m6-sentries | identity C · mechanics C · era(ros-early) C · era(set-era) C · era(late-sets) C |
| d3-manald-heal | identity C · mechanics C · era(set-era) C |
| d3-masquerade-spear | identity C · mechanics C · era(late-sets) C · era(s39) C |
| d3-mundunugu-sb | identity C · mechanics C · era(late-sets) C · era(s39) C |

---

## Advisory verdict histogram (ADVISORY — steward recounts from files)

- CONFIRMED: 50
- CONTRADICTED: 1
- UNSUPPORTED: 0
- SOURCE_NOT_FOUND: 0

0 negatives in this slice — no negative_canon family rows emitted (correct per brief).

---

## Contradictions (1)

**d3-lod-archetype / era / set-era — CONTRADICTED (floor-too-early, D-2a candidate)**
The Legacy of Dreams gem was introduced in Patch 2.6.6 for **Season 18** (confirmed by blizzardwatch.com/2019 announcement). The `set-era` token predates Season 18. The LoD gem is the build's sole identity mechanism — without it there is no "LoD archetype" build. Era floor should be `late-sets` at earliest (Season 18 onward). This is a D-2a floor-too-early contradiction. Erratum queue: `d3-lod-archetype / era / set-era` → CONTRADICTED, floor corrected to late-sets.

---

## SOURCE_NOT_FOUND kits

None. All 12 kits found via maxroll.gg/d3 or icy-veins.com.

Note on d3-manald-heal: no dedicated current maxroll guide exists for the Manald Heal Archon build (it was retired in Season 22 per icy-veins). Icy-veins carries the archived guide (Patch 2.6.9 / Season 21, Deadset). This is a legitimate `set-era` kit with no current-season guide — source found, all claims supported via icy-veins archive.

Note on d3-inarius-bonestorm: maxroll does not publish a stand-alone "Bone Storm" guide; the Inarius set's Bone Storm mechanic is documented via the Inarius Death Nova guide + Necromancer class overview. All claims supported; no SNF.

---

## Dossier coverage

- Total dossier rows: 72 (6 families × 12 kits)
- Abstained rows: 0
- Coverage: 72/72 = **100%**

---

## Author credits

| handle | site | kits covered |
|---|---|---|
| wudijo | maxroll.gg | d3-inarius-bonestorm · d3-m6-sentries · d3-masquerade-spear |
| Northwar | maxroll.gg | d3-inna-allies · d3-invoker-thorns · d3-lon-bombardment |
| Chewi (@chewingnom) | maxroll.gg | d3-jade-harvester · d3-lod-bazooka · d3-mundunugu-sb |
| Rob | maxroll.gg | d3-leapquake · d3-lod-archetype (gem mechanics) |
| Deadset | icy-veins.com | d3-manald-heal |

---

## Red flags for steward erratum queue

**RF-1 (ERRATUM HIGH) — d3-lod-archetype era floor too early:**
DB spec stamps `set-era` but LoD gem was not introduced until Season 18 / Patch 2.6.6 (`late-sets` era). The archetype does not exist before the gem. D-2a violation confirmed. Recommend: correct era floor to `late-sets` in canon_corpus.

**RF-2 (PROBE FABRICATION — confirm and correct) — d3-inna-allies resource:**
Probe facts record `"resource_verbatim": "mana (reserve)"` for the Inna Mystic Ally Monk build. Fetched text (maxroll.gg guide) explicitly states: **"Class Resource: Spirit (Monk's primary resource)"**. Monks use Spirit, not Mana. The probe fact contradicts the d3 class-resource instrument (Monk = Spirit). This is a probe fabrication in the same class as the basin-2 GoD-DH spirit/focus error. Mark for erratum correction: `d3-inna-allies / mechanics / resource` → Spirit.

**RF-3 (IDENTITY NOTE) — d3-lod-archetype vs d3-lod-bazooka vs d3-lon-bombardment distinction:**
Fetched text explicitly confirms: Legacy of Dreams = a gem (liberates two ring slots); Legacy of Nightmares = a ring set (two ring slots, the older mechanic). The distinction holds cleanly — lod-archetype uses the LoD gem, lon-bombardment uses the LoN ring set. No blur detected; confirming for steward: spec IDs are correctly differentiated.

**RF-4 (ERA NOTE) — d3-manald-heal set-era only (no late-sets):**
Icy-veins confirms the build "was retired in Season 22" (beginning of the late-sets era transition). DB stamps only `set-era` — this appears correct. The build's identity (Manald Heal ring + Paralysis proc) predates Season 22; it emerged through "Patch 2.4's lifecycle." No floor-too-early issue. Confirming for steward: `set-era` only is accurate.

**RF-5 (ADVISORY) — d3-lod-bazooka lod-era note:**
The maxroll guide mentions the LoD Bazooka "dominated the META from Season 16 to 19" specifically as the LoD version (after Season 18 when the LoD gem was introduced). Earlier iterations (Season 12-15) used the LoN set, not LoD. DB stamps `late-sets, s39` (no set-era) — this is CORRECT for the LoD-specific version. No contradiction to file; advisory note only.

**RF-6 (ABSTAIN NOTE) — 0 abstentions this batch:**
All 6 dossier families yielded payload for all 12 kits. No source-silent abstentions.

---

## Cross-seam notes

- Crusader debut confirmed: Reaper of Souls, March 25, 2014. No kit in this slice claims vanilla-floor on Crusader kits (invoker-thorns floors at set-era, lon-bombardment floors at set-era) — no D-2b violation.
- Necromancer debut confirmed: Rise of the Necromancer, June 27, 2017. inarius-bonestorm floors at late-sets; masquerade-spear floors at late-sets. Both are post-2017 — no D-2b violation.
- Mundunugu's Regalia confirmed: introduced Season 20 (Patch 2.6.8). DB stamps late-sets — correct.
- M6 Marauder Sentry confirmed pre-Seasons / Season 1 (ros-early floor). DB stamps ros-early · set-era · late-sets — all confirmed.

---

## STEWARD AUDIT ADDENDUM (gandalf, 2026-07-18 — CW3, audited on return)

**ACCEPTED, 6 anchor trims.** File truth: **50 rows = 49C/1X/0U/0SNF** (advisory "50C/1X" — drift series #16, C off by 1; kits 12 ✓, families 12/12/26/0 — zero negative rows per roster ✓). Citations 16/0 quarantined (maxroll 14 · blizzardwatch 1 — release-journalism era anchor, LEGAL per b02 precedent · icy-veins 1). Dossier **72/72 non-abstained = 100% — first full-coverage batch of the run** (d3 living-guide density ceiling; zero abstain-null exposure). No illegal payloads, conf all numeric.

**Content-class gloss/splice cluster TRIMMED at audit (anchor law: glosses trimmed, splices are leaks — 6 rows corrected in-place, verdicts UNCHANGED):** inna-allies identity (mis-truncated title "Season 38" → title-exact "Season 38/39" — steward citation-title check RESOLVED the apparent S38-vs-S39 discrepancy: the page title carries both; s39 attestation REAL) · inna-allies mechanics (composite gloss → verbatim embedded fragment "most commonly used generator"; THIN anchor noted, C corroborated by same-page fetch) · inna-allies era-s39 (date-gloss → title-exact) · invoker-thorns era (framing → embedded verbatim S22 Bombardment quote) · **lod-archetype X anchor** (headline+body splice → headline-only "Diablo 3 Season 18 adds the Legacy of Dreams Legendary gem" — X STANDS) · manald-heal era (three-fragment splice → verbatim Patch-2.4 emergence line, which supports `set-era` directly). b07 = gloss-offender batch (5 of 6 trims one agent-pattern); watch item for CW4+ prompts.

**The X is a clean D-2a floor-too-early:** d3-lod-archetype `set-era` floor CONTRADICTED — LoD gem introduced Patch 2.6.6 / Season 18 (post-set-era). → **ERRATUM HIGH (INGEST-13): era floor `set-era` → `late-sets`.** The LoD-vs-LoN identity split held clean across lod-archetype / lod-bazooka / lon-bombardment (agent RF-3 verified — no blur; lon-bombardment rides the ring set, lod-* the gem).

**Erratum queue adds (INGEST-13):** lod-archetype era floor HIGH (above) · **inna-allies probe `resource_verbatim: "mana (reserve)"` FABRICATION — Monk is Spirit** (probe-fabrication series #3: gd basin-2 · GoD-DH b06 · inna b07 — class-resource instrument caught all three) · advisories CONFIRMED-correct: manald-heal `set-era`-only (build retired S22, never late-sets) · lod-bazooka `late-sets`-only (LoD version S17/18+).
