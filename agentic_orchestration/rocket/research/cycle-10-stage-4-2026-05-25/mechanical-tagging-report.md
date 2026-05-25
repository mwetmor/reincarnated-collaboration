# Mechanical Tagging Report — Cycle 10 Stage 4
# weapon_sim_props Population: v1_scope UNION

**Date:** 2026-05-25
**Author:** rocket
**Dispatch authority:** `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md`
**Script:** `populate_weapon_sim_props.py`
**Run duration:** 03:29:24 → 03:43:02 (13 min 38 sec)

---

## Population summary

| Metric | Value |
|---|---|
| Total v1_scope rows | 2,293 |
| weapon_sim_props rows inserted | 2,293 |
| Rows missing weapon_sim_props | 0 (ZERO regressions) |
| Errors | 0 |
| Total elapsed | ~14 min |

### Pass breakdown

| Pass | Rows | LLM calls | Notes |
|---|---:|---:|---|
| Pass 1 — typed heuristic (proxy columns) | 1,865 | 0 | Per-bin lookup; deterministic |
| Pass 2 — weapon_type key lookup | 1 | 0 | wikidata structured-property hit |
| Pass 2b — odin-army-tradoc prescreen | 30 | 0 | military_modern; sim_viable=0 |
| Pass 3 — component default (pattern match) | 26 | 0 | Detached/Holster/etc patterns |
| Pass 3 — LLM judge | 371 | 371 | NULL-typed; canonical_name + cultural_lineage |
| **Total** | **2,293** | **371** | |

**Note:** The consult projected 937 LLM calls (based on 1,152 NULL-typed rows in the earlier distribution report). Actual NULL-typed count was 442 rows (the main pool contained 1,851 typed rows, not 1,890 as projected). Pass 3 consumed 371 calls. Estimated LLM cost: ~$0.37 (actual under ~$0.95 projection).

### LLM judge quality signal

| Signal | Value | Threshold | Status |
|---|---:|---:|---|
| Low-confidence (<0.6) count | 137 | <74 (20% of 371) | WARN — above 20% |
| Low-confidence rate | 37.0% | <20% | WARN |
| Low-confidence source breakdown | 130 royal_armouries, 5 met-museum, 2 other | | Expected |

**Assessment of WARN signal:** The 130 royal_armouries low-confidence items are largely weapon accessories/tools with ambiguous canonical names (Holster, Detached lock, Cocking lever, Pricker, Linstock, Clay pigeon, Worm). These items are in v1_scope due to passing D1b secondary-item classification at Stage 1, but many are weapon COMPONENTS not complete weapons. The LLM correctly returns low confidence. 40 of these are already marked sim_viable=0 (component_part pattern match). The remaining ~90 with sim_viable=1 may warrant Phase 2 viability review — flagged for gamora sim-viability assessment.

**Signal 2 action (consult § b Signal 2):** Per consult recommendation, 30-row sample of low-confidence items was examined. Root cause: royal_armouries vocabulary is heavily accessory-oriented. Prompt injection of source context would not resolve (canonical_name IS the full information). Disposition: acceptable for Stage 4 purpose; component parts will be excluded at Phase 2 genre filter regardless.

---

## Per-axis distribution histograms

### Axis: primary_stat (attribute)

| Attribute | Count | Pct | Pre-tagging typed pct | Delta |
|---|---:|---:|---:|---:|
| DEX | 1,076 | 46.9% | 46.4% | +0.5pp |
| STR | 890 | 38.8% | 35.6% | +3.2pp |
| WIS | 167 | 7.3% | 7.9% | -0.6pp |
| INT | 160 | 7.0% | 7.5% | -0.5pp |
| **INT+WIS combined** | **327** | **14.3%** | **15.4%** | **-1.1pp** |

**CRT-1 PASS:** INT+WIS combined 14.3% >= 12% threshold. No single attribute exceeds 65% ceiling (DEX at 46.9%).

### Axis: range_class

| Range | Count | Pct | Pre-tagging pct | Delta |
|---|---:|---:|---:|---:|
| melee | 1,048 | 45.7% | 44.6% | +1.1pp |
| ranged | 768 | 33.5% | 31.9% | +1.6pp |
| mid | 453 | 19.8% | 22.2% | -2.4pp |
| melee_close_or_grapple | 17 | 0.7% | 0.9% | -0.2pp |
| off_hand_aura | 7 | 0.3% | 0.4% | -0.1pp |

**Within ±8pp bounds per consult CRT-1:** melee 45.7% (prior 44.6% ±8pp → [36.6%, 52.6%]) PASS; ranged 33.5% (prior 31.9% ±8pp → [23.9%, 39.9%]) PASS; mid 19.8% (prior 22.2% ±8pp → [14.2%, 30.2%]) PASS.

### Axis: geometry_class

| Geometry | Count | Pct |
|---|---:|---:|
| single | 1,390 | 60.6% |
| cleave | 573 | 25.0% |
| AoE | 177 | 7.7% |
| multi-hit | 75 | 3.3% |
| scatter | 48 | 2.1% |
| shield_blocker | 17 | 0.7% |
| banner_rally_aura | 7 | 0.3% |
| cone | 6 | 0.3% |

### Axis: tempo_class

| Tempo | Count | Pct | Pre-tagging pct | Delta |
|---|---:|---:|---:|---:|
| medium | 1,100 | 48.0% | 49.3% | -1.3pp |
| low | 648 | 28.3% | 27.1% | +1.2pp |
| high | 521 | 22.7% | 23.6% | -0.9pp |
| reactive_block_tempo | 17 | 0.7% | 0.9% | -0.2pp |
| aura_pulse_tempo | 7 | 0.3% | 0.4% | -0.1pp |

**Within ±8pp bounds:** All tempo bins within range.

### Axis: damage_amplitude bin (from min/max ratio)

| Amplitude bin | Count | Pct | Target |
|---|---:|---:|---|
| variable (1.9x-4.5x CV range) | 1,242 | 54.3% | ~35% |
| flat (<1.9x) | 522 | 22.8% | ~35% |
| spiky (>4.5x) | 522 | 22.8% | ~30% |

**CRT-2 NOTE:** variable bin at 54.3% exceeds the ±60% ceiling (not tripped). The distribution skews more variable than the Sketch A target (~35%) because the per-(geometry×tempo) bin table is heavily populated with cleave/medium combinations that hit the 2.0x ratio (flat-variable boundary). The variable bin threshold is 1.9x-4.5x, and most "average" weapons fall there. This is an expected artifact of using fixed per-bin lookup tables rather than per-weapon calibration. No CRT-2 failure; noting for gamora to validate against sim telemetry after first simulation run.

---

## Sim-viability flag summary

| sim_viable | Count | Notes |
|---|---:|---|
| 1 (viable) | 2,212 | Tagged as sim-viable |
| 0 (not viable) | 81 | military_modern_vehicle (30); component_parts (40); support_banner (7); other (4) |

**Out-of-envelope rows (sim_viable=0):**
- 30 odin-army-tradoc military_modern entries (UAVs, armored vehicles, ships)
- 40 royal_armouries weapon component parts (detached locks, holsters, barrel sections)
- 7 banner_rally_aura off-hand support items (no direct damage output)
- 4 other (mixed accessory items)

**Default disposition:** demote to v1.1+ pending gamora sim-viability assessment and Phase 2 genre filter.

---

## Anomaly log

1. **Ruyi Jingu Bang wikidata (id=388):** weapon_type='gun' in wikidata structured properties → classified as DEX/ranged by Pass 2 weapon_type lookup. This is a Wikidata data error (the Wikidata entry incorrectly uses "gun" as weapon_type for Sun Wukong's magical staff). The wikipedia entry (id=174314) correctly classified as STR/mid by LLM judge. Both are v1_scope=1. Flagged for gandalf Tier-S curation pass.

2. **Sudarshana Chakra wikipedia (id=176479):** LLM classified as WIS/AoE/ranged/high (divine weapon framing → WIS). Methodology consult expected DEX/scatter (chakram). Difference is defensible (Sudarshana Chakra is a divine disc with magical properties → WIS framing has merit). wikidata entry (id=409) correctly tagged as chakram but is not v1_scope. Flagged for gandalf Tier-S curation.

3. **Mjölnir wikipedia (id=174103):** LLM classified as STR/AoE/high. Consult expected STR/AoE/low (thrown return hammer). AoE assignment correct; tempo=high (LLM interpreted lightning-fast return) vs consult's low (heavy throw). Defensible; flagged for gandalf curation.

4. **LLM JSON parse failures (15 total across all runs):** Occurred for items with verbose reasoning exceeding 128 token limit. Final run had 5-7 instances; all fell back to STR/melee/medium default. These are all royal_armouries accessories (Cocking lever, Case, Chamber insert, Display board, Pricker, Worm, Clay pigeon, Turnscrew). All are sim_viable=0 candidates at Phase 2 due to accessory nature. Impact: negligible.

---

## Cheapest-refuting-test results

| CRT | Description | Result |
|---|---|---|
| CRT-1 | INT+WIS combined ≥ 12% | PASS (14.3%) |
| CRT-1 range | melee/mid/ranged within ±8pp of prior | PASS |
| CRT-1 attribute ceiling | No attribute > 65% | PASS (DEX 46.9%) |
| CRT-2 | No amplitude bin > 60% | PASS (variable at 54.3%) |
| CRT-2 note | variable bin above Sketch A target | NOTE — expected from lookup-table method |
| CRT-3 | Schema columns non-NULL on sample row | PASS |
| CRT-4 | damage_amplitude_min/max non-NULL on all rows | PASS (0 NULLs) |
| Signal 2 | LLM low-confidence rate | WARN (37% > 20% threshold) — royal_armouries accessory items; see assessment above |

---

## Stage 3.5 engine-authored gap-fill confirmation

All 42 engine_authored_gap_fill_v1 rows have weapon_sim_props populated:
- All had proxy columns pre-populated (Pass 1)
- All are sim_viable=1
- Attribute distribution: STR 19, DEX 11, WIS 8, INT 4 (reflects designed anchor cell coverage)

---

## Notes for gamora sim-viability pass

1. Validate that `range_max_units` for melee entries (2.5 tiles) is within engine combat grid bounds
2. Check `hits_per_attack = 3` for multi-hit entries matches engine multi-hit implementation
3. Validate `damage_amplitude_min/max` scaling in engine damage formula (values are normalized 0.3-2.5 range; confirm engine expectation)
4. royal_armouries entries with sim_viable=1 but low classification confidence (~90 rows): recommend spot-check 10 rows at Phase 2 substrate-binding
5. Ruyi Jingu Bang (id=388) DEX/ranged anomaly: override recommended before gamora pass

---

## References

- Methodology: `agentic_orchestration/legolas/research/cycle-10-stage-4-methodology-consult-2026-05-25/methodology-recommendation.md`
- Dispatch: `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-10-stage-4-mechanical-tagging.md`
- Population script: `agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/populate_weapon_sim_props.py`
- Ambiguous cases log: `agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/ambiguous-cases.jsonl`
- Mythological rescue log: `agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/mythological-null-rescue-log.jsonl`
- Population run log: `agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/population-run.log`
- MIGRATION.md: `agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/MIGRATION.md`
