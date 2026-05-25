# Stage 4 Mechanical-Tagging Methodology Recommendation
# Cycle 10 Wave 7 — Legolas Mode A Methodology Consult

**Mode:** A (analytical methodology consult)
**Date:** 2026-05-25
**Commissioner:** rocket (execution lead) via knight-rider dispatch authority `2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md` § 4.1
**Dispatch authority:** Cycle 10 Wave 7 dispatch § 4.1 + Discipline #18.2 (consultation-after-baseline at extension hotspot)
**Baseline empirical evidence consumed:**
- Stage 1 v1.1 confidence-distribution report (`cycle-10-stage-1-2026-05-24/confidence-distribution-v1-1.md`)
- Stage 1.5 per-source schema mapping + coverage histogram (`cycle-10-stage-1-5-2026-05-24/`)
- Stage 3 Phase 3 v1_scope distribution report (`cycle-10-stage-3-2026-05-25/v1-scope-distribution-report.md`)
- Live DB queries against `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (2026-05-25)
- BC-axes lock (`canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`)
- Composition policy v1 (`canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`)
- Attribute system (`canonical/story/attribute-system-2026-05-24.md`)
- v1 BC-target intent / Sketch A (`canonical/story/v1-bc-target-intent-2026-05-24.md`)

---

## Summary

Stage 4 mechanical-tagging on v1_scope (3,042 rows total; 1,890 typed + 1,152 NULL-typed) populates `weapon_sim_props` per-row values across 7 fields: range_min/max, base_attack_speed, charge_time, hits_per_attack, aoe_radius, damage_amplitude_min/max (schema gap to close), primary_stat. The methodology recommended here is a layered 3-pass approach: (1) heuristic derivation from Stage 1 proxy columns + Stage 1.5 extracted_length/weight for already-typed rows; (2) structured-property LLM-judge for NULL-typed rows with weapon_type keys; (3) cultural-lineage + canonical_name LLM-judge for the remainder. Damage amplitude is tagged via a **min/max scalar pair** (not variance coefficient) calibrated to BC Axis 3B bins. NULL-typed row treatment is the largest methodological challenge; the recommendation is a two-tier heuristic-then-LLM-judge pipeline that avoids blanket LLM calls across all 1,152 rows.

---

## (a) Chosen Baseline Approach + Rationale

### Pass 1 — Heuristic derivation for already-typed rows (1,890 rows)

For rows where Stage 1 proxy columns (`proxy_range_class`, `proxy_geometry_class`, `proxy_tempo_class`, `proxy_attribute_class`) are populated, `weapon_sim_props` values derive from fixed per-bin lookup tables applied to those proxy values, with Stage 1.5 `extracted_length_value` used as a refining signal where available.

**Rationale:** Stage 1 proxy columns are the lowest-cost signal with highest per-row coverage for typed rows (22,033 typed substrate-wide at v1.1). The proxy was designed as a mechanical fingerprint; it already encodes range/geometry/tempo/attribute bins. Per-bin numeric ranges in weapon_sim_props are deterministic from those bin assignments. This eliminates LLM calls for 62.1% of v1_scope (1,890 rows) at zero marginal LLM cost.

Stage 1.5 extracted_length refines range_min/max for 134 of the 1,890 typed rows that also have valid cm-unit length data — this subset gets tighter range bounds than pure-bin defaults.

### Pass 2 — Structured-property-key heuristic for NULL-typed rows with weapon_type (47 rows)

Of 1,152 NULL-typed v1_scope rows: 1,117 have `structured_properties` populated (97% coverage), and of those, 47 have a parseable `weapon_type` key (from empirical query: 47/1,152 = 4.1%). These weapon_type values (`"spear"`, `"bow"`, `"shield"`, `"sword"`, `"chakram"`, `"mythological weapon"`, etc.) support a weapon-kind lookup table that maps weapon_type string → (range_class, geometry_class, tempo_class, attribute_class) proxy tuple. Those proxy tuples then feed the same Pass 1 per-bin lookup.

**Rationale:** These 47 rows include many high-value mythological-register items (Gungnir → spear, Gandiva → bow, Sudarshana Chakra → chakram, Excalibur → sword). The weapon_type key is structured and controlled enough that a lookup-table heuristic outperforms LLM-judge on accuracy/cost for this specific subset. See § (c) for lookup table specifications.

### Pass 3 — LLM-judge for remaining NULL-typed rows (1,105 rows)

The remaining NULL-typed rows (1,152 - 47 = 1,105) have no usable structured weapon_type key. These derive primarily from:

- **royal_armouries (647 rows):** have `canonical_name` only (e.g., "Partizan", "Centrefire six-shot pepperbox", "Bayonet", "Lockplates", "Detached upper jaws"). Many are partial items or components, not complete weapons.
- **met-museum (193 rows):** have full canonical_name and often length/weight; 61 have extracted_length_value. These are the highest-quality NULL-typed rows.
- **odin-army-tradoc (168 rows):** modern military vehicles/UAVs (e.g., "Type 076 Class Chinese Amphibious Assault Ship", "LOONG X1 Chinese UAV") — see § (f) for special treatment.
- **wikipedia (85 rows):** have description text in canonical_name.
- **wikidata (46 rows):** have structured_properties but no weapon_type match.
- **Other sources (< 10 rows each):** thin tail.

For these rows, the LLM-judge receives: `canonical_name` + `cultural_lineage_canonical` + `register_canonical` + any available `structured_properties` text + any available `extracted_length_value` + `extracted_weight_value`, and outputs: (`proxy_range_class`, `proxy_geometry_class`, `proxy_tempo_class`, `proxy_attribute_class`) proxy 4-tuple.

Those proxy 4-tuples then feed the Pass 1 per-bin lookup for `weapon_sim_props` values.

**Separation of concerns:** Pass 3 produces proxy classification, not weapon_sim_props values directly. This keeps the LLM-judge scope narrow and allows the same per-bin lookup table to serve all three passes consistently.

### Per-cell-type policy operationalization (Option α/β/C)

The pass structure above is cell-type-agnostic at tagging time. Cell-type policy (Option α/β/C per composition policy § 3) operates at Phase 2 substrate-binding, not at Stage 4 tagging. Stage 4 produces mechanical profiles on all v1_scope rows regardless of cell-type. The cell-type policy then consumes those profiles:

- **Option α (martial; STR/DEX):** weapon_sim_props range/geometry/tempo/amplitude values are the binding coordinate at Phase 2; 5-tuple match required. Stage 4 must produce accurate values for these rows because the binding is tight.
- **Option β (caster; INT/WIS):** weapon_sim_props primary_stat is the binding coordinate; range/geometry/tempo/amplitude values are informational but not the binding axis. Stage 4 accuracy for these rows is lower-stakes at Phase 2.
- **Option C (cross-attribute hybrid):** ω-penalty set by construction. Stage 4 populates values normally; the penalty flag is a Phase 2 computation, not a Stage 4 column.

**Implication for tagging priority:** accuracy matters most for STR/DEX typed rows (Option α binding). The 1,890 already-typed rows in v1_scope are 84.7% DEX/STR by proxy_attribute_class — Pass 1 covers the Option α majority at heuristic accuracy. The LLM-judge pass (Pass 3) is predominantly applied to NULL-typed rows that are 86% historical european and will surface as STR/DEX-heavy once tagged; accuracy here matters for Option α binding. This is an argument for a conservative LLM-judge pass that defaults to melee-STR for ambiguous european-historical items rather than guessing exotic ranges.

---

## (b) Failure-Mode Signals

### Signal 1 — Per-axis distribution anomaly (primary)

Post-tagging, run per-axis bin distribution histogram on the full v1_scope population. Failure signal: any axis where actual distribution is >2 standard deviations from the pre-tagging typed distribution. Specific thresholds:

- `proxy_range_class`: pre-tagging typed distribution is melee 43.4% / ranged 35.1% / mid 21.4%. Post-tagging full distribution should remain within ±8pp of this prior. If mid climbs to >35% or ranged drops below 20%, heuristic is misclassifying something.
- `proxy_tempo_class`: pre-tagging typed distribution is medium 49.3% / low 27.1% / high 23.6%. Post-tagging should remain within ±8pp. High-tempo above 35% or low-tempo above 40% signals a lookup table error.
- `proxy_attribute_class` (critical for Option α/β): pre-tagging DEX 49.0% / STR 35.6% / WIS 7.9% / INT 7.5% (typed-only). Post-tagging INT/WIS share should increase somewhat (NULL-typed pool includes historical european items that frequently tag as STR-melee, plus wikidata mythological items that span all attributes). If INT+WIS post-tagging is still below 12% combined, the Pass 3 LLM-judge is likely defaulting to STR/DEX for mythological items that should be WIS/INT.

### Signal 2 — LLM-judge low-confidence rate above threshold

If Pass 3 LLM-judge returns a confidence score below 0.6 on more than 20% of queried rows, the methodology requires revision. Specific action: sample 30 low-confidence rows, inspect canonical_name quality, and determine whether the bottleneck is (a) ambiguous canonical_names that need description_text injected, (b) component parts rather than weapons (e.g., "Lockplates", "Detached upper jaws"), or (c) odin-army-tradoc modern-military rows that should have been excluded before the LLM pass.

### Signal 3 — weapon_sim_props range value implausible

After population, run: `SELECT COUNT(*) FROM weapon_sim_props WHERE range_max_units > 100 AND range_max_units IS NOT NULL`. Range_max_units in engine units maps to game distance; a `range_max_units > 100` for a melee weapon indicates a lookup table conversion error. Expected: zero rows of this pattern.

### Signal 4 — primary_stat CHECK constraint failure

The current `weapon_sim_props.primary_stat` CHECK constraint is `IN ('STR','INT','WIS')`. DEX is **NOT** in the current constraint. This will cause INSERT failures for all DEX-primary weapons. This is a schema bug that must be resolved before population executes. See § (c) parameter recommendation on schema fix.

### Signal 5 — Damage amplitude NULL rate

Post-population: `SELECT COUNT(*) FROM weapon_sim_props WHERE damage_amplitude_min IS NULL OR damage_amplitude_max IS NULL`. Should be zero after Stage 4 completes. Any NULLs indicate rows that fell through all three passes without amplitude assignment.

---

## (c) Parameter Recommendations

### Per-axis bin boundary thresholds

#### Range class from extracted_length_value (cm-normalized)

Empirical basis: DB query against 134 typed v1_scope rows with cm-unit length data shows:
- `melee` rows: mean 39.8 cm, p50 = 38.1 cm, p90 = 98.2 cm, max 116.8 cm (excluding outliers >200 cm)
- `mid` rows: all 30 observations cluster 141–289 cm (mean 237 cm, min 141 cm) — this is polearm/spear territory
- `ranged` rows: mean 75 cm (excluding outliers), p25 = 24.8 cm, p50 = 70.3 cm, p75 = 117.5 cm

**Recommended thresholds:**

```
length_cm < 100       → range_class = 'melee'     (confidence: HIGH if weapon_kind not projectile)
100 ≤ length_cm < 130  → range_class = 'melee'     (long melee — two-handed swords, halberds on lower end)
130 ≤ length_cm < 400  → range_class = 'mid'       (polearm / spear / reach-weapon territory)
length_cm ≥ 400        → range_class = 'ranged' OR 'mid' depending on weapon_kind
length absent          → fall through to weapon_kind heuristic
```

**Override rule:** if `weapon_kind` or `weapon_type` indicates a projectile launcher (bow, crossbow, firearm, atlatl, sling), assign `range_class = 'ranged'` regardless of physical length. A crossbow may be 70 cm long (length of the stock) but fires at ranged distances.

**Confidence scoring:**
- `length_cm available + weapon_kind confirmed projectile/reach`: HIGH (0.85)
- `length_cm available + weapon_kind absent`: MEDIUM (0.65) — length alone is ambiguous (a 120 cm spear in transport vs a 120 cm bow)
- `weapon_kind available but length absent`: MEDIUM (0.65) if weapon_kind is in known-class lookup
- `canonical_name heuristic only`: LOW (0.45)
- `structured_properties weapon_type key only`: MEDIUM (0.65)

#### Tempo bin from extracted_length + weapon_kind (Pass 1 lookup)

Tempo bin assignment in Stage 1 proxy already encodes this relationship. The per-bin lookup table for `base_attack_speed` should use:

```
tempo_class = 'high'   → base_attack_speed = 2.5 attacks/sec  (daggers, shortswords, quick weapons)
tempo_class = 'medium' → base_attack_speed = 1.5 attacks/sec  (standard weapon tempo)
tempo_class = 'low'    → base_attack_speed = 0.7 attacks/sec  (heavy weapons, charged shots)
```

These are ARPG-canonical priors (per BC-axes lock § 3.5 thresholds: low < 2 events/s, medium 2-6, high ≥ 6 events/s). `base_attack_speed` represents the weapon's contribution to hits/sec, not skill cast rate. Weapons contributing to high-tempo kits deliver more frequent hits at lower per-hit damage amplitude.

`charge_time_s`:
- `tempo_class = 'high'`: charge_time = 0.0 (instant)
- `tempo_class = 'medium'`: charge_time = 0.0 (standard)
- `tempo_class = 'low'` + `attribute_class IN ('STR','DEX')` (martial): charge_time = 0.5 s
- `tempo_class = 'low'` + `attribute_class IN ('INT','WIS')` (caster, Option β): charge_time = 1.2 s (ritual/charge-up)

#### Geometry bin to weapon_sim_props field mapping

```
geometry_class = 'single'   → hits_per_attack = 1, aoe_radius = 0.0
geometry_class = 'cleave'   → hits_per_attack = 1, aoe_radius = 1.5 (arc sweep ~1.5 tile radius)
geometry_class = 'AoE'      → hits_per_attack = 1, aoe_radius = 3.5 (area-blast per BC Axis 2 > 3 tile threshold)
geometry_class = 'multi-hit' → hits_per_attack = 3, aoe_radius = 0.0 (multi-hit per-target)
geometry_class = 'scatter'  → hits_per_attack = 1, aoe_radius = 1.0, (spread-projectile ~1 tile)
geometry_class = 'cone'     → hits_per_attack = 1, aoe_radius = 2.0 (cone treated as small AOE)
```

**Note on BC Axis 2 aoe_radius thresholds (per BC-axes lock § 3.2):** single-target `aoe_radius ≤ 0.5`, small-AOE `0.5 < aoe_radius ≤ 3.0`, large-AOE `> 3.0`. The cleave bin (1.5) maps to small-AOE in BC measurement; AoE bin (3.5) maps to large-AOE. This is correct — geometry-class from Stage 1 proxy is a substrate property; BC Axis 2 geometry is a kit-level measurement aggregated over skill composition. The substrate geometry-class informs which BC bin a weapon naturally supports, but the BC assignment happens at simulation time.

#### Range_min/max field values (engine units, not cm)

Engine units are tiles (per BC-axes lock § 3.1: melee ≤ 3 tiles, mid 3-8 tiles, ranged > 8 tiles). Conversion from substrate cm to engine tiles is NOT a 1:1 mapping — physical weapon length ≠ effective combat range.

**Recommended range_min / range_max per range_class bin (engine tile units):**

```
range_class = 'melee'  → range_min = 0.5, range_max = 2.5
range_class = 'mid'    → range_min = 2.5, range_max = 7.0
range_class = 'ranged' → range_min = 5.0, range_max = 18.0
```

These are substrate-defaults. Stage 1.5 extracted_length refines range_max for rows where length data is available by applying a scaling factor derived from the empirical distribution (melee p90 ≈ 100 cm → range_max ≈ 3.0; mid mean ≈ 237 cm → range_max ≈ 7.0). The linear scaling factor is approximately `range_max_tiles = extracted_length_cm × 0.028`. Apply this refinement only for rows in the confidence ≥ 0.65 band; for 0.45-0.64 band rows, use bin defaults.

### Damage-amplitude rubric design

**Chosen representation: min/max scalar pair (damage_amplitude_min REAL, damage_amplitude_max REAL).**

**Rationale for min/max over variance coefficient:**

The BC-axes lock § 3.6 defines Axis 3B (Damage Amplitude Variance) in terms of CV (stdev/mean) of per-damage-event magnitudes. However, Stage 4 is a substrate-level tag, not a simulation measurement. The substrate does not have fight telemetry yet — amplitude variance is a sim output, not a sim input. What Stage 4 CAN populate is the weapon's inherent damage range (the scalar bounds on the weapon's per-hit damage roll). The CV is then an emergent property measured at simulation time from those bounds.

Variance coefficient as a schema column would be circular: to compute CV = stdev/mean from a distribution, the distribution must already be defined. min/max defines the distribution (assuming uniform or triangular draw within bounds); CV is then derivable at sim time as `(max - min) / (2 * sqrt(3) * (max + min) / 2)` for uniform, or computed directly from fight telemetry. Storing min/max is the appropriate substrate-level representation.

**Distribution model:** uniform distribution assumed at sim entry. `damage_roll = uniform(damage_amplitude_min, damage_amplitude_max)`. This produces CV ≈ `(max - min) / (sqrt(3) * (max + min))`. Under this model, the BC Axis 3B bin boundaries (CV 0.3 / 0.7) translate to:

```
flat     (CV < 0.3)    → amplitude_max / amplitude_min < 1.9×  (narrow spread)
variable (CV 0.3–0.7)  → amplitude_max / amplitude_min in [1.9×, 4.5×]
spiky    (CV ≥ 0.7)    → amplitude_max / amplitude_min > 4.5×
```

**Per-bin baseline amplitude values (normalized to amplitude_min = 1.0):**

```
proxy_geometry_class = 'single',  tempo = 'high'  → amplitude_min = 0.8,  amplitude_max = 1.2  (flat; ratio 1.5×)
proxy_geometry_class = 'cleave',  tempo = 'medium'→ amplitude_min = 0.7,  amplitude_max = 1.4  (flat-variable boundary; ratio 2.0×)
proxy_geometry_class = 'AoE',     tempo = 'low'   → amplitude_min = 0.4,  amplitude_max = 2.0  (variable; ratio 5.0×)
proxy_geometry_class = 'single',  tempo = 'low'   → amplitude_min = 0.3,  amplitude_max = 2.5  (spiky; ratio 8.3×)
proxy_geometry_class = 'multi-hit'                → amplitude_min = 0.6,  amplitude_max = 1.0  (flat; many small hits)
proxy_geometry_class = 'scatter'                  → amplitude_min = 0.5,  amplitude_max = 1.5  (variable; spread shots vary)
```

These are ARPG-canonical priors (not engine-calibrated yet). Primary signal is the (geometry × tempo) cross:

- **High-tempo / single-target weapons (daggers, rapid-strike):** flat variance by construction (many same-sized hits). Ratio ≤ 2×.
- **Low-tempo / single-target weapons (heavy chargers, crossbows, thrown weapons):** spiky by construction (one big hit or miss). Ratio > 4.5×.
- **AoE / cleave weapons:** variable (area coverage introduces roll-spread). Ratio 2-5×.
- **Multi-hit weapons:** flat despite multi-hit (each hit small, consistent). Ratio ≤ 1.5×.

**Tier-S special calibration:** Tier-S named-bearer rows (e.g., Gáe Bolg, Gandiva, Mjölnir) warrant specific amplitude profiles per lore-canonical behavior. Dispatch § 4.2 already flags these for a gandalf curation pass. The minimum requirement from Stage 4 is that the amplitude min/max is set plausibly (Gáe Bolg = thrown spear with curse-causality → single/ranged/low-tempo → spiky; Gandiva = divine bow → ranged/high/flat → flat). These will be reviewed at the gandalf Tier-S pass.

**Attribute-class modulation of amplitude (Option β consideration):**

For INT/WIS-typed rows, amplitude values should be slightly upward-biased vs STR/DEX equivalents at the same geometry/tempo bin. This reflects that caster weapons (staves, orbs, focuses) deliver amplified skill damage rather than physical-contact damage. Recommended modifier: `amplitude_min × 1.2, amplitude_max × 1.5` for `proxy_attribute_class IN ('INT','WIS')`. This ensures that when gamora's sim consumes caster weapon_sim_props, the damage rolls are appropriately elevated without requiring separate per-attribute lookup tables.

### schema fix: primary_stat CHECK constraint

Current constraint: `CHECK (primary_stat IN ('STR','INT','WIS'))`. DEX is absent. This is a schema bug inherited from the pre-DEX attribute system. Stage 4 population will fail on all DEX-typed rows without this fix.

**Required schema migration:**

```sql
-- Drop and recreate the constraint (SQLite does not support ALTER CONSTRAINT)
-- In SQLite, this requires recreating the table.
-- rocket must include this in the Stage 4 schema migration alongside damage_amplitude columns.
```

Alternatively: set `primary_stat = 'DEX'` as text and accept that the CHECK constraint will block it, then loosen the constraint. The MIGRATION.md must document this. This is load-bearing for Stage 4 execution — flag to rocket as a pre-population blocker.

---

## (d) Cheapest-Refuting-Test Design

### CRT-1 — Per-axis bin distribution check (post-tagging, pre-final-commit)

**Design:** Immediately after populating weapon_sim_props for all v1_scope rows (but before the acceptance commit), run a per-axis distribution query and compare to pre-tagging typed-row distribution.

**Concrete SQL:**
```sql
SELECT proxy_attribute_class, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM weapon_knowledge_entries w2
  JOIN weapon_sim_props wsp ON w2.weapon_id = wsp.weapon_id WHERE w2.v1_scope = 1)
FROM weapon_knowledge_entries w
JOIN weapon_sim_props wsp ON w.weapon_id = wsp.weapon_id
WHERE w.v1_scope = 1
GROUP BY proxy_attribute_class;
```

**Pass threshold:**
- No single attribute bin exceeds 65% of populated rows (currently DEX = 49% of typed; ceiling set at 65% to allow for NULL-typed rows tagging STR-heavy as expected from european-historical NULL pool)
- INT + WIS combined share ≥ 12% (pre-tagging = 15.4% of typed; expected to dilute slightly when NULL-typed historical pool is added)
- If INT + WIS combined < 10%, FAIL — methodology is under-representing caster substrate

**Per-range distribution check:**
- melee% within [35%, 55%] (pre-tagging = 43.4%)
- mid% within [15%, 30%] (pre-tagging = 21.4%)
- ranged% within [25%, 45%] (pre-tagging = 35.1%)

**Pass/fail:** all axes within specified bands = PASS. Any axis outside band = FAIL → inspect LLM-judge output for that axis; likely a prompt calibration issue or lookup table boundary error.

### CRT-2 — Damage amplitude ratio distribution check

**Design:** After population, verify that the amplitude ratio distribution maps to Axis 3B bins in proportions consistent with the v1 cell-targeting intent (Sketch A: ~37 forms; spiky forms are ~30% of cells, flat ~35%, variable ~35%).

**Concrete check:**
```sql
SELECT 
  CASE 
    WHEN damage_amplitude_max / damage_amplitude_min < 1.9 THEN 'flat'
    WHEN damage_amplitude_max / damage_amplitude_min < 4.5 THEN 'variable'
    ELSE 'spiky'
  END as amplitude_bin,
  COUNT(*) as n
FROM weapon_sim_props
WHERE weapon_id IN (SELECT weapon_id FROM weapon_knowledge_entries WHERE v1_scope = 1)
  AND damage_amplitude_min > 0;
GROUP BY 1;
```

**Pass threshold:** no single amplitude_bin exceeds 60% of rows. If `flat` exceeds 60%, the lookup table is defaulting too many weapons to flat (likely compound-suffix STR weapons all tagging as `cleave/medium` which has ratio 2.0× — technically variable). If `spiky` exceeds 60%, the LLM-judge is over-assigning spiky to ambiguous mythological weapons.

### CRT-3 — Round-trip schema integrity check (pre-gamora consumption)

**Design:** Before gamora sim-viability pass, verify that all 3 new schema columns are non-NULL on at least one complete row.

```sql
SELECT weapon_id, damage_amplitude_min, damage_amplitude_max, primary_stat
FROM weapon_sim_props
WHERE weapon_id = (SELECT weapon_id FROM weapon_knowledge_entries WHERE v1_scope = 1 LIMIT 1);
```

Expected: all three columns non-NULL, primary_stat value in ('STR','INT','WIS','DEX'). If this query returns NULL on any column, population script has a silent failure mode.

### Ambiguous-case re-review threshold

If LLM-judge returns confidence < 0.60 on more than 20% of Pass 3 rows (i.e., > 220 of ~1,105 rows), this triggers a methodology revision review. At that threshold, rocket should sample 50 of the low-confidence rows and determine whether the prompt can be improved (e.g., injecting source-library context, or adding description_text for royal_armouries rows). If the low-confidence rate is driven by the odin-army-tradoc modern-military rows, those should be pre-screened out before the LLM pass (see § (f)).

---

## (e) Resource-Bounds Projection

### Row-count estimate

| Pass | Rows | LLM calls | Notes |
|---|---:|---:|---|
| Pass 1 — heuristic from proxy + length | 1,890 | 0 | Per-bin lookup table; deterministic |
| Pass 2 — structured-property weapon_type lookup | 47 | 0 | Lookup table on weapon_type key |
| Pass 2b — odin-army-tradoc pre-screen exclusion | 168 | 0 | Flag as military_modern_vehicle; apply default or skip |
| Pass 3 — LLM-judge from canonical_name | ~937 | ~937 | Remaining NULL-typed after pre-screen |
| **Total v1_scope rows** | **3,042** | **~937** | |
| Tier-S/A gandalf curation pass | ~15-30 | ~15-30 | High-value mythological/named-bearer spot-check |
| **Total LLM calls** | | **~950-970** | |

**Note:** The 168 odin-army-tradoc NULL-typed rows (UAVs, armored vehicles, ships) are military_modern register. These should receive a default tag of `primary_stat = 'STR', range_class = 'ranged', tempo = 'low', geometry = 'single'` with `sim_viable = 0` and a viability note `'military_modern_vehicle — out of genre scope for v1'`. This avoids wasting LLM calls on content that will be excluded from Phase 2 form-generation via the genre filter (`genre IN ('fantasy', 'mythological', 'historical')`). The odin-army-tradoc register is `military_modern`; these rows are in v1_scope due to tier-A inclusion at Sub-phase A, not because they are fantasy-genre viable.

### LLM call cost projection

At approximately $0.001 per LLM call (claude-sonnet-4-6 short-prompt inference, ~200 tokens input + ~50 tokens output per row):
- ~950 calls × $0.001 = **~$0.95 estimated LLM cost**

Wall-time estimate: ~950 calls × 1.5 sec/call (with 1 req/2 sec rate limit) = ~23 minutes for Pass 3.

### DB write projection

- 3,042 rows × per-row INSERT or UPDATE into `weapon_sim_props`
- At ~1 ms per write: ~3 seconds for all DB writes
- Schema migration (ALTER TABLE × 2 for damage_amplitude columns + primary_stat CHECK fix): < 1 second

### Total elapsed time estimate

- Pass 1 (heuristic): < 1 minute (in-process Python)
- Pass 2 (lookup): < 10 seconds
- Pass 3 (LLM): ~23 minutes foreground OR ~23 minutes background (per Discipline #19 — recommended background)
- DB writes: ~3 seconds
- Gandalf Tier-S curation: separate async pass; ~15-30 min human review
- **Total automated execution time: ~25 minutes**

This is well within the Wave 7 dispatch envelope (Discipline #1.1 pre-fire resource-bounds per dispatch § 8: `~3,200 rows × per-row tagging compute ~1 sec = ~1 hr foreground OR background` — actual estimate is ~25 min, significantly under the 1-hr ceiling).

### Pre-population DB backup

Per dispatch § 5.5: backup at `cycle-10-stage-4-2026-05-25/backups/telemetry.db.pre-stage-4` before any writes. Backup size should be approximately the current telemetry.db size. Gitignore the backup per convention.

---

## (f) NULL-Typed Row Treatment Recommendation (Per Finding F-4)

### Population breakdown of 1,152 NULL-typed rows

From empirical DB queries:

| Source | Count | Has structured_properties | Has weapon_type key | Has length | Recommendation |
|---|---:|---:|---:|---:|---|
| royal_armouries | 647 | ~0% | 0 | 0% | Pass 3 LLM-judge on canonical_name |
| met-museum | 193 | 193 (100%) | ~0% | 61 | Pass 3 LLM-judge; length refines range |
| odin-army-tradoc | 168 | 168 (100%) | 0 | 102 | Pre-screen exclusion; default tag + sim_viable=0 |
| wikipedia | 85 | ~partial | ~0% | 5 | Pass 3 LLM-judge on canonical_name + any available text |
| wikidata | 46 | 46 (100%) | 47 total across wikidata/wikipedia | varies | Pass 2 for weapon_type-keyed; Pass 3 for remainder |
| Other | < 15 | varies | 0 | 0 | Pass 3 LLM-judge |

**Total Pass 3 rows: ~1,105 (after 47 Pass 2 extraction and 168 odin-army-tradoc pre-screen).**

### LLM-judge prompt design for Pass 3

The prompt should be concise and structured. Recommended format:

```
Given a weapon entry with the following attributes:
- canonical_name: {canonical_name}
- cultural_lineage: {cultural_lineage_canonical}
- register: {register_canonical}
- structured_properties: {structured_properties | 'none'}
- extracted_length_cm: {extracted_length_value | 'unknown'}

Classify the weapon into these bins:
- range_class: melee | mid | ranged
- geometry_class: single | cleave | AoE | multi-hit | scatter | cone
- tempo_class: low | medium | high
- attribute_class: STR | INT | WIS | DEX

Respond with JSON only: {"range":"...", "geometry":"...", "tempo":"...", "attribute":"...", "confidence":0.0-1.0}

Rules:
- If the weapon is a projectile launcher (bow, crossbow, gun, sling), range = ranged
- If the weapon is a polearm, spear, or reach weapon > 2 meters, range = mid
- If the weapon is a sword, axe, dagger, mace, fist weapon, shield, or staff < 1.5m, range = melee
- If the weapon is magical/ritual (wand, orb, tome, staff used for casting), attribute = INT or WIS
- If the weapon is for a warrior/knight archetype, attribute = STR
- If the weapon is for a rogue/archer/finesse archetype, attribute = DEX
- confidence = 0.9 if canonical_name unambiguously identifies the weapon type
- confidence = 0.6 if deduction from name/cultural_lineage only
- confidence = 0.4 if significant ambiguity
```

**Key calibration note:** the `attribute_class` assignment via LLM-judge carries higher variance than range/geometry/tempo. For the mythological-NULL rescue subset specifically (named weapons like Gáe Bulg, Gungnir, Gandiva, Mjölnir, Excalibur), the LLM-judge should have high confidence because these weapons have well-known ARPG-genre analogues. The risk is with royal_armouries items like "Lockplates" or "Detached upper jaws" — these are weapon COMPONENTS, not complete weapons, and the LLM-judge will likely return low-confidence (0.4) on these. Those should be flagged separately for human triage per Signal 2 from § (b).

### Mythological-NULL rescue subset (composition policy § 1.4)

The ~30 mythological-register NULL-typed rows are a SUBSET of the 1,152 NULL-typed total. From empirical query, all 30 mythological-register NULL-typed rows are in the wikidata + wikipedia sources and have `structured_properties` with `weapon_type` keys (Gungnir = spear, Gandiva = bow, Excalibur = sword, etc.).

Recommendation: handle the mythological-NULL rescue as a **targeted Pass 2 extension** rather than routing through general Pass 3. The weapon_type keys in their structured_properties are sufficient for heuristic classification. For the few that have ambiguous `weapon_type` values (`"mythological weapon"`, `"Norse mythical object"`, `"religious concept"`), apply LLM-judge with cultural-tradition context to resolve.

Expected outcomes for the ~30 mythological-rescue rows:
- Gungnir: ranged/single/low/STR (thrown spear, heavy) → actually per lore, INT/WIS is arguable (divine weapon). Recommend STR default for non-divine weapon; gandalf spot-check will correct high-profile items.
- Gandiva: ranged/single-multi/medium/DEX (divine bow, rapid-fire in lore)
- Mjölnir: melee/single-AoE/low/STR (thrown hammer with return; treat as melee/AoE)
- Excalibur: melee/single/medium/STR (sword; Tier-S gandalf curation will refine)
- Gáe Bulg: ranged/single/low/STR (thrown spear) — dispatch § 4.2 explicitly calls out canon-respecting for this item
- Sudarshana Chakra: ranged/scatter/high/DEX (spinning chakram; multiple-return hits)
- Aegis/shields: secondary items → aoe_radius populated but range = melee/mid; primary_stat varies

Post-rescue, update `v1_scope_composition_trace` from `'stage_4_mythological_rescue_pending'` to `'stage_4_mythological_rescue_complete'` per dispatch § 3.3.

### Semantic-layer rep-audit (Discipline #25) at mythological-NULL rescue boundary

Before classifying the ~30 mythological-register NULL-typed rows, apply the semantic-layer rep-audit check per dispatch § 4.6:
- Is the row actually mythological-register content, or is it Mode B/C contamination?
- Check: `canonical_name LIKE '%fictional%'` or `weapon_type LIKE '%fictional%'` (e.g., "Mjolnir" wikidata row has `weapon_type = 'fictional hammer'` and inception date 1962 — this is the Marvel Comics version, not the Norse mythological Mjölnir). These Mode-C rows should be separated from the primary mythological cluster.
- Recommendation: partition the ~30 rows into (a) historically-mythological (Gungnir the Norse spear, Gáe Bulg the Celtic spear, Gandiva the Vedic bow) vs (b) fictionally-mythological (Mjolnir 1962 = Marvel Comics). The fictional variants can receive the same mechanical tag but should have `v1_scope_composition_trace` note indicating the rep-audit finding. They are legitimate v1_scope entries (fantsy register fits); the note is for gandalf's Phase 5 cohesion-judge awareness.

---

## Knowledge Gaps Not Resolved

1. **Engine tile ↔ physical unit calibration:** the recommended `range_max_tiles = extracted_length_cm × 0.028` scaling factor is a prior derived from the BC-axes lock tile definitions and empirical weapon length data. It has not been empirically calibrated against the sim engine. Per Discipline #17, this requires first-deployment telemetry to validate. Gamora's sim-viability pass should include a sanity-check against 2-3 manually-confirmed range values.

2. **Damage amplitude absolute values:** the min/max scalars above are normalized (amplitude_min = 0.3-0.8, amplitude_max = 1.0-2.5). These are RELATIVE values within a weapon's range. The absolute damage magnitude (in game damage units) depends on the engine's damage formula, which is not specified in the BC-axes lock. Rocket must confirm the engine's damage formula entry point before translating these relative values to engine-unit damage values. If the engine expects damage_amplitude in [0,100] units, scale accordingly.

3. **hits_per_attack for multi-hit weapons:** the recommended value of 3 for `geometry_class = 'multi-hit'` is a prior. The engine's actual multi-hit implementation (how many sub-hits does a "multi-hit" weapon produce?) may differ. Gamora's sim-viability smoke-test should verify this field is correctly consumed.

4. **royal_armouries component-parts problem:** 647 of 1,152 NULL-typed rows are royal_armouries items, many of which appear to be weapon components (lockplates, detached jaws, electrotype replicas, equestrian mannequins) rather than weapon systems. The LLM-judge will return low-confidence on these. A pre-pass filtering `canonical_name` against known component-part patterns before invoking LLM-judge would reduce waste. Specific patterns to filter: "Lockplate", "Detached", "Electrotype", "Mannequin", "Case", "Inner barrel", "Fuse Cutter", "Holster". These may warrant sim_viable = 0 by default. Rocket should decide whether to include or exclude these from the population pass; they are in v1_scope because they passed the D1b secondary-item classification, but their weapon_sim_props values will be meaningless if they are components.

---

## Source List

All findings are grounded in direct DB queries and canonical project documents. No external web sources consulted — this is a baseline-empirical methodology consult per Discipline #18.2.

1. `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — BC Axis definitions, bin thresholds, tile-unit range definitions, CV thresholds for Axis 3B
2. `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — § 1.4 mythological-NULL rescue, § 3 Option α/β/C matching policies
3. `canonical/story/v1-bc-target-intent-2026-05-24.md` — Sketch A cell roster, geometry distribution intent per cell type
4. `canonical/story/attribute-system-2026-05-24.md` — 4-attribute system (STR/INT/WIS/DEX); element-attribute coupling
5. `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-25/v1-scope-distribution-report.md` — Phase 3 empirical findings; Finding F-4 (1,152 NULL-typed rows); per-axis distributions
6. `agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-24/confidence-distribution-v1-1.md` — Stage 1 proxy fingerprint typed-row distribution; per-bin counts
7. `agentic_orchestration/elrond/research/cycle-10-stage-1-5-2026-05-24/per-source-schema-mapping.md` — extracted_length/weight per-source coverage; source format details
8. `agentic_orchestration/elrond/research/cycle-10-stage-1-5-2026-05-24/per-source-coverage.md` — per-source extraction coverage rates
9. Live DB queries on `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (2026-05-25):
   - Length/weight distribution by range_class for v1_scope typed rows (melee: n=70, mean=39.8cm; mid: n=28, mean=237cm; ranged: n=36)
   - NULL-typed row source distribution (royal_armouries 647, met-museum 193, odin-army-tradoc 168, ...)
   - structured_properties coverage for NULL-typed rows (97% have properties; 47 have weapon_type key)
   - Mythological-register NULL-typed rows sample (Gungnir, Gandiva, Excalibur, Gáe Bulg, ...)
   - weapon_sim_props schema (via `.schema weapon_sim_props`); current primary_stat CHECK constraint missing DEX
   - v1_scope population count: 3,042 total; 1,890 typed; 1,152 untyped

---

**Author:** legolas (Mode A methodology consult)
**Date:** 2026-05-25
**Authority:** `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md` § 4.1
**Discipline #18.2 compliance:** baseline-informed (Stages 1/1.5/2/2.5/3 consumed before consult fired)
**Output path:** `agentic_orchestration/legolas/research/cycle-10-stage-4-methodology-consult-2026-05-25/methodology-recommendation.md`
