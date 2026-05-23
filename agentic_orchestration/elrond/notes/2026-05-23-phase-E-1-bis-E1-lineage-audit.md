# Elrond diagnostic — Phase E-1-bis E1 lineage audit

**Authored by:** elrond (Pattern-A in-session subagent return, captured by knight-rider for durability — elrond's environment policy prevented direct file write)
**Date:** 2026-05-23
**Mode:** A (analytical / diagnostic; no fixes, no DB writes)
**For:** Matt via knight-rider routing — input to Phase E-1-bis remediation decision

## Verdict (top-line)

**(d) — Neither (a) nor (b) nor (c). The labels themselves are CORRECT. The 94.46% fantasy_generic figure is a v_category_sample membership artifact, not a Step 6.5 lineage-mapper artifact.**

Gandalf's suspicion was directionally correct that the 94.46% figure is a Phase D artifact and that the museum/encyclopedia rows are misrepresented — but the misrepresentation is one filter layer up from where he thought. The Step 6.5 cultural_lineage_canonical assignments respect cleaning-policy § 5.2 source-driven rules well. The Royal Armouries / Met Museum / Wikipedia / Wikidata rows are correctly labeled `european` / `east_asian` / etc. — they are simply **excluded from v_category_sample by the weapon_kind filter**, never reaching Legolas's Phase E-1 feature matrix.

This reshapes gandalf's option-set substantially. Some B-family options now become incoherent (B1/B2/B4 are operating on a corrupt pool but the corruption is upstream of lineage). E1 remediation is real and load-bearing, but the fix lives in Step 4/the v_category_sample definition, not in Step 6.5's lineage mapper.

---

## Q1 — Per-source-library × per-lineage distribution

### Q1a — Underlying weapon_knowledge_entries (post-Phase-D, all non-merged_into rows)

Step 6.5 produced these per-source × cultural_lineage_canonical assignments (sourced live from `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`, 70,693 non-merged rows):

| source_library | dominant lineages |
|---|---|
| royal_armouries (19,008 rows) | european 17,615 (92.7%); east_asian 542; south_asian 517; middle_eastern 163; african 77; southeast_asian 66; smaller buckets |
| met-museum (7,559 rows) | european 3,117 (41.2%); east_asian 2,999 (39.7%); south_asian 497; unknown 329; southeast_asian 279; middle_eastern 253; african 65 |
| wikipedia (8,553 rows) | european 3,856 (45.1%); unknown 1,507; east_asian 1,394; middle_eastern 551; southeast_asian 351; african 335; south_asian 320 |
| wikidata (12,370 rows) | unknown 9,912 (80.1%); east_asian 2,080; european 162; middle_eastern 153 |
| odin-army-tradoc (3,998 rows) | european 1,265; east_asian 1,178; unknown 867; middle_eastern 369; south_asian 123; southeast_asian 88 |
| army-recognition (62 rows) | cross_cultural 37; european 20; east_asian 5 |
| cataclysm-dda (1,599 rows) | cross_cultural 1,452 (90.8%); european 67; east_asian 50; rest small |
| gta-v-data (183 rows) | cross_cultural 183 (100%) |
| nick-aschenbach-dnd-data (6,297) | fantasy_generic 5,992; rest small |
| wow-classic-items (4,440) | fantasy_generic 4,438 |
| bsdata-warhammer-aos (2,185) | fantasy_generic 2,184 |
| diablo2-d2data (521) | fantasy_generic 521 |
| path-of-exile-repoe (494) | fantasy_generic 494 |
| osrsbox-db (940) | fantasy_generic 938 |
| fextralife-ds1/2/3 (591) | fantasy_generic 591 |
| fextralife-elden-ring (375) | south_american_indigenous 342; fantasy_generic 33 (regex anomaly; not load-bearing for E1 — see Q3 note) |
| bloqhead-demigods (320) | fantasy_generic 320 |
| elden-ring-erdb (307) | fantasy_generic 293; small |
| souls-api-thomaslincoln (2 + 56 quarantined) | fantasy_generic |

**Substrate-level lineage roll-up across ALL non-merged rows (70,693 rows):**

The underlying substrate is roughly:
- fantasy_generic ~16,900 (24%)
- european ~25,260 (36%)
- east_asian ~8,300 (12%)
- unknown ~12,920 (18%)
- middle_eastern ~1,500 (2%)
- south_asian ~1,500 (2%)
- cross_cultural ~1,690 (2.4%)
- smaller buckets sum to ~2,500 (3.5%)

**This is NOT a fantasy-monocultural substrate.** It's a roughly balanced museum-heavy substrate with a meaningful fantasy fraction.

### Q1b — v_category_sample (the 16,699 rows that legolas's PCA actually ran on)

Per-source × lineage inside v_category_sample (the source of the 94.46% figure):

| source_library | rows in v_category_sample | dominant lineages |
|---|---|---|
| nick-aschenbach-dnd-data | 6,205 | fantasy_generic 5,901; south_american_indigenous 156; european 134; rest small |
| wow-classic-items | 4,429 | fantasy_generic 4,427 |
| bsdata-warhammer-aos | 2,157 | fantasy_generic 2,156 |
| osrsbox-db | 940 | fantasy_generic 938 |
| diablo2-d2data | 519 | fantasy_generic 519 |
| path-of-exile-repoe | 488 | fantasy_generic 488 |
| fextralife-elden-ring | 374 | south_american_indigenous 341; fantasy_generic 33 |
| bloqhead-demigods | 319 | fantasy_generic 319 |
| elden-ring-erdb | 306 | fantasy_generic 292; small |
| fextralife-ds1/2/3 | 591 | fantasy_generic 591 |
| wikipedia | 220 | european 77; middle_eastern 47; east_asian 42; south_asian 22; unknown 21; small |
| 5e-bits-5e-database-2024 | 110 | fantasy_generic 110 |
| 5e-bits-5e-database | 37 | european 37 |
| elden-ring + remaining | small |
| wikidata | 3 | (negligible) |
| cataclysm-dda | 1 | (negligible) |
| **royal_armouries** | **0** | — |
| **met-museum** | **0** | — |
| **odin-army-tradoc** | **0** | — |
| **army-recognition** | **0** | — |
| **gta-v-data** | **0** | — |

**98.6% of v_category_sample comes from TRPG/MMO/ARPG/soulslike/SRD sources.** The historical/museum/encyclopedia substrate is structurally excluded.

## Q2 — Royal Armouries specifically

**At the source-row level (Step 6.5 output), Royal Armouries is mapped correctly per § 5.2:**

- 19,008 non-merged RA rows
- 17,615 (92.7%) → `cultural_lineage_canonical='european'`
- 542 (2.9%) → `east_asian`
- 517 (2.7%) → `south_asian`
- 163 (0.9%) → `middle_eastern`
- 77 (0.4%) → `african`
- 66 (0.3%) → `southeast_asian`
- the rest in smaller-but-correct buckets

This is the post-collapse state. The merged-into population (19,119 more rows) carry the same lineage labels. So at the source-row level, RA is **healthy** — it dominantly resolves to `european` exactly per cleaning-policy § 5.2 "default `european` (Royal Armouries is European-centric collection); fallback `unknown`."

**But at the v_category_sample level, RA is 0 rows.** All 19,008 are excluded by the `weapon_kind IN ('category','named_template')` filter. RA rows have:
- 13,377 `weapon_kind='ammo_or_consumable'` (correct — Step 1 ammo tagging)
- 19,119 `dedup_status='merged_into'` (correct — Step 2 RA TIERED collapse)
- 5,631 `weapon_kind='unknown'` + `dedup_status='canonical'` (these are the surviving canonicals — they should be `category` but are still `unknown`)

**The 5,631 canonical RA rows never got promoted to `weapon_kind='category'`.** Step 2 (RA collapse) only updates `dedup_status`; it does NOT promote `weapon_kind`. Step 4 (named_template routing) is hardcoded to only touch TRPG/MMO/ARPG/SRD sources. Steps 5/6 demote to `unknown` or promote to `unique` selectively. No step promotes the museum canonicals to `category`.

## Q3 — Met Museum, Wikipedia, Wikidata, modern-military

Same pattern as Royal Armouries — labels are correct at the source-row level; rows are excluded from v_category_sample by `weapon_kind='unknown'`:

| source | non-merged rows | weapon_kind='unknown' fraction | v_category_sample rows | lineage labels (substrate-level) |
|---|---|---|---|---|
| met-museum | 7,559 | 3,844 unknown + 3,715 ammo = 100% | 0 | Correct: european 41.2% / east_asian 39.7% / south_asian 6.6% etc. — matches § 5.2 mapping rule on Met `culture` field. Healthy. |
| wikipedia | 8,553 | 8,324 unknown / 229 in (category/named_template/unique) | 220 (only category-promoted ones survive) | Correct labels — but only 2.57% pool retention because Step 4/5/6 doesn't tag wikipedia rows as category by default. |
| wikidata | 12,370 | 12,319 unknown / 29 in (cat/nt/unique) | 3 | Correct labels — unknown 80% reflects wikidata's sparse `country_of_origin` field, not a mapper bug. The unknown fraction matches the structural-tag absence in the data itself (this is a real-data property, not a mapper artifact). |
| odin-army-tradoc | 3,998 | 100% unknown | 0 | Correct: european 31.6% / east_asian 29.5% / unknown 21.7% / middle_eastern 9.2% etc. — matches § 5.2 COUNTRY_CODE_TO_LINEAGE. Healthy. |
| army-recognition | 62 | 100% unknown | 0 | Correct: cross_cultural 60% / european 32% / east_asian 8% — matches § 5.2 fallback. Healthy. |
| cataclysm-dda | 1,599 | 929 unknown / 670 ammo | 1 (cataclysm-dda rows are `weapon_kind='unknown'` because Step 4 excludes them and no category-promotion step touches them) | Correct: cross_cultural 90.8% — matches § 5.2 (post-apocalyptic US-default with global mix). Healthy. |
| gta-v-data | 183 | 100% unknown | 0 | Correct: cross_cultural 100% — matches § 5.2 (GTA register='military_modern', lineage=cross_cultural). Healthy. |

**Across the board, the Step 6.5 lineage assignments are FAITHFUL to cleaning-policy § 5.2.** The historical substrate is not labeled `fantasy_generic` — it is labeled correctly as `european`, `east_asian`, etc. — but it is then excluded from the analysis pool by the weapon_kind filter.

### One real (but small) regex bug to flag

The fextralife-elden-ring source shows 342 rows mapped to `south_american_indigenous` and the nick-aschenbach-dnd-data source shows 156. This is from the CULTURE_REGEX_PATTERNS line `(re.compile(r"\b(inca|peru|andean|amazon|brazil|colombia)", re.I), "south_american_indigenous")` — the substring `\binca` is matching the in-game word **"Incantation"** (Elden Ring's spell category) and "Inca" or "Amazon" mentions in D&D descriptions. This is genuinely a lineage-mapper bug, but it's small-scale (~500 rows mis-mapped to south_american_indigenous when they should be fantasy_generic), and it affects the F2 weight table's `south_american_indigenous` bucket (count=509 in legolas's table, weight=2.98×). Worth fixing but not the 94.46% explanation.

## Q4 — Step 6.5 logic review

Step 6.5 implementation at `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/scripts/08_step6_5_canonical_taxonomy.py` (committed `9e7d14b`). Reviewed line-by-line against cleaning-policy § 5.2.

### Does Step 6.5 respect § 5.2 source-driven rules? — YES.

`extract_culture_for_row` dispatches on `source_library`:

1. **Confidence 1.0 (explicit structured-tag)**: met-museum uses `sp['culture']`; odin-army-tradoc uses `sp['origin_countries']` against `COUNTRY_CODE_TO_LINEAGE`; wikidata uses `sp['country_of_origin']`. These match § 5.2's "Raw tag field(s)" columns. ✅
2. **Confidence 0.7 (description-regex)**: applied to description_text + cultural_lineage_tags + structured place field. CULTURE_REGEX_PATTERNS covers § 5.2's per-source enumeration broadly. ✅ (with the small Incantation false-positive flagged above)
3. **Confidence 0.5 (source-library default)**: TRPG/MMO/ARPG → `fantasy_generic`; cataclysm/gta-v → `cross_cultural`; royal_armouries → `european`; army-recognition → `cross_cultural`. Matches § 5.2 source defaults. ✅
4. **Confidence 0.3 (fallback)**: met-museum without explicit culture → `unknown`; otherwise → `unknown`. Matches § 5.2 fallback. ✅

### Is there a default-to-fantasy_generic fallback path triggering more than it should? — NO.

The default `unknown` is the global fallback. `fantasy_generic` is only assigned when the source_library matches the explicit TRPG/MMO/ARPG/quarantined-game list. There is no "if source unknown, default to fantasy_generic" fall-through. Museum / encyclopedia / modern-military rows that miss all confidence tiers land at `unknown`, not `fantasy_generic`.

This is confirmed by the live data: of 12,370 wikidata rows, 9,912 are `unknown` (not `fantasy_generic`); of 3,998 odin rows, 867 are `unknown`. The fall-through path is `unknown`-not-`fantasy_generic`, exactly as the policy intends.

### So where does the 94.46% fantasy_generic come from?

It comes from **v_category_sample's weapon_kind filter**:

```
CREATE VIEW v_category_sample AS
        SELECT * FROM weapon_knowledge_entries
        WHERE wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported','either')
          AND weapon_kind IN ('category','named_template')
          AND dedup_status IN ('canonical','unprocessed')
          AND source_library NOT IN (...)
```

The `weapon_kind IN ('category','named_template')` clause is doing the structural work that produces the 94.46% figure. Out of 70,693 active rows:
- 14,190 are `named_template` (almost all from TRPG/MMO/ARPG → all `fantasy_generic` per § 5.2 source defaults)
- 2,586 are `category` (mostly TRPG/MMO/ARPG SRD content → `fantasy_generic`)
- 27 are `unique`
- 36,035 are `unknown` (almost all museum / encyclopedia / modern-military rows that never got a category-promotion step)
- 17,857 are `ammo_or_consumable`

v_category_sample only sees the first three groups — and those groups are 98.6% TRPG/MMO/ARPG content, which is dominantly `fantasy_generic` per § 5.2 source defaults. So when Legolas's PCA pulls v_category_sample, it sees a fantasy-monocultural pool **because the pool was filtered down to fantasy-monocultural sources by the weapon_kind filter**, not because Step 6.5 mis-labeled anything.

### The specific code-path responsible

**No code path is broken at Step 6.5.** The structural gap lives in **Step 4 + the v_category_sample view definition**:

1. `scripts/05_step4_named_template_routing.py` line 45–58 — `TRPG_MMO_ARPG_SOURCES` set is hardcoded to the 12 game sources. Sources outside this set (Royal Armouries, Met Museum, Wikipedia, Wikidata, ODIN, army-recognition, cataclysm-dda, gta-v-data) are **never visited** by Step 4. They keep `weapon_kind='unknown'` (the schema default).

2. `scripts/03_step2_ra_tiered_collapse.py` — Step 2 collapses RA rows but only updates `dedup_status`; never promotes survivors to `weapon_kind='category'`.

3. `scripts/01_schema_migration.py` — the `v_category_sample` view's `weapon_kind IN ('category','named_template')` filter then excludes anything that wasn't promoted. There is no equivalent of "if dedup_status='canonical' AND source IS museum/encyclopedia/modern-military AND not FP and not ammo → weapon_kind='category'" anywhere in the pipeline.

The completion summary (`phase-D-completion-summary.md` § 1 footnote) acknowledges this exactly:

> *Includes `unprocessed`-default rows that didn't go through Steps 4-6 routing because they weren't in TRPG/MMO/ARPG sources AND didn't match FP/unique detection. Most are `unprocessed` from museum sources where Step 4 doesn't apply; engine consumption-time filter via v_category_sample handles routing.*

The gap was documented at completion time but not flagged as load-bearing for Phase E because v_category_sample's row count (16,699) looked reasonable for axis discovery. The empirical impact didn't surface until Legolas ran PCA and got 94.46% monocultural input.

## Q5 — Verdict (formal)

**Disposition: (d) — Neither (a), (b), nor (c) as gandalf framed them.**

Restating the three options gandalf authored:

- **(a) Labels are correct → 94.46% is real substrate property** — PARTIALLY WRONG. Labels are correct, but the 94.46% is NOT a real substrate property — it is a **filter-induced property of v_category_sample**. The true substrate is ~24% fantasy_generic / ~36% european / ~12% east_asian / etc.
- **(b) Labels are broken — Step 6.5 has a mapper bug** — WRONG. Step 6.5 mapper is sound. Honors § 5.2 faithfully. (One minor regex FP on "Incantation"/"Amazon" matching south_american_indigenous, ~500 rows; not load-bearing.)
- **(c) Labels are partially broken** — WRONG. Labels are ~99% correct. The structural problem is upstream of labels.

**The actual disposition: (d) v_category_sample's weapon_kind filter excludes the historical substrate.** The 5,631 RA canonical rows + ~3,844 met-museum non-ammo rows + ~8,324 wikipedia rows + ~12,319 wikidata rows + 3,998 odin rows + 62 army-recognition rows + 1,599 cataclysm-dda rows + 183 gta-v-data rows — totaling roughly **35,960 historical/military/encyclopedia rows** — are all sitting at `weapon_kind='unknown'` and never enter Legolas's feature matrix.

If they were promoted to `weapon_kind='category'`, v_category_sample would grow from 16,699 to roughly 52,000+ rows, and the cultural_lineage_canonical distribution would shift to roughly:
- european ~22,800 (44%)
- fantasy_generic ~17,000 (33%)
- east_asian ~8,300 (16%)
- unknown ~12,900 (25% — much of it wikidata's sparse country field)
- middle_eastern ~1,500
- south_asian ~1,500
- cross_cultural ~1,700
- smaller buckets

That is a meaningfully multi-cultural substrate. Whether axes 2–4 stabilize on PCA against THAT pool is the question Phase E-1 actually wanted to ask — but the question hasn't been asked yet, because the pool was wrong.

## Scope of fix + re-run cost estimate (if Matt authorizes Phase-D-bis)

**Minimum-scope fix:** add a new pipeline step (call it Step 6.6 — "category-promotion sweep for non-game sources") that promotes museum/encyclopedia/modern-military canonical rows from `weapon_kind='unknown'` to `weapon_kind='category'` subject to:
- `dedup_status IN ('canonical','unprocessed')`
- `weapon_kind='unknown'` (not ammo, not unique, not FP-demoted)
- `source_library` in the explicit historical-sources list
- canonical_name does not match Step 5's FP-removal patterns

Estimated mutations: ~30,000–36,000 rows promoted from `unknown` to `category`.

**Re-run cost:**
- Step 6.6 implementation + run: ~2–3 hours (matches the complexity of Step 4)
- Step 6.5 re-run not required (lineage labels already correct on these rows)
- Step 7 F4 cross-source merge re-run: yes, because the newly-promoted category rows become merge candidates against existing TRPG/MMO/ARPG category rows. Wall-clock ~2-4 hours given embedding-cache reuse.
- Phase E-1 re-fire on enlarged v_category_sample: cost is legolas's, but the feature matrix grows from 16,699×160 to ~52K×160 — wall-clock proportional, maybe 1–2 hours.

Total estimated wall-clock: ~6–10 hours of pipeline work + Phase E-1 re-fire.

**Backup state needed:** all 9 pre-step backups still on disk at `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/backups/` per math note § 5. No restoration needed for the minimum-scope fix — Step 6.6 is purely additive (only flips `unknown` → `category`; idempotent; rollback-safe).

## What this changes about gandalf's option-set

Reframing the options through the corrected understanding:

- **A1 (accept 1-axis result)** is no longer the "right answer" given the pool was wrong. Axis 1 (register: historical-vs-fantasy) is a real signal — but it surfaced as the dominant axis BECAUSE the pool was 98.6% fantasy-source content, where register splits along nick-aschenbach D&D-rarity-flavor-naming vs. SRD-baseline boundaries. Run the same PCA on the corrected pool and Axis 1 will likely look quite different — possibly register × lineage interactions become the leading axes rather than register-alone.

- **B1 (cap F2 at 100×)** becomes irrelevant. The F2 inverse-frequency weighting is amplifying singleton-lineages by 1518× because the *pool* has 1 north_american_indigenous row — fix the pool (add the 5 wikipedia north_american_indigenous rows + ODIN's 7 + RA's 2 etc.) and the weight collapses to reasonable magnitudes naturally.

- **B2 (drop F2)** becomes irrelevant for the same reason.

- **B3 (drop LSA text)** stays rejected (tourism).

- **B4 (lineage-stratified sample)** + **B4-prime (source-library-stratified)** become moot — the corrected pool has natural multi-cultural balance without stratification.

- **C1 (NMF)** still interesting as a methodology supplement once the pool is correct.

- **D1 (skip axes / 1-axis lock)** is premature — wait to see what PCA returns on the corrected pool.

- **E1 (the audit Matt commissioned)** has revealed the actual bug. The remediation is "Phase-D-bis Step 6.6: category-promotion sweep for non-game sources" — NOT "Phase-D-bis Step 6.5 lineage normalizer fix." The cost is similar to what gandalf estimated.

## Recommendation to Matt (within elrond's stewardship authority, not pre-empting design)

The empirical evidence supports authorizing **Phase-D-bis Step 6.6 category-promotion sweep** as the targeted fix, then re-firing Phase E-1 on the enlarged v_category_sample (~52K rows). This:

1. **Does not invalidate Step 6.5's work** (lineage labels already correct).
2. **Does not require restore-from-backup** (Step 6.6 is purely additive — promotes `unknown` to `category`).
3. **Unblocks B-family options being coherent again** — Phase E-1 re-runs against a substrate that has the multi-cultural composition gandalf's framework was designed for.
4. **Honors Pattern 6 fidelity** — no axis pre-imposition; just expands the pool to actually contain the structural variance the substrate has.

If Matt instead prefers to accept the existing v_category_sample as-is and commit to gandalf's A1+D1 (1-axis register-only) path, that is design-coherent and downstream-sufficient per gandalf's Q3 reasoning — but it leaves ~35,960 rows of museum/encyclopedia/modern-military substrate unexposed to the engine sampler, which is a long-term substrate-density loss for limited methodology gain.

**This is a steward recommendation in elrond's data-domain authority lane. Final decision is Matt's, routed via knight-rider; gandalf retains design-side framing authority.**

— elrond
