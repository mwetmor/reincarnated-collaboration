# Methodology — Cycle 13 Wave 2 Statistical Co-Occurrence Priors Extraction

**Authored:** 2026-05-27
**Author:** elrond
**Authority basis:** Matt 2026-05-27 + jack-ryan Wave 2 Gate-1 I2 INFO (commit `f9ead71`) + AI-tell line discipline D7 + closeout § 2.5
**Dispatch:** `agentic_orchestration/dispatches/2026-05-27-elrond-cycle-13-wave-2-statistical-co-occurrence-priors.md`
**Output artifact:** `reincarnated-engine/data/synergy_priors/v1_co_occurrence_priors.json`
**Extraction script:** `agentic_orchestration/research/scripts/extract_synergy_co_occurrence_priors_2026_05_27.py`
**Consumer:** rocket Wave 2 W2.4 compositional synergy scan implementation

---

## 1. Substrate corpus scope

**Decision:** the mechanic substrate corpus for the synergy priors is the **engine telemetry abilities + classes** at `reincarnated-engine/data/telemetry.db`, NOT the 2,293-item v1_scope weapon catalogue at `agentic_orchestration/research/curated/catalogue.db`.

**Rationale:** the weapon catalogue is a VISUAL-and-FORM-FACTOR corpus (style register, decomposition signal, dimensionality, palette, linework, animation density) — it carries no ARPG-mechanic semantics. T4-strategy / kit-mechanic / element-pair / scaling-axis / chain-position co-occurrence cannot be extracted from style metadata; only from kit-level mechanical fingerprints. The dispatch language "2,293-item v1_scope per Cycle 10" anchored a substrate-scale expectation; my seam-owner call (per Discipline #18 + open-question 1 in the dispatch) is that this corpus is mis-fit for ARPG-mechanic priors. The telemetry corpus is the load-bearing substrate.

**Substrate-corpus empirical scope:**

| Metric | Value | Verification |
|---|---|---|
| Seasons | 94 | `SELECT COUNT(*) FROM seasons` |
| Class-rows | 631 | `SELECT COUNT(*) FROM classes` |
| Class-abilities | 7,066 | `SELECT COUNT(*) FROM abilities WHERE owner_type='class'` |
| Unique (class_id, season_id) kit-instances with mechanics | 692 | per-kit aggregation in Python |
| All abilities (class + monster + trial) | 17,533 | substrate breadth context |

Lookback window: all-time (season_000001 through season_001NNN). No per-season weighting applied; equal-weight per kit-instance to maximize sample size and surface stable co-occurrence patterns.

## 2. Methodology per dimension

### Dimension 1 — T4-strategy-pair co-occurrence

**Challenge:** T4 strategies (per doc 43 § 2.2 6-strategy registry) are a NEW algorithm concept introduced in Wave 2; no historical T4 metadata exists in the substrate. Strategies must be INFERRED from per-kit signatures.

**Signature mapping:**

| Strategy | Signature heuristic | Substrate basis |
|---|---|---|
| RESOURCE_CONVERSION | `energy_type` in {`combo`, `focus`, `rage`, `stamina-as-resource`} | non-mana energy types historically signal resource-system alteration (rage-as-fury, combo-as-points) |
| DEFENSIVE_CONVERSION | `archetype` in {`tank`, `support_healer`} OR `canonical_element`=`water` | tank/support archetypes + water-as-defensive-element are historical defensive-conversion vehicles |
| GEOMETRY_COLLAPSE | kit has any geometry in {`multi_projectile`, `vortex_pull`, `chain_lightning`, `ricochet_bounce`, `ground_slam`, `leap_strike`, `whirlwind`, `beam_channel`, `fork`, `ground_targeted_circle`} | non-baseline geometries beyond `melee_strike`/`single_target` signal chain-skill geometry alteration |
| MULTIPLIER_STRATEGY | kit has any effect in {`buff_damage`, `lifesteal`, `bleed`} | damage multiplier kits historically carry these effect signatures |
| ELEMENT_CONVERSION | kit has ≥2 elements AND majority element share <80% | multi-element kits with no dominant element historically signal element-conversion chains |
| DUAL_ELEMENT_ADDITION | kit has minority element in 10-40% share range | minority-element-share aligns with doc 43 § 3.4 band anchors (Low 15-25 / Medium 25-40 / High 40-55) |

**Sample size:** 489 of 692 kits (70.7%) exhibit ≥2 inferred strategies. 1,837 strategy-pair instances total.

**Caveat:** signatures are PROXY surrogates. The inferred strategies do not assert that historical kits "had T4 strategies" — they assert that the kit's mechanical fingerprint shows the same SIGNATURE that those T4 strategies would produce. Rocket consumes these priors as historical likelihood that the pair WOULD CO-OCCUR if generated; not as direct historical evidence of T4 instances.

### Dimension 2 — Kit-mechanic co-occurrence

Straightforward: every `effects[].name` per ability is collected; per-kit unique set is intersected with `KIT_MECHANIC_TAGS` allowlist (18 tags: damage / burn / chill / bleed / lifesteal / knockback / root / silence / shock / shield / buff_defense / buff_dodge / heal / heal_over_time / buff_damage / buff_mana_regen / consecrate / drain). Pair-counts via `itertools.combinations(unique_tags, 2)`.

**Sample size:** 692 kits; 128 unique mechanic pairs surface. Top pair: `damage|shield` at 642 instances (4.75% of all pairs).

**Cross-validation:** total effect-name distribution sanity-checked vs the full `abilities.effects` JSON enumeration. Raw distribution `damage: 11,213`, `knockback: 2,263`, `chill: 2,128`, `shield: 1,686`, `buff_damage: 1,639`, `root: 1,235`, `burn: 1,132`. Consistent with substrate's known fire/water/earth/wind primacy + class control archetypes.

### Dimension 3 — Element-pair co-occurrence

Per (class_id, season_id), all distinct elements across abilities are collected. Pair-counts via `combinations(elements, 2)`.

**Sample size:** 436 of 692 kits (63.0%) are multi-element. SQL cross-check: `SELECT COUNT(*) FROM (SELECT owner_id, season_id, COUNT(DISTINCT canonical_element) AS ne FROM abilities WHERE owner_type='class' GROUP BY owner_id, season_id HAVING ne >= 2)` returns 436 — matches Python count exactly.

**Top pairs:**

| Rank | Pair | Raw | Normalized |
|---|---|---|---|
| 1 | water\|wind | 135 | 0.1753 |
| 2 | fire\|wind | 131 | 0.1701 |
| 3 | earth\|fire | 130 | 0.1688 |
| 4 | earth\|water | 115 | 0.1494 |
| 5 | fire\|water | 78 | 0.1013 |
| 6 | earth\|wind | 76 | 0.0987 |

The four primary elements (earth / fire / water / wind) co-occur fairly uniformly. Physical pairs lag (4 pairs total < 12% combined). Lightning + holy + shadow have negligible representation (lightning|water = 2; lightning|wind = 2).

**DUAL_ELEMENT_ADDITION sub-metadata:** primary→minority element transitions + share-band counts (low_15_25 / medium_25_40 / high_40_55 / below_low / above_high) per primary element are extracted. Rocket can consume `dual_addition_metadata.primary_to_minority_counts` for secondary-element selection per doc 43 § 3.4 algorithm.

### Dimension 4 — Scaling-axis co-occurrence

**Methodology:** each effect-name maps to a scaling axis (e.g., `damage` → `damage_magnitude`; `burn` → `dot_tick_damage`; `lifesteal` → `lifesteal_pct`). Each axis has a bucket assignment per ARPG genre convention (PoE / D4 / LE precedent). Pair-counts via `combinations(axes, 2)` per kit.

**Classification per SC-4 expansion Topic 2:**
- `multiplicative_across_buckets`: pair's buckets differ → high-value, high-trap-risk synergy
- `additive_within_bucket`: pair's buckets match → D4/GD same-bucket trap form

**Result:** 36 unique pairs, 10,660 total instances. **ALL 10,660 are multiplicative_across_buckets; ZERO additive_within_bucket.**

**Finding (substrate-led):** the engine's current ability schema produces ZERO same-bucket axis pairings because each effect maps to a unique scaling axis. This is itself a load-bearing observation — the engine substrate naturally AVOIDS the same-bucket trap. The Pass 2 preserve check for scaling-interaction degeneration (per doc 43 § 5.3) cannot calibrate its trap detector against substrate examples because no historical traps exist. **Recommendation routed to gandalf via knight-rider:** consider whether substrate needs synthetic-trap injection at rocket W2.4 test coverage to validate the trap-detection path.

### Dimension 5 — Chain-position co-occurrence

**Methodology:** chain position (T4 capstone vs T1-T3 anchor) is INFERRED (no T4 metadata exists in substrate). Thresholds calibrated to substrate cooldown distribution (empirically: 0.1-19.9s; mean 8.5s; std-dev derived). The dispatch substrate has NO ability with cooldown ≥ 20s; calibration uses substrate top-decile + role-filter + multi-effect-filter:

- **T4 capstone candidate:** `cooldown_seconds >= 15` (top ~9% of pool) AND `len(effects) >= 2` AND `role != 'primary_attack'`
- **T1-T3 anchor:** `role IN {primary_attack, sustain, utility}` OR `cooldown_seconds < 10`

Cross-pairs (T4 mechanic × T1-T3 mechanic) within same kit are counted. Directed pair-counts: 120 unique cross-pairs across 167 kits.

**T4 capstone solo mechanic distribution (top 5):**

| Rank | Mechanic | Raw | Normalized |
|---|---|---|---|
| 1 | buff_damage | 128 | 0.3368 |
| 2 | silence | 104 | 0.2737 |
| 3 | buff_mana_regen | 59 | 0.1553 |
| 4 | damage | 51 | 0.1342 |
| 5 | knockback | 14 | 0.0368 |

**Empirical observation:** historical "T4-capstone-position" mechanics are dominated by `buff_damage` + `silence` + `buff_mana_regen` (combined 77.6%). This aligns with intuition: high-cooldown multi-effect non-primary-attack abilities tend to be utility buffs, hard CC, or resource manipulation — consistent with capstone semantics across ARPG genre.

**Caveat:** chain-position inference is more proxy-laden than dimensions 1-4. Rocket should treat D5 as the lowest-confidence prior; it surfaces "what mechanics historically anchor late-rotation high-cost slots" rather than "what mechanics historically appear at T4." The cooldown ceiling of 19.9s in the current substrate is a HARD CONSTRAINT — the substrate has no T4-tier abilities at the cooldown profile T4 design will likely demand.

## 3. Discipline composition

### Discipline #11 (empirical inspection over assumption)

Every count is computed via `collections.Counter` accumulation over `sqlite3.Row` enumeration. Cross-validation via independent SQL aggregate queries inside `post_script_empirical_assertions`. All 13 assertions PASS:

```
[PASS] substrate.season_count == 94
[PASS] substrate.class_rows == 631
[PASS] substrate.class_abilities == 7066
[PASS] d1.normalized_freq_sums_to_1.0  | sum = 1.000000
[PASS] d1.raw_total >= sample_size_kits_with_2plus | pair_sum=1837; kits=489
[PASS] d2.normalized_freq_sums_to_1.0  | sum = 0.999996
[PASS] d2.kits_with_mechanics <= total_kit_count
[PASS] d3.normalized_freq_sums_to_1.0  | sum = 1.000000
[PASS] d3.multi_element_kits_matches_sql_count | python=436 sql=436
[PASS] d4.multiplicative_plus_additive_equals_raw_total | mult=10660 add=0
[PASS] d4.normalized_freq_sums_to_1.0  | sum = 1.000002
[PASS] d5.t4_capstone_distribution_normalized_sums_to_1 | sum = 1.000002
[PASS] d5.normalized_freq_sums_to_1.0  | sum = 0.999993
```

(Normalized sums of 0.999996 / 1.000002 / 0.999993 are within rounding tolerance of 1.0 due to per-pair 6-decimal rounding.)

### Discipline #18 (methodology selection at hotspots)

Extraction is statistical/Counter-based; this is the **right tool** for the question "how often do X and Y co-occur in the substrate?" The methodology choice is documented in this note BEFORE downstream rocket W2.4 consumption per Discipline #18 sequence: legolas Mode A research (closeout § 2.5 + SC-4 expansion Topic 2 already grounded the methodology) → methodology lock here → execution → empirical assertion verification.

No bootstrapping/significance-testing applied: priors are descriptive frequencies, not inferential parameters; rocket consumes them as PROBABILITY-WEIGHTED HINTS for the synergy scan, not as parameter estimates with confidence intervals. Significance testing would be Wave 2+ scope if rocket surfaces a need for calibrated confidence per prior.

### AI-tell line D7 (statistical, NOT LLM raw-reasoning)

Zero LLM calls; zero LLM raw-reasoning. The priors compose downstream with gandalf-curated pattern library (doc 43 § 5.2 + § 5.3) + algorithmic composition per closeout § 2.5. The composition layer is rocket's W2.4 implementation, not this artifact. This artifact preserves the AI-tell line by being PURELY statistical.

### Principle 6 (round-trip)

Extraction script ends with explicit round-trip smoke:
```python
with open(OUTPUT_PATH, "r") as f:
    reloaded = json.load(f)
assert reloaded["schema_version"] == "v1.0"
assert len(reloaded["dimensions"]) == 5
```
JSON loadable + parseable. Consumer interface documented in `output.consumer_interface.rocket_w2_4`.

## 4. Open-question resolutions (from dispatch § "Open questions")

- **Substrate corpus scope:** full substrate (94 seasons × 631 classes × 7,066 abilities), not subset. Maximizes sample size for stable co-occurrence; per-season weighting NOT applied (equal weight per kit-instance).
- **Normalization choice:** BOTH normalized 0.0-1.0 frequencies AND raw counts emitted per dimension (`normalized_frequencies` + `raw_counts`). Rocket consumes whichever is needed; sample-size metadata included for confidence weighting.
- **File format:** JSON. ~95 KB output; well within rocket-consumption complexity budget; human-readable for jack-ryan Gate-2 inspection; no Parquet overhead.
- **Co-occurrence threshold:** include ALL pairs with count ≥ 1 (no minimum-occurrence threshold). Top-K filtering deferred to rocket-consumer-side per W2.4 composition algorithm needs. Sparse-pair signal (e.g., `lightning|water` at 2) is preserved for rocket's discretion; rocket can apply a min-count filter at consumption time if noise becomes a concern.

## 5. Integration pattern landed

**Pattern A** (priors land during rocket W2.0-W2.3 implementation; rocket reads priors at W2.4). This work was authored within a single session window; rocket Wave 2 is firing concurrently. The priors file is queryable + parseable NOW; rocket can integrate at W2.4 without stub interface.

## 6. Recommended follow-ups (post-Wave-2)

| # | Item | Rationale |
|---|---|---|
| 1 | Synthetic-trap injection in W2.4 test coverage | D4 surfaces ZERO same-bucket pair instances in substrate; the Pass 2 trap-detector cannot calibrate against substrate-native examples. Test coverage needs synthetic same-bucket pairs |
| 2 | Cooldown ceiling extension | D5 calibration limited by substrate ceiling of 19.9s; future T4-tier abilities will likely have cooldown ≥ 30s. After Wave 2 T4 generation produces native T4 abilities, re-extract D5 with native T4 metadata |
| 3 | Sparse-element-pair sample-size review | `lightning|water`, `lightning|wind`, `holy`, `shadow` are barely-represented. Rocket should apply a min-count filter or warn on low-sample priors |
| 4 | Per-archetype prior stratification | All priors are aggregated across all archetypes. Per-archetype priors (e.g., `tank`-only vs `rogue`-only D1 strategy pairs) may surface archetype-specific synergy patterns; deferred to gamora SC-7 calibration phase |
| 5 | Confidence intervals via bootstrap | Current priors are point estimates. If rocket synergy scoring becomes sensitive to prior magnitude, bootstrap-based confidence bands would inform threshold decisions |

## 7. Out of scope (per dispatch)

- T4 algorithm implementation (rocket seam)
- Compositional synergy scan algorithm (rocket W2.4)
- Pattern library curation (gandalf seam per doc 43)
- LLM-based reasoning for synergy detection (D7 anti-pattern)
- Substrate corpus modifications
- Schema migrations on substrate DB
- Cycle 14+ scope

---

**Signed:** elrond (data steward and archivist; catalogue DB + abstraction-analysis seam)
**For:** rocket Wave 2 W2.4 statistical co-occurrence priors consumption per AI-tell D7 + closeout § 2.5
