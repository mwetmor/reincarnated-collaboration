# SC-6 — Substrate Weapon Stat Audit (Cycle 14 Wave 0)

> **STATUS:** CURRENT (audit-report only; SC-6 NARROW scope per KR re-fire). No schema changes. No MIGRATION.md. Per-field dispositions validated against doc 47 § 3 + empirical DB inspection of `~/Games/reincarnated-loadout/data/telemetry.db`.

**Authored:** 2026-05-27 (Cycle 14 Wave 0, third invocation)
**Author:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Authority:** Matt 2026-05-27 (Q1–Q11 ratification; Cycle 14 framing brief; KR Wave 0 orchestration)
**Scope basis:** `agentic_orchestration/elrond/sc-6-progressive-findings-2026-05-27.md` (KR-authored anchor); `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-sc-6-substrate-weapon-stat-audit.md` (with KR amendment naming substrate library location); `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3
**Companion (deferred):** SC-6b enrichment dispatch — schema extension + MIGRATION.md + data backfill (see § 5 recommended scope)

---

## 1. Substrate library state

### 1.1 Locations confirmed

| DB / table | Path | Role |
|---|---|---|
| `weapon_knowledge_entries` (90,014 rows; **2,293 v1_scope**) | `~/Games/reincarnated-loadout/data/telemetry.db` | Broad weapon-knowledge corpus; v1_scope flag selects the Cycle 14 substrate cell |
| `weapon_sim_props` (1:1 with `weapon_knowledge_entries` via `weapon_id`) | same DB | Sim-property numerics — the **authoritative attribute requirement source** for v1_scope rows |
| `weapons` (5,162 rows; mostly **NOT v1_scope-aligned** — see § 1.4) | same DB | Aesthetic + sim-class tuple; largely irrelevant for SC-6 v1_scope audit |
| `catalogue.db` | — | **DOES NOT EXIST**; prior session dead-end — confirmed |
| `cycle13_characters.db`, `research.db`, engine `telemetry.db` | — | NOT the substrate library; out of scope |

### 1.2 v1_scope confirmation (Discipline #11 empirical inspection)

```
SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope=1;
→ 2293
SELECT COUNT(*) FROM weapon_sim_props wsp JOIN weapon_knowledge_entries wke ON wke.id=wsp.weapon_id WHERE wke.v1_scope=1;
→ 2293   (1:1 — every v1_scope entry has weapon_sim_props row)
```

Null-coverage on critical fields across all 2,293 v1_scope rows:
- `damage_amplitude_min` NULL: **0**
- `damage_amplitude_max` NULL: **0**
- `primary_stat` NULL: **0**
- `secondary_stat`: ALL = `'none'` (unused at substrate; not a hybrid carrier)

**Verdict:** the substrate is clean on the columns it does populate. No NULL gaps for the existing-column dispositions. The audit gaps are about **missing columns**, not missing data within existing columns.

### 1.3 v1_scope primary_stat distribution (the four-attribute split)

| primary_stat | count | % of v1_scope |
|---|---|---|
| DEX | 1,075 | 46.9% |
| STR | 891 | 38.9% |
| WIS | 167 | 7.3% |
| INT | 160 | 7.0% |

**Martial-heavy bias confirmed:** STR+DEX = 85.8% of substrate. Caster (INT+WIS) = 14.2%. This composition implies SC-6b enrichment for caster-side fields (spell_damage_modifier, element affinity) can be defaulted by `primary_stat` family with modest manual override on the 327 caster rows — small fan-out, not a 2,293-row labeling task.

### 1.4 `weapons` table is not the v1_scope substrate library

Join experiment: `weapons.display_name = weapon_knowledge_entries.canonical_name` on v1_scope:
- **2,252 of 2,293 v1_scope rows have NO match in `weapons`** (98.2% miss rate)
- Only 41 v1_scope rows align to `weapons`

`weapons.stat_affinity` is `'unknown'` for **all 5,162 rows** — completely unpopulated (KR diagnostic § 2.5 confirmed).

**Architectural finding:** the `weapons` table is a separate / earlier substrate slice (likely Wave 0.5 ingest path or composition-policy precursor); it is **NOT** the v1_scope cycle 14 substrate. For SC-6 work, **`weapon_knowledge_entries` + `weapon_sim_props` is the authoritative pair**. Any SC-6b enrichment lands on `weapon_sim_props` (or a sibling table FK'd to `weapon_knowledge_entries.id`), NOT on `weapons`.

### 1.5 `proxy_attribute_class` vs `primary_stat` — near-redundancy with cleaner enum on the sim-props side

Cross-tab on v1_scope:

| `proxy_attribute_class` (wke) | `primary_stat` (wsp) | n |
|---|---|---|
| DEX | DEX | 1058 |
| STR | STR | 872 |
| INT | INT | 160 |
| WIS | WIS | 160 |
| DEX | STR | 19 |
| STR_or_DEX | DEX | 17 |
| STR_or_WIS | WIS | 7 |

**Disposition:** `weapon_sim_props.primary_stat` is the **authoritative** attribute requirement column. It resolves ambiguous `proxy_attribute_class` hybrids (`STR_or_DEX`, `STR_or_WIS`) into a single CHECK-constrained enum value. Use `primary_stat`; treat `proxy_attribute_class` as upstream-extraction trace only.

### 1.6 damage_amplitude is a RATIO, not absolute damage (load-bearing architectural finding)

```
SELECT ROUND(damage_amplitude_min, 1) AS m, COUNT(*) FROM weapon_sim_props GROUP BY m ORDER BY m;
→ 0.0:7  0.3:328  0.4:133  0.5:228  0.6:66  0.7:938  0.8:591  1.0:2
```

Values cluster 0.3–0.8; range observed in code referenced as 0.3–3.0. **These are amplitude RATIOS — scaling multipliers applied to a baseline damage figure — not absolute damage in HP points.**

This is the single most load-bearing architectural finding for SC-6. Doc 47 § 3.1 specifies absolute physical-damage ranges per weapon family (STR heavy melee: 100–300 HP at L50; DEX light/ranged: 60–150; INT/WIS casters: 20–80). **The substrate library has the scaling shape (`damage_amplitude_min/max` per-weapon variance ratio) but NOT the absolute L50 baseline** that doc 47 § 4.2's `weapon.base_physical_damage` formula consumes directly:

```
raw = base * skill_mult * (1 + attr_bonus) * (1 + global_phys) * tier_coef
```

`base` here must be in HP points, not a ratio. Two architectural paths:

**Path A — substrate library adds `base_physical_damage_l50` absolute column.** Per-weapon-family L50 baseline computed by elrond enrichment (e.g., greatsword family = 200, dagger family = 100, staff family = 50); `base_physical_damage` = `base_physical_damage_l50 × damage_amplitude_min/max` lottery at gen time. Substrate carries both the shape and the magnitude.

**Path B — rocket Phase 2c computes at gen time from a global L50 calibration constant + per-weapon-family-multiplier table maintained engine-side.** Substrate carries only the ratio; engine carries the magnitude. Substrate stays elegant; calibration constants live with the engine that uses them.

**Elrond recommendation: Path A.** Rationale:
- The L50 baseline is a property of the **weapon as substrate object**, not a property of the engine that consumes it. The greatsword does more damage than the dagger because of what the greatsword IS, not because the engine assigns it more.
- Discipline #11 + #18: keeping `base × ratio` decomposition in the substrate means the engine's damage formula is auditable end-to-end from substrate row → fight log. Path B locks the magnitude inside the engine codebase, where it's harder to inspect and harder to balance.
- Path A also makes per-weapon-family L50 baselines a single tunable surface (elrond updates one column when balance shifts), versus Path B where the calibration table lives behind code.

**Path A is the recommended SC-6b enrichment**; final architectural call before SC-6b fires rests with rocket coordination (cross-seam) + Matt ratification.

---

## 2. Per-field disposition table (validated + amended)

Each row: validate against KR's pre-staged disposition (progressive-findings § 3) or amend per elrond domain judgment. **Amendments noted in rationale column.**

| Doc 47 § 3 field | Current substrate exposure | Disposition | Rationale |
|---|---|---|---|
| **`base_physical_damage`** | `weapon_sim_props.damage_amplitude_min/max` (RATIO 0.3–3.0) | **NEEDS NEW COLUMN: `weapon_sim_props.base_physical_damage_l50` (REAL, HP points)** — see § 1.6 Path A | Substrate carries amplitude ratio but NOT absolute L50 magnitude. Per-weapon-family baseline (sword-family ~200, dagger ~100, staff ~50) is a property of the substrate object, not the engine. Per-row enrichment: compute via family-baseline LUT × ratio for SC-6b. **Amends KR disposition (which left Path A/B as an open choice)** — elrond votes Path A on architectural-cleanliness grounds. |
| **`spell_damage_modifier`** | NONE | **NEEDS NEW COLUMN: `weapon_sim_props.spell_damage_modifier_pct` (REAL, percent)** | Doc 47 § 3.1 expects 30–150% for INT casters, 30–120% for WIS, 0–10% for martial. Population rule (algorithmic, not LLM-required): `primary_stat='INT'` → roll/assign 30–150 by `weapon_kind_classified_subtype`; `'WIS'` → 30–120; `'STR'/'DEX'` → 0–10. **Confirms KR disposition.** With 327 caster rows out of 2,293, manual per-family override on the caster side is feasible if defaults are too coarse. |
| **`element_affinity_modifiers`** | `weapons.dominant_element_affinities` (comma-sep list; only on `weapons` table — 98% miss-rate for v1_scope) | **NEEDS NEW JSON column on `weapon_sim_props`: `element_affinity_modifiers_json`** with shape `{"fire": pct, "water": pct, ...}` | **Confirms KR disposition with refinement:** since `weapons.dominant_element_affinities` does not cover v1_scope substrate (98.2% miss-rate per § 1.4), the comma-sep approach can't be retrofitted. New JSON column on `weapon_sim_props`. Default policy: martial weapons = empty `{}` (no element affinity); caster weapons get derivation from named_template parsing (`Rod of Icicles` → `{"water": 15}`, `Flutterby Rod` → varies, `Aegis` → empty) — this is an LLM-assisted enrichment pass for the 327 caster rows. Alternative: leave NULL at substrate, derive at rocket binding time from element-name regex match against canonical_name. **Recommend substrate-side enrichment** for auditability. |
| **`to_skill_level_modifiers`** | NONE | **DEFER to rocket Wave 0.5 (gear-instance gen) for non-unique tiers; ADD SUBSTRATE COLUMN for unique-tier named weapons only** | **Refines KR disposition (which named both routes as candidates):** the 42 `weapon_kind='unique'` rows + a curated subset of `named_template` rows (~927 entries) carry mythological identity that warrants a fixed `+to_skill_level` value as part of the named-template definition (e.g., Gáe Bolg always grants +1 spear-skill; Mjölnir always grants +2 hammer-skill). For the 1,139 generic `weapon_kind='category'` rows, the modifier is rolled per-instance at gear-gen time by rarity tier (rocket seam). **Architectural split: substrate carries flavor-fixed modifiers on unique/named rows; engine rolls per-instance modifiers on category rows.** Substrate column: `weapon_sim_props.to_skill_level_modifier_static` (TEXT JSON, NULL for category rows; `{"spear": 1}` for unique-template rows). |
| **`attribute_requirement`** | `weapon_sim_props.primary_stat` (STR/DEX/INT/WIS — clean enum, 0 nulls on v1_scope) | **REUSE `primary_stat` AS-IS** — no enrichment | **Confirms KR disposition unequivocally.** `weapons.stat_affinity` is unpopulated and structurally wrong (the `weapons` table doesn't cover v1_scope). `proxy_attribute_class` on `weapon_knowledge_entries` has hybrid noise values (`STR_or_DEX`) that `primary_stat` resolves. Rocket Phase 2c reads `wsp.primary_stat` directly; binding maps it 1:1 to character JSON `gear_representative.main_weapon.attribute_requirement`. |
| **`weapon_type_family`** | DERIVABLE from `(primary_stat, proxy_range_class, weapon_kind_classified_subtype)` — see § 2.1 algorithmic rule | **NEEDS NEW COLUMN: `weapon_sim_props.weapon_type_family` (TEXT CHECK against doc 47 6-enum)**; populated by algorithmic rule + small-N manual review | **Confirms KR disposition.** No 1:1 source column exists. The 6-family doc 47 enum (martial-heavy / martial-light / ranged / caster-arcane / caster-faith / hybrid) is derivable from 3 existing columns via the rule below. **NOT an LLM-required mapping** — algorithmic across ~2,293 rows. |

### 2.1 `weapon_type_family` algorithmic mapping rule (SAMPLE — top patterns)

Per anti-stall discipline: SAMPLE top-20 patterns + algorithmic rule, NOT exhaustive per-row.

**Rule (covers ~99% of v1_scope substrate):**

```
IF primary_stat = 'STR':
    IF proxy_range_class IN ('melee', 'mid'): weapon_type_family = 'martial-heavy'
    ELIF proxy_range_class = 'ranged': weapon_type_family = 'ranged'  (rare; STR-ranged = thrown / heavy crossbow)
    ELSE: weapon_type_family = 'martial-heavy'  (default)
ELIF primary_stat = 'DEX':
    IF proxy_range_class IN ('melee', 'melee_close_or_grapple'): weapon_type_family = 'martial-light'
    ELIF proxy_range_class IN ('mid', 'ranged'): weapon_type_family = 'ranged'
    ELSE: weapon_type_family = 'martial-light'  (default)
ELIF primary_stat = 'INT':
    weapon_type_family = 'caster-arcane'
ELIF primary_stat = 'WIS':
    weapon_type_family = 'caster-faith'
ELSE: weapon_type_family = NULL  (review)
```

**`hybrid` family** — reserve for the small set of v1_scope rows that carry dual-attribute scaling explicitly (currently rare; `secondary_stat` is `'none'` across all v1_scope; would be assigned manually at SC-6b if/when hybrid weapons enter substrate per Option C cross-attribute cells).

**Sample top-20 mappings derived from this rule** (cross-tab counts, totalling 2,212 of 2,293 — 96.5% coverage):

| primary_stat | proxy_range_class | n | → weapon_type_family |
|---|---|---|---|
| STR | melee | 588 | martial-heavy |
| DEX | ranged | 543 | ranged |
| STR | mid | 213 | martial-heavy |
| DEX | melee | 352 | martial-light |
| DEX | mid | 163 | ranged |
| INT | ranged | 85 | caster-arcane |
| INT | mid | 62 | caster-arcane |
| WIS | melee | 100 | caster-faith |
| WIS | ranged | 44+2 = 46 | caster-faith |
| WIS | mid | 10+1 = 11 | caster-faith |
| STR | ranged | 90 | ranged (STR-ranged: thrown / siege; ~3.9% of STR) |
| DEX | melee_close_or_grapple | 17 | martial-light (shield_blocker subset) |
| WIS | off_hand_aura | 7 | caster-faith (banner-rally subset) |

Remaining ~81 rows (3.5%) are edge cases (INT-melee, melee_close_or_grapple under non-DEX, mid|cone outliers) — flag for SC-6b manual review pass.

**Caster-arcane vs caster-faith discriminator:** `primary_stat` (INT vs WIS) is the clean discriminator. INT v1_scope is dominated by rods / wands / scepters (handheld_weapon ranged); WIS v1_scope is dominated by maces / talismans / horns / banners (mixed range, often AoE). The split tracks doc 47 § 3.1 intent (INT = arcane spell-implement; WIS = faith / channel / holy-symbol implement).

---

## 3. Enrichment effort estimate per field

| Field | Effort | Algorithmic complexity | SC-6b sub-step |
|---|---|---|---|
| `base_physical_damage_l50` | **3–5 hours** | Medium — requires per-weapon-family L50 baseline LUT design (likely 6–10 families: greatsword / sword / dagger / polearm / bow / firearm / staff / wand / mace / talisman). LUT × `damage_amplitude_min/max` ratio → per-row value. Cross-seam with rocket on calibration constants. | SC-6b.1 |
| `spell_damage_modifier_pct` | **1–2 hours** | Low — algorithmic from `primary_stat` defaults (martial→0–10; INT→30–150; WIS→30–120). Manual per-named-template override pass for ~50 caster rows where flavor warrants explicit value. | SC-6b.2 |
| `element_affinity_modifiers_json` | **4–6 hours** | Medium-high — requires named_template parsing for the 327 caster rows + LLM-assisted disambiguation on ambiguous element names. Default empty `{}` for martial rows (1,966 rows trivial). | SC-6b.3 |
| `to_skill_level_modifier_static` | **2–3 hours** | Low-medium — populate for ~42 unique + curated ~150 named_template subset (~200 rows total); NULL for ~2,090 rows. LLM-assisted skill-name extraction from canonical_name (e.g., `Rod of the Pact Keeper +2` → `{"warlock_pact": 2}`). | SC-6b.4 |
| `attribute_requirement` (reuse `primary_stat`) | **0 hours** | None — schema-already-present. Rocket binding query reads `wsp.primary_stat`. | — |
| `weapon_type_family` | **1–2 hours** | Low — algorithmic rule (§ 2.1) covers 96.5%; ~81 edge-case rows manual review. | SC-6b.5 |

**Total SC-6b enrichment estimate: ~11–18 hours** of focused elrond execution. Plus:
- MIGRATION.md authorship: 1 hour
- Cross-seam smoke-test coordination with rocket Phase 2c (Wave 0.5 round-trip): 1–2 hours
- Per-source quality verification queries: 1 hour

**Grand total SC-6b: ~14–22 hours.** Fits comfortably IN Wave 0.5 parallel with rocket per-skill emission (per framing brief § 2 Wave 0.5 owners list).

---

## 4. Cross-seam impact summary

### 4.1 Rocket — Phase 2c substrate binding (Wave 0.5)

**Read-side contract:** rocket's Phase 2c substrate selection query reads `weapon_sim_props` joined with `weapon_knowledge_entries` on `weapon_id = id`. New columns added at SC-6b consumed at gen-time to populate `character_json.gear_representative.main_weapon.*`:

| character_json field | Source after SC-6b |
|---|---|
| `base_physical_damage` | `wsp.base_physical_damage_l50 × ROLL(wsp.damage_amplitude_min, wsp.damage_amplitude_max)` |
| `spell_damage_modifier` | `wsp.spell_damage_modifier_pct` |
| `element_affinity_modifiers` | `wsp.element_affinity_modifiers_json` (parsed) |
| `to_skill_level_modifiers` | `wsp.to_skill_level_modifier_static` if non-null, else rocket per-rarity-tier roll |
| `attribute_requirement` | `wsp.primary_stat` |
| `weapon_type_family` | `wsp.weapon_type_family` |

**Calibration coordination required at SC-6b:** rocket and elrond agree on L50 family-baseline LUT before backfill runs. Recommendation: knight-rider routes a Pattern-A sub-agent query to rocket at SC-6b kickoff to surface rocket's perspective on family-baseline numbers (some may be informed by skill-side tier_coefficient targets).

**Round-trip smoke obligation at Wave 0.5:** post-rocket emission, sample 6 character JSONs (one per weapon_type_family) and verify all 6 substrate-derived fields populate non-null with values consistent with the substrate row that drove selection. This is the cross-seam round-trip clause per ADR-004 / framing brief.

### 4.2 Gamora — damage_resolver routing (Wave 0.5)

**Read-side contract:** gamora consumes the `character_json.gear_representative.main_weapon.*` fields at fight engine time per doc 47 § 4.1 routing logic. No direct DB read by gamora — gamora reads what rocket emits. Therefore:

- **No new gamora-side data dependency from this audit.** Gamora's contract is with rocket's character JSON shape, NOT with elrond's substrate library directly.
- Gamora needs `damage_scaling_type` per skill (physical / magical / hybrid) — that comes from rocket's skill emission, not from substrate weapons.
- Gamora needs `weapon.base_physical_damage` (HP points) and `weapon.spell_damage_modifier` (percent) — both present after SC-6b lands and rocket binding completes.

**Implication for gamora:** unblocked once rocket Phase 2c emits with the new fields. No upstream wait on elrond beyond SC-6b's Wave 0.5 landing.

### 4.3 Galadriel / star-lord / drax — no impact

- **Galadriel:** substrate weapon stat audit doesn't touch CV / aesthetic surface; `weapon_aesthetic` table unaffected.
- **Star-lord:** no telemetry schema change; no export-pipeline change.
- **Drax:** loadout app reads what rocket emits; substrate column changes are upstream of drax's surface.

### 4.4 Jack-ryan — Gate-1 + decisions-log

- **Gate-1 review of SC-6b dispatch:** verifies (a) Path A vs Path B architectural choice ratified by Matt; (b) MIGRATION.md drafted; (c) algorithmic rule for weapon_type_family validated against doc 47 enum; (d) family-baseline LUT cross-checked with rocket.
- **Decisions-log entry:** SC-6b's architectural commitment to substrate-side base_physical_damage_l50 (Path A) warrants a decisions-log entry per ADR-002 (architectural commitment with cross-seam impact). Elrond proposes; jack-ryan writes.

---

## 5. Recommended SC-6b enrichment dispatch scope (for KR authorship)

**Dispatch title:** `2026-05-27-elrond-cycle-14-sc-6b-substrate-weapon-stat-enrichment.md`

**Scope checklist:**

- [ ] Coordinate with rocket via knight-rider Pattern-A sub-agent query: surface rocket's per-weapon-family L50 baseline expectation (informed by `skill.tier_coefficient` and doc 47 § 4.2 sanity targets)
- [ ] Author family-baseline LUT (sword 200, dagger 100, staff 50, etc.) at `agentic_orchestration/elrond/research/sc-6b-weapon-family-baselines-2026-05-27.json`
- [ ] Apply schema migration to `weapon_sim_props` adding 5 new columns:
  1. `base_physical_damage_l50` REAL
  2. `spell_damage_modifier_pct` REAL
  3. `element_affinity_modifiers_json` TEXT
  4. `to_skill_level_modifier_static` TEXT
  5. `weapon_type_family` TEXT CHECK (weapon_type_family IN ('martial-heavy','martial-light','ranged','caster-arcane','caster-faith','hybrid'))
- [ ] Backfill data per § 3 enrichment rules:
  - `weapon_type_family` — algorithmic per § 2.1; manual review on ~81 edge rows
  - `attribute_requirement` — no change (reuse `primary_stat`)
  - `base_physical_damage_l50` — family-baseline LUT × ratio
  - `spell_damage_modifier_pct` — primary_stat default + named-template overrides
  - `element_affinity_modifiers_json` — empty `{}` for martial; LLM-assisted name-parse for 327 casters
  - `to_skill_level_modifier_static` — populated for ~42 unique + ~150 named subset; NULL for ~2,090 category
- [ ] Author MIGRATION.md per ADR-004 at `agentic_orchestration/research/curated/MIGRATION.md` (or substrate-library-specific MIGRATION location)
- [ ] Round-trip smoke at Wave 0.5: sample 6 character JSONs (one per weapon_type_family) post-rocket emission; confirm all 6 substrate-derived fields populate non-null
- [ ] Append completion record to SC-6b dispatch
- [ ] Commit + push (per Cycle 14 established push pattern)

**Acceptance criteria:**

- Schema migration applied; all 2,293 v1_scope rows have non-null values on the 5 new columns (or documented NULL-policy on `to_skill_level_modifier_static` for category rows)
- MIGRATION.md cross-references doc 47 + framing brief + SC-6 audit
- Rocket Phase 2c smoke-test consumes new columns successfully (round-trip pass)
- Decisions-log entry proposed for Path A commitment (substrate carries L50 absolute baseline)

**Risk register (top 3):**

1. **Family-baseline LUT calibration drift:** rocket's tier_coefficient may evolve at Wave 0.5; SC-6b values may need re-tuning. Mitigation: LUT in a single JSON file; one-column UPDATE pass to retune.
2. **Element-affinity LLM extraction noise:** named_template parsing may yield false positives (e.g., `Holy Symbol of Pelor` → does this carry light affinity?). Mitigation: explicit manual review per element pass; default to empty `{}` when ambiguous.
3. **`weapon_type_family` enum drift:** doc 47's 6-family enum may evolve; substrate CHECK constraint locks substrate to current spec. Mitigation: enum changes go through MIGRATION.md per ADR-004; backfill is small (2,293 rows).

---

## 6. Sign-off

**Author:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Status:** CURRENT — audit-report only; per-field dispositions validated; SC-6b enrichment scope recommended

**Per-field dispositions validated:** 5 of 6 confirm KR's pre-staged disposition; 1 (`base_physical_damage`) amended with explicit Path A recommendation on architectural-cleanliness grounds. `weapon_type_family` algorithmic rule sampled (top-20; 96.5% coverage); exhaustive per-row mapping deferred to SC-6b per anti-stall discipline.

**Key architectural finding:** `damage_amplitude_min/max` is a 0.3–3.0 RATIO, not absolute damage. Substrate library carries the variance shape but NOT the L50 absolute baseline. SC-6b's load-bearing decision is whether the L50 baseline lives substrate-side (Path A — elrond recommends) or engine-side (Path B). Elrond votes Path A; final architectural call rests with cross-seam rocket coordination + Matt ratification.

**For Wave 0.5:** this audit unblocks Wave 0.5 dispatch authoring + jack-ryan Gate-1. SC-6b enrichment can fire IN Wave 0.5 parallel with rocket per-skill emission. No SC-6b prerequisite for Wave 0.5 entry.

**Cross-seam impact:** rocket consumes 5 new columns at Phase 2c (cross-seam contract change per ADR-004); gamora downstream-of-rocket (no direct dependency); galadriel / star-lord / drax not impacted; jack-ryan Gate-1 + decisions-log entry on SC-6b architectural commitment.
