# T4 Strategy Applicability Research — Cascade-Resumption-3 Pre-S2 Methodology Consultation

**Date:** 2026-05-29
**Author:** gamora
**Authority:** cascade-resumption-3 dispatch `2026-05-29-gamora-cycle-14-cascade-resumption-3-t4-strategy-applicability-research.md` + Amendment 2 (parallel fan-out enabled) + Amendment 3 (Disc #48 RAM-awareness retired)
**Pattern:** Pattern A-light analytical work (~2-4h; no code modification)
**Consumed-by:** KR for S2 gauntlet variant enumeration expansion dispatch authoring

---

## 0. Disc #42a Framing-Audit at Dispatch Consumption

**Q1 — Load-bearing framing assumptions this research depends on:**
1. The 18 BC cells in `endgame_encounter_catalog.py` (post-S1 commit `99d67aa`) are the operative substrate base for S2
2. The 6 Layer 2 T4 strategies per doc 47 § 4.6.2 are: Element Conversion Variant A, Variant B, Variant C + TRADE_OFF REVERSED + GEOMETRY_COLLAPSE + RESOURCE_CONVERSION
3. TRADE_OFF REVERSED is canonically PLACEHOLDER (doc 47 § 4.6.5) but engine has `trade_off_reversed_frenzy` implemented (hit -30% / crit +30%) per `combatant.py:588-609`, Matt-locked 2026-05-28 evening late
4. "Applicable" means the strategy's mechanic has substrate match + non-trivial probability of landing in-band under strip-and-ship
5. The 3 investment profiles are low / mid / max per doc 51 Patterns 1+2 (decay=0.65 active; decay=0.50 passive)

**Q2 — Refutation evidence in hand:**
- TRADE_OFF REVERSED has a canonical-doc PLACEHOLDER status but engine `trade_off_reversed_frenzy` is implemented. This creates a vocabulary split: "TRADE_OFF REVERSED (canonical)" vs "trade_off_reversed_frenzy (engine)". For this matrix the engine implementation is the applicability basis — the strategy IS evaluable at S2.
- GEOMETRY_COLLAPSE is Category B (chain-specific per `t4_category_schema.py:24,97`), not CHARACTER_WIDE. Applicability varies by whether the kit's chains include AOE-geometry skills. BC cell range/tempo axes correlate with AOE-vs-single-target geometry expectations.
- STR/DEX attribute maps to Element Conversion Variant C (Physical Hybrid); INT/WIS attribute maps to Variant A (Mono-caster). Variant B (Hybrid Dual-Add) is a third option applicable where multi-element kit composition surfaces. This attribute-keyed routing is empirically embedded in `unified_calibration_loop.py:646-658`.

**Q3 outcome: PROCEED.** Framing is sound. TRADE_OFF REVERSED / frenzy canonical-vs-engine vocabulary gap is captured as a surface finding in § 5.

---

## 1. Per-BC-cell × T4-strategy applicability matrix (108 cells)

### 1.1 Strategy mechanics summary (reference)

| Strategy | Mechanic (engine) | Applicable-when | Strip risk |
|---|---|---|---|
| **ECA** (Element Conversion Variant A) | 1.50× multiplicative on magical damage (`ELEMENT_CONVERSION_VARIANT_A_MAGNITUDE`) | INT/WIS kit (magical-primary damage path) | Low — 1.50× is large; lands in-band for cohort-preferred encounters |
| **ECB** (Element Conversion Variant B) | 1.25× multiplicative on magical damage (`ELEMENT_CONVERSION_VARIANT_B_MAGNITUDE`) | Dual-element or multi-element kits where neither single-element nor pure-physical | Moderate — 1.25× is moderate; lands in-band for encounter types where kit has mid-level elemental output |
| **ECC** (Element Conversion Variant C) | 0.25 additive elemental on physical base (`ELEMENT_CONVERSION_VARIANT_C_MAGNITUDE`) + ailment deferred | STR/DEX kit (physical-primary damage path); adds elemental flavor channel | Moderate-high — 0.25 additive on physical base is small absolute delta; may miss in-band at encounters where mob elemental resistance is high |
| **TOR** (TRADE_OFF REVERSED — frenzy) | Hit chance -30% additive + Crit chance +30% additive (engine: `trade_off_reversed_frenzy`) | Any kit where accuracy is not at floor (accuracy > 0.30 pre-TOR); burst/spiky amplitude favors the high-crit variance profile | Moderate — high-crit variance can over- or under-perform cohort median; flat/high-tempo encounters strip more (consistency demanded); spiky encounters benefit |
| **GC** (Geometry Collapse) | AOE-geometry skills: aoe_radius × 0.5; damage_multiplier × 1.5 (engine: `combatant.py:534-556`) | Kits with AOE-geometry active skills on chains (multi-target encounters: open_arena, magic_pack, elite_pack scenarios); Category B (chain-specific) | Variable — in open-arena / pack encounters YES; single-target boss-only encounters NO |
| **RC** (Resource Conversion) | Skill cost resource = HP instead of mana (`t4_cost_resource="HP"`; `fight_engine.py:593-650`) | Any kit where HP-cost instead of mana does not kill the combatant within fight duration; STR/DEX heavy-HP kits more robust; WIS/INT kits with lower HP pool at higher risk | High at low investment (small HP pool → risk of HP drain death); Moderate-Low at max investment (HP pool large enough) |

### 1.2 BC cell reference table (18 cells)

| # | encounter_id | range | tempo | amplitude | attr | proxy | KPM profile notes |
|---|---|---|---|---|---|---|---|
| 1 | bc_melee_low_spiky_str_none | melee | low | spiky | STR | none | Burst-window boss; DPS-min-maxer risk; Defensive risk |
| 2 | bc_melee_high_flat_str_none | melee | high | flat | STR | none | Swarm sustained; all cohorts viable |
| 3 | bc_melee_medium_variable_str_none | melee | medium | variable | STR | none | Elite anchor + mixed adds; all cohorts viable |
| 4 | bc_ranged_low_spiky_str_none | ranged | low | spiky | STR | none | Choke burst; Defensive risk |
| 5 | bc_melee_high_flat_dex_none | melee | high | flat | DEX | none | High-mobility swarm; Defensive slow-clear risk |
| 6 | bc_ranged_high_flat_dex_none | ranged | high | flat | DEX | none | Sustained ranged flat; all DPS viable |
| 7 | bc_ranged_low_spiky_dex_none | ranged | low | spiky | DEX | none | Chokepoint burst; Defensive slow-clear risk |
| 8 | bc_mid_high_flat_dex_none | mid | high | flat | DEX | none | Magic leader + adds mid-range; Defensive KPM risk |
| 9 | bc_ranged_medium_variable_int_none | ranged | medium | variable | INT | none | Open swarm mid-range; all DPS viable |
| 10 | bc_ranged_low_spiky_int_none | ranged | low | spiky | INT | none | Boss + swarm spiky; DPS-min-maxer high KPM |
| 11 | bc_mid_low_spiky_int_none | mid | low | spiky | INT | none | Mid-range chokepoint-style |
| 12 | bc_melee_high_flat_int_none | melee | high | flat | INT | none | Contested STR-INT cell; all DPS viable |
| 13 | bc_ranged_medium_variable_int_light | ranged | medium | variable | INT | light | Proxy-light; Hybrid favored |
| 14 | bc_mid_medium_variable_wis_none | mid | medium | variable | WIS | none | WIS mid-range rotation; Balanced/Defensive |
| 15 | bc_melee_medium_variable_wis_none | melee | medium | variable | WIS | none | WIS melee Balanced/Defensive |
| 16 | bc_ranged_low_spiky_wis_none | ranged | low | spiky | WIS | none | Burst timing constraint; Defensive/Balanced |
| 17 | bc_ranged_medium_variable_wis_none | ranged | medium | variable | WIS | none | WIS ranged open swarm; DPS-min-maxer elemental burst |
| 18 | bc_melee_high_variable_wis_none | melee | high | variable | WIS | none | All cohorts viable; variable amplitude |

### 1.3 108-cell applicability matrix

Key: YES = substrate match + non-trivial in-band probability; PARTIAL = conditional on kit composition detail; NO = structural mismatch or near-certain strip

**STR cells (BC 1-4): physical-primary, melee/ranged, no-proxy**

| BC# | ECA | ECB | ECC | TOR | GC | RC |
|---|---|---|---|---|---|---|
| 1 melee/low/spiky/STR/none | NO | PARTIAL | YES | YES | PARTIAL | PARTIAL |
| 2 melee/high/flat/STR/none | NO | PARTIAL | YES | PARTIAL | YES | PARTIAL |
| 3 melee/medium/variable/STR/none | NO | PARTIAL | YES | PARTIAL | YES | PARTIAL |
| 4 ranged/low/spiky/STR/none | NO | PARTIAL | YES | YES | PARTIAL | PARTIAL |

**DEX cells (BC 5-8): physical-primary, melee/ranged/mid, no-proxy**

| BC# | ECA | ECB | ECC | TOR | GC | RC |
|---|---|---|---|---|---|---|
| 5 melee/high/flat/DEX/none | NO | PARTIAL | YES | PARTIAL | YES | PARTIAL |
| 6 ranged/high/flat/DEX/none | NO | PARTIAL | YES | PARTIAL | YES | PARTIAL |
| 7 ranged/low/spiky/DEX/none | NO | PARTIAL | YES | YES | PARTIAL | PARTIAL |
| 8 mid/high/flat/DEX/none | NO | PARTIAL | YES | PARTIAL | YES | PARTIAL |

**INT cells (BC 9-13): magical-primary, ranged/mid/melee, no-proxy + 1 proxy-light**

| BC# | ECA | ECB | ECC | TOR | GC | RC |
|---|---|---|---|---|---|---|
| 9 ranged/medium/variable/INT/none | YES | PARTIAL | NO | PARTIAL | YES | PARTIAL |
| 10 ranged/low/spiky/INT/none | YES | PARTIAL | NO | YES | PARTIAL | PARTIAL |
| 11 mid/low/spiky/INT/none | YES | PARTIAL | NO | YES | YES | PARTIAL |
| 12 melee/high/flat/INT/none | YES | PARTIAL | NO | PARTIAL | YES | PARTIAL |
| 13 ranged/medium/variable/INT/light | YES | YES | NO | PARTIAL | YES | YES |

**WIS cells (BC 14-18): magical-primary, mid/melee/ranged, no-proxy**

| BC# | ECA | ECB | ECC | TOR | GC | RC |
|---|---|---|---|---|---|---|
| 14 mid/medium/variable/WIS/none | YES | PARTIAL | NO | PARTIAL | YES | PARTIAL |
| 15 melee/medium/variable/WIS/none | YES | PARTIAL | NO | PARTIAL | YES | PARTIAL |
| 16 ranged/low/spiky/WIS/none | YES | PARTIAL | NO | YES | PARTIAL | PARTIAL |
| 17 ranged/medium/variable/WIS/none | YES | YES | NO | PARTIAL | YES | PARTIAL |
| 18 melee/high/variable/WIS/none | YES | PARTIAL | NO | PARTIAL | YES | PARTIAL |

### 1.4 Per-cell reasoning summary

**ECA (Element Conversion Variant A — 1.50× magical)**
- YES for all INT/WIS cells (BC 9-18): the 1.50× multiplicative on magical damage path is the canonical INT/WIS assignment per `unified_calibration_loop.py:657`. Substrate match is exact (magical-primary damage path). Strip risk is LOW — the 1.50× magnitude was empirically validated at Phase 4 RE-RUN-5 (BVV compound_pass=True across all 7 profiles).
- NO for all STR/DEX cells (BC 1-8): physical-primary kits route to ECC not ECA. Applying ECA to physical-primary kit applies the 1.50× multiplicative to near-zero magical output — effective magnitude approaches 0, structurally unable to produce in-band cell. Structural NO.

**ECB (Element Conversion Variant B — 1.25× magical, dual-element)**
- YES for BC 13 (INT/proxy-light) and BC 17 (WIS/ranged/variable): the proxy-light cell and open-swarm variable cell have the widest kit-composition diversity. Multi-element substrate sampling (post-S7) may surface dual-element INT/WIS kits where neither ECA (pure-mono) nor ECC (pure-physical) is the exact fit. ECB applies where the kit has secondary magical element channels.
- PARTIAL for all remaining INT/WIS cells (BC 9-12, 14-16, 18): ECB is applicable IF the kit's substrate produces a dual-element composition. At 1-substrate-sample (pre-S7), most INT/WIS kits will be single-element and ECA is the stronger fit. Post-S7 multi-sample increases the ECB-applicable fraction. "PARTIAL" = depends on substrate sample outcome, not structurally excluded.
- PARTIAL for all STR/DEX cells (BC 1-8): ECB on physical-primary kits applies 1.25× to the magical channel. For kits with a modest magical secondary (e.g., DEX/mid kits with a magical off-chain), ECB may produce a partial in-band contribution. Low probability but not structurally zero. Strip probability HIGH for pure-physical kits.

**ECC (Element Conversion Variant C — 0.25 additive elemental on physical base)**
- YES for all STR/DEX cells (BC 1-8): the 0.25 additive elemental on physical base is the canonical STR/DEX assignment per `unified_calibration_loop.py:654`. Strip risk is MODERATE — the 0.25 additive is small in absolute terms, but Phase 4 RE-RUN-5 confirmed compound_pass=True at max investment for these cells. At low investment (Pattern 1: 35% of max), the ECC additive becomes very small — sub-floor risk at low-invest.
- NO for all INT/WIS cells (BC 9-18): magical-primary kits have near-zero physical base. The 0.25 additive on near-zero physical = near-zero absolute bonus. Structurally unable to produce in-band contribution. Structural NO.

**TOR (TRADE_OFF REVERSED — frenzy: hit -30% / crit +30%)**

IMPORTANT ENGINE FINDING: canonical doc 47 § 4.6.5 marks TRADE_OFF REVERSED as "PLACEHOLDER" but `combatant.py:588-609` has `trade_off_reversed_frenzy` implemented with Matt-locked parameters (hit -30% / crit +30%) per `damage_resolver.py:270-271`. The mechanic IS evaluable at S2. The canonical vocabulary gap (doc says PLACEHOLDER; engine has implementation) is surfaced to KR in § 5.

- YES for cells where spiky-amplitude and low-tempo create burst-window context: BC 1 (melee/low/spiky/STR), BC 4 (ranged/low/spiky/STR), BC 7 (ranged/low/spiky/DEX), BC 10 (ranged/low/spiky/INT), BC 11 (mid/low/spiky/INT), BC 16 (ranged/low/spiky/WIS). Spiky amplitude favors high-crit variance — the TOR frenzy mechanic produces large burst when crits land, matching the encounter's expected damage distribution.
- PARTIAL for flat/variable amplitude cells: TOR frenzy produces variance. Flat amplitude encounters (BC 2, 5, 6, 8, 12) demand consistent sustained output — TOR frenzy may over- or under-perform depending on crit-roll distribution. Not structurally excluded but band-landing probability lower than in spiky encounters.
- PARTIAL for medium/variable tempo cells: similar reasoning. Variable amplitude with medium tempo (BC 3, 9, 14, 15, 17, 18) allows some crit-burst absorption but TOR frenzy remains a variance-amplifier that may miss band.

**GC (Geometry Collapse — AOE radius × 0.5 / damage_multiplier × 1.5 for AOE skills)**

GC is Category B (chain-specific). Applicability depends on whether the kit's chains include AOE-geometry skills. BC axis range/tempo correlate with expected geometry:
- YES for multi-target encounter contexts: BC 2 (high/flat/STR swarm), BC 3 (medium/variable/STR elite+adds), BC 5 (high/flat/DEX swarm), BC 6 (high/flat/DEX sustained ranged), BC 8 (high/flat/DEX magic leader+adds), BC 9 (medium/variable/INT open swarm), BC 11 (mid/low/spiky/INT), BC 12 (high/flat/INT), BC 13 (INT/proxy-light), BC 14 (medium/variable/WIS mid), BC 15 (medium/variable/WIS melee), BC 17 (medium/variable/WIS ranged), BC 18 (high/variable/WIS melee). Multi-mob encounters with AOE-geometry kits: GC's 1.5× damage_multiplier on AOE skills compensates for the radius reduction — in tight-pack encounters (melee swarm, chokepoint, open arena) the reduced radius may still hit 2+ mobs at 1.5× each, net positive.
- PARTIAL for single-target or ambiguous contexts: BC 1 (boss/spiky/STR — single-target boss is primary; GC applies only if kit has AOE chain), BC 4 (ranged/choke/STR), BC 7 (ranged/spiky/DEX), BC 10 (spiky/INT — boss+swarm context may not benefit from radius reduction), BC 16 (low/spiky/WIS). These have mixed single-target and multi-target elements; GC strips if the primary kill target is the boss (single-target) not the adds.

**RC (Resource Conversion — HP cost instead of mana)**

RC's in-band probability is determined by HP pool relative to skill cost rate across fight duration.
- YES for BC 13 (INT/proxy-light/light): the proxy-light cell has the broadest kit diversity including Hybrid cohort, and the proxy familiar may provide HP sustain. RC is viable when HP sustain channels exist in the kit.
- PARTIAL for all remaining cells: RC is structurally applicable (engine wires HP-cost branch regardless of BC cell), but in-band probability depends heavily on investment profile. At max investment, HP pool is sufficient for most kits across most encounter types. At low investment, HP pool is smaller and RC risk of HP-drain death or unsustainable cost is higher. STR/DEX kits (BC 1-8) have higher HP pools per attribute profile → RC more viable than INT/WIS kits (BC 9-18) with smaller HP pools. "PARTIAL" across the board captures this uncertainty; INT/WIS cells have higher strip probability than STR/DEX cells.

---

## 2. Methodology notes for S2 dispatch authoring

### 2.1 Variant cycling axes priority (per gandalf authorization § 3 line 227 pre-ratified)

**Axis 1 (T4 strategy):** cycle through 6 Layer 2 strategies per BC cell. 5 of 6 are evaluable immediately (ECA + ECB + ECC + TOR-frenzy + GC). RC is evaluable. TOR canonical-vs-engine vocabulary gap is resolved by the engine: use `trade_off_reversed_frenzy` key in alteration_fields.

**Axis 2 (investment profile):** cycle through low / mid / max per doc 51 Patterns 1+2. 3 profiles. All 3 are straightforward — the Pattern 1 formula (decay=0.65) and Pattern 2 formula (decay=0.50) parameterize each profile deterministically.

**Axis 3 (skill tree variant / substrate sample):** conditional on S7 output. With S7 delivering N=3 substrate samples per BC cell (54+ kits total), "skill tree variant" becomes "which of the N substrate-sampled kits for this BC cell." S7 multi-sample is the load-bearing source of within-BC-cell variant diversity; separate within-kit skill-composition cycling is a Cycle 15+ scope extension.

**Effective axis priority rationale:** T4 strategy first because it is the dimension with highest expected variant cardinality uplift per BC cell (6 strategies × 18 cells = 108 Layer 2 evaluations). Investment profile second because it is fixed at 3 levels — straightforward enumeration. Substrate sample variant third because it depends on S7 completion.

### 2.2 The ENUMERATE-vs-PRE-FILTER decision

**Option A — Enumerate-all-and-strip:** generate (18 BC × 6 T4 strategies × 3 invest) = 324 evaluation cells. Run gauntlet on all 324. Strip cells that miss in-band per § 10.8. Ship the survivors.

Pros: honest empirical strip signal; no analytical pre-filter error; full Cycle 14 v1 empirical data for Cycle 15 design-call inheritance. Cons: ~324 evaluation cells (vs current ~18); wall-time increase significant (~18×).

**Option B — Pre-filter-and-enumerate-survivors:** apply the applicability matrix (this research) as a pre-filter. Only enumerate YES + PARTIAL cells. Estimated eligible cells: 18 × (ECA: 10 YES + 8 PARTIAL) + (ECB: 2 YES + 16 PARTIAL) + (ECC: 8 YES + 0) + (TOR: 6 YES + 12 PARTIAL) + (GC: 13 YES + 5 PARTIAL) + (RC: 1 YES + 17 PARTIAL). Roughly 18 YES + 76 PARTIAL = ~94 cells pre-filtered to ~80 active evaluations (YES always; PARTIAL at gamora discretion).

Pros: faster; focuses gauntlet on high-signal cells; avoids known-NO cells (e.g., ECA on STR kits). Cons: pre-filter error if analytical applicability judgment is wrong; loses honest NO-cell empirical signal.

**Recommendation (§ 6 elaborates):** PARTIAL enumerate — enumerate all YES cells + PARTIAL cells; skip only structural NO cells (ECA on STR/DEX; ECC on INT/WIS). Structural NOs are provably non-contributory (zero-magnitude on primary damage path). PARTIAL cells carry uncertainty worth resolving empirically — strip signal from PARTIAL cells is valuable Cycle 15 design input. This eliminates 8 known-NO ECA cells + 9 known-NO ECC cells = 17 cells, reducing 324 to ~307 evaluations. The computational saving is modest but the analytical clarity is high.

**This is a methodology multi-option surface per § 5 / Disc #18.** KR should route to gandalf for design-spec-as-math handoff if the choice between Option A, B, and PARTIAL-enumerate has architectural implications beyond gamora seam discretion.

### 2.3 Strip-and-ship interaction with S2 variant rows

Per doc 51 § 10.8.9 two-layer architecture: Primary T4 (DIRECT_DAMAGE_AMP) is exempt from strip-and-ship, guaranteed in-band universally. Layer 2 strategies apply strip-and-ship per § 10.8.1. Under S2 variant enumeration:

- Each (BC × T4_strategy × investment_profile) tuple is one gauntlet evaluation cell
- The cell's BVV result (compound_pass or per-target breakdown) determines strip-or-ship disposition
- A cell that strips does NOT reduce the kit's ship status (Primary T4 guarantees ship)
- The S2 output is the set of (BC × T4_strategy × invest) tuples that land in-band — the "shipped Layer 2 variant population"
- ≥22 unique kit-variant rows target counts both shipped and stripped — the target is for the ENUMERATED variant population, not the shipped-only population

### 2.4 Investment-profile per-strategy interaction

| Strategy | Low invest | Mid invest | Max invest |
|---|---|---|---|
| ECA | PARTIAL — 1.50× on smaller magical base; may land under-band at low invest | YES — 1.50× on mid magical base; likely in-band for preferred enc types | YES — empirically validated at Phase A1 RE-RUN-5 |
| ECB | LOW — 1.25× on smaller base; near-NO at low invest | PARTIAL — depends on dual-element exposure | YES — in-band at max invest for dual-element kits |
| ECC | LOW — 0.25 additive on 35% Pattern 1 floor = very small; likely strip | PARTIAL — 0.25 additive on ~60-70% base; marginal | PARTIAL — 0.25 additive on full base; Phase 4 confirmed for some cells |
| TOR | PARTIAL — hit -30% at low accuracy is high-risk; crit +30% less impactful at low base-crit | PARTIAL — moderate accuracy reduction absorbed; crit boost effective | PARTIAL — full accuracy headroom absorbs -30%; crit +30% at high base-crit is significant burst |
| GC | PARTIAL — 1.5× on lower base damage; may land in-band for multi-mob encounters | PARTIAL-YES — 1.5× at mid invest; good for open-arena swarm encounters | YES for AOE-primary kits in multi-mob encounters |
| RC | NO-LOW — small HP pool; HP-cost risk of drain death | PARTIAL — HP pool grows; risk lower; still encounter-dependent | PARTIAL-YES — large HP pool absorbs cost; most encounter types viable |

### 2.5 Cohort_archetype interaction

| Strategy | DPS-min-maxer | Balanced | Defensive | Hybrid |
|---|---|---|---|---|
| ECA | STRONG — mono-cast max output; 1.50× aligns with KPM-peak archetype | GOOD | NEUTRAL — Defensive cohort may not use magical primary | GOOD for Hybrid with magical channel |
| ECB | GOOD for multi-element DPS-min-maxer | STRONG — dual coverage aligns with Balanced multi-threat | NEUTRAL | STRONG for Hybrid |
| ECC | STRONG for physical DPS-min-maxer | GOOD | GOOD — additive elemental on physical preserves defensive playstyle | GOOD |
| TOR | STRONG at spiky amplitude — max crit burst aligns with DPS-min-maxer burst philosophy | NEUTRAL — crit variance inconsistent with Balanced | WEAK — hit reduction is dangerous for Defensive survivability; stat drain is antithetical | PARTIAL — depends on HP sustain |
| GC | STRONG for AOE DPS-min-maxer in multi-mob | STRONG | PARTIAL — reduced radius may cause misses reducing KPM | GOOD |
| RC | PARTIAL — HP cost for max output is DPS-min-maxer tradeoff | PARTIAL | WEAK — HP cost is antithetical to Defensive survivability | GOOD — Hybrid HP sustain channels offset cost |

---

## 3. Strip-and-ship disposition predictions per cell

Predicted strip frequency (H=High strip likelihood; M=Moderate; L=Low):

| BC# | ECA | ECB | ECC | TOR | GC | RC |
|---|---|---|---|---|---|---|
| 1 STR/melee/low/spiky | STRIP (structural) | H | L-M | L (spiky favors) | H (boss single-target) | M |
| 2 STR/melee/high/flat | STRIP (structural) | H | M | M-H (flat demands consistent) | L (swarm; AOE kits) | M |
| 3 STR/melee/med/var | STRIP (structural) | H | M | M | L (elite+adds multi) | M |
| 4 STR/ranged/low/spiky | STRIP (structural) | H | L-M | L (spiky favors) | H (choke; single-target heavy) | M |
| 5 DEX/melee/high/flat | STRIP (structural) | H | M | M-H | L (swarm; AOE kits) | M |
| 6 DEX/ranged/high/flat | STRIP (structural) | H | M | M-H | L (bottleneck mobs) | M |
| 7 DEX/ranged/low/spiky | STRIP (structural) | H | L-M | L (spiky favors) | H (single-target heavy) | M |
| 8 DEX/mid/high/flat | STRIP (structural) | H | M | M-H | M (leader+adds; AOE moderate) | M |
| 9 INT/ranged/med/var | L | M | STRIP (structural) | M | L (open swarm; AOE) | M-H |
| 10 INT/ranged/low/spiky | L | M | STRIP (structural) | L (spiky favors) | H (boss+swarm; boss is primary) | M-H |
| 11 INT/mid/low/spiky | L | M | STRIP (structural) | L | L-M | M-H |
| 12 INT/melee/high/flat | L | M | STRIP (structural) | M-H | L (swarm; AOE) | M-H |
| 13 INT/ranged/med/var/light | L | L | STRIP (structural) | M | L | L |
| 14 WIS/mid/med/var | L | M | STRIP (structural) | M | L | M-H |
| 15 WIS/melee/med/var | L | M | STRIP (structural) | M | L | M-H |
| 16 WIS/ranged/low/spiky | L | M | STRIP (structural) | L (spiky favors) | H (spiky; single-target heavy) | M-H |
| 17 WIS/ranged/med/var | L | L | STRIP (structural) | M | L | M-H |
| 18 WIS/melee/high/var | L | M | STRIP (structural) | M | L | M-H |

**Summary of high-confidence strips:**
- ECA on STR/DEX cells (BC 1-8): 8 structural strips (100%)
- ECC on INT/WIS cells (BC 9-18): 10 structural strips (100%)
- GC on low/spiky single-target-heavy cells: BC 1, 4, 7, 10, 16 — H strip (5 cells)
- RC on INT/WIS cells at low/mid invest: H strip probability across 10 cells at low invest

**High-confidence ships:**
- ECA on INT/WIS cells at max invest: 10 cells — L strip = HIGH ship
- ECC on STR/DEX at max invest: 8 cells — L-M strip = MODERATE-HIGH ship
- GC on multi-mob/swarm cells (BC 2, 3, 5, 6, 9, 12, 14, 15, 17, 18): L strip = HIGH ship
- TOR on spiky-amplitude cells (BC 1, 4, 7, 10, 11, 16): L strip = HIGH ship

---

## 4. Variant cardinality estimate

### 4.1 Base cardinality (18 BC × 6 strategies × 3 invest)

Full enumeration: 18 × 6 × 3 = **324 cells**

### 4.2 With structural NO pre-filter (recommended)

Structural NOs to exclude: ECA on BC 1-8 (8 cells × 3 invest = 24) + ECC on BC 9-18 (10 cells × 3 invest = 30) = 54 structural NO cells.

Post-filter: 324 - 54 = **270 cells**

### 4.3 With investment profile collapsing at low (RC/ECC low-invest near-certain strip)

If low-invest is dropped for RC across INT/WIS cells (10 × 1 = 10) and ECC low-invest for STR/DEX (8 × 1 = 8) the further reduction is 18 cells → **252 cells**.

However, the recommendation is NOT to drop these — the empirical strip signal at low invest for RC and ECC is valuable Cycle 15 input. Enumerate them, let strip-and-ship produce the data.

### 4.4 Post-S7 multi-sample multiplier

S7 delivers N=3 substrate samples per BC cell. If S2 cycles T4 strategy × invest per substrate-sample (each of the 54 kits gets the T4 × invest treatment): 54 kits × 6 strategies × 3 invest = **972 cells**.

This is almost certainly too broad for a single gauntlet run. The recommended S2 scoping is one representative substrate sample per BC cell for the T4 × invest sweep, with multi-sample diversity exercised at the PM-1 clustering layer (which uses the substrate-diverse kit population as its input). This maintains the ≥22 unique-kit-variant-rows target while keeping gauntlet wall-time tractable.

### 4.5 Effective variant cardinality meeting ≥22 target

With 18 BC cells × 6 T4 strategies (- 2 structural NO categories) × 3 invest = **270 evaluations**. Post-strip, anticipated shipped variants:

- ECA: ~10 YES × 3 invest = 30 shipped
- ECB: ~2 YES + ~8 high-PARTIAL × 3 invest = ~30 candidates (assume 50% ship = 15 shipped)
- ECC: ~8 YES × 3 invest = 24 shipped (low invest likely strips → ~16 shipped)
- TOR: ~6 YES + ~9 PARTIAL × 3 invest = ~45 candidates (assume 60% ship = 27 shipped)
- GC: ~13 YES × 3 invest = 39 shipped
- RC: ~1 YES + ~10 PARTIAL × 3 invest = ~33 candidates (assume 30% ship at all-invest = ~10 shipped)

**Total projected shipped variants: ~102-132** depending on strip outcomes. This is well above the ≥22 target.

Even at the pessimistic end (all PARTIAL cells strip, only YES cells ship), the shipped count is:
- ECA 10×3=30 + ECC 8×2=16 (drop low) + TOR 6×3=18 + GC 13×3=39 = **103 minimum shipped from YES cells at all-invest for non-strip-risky strategies**

The ≥22 target is structurally satisfied. No surface to KR required on cardinality grounds.

---

## 5. Disc #18 surface conditions

### 5.1 METHODOLOGY MULTI-OPTION (Disc #18 surface)

The ENUMERATE-vs-PRE-FILTER decision (§ 2.2 Option A vs B vs PARTIAL-enumerate) has three viable methodologies. Gamora recommendation is PARTIAL-enumerate (skip structural NOs; enumerate PARTIAL and YES). The decision has architectural implications:

- **Option A (enumerate all 324):** maximally honest empirical data; highest wall-time cost; definitive strip-signal for Cycle 15 design calls
- **Option B (pre-filter to ~80-94 cells):** fastest; relies on this applicability matrix being correct; risks missing unexpected PARTIAL-to-ship outcomes
- **Option C / PARTIAL-enumerate (skip 54 structural NOs; enumerate ~270):** compromise; maintains empirical honesty on PARTIAL cells; eliminates only provably-zero-magnitude cells

**Surface to KR:** this is a Disc #18 methodology multi-option choice. KR routes to gandalf for design-spec-as-math handoff OR makes the call per pre-ratified contingent decisions (gandalf authorization § 3 "T4 strategy first; investment profile second" is the axis-priority pre-ratification, not the ENUMERATE-vs-PRE-FILTER choice). Gamora recommendation: PARTIAL-enumerate (Option C). Wall-time estimate: ~270 cells vs ~18 current = ~15× wall-time increase. With smoke-mode available, this is tractable. Refer to KR.

### 5.2 TRADE_OFF REVERSED canonical-vs-engine vocabulary gap (architectural surface)

Doc 47 § 4.6.5 marks TRADE_OFF REVERSED as "PLACEHOLDER — specific mechanic in design-ambiguity state at v1.2 authoring time." Engine `combatant.py:588-609` has `trade_off_reversed_frenzy` implemented with Matt-locked parameters (hit -30% / crit +30%, PoE Frenzy precedent). This is a canonical-vs-implementation gap per Disc #42a Instance 6 pattern.

**Implication for S2:** S2 can enumerate `trade_off_reversed_frenzy` as the TOR mechanic. The implementation IS the canonical mechanic by virtue of being Matt-locked. The canonical doc gap should be updated by gandalf to reflect the locked mechanic — this is a routine framing-capture amendment, not a design escalation. Surfaced to KR for routing to gandalf doc amendment (low priority; does not block S2).

### 5.3 Cardinality above ≥22 target — no escalation required

The ≥22 target (per gandalf authorization line 199) is structurally satisfied at even the most conservative cardinality estimate (§ 4.5). No surface required.

---

## 6. S2 dispatch authoring recommendations to knight-rider

### 6.1 Recommended S2 scope

**Gauntlet variant enumeration expansion scope for S2:**
1. For each of 18 BC cells, enumerate the following T4 strategy × investment profile combinations per the applicability matrix:
   - **ECA (YES cells):** BC 9-18 (10 cells) × low/mid/max = 30 evaluations
   - **ECB (YES + PARTIAL cells):** all 18 BC × low/mid/max = 54 evaluations (let strip-and-ship winnow PARTIAL)
   - **ECC (YES cells):** BC 1-8 (8 cells) × low/mid/max = 24 evaluations
   - **TOR (YES + PARTIAL cells):** all 18 BC × low/mid/max = 54 evaluations
   - **GC (YES + PARTIAL cells):** all 18 BC × low/mid/max = 54 evaluations
   - **RC (YES + PARTIAL cells):** all 18 BC × low/mid/max = 54 evaluations
   - Skip structural NOs: ECA on BC 1-8 (24 skip) + ECC on BC 9-18 (30 skip)
   - **Total: 270 evaluation cells**

2. Each evaluation cell runs the gauntlet under the specified T4 alteration_fields and investment-profile parameterization. BVV compound_pass per cell. Strip-and-ship per § 10.8.9.

3. Output: kit_results with ≥22 unique (BC × T4_strategy × invest) rows in the shipped set. Structural NO cells not enumerated; their strip is implicit.

### 6.2 alteration_fields key mapping for S2

S2 dispatch must specify alteration_fields for each T4 strategy variant. Confirmed engine-operative keys:
- ECA: `{"element_conversion": {"target_element": "<kit_element>", "scope": "all_damage", "variant": "A"}}`
- ECB: `{"element_conversion": {"target_element": "<kit_element>", "scope": "all_damage", "variant": "B"}}`
- ECC: `{"element_conversion": {"target_element": "<kit_element>", "scope": "all_damage", "variant": "C"}}`
- TOR-frenzy: `{"trade_off_reversed_frenzy": {"hit_reduction": 0.30, "crit_boost": 0.30}}`
- GC: `{"geometry_collapse": {"damage_multiplier_bonus": 1.5}}`
- RC: `{"resource_conversion": {"cost_resource": "HP"}}`
- Primary T4 (DIRECT_DAMAGE_AMP): `{"direct_damage_amplification": {"preferred_encounter_type": "<enc_id>"}}`

Note: Primary T4 should be active for ALL cells (it's universal per § 4.6.1). Layer 2 strategies compose WITH the Primary T4, not instead of it.

### 6.3 Investment profile parameterization

Per doc 51 Patterns 1+2:
- **low:** Pattern 1 active = 0.35 × base_at_max (points=0 equivalent); Pattern 2 passive = 0.50 × base_at_max (points=0 equivalent)
- **mid:** Pattern 1 active = 0.67 × base_at_max (~7-8 points); Pattern 2 passive = 0.75 × base_at_max (~2-3 points)
- **max:** Pattern 1 active = 1.00 × base_at_max (15/15); Pattern 2 passive = 1.00 × base_at_max (5/5)

These are the doc 51 §§ 3+4 formulas with decay=0.65 (active) and decay=0.50 (passive) at the respective point fractions.

### 6.4 Recommended dispatch structure for S2

S2 dispatch should specify:
- Owner: rocket + gamora (gauntlet expansion is gamora seam; kit-generation substrate is rocket seam)
- Dependency: S7 CLOSED (substrate-diverse base required per authorization; 54+ kits from multi-sample)
- Scope: gauntlet cycling infrastructure extension (Phase 4 sweep dimension expansion) to cycle T4 strategy and investment profile as variant axes
- Acceptance: gauntlet emits ≥22 unique (BC × T4_strategy × invest) shipped rows in kit_results; no reduction to 18-base
- Architecture guard: Primary T4 always active; Layer 2 strategies compose on top; strip-and-ship per § 10.8.9
- ENUMERATE-vs-PRE-FILTER: per KR routing (§ 5.1 Disc #18 surface); gamora recommendation = PARTIAL-enumerate Option C

### 6.5 Key open question for KR routing (Disc #18)

**Should S2 enumerate-all-and-strip (324 cells) OR partial-enumerate (270 cells with structural NOs excluded)?**

Gamora recommendation: PARTIAL-enumerate (270). Rationale: structural NOs are provably zero-magnitude (ECA on physical-primary kits; ECC on magical-primary kits). Enumerating them produces zero strip-signal insight — the strip outcome is mathematically determined. Excluding them is not pre-filter error; it is application of the damage-path architecture. All PARTIAL cells should be enumerated — their strip/ship outcomes are genuine empirical data.

KR routes this to gandalf or decides per pre-ratified authorization scope. Does NOT require Matt escalation per seam-owner hive-mind decision-routing authority unless gandalf raises architectural concern.

---

## 7. Acceptance gate verification (per dispatch § 3)

- [x] § 2.3 output document authored at `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-t4-strategy-applicability-research.md` — DONE
- [x] 108-cell applicability matrix populated — §§ 1.3 + 1.4 cover all 18 BC × 6 strategies = 108 cells
- [x] Methodology notes + cardinality estimate — §§ 2 + 4
- [x] KR consumption-ready — § 6 concrete S2 dispatch authoring recommendations

---

## 8. Disc #42a framing-audit output record

- Q1 load-bearing assumptions identified: 5 (§ 0 above)
- Q2 refutation evidence: TRADE_OFF REVERSED canonical-vs-engine gap surfaced; ECA/ECC attribute-keyed routing confirmed empirically
- Q3 outcome: PROCEED — no framing-refusal trigger; vocabulary gap is a doc amendment item, not a blocking architectural issue
