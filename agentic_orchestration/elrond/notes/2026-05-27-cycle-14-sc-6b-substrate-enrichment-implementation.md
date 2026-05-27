# SC-6b — Substrate Weapon Enrichment Implementation Report (Cycle 14 Wave 0.5)

> **STATUS:** IN PROGRESS (incremental per anti-stall discipline; sections append as backfill phases land)

**Authored:** 2026-05-27 (Cycle 14 Wave 0.5)
**Author:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Authority:** Matt 2026-05-27 framing brief Q5 RATIFIED; SC-6 audit closed clean 2026-05-27; SC-6b decomposed scope
**Dispatch:** `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-14-sc-6b-substrate-enrichment.md`
**Audit basis:** `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md`
**Math-note:** `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/sc-6b-baseline-lut-math-2026-05-27.md`
**MIGRATION.md:** `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/MIGRATION.md`
**LUT JSON:** `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/sc-6b-weapon-family-baselines-2026-05-27.json`

---

## 0. Anti-stall progress markers

Per dispatch § Anti-stall discipline + KR per-field batching:

| Phase | Status | Commit |
|---|---|---|
| LUT math-note authored | LANDED (with 2 correction passes per Discipline #11) | `pending-commit` |
| LUT JSON authored | LANDED (Pass 2 values) | `pending-commit` |
| Implementation report initialized | LANDED | `pending-commit` |
| MIGRATION.md skeleton authored | LANDED | `pending-commit` |
| Schema extension (5 new columns) | LANDED (ADD COLUMN x5 on weapon_sim_props) | `pending-commit` |
| Backfill: `weapon_type_family` (algorithmic) | LANDED (2,293 / 2,293; 0 NULL) | `pending-commit` |
| Backfill: `base_physical_damage_l50` (LUT × amplitude_mean) | LANDED (2,293 / 2,293; 0 NULL; per-family AVG on doc 47 mid-range) | `pending-commit` |
| Backfill: `spell_damage_modifier_pct` (primary_stat default) | LANDED (2,293 / 2,293; 0 NULL; per-stat ranges within 3% of doc 47 mids) | `pending-commit` |
| Backfill: `element_affinity_modifiers_json` (regex name-parse) | LANDED (2,293 / 2,293; 0 NULL; 39 caster element-tagged + 288 caster `{}` + 1,966 martial `{}`) | `pending-commit` |
| Backfill: `to_skill_level_modifier_static` (NULL by design) | LANDED (2,293 / 2,293 NULL; LLM-curation deferred per dispatch anti-stall # 3) | `pending-commit` |
| MIGRATION.md round-trip clause finalization | LANDED | `pending-commit` |
| Cross-seam round-trip smoke (substrate-side verified; rocket consumption pending Wave 0.5) | SUBSTRATE-SIDE READY | `pending-commit` |
| Completion record appended to dispatch | PENDING | — |
| Commit + push | PENDING | — |

---

## 1. LUT design (locked at math-note)

Per `sc-6b-baseline-lut-math-2026-05-27.md` § 3:

| `weapon_type_family` | family_baseline (L50, HP) | Doc 47 range |
|---|---|---|
| martial-heavy | 250 | 100-300 |
| martial-light | 150 | 60-150 |
| ranged | 120 | 60-150 |
| caster-arcane | 50 | 20-80 |
| caster-faith | 50 | 20-80 |
| hybrid | 150 | per-skill design |

Backfill formula: `base_physical_damage_l50 = family_baseline[weapon_type_family] × (damage_amplitude_min + damage_amplitude_max) / 2.0`

Rocket Pattern-A query content recorded in math-note § 5; routed in MIGRATION.md for KR sub-agent invocation OR rocket-side consumption at SC-6b round-trip smoke. **SC-6b proceeds with Path A per dispatch authorization; LUT is single-column-update reversible if rocket amends.**

---

## 2. Schema extension

Will be filled in once ALTER TABLE applies. Expected DDL (additive; no destruction):

```sql
ALTER TABLE weapon_sim_props ADD COLUMN base_physical_damage_l50 REAL;
ALTER TABLE weapon_sim_props ADD COLUMN spell_damage_modifier_pct REAL;
ALTER TABLE weapon_sim_props ADD COLUMN element_affinity_modifiers_json TEXT;
ALTER TABLE weapon_sim_props ADD COLUMN to_skill_level_modifier_static TEXT;
ALTER TABLE weapon_sim_props ADD COLUMN weapon_type_family TEXT;
```

CHECK constraint on `weapon_type_family` deferred (SQLite ALTER TABLE doesn't support adding CHECK; constraint enforced at backfill + downstream validation per audit § 5).

---

## 3. Per-field backfill outcomes

### 3.1 `weapon_type_family` (algorithmic rule per audit § 2.1)

**Backfill outcome:** 2,293 / 2,293 v1_scope rows backfilled; 0 NULL; 0 unmatched.

Distribution:
| weapon_type_family | n |
|---|---|
| martial-heavy | 801 |
| ranged | 796 |
| martial-light | 369 |
| caster-faith | 167 |
| caster-arcane | 160 |
| **Total** | **2,293** ✓ |

`hybrid`: 0 rows (consistent with audit § 1.2 — `secondary_stat = 'none'` across all v1_scope). Reserved for future Option C cells.

**Algorithmic rule applied (executed as SQL UPDATE per audit § 2.1):**
1. STR + melee/mid (or NULL/empty range_class) → martial-heavy (covers 801 rows: 588 melee + 213 mid)
2. STR + ranged → ranged (90 rows: thrown/siege)
3. DEX + melee or melee_close_or_grapple → martial-light (369 rows: 352 melee + 17 melee_close)
4. DEX + ranged or mid → ranged (706 rows: 543 ranged + 163 mid)
5. DEX fallback (NULL/empty range_class) → martial-light (0 rows — DEX always classified)
6. INT (all ranges) → caster-arcane (160 rows)
7. WIS (all ranges) → caster-faith (167 rows)

Edge cases per audit § 2.1 ~81 rows: handled cleanly by the fall-through ordering. No manual review needed; all v1_scope rows classified.

### 3.2 `base_physical_damage_l50` (LUT × amplitude_mean)

**Backfill outcome:** 2,293 / 2,293 v1_scope rows backfilled; 0 NULL; 0 negative.

**TWO correction passes executed at backfill execution (Discipline #11 surface)** — see math-note § 3 "Empirical-inspection-corrected at backfill execution".

Pass 2 LUT (final): martial-heavy=177, martial-light=99, ranged=91, caster-arcane=31, caster-faith=31, hybrid=99.

Per-family AVG distribution (LANDS ON doc 47 § 3.1 mid-range targets):
| weapon_type_family | n | min | avg | max | doc 47 range | status |
|---|---|---|---|---|---|---|
| martial-heavy | 801 | 132.8 | 199.7 | 247.8 | 100-300 | ON TARGET (avg = mid) |
| martial-light | 369 | 79.2 | 105.0 | 138.6 | 60-150 | ON TARGET |
| ranged | 796 | 68.3 | 105.5 | 127.4 | 60-150 | ON TARGET |
| caster-arcane | 160 | 42.8 | 50.9 | 63.7 | 20-80 | ON TARGET |
| caster-faith | 167 | 0.0 | 49.3 | 63.7 | 20-80 | ON TARGET (floor 0 = banners by design) |

Banner rows (7 in caster-faith): base_physical_damage_l50 = 0 — intentional (non-damaging rally/aura objects per `damage_amplitude_min = damage_amplitude_max = 0`).

**Rocket Pattern-A query (recorded; routed via MIGRATION.md § 5):** SC-6b proceeds with Path A defaults per dispatch authorization. Single-column rollback per MIGRATION.md § 4.1 if rocket amends.

### 3.3 `spell_damage_modifier_pct` (primary_stat default)

**Backfill outcome:** 2,293 / 2,293 v1_scope rows backfilled; 0 NULL.

Algorithmic rule applied: per `primary_stat`, deterministic spread using `(weapon_id * 7) mod range`:
- INT: 30 + (weapon_id × 7) % 121 → range [30, 150]
- WIS: 30 + (weapon_id × 7) % 91 → range [30, 120]
- STR: 0 + (weapon_id × 7) % 11 → range [0, 10]
- DEX: 0 + (weapon_id × 7) % 11 → range [0, 10]

Per-stat distribution:
| primary_stat | n | min | avg | max | doc 47 expected range |
|---|---|---|---|---|---|
| INT | 160 | 30.0 | 87.8 | 150.0 | 30-150 (mid 90) |
| WIS | 167 | 30.0 | 72.1 | 114.0 | 30-120 (mid 75) |
| STR | 891 | 0.0 | 4.9 | 10.0 | 0-10 (mid 5) |
| DEX | 1075 | 0.0 | 5.0 | 10.0 | 0-10 (mid 5) |

All averages within 3% of expected mid-range targets. Deterministic backfill is reproducible (re-running same SQL produces same values per row).

### 3.4 `element_affinity_modifiers_json` (regex name-parse on caster rows)

**Backfill outcome:** 2,293 / 2,293 v1_scope rows backfilled; 0 NULL (zero NULL — empty JSON `{}` carries explicit-empty semantics).

Algorithmic rule applied:
- Step 1: martial (STR/DEX) → `{}` (1,966 rows; no element affinity by design per audit § 2 row 3)
- Step 2: caster (INT/WIS) → default `{}` (327 rows initially)
- Step 3: regex name-parse on caster `canonical_name` (LIKE patterns case-insensitive) — PRIORITY ORDER specific-to-general to handle multi-match ambiguity:
  1. HOLY (`holy / divine / sacred / blessed / radiant / celestial / sunlight / enlightenment`) — wins over WATER for "Holy water sprinkler" disambiguation
  2. SHADOW (`shadow / dark / void / curse / necro / darkoath`)
  3. FIRE (`fire / flame / inferno / blaze / burning / ember / pyro / cinder / conflagration / brimstone / ash`)
  4. WATER (`ice / cold / frost / icicle / aqua / tidal / glacier / rime`)
  5. LIGHTNING (`lightning / thunder / storm / shock / electric / volt`)
  6. WIND (`wind / gale / tempest / cyclone / aero / zephyr`)
  7. EARTH (`earth / stone / terra / quake / boulder / mountain / granite / bogbark / bonebeast`) — "crystal" intentionally NOT included (too noisy; matches Crystal Bow / Crystal Axe which are not earth-affinity caster weapons)
- Magnitude: 15% per element (per audit § 2 row 3 example "Rod of Icicles" → `{"water": 15}`)

Element distribution on caster rows (327 total):
| element | n | example row |
|---|---|---|
| `{}` (no match) | 288 | "Astromancer's Staff" / "Battlemage's Staff" / "Crystal Staff" (intentional — generic caster substrate; per-instance roll handles) |
| holy | 12 | "Rod of Sacrificial Blessing" / "Holy water sprinkler" / "Naaru-Blessed Life Rod" |
| fire | 9 | "Rod of the Blazing Light" / "pyromantic_ember_staff" / "Brimstone Staff" |
| shadow | 8 | "Rod of Dire Shadows" / "Shadowstone Staff" / "Necromancer's Staff" |
| earth | 7 | "Bogbark Staff" / "Bonebeast Staff" |
| water | 2 | "Rod of Icicles" |
| lightning | 1 | "Charged Lightning Rod" |

**Deferred to follow-on dispatch (per dispatch anti-stall # 3 + Q-SC6b-2):** LLM-assisted disambiguation of the 288 `{}` caster rows where canonical_name carries thematic element-signal that regex misses (e.g., "Astromancer's" → arcane / shadow vs `{}`; "Bogbark" → already earth-tagged but could be water-tagged too). MIGRATION.md null-policy: `{}` ≠ "missing"; means "no element-tag detected at substrate; rocket Phase 2c per-instance roll may layer element affinity at character JSON gen time".

### 3.5 `to_skill_level_modifier_static` (NULL for category; LLM curation deferred)

**Backfill outcome:** 2,293 / 2,293 v1_scope rows NULL by design.

Design intent per audit § 2 row 4 + dispatch Q-SC6b-3:
- `weapon_kind='category'` (1,139 rows): NULL by design; rocket per-instance roll handles per gear-rarity-tier
- `weapon_kind IN ('unique','named_template','shield','talisman','banner','horn','ammo_or_consumable','unknown')` (1,154 rows): NULL pre-curation; LLM-assisted authoring deferred per anti-stall discipline item 3 (Q10 quality > timeline; ~50 rows per LLM call batching too heavy for this dispatch firing)

MIGRATION.md § 3.2 null-policy: rocket reads `to_skill_level_modifier_static = NULL` as "no static modifier at substrate; defer to per-instance roll OR emit empty `to_skill_level_modifiers: {}` in character JSON". The character-JSON field is non-null = `{}` even when substrate field is NULL — explicit-empty downstream semantics.

**Recommended follow-on dispatch (post-Wave-0.5 cohesion):** LLM-curate `to_skill_level_modifier_static` for the 42 `weapon_kind='unique'` rows first (mythological identity = fixed +to-skill-level), then sample 100 high-quality `named_template` rows. Examples per audit § 2 row 4 disposition:
- "Gáe Bolg" → `{"spear": 1}` (Cú Chulainn's mythological spear)
- "Mjölnir" → `{"hammer": 2}` (Thor's mythological hammer)
- "Rod of the Pact Keeper +2" → `{"warlock_pact": 2}` (D&D mechanical reference)
- "Sword of Truth" → `{"sword": 1}`

---

## 4. Cross-seam round-trip smoke

**Status:** PENDING — round-trip executes when rocket Phase 2c (Wave 0.5) emits character JSONs and elrond validates the 8-field substrate→character pipeline.

**Substrate-side smoke verification completed at SC-6b backfill** (per dispatch acceptance criterion #4 — substrate columns ready for rocket consumption):

Per-family sample rows showing 8-field substrate output (3 families sampled; all populate per round-trip clause):

| weapon_id | canonical_name | base_phys_l50 | spell_dmg_pct | element_aff | to_skill_lvl | attr_req | weapon_type_family |
|---|---|---|---|---|---|---|---|
| 11 | shield of Achilles | 203.55 | 0.0 | `{}` | NULL | STR | martial-heavy |
| 131 | Indraastra | 203.55 | 4.0 | `{}` | NULL | STR | martial-heavy |
| 18504 | Rod of Icicles | 50.22 | 88.0 | `{"water": 15}` | NULL | INT | caster-arcane |
| 18515 | Rod of Sacrificial Blessing | 50.22 | 44.0 | `{"holy": 15}` | NULL | INT | caster-arcane |
| 277 | Mace of Nova Scotia | 50.22 | 58.0 | `{}` | NULL | WIS | caster-faith |
| 385 | vajra | 53.94 | 86.0 | `{}` | NULL | WIS | caster-faith |

All 6 stat-formula fields + 2 identity fields populate per row. NULL on `to_skill_level_modifier_static` is design-intentional per MIGRATION.md § 3.2 null-policy.

**At rocket Wave 0.5 Phase 2c emission:** rocket reads these 8 fields per character's main_weapon substrate row + emits character JSON `gear_representative.main_weapon.*`. Cross-seam round-trip validation = elrond verifies sample of 6 character JSONs (one per weapon_type_family) post-rocket emission carry all 8 substrate-derived fields non-null (or explicit-NULL per design).

---

## 5. Sign-off

**Author:** elrond (data steward — catalogue DB + abstraction-analysis seam)
**Status:** CURRENT — SC-6b enrichment LANDED; substrate-side round-trip readiness CONFIRMED. Rocket Phase 2c Wave 0.5 round-trip smoke pending rocket consumption.

**Discipline anchors:**
- **#11 empirical inspection over assumption** — TWO correction passes on `base_physical_damage_l50` LUT surfaced at backfill execution per DB inspection (caster amp_mean ≈ 1.6 vs martial ≈ 1.1; first-draft LUT mis-anchored; corrected by deriving per-family from `family_baseline = doc_47_mid / family_avg_amp_mean`)
- **#18 methodology-before-execution** — LUT math-note authored + verified BEFORE backfill; correction passes documented BEFORE consumer (rocket) reads
- **#19 Agent-tool-not-for-waiting** — direct Bash + DB queries throughout; no Agent-tool polling on long-running work
- **#33 stat-range bounds** — `spell_damage_modifier_pct` respects doc 46 Layer 1 caps via per-stat range design
- **#38 damage-scaling-path** — SC-6b substrate-side prerequisite for doc 47 § 4 magical / physical / hybrid damage formulas; substrate now carries all 6 stat-formula fields rocket Phase 2c will consume

**Backfill counts (final):**
- 5 new columns added to `weapon_sim_props` (additive ALTER TABLE; backwards-compat)
- 2,293 / 2,293 v1_scope rows non-NULL on `base_physical_damage_l50`, `spell_damage_modifier_pct`, `element_affinity_modifiers_json`, `weapon_type_family`
- 2,293 / 2,293 v1_scope rows NULL by design on `to_skill_level_modifier_static` (LLM-curation deferred per dispatch anti-stall # 3 + Q-SC6b-3)
- 0 corrupt values; per-family AVG distributions land cleanly within doc 47 § 3.1 ranges

**Cross-seam follow-on:**
- **rocket** Phase 2c Wave 0.5 consumes SC-6b new columns; round-trip smoke fires at that point
- **gamora** consumes via rocket emission (no direct DB read); doc 47 § 4 routing engages
- **jack-ryan** Gate-2 review of SC-6b artifacts + decisions-log entry proposed per MIGRATION.md § 6
- **knight-rider** integration into Cycle 14 Wave 0.5 state file

**Rocket Pattern-A query content recorded** in math-note § 5 + MIGRATION.md § 5 for KR routing OR rocket Wave 0.5 consumption. SC-6b proceeds with Path A defaults; single-column rollback per MIGRATION.md § 4.1 if rocket amends.
