# Weapon Substrate Composition Policy v1 — Stage 3 Execution Spec

> **STATUS:** CURRENT (load-bearing as of 2026-05-24) — Stage 3 design call output (D1-D7 locked); consumed by Stage 3 execution (elrond constrained-sampling) → produces v1_scope membership for Reincarnated v1 ship.

**Date:** 2026-05-24
**Author:** gandalf (story-and-design steward)
**Status:** ACTIVE — Stage 3 design call CLOSED 2026-05-24 with D1-D7 all locked; this doc consolidates synthesis + drives Stage 3 execution dispatch (knight-rider routes to elrond next)
**Authority:** Matt 2026-05-24 — D1/D2/D3/D4/D5/D6/D7 all locked during Cycle 10 Stage 3 design call session
**Companion docs:**
- `canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 transcription — cell-targeting intent)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` (Architecture B production canonical)
- `canonical/story/skill-system-2026-05-24.md` (Phase 2 + Phase 5 + algorithm § 8 + § 8.6 + § 12.4)
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute system)
- `canonical/story/off-hand-items-2026-05-24.md` (Main/Secondary architecture)
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` (Cycle 10 dispatch parent)
- `agentic_orchestration/gandalf/notes/2026-05-24-stage-3-design-call-and-engine-architecture-state-capture.md` (state capture; D1-D7 + Architecture A/B/C discussion)
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` (genre context)
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (Discipline #25 semantic-layer rep-audit)
- `~/Games/reincarnated-loadout/data/telemetry.db` (substrate DB; live state)
- `canonical/00-ground-state.md` (current truth oracle)

---

## 0. TL;DR

Stage 3 design call closed 2026-05-24 with D1-D7 locked. This doc captures the composition policy:

- **v1_scope target size:** ~1,700-3,100 items (main weapons + secondary items + Stage 3.5 gap-fills + Stage 4 mythological-NULL rescues)
- **Substrate genre filter:** Reincarnated v1 = `genre IN ('fantasy', 'mythological', 'historical')` per Architecture B substrate-genre-flagging
- **Cell-type matching policies:** Option α (martial 5-tuple) / Option β (caster attribute-level) / Option C (cross-attribute ω-penalty)
- **Per-axis target weights:** substrate-led skew accepted (Sketch D); Pan-Fantasy/Hybrid 20% hefty; Tier-S/A protected
- **Sidecar B scope:** off-hand items (~1,400-5,500 rows) + 5 thin-cell-enrichment targets + 4 thin-tradition boost
- **Stage 3.5 gap-fill scope:** ~25-50 engine-authored entries (4 Sketch F anchors via gap-fill per D5 + Cell 14 Pyromantic per D2)
- **Stage 4 mythological-NULL rescue:** ~30 rows accurate-tagged at Stage 4 per Discipline #18 consult

---

## 1. v1_scope membership rules

### 1.1 Tier-S auto-promote (per D1)

**D1a — Main weapon auto-promote:**
- Rule: `quality_tier = 'S' AND weapon_kind_classified_subtype = 'handheld_weapon'`
- Approximate rows: **449**

**D1b — Secondary (Main/Secondary architecture per Matt 2026-05-24) auto-promote:**
- Rule: `quality_tier = 'S' AND weapon_kind_classified_subtype IN ('armor_shield', 'accessory_handheld', 'accessory_weapon_integrated')`
- Approximate rows: **~100-160**
- Subcategories:
  - `armor_shield`: ~30-50 rows (Aegis, Achilles shield, Saint George shield, Battersea Shield, named historical shields)
  - `accessory_handheld`: ~40-60 rows (powder flasks/horns, banners, focuses, talismans, hand-carriable ornaments)
  - `accessory_weapon_integrated`: ~30-50 rows (tsuba/menuki, grips, magazines, scopes, pommels, crossguards, quivers)

**D1c — Excluded from v1_scope:**
- `weapon_kind_classified_subtype IN ('siege_vehicle', 'art_object', 'other', 'ammo_consumable')`: ~422 rows
- `weapon_kind_classified_subtype IN ('accessory_horse_or_equipment', 'armor_body_or_head')`: ~105-145 rows (mounted-combat scope-creep + character-armor-slot deferred to v1.1+)
- **Total D1c excluded: ~525-565 Tier-S rows**

**Implementation requirement (Stage 3 execution prerequisite):**
- Elrond second-pass classifier subdivides 130 accessory + 125 armor rows into subcategories per D1 schema (~30 min)
- Substrate-fit lookup for accessory_weapon_integrated → parent-weapon-kind compatibility (gandalf; ~30 min)

### 1.2 Tier-A preferred-include (per Sketch F § 5.4 + D6 synthesis)

- Tier A (~7,355 rows) is **preferred-include** at composition policy weighted sampling
- Modulated by per-axis target weights (§ 2 below)
- Particularly: **military_modern Tier A (~2,258 rows; 31% of Tier A) is TRIMMED** per Sketch D fantasy+historical-leaning target (unless D10 Path C confirms sci-fi/cyberpunk relevance — deferred per current Sketch D)

### 1.3 Tier-B + Tier-C constrained-sampling

- Tier B (~38,414 rows) + Tier C (~22,303 rows) subject to constrained-sampling per per-axis target weights + per-cell coverage floors (§ 2 + § 4 below)
- Sampling method: per Discipline #18 legolas Mode A consult (queued); recommended greedy-with-swap-repair OR LP solver for constrained-knapsack-with-must-include

### 1.4 Stage 4 mythological-NULL rescue (per D4a)

- 30 mythological-register rows currently NULL-typed by Stage 1 proxy fingerprint
- Stage 4 mechanical-tagging with Discipline #18 consult + jack-ryan Gate-2
- Rescued rows enter v1_scope at legendary-tier per Architecture B substrate-as-base-type-templates + tiered-instance-loot

### 1.5 Stage 3.5 engine-authored gap-fills (per D5 + D7)

- 4 Sketch F anchor forms (Hattori Hanzō + Lu Bu + Moctezuma + Gilgamesh) × ~5-10 entries each = ~20-40 entries
- Cell 14 Pyromantic Caster × ~5-10 entries
- **Total Stage 3.5 budget: ~25-50 engine-authored entries**

### 1.6 Sidecar B substrate-enrichment (per D2 + Sketch D consolidation)

| Sidecar B sub-scope | Estimated additions |
|---|---|
| Off-hand item substrate (mining + targeted crawl per off-hand-items doc) | ~1,400-5,500 rows |
| Thin-cell-enrichment targets (5) — WIS-broad + Celtic/Druidic + Sub-Saharan-African + East-Asian fist-and-staff + fantasy-coinage Necromancy | additional cell-coverage |
| Thin-tradition boost — Mesoamerican + Vedic + Egyptian + Sumerian per Sketch D § 4.3 | additional tradition-coverage |

### 1.7 v1_scope total estimate

| Source | Estimated contribution |
|---|---|
| D1a auto-promote Tier-S handheld | 449 |
| D1b auto-promote Tier-S secondary | ~100-160 |
| Per-cell Tier A/B substrate via composition policy weighted sampling | ~500-1,000 |
| Stage 4 mechanical-tagging surfaces additional typed rows (currently 21,507 typed; could grow to 30-40K post-Stage-4) | additional cell-coverage |
| Sidecar B off-hand items (subset of 1,400-5,500 sourced) | ~600-1,400 |
| Sidecar B thin-cell + thin-tradition enrichment | additional |
| Stage 3.5 gap-fills | ~25-50 |
| Stage 4 mythological-NULL rescue | ~30 |
| **Total v1_scope estimate** | **~1,700-3,100 items** |

---

## 2. Target weights per axis

### 2.1 Register weights (per Sketch D substrate-led skew acceptance)

| Register | Target v1_scope share |
|---|---|
| historical | ~50-55% (slight trim from substrate's 66.4%) |
| fantasy | ~30-35% (slight boost from substrate's 25.1%; Pan-Fantasy bucket per Sketch D 20% allocation) |
| military_modern | ~5-8% (significant trim from substrate's 8.4%; defer modern firearms unless D10 Path C confirms) |
| mythological | (current substrate 0%; Stage 4 rescue adds ~30 rows) |

### 2.2 Cultural-tradition weights (per Sketch D Pan-Fantasy hefty refinement)

| Cultural tradition | Target v1 form share | Approximate substrate share in v1_scope |
|---|---|---|
| European medieval/Arthurian/Carolingian | ~18% (~6-7 forms) | ~30-35% of v1_scope |
| East Asian (Japanese folklore + Chinese Three Kingdoms) | ~15% (~5-6 forms) | ~17-20% |
| **Cross-cultural / Pan-Fantasy / Hybrid (HEFTY per Matt)** | **~20% (~7-8 forms)** | **~15-18%** |
| Norse mythological | ~10% (~4 forms) | ~8-10% |
| Greek mythological | ~8% (~3 forms) | ~6-8% |
| Celtic / Gaelic | ~6% (~2 forms) | ~5-6% |
| Mesoamerican (per Custer/Moctezuma vision; D5 gap-fill) | ~4% (~1-2 forms) | ~3-5% via Sidecar B + Stage 3.5 |
| Egyptian / North African | ~4% (~2 forms) | ~3-4% via Sidecar B |
| Vedic / Hindu | ~4% (~2 forms) | ~3-4% via Sidecar B |
| Slavic / Eastern European | ~3% (~1 form) | ~2-3% |
| Sumerian / Mesopotamian (per D5 Gilgamesh gap-fill) | ~3% (~1 form) | ~2-3% via Stage 3.5 + Sidecar B |

### 2.3 Period weights (substrate-led)

Substrate distribution per period:
- fictional: 20.2%
- unknown: 19.8%
- early_modern: 19.7%
- contemporary: 11.2%
- industrial: 10.0%
- modern: 8.8%
- classical: 7.6%
- medieval: 2.7%
- pre_classical: 0.0%

**Composition policy:** preserve substrate-led skew for period; medieval/classical priority for medieval-fantasy-isekai genre via composition weighting (~10-15% medieval/classical share via weighted sampling); contemporary/modern trim per fantasy+historical lean (sync with register trim).

### 2.4 Mechanical-cell weights (per Stage 0 cell-targeting intent)

Per `canonical/story/v1-bc-target-intent-2026-05-24.md` Sketch A: ~37 forms across ~22 cells in 5-tuple BC-target subspace.

| Attribute | Target form share | Cell coverage |
|---|---|---|
| STR | ~24% (~9 forms) | 5 cells |
| DEX | ~27% (~10 forms) | 6 cells |
| INT | ~27% (~10 forms) | 7 cells |
| WIS | ~24% (~9 forms) | 7 cells |
| Proxy-density none | ~75% (~28 forms) | ~15 cells |
| Proxy-density light | ~10% (~4 forms) | ~3 cells |
| Proxy-density heavy | ~15% (~5 forms) | ~4 cells |

### 2.5 Tier protection rules

- **Tier S:** auto-include per D1; pre-committed regardless of other sampling
- **Tier A:** preferred-include; eviction last; modulated by register/cultural-tradition targets (military_modern Tier A trimmed)
- **Tier B:** standard pool; subject to constrained sampling against all targets
- **Tier C:** eligible low-priority; included only to meet cell-coverage floors when higher-tier alternatives unavailable

---

## 3. Cell-type matching policies (Option α/β/C per Architecture B Phase 2 substrate-binding)

### 3.1 Option α — Martial cells (per skill-system § 13 + Architecture B § 5.2)

- Cell types: STR or DEX primary; physical-element coupling
- Substrate-binding rule: 5-tuple mechanical-fingerprint match required at Phase 2
- Rationale: weapon-attack IS combat delivery; weapon mechanical profile matches cell BC-target directly

### 3.2 Option β — Caster cells (per skill-system § 13 + Architecture B § 5.2)

- Cell types: INT or WIS primary; non-physical-element coupling
- Substrate-binding rule: attribute-level match only at Phase 2 (skills deliver kit BC-target; weapon scales)
- Rationale: skills are primary damage source (per caster-kit definition); weapon's intrinsic mechanical profile secondary

### 3.3 Option C — Cross-attribute hybrid cells

- Cell types: Red Mage (melee-INT) / Monk-archetype (melee-WIS) / Holy Knight (melee-WIS-mixed)
- Substrate-binding rule: cross-attribute wielding permitted with ω-penalty per BDI ω-field resource-dimension (0.0 cross vs 1.0 same-attribute)
- Rationale: hybrid identity emerges through cohesion-judge composition at Phase 5; Phase 2 substrate binding accepts cross-attribute with mechanical penalty

---

## 4. Thin-cell resolution policy (per D2 + Architecture B)

Per `canonical/story/v1-bc-target-intent-2026-05-24.md` § 1 cell roster + Stage 2 thin-cell-list:

### 4.1 Per-cell routing decisions (locked at Stage 3 design call)

| Cell | Archetype | Status | Action per D2 |
|---|---|---|---|
| 13 | Artillery Mage `(ranged, low, spiky, INT)` | CRITICAL (3 typed) | FOLD into Cell 12 Standard Wizard via T4 algorithmic alteration |
| 14 | Pyromantic Caster `(mid, low, spiky, INT)` | CRITICAL (0 typed) | Stage 3.5 engine-author gap-fill (~5-10 entries) |
| 15 | Red Mage/Spellsword `(melee, high, flat, INT)` | CRITICAL (0 typed) | Phase 5 cohesion-judge composes over STR-melee substrate base + INT-flavored kit (Option C) |
| 17 | Necromancer Summoner `(mid, low, spiky, INT, heavy)` | CRITICAL (0 typed) | Sidecar B fantasy-coinage Necro enrichment + algorithm § 8.6 proxy-spawn |
| 19 | Channeling Cleric `(mid, medium, variable, WIS)` | CRITICAL (3 typed) | Sidecar B WIS-broad enrichment (Option β downgrades from rescue to optimization) |
| 21 | Ritual Mage/Oracle `(ranged, low, spiky, WIS)` | THIN (51 typed) | ACCEPT low floor (single form; close to 60 floor) |
| 22 | Storm Caller/Druid `(ranged, medium, variable, WIS)` | CRITICAL (2 typed) | Sidecar B Celtic/Druidic enrichment |
| 23 | Monk-archetype `(melee, high, variable, WIS)` | CRITICAL (0 typed) | Sidecar B East-Asian fist-and-staff + Stage 4 mistagged-rescue (quarterstaff cross-attribute via Option C) |
| 24 | Druid Beastmaster `(mid, low, variable, WIS, heavy)` | CRITICAL (8 typed) | Sidecar B Celtic/Pacific enrichment + algorithm proxy-spawn |
| 25 | Witch Doctor Petmaster `(mid, medium, variable, WIS, heavy)` | CRITICAL (3 typed) | Sidecar B Sub-Saharan-African enrichment + algorithm proxy-spawn |
| 2 | Light Fighter `(melee, high, flat, STR)` | UNDER-FLOOR-HIGHCONF | ACCEPT 0.45-conf pool + Stage 4 mechanical-tagging priority |
| 9 | Twin-Blade Fencer `(mid, high, flat, DEX)` | MODE-A-THIN | ACCEPT Pan-Fantasy |

### 4.2 5-tuple cell-pair sharing (per D3 Option A)

5 routing-ambiguous cell pairs share 4-tuple substrate (proxy-density discriminated at form-generation via algorithm § 8.6):

| # | Cell A (proxy=none) | Cell B (proxy=light/heavy) | Shared 4-tuple |
|---|---|---|---|
| 1 | Cell 1 Heavy Barbarian | Cell 5 Ancestor-Warrior | `(melee, low, spiky, STR)` |
| 2 | Cell 7 Archer | Cell 10 Falconer | `(ranged, high, flat, DEX)` |
| 3 | Cell 12 Standard Wizard | Cell 16 Arcane-Familiar Mage | `(ranged, medium, variable, INT)` |
| 4 | Cell 14 Pyromantic Caster | Cell 17 Necromancer Summoner | `(mid, low, spiky, INT)` |
| 5 | Cell 19 Channeling Cleric | Cell 25 Witch Doctor Petmaster | `(mid, medium, variable, WIS)` |

Cohesion-judge at Phase 5 uses cultural-tradition substrate signal to bias form-assignment within shared cell-pair pool.

---

## 5. Bi-modal form-library + named-bearer discipline (per Sketch F + Matt 2026-05-24 universal archetypal naming)

### 5.1 Bi-modal lock

- ~32% named-personage forms (engine-internal substrate-anchor; player-facing UNIFORM archetypal)
- ~68% engine-named-original forms (no engine-internal named-bearer anchor)
- Player experience IDENTICAL across both — uniform archetypal naming + uniform loot-progression

### 5.2 Per-cultural-tradition Sketch F anchor allocation (locked per D5)

| Cultural tradition | Named-bearer engine-anchor (Sketch F) | Stage 3.5 gap-fill required (per D5) |
|---|---|---|
| European Arthurian | Arthur (Tier 1 broadly-fictionalized) | NO (substrate-resident) |
| European Carolingian | Roland (Tier 1) | NO (substrate-resident) |
| East Asian Japanese | Hattori Hanzō (Tier 2 soft-attribution) | **YES** — Stage 3.5 gap-fill (~5-10 entries) |
| East Asian Chinese | Lu Bu (Tier 2 soft-attribution) | **YES** — Stage 3.5 gap-fill (~5-10 entries) |
| Norse | Thor (Tier 1) | NO (substrate-resident) |
| Greek | Achilles (Tier 1) | NO (substrate-resident) |
| Celtic | Cú Chulainn (Tier 1) | NO (substrate-resident) |
| Mesoamerican | Moctezuma (Tier 2 soft-attribution + nested mythology Quetzalcoatl) | **YES** — Stage 3.5 gap-fill (~5-10 entries) |
| Egyptian | Cleopatra (Tier 2 soft-attribution) | NO (substrate-resident) |
| Vedic | Karna (Tier 1) | NO (substrate-resident) |
| Slavic | Baba Yaga (Tier 1) | NO (substrate-resident) |
| Sumerian | Gilgamesh (Tier 1) | **YES** — Stage 3.5 gap-fill (~5-10 entries) |

### 5.3 Phase 5 cohesion-judge naming discipline (per skill-system § 12.3 + § 12.4)

1. Phase 5 cohesion-judge scores kit-substrate alignment (HIGH/MID/LOW per Matt graduated-alignment discipline)
2. Per-tier discipline applies:
   - Tier 1 broadly-fictionalized: engine-internal name OK; player-facing archetypal per universal naming
   - Tier 2 real-historical-person: engine-internal anchor only; player-facing archetypal with soft-attribution per skill-system § 12.3
   - Tier 3 living-religious / marginalized-culture: EXCLUDED from v1 LLM-naming pool entirely
3. Naming-space partitioning per engine-anchor (cohesion-judge respects per-anchor reserved patterns; avoid aggregate-signal-convergence)
4. Nested mythology naming per skill-system § 12.4: Tier-2 invokes Tier-1 OK at proxy-named-entity level

---

## 6. Architecture B integration (per `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`)

### 6.1 Substrate-bound at Phase 2

Stage 3 produces v1_scope subset; Phase 2 generation pulls specific substrate rows from v1_scope at form-generation per Option α/β/C policies. Substrate's cultural-tradition + period + named-bearer signals available immediately at Phase 2 for algorithm § 8 + § 8.6 + Phase 5 cohesion-coalescence.

### 6.2 Substrate-genre-flagging

Reincarnated v1 filter: `genre IN ('fantasy', 'mythological', 'historical')`. Engine pulls from genre-tagged subset. Future commercial profiles use different genre filters (sci-fi cyberpunk = `'sci_fi', 'cyberpunk'`; etc.).

### 6.3 Phase 5 cohesion-coalescence composition

Substrate already bound at Phase 2 (per Architecture B); Phase 5 cohesion-judge:
1. Confirms substrate-thematic fit
2. Maps sub-element flavor at LLM-runtime per substrate's cultural-tradition (renamed 2026-05-24 from "element canonical-pair flavor" to disambiguate from retired seasonal-realm-mapping concept AND from legendary canonical-pair set-bonuses)
3. Bi-modal form-library assignment per § 5
4. Naming-space partitioning per engine-anchor
5. Nested mythology naming per skill-system § 12.4
6. Archetypal form/skill naming + spirit-guide explainer per skill-system § 9
7. Loot-tier assignment per substrate Tier S/A/B/C (Architecture B substrate-as-base-type-templates + tiered-instance-loot)

### 6.4 Legendary canonical-pair set-bonuses

Per Matt 2026-05-24 legendary-pair lock: canonical-pair substrate items (Excalibur + Avalon scabbard; Mjolnir + Megingjörð belt; etc.) tagged at substrate-curation; player-equip-both triggers set-bonus regime-change at gameplay layer (post-Phase-5; loot-architecture territory per future canonical doc).

### 6.5 Sub-element flavor

Per Matt 2026-05-24 sub-element lock (renamed from "element canonical-pair flavor" to disambiguate from retired seasonal-realm-mapping concept AND from legendary canonical-pair set-bonuses): core element set stable (8 elements); per-form sub-element manifestation at LLM-runtime per substrate's cultural-tradition. Phase 5 cohesion-judge maps element → sub-element flavor. Sub-elements are flavor variants of core elements (e.g., earth has sub-elements bone / obsidian / stone / crystal / sand / mud / ash / iron; shadow has darkness / vampiric / umbral / abyss / night-jaguar; etc.).

---

## 7. Stage 3 execution parameters for elrond

### 7.1 Constrained-sampling algorithm

- Per Discipline #18 methodology consult (legolas Mode A ~30-60 min) BEFORE execution
- Recommended methods: greedy-with-swap-repair (simple; design-call-friendly) OR LP solver (more optimal; requires solver)
- Tier S + A pre-committed; Tier B + C optimized against constraints

### 7.2 Constraint specifications

| Constraint type | Specification |
|---|---|
| Per-axis target weights | Register / cultural-tradition / period / mechanical-cell / proxy-density per § 2 |
| Per-cell coverage floors | Per Sketch B floor magnitudes (30-120 per cell-type); cell-pair sharing per § 4.2 |
| Tier protection | Tier S auto-include; Tier A preferred (military_modern Tier A trimmed); Tier B/C standard sampling |
| Genre filter | `genre IN ('fantasy', 'mythological', 'historical')` per Architecture B substrate-genre-flagging |
| Cell-type matching policies | Option α (martial 5-tuple) / Option β (caster attribute-level) / Option C (cross-attribute ω-penalty) per § 3 |

### 7.3 Output specifications

- New column on `weapon_knowledge_entries`: `v1_scope BOOLEAN`
- New column: `v1_scope_composition_trace TEXT` (JSON capturing why row entered v1_scope — Tier rule / cell coverage / Sketch F anchor / etc.)
- New column: `v1_scope_genre_filter TEXT` (which genre filter row passed — fantasy / mythological / historical for v1; extensible for future profiles)
- Substrate optionality preserved per Variant C: non-v1_scope rows stay in substrate; v1.1+ work can reach them

### 7.4 Empirical-criterion for completion

- v1_scope column populated on all 69K+ active rows
- v1_scope subset size 1,700-3,100 items (or different per actual sampling output; design call sign-off if outside range)
- Per-axis distribution + per-tier counts + per-cell coverage reported to Matt + gandalf for sign-off
- Gap-cell list passed to Stage 3.5 (where Sidecar B / Stage 3.5 gap-fills couldn't satisfy floor)

---

## 8. Sidecar B execution scope (consolidated)

### 8.1 Off-hand items substrate inclusion (per Sidecar B dispatch)

- Existing-source mining: royal_armouries + Met Museum + Wikipedia + Wikidata
- Targeted Mode B crawl supplements: tactical-treatises, ritual-implements, named-mythological focuses
- Schema extension (Approach B single-table per off-hand-items canonical doc)
- Estimated additions: ~1,400-5,500 rows across 6 categories (shield + tome + banner + focus + horn + talisman + weapon-integrated accessory)

### 8.2 Thin-cell-enrichment (per D2 — 5 targets)

| Target | Cells served |
|---|---|
| WIS-broad enrichment | Cells 19, 21, 22, 23, 24, 25 |
| Celtic/Druidic | Cells 22, 24 |
| Sub-Saharan-African | Cell 25 (+ Sketch D § 4.2 African-tradition boost) |
| East-Asian fist-and-staff | Cell 23 |
| Fantasy-coinage Necromancy | Cell 17 |

### 8.3 Thin-tradition boost (per Sketch D § 4.3)

- Mesoamerican
- Vedic / Hindu
- Egyptian
- Sumerian

(Compounds with Sketch F anchor gap-fills per D5: Moctezuma gap-fill complements Mesoamerican thin-tradition boost; Gilgamesh gap-fill complements Sumerian thin-tradition boost)

### 8.4 Owner + cost estimate

- elrond (lead) + legolas Mode B (crawl) + gandalf (cultural-curation review)
- ~1-2 days legolas Mode B crawl + ~half-day elrond schema/extraction + ~1 hour gandalf curation review

---

## 9. Stage 3.5 engine-authored gap-fill scope (consolidated per D5 + D7)

### 9.1 Scope

| Source | Entries | Cultural-tradition | Tier discipline |
|---|---|---|---|
| Cell 14 Pyromantic Caster (per D2) | ~5-10 | Pan-Fantasy | Tier A (engine-authored Pan-Fantasy slot) |
| Hattori Hanzō anchor form (per D5) | ~5-10 | Japanese folklore | Tier S (Sketch F anchor); Tier 2 soft-attribution |
| Lu Bu anchor form (per D5) | ~5-10 | Chinese Three Kingdoms | Tier S; Tier 2 soft-attribution |
| Moctezuma anchor form (per D5) | ~5-10 | Mesoamerican | Tier S; Tier 2 soft-attribution; nested Quetzalcoatl per skill-system § 12.4 |
| Gilgamesh anchor form (per D5) | ~5-10 | Sumerian / Mesopotamian | Tier S; Tier 1 broadly-fictionalized |
| **Total Stage 3.5 budget** | **~25-50 engine-authored entries** | | |

### 9.2 Per-entry discipline

| Discipline | Rule |
|---|---|
| D7 AI-tell discipline | Templated LLM with narrow blanks; gandalf-curated; NOT raw LLM dialogue generation |
| Cultural-sensitivity (per Q-B verdict § 3.2) | Tier 1/2 OK per their respective disciplines; NO Tier 3 content in gap-fills |
| Provenance flag | `source_library = 'engine_authored_gap_fill_v1'` |
| Stage 3.6 research-replacement notes | Each gap-fill flagged as v1.1+ Track M-targeted web-research substitution candidate |
| Naming-space partitioning | Engine-internal anchor recorded; player-facing archetypal name per universal naming + skill-system § 12.3 + § 12.4 |
| Quality review | gandalf reviews every gap-fill entry before commit |
| Sim-viability check | rocket runs sim-viability per gap-fill per T4-A § 3.3 step 5; jack-ryan Gate-2 ratifies |

### 9.3 Per-entry mechanical profile schema

Each gap-fill entry populates: canonical_name (engine-internal; archetypal at Phase 5 cohesion via cohesion-judge), description_text, structured_properties, register_canonical, historical_period_canonical, cultural_lineage_canonical, proxy_attribute_class, proxy_range_class, proxy_geometry_class, proxy_tempo_class, quality_tier, extracted_named_bearer (engine-internal anchor for Sketch F gap-fills), named_mythological_match, all Stage 4 mechanical-tagging fields.

### 9.4 Owner + cost estimate

- rocket (engine generator for skill kit) + gandalf (cultural-tradition curation + lore + naming review) + star-lord (LLM call infrastructure per Phase 5 cohesion-coalescence) + jack-ryan (Gate-2 sim-viability)
- Estimated: ~half-day per Sketch F anchor (5 sessions × 1-2 hours each) + ~2-3 hours for Cell 14; total ~1-2 days

---

## 10. Cycle 10 execution sequence (post-D7-lock)

```
Stage 3 design call CLOSED (D1-D7 LOCKED 2026-05-24)
    ↓
Composition policy canonical doc landed (THIS DOC)
    ↓
Knight-rider authors Stage 3 execution dispatch routing to elrond
    ↓
Stage 3 execution: elrond constrained-sampling per composition policy
    ↓
v1_scope materialized (per-row v1_scope flag + composition trace)
    ↓
Matt + gandalf sign-off (per-axis distribution + per-tier counts + per-cell coverage report)
    ↓
Wave 5 fires:
    ├─ Stage 3.5 engine-authored gap-fills (rocket + gandalf + star-lord)
    └─ Stage 4 accurate mechanical-tagging (rocket + gamora + jack-ryan + legolas Mode A consult)
    ↓
Stage 3.6 research-replacement notes (gandalf)
    ↓
Cycle 10 wind-down (gandalf + knight-rider):
    ├─ Roadmap § 1.0 + § 3.8 updates
    ├─ Ground-state oracle § 1 + § 5 updates
    ├─ Cycle 10 closeout handoff
    ├─ Post-Stage-3 canonical authoring queue:
    │   ├─ Phase 4 simplified archive math spec (per session ULTRA-think)
    │   ├─ Phase 5 cohesion-judge calibration spec (per session ULTRA-think)
    │   ├─ Loot architecture canonical doc (per Architecture B Implication 1)
    │   ├─ Sub-element architecture canonical doc (renamed from "element canonical-pair flavor")
    │   └─ Naming-space partitioning canonical doc
    └─ Recognition 1 (sampling-proportionality) v1.1+ flag → v1 LOCKED via this composition policy doc
```

---

## 11. Empirical grounding (current data per Stage 1 + 1.5 + 2 + 2.5)

### 11.1 Tier distribution (Stage 2.5 complete)

| Tier | Rows | % of substrate |
|---|---|---|
| S | 1,065 | 1.5% |
| A | 7,355 | 10.6% |
| B | 38,414 | 55.6% |
| C | 22,303 | 32.3% |

### 11.2 Hard observations informing composition policy

1. **INT/WIS substrate STRUCTURALLY THIN at Tier S/A** (Tier S: 0 INT + 8 WIS; Tier A: 8 INT + 21 WIS) — caster Tier-S protection structurally limited; Sidecar B + Stage 3.5 covers gap
2. **68% of substrate UNTYPED** by Stage 1 fingerprint — Stage 4 mechanical-tagging quality determines v1_scope final size
3. **Tier S over-represents historical** (82% vs substrate 66.4%) — substrate-led skew confirmed per Sketch D acceptance
4. **Tier A military_modern anomalously high** (31% = 2,258 rows) — composition policy TRIMS per Sketch D fantasy+historical-leaning
5. **964 named-bearer rows extracted** (Stage 1.5) — substantial Track M1 mining dividend for legendary-tier composition

### 11.3 Projected additions (not yet executed)

- Sidecar B substrate-enrichment: ~1,400-5,500 rows
- Stage 3.5 gap-fills: ~25-50 entries
- Stage 4 mythological-NULL rescue: ~30 rows
- Final v1_scope estimate: ~1,700-3,100 items

---

## 12. What this doc does NOT do

- NOT a Stage 3 execution dispatch — that's knight-rider's authoring territory next
- NOT a Sidecar B execution spec — Sidecar B dispatch already authored; this doc consolidates Sidecar B scope into composition policy context
- NOT a Stage 3.5 gap-fill authoring spec — gap-fills authored per Wave 5; this doc consolidates scope
- NOT a Stage 4 mechanical-tagging spec — that's rocket+gamora+jack-ryan post-D6 work per dispatch
- NOT a Phase 5 cohesion-judge calibration spec — that's P5 work queued post-Stage-3 (per session ULTRA-think recommendations)
- NOT an MVP scope lock — MVP scope lock fires post-T4-B post-mortem per 02-roadmap § 3.3
- NOT a faction-architecture canonical doc — faction-architecture deferred per 02-roadmap § 3.4; gated on P4 cluster semantic labeling

---

## 13. Cross-references

### Active project canon this doc consumes
- `canonical/00-ground-state.md` § 1 (current truth oracle)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` (Architecture B production canonical)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 cell-targeting intent)
- `canonical/story/skill-system-2026-05-24.md` (skill composition + algorithm § 8 + § 8.6 + § 12.3 + § 12.4 + § 13)
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute system)
- `canonical/story/off-hand-items-2026-05-24.md` (Main/Secondary architecture)
- `canonical/story/v1-1-plus-design-discipline-recognitions-2026-05-23.md` (Recognition 1 sampling-proportionality LOCKS via this doc)
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` (genre context)
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (Discipline #25 semantic-layer rep-audit)
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` (Cycle 10 dispatch parent)
- `agentic_orchestration/gandalf/notes/2026-05-24-stage-3-design-call-and-engine-architecture-state-capture.md` (state capture)

### Live state references
- `~/Games/reincarnated-loadout/data/telemetry.db` (substrate DB; weapon_knowledge_entries; Stage 1/1.5/2/2.5 columns populated; v1_scope column added at Stage 3 execution)

### Downstream artifacts this doc anchors
- Stage 3 execution dispatch (knight-rider authors next)
- v1_scope subset materialized at Stage 3 execution
- Wave 5 Stage 3.5 + Stage 4 work
- Post-Stage-3 canonical authoring queue (Phase 4/5 amendments + loot architecture + sub-element architecture [renamed from "element canonical-pair flavor"] + naming-space partitioning)
- T4-B post-mortem (post-engine-form-generation; ~3-5 weeks from now)

---

## 14. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-24 — D1-D7 all locked at Cycle 10 Stage 3 design call session
**Status:** CURRENT — production composition policy; Stage 3 execution dispatch consumes this doc
**Re-engagement gate:** Stage 3 execution sign-off (per-axis distribution + per-tier counts + per-cell coverage report); if v1_scope subset materially deviates from estimate, design call re-engages for amendment

---

**Signed:** gandalf
**For:** the canonical composition policy v1 driving Stage 3 execution (elrond constrained-sampling) → v1_scope membership for Reincarnated v1 ship; consolidates D1-D7 locks + all session architectural commitments (Architecture B + Option α/β/C + universal archetypal naming + bi-modal form library + sub-element flavor [renamed 2026-05-24 from "element canonical-pair flavor"] + legendary canonical-pair set-bonuses [DISTINCT concept for paired legendary items] + Sketch D + Sketch F + Sidecar B + Stage 3.5 gap-fills + Stage 4 mythological-NULL rescue + Pattern 6 alignment + substrate-genre-flagging).
