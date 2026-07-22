# Faction-coalescence probe — 270-kit corpus-of-record census

**Author:** elrond (data steward) · **Date:** 2026-07-21 · **Status:** CURRENT (findings; empirical, no design ruling)
**Mode:** READ-ONLY analytical probe · **Commission:** gandalf brief `2026-07-21-elrond-faction-coalescence-probe-brief.md`, Matt-authorized
**Subset:** `kit_master WHERE game IN ('d2','gd','poe1','poe2','le')` — verified **270** (d2 60 / gd 41 / poe1 94 / poe2 38 / le 37). DB `corpus.db` (SSOT). Atlas coords `atlas/atlas.json` Edition-I (frozen 2026-07-14; dims PERFORM↔DEPLOY / EMBODY↔LAUNCH). No writes, no schema edits.

---

## Top-line (the census, one screen)

**How many factions accrue, per axis** — atlas-diversity ratio = mean within-group atlas-std ÷ global atlas-std (0.4419). **≈1.0 = faction spans the atlas (mechanically diverse — the desired Gate-C property); low = mechanically narrow.**

| Axis | col mapped | **k** | size min/med/max | NULL% | atlas-diversity | enmity |
|---|---|---:|---|---:|---:|---|
| **source-game** | `game` | **5** | 37/41/94 | 0.0% | **0.977** high | NONE natural |
| **era_year (release-era)** | `era_year` | **4** | 41/68/93 | 0.0% | **0.986** high | path only (fails ≥2 raw) |
| era (per-expansion) | `eras` | 104 | 1/2/15 | 0.7% | 0.718 mid | path only |
| gx (mastery codes) | `gx` | 58 | 1/2/12 | **42.2%** | 0.562 narrow | NONE natural |
| **delivery-family (7-col)** | `geometry_value` fold | **7** | 6/30/68 | 1.9% | 0.782 mid | NONE natural |
| movement-row | `commit_val` proxy | 3 | 13/22/233 | 0.7% | 0.747 mid | NONE natural |
| role-orientation | ailment proxy | 2 | 128/135/142 | 0.0% | 0.993 high | opposition (degenerate, k=2) |
| range (engagement) | `range_val` | 3 | 62/89/119 | 0.0% | 0.955 high | NONE natural |
| attr class-attr | `attr_val` | 4 | 36/64/105 | 0.4% | 0.968 high | NONE natural |
| **elements (primary)** | `elements_attested` | **13** (5 dominant) | 1/4/77 | 0.0% | 0.649 narrow-ish | **WHEEL — natural ≥2** |

**Mechanical k-sweep** (KMeans silhouette on atlas x,y; 268 subset points, 2 lack coords): silhouette **flat 0.409–0.439 across all k=3..12**, weak peak k=5 (0.439). **No decisive k. Confirms the Edition-I prior verbatim — "continuum with condensations, not discrete cells." The mechanical reading yields NO natural faction count.** (Q1 axis #8 reported honestly: mechanics do not vote a faction integer.)

## Q2 — War-graph feasibility (min-degree ≥2 per faction, no forced edges)

- **Only elements admit a natural enmity relation.** Elemental opposition/wheel is genre-native (fire↔water/cold, earth↔lightning/air, holy↔shadow). The 5 dominant attested elements (fire 64, lightning 41, shadow 33, water 24, earth 16; +physical 77 as a non-elemental bloc) support a **cycle/wheel C₅ → every faction degree exactly 2**, and odd-cycle wheels give natural three-way fights (triangles). This is the one axis where Matt's "each adversary also a direct enemy of two factions" holds *without arbitrary edges*.
- **era_year / eras admit a *path*, not a cycle.** 2000→2013→2016→2024 is orderable, so adjacency-enmity is meaningful, but the two endpoints reach degree 1 — **fails min-degree ≥2** unless the path is wrapped into a ring, which is an arbitrary (forced) edge. Reportable as a near-miss, not a pass.
- **source-game, gx, delivery, movement, range, attr — NO natural enmity.** Game-of-origin has no intrinsic "d2 is enemy of poe1" relation (brief anticipated this — confirmed). Delivery/movement/range/attr are orthogonal descriptors, not antagonists; any war-graph would be fully forced.
- **role (k=2)** admits trivial opposition (damage↔control) but degenerate: 2 factions is below the sensible-k floor and a 2-cycle is min-degree 1.
- Devourer force excluded per brief (hostile-to-all trivially assignable outside the graph).

## Q3 — Element-evidence coverage (descriptor feasibility; NOT a mapping — Q21 stands)

- `elements_attested` (elemental-only projection): **177/270 = 65.6%** carry an element token. Per game: d2 55% / gd 73% / le 65% / poe1 69% / poe2 66%. Multi-element ambiguity **29/270 = 10.7%**.
- **The 34.4% "gap" is NOT missing data — it is signal.** All 93 element-null kits carry `elem_raw`, and 85 of them read **"physical"** (the rest magic/void/n-a). This is THE PHYSICAL RULE working as designed (pure-physical kits are element-neutral, not undocumented).
- **`elem_raw` coverage = 270/270 = 100%, 0 NULL** (21 raw values: physical 85, fire 54, lightning 38, cold 27, chaos 22, + long tail incl. 5 "n/a", 4 ambiguous "?"). A future *descriptive* `original_element` field is **fully feasible** off `elem_raw` with near-total coverage; the free engine element axis stays untouched.

## Q4 — OM-7 rider: era-coordinate feasibility

- **Coarse (release-era-per-game) already exists, free, 100%:** `era_year` = **4 clean buckets** (2000/2013/2016/2024). **But it is near-collinear with game-of-origin** — 2000=d2, 2013=poe1, 2016=gd, 2024=le+poe2 (crosstab in appendix). Release-era is essentially a 4-way re-bucketing of the 5-way `game` axis (merges le+poe2). Sufficient for coarse era-descent gating; adds ~zero new partition information over `game`.
- **Fine (per-expansion) also already exists:** `eras` populated 268/270 (0.7% null), 104 distinct patch-strings (e.g., `3.0-3.6;3.7-3.13`, `lod;d2r`). Per-kit expansion dating is **present, no crawl needed** — cost is normalization only (parse patch-strings → ordinal era index), an in-house curation pass, not acquisition. `skill_debut_year` is populated only 7/270 — not a viable finer grain.

---

## Appendix A — full group counts

**source-game:** poe1 94, d2 60, gd 41, poe2 38, le 37.
**era_year:** 2013→93, 2024→76, 2000→60, 2016→41.
**delivery-family (7-col fold):** PROJECTILE 68, MELEE 64, NOVA 56, ZONE 30, SUMMON 26, ORBITAL 15, BEAM 6 (orphans 5: `d2-wl-void-rift`, `gd-berserker-wereforms`, `le-skeleton-necro`, `le-wraithlord-necro`, `le-low-life-ward` — no `geometry_value`).
**movement-row (commit_val proxy):** FREE-MOVE(instant) 233, ROOTED(channel) 22, WALK(wind-up) 13, null 2.
**attr class-attr:** INT 105, DEX 73, STR 55, WIS 36, null 1.
**range:** melee 119, ranged 89, dual 62.
**elements primary:** physical 77, fire 64, lightning 41, shadow 33, water 24, earth 16, + tail (n/a 4, magic 3, holy 2, pierce 2, cold 2, void 1, bleed 1).
**gx:** 58 groups, largest GAP-D2-01 12 / GX-03 12; 114 null.

## Appendix B — mechanical k-sweep (silhouette, atlas x,y)

k=3 .413 · k=4 .418 · **k=5 .439** · k=6 .410 · k=7 .420 · k=8 .422 · k=9 .409 · k=10 .413 · k=11 .411 · k=12 .416. Flat curve; no elbow; no gap-stat separation implied. Substrate does not vote a faction integer under the mechanical reading (Edition-I prior held; not re-derived).

## Appendix C — era_year × game crosstab (collinearity evidence for Q4)

| era_year | d2 | poe1 | gd | le | poe2 |
|---|---:|---:|---:|---:|---:|
| 2000 | 60 | — | — | — | — |
| 2013 | — | 93 | — | — | — |
| 2016 | — | — | 41 | — | — |
| 2024 | — | 1 | — | 37 | 38 |

## Axis→column mapping notes (schema honesty — absence is a finding)

- **delivery-family** is *derived* (fold of per-skill `geometry_value` → 7-col, kit-dominant footprint); it is not a stored enum. Fold rule reproducible from `mapping_json.skills[].geometry_value`.
- **movement-row (FREE-MOVE/WALK/ROOTED)** is **not a stored column.** Nearest structured proxy = `commit_val` (instant/wind-up/channel). Reported as a proxy, not the literal row.
- **role-orientation (damage/control/hybrid)** is **not a stored enum.** `option_c_substrate_flags` is 100% NULL on the subset. Proxied here from `ailments_attested` presence (control-signal) — heuristic only, flagged; a native role field would require authoring, not extraction.
- **architecture** (decomposition monolithic-vs-decomposed) is **100% empty on the subset** — decomposition-via-`architecture` is unrecoverable from schema today. `grain`='kit' for 268/270 (uniform; no decomposition partition).
- **lineage** column is **97.8% NULL** (264/270) — collapses as a coalescence axis. The mastery-code carrier is `gx` (42.2% NULL, compound values, "-proposed" tails).

---

## Q5 — Top-line synthesis (empirical fitness ranking; the design ruling is Matt's, downstream)

Ranked against the four brief criteria — (a) sensible k≈4–10, (b) tolerable size balance, (c) high within-faction atlas diversity, (d) natural ≥2-degree enmity — **only one axis satisfies all four, and it is elements.** Primary-element gives k≈5 dominant blocs (fire/lightning/shadow/water/earth) with a genre-native opposition wheel that reaches min-degree 2 without a single forced edge (uniquely satisfies (a)+(d)); its atlas-diversity is the *one caveat* (0.649 — the mechanically-narrowest of the sensible-k axes, since elemental kits do cluster somewhat by geometry), but 0.649 is still substantial spread, and the physical bloc (77 kits) is a natural non-elemental faction / devourer-adjacent reservoir. **Second-fittest is a *pairing*, not a standalone: `source-game` (or its near-twin `era_year`) supplies the best k+balance+diversity profile (k=5, sizes 37–94, diversity 0.977 — factions that maximally span the atlas, the exact Gate-C property Matt wants) but carries NO natural enmity — so it fits (a)(b)(c) and fails (d) alone; it becomes viable only if enmity is imported from a second axis (elements-wheel or era-adjacency-ring) laid over the game/era partition.** Delivery-family (k=7, diversity 0.782) is the runner-up structural partition but likewise has no native enmity. The mechanical clustering axis is empirically *unfit* for faction coalescence — the flat silhouette curve means it yields no stable faction count at all. Net empirical read: **elements is the only single axis that natively closes the war-graph; game/era is the only single axis that natively maximizes faction atlas-diversity; the two are complementary and neither alone satisfies all four — a hybrid (game/era for membership, elements-wheel for enmity) is the empirically-indicated shape, but that composition is a design call, not a substrate finding.**
