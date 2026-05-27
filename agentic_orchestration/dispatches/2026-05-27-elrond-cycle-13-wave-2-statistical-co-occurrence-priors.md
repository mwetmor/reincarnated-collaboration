# Dispatch — 2026-05-27 — elrond — Cycle 13 Wave 2 Statistical Co-Occurrence Priors (W2.4 Concurrent Dependency)

**From:** knight-rider
**To:** elrond
**Approved by:** Matt 2026-05-27 + jack-ryan Wave 2 Gate-1 I2 INFO (commit `f9ead71`) flagging elrond statistical co-occurrence priors as W2.4 concurrent dependency per AI-tell line D7 + closeout § 2.5 ("pattern library (gandalf-curated) + statistical co-occurrence priors (elrond) + algorithmic composition. NOT LLM raw-reasoning for core synergy detection")
**Estimated effort:** 3-6 hrs substrate analysis + co-occurrence statistical extraction
**Acceptance:** statistical co-occurrence priors structured file produced for rocket W2.4 consumption; T4-strategy-pair / kit-mechanic / element-pair / scaling-axis / chain-position co-occurrence frequencies extracted from existing substrate; rocket consumes via load-from-file integration pattern

## Context

Cycle 13 Wave 2 = T4 algorithm Phases 1-2 implementation. Sub-wave W2.4 = compositional synergy scan (Pass 1 resolve + Pass 2 preserve). Per AI-tell line discipline (D7) + closeout § 2.5 + doc 43 § 5: compositional synergy scan must NOT use LLM raw-reasoning; instead uses pattern library (gandalf-curated; in doc 43) + **statistical co-occurrence priors (elrond — THIS DISPATCH)** + algorithmic composition.

Rocket Wave 2 implementation is firing in parallel (commit forthcoming). Rocket W2.4 implementation needs elrond statistical co-occurrence priors as input. Two possible integration patterns:
- **Pattern A (preferred):** elrond priors land during rocket W2.0-W2.3 implementation; rocket reads priors at W2.4
- **Pattern B (fallback):** elrond priors land after rocket reaches W2.4; rocket implements W2.4 with stub-priors interface (load-from-file pattern) + integrates elrond's output at completion

Either pattern works; this dispatch fires in parallel with rocket Wave 2.

## Required reading before starting

1. `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` § 5 (compositional synergy scan two-pass; AI-tell line D7 + pattern library + statistical priors composition)
2. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-1-doc-43-critique.md` (Gate-1 I2 flag substantive)
3. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 2.5 (compositional synergy scan + AI-tell line discipline)
4. `agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` Topic 2 (synergy taxonomy; 5-category framework including 5th Scaling-interaction)
5. `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes operational truth — substrate analysis dimensions)
6. `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (composition policy v1; substrate context)
7. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#18 methodology + #11 empirical inspection + D7 AI-tell line)
8. `agentic_orchestration/operating-procedures/elrond.md` (your operating procedure; substrate seam authority)
9. Catalogue DB + abstraction-analysis tables (your seam): existing substrate corpus per `weapon_knowledge_entries` etc.; v1_scope = 2,293 items LOCKED per Cycle 10 close

## Math-before-code

NOT applicable — substrate analysis + statistical extraction; no engine code.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip required.** Elrond produces structured priors file consumed by rocket W2.4 implementation. Round-trip smoke: priors file produced; rocket can load + parse + use per W2.4 integration pattern. Schema TBD by elrond (recommend JSON or Parquet; structured for rocket consumption).

**Suggested file location:** `reincarnated-engine/data/synergy_priors/v1_co_occurrence_priors.json` (or equivalent path per elrond canonical structure).

## Scope

### Co-occurrence prior dimensions to extract

From existing substrate corpus, extract statistical co-occurrence frequencies across these dimensions:

- [ ] **T4-strategy-pair co-occurrence** — how frequently do existing kits in substrate exhibit pairs of T4-relevant mechanics (e.g., RESOURCE_CONVERSION + DEFENSIVE_CONVERSION? ELEMENT_CONVERSION + GEOMETRY_COLLAPSE?). 6-strategy registry × 6-strategy = 36 pairs (or 21 unique ordered pairs)
- [ ] **Kit-mechanic co-occurrence** — across mechanics in `mechanics_canonical` taxonomy, which mechanics naturally co-occur in substrate (e.g., bleed + thorny + brutal_strike often together; vs ranged + tank rarely together)
- [ ] **Element-pair co-occurrence** — which element pairs co-occur (per closeout § 2.4 DUAL_ELEMENT_ADDITION: PoE "X% physical as fire"; D4 "all skills deal X% as cold" — substrate analog: physical+fire co-occurrence? wind+lightning?)
- [ ] **Scaling-axis co-occurrence** — per SC-4 expansion 5th Scaling-interaction category: which scaling axes naturally compose (e.g., crit_chance + crit_damage = true multiplicative across separate buckets; attack_speed + cast_speed = additive same-bucket trap; etc.)
- [ ] **Chain-position co-occurrence** — for class structures with chain-investment patterns (per doc 41 chain architecture), which mechanics typically anchor T4 capstone position vs T1-T3 nodes

### Output spec

- [ ] Structured file at chosen path (recommend `reincarnated-engine/data/synergy_priors/v1_co_occurrence_priors.json`):
  - Schema: per dimension, key-value pairs with co-occurrence frequencies (normalized 0.0-1.0 OR raw counts; document choice)
  - Metadata: substrate corpus size; extraction date; methodology brief
- [ ] Companion methodology note at `agentic_orchestration/elrond/notes/2026-05-27-wave-2-synergy-priors-methodology.md` documenting extraction process + caveats

### Discipline compose-check

- [ ] **#11 empirical inspection** — verify all extracted counts empirically (file + grep + Python Counter; cite verification mechanism)
- [ ] **#18 methodology** — extraction is methodology output for Wave 2 W2.4; document methodology pattern
- [ ] **AI-tell line D7** — extraction is statistical (not LLM raw-reasoning); preserves AI-tell line

## Acceptance criteria

- [ ] Structured priors file produced at agreed path
- [ ] All 5 co-occurrence dimensions extracted with empirical counts
- [ ] Methodology note authored
- [ ] Post-script empirical count assertions per dimension (Discipline #11)
- [ ] Tagged commit per elrond convention: `elrond: Cycle 13 Wave 2 statistical co-occurrence priors (rocket W2.4 dependency per AI-tell D7 + closeout § 2.5)`
- [ ] Round-trip: priors file loadable + parseable by rocket; smoke-verifiable

## Out of scope

- T4 algorithm implementation (rocket seam)
- Compositional synergy scan algorithm (rocket W2.4)
- Pattern library curation (gandalf seam per doc 43)
- LLM-based reasoning for synergy detection (D7 anti-pattern)
- Substrate corpus modifications
- Schema migrations on substrate DB
- Cycle 14+ scope

## Open questions for the agent to resolve

- Substrate corpus scope: full 2,293-item v1_scope OR subset filtered by mechanic-density / cluster representation; your seam-owner call per #11 empirical-grounding
- Normalization choice: 0.0-1.0 normalized frequencies vs raw counts; recommend normalized for rocket consumption simplicity + raw in metadata
- File format: JSON (simpler) vs Parquet (efficient for large priors); recommend JSON per size + ease of consumption
- Co-occurrence threshold: include all pairs with count ≥ N, OR include top-K per dimension; your seam call

## References

- `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` § 5 (synergy scan substrate)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-1-doc-43-critique.md` (I2 flag source)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 2.5
- `agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` Topic 2
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- `agentic_orchestration/operating-procedures/elrond.md`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#11 + #18 + D7)

---

**Cycle:** 13
**Wave:** 2 concurrent dependency (W2.4 input)
**Gates:** rocket W2.4 compositional synergy scan implementation
**Priority:** P2 — concurrent with rocket Wave 2; preferred to land during rocket W2.0-W2.3 phase

---

## Completion record — 2026-05-27 (elrond)

**Integration pattern landed:** Pattern A (priors land during rocket W2.0-W2.3; rocket reads at W2.4).

**Substrate corpus used:** engine telemetry mechanic substrate at `reincarnated-engine/data/telemetry.db` — 94 seasons, 631 class-rows, 7,066 class-abilities, 17,533 total abilities. The dispatch-referenced 2,293-item v1_scope weapon catalogue (Cycle 10) is a VISUAL/FORM-FACTOR corpus carrying no ARPG-mechanic semantics; NOT used for these priors. Seam-owner call per Discipline #18 + dispatch open-question 1.

**5-dimension extraction summary + sample sizes:**

| # | Dimension | Unique pairs | Sample kits | Top pair (raw / normalized) |
|---|---|---|---|---|
| 1 | T4-strategy-pair | 14 | 489 | `GEOMETRY_COLLAPSE\|MULTIPLIER_STRATEGY` 379 / 0.2063 |
| 2 | Kit-mechanic-pair | 128 | 692 | `damage\|shield` 642 / 0.0475 |
| 3 | Element-pair | 12 | 436 multi-element | `water\|wind` 135 / 0.1753 |
| 4 | Scaling-axis-pair | 36 | 692 | All 10,660 instances are multiplicative_across_buckets; ZERO additive_within_bucket (substrate-led finding) |
| 5 | Chain-position cross-pair | 120 directed | 167 (cd ≥ 15s heuristic; substrate ceiling 19.9s) | T4 capstone dominated by `buff_damage` 0.3368 + `silence` 0.2737 + `buff_mana_regen` 0.1553 |

**Post-script empirical assertions (Discipline #11 — all 13 PASS):**

```
[PASS] substrate.season_count == 94
[PASS] substrate.class_rows == 631
[PASS] substrate.class_abilities == 7066
[PASS] d1.normalized_freq_sums_to_1.0   | sum = 1.000000
[PASS] d1.raw_total >= sample_size_kits | pair_sum=1837; kits=489
[PASS] d2.normalized_freq_sums_to_1.0   | sum = 0.999996
[PASS] d2.kits_with_mechanics <= total_kit_count
[PASS] d3.normalized_freq_sums_to_1.0   | sum = 1.000000
[PASS] d3.multi_element_kits_matches_sql_count | python=436 sql=436
[PASS] d4.multiplicative_plus_additive_equals_raw_total | mult=10660 add=0
[PASS] d4.normalized_freq_sums_to_1.0   | sum = 1.000002
[PASS] d5.t4_capstone_dist_normalized_sums_to_1 | sum = 1.000002
[PASS] d5.normalized_freq_sums_to_1.0   | sum = 0.999993
```

**Round-trip per Principle 6:** PASS — JSON re-loadable + re-parseable; schema_version "v1.0"; 5 dimensions present.

**AI-tell line D7:** PRESERVED — zero LLM calls; zero LLM raw-reasoning; pure `collections.Counter` frequency extraction.

**Substrate-led finding flagged to gandalf via knight-rider:** D4 has zero additive-within-bucket pairs because the engine's effect-name → scaling-axis mapping is currently 1-to-1. The Pass 2 trap-detector for scaling-interaction degeneration cannot calibrate against substrate-native same-bucket examples. **Recommendation:** rocket W2.4 test coverage should inject synthetic same-bucket pairs to validate trap-detection path.

**Artifacts:**
- `reincarnated-engine/data/synergy_priors/v1_co_occurrence_priors.json` (~95 KB; rocket-consumer-ready)
- `agentic_orchestration/elrond/notes/2026-05-27-wave-2-synergy-priors-methodology.md` (methodology + extraction provenance + 5 recommended follow-ups)
- `agentic_orchestration/research/scripts/extract_synergy_co_occurrence_priors_2026_05_27.py` (reproducible extraction; idempotent re-run)

**Status:** COMPLETE.
