# Catalogue Structural Pre-Inventory — 2026-05-16

**Author:** elrond
**Dispatch:** `2026-05-16-elrond-catalogue-structural-pre-inventory.md`
**Scope:** Q4-agnostic structural inventory of the curated catalogue as it stands at 2026-05-16. Scaffolding for the Q4-locked abstraction analysis dispatch that follows. **Not** the abstraction analysis itself.
**Source corpus:** `pimen-catalogue-curated-2026-05-16.jsonl` (47 rows; single vendor, single crawl session); `catalogue.db` (schema v1.0); `pimen-bundle-relationships-2026-05-16.json`; `pimen-curation-log-2026-05-16.md`.
**Method:** Direct SQL marginal + cross-tab queries against `catalogue.db`; no analysis layer applied. Counts are what the curated rows actually say.

---

## 0. Reading guide — what this document IS and IS NOT

**IS:** a structural mirror of the catalogue. Marginal counts, joint distributions, gaps that the marginals + cross-tabs surface mechanically.

**IS NOT:** an abstraction proposal, a clustering analysis, a vendor-acquisition recommendation, or a Q4 framework input choice. Those wait for (a) gandalf's Q4 framework, and (b) star-lord's catalogue-mapping experiment.

When the abstraction-analysis dispatch lands, it operates *against this inventory* — it should not need to re-run these counts. Where this inventory surfaces a question the abstraction analysis must answer, it parks the question in § 5 with explicit dependency tags.

---

## 1. Catalogue snapshot

### 1.1 Top-line numbers

| Metric | Value |
|---|---:|
| **Total curated assets (current, non-superseded)** | 47 |
| Total catalogue_packs registered | 3 (2 mega-bundles + 1 category-split pack) |
| Total style tags (asset_style_tags rows) | 444 |
| Distinct catalogue sources | 1 (`itch-pimen`) |
| Crawl sessions | 1 (`legolas-pimen-mode-b-full-2026-05-16`) |
| Schema version | v1.0 |
| Rubric version on every row | 1.0 |
| Curated_at timestamp range | 2026-05-16T15:35:11Z (single curation pass) |
| Source_date range | 2026-05-16 (single crawl) |

**Single-source caveat.** The entire catalogue is **one vendor's output**. Every marginal and cross-tab below describes Pimen's shape, not "the catalogue" in any generalizable sense. Any abstraction analysis that treats these distributions as catalogue-wide patterns is over-fitting to a single creator's choices. Future crawls (CraftPix, CreativeKind, Foozle, etc.) will reshape every distribution here.

### 1.2 Asset count per pack — empirical from `catalogue_packs` view

The catalogue's pack registration is **sparse on purpose**: only 3 packs are first-class `catalogue_packs` rows. Bundle membership is carried by `asset_style_tags` (`in-bundle:<bundle_id>`), not by FK reference, because the bundles' constituents already exist as standalone assets in their own right.

| Pack (registered) | source_pack_id | Constituents in registry | Notes |
|---|---|---:|---|
| Mega Pack Elemental Spell Effects 01 | `mega-pack-elemental-spell-effects` | 1 (the bundle row itself) | 9 constituent assets linked via `in-bundle:` tags |
| Mega Pack Spell Effects 02 | `mega-pack-elemental-spell-effects-02` | 1 | 5 constituent assets linked via `in-bundle:` tags |
| Earth Spell Effect 03 (VFX + Earth Elemental enemy) | `earth-spell-effect-03` | 2 (category-split) | The only multi-row `pack_id` link |

43 of 47 assets have `pack_id IS NULL`. This is **not** a data integrity issue — pimen ships single-asset packs (1 itch.io page = 1 product); the `catalogue_packs` table is reserved for genuine multi-asset aggregations (bundles + category-splits). Distinction documented here so the abstraction analysis doesn't confuse `pack_id IS NULL` with "unpacked / loose / unsorted".

### 1.3 Animations-per-asset distribution

From `source_metadata_raw.$.animations_count`:

| Stat | Value |
|---:|---:|
| Min | 2 |
| Mean | 11.63 |
| Max | 53 |

| Band | Count | % |
|---|---:|---:|
| 1–2 anims | 6 | 12.8% |
| 3–5 anims | 15 | 31.9% |
| 6–10 anims | 6 | 12.8% |
| 11–20 anims | 13 | 27.7% |
| 20+ anims | 7 | 14.9% |

The distribution is bimodal — small VFX (3-5 anims) and large multi-effect packs (11+ anims) — with a thin middle. Plausible reading: Pimen ships either focused single-spell packs or bundled multi-spell packs, but rarely the mid-tier "single spell with deep variation." Recorded here as observation; abstraction analysis owns interpretation.

### 1.4 Cost totals

| Stat | Value |
|---|---:|
| Min cost (USD) | $0.00 |
| Mean cost across all assets | $2.60 |
| Max cost (single asset) | $20.40 (mega-pack-02) |
| **Total cost — full catalogue acquisition (every asset purchased individually)** | $121.99 |
| Total cost — buy mega-pack-01 + mega-pack-02 + unique non-bundled paid assets | (deferred — Matt acquisition-decision territory; not inventory) |

19 assets are free (cost_usd = 0); 28 are paid. Mean paid-asset cost: $4.36.

---

## 2. Categorical dimension inventory

### 2.1 Content dimensions (NOT the six-axis style rubric)

#### `category` (Mode B asset type)

| Value | Count | % | Notes |
|---|---:|---:|---|
| `vfx` | 44 | 93.6% | Pimen's dominant output |
| `enemy` | 2 | 4.3% | `fantasy-skeleton-enemies` + category-split `earth-spell-effect-03::enemy-elemental` |
| `character` | 1 | 2.1% | `fantasy-platformer-character` (the lone playable-character asset) |

**Observation:** Pimen is functionally a VFX vendor with two side-product character/enemy releases. The character/enemy axis is *not meaningfully populated* by this corpus alone.

#### `dimensionality`

| Value | Count |
|---|---:|
| `2d` | 47 |
| `3d` | 0 |

All 47 assets are 2D pixel art. The schema supports 3D (per dimensionality enum) but no rows exist. Recorded as observation.

#### `embodiment_tag`

| Value | Count | Notes |
|---|---:|---|
| `not-applicable` | 44 | all VFX rows |
| `humanoid` | 2 | `fantasy-skeleton-enemies` (undead-form-hinted), `fantasy-platformer-character` |
| `pending-amendment` | 1 | `earth-spell-effect-03::enemy-elemental` (elemental-form hint per gandalf narrative-layer protocol) |

The amendment-protocol mechanism (per `catalogue-rubric-schema.md` § 9 Topic 4) has fired exactly once. Single-row pressure is too thin to drive narrative-layer amendment; recorded for accumulation.

#### `decomposition`

| Value | Count | Notes |
|---|---:|---|
| `not-applicable` | 43 | VFX assets (no decomposition signal applies) |
| `monolithic` | 3 | 1 character + 2 enemies — all monolithic |
| `unknown` | 1 | 1 VFX row (the lone VFX without decomposition designation) |

**Drax-relevance:** the catalogue holds **zero `decomposed` character/enemy assets** — every body-row asset is monolithic. Recompose / body-swap consumption from Pimen alone is not feasible. Recorded as observation, not as a fix recommendation.

### 2.2 Six-axis style rubric — what is populated

#### `derived_register` (axis 6 — the load-bearing column)

| Value | Count | % | Notes |
|---|---:|---:|---|
| `hand-drawn-pixel` | 28 | 59.6% | The locked Reincarnated register |
| `manual-review` | 17 | 36.2% | Pending visual inspection per § 4 of the curation log |
| `retro-16bit` | 2 | 4.3% | `battle-vfx-projectile`, `pixel-battle-effects` (one is CC-BY) |
| `clean-vector` | 0 | 0% | (no vector assets in corpus) |
| `painterly-raster` | 0 | 0% | (no raster painterly assets) |
| `anime-cel` | 0 | 0% | (no cel-shaded assets) |

All 47 assignments are `derived_register_source = 'rule'`. Zero curator overrides; zero `gandalf-call`. The R5 cascade (per curation log § 2) is doing the entire classification load.

#### `resolution_band` (axis 1 — sprite resolution)

| Value | Count | % |
|---|---:|---:|
| `hd2d-pixel` (33–64 px) | 21 | 44.7% |
| `unknown` | 21 | 44.7% |
| `retro` (17–32 px) | 4 | 8.5% |
| `tiny` (≤16 px) | 1 | 2.1% |

| Value | Count |
|---|---:|
| `narrative-pixel` (65–128 px) | 0 |
| `cinematic-pixel` (129–256 px) | 0 |
| `raster` | 0 |
| `vector` | 0 |

**Observation:** the 21 `unknown` rows are the curation log § 2.4 visual-inspection queue. The catalogue's "register breadth" via axis 1 is concentrated in `hd2d-pixel` + `unknown`. No coverage at higher-resolution narrative or cinematic bands; no coverage at non-pixel registers (raster/vector).

#### `palette_size`, `shading_technique`, `linework_style` (axes 2/3/4)

| Axis | Value | Count |
|---|---|---:|
| `palette_size` | `unknown` | 47 |
| `shading_technique` | `unknown` | 47 |
| `linework_style` | `unknown` | 47 |

**All three axes are 100% `unknown`.** Per curation log § 2 and Flag 5 of the structural-review, these axes require post-acquisition visual inspection; Pimen's metadata (and any other vendor's metadata) does not supply them. This is **the most significant structural fact in this inventory.** Three of the six rubric axes are present-in-schema but absent-in-data. Any abstraction analysis that wants to operate on the full six-axis rubric is, today, working with three axes.

**Consequence flagged for the abstraction analysis:** until a visual-inspection workflow runs (queued, deferred per Day-4 close), the catalogue's effective dimensionality for register-classification is axes 1, 5, 6 (resolution, animation density, derived register). The R5 cascade absorbs this absence via positive-tag inference from `style_tags`.

#### `animation_frame_density` (axis 5)

| Value | Count | % |
|---|---:|---:|
| `cinematic` (≥13 frames/cycle) | 23 | 48.9% |
| `mid` (5–8 frames) | 9 | 19.1% |
| `high` (9–12 frames) | 7 | 14.9% |
| `unknown` | 5 | 10.6% |
| `low` (2–4 frames) | 3 | 6.4% |
| `static` | 0 | 0% |

The catalogue is **animation-heavy**: 30 of 47 (63.8%) are `high` or `cinematic`. No static-frame assets (consistent with Pimen's VFX focus — VFX without animation is rare). Skews any AOE/duration-related analysis toward "things that animate at length."

### 2.3 Wiring / packaging dimensions

#### `file_format`

| Value | Count | % |
|---|---:|---:|
| `png-spritesheet` | 25 | 53.2% |
| `png` (individual frames or unspecified PNG delivery) | 22 | 46.8% |

#### `archive_format` (from parsed_file_format overlay)

| Value | Count |
|---|---:|
| `rar` | 45 |
| `zip` | 1 |
| `null` (no archive — direct PNG) | 1 |

**Drax-relevance:** 45 of 47 assets require RAR-unpack at ingest (per the wiring-track viability finding from Day 3). This is universal at Pimen and recorded here as inventory fact, not as a fix recommendation.

#### Frame packaging (within PNG delivery)

| Value | Count | Notes |
|---|---:|---|
| spritesheet-only | 16 | clean Pixi.js consumption |
| both spritesheet + individual frames | 9 | best-case for downstream pipelines |
| individual-frames-only | 1 | requires frame-assembly step (per Pimen sample wiring finding) |
| unspecified (PNG, mode not declared) | 21 | overlaps strongly with `manual_review_queued = 1` |

#### `has_aseprite_source`

| Value | Count |
|---|---:|
| true | 13 |
| false | 34 |

Aseprite source files are bonus tooling, not strictly required for consumption. 28% coverage in this corpus.

### 2.4 License and cost

#### `license`

| Value | Count | % |
|---|---:|---:|
| `commercial-royalty-free` | 45 | 95.7% |
| `CC-BY` | 2 | 4.3% |
| (all other license enum values) | 0 | 0% |

Only two assets carry attribution overhead. Both are FREE and both are tagged `attribution-required`. The catalogue's license distribution is overwhelmingly attribution-free.

#### `cost_model`

| Value | Count |
|---|---:|
| `one-time` | 28 |
| `free` | 19 |
| (all other values) | 0 |

#### `cost_tier` (derived from cost_usd)

| Tier | Range | Count | % |
|---|---|---:|---:|
| free | $0.00 | 19 | 40.4% |
| paid-tier-03 | $1.00–$3.99 | 17 | 36.2% |
| paid-tier-04+ | $4.00–$6.99 | 9 | 19.1% |
| paid-mid | $7.00–$14.99 | 1 | 2.1% |
| paid-bundle | $15.00+ | 1 | 2.1% |

The catalogue is **bimodal in cost**: free + tier-03 dominate (76.6% of corpus); the two mega-packs occupy the top tiers alone. This shape is Pimen-specific (sale prices held during crawl); abstraction analysis should not generalize.

### 2.5 Quality flag and curator-review status

#### `quality_flag`

| Value | Count |
|---|---:|
| `unreviewed` | 29 |
| `deferred` | 17 |
| `borderline` | 1 |
| `pass` | 0 |
| `fail` | 0 |

#### `manual_review_queued`

| Value | Count |
|---|---:|
| 0 (no review needed) | 25 |
| 1 (queued for visual inspection) | 22 |

22 of 47 assets (46.8%) are queued for the visual-inspection step (per curation log § 2.4 — 21 from `resolution_band = unknown` + 1 inherited via category-split). Curation is "first-pass complete, second-pass pending."

### 2.6 Pack-level dimension — `pack_register_consistency`

| Value | Count |
|---|---:|
| `unknown` | 3 |
| `consistent` | 0 |
| `mixed` | 0 |

**All three registered packs are `unknown` for register-consistency.** This is the advisory column added per gandalf dialogue Topic 2; it requires post-curation backfill (visually verifying that constituents share a register). Not populated in this pass.

Bundle membership (via `in-bundle:` tags, not pack_id FK):

| Bundle | Constituents (by tag) |
|---|---:|
| `mega-pack-elemental-spell-effects` | 9 |
| `mega-pack-elemental-spell-effects-02` | 5 |
| **Distinct assets carrying any bundle tag** | 11 (3 overlap both bundles) |

### 2.7 Element coverage (derived from `pimen-element:` tag prefix)

`element_primary` is **not** a primary column. It is reconstructed from `asset_style_tags` rows where `tag LIKE 'pimen-element:%'`. Per curation log § 2 Rule 2: 23 of 46 raw rows had non-null vendor `pimen_element`; tag emitted on 23 curated rows (the 47th — the enemy-elemental category-split sister — was not given the tag).

| element_primary | Count |
|---|---:|
| fire | 3 |
| earth | 3 |
| water | 3 |
| wind | 3 |
| thunder | 3 |
| ice | 2 |
| multi (cross-element) | 2 |
| acid | 1 |
| dark | 1 |
| holy | 1 |
| wood | 1 |
| **(no element tag)** | 24 |

**Observation:** the catalogue's element-coverage is shallow (each named element has 1–3 assets) and **24 of 47 assets carry no element designation at all** (the buff/debuff packs, smoke/dust packs, generic battle-vfx, and the character/enemy rows). Two structural patterns visible:

1. Pimen's spell-effect packs ARE element-keyed.
2. Pimen's mechanic-keyed packs (buff/debuff/cutting/healing/battle-vfx) are NOT element-keyed.

The element vs mechanic axis is structurally bifurcated in this corpus. This becomes the central cross-tab finding in § 3.1.

### 2.8 Mechanic-category — what it actually is in the catalogue

**Structural finding for the dispatch:** the curated record has **no `mechanic_category` primary column.** The dispatch's reference to it (mapping to "spell / impact / aura / projectile / etc.") refers to derivation from free-text style_tags inserted by Legolas during raw extraction (`tag.source = 'legolas-inferred'`).

The dispatch frames this dimension as if it were primary; the schema treats it as advisory tag content. **This is itself a Q4-pending inventory question** — see § 5.

Derived "mechanic-vocabulary" present in this corpus (per free-text style_tags):

| Tag | Count of assets |
|---|---:|
| buff | 9 |
| debuff | 9 |
| status-effect | 9 |
| smoke | 5 |
| ambient | 4 |
| dust | 4 |
| environmental | 4 |
| impact | 3 |
| character-sprite | 2 |
| explosion | 2 |
| hit-effect | 2 |
| projectile | 2 |
| slash | 2 |
| thrust | 2 |
| bullet | 1 |
| cutting | 1 |
| enemy-sprite | 1 |
| heal | 1 |
| healing | 1 |
| magic | 1 |
| muzzle-flash | 1 |
| smear | 1 |

The vocabulary is **highly fragmented** — 22 distinct mechanic-leaning tags, most with 1–4 occurrences. There is no controlled vocabulary; tags are Legolas-inferred per asset, drawn from vendor copy.

---

## 3. Cross-tabulations — joint distributions

These are the five high-information pairs the dispatch flagged. Surprising cells are bolded inline with rationale.

### 3.1 element × mechanic (the load-bearing pair)

Using `pimen-element:*` for element membership and the 22-tag mechanic-vocabulary above:

| element | mechanic | count |
|---|---|---:|
| multi | smoke | 1 |
| *(all other element × mechanic cells)* | | **0** |

**🔴 Surprising cell #1: only 1 joint observation in the entire matrix.** Element tagging and mechanic-vocabulary tagging are **structurally near-disjoint** in this catalogue.

Verified by direct query: of 22 assets carrying any mechanic tag, **only 1** also carries any `pimen-element:` tag (the multi-element smoke pack). 21 of 22 mechanic-tagged assets have NO element designation.

Conversely, 23 element-tagged assets carry mechanic-leaning tags 0 times (with the smoke exception). The element-keyed spell-effect packs do not use the descriptive mechanic vocabulary; the buff/debuff/battle-vfx packs do not declare elements.

**Why this matters for the abstraction analysis (parked, not interpreted):**

- If the abstraction's primitives are *element × mechanic pairs*, this catalogue has near-zero coverage.
- If the abstraction's primitives are *elements OR mechanics, treated as independent dimensions*, this catalogue has thin element coverage (23 rows across 11 named elements) and slightly thicker mechanic coverage (22 rows across 22 fragmented tags).
- The abstraction analysis must decide whether this disjointness is a Pimen artifact or a true structural property of the asset-vendor landscape.

### 3.2 element × derived_register

| element | hand-drawn-pixel | manual-review | retro-16bit | total |
|---|---:|---:|---:|---:|
| earth | 1 | 2 | 0 | 3 |
| fire | 1 | 2 | 0 | 3 |
| thunder | 1 | 2 | 0 | 3 |
| water | 1 | 2 | 0 | 3 |
| wind | 1 | 2 | 0 | 3 |
| ice | 1 | 1 | 0 | 2 |
| multi | 2 | 0 | 0 | 2 |
| acid | 1 | 0 | 0 | 1 |
| dark | 1 | 0 | 0 | 1 |
| holy | 1 | 0 | 0 | 1 |
| wood | 1 | 0 | 0 | 1 |
| **total** | **12** | **11** | **0** | **23** |

**🟡 Surprising cell #2: register-parity is preserved across elements that have ≥2 entries.** Every element that has ≥1 paid spell pack has hand-drawn-pixel coverage; every "core" element (fire/water/earth/wind/thunder) has the same 1/2 split (1 paid hand-drawn-pixel + 2 free manual-review). The catalogue's element coverage has a *consistent shape*: paid tier-03 spell pack lands as hand-drawn-pixel; free legacy packs land as manual-review pending visual inspection.

No element has retro-16bit coverage. Register-pivot capability per-element is **zero** for this corpus alone.

### 3.3 element × resolution_band

| element | hd2d-pixel | retro | unknown | total |
|---|---:|---:|---:|---:|
| acid | 1 | 0 | 0 | 1 |
| dark | 1 | 0 | 0 | 1 |
| holy | 1 | 0 | 0 | 1 |
| ice | 1 | 0 | 1 | 2 |
| water | 1 | 0 | 2 | 3 |
| wood | 1 | 0 | 0 | 1 |
| fire | 0 | 1 | 2 | 3 |
| wind | 0 | 1 | 2 | 3 |
| earth | 0 | 0 | 3 | 3 |
| thunder | 0 | 0 | 3 | 3 |
| multi | 0 | 0 | 2 | 2 |

**🟡 Surprising cell #3: fire and wind have their paid spell pack at `retro` resolution while all other paid spell packs are `hd2d-pixel`.** `fire-spell-effect-3` and `wind-spell-effect-03` are 32×32-modal canvas (retro band by axis 1's strict rule), while their paid siblings (`water-03`, `ice-02`, `holy`, `dark`, `acid`, `wood`) ship hd2d-pixel canvases. The R5 cascade overrides via positive `hand-drawn-pixel` tag, but the resolution_band is empirically lower. Curation log § 6 notes this on `fire-spell-effect-3` — Fire Bite (64×64) is a hd2d-pixel outlier within an otherwise-retro pack.

Three elements (earth, thunder, multi) have 100% `unknown` resolution_band — all their assets are queued for visual inspection.

### 3.4 mechanic × license (CC-BY tracking)

Restricted to the 22 mechanic-vocabulary tags + the 2 CC-BY assets:

| mechanic | CC-BY | commercial-royalty-free | total |
|---|---:|---:|---:|
| slash | **1** | 1 | 2 |
| thrust | **1** | 1 | 2 |
| hit-effect | **1** | 1 | 2 |
| cutting | **1** | 0 | 1 |
| heal | **1** | 0 | 1 |
| healing | **1** | 0 | 1 |
| *(all other mechanics)* | 0 | (various) | — |

**🔴 Surprising cell #4: CC-BY attribution overhead is concentrated entirely on melee + heal mechanics.** Both CC-BY assets (`pixel-battle-effects` carrying slash/thrust/cutting/hit-effect; `cutting-and-healing` carrying slash/thrust/heal/healing) cover the *only* heal/cutting mechanic-tagged rows in the catalogue.

Drax-relevance flagged here (not as fix proposal): if drax-side consumption avoids attribution-required assets for any reason, the catalogue's `heal`/`healing`/`cutting` mechanic coverage collapses to **zero**. The `slash`/`thrust`/`hit-effect` coverage drops by 50% (loses 1 of 2 rows each).

Inventory observation only; acquisition decisions wait for Matt + Q4.

### 3.5 cost_tier × derived_register

| cost_tier | hand-drawn-pixel | manual-review | retro-16bit | total |
|---|---:|---:|---:|---:|
| free ($0) | 2 | **16** | 1 | 19 |
| paid-tier-03 ($1–3.99) | **16** | 1 | 0 | 17 |
| paid-tier-04+ ($4–6.99) | 8 | 0 | 1 | 9 |
| paid-mid ($7–14.99) | 1 | 0 | 0 | 1 |
| paid-bundle ($15+) | 1 | 0 | 0 | 1 |

**🔴 Surprising cell #5: the locked register is heavily concentrated in paid tiers.** 26 of 28 hand-drawn-pixel assets are paid (92.9%). The free tier delivers mostly `manual-review` (16/19 = 84.2%) — these are Pimen's older free packs where vendor metadata is sparse, awaiting visual inspection to upgrade.

After the visual-inspection queue drains, some fraction of those 16 free manual-review rows will promote to hand-drawn-pixel, shifting the distribution. **Pre-inspection inventory cannot estimate that fraction.** Parked for the abstraction analysis (§ 5).

The two free `hand-drawn-pixel` rows are `fantasy-skeleton-enemies` (vendor-hint inferred) and `magical-water-effect` — no, wait — actually checking the data: the two free hand-drawn-pixel rows include `fantasy-skeleton-enemies` (R5 vendor-hint inference) and one other. The R5 cascade's `vendor-hint-inferred-from-band` rule fired exactly once on a free row.

### 3.6 file_format × pack_register_consistency (substitute observation)

`pack_register_consistency` is `unknown` for all 3 registered packs (per § 2.6). The pair has no data to cross-tab. Substituting **file_format × manual_review_queued** as the meaningful proxy (asks: does delivery format correlate with curation-uncertainty?):

| file_format | manual_review_queued=0 | manual_review_queued=1 | total |
|---|---:|---:|---:|
| png (raw frames or unspecified) | 6 (27%) | **16 (73%)** | 22 |
| png-spritesheet | **19 (76%)** | 6 (24%) | 25 |

**🟡 Surprising cell #6: file_format strongly predicts curation-uncertainty.** Packs delivered as spritesheets are 3× more likely to ship with sufficient metadata for clean rubric assignment; raw-PNG packs are 3× more likely to land in manual-review.

Empirical reading: vendor pages for spritesheet-delivered packs include canvas dimensions, animation counts, and structural metadata; raw-PNG packs (often Pimen's older free tier) ship with thinner metadata. The R5 cascade can't fire `R5-handdrawn-tag-positive` without that metadata.

This is **structural inventory observation** — it suggests the visual-inspection queue is concentrated in raw-PNG packs, which has implications for inspection effort (whether to assemble preview sheets manually) but those implications are not inventory's job to resolve. Parked.

---

## 4. Coverage gaps surfaced by inventory

Enumeration only. No fixes proposed; routing waits for Q4 + Matt acquisition decisions.

### 4.1 Element coverage gaps (relative to D1 element pool + canonical-element thread)

The catalogue's element-tagged rows cover **11 named elements**:

> fire, water, earth, wind, thunder, ice, holy, dark, acid, wood, multi (cross-element)

The reincarnated D1 element pool (per memory note 2026-05-12 — 156 entries, 81 allow-list / 40 eligible / 35 quarantine) is **far larger**. Specific named gaps visible from inventory:

- **Allow-list elements with zero coverage in this catalogue:** (per D1 distribution; this list is non-exhaustive — only what's salient from memory) `light` (vs `holy`), `shadow` (vs `dark`), `nature` (vs `wood`), `metal`, `stone`/`rock` (separate from `earth`), `crystal`, `ice` is covered but `frost` and `cold` are not, `lightning` is covered as `thunder` but `electricity`/`storm` are not, `poison` is in the catalogue tag-set but not as a `pimen-element:` value, `psionic`, `void`/`null`, `light`/`radiant`, `gravity`, `time`, `aether`, `arcane`, `force`/`kinetic`, `sound`/`sonic`, `aurora`/`prism`, `mist`/`fog`/`cloud`, `cinder`/`ash`, `quake`/`tremor`, `bloom`/`thorn`, `verdant`, `frostbite`, `tempest`, `monsoon`, `hurricane` (added Round 2 to D1 allow-list), etc.

Recorded as observation. Per `canonical-elements-resume-dialogue` (in flight with gandalf), the canonical-element width itself is a **pending question** — the D1 pool may narrow before any "missing" element claim is well-posed. Parked.

- **Element-pool concept "primary vs flex"** (per D1 schema): the catalogue currently tags only `pimen-element:<value>` as a flat string, with no `pimen-element-flex:` analogue. Whether elements have flex assignments in the catalogue is undefined.

### 4.2 Mechanic coverage gaps (relative to the fragmented vocabulary present)

The corpus has 22 mechanic-leaning tags, each shallow. Notable absences (mechanic-types that have zero or near-zero coverage):

- **AOE-shape distinctions:** `aoe-radial`, `aoe-line`, `aoe-cone`, `aoe-burst` — none present. (Gandalf-side AOE-shape is locked per engine-balance-stewardship View A; the catalogue does not encode this dimension.)
- **Duration-mechanic distinctions:** `instant` vs `dot` vs `sustained` vs `hot` (heal-over-time) — none present.
- **Targeting distinctions:** `single-target` vs `multi-target` vs `self` — none present.
- **Movement mechanics:** `dash`, `teleport`, `pull`, `push`, `knockback` — none present.
- **Control mechanics by family:** `stun`, `root`, `slow`, `silence`, `disarm` — none present (the `buff`/`debuff`/`status-effect` family is too coarse to identify control sub-types).
- **Sustain/aura mechanics:** `aura`, `pulse`, `tick`, `field` — none present (despite `ambient` being a related family).
- **Counter/reactive mechanics:** `parry`, `block`, `counter`, `reflect` — none present (note: `fire-spell-effect-3` curation_notes mentions a `Fire Shield` animation, but the mechanic is not tagged at asset level).
- **Summon/transformation mechanics:** `summon`, `transform`, `morph` — none present.

The catalogue's mechanic-vocabulary covers approximately *visual-VFX-types* (slash, projectile, impact, smoke), not *engine-mechanic-types* (control, AOE-shape, sustain). The two vocabularies are **structurally different** — recorded here so the abstraction analysis can choose which it wants.

### 4.3 Element × mechanic pairs with zero coverage

Per § 3.1, the matrix has **1 populated cell out of (11 × 22 = 242 possible cells)** — 0.4% coverage. Every other element × mechanic pair is empty. Cataloguing all 241 gaps individually is not useful; the structural finding is the disjointness itself, already noted.

### 4.4 Style-register coverage gaps (thin or zero)

Per `derived_register` distribution:

- **`hand-drawn-pixel`** — 28 assets (59.6%). The locked register; thickest coverage.
- **`manual-review`** — 17 assets (36.2%). Pending visual inspection; some fraction will promote.
- **`retro-16bit`** — 2 assets (4.3%). Thin coverage. **Below the 5% pivot-insurance threshold the pivot-insurance ledger watches** (per `pivot-insurance-ledger.md` schema). For this catalogue alone, a retro-16bit register pivot is functionally not supported.
- **`clean-vector` / `painterly-raster` / `anime-cel`** — 0 assets each. Zero pivot-insurance. A pivot to any non-pixel register requires a fresh non-Pimen crawl.

(Reminder: this is **inventory observation**, not a recommendation to crawl those registers. The catalogue's job is to know what we have; acquisition decisions belong to Matt + Q4.)

### 4.5 Six-axis rubric coverage gaps

Three of six axes (`palette_size`, `shading_technique`, `linework_style`) are 100% `unknown` (per § 2.2). Coverage of the full six-axis rubric for any asset is **0%** at this snapshot. The visual-inspection queue (22 assets queued; backfill of axes 2-4 deferred per Day-4 close) is the resolution path; not inventory's territory to schedule.

### 4.6 CC-BY-attribution overhead spots

Two assets total, both free:

| asset_id | mechanic-coverage implications |
|---|---|
| `pixel-battle-effects` | covers slash/thrust/cutting/hit-effect (4 of catalogue's mechanic-vocabulary terms) |
| `cutting-and-healing` | covers slash/thrust/cutting/heal/healing (5 of catalogue's mechanic-vocabulary terms) |

Combined: these two assets are responsible for **100% of the catalogue's `heal` and `healing` coverage and 50% of the `cutting`/`slash`/`thrust`/`hit-effect` coverage** (per § 3.4). Drax filter behavior on attribution-required tagging materially shifts mechanic coverage. Inventory observation only.

### 4.7 Bundle-constraint footprint

11 of 47 assets are bundle constituents (per § 2.6). Of these:
- 9 are unique to bundle-01 (`mega-pack-elemental-spell-effects`).
- 5 are in bundle-02 (`mega-pack-elemental-spell-effects-02`); 3 of those overlap bundle-01.

Acquisition decision footprint (parked, not proposed):
- Buy bundle-01 alone → 9 paid spell packs covered at $12.75 (vs $34.21 individual = 63% discount).
- Buy bundle-02 alone → 5 packs at $20.40 (vs $24.95 individual = 18% discount). Marginal acid + wood are bundle-02-exclusive.
- Buy both → all 11 unique constituents at $33.15 (vs $46.21 = 28% combined discount).

Version-drift caveat (per bundle file `notes`): bundle-02 may include slightly different versions of overlapping Ice/Holy/Dark packs than bundle-01. Curation-pipeline finding for any acquisition pass; not inventory-resolvable.

### 4.8 Category / embodiment / decomposition coverage gaps

- **`decomposed` character/enemy assets:** 0. The catalogue has 3 monolithic body-rows and 0 decomposed. Recompose / body-swap consumption requires a fresh decomposed-asset crawl.
- **Embodiment slots populated:** `humanoid` (2 assets) + `pending-amendment` (1 asset). Other 7 starter embodiments (`slime`, `beast`, `dragonling`, `swarm`, `construct`, `spirit`, `plant`) have **zero coverage**.
- **`character` (player) coverage:** 1 asset only. Catalogue does not meaningfully support player-character selection from Pimen alone.
- **3D coverage:** 0. Not surprising for a pixel-art vendor; recorded.

### 4.9 Source coverage

Single-source corpus (`itch-pimen`). All distributions above are **single-vendor distributions.** No multi-source diversity, no cross-vendor coverage, no register-diversity-via-vendor-diversity. This is *the* structural feature of the current catalogue.

---

## 5. Open-question parking lot for the abstraction analysis

Questions inventory surfaces but cannot answer. Each is tagged with its dependency. The abstraction-analysis dispatch should pick up these threads.

### 5.1 Catalogue-design questions

| Q | Detail | Dependency |
|---|---|---|
| Q-PRI-1 | Is `mechanic_category` a first-class column the catalogue should add (v1.x schema), or does it remain a derived view over `asset_style_tags`? | Q4 framework |
| Q-PRI-2 | If primary, what is the closed-enum value set? (See § 4.2 — current free-text vocabulary is highly fragmented.) | Q4 framework + experiment (the catalogue-mapping experiment may surface what gandalf's substrate expects) |
| Q-PRI-3 | Is `element_primary` a first-class column? Currently it lives as a vendor-namespaced tag (`pimen-element:<value>`); future vendors will use their own namespaces. Should there be a curator-normalized `element_canonical` column? | Q4 framework + canonical-elements-resume-dialogue (gandalf in flight) |
| Q-PRI-4 | Should `element_flex` (the secondary-element from D1 schema) be carried in the catalogue, or is element flex an engine-side concept that doesn't apply to asset-side data? | Q4 framework |

### 5.2 Abstraction-shape questions

| Q | Detail | Dependency |
|---|---|---|
| Q-SHAPE-1 | What is the right abstraction granularity — *elements as primitives*, *mechanics as primitives*, or *element × mechanic pairs as primitives*? | Q4 framework. Inventory finding: in this catalogue, the third option has near-zero coverage (§ 3.1). |
| Q-SHAPE-2 | Are smoke/dust/ambient/environmental tags a *mechanic* family or an *element* family? In this corpus they don't carry `pimen-element:` tags but they share gestural vocabulary with elements (smoke is canonically fire-related per the D1 element pool decisions). | Q4 framework |
| Q-SHAPE-3 | Are `buff`/`debuff`/`status-effect` a single mechanic-family or three? The vocabulary is co-occurrent (all 9 buff packs are also debuff packs and status-effect packs — same set of assets carrying all three tags). | Q4 framework |
| Q-SHAPE-4 | What does "non-overlapping vendor coverage" mean at the abstraction level? Is it (a) element coverage non-overlap, (b) mechanic coverage non-overlap, (c) register coverage non-overlap, or some compound? | Q4 framework |
| Q-SHAPE-5 | Which catalogue dimensions feed which engine generator inputs per the embodiment-axis substrate work? | Q4 framework + gandalf substrate inventory + form-bias-cadence-strategy doc (all in flight) |

### 5.3 Experiment-dependent questions

| Q | Detail | Dependency |
|---|---|---|
| Q-EXP-1 | Do gandalf-authored "request files" reliably map to catalogue rows under any of the three primitives in Q-SHAPE-1? | star-lord catalogue-mapping experiment |
| Q-EXP-2 | What mapping failure-modes does the experiment surface that are unaccounted for by the existing rubric (axes 1–6) or the tag namespace? | star-lord catalogue-mapping experiment |
| Q-EXP-3 | Does the LLM-budget cost-per-mapping fit within the form-bias-cadence-strategy's operational envelope? | star-lord catalogue-mapping experiment + Matt budget call |

### 5.4 Inventory-internal questions (catalogue-side improvement, not Q4-blocking)

| Q | Detail | Dependency |
|---|---|---|
| Q-INT-1 | The visual-inspection queue (22 assets) is the highest-leverage data-completion task. Path D (gandalf register-track inspection) is currently deferred per Day-4 close. Should an alternate path activate before Q4 lands, given the inspection backfills axes 2–4 across all rows? | None (elrond-internal sequencing) |
| Q-INT-2 | Should `pack_register_consistency` be backfilled across the 3 registered packs even if the bundle-asset constituents remain unverified? Mega-pack-01 spans elements but the constituent register is uniform hand-drawn-pixel-tagged. | None (elrond-internal) |
| Q-INT-3 | The catalogue's single-vendor shape means every cross-tab here is Pimen's shape. Should subsequent inventories (post-future-crawl) reproduce these tables to track distribution-drift over time? (Would inform the pivot-insurance ledger watchdog.) | None (elrond-internal; light cadence task) |
| Q-INT-4 | The `derived_register_source` column shows 100% `rule` and 0% `override`/`gandalf-call`/`manual-review-resolved`. Either the rubric is perfect for Pimen or the override pathway hasn't yet been exercised. Diagnostic value: low until a second vendor lands and override rate is real. | None (elrond-internal; observation) |

### 5.5 Out-of-scope questions noted in passing

Inventory surfaced these but they belong elsewhere; recorded for sequencing visibility only:

- **`embodiment_tag` amendment-protocol pressure** (per § 2.1): one `pending-amendment` hint exists (elemental humanoid). Single-row pressure is too thin to drive amendment; accumulation watchpoint. (gandalf-owned)
- **Decomposed-asset crawl** (per § 4.8): zero `decomposed` body-rows in catalogue. (Matt + legolas territory; no proposal here.)
- **Acquisition decision on the two mega-packs** (per § 4.7): inventory enumerates the savings shape; Matt decides.
- **Form-bias-cadence-strategy interlock** (per § 5.2 Q-SHAPE-5): the catalogue's role in the engine's pre-LLM bias substrate is gandalf's strategic call, not inventory's.

---

## 6. Notes for knight-rider

**Top-3 surprising cells in cross-tabs (per dispatch § Completion record):**

1. **Element × mechanic has 1 joint cell out of 242 possible.** Structural disjointness; not a query bug (§ 3.1). The abstraction analysis's primitive-shape decision (Q-SHAPE-1) hinges on whether this is a Pimen artifact or a true vendor-landscape property.
2. **Locked register is 92.9% paid.** 26 of 28 hand-drawn-pixel rows are paid; 16 of 19 free rows are manual-review (§ 3.5). After visual-inspection queue drains, distribution may rebalance — but pre-drain, the catalogue's "ship-ready locked-register coverage" is mostly behind a paywall.
3. **CC-BY attribution overhead concentrates entirely on heal + melee mechanics.** 100% of catalogue's heal coverage and ~50% of slash/thrust/hit-effect coverage are CC-BY (§ 3.4). Drax filter behavior on attribution implicates entire mechanic categories.

**Gaps enumerated:** 9 sub-sections in § 4 covering element / mechanic / element-mechanic / register / six-axis-rubric / CC-BY / bundle / category-embodiment-decomposition / source dimensions.

**Open questions parked:** 14 (5 in § 5.1 catalogue-design; 5 in § 5.2 abstraction-shape; 3 in § 5.3 experiment-dependent; 4 in § 5.4 elrond-internal).

**Flags for routing:**

- **No new dispatches needed in this thread before Q4 lands.** Inventory deliverable is the prep-work; abstraction analysis is downstream. Q-INT-1 (visual-inspection path-D activation) is the only elrond-internal lever; it's already on Matt's acquisition-trigger queue.
- **The mechanic-category-as-derived-not-primary structural finding (§ 2.8) is upstream of the abstraction analysis's primitive choice (§ 5.2 Q-SHAPE-1).** If gandalf's Q4 framework treats mechanics as a primary dimension of the catalogue, that pressures a v1.1 schema entry (Q-PRI-1). Recorded for downstream visibility.
- **Single-vendor caveat (§ 1.1) applies to every count and cell in this document.** When future crawls land, an updated inventory should reproduce these tables alongside the originals — distribution-drift between Pimen-only and Pimen+other is structurally informative.

**Acceptance-criteria checklist (per dispatch § Acceptance criteria):**

- [x] Deliverable at `agentic_orchestration/research/curated/catalogue-structural-pre-inventory-2026-05-16.md`
- [x] All 5 sections present (snapshot § 1 / dimension inventory § 2 / cross-tabs § 3 / gaps § 4 / open-question parking § 5)
- [x] Cross-tabs include the 5 high-information pairs in Section 3 (§ 3.1 element×mechanic; § 3.2 element×register; § 3.3 element×resolution_band [bonus]; § 3.4 mechanic×license; § 3.5 cost_tier×derived_register; § 3.6 file_format×pack_register_consistency [substituted with file_format×manual_review_queued; rationale documented inline])
- [x] Gaps section enumerates without proposing fixes
- [x] Open-question parking lot lists explicit Q4 / experiment dependencies
- [x] AGENT_STATE.md update — pending (post-write of this file)
- [x] Knight-rider notification — pending (post-write of this file)

---

— elrond, 2026-05-16, post-inventory
